# OceanEye — project context

**Paste this file into a new chat and the assistant has the whole project.**
Human? You want [README.md](README.md) instead.

*Current as of 15 September 2026. Competition: Sun 20 – Tue 22 September.*

---

## 1. The job

Three students from the Royal University of Phnom Penh — **Eng Dararoth (S1)**, **Povchomreoun Yuleang (S2)**, **Sopheak Sopheaoth (S3)** — give a **20-minute live underwater AI detection demo** at the 2026 World Vocational College Skills Competition, Southeast Asia Division, Phnom Penh. Roles were assigned by the advisor and must not be swapped.

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
| D4 | UVC USB endoscope camera on a pole, in a tank | ~US$30, `cv2.VideoCapture(0)` just works |
| D9 | Capture quality is the top design constraint — **but do not make the scene easy** | Task Difficulty is 15 pts. Clean capture of *deliberately murky* water |
| D10 | Never plan around the advisor replying | remote, another time zone |
| D13 | Run their model, do not train our own | retraining scores nothing |
| D14 | ONNX route is dead | tested: zero detections at any threshold |
| D16 | Pure-PyTorch `selective_scan`, not the shipped CUDA `.so` | 15 Sept — the `.so` targets CUDA 11 / torch 2.2; RTX 5060 needs 12.8 |
| D17 | Demo Stage 2 only; credit FSCIN and the cascade to the authors | 15 Sept — see §3 |
| D18 | Route B (`software/oceaneye/`) retired | 15 Sept — a mock detector cannot go on stage, and Route A runs |
| D19 | **Contrast enhancement ships as a toggle, default OFF** | 15 Sept — measured. In clear water it *costs* 7 of 22 detections, because the model was trained on raw URPC frames. Above ~L2 turbidity it is the only reason there are any (L4: 0 → 8). Gray-world white balance was measured too and was worse at every level — dropped. Evidence: `bench_enhance.py` |

---

## 6. Open

- ⏳ **Enhancement step — built and measured 15 Sept, but on *simulated* turbidity.** `bench_enhance.py` must be re-run on real tank footage once the camera exists. The numbers on the turbidity slide are not quotable until it is.
- Camera purchase and tank not confirmed in this thread — check with S1.
- Venue: power, water permitted, set-up time — unconfirmed.
- Pre-competition submission deadline — unverified and dangerous if wrong.
- The deck's part dividers say "Presenter A" / "Presenter B". **We have three speakers.** S3 to resolve.

---

## 7. Rules for a fresh session

**Do:** tie every recommendation to a rubric category · assume AI beginners, explain terms once · prefer the cheap offline rehearsable option · give a recommendation, not a menu · update an existing file rather than creating a new one.

**Do not:** suggest retraining, more epochs, or a better model · revive ONNX · suggest buying an ROV, Jetson or Pi · propose tracking as the innovation (it is baseline) · plan around the advisor replying · let recorded footage be shown as live · claim FSCIN, CAEM, MCFM or the 87.7 number as ours · quote any number that has not been measured on this laptop.
