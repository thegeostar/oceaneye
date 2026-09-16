# OceanEye — project context

**Paste this file into a new chat and the assistant has the whole project.**
Human? You want [README.md](README.md) instead.

*Current as of 16 September 2026.*

---

## 1. The job

Three students from the Royal University of Phnom Penh — **Eng Dararoth (S1)**, **Povchomreoun Yuleang (S2)**, **Sopheak Sopheaoth (S3)** — are **Group 22** at the 2026 World Vocational College Skills Competition, Southeast Asia Division, Phnom Penh. Roles were assigned by the advisor and must not be swapped.

**Registered project title, word for word** (organisers' list): *"OceanEye: AI Vision-Driven Intelligent Underwater Perception and Detection System"* / `OceanEye—AI视觉驱动的水下智能感知与检测系统`. Older docs said "…Underwater Robot Intelligent Biological Detection System" — that is **not** the registered name.

### The deliverable — two parts, not one

From the invitation letter, *Participation Requirements*, verbatim:

> "they must complete the **skill operation within 20 minutes** at the competition venue, **followed by an on-site presentation**… All participating teams are required to bring their own competition-related equipment."

- **20 minutes = the operation only** (S1 setup/rig 00:00–08:00, S2 the AI 08:00–20:00). A ceiling, not a target.
- **The presentation follows it and has no stated length.** S3 owns it. Unknown → deck flexes 5–10 min. **Do not "correct" this back into one 20-minute block** — that was our misreading until 16 Sept.

### Schedule — from the agenda uploaded 16 Sept, which supersedes the letter's 19–21 Sept version

| Day | What |
|---|---|
| **Sun 20** | 08:00–15:00 registration · **16:00–18:00 drawing lots + rehearsal, Auditorium** ← bring the whole rig |
| **Mon 21** | 08:00–12:00 Groups 1–15 · **13:30–17:00 Groups 16–30 ← us, Room 501** |
| **Tue 22** | 09:00–12:00 results · 14:00–15:20 closing + awards · 15:30–21:00 departure |

Room 501 = New Generation Information Technology track. Group numbering is **per university**, so "Group 22" in the agenda must be confirmed at drawing lots. Detail: [team/competition_days.md](team/competition_days.md).

**Assume no venue internet and no venue GPU.** Everything runs offline on one laptop (Ubuntu, RTX 5060 8 GB, sm_120).

### Scoring — 100 points

| Category | Pts | Notes |
|---|---|---|
| Technical Proficiency | 60 | Standardization 10 · Proficiency 15 · **Task Difficulty 15** · Tech Advancement 15 · Presentation 5 |
| Professional Conduct | 10 | Ethics 4 (**includes respect for IP**) · Craftsmanship 3 · Safety 3 |
| Application Value | 10 | Practicality 4 · Cost-Effectiveness 3 · Sustainability 3 |
| Teamwork | 10 | scored by observation |
| Innovation | 10 | Awareness 4 · Outcomes 6 |

> **No points are awarded for model accuracy.** 25 points go to a smooth, repeatable, rehearsed run. **Rehearse more than you build.**

---

## 2. Whose work this is

The model is **not ours**. Attribution is a scored item, so get the chain right:

| | |
|---|---|
| **Author of the method and code** | **李凯旋 Li Kaixuan** — 2026 undergraduate thesis, Nanjing Vocational University of Industry Technology |
| **Supervisor** | **王丽 Wang Li** (second supervisor 陈宝玉 Chen Baoyu) — she is our advisor, remote, will not attend |
| **Thesis** | *基于深度学习的水下图像超分辨率重建与目标检测方法研究*, May 2026 — `advisor/` |
| **Patent** | 《一种改进的YOLOv8水下图像目标检测方法、装置、介质、程序》, CNIPA 202510291747.5, substantive examination |
| **Software copyright** | 2025SR0806055 |
| **FSCIN chapter published at** | 5th Intl. Conf. on Applied Mathematics, Modeling and Computer Simulation |

Say **"Li Kaixuan's method, supervised by Prof. Wang Li"** — not "Prof. Wang's model". The code confirms it: `predict_img.py` still carries his path, `/Users/likaixuan/…`.

*(The 发明杯 award certificate on deck slide 17 lists a different student team — 李丽颖, 陈路灼, 王博, 周芥宇 — same supervisor, related project. Do not present it as the thesis team.)*

---

## 3. ⚠️ The gap between the deck and what we can run

The advisor's deck (`advisor/OceanEye-Cambodia-Report.pdf`, bilingual, 18 slides) presents a **two-stage cascade**. We hold **one stage, and not the same one**.

| Deck / thesis claims | What is actually in `software/advisor_code/` |
|---|---|
| **Stage 1 — FSCIN** super-resolution (SFAM, FFT+SwinT, texture-structure loss) | ❌ **absent.** No code, no weights, no reference to it anywhere |
| **Stage 2 — "improved YOLOv8"** = C2f replaced by FFEM (**CAEM + VSSM + MCFM**) | ⚠️ **partial.** Only VSSM exists. No CAEM, no MCFM, no FFEM — grep confirms |
| Result: **mAP50 0.873**, cascade **mAP@0.5 87.7** | Our weights are stock **Mamba-YOLO-L**, measured **0.867** |

**Decision taken 15 Sept: demo one stage, credit the rest.** We present what runs — Mamba-YOLO-L, our own measured number — and present FSCIN and the 87.7 cascade as the research group's published work *behind* the system, never as ours. This protects Professional Conduct (10 pts) and turns the gap into an attribution gain.

### The only numbers we may quote as ours

| Number | What it is | Evidence we hold |
|---|---|---|
| **mAP50 = 0.867** | best epoch (135) of the training run we were given | `output_dir/mscoco/mambayolo_n/results.csv` ✅ |
| 0.856 | final epoch (235 of 300 requested) | same file |
| **1.12 s / image** | measured on this laptop | `python verify_model.py` ✅ |
| **~26 fps** camera feed, boxes ~1×/s | measured | `HOW_TO_RUN.md` §8 ✅ |
| starfish 0.83 · holothurian 0.78 | on `000013.jpg`, **byte-identical** to the author's own shipped result | `app/static/000013_detected.jpg` ✅ |

Everything below is **theirs, cite it**: 0.873 and 0.855 (thesis Table 4.2), the 87.7/82.5 cascade (§4.5, and note it is measured against images *they* downsampled ×4), FSCIN's 30.04 dB PSNR (Table 3.1).

---

## 4. What runs today

```bash
source .venv311/bin/activate        # NOT .venv — see HOW_TO_RUN.md §0
cd software/advisor_code && python verify_model.py     # acceptance test
cd app && python app.py             # http://localhost:8080
```

- **Model runs**, 1.12 s/image, on a pure-PyTorch reimplementation of the `selective_scan` operator (the shipped CUDA `.so` cannot load on sm_120). Bit-for-bit identical detections.
- **Flask app**: Image Detection · Video Detection · Real-time Monitoring. Camera tab opens a real camera.
- **Acceptance test that never changes:** `verify_model.py` must print `starfish 0.83` and `holothurian 0.78`. If it does not, revert whatever changed.

Full operating detail: **[software/advisor_code/HOW_TO_RUN.md](software/advisor_code/HOW_TO_RUN.md)**.

### Three things that must never be claimed on stage

1. **Login is a placeholder** — any username and password work. Never call it authentication.
2. **No tracking.** Counts are per-frame. One sea cucumber for 100 frames counts 100 times. It is a detection count, not a survey count.
3. **Recorded footage is stamped** `PLAYING RECORDED FOOTAGE - NOT LIVE`. The original code played a file while labelled real-time; that is fixed, and it must stay fixed.

---

## 5. Settled decisions

| # | Decision | Why |
|---|---|---|
| D1 | Optimise for rehearsal, not accuracy | 25 pts to execution, 0 to mAP |
| D3 | No commercial ROV | US$2,500+, unobtainable. Reframed as cost-effectiveness |
| D4 | ~~UVC USB endoscope on a pole, in the water~~ → **superseded 15 Sept: the lent Logitech 1080p webcam, filming through the glass wall** | A camera is already in hand, so nothing is blocked on shipping. Cost: it sees glass-and-air, not a real underwater light path, which widens the gap to the training data. That is what D20 is for |
| D9 | Capture quality is the top design constraint — **but do not make the scene easy** | Task Difficulty is 15 pts. Clean capture of *deliberately murky* water |
| D10 | Never plan around the advisor replying | remote, another time zone |
| D13 | Run their model, do not train our own | retraining scores nothing |
| D14 | ONNX route is dead | tested: zero detections at any threshold |
| D16 | Pure-PyTorch `selective_scan`, not the shipped CUDA `.so` | 15 Sept — the `.so` targets CUDA 11 / torch 2.2; RTX 5060 needs 12.8 |
| D17 | Demo Stage 2 only; credit FSCIN and the cascade to the authors | 15 Sept — see §3 |
| D18 | Route B (`software/oceaneye/`) retired | 15 Sept — a mock detector cannot go on stage, and Route A runs |
| D19 | **Contrast enhancement ships as a toggle, default OFF** | 15 Sept — measured. In clear water it *costs* 7 of 22 detections, because the model was trained on raw URPC frames. Above ~L2 turbidity it is the only reason there are any (L4: 0 → 8). Gray-world white balance was measured too and was worse at every level — dropped. Evidence: `bench_enhance.py` |
| D20 | **Confidence floor is a knob (`OCEANEYE_CONF`), default unchanged at 0.25** | 15 Sept — all three paths silently used ultralytics' 0.25 and nothing could change it (`Model.predict` merges `custom={"conf":0.25}` *over* `self.overrides`, so only a call-site kwarg wins). Our specimens are off-distribution, so a real detection at 0.18 was indistinguishable from the model seeing nothing. `verify_model.py img.jpg 0.05` now shows what it almost saw |

---

## 6. Open

- 🔴 **The model has never seen our own specimens.** Everything measured so far is on the authors' URPC images. Camera is in hand (Logitech, outside the glass); tank and 4 real specimens still to buy. **This is the largest single unknown left** — the weights are frozen on murky seabed footage and our scene is lit glassware. Procedure for reading the result: "Your own tank" in `HOW_TO_RUN.md` §5. Expect lower confidences; that is not a broken install.
- ⏳ **Enhancement step — built and measured 15 Sept, but on *simulated* turbidity.** `bench_enhance.py` must be re-run on real tank footage once the specimens exist. The numbers on the turbidity slide are not quotable until it is.
- 🆕 **The advisor is sending her underwater enhancement code** (announced 16 Sept; likely the FSCIN stage-1 restoration from §3). **Decision D21: it goes into `bench_enhance.py` as a third measured arm, NOT into the demo path.** Wednesday 16th is the feature freeze, and any enhancement shifts inputs off the distribution the frozen weights were trained on — the same effect already measured for CLAHE. If it beats CLAHE on the turbidity ladder, swap what the existing toggle calls; if it does not, we have an honest slide saying we evaluated the authors' own method and reported the result. Either outcome earns Technological Advancement and IP-respect points; neither risks the demo. **Do not wire it into `predict_video.py` on the strength of it being hers.**
- ⏳ **The demo's confidence floor is not yet chosen.** Default 0.25 holds until someone finds the lowest clean value on the real tank, then pins it and rehearses with it.
- Venue: power, water permitted, set-up time — unconfirmed.
- Pre-competition submission deadline — unverified and dangerous if wrong.
- The deck's part dividers say "Presenter A" / "Presenter B". **We have three speakers.** S3 to resolve.

---

## 7. The plan — three working days, then three days on site

Ordered by *what is unrecoverable if skipped*, not by size. ★ = found by adversarial review 15 Sept.

### Carried over from Tue 15 — still not done, still blocking
1. **Email the organiser.** Submission deadline? Power and plug type? **Projector resolution?** ★ **How long may the presentation run?** — the agenda answered the dates and gave us a Sunday rehearsal, but not these.
2. **Send the permission message** ([team/S3_presentation.md](team/S3_presentation.md) §1) — and ★ **fix the fallback rule now, in writing: if no reply by Thursday noon, we present the model as a third-party component under evaluation and demo no proprietary internals.** Decide it cold, not on stage.
3. ✅ ~~Buy the camera~~ — solved, the lent Logitech, $0. **Now blocking: the tank and four real specimens.** Until they exist the model has never been tested on anything of ours.
4. **Back up `best.pt` ×3** — laptop, USB, cloud.

### Wed 16 — FEATURE FREEZE at end of day
5. ★ **Run the whole demo at 1024×768.** It is being built on a 1920px laptop and shown on a venue projector. If the labels become a grey smear three metres back, the 15 Task Difficulty points are invisible — judges do not award what they cannot see. Fix font and box thickness, not the model.
6. ★ **Pre-measure the clay into a sealed marked bottle.** Clouding the tank is a one-way door: you get *one* attempt and cannot rehearse what follows it. A fixed dose makes rehearsal and the live run the same experiment.
7. ★ Rehearse the **full enhancement A/B**: clear+off, clear+on, turbid+off, turbid+on. Own the control condition before a judge asks for it.
8. ★ **Rename the on-screen `Count` to `Detections in this frame`.** One line. It turns a false measurement claim into a true one without building a tracker.
9. ★ **Strike through FSCIN and the two missing modules on the advisor's architecture slide**, marked "not implemented in this build". The diagram becomes the disclosure.
10. Write the **one-page printed leave-behind** for the judges — policy, cost, sustainability, IP. Those lines are text-scoreable, so hand them over to be read in parallel and spend all 20 spoken minutes on the tank.
11. ★ A **demo-mode checklist**: airplane mode, do-not-disturb, disable sleep and screensaver, lock the resolution. The OS betrays you at minute 14, never in a three-minute test.

### Thu 17 — rehearse the failures, not the happy path
12. ★ **Drop a plastic spoon into the tank on purpose.** The model has four classes and **no reject class** — it will label it confidently. Rehearse the line: *"closed-set detector, no background class — that is a known limitation and it is on our slide."* Have the limitation slide.
13. ★ **Separate the driver from the speaker.** Whoever talks must not touch the keyboard, or every hand-off is 15 seconds of dead air, three times.
14. ★ **Split subsystem ownership** — camera, model, web app — one owner each, able to survive three follow-ups. A judge who asks the quiet one a question is testing Teamwork (10 pts, scored purely by watching).
15. ★ **One rehearsal on battery with the charger locked away.** If it survives setup + 20 minutes unplugged, the venue power unknown disappears entirely.
16. Cold boot, **Wi-Fi off**, full run.

### Fri 18 — frozen and boring
17. Tag a known-good commit. **No changes after the last full rehearsal** — every one invalidates it.
18. Two USBs + cloud. Slides as PDF *and* PPTX.
19. ★ **Pack one crate in reverse-use order and time the setup cold**, sealed crate to first inference. Setup is the only part never practised, and judges are already watching.
20. ★ The teamwork clock **starts when you enter the room and stops when the last cable is coiled.** Most teams go silent and scatter during exactly the minutes that are still being observed.

### Sun 20 — on site, 16:00–18:00
21. **The rehearsal slot is a scored dress rehearsal that does not count.** Bring everything. Test on the venue projector, find the sockets, confirm our slot at drawing lots, ask the presentation length. Anything learned goes into `team/IF_IT_BREAKS.md` that evening.

**Deliberately not doing:** a side-by-side 2.3 s vs 1.12 s speed race (needs the old code path back under a freeze), an on-screen segment timer (a printed card does it), a hot-spare second app instance (4 GB extra VRAM on an 8 GB card risks OOM in the thing it protects), object tracking (no time — say so instead).

**One open licence question worth ten minutes:** Ultralytics YOLOv8 is **AGPL-3.0**, and AGPL §13 attaches to *network interaction*, not file distribution. A Flask app reachable on the venue LAN may trigger it. Cheapest fix: bind to `127.0.0.1` and say you did, or add a `LICENSES/` folder and an offer-of-source line in the footer.

---

## 8. Rules for a fresh session

**Do:** tie every recommendation to a rubric category · assume AI beginners, explain terms once · prefer the cheap offline rehearsable option · give a recommendation, not a menu · update an existing file rather than creating a new one.

**Do not:** suggest retraining, more epochs, or a better model · revive ONNX · suggest buying an ROV, Jetson or Pi · propose tracking as the innovation (it is baseline) · plan around the advisor replying · let recorded footage be shown as live · claim FSCIN, CAEM, MCFM or the 87.7 number as ours · quote any number that has not been measured on this laptop.
