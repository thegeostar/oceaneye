# How to run Prof. Wang's model

← [README.md](../../README.md) · **Owner: S2** · Full background: [advisor/Advisor_Code_Findings.md](../../advisor/Advisor_Code_Findings.md)

> ✅ **The model works on this laptop as of 14 Sept 2026.** It detects
> `starfish 0.83` and `holothurian 0.78` on her sample image — the exact numbers from her
> own shipped result. Setup is done; you do not need to reinstall anything.
>
> **One thing to know: ~1.1 seconds per image, not 30 fps.** Why, is in section 7.
> It was 2.3 s until 15 Sept; what changed is in section 8. The **live camera feed is
> smooth at ~26 fps** — the boxes refresh about once a second, the video never stalls.

## 0. Check which environment you're in — every single time

VS Code **auto-activates the wrong one.** When you open a terminal it turns on `.venv`, which
is Python 3.12 and has no PyTorch. Her model needs `.venv311`. Look at the start of your prompt:

| Prompt shows | Which one | Her model runs? |
|---|---|---|
| `(.venv)` | Python 3.12 — our own demo code | ❌ no |
| `(.venv311)` | Python 3.11 — Prof. Wang's model | ✅ yes |

```bash
deactivate                      # leave whichever one VS Code picked
source .venv311/bin/activate    # enter the right one
python --version                # must say 3.11.x
```

**If you ever see `ModuleNotFoundError: No module named 'torch'`, this is almost always why.**
You are in `.venv`, not `.venv311`. It does not mean the install failed.

---

## 1. Only 6 things in this folder matter

There are ~3,000 files. Ignore all but these.

| Path | What it is |
|---|---|
| `output_dir/mscoco/mambayolo_n/weights/best.pt` | **The AI itself.** 139 MB. Irreplaceable — back it up |
| `app/app.py` | The web page. Run this to get the upload interface |
| `app/predict_img.py` | Detects on one photo |
| `app/predict_video.py` | Detects on a video file |
| `app/predict_camera.py` | Detects on the live camera |
| `app/upload/` | Her sample photos and videos to test with |

Everything else — `ultralytics/`, `selective_scan/`, `tests/`, `runs/`, `URPC/` — is the engine.
You never open it.

**Two files to never run:** `untitled.py` (made the broken ONNX file) and `test.py`
(still has her Chinese cloud server paths).

---

## 2. Install — once, about 40 minutes

⚠️ **Do NOT use `requirements.txt`.** It pins `torch==2.2.1`, which is too old to use your
RTX 5060 at all. Following it wastes an evening. Use the commands below instead.

```bash
# 1. Python 3.11 — her compiled GPU file will not load on 3.12
sudo add-apt-repository ppa:deadsnakes/ppa && sudo apt update
sudo apt install python3.11 python3.11-venv

# 2. A separate environment. Do NOT reuse ../../.venv (that one is 3.12 and must stay working)
cd "/home/eng-dararoth/Desktop/Events/2026 World Vocational College Skills Competition"
python3.11 -m venv .venv311
source .venv311/bin/activate

# 3. PyTorch for the RTX 5060. ~3 GB download — start it and go do something else
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
python -c "import torch; print(torch.__version__, torch.cuda.get_device_name(0))"

# 4. The Python packages her code needs
pip install einops timm opencv-python pandas matplotlib pyyaml tqdm psutil \
            py-cpuinfo seaborn scipy requests pillow flask flask-session
```

❌ **Do NOT run `pip install ./selective_scan`.** It cannot work on this laptop and the
error it gives is misleading. See section 7.

---

## 3. First test — one photo, 30 seconds

Do this **before** the web app. If it fails, you know the problem is the model, not Flask.

```bash
cd "/home/eng-dararoth/Desktop/Events/2026 World Vocational College Skills Competition"
source .venv311/bin/activate
cd software/advisor_code
python verify_model.py
```

Expected output:

```
inference: 1.13 s
detections: 2
   starfish       0.83
   holothurian    0.78
```

Works on any image: `python verify_model.py path/to/your/photo.jpg`

Now open two files side by side:

