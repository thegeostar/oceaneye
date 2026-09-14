# What Prof. Wang actually sent us — tested, 13 September

> **← Back to [README.md](../README.md)**
>
> **Owner:** S2 · **Open it when:** you are deciding what to run on stage, or someone asks "can't we just use her code?"
>
> **TL;DR**
> - She sent a **real trained model** (`best.pt`, 145 MB, mAP50 **0.867**) — this is the single most valuable thing we have received.
> - It is **Mamba-YOLO**, not YOLOv5, not plain YOLOv8. The old argument is settled.
> - **It does not run on our laptop yet.** It needs PyTorch + a compiled CUDA operator. Neither is installed.
> - **The ONNX file she shipped is broken — I tested it. It detects nothing.** Do not build the demo on it.
> - She also sent a **45-second underwater test video**, which is the footage her own demo runs on.

**Everything marked ✅ below was run and observed on this laptop. Everything marked 🔶 is read off the files but not executed.** That distinction matters — we do not say numbers we have not seen.

---

## 1. Inventory — what arrived

| Item | Where | Size | State |
|---|---|---|---|
| Trained weights (main) | `output_dir/mscoco/mambayolo_n/weights/best.pt` | 145 MB | ✅ present, correct class list |
| Trained weights (2nd run) | `output_dir/mscoco/mambayolo_n10/weights/best.pt` | 115 MB | ✅ present, slightly worse |
| ONNX export | `…/mambayolo_n/weights/best.onnx` | 365 MB | ❌ **broken — see §4** |
| Prebuilt CUDA operator | `selective_scan/*.so` | 90 MB | 🔶 Linux + Python **3.11** only |
| Flask web app | `app/` | — | 🔶 needs the model to run |
| Training logs + curves | `output_dir/*/results.csv`, `*.png` | — | ✅ readable, honest |
| Her test footage | `advisor/videos/video_2026-09-13_13-57-08.mp4` | 8 MB | ✅ 45 s, 1280×720, 10 fps |
| Her URPC dataset config | `URPC/URPC.yaml` | — | ✅ 4 classes, correct order |
| The dataset itself | — | — | ❌ **not sent.** 3,717 train images referenced, none included |

**She did not send the training images.** We have the model, not the data it learned from. That is fine — we are not retraining — but it means we cannot reproduce her numbers, only quote them.

---

## 2. The model question is settled

| Claim | Source | Verdict |
|---|---|---|
| "improved YOLOv8" | her script, her patent title | ✅ true — YOLOv8's skeleton and head |
| "YOLOv5 + DeepSort" | her old reference video | ❌ **not this code.** Different project, ignore it |
| Mamba / state-space model | the code, PPT slide 5 | ✅ **this is what it is** |

The architecture is **Mamba-YOLO-L**: YOLOv8's detection head and PANet neck, with every `C2f` block replaced by a `VSSBlock` (a *Vision State-Space* block — the "fine-grained feature extraction module" on PPT slide 5).

**Say on stage:** *"Mamba-YOLO — a YOLOv8 architecture in which the feature blocks are replaced with Mamba state-space blocks."* That sentence is true, matches her patent, and matches the code. See [`PPTX_Translation_EN.md`](PPTX_Translation_EN.md) slides 5 and 7.

**Classes, in the order the model outputs them** (`URPC/URPC.yaml`, confirmed identical on PPT slide 12):

```
0 holothurian (sea cucumber)   1 echinus (sea urchin)   2 starfish   3 scallop
```

---

## 3. The accuracy number to use

From her own training log, `output_dir/mscoco/mambayolo_n/results.csv` — ✅ read directly:

| | Value | Where |
|---|---|---|
| **Best mAP50** | **0.867** | epoch 135 |
| Best mAP50-95 | 0.522 | epoch 135 |
| Precision / Recall | 0.821 / 0.817 | epoch 135 |
| Epochs actually finished | **235** (of 300 requested) | last row |
| Trained on | rented cloud GPU, batch 6, single card | `args.yaml` |

