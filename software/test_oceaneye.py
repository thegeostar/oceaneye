#!/usr/bin/env python3
"""Self-check for the OceanEye system.  Run it after any change:

    python test_oceaneye.py

Needs only numpy and opencv - no model, no camera, no internet. If this passes,
the pipeline is intact and the only thing missing is real hardware and real weights.
"""

import csv
import shutil
import tempfile
from pathlib import Path

import numpy as np

import train_oceaneye
from oceaneye import capture, config, detect, runner, session, vision


def test_gray_world_balances_channels():
    """A blue-cast image should come out with its channel means close together."""
    img = np.zeros((60, 60, 3), np.uint8)
    img[:, :, 0] = 200      # B
    img[:, :, 1] = 120      # G
    img[:, :, 2] = 40       # R
    out = vision.gray_world_white_balance(img)
    means = [out[:, :, c].mean() for c in range(3)]
    assert max(means) - min(means) < 2.0, f"channels still unbalanced: {means}"


def test_clahe_preserves_shape_and_type():
    img = (np.random.default_rng(0).random((48, 64, 3)) * 255).astype(np.uint8)
    out = vision.clahe_enhance(img)
    assert out.shape == img.shape and out.dtype == img.dtype


def test_turbidity_is_physically_ordered():
    """depth=0 changes nothing, and red must fade fastest underwater."""
    img = np.full((32, 32, 3), 200, np.uint8)

    same = vision.simulate_turbidity(img, depth=0.0)
    assert np.array_equal(same, img), "depth=0 must be a no-op"

    murky = vision.simulate_turbidity(img, depth=2.0)
    drop = [int(img[:, :, c].mean()) - int(murky[:, :, c].mean()) for c in range(3)]
    assert drop[2] > drop[1] > drop[0], f"red should fade fastest, got B,G,R drops {drop}"


def test_config_layers_and_cli_override():
    defaults = config.load()
    assert defaults["capture"]["source"] == "0"

    desk = config.load("desk")                      # resolved from profiles/ by name
    assert desk["capture"]["source"] == "synthetic"
    assert desk["model"]["path"] == "mock"
    assert desk["capture"]["width"] == 1280, "unspecified keys must fall back to defaults"

    class Args:                                     # stands in for argparse output
        source, model, conf = "7", None, 0.5
        imgsz = device = outdir = backup = None
        track = no_track = no_enhance = turbid = no_log = False

    merged = config.apply_cli(desk, Args())
    assert merged["capture"]["source"] == "7", "CLI must beat the profile"
    assert merged["model"]["conf"] == 0.5
    assert merged["model"]["path"] == "mock", "untouched flags must not clobber the profile"


def test_source_classification():
    assert capture.classify("synthetic")[0] == "synthetic"
    assert capture.classify("2") == ("camera", 2)
    assert capture.classify("rtsp://cam/live")[0] == "url"
    with tempfile.TemporaryDirectory() as tmp:
        img = Path(tmp) / "a.jpg"
        import cv2
        cv2.imwrite(str(img), np.zeros((8, 8, 3), np.uint8))
        assert capture.classify(str(img))[0] == "image"
        assert capture.classify(tmp)[0] == "images"


def test_synthetic_scene_and_mock_detector_agree():
    """The mock detector must find every species the synthetic scene draws."""
    cap = capture.Capture(dict(config.DEFAULTS["capture"], source="synthetic"))
    ok, frame = cap.read()
    assert ok and frame.shape[:2] == (720, 1280)

    detector = detect.MockDetector(classes=list(vision.SPECIES_COLOURS))
    found = {d.cls_name for d in detector.infer(frame)}
    assert found == set(vision.SPECIES_COLOURS), f"mock detector missed: {set(vision.SPECIES_COLOURS) - found}"
    cap.release()


def test_tracking_keeps_ids_stable():
    """A creature that drifts a little must keep its ID, or counting is meaningless."""
    tracker = detect.CentroidTracker()
    first = tracker.assign([detect.Detection(0, "scallop", 0.9, (100, 100, 140, 140), None)])
    second = tracker.assign([detect.Detection(0, "scallop", 0.9, (108, 104, 148, 144), None)])
    assert first[0].track_id == second[0].track_id, "same object got a new ID"

    far = tracker.assign([detect.Detection(0, "scallop", 0.9, (600, 600, 640, 640), None)])
    assert far[0].track_id != first[0].track_id, "a different object reused an ID"


