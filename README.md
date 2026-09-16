# OceanEye — Group 22

**Today is Wednesday 16 September.** Three working days: Wed 16 → Fri 18. Sat 19 travels.

**We compete Monday 21 September, 13:30–17:00, Room 501.** Rehearsal on the real stage **Sunday 20th, 16:00–18:00** — bring everything.
📄 **All three days, hour by hour → [team/competition_days.md](team/competition_days.md)**

---

## Read one file. Yours.

| You | Open this | It contains |
|---|---|---|
| **S1** | **[team/S1_hardware.md](team/S1_hardware.md)** | Camera, tank, lighting, filming, packing. **Operation 00:00–08:00** |
| **S2** | **[team/S2_software.md](team/S2_software.md)** | Making the AI run, camera→AI, backups. **Operation 08:00–20:00** |
| **S3** | **[team/S3_presentation.md](team/S3_presentation.md)** | Slides, attribution, the story. **The presentation, which comes *after* the 20 minutes** |

Each one is a single page with dated checkboxes. **Nobody reads everything.**

> ⚠️ **Changed 16 Sept.** We had been splitting one 20-minute block three ways. The invitation letter actually says *"complete the skill operation **within 20 minutes**… **followed by** an on-site presentation"* — so the 20 minutes is **S1 + S2 only**, and S3's slides are a separate thing afterwards. **S2 gains about 5 minutes; S3 is no longer squeezed.** The presentation's own length is not stated anywhere — ask at drawing lots on the 20th.

Two more, for everyone:
- **[team/competition_days.md](team/competition_days.md)** — the three days hour by hour. **Read before you pack.**
- **[team/IF_IT_BREAKS.md](team/IF_IT_BREAKS.md)** — what to say on stage when something fails. **Print it.**
- **[team/glossary.md](team/glossary.md)** — every technical word in plain English. Search it, don't read it.

---

## What we are building, in 5 lines

1. A **USB webcam** looking through the wall of a glass tank of water, with **real** sea creatures in it (from the market — the AI was trained on real ones, so toys risk being misread).
2. Software on a laptop that watches the video, **draws a box around each creature** and names it.
3. Four creatures only: **sea cucumber, sea urchin, scallop, starfish.**
4. It must work **with the Wi-Fi off.** The venue has no internet.
5. **A 20-minute live operation, then a presentation.** Three of us, one part each.

**The thing that wins:** 25 of the 100 points go to *running it smoothly* — Skill Proficiency 15 + Operational Standardization 10. Zero points go to how clever the AI is. **Rehearse more than you build.**

---

## Where the project stands

✅ **The model runs.** 1.12 s per image, live camera smooth at ~26 fps, UI fully English. It reproduces the authors' own published detections byte for byte. → [HOW_TO_RUN.md](software/advisor_code/HOW_TO_RUN.md)

🔴 **The advisor's deck claims more than we can run.** It presents a two-stage system (FSCIN restoration → improved YOLOv8). We have one stage, and only one of its three modules. **We demo what runs and credit the rest to the authors.** Read this before writing any slide: [advisor/Advisor_Code_Findings.md](advisor/Advisor_Code_Findings.md) §3.

✅ **Camera in hand** — the lent Logitech 1080p webcam. It films *through* the glass, so it stays dry.

⏳ **Untested on our own creatures.** Tank and 4 specimens still to buy. Expect weaker detections than on her sample images and know how to read that before panicking → ["Your own tank"](software/advisor_code/HOW_TO_RUN.md) in HOW_TO_RUN §5.

⏳ Written permission to use the model publicly is not yet in hand.

---

## The 5 rules

1. **Never wait for the advisor.** Ask, then keep working. Adjust when she answers.
2. **Nothing new after Wednesday 16th.** Feature freeze. "What if we also added…" → write it on an after-the-competition list.
3. **Do NOT make the scene easy.** Clean footage of *deliberately murky* water. Difficulty is worth 15 points — don't throw it away by using clear water.
4. **Never say a number you haven't measured.** One follow-up question exposes a bluff, and honesty is scored directly.
5. **Never present someone else's result as ours.** The model is Li Kaixuan's, supervised by Prof. Wang Li. Respect for IP is an explicit 4-point item — and saying so out loud *earns* those points.

---

## Where everything else lives

Open these only when your page sends you there.

| Folder | What's in it | Whose |
|---|---|---|
| `advisor/` | **[Advisor_Code_Findings.md](advisor/Advisor_Code_Findings.md)** = what runs, what doesn't, which numbers we may quote. `OceanEye-Cambodia-Report.pdf` = the bilingual 18-slide deck. The thesis PDF = the method behind it | S2 / S3 |
| `presentation/` | `Operation_Script_v2.docx` — stage script, Q&A bank, fallback lines. **Read only your own role** | all |
| `hardware/` | Shopping list, shops, prices. **`Purchase_Log.md` is a form — fill it in** | S1 |
| `software/` | **[advisor_code/HOW_TO_RUN.md](software/advisor_code/HOW_TO_RUN.md)** is the only page you need | S2 |
| `reference/` | Official rules and scoring · [`Core_Strategy_Data_Quality.md`](reference/Core_Strategy_Data_Quality.md) (why the light goes to the side) · `Research_Brief.md` (**not this week**, look-up only) | all |
| `CONTEXT.md` | For starting a new AI chat, not for humans | — |

---

## Sharing this folder

`git` + a private GitHub repo, step by step: **[team/github_setup.md](team/github_setup.md)**

The big files (AI weights, advisor code, videos) **cannot go on GitHub.** They go in a shared Google Drive folder. Both, not one.

> 🔴 **`software/advisor_code/output_dir/mscoco/mambayolo_n/weights/best.pt` is the single most valuable file we have.** 139 MB, and it only exists because the advisor sent it. **Two USB sticks and a cloud folder, today.**

---

## Daily rhythm

Every evening, paste into the chat: *"Day N done. Here's what we produced: [paste]. Sufficient, or adjust?"*