- **`proof.jpg`** — what your laptop produced
- **`app/static/000013_detected.jpg`** — what *her* laptop produced on the same photo

Hers shows **holothurian 0.78** and **starfish 0.83**. **Your boxes should match.**

> ⚠️ A model that loads but detects nothing looks *identical* to a working one until you
> check this. That is exactly how the broken ONNX file fooled us. Do not skip the comparison.

---

## 4. The web page — what you asked for

```bash
cd app
python app.py
```

Open **http://localhost:8080** in your browser.

- **Login:** type anything. Any username, any password works — there is no real login.
  ⚠️ **Never call this "user authentication" on stage.**
- **Image Detection** — upload a photo, get boxes back. Start here.
- **Video Detection** — upload an `.mp4`. Try `app/upload/URPC_test_video.mp4` (her real
  underwater footage) or `../../advisor/videos/video_2026-09-13_13-57-08.mp4`.
- **Real-time Monitoring** — the camera tab. See section 5.

Photos to test with, already in `app/upload/`:
`000013.jpg` · `003045.jpg` · `test_000080.jpg` · `test_000183.jpg` — these are real URPC
underwater images and **will** detect.

Stop the server with **Ctrl+C**.

---

## 5. The camera — when you're ready

Plug the Logitech webcam in first, then check Linux sees it:

```bash
v4l2-ctl --list-devices
```

Note the number in `/dev/videoN`. The laptop's built-in camera is usually `0`, so the
Logitech is often `1` or `2`.

Then open **Real-time Monitoring** in the web page and give it that number.

> ⚠️ **In her original code this tab ignored the camera and secretly played a video file.**
> That is fixed in our copy — it opens the real camera now. If it ever falls back to
> recorded footage it stamps `PLAYING RECORDED FOOTAGE - NOT LIVE` on the screen.
> Never narrate a recorded file as live. Professional Conduct is 10 points.

---

## 6. When something fails

| Message | Meaning | Do this |
|---|---|---|
| `ModuleNotFoundError: torch` | Wrong environment | `source .venv311/bin/activate` |
| `ModuleNotFoundError: selective_scan_cuda_core` | Step 4 didn't finish | Re-run step 4 |
| `undefined symbol` / `no kernel image` | GPU mismatch | **Stop. Ask in chat.** Use the fallback |
| `Address already in use` | Server already running | `pkill -f app.py` then retry |
| Boxes appear but confidence is low | Normal on non-URPC images | Not a bug — the model expects real underwater scenes |
| Nothing detected at all | Could be a dead model | Run section 3 and compare against her file |

**The accuracy number to quote is `mAP50 = 0.867`** — it's in
`output_dir/mscoco/mambayolo_n/results.csv`, a file you hold and can show a judge.
Never say 0.873; that's from her slide, a run we don't have.

---

## 7. Why it takes 2.3 seconds, and what to say about it

Her model needs a hand-written GPU routine called `selective_scan`. She shipped it
prebuilt — but compiled against **torch 2.2 + CUDA 11**, in March 2025.

This laptop cannot use those files, for two independent reasons:

1. **The RTX 5060 is sm_120 (Blackwell).** CUDA 11 cannot drive it at all, so torch must be
   2.7+ with CUDA 12.8. Downgrading torch is not an option — the old one can't see the GPU.
2. **PyTorch changed its C++ ABI in between.** All **39** libtorch symbols her `.so` files
   import were removed. Checked with `nm`, not guessed.

Rebuilding needs `nvcc` from the CUDA 12.8 toolkit: the pip wheel ships only `ptxas`, and
Ubuntu's apt package is CUDA 12.0, which predates sm_120. That leaves a ~3 GB download.

**So the operator is reimplemented in plain PyTorch** in
[`selective_scan_fallback.py`](selective_scan_fallback.py). Same maths, same weights, same
answers — just not hand-tuned CUDA. It is checked two ways: against a naive step-by-step
loop (`python selective_scan_fallback.py`, agrees to 3e-06), and against her own published
result on `000013.jpg` (identical to two decimals).

