← [START_HERE.md](../START_HERE.md) · [Her slides in English](../02_Advisor/PPTX_Translation_EN.md) · [Operation_Script_v2.docx](../04_Presentation/Operation_Script_v2.docx)

# S3 — Slides, Attribution, Cambodia Story

**You own:** the slide deck, the attribution/IP slide, all messages to Prof. Wang, the Cambodia impact story.
**On stage:** minutes **13:00–20:00** — results, Cambodia, attribution, close.
**Competition moved:** now **Sun 20 – Tue 22 Sept**. Today is **Mon 14 Sept**. Five working days, Sat 19 = travel.

## 1. DO THIS FIRST TODAY — get written permission ⚠️

We are about to show a patented model belonging to her group, in front of international judges. Permission in writing turns that from a risk into 4 points. Send this now on WeChat, then keep working — do not wait for a reply.

> Dear Professor Wang,
>
> Thank you very much for the slides, the code, the model and the test video. We have set up the project and read through your system — it is a great help. We have five short questions:
>
> 1. **May we use your trained model and your test video in our competition demonstration, with full attribution to your group and to the patent?** We would like to put the patent number and the software copyright number on our attribution slide. A short written "yes" from you is all we need.
> 2. Which versions of Python, PyTorch and CUDA did you use to run the model? We are configuring the environment and want to match yours exactly.
> 3. We tried the `best.onnx` file and it produced no detections, although `best.pt` works on your own example images. Is the ONNX export expected to work, or should we use `best.pt`?
> 4. If convenient, could you share the URPC dataset or the link you used? We do not plan to retrain — we would like to show a labelled example on our slides.
> 5. The competition has been moved to **20–22 September**. Will you be available online during those days if we need support? And may we still receive the English version of the presentation?
>
> We are working hard and will send you a video of our full run before the competition.
>
> Thank you,
> Group 22 — Dararoth, Yuleang, Sophearoth

Ask her separately and later (not in this message): *"What is our innovation point, in your view?"* — worth 10 points and she has seen this competition before.

## 2. The attribution slide — paste this literally

Every number below is real and checked against her slide 11 and her `URPC.yaml`. Do not retype from memory.

> ### Attribution and Intellectual Property
>
> - **Detection model:** Mamba-YOLO — a YOLOv8 architecture in which the feature blocks are replaced with Mamba state-space blocks. Developed by **Prof. Wang Li's research group, Nanjing Vocational University of Industry Technology**. Used with her permission.
> - **Patent application 202510291747.5** — *"An improved YOLOv8 underwater image object detection method, apparatus, medium and program"*. Filed with CNIPA (China National Intellectual Property Administration) on **12 March 2025**, accepted, 10 claims. Inventors: Li Kaixuan, Wang Li, Chen Shuzhuo, Yin Zihang, Zhu Jun.
> - **Software copyright 2025SR0806055** — *"Deep-Learning-Based Underwater Image Enhancement and Object Detection Platform V1.0"*, registered.
> - **Dataset:** URPC underwater dataset, YOLO-format labels, 4 classes in this order — `0 holothurian (sea cucumber) · 1 echinus (sea urchin) · 2 starfish · 3 scallop`. The model we run was trained on **3,717 training images / 112 validation images**, from a collected pool of 25,060.
> - **Licences:** Mamba-YOLO (Apache 2.0) · Ultralytics YOLOv8 (AGPL-3.0) · selective-scan operator from VMamba.
> - **Our contribution:** deployment on a US$30 camera platform, our own tank footage, unique counting via tracking (her code counts per frame), and a measured turbidity operating limit.

Say it out loud too: *"The detection model is not ours. It is patented work from our advisor's research group, which we run with her permission and full credit. What is ours is everything around it."* That sentence is the 4 points.

## 3. The slides to build (keep it to ~10)

| # | Slide | What goes on it |
|---|---|---|
| 1 | Title | OceanEye · Group 22 · Dararoth, Yuleang, Sophearoth. **Not her team's names.** |
| 2 | The problem | Water scatters and absorbs light → low contrast, blur, noise; small creatures look like background. One photo, your own words. |
| 3 | Our platform | Photo of the tank + US$30 waterproof USB camera, torch 20–40 cm to the side. Say the cost out loud. |
| 4 | The model | "Mamba-YOLO — a YOLOv8 architecture in which the feature blocks are replaced with Mamba state-space blocks." State-space models are a 2024 line; linear, not quadratic, in sequence length. |
| 5 | Before / after | 3 image pairs, the underwater colour fix. Label honestly: helps human viewing more than it helps the AI. |
| 6 | Results | **mAP50 = 0.867** from the training log we hold. Published table: YOLOv8 0.855 → this method 0.873, +0.018. Note that APm went *down* (0.402 → 0.391) — saying so earns credit. |
| 7 | ⭐ Turbidity ladder | The L0–L3 table from rehearsal. *"We measured where it stops working."* |
| 8 | Counting | Track IDs on screen. Her code counts per frame; we count creatures. |
| 9 | Cambodia | Technology transfer, see §4. Tonle Sap / Mekong photo. |
| 10 | **Attribution** | §2 above, pasted whole. |
| 11 | Thanks | Plus 2–3 *hidden* slides for Q&A: cost breakdown, class list, licence text. |

