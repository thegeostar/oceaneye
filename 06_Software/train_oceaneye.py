#!/usr/bin/env python3
"""Fine-tuning: dataset preparation, auto-labelling, and the training run.

Separate from oceaneye_demo.py on purpose. Nothing here runs on stage; this file
is used two or three times all week and then never again.

The order you will actually use it in:

    # 1. DUO (VOC XML) or Brackish (already YOLO) -> a dataset ultralytics can read.
    #    Always renders check_*.jpg samples. LOOK AT THEM before training.
    python train_oceaneye.py prep ../08_Data/datasets/DUO

    # 2. Fine-tune from pretrained weights. Never from scratch.
    python train_oceaneye.py train ../08_Data/datasets/DUO/oceaneye.yaml

    # 3. Later, with tank footage: pre-label it with the model you just trained,
    #    correct the mistakes by hand, then run `train` again on the result.
    python train_oceaneye.py autolabel ../08_Data/footage/run1.mp4

Runs the same way in a terminal or in Google Colab (`!python train_oceaneye.py ...`).
A notebook was deliberately not used: one command is fewer moving parts than twelve
cells that must be run in the right order.
"""

from __future__ import annotations

import argparse
import json
import random
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import cv2

from oceaneye import capture, detect, vision

# Fixed order, shared with the demo so a class id means the same thing everywhere
# and each species keeps its colour on screen and in the slides.
CLASSES = list(vision.SPECIES_COLOURS)

# DUO/URPC annotations are not always spelled the way our class list is.
ALIASES = {
    "holothurian": "holothurian", "sea cucumber": "holothurian", "seacucumber": "holothurian",
    "echinus": "echinus", "sea urchin": "echinus", "seaurchin": "echinus", "urchin": "echinus",
    "scallop": "scallop",
    "starfish": "starfish", "star fish": "starfish", "asteroidea": "starfish",
}

IMAGE_SUFFIXES = capture.IMAGE_SUFFIXES


def class_id(raw: str):
    """Map an annotation's class name onto our fixed list. None = a class we ignore."""
    key = str(raw).strip().lower()
    name = ALIASES.get(key, key)
    return CLASSES.index(name) if name in CLASSES else None


# ---------------------------------------------------------------------------
# VOC XML -> YOLO txt
# ---------------------------------------------------------------------------


def voc_to_yolo(xml_path):
    """Return (image_filename, [(cls_id, cx, cy, w, h), ...]) with values normalised 0-1.

    YOLO wants the box CENTRE and its size, as a fraction of the image. VOC gives
    opposite CORNERS in pixels. Getting this conversion wrong produces labels that
    look plausible in a text file and are visibly wrong on an image - which is why
    `prep` always renders samples afterwards.
    """
    root = ET.parse(xml_path).getroot()
    size = root.find("size")
    width = float(size.findtext("width", 0))
    height = float(size.findtext("height", 0))
    if width <= 0 or height <= 0:
        raise ValueError(f"{xml_path.name}: no usable <size>")

    rows = []
    for obj in root.findall("object"):
        cid = class_id(obj.findtext("name", ""))
        if cid is None:
            continue
        box = obj.find("bndbox")
        x1 = float(box.findtext("xmin", 0))
        y1 = float(box.findtext("ymin", 0))
        x2 = float(box.findtext("xmax", 0))
        y2 = float(box.findtext("ymax", 0))
        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))
        # Some URPC boxes run a pixel or two past the edge. Clamp, do not discard.
        x1, x2 = max(x1, 0.0), min(x2, width)
        y1, y2 = max(y1, 0.0), min(y2, height)
        if x2 - x1 < 1 or y2 - y1 < 1:
            continue
        rows.append((cid,
                     ((x1 + x2) / 2) / width,
                     ((y1 + y2) / 2) / height,
                     (x2 - x1) / width,
                     (y2 - y1) / height))
    return root.findtext("filename", "") or xml_path.stem, rows


