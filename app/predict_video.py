"""Shared model, drawing helpers and the video-file detection stream."""
import os
import sys
from collections import Counter
from functools import lru_cache

import cv2

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT)
from ultralytics import YOLO  # noqa: E402

WEIGHTS = os.environ.get('OCEANEYE_WEIGHTS', os.path.join(ROOT, 'model', 'best.pt'))
# Minimum confidence for a detection. Lower it to inspect weak detections on new footage.
CONF = float(os.environ.get('OCEANEYE_CONF', '0.25'))
OUT_DIR = os.path.join(ROOT, 'app', 'static', 'detected')

# Contrast enhancement helps in murky water but costs detections in clear water,
# so it starts off and the dashboard toggles it at run time.
ENHANCE = False
_CLAHE = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))


@lru_cache(maxsize=1)
def load_model():
    """Load the detector once; the image, video and camera paths share it."""
    return YOLO(WEIGHTS)


def enhance(frame):
    """Apply CLAHE to the lightness channel when ENHANCE is on. Colours stay unchanged."""
    if not ENHANCE:
        return frame
    l, a, b = cv2.split(cv2.cvtColor(frame, cv2.COLOR_BGR2LAB))
    return cv2.cvtColor(cv2.merge((_CLAHE.apply(l), a, b)), cv2.COLOR_LAB2BGR)


def export_path(video_path):
    """Path of the annotated copy of `video_path`."""
    name = os.path.splitext(os.path.basename(video_path))[0]
    return os.path.join(OUT_DIR, name + '_detected.mp4')


def draw_texts(image, items, font_size=32, color=(0, 0, 255)):
    """Draw (text, (x, y)) pairs onto a BGR image in place. (x, y) is the top-left corner."""
    for text, (x, y) in items:
        cv2.putText(image, text, (int(x), int(y + font_size)), cv2.FONT_HERSHEY_SIMPLEX,
                    font_size / 32, color, 2, cv2.LINE_AA)
    return image


def draw_counts(image, names, font_size=32, color=(0, 0, 255)):
    """Draw how many of each class were detected, stacked in the top-left corner."""
    counts = sorted(Counter(names).items())
    return draw_texts(image, [(f'{name}: {n}', (20, 20 + i * 40))
                              for i, (name, n) in enumerate(counts)], font_size, color)


def mjpeg_part(image):
    """Encode a frame as one part of a multipart/x-mixed-replace stream."""
    ok, buffer = cv2.imencode('.jpg', image)
    if not ok:
        return b''
    return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n'


def process_frame(frame, model):
    """Detect on one frame and return it annotated with boxes and per-class counts."""
    result = model.predict(enhance(frame), verbose=False, conf=CONF)[0]
    names = [model.names[int(c)] for c in result.boxes.cls.tolist()]
    return draw_counts(result.plot(), names)


def run_video_processing(video_path):
    """Stream annotated frames of a video and save an annotated copy alongside.

    The copy is written under a temporary name and renamed after the last frame, so an
    interrupted stream never leaves a partial file behind.
    """
    model = load_model()
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        yield 'Video open failed'
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps > 0:  # some containers report 0 or NaN
        fps = 25.0

    os.makedirs(OUT_DIR, exist_ok=True)
    final_path = export_path(video_path)
    root, ext = os.path.splitext(final_path)
    tmp_path = f'{root}.part{os.getpid()}{ext}'  # VideoWriter picks the codec from the extension
    if os.path.exists(final_path):
        os.remove(final_path)

    writer = None
    completed = False
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            annotated = process_frame(frame, model)
            if writer is None:
                height, width = annotated.shape[:2]
                # ponytail: mp4v plays in desktop players, not browsers; use avc1 where OpenCV has H.264
                writer = cv2.VideoWriter(tmp_path, cv2.VideoWriter_fourcc(*'mp4v'),
                                         fps, (width, height))
            if writer.isOpened():
                writer.write(annotated)
            yield mjpeg_part(annotated)
        completed = True
    finally:
        cap.release()
        if writer is not None:
            writer.release()
            if os.path.exists(tmp_path):
                if completed:
                    os.replace(tmp_path, final_path)
                else:
                    os.remove(tmp_path)
