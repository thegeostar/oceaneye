"""Measure whether CLAHE contrast enhancement helps the detector.

    python bench_enhance.py

Runs the test images through a simulated turbidity sweep, with and without enhancement,
and reports detection counts and mean confidence (there are no ground-truth labels).
It asserts that enhancement costs detections in clear water and recovers them in heavy
turbidity, which is why ENHANCE defaults to off.
"""
import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'app'))
import predict_video  # noqa: E402

IMAGES = ('000013.jpg', '003045.jpg', 'test_000080.jpg', 'test_000183.jpg')
LEVELS = [('L0 clear', 0), ('L1', 0.7), ('L2', 1.4), ('L3', 2.2), ('L4 extreme', 3.0)]


def enhanced(frame):
    """Run the app's own enhance() with the toggle forced on."""
    was, predict_video.ENHANCE = predict_video.ENHANCE, True
    try:
        return predict_video.enhance(frame)
    finally:
        predict_video.ENHANCE = was


def turbid(img, depth):
    """Simulate turbid water with I = J*t + B*(1 - t). Red (index 2 in BGR) attenuates fastest."""
    if depth <= 0:
        return img
    beta, veil = (0.25, 0.4, 0.9), (150, 140, 90)
    out = img.astype(np.float32)
    for c in range(3):
        t = np.exp(-beta[c] * depth)
        out[:, :, c] = out[:, :, c] * t + veil[c] * (1 - t)
    return np.clip(out, 0, 255).astype(np.uint8)


def score(model, images):
    """Total detections and mean confidence over a list of images."""
    confs = []
    for img in images:
        confs += model.predict(img, verbose=False, conf=predict_video.CONF)[0].boxes.conf.tolist()
    return len(confs), sum(confs) / len(confs) if confs else 0.0


def main():
    model = predict_video.load_model()
    images = [cv2.imread(str(HERE / 'app' / 'upload' / name)) for name in IMAGES]
    assert all(img is not None for img in images), 'missing test images in app/upload'

    print(f"{'turbidity':<12} {'raw n':>6} {'raw c':>7} | {'CLAHE n':>8} {'CLAHE c':>8}")
    rows = {}
    for label, depth in LEVELS:
        murky = [turbid(img, depth) for img in images]
        raw, enh = score(model, murky), score(model, [enhanced(img) for img in murky])
        rows[label] = raw[0], enh[0]
        print(f'{label:<12} {raw[0]:>6} {raw[1]:>7.3f} | {enh[0]:>8} {enh[1]:>8.3f}')

    clear, heavy = rows['L0 clear'], rows['L4 extreme']
    assert clear[0] > clear[1], f'enhancement should cost detections in clear water: {clear}'
    assert heavy[1] > heavy[0], f'enhancement should help in heavy turbidity: {heavy}'
    assert predict_video.ENHANCE is False, 'ENHANCE should default to off'
    print('OK: enhancement hurts in clear water and helps in heavy turbidity')


if __name__ == '__main__':
    main()
