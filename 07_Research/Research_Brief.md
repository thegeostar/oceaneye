# OceanEye — Research & Preparation Brief
### AI Vision-Driven Intelligent Underwater Perception and Detection System
**Group 22 · Royal University of Phnom Penh · Track: New Generation Information Technology**

| | |
|---|---|
| **Team** | ENG DARAROTH · POVCHOMREOUN YULEANG · SOPHEAK SOPHEAROTH |
| **Chinese advisor** | 王丽 (Wang Li), School of Computer Science |
| **Advisor meeting** | Fri 11 Sept, 15:00–16:00 Beijing = **14:00–15:00 Phnom Penh** · Tencent Meeting **228-177-824** |
| **Competition** | 2026 World Vocational College Skills Competition — Southeast Asia Division |
| **Dates & venue** | **19–21 September 2026**, Cambodia–China University of Technology and Science (CCUTech), Phnom Penh |
| **Scale** | 80 teams, 8 countries. Winners advance to the global finals in China. |
| **Brief written** | 11 September 2026 · **Revised 11 September (evening) — see revision notice below** |

> ## 🛑 Do not read this file this week
>
> **← [START_HERE.md](../START_HERE.md) is all you need before 19 September.** This is 1,000 lines of background. Reading it will cost you a day you do not have.
>
> **Owner:** S2 · **Open it when:** you need to *look one thing up*, not to study · **Use the jump table below. Never read it top to bottom.**

