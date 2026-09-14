"""The run loop and the pre-flight check.

This file knows nothing about which camera or which model is in use. It reads frames,
enhances them, detects, counts, draws, logs, and listens for the keys. Change the
hardware and this file does not change.
"""

from __future__ import annotations

import os
import shutil
import socket
import sys
import time
from pathlib import Path

import cv2
import numpy

from . import capture, config, detect, session as session_mod, vision

LEVELS = ["L0", "L1", "L2", "L3"]     # turbidity ladder: clear -> 3 spoons of clay

KEYMAP = """
  e        enhancement on/off        (the before/after moment)
  t        tracking on/off           (unique counting)
  u        simulated turbidity on/off
  0 1 2 3  tag the turbidity level   L0 clear .. L3 heaviest
  - / =    confidence down / up      (0.05 steps)
  p        PANIC: confidence -> 0.20 (nothing is being detected on stage)
  r        start/stop recording
  b        switch to the backup video  (the camera just died)
  space    pause      s  save frame      h  this help      q  quit
"""


def gui_available():
    """True if this OpenCV build and this session can actually open a window.

    opencv-python-headless has no highgui, and a machine with no DISPLAY cannot show
    one. Either way we fall back to headless instead of dying mid-demo.
    """
    if not hasattr(cv2, "imshow"):
        return False
    if sys.platform.startswith("linux") and not (
        os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")
    ):
        return False
    try:
        cv2.namedWindow("__oceaneye_probe__", cv2.WINDOW_AUTOSIZE)
        cv2.destroyWindow("__oceaneye_probe__")
        cv2.waitKey(1)
        return True
    except cv2.error:
        return False


def run(cfg, headless=False, max_frames=0, save_video=None, run_name=None):
    """Execute one demo run. Returns the summary dict."""
    cap = capture.Capture(cfg["capture"])
    detector = detect.load(cfg["model"])
    counter = detect.Counter()

    sess = session_mod.Session(cfg["session"]["outdir"], name=run_name,
                              log=cfg["session"]["log"], settings=cfg)

    show = not headless and gui_available()
    want_video = bool(save_video or cfg["session"]["autosave_video"])
    if not headless and not show:
        print("[OceanEye] no GUI available - running headless")
    if not show and not want_video:
        print("[OceanEye] note: headless and not recording; results go to CSV only")

    disp = cfg["display"]
    enhance = disp["enhance"]
    turbid = disp["turbidity"]
    scale = disp["hud_scale"]
    window = disp["window"]
    track = cfg["model"]["track"]
    conf = cfg["model"]["conf"]
    backup = cfg["fallback"]["backup_video"]

    level = "L0"
    paused = False
    frames = 0
    fps = 0.0
    prev_t = None
    annotated = None
    swapped = False

    print(f"[OceanEye] {config.describe(cfg)}")
    print(f"[OceanEye] capture reports: {cap.settings}")
    print(f"[OceanEye] output: {sess.root}")
    if show:
        print(KEYMAP)

    try:
        while True:
            if not paused:
                ok, frame = cap.read()
                if not ok:
                    if cap.is_still and annotated is not None:
                        paused = True          # single image: hold it, do not flash and exit
                        continue
                    print("[OceanEye] end of stream")
                    break

                proc = vision.simulate_turbidity(frame) if turbid else frame
                if enhance:
                    proc = vision.enhance_underwater(proc)

                detections = detector.infer(proc, track=track, conf=conf)
                counter.update(detections)

                now = time.time()
                if prev_t is not None:
                    inst = 1.0 / max(now - prev_t, 1e-6)
                    fps = inst if fps == 0.0 else 0.9 * fps + 0.1 * inst
                prev_t = now

                annotated = vision.draw_detections(
                    proc.copy(), detections, scale=scale,
                    show_conf=disp["show_conf"], show_id=disp["show_track_id"])

                hud = [
                    (f"FPS {fps:4.1f}   conf {conf:.2f}   turbidity {level}", (0, 255, 255)),
                    (f"In frame: {len(detections)}" +
                     (f"   Unique total: {counter.total_unique}" if track else ""), (0, 255, 0)),
                ]
                hud += counter.hud_lines(track)
                hud.append((f"Enhancement {'ON' if enhance else 'OFF'}"
                            + ("   SIM-TURBIDITY" if turbid else "")
                            + ("   REC" if sess.recording else ""), (255, 200, 0)))
                annotated = vision.draw_hud(annotated, hud, scale=scale)

                if detector.is_mock:
                    vision.draw_banner(annotated,
                                       "MOCK DETECTOR - no trained model loaded - pipeline test only",
                                       (0, 0, 255), scale)
                if swapped:
                    vision.draw_banner(annotated, "PLAYING RECORDED SURVEY FOOTAGE",
                                       (0, 200, 255), scale)

                sess.log(frames, detections, level=level, enhance=enhance, turbid=turbid,
                         conf_thres=conf, fps=fps)

                if want_video:
                    # One attempt, on the first frame, once the frame size is known.
                    # Retrying would re-print the same failure on every frame.
                    want_video = False
                    sess.start_recording(annotated, fps=cfg["capture"]["fps"],
                                         filename=save_video or "recording.mp4")
                sess.write_frame(annotated)

                if show:
                    cv2.imshow(window, annotated)

                frames += 1
                if max_frames and frames >= max_frames:
                    print(f"[OceanEye] reached max-frames {max_frames}")
                    break

            if not show:
                if paused:            # headless still image: nothing further to do
                    break
                continue

            if cv2.getWindowProperty(window, cv2.WND_PROP_VISIBLE) < 1:
                break

            key = cv2.waitKey(30 if paused else 1) & 0xFF
            if key in (ord("q"), 27):
                break
            elif key == ord("e"):
                enhance = not enhance
                print(f"[OceanEye] enhancement {'ON' if enhance else 'OFF'}")
            elif key == ord("t"):
                track = not track
                print(f"[OceanEye] tracking {'ON' if track else 'OFF'}")
            elif key == ord("u"):
                turbid = not turbid
            elif key in (ord("0"), ord("1"), ord("2"), ord("3")):
                level = LEVELS[key - ord("0")]
                print(f"[OceanEye] turbidity level -> {level}")
            elif key in (ord("-"), ord("_")):
                conf = max(0.05, round(conf - 0.05, 2))
                print(f"[OceanEye] conf {conf:.2f}")
            elif key in (ord("="), ord("+")):
                conf = min(0.95, round(conf + 0.05, 2))
                print(f"[OceanEye] conf {conf:.2f}")
            elif key == ord("p"):
                conf = 0.20
                print("[OceanEye] PANIC conf 0.20")
            elif key == ord("r"):
                if sess.recording:
                    sess.stop_recording()
                elif annotated is not None:
                    path = sess.start_recording(annotated, fps=cfg["capture"]["fps"])
                    print(f"[OceanEye] recording -> {path}")
            elif key == ord("b"):
                if not backup:
                    print("[OceanEye] no backup video configured (set fallback.backup_video)")
                else:
                    print(f"[OceanEye] switching to backup: {backup}")
                    cap.swap_to(backup)
                    swapped = True
            elif key == ord(" "):
                paused = not paused
            elif key == ord("s"):
                if annotated is not None:
                    print(f"[OceanEye] saved {sess.snapshot(annotated)}")
            elif key == ord("h"):
                print(KEYMAP)
    except KeyboardInterrupt:
        print("\n[OceanEye] interrupted")
    finally:
        cap.release()
        summary = sess.close(counter=counter,
                             extra={"detector": detector.label, "mock": detector.is_mock,
                                    "capture": cap.settings})
        if show:
            cv2.destroyAllWindows()

    session_mod.print_summary(summary)
    return summary


