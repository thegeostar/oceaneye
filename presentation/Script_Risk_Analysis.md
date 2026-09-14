# Script Risk Analysis — Is the Advisor's Script Overfitted to a Previous Competition?

> **← [README.md](../README.md) is the main page. This one is already actioned — the fixes are in `Operation_Script_v2.docx`, which is what you actually read and speak.**
>
> **Owner:** S3 · **Open it when:** a judge (or Prof. Wang) asks *why* your script differs from hers · **You do not need this to rehearse.**

> ### 🔄 Updated 13 September — one section flipped
> Prof. Wang sent her actual code and model. **§5 has been rewritten: the "our model is not cutting-edge" problem no longer exists.** It is Mamba-YOLO, a 2024 state-space architecture with a 2025 patent behind it, and that is worth real points on Technological Advancement (15 pts). §1's inference about reused material stands, and everything else below is unchanged.

## 🏃 The verdict in 4 lines

1. Her **technical content is sound.** Keep it. Roles, species, workflow, model stack — all unchanged. ✅ **Now confirmed against her actual code, not inferred.**
2. Her **framing** is aimed at a Chinese marine audience and a presentation format. You face a Cambodian venue and a *20-minute live operation*.
3. That gap is worth **25–30 unclaimed rubric points** (safety, cost, IP, sustainability, local relevance, teamwork).
4. ⭐ **The fix: technology-transfer framing.** *"Chinese marine technology, adapted to Mekong freshwater aquaculture."* Free, contradicts nobody, travels well to the finals in China.

---

## 1. What the evidence actually supports

Let me separate what I can demonstrate from what I am inferring.

**Demonstrated:**
- Her reference videos are **@DWIRobo vendor marketing clips** dated **April and June 2025**, and the underwater footage inside one is timestamped **2021**.
- The script's four species — **sea cucumber, sea urchin, scallop, starfish** — are exactly the **URPC / DUO** class list, a Chinese underwater robot-picking competition dataset.
- The script's stated application domain is **"marine monitoring, ecological protection, underwater exploration"**, and the vendor caption uses **海洋牧场 (marine ranching)**.
- The script contains **no mention** of safety, cost, intellectual property, teamwork, or sustainability.
- The script contains **no numbers** at all.

**Inferred (lower confidence):** that this is a reused or adapted deck from a prior cycle. The 2021 footage and 2025 vendor clips are consistent with reuse, but they could equally be convenient illustrations. **I cannot prove the script is last year's.** What I *can* show is that it is **misaligned with the 2026 rubric in measurable ways** — and that is the actionable finding, regardless of its origin.

---

## 2. The assumptions embedded in the script

| # | Hidden assumption | Is it true for you? |
|---|---|---|
| A1 | A professional ROV is available | ❌ No. ~US$2,500; you have US$100 |
| A2 | The setting is **marine** (saltwater, ocean) | ❌ Cambodia's fisheries are overwhelmingly **inland freshwater** — Tonle Sap, Mekong |
| A3 | The application is **marine ranching (海洋牧场)** | ⚠️ A Chinese national strategy. Cambodia has essentially none |
| A4 | The four species are locally meaningful | ❌ Temperate North Pacific benthic species. Not found in Cambodian waters |
| A5 | The audience values technical showcase | ⚠️ Partly. The 2026 rubric weights application, conduct, teamwork and innovation at **40%** |
| A6 | The deliverable is a **presentation** | ❌ It is a **20-minute skill operation**, then a presentation |
| A7 | Accuracy and technology are what score | ❌ Accuracy scores nothing directly |

---

## 3. Where it misaligns with the actual 2026 rubric

I scored the original script against the official criteria. This is the core finding:

