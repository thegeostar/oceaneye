"""Does contrast enhancement before the detector help? Measured, not assumed.

    python bench_enhance.py

This is the evidence behind `ENHANCE = False` in app/predict_video.py and behind the
turbidity slide. It asserts the two findings that decide the design, so if either
stops being true the script fails instead of quietly misleading a slide.

Two experiments:

1. REAL footage, no simulation — 4 URPC images and one underwater video as shipped.
   Enhancement lost detections: 60 -> 54, and 003045.jpg alone went 7 -> 3. On the
   video alone it was a wash (38 -> 39), so the whole loss is in the stills.

2. A simulated turbidity sweep, to find where that flips. It flips between L1 and L2:
   below it enhancement destroys detections, above it enhancement is the only reason
   there are any.

Gray-world white balance was measured as a third arm and lost to CLAHE alone at every
turbidity level, so it is not in the app and no longer has an arm here. Only the CLAHE
half shipped.

No ground-truth labels, so this reports detection count and mean confidence, not mAP.
Turbidity is simulated with the image-formation model, not real clay —
**re-run against real tank footage before quoting numbers on stage.**
"""
import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "app"))
from predict_video import enhance as app_enhance, load_model  # noqa: E402
import predict_video  # noqa: E402

IMAGES = ("000013.jpg", "003045.jpg", "test_000080.jpg", "test_000183.jpg")
# OceanEye: cv_966.mp4 was listed here and is not in the repo, so it was skipped in
# silence and the printed totals no longer matched the ones quoted above. Dropped.
VIDEOS = ("URPC_test_video.mp4",)


def enhanced(frame):
    """Force the app's own enhance() on, so this measures what ships."""
    was, predict_video.ENHANCE = predict_video.ENHANCE, True
    try:
        return app_enhance(frame)
    finally:
        predict_video.ENHANCE = was


def turbid(img, depth):
    """I = J*t + B*(1-t). beta is BGR; red is absorbed fastest, so index 2 is largest."""
    if depth <= 0:
        return img
    beta, veil = (0.25, 0.4, 0.9), (150, 140, 90)
    out = img.astype(np.float32)
    for c in range(3):
        t = np.exp(-beta[c] * depth)
        out[:, :, c] = out[:, :, c] * t + veil[c] * (1 - t)
    return np.clip(out, 0, 255).astype(np.uint8)


def score(model, img):
    r = model.predict(img, verbose=False)[0]
    if r.boxes is None or len(r.boxes) == 0:
        return 0, 0.0
    c = r.boxes.conf.tolist()
    return len(c), sum(c) / len(c)


def frames(path, n=12):
    cap = cv2.VideoCapture(str(path))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
    for i in range(n):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(i * total / n))
        ok, f = cap.read()
        if ok:
            yield f
    cap.release()


def real_footage(model, up):
    print("1. REAL footage, as shipped\n")
    print(f"{'source':<32} {'raw n':>6} {'raw c':>7} {'enh n':>6} {'enh c':>7}")
    print("-" * 62)
    raw_n = enh_n = 0
    for name in IMAGES:
        p = up / name
        # loud, not silent: a missing fixture shrinks the totals below, and a total that
        # quietly disagrees with the one in the docstring is how a slide goes stale
        assert p.exists(), f"missing test image {p}"
        img = cv2.imread(str(p))
        a, b = score(model, img)
        c, d = score(model, enhanced(img))
        print(f"{name:<32} {a:>6} {b:>7.3f} {c:>6} {d:>7.3f}")
        raw_n += a
        enh_n += c
    for name in VIDEOS:
        p = up / name
        # the videos are too big for the repo and live in the shared Drive folder, so a
        # fresh clone legitimately has none. Say so rather than shrinking the totals
        # behind the reader's back.
        if not p.exists():
            print(f"{name + ' (not present, skipped)':<32}")
            continue
        a = c = 0
        for f in frames(p):
            a += score(model, f)[0]
            c += score(model, enhanced(f))[0]
        print(f"{name + ' (12 frames)':<32} {a:>6} {'':>7} {c:>6}")
        raw_n += a
        enh_n += c
    print("-" * 62)
    print(f"{'TOTAL':<32} {raw_n:>6} {'':>7} {enh_n:>6}\n")
    assert enh_n < raw_n, (
        f"enhancement no longer hurts on clear footage ({raw_n} -> {enh_n}). "
        "If this is genuinely better, ENHANCE may now default to True — but "
        "re-check the turbidity sweep below before changing it.")
    return raw_n, enh_n


def ladder(model, up):
    print("2. Simulated turbidity sweep\n")
    imgs = [cv2.imread(str(up / n)) for n in IMAGES]
    imgs = [i for i in imgs if i is not None]
    assert imgs, f"no test images found in {up}"

    print(f"{'turbidity':<12} {'raw n':>6} {'raw c':>7} | {'CLAHE n':>8} {'CLAHE c':>8}")
    print("-" * 50)
    rows = {}
    for label, depth in [("L0 clear", 0), ("L1", 0.7), ("L2", 1.4),
                         ("L3", 2.2), ("L4 extreme", 3.0)]:
        out = []
        for fn in (lambda x: x, enhanced):
            n, cs = 0, []
            for img in imgs:
                a, b = score(model, fn(turbid(img, depth)))
                n += a
                if a:
                    cs.append(b)
            out += [n, sum(cs) / len(cs) if cs else 0.0]
        rows[label] = out
        print(f"{label:<12} {out[0]:>6} {out[1]:>7.3f} | {out[2]:>8} {out[3]:>8.3f}")
    return rows


def main():
    model = load_model()
    up = HERE / "app" / "upload"
    real_footage(model, up)
    rows = ladder(model, up)

    clear, murky = rows["L0 clear"], rows["L4 extreme"]
    assert clear[0] > clear[2], (
        f"enhancement must LOSE detections in clear water ({clear[0]} vs {clear[2]}); "
        "that is the whole reason ENHANCE defaults to False.")
    assert murky[2] > murky[0], (
        f"enhancement must WIN in heavy turbidity ({murky[0]} vs {murky[2]}); "
        "if it no longer does, the toggle earns nothing and should be deleted.")
    assert predict_video.ENHANCE is False, "ENHANCE must ship defaulting to False"

    print(f"\nOK — enhancement costs {clear[0] - clear[2]} detections when clear, "
          f"and recovers {murky[2] - murky[0]} when heavily turbid.")
    print("Toggle justified, default OFF. Re-measure on real tank footage.")


if __name__ == "__main__":
    main()
