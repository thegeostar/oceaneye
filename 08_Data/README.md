# Data

> **← [START_HERE.md](../START_HERE.md) is the main page. This one just says what goes in these three folders.**
>
> **Owner:** S2 · **Open it when:** saving your own footage (Day 2–3), or backing up weights.
>
> **TL;DR — changed 13 September**
> - ❌ **Do not download DUO or Brackish.** We are not training. Prof. Wang sent a finished model.
> - ✅ The weights that matter are **already on disk**, in her code folder.
> - ⭐ The only data still worth collecting is **your own tank footage**.

Bulk files. Nothing here is written by hand — it is downloaded, recorded, or produced by training.

```
08_Data/
├── datasets/   ⛔ not needed any more — see below
├── footage/    ⭐ video recorded from your own rig — still the point
└── weights/    backups of the model file
```

## ⭐ Where the model actually lives

```
06_Software/advisor_code/output_dir/mscoco/mambayolo_n/weights/best.pt     145 MB
```

That is Prof. Wang's trained Mamba-YOLO, **mAP50 0.867**. It arrived 13 September.

> 🔴 **Back it up today: laptop + 2 USB sticks + cloud.** It cannot be re-downloaded from anywhere. If it is lost we have to ask her for it again, and she is slow. Copy it into `weights/` as well so there is one in this folder where you expect it.

A second, slightly worse run is at `…/mambayolo_n10/weights/best.pt` (mAP50 0.863) — a spare, if the first file ever corrupts.

⚠️ **Ignore `best.onnx`** if you ever see it in her original folder. It is tested and broken — zero detections at any threshold. It is deliberately not in our working copy.

## `datasets/` — ⛔ do not download

**We are not training**, so we do not need training photos. Training earns zero rubric points and her model is better than anything we would produce this week.

Keep these links only for the attribution slide and in case the last-resort plan is ever needed:

- **DUO** — 7,782 images, 74,515 boxes, exactly our four classes. 🔗 https://github.com/chongweiliu/DUO
- **Brackish Underwater** — 14,674 images shot 9 m down in genuinely murky water. 🔗 https://public.roboflow.com/object-detection/brackish-underwater

**What her model was actually trained on: URPC** — 3,717 training / 112 validation images, drawn from a 25,060-image pool. **She did not send the images**, only the config. So we can quote her result with attribution; we cannot reproduce it. Say it that way if asked.

## `footage/` — ⭐ this is the part that is still ours to do

Video from your own tank rig. **This is the most valuable data you will produce**, and it is now the *only* data work left. It is what makes the demo yours rather than a replay of hers.

Suggested naming: `YYYYMMDD_turbidityL0_run1.mp4`

Always record:
- A clean baseline run at each turbidity level (L0–L3) for the ladder demo
- **The Tier-0 backup**: a full perfect run, for use if hardware fails on the day

Also here: **`02_Advisor/Reference_Videos/video_2026-09-13_13-57-08.mp4`** — her 45-second raw seabed clip. It is the footage her own demo runs on, so it is the safest possible input for a first end-to-end test. Use it to prove the pipeline works, then switch to your own.

## `weights/`

- `best.pt` — **copy hers here.** The single most important file in the project.
- Keep `yolov8n.pt` (in her code folder) as the fallback starting point if the last-resort plan is ever needed.

> 🔴 **`best.pt` must exist in three places: laptop, USB stick ×2.** Do it today, not later.

## Not version-controlled

These files are large. If you ever put this project in git, add:

```
08_Data/
06_Software/advisor_code/output_dir/
.venv/
.venv311/
__pycache__/
*.pt
*.onnx
*.mp4
```
