# OceanEye: the proof that the model actually works on this laptop.
#
# Runs best.pt on one of Prof. Wang's own sample images and prints what it found.
# Her result for 000013.jpg is shipped in app/static/000013_detected.jpg and shows
# holothurian 0.78 and starfish 0.83. Ours should match.
#
#   python verify_model.py                     # her sample
#   python verify_model.py path/to/other.jpg   # anything else

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ultralytics import YOLO

WEIGHTS = "output_dir/mscoco/mambayolo_n/weights/best.pt"
image = sys.argv[1] if len(sys.argv) > 1 else "app/upload/000013.jpg"

print(f"weights : {WEIGHTS}")
print(f"image   : {image}")

model = YOLO(WEIGHTS)

t = time.time()
result = model(image, verbose=False)[0]
elapsed = time.time() - t

print(f"\ninference: {elapsed:.2f} s")
print(f"detections: {len(result.boxes)}")
for cls, conf in sorted(zip(result.boxes.cls.tolist(), result.boxes.conf.tolist()),
                        key=lambda z: -z[1]):
    print(f"   {result.names[int(cls)]:<14} {conf:.2f}")

out = "proof.jpg"
result.save(out)
print(f"\nsaved {out}")
print("compare against app/static/000013_detected.jpg — the boxes should match")
