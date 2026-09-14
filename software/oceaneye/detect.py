"""Detection, tracking and counting — behind one interface.

Two detectors exist and produce identical output:

  YoloDetector  the real one (ultralytics). Loads .pt, .onnx, .engine or ncnn,
                so the same code runs on a laptop now and a smaller board later.
  MockDetector  no model, no weights, no download. Finds the coloured shapes in
                the synthetic scene so the rest of the system can be built and
                rehearsed today. It is labelled on screen and it is not a model.

Swapping in a different detector later means adding a class with .infer() here.
Nothing else in the project needs to change.
"""

from __future__ import annotations

from collections import defaultdict
from typing import NamedTuple

import cv2
import numpy as np

from . import vision


class Detection(NamedTuple):
    cls_id: int
    cls_name: str
    conf: float
    xyxy: tuple          # (x1, y1, x2, y2)
    track_id: int | None


# ---------------------------------------------------------------------------


class YoloDetector:
    is_mock = False

    def __init__(self, path, conf=0.35, iou=0.45, imgsz=640, device="", tracker="bytetrack.yaml"):
        from ultralytics import YOLO      # imported late so --help works without it

        self.model = YOLO(path)
        self.names = self.model.names
        self.conf, self.iou, self.imgsz = conf, iou, imgsz
        self.device = device or None
        self.tracker = tracker
        self.label = str(path)

    def infer(self, frame, track=False, conf=None):
        kwargs = dict(conf=conf or self.conf, iou=self.iou, imgsz=self.imgsz,
                      device=self.device, verbose=False)
        if track:
            results = self.model.track(frame, tracker=self.tracker, persist=True, **kwargs)
        else:
            results = self.model(frame, **kwargs)

        boxes = results[0].boxes
        out = []
        if boxes is None:
            return out

        ids = boxes.id.int().tolist() if getattr(boxes, "id", None) is not None else None
        for i in range(len(boxes)):
            cls_id = int(boxes.cls[i])
            out.append(Detection(
                cls_id=cls_id,
                cls_name=str(self.names.get(cls_id, cls_id)),
                conf=float(boxes.conf[i]),
                xyxy=tuple(float(v) for v in boxes.xyxy[i].tolist()),
                track_id=ids[i] if ids else None,
            ))
        return out


class MockDetector:
    """Colour-blob detector. Exists so the pipeline runs with zero weights.

    Finds saturated blobs whose hue matches a species colour. That is image
    processing, not machine learning — it only works on the synthetic scene and
    it must never be presented as the model.
    """

    is_mock = True

    def __init__(self, classes=None, min_area=400, conf=0.35, **_ignored):
        self.names = {i: n for i, n in enumerate(classes or list(vision.SPECIES_COLOURS))}
        self.min_area = min_area
        self.conf = conf
        self.label = "MOCK (no model loaded)"
        self._tracker = CentroidTracker()

    def infer(self, frame, track=False, conf=None):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        found = []

        for cls_id, name in self.names.items():
            colour = vision.colour_for(name, cls_id)
            hue = int(cv2.cvtColor(np.uint8([[colour]]), cv2.COLOR_BGR2HSV)[0][0][0])
            lo, hi = (hue - 10) % 180, (hue + 10) % 180
            if lo <= hi:
                mask = cv2.inRange(hsv, (lo, 90, 70), (hi, 255, 255))
            else:                      # red wraps past 180
                mask = cv2.inRange(hsv, (0, 90, 70), (hi, 255, 255)) | \
                       cv2.inRange(hsv, (lo, 90, 70), (179, 255, 255))

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < self.min_area:
                    continue
                x, y, w, h = cv2.boundingRect(contour)
                fill = area / float(max(w * h, 1))          # stands in for confidence
                found.append(Detection(cls_id, name, round(min(0.99, 0.55 + 0.45 * fill), 2),
                                       (x, y, x + w, y + h), None))

        threshold = conf or self.conf
        found = [d for d in found if d.conf >= threshold]
        return self._tracker.assign(found) if track else found


