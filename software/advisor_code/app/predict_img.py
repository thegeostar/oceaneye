import os  # file and directory paths
import sys

import cv2  # OpenCV, for image handling
from PIL import Image

# parent directory of this script
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# add the parent directory to sys.path
sys.path.insert(0, parent_dir)

# OceanEye: the weights path and the shared model live in predict_video.py, so the
# image, video and camera paths all use one copy. Override with
#   OCEANEYE_WEIGHTS=/path/to/other.pt python app.py
from predict_video import load_model  # noqa: E402  (needs sys.path above)


def detect(img_path):
    # read the image
    img = cv2.imread(img_path)
    # run detection
    results = load_model()(img)

    # render the result
    for r in results:
        im_array = r.plot()  # BGR array with the boxes drawn on
        im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
        # build the output path
        # OceanEye: was .replace('.jpg', ...), which for a .png/.jpeg upload returned the
        # INPUT filename unchanged and overwrote the original. splitext handles any suffix.
        output_filename = os.path.splitext(os.path.basename(img_path))[0] + '_detected.jpg'
        output_path = os.path.join(parent_dir, 'app', 'static', output_filename)
        # save the annotated image
        im.save(output_path)


    # return the path of the annotated image
    return output_path
    
# # smoke test
# img_path = "/Users/likaixuan/Desktop/project/data/dataset/test/image/3.jpg"
# output_path = detect(img_path)
# # render the result
# import matplotlib.pyplot as plt
# img = cv2.imread(output_path)
# plt.imshow(img)
# plt.show()