⚠️ **Her slide says 0.873. Her log says 0.867.** Small gap, probably a different run. **Quote 0.867** — it is the one we can point a judge at, in a file we hold. If asked about 0.873, say "that is the figure published by the research group; the run we were given measures 0.867."

The second run (`mambayolo_n10`) tops out at 0.863. Use `mambayolo_n`.

---

## 4. ❌ The ONNX file is broken — tested

**What I did:** loaded `best.onnx` in ONNX Runtime 1.30 on CPU and ran four images through it, including `app/upload/000013.jpg` — an image she has already run, whose result she shipped as `app/static/000013_detected.jpg` showing **holothurian 0.78** and **starfish 0.83**.

**What happened:** ✅ the file loads, ✅ the output shape is correct (`1 × 8 × 8400` = 4 box coordinates + 4 classes), ✅ it runs in ~550 ms per frame — and **the highest confidence over all 8,400 candidate boxes was 0.000.** Same on all four images. Nothing is detected, ever, at any threshold.

**Why:** the export script she left behind (`untitled.py`) traces a model whose core operator is a hand-written CUDA kernel. That kernel cannot be captured into ONNX, so the exported graph is structurally right and numerically empty. The file is 365 MB of nothing.

> 🔴 **Consequence: there is no shortcut.** "Just run the ONNX on CPU with no PyTorch" was the cheap path to an offline demo. It is closed. I left `best.onnx` out of our working copy so nobody loses a day to it; the original is untouched in `advisor/`.

---

## 5. 🔶 What it takes to run `best.pt`

The model needs one custom operator, `selective_scan_cuda_core`. In the code (`ultralytics/nn/modules/common_utils_mbyolo.py:125`) it is called directly with **no fallback** — if the operator is missing, the model cannot run at all, on CPU or GPU.

**The good news:** she shipped it **already compiled**, for Linux x86-64 — we do not need the CUDA compiler.

**The three catches**, all ✅ verified on this laptop:

| | Needs | We have | Gap |
|---|---|---|---|
| Python | **3.11** exactly (the `.so` is built for it) | 3.12 only | must install 3.11 |
| PyTorch | not installed | not installed | must install |
| GPU support in the `.so` | built for sm_70 / sm_80 / sm_90 | RTX 5060 is **sm_120** | must JIT from the embedded `compute_90` PTX |

That last row is the real risk and I could not test it — the PyTorch install was blocked. The `.so` does carry forward-compatible PTX, which is exactly the mechanism that lets an old binary run on a newer GPU, so **it will probably work with a slow first launch.** Probably is not a word we take to a competition.

**If it does not work, the fallback is small and certain:** the CUDA operator can be replaced with ~25 lines of ordinary PyTorch that compute the same thing. Same weights, same accuracy, slower. It removes Python 3.11, the `.so`, and the GPU-architecture question in one go. That is the insurance policy, and it is a couple of hours' work, not a couple of days'.

---

## 6. ⚠️ "Real-time Monitoring" does not use a camera

Her Flask app has three tabs — Video Detection, Image Detection, **Real-time Monitoring**. The third one takes a camera index, ignores it, and plays a hardcoded file called `测试视频.mp4` ("test video"). Original `predict_camera.py`:

```python
def run_camera_processing(camera_index=0):     # camera_index is never used again
    mp4 = "E:/URPC/code_URPC/测试视频.mp4"
    cap = cv2.VideoCapture(mp4)
```

**The 45-second video she sent on 13 September is that footage** — it is the same scene that appears in her platform screenshot on PPT slide 10.

This is almost certainly a debugging shortcut she never took out, not a deception. But **we cannot ship it as-is.** Professional Conduct is 10 points, and standing in front of judges while a recorded file is labelled "real-time monitoring" is exactly what loses them. Fixed in our copy — §7.

