# What is still unknown

← [README.md](../README.md) · **Owner: S3** · *Trimmed 15 Sept 2026 — the report and thesis answered most of this.*

> The message to send is in **[team/S3_presentation.md §1](../team/S3_presentation.md)**. It lives there, not here, so there is only one copy.

---

## Answered — do not ask again

| Question | Answer, and where it came from |
|---|---|
| Will you send the PowerPoint / an English version? | ✅ `advisor/OceanEye-Cambodia-Report.pdf` — 18 slides, **bilingual** |
| Can you send the model and code? | ✅ Sent 13 Sept. It runs — 1.12 s/image |
| YOLOv5 or YOLOv8? | ✅ **Neither: Mamba-YOLO-L.** Settled by reading the code |
| Which dataset? | ✅ **URPC2021**, 4 classes, order `holothurian · echinus · starfish · scallop` |
| Which Python / PyTorch / CUDA did you use? | ✅ Thesis Table 4.1 — Python 3.10.19, PyTorch 2.1.0, CUDA 11.8, Ultralytics 8.4.24, Ubuntu 22.04, 48 GB vGPU, 300 epochs, batch 16, 640×640 |
| What accuracy may we quote? | ✅ **0.867** — best epoch in the log we hold. Not 0.873, which is their full three-module model |
| Does enhancement help detection, or only human viewing? | ✅ **It helps detection, measurably** — thesis §4.5, mAP 76.2 → 87.7 on degraded input. Cite as theirs |
| Is a camera platform acceptable instead of an ROV? | ✅ Effectively — she said the China hardware cannot arrive and we must use our own |
| Is `best.onnx` supposed to work? | We measured zero detections at any threshold. Report it as courtesy; it changes nothing for us |

---

## Still open — with the advisor

1. 🔴 **Written permission** to demonstrate the model and footage publicly, with attribution. **Worth 4 rubric points and not yet in hand.** This is the only urgent one.
2. The URPC2021 dataset or its link — to show one labelled example on a slide. Low urgency, we are not retraining.
3. Available online 20–22 Sept? Plan as if no.
4. *"What is our innovation point, in your view?"* — ask separately, later. Worth 10 points.

## Still open — with the organisers, and more urgent than they look

5. 🔴 **Is anything due before 20 September** — a report, abstract or slide submission? Missing a deadline is the worst possible way to lose. **Ask this today.**
6. Venue power: sockets, voltage, plug type?
7. Is a water tank permitted? How long do we get to set up before the 20 minutes starts? Can we test the day before?
8. Is there a safety protocol for water near electrical equipment? *(Safety Awareness is 3 points.)*

## Still open — inside the team

9. Do the other two laptops have an NVIDIA GPU? If only one machine can run the model, **that machine goes on stage and its charger is not optional.**
10. How many hours per day can all three of you actually work, 15–18 Sept?
11. Has the camera been bought? This is the last unbought item and shipping time is the binding constraint, not money.