| Rubric category | Pts | Addressed in her script? |
|---|---|---|
| Operational Standardization | 10 | ⚠️ Partly — no timing, no procedure, no checklist |
| Skill Proficiency | 15 | ⚠️ Narration only; little actual *operation* |
| Task Difficulty | 15 | ⚠️ Challenges described, none **demonstrated** |
| Technological Advancement | 15 | ⚠️ YOLOv5/v8 presented as advancement in 2026 |
| On-site Presentation | 5 | ✅ Yes — this is what the script is |
| **Professional Ethics / IP** | **4** | ❌ **Absent** |
| Craftsmanship | 3 | ❌ Absent |
| **Safety Awareness** | **3** | ❌ **Absent** |
| **Practicality / national strategy** | **4** | ⚠️ Aimed at *Chinese* strategy, not the host region |
| **Cost-Effectiveness** | **3** | ❌ **Absent** |
| **Sustainability** | **3** | ❌ **Absent** |
| Teamwork (observed) | 10 | ⚠️ Roles exist; no visible collaboration |
| Innovation | 10 | ⚠️ Describes a standard pipeline |

> **Roughly 25–30 points of rubric surface are untouched by the original script** — not because it is a bad script, but because it was written to *explain a system*, and the 2026 rubric scores *how a team operates*.

**This is the innovation opportunity.** Not a better model. Better alignment.

---

## 4. The single biggest misalignment — and how to fix it without contradicting her

The script's application story is **Chinese marine ranching**. You will present it **in Phnom Penh**, to a **Southeast Asia division**, judged partly on *"alignment with national strategies… regional development, rural revitalization."*

### ❌ The wrong fix
Replace her marine framing with a Cambodian one. This would contradict your advisor, discard the Chinese context that the organisers (the PRC Ministry of Education) value, and be tactically stupid given **winners advance to the global finals in China**.

### ✅ The right fix — technology transfer framing

Present it as **Chinese marine technology adapted to Mekong freshwater aquaculture.** Keep every word of her technical content; add a transfer layer.

> *"This technology was developed for marine ranching, where China leads the world. We asked a different question: can it work in the water we actually have? Cambodia's fisheries are inland and highly turbid — the Tonle Sap in flood season is far harder than clear coastal water. Our contribution is adapting this proven approach to that harder case."*

**Why this is strictly better:**
- Flatters the origin technology instead of discarding it ✅
- Hits *regional development* and *rural revitalization* explicitly ✅
- Frames your constraint (turbid water) as a **harder technical problem** — Task Difficulty ✅
- Reads as China–ASEAN cooperation, which is precisely what this competition exists to promote ✅
- **Cannot be read as contradicting your advisor** ✅
- Travels well to the global finals in China ✅

---

## 5. On "Technological Advancement" — ✅ this problem dissolved on 13 September

**What this section used to say:** YOLOv5 is from 2020 and YOLOv8 from 2023, so neither is cutting-edge in 2026, and we would have to move the advancement claim somewhere else.

**That was based on a guess about which model she used, and the guess was wrong.** Her code arrived on 13 September. The model is **Mamba-YOLO** — a **state-space (SSM) architecture**, the 2024 research line currently displacing attention-based vision models — and the method is the subject of a **patent application filed in March 2025** (CNIPA 202510291747.5).

**So the strongest claim is now simply true.** This criterion is worth 15 points:

> *"We deploy a state-space vision model — Mamba-YOLO — in which the standard YOLOv8 feature blocks are replaced by Vision State-Space blocks. State-space models are a 2024 development that scales linearly rather than quadratically with sequence length, and the underlying method is the subject of a patent application filed in March 2025."*

Every clause there is checkable. **Rehearse it until it is comfortable** — a judge who knows the field will follow up, and one who does not will still register that you know what you are running.

⚠️ **Do not overreach.** The honest boundaries:
- **The model is not ours.** It is her group's, used with attribution. Say so in the same breath — it turns a possible criticism into 4 Professional Conduct points. → [`../advisor/PPTX_Translation_EN.md`](../advisor/PPTX_Translation_EN.md) slide 11.
- **The gain over plain YOLOv8 is +0.018 mAP50** (0.855 → 0.873 in her table). Real, modest. Not a breakthrough.
- **Quote 0.867** — the number in the training log we actually hold, not the 0.873 on her slide.

**Three claims that are still genuinely ours:**

