← [START_HERE.md](../START_HERE.md)

# S1 — Hardware, tank, footage, packing

**Today is Monday 14 September. The competition is Sun 20 – Tue 22 September. You have 5 working days: Mon 14 → Fri 18. Sat 19 is travel/rest.**

## What you own

1. **Buying** the camera, torch, tank and props — budget ceiling **US$100 total**, log every item in [`../05_Hardware/Purchase_Log.md`](../05_Hardware/Purchase_Log.md).
2. **Building** the tank rig and the lighting, **filming the backup video**, and packing the equipment box.
3. **Stage minutes 00:00–06:30** — the robot and the safety lines (safety is 3 rubric points for 30 seconds of talking).

---

## 🔴 DO THIS FIRST TODAY — buy the camera, in person, before anything else

Nothing has been bought. Everything else on this page waits on this. Go to a market today; do not order online unless it can arrive **by Wed 16 Sept**.

Buy a **waterproof USB endoscope camera** — a small camera on a long cable, sold for looking inside pipes and car engines. **US$15–35.**

The listing must say one of: **"UVC"**, **"works with PC / Windows"**, **"no driver needed"**.
*UVC = the standard that makes the laptop treat it as an ordinary webcam. No UVC, no demo — our code cannot open it at all.*

- ❌ Listing only shows a **phone app** → wrong product, do not buy.
- ❌ **Wi-Fi** camera → wrong product. It must be a USB-A or USB-C plug.
- ✅ IP67/IP68 (fully waterproof when submerged), 720p is plenty, 3–10 m cable (that cable is our "tether").
- ✅ **Test it in the shop before you pay.** Plug into a laptop; if the Camera app shows a picture, it is UVC.

**Where:** Phsar Thmei (Central Market) electronics stalls — widest selection, bargain and test. Also Phsar Toul Tom Poung (Russian Market) and Phsar Olympic. Aquarium/pet shops for tank and gravel. Toy or party stalls for the creatures. Dive/fishing shops for a better torch. Hardware shops for PVC, zip ties, black sheeting, clay. ⚠️ Stock and prices are **unverified** — phone ahead before crossing the city.

---

## Mon 14 September — buy everything, test the camera wet

- [ ] Waterproof **UVC USB endoscope camera** — $15–35
- [ ] **Waterproof LED torch** — $8–15. ⭐ This matters **more** than a better camera. Given the choice, take a 720p camera plus a torch over a 1080p camera with ring lights only.
- [ ] **Clear** plastic box or small aquarium, 40–60 cm — $10–25. Must be see-through or the judges cannot see the water going murky.
- [ ] Plastic toy **sea cucumber, sea urchin, scallop, starfish** — $5–15
- [ ] **2 × USB flash drives**, 16 GB+ — $8–12
- [ ] Powered USB extension 3–5 m $5–10 (a passive cable fails beyond ~5 m) · gravel/sand $3–6 · matte black sheet or card $2–4 · powdered clay or fine soil $1–2 · white translucent plastic for a diffuser (milk jug, baking paper) $1–2 · PVC pipe + zip ties $4–8 · towels + floor sheeting $3–5
- [ ] **Write every item, price, shop and date in [`../05_Hardware/Purchase_Log.md`](../05_Hardware/Purchase_Log.md)** — the cost slide is 3 points. Core spend should land at **$62–96** inside the **$100** ceiling.
- [ ] **Submersion test today, not Friday:** hold the probe head in a glass of water 10 minutes, nothing valuable nearby. Check for fogging or water inside.
- [ ] Hand the camera to S2 and confirm the laptop sees it: `python oceaneye_demo.py --source 0` (try `1` or `2` if `0` is the built-in webcam).

## Tue 15 September — build the tank and the lighting

- [ ] Line the **far wall and floor with matte black** card or plastic. Fill with water, add gravel and the four creatures.
- [ ] Mount the camera on the PVC pole with zip ties so it is **rigid** — motion blur kills small-target detection.
- [ ] **Turn the camera's own ring LEDs down or off.** Zip-tie the torch **20–40 cm to the side**, angled onto the creatures. Tape the white translucent plastic over the torch as a diffuser.
- [ ] Set the camera **10–25 cm** from the creatures. Find the distance where **3–6 targets** are visible and stop there.
- [ ] With S2, **lock the camera settings** (see below) and copy the numbers into the Purchase_Log table.
- [ ] Film **2–3 minutes of footage** of the rig working. This is raw material for S2 and your insurance.
- [ ] Read your script minutes 00:00–06:30 aloud once, with a timer.

