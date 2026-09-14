#!/usr/bin/env python3
"""
OceanEye - AI Vision-Driven Intelligent Underwater Perception and Detection System
Group 22 | Royal University of Phnom Penh
2026 World Vocational College Skills Competition - Southeast Asia Division

Command-line front end. All the work happens in the oceaneye/ package.
Runs fully OFFLINE.

    # no camera and no model needed - proves the whole pipeline works today
    python oceaneye_demo.py --profile desk --max-frames 200

    # the real thing, once hardware and weights exist
    python oceaneye_demo.py --profile endoscope --model ../08_Data/weights/best.pt

    # check everything the night before, with Wi-Fi OFF
    python oceaneye_demo.py --profile endoscope --preflight

    # find which index the endoscope is on
    python oceaneye_demo.py --list-cameras

Keys during playback: press h in the window for the full list.
"""

import argparse
import sys

from oceaneye import capture, config, runner


def build_parser():
    ap = argparse.ArgumentParser(
        description="OceanEye underwater detection demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=runner.KEYMAP,
    )
    ap.add_argument("--profile", default=None,
                    help="device profile: a .toml path, or a name from profiles/")
    ap.add_argument("--source", default=None,
                    help="0/1/2 camera · file.mp4 · photo.jpg · folder/ · rtsp://... · synthetic")
    ap.add_argument("--model", default=None,
                    help="path to weights (.pt/.onnx/.engine), or 'mock' for no model")
    ap.add_argument("--conf", type=float, default=None, help="confidence threshold")
    ap.add_argument("--imgsz", type=int, default=None, help="inference image size")
    ap.add_argument("--device", default=None, help="cpu, cuda:0 (default: auto)")
    ap.add_argument("--backup", default=None, help="video to switch to with the 'b' key")

    ap.add_argument("--track", action="store_true", help="force tracking on")
    ap.add_argument("--no-track", action="store_true", help="force tracking off")
    ap.add_argument("--no-enhance", action="store_true", help="start with enhancement off")
    ap.add_argument("--turbid", action="store_true", help="start with simulated turbidity on")

    ap.add_argument("--headless", action="store_true", help="no window")
    ap.add_argument("--save-video", default=None, metavar="OUT.mp4",
                    help="record the annotated run from the first frame")
    ap.add_argument("--outdir", default=None, help="where run folders are created")
    ap.add_argument("--name", default=None, help="name this run instead of using a timestamp")
    ap.add_argument("--no-log", action="store_true", help="do not write detections.csv")
    ap.add_argument("--max-frames", type=int, default=0, help="stop after N frames (0 = no limit)")

    ap.add_argument("--preflight", action="store_true",
                    help="check model, camera, fps, offline status, disk - then exit")
    ap.add_argument("--list-cameras", action="store_true",
                    help="probe camera indices 0-5 and exit")
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)

    if args.list_cameras:
        found = capture.list_cameras()
        if not found:
            print("[OceanEye] no cameras found. Plug it in, then check: v4l2-ctl --list-devices")
            return 1
        for cam in found:
            print(f"  --source {cam['index']}   {cam['width']}x{cam['height']}")
        return 0

    cfg = config.apply_cli(config.load(args.profile), args)

    if args.preflight:
        return 0 if runner.preflight(cfg) else 1

    runner.run(cfg, headless=args.headless, max_frames=args.max_frames,
               save_video=args.save_video, run_name=args.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