def test_counter_separates_species():
    counter = detect.Counter()
    counter.update([
        detect.Detection(0, "scallop", 0.8, (0, 0, 10, 10), 1),
        detect.Detection(0, "scallop", 0.6, (20, 0, 30, 10), 2),
        detect.Detection(1, "starfish", 0.9, (40, 0, 50, 10), 3),
    ])
    counter.update([detect.Detection(0, "scallop", 0.7, (0, 0, 10, 10), 1)])   # same individual

    summary = counter.summary()
    assert summary["scallop"]["unique"] == 2, "one scallop was counted twice"
    assert summary["starfish"]["unique"] == 1
    assert counter.total_unique == 3
    assert abs(summary["scallop"]["mean_conf"] - 0.7) < 0.01


def test_session_writes_a_usable_csv():
    tmp = Path(tempfile.mkdtemp())
    try:
        sess = session.Session(tmp, name="unit", log=True, settings={"hello": "world"})
        dets = [detect.Detection(0, "echinus", 0.81, (1, 2, 3, 4), 5)]
        sess.log(0, dets, level="L0", conf_thres=0.35, fps=24.0)
        sess.log(1, dets, level="L2", conf_thres=0.35, fps=24.0)
        summary = sess.close(counter=detect.Counter())

        rows = list(csv.DictReader((tmp / "unit" / "detections.csv").open()))
        assert len(rows) == 2
        assert rows[0]["species"] == "echinus" and rows[0]["level"] == "L0"
        assert rows[1]["level"] == "L2", "turbidity level must be recorded per row"

        levels = {r["level"]: r for r in summary["by_level"]}
        assert set(levels) == {"L0", "L2"}
        assert abs(levels["L0"]["mean_conf"] - 0.81) < 0.01
        assert (tmp / "unit" / "settings.json").exists(), "runs must record their own config"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_voc_to_yolo_converts_corners_to_centres():
    """The conversion that silently poisons a training run if it is wrong.

    VOC gives opposite corners in pixels; YOLO wants the centre and the size as a
    fraction of the image. A known box must come back out exactly.
    """
    xml = """<annotation>
      <filename>a.jpg</filename>
      <size><width>200</width><height>100</height></size>
      <object><name>sea urchin</name>
        <bndbox><xmin>50</xmin><ymin>20</ymin><xmax>150</xmax><ymax>70</ymax></bndbox>
      </object>
      <object><name>rock</name>
        <bndbox><xmin>0</xmin><ymin>0</ymin><xmax>10</xmax><ymax>10</ymax></bndbox>
      </object>
      <object><name>starfish</name>
        <bndbox><xmin>190</xmin><ymin>90</ymin><xmax>260</xmax><ymax>140</ymax></bndbox>
      </object>
    </annotation>"""

    tmp = Path(tempfile.mkdtemp())
    try:
        path = tmp / "a.xml"
        path.write_text(xml)
        filename, rows = train_oceaneye.voc_to_yolo(path)

        assert filename == "a.jpg"
        assert len(rows) == 2, "the unknown class 'rock' must be dropped, not renumbered"

        cid, cx, cy, bw, bh = rows[0]
        assert cid == train_oceaneye.CLASSES.index("echinus"), "'sea urchin' must map to echinus"
        assert abs(cx - 0.5) < 1e-6 and abs(cy - 0.45) < 1e-6, f"centre wrong: {cx}, {cy}"
        assert abs(bw - 0.5) < 1e-6 and abs(bh - 0.5) < 1e-6, f"size wrong: {bw}, {bh}"

        # The third box runs off the edge; it must be clamped inside the image.
        _, cx, cy, bw, bh = rows[1]
        assert cx + bw / 2 <= 1.0 + 1e-9 and cy + bh / 2 <= 1.0 + 1e-9, "box not clamped"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_end_to_end_run_with_no_hardware():
    """The whole system, start to finish, on a machine with no camera and no weights."""
    tmp = Path(tempfile.mkdtemp())
    try:
        cfg = config.load("desk")
        cfg["session"]["outdir"] = str(tmp)
        summary = runner.run(cfg, headless=True, max_frames=15, run_name="e2e",
                             save_video="run.mp4")

        assert summary["frames"] == 15
        assert summary["mock"] is True, "must be flagged as mock so it is never mistaken for the model"
        assert set(summary["by_species"]) == set(vision.SPECIES_COLOURS)
        for name, stats in summary["by_species"].items():
            assert stats["unique"] >= 1, f"{name} was never tracked"
        assert (tmp / "e2e" / "detections.csv").exists()
        assert (tmp / "e2e" / "summary.json").exists()
        assert (tmp / "e2e" / "run.mp4").stat().st_size > 0, "recording never opened"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for test in tests:
        try:
            test()
            print(f"  PASS  {test.__name__}")
        except AssertionError as exc:
            failed += 1
            print(f"  FAIL  {test.__name__}: {exc}")
        except Exception as exc:
            failed += 1
            print(f"  ERROR {test.__name__}: {type(exc).__name__}: {exc}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    raise SystemExit(1 if failed else 0)