def read_source_names(root: Path):
    """Class names from a dataset's own data.yaml, in source index order.

    A Roboflow export uses ITS class ids, not ours - Brackish has fish, crab and
    jellyfish in it. Copying those numbers across unchanged would train the model on
    confidently wrong labels, so the names are read and remapped instead.

    Only the `names:` block is parsed, in all three shapes ultralytics accepts, which
    is why this does not need pyyaml.
    """
    for candidate in ("data.yaml", "data.yml"):
        for path in sorted(root.rglob(candidate)):
            text = path.read_text()
            names, collecting = [], False
            for line in text.split("\n"):
                stripped = line.strip()
                if stripped.startswith("names:"):
                    inline = stripped[len("names:"):].strip()
                    if inline.startswith("["):          # names: ['a', 'b']
                        return [n.strip(" '\"") for n in inline.strip("[]").split(",") if n.strip()]
                    collecting = True
                    continue
                if collecting:
                    if stripped.startswith("- "):       # - a
                        names.append(stripped[2:].strip(" '\""))
                    elif ":" in stripped and stripped.split(":")[0].strip().isdigit():
                        names.append(stripped.split(":", 1)[1].strip(" '\""))
                    elif stripped and not line.startswith((" ", "\t", "-")):
                        break                           # next top-level key
            if names:
                return names
    return None


def find_images(root: Path):
    """Every image under root, by stem, skipping anything we generated ourselves."""
    out = {}
    for path in root.rglob("*"):
        if path.suffix.lower() in IMAGE_SUFFIXES and "oceaneye_yolo" not in path.parts:
            out.setdefault(path.stem, path)
    return out


def write_yaml(path: Path, root: Path):
    """data.yaml, the file ultralytics actually reads. Paths are absolute to survive Colab."""
    lines = [
        "# Generated by train_oceaneye.py - safe to regenerate, do not hand-edit.",
        f"path: {root.resolve()}",
        f"train: {(root / 'train' / 'images').resolve()}",
        f"val: {(root / 'val' / 'images').resolve()}",
        f"nc: {len(CLASSES)}",
        "names:",
    ]
    lines += [f"  {i}: {name}" for i, name in enumerate(CLASSES)]
    path.write_text("\n".join(lines) + "\n")
    return path