1. **Unique counting with tracking** — ⭐ **stronger than when this was written.** Her shipped code has **no tracking at all**; its counts are per-frame, so one sea cucumber seen 100 times counts as 100. Adding tracking turns that into a real survey count. It is a demonstrable delta over what we were given, and we can show both side by side.
2. **Measured graceful-degradation characterisation** — the turbidity ladder in `reference/Core_Strategy_Data_Quality.md`. Almost nobody characterises their operating envelope. More scientifically mature than quoting an mAP.
3. **Ultra-low-cost deployment** — a US$30 acquisition platform against a US$2,500 ROV, with measured power draw. *"Cutting-edge"* legitimately includes cost-down engineering, and it serves Cost-Effectiveness and Sustainability directly.

**The honest framing, which is also the best one:** *"The detection model is state-of-the-art work from our advisor's research group, which we deploy with full attribution. Our own contribution is making it run on US$30 of hardware, measuring where it stops working, and turning its per-frame detections into real counts."*

That survives any follow-up question. Pretending the model is ours would not.

---

## 6. Where the script may be structurally overfitted to a presentation format

Her script is written as three monologues. The 2026 format is a **20-minute skill operation** followed by a presentation. Under *Skill Proficiency*, judges are watching you **do things**, not describe them.

| Script says | Operation should show |
|---|---|
| "Underwater environments are very complex" | **Stir clay into the tank.** Let them watch it degrade |
| "The robot can move underwater and collect information" | **Actually pilot it.** Narrate while your hands work |
| "After AI processing, the system detects targets" | **Run it live**, point at a box, read the confidence aloud |
| "Improves efficiency, reduces manual workload" | **Show the timer.** "Manual count: 4 minutes. Ours: 6 seconds" |
| "Applied in ecological monitoring" | **Show the count table** and what a decision-maker does with it |

**Rule: every claim in the script should be converted into something the judges watch happen.** That conversion is already applied in `Operation_Script_v2.docx`.

---

## 7. What to keep, unchanged

Being clear, because most of it is good:

- ✅ **The three roles** — hers to assign, and they map cleanly to the operation
- ✅ **The four species** — fixed by the dataset; changing them would waste your only labelled data
- ✅ **The four-stage workflow** — acquisition → processing → detection → analysis. Clean and correct
- ✅ **The underwater physics explanation** — absorption, scattering, low contrast. Accurate
- ✅ **The technical approach** — detection + tracking + counting. Right for the problem
- ✅ **The overall narrative arc** — problem → platform → algorithm → results → application

**The technical content is sound. It is the framing and the format that need work.**

---

## 8. What to raise with her, and how

Do **not** tell her the script is outdated. Ask questions that let her arrive there:

1. *"We noticed the rubric gives points for safety, cost, and intellectual property. Should we add these to the script?"*
2. *"Since the competition is in Cambodia, would it strengthen our application section to connect the technology to Cambodian aquaculture and the Tonle Sap?"*
3. *"The rubric mentions cutting-edge technology. Should we emphasise our turbidity augmentation and low-cost deployment as the innovation, since YOLOv5/v8 are established?"*
4. *"The format is a 20-minute operation. Should we convert parts of the script into live demonstrations rather than explanations?"*

Each of these is a genuine question, gives her ownership of the answer, and gets you what you need. Add them to Section B of `presentation/Open_Questions.md`.

---

## 9. Bottom line

| | |
|---|---|
| **Is the script overfitted?** | Its **framing** is — to a Chinese marine audience and a presentation format. Its **technical content** is not. |
| **Biggest risk** | Losing 25–30 rubric points in categories the script never addresses (IP, safety, cost, sustainability, teamwork, local relevance) |
| **Biggest opportunity** | **Technology-transfer framing**: Chinese marine technology adapted to Mekong freshwater aquaculture. Free, contradicts nobody, and directly targets the rubric |
| **What NOT to change** | Roles, species, workflow, technical approach, and the model stack |
| **Already actioned** | `Operation_Script_v2.docx` adds timing, safety, IP, cost, sustainability, Cambodia framing, visible hand-offs, a Q&A bank, and fallback scripts |
