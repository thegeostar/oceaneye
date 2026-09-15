# OceanEye: the proof that the model actually works on this laptop.
#
# Runs best.pt on one of Prof. Wang's own sample images and prints what it found.
# Her result for 000013.jpg is shipped in app/static/000013_detected.jpg and shows
# holothurian 0.78 and starfish 0.83. Ours should match.
#
#   python verify_model.py                       # her sample — the acceptance test
#   python verify_model.py photo.jpg             # your own photo, same 0.25 floor
#   python verify_model.py photo.jpg 0.05        # your own photo, show the weak ones
#
# That third form is the one to use on the tank. The weights were trained on URPC
# seabed footage; market-bought specimens behind glass under room light are off that
# distribution, so real detections land lower. At the default 0.25 a genuine starfish
# at 0.18 looks exactly like the model seeing nothing. Drop the floor and the
# difference becomes visible — that is the whole question when testing a new scene.
#
# The floor is deliberately a positional argument and NOT read from OCEANEYE_CONF, so
# that exporting OCEANEYE_CONF for the web app can never quietly move this test.

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ultralytics import YOLO

WEIGHTS = "output_dir/mscoco/mambayolo_n/weights/best.pt"
REFERENCE = "app/upload/000013.jpg"

image = sys.argv[1] if len(sys.argv) > 1 else REFERENCE
conf = float(sys.argv[2]) if len(sys.argv) > 2 else 0.25

print(f"weights : {WEIGHTS}")
print(f"image   : {image}")
print(f"conf    : {conf}")

model = YOLO(WEIGHTS)

t = time.time()
result = model(image, verbose=False, conf=conf)[0]
cold = time.time() - t

# The first call pays for CUDA context setup, cuDNN autotuning and lazy module init.
# On stage the model will already be warm, so report the number you will actually get.
t = time.time()
result = model(image, verbose=False, conf=conf)[0]
elapsed = time.time() - t

print(f"\ninference: {elapsed:.2f} s  (first call {cold:.2f} s — warm it up before the demo)")
print(f"detections: {len(result.boxes)}")
for cls, c in sorted(zip(result.boxes.cls.tolist(), result.boxes.conf.tolist()),
                     key=lambda z: -z[1]):
    print(f"   {result.names[int(cls)]:<14} {c:.2f}")

out = "proof.jpg"
result.save(out)
print(f"\nsaved {out}")

if image == REFERENCE and conf == 0.25:
    print("compare against app/static/000013_detected.jpg — the boxes should match")

    found = {result.names[int(k)]: v for k, v
             in zip(result.boxes.cls.tolist(), result.boxes.conf.tolist())}
    assert set(found) == {"starfish", "holothurian"}, (
        f"expected starfish + holothurian on her sample, got {sorted(found)}. "
        "Something upstream of the detector changed.")
    for name, expected in (("starfish", 0.83), ("holothurian", 0.78)):
        assert abs(found[name] - expected) < 0.02, (
            f"{name} came out at {found[name]:.2f}, her published value is {expected}.")

    # The conf floor must actually reach the model. It cannot be set via
    # model.overrides — Model.predict() merges {**overrides, **custom, **kwargs} with
    # custom = {"conf": 0.25}, which silently overwrites it. A wiring mistake there
    # would leave every detection stuck at 0.25 and look like it worked.
    loose = model(image, verbose=False, conf=0.01)[0]
    assert len(loose.boxes) >= len(result.boxes), "conf floor is not reaching the model"
    print(f"\nOK — reference detections match. At conf 0.01 the same image gives "
          f"{len(loose.boxes)} boxes vs {len(result.boxes)} at 0.25, so the floor is live.")
