# OceanEye: measure sec/image and peak VRAM for the selective scan.
#
# Replaces bench_chunk.py, which tuned the chunk length of the old Python loop.
# There is no loop left to tune; what matters now is how many channels are held
# in flight at once, so that is what this sweeps.
#
#   python bench_scan.py

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import torch
import selective_scan_fallback as ssf
from ultralytics import YOLO

IMG = "app/upload/000013.jpg"
model = YOLO("output_dir/mscoco/mambayolo_n/weights/best.pt")


def timed(chunk, block_mb, runs=5):
    ssf._CHUNK = chunk
    ssf._BLOCK_BYTES = block_mb << 20
    model(IMG, verbose=False)                       # warm up
    torch.cuda.synchronize()
    torch.cuda.reset_peak_memory_stats()
    best = float("inf")
    for _ in range(runs):
        t = time.time()
        model(IMG, verbose=False)
        torch.cuda.synchronize()
        best = min(best, time.time() - t)
    return best, torch.cuda.max_memory_allocated() / 1e9


print(f"{'chunk':>6} {'block':>8} {'sec/img':>9} {'fps':>6} {'peak VRAM':>11}")
for chunk in (4, 8, 16, 32, 64, 128):
    for mb in (192, 768):
        try:
            secs, peak = timed(chunk, mb)
            print(f"{chunk:>6} {mb:>5} MB {secs:>9.3f} {1/secs:>6.1f} {peak:>8.2f} GB")
        except torch.cuda.OutOfMemoryError:
            torch.cuda.empty_cache()
            print(f"{chunk:>6} {mb:>5} MB {'OOM':>9}")