def render_checks(images_dir: Path, labels_dir: Path, outdir: Path, count=5):
    """Draw the converted labels back onto the images.

    This is the gate, not a nicety. It is the only cheap way to catch a coordinate
    mistake before it silently poisons a training run.
    """
    outdir.mkdir(parents=True, exist_ok=True)
    labelled = [p for p in sorted(labels_dir.glob("*.txt")) if p.stat().st_size > 0]
    if not labelled:
        return []

    random.Random(22).shuffle(labelled)
    written = []
    for label_path in labelled[:count]:
        matches = [p for p in images_dir.glob(f"{label_path.stem}.*")
                   if p.suffix.lower() in IMAGE_SUFFIXES]
        if not matches:
            continue
        frame = cv2.imread(str(matches[0]))
        if frame is None:
            continue
        h, w = frame.shape[:2]
        dets = []
        for line in label_path.read_text().split("\n"):
            parts = line.split()
            if len(parts) != 5:
                continue
            cid, cx, cy, bw, bh = int(parts[0]), *(float(v) for v in parts[1:])
            dets.append(detect.Detection(
                cid, CLASSES[cid] if cid < len(CLASSES) else str(cid), 1.0,
                ((cx - bw / 2) * w, (cy - bh / 2) * h,
                 (cx + bw / 2) * w, (cy + bh / 2) * h), None))
        out = outdir / f"check_{label_path.stem}.jpg"
        cv2.imwrite(str(out), vision.draw_detections(frame, dets, show_conf=False))
        written.append(out)
    return written


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_prep(args):
    root = Path(args.dataset)
    if not root.is_dir():
        print(f"[prep] ERROR: not a folder: {root}")
        return 1

    xmls = [p for p in root.rglob("*.xml") if "oceaneye_yolo" not in p.parts]
    existing = [p for p in root.rglob("*.txt")
                if p.parent.name == "labels" and "oceaneye_yolo" not in p.parts]

    if not xmls and not existing:
        print(f"[prep] ERROR: found no .xml annotations and no labels/*.txt under {root}")
        print("[prep]        Is the archive extracted? Expected VOC XML (DUO) or "
              "YOLO labels/ (Roboflow).")
        return 1

    out = root / "oceaneye_yolo"
    if out.exists():
        shutil.rmtree(out)
    pairs = []

    if xmls:
        print(f"[prep] VOC format: {len(xmls)} annotation files")
        images = find_images(root)
        skipped = 0
        for xml_path in xmls:
            try:
                filename, rows = voc_to_yolo(xml_path)
            except (ET.ParseError, ValueError):
                skipped += 1
                continue
            image = images.get(Path(filename).stem) or images.get(xml_path.stem)
            if image is None:
                skipped += 1
                continue
            pairs.append((image, rows))
        if skipped:
            print(f"[prep] skipped {skipped} annotations with no matching image or bad XML")
    else:
        print(f"[prep] already YOLO format: {len(existing)} label files")
        source_names = read_source_names(root)
        if source_names is None:
            print("[prep] WARNING: no data.yaml found, so the source class ids are ASSUMED "
                  "to match ours.")
            print(f"[prep]          Ours are {dict(enumerate(CLASSES))}. If the dataset uses "
                  "any other order, the labels are wrong.")
            remap = None
        else:
            remap = {i: class_id(name) for i, name in enumerate(source_names)}
            kept = {source_names[i]: CLASSES[v] for i, v in remap.items() if v is not None}
            dropped = [source_names[i] for i, v in remap.items() if v is None]
            print(f"[prep] source classes: {source_names}")
            print(f"[prep] kept: {kept or 'NONE'}")
            if dropped:
                print(f"[prep] dropped (not one of our four species): {dropped}")
            if not kept:
                print("[prep] ERROR: none of this dataset's classes are our species. "
                      "Wrong dataset?")
                return 1

        for label_path in existing:
            image_dir = label_path.parent.parent / "images"
            matches = [p for p in image_dir.glob(f"{label_path.stem}.*")
                       if p.suffix.lower() in IMAGE_SUFFIXES]
            if not matches:
                continue
            rows = []
            for line in label_path.read_text().split("\n"):
                parts = line.split()
                if len(parts) != 5:
                    continue
                source_id = int(parts[0])
                cid = source_id if remap is None else remap.get(source_id)
                if cid is None:
                    continue
                rows.append((cid, *(float(v) for v in parts[1:])))
            pairs.append((matches[0], rows))

    if not pairs:
        print("[prep] ERROR: could not pair a single annotation with an image.")
        return 1

    # Deterministic split, so a re-run does not quietly move images between
    # train and val and make two training runs incomparable.
    random.Random(22).shuffle(pairs)
    cut = max(1, int(len(pairs) * (1 - args.val_split)))
    splits = {"train": pairs[:cut], "val": pairs[cut:]}

    boxes = 0
    per_class = dict.fromkeys(CLASSES, 0)
    for split, items in splits.items():
        (out / split / "images").mkdir(parents=True, exist_ok=True)
        (out / split / "labels").mkdir(parents=True, exist_ok=True)
        for image, rows in items:
            dest = out / split / "images" / image.name
            if args.copy_images:
                shutil.copy2(image, dest)
            else:
                try:
                    dest.symlink_to(image.resolve())
                except OSError:                      # Windows without developer mode
                    shutil.copy2(image, dest)
            text = "\n".join(f"{cid} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}"
                             for cid, cx, cy, bw, bh in rows)
            (out / split / "labels" / f"{dest.stem}.txt").write_text(text + ("\n" if text else ""))
            boxes += len(rows)
            for cid, *_ in rows:
                if cid < len(CLASSES):
                    per_class[CLASSES[cid]] += 1

    yaml_path = write_yaml(root / "oceaneye.yaml", out)
    (out / "preprocessing.json").write_text(json.dumps({
        "enhanced_at_training": False,
        "rule": "Inference must use the same preprocessing as training "
                "(Core_Strategy_Data_Quality.md §4).",
        "action": "This dataset is RAW. Keep display.enhance = false in the profile you "
                  "demo with, or use enhancement for visualisation only.",
    }, indent=2))

    print(f"[prep] train {len(splits['train'])} · val {len(splits['val'])} · {boxes} boxes")
    for name, n in per_class.items():
        print(f"[prep]   {name:<14}{n:>7}")
        if n == 0:
            print(f"[prep]   ^^ WARNING: no boxes for {name}. Check the source class names.")
    print(f"[prep] wrote {yaml_path}")

    checks = render_checks(out / "train" / "images", out / "train" / "labels", out / "checks")
    print(f"\n[prep] 🔴 OPEN THESE {len(checks)} IMAGES BEFORE YOU TRAIN:")
    for path in checks:
        print(f"[prep]   {path}")
    print("[prep] Boxes must sit ON the animals. If they are offset, shifted or the "
          "wrong size, STOP - training on bad labels wastes the whole day.\n")
    return 0


