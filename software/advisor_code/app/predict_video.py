import cv2
import sys
import os

# parent directory of this script
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# add the parent directory to sys.path
sys.path.insert(0, parent_dir)

from ultralytics import YOLO
from collections import defaultdict
from functools import lru_cache

# OceanEye: weights path was hardcoded to E:/URPC/... . See predict_img.py.
WEIGHTS = os.environ.get("OCEANEYE_WEIGHTS", os.path.join(
    parent_dir, "output_dir/mscoco/mambayolo_n/weights/best.pt"))

@lru_cache(maxsize=1)
def load_model():
    """The one model for this process.

    OceanEye: every entry point used to call YOLO(WEIGHTS) itself, and
    predict_img.detect() did it per uploaded image — re-reading 139 MB off disk
    and rebuilding the graph on every request. Loaded once here instead, so the
    image, video and camera paths all share a single copy in VRAM.
    """
    return YOLO(WEIGHTS)


# OceanEye: contrast enhancement, off by default. One flag, read by the image, video and
# camera paths, flipped live from the web page so the before/after is a demo moment.
#
# Measured (bench_enhance.py), 4 real URPC images under simulated turbidity:
#
#   turbidity   raw        CLAHE
#   L0 clear    22 @ 0.68  15 @ 0.60   <- enhancement LOSES 7 detections
#   L1          19 @ 0.62  19 @ 0.59   <- break-even
#   L2          11 @ 0.41  17 @ 0.56   <- crossover
#   L3           3 @ 0.30  11 @ 0.60
#   L4           0 @ 0.00   8 @ 0.55   <- raw finds nothing at all
#
# So it must default OFF: on clear water it throws away a third of the detections,
# because the model was trained on raw URPC frames and this shifts them off that
# distribution. Above ~L2 it is the difference between a live demo and a dead one.
# Gray-world white balance was measured too and was worse at every level — dropped.
ENHANCE = False

_CLAHE = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))


def enhance(frame):
    """Local contrast boost on the L channel only, so colour is untouched."""
    if not ENHANCE:
        return frame
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    return cv2.cvtColor(cv2.merge((_CLAHE.apply(l), a, b)), cv2.COLOR_LAB2BGR)


def draw_texts(image, items, font_size=32, color=(0, 0, 255)):
    """Draw (text, (x, y)) pairs onto a BGR frame, in place. (x, y) is the top-left.

    OceanEye: was draw_chinese_text, called once per line, each call re-reading a
    .ttf off disk and converting the whole frame BGR->RGB->PIL->RGB->BGR. Measured
    at 182 ms on a 4K frame — 33x the cost of drawing the boxes — which capped the
    live feed near 5 fps however fast the model got. The TrueType hunt only existed
    to get Chinese glyphs and every label is English now, so this uses cv2 directly.
    Hershey is vector-scaled and stays readable on a projector; the thing the old
    font list was avoiding was PIL's bitmap load_default(), not cv2.
    """
    scale = font_size / 32
    for text, (x, y) in items:
        # PIL positioned from the top-left, cv2 from the baseline: keep it where it was
        cv2.putText(image, text, (int(x), int(y + font_size)),
                    cv2.FONT_HERSHEY_SIMPLEX, scale, color, 2, cv2.LINE_AA)
    return image


def draw_labels(image, lines, position=(20, 20), line_height=40, font_size=32,
                color=(0, 0, 255)):
    """Draw text lines onto a BGR frame, stacked top-down from `position`."""
    x, y = position
    return draw_texts(image, [(line, (x, y + i * line_height))
                              for i, line in enumerate(lines)], font_size, color)

def process_frame(frame, model):
    """Run the model on one frame and draw the boxes plus a per-class count."""
    # verbose=False: ultralytics otherwise prints a timing line per frame, which on a
    # video is thousands of lines of console spam and a blocking write per frame.
    results = model.predict(enhance(frame), verbose=False)
    class_counts = defaultdict(int)
    annotated_frame = frame.copy()

    if results[0].boxes is not None:
        # draw the boxes and count each class
        annotated_frame = results[0].plot(conf=True, labels=True)

        for cls_id in results[0].boxes.cls.cpu().numpy():
            class_name = model.names[int(cls_id)]
            class_counts[class_name] += 1

    # counts go in the top-left corner
    return draw_labels(annotated_frame,
                       [f'{name}: {count}' for name, count in class_counts.items()])

def run_video_processing(video_path):
    """Frame generator for the video stream."""
    model = load_model()
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        yield "Video open failed"
        return

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            processed_frame = process_frame(frame, model)
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            if not ret:
                continue

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    finally:
        cap.release()