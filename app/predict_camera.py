"""Live camera detection stream.

The capture loop streams every camera frame while a worker thread runs the model on the
newest one, so the video stays smooth and the boxes update as fast as inference allows.
"""
import os
import threading
import time

import cv2

from predict_video import CONF, draw_counts, draw_texts, enhance, load_model, mjpeg_part

# Optional recorded clip to play when the camera cannot be opened. It is labelled on screen.
FALLBACK_VIDEO = os.environ.get('OCEANEYE_CAMERA_FALLBACK', '')
BOX_COLOR = (0, 200, 0)


def _detect(model, frame):
    """Run the model once and return (x1, y1, x2, y2, name, conf) tuples."""
    r = model.predict(enhance(frame), verbose=False, conf=CONF)[0]
    return [(int(x1), int(y1), int(x2), int(y2), r.names[int(c)], float(p))
            for (x1, y1, x2, y2), c, p
            in zip(r.boxes.xyxy.tolist(), r.boxes.cls.tolist(), r.boxes.conf.tolist())]


def _overlay(frame, detections):
    """Draw detections from an earlier frame onto the current one."""
    for x1, y1, x2, y2, _, _ in detections:
        cv2.rectangle(frame, (x1, y1), (x2, y2), BOX_COLOR, 2)
    draw_texts(frame, [(f'{name} {conf:.2f}', (x1, max(0, y1 - 34)))
                       for x1, y1, _, _, name, conf in detections], 28, BOX_COLOR)
    return draw_counts(frame, [d[4] for d in detections], 28, BOX_COLOR)


def run_camera_processing(camera_index=0):
    """Yield annotated frames from a camera as a multipart JPEG stream."""
    model = load_model()
    cap = cv2.VideoCapture(camera_index)
    recorded = False
    if not cap.isOpened() and FALLBACK_VIDEO:
        cap, recorded = cv2.VideoCapture(FALLBACK_VIDEO), True
    if not cap.isOpened():
        yield f'Camera {camera_index} open failed'
        return

    # Single-slot handoff: the capture loop publishes the newest frame and the worker the
    # newest detections, so a slow model skips frames instead of building a backlog.
    state = {'frame': None, 'detections': [], 'stop': False}

    def worker():
        while not state['stop']:
            frame, state['frame'] = state['frame'], None
            if frame is None:
                time.sleep(0.01)
                continue
            try:
                state['detections'] = _detect(model, frame)
            except Exception as exc:  # one bad frame should not end the stream
                print(f'Detection failed: {exc}')

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            state['frame'] = frame
            annotated = _overlay(frame.copy(), state['detections'])
            if recorded:
                draw_texts(annotated, [('RECORDED FOOTAGE - NOT LIVE',
                                        (20, annotated.shape[0] - 50))])
            yield mjpeg_part(annotated)
    finally:
        state['stop'] = True
        thread.join(timeout=2)
        cap.release()
