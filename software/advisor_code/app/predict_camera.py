"""Live-camera detection stream.

OceanEye: this whole file was rewritten. Changes vs. the original:

1. The original ACCEPTED a camera_index and then ignored it, opening a hardcoded
   `E:/URPC/code_URPC/test_video.mp4` instead. Clicking "Real-time Monitoring" played
   a recorded file while presenting itself as a live camera. Fixed: it opens the
   camera. A recorded file is still available, but only when you ask for it by
   setting OCEANEYE_CAMERA_FALLBACK, and the stream then says so on screen.
2. draw_chinese_text/process_frame were copy-pasted from predict_video.py with a
   different (empty, always-failing) font path. Imported from there instead, so the
   font and the drawing logic have one home.
3. Detection no longer sits in the capture loop. It used to run the model on every
   frame before yielding it, so the browser only ever saw a frame once the model
   had finished — the video itself stuttered at model speed, about 1 fps. Now the
   capture loop yields frames as fast as the camera produces them and a worker
   thread detects on the newest frame it can get, so the feed is smooth and the
   boxes refresh whenever inference finishes. The video is genuinely live
   throughout; only the boxes lag, by roughly one inference.
"""
import os
import threading
import time

import cv2

from predict_video import draw_texts, load_model

# Set this to a video file to allow a fallback when no camera opens. Unset = no fallback,
# which is the honest default: a failed camera should look failed, not look live.
FALLBACK_VIDEO = os.environ.get("OCEANEYE_CAMERA_FALLBACK", "")

BOX_COLOUR = (0, 200, 0)


def _overlay(frame, detections):
    """Draw a detection set from a previous frame onto the current one.

    The boxes are up to one inference old. That is fine for a fixed camera on a
    tank — the creatures are where they were a second ago — but it is why this
    draws them itself instead of calling results.plot(), which can only draw onto
    the exact frame it detected on.
    """
    if not detections:
        return frame

    texts = []
    for x1, y1, x2, y2, name, conf in detections:
        cv2.rectangle(frame, (x1, y1), (x2, y2), BOX_COLOUR, 2)
        texts.append((f"{name} {conf:.2f}", (x1, max(0, y1 - 34))))

    counts = {}
    for *_, name, _conf in detections:
        counts[name] = counts.get(name, 0) + 1
    for i, (name, n) in enumerate(sorted(counts.items())):
        texts.append((f"{name}: {n}", (20, 20 + i * 40)))

    return draw_texts(frame, texts, font_size=28, color=BOX_COLOUR)


def _detect(model, frame):
    """Run the model once and flatten the result into plain tuples."""
    result = model.predict(frame, verbose=False)[0]
    if result.boxes is None:
        return []
    return [(int(x1), int(y1), int(x2), int(y2), result.names[int(cls)], float(conf))
            for (x1, y1, x2, y2), cls, conf
            in zip(result.boxes.xyxy.tolist(), result.boxes.cls.tolist(),
                   result.boxes.conf.tolist())]


def run_camera_processing(camera_index=0):
    """Frame generator for the video stream — yields multipart JPEG frames."""
    model = load_model()

    cap = cv2.VideoCapture(camera_index)
    recorded = False
    if not cap.isOpened() and FALLBACK_VIDEO:
        cap = cv2.VideoCapture(FALLBACK_VIDEO)
        recorded = True
    if not cap.isOpened():
        yield f"Camera {camera_index} open failed"
        return

    # Single-slot handoff both ways: the capture loop publishes the newest frame,
    # the worker publishes the newest detections. Nothing queues, so a slow model
    # can never build a backlog — it just skips the frames it missed.
    state = {"frame": None, "detections": [], "stop": False}

    def worker():
        while not state["stop"]:
            frame = state["frame"]
            if frame is None:
                time.sleep(0.01)
                continue
            state["frame"] = None            # claim it
            try:
                state["detections"] = _detect(model, frame)
            except Exception as exc:         # a bad frame must not kill the feed
                print(f"detection failed on one frame: {exc}")

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

    try:
        while True:
            success, frame = cap.read()
            if not success:
                break

            state["frame"] = frame           # newest wins; older ones are dropped
            annotated = _overlay(frame.copy(), state["detections"])
            if recorded:
                # Never let recorded footage pass for a live feed.
                annotated = draw_texts(
                    annotated,
                    [("PLAYING RECORDED FOOTAGE - NOT LIVE",
                      (20, annotated.shape[0] - 50))], color=(0, 0, 255))

            ret, buffer = cv2.imencode('.jpg', annotated)
            if not ret:
                continue

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    finally:
        state["stop"] = True
        thread.join(timeout=2)
        cap.release()
