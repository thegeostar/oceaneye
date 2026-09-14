# Software — OceanEye

> **← [START_HERE.md](../START_HERE.md) tells you what to do today. This page is every command you will type, in one place.**
>
> **Owner:** S2 · **Open it when:** installing (Day 1), running the demo (Day 3+), or the night before the competition for the pre-flight check.

---

## ⚠️ There are now TWO codebases in this folder. Know which one you are in.

| Folder | Whose | What it is | Runs today? |
|---|---|---|---|
| **`advisor_code/`** | **Prof. Wang's**, our editable copy | **Mamba-YOLO + her Flask web app + her trained `best.pt`.** The real model. This is what should go on stage | ❌ **not yet** — needs Python 3.11 + PyTorch |
| `oceaneye/` + `oceaneye_demo.py` | ours | Capture, enhancement, tracking, counting, CSV logging, stage-recovery keys. Runs with no camera and no model | ✅ **yes, right now** |

**They are not competitors.** Hers has the model; ours has the rehearsal and recovery machinery. The plan is to run hers, with ours as the fallback that already works.

🔴 **Never edit `../02_Advisor/Mamba-YOLO-main/`.** That is her original and our reference. Work in `advisor_code/`. Every change we made there is tagged — find them all with:

```bash
grep -rn "OceanEye:" advisor_code/
```

📄 **What her code actually is, what was tested, what is broken → [`../02_Advisor/Advisor_Code_Findings.md`](../02_Advisor/Advisor_Code_Findings.md)**

---

## 🎯 Getting her model running — the one job that matters

Her model needs a hand-written GPU routine called `selective_scan`. She shipped it **precompiled** (that saves days), but only for **Python 3.11** — this laptop has 3.12.

```bash
# 1. Python 3.11
sudo add-apt-repository ppa:deadsnakes/ppa && sudo apt update
sudo apt install python3.11 python3.11-venv

# 2. A SEPARATE env. Do not reuse ../.venv — it is 3.12 and it stays that way
cd "/home/eng-dararoth/Desktop/Events/2026 World Vocational College Skills Competition"
python3.11 -m venv .venv311 && source .venv311/bin/activate

# 3. PyTorch for the RTX 5060 (sm_120 — new enough to need the cu128 build)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
python -c "import torch; print(torch.__version__, torch.cuda.get_device_name(0))"

# 4. Her code + the compiled operator  ← this step decides the week
cd 06_Software/advisor_code
pip install -e . && pip install ./selective_scan
python -c "import selective_scan_cuda_core; print('the hard part works')"
```

**Then prove it detects, not just loads:**

```bash
python -c "
from ultralytics import YOLO
m = YOLO('output_dir/mscoco/mambayolo_n/weights/best.pt')
r = m('app/upload/000013.jpg'); r[0].save('proof.jpg'); print(r[0].boxes)"
```

Open `proof.jpg` beside `app/static/000013_detected.jpg` — **her own output on the same image**, `holothurian 0.78`, `starfish 0.83`. **Your boxes must match hers.** A model that loads but detects nothing looks exactly like a working one until you run this check. That is not hypothetical — it is precisely how her `best.onnx` failed.

**Her web app:**

```bash
python app/app.py          # then open http://localhost:8080
```

Three tabs: Video Detection · Image Detection · Real-time Monitoring. Feed it `../../02_Advisor/Reference_Videos/video_2026-09-13_13-57-08.mp4`.

> ⚠️ **Her "Real-time Monitoring" originally ignored the camera and played a hidden video file.** Fixed in our copy: it opens the camera, and a recorded fallback is opt-in and stamped `PLAYING RECORDED FOOTAGE - NOT LIVE` on screen. If you ever want it deliberately:
> ```bash
> OCEANEYE_CAMERA_FALLBACK=/path/to/clip.mp4 python app/app.py
> ```
> **Also:** her login accepts any password, and the on-screen counts are per-frame with no tracking. Do not claim either as a feature.

