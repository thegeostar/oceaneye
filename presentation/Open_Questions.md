# OceanEye — Questions for Prof. Wang Li (王丽)

> **← [README.md](../README.md) · Day 1 step 2 sends you here.**
>
> **Owner:** S3 · **Do this now:** scroll to [📋 Copy-paste message](#-copy-paste-message-for-wechat--the-group), copy it, send it · **Then keep working.** Do not wait for her reply.
>
> **TL;DR**
> - **Rewritten 13 September.** She sent the slides, the code, the weights and a test video, so most of the old questions are dead — sending them now would ask her for things she already gave.
> - **Five questions left.** One of them — written permission — is worth real rubric points.
> - Section B is unchanged and still useful. Ask those as they come up, never all at once.

---

## ✅ What she already answered by sending files (do not ask again)

| Old question | Answer, and where it came from |
|---|---|
| A1 · Is a simple camera platform acceptable instead of an ROV? | **Effectively yes.** She said the China hardware cannot arrive and we must use our own. Worth one confirming line in the message below, no more |
| A2 · Will you send the PowerPoint? | ✅ Sent 13 Sept, in Chinese. English version promised, **not yet arrived** — still chased below |
| A3 · Can you send the model and code? | ✅ **Sent — and they are real.** `best.pt`, 145 MB, mAP50 0.867. The single biggest thing that has happened to this project |
| A4 · Is there a budget? | Unanswered, but overtaken — the camera is the only unbought item and it is ~US$30 |
| A5 · YOLOv5 or YOLOv8? | ✅ **Neither: Mamba-YOLO-L.** Settled by reading her code. Do not reopen |
| A6 · Is the data URPC/DUO? | ✅ **URPC**, 4 classes, order `holothurian · echinus · starfish · scallop` |
| A7 · Available online during the competition? | Still unanswered — kept below |

📄 Full detail on what arrived → [`../advisor/Advisor_Code_Findings.md`](../advisor/Advisor_Code_Findings.md)

---

# The five questions that are left

### 🔴 Q1. May we use your model and your video publicly, with attribution?

**The most important question on this page now**, and it has replaced the old A1 at the top.

We are about to demonstrate, in front of international judges, a model that is **her group's patented work** (CNIPA application 202510291747.5, on which she is an inventor). Attribution with permission is a **4-point scoring item**. Attribution without permission is a problem nobody wants to discover on stage.

She will almost certainly say yes. Get it **in writing** anyway — a WeChat message is enough.

---

### 🔴 Q2. Which PyTorch and CUDA version did you run?

Sounds trivial. It is not — it could save us a full day.

Her model needs a compiled piece of GPU code, and compiled code only works with the exact Python and PyTorch it was built against. **If she answers this, getting her model running becomes mechanical instead of guesswork.** This is the current blocker on the entire project.

---

### 🟠 Q3. Is `best.onnx` supposed to work?

We tested it: it loads, it runs, and it **detects nothing at any threshold** — on the very images her `.pt` detects confidently. The custom Mamba operator does not survive ONNX export.

Ask plainly and without blame. She may not know, and she would want to. *(We have already stopped relying on it, so her answer changes nothing for us — but reporting it is the professional thing to do, and it shows we actually ran her code.)*

---

### 🟠 Q4. Can you send the URPC dataset, or the link you used?

We are **not retraining** — we do not need it to run the demo. But having it lets us show a labelled sample on a slide and answer "what was it trained on?" with a file rather than a claim.

Low urgency. Do not let it delay anything.

---

### 🟡 Q5. Will you be available online during 19–21 September?

Unchanged from the old list, still unanswered. Plan as if the answer is no (that is decision D10), but ask, because a 10-minute call the night before is worth a lot if it is available.

**Also still chasing: the English slides.** Fold it into the same message.

---

## 📋 Copy-paste message for WeChat / the group

> Dear Professor Wang,
>
> Thank you very much for the slides, the code, the model and the test video. We have set up the project and read through your system — it is a great help.
>
> We have five short questions:
>
> 1. May we use your trained model and your test video in our competition demonstration, with full attribution to your group and to the patent? We would like to put the patent number and the software copyright number on our attribution slide.
> 2. Which versions of Python, PyTorch and CUDA did you use to run the model? We are configuring the environment and want to match yours exactly.
> 3. We tried the `best.onnx` file and it produced no detections, although `best.pt` works in your own example images. Is the ONNX export expected to work, or should we use `best.pt`?
> 4. If it is convenient, could you share the URPC dataset or the link you used? We do not plan to retrain — we would like to show a labelled example on our slides.
> 5. Will you be available online during 19–21 September if we need support? And may we still receive the English version of the presentation?
>
> We are working hard and will send you a video of our full run before the competition.
>
> Thank you,
> Group 22 — Dararoth, Yuleang, Sophearoth

---

# SECTION B — Ask along the way

Grouped by when they naturally come up. Do not send these all at once — you will overwhelm her and dilute the five above.

## Ask around Day 3 (once the model is running)

**B1. ✅ Mostly answered.** *What accuracy may we quote?* — her training log says **mAP50 0.867**; her slide says 0.873. **Quote 0.867**, it is the one we hold a file for. Only ask her if you want the 0.873 run explained.

**B2. Does the enhancement step help detection, or only human viewing?**
She may already have measured this. If not, you measure it and report honestly.

**B3. ❌ Dead.** *How many images and how long should we train?* — we are not training.

**B4. Should the demo show live video, or is processing a recorded file acceptable?**
⚠️ **Sharper now than when it was written.** Her own code's "Real-time Monitoring" tab plays a recorded file while labelled real-time. Ask her directly what she intends to be shown as live — and whichever way she answers, we label recorded footage as recorded.

## Ask around Day 3–4 (when the presentation takes shape)

**B5. Is the presentation in English? How long? Are slides allowed?**
The script is English with Chinese headers, so English is likely — but confirm.

**B6. Must all three of us speak, and in the assigned order?**
Affects rehearsal.

**B7. Is anything due before 19 September — a report, abstract, or slide submission?**
**Ask this one early if you can.** Missing a submission deadline would be the worst way to lose.

**B8. What is our innovation point, in your view?**
Her system already does detection and counting. So what makes *Group 22's* version different? Candidates to put to her — the first one is stronger than it was, because **her shipped code has no tracking at all**:
- **Unique counting with tracking** — turning per-frame detections into a real survey count. A genuine, demonstrable delta over what she sent us
- **Turbid-water robustness** — simulating Tonle Sap conditions no dataset covers
- **Cambodian application** — reframing marine ranching (海洋牧场) for inland freshwater aquaculture
- **Ultra-low-cost deployment** — a US$30 acquisition platform instead of a US$2,500 ROV

She has seen this competition before. Her answer is worth 10 rubric points.

**B9. Can we use Cambodian or Southeast Asian footage?**
Even 30 seconds of local pond or Tonle Sap video beside the Chinese dataset results would make the application story concrete.

## Ask around Day 4–5 (logistics)

**B10. What power is available at the venue — sockets, voltage, plug type?**

**B11. Can we set up and test the day before? How long do we get to set up before our 20 minutes starts?**

**B12. Is there a safety protocol we must follow for water and electrical equipment?**
*Safety Awareness is 3 points.*

**B13. Would you review a video recording of our full run before 19 September?**
Ask in advance so she reserves the time.

**B14. What did winning teams do well in past years? What did losing teams get wrong?**
Pure gold if she answers, but low urgency.

---

# What I still need from YOU (not from her)

1. ~~**Do any of your laptops have an NVIDIA graphics card?**~~ ✅ **Answered — RTX 5060, 8 GB, verified.** Follow-up: **do the other two laptops have one?** If only one machine can run the model, that machine goes on stage and its charger is not optional.
2. **How many hours per day can all three of you actually work, 13–16 September?** If you have classes, tell me and I will compress the plan.
3. **How reliable is your internet at home?** Day 2 needs a ~3 GB PyTorch download.
4. **Can you get to an electronics market or does everything ship?** The camera is the last unbought item.

Answer these in chat and I will adjust the roadmap the same day.
