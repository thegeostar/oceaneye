"""Single-image detection."""
import os

import cv2

from predict_video import CONF, OUT_DIR, enhance, load_model


def detect(img_path):
    """Detect on one image and return the path of the annotated copy."""
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f'Cannot read {os.path.basename(img_path)} as an image')

    result = load_model()(enhance(img), verbose=False, conf=CONF)[0]
    os.makedirs(OUT_DIR, exist_ok=True)
    name = os.path.splitext(os.path.basename(img_path))[0] + '_detected.jpg'
    output_path = os.path.join(OUT_DIR, name)
    cv2.imwrite(output_path, result.plot())
    return output_path
