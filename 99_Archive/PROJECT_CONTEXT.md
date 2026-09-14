# PROJECT CONTEXT — OceanEye (Group 22)
### Master context file. If you are a fresh Claude session, read this first and you will have the whole project.

> **🤖 This file is for Claude, not for you.** Paste it into a new chat and the assistant knows everything.
>
> **👤 Human? → [START_HERE.md](START_HERE.md).** That page is what to do today. This one is the reference behind it.
>
> **Maintained by:** Eng Dararoth · **Last updated:** 11 September 2026 (evening) · **Update it whenever a decision changes.**

**Jump to:** [§1 rubric](#the-scoring-rubric-official--01_competitionscoring_criteriadocx) · [§2 team & advisor](#2-the-team) · [§4 hardware](#4-hardware--constraints-and-plan) · [§5 software](#5-software-approach) · [§6 decision log](#6-decision-log--what-was-decided-and-why) · [§8 open risks](#8-known-limitations--open-assumptions) · [§10 rules for Claude](#10-guidance-for-a-fresh-claude-session)

---

## 0. Thirty-second summary

Three Cambodian students with **no prior AI experience** must deliver a **20-minute live underwater AI detection demo** at a competition in Phnom Penh on **19–21 September 2026**. Their Chinese advisor supplies the concept and a script but is **remote-only and will not attend**. They have **~US$100** and must buy all hardware themselves. The scoring rubric rewards **rehearsed execution, not model accuracy**. The plan is therefore: a **US$30 waterproof USB camera** in a tank, **the advisor's own trained Mamba-YOLO model** (received 13 Sept, mAP50 0.867, patent-backed), and a **fully offline, heavily rehearsed demo**. The open risk is no longer *what model* — it is *getting her model to run on this laptop before Monday*.

---

## 1. Competition facts

| | |
|---|---|
| **Event** | 2026 World Vocational College Skills Competition — **Southeast Asia Division** |
| **Organiser / Host** | Ministry of Education of the PRC / Cambodia–China University of Technology and Science (CCUTech) |
| **Dates & venue** | **19–21 September 2026**, Phnom Penh, Cambodia |
| **Scale** | 80 teams, 8 countries. Winners advance to global finals **in China** |
| **Theme** | "Skilled Youth, Shining Future" |
| **Track** | New Generation Information Technology (one of three) |
| **Format** | **20-minute live "skill operation"**, then an on-site presentation + Q&A |
| **Equipment** | **Teams bring their own.** Assume no venue internet, no venue GPU |
| **Source** | `01_Competition/Invitation_Letter.pdf` |

### The scoring rubric (official — `01_Competition/Scoring_Criteria.docx`)

| Category | Pts | Sub-criteria |
|---|---|---|
| **I. Technical Proficiency** | **60** | Operational Standardization 10 · Skill Proficiency 15 · Task Difficulty 15 · Technological Advancement 15 · On-site Presentation 5 |
| **II. Professional Conduct** | **10** | Professional Ethics & Norms 4 (**explicitly includes "respect for IP"**) · Craftsmanship 3 · Safety Awareness 3 |
| **III. Application Value** | **10** | Practicality 4 (**"aligned with national strategies… rural revitalization"**) · Cost-Effectiveness 3 · Sustainability 3 |
| **IV. Teamwork** | **10** | Team Spirit 5 · Communication & Collaboration 5 (**scored by observation**) |
| **V. Innovation & Creativity** | **10** | Innovation Awareness 4 · Innovation Outcomes 6 |

> ### ⭐ The single most important strategic fact
> **No points are awarded for model accuracy (mAP) directly.** But **25 points** (Operational Standardization 10 + Skill Proficiency 15) are awarded for a smooth, repeatable, rehearsed run. Optimise for *"the demo visibly works, every time, in that room"* — not for a benchmark number. See §7 for how this interacts with data quality.

---

## 2. The team

| Role | Name | Owns (sprint) | Owns (competition) |
|---|---|---|---|
| **S1** | *(assign)* | Hardware, tank, camera, footage, safety | Underwater Robot Operation & Data Acquisition |
| **S2** | *(assign)* | Model, environment, training, enhancement, offline packaging | AI Algorithm Demonstration |
| **S3** | *(assign)* | Results, slides, application story, attribution, timing | Result Analysis & Application Presentation |

Team members: **ENG DARAROTH**, **POVCHOMREOUN YULEANG**, **SOPHEAK SOPHEAROTH** (Royal University of Phnom Penh).
**Roles were assigned by the advisor and must not be swapped.**

### The advisor — critical working constraint

**王丽 (Wang Li)**, School of Computer Science, based in **China**.

- **Online only. Never meets in person. Will NOT be at the competition.**
- Has sent: an English operation script, two reference videos, role assignments.
- Has **not** sent: the PowerPoint (shown in Chinese on a call, file not shared), model weights, or code.
- Guidance so far has been **thin**. The team must drive.

> **Rule for all planning: never make a plan that depends on her replying, attending, or supplying anything.** Ask, then proceed. Adjust when she answers.

---

## 3. What the project actually is

**Title (hers, use this one):** *OceanEye — AI Vision-driven Underwater Robot Intelligent Biological Detection System*
（OceanEye—AI视觉驱动的水下智能感知与检测系统）

**Pipeline:** underwater image acquisition → AI image processing → target detection → result analysis.

**Target classes (fixed by her script, ✅ confirmed by her code and slide 12):** sea cucumber (*holothurian*), sea urchin (*echinus*), starfish, scallop.
👉 **The output order is `0 holothurian · 1 echinus · 2 starfish · 3 scallop`.** This is **URPC** — China's underwater robot-picking competition data. Confirmed source, no longer a guess.

### What her videos actually show

`02_Advisor/Reference_Videos/`. The first two are phone recordings of Douyin posts from **@DWIRobo**, a commercial ROV vendor — marketing material, not her own work. The third is hers.

| Video | Content |
|---|---|
| `ROV_Operation_WaterTank_61s.mp4` | A **tethered commercial ROV** in an **indoor water tank**, piloted with a **handheld controller with a built-in screen**. Caption specs: **8 thrusters, 12 kg thrust, 100 m depth**. |
| `AI_Detection_YOLOv5-DeepSort_8s.mp4` | A window titled **"YOLOv5 + DeepSort"** on turbid green footage, **"Total Counts: holothurian: 81, echinus: 4"**, per-object **track IDs**. Footage timestamped 2021. ⚠️ **This is NOT her code** — a different project, and the source of a week of confusion. Ignore it |
| `video_2026-09-13_13-57-08.mp4` ★ | **Sent 13 Sept. 45 s, 1280×720, 10 fps, raw green seabed footage** with a diver's collection tool in frame, timestamped 2014. No boxes — it is detector *input*. **It is the footage her own demo runs on** (same scene as her platform screenshot, PPT slide 10), and it is what her "Real-time Monitoring" tab secretly plays |

*(Analysed frame-by-frame with OpenCV — no `ffmpeg` available, so audio was not reviewed.)*

**Implication:** detection **plus tracking plus per-species counting** is the expected **baseline**, not an innovation. Note her shipped code does **not** do tracking — its counts are per-frame. If we add tracking, that is a genuine delta we can claim.

---

## 4. Hardware — constraints and plan

**Budget: ~US$100 total, self-funded. Must be portable and bought in Phnom Penh.** Full detail: `05_Hardware/Hardware_Plan.md`.

A commercial ROV like the one in her video starts around **US$2,500** and cannot be bought, shipped, and learned in the available time. **This was accepted as out of scope, not treated as a failure.**

### The chosen platform

> **A waterproof IP67 UVC USB endoscope/borescope camera (~US$15–40) on a pole or frame, in a clear tank.**

Why this and not something else:
1. **UVC compliance** means the laptop sees it as a plain webcam → `cv2.VideoCapture(0)` works. **This simultaneously solves the "how does video get from the robot into the laptop" problem**, which was the project's biggest technical unknown.
2. It has a **tether and LED lights** — the two things the script narrates.
3. **Cost-Effectiveness and Sustainability are 6 rubric points.** A US$30 rig is a *better* story for Cambodian aquaculture than an imported US$2,500 ROV.
4. It is honestly presentable as an *"underwater image acquisition platform"* — no overclaiming.

### Explicit non-goals
- ❌ **No microcontroller / Arduino / Raspberry Pi.** The camera is USB→laptop. A microcontroller adds failure modes and earns zero rubric points. Only revisit if thrusters are added.
- ❌ **No DIY ROV build.** A school-club ROV is a $100–150, multi-week project. There are 5 working days.
- ❌ **No edge-device deployment.** A Pi would consume most of the budget. Run on the laptop and quote power draw instead.

### Fallback tiers
- **Tier 1 (plan):** USB camera + tank → live demo
- **Tier 0 (insurance):** pre-recorded footage only. Build it regardless — it doubles as the Day 3 backup recording.
- **Decision gate:** if the camera cannot arrive by **Tue 16 Sept**, switch to Tier 0 and stop spending time on hardware.

---

## 5. Software approach

**Environment:** Python venv at project root (`.venv/` — do **not** move it, venvs contain absolute paths). OpenCV + numpy + **onnxruntime** installed; system Python is **3.12 only**. **PyTorch still not installed** as of 13 Sept — now a blocker for her model, see below.

**Hardware (measured 13 Sept):** **NVIDIA RTX 5060 Laptop GPU, 8 GB** (driver 580, CUDA 13.0, **no `nvcc`**), 16 cores, 31 GB RAM, 537 GB free, Ubuntu 24.04. ✅ **The "no GPU → use Colab" assumption is dead — there is a GPU.**

**Model:** ✅ **RESOLVED 13 Sept — she sent the code and the trained weights.** It is **Mamba-YOLO-L**: YOLOv8's neck and head with every `C2f` block replaced by a `VSSBlock` (Mamba state-space block). "Improved YOLOv8" and "Mamba" are both correct; **"YOLOv5 + DeepSort" was a different project — discard it.** Weights `best.pt`, 145 MB, **mAP50 0.867** in her own training log (her slide claims 0.873 — quote 0.867, it is the one we hold). Backed by CNIPA patent application 202510291747.5 and software copyright 2025SR0806055.

⚠️ **The model does not run yet.** It needs PyTorch plus a compiled CUDA operator (`selective_scan_cuda_core`, shipped prebuilt for Linux/**Python 3.11** only; targets sm_70/80/90 + compute_90 PTX, our GPU is sm_120). **Her ONNX export is broken — tested: zero detections on images her own `.pt` detects at 0.78–0.83.** Full tested detail and the fallback plan: `02_Advisor/Advisor_Code_Findings.md`.

**Dataset:** ✅ **URPC**, 4 classes in the order `0 holothurian · 1 echinus · 2 starfish · 3 scallop` (her `URPC/URPC.yaml`, confirmed on PPT slide 12). **She did not send the images** — 3,717 train / 112 val referenced, none included. DUO remains the closest public equivalent if we ever fine-tune; Brackish Underwater is the secondary set for the turbid-water story. **Retraining is not the plan** — it scores nothing (D1) and we now have working weights.

### Code — device-agnostic, and it already runs (D11)

`06_Software/` is a small package behind a thin CLI. **No specific camera, laptop or board is named anywhere in the code** — hardware lives in a `.toml` profile. Full detail: `06_Software/README.md`.

```
oceaneye_demo.py     the command line
oceaneye/
   config.py         device profiles (.toml, read by stdlib tomllib) + CLI override
   vision.py         gray-world white balance, CLAHE, turbidity physics, drawing
   capture.py        any source: camera index · file · image · folder · rtsp · synthetic
   detect.py         YoloDetector | MockDetector, tracking, per-species counting
   session.py        detections.csv · summary.json · settings.json · snapshots · recording
   runner.py         the run loop and the pre-flight check
profiles/            desk.toml (no hardware) · endoscope.toml (the rig) · recorded.toml (Tier 0)
test_oceaneye.py     10 self-checks, numpy+opencv only
```

**The point of the design:** `--profile desk` runs the *entire* pipeline — enhancement, detection, tracking, unique counting, CSV logging, recording — against a **generated** underwater scene using a **mock colour-blob detector**, so the software gets built and rehearsed while the camera is still in a shop. The mock is labelled `MOCK DETECTOR` in red on screen and flagged `"mock": true` in `summary.json`; it must never be presented as the model. Moving to real hardware means editing `profiles/endoscope.toml`, not code.

**Verified working as of 12 Sept:** 10/10 self-checks pass with only numpy+opencv; the real camera path was tested against the built-in webcam (asked 1280×720 MJPG@30, measured 29.9 fps, driver deviations caught and reported).

Three things worth knowing before touching it:
- **Every camera setting is read back from the driver and printed.** `set()` silently fails on many UVC cameras, so record what it *reports*, not what you asked for.
- **Stage-recovery keys:** `p` drops confidence to 0.20, `b` hot-swaps to the backup video (and says so on screen), `e` toggles enhancement. `0`–`3` tag the turbidity level so the ladder table in the slides is measured, not remembered.
- `--preflight` checks model, camera, measured fps, offline status, backup video and disk, then exits without changing anything.

**Still open:** never run against real weights; no waterproof camera yet.

### Her code — our editable copy (D12)

`06_Software/advisor_code/` is our working copy of `02_Advisor/Mamba-YOLO-main/`. **The original is never edited.** Every change we make carries an `# OceanEye:` comment — `grep -rn "OceanEye:" 06_Software/advisor_code/`. Her Flask app (Video Detection · Image Detection · Real-time Monitoring) is the demo she intends us to give.

⚠️ Her **"Real-time Monitoring" tab never opened a camera** — it ignored the camera index and played a hardcoded `测试视频.mp4`. That file is the 45-second video she sent on 13 Sept. Fixed in our copy: it opens the camera, and a recorded fallback is opt-in and stamped `PLAYING RECORDED FOOTAGE - NOT LIVE` on screen. **Presenting recorded footage as live would directly cost Professional Conduct points** — this is not a style preference.

Two more of her features that must not be claimed on stage: **login accepts any password** (it is a placeholder; `user.py` is never imported), and **there is no tracking** — the on-screen numbers are per-frame detection counts, not individuals.

**Hard requirement: the entire demo must run with Wi-Fi switched OFF.** Weights must be pre-cached and verified offline — `--preflight` reports this explicitly.

---

## 6. Decision log — what was decided and why

| # | Decision | Rationale | Date |
|---|---|---|---|
| D1 | **Optimise for rehearsal, not accuracy** | Rubric gives 25 pts to standardization + proficiency, 0 to mAP | 11 Sep |
| D2 | **Do not switch to YOLO26** *(earlier recommendation withdrawn)* | Advisor has a working YOLOv5/v8 pipeline. Switching frameworks days before a demo is how teams lose | 11 Sep |
| D3 | **No commercial ROV** | US$2,500+ and unobtainable in 8 days. Reframed as a cost-effectiveness advantage | 11 Sep |
| D4 | **UVC USB camera as the platform** | Solves acquisition *and* the video-into-laptop problem in one ~US$30 purchase | 11 Sep |
| D5 | **DUO as primary dataset** | Her four species are exactly DUO's class list | 11 Sep |
| D6 | **Feature freeze on Day 4 (Tue 16 Sept)** | Late features are the classic failure mode | 11 Sep |
| D7 | **Keep advisor's script structure and 3 roles; add a localisation layer** | Roles are hers to assign. Cambodia framing is free rubric points and doesn't contradict her | 11 Sep |
| D8 | **Tracking is baseline, not innovation** | Her reference video already shows track IDs + Total Counts | 11 Sep |
| D9 | **Data capture quality is the primary design constraint** | Information lost at capture cannot be recovered in software; it is the cheapest lever on visible demo success | 11 Sep |
| D10 | **Never plan around the advisor responding** | She is remote, in another time zone, and has been slow/thin so far | 11 Sep |
| D11 | **Software-first, device-agnostic: no hardware named in code, only in `.toml` profiles** | The camera did not exist yet and the platform was still unknown. A synthetic scene + mock detector let the whole pipeline be built, tested and rehearsed on day 1, and made the hardware choice reversible instead of load-bearing | 12 Sep |
| D12 | **Work on a copy of her code in `06_Software/advisor_code/`; never edit `02_Advisor/`** | The original is the reference we check against, and the thing we attribute. Every edit is tagged `# OceanEye:` so the diff is always legible to her and to a judge | 13 Sep |
| D13 | **Run HER model (Mamba-YOLO `best.pt`), do not train our own** | She sent real weights with a real patent behind them — a stronger and more honest demo than anything we could train in six days, and retraining scores zero (D1) | 13 Sep |
| D14 | **Abandon the ONNX route** | Tested: her `best.onnx` returns zero detections at any threshold on images her `.pt` detects at 0.78–0.83. The custom CUDA operator does not survive ONNX export. Excluded from our working copy so nobody loses a day to it | 13 Sep |
| D15 | **Hard cutoff Mon 15 Sept on getting `best.pt` to run.** If no correct box on one image by then → switch to the pure-PyTorch `selective_scan` fallback; if that stalls → our own pipeline, stated plainly | A three-link chain (Python 3.11 → PyTorch → sm_120) can eat the whole week silently. The cutoff is what stops that | 13 Sep |

---

## 7. The core strategic insight (read this before proposing anything)

Full treatment: **`03_Planning/Core_Strategy_Data_Quality.md`**.

**The apparent paradox:** accuracy earns no points, yet data quality is the top priority. Both are true.

- What the judges score is **whether the detection visibly works on screen during 20 minutes in that room.** A held-out mAP number is invisible to them.
- **Capture quality is the cheapest, highest-leverage input to that visible success** — far cheaper than more epochs or a bigger model, both of which cost hours and earn nothing.
- **But do not make the *scene* easy.** Task Difficulty is worth 15 points and rewards a genuinely hard case.

> **The rule: maximise capture quality; do NOT minimise scene difficulty.**
> High SNR on a deliberately hard subject. Clean capture of murky water — not clean water.

**The signature demo moment:** stir clay into the tank live, on camera, and show the system continuing to detect as turbidity rises. That is Task Difficulty, Skill Proficiency, and Technological Advancement in one 60-second move, for about US$2.

---

## 8. Known limitations & open assumptions

**Assumptions currently unverified** (see `03_Planning/Open_Questions.md`):
1. A simplified camera platform is acceptable instead of a real ROV — **still unconfirmed.** ⬇️ Risk dropped sharply on 13 Sept: she said the China hardware cannot arrive in time and we must use our own, which is itself the answer
2. ~~The advisor will share the PPT / weights / code~~ — ✅ **done 13 Sept.** Slides (Chinese), code, weights and a test video all received
3. ~~YOLOv5 vs YOLOv8~~ — ✅ **resolved: Mamba-YOLO-L**
4. Presentation is in English — likely; she has promised an English deck, not yet sent
5. No pre-competition submission deadline exists — **unverified and dangerous if wrong**
6. A water tank is permitted at the venue — unconfirmed
7. Venue has no internet — assumed; building offline regardless
8. 🔴 **NEW: that `best.pt` can be made to run on this laptop before 15 Sept** — the single highest-risk open item now. See D15

**Known limitations:**
- Team are absolute AI beginners; every concept needs explaining on first use
- ~~No GPU confirmed~~ — ✅ **RTX 5060, 8 GB, confirmed 13 Sept.** Colab is no longer needed; the constraint moved from *having* a GPU to *software support for a very new GPU* (sm_120)
- Camera shipping time is the binding constraint, not money
- **We have her model but not her data** — her numbers can be quoted with attribution, never reproduced
- Advisor's ROV specs (8 thrusters / 100 m) were read off a vendor video and may not describe any machine the team will ever touch — **do not quote them on stage unverified**
- Videos analysed visually only; audio not reviewed

---

## 9. Folder map

```
START_HERE.md              ← the day-by-day action list + jargon cheat sheet (start here if human)
PROJECT_CONTEXT.md         ← this file (start here if Claude)

01_Competition/            Official event documents
   Invitation_Letter.pdf       format, dates, 20-min rule, bring-own-equipment
   Scoring_Criteria.docx       the official 100-point rubric
   Team_Schedule_AllGroups.xlsx  all 28 groups, advisors, meeting times

02_Advisor/                Everything from Prof. Wang Li — REFERENCE ONLY, never edited
   Advisor_Messages.txt        her messages (roles, video summary, "install Mamba")
   Original_Script_v1.pdf      her English operation script
   Original_Script_v1_extracted.txt   plain-text extraction
   GX_2024_0017_…_李凯旋.pptx    ★ her research deck, Chinese, 13 slides
   PPTX_Translation_EN.md    ★ full English translation, slide by slide
   Advisor_Code_Findings.md  ★ what her code/weights actually are, and what we tested
   Mamba-YOLO-main/            her code + trained weights (copy lives in 06_Software/)
   Reference_Videos/           two Douyin clips + her 45 s underwater test video (13 Sept)

03_Planning/               Day-to-day execution
   5Day_Roadmap.docx           ★ daily tracking sheet, 12–16 Sept — PRINT THIS
   Open_Questions.md           Section A = ask now · Section B = ask later
   Core_Strategy_Data_Quality.md  ★ the core technical strategy

04_Presentation/           What we say and do on stage
   Operation_Script_v2.docx    ★ revised script w/ timing, safety, IP, Q&A, fallbacks
   Script_Risk_Analysis.md     where the advisor's script may be overfitted to last year

05_Hardware/               S1's lane
   Hardware_Plan.md            ★ BOM, Phnom Penh sourcing, tiers, safety
   Purchase_Log.md             what was actually bought, when, for how much

06_Software/               S2's lane
   advisor_code/             ★ OUR editable copy of her Mamba-YOLO. Edits tagged "# OceanEye:"
   oceaneye_demo.py            ★ the CLI — thin, all the flags
   oceaneye/                   the package (config · vision · capture · detect · session · runner)
   profiles/                 ★ desk · endoscope · recorded — hardware lives HERE, not in code
   test_oceaneye.py            10 self-checks; run after any change
   README.md                 ★ every command, the keys, moving to new hardware

07_Research/               Background reading — look-up only, NOT a task list
   Research_Brief.md           beginner's guide + datasets + rubric decode.
                               ⚠️ Written before any resources existed. Its model and
                               dataset advice is superseded by 02_Advisor/Advisor_Code_Findings.md.
                               Still good: §2.6 why underwater is hard, §4.1 what NOT to do,
                               §5.3 the IP/attribution slide draft

08_Data/                   Gitignore-able bulk
   footage/  datasets/  weights/

99_Archive/                Superseded. Ignore.
.venv/                     Python environment — DO NOT MOVE
```

---

## 10. Guidance for a fresh Claude session

**Do:**
- Treat the rubric in §1 as the objective function. Tie recommendations to specific point categories.
- Assume beginners. Explain every term on first use.
- Prefer the cheap, offline, rehearsable option over the technically impressive one.
- Check §6 before recommending anything — a decision may already have been made and reversed.
- Give a recommendation, not a menu of options.

**Do not:**
- ❌ Suggest switching model frameworks (D2)
- ❌ Suggest buying an ROV, Jetson, or Raspberry Pi (D3, §4 non-goals)
- ❌ Suggest a plan that depends on the advisor replying or attending (D10)
- ❌ Suggest training at the venue — inference only, weights frozen beforehand
- ❌ Propose tracking/counting as the innovation (D8)
- ❌ Recommend chasing mAP improvements — they score nothing (D1)
- ❌ Create more documents than necessary; the team is easily overwhelmed. Update existing files first.
- ❌ Hard-code a camera, resolution, device path or model path in the code — it belongs in a `.toml` profile (D11)
- ❌ Propose retraining, more epochs, or a better model. **We have her weights** (D13)
- ❌ Revive the ONNX route — it is tested and dead (D14)
- ❌ Edit anything under `02_Advisor/` — work in `06_Software/advisor_code/` (D12)
- ❌ Let a recorded video be presented as a live camera feed. It costs Professional Conduct points and it is her code's default behaviour, so it must be checked every time

**Current phase as of 13 Sept 2026 (afternoon):** Day 2. **Everything changed today** — the advisor sent her slides, her code, her trained weights and a test video, and told the team the China hardware will not arrive so they must use their own.

- ✅ Resolved: which model (Mamba-YOLO-L), which dataset (URPC), what accuracy (0.867), the IP story (patent + copyright numbers in hand), and that the laptop has an RTX 5060
- ❌ Dead ends found and closed: her ONNX export detects nothing (tested); her "real-time" tab plays a file
- 🔴 **The one thing that matters now:** getting `best.pt` to load and draw one correct box. Needs Python 3.11 + PyTorch. Hard cutoff Mon 15 Sept (D15)
- ⏳ Still outstanding: camera not bought, English slides not received

Sprint runs 12–16 Sept, buffer 17–18, competition 19–21.
