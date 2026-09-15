← [README.md](../README.md) · [The bilingual deck](../advisor/OceanEye-Cambodia-Report.pdf) · [What we may claim](../advisor/Advisor_Code_Findings.md) · [Operation_Script_v2.docx](../presentation/Operation_Script_v2.docx)

# S3 — Slides, Attribution, Cambodia Story

**You own:** the slide deck, the attribution/IP slide, all messages to the advisor, the Cambodia impact story.
**On stage:** minutes **13:00–20:00** — results, Cambodia, attribution, close.
**Today is Tue 15 Sept.** Four working days: Tue 15 → Fri 18. Sat 19 = travel. Competition **Sun 20 – Tue 22**.

---

## 0. ⚠️ Read this before you build a single slide

The advisor's deck presents a **two-stage system**: FSCIN image restoration → improved YOLOv8. **We can run neither of those exactly.** We run one stage, and only one of its three modules.

| Their deck says | We actually have |
|---|---|
| FSCIN super-resolution, 30.04 dB | ❌ nothing — no code, no weights |
| "Improved YOLOv8" = CAEM + VSSM + MCFM | ⚠️ VSSM only (Mamba-YOLO-L) |
| mAP50 **0.873**, cascade **87.7** | **0.867**, from our own log file |

**So: use their slides 3–6 and 15 (policy, pain points, Cambodia scenarios) freely. Slides 7, 9, 10 and 14 are FSCIN — show them only as "the research behind this system", never as our pipeline.** Full detail: [Advisor_Code_Findings.md §3](../advisor/Advisor_Code_Findings.md).

Their deck also has only **two** presenter slots ("Presenter A/B"). We are three. Fix the dividers.

---

## 1. Still outstanding — written permission ⚠️

We are about to show patented work in front of international judges. Permission in writing turns that from a risk into 4 points. Send now, keep working, do not wait.

> Dear Professor Wang,
>
> Thank you very much for the report and for Li Kaixuan's thesis — they answered a great deal, and the bilingual deck is a huge help.
>
> Two requests:
>
> 1. **May we use the trained model and your test footage in our competition demonstration, with full attribution to Li Kaixuan, to you, and to the patent?** We will put the patent number and the software copyright number on our attribution slide. A short written "yes" is all we need.
> 2. If convenient, could you share the URPC2021 dataset or the link? We do not plan to retrain — we would only like to show one labelled example on a slide.
>
> Two things we should report: the `best.onnx` export produces no detections at any threshold on images the `.pt` detects confidently, and the prebuilt `selective_scan` binaries cannot load on our RTX 5060, so we reimplemented that operator in plain PyTorch. It reproduces your published result on `000013.jpg` exactly.
>
> We will send you a video of our full run before the competition.
>
> Thank you,
> Group 22 — Dararoth, Yuleang, Sophearoth

Ask separately and later: *"What is our innovation point, in your view?"* — worth 10 points, and she has seen this competition before.

---

## 2. The attribution slide — paste this literally

> ### Attribution and Intellectual Property
>
> - **Detection model:** Mamba-YOLO — a YOLOv8 architecture in which the feature blocks are replaced with Mamba state-space blocks. Method and implementation by **Li Kaixuan**, supervised by **Prof. Wang Li**, Nanjing Vocational University of Industry Technology. Used with permission.
> - **Patent application 202510291747.5** — *"An improved YOLOv8 underwater image object detection method, apparatus, medium and program"*. Filed with CNIPA on **12 March 2025**, accepted, 10 claims. Inventors: Li Kaixuan, Wang Li, Chen Shuzhuo, Yin Zihang, Zhu Jun.
> - **Software copyright 2025SR0806055** — *"Deep-Learning-Based Underwater Image Enhancement and Object Detection Platform V1.0"*.
> - **Dataset:** URPC2021, YOLO-format labels, 4 classes in this order — `0 holothurian (sea cucumber) · 1 echinus (sea urchin) · 2 starfish · 3 scallop`. Trained on 3,717 training / 112 validation images.
> - **Licences:** Mamba-YOLO (Apache 2.0) · Ultralytics YOLOv8 (AGPL-3.0) · selective-scan operator from VMamba.
> - **What is ours:** porting the model to current hardware — the published CUDA operator could not run on our GPU, so we reimplemented it in portable PyTorch and verified it reproduces the authors' published detections exactly; a 2× inference speed-up with identical output; making the live camera feed genuinely live; a US$30 acquisition platform; our own turbid-water footage and a measured turbidity operating limit.

Say it out loud too: *"The detection model is not ours. It is patented work by our advisor's student, which we run with permission and full credit. What is ours is everything around it — and getting it to run at all on current hardware was real engineering."* That sentence is the 4 points.

---

## 3. The slides to build (keep it to ~10)

