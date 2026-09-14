# START HERE — OceanEye, Group 22

**Today is Sunday 13 September. The competition is Saturday 19 September. You have 6 days.**

This page is the only one you have to read. Do the things on it, in the order they appear.

Every technical word is explained the first time it appears. The full word list is at the bottom.

---

# 🔔 Read this first — everything changed today

Prof. Wang sent **four things**: her slides (in Chinese), **her code**, **her trained AI**, and a **45-second underwater test video**. She also said the hardware from China **cannot arrive in time** — we buy our own.

**What that means, in plain terms:**

| Yesterday's plan | Today |
|---|---|
| "Train our own AI on Day 2" | ❌ **Cancelled.** She sent a finished, trained AI. Ours would be worse and scores nothing anyway |
| "Is it YOLOv5 or YOLOv8?" | ✅ **Answered: Mamba-YOLO.** The argument is over |
| "Download the DUO dataset" | ❌ **Not needed.** We are not training |
| "Does any laptop have an NVIDIA graphics card?" | ✅ **Yes — RTX 5060 in this one.** Checked, not assumed |
| Nothing concrete to attribute | ✅ **A real patent number and copyright number.** The 4-point slide, handed to us |
| — | 🔴 **NEW: her AI does not run on this laptop yet.** That is now the whole job |

📄 **What she sent, and what state it is really in → [`02_Advisor/Advisor_Code_Findings.md`](02_Advisor/Advisor_Code_Findings.md)**
📄 **Her slides, in English → [`02_Advisor/PPTX_Translation_EN.md`](02_Advisor/PPTX_Translation_EN.md)**

⚠️ **Two things in her code you must never repeat on stage.** Her **"Real-time Monitoring" button does not use a camera** — it plays a hidden video file. And her **login accepts any password**. Both are fixed or flagged in our copy. Saying "this is live" over a recorded file is precisely what loses Professional Conduct points.

---

## What you are building, in 5 lines

1. A **waterproof USB camera** on a pole, in a clear tank of water, with plastic sea creatures in it.
2. Software on a laptop that watches the video and **draws a box around each creature** and names it.
3. Four creatures only: **sea cucumber, sea urchin, scallop, starfish.**
4. It must work **with the Wi-Fi turned off.** The venue has no internet.
5. You get **20 minutes on stage.** Three of you, one part each.

**The thing that wins:** 25 of the 100 points go to *doing the run smoothly*. Zero points go to how clever the AI is. So rehearse more than you build.

---

# Day 1 — Sat 12 Sept ✅ mostly done

**Only one thing from this day is still open: ⚠️ the camera is not bought.** Step 1 below is still live and still the most time-critical thing S1 does. Steps 2–5 are superseded — read the strikethroughs so you know why, then move to Day 2.

### 1. ⚠️ STILL OPEN — Order the camera — S1 — do this before anything else

Shipping time is what kills you, not money.

Buy: **a waterproof USB endoscope camera** (a small camera on a long cable, sold for looking inside pipes and car engines).

It MUST say one of these: **"UVC"**, **"works with PC"**, **"no driver needed"**.
- *UVC = a standard that makes the laptop treat it like a normal webcam. Without it, our code cannot open the camera at all.*
- ❌ If the listing only shows a phone app → **wrong product, do not buy.**
- ❌ Wi-Fi camera → **wrong product.** Must be a USB plug.

Also buy today:
- A **waterproof LED torch** (~$8–15). ⭐ This matters *more* than a better camera. Explained in Day 2.
- A **clear** plastic box or small aquarium, 40–60 cm (~$10–25). Must be see-through so judges can see the water.
- Plastic toy sea creatures — cucumber, urchin, scallop, starfish (~$5–15).
- 2 × USB flash drives (~$8–12).

Where: Phsar Thmei (Central Market) electronics stalls, Russian Market, Phsar Olympic. Aquarium shops for the tank. Toy stalls for the creatures.