`bench_scan.py` tunes the two speed knobs and prints peak VRAM.

### What this means for the demo

| Use | Works? |
|---|---|
| Upload a photo, get boxes | ✅ fine — 1.2 s |
| Process a video beforehand and play the result | ✅ fine — do this for the stage |
| Live camera | ✅ **smooth video, boxes refresh ~1×/s** — see §8 |

**Say this if a judge asks:** *"The published model uses a custom CUDA kernel built for an
older GPU generation. We reimplemented that operator in portable PyTorch so it runs on
current hardware — we verified it reproduces the original author's published detections
exactly. It trades throughput for portability."*

That is a genuinely strong answer. It is real engineering work, it is honest, and it shows
you understood the model rather than just running it.

---

## 8. Making it faster — done, 15 Sept

**2.30 s → 1.13 s per image, with the detections bit-for-bit unchanged.** The acceptance
test still prints `starfish 0.83` and `holothurian 0.78`. Nothing below trades accuracy.

**What was actually wrong.** Profiling said **96.9 %** of the time was inside
`selective_scan` — everything else in the network came to 0.073 s. Per image the old code
ran ~7 080 Python loop steps issuing ~70 000 tiny GPU operations, so the GPU sat idle
waiting for Python.

The recurrence `x_t = a_t·x_{t-1} + b_t` is **associative**, so that loop was never
mathematically required — it can be done in `log2(L)` parallel steps instead of `L`.

Two things had to be got right, and both were decided by measurement:

- **The tempting one-line version does not work.** Rewriting the scan as a single
  `cumsum` needs `exp(-s)`, and the running `|s|` in this model reaches **113 within 8
  steps** while float32 `exp()` overflows at **88.7**. Not risky — unusable. That is why
  the code folds decay factors (all in `(0,1]`, so they can only shrink) instead.
- **Going fully parallel was no faster.** A flat `log2(L)` scan needs 14 passes over a
  0.75 GB tensor; at ~250 GB/s that measured **2.55 s — slower than the loop it replaced.**
  It had simply stopped being launch-bound and become bandwidth-bound. The fix is the
  two-level scan now in the file: scan inside chunks of 16, then scan only the per-chunk
  carries, which cuts the wide passes from 14 to about 4.

Also fixed, outside the model:

| Was | Now |
|---|---|
| `predict_img.detect()` re-read the 139 MB checkpoint **on every uploaded image** | loaded once, shared by the image, video and camera paths |
| Label text did a full frame BGR→RGB→PIL→RGB→BGR round-trip **per class per frame**, re-reading the .ttf off disk each time — 182 ms on a 4 K frame | drawn with `cv2.putText`, 4.6 ms (**40×**) |
| The camera loop ran the model **before** yielding each frame, so the video stuttered at model speed | detection moved to a worker thread; frames stream at camera rate |

**Live camera, measured:** **26 fps** to the browser while detections refresh about once a
second. The video is genuinely live the whole time — only the boxes lag, by roughly one
inference. Nothing is pre-recorded and nothing is misrepresented.

### Things deliberately not done

- **`torch.compile`** — did not finish compiling in **10 minutes**; the scan's
  shape-dependent loop recompiles per input shape. Abandoned, not deferred.
- **fp16 / `half=True`** — measured **1.129 s vs 1.131 s, i.e. no change**, because the
  scan casts to float32 internally. Costs accuracy for nothing.
- **Smaller input (416 / 320)** — 2–4× faster but it loses real detections: at 320 the
  holothurian falls 0.78 → 0.42 and only 3 of the 7 sea urchins in `003045.jpg` are
  found. Rejected: rule 4 says do not make the scene easy, and difficulty is worth
  15 points.

Whatever changes next, the acceptance test never changes: `python verify_model.py` must
still print `starfish 0.83` and `holothurian 0.78`. If it doesn't, the optimisation is
wrong — revert it.

> **Nothing in the rubric rewards frames per second.** It rewards *"smooth and precise
> operations"*. A calm feed with live boxes reads as live to a judge; a stuttering one
> does not. Speed is an upgrade, not a rescue — the demo already worked at 2.3 s.
