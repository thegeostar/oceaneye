"""Check the exported video: a finished stream saves a copy with the source's frame count
and frame rate, and an interrupted stream leaves no file behind.

    python test_export_video.py
"""
import os
import sys
import tempfile

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from predict_video import export_path, run_video_processing  # noqa: E402

FPS, FRAMES, SIZE = 12.0, 8, (320, 240)


def make_clip(path):
    """Write a short synthetic clip."""
    writer = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'mp4v'), FPS, SIZE)
    assert writer.isOpened(), "cannot write the test clip"
    for i in range(FRAMES):
        frame = np.full((SIZE[1], SIZE[0], 3), 20, np.uint8)
        cv2.circle(frame, (40 + i * 30, 120), 25, (60, 120, 200), -1)
        writer.write(frame)
    writer.release()


def properties(path):
    cap = cv2.VideoCapture(path)
    try:
        return int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), cap.get(cv2.CAP_PROP_FPS)
    finally:
        cap.release()


def main():
    with tempfile.TemporaryDirectory() as work:
        check(os.path.join(work, 'length_check.mp4'))


def check(clip):
    make_clip(clip)
    out = export_path(clip)

    # Played to the end: the copy matches the source.
    for _ in run_video_processing(clip):
        pass
    assert os.path.exists(out), f"nothing was recorded at {out}"
    src_frames, src_fps = properties(clip)
    out_frames, out_fps = properties(out)
    assert (out_frames, out_fps) == (src_frames, src_fps), (
        f"source is {src_frames} frames at {src_fps} fps, copy is {out_frames} at {out_fps}")
    print(f"full stream: {out_frames} frames at {out_fps} fps")

    # Cut short: the partial recording is discarded.
    stream = run_video_processing(clip)
    next(stream)
    next(stream)
    stream.close()  # what Flask does when the client disconnects
    assert not os.path.exists(out), "an interrupted stream left a file behind"
    leftovers = [f for f in os.listdir(os.path.dirname(out)) if '.part' in f]
    assert not leftovers, f"temp recordings left behind: {leftovers}"
    print("interrupted stream: no file left behind")


if __name__ == "__main__":
    main()
    print("OK")