📄 **Full shopping list, prices, and every shop → [`05_Hardware/Hardware_Plan.md`](05_Hardware/Hardware_Plan.md).** Log what you buy in [`05_Hardware/Purchase_Log.md`](05_Hardware/Purchase_Log.md) — the cost slide is worth 3 points.

**Test it in the shop before you pay.** Plug it into a laptop. If the laptop's Camera app shows a picture, it works.

**Write down the delivery date.** If it cannot arrive by **Tue 16 Sept**, stop buying hardware and use recorded video instead. That is a real plan, not a failure.

### 2. ✅ DONE — Send the questions to Prof. Wang — S3

She answered most of them on 13 September by sending the code, the weights and the slides. **`03_Planning/Open_Questions.md` has been rewritten** — the old copy-paste message is gone, because sending it now would ask her for things she already gave us. There are **five new questions**, and one of them matters a lot: written permission to use her model publicly.

### 3. ⏳ CHANGED — Install the software — S2

The old instruction was `pip install ultralytics`. **That is no longer enough.** Her model needs a specific Python version and a matching PyTorch. The install is now Day 2's main job — see below.

What is installed and verified today: `numpy`, `opencv`, `onnxruntime`.

```bash
cd "/home/eng-dararoth/Desktop/Events/2026 World Vocational College Skills Competition"
source .venv/bin/activate
python -c "import cv2, numpy; print('OK')"
```

- *`.venv` = a private folder holding this project's Python software so it can't clash with anything else on the laptop. **Do not move it** — it breaks.*
- *`ultralytics` = the company/library that makes YOLO.*
- *`YOLO` = the detector. It looks at a picture and reports "sea urchin, here, 87% sure". The name means "You Only Look Once" — it scans the image in a single pass, which is why it's fast enough for live video.*
- *`opencv` (imported as `cv2`) = the library that opens cameras and video files and draws on images.*

**Write down the exact commands that worked** in [`06_Software/README.md`](06_Software/README.md). You will need to repeat them under pressure.

📄 **If any of this errors → [`06_Software/README.md`](06_Software/README.md)** has the full install, the Windows commands, and what to do when `.venv` breaks.

### 4. ✅ SUPERSEDED — Download the DUO dataset — S2

**Do not download it.** We are not training, so we do not need training photos.

- *Weights = a file (ends in `.pt`) holding everything the AI has learned. It IS the trained AI.*
- **We already have the weights.** Prof. Wang's `best.pt`, 145 MB, sitting in `06_Software/advisor_code/output_dir/mscoco/mambayolo_n/weights/`. Nothing to download.

🔴 **Back that file up TODAY. Two USB sticks and a cloud folder.** If it is lost we cannot get it back without her, and she is slow. It is the single most valuable file in this project.

📄 Licences still matter — *respect for IP* is 4 points, and we now have the exact numbers to put on the slide → [`02_Advisor/PPTX_Translation_EN.md`](02_Advisor/PPTX_Translation_EN.md) slide 11.

### 5. Run the whole system — S2 — ⭐ needs no camera and no model

The software is already built and it does **not** wait for hardware. Run it today:

```bash
cd 06_Software
python oceaneye_demo.py --profile desk
```

That runs every stage — enhancement, detection, tracking, per-species counting, recording, CSV logging — against a **generated** underwater scene. The screen says `MOCK DETECTOR` in red, because nothing is real except the software. That is the point: you can rehearse the operation, the keys, and the hand-offs **before anything arrives.**

Also run the self-check, so you know the software is intact:

```bash
python test_oceaneye.py        # expect 10/10 passed
```

Screenshot both. That is today's proof of progress, and it does not depend on a shop, a courier, or a reply from Prof. Wang.

📄 **Every way to run it, all the keys, and how to point it at new hardware → [`06_Software/README.md`](06_Software/README.md).**

### 6. Everyone reads their own part of the script — 20 min each

Open `04_Presentation/Operation_Script_v2.docx`. **Read only your own role.** Highlight your lines.

