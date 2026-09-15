# OceanEye — Hardware Plan
### What to buy, what it costs, and what to do if you can't get a robot

> **← [README.md](../README.md) tells you what to do today. This page is the detail behind Day 1 step 1.**
>
> **Owner:** S1 · **Open it when:** you are about to spend money · **Done with it when:** the camera works and is logged in [Purchase_Log.md](Purchase_Log.md).

> ### 🔔 Confirmed 13 September — this plan is now the only plan
> Prof. Wang said the **hardware from China cannot arrive in time** and we must use our own. The question this whole document was hedging against — *"what if a real ROV shows up?"* — is closed. **Nobody is sending anything. Buy the camera.**
>
> One thing got easier, one got harder:
> - ✅ **The laptop has an RTX 5060 graphics card** — checked with `nvidia-smi`, not assumed. The AI has enough power to run right here. No cloud, no borrowed machine.
> - ⏰ **You have one day less.** Everything below is unchanged except urgency: if it cannot arrive by **Tue 16 Sept**, switch to Tier 0 and stop spending.

> ### 🔔 Superseded 15 September — the camera question is closed
> **We are using the lent Logitech 1080p USB webcam, filming through the glass from outside** (decision D4). It is not waterproof and nothing goes in the water any more.
>
> **Do not buy a camera.** Everything below about endoscopes, IP67 ratings, tethers and submersion testing is kept **only as a fallback** in case the Logitech fails. The still-current parts are the **torch, tank, lighting geometry and budget**.
>
> The buying list you actually work from is [`../team/S1_hardware.md`](../team/S1_hardware.md).

## 🏃 The 60-second version

1. ~~Buy a waterproof UVC USB endoscope camera~~ — **done, $0. The Logitech is lent and in hand.**
2. Buy a **separate torch** (~$8–15). This matters **more** than the camera. No longer needs to be waterproof — it lights the tank from outside.
3. Buy a **clear** tank, **real** creatures from the seafood market, 2 USB sticks. Core spend now: **~$47–81**.
4. **Real creatures, not toys** — the model was trained on real animals and may not see a plastic one at all.
5. **If the tank and creatures cannot be had by Tue 16 Sept → stop buying, switch to recorded video (Tier 0 below).**

Everything after this point is the *why* and the *where*. You only need it if something above goes wrong.

---

## The situation, stated plainly

Your advisor is in China and will only meet you online. She will **not** be physically present, including at the competition. You are likely buying your own equipment. You have **8 days** until 19 September.

The robot in her video is a commercial ROV: **8 thrusters, 12 kg thrust, 100 m depth rating.** Inspection-grade ROVs like that start around **US$2,500** and go up. You will not buy, ship, and learn to pilot one in 8 days.

**This is not a crisis. It is a scoping decision, and it needs to be made tomorrow.**

The rubric never says "commercial ROV." It says *Task Difficulty*, *Skill Proficiency*, and *Cost-Effectiveness*. A cheap platform you built yourself, operated fluently, with honest framing, can score **higher** than borrowed equipment you fumble — and it directly serves the *Cost-Effectiveness* and *Sustainability* criteria (6 points) that a $2,500 ROV actively undermines.

---

## Recommended: Tier 1 — the waterproof USB camera probe

**Buy this tomorrow. It solves two problems at once.**

A **waterproof USB endoscope / borescope camera** — the type sold for inspecting pipes and car engines.

| Spec to look for | Why |
|---|---|
| **IP67 or IP68 waterproof** | Must survive full submersion, not just splashes |
| **UVC compliant** (says "works with PC / Windows / no driver") | ⭐ **The critical one.** UVC means your laptop sees it as an ordinary webcam, so `cv2.VideoCapture(0)` just works. No SDK, no capture card, no driver hell. |
| **USB-A or USB-C wired** (not Wi-Fi) | Wi-Fi models drop frames and need an app. Wired is reliable and offline. |
| **720p or 1080p** | 720p is plenty — you run the model at 640px anyway |
| **Built-in adjustable LEDs** | Underwater lighting, exactly like the real ROV. Non-negotiable. |
| **3–10 m cable** | This is your tether |

**Cost: roughly US$15–40.** Search Lazada / Shopee Cambodia or the Phnom Penh electronics market for *"USB endoscope camera waterproof"* or *"borescope inspection camera USB"*.

### Why this is the right answer, not a compromise

1. **It kills your worst unknown.** `OPEN_QUESTIONS.md` Q2 asks how video gets from the robot into the laptop. With a UVC camera, the answer is "it's a webcam" — one line of code, no capture card, no shipping risk.
2. **It has a tether and lights** — the two things you narrate in the script.
3. **It's genuinely honest.** You present it as an *underwater image acquisition platform*, which is exactly what it is. You never call it something it isn't.
4. **It's Cost-Effectiveness evidence.** "Our entire acquisition system costs thirty dollars and runs on a laptop" is a *stronger* story for Cambodian aquaculture than a $2,500 imported ROV.
5. **It cannot leak onto your laptop.** It's designed for wet work.

