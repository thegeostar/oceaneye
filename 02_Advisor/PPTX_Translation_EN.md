# Prof. Wang's PowerPoint — full English translation

> **← Back to [START_HERE.md](../START_HERE.md)**
>
> **Owner:** S3 · **Open it when:** you need to know what her slides actually say, or you are writing the attribution slide.
>
> **TL;DR**
> - 13 slides. Chinese file: `GX_2024_0017_基于深度学习的水下图像清晰化与目标检测方法研究_李凯旋.pptx`
> - It is **not our competition deck.** It is a Chinese university research-project report by **her student Li Kaixuan**, which she forwarded as the technical background.
> - It answers the model question for good: the system is **Mamba-YOLO**, not YOLOv5 and not plain YOLOv8. See slide 5 and 7.
> - It gives us the **patent and copyright numbers** — those go on the attribution slide, worth 4 points.
> - Slide numbers below match the slide numbers in PowerPoint exactly. Open both side by side.

**Translation notes:** Chinese technical papers write *本发明* ("the present invention") because the text was reused from the patent application. I have kept that phrasing where it appears so you can match it to the Chinese. Where a term has a standard English name in the code, I give both.

---

## Title of the whole deck

**"Research on Deep-Learning-Based Underwater Image Enhancement and Object Detection Methods"**

