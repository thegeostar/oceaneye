# S2 — Software

← [README.md](../README.md) · **how to run it: [`../software/advisor_code/HOW_TO_RUN.md`](../software/advisor_code/HOW_TO_RUN.md)** · what we may claim: [`../advisor/Advisor_Code_Findings.md`](../advisor/Advisor_Code_Findings.md)

**You own:** the AI running, camera → AI, what the judges see on screen, and the backups.
**On stage:** operation minutes **08:00 – 20:00** — the AI section. *Grew from 6½ to 12 minutes on 16 Sept: the 20-minute clock covers the **operation only**, and S3's presentation follows it rather than eating the last 7 minutes. Use the extra time on the turbidity ladder, not on more talking.*
**Today is Wed 16 Sept — three working days.** **Mon 21 we compete, 13:30–17:00, Room 501.** Stage rehearsal **Sun 20, 16:00–18:00** → [competition_days.md](competition_days.md).

---

## ✅ The hard part is done

The model runs. **1.12 s per image, live camera smooth at ~26 fps**, and it reproduces the authors' own published detections byte for byte. The install, the GPU problem and the speed problem are all behind us.

```bash
source .venv311/bin/activate          # NOT .venv — see HOW_TO_RUN.md §0
cd software/advisor_code
python verify_model.py                # must print starfish 0.83 · holothurian 0.78
cd app && python app.py               # http://localhost:8080
```

> 🔴 **`verify_model.py` is the acceptance test and it never changes.** If it stops printing `starfish 0.83` and `holothurian 0.78`, whatever you changed is wrong — revert it. A model that loads but detects nothing looks *identical* to a working one until you run this. That is exactly how the broken ONNX fooled us.

**Class order the model outputs, memorise it:** `0 holothurian` (sea cucumber) · `1 echinus` (sea urchin) · `2 starfish` · `3 scallop`.

**Two things not to burn a day on — both tested and dead:** the ONNX export (zero detections at any threshold) and the prebuilt CUDA `.so` (cannot load on an RTX 5060; we reimplemented that operator in plain PyTorch instead).

---

## Your week — Wed 16 → Fri 18, then on site

**Carried over from Tue 15 — backups and the camera**
- [ ] 🔴 **Back up `best.pt` ×3** — laptop, USB stick, cloud. 139 MB, irreplaceable, and it exists only because the advisor sent it. Do this before anything else.
- [ ] **Lock the camera settings before any AI work** — exposure, white balance, gain, and force MJPG *(a compressed format; without it many USB cameras crawl at ~5 fps)*. Check ≥25 fps. Copy the numbers the driver **reports back** into `../hardware/Purchase_Log.md`, not the ones you asked for.
- [ ] Live end to end: camera in, boxes out, on the Real-time Monitoring tab.
- [ ] 🔴 **The moment S1 hands over the creatures: photograph them in the tank and run**
      `python verify_model.py that_photo.jpg 0.05`
      **Expect weaker results than on her sample images — that is normal, not a broken install.** The AI learnt on murky seabed footage; ours is lit glassware. The `0.05` is what tells you *"it sees a starfish at 0.18 but is hiding it"* apart from *"it truly sees nothing"* — those look identical on screen otherwise. Full procedure and what to do about each outcome: **"Your own tank"** in [`HOW_TO_RUN.md`](../software/advisor_code/HOW_TO_RUN.md) §5.
- [ ] Pick the demo's confidence floor from that test and **write the number down**: `OCEANEYE_CONF=0.10 python app/app.py`. Lowest value that is still clean. Too low = phantom boxes on gravel, which looks worse on stage than a missed creature. **Rehearse with the number you pick.**
- [ ] ⏰ **14:00 — camera not working? Switch to recorded video permanently and never look back.**

**Wed 16 — FEATURE FREEZE**
- [ ] Nothing new after today. "What if we also added…" → **no**.
- [ ] Clean the screen: no debug text, no error spam, fonts big enough for a projector.
- [ ] Copy everything (weights, code, videos, slides) to **2 USB sticks + 1 cloud folder**.
- [ ] Rehearse the turbidity ladder with the team — stir clay in live, log L0–L3. **This is the 15-point Task Difficulty moment.**
- [ ] **Pre-process one video now** and keep the output file on the desktop. That file is your stage insurance — see below.