| # | Slide | What goes on it |
|---|---|---|
| 1 | Title | OceanEye · Group 22 · Dararoth, Yuleang, Sophearoth. **Not their team's names.** |
| 2 | The problem | Water scatters and absorbs light → low contrast, blur, noise; small creatures look like background. Their deck slide 6 is exactly this — reuse it. |
| 3 | Our platform | Photo of the tank + a **borrowed 1080p USB webcam filming through the glass**, torch 20–40 cm to the side. Say the cost out loud — the camera was **$0**, the whole rig is under $100. Frugality is the point, not an apology. |
| 4 | The model | "Mamba-YOLO — a YOLOv8 architecture in which the feature blocks are replaced with Mamba state-space blocks." State-space models are a 2024 line; linear, not quadratic, in sequence length. |
| 5 | ⭐ Making it run | The honest engineering slide: the published CUDA kernel targets an older GPU generation; we reimplemented it in portable PyTorch and it reproduces their result **byte for byte**. 2.3 s → 1.1 s. **This is the strongest slide we own.** |
| 6 | Results | **mAP50 = 0.867** from the training log we hold. Published comparison: YOLOv8 0.855 → their full method 0.873. Note that APm went *down* (0.402 → 0.391) — saying so earns credit. |
| 7 | ⭐ Turbidity ladder | The L0–L4 table from rehearsal — **and the crossover**. Enhancement *costs* detections in clear water (22 → 15) and rescues them when murky (0 → 8). *"We measured where it stops working, and where the fix starts paying."* Numbers: `bench_enhance.py`, re-run on real tank footage first |
| 8 | Cambodia | §4 below. Their slides 4 and 15 give you 516 community fisheries and four scenarios — use them. |
| 9 | **Attribution** | §2 above, pasted whole. |
| 10 | Thanks | Plus 2–3 *hidden* slides for Q&A: cost breakdown, class list, licence text. |

⚠️ **Deleted from the old plan — we cannot back these:**
- ~~"Counting — track IDs on screen, we count creatures"~~ — **there is no tracking in anything we run.** Counts are per-frame. Claiming otherwise is a Professional Conduct failure.
- ~~"Before/after enhancement: helps human viewing more than the AI"~~ — that was a guess, and it was wrong in **both** directions. Measured 15 Sept: enhancement *hurts* in clear water (22 → 15 detections) and *rescues* the demo in murky water (0 → 8). It now ships as a toggle, default off, and slide 7 carries the real curve. **Say the clear-water loss out loud** — "we turn it off when the water is clean, because it costs us detections" is a far stronger claim than "enhancement helps".

---

## 4. The Cambodia story — say it this way

Do **not** replace their marine framing. Add a transfer layer on top of it:

> *"This technology was developed for marine ranching, where China leads the world. We asked a different question: can it work in the water we actually have? Cambodia's fisheries are inland and highly turbid — the Tonlé Sap in flood season is far harder than clear coastal water. Our contribution is adapting this proven approach to that harder case."*

This flatters the origin technology, hits *regional development* and *rural revitalization* by name, frames turbid water as a **harder** problem (Task Difficulty), reads as China–ASEAN cooperation, contradicts the advisor nowhere, and travels well if we advance to the finals in China.

Their deck hands you the policy anchors free: Pentagonal Strategy Phase I · Digital Economy and Society Framework 2021–2035 · Circular Strategy on Environment 2023–2028 · **516 community fisheries, 472 freshwater / 44 marine**.

⚠️ The four species are North Pacific, not Cambodian. Be first to say so: *"These four species come from the dataset. The method transfers; the species list would be retrained on local fish."*

---

## 5. Your week — Tue 15 → Fri 18

**Tue 15**
- [ ] Send the permission message above. Before anything else.
- [ ] Read §0 and mark which of the advisor's slides you may reuse as-is.
- [ ] Build slides 1–4 and 8–10 with **placeholder numbers in [brackets]** so the gaps are obvious.
- [ ] Write the attribution slide (§2) in full — it needs no data from anyone. Then read your section of `Operation_Script_v2.docx` aloud once, with a timer.

**Wed 16 — FEATURE FREEZE**
- [ ] Replace every placeholder with a real measured number. Anything still in brackets tonight gets **deleted**, not guessed.
- [ ] Deck finished. No new slides after tonight.
- [ ] Two full **timed** run-throughs. Record #1 on a phone, watch it back, fix only what broke.
- [ ] Q&A prep: decide who answers what. You take model-origin, IP, accuracy and Cambodia questions.

**Thu 17**
- [ ] Rehearsals #3, #4 (deliberately break something and practise the recovery line), #5 (**no notes in hand**).
- [ ] Practise the hand-off out loud: *"Sophearoth, the feed is yours."* Fumbled hand-offs cost teamwork points directly.
- [ ] Send the advisor a video of the full run.

**Fri 18**
- [ ] Slides on 2 USB sticks + 1 cloud folder, exported to **PDF** as well as PPTX.
- [ ] Full run with **Wi-Fi off**, after a **cold boot**. Final check: every number on every slide is one you can point at a file for.
- [ ] Sat 19 = travel/rest. **Nothing new.**

---

## 6. Where the points are — verified against `reference/Scoring_Criteria.docx`

| Pts | Item | Note |
|---|---|---|
| **25** | Skill Proficiency 15 + Operational Standardization 10 | ⚠️ There is **no line item called "rehearsal"** — the 25 everyone quotes is these two added together, and rehearsal is how you win both. |
| 15 | Task Difficulty | ✅ The turbidity ladder is this. |
| 15 | Technological Advancement | Mamba-YOLO + the 2025 patent + our port to current hardware. |
| **10** | **Teamwork** | ✅ Team Spirit 5 + Communication 5. Scored purely by watching you. |
| **10** | **Professional Conduct** | Ethics/IP **4** + Craftsmanship **3** + Safety Awareness **3**. |
| **4** | "respect for IP" | ✅ This is §2. Almost no team does it. Cheapest points on the board. |
| **3** | Cost-Effectiveness | ✅ Say "US$30, not US$2,500" and log every purchase. |
| 10+10+5 | Application Value · Innovation · On-site Presentation | Presentation is only **5**, so the deck serves the operation, not the reverse. |

**Four sentences that must never leave your mouth:**
1. "we achieved 0.873" — quote **0.867**; 0.873 is their full three-module model, which we do not have.
2. "this is live" over a recorded file — say *"this is our recorded survey footage"*.
3. "the system has user authentication" — the login accepts any password.
4. "we count individual creatures" — **there is no tracking.** They are per-frame detections.