⚠️ Parts of this file are **out of date** — it was written before Prof. Wang sent her materials. [Read the revision notice](#-revision-notice--read-before-following-any-advice-in-this-document) before acting on anything here.

## 🔍 Look something up

| I need… | Go to |
|---|---|
| What object detection / CNN / transfer learning actually *is* | [Part 2.1–2.5](#part-2--the-research-brief-underwater-ai-vision-from-zero) |
| Why underwater is genuinely hard *(your Task Difficulty argument)* | [Part 2.6](#26-why-underwater-is-genuinely-hard-your-task-difficulty-argument) |
| Copy-paste code: install, first detection, training, tracking | [Part 2.8](#28-code-from-zero-to-working-detector) · [Appendix B](#appendix-b--one-page-quick-reference) |
| Dataset links and licences *(for the attribution slide)* | [Part 1.1](#11-datasets--start-here) |
| The rubric, decoded category by category | [§0.2](#02-the-scoring-rubric-decoded) |
| Our innovation angle — physics-informed turbidity | [Angle 1](#-angle-1--physics-informed-synthetic-turbidity-train-for-the-tonle-sap-without-diving-into-it) |
| **What NOT to do** *(possibly the most useful page here)* | [§4.1](#41-what-not-to-do-this-list-may-be-the-most-valuable-page-here) |
| The IP / attribution slide — 4 easy points | [§5.3](#53-your-ip--attribution-slide-draft-it-now--4-easy-points) |
| A word I don't understand | [Word list in START_HERE.md](../START_HERE.md#-word-list--every-technical-term-in-plain-english) *(shorter and in plain English)* |

---

## ⚠️ REVISION NOTICE — read before following any advice in this document

On the evening of 11 September, Prof. Wang Li sent the team an operation script, two reference videos, and role assignments. Those revealed facts this brief did not know. **Where this document and her materials disagree, her materials win.**

> ### 🔴 SECOND REVISION — 13 September. Most of this document is now historical.
>
> She sent **her code, her trained model, her slides and a test video.** This brief was written when we had none of that and were guessing. **The guesses are now answered by files on disk.**
>
> | This brief says | Actually true |
> |---|---|
> | Choose a model / a dataset | ❌ **Both already decided.** Mamba-YOLO + URPC. Not our choice to make |
> | Train and fine-tune (Part 2.8, Part 3) | ❌ **We are not training.** She sent finished weights, mAP50 0.867 |
> | "Assume no GPU, use Colab" | ❌ **RTX 5060 confirmed in this laptop** |
> | Dataset download links (Part 1.1) | ⚠️ Reference only — do not download |
>
> **Read instead:** [`../02_Advisor/Advisor_Code_Findings.md`](../02_Advisor/Advisor_Code_Findings.md) and [`../02_Advisor/PPTX_Translation_EN.md`](../02_Advisor/PPTX_Translation_EN.md).
>
> **Still genuinely useful here — the reason this file was kept rather than deleted:**
> - **§2.6** why underwater vision is hard — best source for the *Task Difficulty* argument (15 pts)
> - **§4.1** what NOT to do — arguably the most valuable page in the project
> - **§5.3** the IP & attribution slide draft — now fillable with real patent numbers
> - **Appendix A** glossary, when a term in another document is unfamiliar

### What is now SUPERSEDED (do not follow)

| Section | What it says | What is actually true now |
|---|---|---|
| **Part 1.2, "Why YOLO26 specifically"** | Use YOLO26 for the 15 Technological Advancement points | ❌ **Do not switch frameworks.** Her script says *improved YOLOv8*; her reference video shows *YOLOv5 + DeepSort*. **Use whatever already works.** Confirm which one with her — see `OPEN_QUESTIONS.md` Q6. A framework switch with days left is how teams lose. |
| **Part 3.1, the 8-day plan (11→19 Sept)** | Day-by-day schedule | ❌ Replaced by **`OceanEye_5Day_Roadmap.docx`** (12–16 Sept + buffer). Use that, not this table. |
| **Part 4, bonus angle: "multi-object tracking for non-double-counted census"** | Presented as your innovation | ❌ **Already in her reference system.** Her video shows per-object track IDs and a "Total Counts" panel. Tracking is now your *baseline*, not your differentiator. You must still build it — but you cannot claim it as novel. |
| **Throughout: "assume no venue GPU / laptop-only demo"** | Vision-only software demo | ⚠️ Incomplete. The project includes a **physical underwater robot** and three fixed roles. See `OceanEye_Operation_Script_v2.docx`. |
| **Part 1.1 dataset tiers** | Start with Aquarium, then Brackish | ⚠️ Reordered. Her four target species — **sea cucumber, sea urchin, scallop, starfish** — are *exactly* the **DUO** class list. **DUO is now your primary dataset**, not a Tier-2 option. Brackish stays useful for the turbid-water story. |

### What is still fully valid (this is most of the document)

- **Part 2 in its entirety** — the beginner's guide to detection, CNNs, transfer learning, and underwater physics. This is your conceptual foundation and none of it has changed.
- **Part 1.1 datasets** — the catalogue is accurate; only the priority order changed.
- **Part 2.8 code** — preprocessing, training, evaluation, video loop, and tracking all still apply. Substitute your actual model file for `yolo26n.pt`.
- **Part 3.2–3.5** — learning resources, papers, tools, and the offline checklist.
- **Part 4 innovation angles #1 (physics-informed turbidity) and #3 (low-cost edge deployment)** — both still strong, and angle #1 is now *more* valuable because it is the clearest thing that is genuinely yours.
- **§0.2 rubric decode and §5 execution plan** — unchanged and still the most important strategic content here.

### One new hard constraint this document did not know

**Your advisor is in China and will only ever meet you online. She will not be physically present — not during preparation, and not at the competition.** You are also likely buying your own equipment. Everything must therefore be self-sufficient and cheap. See `HARDWARE_PLAN.md`.

---

## Part 0 — What we actually know about your competition (read this before anything else)

This section is not generic advice. It comes from the three official documents in this folder: the CCUTech invitation letter, the finals scoring criteria, and the team/schedule spreadsheet. **Most competing teams will not have read their own rubric carefully. You will.**

### 0.1 The format constraint that changes everything

From the invitation letter, *Participation Requirements*:

> "Teams participating in the on-site competition **must complete the skill operation within 20 minutes** at the competition venue, followed by an **on-site presentation**... All participating teams are **required to bring their own competition-related equipment**."

Three consequences, and they are non-negotiable:

1. **You are being judged on a live 20-minute operation, not on a research paper or a leaderboard score.** Nobody will check whether your mAP is 71.2 or 68.4. They will watch whether your system *works, live, in front of them, without crashing.*
2. **You bring your own equipment.** Assume: no venue internet, no venue GPU, no cloud access, no time to `pip install` anything. Your laptop must run the entire demo **offline, from a cold boot, in under 20 minutes.**
3. **Training happens before 19 September. The venue is for inference only.** Any plan involving "we'll train the model at the competition" is a plan to fail. Train now, freeze the weights, put them on the laptop *and* on two USB sticks.

### 0.2 The scoring rubric, decoded

The official criteria total 100 points across five indicators. Here is what each one actually rewards, translated into actions:

| Indicator | Weight | What wins points |
|---|---|---|
| **I. Technical Proficiency** | **60** | |
| → Operational Standardization | 10 | Follow a written, repeatable procedure. Same steps every time. Looks professional, not improvised. |
| → Skill Proficiency | 15 | Fluent hands on keyboard. No fumbling, no "wait, why isn't this working." **Rehearsal is worth more than features.** |
| → Task Difficulty | 15 | Show something genuinely hard — turbid water, small/occluded targets, real-time video — not one clean photo. |
| → **Technological Advancement** | **15** | "New industry standards, cutting-edge and digital technologies." → Use a **2026-current** model (YOLO26, released Jan 2026), not YOLOv5 from 2020. This is 15 free points for choosing correctly. |
| → On-site Presentation | 5 | Clear logic, key points highlighted, accurate expression. |
| **II. Professional Conduct** | **10** | |
| → Professional Ethics & Norms | 4 | **"Respect for IP"** — explicitly in the rubric. One attribution slide listing every dataset licence and model licence you used. Almost no student team does this. Cheap points. |
| → Craftsmanship | 3 | Clean UI, tidy cabling, labelled equipment, no debug spam in the terminal. |
| → Safety Awareness | 3 | If you demo with water: no mains power near the tank, sealed/battery camera, a towel and a written safety note. Say it out loud during the demo. |
| **III. Application Value** | **10** | Practicality, cost-effectiveness, **sustainability**, and alignment with **national strategies** (rural revitalization, quality employment). → See §0.3. |
| **IV. Teamwork** | **10** | Three named roles, visible hand-offs, all three speak. Judges score this by watching you, so make collaboration *visible*. |
| **V. Innovation & Creativity** | **10** | Originality in integration, new tech application, process improvement. → See Part 4. |

**The strategic read:** 60 of 100 points are Technical Proficiency, and within it, **Skill Proficiency (15) + Operational Standardization (10) = 25 points are pure rehearsal.** They cost you nothing but time and are entirely within your control. A team with a mediocre model and a flawless 20-minute run beats a team with a brilliant model and a crash.

### 0.3 Your Application Value story (worth 10 points, and it's sitting right there)

You are a Cambodian team competing in Phnom Penh. Use it. The judges will hear 79 other pitches; yours should be the one that is obviously *from here*.

The facts to cite:

- Fish provide **more than 50% of the average animal protein intake in Cambodia**.
- The Tonle Sap supports one of the world's largest freshwater fisheries — and long-term Lower Mekong data show fish populations down **87.7%**, with significant declines in over **74% of species**, hitting the largest species hardest.
- Cambodia's policy response is a pivot from capture fisheries to **aquaculture** (striped catfish, tilapia, snakehead, carps).
- Tonle Sap water is **highly turbid** — heavy suspended sediment from the flood pulse. This is not a disadvantage for you; it is the *reason your project is hard and therefore valuable*. Clear-water models fail here.

**Your one-sentence framing:**

> "OceanEye brings low-cost AI vision to Cambodia's aquaculture and inland fisheries — automated fish counting, size estimation, and debris detection in the turbid water where conventional vision systems fail — supporting food security and rural livelihoods for the 50%+ of Cambodian protein that comes from fish."

That sentence hits Practicality, Sustainability, national strategy alignment, and rural revitalization in one breath. Memorize it.

### 0.4 Who else is in your track (from the schedule file)

Same track, New Generation Information Technology — worth knowing:

- **Group 7** — Cross-Scenario Person Re-Identification (advisor 高尚)
- **Group 28** — SmartVision Campus, multi-camera cross-camera tracking (advisor 朱其慎)
- **Group 12** — Low-altitude hyperspectral remote sensing for agriculture (advisor 孟令武)
- **Group 25** — Multi-crop ripeness detection & yield prediction (advisor 高国强)

Groups 7 and 28 are doing detection + tracking on *land*. Groups 12 and 25 are doing detection in *agriculture*. **Your differentiator is the physics of water** — light absorption, scattering, turbidity. Nobody else has to solve that. Lean on it hard: it is your Task Difficulty score (15 pts) and half your Innovation score.

Practically: Groups 7 and 28 will hit the same tracking and small-object problems you will. Talk to them. Shared debugging is free, and the rubric rewards collaboration.

### 0.5 Questions to ask Wang Li today

Write these down before the 14:00 call:

1. **Is the 20-minute operation a fixed script given to us on the day, or do we design it ourselves?** (This determines everything.)
2. **What hardware can we bring? Is there a camera / water tank / test rig at the venue, or do we supply everything?**
3. **Will there be internet at the venue?** (Assume no; confirm.)
4. **Is the presentation in English or Chinese? How long? Slides allowed?**
5. **Does "underwater" mean real water, a tank, or video playback?** A pre-recorded video demo is far lower-risk — confirm whether it is acceptable.
6. **Does she have access to Chinese datasets or lab equipment we don't** — e.g. URPC competition data, a lab water tank, a Jetson board?
7. **What does she consider the innovation point?** She has seen this competition before. Her answer is worth more than this entire document.

---

# Part 1 — Curated Datasets & Code Repositories

Difficulty flags: 🟢 **Beginner** (download and use today) · 🟡 **Intermediate** (needs setup/conversion) · 🔴 **Advanced** (research-grade, read about it but don't depend on it).

## 1.1 Datasets — start here

### 🟢 Tier 1: Use these in week one

**1. Aquarium (Roboflow Public)** — *your day-1 dataset*
🔗 https://public.roboflow.com/object-detection/aquarium
- **Size/type:** 638 images, 7 classes — fish, jellyfish, penguin, shark, puffin, stingray, starfish. Bounding boxes.
- **Licence:** CC BY 4.0 (attribution required — put it on your IP slide).
- **Why it's relevant:** Small enough to train in ~15 minutes on a free Colab GPU. Exports directly to YOLO format with one click, so there is zero data-wrangling. It is the fastest possible path from "no model" to "working model."
- **Honest caveat:** These are *aquarium* images — clear water, good lighting. They are **not** representative of Tonle Sap conditions. Use this to learn the pipeline, then move to Brackish.
- **Difficulty:** 🟢 Beginner.

**2. Brackish Underwater (Aalborg University)** — *your realism dataset, and the closest public analogue to Cambodian water*
🔗 https://public.roboflow.com/object-detection/brackish-underwater
- **Size/type:** 14,674 images (12,444 annotated), 960×540 and 1920×1080 versions. Classes: fish, small fish, crab, shrimp, jellyfish, starfish.
- **Licence:** CC BY 4.0. Cite Pedersen et al., CVPR Workshops 2019, *"Detection of Marine Animals in a New Underwater Dataset with Varying Visibility."*
- **Why it's relevant:** **This is the single most important dataset for your story.** It was captured by a camera mounted 9 m below the surface of the Limfjords bridge in Denmark — brackish, turbid, *genuinely murky* water with varying visibility. The name of the paper literally contains "varying visibility." When you tell judges "we trained for turbid water like the Tonle Sap," this is your evidence.
- **Difficulty:** 🟢 Beginner (Roboflow-hosted, one-click YOLO export).

**3. DUO — Detecting Underwater Objects** — *the academic benchmark*
🔗 https://github.com/chongweiliu/DUO · mirror: https://figshare.com/articles/dataset/DUO_zip/25370527
📄 Paper: https://arxiv.org/abs/2106.05681
- **Size/type:** 7,782 images (6,671 train / 1,111 test), 74,515 bounding boxes, 4 classes: holothurian (sea cucumber), echinus (sea urchin), scallop, starfish.
- **Why it's relevant:** DUO is a *cleaned re-annotation* of the URPC 2017–2020 underwater robot competition datasets, which were full of labelling errors. If you want to say "we benchmarked against the standard," this is the standard. It is also **Chinese-origin data from the URPC robot-picking competition** — Wang Li will likely recognize it immediately, which is worth something.
- **Difficulty:** 🟡 Intermediate (needs conversion from COCO JSON to YOLO txt format — ~20 lines of Python).

### 🟡 Tier 2: Add if time allows

**4. RUOD (Real-world Underwater Object Detection)**
🔗 Search "RUOD dataset underwater" — dlut-dimt GitHub
- **Size/type:** 14,000 images, 74,903 labels, **10 classes**: fish, diver, starfish, coral, turtle, echinus, holothurian, scallop, cuttlefish, jellyfish.
- **Why it's relevant:** Most *diverse* underwater set available, and includes a **diver** class — useful if you want a safety/human-detection angle. RUOD and DUO are the two datasets recommended in the literature as unified benchmarks.
- **Difficulty:** 🟡 Intermediate.

**5. TrashCan 1.0 — underwater marine debris** — *your sustainability angle*
🔗 https://doi.org/10.13020/g1gx-y834 · 📄 https://arxiv.org/pdf/2007.08097
- **Size/type:** 7,212 images, instance segmentation + bounding boxes. Two variants: TrashCan-Material and TrashCan-Instance.
- **Companion:** **Trash-ICRA19** — 7,683 images at 480×320, bounding boxes. 🔗 https://irvlab.cs.umn.edu/resources/trash-icra19
- **Why it's relevant:** The rubric awards 3 points for **Sustainability** ("environmental awareness; green and low-carbon"). Adding a "plastic bottle / debris" class to your detector turns OceanEye from a fish counter into an *environmental monitoring* system. This is a genuinely cheap way to buy those points — it is one extra class in your training data.
- **Difficulty:** 🟡 Intermediate.

**6. DeepFish (James Cook University)**
🔗 https://github.com/alzayats/DeepFish · 📄 https://www.nature.com/articles/s41597-022-01416-0
- **Size/type:** ~40,000 images from 20 habitats in tropical Australia. Three subsets — FishClf (classification), FishLoc (point annotations), FishSeg (segmentation).
- **Why it's relevant:** Tropical habitats, closer to SE Asian conditions than Denmark. Large and well-documented in *Scientific Data*.
- **Caveat:** Point and segmentation labels, **not** bounding boxes — you'd need conversion. Don't start here.
- **Difficulty:** 🟡 Intermediate.

**7. OzFish (Australian Institute of Marine Science)**
- **Size/type:** ~43,000 bounding box annotations across ~1,800 images.
- **Why it's relevant:** Very dense annotations (~24 fish per image) — excellent for learning small/crowded object detection. Used as a benchmark in the YOLO-Fish paper.
- **Difficulty:** 🟡 Intermediate.

### 🔴 Tier 3: Know they exist, cite them, don't depend on them

**8. FathomNet (MBARI / NOAA / National Geographic)**
🔗 https://fathomnet.org · https://www.mbari.org/data/fathomnet/ · 📄 https://www.nature.com/articles/s41598-022-19939-2
- **Size/type:** Very large, growing, deep-sea ROV/AUV imagery spanning 30+ years of deployments. Web-service API, taxonomic hierarchy, and an ML model zoo.
- **Why it's relevant:** Strong *citation* value — MBARI reported that FathomNet-trained models **cut human annotation effort by 81% and increased labelling rate tenfold.** That is a perfect statistic for your Application Value slide ("this approach is proven to reduce expert workload by 81%").
- **Caveat:** Deep-sea imagery is a different domain from shallow turbid lake water. Great for the pitch, less useful for your actual model.
- **Difficulty:** 🔴 Advanced (API-based access).

**9. UIEB — Underwater Image Enhancement Benchmark**
🔗 https://li-chongyi.github.io/proj_benchmark.html
- **Size/type:** 950 real underwater images, 890 with high-quality reference (ground-truth "corrected") images.
- **Why it's relevant:** The standard dataset for *image enhancement* (making murky images clear), not detection. If you build a before/after enhancement demo — and you should, it is visually spectacular for judges — this is where the data and the Water-Net reference model come from.
- **Difficulty:** 🟡 Intermediate.

**10. EUVP** — paired and unpaired underwater images for training FUnIE-GAN. Companion dataset to the enhancement repo in §1.2. 🔴 Advanced.

**11. AQUA20** — benchmark for underwater *species classification* under challenging conditions (turbidity, low light, occlusion). 📄 https://arxiv.org/pdf/2506.17455. 🔴 Advanced.

**12. COU — Common Objects Underwater** — robustness-focused detection benchmark. 📄 https://arxiv.org/pdf/2502.20651. 🔴 Advanced.

### 📚 The meta-resource
**Collection of Underwater Object Detection Datasets**
🔗 https://github.com/mousecpn/Collection-of-Underwater-Object-Detection-Dataset
One curated list linking most underwater detection datasets. Bookmark it; it saves an hour of searching.

---

## 1.2 Code repositories

### 🟢 The one you will actually use

**Ultralytics (YOLO26 / YOLO11)**
🔗 https://github.com/ultralytics/ultralytics · Docs: https://docs.ultralytics.com/models/yolo26/
- **What it is:** The training + inference framework for the YOLO family. `pip install ultralytics` gives you detection, segmentation, pose, classification, oriented detection, **and monocular depth estimation** in one API.
> ⛔ **SUPERSEDED — read this box before the paragraph below.** Your advisor's pipeline is **YOLOv5 + DeepSort** (per her video) or **improved YOLOv8** (per her script). **Do not switch to YOLO26.** Keep the paragraph below only as background on why newer detectors handle small objects better — that argument still supports *her* multi-scale-fusion improvements, which is what you will actually present. Confirm the model with her: `OPEN_QUESTIONS.md` Q6.

- **Why YOLO26 specifically (released January 2026):** *(background only — not your build target)* This is a 15-point *Technological Advancement* argument in the abstract. YOLO26 removed two long-standing bottlenecks — **Distribution Focal Loss (DFL)** and **Non-Maximum Suppression (NMS)** — giving **native end-to-end, NMS-free inference**. It adds **STAL (Small-Target-Aware Label Assignment)**, **ProgLoss (Progressive Loss Balancing)**, and the **MuSGD optimizer**. Across five scales it reaches **40.9–57.5 mAP on COCO at 1.7–11.8 ms** (T4 TensorRT), with up to **43% faster CPU ONNX inference** for YOLO26n vs YOLO11n.
- **Why those two features matter for *you* specifically — say this to the judges:**
  - **STAL is small-target-aware label assignment.** Underwater objects are small, distant, and low-contrast. A 2026 model with an explicit small-target mechanism is *technically the right choice for this problem*, not just the newest one. That is the difference between "we used the latest" and "we used the latest *for a reason*."
  - **NMS-free inference** removes a post-processing step, which means lower and more *predictable* latency on a CPU laptop — exactly what you need for a live demo with no GPU.
- **Licence:** ⚠️ **AGPL-3.0.** This matters for your IP slide (4 pts). AGPL is fine for an open academic/competition project, but you must say so: *"Ultralytics YOLO26 is used under AGPL-3.0; our code is released under the same licence."* Mentioning this unprompted is exactly the "respect for IP" the rubric asks for.
- **Difficulty:** 🟢 Beginner — genuinely 3 lines to a working detector.
- **Model checkpoints:** `yolo26n.pt` (nano — use this), `yolo26s.pt`, `yolo26m.pt`, `yolo26l.pt`, `yolo26x.pt`. Task variants: `-seg`, `-sem`, `-depth`, `-cls`, `-pose`, `-obb`.

> **Fallback:** If `yolo26n.pt` gives you any trouble in the next 8 days, **switch to `yolo11n.pt` immediately and don't look back.** A working YOLO11 demo scores far more than a broken YOLO26 one. Test both this week and keep whichever is stable.

### 🟢 Beginner-readable underwater examples

**Underwater Object Detection using YOLOv8** — https://github.com/ShahidHasib586/Underwater-object-detection-using-yolov8
Straightforward, readable end-to-end project: dataset → train → predict. Good to read *before* you write your own. 🟢

**Underwater Animal Detection** — https://github.com/HarishValliappan/Underwater-Animal-Detection
Similar, with downloadable weights. 🟢

**YOLO-Fish** — https://github.com/tamim662/YOLO-Fish
📄 Paper: *YOLO-Fish: A robust fish detection model to detect fish in realistic underwater environment* (Ecological Informatics, 2022)
Pretrained weights for DeepFish, OzFish, and a merged dataset. A published, citable fish detector. 🟡 (Darknet-based — older framework.)

### 🟡 Underwater image enhancement (the visual wow-factor)

**FUnIE-GAN** — https://github.com/xahidbuffon/FUnIE-GAN
*Fast Underwater Image Enhancement for Improved Visual Perception* (RA-L 2020). TensorFlow **and** PyTorch implementations. Designed for real-time use on robots — "fast" is in the name, which matters for a live demo. 🟡

**Awesome Underwater Image Enhancement** — https://github.com/lizhh268/awesome_underwater_image_enhancement-UIE-
Continuously updated index of UIE datasets, papers, and code. Start here rather than searching. 🟢 (to browse)

**RAUNE-Net** — https://github.com/fansuregrin/RAUNE-Net · 📄 https://arxiv.org/pdf/2311.00246
Residual + attention underwater enhancement. 🔴

**Deep-WaveNet** — https://github.com/pksvision/Deep-WaveNet-Underwater-Image-Restoration
Wavelength-aware restoration — explicitly models the fact that red light dies first underwater. Conceptually elegant; good to *cite* even if you don't run it. 🔴

> ⚠️ **Important nuance most teams get wrong:** enhancing an image so it looks prettier to *humans* does **not** reliably improve *detector* accuracy. The research is genuinely mixed on this. Use enhancement as a **visualization layer** (judges love the before/after slider) and as an **augmentation strategy**, but always report your detection numbers on raw images too. Saying this out loud demonstrates real understanding and costs you nothing.

### 🔴 Advanced / for citation

**DG-YOLO** — https://github.com/mousecpn/DG-YOLO — *Towards Domain Generalization in Underwater Object Detection* (ICIP 2020). Directly addresses "model trained in one water condition fails in another" — i.e. your core scientific problem. Cite it. 🔴

**YSOOB** — *You Sense Only Once Beneath: Ultra-Light Real-Time Underwater Object Detection* — 📄 https://arxiv.org/html/2504.15694v1
**1.2M parameters**, mAP50 of **83.1% / 82.9%** on URPC2020 / DUO, **57.8 FPS on Jetson Xavier NX** with TensorRT FP16. The reference point for the "ultra-light edge deployment" angle. 🔴

**Key surveys to cite (read the abstracts, not the papers):**
- *Underwater Optical Object Detection in the Era of Artificial Intelligence: Current, Challenge, and Future* — ACM Computing Surveys — https://dl.acm.org/doi/10.1145/3759243
- *A Structured Review of Underwater Object Detection Challenges and Solutions: From Traditional to Large Vision Language Models* — https://arxiv.org/pdf/2509.08490
- *Improve Underwater Object Detection through YOLOv12 Architecture and Physics-informed Augmentation* — https://arxiv.org/pdf/2506.23505 ← **directly supports Innovation Angle #1 in Part 4.**

---

# Part 2 — The Research Brief: Underwater AI Vision from Zero

*This part assumes you know nothing about neural networks. Read it in order. ~25 minutes.*

## 2.1 What a computer actually sees

A digital image is a **grid of numbers**. A 640×640 colour photo is 640 × 640 × 3 = 1,228,800 numbers, each from 0–255, in three channels: **R**ed, **G**reen, **B**lue.

That's it. There are no "fish" in the file. There is no "water." There is a grid of brightness values. Every task in computer vision is the same task: **find a mathematical function that turns that grid of numbers into an answer you care about.**

> **Key term — tensor:** a multi-dimensional array of numbers. An image is a tensor of shape (height, width, channels). Frameworks like PyTorch usually reorder this to (channels, height, width). When an error message says "expected shape (3, 640, 640) but got (640, 640, 3)", this is what it means — and it will happen to you.

## 2.2 Classification vs. Detection vs. Segmentation

Three different questions you can ask about an image:

| Task | Question | Output |
|---|---|---|
| **Classification** | "*What* is in this image?" | One label: `"fish"` |
| **Object Detection** | "*What* is in this image, and *where*, and *how many*?" | A list of boxes: `[fish, x=120, y=340, w=55, h=30, confidence=0.89]` |
| **Instance Segmentation** | "Which *exact pixels* belong to each object?" | A pixel mask per object |

**OceanEye is an object detection problem.** You need to know *how many* fish and *where* they are — a single label for the whole frame is useless for counting.

> **Key term — bounding box:** a rectangle described by 4 numbers. Usually either `(x_min, y_min, x_max, y_max)` — the corners — or `(x_center, y_center, width, height)`. YOLO uses the second form, **normalized** to 0–1 (divided by image width/height). This is why a YOLO label file looks like:
> ```
> 0 0.451 0.622 0.085 0.047
> ```
> which reads: *class 0, centred at 45.1% across and 62.2% down, 8.5% of the image wide and 4.7% tall.*

> **Key term — confidence:** a number from 0 to 1, how sure the model is. You pick a **threshold** (commonly 0.25–0.5). Below it, the detection is discarded. **Lowering the threshold finds more fish but produces more false alarms.** Tuning this is the single fastest way to change how your demo looks — know the number you're using and why.

## 2.3 Why CNNs work

A **neural network** is a long chain of simple mathematical operations (multiply, add, and a nonlinear squash) with millions of adjustable numbers called **weights**. **Training** = automatically nudging those weights until the outputs match the correct answers.

A **Convolutional Neural Network (CNN)** is a neural network specialized for images. Three ideas make it work, and they're all intuitive:

**1. Local patterns.** A small filter — say 3×3 pixels — slides across the whole image looking for one specific local pattern: a vertical edge, a colour transition, a spot of texture. This sliding operation is a **convolution**.

**2. Hierarchy.** Stack these layers. Early layers detect edges and colours. Middle layers combine edges into textures, fins, and eye-shapes. Deep layers combine those into "this is a fish." Nobody programs this hierarchy — it *emerges* from training.

**3. Weight sharing.** The same 3×3 filter is used at every position in the image. So a fish is recognized whether it's top-left or bottom-right, and the network needs far fewer weights than if every pixel had its own. This is called **translation invariance**, and it's why CNNs work on images while plain networks don't.

> **Key term — feature map:** the output of a convolutional layer — a grid showing "how strongly this pattern was found at each location."

## 2.4 Transfer learning — the most important idea in this brief

**Read this section twice. It is the reason your team can succeed in 8 days.**

Training a CNN from scratch requires millions of images and weeks of GPU time. You have neither.

**But you don't need to.** The early and middle layers of a CNN learn *general-purpose* visual machinery — edges, curves, textures, shapes. That machinery is the same whether you're looking at cars, cats, or catfish. Only the last layers are specific to particular objects.

So:

1. Download a model already trained on **COCO** (a general dataset of 330,000 images, 80 everyday object classes).
2. Keep all the learned visual machinery.
3. Replace the final layer to predict *your* classes (fish, crab, debris).
4. Train briefly on your small dataset to adapt.

This is **transfer learning** (or **fine-tuning**). It turns "millions of images and weeks of compute" into **"a few hundred images and twenty minutes."**

> **Analogy for your presentation:** it's like hiring a photographer who has spent 20 years shooting everything, and spending one afternoon teaching them to identify Cambodian fish species. You are not teaching them what a camera is. That is the 20 years you're getting for free.

When you write `YOLO("yolo26n.pt")`, the `.pt` file *is* those pretrained weights. That one line is transfer learning.

## 2.5 How object detectors work

**Two-stage detectors (e.g. Faster R-CNN)** work in two passes: a *Region Proposal Network* suggests ~2,000 regions that might contain something, then a classifier examines each one. **Accurate but slow.** Historically the accuracy champion.

**One-stage detectors (YOLO = "You Only Look Once")** do it in a single pass: divide the image into a grid; every grid cell simultaneously predicts boxes, classes, and confidences. **Much faster**, and modern versions match two-stage accuracy.

**For OceanEye, use YOLO.** You need real-time video for a live demo, the ecosystem is vastly more beginner-friendly, and the accuracy gap has closed.

> **Key term — NMS (Non-Maximum Suppression):** detectors often fire several overlapping boxes on one fish. NMS keeps the highest-confidence box and deletes overlapping duplicates. **YOLO26 can skip NMS entirely** (its "one-to-one head"), making inference genuinely end-to-end and latency more predictable.

> **Key term — IoU (Intersection over Union):** overlap between two boxes = shared area ÷ combined area. 1.0 = perfect, 0 = no overlap. Used both by NMS and by evaluation.

> **Key term — mAP (mean Average Precision):** the standard accuracy score, 0–1. **mAP50** counts a detection as correct if IoU ≥ 0.5 (lenient). **mAP50-95** averages across thresholds 0.5→0.95 (strict). When a paper says "83.1% mAP50 on DUO," that's this. For your demo, mAP50 is the number to quote.

> **Key term — FPN (Feature Pyramid Network):** small objects vanish in deep layers because the feature maps get spatially coarse. An FPN merges high-resolution early features with semantically-rich deep features, so the detector can see both a whale and a shrimp. **This is the main architectural reason modern detectors handle small underwater objects at all** — and it is directly relevant to your Task Difficulty score.

## 2.6 Why underwater is genuinely hard (your Task Difficulty argument)

This is your differentiator. Understand it properly; it's the most technically credible thing you can say.

### 2.6.1 Light absorption — water eats colour, by wavelength

Water absorbs light **selectively by wavelength**, and long wavelengths die first:

| Colour | Roughly gone by |
|---|---|
| 🔴 Red | ~5 m |
| 🟠 Orange | ~10 m |
| 🟡 Yellow | ~20 m |
| 🟢 Green | ~30 m |
| 🔵 Blue | penetrates deepest |

**Consequence:** every underwater image has a **blue-green colour cast**, and the red channel is nearly empty — it carries mostly noise. A model trained on normal land photos has learned colour relationships that simply do not hold underwater. This is a **domain shift**, and it's why a COCO-pretrained model performs poorly on raw underwater images until you fine-tune it.

### 2.6.2 Scattering — water adds fog

Suspended particles bounce light in all directions:
- **Forward scattering** blurs edges — objects lose sharpness with distance.
- **Backscattering** bounces your own light source straight back into the lens, producing a **veiling haze** that destroys contrast. If you've seen dive footage full of glowing white specks — "marine snow" — that's backscatter.

**Consequence:** low contrast, washed-out images, and a **fog that gets worse with distance**. Distant = faint = hard.

### 2.6.3 Turbidity — the Tonle Sap problem

Turbidity is suspended sediment. The Tonle Sap's flood pulse carries enormous sediment loads, so visibility can drop to well under a metre. **This is the headline challenge for a Cambodian deployment, and it's exactly what the Brackish dataset (§1.1) was built to represent.** Make this connection explicitly in your presentation — it shows you chose your data for a reason.

### 2.6.4 The rest of the list

- **Refraction** — light bends passing through water → glass port → air, magnifying objects by roughly 1.33× and introducing geometric distortion. **This matters enormously if you attempt size estimation** (see Innovation Angle #3).
- **Non-uniform artificial lighting** — below a certain depth you supply your own light, creating a bright hotspot in the centre and dark vignetted corners. The same fish looks different depending on where it sits in the frame.
- **Small, dense, occluded targets** — fish school; sea urchins carpet the seabed. Dozens of small overlapping objects per frame.
- **Camouflage** — flounder, sea cucumbers, and bottom-dwellers evolved *specifically* to defeat visual detection. You are fighting natural selection.
- **Caustics** — rippling light patterns in shallow water create moving high-contrast shapes that generate false positives.
- **Motion blur** — the camera, the platform, and the fish are all moving, often in current.
- **Noisy labels and class imbalance** — even the benchmark datasets have annotation errors (this is precisely why DUO exists), and you'll have 10,000 "fish" and 40 "turtle."

> **How to say this in your presentation, in one line:**
> *"Underwater vision fails for three physical reasons — wavelength-selective absorption removes colour, scattering removes contrast, and turbidity removes range. OceanEye addresses all three: physics-informed augmentation for absorption, enhancement preprocessing for contrast, and a small-target-aware detector for range."*

## 2.7 How modern detectors fight back

| Problem | Technique | In practice |
|---|---|---|
| Colour cast | White balance / colour restoration | Gray-World or CLAHE preprocessing (§2.8) |
| Low contrast | CLAHE, or a learned enhancer (FUnIE-GAN) | Boosts local contrast before detection |
| Small objects | **FPN multi-scale features**, higher `imgsz`, **STAL** in YOLO26 | Train at `imgsz=960` instead of 640 |
| Domain shift | **Transfer learning + heavy augmentation** | Fine-tune on underwater data; simulate turbidity |
| Overlapping boxes | NMS, or NMS-free one-to-one head | `nms=False` in YOLO26 |
| Scarce labelled data | Transfer learning, augmentation, synthetic data | Your entire strategy |
| Camouflage/occlusion | Attention mechanisms, edge/wavelet features | Research-grade — cite, don't build |
| Double-counting in video | **Multi-object tracking** (ByteTrack) | Track IDs → count unique fish, not frames |

## 2.8 Code: from zero to working detector

*Every block below is runnable. Type them yourself rather than copy-pasting — you'll learn faster and you'll be able to fix them live on 20 September.*

### Step 0 — Installation

```bash
# Create an isolated environment so you can't break your system Python
python3 -m venv oceaneye-env
source oceaneye-env/bin/activate        # Windows: oceaneye-env\Scripts\activate

# Install the essentials
pip install ultralytics opencv-python matplotlib

# Verify
python -c "from ultralytics import YOLO; print('OK')"
```

**What this does:** `venv` creates a private sandbox for your project's libraries. `ultralytics` pulls in PyTorch (the deep learning engine) automatically. `opencv-python` (imported as `cv2`) handles image and video I/O.

> ⚠️ **Do this today, not on 18 September.** Environment setup is where beginners lose days. Once it works, **write down the exact commands that worked** and put them in your repo.

### Step 1 — Your first detection (3 lines)

```python
from ultralytics import YOLO

model = YOLO("yolo26n.pt")          # downloads pretrained weights on first run
results = model("underwater.jpg")   # run inference
results[0].show()                   # display with boxes drawn
```

**Line by line:**
1. Import the YOLO class.
2. `YOLO("yolo26n.pt")` downloads (first time only) and loads a model pretrained on COCO. **`n` = nano**, the smallest and fastest — right for a CPU laptop. This is transfer learning in one line.
3. Calling the model on a path runs the full pipeline: load → resize → normalize → forward pass → NMS → boxes.
4. `.show()` opens a window with boxes drawn.

> **Expect this to underperform on raw underwater images.** COCO has no "sea urchin" class, and its colour statistics are from land photos. That gap *is* your project. Run it anyway — seeing the failure makes §2.6 concrete.

### Step 2 — Reading results properly

```python
from ultralytics import YOLO

model = YOLO("yolo26n.pt")
results = model("underwater.jpg", conf=0.25)   # confidence threshold

for box in results[0].boxes:
    class_id   = int(box.cls[0])                  # numeric class index
    class_name = model.names[class_id]            # human-readable name
    confidence = float(box.conf[0])               # 0.0 - 1.0
    x1, y1, x2, y2 = box.xyxy[0].tolist()         # corner coordinates in pixels

    print(f"{class_name:12s} {confidence:.2f}  "
          f"box=({x1:.0f},{y1:.0f})-({x2:.0f},{y2:.0f})")

print(f"\nTotal objects detected: {len(results[0].boxes)}")
```

**What's happening:** `results` is a list (one entry per image). `results[0].boxes` holds every surviving detection. Each box carries `.cls` (class index), `.conf` (confidence), and coordinates in several formats — `.xyxy` (corners), `.xywh` (centre+size), `.xywhn` (normalized). **That last line is your fish count** — the core output of OceanEye.

### Step 3 — Underwater preprocessing

Two classical techniques, no training required, that visibly improve murky images. **This is your before/after demo.**

```python
import cv2
import numpy as np

def gray_world_white_balance(img):
    """Remove the blue-green colour cast.

    Assumes the average colour of a natural scene should be gray.
    Underwater it isn't (red is absorbed), so we rescale each channel
    to force the averages to match. Cheap, fast, surprisingly effective.
    """
    result = img.astype(np.float32)
    avg_b, avg_g, avg_r = [result[:, :, i].mean() for i in range(3)]
    avg_gray = (avg_b + avg_g + avg_r) / 3.0

    for i, avg in enumerate((avg_b, avg_g, avg_r)):
        if avg > 0:                                  # avoid divide-by-zero
            result[:, :, i] *= (avg_gray / avg)

    return np.clip(result, 0, 255).astype(np.uint8)


def clahe_enhance(img, clip_limit=3.0, tile=(8, 8)):
    """Boost local contrast to cut through scattering haze.

    CLAHE = Contrast Limited Adaptive Histogram Equalization.
    'Adaptive' = works on small tiles, so dark corners get boosted
    independently of the bright centre (fixes non-uniform lighting).
    'Contrast Limited' = caps the boost so noise isn't amplified.

    We convert to LAB and touch only L (lightness), leaving A and B
    (colour) alone — so we add contrast without wrecking the colours.
    """
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile).apply(l)
    return cv2.cvtColor(cv2.merge((l, a, b)), cv2.COLOR_LAB2BGR)


def enhance_underwater(img):
    """Full pipeline: fix colour, then fix contrast. Order matters."""
    return clahe_enhance(gray_world_white_balance(img))


if __name__ == "__main__":
    img = cv2.imread("underwater.jpg")
    out = enhance_underwater(img)
    cv2.imwrite("enhanced.jpg", out)
    cv2.imshow("Before | After", np.hstack([img, out]))   # side by side
    cv2.waitKey(0)
    cv2.destroyAllWindows()
```

**Why this works:**
- **Gray-World** attacks §2.6.1 (absorption). Underwater, blue dominates and red is starved; rescaling channels to equal means restores something close to natural colour.
- **CLAHE** attacks §2.6.2 (scattering) *and* non-uniform lighting, because it operates per-tile.
- **Order matters:** colour first, then contrast. Reversed, you amplify the cast before correcting it.
- **The LAB trick** is the professional touch — operating on RGB directly shifts hues and produces garish results. Explain this in your presentation; it shows you understand colour spaces.

> **Demo tip:** `np.hstack` side-by-side is the single most persuasive visual you can show a non-technical judge. It takes two seconds to understand and looks like magic.

### Step 4 — Training on your own data

**Dataset layout** (Roboflow exports exactly this):

```
oceaneye_dataset/
├── data.yaml
├── train/
│   ├── images/     img001.jpg, img002.jpg, ...
│   └── labels/     img001.txt, img002.txt, ...   ← one .txt per image
├── valid/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

**`data.yaml`:**

```yaml
path: ./oceaneye_dataset
train: train/images
val: valid/images
test: test/images

names:
  0: fish
  1: crab
  2: starfish
  3: jellyfish
  4: debris
```

Each label `.txt` contains one line per object: `class_id x_center y_center width height`, all normalized 0–1 (§2.2).

**Training:**

```python
from ultralytics import YOLO

model = YOLO("yolo26n.pt")        # start from pretrained — NOT from scratch

results = model.train(
    data="oceaneye_dataset/data.yaml",
    epochs=100,          # full passes over the dataset
    imgsz=960,           # ↑ from default 640: helps small underwater objects
    batch=8,             # lower this if you hit "CUDA out of memory"
    patience=25,         # early-stop if no improvement for 25 epochs
    device=0,            # 0 = first GPU; "cpu" if you have none

    # --- Augmentation: our defence against domain shift ---
    hsv_h=0.015,         # hue jitter — simulates different water colours
    hsv_s=0.7,           # saturation jitter — simulates turbidity
    hsv_v=0.4,           # brightness jitter — simulates depth/lighting
    degrees=10,          # rotation — camera tilt
    scale=0.5,           # zoom — objects at varying distance
    fliplr=0.5,          # horizontal flip (50% of the time)
    mosaic=1.0,          # stitch 4 images together — great for small objects

    project="oceaneye",
    name="run1",
)
```

**What each part does:**
- **`YOLO("yolo26n.pt")` then `.train()`** — this is fine-tuning (§2.4). Starting from `yolo26n.yaml` instead would train from scratch and would fail with your data volume. **Do not do that.**
- **`epochs`** — one epoch = one pass over all training images. 100 is a reasonable start; `patience` stops early if it plateaus.
- **`imgsz=960`** — bigger input means small fish occupy more pixels and survive the downsampling. Costs memory and speed. **This is one of your highest-leverage knobs for underwater work.**
- **Augmentation** — randomly distorting training images so the model learns *fish*, not *fish in this exact lighting*. The HSV parameters simulate different water conditions, which is precisely the domain-shift defence from §2.6. **`mosaic` is especially valuable for small-object detection.**

**Where results land:** `oceaneye/run1/weights/best.pt` (best validation score) and `last.pt` (final epoch). **`best.pt` is your deliverable — back it up immediately, in three places.**

**No GPU?** Use **Google Colab** (free T4 GPU): upload the dataset, `!pip install ultralytics`, run the same code, download `best.pt`. A small dataset trains in 20–40 minutes.

### Step 5 — Evaluate

```python
from ultralytics import YOLO

model = YOLO("oceaneye/run1/weights/best.pt")
metrics = model.val(data="oceaneye_dataset/data.yaml")

print(f"mAP50    : {metrics.box.map50:.3f}")   # lenient  — quote this one
print(f"mAP50-95 : {metrics.box.map:.3f}")     # strict
print(f"Precision: {metrics.box.mp:.3f}")      # of detections, how many were right
print(f"Recall   : {metrics.box.mr:.3f}")      # of real objects, how many we found
```

**How to read these:**
- **Precision** — when the model says "fish," how often is it right? Low = false alarms.
- **Recall** — of all real fish, how many did we find? Low = misses.
- They trade off via the confidence threshold. **Lower threshold → higher recall, lower precision.**
- **mAP50 is the headline number for your slides.** For reference: published underwater models reach ~83% mAP50 on DUO. If you get 60–75% on your own data in a week, that is a genuinely respectable result — say so honestly rather than inflating it. Judges respect calibrated claims, and honesty is literally in the rubric (Professional Ethics, 4 pts).

### Step 6 — Live video with counting and FPS (your demo core)

```python
import cv2
import time
from ultralytics import YOLO
from preprocessing import enhance_underwater      # from Step 3

model  = YOLO("oceaneye/run1/weights/best.pt")
cap    = cv2.VideoCapture("demo_underwater.mp4")  # or 0 for a webcam
ENHANCE = True                                    # toggle live with 'e'

prev_t, fps = time.time(), 0.0

while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
        break

    proc = enhance_underwater(frame) if ENHANCE else frame

    results = model(proc, conf=0.35, verbose=False)
    annotated = results[0].plot()                 # draws boxes + labels

    # --- smoothed FPS (judges ask "is it real-time?") ---
    now = time.time()
    fps = 0.9 * fps + 0.1 * (1.0 / max(now - prev_t, 1e-6))
    prev_t = now

    count = len(results[0].boxes)
    cv2.putText(annotated, f"Objects: {count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 255, 0), 2)
    cv2.putText(annotated, f"FPS: {fps:.1f}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 255, 255), 2)
    cv2.putText(annotated, f"Enhance: {'ON' if ENHANCE else 'OFF'}", (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 200, 0), 2)

    cv2.imshow("OceanEye - Group 22", annotated)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('e'):
        ENHANCE = not ENHANCE                     # live A/B toggle

cap.release()
cv2.destroyAllWindows()
```

**Why this is built the way it is:**
- **The `e` key toggle is your best demo move.** Flip enhancement on and off live and let the judges watch the detection count change. It's interactive, it proves the system is really running (not a video), and it demonstrates the contribution of your preprocessing in two seconds. Practice this until it's smooth.
- **The FPS counter** is direct evidence for *real-time* claims, and it's smoothed (exponential moving average) so it doesn't flicker distractingly.
- **`verbose=False`** suppresses per-frame console spam. That's *Craftsmanship* (3 pts) — a clean terminal reads as professional.

### Step 7 — Tracking: count unique fish, not frames

Naive counting double-counts the same fish across frames. **Tracking assigns each fish a persistent ID.**

```python
from ultralytics import YOLO

model = YOLO("oceaneye/run1/weights/best.pt")
seen_ids = set()

for result in model.track(source="demo_underwater.mp4", tracker="bytetrack.yaml",
                          persist=True, stream=True, conf=0.35):
    if result.boxes.id is not None:
        seen_ids.update(result.boxes.id.int().tolist())

print(f"Unique individuals observed: {len(seen_ids)}")
```

**Why this matters more than it looks:** "we detected 340 fish" is meaningless if it's one fish seen 340 times. "We counted **17 unique individuals**" is a real biological measurement — the kind a fisheries officer could actually use. `persist=True` carries IDs across frames; `stream=True` processes frame-by-frame instead of loading the whole video into RAM. **This single upgrade moves you from "demo" to "instrument."**

### Step 8 — Export for speed (optional, do last)

```python
from ultralytics import YOLO

model = YOLO("oceaneye/run1/weights/best.pt")
model.export(format="onnx")      # portable, fast on CPU — your safest option
# model.export(format="engine")  # TensorRT — NVIDIA GPU only, fastest
```

**ONNX** is a universal model format that runs without PyTorch and is notably faster on CPU. For a laptop demo with no GPU, exporting to ONNX is the cheapest speed win available. YOLO26 reports up to **43% faster CPU ONNX inference** vs YOLO11n.

> **Do this only once everything else works.** Export is a classic source of last-minute breakage.

---

# Part 3 — Rapid Upskilling: Your 8-Day Plan

## 3.1 Day-by-day  ⛔ SUPERSEDED

> **This schedule is out of date.** Use **`OceanEye_5Day_Roadmap.docx`** instead — it runs 12–16 September with a 17–18 September rehearsal buffer, includes the robot/procurement workstream, and has daily tracking boxes. The table below is kept only to show the reasoning behind the sequencing.

### (superseded) original 8-day table

| Day | Date | Focus | Concrete deliverable |
|---|---|---|---|
| **0** | **Thu 11** | **Advisor call 14:00 PP.** Ask the §0.5 questions. Install everything (Step 0). | Working `ultralytics` install on all 3 laptops |
| **1** | Fri 12 | Ultralytics Academy basics. Run Steps 1–2 on any underwater photo. | First detection on screen |
| **2** | Sat 13 | Download Aquarium + Brackish. Train on Aquarium in Colab (Step 4). | Your first `best.pt` |
| **3** | Sun 14 | Train on Brackish (the real one). Build preprocessing (Step 3). | Before/after enhancement images |
| **4** | Mon 15 | Video pipeline (Step 6) + tracking (Step 7). Choose your innovation angle (Part 4). | Live video demo running |
| **5** | Tue 16 | **Freeze features.** Record backup demo video. Build slides. | Frozen `best.pt` + backup video + slide deck |
| **6** | Wed 17 | **Full dress rehearsal ×3, timed to 20 minutes.** Fix only what breaks. | Timed, working run |
| **7** | Thu 18 | Rehearse ×3 more. Pack equipment. Test on venue-like conditions. | Packed bag, printed runbook |
| **8** | **Fri 19** | **Competition begins.** | — |

> **The hard rule: feature freeze on Day 5 (Tue 16).** After that, you fix bugs and rehearse. Nothing new. Teams lose competitions by adding a feature the night before. The rubric pays 25 points for standardization + proficiency — that is *rehearsal money*, and it's the highest-return use of Days 6–7.

## 3.2 Tutorials and courses (prioritized)

### 🟢 Do these first — highest value per hour

1. **Ultralytics Academy** — https://academy.ultralytics.com/
   Free, official, hands-on, with a certificate. Built by the people who make YOLO. **Start here on Day 1.** The certificate is also a nice artifact to mention.
2. **Ultralytics Docs — Quickstart & Python Usage** — https://docs.ultralytics.com/
   Your daily reference. Bookmark the Predict, Train, and Track pages specifically.
3. **YOLO26 model page** — https://docs.ultralytics.com/models/yolo26/
   Read this before your presentation. It's the source of your Technological Advancement talking points.
4. **Roboflow Learn / Blog** — https://blog.roboflow.com/
   Practical, beginner-oriented, "working model in a day" articles. Excellent for dataset preparation.

### 🟡 Read if you have spare time

5. **OpenCV-Python Tutorials** — https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
   Official. Focus only on: reading/writing images, colour spaces, histogram equalization. Ignore the rest for now.
6. **PyTorch 60-Minute Blitz** — https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html
   Useful for understanding what's under the hood. **Not required** to succeed — Ultralytics hides PyTorch from you.
7. **LearnOpenCV — YOLO26 real-time deployment** — https://learnopencv.com/yolov26-real-time-deployment/
   Practical deployment walkthrough for the exact model you're using.

### 🔴 For context only — do not attempt this week

8. **Stanford CS231n** — https://cs231n.github.io/
   The gold-standard CNN course. Genuinely excellent and genuinely demanding. **Bookmark it for after the competition.** Attempting it now will consume your week and produce no demo.

## 3.3 Papers worth knowing (read abstracts + figures only)

| Paper | Why | Link |
|---|---|---|
| *Underwater Optical Object Detection in the Era of AI* (ACM Computing Surveys) | The definitive survey. One citation covers the whole field. | https://dl.acm.org/doi/10.1145/3759243 |
| *A Structured Review of Underwater Object Detection Challenges and Solutions* | Organizes challenges into image degradation, noisy labels, small objects, class imbalance — a ready-made structure for your problem slide. | https://arxiv.org/pdf/2509.08490 |
| *A Dataset and Benchmark of Underwater Object Detection for Robot Picking* (DUO) | Your benchmark dataset citation. | https://arxiv.org/abs/2106.05681 |
| *Improve Underwater Object Detection through YOLOv12 and Physics-informed Augmentation* | Direct evidence for Innovation Angle #1. | https://arxiv.org/pdf/2506.23505 |
| *You Sense Only Once Beneath* (YSOOB) | 1.2M params, 57.8 FPS on Jetson — the edge-deployment benchmark. | https://arxiv.org/html/2504.15694v1 |
| *FathomNet* (Scientific Reports) | Source of the "81% reduction in human effort" statistic. | https://www.nature.com/articles/s41598-022-19939-2 |
| *Ultralytics YOLO Evolution: YOLO26, YOLO11, YOLOv8, YOLOv5* | Justifies your model choice with a citation. | https://arxiv.org/abs/2510.09653 |

> **How to read a paper in 5 minutes:** Title → Abstract → every Figure and its caption → Table 1 → Conclusion. Skip the maths. You need the *claim* and the *number*, not the derivation.

## 3.4 Tools to install (in this order)

| Tool | Purpose | Install | Priority |
|---|---|---|---|
| **Python 3.10+** | Everything | python.org or your distro | 🔴 Essential |
| **PyTorch** | The deep learning engine | auto-installed by ultralytics | 🔴 Essential |
| **Ultralytics** | YOLO train + inference | `pip install ultralytics` | 🔴 Essential |
| **OpenCV** | Image/video I/O, preprocessing | `pip install opencv-python` | 🔴 Essential |
| **Google Colab** | Free GPU for training | https://colab.research.google.com | 🔴 Essential (no local GPU) |
| **Roboflow** | Dataset hosting, annotation, format conversion | https://roboflow.com (free tier) | 🟠 Strongly recommended |
| **Git + GitHub** | Version control, and evidence of professional practice | `apt install git` | 🟠 Recommended |
| **LabelImg / CVAT** | Annotating your *own* images | `pip install labelImg` | 🟡 Only if collecting own data |
| **Gradio / Streamlit** | A clickable web UI for the demo | `pip install gradio` | 🟡 Nice-to-have |

> **On Gradio:** a simple web interface looks considerably more polished than a terminal window and costs about 30 lines. It runs locally with no internet. **Consider it on Day 4 if — and only if — your core pipeline already works.**

## 3.5 Pretrained models and where to get weights

- **Ultralytics YOLO26 checkpoints** — auto-download on first use: `yolo26n/s/m/l/x.pt` plus `-seg`, `-sem`, `-depth`, `-cls`, `-pose`, `-obb` variants. ⚠️ **Download these on Day 1 while you have internet.** They cache in `~/.cache/` — confirm the demo works with the network disabled.
- **Roboflow Universe** — https://universe.roboflow.com — thousands of community datasets, many with *already-trained* models you can test instantly. Search "underwater," "aquarium," "fish."
- **FathomNet Model Zoo** — marine-specific pretrained models via the FathomNet API.
- **YOLO-Fish weights** — https://github.com/tamim662/YOLO-Fish — pretrained on DeepFish/OzFish.
- **Hugging Face Hub** — https://huggingface.co/models?pipeline_tag=object-detection — search "underwater" / "fish."

> 🔴 **Offline checklist, non-negotiable:** by Day 6 you must verify the *entire* demo runs with **Wi-Fi switched off**. Anything that silently downloads on first run will fail at the venue. Test it, then test it again on a different laptop.

---

# Part 4 — Innovation Opportunities: Competition-Winning Angles

*Worth 10 points directly (Innovation & Creativity), plus a large share of Technological Advancement (15) and Task Difficulty (15). Pick **one** as primary. Mention the others as "future work" — that's free credit for vision.*

---

## 🥇 Angle 1 — Physics-Informed Synthetic Turbidity ("Train for the Tonle Sap without diving into it")

**The problem it solves:** There is no labelled dataset of Cambodian freshwater fish in Tonle Sap turbidity. You cannot create one in 8 days. Without it, any model you train is a foreign model applied to local water.

**The insight:** You don't need turbid *photos*. You need to **simulate turbidity on clear photos you already have** — using the physics from §2.6, not random noise.

The underwater image formation model says an observed image is roughly:

```
I(x) = J(x)·t(x) + B·(1 − t(x))
```

where `J` is the clear scene, `t = exp(−β·d)` is transmission (β = attenuation coefficient, **wavelength-dependent**, d = distance), and `B` is the background veiling light. Higher β = murkier water.

```python
import numpy as np

def simulate_turbidity(img, beta=(0.25, 0.4, 0.9), depth=1.0, veil=(150, 140, 90)):
    """Apply the underwater image formation model to a clear image.

    beta : per-channel attenuation in BGR order (OpenCV convention).
           Red is absorbed FASTEST underwater, so beta_R (index 2) must be
           the LARGEST and beta_B (index 0) the smallest. Reversing this
           order produces physically backwards images -- an easy mistake.
    depth: scene distance proxy. Larger -> murkier. depth=0 is a no-op.
    veil : background scattered light in BGR -- the blue-green "fog".
           Tune beta and veil until your synthetic frames visually match
           real frames from the Brackish dataset.
    """
    out = img.astype(np.float32)
    for c in range(3):
        t = np.exp(-beta[c] * depth)                     # transmission
        out[:, :, c] = out[:, :, c] * t + veil[c] * (1 - t)
    return np.clip(out, 0, 255).astype(np.uint8)
```

**Your method (executable in 2 days):**
1. Take a clear-water dataset (Aquarium, or photos of local fish from a market/pond).
2. Generate 3–5 turbidity levels per image with `depth` sampled randomly.
3. Train on the augmented set.
4. **Evaluate on real turbid images (Brackish test split)** and compare against a baseline trained without the augmentation.

**Why it wins:**
- ✅ Produces a **real number**: "physics-informed augmentation improved mAP50 on turbid test data from X to Y." Judges love a measured improvement.
- ✅ It is **grounded in physics**, not a trick — you can explain the equation, and it maps directly to §2.6.1.
- ✅ **Directly solves a Cambodian problem** with no Cambodian data. That is a genuinely clever answer to a genuinely hard constraint.
- ✅ Backed by 2026 literature (*Physics-informed Augmentation*, arXiv 2506.23505) — you're extending published work, not inventing something unverifiable.
- ✅ Costs **zero** extra data collection. Highest value-to-effort ratio on this list.

**Demo moment:** show the same model, side by side, with and without the augmentation, running on murky footage. The difference will be visible.

**Risk:** 🟢 Low. Worst case, the improvement is small — and reporting a small honest improvement still scores well.

---

## 🥈 Angle 2 — Detection + Monocular Depth Fusion for Fish Size and Biomass Estimation

**The problem it solves:** Counting fish is useful. **Measuring** them is what fisheries science actually needs — size distribution reveals whether a stock is healthy or being fished down to juveniles. Recall the Mekong data: declines hit **the largest species hardest**. Size is the signal that matters.

**The insight — and this is the part almost nobody will notice:** **YOLO26 ships a monocular depth estimation variant (`yolo26n-depth.pt`)** in the same unified API as detection. One framework, one install, two modalities.

```python
from ultralytics import YOLO
import numpy as np

detector = YOLO("oceaneye/run1/weights/best.pt")   # your fine-tuned detector
depther  = YOLO("yolo26n-depth.pt")                # monocular depth

REFRACTION = 1.33          # water->glass->air magnification (see 2.6.4)
FOCAL_PX   = 800.0         # from camera calibration; measure yours

det = detector("frame.jpg")[0]
dep = depther("frame.jpg")[0]
depth_map = dep.depth if hasattr(dep, "depth") else None   # verify attribute name

for box in det.boxes:
    x1, y1, x2, y2 = box.xyxy[0].tolist()
    box_px = x2 - x1

    if depth_map is not None:
        region = depth_map[int(y1):int(y2), int(x1):int(x2)]
        d = float(np.median(region))           # median resists outliers
        # pinhole model, corrected for refraction
        length_m = (box_px * d) / (FOCAL_PX * REFRACTION)
        print(f"Fish at {d:.2f} m -> estimated length {length_m*100:.1f} cm")
```

> ⚠️ **Verify the depth-output attribute name against the current Ultralytics docs before relying on this** — the depth task is new in YOLO26 and the API surface may differ. Budget an hour for this. If it doesn't cooperate, fall back to Angle 1.

**Why it wins:**
- ✅ **Nobody else will do this.** Detection is table stakes; detection + depth is a system.
- ✅ It converts a demo into an **instrument** — "17 fish, mean length 12.4 cm, size distribution shown here" is a *scientific measurement*.
- ✅ Ties straight to Application Value: aquaculture biomass estimation, harvest timing, stock assessment.
- ✅ **The refraction correction is a killer detail.** Mentioning that you corrected for the 1.33× underwater magnification proves domain understanding no other team will demonstrate.

**Risk:** 🟠 Medium. Monocular depth is **relative**, not metric, without calibration. **Handle this honestly:** calibrate with a known-size object in frame (a 10 cm ruler or a printed checkerboard) and state clearly that it's a calibrated relative estimate. Honest framing scores under Professional Ethics; overclaiming can lose you those points if a judge probes.

---

## 🥉 Angle 3 — Ultra-Light Edge Deployment: "Real AI on $50 Hardware"

**The problem it solves:** Cambodian fish farmers and Tonle Sap fisheries officers will never own a workstation GPU. A solution that needs one is not a solution for them.

**The insight:** The rubric explicitly rewards **Cost-Effectiveness (3 pts)** and **Sustainability (3 pts)**. A model that runs on a cheap, low-power board is not a compromise — **it is the product.**

**Your method:**
1. Train `yolo26n` (nano — 1.7 ms on a T4).
2. Export to **ONNX** (§2.8 Step 8) — up to 43% faster on CPU.
3. Benchmark honestly on the hardware you actually have: laptop CPU, and a Raspberry Pi or Jetson Nano if you can borrow one.
4. Report a table: **FPS · model size (MB) · power draw (W) · hardware cost (USD)**.
5. Benchmark against YSOOB's published figures (1.2M params, 57.8 FPS on Jetson Xavier NX) to show you know the state of the art.

**Why it wins:**
- ✅ **Cost-effectiveness and sustainability are 6 rubric points that most teams completely ignore.**
- ✅ A power-draw figure in watts is an unusual, memorable, and verifiable slide.
- ✅ Makes the deployment story concrete: solar-powered monitoring buoys on the Tonle Sap.
- ✅ **Perfectly aligned with your 20-minute constraint** — a light model is a reliable demo.

**Risk:** 🟢 Low. Even with no edge hardware, benchmarking on your own laptop CPU and reporting it honestly is a complete, valid version of this angle.

---

## 🎁 Bonus angles (mention as "future work" — free vision credit)

- ⛔ **Multi-object tracking for non-double-counted census** (§2.8 Step 7) — **no longer an innovation angle.** Your advisor's reference system already displays per-object track IDs and a live "Total Counts" panel, so this is the expected baseline. **Build it anyway** (§2.8 Step 7 is still the right code), but present it as *implementation*, not novelty. Your differentiator must come from Angle #1 or #3 above.
- **Active learning / human-in-the-loop labelling** — model auto-labels, human corrects only the uncertain cases. Cite FathomNet's **81% effort reduction**. Strong story, no code required to *pitch* it.
- **Debris + species in one model** — one extra class from TrashCan turns OceanEye into an environmental monitor. Direct Sustainability points.
- **Night / low-light detection with artificial illumination** — genuinely under-explored, and fish behave differently at night. Honest and interesting as future work.
- **Sonar + optical fusion** — when water is too turbid for any camera, sonar still works. Cite the forward-looking sonar edge framework (*Sensors* 26:3133). Pure future work — do not attempt in 8 days.

## 4.1 What NOT to do (this list may be the most valuable page here)

| ❌ Don't | ✅ Instead | Why |
|---|---|---|
| Train from scratch | Fine-tune from `.pt` weights | You don't have the data or the time (§2.4) |
| Build a custom architecture | Use YOLO26 as shipped | Weeks of work, near-certain worse results |
| Depend on venue internet | Everything offline, weights pre-cached | Assume no Wi-Fi. Test with it disabled. |
| Train at the competition | Freeze `best.pt` on Day 5 | 20 minutes is inference time only |
| Chase the last 2% of mAP | Rehearse the demo | 25 rubric points are rehearsal; 0 are mAP |
| Add features after Day 5 | Feature freeze, then fix bugs only | The classic way teams lose |
| Read CS231n this week | Ultralytics Academy | Wrong tool for an 8-day timeline |
| Overclaim results | State honest numbers | Professional Ethics = 4 pts; judges probe |
| Use only clear-water data | Include Brackish | Your whole story is turbid water |
| Keep one copy of your weights | 3 copies: laptop, 2 USB sticks | Hardware fails on competition day |

---

# Part 5 — Competition Execution Plan

## 5.1 Suggested 20-minute operation runbook

Design your operation as a fixed, rehearsed sequence. **Write it on paper and follow it every single time** — that is literally what "Operational Standardization" (10 pts) measures.

| Time | Action | Who | Rubric hit |
|---|---|---|---|
| 0:00–1:30 | Setup: laptop on, camera/video connected, safety check stated aloud | Member A | Standardization, **Safety (3)** |
| 1:30–3:00 | Show the problem: raw murky footage, COCO model failing on it | Member B | **Task Difficulty (15)** |
| 3:00–6:00 | Enable enhancement — live `e` toggle, before/after | Member A | Skill Proficiency |
| 6:00–11:00 | Run OceanEye detection on live video: boxes, counts, FPS | Member A | **Skill Proficiency (15)** |
| 11:00–14:00 | Tracking: unique-individual count, not frame count | Member C | **Innovation (10)** |
| 14:00–17:00 | Your innovation angle (Part 4) with measured results | Member B | **Innovation + Tech Advancement (25)** |
| 17:00–19:00 | Application: Tonle Sap deployment, cost, power, sustainability | Member C | **Application Value (10)** |
| 19:00–20:00 | Attribution & licences slide; close | All three | **Ethics/IP (4)** |
| then | On-site presentation & Q&A | All three | **Presentation (5)** |

**Notes:**
- **All three members must speak and must visibly hand off to each other.** Teamwork is 10 points scored by observation — make the collaboration *visible*, not just real.
- Rehearse the transitions specifically. Fumbled hand-offs read as poor collaboration even when the work was shared perfectly.

## 5.2 Risk register — prepare these before you leave for the venue

| Risk | Probability | Mitigation |
|---|---|---|
| No internet at venue | **High** | All weights pre-cached; test with Wi-Fi off |
| Laptop GPU/driver failure | Medium | ONNX CPU fallback, pre-tested |
| Live camera fails | Medium | Pre-recorded video file as source; one keystroke to switch |
| Model crashes mid-demo | Low–Medium | **Backup screen-recording of a perfect run** on the desktop |
| Time overrun | **High** | Rehearse with a visible timer; cut §14:00–17:00 first if behind |
| Power/battery | Medium | Full charge + charger + local plug adapter |
| File corruption | Low | `best.pt` + full code on 2 USB sticks **and** a cloud copy |
| Nerves / language | **High** | Script your lines. Rehearse aloud, in English, six times. |

## 5.3 Your IP & attribution slide (draft it now — 4 easy points)

> **Datasets used:** Aquarium (Roboflow, CC BY 4.0) · Brackish Underwater, Pedersen et al., CVPR Workshops 2019 (CC BY 4.0) · DUO, Liu et al., 2021 · TrashCan 1.0, Hong et al., 2020
> **Models & frameworks:** Ultralytics YOLO26 (**AGPL-3.0**) · PyTorch (BSD) · OpenCV (Apache 2.0)
> **Our contribution:** physics-informed turbidity augmentation, underwater preprocessing pipeline, tracking-based unique-individual counting, edge benchmarking. Released under AGPL-3.0 in compliance with the Ultralytics licence.

Naming the AGPL obligation *unprompted* is exactly the professional conduct the rubric asks for, and it takes one slide.

---

## Appendix A — Glossary

| Term | Plain meaning |
|---|---|
| **Augmentation** | Randomly distorting training images so the model generalizes |
| **Backscatter** | Your light bouncing off particles into the lens — underwater haze |
| **CLAHE** | Contrast-boosting algorithm that works tile-by-tile |
| **CNN** | Neural network specialized for images |
| **COCO** | 330k-image, 80-class general dataset most models are pretrained on |
| **Confidence** | 0–1 score of how sure the model is |
| **Domain shift** | Test data differs from training data; accuracy collapses |
| **Epoch** | One full pass over the training set |
| **Fine-tuning** | Adapting a pretrained model to your data — see transfer learning |
| **FPN** | Feature Pyramid Network — merges scales so small objects survive |
| **FPS** | Frames per second — your real-time metric |
| **Inference** | Running a trained model to get predictions |
| **IoU** | Box overlap: shared area ÷ combined area |
| **mAP50** | Accuracy score counting IoU ≥ 0.5 as correct |
| **NMS** | Removes duplicate overlapping boxes. YOLO26 can skip it. |
| **ONNX** | Portable model format; fast on CPU |
| **Precision** | Of detections made, the fraction that were correct |
| **Recall** | Of real objects present, the fraction found |
| **STAL** | YOLO26's small-target-aware label assignment |
| **Tensor** | Multi-dimensional array of numbers |
| **Transfer learning** | Reusing a pretrained model's learned features |
| **Turbidity** | Cloudiness from suspended particles |
| **Weights** | The learned numbers inside a network; the `.pt` file |

## Appendix B — One-page quick reference

```bash
# Setup (once)
python3 -m venv oceaneye-env && source oceaneye-env/bin/activate
pip install ultralytics opencv-python

# Predict on an image
yolo predict model=yolo26n.pt source=underwater.jpg conf=0.25

# Train on your dataset
yolo train model=yolo26n.pt data=data.yaml epochs=100 imgsz=960 batch=8

# Validate
yolo val model=runs/detect/train/weights/best.pt data=data.yaml

# Track in video
yolo track model=best.pt source=demo.mp4 tracker=bytetrack.yaml

# Export for CPU speed
yolo export model=best.pt format=onnx
```

```python
# The five lines that matter
from ultralytics import YOLO
model   = YOLO("yolo26n.pt")                      # transfer learning
model.train(data="data.yaml", epochs=100, imgsz=960)
best    = YOLO("runs/detect/train/weights/best.pt")
results = best("underwater.jpg", conf=0.35)
print(f"Detected {len(results[0].boxes)} objects")
```

---

## Final word

You are not being asked to advance the state of the art. You are being asked to demonstrate, in 20 minutes, that three students from RUPP can take a real Cambodian problem — turbid water, declining fish stocks, no budget — and build a working AI system that addresses it.

That is completely achievable in 8 days, because of §2.4: **you are standing on a model that has already been trained on millions of images.** Your job is to point it at the right problem, adapt it to the right water, and run it flawlessly on the day.

The physics of water is your moat. No other team in your track has to fight light absorption, scattering, and turbidity. Make that difficulty visible, show you understood it, and show that you solved it anyway.

**Good luck. សូមសំណាងល្អ។**

---

*Compiled 11 September 2026 for Group 22, Royal University of Phnom Penh. Sources are hyperlinked inline throughout; all technical claims are traceable to the linked papers, datasets, and documentation.*