def cmd_train(args):
    try:
        from ultralytics import YOLO
    except ImportError:
        print("[train] ERROR: ultralytics is not installed.\n"
              "[train]        pip install ultralytics")
        return 1

    data = Path(args.data)
    if not data.exists():
        print(f"[train] ERROR: no such data yaml: {data}   (run `prep` first)")
        return 1

    note = data.parent / "oceaneye_yolo" / "preprocessing.json"
    if note.exists():
        info = json.loads(note.read_text())
        print(f"[train] preprocessing: {info['action']}")

    print(f"[train] fine-tuning {args.model} -> {args.epochs} epochs, imgsz {args.imgsz}")
    print("[train] starting from PRETRAINED weights (transfer learning), not from scratch.")

    model = YOLO(args.model)
    model.train(data=str(data.resolve()), epochs=args.epochs, imgsz=args.imgsz,
                batch=args.batch, device=args.device or None, patience=args.patience,
                project=args.project, name=args.name, exist_ok=True, verbose=True)

    best = Path(model.trainer.best)
    metrics = model.val(data=str(data.resolve()), imgsz=args.imgsz, verbose=False)

    dest = Path(args.out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(best, dest)

    print("\n" + "=" * 62)
    print(f"  mAP50     {metrics.box.map50:.4f}   <- this is the number you say on stage")
    print(f"  mAP50-95  {metrics.box.map:.4f}")
    print("=" * 62)
    for i, name in enumerate(CLASSES):
        try:
            print(f"  {name:<14}mAP50 {metrics.box.ap50[i]:.4f}")
        except (IndexError, TypeError):
            pass
    print("=" * 62)
    print(f"  weights: {dest}")
    print(f"  run it:  python oceaneye_demo.py --profile endoscope --model {dest}")
    print("  🔴 copy best.pt to TWO USB sticks now, not later.")
    print("=" * 62 + "\n")
    return 0


def cmd_autolabel(args):
    """Pre-label your own footage with an existing model, so a human only corrects.

    Core_Strategy §5: 200-300 frames from your actual tank beats thousands of foreign
    images for your demo. Labelling those by hand is hours; correcting them is minutes.
    """
    out = Path(args.out)
    (out / "images").mkdir(parents=True, exist_ok=True)
    (out / "labels").mkdir(parents=True, exist_ok=True)

    detector = detect.load({"path": args.model, "conf": args.conf, "classes": CLASSES})
    if detector.is_mock:
        print("[autolabel] ERROR: no real model loaded - mock labels are worthless here.")
        print("[autolabel]        pass --model ../08_Data/weights/best.pt")
        return 1

    cap = capture.Capture({"source": args.source, "width": 1280, "height": 720,
                           "fps": 30, "fourcc": "MJPG", "backend": "auto", "flip": "",
                           "warmup_frames": 0, "controls": {}})
    index = kept = empty = 0
    try:
        while kept < args.limit:
            ok, frame = cap.read()
            if not ok:
                break
            index += 1
            if index % args.every:
                continue
            dets = detector.infer(frame, track=False, conf=args.conf)
            if not dets:
                empty += 1
                continue
            stem = f"{Path(str(args.source)).stem}_{index:06d}"
            cv2.imwrite(str(out / "images" / f"{stem}.jpg"), frame)
            h, w = frame.shape[:2]
            rows = []
            for det in dets:
                x1, y1, x2, y2 = det.xyxy
                rows.append(f"{det.cls_id} {((x1 + x2) / 2) / w:.6f} {((y1 + y2) / 2) / h:.6f} "
                            f"{(x2 - x1) / w:.6f} {(y2 - y1) / h:.6f}")
            (out / "labels" / f"{stem}.txt").write_text("\n".join(rows) + "\n")
            kept += 1
    finally:
        cap.release()

    print(f"[autolabel] {kept} frames written to {out}  ({empty} had no detections, skipped)")
    print("[autolabel] 🔴 These labels are GUESSES. Open them in a labelling tool "
          "(labelImg, Label Studio, Roboflow), fix the mistakes, then run `prep` and `train`.")
    print("[autolabel] Say so on stage: fine-tuning on your own deployment data is "
          "domain adaptation, and it is standard practice - not something to hide.")
    return 0


# ---------------------------------------------------------------------------


def build_parser():
    ap = argparse.ArgumentParser(
        description="OceanEye dataset prep and fine-tuning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("prep", help="convert a dataset to YOLO format and render label checks")
    p.add_argument("dataset", help="folder holding the extracted dataset")
    p.add_argument("--val-split", type=float, default=0.15)
    p.add_argument("--copy-images", action="store_true",
                   help="copy instead of symlink (needed on some Windows setups)")
    p.set_defaults(func=cmd_prep)

    p = sub.add_parser("train", help="fine-tune from pretrained weights")
    p.add_argument("data", help="the oceaneye.yaml written by prep")
    # yolov8n because the advisor's script claims "improved YOLOv8" and what you say
    # on stage must match what you ran. Same ultralytics API as v11, so this is not a
    # framework switch (see PROJECT_CONTEXT D2).
    p.add_argument("--model", default="yolov8n.pt", help="pretrained starting weights")
    p.add_argument("--epochs", type=int, default=60)
    p.add_argument("--imgsz", type=int, default=640)
    p.add_argument("--batch", type=int, default=16, help="lower it if you run out of memory")
    p.add_argument("--device", default="", help="'' auto · cpu · 0 · cuda:0")
    p.add_argument("--patience", type=int, default=15, help="stop early if it plateaus")
    p.add_argument("--project", default="../08_Data/training")
    p.add_argument("--name", default="oceaneye")
    p.add_argument("--out", default="../08_Data/weights/best.pt")
    p.set_defaults(func=cmd_train)

    p = sub.add_parser("autolabel", help="pre-label your own footage with a trained model")
    p.add_argument("source", help="video file, folder of images, or camera index")
    p.add_argument("--model", default="../08_Data/weights/best.pt")
    p.add_argument("--every", type=int, default=10, help="keep every Nth frame")
    p.add_argument("--limit", type=int, default=300, help="stop after N kept frames")
    p.add_argument("--conf", type=float, default=0.25)
    p.add_argument("--out", default="../08_Data/datasets/own_rig")
    p.set_defaults(func=cmd_autolabel)
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