### Verify it works the day it arrives

```python
import cv2
cap = cv2.VideoCapture(0)          # try 1, 2 if 0 is your built-in webcam
print("opened:", cap.isOpened())
ok, frame = cap.read()
print("frame:", ok, frame.shape if ok else None)
cv2.imwrite("probe_test.jpg", frame)
```

If that prints a shape, you are done — give that camera index to S2 for the app's Real-time Monitoring tab and the whole pipeline works.

> **On Linux, check it enumerates:** `v4l2-ctl --list-devices`. If the camera appears but OpenCV won't open it, try `cv2.VideoCapture(0, cv2.CAP_V4L2)`.

---

## The full bill of materials — ordered by effect on data quality

Priorities follow `reference/Core_Strategy_Data_Quality.md`. **Note item 2: an offset torch matters more than a better camera.** If budget forces a choice, take a 720p camera plus a separate torch over a 1080p camera with ring lights only. Lighting geometry beats resolution.

### Core — buy these (~US$62–96)

| # | Item | Purpose | Est. USD | When |
|---|---|---|---|---|
| 1 | **Waterproof UVC USB endoscope camera**, IP67, 720p+, 5–10 m cable | Acquisition + solves the video-into-laptop problem | 15–35 | 🔴 **Day 1** |
| 2 | **Waterproof LED torch** (dive light or IP68 work light) | ⭐ **Offset lighting — the single biggest image-quality win** | 8–15 | 🔴 **Day 1** |
| 3 | **Clear plastic box or small aquarium**, 40–60 cm | The demo tank. **Must be clear** so judges see the water state | 10–25 | 🔴 **Day 1** |
| 4 | **Plastic/rubber sea creature toys** — cucumber, urchin, scallop, starfish | Detection targets | 5–15 | 🔴 **Day 1** |
| 5 | **2 × USB flash drives** (16 GB+) | Backups of weights, code, footage | 8–12 | 🔴 **Day 1** |
| 6 | **Powered USB extension**, 3–5 m | Tank to laptop. Passive cable fails beyond ~5 m | 5–10 | 🟠 Day 1–2 |
| 7 | **Aquarium gravel / sand / small rocks** | Cluttered seabed → genuine Task Difficulty | 3–6 | 🟠 Day 2 |
| 8 | **Matte black plastic sheet or card** | Line the tank's far wall — kills reflections and glare | 2–4 | 🟠 Day 2 |
| 9 | **Powdered clay / kaolin / fine soil** | ⭐ The turbidity ladder demo | 1–2 | 🟠 Day 2 |
| 10 | **White translucent plastic** (milk jug, baking paper) | Light diffuser — removes hotspots and hard shadows | 1–2 | 🟠 Day 2 |
| 11 | **PVC pipe + fittings + zip ties** | Camera mount / "pilot" pole | 4–8 | 🟡 Day 2–3 |
| 12 | **Towels + plastic floor sheeting** | Safety (3 pts) and Craftsmanship (3 pts) | 3–5 | 🟠 Day 2 |
| 13 | **Silicone sealant / self-amalgamating tape** | Reinforce the cable entry | 3–5 | 🟡 Day 2 |

### Worth adding if budget allows

| Item | Purpose | Est. USD |
|---|---|---|
| **Second identical camera** | Redundancy. If the first floods on the 18th you still have a demo | 15–35 |
| Printed white/grey calibration card | Objective white balance; a professional Q&A answer | ~1 |
| Small submersible pump | Creates current, keeps sediment suspended | 8–12 |
| Cheap RC boat/submarine toy | Real movement — only if everything else already works | 30–60 |

**Realistic total: US$62–96 core**, leaving headroom in the US$100 budget for a spare camera or contingency.

---

## Where to buy in Phnom Penh

⚠️ **I cannot verify live stock or prices — treat this as a search strategy, not a guarantee.** Phone ahead before crossing the city.

### Buy in person wherever possible
**Same-day purchase eliminates your biggest risk, which is shipping time, not money.**

| Source | Good for |
|---|---|
| **Phsar Thmei (Central Market)** — electronics stalls | USB cameras, cables, flash drives, torches. Widest selection; bargain, and ask to test before paying |
| **Phsar Toul Tom Poung (Russian Market)** | Phone/computer accessories, cables, adapters |
| **Phsar Olympic** | Electronics, tools, hardware |
| **Aquarium / pet shops** | Tank, gravel, substrate, plants, small pump — also plausible model creatures |
| **Toy shops / party-supply stalls** | Plastic sea animals — cheapest route to targets |
| **Hardware / construction shops** | PVC, zip ties, sealant, black sheeting, clay |
| **Dive or fishing shops** | Waterproof torches, better quality than market ones |

### Online — only if it can arrive by Tuesday 16 September
- **Lazada Cambodia** — check the *estimated delivery date*, not the listing's shipping claim
- **Facebook Marketplace / Facebook shop groups** — very active in Cambodia, often next-day, and you can message the seller to confirm UVC support
- ❌ **Avoid Taobao/1688 agents** — typically 7–14 days. Too slow.

