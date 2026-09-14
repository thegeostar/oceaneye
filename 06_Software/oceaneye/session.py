"""Evidence: what happened during a run, written to disk while it happens.

Every run produces its own folder under runs/:

    runs/2026-09-12_1431/
        detections.csv   one row per detection - the raw measurement
        summary.json     per-species and per-turbidity-level totals
        settings.json    exactly which config produced this run
        snap_001.jpg     frames saved with the 's' key
        recording.mp4    if recording was on

Two reasons this exists rather than reading numbers off the screen:
the turbidity-ladder table in the slides has to be measured, not remembered, and
"we recorded every run" is a straight answer to a judge asking where a number came from.
"""

from __future__ import annotations

import csv
import json
import time
from datetime import datetime
from pathlib import Path

import cv2

CSV_COLUMNS = ["frame", "t_sec", "level", "enhance", "turbid", "conf_thres",
               "species", "conf", "track_id", "x1", "y1", "x2", "y2", "fps"]


class Session:
    def __init__(self, outdir="runs", name=None, log=True, settings=None):
        self.root = Path(outdir) / (name or datetime.now().strftime("%Y-%m-%d_%H%M%S"))
        self.root.mkdir(parents=True, exist_ok=True)
        self.started = time.time()
        self.enabled = log
        self.snapshots = 0
        self.frames = 0
        self.writer = None
        self.video_path = None
        self._fh = None
        self._csv = None
        # level -> {"detections": n, "conf_sum": x, "frames": n}
        self.levels = {}

        if settings is not None:
            (self.root / "settings.json").write_text(json.dumps(settings, indent=2, default=str))

        if self.enabled:
            self._fh = (self.root / "detections.csv").open("w", newline="")
            self._csv = csv.writer(self._fh)
            self._csv.writerow(CSV_COLUMNS)

    # -- logging ------------------------------------------------------------

    def log(self, frame_idx, detections, level="L0", enhance=True, turbid=False,
            conf_thres=0.0, fps=0.0):
        """One CSV row per detection, plus running per-level statistics."""
        self.frames += 1
        stats = self.levels.setdefault(level, {"detections": 0, "conf_sum": 0.0, "frames": 0})
        stats["frames"] += 1
        stats["detections"] += len(detections)
        stats["conf_sum"] += sum(d.conf for d in detections)

        if not self.enabled:
            return
        elapsed = round(time.time() - self.started, 3)
        for det in detections:
            x1, y1, x2, y2 = (round(float(v), 1) for v in det.xyxy)
            self._csv.writerow([frame_idx, elapsed, level, int(enhance), int(turbid),
                                round(conf_thres, 2), det.cls_name, round(det.conf, 3),
                                det.track_id, x1, y1, x2, y2, round(fps, 1)])

    # -- artefacts ----------------------------------------------------------

    def snapshot(self, frame):
        self.snapshots += 1
        path = self.root / f"snap_{self.snapshots:03d}.jpg"
        cv2.imwrite(str(path), frame)
        return path

    def start_recording(self, frame, fps=25.0, filename="recording.mp4"):
        """Start writing annotated video. This is how the stage backup gets made."""
        if self.writer is not None:
            return self.video_path
        h, w = frame.shape[:2]
        if not fps or fps <= 0 or fps > 240:
            fps = 25.0
        self.video_path = self.root / filename
        self.writer = cv2.VideoWriter(str(self.video_path),
                                      cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
        if not self.writer.isOpened():
            self.writer = None
            print(f"[OceanEye] ERROR: cannot write video to {self.video_path}")
            return None
        return self.video_path

    def stop_recording(self):
        if self.writer is not None:
            self.writer.release()
            self.writer = None
            print(f"[OceanEye] recording saved: {self.video_path}")
        return self.video_path

    def write_frame(self, frame):
        if self.writer is not None:
            self.writer.write(frame)

    @property
    def recording(self):
        return self.writer is not None

    # -- finishing ----------------------------------------------------------

    def level_table(self):
        """The turbidity ladder, ready to paste into the slides."""
        rows = []
        for level in sorted(self.levels):
            stats = self.levels[level]
            n = stats["detections"]
            rows.append({
                "level": level,
                "frames": stats["frames"],
                "detections": n,
                "per_frame": round(n / stats["frames"], 2) if stats["frames"] else 0.0,
                "mean_conf": round(stats["conf_sum"] / n, 3) if n else 0.0,
            })
        return rows

    def close(self, counter=None, extra=None):
        self.stop_recording()
        if self._fh is not None:
            self._fh.close()

        summary = {
            "run": self.root.name,
            "duration_sec": round(time.time() - self.started, 1),
            "frames": self.frames,
            "by_level": self.level_table(),
            "by_species": counter.summary() if counter else {},
        }
        if extra:
            summary.update(extra)
        (self.root / "summary.json").write_text(json.dumps(summary, indent=2))
        return summary


def print_summary(summary):
    """Console report at the end of a run. Read these numbers into the slides."""
    print("\n" + "=" * 62)
    print(f"  RUN: {summary['run']}   {summary['frames']} frames   "
          f"{summary['duration_sec']}s")
    print("=" * 62)

    species = summary.get("by_species") or {}
    if species:
        print(f"  {'species':<16}{'unique':>8}{'detections':>12}{'mean conf':>11}")
        for name, s in species.items():
            print(f"  {name:<16}{s['unique']:>8}{s['detections']:>12}{s['mean_conf']:>11.3f}")

    levels = summary.get("by_level") or []
    if levels:
        print("\n  turbidity ladder")
        print(f"  {'level':<8}{'frames':>8}{'detections':>12}{'per frame':>11}{'mean conf':>11}")
        for row in levels:
            print(f"  {row['level']:<8}{row['frames']:>8}{row['detections']:>12}"
                  f"{row['per_frame']:>11.2f}{row['mean_conf']:>11.3f}")
    print("=" * 62)