- S1 = minutes 00:00–06:30 (robot + safety)
- S2 = minutes 06:30–13:00 (the AI)
- S3 = minutes 13:00–20:00 (results + Cambodia + attribution)

### 7. Make a shared folder — S3

Script, weights, footage, slides all in one place all three of you can reach.

---

# 🔴 TODAY — Day 2 (Sun 13 Sept) · Make her AI run, build the tank

**If only one thing gets done today: her `best.pt` draws one correct box on one image.**

Everything else this week depends on that single result. Until it happens, we do not know which demo we are giving.

### S2 — the AI · this is the whole job now

**We no longer train anything.** She sent a finished model. Our job is to make it run.

**Why it is not just `pip install`:** her model needs a hand-written piece of GPU code called `selective_scan`. The good news is she shipped it **already compiled** — that saves days. The catch is the compiled file only works with **Python 3.11**, and this laptop has 3.12.

```bash
# Step 1 — get Python 3.11 (her compiled file will not load on 3.12)
sudo add-apt-repository ppa:deadsnakes/ppa && sudo apt update
sudo apt install python3.11 python3.11-venv

# Step 2 — a SEPARATE environment for her code. Do not reuse .venv
cd "/home/eng-dararoth/Desktop/Events/2026 World Vocational College Skills Competition"
python3.11 -m venv .venv311
source .venv311/bin/activate

# Step 3 — PyTorch. This laptop has an RTX 5060, which is very new and needs the cu128 build
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
python -c "import torch; print(torch.__version__, torch.cuda.get_device_name(0))"

# Step 4 — her code, and the compiled GPU piece
cd 06_Software/advisor_code
pip install -e .
pip install ./selective_scan
python -c "import selective_scan_cuda_core; print('the hard part works')"
```

- [ ] 🔴 **Step 4 decides the week.** If that last line prints, you are nearly there. If it says `undefined symbol` or `no kernel image is available`, **stop and say so in the chat** — there is a prepared fallback that deletes this whole problem. It costs an afternoon, not a week. Do not grind at it alone.
- [ ] Then the real test — does it actually *detect*, not just load?
  ```bash
  python -c "
  from ultralytics import YOLO
  m = YOLO('output_dir/mscoco/mambayolo_n/weights/best.pt')
  r = m('app/upload/000013.jpg'); r[0].save('proof.jpg'); print(r[0].boxes)"
  ```
  Open `proof.jpg`. Next to it open `app/static/000013_detected.jpg` — **that is her own result on the same photo**, showing `holothurian 0.78` and `starfish 0.83`. **Your boxes should match hers.** That comparison is the proof. A model that loads but detects nothing looks identical to a working one until you check.
- [ ] Then run it on her video: `python app/app.py`, open `http://localhost:8080`, choose **Video Detection**, load `02_Advisor/Reference_Videos/video_2026-09-13_13-57-08.mp4`.
- [ ] Write down **mAP50 = 0.867**. *mAP50 = a 0-to-1 accuracy score.* It comes from her own training log and you can point a judge at the file. ⚠️ **Never say 0.873** — that is her slide's number, from a run we do not have.
- [ ] Make 3 **before/after** image pairs showing the underwater colour fix. These go on the slides.

> ### ⏰ Hard cutoff: end of Monday 15 September
> No correct box by then → switch to the fallback. If that stalls too → run our own pipeline and say plainly what we ran. **Deciding late is what kills teams, not deciding wrong.**

🔴 **Back up `best.pt` in 3 places today.** Laptop, USB stick, cloud. It cannot be re-downloaded — it only exists because she sent it.

📄 **Everything already tested, including two dead ends you do not need to re-discover → [`02_Advisor/Advisor_Code_Findings.md`](02_Advisor/Advisor_Code_Findings.md)**

### S1 — the tank and the light

Fill the tank. Add gravel and the toy creatures.

⭐ **The single biggest thing you will do this week:**

**Move the light away from the camera.** Turn the camera's own ring lights DOWN or OFF. Put the separate torch **20–40 cm to the side**, pointing at the creatures from an angle.

