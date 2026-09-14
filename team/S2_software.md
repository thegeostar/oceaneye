# S2 — Software

← [START_HERE.md](../START_HERE.md) · full detail: [`../02_Advisor/Advisor_Code_Findings.md`](../02_Advisor/Advisor_Code_Findings.md) · every command: [`../06_Software/README.md`](../06_Software/README.md)

**You own:** making Prof. Wang's AI run, camera → AI, what the judges see on screen, and the backups.
**On stage:** minutes **06:30 – 13:00** — the AI section.
**Today is Mon 14 Sept. Competition is Sun 20 – Tue 22 Sept.** Five working days.

---

## 🔴 THE ONE THING THAT DECIDES THE WEEK

**Get `best.pt` to draw one correct box on one image.**

Until that happens we do not know which demo we are giving. Nothing else you do this week matters more — not the screen, not the slides, not the camera. Do this before anything else, today.

Two things you must not burn a day on, because they were already tested and failed:

- ❌ **`best.onnx` is broken.** It loads, the output shape is right, it runs at ~550 ms/frame, and the highest confidence over all 8,400 candidate boxes was **0.000** — on four images, including one her own `.pt` detects at 0.78. It is 365 MB of nothing. The "run it on CPU, no PyTorch" shortcut is closed. Do not build on it.
- ❌ **We are not training anything.** She sent a finished model that beats anything we could train in five days, and training scores zero rubric points.

🔴 **Before you install anything: back up `best.pt` in 3 places — laptop, USB stick, cloud.** It is **139 MB** and it exists only because she sent it. It cannot be re-downloaded.

---

## The install, in order

The model needs one hand-written GPU routine called `selective_scan_cuda_core`. Her code calls it directly with **no fallback** — miss it and the model will not run at all, CPU or GPU. She shipped it **already compiled**, which saves us days, but the compiled file only works with **Python 3.11** and this laptop has 3.12. That is the whole reason for steps 1–2.

```bash
# 1. Install Python 3.11 — her compiled file will not load on 3.12
sudo add-apt-repository ppa:deadsnakes/ppa && sudo apt update
sudo apt install python3.11 python3.11-venv

# 2. A SEPARATE environment for her code. Never reuse ../.venv — that is 3.12
#    and it stays 3.12, so a failure here cannot break what already works
cd "/home/eng-dararoth/Desktop/Events/2026 World Vocational College Skills Competition"
python3.11 -m venv .venv311 && source .venv311/bin/activate

# 3. PyTorch. This laptop's RTX 5060 is new enough to need the cu128 build.
#    ~3 GB download — start it and go do something else
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
python -c "import torch; print(torch.__version__, torch.cuda.get_device_name(0))"

# 4. Her code + the compiled GPU piece  ← THIS STEP DECIDES THE WEEK
cd 06_Software/advisor_code
pip install -e . && pip install ./selective_scan
python -c "import selective_scan_cuda_core; print('the hard part works')"
```

**Why step 4 might fail:** the `.so` file was built for GPU generations sm_70 / sm_80 / sm_90. Our RTX 5060 is **sm_120** — newer. It should still run by JIT-compiling from the `compute_90` PTX embedded in the file (PTX = a portable half-compiled form kept inside exactly so an old binary can run on a newer card). Expect a **slow first launch**. "Should" is not a word we take to a competition — hence the cutoff below.

⚠️ **If step 4 says `undefined symbol` or `no kernel image is available`: stop and say so in the chat.** Do not grind at it alone. The prepared fallback replaces that CUDA operator with **~25 lines of ordinary PyTorch** — same weights, same accuracy, slower — and it deletes Python 3.11, the `.so` and the sm_120 question in one move. An afternoon, not a week.

---

## ✅ The verification — loading is not detecting

A model that loads but detects nothing looks **identical** to a working one until you run this. That is precisely how `best.onnx` fooled us.

```bash
python -c "
from ultralytics import YOLO
m = YOLO('output_dir/mscoco/mambayolo_n/weights/best.pt')
r = m('app/upload/000013.jpg'); r[0].save('proof.jpg'); print(r[0].boxes)"
```

