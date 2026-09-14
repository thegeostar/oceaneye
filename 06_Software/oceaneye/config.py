"""Device profiles.

The whole point of this file: moving to a different camera, laptop or single-board
computer should mean editing a .toml file, never editing code.

TOML is used because Python 3.11+ reads it from the standard library (tomllib) and
it allows comments, so the profile can explain itself to whoever edits it next.
"""

from __future__ import annotations

import copy
import tomllib
from pathlib import Path

# Every setting the system understands, with a working default.
# A profile only needs to list what it changes.
DEFAULTS = {
    "capture": {
        "source": "0",          # "0" webcam · "clip.mp4" · "frames/" · "rtsp://..." · "synthetic"
        "width": 1280,
        "height": 720,
        "fps": 30,
        "fourcc": "MJPG",       # MJPG or many UVC cameras crawl at ~5 fps
        "backend": "auto",      # auto | v4l2 | any
        "flip": "",             # "" | h | v | hv
        "warmup_frames": 5,     # frames to throw away while auto-gain settles
        "controls": {           # all optional; unsupported ones are skipped, never fatal
            "auto_exposure": False,
            "exposure": 150,
            "auto_white_balance": False,
            "white_balance": 4500,
            "gain": 0,
            "focus": -1,        # -1 = leave alone
            "brightness": -1,
            "contrast": -1,
        },
    },
    "model": {
        "path": "yolo11n.pt",   # "mock" runs the pipeline with no weights at all
        "conf": 0.35,
        "iou": 0.45,
        "imgsz": 640,
        "device": "",           # "" = auto · "cpu" · "cuda:0"
        "track": True,
        "tracker": "bytetrack.yaml",
        "classes": ["holothurian", "echinus", "scallop", "starfish"],
    },
    "display": {
        "enhance": True,
        "turbidity": False,
        "hud_scale": 1.0,       # raise to 1.4 on a projector so judges can read it
        "window": "OceanEye - Group 22 - RUPP",
        "show_conf": True,
        "show_track_id": True,
    },
    "session": {
        "outdir": "runs",
        "log": True,            # per-detection CSV — this is what fills the results table
        "autosave_video": False,
    },
    "fallback": {
        "backup_video": "",     # press 'b' on stage to switch to this instantly
    },
}


def _merge(base: dict, override: dict) -> dict:
    """Deep-merge override into a copy of base. Unknown keys are kept, not dropped."""
    out = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _merge(out[key], value)
        else:
            out[key] = value
    return out


def load(profile_path=None) -> dict:
    """Return the full config: DEFAULTS, with a profile layered on top if given."""
    if not profile_path:
        return copy.deepcopy(DEFAULTS)

    path = Path(profile_path)
    if not path.exists():                       # allow bare names: --profile endoscope
        guess = Path(__file__).resolve().parent.parent / "profiles" / f"{path.stem}.toml"
        if guess.exists():
            path = guess
        else:
            raise SystemExit(f"[OceanEye] ERROR: profile not found: {profile_path}")

    with path.open("rb") as fh:
        return _merge(DEFAULTS, tomllib.load(fh))


def apply_cli(cfg: dict, args) -> dict:
    """Command-line flags beat the profile. Only flags the user actually passed."""
    mapping = {
        "source": ("capture", "source"),
        "model": ("model", "path"),
        "conf": ("model", "conf"),
        "imgsz": ("model", "imgsz"),
        "device": ("model", "device"),
        "outdir": ("session", "outdir"),
        "backup": ("fallback", "backup_video"),
    }
    for attr, (section, key) in mapping.items():
        value = getattr(args, attr, None)
        if value is not None:
            cfg[section][key] = value

    if getattr(args, "track", False):
        cfg["model"]["track"] = True
    if getattr(args, "no_track", False):
        cfg["model"]["track"] = False
    if getattr(args, "no_enhance", False):
        cfg["display"]["enhance"] = False
    if getattr(args, "turbid", False):
        cfg["display"]["turbidity"] = True
    if getattr(args, "no_log", False):
        cfg["session"]["log"] = False
    return cfg


def describe(cfg: dict) -> str:
    """One-line summary for the console and the run log."""
    c, m = cfg["capture"], cfg["model"]
    return (f"source={c['source']} {c['width']}x{c['height']}@{c['fps']} {c['fourcc']} | "
            f"model={m['path']} conf={m['conf']} imgsz={m['imgsz']} track={m['track']}")
