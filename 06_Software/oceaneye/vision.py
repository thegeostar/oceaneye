"""Pixel work: underwater enhancement, turbidity physics, and everything drawn on screen.

Pure functions over numpy arrays. No camera, no model, no files — which is why this
module is the easiest part to reuse, test, and port to another device.
"""

from __future__ import annotations

from functools import lru_cache

import cv2
import numpy as np

# Fixed colours per species, so the same animal is always the same colour on screen,
# in the synthetic scene, and in the slides. BGR (OpenCV order).
SPECIES_COLOURS = {
    "holothurian": (0, 140, 255),    # sea cucumber - orange
    "echinus": (200, 0, 150),        # sea urchin    - purple
    "scallop": (0, 220, 220),        # scallop       - yellow
    "starfish": (40, 40, 230),       # starfish      - red
}
_FALLBACK_PALETTE = [(0, 255, 0), (255, 200, 0), (255, 0, 255), (0, 255, 255),
                     (255, 255, 0), (120, 255, 120)]


def colour_for(name: str, index: int = 0):
    """Species colour by name; falls back to a palette for any other class list."""
    key = str(name).lower()
    for species, colour in SPECIES_COLOURS.items():
        if species in key or key in species:
            return colour
    return _FALLBACK_PALETTE[index % len(_FALLBACK_PALETTE)]


# ---------------------------------------------------------------------------
# Underwater enhancement
# ---------------------------------------------------------------------------


def gray_world_white_balance(img, sample_step=4):
    """Remove the blue-green colour cast caused by wavelength-selective absorption.

    Water absorbs red light first (gone by ~5 m), so underwater images are
    starved of red. Gray-World assumes a natural scene averages to gray and
    rescales each channel to force that, restoring roughly natural colour.

    The channel gains are measured on every sample_step-th pixel and applied with a
    256-entry lookup table. Same result as full-image float maths, about 6x faster,
    which matters because this runs on every frame of a live demo. Set sample_step=1
    for the exact full-image statistics.
    """
    small = img[::sample_step, ::sample_step] if sample_step > 1 else img
    means = [float(small[:, :, i].mean()) for i in range(3)]
    avg_gray = sum(means) / 3.0

    ramp = np.arange(256, dtype=np.float32)
    table = np.empty((256, 1, 3), dtype=np.uint8)
    for i, avg in enumerate(means):
        gain = avg_gray / avg if avg > 1e-6 else 1.0
        table[:, 0, i] = np.clip(ramp * gain, 0, 255).astype(np.uint8)
    return cv2.LUT(img, table)


@lru_cache(maxsize=8)
def _clahe(clip_limit, tile):
    """CLAHE objects are reusable; building one per frame is pure waste."""
    return cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile)


def clahe_enhance(img, clip_limit=3.0, tile=(8, 8)):
    """Boost local contrast to cut through scattering haze.

    Runs on the L (lightness) channel in LAB space only, so contrast improves
    without distorting colour. Tile-based, so dark vignetted corners get
    boosted independently of a bright centre hotspot.
    """
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = _clahe(clip_limit, tile).apply(l)
    return cv2.cvtColor(cv2.merge((l, a, b)), cv2.COLOR_LAB2BGR)


def enhance_underwater(img, clip_limit=3.0):
    """Colour correction first, then contrast. Order matters."""
    return clahe_enhance(gray_world_white_balance(img), clip_limit=clip_limit)


def simulate_turbidity(img, beta=(0.25, 0.4, 0.9), depth=1.0, veil=(150, 140, 90)):
    """Physics-informed turbidity simulation (training augmentation).

    Implements I = J*t + B*(1-t) with t = exp(-beta*d), the underwater image
    formation model. Use this to synthesise murky Tonle Sap-like conditions
    from clear-water training images.

    beta  : per-channel attenuation in **BGR order** (OpenCV convention).
            Red light is absorbed FASTEST underwater, so beta_R (index 2)
            must be the LARGEST value and beta_B (index 0) the smallest.
            Getting this order backwards produces physically wrong images.
    depth : distance proxy. Larger -> murkier. depth=0 is a no-op.
    veil  : background scattered light in BGR - the blue-green "fog" colour.
            Tune beta and veil until your synthetic images visually match
            real frames from the Brackish dataset.
    """
    out = img.astype(np.float32)
    for c in range(3):
        t = np.exp(-beta[c] * depth)
        out[:, :, c] = out[:, :, c] * t + veil[c] * (1 - t)
    return np.clip(out, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------


def draw_detections(frame, detections, scale=1.0, show_conf=True, show_id=True):
    """Draw our own boxes rather than the model's, so the mock detector, a YOLO
    model and any future detector all look identical on stage."""
    font = cv2.FONT_HERSHEY_SIMPLEX
    thickness = max(2, int(2 * scale))

    for det in detections:
        x1, y1, x2, y2 = (int(v) for v in det.xyxy)
        colour = colour_for(det.cls_name, det.cls_id)
        cv2.rectangle(frame, (x1, y1), (x2, y2), colour, thickness)

        label = det.cls_name
        if show_conf:
            label += f" {det.conf:.2f}"
        if show_id and det.track_id is not None:
            label += f" #{det.track_id}"

        size = 0.6 * scale
        (tw, th), _ = cv2.getTextSize(label, font, size, thickness - 1)
        top = max(y1 - th - 8, 0)
        cv2.rectangle(frame, (x1, top), (x1 + tw + 8, top + th + 8), colour, -1)
        cv2.putText(frame, label, (x1 + 4, top + th + 2), font, size, (0, 0, 0), thickness - 1)
    return frame


def draw_hud(frame, lines, scale=1.0):
    """Status panel. Dark outline keeps text legible against any scene."""
    font = cv2.FONT_HERSHEY_SIMPLEX
    size = 0.9 * scale
    step = int(38 * scale)
    for i, (text, colour) in enumerate(lines):
        origin = (20, int(40 * scale) + i * step)
        cv2.putText(frame, text, origin, font, size, (0, 0, 0), int(4 * scale))
        cv2.putText(frame, text, origin, font, size, colour, max(1, int(2 * scale)))
    return frame


def draw_banner(frame, text, colour=(0, 0, 255), scale=1.0):
    """Full-width strip at the bottom. Used for warnings the judges must not miss."""
    h, w = frame.shape[:2]
    bar = int(46 * scale)
    cv2.rectangle(frame, (0, h - bar), (w, h), (0, 0, 0), -1)
    cv2.putText(frame, text, (16, h - int(14 * scale)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8 * scale, colour, max(1, int(2 * scale)))
    return frame


def flip(frame, mode):
    """Camera mounted upside down? Fix it here, not with a screwdriver at the venue."""
    if mode == "h":
        return cv2.flip(frame, 1)
    if mode == "v":
        return cv2.flip(frame, 0)
    if mode == "hv":
        return cv2.flip(frame, -1)
    return frame
