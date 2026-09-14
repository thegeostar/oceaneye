# Core Strategy — Data Capture Quality as the Primary Design Constraint

> **← [START_HERE.md](../START_HERE.md) tells you what to do. This page is *why*. It is the reasoning behind most of the decisions on that page.**
>
> **Owner:** all three · **Open it when:** you are about to make a hardware or software choice and want to know which option is right · **Read once, properly.** Then use START_HERE for daily work.

## 🏃 The whole document in 6 lines

1. Judges score **"did the demo visibly work in that room for 20 minutes"** — not accuracy. (§1)
2. Information destroyed at the camera **cannot be recovered by software.** Enhancement moves detail around; it never creates it. (§2)
3. ⭐ **Move the light 20–40 cm away from the lens.** Free, and the single biggest win available to you. (§3)
4. **Lock exposure, white balance, gain, and force MJPG** — then write the numbers down. Most teams never do this. (§3.8)
5. **Fine-tune on footage from your own tank.** 200–300 of your own frames beat thousands of foreign ones. (§5)
6. ⭐ **The rule: maximise capture quality, do NOT minimise scene difficulty.** Clean footage of *deliberately murky* water. (§1)

**Jump to:** [§1 the rule](#1-first-the-paradox-you-raised--resolved) · [§3 the leverage ladder](#3-the-leverage-ladder--do-these-in-order) · [§3.8 lock the camera](#-tier-3--free-and-constantly-overlooked) · [§6 turbidity ladder](#6-the-signature-demo-the-turbidity-ladder) · [§7 where to spend effort](#7-where-to-spend-your-effort--the-answer-to-accuracy-isnt-scored) · [§10 success test](#10-success-test)

---

## 1. First, the paradox you raised — resolved

You were right to push on this. I said *"accuracy earns no rubric points."* I am now saying *"data quality is the most important thing."* Both are true, and the resolution matters:

> **What is scored is not accuracy. It is whether the detection visibly works, on screen, in that room, for those 20 minutes.**

A held-out mAP score is invisible to judges. What they see is: do boxes appear on the right animals, does the count increment sensibly, does it hold up when the operator changes something. That visible reliability is scored under **Skill Proficiency (15)** and **Task Difficulty (15)**, and a crash or a blank screen destroys both.

So the objective function is not `maximize mAP`. It is:

```
maximize  P(the demo visibly succeeds on 19 September)
```

**Capture quality is the cheapest and highest-leverage input to that probability.** That is the whole argument. Not because clean data raises a benchmark number, but because clean data is what makes the live run survive contact with a real room.

### The trap on the other side

If you optimise naively for "the model must succeed," you will be tempted to make the *scene* easy — clear water, big targets, close range, no clutter. **That would cost you Task Difficulty (15 points)**, which explicitly rewards work that is *"sufficiently challenging."*

> ## ⭐ The rule
> **Maximise capture quality. Do NOT minimise scene difficulty.**
>
> - **Capture quality** = signal-to-noise, focus, exposure stability, lighting geometry, rigidity → **always maximise**
> - **Scene difficulty** = turbidity, small targets, occlusion, clutter, camouflage → **deliberately keep high, and show it**

You want a **high-fidelity recording of a genuinely hard scene.** Not a clean recording of an easy one. This distinction is the strategic core of the project.

---

## 2. The physical principle

Light travels: **subject → water → port glass → lens → sensor → file → model.**

Every stage destroys information, and **information destroyed at capture cannot be restored downstream.**

This is the part beginners get wrong. Enhancement algorithms — white balance, CLAHE, dehazing — **redistribute signal that is already present.** They do not create signal. If the sensor recorded mostly noise in the red channel, CLAHE will faithfully amplify that noise into colourful garbage.

> **Corollary:** one hour spent improving lighting geometry is worth more than ten hours spent tuning the enhancement pipeline. Spend your effort as early in the chain as possible.

---

## 3. The leverage ladder — do these in order

### 🥇 Tier 1 — free, and the largest effect

**1. Separate the light from the lens. This is the single biggest win available to you.**

The number one underwater imaging mistake is putting the light next to the camera. Every suspended particle between lens and subject reflects your light straight back — **backscatter** — and the image fills with glowing white specks and a veiling haze. The effect grows with turbidity, which is exactly the condition you are designing for.

Your USB endoscope has LEDs in a ring *around the lens*. **That is the worst possible geometry.**

> **Do this:** turn the built-in ring LEDs **down or fully off**, and light the scene with a **separate waterproof torch offset 20–40 cm to the side**, angled so its cone hits the subject but the lens never looks directly down the illuminated water column.
>
> Cost: one torch and a zip tie. Effect: dramatic. Very few student teams know this.

**2. Shorten the water path.** Attenuation is exponential in distance — `I = I₀·e^(−βd)`. Halving the camera-to-subject distance beats any algorithm you could write. Work at **10–25 cm**, not a metre. In a tank you control this completely.
*Trade-off:* closer means a narrower field of view and fewer targets per frame. Find the distance where 3–6 targets are visible and stop there.

**3. Kill reflections.** Line the far wall and floor of the tank with **matte black** plastic or card. Removes room-light reflections, glass glare, and specular hotspots. Also makes the tank read better on camera for the judges. Cost: ~US$3.

**4. Clean the optics before every run.** Bubbles and smears on the port destroy small-object detection. Wipe it, and rub a trace of dish soap on the port — a standard diver's trick that stops bubbles adhering. **Put this on the pre-flight checklist.**

**5. Stabilise.** Motion blur is fatal for small targets. Mount the camera rigidly. Move slowly, and pause while detections are being read aloud.

### 🥈 Tier 2 — a few dollars, large effect

**6. Diffuse the light (~US$2).** A bare LED gives a hotspot, hard shadows, and dark vignetted corners — so the same animal looks different depending on where it sits in frame. Tape a piece of **white translucent plastic** (a milk-jug wall, baking paper) over the torch. Soft, even illumination. This directly attacks the "non-uniform artificial lighting" problem.

**7. Print a white-balance / colour reference card (~US$1).** A small white-and-grey card placed in frame at the start of a run lets you set white balance objectively, and gives you a defensible answer when a judge asks how you handled colour distortion. *"We calibrate against a reference target"* is a professional answer.

### 🥉 Tier 3 — free, and constantly overlooked

**8. Lock the camera's automatic settings. Most teams never do this, and it silently ruins everything.**

By default a webcam continuously re-adjusts exposure, gain, and white balance. Consequences:
- Brightness and colour **drift between frames**, so the model sees a moving target
- Detections flicker on and off, which looks like an unreliable system to a judge
- **Runs are not reproducible**, which undermines *Operational Standardization (10 pts)*

Lock everything before the run:

```python
import cv2

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)          # explicit backend on Linux

# ⚠️ Set FOURCC FIRST. Many UVC cameras default to raw YUYV, which caps
# 1080p at ~5 fps. MJPG is compressed and gives you 30 fps.
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

# Disable the automatics (values are driver-dependent — verify, don't trust)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)   # 0.25 = manual on many V4L2 drivers
cap.set(cv2.CAP_PROP_EXPOSURE, 150)         # tune by eye, then WRITE THE NUMBER DOWN
cap.set(cv2.CAP_PROP_AUTO_WB, 0)
cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 4500)
cap.set(cv2.CAP_PROP_GAIN, 0)               # gain adds noise — keep low, add light instead

for prop, name in [(cv2.CAP_PROP_FRAME_WIDTH, 'w'), (cv2.CAP_PROP_FPS, 'fps'),
                   (cv2.CAP_PROP_EXPOSURE, 'exp')]:
    print(name, cap.get(prop))     # always verify — set() silently fails on many drivers
```

More reliable on Linux, and worth doing as a shell step before launching:

```bash
v4l2-ctl --list-devices                    # find your camera
v4l2-ctl -d /dev/video0 --list-ctrls       # see what it actually supports
v4l2-ctl -d /dev/video0 -c auto_exposure=1 -c exposure_time_absolute=150 \
                        -c white_balance_automatic=0 -c gain=0
```

> **Record the exact settings that worked in `05_Hardware/Purchase_Log.md`.** Reproducing them on competition day is worth real points, and rediscovering them under pressure is a nightmare.

**9. Prefer light over gain.** If the image is dark, add illumination — never raise gain/ISO. Gain multiplies noise, and noise is what destroys small-target detection.

---

## 4. Software: enhancement, and the trap inside it

Enhancement code already exists in `06_Software/oceaneye/vision.py`: gray-world white balance, then CLAHE on the LAB lightness channel. That order is deliberate — correct colour first, then contrast, or you amplify the cast before removing it.

> ### ⚠️ The trap that will silently cost you accuracy
> **Whatever preprocessing you apply at inference, you must also apply during training.**
>
> If you train on raw images and run inference on enhanced ones, you have manufactured a domain shift and made your system *worse* — while believing you improved it. Pick one pipeline and use it on both sides. Write it down.

**Second point, for honesty:** enhancement reliably improves what a *human* sees. Its effect on *detector* accuracy is genuinely mixed in the literature. So:

- Use enhancement as a **visualisation layer** — the before/after toggle is your best visual moment
- Use turbidity simulation as **training augmentation** — this is well supported
- **Measure** the effect on detection and report it honestly, whatever it is

A judge asking *"does that actually help the AI, or just look nicer?"* is answerable with: *"It helps the operator see. For the detector we measured a change of X points — we use it primarily for visualisation and as an augmentation strategy."* That answer scores under Professional Ethics. A bluff does not.

---

## 5. The one thing that most improves live demo success

> **Fine-tune on footage from your own rig, in your own tank, under your own lighting.**

A model trained on the DUO dataset has learned Chinese seabed conditions. Your tank looks nothing like that. Even 200–300 labelled frames captured on your actual setup will outperform a model trained on thousands of foreign images, *for your specific demo*.

**Procedure:** capture 3–5 minutes on the rig → extract every 10th frame → label with the pre-trained model and correct the mistakes (auto-labelling, far faster than from scratch) → fine-tune → verify on a fresh recording.

**Disclose it.** *"We fine-tuned on data captured with our own platform to adapt the model to our deployment conditions"* is **domain adaptation** — standard, respectable practice, and exactly what a real deployment would do. Stating it plainly is a strength. Hiding it would be the problem.

---

## 6. The signature demo: the turbidity ladder

This is your innovation moment, it costs about US$2, and no other team will do it.

**Setup:** clean water, camera fixed, lighting fixed, settings locked. A measured amount of clay/fine soil to hand, and a spoon.

**Run:** at each turbidity level, hold 20 seconds and record what the system reports.

| Level | Water | What you say |
|---|---|---|
| L0 | Clear | "Baseline. The system detects N targets." |
| L1 | 1 spoon clay | "This is typical coastal water." |
| L2 | 2 spoons | "This is Tonle Sap in flood season." |
| L3 | 3 spoons | "This is beyond what any camera system handles — and here is where ours stops." |

**Why this wins:**
- It is **live, physical, and unfakeable.** It proves the system is running, not a video.
- It manufactures **Task Difficulty (15 pts)** on demand, in front of the judges.
- Showing where it **fails** is more credible than claiming it never does — and *"we characterised our operating envelope"* is engineering, not excuse-making.
- It produces **real numbers you are allowed to quote** — measured on your own rig, not borrowed from a paper.
- It is the perfect moment for the enhancement toggle: at L2, flip enhancement off and on.

**Measure this during rehearsal**, three runs per level, and put the table in your slides:

| Turbidity | Detections | Mean confidence | Enhancement ON vs OFF |
|---|---|---|---|
| L0 | | | |
| L1 | | | |
| L2 | | | |
| L3 | | | |

That table is a **graceful-degradation curve for a US$30 sensor**. It is honest, it is yours, and it is genuinely more interesting than another team's mAP claim.

---

## 7. Where to spend your effort — the answer to "accuracy isn't scored"

| Lever | Cost | Effect on *visible* demo success | Rubric points touched |
|---|---|---|---|
| Offset the light from the lens | $8, 1 hr | 🟩 **Very high** | Task Difficulty, Skill Proficiency |
| Lock exposure / WB / MJPG | $0, 30 min | 🟩 **Very high** | Operational Standardization |
| Shorten camera-to-subject distance | $0, 15 min | 🟩 **Very high** | Skill Proficiency |
| Fine-tune on own-rig footage | 2–3 hrs | 🟩 **Very high** | Skill Proficiency |
| Matte black tank lining | $3, 20 min | 🟨 High | Craftsmanship |
| Light diffuser | $2, 10 min | 🟨 High | — |
| Enhancement pipeline | 3 hrs | 🟨 Medium (visually: very high) | Tech Advancement, Presentation |
| Turbidity ladder rehearsal | $2, 2 hrs | 🟩 **Very high** | Task Difficulty, Innovation |
| More training epochs | 6+ hrs | 🟥 Low | ~none |
| Bigger model | hrs, slower FPS | 🟥 Low / negative | ~none |
| Architecture modifications | days | 🟥 Negligible in 5 days | ~none |

**Read the bottom three rows.** That is what "accuracy isn't scored" actually means in practice: the classic accuracy levers are expensive and earn nothing, while the top rows are cheap, fast, and decide whether the demo works at all.

**Data quality is not a substitute for accuracy work — it is a cheaper route to the same visible outcome.**

---

## 8. Consequences for hardware selection

Ranked by how much they affect capture quality — buy in this order:

1. **Camera must be UVC** — non-negotiable. No UVC, no manual control, no locked exposure, no reproducibility.
2. **A separate waterproof torch matters more than a better camera.** Given a choice between a 1080p camera with ring lights only, and a 720p camera plus an offset torch — **take the 720p and the torch.** Lighting geometry beats resolution.
3. **Manual focus, or fixed focus at a known distance,** beats autofocus. Autofocus hunts in low contrast and will hunt constantly underwater.
4. **Resolution above 1080p is wasted.** You infer at 640px. Spend the money on light.
5. **A clear tank, not an opaque tub** — judges must see the scene and the water state, otherwise the turbidity demo is invisible to them.
6. **Wired USB, never Wi-Fi.** Wi-Fi cameras drop frames, add latency, need an app, and may not work offline.

---

## 9. Consequences for software strategy

1. **Build the capture layer before the model layer.** Get a stable, locked, well-lit stream first. Model work on an unstable stream is wasted.
2. **Log the capture settings alongside every recording.** Reproducibility is a scored criterion.
3. **One preprocessing pipeline, used identically in training and inference.** (§4)
4. **Fine-tune on own-rig footage** — highest-leverage software task available. (§5)
5. **Keep the enhancement toggle bound to a key** — it is your best visual and your best proof the system is live.
6. **Instrument the demo:** on-screen count, per-species totals, FPS, and turbidity level. Numbers on screen turn a demo into a measurement.
7. **Fail gracefully.** If a frame is unreadable, show "low visibility — no confident detection" rather than freezing or crashing. A system that reports its own uncertainty looks far more professional than one that guesses.

---

## 10. Success test

You have got this right when, on 16 September, all of the following are true:

- [ ] The image is well-lit with the light **offset from the lens**, and you can explain why
- [ ] Exposure, white balance and gain are **locked**, and the values are written down
- [ ] The camera reports **≥ 25 fps** at your chosen resolution (MJPG confirmed)
- [ ] The model was **fine-tuned on footage from this exact rig**
- [ ] The turbidity ladder has been run **three times** and the numbers are in the slides
- [ ] The same preprocessing runs in **both** training and inference
- [ ] You can state, honestly, at what turbidity the system stops working
