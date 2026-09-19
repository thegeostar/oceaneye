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

# OceanEye: was hardcoded to E:/URPC/... on the author's Windows machine. Derived from
# __file__ so the app runs wherever the folder is copied, and defined here only — the
# image and camera paths import it from this module rather than repeating it.
WEIGHTS = os.environ.get("OCEANEYE_WEIGHTS", os.path.join(
    parent_dir, "output_dir/mscoco/mambayolo_n/weights/best.pt"))

# OceanEye: confidence floor. Nothing here set one, so all three paths silently used
# ultralytics' built-in 0.25 — and it cannot be changed by setting model.overrides,
# because Model.predict() merges {**self.overrides, **custom, **kwargs} with
# custom = {"conf": 0.25}, which overwrites it. Only a kwarg at the call site wins,
# so every call site passes CONF.
#
# Why it needs a knob: the weights were trained on URPC seabed footage. Our own tank
# is market-bought specimens behind glass under room light — off that distribution.
# The model will still fire on them, but weaker, and at 0.25 a real detection at 0.18
# is indistinguishable from the model seeing nothing at all. That is the one thing you
# must be able to tell apart when testing a new scene.
#
#   OCEANEYE_CONF=0.05 python app.py     # tank testing: show me what it ALMOST saw
#
# Default stays 0.25 so verify_model.py still reproduces starfish 0.83 / holothurian 0.78.
# Find the lowest value that is still clean on YOUR tank, then pin it for the demo.
CONF = float(os.environ.get("OCEANEYE_CONF", "0.25"))

# where annotated results are written, for the image, video and camera paths alike
OUT_DIR = os.path.join(parent_dir, 'app', 'static', 'detected')


def export_path(video_path):
    """Where the annotated copy of `video_path` lands once it is complete."""
    name = os.path.splitext(os.path.basename(video_path))[0]
    return os.path.join(OUT_DIR, name + '_detected.mp4')


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
    results = model.predict(enhance(frame), verbose=False, conf=CONF)
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
    """Frame generator for the video stream, recording an annotated copy as it goes.

    OceanEye: the annotated frames used to exist only inside this stream, so there was
    nothing left to download once it had played. Re-running the video to a file
    afterwards would cost a second full pass — 1.16 s/frame measured, ~9 minutes for the
    45 s test clip — so the copy is written here, beside the stream, for a few
    milliseconds per frame on top of the second the model already takes.

    It is written under a temp name and renamed only after the last frame is read, so a
    stream that is cut short leaves no download at all rather than a video shorter than
    the one that was uploaded.
    """
    model = load_model()
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        yield "Video open failed"
        return

    # the source frame rate, so the copy runs exactly as long as the upload. Some
    # containers report 0 or nan for it; 25 is the usual stand-in. (x != x is nan.)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps != fps or fps <= 0:
        fps = 25.0

    os.makedirs(OUT_DIR, exist_ok=True)
    final_path = export_path(video_path)
    # the temp name keeps the .mp4 suffix: VideoWriter picks its container from the
    # extension and refuses to open anything it does not recognise, .part included
    root, ext = os.path.splitext(final_path)
    tmp_path = f'{root}.part{os.getpid()}{ext}'
    # clear the copy from any earlier run, so a file being there always means THIS run
    # finished — never an older recording of the same upload
    if os.path.exists(final_path):
        os.remove(final_path)

    writer = None
    completed = False
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            processed_frame = process_frame(frame, model)

            # opened on the first frame, sized from that frame rather than from the
            # capture properties: plot() draws on whatever went into the model, and a
            # writer whose size disagrees with the frame silently writes nothing
            if writer is None:
                height, width = processed_frame.shape[:2]
                # ponytail: mp4v is the only codec this OpenCV build can write — it has
                # no H.264 encoder, avc1 fails to open. VLC and the usual desktop
                # players read it; browsers do not. Convert if a browser has to play it.
                writer = cv2.VideoWriter(tmp_path, cv2.VideoWriter_fourcc(*'mp4v'),
                                         fps, (width, height))
            if writer.isOpened():
                writer.write(processed_frame)

            ret, buffer = cv2.imencode('.jpg', processed_frame)
            if not ret:
                continue

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        completed = True

    finally:
        cap.release()
        if writer is not None:
            writer.release()  # has to close before the file is whole
            # no tmp_path at all means the codec refused to open and nothing was recorded
            if os.path.exists(tmp_path):
                if completed:
                    os.replace(tmp_path, final_path)
                else:
                    os.remove(tmp_path)