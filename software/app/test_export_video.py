"""The downloaded video has to be as long as the one that was uploaded.

run_video_processing records while it streams, so the file it leaves behind is only
worth offering if it holds every frame. Two things are checked here: a stream that runs
to the end produces a copy with the same frame count and frame rate as the source, and a
stream that is cut short produces no file at all — an early download is better refused
than served three seconds of a forty-five second clip.

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
    """A small clip, so this runs the real model without running for minutes."""
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
    work = tempfile.mkdtemp()
    clip = os.path.join(work, 'length_check.mp4')
    make_clip(clip)
    out = export_path(clip)

    # played to the end: the copy matches the source, so it runs just as long
    for _ in run_video_processing(clip):
        pass
    assert os.path.exists(out), f"nothing was recorded at {out}"
    src_frames, src_fps = properties(clip)
    out_frames, out_fps = properties(out)
    assert (out_frames, out_fps) == (src_frames, src_fps), (
        f"source is {src_frames} frames at {src_fps} fps but the download is "
        f"{out_frames} at {out_fps} — the two do not run for the same time")
    print(f"full stream: {out_frames} frames at {out_fps} fps, "
          f"{out_frames / out_fps:.2f}s, same as the upload")

    # cut short: the half-written file is thrown away rather than offered
    stream = run_video_processing(clip)
    next(stream)
    next(stream)
    stream.close()  # what Flask does when the browser goes away
    assert not os.path.exists(out), (
        "a stream that stopped early still left a downloadable file — it would be "
        "shorter than the upload")
    leftovers = [f for f in os.listdir(os.path.dirname(out)) if '.part' in f]
    assert not leftovers, f"temp recordings left behind: {leftovers}"
    print("cut-short stream: no file offered, no .part left behind")


if __name__ == "__main__":
    main()
    print("OK")
    sys.exit(0)