# ---------------------------------------------------------------------------
# Pre-flight
# ---------------------------------------------------------------------------


def _online(timeout=1.5):
    """True if the machine can reach the internet. Used to PROVE we do not need it."""
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=timeout).close()
        return True
    except OSError:
        return False


def preflight(cfg, frames=30):
    """Everything that can be checked before the demo, checked now instead of on stage.

    Run this after a full laptop restart with Wi-Fi OFF. That is the test that catches
    what nothing else catches.
    """
    ok = True

    def line(good, text, warn=False):
        nonlocal ok
        mark = "PASS" if good else ("WARN" if warn else "FAIL")
        if not good and not warn:
            ok = False
        print(f"  [{mark}] {text}")

    print("\n" + "=" * 62)
    print("  OCEANEYE PRE-FLIGHT")
    print("=" * 62)

    print(f"  python {sys.version.split()[0]} | opencv {cv2.__version__} | numpy {numpy.__version__}")
    line(gui_available(), "display available (a window can be opened)", warn=True)

    # A profile that deliberately asks for the mock detector is not broken, so the
    # missing model stack is only a warning in that case.
    wants_mock = str(cfg["model"]["path"]).lower() in {"mock", "none", ""}
    try:
        import ultralytics
        line(True, f"ultralytics {ultralytics.__version__}")
    except ImportError:
        line(False, "ultralytics NOT installed - detection will be MOCK only", warn=wants_mock)

    try:
        import torch
        cuda = torch.cuda.is_available()
        line(True, f"torch {torch.__version__} | GPU: {torch.cuda.get_device_name(0) if cuda else 'none (CPU)'}")
    except ImportError:
        line(False, "torch NOT installed", warn=True)

    # Being online is not a fault, but it leaves the offline claim untested.
    if _online():
        line(False, "machine is ONLINE - re-run with Wi-Fi OFF to prove offline operation",
             warn=True)
    else:
        line(True, "offline - nothing here needs the internet")

    detector = detect.load(cfg["model"])
    line(not detector.is_mock, f"detector: {detector.label}", warn=wants_mock)

    try:
        cap = capture.Capture(cfg["capture"])
    except SystemExit as exc:
        line(False, str(exc))
        print("=" * 62)
        return False

    grabbed, start = 0, time.time()
    for _ in range(frames):
        got, frame = cap.read()
        if got:
            grabbed += 1
    elapsed = max(time.time() - start, 1e-6)
    cap.release()

    line(grabbed == frames, f"captured {grabbed}/{frames} frames from {cfg['capture']['source']}")
    measured = grabbed / elapsed
    line(measured >= 20, f"capture+read rate {measured:.1f} fps (want >= 20)", warn=measured >= 10)
    print(f"         reported by device: {cap.settings}")

    backup = cfg["fallback"]["backup_video"]
    if backup:
        line(Path(backup).exists(), f"backup video present: {backup}")
    else:
        line(False, "no backup video configured - set fallback.backup_video", warn=True)

    free_gb = shutil.disk_usage(".").free / 1e9
    line(free_gb > 2, f"{free_gb:.1f} GB free for recordings")

    print("=" * 62)
    print("  READY" if ok else "  NOT READY - fix the FAIL lines above")
    print("=" * 62 + "\n")
    return ok