Why: every speck of dirt in the water bounces a light that sits next to the lens straight back at it. You get glowing white specks and fog. That is called **backscatter**. Moving the light 30 cm sideways removes most of it. Cost: one zip tie. Almost no student team knows this.

Three more, all cheap, all big:
- **Get close.** Work at **10–25 cm** from the creatures, not a metre. Water eats light fast; halving the distance beats any software.
- **Line the far wall with matte black** plastic or card (~$3). Kills reflections and glare.
- **Wipe the lens before every single run.** Rub a trace of dish soap on it — stops bubbles sticking. Put this on the checklist.

Then film **2–3 minutes of footage**. This is your insurance if the live demo fails on stage.

### S3 — slides

Draft the results slides with fake placeholder numbers. Leave the gaps clearly marked. Real numbers arrive Day 3.

### All — read your script section aloud once, with a timer.

---

# Day 3 — Mon 14 Sept · Connect camera to AI

**The hardest day. If only one thing gets done: video goes in, boxes come out, counts appear on screen.**

### Morning — S1 + S2

- [ ] Plug the camera in. Check the laptop sees it:
  ```bash
  python oceaneye_demo.py --source 0
  ```
  *`--source 0` means "use camera number 0". Try `1` or `2` if `0` is the laptop's built-in webcam.*

> ### ⏰ Hard deadline: 14:00
> Camera not working by 2pm? **Switch to recorded video permanently and do not look back.** A rehearsed video demo beats a half-working camera. Make the decision once and move on.

### S2 — lock the camera settings first, before any AI work

By default a webcam constantly re-adjusts its own brightness and colour. That makes detections flicker on and off, which looks broken to a judge, and means your run is never the same twice — which costs you points directly.

Lock it, and **write the numbers down**:

```bash
v4l2-ctl -d /dev/video0 --list-ctrls    # see what your camera supports
v4l2-ctl -d /dev/video0 -c auto_exposure=1 -c exposure_time_absolute=150 \
                        -c white_balance_automatic=0 -c gain=0
```

- *Exposure = how long the sensor collects light per frame. Lock it or brightness drifts.*
- *White balance = what the camera thinks "white" is. Lock it or colours drift.*
- *Gain = electronic brightness boost. It also boosts noise. Keep it at 0 — **add more light instead**.*

Also force **MJPG**: *a compressed video format. Many USB cameras default to a raw format that caps them at ~5 frames per second. MJPG gets you 30.* Check you see **≥25 fps**.

Record the working numbers in [`05_Hardware/Purchase_Log.md`](05_Hardware/Purchase_Log.md) (there is a table waiting for them). Finding them again under pressure on competition day is a nightmare.

📄 **The Python version of this, and why it matters → [`03_Planning/Core_Strategy_Data_Quality.md`](03_Planning/Core_Strategy_Data_Quality.md) §3.**

### S2 — then the AI parts

- [ ] Run detection on the live stream end to end.
- [ ] Turn on **tracking**: `--track`. *Tracking gives each creature a number that follows it between frames. Without it, one sea cucumber seen 100 times is counted 100 times. With it, you count creatures — which is a real measurement.*
- [ ] Show **"Total Counts"** per species on screen.
- [ ] Show **FPS** on screen. *FPS = frames per second, how many pictures it processes each second. Judges will ask if it's really live. Above 20 is real-time.*

### S1 — 🎬 RECORD A BACKUP VIDEO of a perfect full run. Do not skip this.

This is what you play if everything breaks on stage. Put it on the desktop and on a USB stick.

### S3 — replace every placeholder number in the script and slides with the real one.

### All — first full run-through of all three parts. Untimed. Just get through it.

---

# Day 4 — Tue 15 Sept · FEATURE FREEZE

**Write "FEATURE FREEZE" on the wall this morning. Nothing new gets built after today.**

If anyone says "what if we also added…" the answer is **no**. Write it on an "after the competition" list. Adding features late is the single most common way teams lose.