### Search terms
> `USB endoscope camera waterproof` · `borescope inspection camera USB` · `endoscope 内窥镜 USB 防水`

---

## ⚠️ Verify UVC before you pay — this is what can waste your budget

Many cheap "endoscope" cameras are **Wi-Fi or Android-OTG only** and will **not** work as a plain webcam.

**Require:**
- ✅ *"Works with PC / Windows / laptop"*, *"no driver needed"*, or *"UVC"*
- ✅ A **USB-A or USB-C plug** — not a Wi-Fi box, not a phone-only OTG dongle
- ❌ If the listing only ever shows a phone app → **wrong product**

**Test it in the shop.** Plug into a laptop; if the built-in Camera app shows a picture, it is UVC and OpenCV will open it.

**Then within 10 minutes of getting home**, run the probe test above, and immediately do the settings-lock test in `reference/Core_Strategy_Data_Quality.md` §3.8 — especially confirming **≥25 fps with MJPG**, because many UVC cameras default to raw YUYV and crawl at 5 fps.

**Test waterproofing on Day 1, not Day 5:** submerge the probe head in a glass of water for 10 minutes with nothing valuable nearby. Check for fogging or ingress.

---

## Gaps the advisor might fill

Ask, but do not wait (`presentation/Open_Questions.md` Section A):

| Gap | If she provides it |
|---|---|
| A real ROV at the venue | Everything changes — keep the tank rig as backup regardless |
| **Trained weights + code** | ⭐ Highest-value item she can give. Costs her nothing, saves you a day |
| Budget approval | Buys the spare camera |
| Her own tank footage / dataset | Reduces your data-collection load |
| Confirmation a simplified platform is acceptable | Removes your single largest project risk |

---

## Record everything you buy

Log every purchase in **`hardware/Purchase_Log.md`** — item, price, shop, date. You need it for the cost-effectiveness slide (3 rubric points), and if a part fails you need to know where to get another one fast.

### 🎯 The turbidity trick — your best demo moment for $2

Fill the tank with clean water and run detection. Then **stir in a spoon of clay or soil live in front of the judges**, and run it again.

You are demonstrating, in real time, the exact physical problem your whole project is about — and showing that your enhancement pipeline still works when the water degrades. It costs almost nothing, it is visually unmistakable, and **no other team will do it.**

This is the single highest-value item in this document. Practise it: too much clay and you see nothing at all, which is a different (and less useful) demo.

---

## Tier 2 — only if Tier 1 works and you have spare time

Add **movement** so "robot operation" is more literal:

- A cheap RC toy submarine or RC boat ($30–60) with the camera cable-tied to it
- Or a small bilge pump / DC motor on a PVC frame for basic thrust ($20–40)
- Or — simplest and perfectly defensible — mount the camera on a pole and move it manually as a **"manually positioned survey probe"**

**Do not attempt a full DIY ROV build.** A school-club ROV is a $100–150 build and a multi-week project. You have 5 working days and an AI system to finish. Moving parts underwater will consume all of it.

---

## Tier 0 — the fallback if nothing arrives in time

Pre-recorded footage only. The app's **Video Detection** tab runs on an uploaded file exactly as the camera tab runs on a camera — same model, same boxes. Say *"this is our recorded survey footage"* and nothing is lost but the live moment.

**Sources:** her reference videos, public underwater footage, DUO/Brackish dataset images played as a sequence, or footage you shoot with a phone in a waterproof bag.

This still earns most points — but you lose the live acquisition story, and *Task Difficulty* suffers. **Treat Tier 0 as insurance, not the plan.** Build it regardless, because it is also your Day 3 backup recording.

---

## Decision deadline

> **By end of Day 1 (Sat 12 Sept), Student 1 must be able to answer:**
> 1. Has the camera been ordered, and what is its promised delivery date?
> 2. If it cannot arrive by Monday 15 Sept, are we going Tier 0?
> 3. Has Prof. Wang approved a simplified acquisition platform? *(see `OPEN_QUESTIONS.md` question A1 — this is the single most important question you will ask her)*

**If the camera cannot arrive by Tuesday 16 September, switch to Tier 0 and stop spending time on hardware.** A rehearsed video demo beats a half-working camera you plugged in for the first time the night before.

---

## Safety — worth 3 rubric points, and genuinely important

Water and electricity. Take this seriously, then *say it out loud during the demo*.

- **No mains-powered device within reach of the water.** Laptop on battery during the demo if you can.
- **The camera is the only thing that goes in the water.** Never the laptop, never a power adapter.
- **Dry the floor. Keep a towel visible.** Judges notice.
- **Cable management** — tape the USB run down so nobody trips.
- **Check the probe seal before every submersion**, and say so as part of your pre-flight checklist.
- If you add any powered thruster: **battery only, never mains.**

The script (`OceanEye_Operation_Script_v2.docx`, Student 1, 01:00–01:30) has the spoken safety check. Do not skip it — it is 3 points for 30 seconds of talking.