Open your `proof.jpg` side by side with **`app/static/000013_detected.jpg`** — her own output on that same photo, showing **holothurian 0.78** and **starfish 0.83**. **Your boxes must match hers.** If they do, the week is won. If `proof.jpg` is empty, you are in the same hole the ONNX was in — go to the fallback.

Class order the model outputs, memorise it: **`0 holothurian` (sea cucumber) · `1 echinus` (sea urchin) · `2 starfish` · `3 scallop`**.

---

## Day by day

**Mon 14 — the model, nothing else**
- [ ] Back up `best.pt` ×3 (laptop, USB, cloud) — **first thing, before any install**
- [ ] Install steps 1–4 above
- [ ] Run the verification. `proof.jpg` matches her `000013_detected.jpg` → say so in the chat immediately
- [ ] Then her web app: `python app/app.py` → `http://localhost:8080` → **Video Detection** → `../../02_Advisor/Reference_Videos/video_2026-09-13_13-57-08.mp4`
- [ ] Write down **mAP50 = 0.867** *(a 0-to-1 accuracy score)* — from her own `results.csv`, epoch 135, a file we hold

**Tue 15 — camera → AI · ⏰ decisions day**
- [ ] **Lock the camera settings before any AI work** — exposure, white balance, gain, and force MJPG *(a compressed format; without it many USB cameras crawl at ~5 fps)*. Check ≥25 fps. Copy the numbers the driver **reports back** into `../05_Hardware/Purchase_Log.md`, not the ones you asked for
- [ ] Live stream end to end: video in, boxes out, per-species counts and FPS on screen
- [ ] ⏰ **14:00** — camera not working? Switch to recorded video permanently and never look back
- [ ] ⏰ **End of day** — the hard cutoff below

**Wed 16 — FEATURE FREEZE**
- [ ] Nothing new gets built after today. "What if we also added…" → **no**
- [ ] Clean the screen: no debug text, no error spam, fonts big enough for a projector
- [ ] Copy everything (weights, code, videos, slides) to **2 USB sticks + 1 cloud folder**
- [ ] Rehearse the turbidity ladder with the team — stir clay in live, log L0–L3

**Thu 17 — rehearse**
- [ ] **Cold-boot test:** shut the laptop fully down, restart, run the whole demo from nothing, **Wi-Fi off**. This catches what nothing else catches
- [ ] Rehearse a deliberate break: press the panic key, open the backup video, keep talking
- [ ] Your 06:30–13:00 section, three times, no notes

**Fri 18 — packed and boring**
- [ ] Full run ×2, on time. No code changes
- [ ] Backup recording on the desktop and it opens. Both USB sticks verified on a second machine

---

## ⏰ Hard cutoff — end of Tuesday 15 September

**No correct box by then → stop, switch to the ~25-line plain-PyTorch operator fallback.** If that also stalls by Wednesday morning → run our own pipeline (`source ../.venv/bin/activate; python oceaneye_demo.py --profile desk`, already works today) and **say plainly on stage what we ran.** Deciding late is what kills teams, not deciding wrong.

**Stage recovery keys — learn by heart:** `p` = panic, drops confidence to 0.20 ("the threshold is set high for precision, let me lower it") · `b` = backup video, stamps `PLAYING RECORDED SURVEY FOOTAGE` on screen · `e` = enhancement on/off, the before/after moment. **Never debug on stage.**

---

## Say this, never say that

✅ **"Mamba-YOLO — a YOLOv8 architecture in which the feature blocks are replaced with Mamba state-space blocks."** True, matches her code and her patent.
✅ mAP50 **0.867**. ⚠️ **Never 0.873** — that is her slide's number, from a run we do not have. If asked: *"0.873 is the figure published by the research group; the run we were given measures 0.867."*
❌ Never call her **"Real-time Monitoring"** tab live — it ignores the camera index and plays a hidden recorded file. Ours is fixed and stamped, hers is not.
❌ Never call her login **"user authentication"** — it accepts any username and any password.
❌ Never call the on-screen number a **survey count** — there is no tracking in her app; one sea cucumber seen 100 frames counts 100 times. It is a detection count.
