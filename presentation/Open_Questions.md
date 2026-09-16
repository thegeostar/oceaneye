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

## Answered by the new agenda — uploaded 16 Sept

`reference/Agenda_for_2026_…Southeast.doc` supersedes the 19–21 Sept agenda attached to the invitation letter. Detail: [`../team/competition_days.md`](../team/competition_days.md).

| Question | Answer |
|---|---|
| When exactly do we compete? | **Mon 21 Sept, 13:30–17:00** (Groups 16–30), **Room 501**, New Generation Information Technology Track |
| Can we test the day before? | ✅ **Yes — Sun 20 Sept, 16:00–18:00, Auditorium: "Registration, drawing lots and rehearsal."** Bring the whole rig |
| When can we travel home? | Not before **Tue 22 Sept.** Awarding is 14:40, departure 15:30–21:00 |

## Still open — with the organisers, and more urgent than they look

5. 🔴 **Is anything due before 20 September** — a report, abstract or slide submission? Missing a deadline is the worst possible way to lose. **Ask this today.**
6. 🔴 **How long may the presentation run?** The letter caps the *operation* at 20 minutes, then says "followed by an on-site presentation" **with no duration given.** We had been assuming it was all one 20-minute block; it is not. **Ask at drawing lots on the 20th.** Until then S3's deck flexes between 5 and 10 minutes.
7. 🔴 **Does the agenda's "Group 22" mean us?** Each university numbers its own groups and we are Group 22 on the RUPP list. Morning vs afternoon hangs on it. **Confirm on the 20th, not on the 21st.**
8. Venue power: sockets, voltage, plug type? *(You can answer this yourself at the Sunday rehearsal — go and look.)*
9. Is a water tank permitted on stage, and how long do we get to set up before the clock starts?
10. Is there a safety protocol for water near electrical equipment? *(Safety Awareness is 3 points.)*

## Still open — inside the team

11. Do the other two laptops have an NVIDIA GPU? If only one machine can run the model, **that machine goes on stage and its charger is not optional.**
12. How many hours per day can all three of you actually work, 16–18 Sept?
13. ✅ ~~Has the camera been bought?~~ **Solved — the lent Logitech, $0.** Now: **have the tank and the four real creatures been bought?** That is the last blocking item.
