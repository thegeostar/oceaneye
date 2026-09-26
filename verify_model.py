"""Check that the model loads and reproduces the reference detections.

    python verify_model.py                  # reference image, must match
    python verify_model.py photo.jpg        # any image at the default threshold
    python verify_model.py photo.jpg 0.05   # lower the threshold to show weak detections
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ultralytics import YOLO  # noqa: E402

WEIGHTS = os.path.join(HERE, 'model', 'best.pt')
REFERENCE = os.path.join(HERE, 'app', 'upload', '000013.jpg')
EXPECTED = {'starfish': 0.83, 'holothurian': 0.78}

image = sys.argv[1] if len(sys.argv) > 1 else REFERENCE
conf = float(sys.argv[2]) if len(sys.argv) > 2 else 0.25

model = YOLO(WEIGHTS)
model(image, verbose=False, conf=conf)  # warm-up: the first call includes CUDA setup

start = time.time()
result = model(image, verbose=False, conf=conf)[0]
print(f'inference: {time.time() - start:.2f} s')
print(f'detections: {len(result.boxes)}')
found = {}
for cls, score in sorted(zip(result.boxes.cls.tolist(), result.boxes.conf.tolist()),
                         key=lambda z: -z[1]):
    name = result.names[int(cls)]
    found.setdefault(name, score)
    print(f'   {name:<14} {score:.2f}')

out = os.path.join(HERE, 'proof.jpg')
result.save(out)
print(f'\nsaved {out}')

if image == REFERENCE and conf == 0.25:
    assert set(found) == set(EXPECTED), f'expected {sorted(EXPECTED)}, got {sorted(found)}'
    for name, expected in EXPECTED.items():
        assert abs(found[name] - expected) < 0.02, f'{name}: {found[name]:.2f}, expected {expected}'
    # A lower threshold must return at least as many boxes, or conf is not reaching the model.
    assert len(model(image, verbose=False, conf=0.01)[0].boxes) >= len(result.boxes)
    print('OK: reference detections match')
