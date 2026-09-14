# OceanEye — Group 22

**Competition: Sunday 20 – Tuesday 22 September 2026.** *(Moved from 19–21.)*
**Today is Monday 14 September.** Five working days: Mon 14 → Fri 18. Sat 19 travels.

---

## Read one file. Yours.

| You | Open this | It contains |
|---|---|---|
| **S1** | **[team/S1_hardware.md](team/S1_hardware.md)** | Camera, tank, lighting, filming, packing. Stage 00:00–06:30 |
| **S2** | **[team/S2_software.md](team/S2_software.md)** | Making the AI run, camera→AI, backups. Stage 06:30–13:00 |
| **S3** | **[team/S3_presentation.md](team/S3_presentation.md)** | Slides, attribution, Prof. Wang, the story. Stage 13:00–20:00 |

Each one is a single page with dated checkboxes. **Nobody reads everything.**

Two more, for everyone:
- **[team/IF_IT_BREAKS.md](team/IF_IT_BREAKS.md)** — what to say on stage when something fails. **Print it.**
- **[team/glossary.md](team/glossary.md)** — every technical word in plain English. Search it, don't read it.

---

## What we are building, in 5 lines

1. A **waterproof USB camera** on a pole, in a clear tank of water, with plastic sea creatures in it.
2. Software on a laptop that watches the video, **draws a box around each creature** and names it.
3. Four creatures only: **sea cucumber, sea urchin, scallop, starfish.**
4. It must work **with the Wi-Fi off.** The venue has no internet.
5. **20 minutes on stage.** Three of us, one part each.

**The thing that wins:** 25 of the 100 points go to *running it smoothly* — Skill Proficiency 15 + Operational Standardization 10. Zero points go to how clever the AI is. **Rehearse more than you build.**

---

## Today's one thing each

| | Do this before anything else today |
|---|---|
| **S1** | **Buy the camera.** Nothing has been bought yet. Shipping time is what kills us, not money. |
| **S2** | **Get `best.pt` to draw one correct box on one image.** Nothing is installed yet. This decides the week. |
| **S3** | **Message Prof. Wang** for written permission to use her model and video publicly. |

---

## The 5 rules

1. **Never wait for Prof. Wang.** Ask, then keep working. Adjust when she answers.
2. **Never let hardware block software.** `python oceaneye_demo.py --profile desk` runs the whole system with no camera and no model.
3. **Nothing new after Wednesday 16th.** Feature freeze. "What if we also added…" → no, write it on an after-the-competition list.
4. **Do NOT make the scene easy.** Clean footage of *deliberately murky* water. Difficulty is worth 15 points — don't throw it away by using clear water.
5. **Never say a number you haven't measured.** One follow-up question exposes a bluff, and honesty is scored directly.

---

## Where everything else lives

Open these only when your page sends you there.

| Folder | What's in it | Whose |
|---|---|---|
| `advisor/` | What Prof. Wang sent. **[Advisor_Code_Findings.md](advisor/Advisor_Code_Findings.md)** = what actually works and what's broken. **[PPTX_Translation_EN.md](advisor/PPTX_Translation_EN.md)** = her slides in English; slide 11 is the attribution slide | S2 / S3 |
| `presentation/` | `Operation_Script_v2.docx` — the stage script, Q&A bank, fallback lines. **Read only your own role** | all |
| `hardware/` | Shopping list, shops, prices. **`Purchase_Log.md` is a form — fill it in** | S1 |
| `software/` | Our code + `README.md`, every command you type. `advisor_code/` is Prof. Wang's, with our fixes | S2 |
| `reference/` | Official rules and scoring · [`Core_Strategy_Data_Quality.md`](reference/Core_Strategy_Data_Quality.md) (why the light goes to the side) · `Research_Brief.md` (**not this week**, look-up only) | all |
| `archive/` · `.venv/` | Old drafts and the Python install. Ignore both. **Never move `.venv/`** | — |

---

## Sharing this folder

`git` + a private GitHub repo — step by step, assuming you've never used it:
**[team/github_setup.md](team/github_setup.md)**

The big files (AI weights, advisor code, videos) **cannot go on GitHub**. They go in a shared Google Drive folder. Both, not one.

> 🔴 **`software/advisor_code/output_dir/mscoco/mambayolo_n/weights/best.pt` is the single most valuable file we have.** 139 MB, and it only exists because Prof. Wang sent it. **Two USB sticks and a cloud folder, today.**

---

## Daily rhythm

Every evening, paste into the chat: *"Day N done. Here's what we produced: [paste]. Sufficient, or adjust?"*
