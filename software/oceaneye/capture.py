"""Where frames come from — and the only place that knows about hardware.

Swap the camera, the laptop, or the whole rig, and this is the file that absorbs it.
Everything downstream just receives BGR numpy frames.

Supported sources, all through the same interface:
    "0", "1", ...      USB / UVC camera by index
    "clip.mp4"         a recorded video file
    "photo.jpg"        a single image (held on screen, not flashed)
    "frames/"          a folder of images, played in filename order
    "rtsp://..."       network camera, or a phone streaming app
    "synthetic"        a generated underwater scene - no hardware needed at all
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

from . import vision

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}

# Profile control name -> OpenCV property. The two auto_* flags are handled
# separately because their values are driver-dependent, not plain numbers.
_CONTROL_PROPS = {
    "exposure": cv2.CAP_PROP_EXPOSURE,
    "white_balance": cv2.CAP_PROP_WB_TEMPERATURE,
    "gain": cv2.CAP_PROP_GAIN,
    "focus": cv2.CAP_PROP_FOCUS,
    "brightness": cv2.CAP_PROP_BRIGHTNESS,
    "contrast": cv2.CAP_PROP_CONTRAST,
}


def classify(raw: str):
    """Return (kind, value). kind is one of: synthetic, camera, url, images, image, video."""
    raw = str(raw).strip()
    if raw.lower() in {"synthetic", "sim", "demo"}:
        return "synthetic", None
    if raw.isdigit():
        return "camera", int(raw)
    if "://" in raw:
        return "url", raw

    path = Path(raw)
    if path.is_dir():
        files = sorted(p for p in path.iterdir() if p.suffix.lower() in IMAGE_SUFFIXES)
        if not files:
            raise SystemExit(f"[OceanEye] ERROR: no images in folder: {raw}")
        return "images", files
    if not path.exists():
        raise SystemExit(f"[OceanEye] ERROR: source not found: {raw}")
    if path.suffix.lower() in IMAGE_SUFFIXES:
        return "image", str(path)
    return "video", str(path)


# ---------------------------------------------------------------------------
# Synthetic scene - lets the entire system be built and rehearsed with no camera
# ---------------------------------------------------------------------------


class SyntheticScene:
    """A fake underwater tank: four drifting creatures, gradient backdrop, sensor noise.

    Not a simulation of anything real. Its job is to exercise every downstream stage
    - detection, tracking, counting, logging, recording - while the hardware is still
    in a shop. The colours match vision.SPECIES_COLOURS so the mock detector can find
    them without a trained model.
    """

    def __init__(self, width=1280, height=720, seed=22):
        self.w, self.h = width, height
        rng = np.random.default_rng(seed)
        self.t = 0
        self.creatures = []
        for i, (name, colour) in enumerate(vision.SPECIES_COLOURS.items()):
            self.creatures.append({
                "name": name,
                "colour": colour,
                "radius": int(rng.integers(26, 46)),
                "cx": float(rng.integers(150, max(160, width - 150))),
                "cy": float(rng.integers(120, max(130, height - 120))),
                "phase": float(rng.random() * 6.28),
                "speed": 0.6 + 0.5 * i,
            })
        self._backdrop = self._make_backdrop()
        # Pre-rolled sensor noise, cycled per frame. Generating 2.7M gaussian
        # samples every frame cost 170 ms and made the HUD read a fake 5 fps.
        self._noise = [rng.normal(0, 4, (height, width, 3)).astype(np.float32)
                       for _ in range(8)]

    def _make_backdrop(self):
        """Blue-green vertical gradient, darker at the top, like a lit tank."""
        grad = np.linspace(0.35, 1.0, self.h, dtype=np.float32)[:, None]
        base = np.zeros((self.h, self.w, 3), dtype=np.float32)
        base[:, :, 0] = 120 * grad     # B
        base[:, :, 1] = 105 * grad     # G
        base[:, :, 2] = 55 * grad      # R  (water eats red)
        return base

    def read(self):
        frame = self._backdrop.copy()
        self.t += 1

        for c in self.creatures:
            c["cx"] += c["speed"] * np.cos(self.t * 0.01 + c["phase"])
            c["cy"] += c["speed"] * 0.6 * np.sin(self.t * 0.013 + c["phase"])
            c["cx"] = float(np.clip(c["cx"], c["radius"] + 5, self.w - c["radius"] - 5))
            c["cy"] = float(np.clip(c["cy"], c["radius"] + 5, self.h - c["radius"] - 5))
            cv2.circle(frame, (int(c["cx"]), int(c["cy"])), c["radius"],
                       [float(v) for v in c["colour"]], -1)

        frame += self._noise[self.t % len(self._noise)]
        return True, np.clip(frame, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------------------
# The one capture object the rest of the system talks to
# ---------------------------------------------------------------------------


class Capture:
    def __init__(self, cfg_capture: dict):
        self.cfg = cfg_capture
        self.kind, self.value = classify(cfg_capture["source"])
        self.flip_mode = cfg_capture.get("flip", "")
        self.is_still = self.kind == "image"
        self._images = []
        self._index = 0
        self._cap = None
        self._scene = None
        self.settings = {}
        self._open()

    # -- opening ------------------------------------------------------------

    def _backend_flag(self):
        wanted = self.cfg.get("backend", "auto")
        if wanted == "v4l2":
            return cv2.CAP_V4L2
        if wanted == "auto" and sys.platform.startswith("linux") and self.kind == "camera":
            return cv2.CAP_V4L2          # far more reliable than the default on Linux
        return cv2.CAP_ANY

    def _open(self):
        if self.kind == "synthetic":
            self._scene = SyntheticScene(self.cfg["width"], self.cfg["height"])
            self.settings = {"source": "synthetic", "width": self.cfg["width"],
                             "height": self.cfg["height"], "fps": self.cfg["fps"]}
            return

        if self.kind == "images":
            self._images = [str(p) for p in self.value]
            self.settings = {"source": "images", "count": len(self._images)}
            return

        target = self.value if self.kind == "camera" else str(self.value)
        self._cap = cv2.VideoCapture(target, self._backend_flag())
        if not self._cap.isOpened():
            raise SystemExit(
                f"[OceanEye] ERROR: could not open source: {self.cfg['source']}\n"
                f"           try --list-cameras, or a different index (0/1/2)."
            )
        if self.kind == "camera":
            self.settings = self._apply_camera_settings()
            self._warmup()
        else:
            self.settings = self._read_back()

    # -- device settings ----------------------------------------------------

    def _apply_camera_settings(self) -> dict:
        """Ask the camera for the settings we want, then check what it actually did.

        set() silently fails on a lot of UVC drivers, which is why every value is
        read back. FOURCC is set first on purpose: many cameras default to raw YUYV
        and cap 1080p at ~5 fps, and changing the codec afterwards resets the size.
        """
        cap, cfg = self._cap, self.cfg
        fourcc = cfg.get("fourcc") or "MJPG"
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*fourcc))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, cfg["width"])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cfg["height"])
        cap.set(cv2.CAP_PROP_FPS, cfg["fps"])

        controls = cfg.get("controls", {})
        # 0.25 = manual, 0.75 = auto on most V4L2 drivers. Driver-dependent and ugly;
        # if it does not take, the v4l2-ctl path below is the reliable one.
        if "auto_exposure" in controls:
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75 if controls["auto_exposure"] else 0.25)
        if "auto_white_balance" in controls:
            cap.set(cv2.CAP_PROP_AUTO_WB, 1 if controls["auto_white_balance"] else 0)
        for name, prop in _CONTROL_PROPS.items():
            value = controls.get(name)
            if value is not None and value >= 0:
                cap.set(prop, float(value))

        self.v4l2_lock()
        return self._read_back()

    def _read_back(self) -> dict:
        cap = self._cap
        code = int(cap.get(cv2.CAP_PROP_FOURCC))
        actual = {
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "fps": round(cap.get(cv2.CAP_PROP_FPS), 1),
            "fourcc": "".join(chr((code >> (8 * i)) & 0xFF) for i in range(4)).strip() or "?",
        }
        if self.kind == "camera":
            for name, prop in _CONTROL_PROPS.items():
                actual[name] = round(cap.get(prop), 2)
        return actual

    def v4l2_lock(self):
        """Linux only, best effort. v4l2-ctl succeeds where OpenCV's set() quietly does not.

        Note the inversion: v4l2 auto_exposure=1 means MANUAL, 3 means auto. That is
        the driver's convention, not a typo.
        """
        if not sys.platform.startswith("linux") or self.kind != "camera":
            return False
        if not shutil.which("v4l2-ctl"):
            return False

        controls = self.cfg.get("controls", {})
        pairs = []
        if "auto_exposure" in controls:
            pairs.append(f"auto_exposure={3 if controls['auto_exposure'] else 1}")
        if controls.get("exposure", -1) >= 0 and not controls.get("auto_exposure", False):
            pairs.append(f"exposure_time_absolute={int(controls['exposure'])}")
        if "auto_white_balance" in controls:
            pairs.append(f"white_balance_automatic={1 if controls['auto_white_balance'] else 0}")
        if controls.get("white_balance", -1) >= 0:
            pairs.append(f"white_balance_temperature={int(controls['white_balance'])}")
        if controls.get("gain", -1) >= 0:
            pairs.append(f"gain={int(controls['gain'])}")
        if not pairs:
            return False

        cmd = ["v4l2-ctl", "-d", f"/dev/video{self.value}", "-c", ",".join(pairs)]
        try:
            done = subprocess.run(cmd, capture_output=True, timeout=5, text=True)
            if done.returncode != 0:
                print(f"[OceanEye] v4l2-ctl declined some controls: {done.stderr.strip()}")
            return done.returncode == 0
        except (OSError, subprocess.SubprocessError) as exc:
            print(f"[OceanEye] v4l2-ctl unavailable: {exc}")
            return False

    def _warmup(self):
        for _ in range(int(self.cfg.get("warmup_frames", 0))):
            self._cap.read()

    # -- reading ------------------------------------------------------------

    def read(self):
        if self._scene is not None:
            ok, frame = self._scene.read()
        elif self._images:
            if self._index >= len(self._images):
                return False, None
            frame = cv2.imread(self._images[self._index])
            self._index += 1
            ok = frame is not None
        else:
            ok, frame = self._cap.read()

        if ok and self.flip_mode:
            frame = vision.flip(frame, self.flip_mode)
        return ok, frame

    def swap_to(self, source: str):
        """Hot-swap the source mid-run. This is the on-stage 'the camera just died' key."""
        self.release()
        self.cfg = dict(self.cfg, source=source)
        self.kind, self.value = classify(source)
        self.is_still = self.kind == "image"
        self._cap = self._scene = None
        self._images, self._index = [], 0
        self._open()

    def release(self):
        if self._cap is not None:
            self._cap.release()


def list_cameras(limit=6):
    """Probe camera indices so you can find the endoscope instead of the built-in webcam."""
    found = []
    # Probing absent indices makes the V4L2 backend shout. Expected, and not useful here.
    try:
        previous = cv2.getLogLevel()
        cv2.setLogLevel(0)
    except AttributeError:
        previous = None
    flag = cv2.CAP_V4L2 if sys.platform.startswith("linux") else cv2.CAP_ANY
    for index in range(limit):
        cap = cv2.VideoCapture(index, flag)
        if cap.isOpened():
            ok, frame = cap.read()
            if ok and frame is not None:
                h, w = frame.shape[:2]
                found.append({"index": index, "width": w, "height": h})
        cap.release()
    if previous is not None:
        cv2.setLogLevel(previous)
    return found