**If step 4 fails** with `undefined symbol` or `no kernel image is available`: **stop and say so in the chat.** The prepared fallback replaces the compiled operator with ~25 lines of ordinary PyTorch — same weights, same accuracy, slower — and removes the Python 3.11, the `.so` and the GPU-generation problem in one move. An afternoon, not a week. Do not grind at it alone.

---

## 🏃 Our own pipeline — no camera, no model, no internet

```bash
source ../.venv/bin/activate
python oceaneye_demo.py --profile desk
```

That runs the **entire system** against a generated underwater scene: enhancement, detection, tracking, per-species counting, CSV logging, recording. Nothing is real except the software — the screen says so in red. It exists so the software gets built and rehearsed **while the hardware is still in a shop**.

When the camera and the weights arrive, nothing changes except one file: `profiles/endoscope.toml`.

**Jump to:** [Install](#install) · [The three ways to run](#the-three-ways-to-run) · [Keys](#keys-during-playback) · [Moving to different hardware](#moving-to-different-hardware) · [What comes out of a run](#what-comes-out-of-a-run) · [Pre-flight](#pre-flight--do-this-the-night-before) · [If the FPS is low](#if-the-fps-is-low) · [The code](#the-code)

---

## Install

**Two environments, on purpose.** Her model needs Python 3.11; ours is happy on 3.12. Keeping them apart means a failed experiment on her side cannot break the thing that already works.

| Env | Python | For | Contains |
|---|---|---|---|
| `../.venv` | 3.12 | **ours** — `oceaneye_demo.py` | numpy, opencv, onnxruntime |
| `../.venv311` | 3.11 | **hers** — `advisor_code/` | torch, ultralytics, selective_scan |

```bash
cd "/home/eng-dararoth/Desktop/Events/2026 World Vocational College Skills Competition"
source .venv/bin/activate             # Windows: .venv\Scripts\activate
python -c "import cv2, numpy; print('OK')"
```

> ⚠️ **Do not move or copy `.venv/`.** Virtual environments store absolute paths and break when relocated. If it breaks, delete it and recreate.

**Write down the exact commands that worked** in this file. You will need to repeat them under pressure.

**Our pipeline needs nothing else to start.** With only `numpy` and `opencv` it runs on the mock detector and `python test_oceaneye.py` passes. Everything heavy — torch, ultralytics — belongs in `.venv311` with her code.

---

## The three ways to run

| Profile | What it uses | When |
|---|---|---|
| **`desk`** | Generated scene + mock detector | **Now.** No hardware, no weights. Build and rehearse the software |
| **`endoscope`** | The real USB camera + `best.pt` | Day 3 onward, once both exist |
| **`recorded`** | A video file + `best.pt` | Tier 0 fallback, and rehearsing the backup |

```bash
python oceaneye_demo.py --profile desk                     # today
python oceaneye_demo.py --profile endoscope                # the real rig
python oceaneye_demo.py --profile recorded --source run1.mp4

python oceaneye_demo.py --list-cameras                     # which index is the endoscope?
python oceaneye_demo.py --profile endoscope --preflight    # check everything, change nothing
python test_oceaneye.py                                    # is the software still intact?
```

Any flag beats the profile, so you never have to edit a file to try something:

```bash
python oceaneye_demo.py --profile endoscope --conf 0.25 --no-enhance
python oceaneye_demo.py --source ../08_Data/footage/run1.mp4 --headless --save-video out.mp4
```

`--source` accepts **all of these**: `0` (camera index) · `clip.mp4` · `photo.jpg` · `frames/` (a folder of images) · `rtsp://…` or `http://…` (network or phone camera) · `synthetic`.

---

## Keys during playback

```
e        enhancement on/off        (the before/after moment — practise this one)
t        tracking on/off           (unique counting)
u        simulated turbidity on/off
0 1 2 3  tag the turbidity level   L0 clear .. L3 heaviest
- / =    confidence down / up      (0.05 steps)
p        PANIC: confidence -> 0.20 (nothing is being detected on stage)
r        start/stop recording
b        switch to the backup video  (the camera just died)
space    pause      s  save frame      h  this help      q  quit
```

Three of these are stage-recovery keys. **Learn `p`, `b` and `e` by heart.**

- **`p`** — nothing is showing up. Drops the threshold to 0.20 in one keystroke. Say: *"The confidence threshold is set high for precision. Let me lower it."*
- **`b`** — the camera has died. Switches to the backup video instantly and puts `PLAYING RECORDED SURVEY FOOTAGE` on screen, so you are never pretending it is live.
- **`0` `1` `2` `3`** — press these as you stir clay in. Every detection is then tagged with its turbidity level in the CSV, and the run summary prints the ladder table for your slides. **You do not have to write numbers down while presenting.**

---

## Moving to different hardware

This is the part that matters for later. **Nothing about a specific device is written in the code.** It all lives in a `.toml` profile:

```toml
[capture]
source  = "0"          # or "rtsp://…", or a file, or "synthetic"
width   = 1280
height  = 720
fps     = 30
fourcc  = "MJPG"       # without this many UVC cameras crawl at ~5 fps
backend = "v4l2"       # "auto" on Windows/macOS
flip    = ""           # "h"/"v"/"hv" if the camera is mounted rotated

[capture.controls]     # locked, not automatic — see Core_Strategy §3.8
auto_exposure      = false
exposure           = 150
auto_white_balance = false
white_balance      = 4500
gain               = 0

[model]
path = "../08_Data/weights/best.pt"   # .pt, .onnx, .engine, or "mock"
```

To support a new camera, laptop, or single-board computer: **copy a profile, change the numbers, run `--preflight`.** No code edits.

> ⭐ **Every setting is read back from the driver and printed.** `set()` silently fails on a lot of UVC cameras, so "I asked for it" is not evidence. Tested on the built-in webcam here: asked for exposure 150, the driver gave 156; asked for gain 0, the floor was 1. **Copy the values it prints into [`../05_Hardware/Purchase_Log.md`](../05_Hardware/Purchase_Log.md), not the values you asked for.**

On Linux the system also calls `v4l2-ctl` for the same controls, because it succeeds where OpenCV quietly does not. Missing `v4l2-ctl` is a warning, never a crash.

---

## What comes out of a run

Every run gets its own folder, written **while it happens**, not afterwards:

```
runs/2026-09-12_1831/
    detections.csv   one row per detection: frame, time, level, species, conf, track id, box, fps
    summary.json     per-species totals and the turbidity ladder
    settings.json    the exact config that produced this run
    snap_001.jpg     frames you saved with 's'
    recording.mp4    if recording was on
```

The console prints the same summary at the end:

```
  species           unique  detections  mean conf
  holothurian           33          75      0.742
  scallop                3          10      0.822
  starfish              65         206      0.725

  turbidity ladder
  level     frames  detections  per frame  mean conf
  L0            60         291       4.85      0.733
```

**That ladder table is the one in your slides.** It is measured, it is yours, and `detections.csv` is the receipt if a judge asks where a number came from.

> `runs/` fills up with video. Delete old ones; keep the good ones.

---

## Pre-flight — do this the night before

```bash
python oceaneye_demo.py --profile endoscope --preflight
```

Checks the model loads, the camera opens, the **real measured frame rate**, the settings the driver actually applied, whether a backup video exists, free disk space, and whether the machine is online.

**Run it after a full laptop restart with the Wi-Fi OFF.** If it says `offline - nothing here needs the internet`, that requirement is proven rather than assumed. That is the test that catches what nothing else catches.

---

## If the FPS is low

Measured on this laptop, enhancement only, before the model even runs:

| Capture resolution | Enhancement cost | Ceiling |
|---|---|---|
| 1280×720 | 38 ms/frame | ~26 fps |
| **960×540** | **10 ms/frame** | **~100 fps** |
| 640×480 | 7 ms/frame | ~135 fps |

**First lever: drop `width`/`height` to 960×540 in the profile.** A projector cannot show more than that anyway, and it costs you nothing visually. Then, in order: turn enhancement off with `e`, lower `imgsz`, use a smaller model.

Judges will ask whether it is really live. Above 20 fps is a real-time answer.

---

## The code

```
oceaneye_demo.py     the command line — thin, all the flags
oceaneye/
    config.py        device profiles (.toml). Change hardware HERE, not in code
    vision.py        enhancement, turbidity physics, drawing   (pure functions)
    capture.py       any source: camera, file, folder, stream, synthetic
    detect.py        YOLO or mock detector, tracking, per-species counting
    session.py       CSV log, snapshots, recording, run summary
    runner.py        the run loop and the pre-flight check
profiles/            desk.toml · endoscope.toml · recorded.toml
train_oceaneye.py    dataset prep · fine-tuning · auto-labelling (never runs on stage)
test_oceaneye.py     11 self-checks. Run after any change
```

It is importable, so anything you build later reuses it instead of copying it:

```python
from oceaneye import config, runner
cfg = config.load("profiles/endoscope.toml")
runner.run(cfg, headless=True, max_frames=300)
```

| Function | Does |
|---|---|
| `vision.gray_world_white_balance()` | Removes the blue-green cast from wavelength-selective absorption |
| `vision.clahe_enhance()` | Local contrast boost on the LAB L-channel — cuts scattering haze |
| `vision.enhance_underwater()` | The pipeline: colour first, then contrast. **Order matters** |
| `vision.simulate_turbidity()` | Physics-based murky-water simulation for training augmentation. Betas are **BGR order**; red (index 2) attenuates fastest |
| `capture.Capture` | Opens any source, applies device settings, **reads them back** |
| `detect.Counter` | Per-species frame counts, unique individuals, mean confidence |
| `session.Session` | Writes the CSV and the summary as the run happens |

---

## Fine-tuning — `train_oceaneye.py` · ⛔ not the plan any more

> 🛑 **Skip this section unless something has gone badly wrong.**
>
> **We are not training.** Prof. Wang sent a finished model with better numbers than we could reach in six days, and training earns **zero rubric points**. This section survives for one reason only: if her model cannot be made to run *and* the pure-PyTorch fallback also fails, fine-tuning a stock YOLOv8 on public data is the last resort that still puts a real detector on stage.
>
> If you find yourself reading this in earnest, say so in the chat first.

Separate file, used two or three times all week and never on stage. Works the same in a terminal or in Colab (`!python train_oceaneye.py …`).

```bash
python train_oceaneye.py prep ../08_Data/datasets/DUO             # 1. dataset -> YOLO format
python train_oceaneye.py train ../08_Data/datasets/DUO/oceaneye.yaml   # 2. fine-tune
python train_oceaneye.py autolabel ../08_Data/footage/run1.mp4    # 3. later, own footage
```

**`prep`** handles both dataset shapes you will meet: **DUO** (VOC XML → converted) and **Brackish** (Roboflow, already YOLO → class ids **remapped** by name, because Brackish's `starfish` is index 5, not 3, and the rest of its classes are fish and crabs we drop). It writes `oceaneye.yaml`, a deterministic 85/15 split, and per-species box counts.

> 🔴 **`prep` always renders 5 `check_*.jpg` images with the converted labels drawn back on. Open them.** A coordinate mistake looks fine in a text file and is obvious on an image. This is the gate — everything downstream is wasted if it fails.

**`train`** starts from pretrained weights (`yolov8n.pt` by default — the advisor's script claims "improved YOLOv8", and what you say on stage must match what you ran; same ultralytics API as v11, so this is not a framework switch). It reports **mAP50**, per-class mAP50, and copies `best.pt` into `08_Data/weights/`. Useful flags: `--batch 8` if you run out of memory, `--epochs 30` if you are short of time, `--device cpu` to force it.

**`autolabel`** pre-labels your own tank footage with a model you already trained, keeping every 10th frame. You then *correct* the guesses in a labelling tool instead of drawing 300 boxes from scratch, and run `prep` + `train` again. Core_Strategy §5 calls this the single biggest improvement to live-demo reliability. It refuses to run on the mock detector.

⚠️ **Preprocessing parity.** `prep` writes `preprocessing.json` recording that the dataset is **raw**. Whatever you train on must match what you infer with — train raw, demo with `display.enhance = false`, or your enhancement is a domain shift that makes detection *worse*. The run's `settings.json` records which you used, so the two are checkable.

---

## Before you touch the model — read this

**[`../03_Planning/Core_Strategy_Data_Quality.md`](../03_Planning/Core_Strategy_Data_Quality.md) §3.8** covers locking exposure, white balance and MJPG on the camera. Do that **before** any model work. An unstable input stream makes every downstream measurement meaningless.

Two rules that will otherwise cost you silently:

1. **Apply the same preprocessing in training and inference.** Train on raw, infer on enhanced → you have created a domain shift and made things worse. The run's `settings.json` records which you used, so check it.
2. **Fine-tune on footage from your own rig.** 200–300 frames from your actual tank beats thousands of foreign images, for your demo.

---

## Offline requirement

The venue has no internet. Before 18 September, verify with **Wi-Fi switched off**:

- [ ] `python oceaneye_demo.py --profile endoscope --preflight` reports **offline** and **READY**
- [ ] Weights load from local disk with no download
- [ ] Works after a **full laptop restart**
- [ ] Backup screen recording of a perfect run is on the desktop **and set as `fallback.backup_video`**
- [ ] Everything copied to 2 USB sticks

---

## Status (13 Sept 2026)

### Her code — `advisor_code/`
- ✅ **Real trained weights received** — `best.pt`, 145 MB, **mAP50 0.867** from her own training log
- ✅ **Model identified: Mamba-YOLO-L** (YOLOv8 skeleton, `VSSBlock` in place of `C2f`). The YOLOv5-vs-YOLOv8 question is closed
- ✅ **Copied and made portable** — hardcoded `E:/URPC/…` Windows paths removed, Linux fonts, camera-index crash, `.png` overwrite bug and the fake "real-time" tab all fixed. All four edited files pass a syntax check
- ✅ **Prebuilt CUDA operator found** — `selective_scan_*.so`, Linux x86-64, Python 3.11. No CUDA compiler needed *if* it loads
- ❌ **`best.onnx` is broken.** Tested in ONNX Runtime: loads, correct output shape, ~550 ms/frame, and **zero detections at any threshold** on images her `.pt` detects at 0.78–0.83. Excluded from our copy
- ⏳ **Never executed.** PyTorch is not installed. **This is the blocker on the whole project**
- ⚠️ **Unknown:** whether the precompiled operator runs on the RTX 5060. It targets sm_70/80/90 with compute_90 PTX; our GPU is sm_120. Forward-JIT should cover it. *Should*

### Our code
- ✅ **Full system runs with no hardware and no weights** — `--profile desk`, mock detector, synthetic scene
- ✅ **11/11 self-checks pass** with only numpy + opencv installed
- ✅ **Real camera path verified** against the built-in webcam: asked for 1280×720 MJPG@30, got it; measured 29.9 fps; settings read back and driver deviations caught
- ✅ Recording, CSV logging, per-species counting, turbidity tagging, run summary all working
- ✅ **Fine-tuning pipeline written and tested** — now demoted to last resort (see above)
- ⏳ **Never run against a real trained model**
- ⏳ No waterproof camera acquired yet (built-in webcam only)

### This laptop, measured
RTX 5060 Laptop GPU 8 GB · driver 580 / CUDA 13.0 · **no `nvcc`** · 16 cores · 31 GB RAM · 537 GB free · Ubuntu 24.04 · **Python 3.12 only**