Two smaller things in the same file, worth knowing before anyone claims a feature on stage:

- **Login accepts any username and password.** `app.py` never checks anything; `user.py` (which does have real password hashing and MySQL) is never imported. Do not describe this as "user authentication" — it is a placeholder screen.
- **No tracking.** Counts are per-frame. One sea cucumber visible for 100 frames is counted 100 times. Do not call the number on screen a survey count; it is a detection count.

---

## 7. What I changed in our copy

Our editable copy is **`software/advisor_code/`**. Her original in `advisor/Mamba-YOLO-main/` has **not been touched**.

Every change is commented `# OceanEye:` so you can find them with `grep -rn "OceanEye:" software/advisor_code/`.

| File | Change | Why |
|---|---|---|
| `app/app.py` | `E:/URPC/…` paths → derived from the file's own location | nothing opened on Linux |
| `app/app.py` | typo `global_last_uploaded_video_pathc` | it declared a variable that does not exist |
| `app/app.py` | `camera_index` None-check | visiting `/camera_feed` without a parameter crashed with a `TypeError` |
| `app/predict_img.py` | weights path → relative, plus `OCEANEYE_WEIGHTS` override | one knob to swap models |
| `app/predict_img.py` | `.replace('.jpg', …)` → `os.path.splitext` | a `.png` upload **overwrote the original file** and returned the wrong path |
| `app/predict_video.py` | weights path → relative | same |
| `app/predict_video.py` | font list instead of the Windows-only path | on Linux it silently fell back to an 11-pixel font — unreadable on a projector |
| `app/predict_camera.py` | **actually opens the camera**; recorded fallback only if you opt in, and it is stamped `PLAYING RECORDED FOOTAGE - NOT LIVE` | §6 |
| `app/predict_camera.py` | imports the shared helpers instead of a 45-line copy-paste | the font bug existed twice |

Also left out of the copy: `best.onnx` (broken), `last.pt` files, `__pycache__` (stale Python 3.8/3.10/3.11 bytecode), `.idea/`, `flask_session/`. 1.4 GB → 751 MB.

✅ All four edited files pass a syntax check. **None of them have been executed** — that needs PyTorch.

Still carrying her hardcoded cloud paths, untouched because we will not run them: `test.py`, `untitled.py` (the script that produced the broken ONNX).

---

## 8. The decision that has to be made now

Two routes to a demo. **They are not exclusive — Route B is the insurance for Route A, and it costs one afternoon.**

**Route A — run her model.** Install Python 3.11 + PyTorch, load `best.pt`, run it on her 45-second video and on our own footage. If the GPU cooperates this is the strongest possible demo: a real published model, a real patent, real numbers.
*Risk:* the Python 3.11 / PyTorch / sm_120 chain has three places to fail, and we have six days.

**Route B — keep our own pipeline, use it if Route A stalls.** `software/oceaneye` already runs end to end today.
*Risk:* without Route A's weights it has no real model, and a mock detector cannot go on stage.

🔴 **The honest read: Route A is worth the attempt and should start today, because the prize — a real model with a real patent behind it — is not something we can build ourselves this week.** Set a hard cutoff: if `best.pt` has not produced one correct box on one image by **end of Monday 15 September**, stop, switch to the pure-PyTorch operator fallback (§5), and if that also stalls, fall back to Route B and say plainly what we ran.

---

## 9. Ask her these — she can answer in one message

1. **May we use your weights and your test video in a public competition demonstration, with attribution?** Get this in writing. It is the difference between a 4-point attribution slide and a problem.
2. Which PyTorch and CUDA version did you run? *(Saves us a day of guessing — the answer makes Route A nearly mechanical.)*
3. Is `best.onnx` supposed to work? *(We measured zero detections. She may not know.)*
4. Can you send the URPC dataset, or the link you used?
5. **The English slides.**