**Thu 17 — rehearse**
- [ ] **Cold-boot test:** shut the laptop fully down, restart, run the whole demo from nothing, **Wi-Fi off**. This catches what nothing else catches.
- [ ] Rehearse the recovery below until it is boring.
- [ ] Your 08:00–20:00 operation section, three times, no notes.

**Fri 18 — packed and boring**
- [ ] Full run ×2, on time. No code changes.
- [ ] Backup recording on the desktop and it opens. Both USB sticks verified on a second machine.

---

## ⚠️ Stage recovery — what it actually is

There is **no panic key**. The app is a web page with three tabs, so recovery is done by switching tabs, calmly, while talking:

| If this happens | Do this | Say this |
|---|---|---|
| Camera feed freezes or will not open | Switch to the **Video Detection** tab, load the file you pre-processed on Wed | *"Let me switch to our recorded survey footage from yesterday's run."* |
| Nothing is detected in the tank | Switch to **Image Detection**, upload `app/upload/000013.jpg` | *"Here is the same system on the reference dataset image."* |
| The whole app dies | Ctrl+C, `python app.py`, ~10 s to restart. Keep talking to the judges | *"I'm restarting the service — meanwhile, the architecture is…"* |

**Warm the model up before you go on stage.** The first inference takes ~3.8 s, every one after that ~1.1 s. Run one image in the green room so the judges never see the cold start.

### ⭐ The Enhancement button — your best 30 seconds

On the Real-time Monitoring tab there is now an **Enhancement: OFF** button. It flips contrast enhancement on the frames the *model* sees; the video you and the judges watch stays the real murky water.

**Leave it OFF.** We measured it: in clear water it *throws away* 7 of 22 detections, because the model was trained on raw URPC frames and enhancement shifts them off that distribution. It only starts paying once the water is genuinely murky.

That is exactly the clay demo:

1. Clear tank, enhancement **OFF** — boxes everywhere, high confidence.
2. Stir the clay in. Keep talking. Detections fall away as the water clouds.
3. *"At this turbidity the detector has lost most of the targets. Watch."* → press **Enhancement**.
4. Boxes come back.

Measured on simulated turbidity — `python bench_enhance.py` prints the table:

| Turbidity | raw | enhanced |
|---|---|---|
| clear | **22 @ 0.68** | 15 @ 0.60 |
| L2 | 11 @ 0.41 | **17 @ 0.56** |
| L4 heavy | **0** | **8 @ 0.55** |

> ⚠️ **Those numbers are from simulated turbidity, not real clay.** Re-run `bench_enhance.py` on your own tank footage before anyone quotes a number on stage. If the real numbers differ, use the real ones — that is the whole point.

**Never debug on stage.** Switching tabs reads as composure; typing reads as failure.

---

## Say this, never say that

✅ **"Mamba-YOLO — a YOLOv8 architecture in which the feature blocks are replaced with Mamba state-space blocks."** True, matches the code and the patent.

✅ **mAP50 = 0.867** — best epoch in the training log we hold, a file you can show a judge.

✅ **"The published model uses a custom CUDA kernel built for an older GPU generation. We reimplemented that operator in portable PyTorch so it runs on current hardware, and verified it reproduces the original author's published detections exactly. It trades throughput for portability."** ← **This is your strongest answer of the day.** It is real engineering, it is honest, and it shows you understood the model rather than just running it.

❌ **Never 0.873.** That is the authors' full three-module model (CAEM + VSSM + MCFM); we have one of the three. If asked: *"0.873 is the figure published by the research group for their complete method; the weights we were given measure 0.867."*

❌ **Never claim FSCIN or the 87.7 cascade.** We have no super-resolution stage at all. See [Advisor_Code_Findings.md §3](../advisor/Advisor_Code_Findings.md).

❌ **Never call the login "user authentication."** It accepts any username and any password.

❌ **Never call the on-screen number a survey count.** There is no tracking — one sea cucumber seen for 100 frames counts 100 times. It is a detection count.

❌ **Never present recorded footage as live.** The original code did exactly this; ours stamps `PLAYING RECORDED FOOTAGE - NOT LIVE` on screen. Keep it that way.