## Wed 16 September — 🎬 record the backup video, rehearse

- [ ] **Record one perfect full run, start to finish.** This is what you play if everything dies on stage. Desktop **and** USB stick.
- [ ] Rehearse the **turbidity ladder**: stir one spoon of clay in live, then two, then three. ⚠️ Practise the amount — too much clay and nothing is visible, which is a boring demo. Say out loud where it stops working.
- [ ] Practise the **pre-flight checklist** out loud (it is in `04_Presentation/Operation_Script_v2.docx`): seal checked, lens wiped, floor dry, laptop on battery.
- [ ] First full three-person run-through, untimed.

## Thu 17 September — pack the box, rehearse timed

- [ ] **Pack the equipment box against a written list** and tick every item: camera, spare cable, torch + spare batteries, tank, gravel, 4 creatures, clay in a sealed bag, black lining, diffuser, PVC + zip ties, USB extension, 2 USB sticks, towels, floor sheeting, dish soap, laptop **charger**.
- [ ] Unpack it, set the whole rig up from the box, timed, then repack.
- [ ] Two **timed** run-throughs. Record one on a phone, watch it back.

## Fri 18 September — nothing new

- [ ] Rehearse with **no notes in your hands**. Practise the hand-off line to S2.
- [ ] Confirm the backup recording **opens** from the USB stick on the stage laptop, then final pack.
- [ ] Stop on a good run. Sleep matters more than one more rehearsal.

---

## The 4 things that actually matter

**1. Put the light to the side.** ⭐ The single biggest win of your week. Ring lights around the lens are the worst possible geometry: every speck of dirt in the water bounces that light straight back into the lens, giving glowing white specks and fog — *backscatter*. Ring LEDs off, torch **20–40 cm to the side**. Cost: one zip tie. Almost no student team knows this.

**2. Get close.** Work at **10–25 cm**, not a metre. Water eats light exponentially with distance, so halving the distance beats any software anyone could write.

**3. Matte black far wall.** ~$3 of card kills room reflections and glass glare.

**4. Wipe the lens before every single run.** Rub a trace of **dish soap** on the port — a diver's trick that stops bubbles sticking. It is on the pre-flight checklist.

### Lock the camera, then write the numbers down

A webcam left alone keeps re-adjusting its own brightness and colour, so detections flicker and no two runs match — that costs *Operational Standardization* points directly.

```bash
v4l2-ctl --list-devices                    # find the camera
v4l2-ctl -d /dev/video0 --list-ctrls       # see what it supports
v4l2-ctl -d /dev/video0 -c auto_exposure=1 -c exposure_time_absolute=150 \
                        -c white_balance_automatic=0 -c gain=0
```

Also force **MJPG** (a compressed format — many UVC cameras default to raw YUYV and crawl at ~5 fps) and confirm **≥25 fps**. If the picture is dark, **add light — never raise gain**, because gain multiplies noise. Copy exposure, white balance, gain, resolution, torch distance and camera-to-subject distance into the Purchase_Log table — rediscovering them under pressure on stage day is a nightmare.

## Hard deadlines, and what to do when you miss them

| Deadline | If you miss it |
|---|---|
| **Mon 14, end of day** — camera bought and it opens on the laptop | Buy tomorrow morning only. Tell the team in chat tonight. |
| **Wed 16, 14:00** — camera works in the tank, end to end | 🔴 **Switch to Tier 0 permanently: recorded video only.** Stop spending on hardware. A rehearsed video demo beats a half-working camera. Decide once, do not look back — deciding late is what kills teams, not deciding wrong. |
| **Wed 16, end of day** — backup video recorded and it plays | Record it Thursday morning before anything else. You do not travel without it. |
| **Thu 17** — box packed and checked | Pack Friday morning, then set up once from the box. |

**On stage, if the camera dies:** say *"We will continue with our recorded survey data, collected with this same platform."* Then open the backup footage. Never apologise twice, never go silent, never blame the equipment — judges score the recovery.

⚠️ **Safety, spoken aloud in the demo (3 points):** no mains-powered device within reach of the water · the camera is the only thing that goes in · laptop on battery · floor dry and a towel visible · USB cable taped down so nobody trips · seal checked before every submersion.
