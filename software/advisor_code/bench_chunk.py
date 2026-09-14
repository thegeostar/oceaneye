# OceanEye: find the fastest chunk size for the pure-PyTorch selective scan.
# Bigger chunks mean fewer Python-loop steps but a bigger decay matrix in VRAM.

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import torch
import selective_scan_fallback as ssf
from ultralytics import YOLO

IMG = "app/upload/000013.jpg"
model = YOLO("output_dir/mscoco/mambayolo_n/weights/best.pt")

_orig = ssf.selective_scan_pytorch


def timed(chunk, runs=3):
    ssf.selective_scan_pytorch = lambda *a, **k: _orig(*a, **{**k, "chunk": chunk})
    import ultralytics.nn.modules.common_utils_mbyolo as cu
    cu.selective_scan_pytorch = ssf.selective_scan_pytorch

    model(IMG, verbose=False)               # warm up
    torch.cuda.synchronize()
    best = float("inf")
    for _ in range(runs):
        t = time.time()
        model(IMG, verbose=False)
        torch.cuda.synchronize()
        best = min(best, time.time() - t)
    peak = torch.cuda.max_memory_allocated() / 1e9
    torch.cuda.reset_peak_memory_stats()
    return best, peak


print(f"{'chunk':>6} {'sec/img':>9} {'fps':>6} {'peak VRAM':>11}")
for chunk in (2, 4, 8, 16, 32):
    try:
        secs, peak = timed(chunk)
        print(f"{chunk:>6} {secs:>9.2f} {1/secs:>6.1f} {peak:>9.1f} GB")
    except torch.cuda.OutOfMemoryError:
        torch.cuda.empty_cache()
        print(f"{chunk:>6} {'OOM':>9}")
        break