## 4. The Cambodia story — say it this way

Do **not** replace her marine framing. Add a transfer layer on top of it:

> *"This technology was developed for marine ranching, where China leads the world. We asked a different question: can it work in the water we actually have? Cambodia's fisheries are inland and highly turbid — the Tonle Sap in flood season is far harder than clear coastal water. Our contribution is adapting this proven approach to that harder case."*

This flatters the origin technology, hits *regional development* and *rural revitalization* by name, frames turbid water as a **harder** problem (Task Difficulty), reads as China–ASEAN cooperation, contradicts your advisor nowhere, and travels well if we advance to the finals in China.

⚠️ The four species are North Pacific, not Cambodian. Be first to say so: *"These four species come from the dataset. The method transfers; the species list would be retrained on local fish."*

## 5. Your week — Mon 14 → Fri 18

**Mon 14**
- [ ] Send the permission message above. Before anything else.
- [ ] Build slides 1–5 and 9–11 with **placeholder numbers in [brackets]** so the gaps are obvious.
- [ ] Write out the attribution slide (§2) in full — it needs no data from anyone, so finish it today. Then read your own section of `Operation_Script_v2.docx` aloud once, with a timer.

**Tue 15**
- [ ] Replace every placeholder with a real measured number — including slide 6 (0.867, plus the honest APm note). Anything still in brackets tonight gets **deleted**, not guessed.
- [ ] First untimed run-through of all three parts.

**Wed 16 — FEATURE FREEZE**
- [ ] Deck finished. No new slides after tonight.
- [ ] Two full **timed** run-throughs. Record #1 on a phone, watch it back, fix only what broke.
- [ ] Q&A prep: decide now who answers what. You take model-origin, IP, accuracy and Cambodia questions.

**Thu 17**
- [ ] Rehearsals #3, #4 (deliberately break something and practise the recovery line), #5 (**no notes in hand**).
- [ ] Practise the hand-off out loud: *"Sophearoth, the feed is yours."* Fumbled hand-offs cost teamwork points directly.
- [ ] Send Prof. Wang a video of the full run.

**Fri 18**
- [ ] Slides on 2 USB sticks + 1 cloud folder, exported to **PDF** as well as PPTX.
- [ ] Full run with **Wi-Fi off**, after a **cold boot**. Final check: every number on every slide is one you can point at a file for.
- [ ] Sat 19 = travel/rest. **Nothing new.**

## 6. Where the points are — verified against `01_Competition/Scoring_Criteria.docx`

| Pts | Item | Note |
|---|---|---|
| **25** | Skill Proficiency 15 + Operational Standardization 10 | ⚠️ There is **no line item called "rehearsal"** — the 25 everyone quotes is these two added together, and rehearsal is how you win both. Right idea, wrong label. |
| 15 | Task Difficulty | ✅ The turbidity ladder is this. |
| 15 | Technological Advancement | Mamba-YOLO + the 2025 patent. |
| **10** | **Teamwork** | ✅ Team Spirit 5 + Communication & Collaboration 5. Scored purely by watching you. |
| **10** | **Professional Conduct** | ✅ — but it splits: Ethics/IP **4** + Craftsmanship **3** + Safety Awareness **3**. |
| **4** | Professional Ethics & Norms — "respect for IP" | ✅ This is §2. Almost no team does it. Cheapest points on the board. |
| **3** | Cost-Effectiveness | ✅ Say "US$30, not US$2,500" on stage and log every purchase. |
| 10+10+5 | Application Value · Innovation & Creativity · On-site Presentation | Practicality 4 (§4 is this) + Cost-Eff. 3 + Sustainability 3 · Innovation Awareness 4 + Outcomes 6 · Presentation only **5**, so the deck serves the operation, not the reverse. |

**Three sentences that must never leave your mouth:** "we achieved 0.873" (quote **0.867** — it is in a file we hold; 0.873 is her slide, from a run we do not have) · "this is live" over a recorded file (say *"this is our recorded survey footage"*) · "the system has user authentication" (her login accepts any password).