*(File-name prefix `GX_2024_0017` is her university's internal project number. `李凯旋` = Li Kaixuan, the student author.)*

---

## Slide 1 — Title

> **Research on Deep-Learning-Based Underwater Image Enhancement and Object Detection Methods**
>
> Team members: Li Kaixuan, Chen Shuzhuo, Zhou Qiaoyu, Wang Bo, Zhu Jiajia
> Supervisors: **Wang Li**, Zhou Ying

*On screen: university logo and a photo background.*

⚠️ **These are not our names.** This is her research group in China. Our team is Dararoth, Yuleang, Sophearoth. Do not present this slide as ours.

---

## Slide 2 — Contents

> **01** Project Introduction
> **02** Main Work
> **03** Results Achieved

---

## Slide 3 — Section divider

> **01 — Project Introduction**

---

## Slide 4 — Why underwater detection is hard

> ### 01 Project Introduction
>
> **How the underwater environment affects object detection**
> The underwater environment is complex. Light is refracted, scattered and attenuated, so images have low contrast, are blurred, and carry significant noise. Suspended particles and underwater micro-organisms add further noise interference, making it hard for traditional detection algorithms to pick out image detail. Across different depths and environments the appearance and colour of a target vary considerably, which increases the difficulty further.
>
> **Shortcomings of existing methods**
> - **Low accuracy:** existing algorithms struggle to identify targets correctly in low-contrast underwater images.
> - **Insensitive to tiny targets:** small targets underwater are usually missed because they resemble the background.
> - **Weak adaptation to moving targets:** rapid changes in target pose and position underwater challenge traditional detection algorithms.
>
> **Why underwater object detection matters**
> An efficient underwater detection system supports marine resource development and ecological protection, and provides effective monitoring for marine engineering and defence. Improving the accuracy and real-time performance of underwater detection has significant social, economic and strategic value.

💡 **Use this slide.** Paragraph 1 is the best plain-language answer to *"why is this a hard problem?"* that we have, and a judge will ask it. Rewrite it in your own words — do not read it out.

---

## Slide 5 — The three innovations ⭐

> ### 01 Project Introduction
>
> **Overview of the project's innovations**
>
> 1. **Fine-grained feature extraction module** — by applying a **state-space model**, this module improves the detection system's ability to handle low-contrast and moving targets, and effectively reduces noise interference.
> 2. **Local feature extraction module** — designed specifically for tiny-target detection; it captures the features of tiny targets accurately against complex backgrounds and at low resolution.
> 3. **Multi-scale cross-attention module** — multi-scale feature fusion plus a cross-attention mechanism extracts multi-scale information better, so the model adapts more strongly to targets of different sizes.

*On screen: a large architecture diagram, rotated sideways. It reads: input image → **Object detection backbone** (Simple Stem → fine-grained feature extraction module → Vision Clue Merge → … → SPPF) → **Path aggregation network** (the neck) → **Head** (P3 80×80 small / P4 40×40 medium / P5 20×20 large) → output image with boxes.*

🔑 **This is the slide that resolves our model question.**
"Fine-grained feature extraction module" + "state-space model" = the **`VSSBlock`** in the code she sent. "State-space model" is what the **Mamba** family of models is. So:

| What it is called | Where |
|---|---|
| 细粒度特征提取模块 / fine-grained feature extraction module | the slide |
| `VSSBlock` | `ultralytics/nn/modules/mamba_yolo.py` |
| Mamba / SSM (state-space model) | the research field |
| Vision Clue Merge | both — it is the downsampling step, named the same in the code |

**Say "Mamba-YOLO" on stage, not "YOLOv5" and not "YOLOv8".** More in [`Advisor_Code_Findings.md`](Advisor_Code_Findings.md).

---

## Slide 6 — Section divider

> **02 — Main Work**

---

## Slide 7 — What they built

> ### 02 Main Work
>
> **Data collection**
> - Collect and organise a representative underwater image dataset.
> - Annotate the images, covering diversity of target species, size and pose.
>
> **Model development**
> - **Modular redesign:** replace the **C2f** module in the YOLOv8 architecture with the fine-grained feature extraction module, the local feature extraction module and the multi-scale cross-attention module, improving the system's fine-grained detection performance.
> - **Multi-task loss function:** train the model with a multi-task loss so it stays accurate and robust in complex, changeable underwater environments.
>
> **Platform development**
> - Completed application deployment (**Flask + HTML**).
> - Implemented **real-time monitoring, local video detection, and image detection**.

🔑 **"Replace the C2f module in YOLOv8"** is the precise, honest sentence to use on stage. It is why she says "improved YOLOv8" and why the code says Mamba — both are true. The skeleton is YOLOv8; the blocks inside it are Mamba blocks.

📄 The three platform features named here are exactly the three tabs in her Flask app. See [`Advisor_Code_Findings.md`](Advisor_Code_Findings.md) — **one of the three does not do what its name says.**

---

## Slide 8 — Section divider

> **03 — Results Achieved**

---

## Slide 9 — The numbers ⭐

> ### 02 Results *(her heading says 02; the section is 03 — her typo)*
>
> **Quantitative comparison**
> - Performance compared against the original YOLOv8 and other mainstream methods:
>
> | | mAP50 | mAP50-95 | APs | APm | APl |
> |---|---|---|---|---|---|
> | Original YOLOv8 | 0.855 | 0.516 | 0.166 | 0.402 | 0.664 |
> | **The present invention** | **0.873** | **0.530** | **0.177** | 0.391 | **0.675** |
>
> **Analysis of experimental results**
> - **Detection accuracy (mAP):** in complex underwater environments the system's mean average precision is about **2% higher** than existing underwater detection methods, and it identifies low-contrast, low-clarity underwater targets accurately.
> - **Detection speed (FPS):** while maintaining high accuracy the system keeps a high detection rate, and **on a GPU-equipped system it achieves real-time detection**, meeting the needs of real-time underwater applications.
> - **Robustness:** the system adapts to changes across different depths and water qualities — clear water, turbid water, insufficient lighting — and is robust to small targets and cluttered backgrounds.

**Read the table like this:** *mAP50* = accuracy score when a box counts as correct if it overlaps the true box by half. *APs / APm / APl* = accuracy on small / medium / large objects separately. Higher is better, 1.0 is perfect.

⚠️ **Three honest things about this table.**
1. The gain is **+0.018 mAP50** (0.855 → 0.873) — about 2%, as she says. Real, but small. Do not oversell it.
2. **`APm` went *down*** (0.402 → 0.391). Medium objects got slightly worse. If a judge reads the table and asks, say so plainly — noticing it earns more credit than hiding it.
3. **These are her group's numbers on her hardware, not ours.** Say *"the published result for this model is 0.873"*, never *"we achieved 0.873"*. The training logs she sent show **mAP50 0.867** on the actual run — close, but not the same number, so quote the one you can point at.

📄 **"Real-time on a GPU-equipped system" is the load-bearing sentence for us.** Our laptop has a GPU. Whether this model runs on *our* GPU is the open question — [`Advisor_Code_Findings.md`](Advisor_Code_Findings.md).

---

## Slide 10 — The software platform

> ### 03 Results
>
> **Code deliverables**
> - A complete underwater image object detection algorithm has been developed and successfully deployed to an HTML front end.

*On screen: two screenshots of the web application. The header reads **"Underwater Image Enhancement and Object Detection System"**, with three tabs: **Video Detection · Image Detection · Real-time Monitoring**, a **"Select Video"** button on the right, and a live counter in the top-left of the video showing `starfish: 1` / `holothurian: 4` over green underwater footage with labelled boxes (holothurian 0.87, starfish 0.90, …). Footer: © 2025.*

🔑 **The footage in that screenshot is the video she sent us on 13 September.** Same scene, same green water. So her demo is: open this web page, load that video, let it play with boxes drawn. That is the demo we are being handed.

---

## Slide 11 — Patents and copyright ⭐⭐

> ### 03 Results
>
> **Academic results**
> - One **patent application** filed — *"An underwater object detection method based on improved YOLOv8"* — **accepted** (application no. **2025102917475**)
> - One **software copyright** filed — *"Deep-Learning-Based Underwater Image Enhancement and Object Detection Platform V1.0"* — **registered** (registration no. **2025SR0806055**)
> - Demonstrates technical innovation and legal protection.

*On screen: a scan of the official acceptance notice from the **China National Intellectual Property Administration (CNIPA)**. Readable detail:*

| Field | Value |
|---|---|
| Application no. | **202510291747.5** |
| Filing date | **12 March 2025** |
| Applicant | **Nanjing Vocational University of Industry Technology** (南京工业职业技术大学) |
| Inventors | Li Kaixuan, **Wang Li**, Chen Shuzhuo, Yin Zihang, Zhu Jun |
| Title | An improved YOLOv8 underwater image object detection method, apparatus, medium and program |
| Claims | 10 |

🏆 **This is the 4-point attribution slide, handed to us.** Professional Conduct includes 4 points for respect for intellectual property, and almost no team does this properly. Put on our slide, in English:

> The detection model is the Mamba-YOLO-based system developed by Prof. Wang Li's group at Nanjing Vocational University of Industry Technology.
> Patent application 202510291747.5 (CNIPA, filed 12 March 2025) · Software copyright 2025SR0806055.
> Built on Mamba-YOLO (Apache 2.0) and Ultralytics YOLOv8 (AGPL-3.0). Selective-scan operator from VMamba.
> Our contribution: *[whatever we actually add — deployment, our own footage, our own measurements]*.

⚠️ **Prof. Wang is the 2nd inventor on that patent.** The work belongs to her group. We are demonstrating it with permission — that is a fine and honest story, and it is the story we tell.

---

## Slide 12 — The dataset

> ### 03 Results
>
> **Dataset**
> - Successfully collected **25,060 samples** from relevant public datasets, using **YOLO-format labels**, containing four classes:
>   - **0: holothurian** (sea cucumber)
>   - **1: echinus** (sea urchin)
>   - **2: starfish**
>   - **3: scallop**
> - Provides the base data for follow-up research.

*On screen: a macOS Finder window titled "Underwater image dataset", showing `images` and `labels` folders; `images` is **2.14 GB, 25,060 items**, modified 23 May 2025.*

🔑 **The class order here is the order the model outputs.** `0 holothurian, 1 echinus, 2 starfish, 3 scallop` — confirmed identical in her `URPC/URPC.yaml`. If we ever write our own label list, it must be in this order or every name will be wrong.

⚠️ Note the mismatch worth knowing: the **25,060** figure is her whole collected pool, but the config she actually trained from lists **3,717 training images and 112 validation images**. Quote 3,717 if asked what the model was trained on, or say "a 25,000-image pool" only about the collection.

---

## Slide 13 — Closing

> **Thanks!**
> Thank you, respected experts!

---

## What this deck changes for us

| Question we had | Answer |
|---|---|
| YOLOv5 or YOLOv8? | **Neither on its own — Mamba-YOLO**, i.e. YOLOv8's skeleton with Mamba state-space blocks replacing C2f |
| Which dataset? | URPC, 4 classes, in the order holothurian / echinus / starfish / scallop |
| What accuracy do we quote? | 0.873 mAP50 published; **0.867 in the run she sent us** — quote the second |
| What goes on the attribution slide? | Patent 202510291747.5 · copyright 2025SR0806055 · Apache 2.0 + AGPL-3.0 |
| Is this deck our presentation? | **No.** It is a Chinese research report. She said an English deck is coming |

**Still missing, still worth asking her:** the English deck, and whether we may use her weights and her video in a public demonstration. Ask for that permission in writing — it is the difference between attribution and a problem.