**If only one thing gets done: the full 20 minutes runs twice, start to finish, without crashing.**

- [ ] **S3** — finish the slides, including the **attribution slide**. That slide says which open-source model and which dataset you used, and what is genuinely yours. It is worth **4 points** and almost no team does it. Cheapest points on the board.
- [ ] **S2** — clean the screen. No debug text, no error spam, big readable fonts.
- [ ] **S2** — copy everything (weights, code, videos, slides) to **2 USB sticks + 1 cloud folder**.
- [ ] **S1** — print the pre-flight checklist (it's in the script document). Practise saying it out loud.
- [ ] **All** — rehearse the ⭐ signature moment: **the turbidity ladder.**

### ⭐ The turbidity ladder — your best 60 seconds, costs $2

*Turbidity = how cloudy the water is.*

On stage, you stir a spoon of clay into the tank **live**, and show the AI still working as the water goes murky.

Why it wins: it proves the system is genuinely running and not a pre-recorded video, it creates real difficulty in front of the judges, and no other team will do it.

Rehearse it and fill this in — **three runs per level** — then put the table in your slides:

| Level | Water | Detections | Average confidence |
|---|---|---|---|
| L0 | clear | | |
| L1 | 1 spoon clay | | |
| L2 | 2 spoons | | |
| L3 | 3 spoons | | |

Say out loud where it stops working. **"We measured our operating limit"** is engineering. Pretending it never fails is not, and a judge will catch it.

⚠️ Practise the amount of clay. Too much and you see nothing at all, which is a boring demo.

- [ ] **All** — two full **timed** run-throughs. Record #1 on a phone, watch it back, fix what broke. Run #2 fixes only what broke. **Add nothing.**
- [ ] **All** — Q&A prep. Decide now who answers what. The question bank is in the script document.

---

# Day 5 — Wed 16 Sept · Rehearse until it's boring

**If only one thing gets done: three runs in a row, on time, nobody reading from paper.**

- [ ] Rehearsal #3 — standing up, in realistic conditions.
- [ ] Rehearsal #4 — **deliberately break something** and practise the recovery lines.
- [ ] Rehearsal #5 — **no notes in your hands.**
- [ ] Practise the hand-offs specifically. *"Sophearoth, the feed is yours."* Fumbled hand-offs cost teamwork points, and teamwork is 10 points scored purely by watching you.
- [ ] Mock Q&A — one person plays a hostile judge.
- [ ] **S2 — cold-boot test.** Shut the laptop fully down. Restart. Run the whole demo from nothing, Wi-Fi off. This catches the failures nothing else catches.
- [ ] **S1** — pack the equipment box against the checklist.
- [ ] **S3** — send Prof. Wang a video of the full run.

**Stop on a good run.** Do not end the day on a failure. Sleep matters more than one more rehearsal.

---

# 17–18 Sept · Nothing new

Rehearse and travel only. No code. No features. No new slides.

**Before you travel, all of these must be true:**

- [ ] Full 20-minute run done end to end **at least 5 times**
- [ ] Works with **Wi-Fi off**
- [ ] Works after a **full laptop restart**
- [ ] Backup recording on the desktop, and it opens
- [ ] Everything on **2 USB sticks + 1 cloud folder**
- [ ] Every unconfirmed number in the script has been verified or removed
- [ ] All three can speak their part **without reading**
- [ ] Attribution slide done
- [ ] Safety lines spoken aloud in every rehearsal

---

# 🆘 When something breaks on stage

**Never apologise twice. Never go silent. Never blame the equipment.**

Judges score how you recover. A team that handles a failure calmly can score *higher* than a team that had no failure.

| If this breaks | Say exactly this | Then |
|---|---|---|
| Camera / robot dies | "We will continue with our recorded survey data, collected with this same platform." | S1 opens the backup footage |
| No video reaching laptop | "We will use the survey footage we captured during preparation." | S2 opens the saved file. **Do not debug on stage.** |
| Model crashes | "One moment — we have a verified backup of this run." | S2 plays the backup recording and narrates it live |
| It detects nothing | "The confidence threshold is set high for precision. Let me lower it." | Press the key to drop conf to 0.20. **Know this keystroke by heart.** |
| Laptop freezes | "We will restart — about forty seconds. Meanwhile, let me explain what you're about to see." | S3 talks while S2 restarts |
| You forget your line | "Let me show you directly." | Walk to the screen and describe what's visible |

---

# The 5 rules

1. **Never wait for Prof. Wang.** Ask, then work. Adjust when she answers.
2. **Order hardware before you install software** — shipping is the constraint. But **never let hardware block the software**: `--profile desk` runs the full system with no camera and no model.
3. **Nothing new after Tuesday.**
4. **Maximise capture quality. Do NOT make the scene easy.** Clean, sharp, well-lit footage of *deliberately murky, cluttered water*. Difficulty is worth 15 points — don't throw it away by using clear water.
5. **Never say a number you haven't measured.** "Respect for IP" and honesty are scored directly, and one follow-up question exposes a bluff.

---

# 📖 Word list — every technical term, in plain English

Hand this page to anyone who gets lost.

### The AI itself

| Word | What it means | Why it matters to us |
|---|---|---|
| **AI model** | A file that has learned a pattern from examples. Not a program someone wrote rule by rule. | The thing that finds the creatures |
| **YOLO** | The family our detector belongs to. "You Only Look Once" — scans a picture in one pass, so it's fast enough for live video. | Our whole demo |
| **Mamba** / **state-space model** | A newer way for an AI to look at a picture. Instead of comparing every part to every other part (expensive), it sweeps across the image keeping a running summary. Cheaper, and better at faint, low-contrast things — which is why it suits murky water. | ⭐ **This is what her model uses** |
| **Mamba-YOLO** | The actual model we run: YOLOv8's skeleton, with Mamba blocks inside it instead of the usual ones. | Say **this** name on stage. Not YOLOv5, not plain YOLOv8 |
| **`selective_scan`** | The small piece of hand-written GPU code that does the Mamba sweep. Written in CUDA, not Python, so it must be compiled for your exact Python version and graphics card. | The one thing standing between us and a working demo |
| **CUDA / sm_120** | CUDA is NVIDIA's language for programming a graphics card. `sm_120` is the model number of our RTX 5060's chip generation. Code compiled for an older chip usually still runs on a newer one, but "usually" is doing work in that sentence. | Why Step 4 on Day 2 might fail |
| **Detection** | Finding *where* something is in a picture and *what* it is. Different from classification, which only says what. | "Sea urchin, top-left, 87% sure" |
| **Bounding box** | The rectangle drawn around each creature. | What judges actually see on screen |
| **Confidence** | How sure the AI is, 0 to 1. 0.87 = 87% sure. | Read one aloud on stage — it proves the system is live |
| **Class** | One category the AI can recognise. We have exactly 4. | sea cucumber, sea urchin, scallop, starfish |
| **Weights** / `.pt` file | The file holding everything the AI learned. **This file IS the trained AI.** | Lose it and you lose the week. Back it up 3× |
| **Threshold** (`--conf`) | The minimum confidence needed before a box is drawn. Higher = fewer but surer boxes. | Lower it to 0.20 if nothing shows on stage |

### Training

| Word | What it means | Why it matters to us |
|---|---|---|
| **Dataset** | A folder of photos where humans already drew the correct boxes. | What the AI learns from |
| **DUO** | The specific dataset with exactly our 4 creatures. ~7,800 underwater photos. | Our training data |
| **Training** | Showing the AI thousands of labelled photos until it learns the pattern. | Day 2 |
| **Pretrained** | An AI that already learned general vision from millions of photos. | Always start here |
| **Fine-tuning** | Giving a pretrained AI extra lessons on *your* specific thing. Hours, not weeks. | How we get our 4 creatures. Never train from scratch |
| **Epoch** | One complete pass through all the training photos. | More epochs = longer training, and it earns us **zero points** — don't chase it |
| **mAP50** | A 0-to-1 accuracy score. 0.78 is good. | You say this on stage. It must be real |
| **Augmentation** | Making fake-but-realistic variations of training photos (blurrier, murkier) so the AI copes with more situations. | How we prepare it for cloudy water |
| **Inference** | *Using* a trained AI on new pictures. The opposite of training. | What happens on stage. **No training at the venue** |
| **GPU** | Graphics chip. Trains AI ~50× faster than a normal processor. | If no laptop has one, use Google Colab |
| **Google Colab** | A free AI computer you use in a web browser. | Train there, then bring the `.pt` file home and run it offline |

### Camera and image

| Word | What it means | Why it matters to us |
|---|---|---|
| **UVC** | A standard that makes a USB camera work as a plain webcam, no driver needed. | ⭐ **No UVC = our code cannot open it.** Check before paying |
| **IP67** | Rating meaning fully waterproof when submerged. | It's going in water |
| **OpenCV** / `cv2` | The library that opens cameras, reads video, draws boxes. | Already installed |
| **FPS** | Frames per second — pictures processed each second. Above 20 = real-time. | Show it on screen; judges will ask |
| **Resolution** | Picture size in pixels, e.g. 1280×720. | 720p is plenty — we shrink to 640 anyway. Spend money on light instead |
| **MJPG** | A compressed camera format. | Many cameras default to a raw format stuck at 5 fps. Force MJPG for 30 |
| **Exposure** | How long the sensor collects light per frame. | **Lock it** or brightness drifts between frames |
| **White balance** | What the camera thinks "white" is. | **Lock it** or colours drift and detections flicker |
| **Gain** | Electronic brightness boost — also boosts noise. | Keep at 0. Add real light instead |
| **Backscatter** | Glowing specks and fog from light bouncing off dirt in water, straight back into a lens sitting next to the light. | ⭐ Why the torch goes 20–40 cm to the *side* |
| **Turbidity** | How cloudy the water is. | Our signature demo — and the real condition in Tonle Sap |
| **Enhancement** | Software that fixes underwater colour and contrast. It **redistributes** detail that's already there — it cannot invent detail the camera never recorded. | Great for what humans see. Be honest that it helps the AI less |
| **White balance correction** | Removing the blue-green cast, because water absorbs red light first. | The left/right before-after slide |
| **CLAHE** | Contrast boost applied tile-by-tile, so dark corners get fixed separately from the bright middle. | The other half of the before-after slide |

### Video and results

| Word | What it means | Why it matters to us |
|---|---|---|
| **Tracking** | Giving each creature a number that follows it frame to frame. | Without it, one cucumber seen 100× counts as 100 |
| **Track ID** | That number. | Point at it on screen — it proves counting is real |
| **ByteTrack** | The specific tracking method our code uses. | Turned on with `--track` |
| **Domain shift** | When the AI is trained on one kind of image but shown a different kind — accuracy silently collapses. | ⚠️ **Use the same image processing in training AND on stage.** Otherwise you make it worse while believing you improved it |
| **Domain adaptation** | Fine-tuning on footage from *your own* tank so the AI matches your real conditions. | 200–300 of your own frames beat thousands of foreign ones. Say so openly — it's professional practice |
| **Offline** | Runs with no internet. | Hard requirement. Test with Wi-Fi **off** |
| **Cold boot** | Full shutdown, then restart, then run. | The test that catches what nothing else catches |

### Hardware

| Word | What it means | Why it matters to us |
|---|---|---|
| **ROV** | Remotely Operated Vehicle — a real underwater robot with thrusters. Costs $2,500+. | We are **not** using one. A $30 camera is a *better* story for Cambodia, not a worse one |
| **Tether** | The cable from the underwater camera to the surface. | Ours is the USB cable. Mention it — it's in the script |
| **Endoscope / borescope** | A small camera on a long cable, sold for inspecting pipes and engines. | This is our "robot" |

---

# 📁 Where everything lives

**This page is enough.** Open something else only when a step above sends you there, or when this table matches what you need.

| Open this | When | Whose |
|---|---|---|
| **[`02_Advisor/Advisor_Code_Findings.md`](02_Advisor/Advisor_Code_Findings.md)** | 🆕 ⭐ **Today.** What she actually sent, what was tested, what is broken, and the cutoff decision | S2 |
| **[`02_Advisor/PPTX_Translation_EN.md`](02_Advisor/PPTX_Translation_EN.md)** | 🆕 ⭐ **Today.** Her 13 slides in English, slide by slide. **Slide 11 is your attribution slide** | S3 |
| **[`05_Hardware/Hardware_Plan.md`](05_Hardware/Hardware_Plan.md)** | Before you spend money. What to buy, where in Phnom Penh, what to do if the camera never arrives | S1 |
| **[`05_Hardware/Purchase_Log.md`](05_Hardware/Purchase_Log.md)** | The day you buy anything, and the day the camera arrives. **Also where the locked camera settings live** | S1 |
| **[`06_Software/README.md`](06_Software/README.md)** | ⭐ **Every command you type.** Install, run the demo, keyboard shortcuts, offline checklist | S2 |
| **[`08_Data/README.md`](08_Data/README.md)** | Downloading the datasets · where footage and `best.pt` go | S2 |
| **[`03_Planning/Open_Questions.md`](03_Planning/Open_Questions.md)** | Today, for 5 minutes. Copy the message, send it, move on | S3 |
| **[`03_Planning/Core_Strategy_Data_Quality.md`](03_Planning/Core_Strategy_Data_Quality.md)** | ⭐ Once, properly. *Why* the light goes to the side and *why* you lock the camera | all |
| **[`04_Presentation/Operation_Script_v2.docx`](04_Presentation/Operation_Script_v2.docx)** | ⭐ Daily. **Read only your own role.** Also holds the Q&A bank and fallback lines | all |
| **[`04_Presentation/Script_Risk_Analysis.md`](04_Presentation/Script_Risk_Analysis.md)** | Only if asked why your script differs from Prof. Wang's | S3 |
| **[`03_Planning/5Day_Roadmap.docx`](03_Planning/5Day_Roadmap.docx)** | Every evening — tick the checkpoint table. **Print it** | all |
| **[`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md)** | Starting a new Claude chat. Paste it in and it knows everything | — |
| [`07_Research/Research_Brief.md`](07_Research/Research_Brief.md) | 🛑 **Not this week.** Look-up only — it has a jump table at the top | S2 |
| `01_Competition/` · `02_Advisor/` | The official rules, and Prof. Wang's originals. Reference only | — |
| `99_Archive/` · `.venv/` | Ignore. **Never move `.venv/`** — it breaks | — |

**Nobody reads everything.** S1 owns hardware, S2 owns the AI, S3 owns the slides and the story.

---

# ✅ Daily rhythm

Every evening, paste this into the chat:

> *"Day N done. Here's what we produced: [paste]. Sufficient, or adjust?"*

Then tick the checkpoint table on page 1 of `03_Planning/5Day_Roadmap.docx`.

---

# 📌 Answers still needed from you

1. ~~Does any laptop have an **NVIDIA graphics card**?~~ ✅ **Answered 13 Sept — RTX 5060 Laptop GPU, 8 GB, in this machine.** Checked with `nvidia-smi`, not assumed. *(Still worth knowing: do the **other two** laptops have one? If only one machine can run the model, that machine must be on stage, and it must have a charger.)*
2. How many **hours per day** can all three work, 13–16 Sept?
3. How reliable is your **internet**? *(This one now matters more: Day 2 needs a ~3 GB PyTorch download.)*
4. Can you reach an **electronics market**, or does everything have to ship? *(The camera is the last unbought item.)*
5. 🆕 **Has Prof. Wang given written permission to use her model and her video in a public demonstration?** If not, ask today — see `03_Planning/Open_Questions.md`.

Answer these in chat and the plan gets adjusted the same day.