class CentroidTracker:
    """Nearest-centroid ID assignment.

    ponytail: greedy nearest-match, no motion model, no re-identification. Good enough
    to exercise unique-counting with the mock detector. The real runs use ByteTrack via
    ultralytics; if the mock ever needs better, port ByteTrack rather than growing this.
    """

    def __init__(self, max_distance=90):
        self.max_distance = max_distance
        self.next_id = 1
        self.tracks = {}            # id -> (cx, cy, cls_id)

    @staticmethod
    def _centre(det):
        x1, y1, x2, y2 = det.xyxy
        return (x1 + x2) / 2.0, (y1 + y2) / 2.0

    def assign(self, detections):
        out, claimed = [], set()
        for det in detections:
            cx, cy = self._centre(det)
            best, best_dist = None, self.max_distance
            for tid, (tx, ty, tcls) in self.tracks.items():
                if tid in claimed or tcls != det.cls_id:
                    continue
                dist = ((cx - tx) ** 2 + (cy - ty) ** 2) ** 0.5
                if dist < best_dist:
                    best, best_dist = tid, dist
            if best is None:
                best = self.next_id
                self.next_id += 1
            claimed.add(best)
            self.tracks[best] = (cx, cy, det.cls_id)
            out.append(det._replace(track_id=best))
        return out


def load(cfg_model: dict):
    """Build the detector named in the config. Falls back to mock, loudly, never silently."""
    path = str(cfg_model.get("path", "")).strip()
    classes = cfg_model.get("classes")

    if path.lower() in {"", "mock", "none"}:
        print("[OceanEye] MOCK detector — no weights loaded. Pipeline test only.")
        return MockDetector(classes=classes, conf=cfg_model.get("conf", 0.35))

    try:
        return YoloDetector(
            path,
            conf=cfg_model.get("conf", 0.35),
            iou=cfg_model.get("iou", 0.45),
            imgsz=cfg_model.get("imgsz", 640),
            device=cfg_model.get("device", ""),
            tracker=cfg_model.get("tracker", "bytetrack.yaml"),
        )
    except ImportError:
        print("[OceanEye] WARNING: ultralytics is not installed — falling back to MOCK.")
        print("[OceanEye]          pip install ultralytics")
    except Exception as exc:                       # bad path, corrupt weights, no torch
        print(f"[OceanEye] WARNING: could not load '{path}' ({exc}) — falling back to MOCK.")
    return MockDetector(classes=classes, conf=cfg_model.get("conf", 0.35))


# ---------------------------------------------------------------------------


class Counter:
    """Per-species totals. Unique individuals need tracking; frame counts do not.

    'Total Counts' per species is what the advisor's reference system shows, so it is
    the baseline the judges expect to see on screen.
    """

    def __init__(self):
        self.frame_counts = defaultdict(int)     # last frame, per species
        self.unique_ids = defaultdict(set)       # species -> set of track ids
        self.conf_sum = defaultdict(float)
        self.conf_n = defaultdict(int)

    def update(self, detections):
        self.frame_counts = defaultdict(int)
        for det in detections:
            self.frame_counts[det.cls_name] += 1
            self.conf_sum[det.cls_name] += det.conf
            self.conf_n[det.cls_name] += 1
            if det.track_id is not None:
                self.unique_ids[det.cls_name].add(det.track_id)

    def mean_conf(self, species):
        n = self.conf_n[species]
        return self.conf_sum[species] / n if n else 0.0

    @property
    def total_unique(self):
        return sum(len(ids) for ids in self.unique_ids.values())

    def hud_lines(self, tracking):
        lines = []
        species = sorted(set(self.frame_counts) | set(self.unique_ids))
        for name in species:
            colour = vision.colour_for(name)
            if tracking:
                lines.append((f"{name}: {len(self.unique_ids[name])} total "
                              f"({self.frame_counts[name]} now)", colour))
            else:
                lines.append((f"{name}: {self.frame_counts[name]}", colour))
        return lines

    def summary(self):
        species = sorted(set(self.conf_n) | set(self.unique_ids))
        return {name: {"unique": len(self.unique_ids[name]),
                       "detections": self.conf_n[name],
                       "mean_conf": round(self.mean_conf(name), 3)} for name in species}
