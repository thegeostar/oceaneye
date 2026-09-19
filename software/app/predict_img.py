import os
import sys

import cv2

# parent directory of this script
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# add the parent directory to sys.path
sys.path.insert(0, parent_dir)

# OceanEye: the weights path and the shared model live in predict_video.py, so the
# image, video and camera paths all use one copy. Override with
#   OCEANEYE_WEIGHTS=/path/to/other.pt python app.py
from predict_video import CONF, OUT_DIR, enhance, load_model  # noqa: E402  (needs sys.path above)


def detect(img_path):
    """Run the detector on one image and return the path of the annotated copy."""
    img = cv2.imread(img_path)
    # OceanEye: imread returns None for anything it cannot decode — a HEIC photo, a
    # renamed .txt — and the model then failed deep inside torch with an opaque message.
    if img is None:
        raise ValueError(f"cannot read {os.path.basename(img_path)} as an image")

    # one image in, one result out
    # OceanEye: was a `for r in results:` loop that saved inside the loop and returned
    # after it, so an empty result list raised UnboundLocalError instead of anything useful.
    r = load_model()(enhance(img), verbose=False, conf=CONF)[0]

    # OceanEye: was .replace('.jpg', ...), which for a .png/.jpeg upload returned the
    # INPUT filename unchanged and overwrote the original. splitext handles any suffix.
    output_filename = os.path.splitext(os.path.basename(img_path))[0] + '_detected.jpg'
    # OceanEye: wrote straight into static/, so uploading 000013.jpg overwrote
    # static/000013_detected.jpg — the published reference verify_model.py checks against.
    os.makedirs(OUT_DIR, exist_ok=True)
    output_path = os.path.join(OUT_DIR, output_filename)

    # plot() returns BGR and imwrite expects BGR, so this writes straight out. It used
    # to go through PIL, which meant a channel flip in and another one back for nothing.
    cv2.imwrite(output_path, r.plot())
    return output_path
