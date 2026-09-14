# How to run Prof. Wang's model

← [README.md](../../README.md) · **Owner: S2** · Full background: [advisor/Advisor_Code_Findings.md](../../advisor/Advisor_Code_Findings.md)

> 🔴 **Right now, nothing here runs.** PyTorch is not installed and the laptop has the wrong
> Python version. Section 2 fixes that. Until it's done, every command below will fail.

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

# 4. Her code + the compiled GPU piece  ← THIS STEP DECIDES THE WEEK
cd software/advisor_code
pip install -e .
pip install ./selective_scan
python -c "import selective_scan_cuda_core; print('the hard part works')"

# 5. The web page needs these two as well
pip install flask flask-session
```

**If step 4 prints `undefined symbol` or `no kernel image is available` — stop and say so in
the chat.** Don't grind at it. There's a prepared fallback that replaces the CUDA operator
with ~25 lines of plain PyTorch and deletes this whole problem in one afternoon.

---

## 3. First test — one photo, 30 seconds

Do this **before** the web app. If it fails, you know the problem is the model, not Flask.

```bash
source ../../.venv311/bin/activate
cd "/home/eng-dararoth/Desktop/Events/2026 World Vocational College Skills Competition/software/advisor_code"

python -c "
from ultralytics import YOLO
m = YOLO('output_dir/mscoco/mambayolo_n/weights/best.pt')
r = m('app/upload/000013.jpg')
r[0].save('proof.jpg')
print(r[0].boxes)"
```

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
