← [README.md](../README.md)

# S1 — Hardware, tank, footage, packing

**Today is Tuesday 15 September. The competition is Sun 20 – Tue 22 September. You have 4 working days: Tue 15 → Fri 18. Sat 19 is travel/rest.**

## What you own

1. **Buying** the camera, torch, tank and props — budget ceiling **US$100 total**, log every item in [`../hardware/Purchase_Log.md`](../hardware/Purchase_Log.md).
2. **Building** the tank rig and the lighting, **filming the backup video**, and packing the equipment box.
3. **Stage minutes 00:00–06:30** — the robot and the safety lines (safety is 3 rubric points for 30 seconds of talking).

---

## ✅ The camera is solved — do not buy one

We are using the **lent Logitech 1080p USB webcam**. It is already UVC, already 1080p, and costs nothing.

**It is not waterproof and it never goes in the water.** It sits *outside* the tank and films **through the glass wall**. This is the whole plan now — no pole, no tether, no submersion test, nothing to flood.

> The old plan (a waterproof endoscope on a pole, in the water) is **retired** — decision D4. The endoscope buying guide is still in [`../hardware/Hardware_Plan.md`](../hardware/Hardware_Plan.md) as a fallback if the Logitech dies, but do not spend money on it now.

## 🔴 DO THIS FIRST TODAY — the tank and the four creatures

That is now the only thing blocking the whole team. S2 cannot test the AI on anything real until these exist.

- **A clear glass tank**, 40–60 cm. Must be see-through or the judges cannot watch the water go murky.
- **Four REAL creatures: sea cucumber, sea urchin, scallop, starfish.** Seafood market or a dried-goods shop. **Not toys.**
  > ⚠️ **Why real matters.** The AI was trained on photographs of real animals on a real seabed. A plastic toy is the wrong colour, the wrong texture and the wrong shape, and the model may simply not see it — or name it wrong, on stage, in front of a judge. Dried is fine. Plastic is a gamble we do not need to take.

**Where:** Aquarium/pet shops for the tank and gravel. **Seafood market or dried-goods stalls for the four creatures.** Dive/fishing shops for a torch. Hardware shops for PVC, zip ties, black sheeting, clay. ⚠️ Stock and prices are **unverified** — phone ahead before crossing the city.

**Hand them to S2 the moment you have them.** The first question is whether the AI sees them at all, and nobody can answer it until then.

---

## Mon 14 September — buy everything, test the camera wet

- [x] ~~Waterproof UVC USB endoscope camera~~ — **not needed, the Logitech is lent and in hand. $0.**
- [ ] **LED torch** — $8–15. ⭐ Lighting matters **more** than the camera. It does not need to be waterproof any more: it lights the tank from outside, like the camera.
- [ ] **Clear glass tank or plastic box**, 40–60 cm — $10–25. Must be see-through or the judges cannot see the water going murky.
- [ ] **REAL sea cucumber, sea urchin, scallop, starfish** — seafood or dried-goods market, $5–15. **Not plastic toys** — see the box above.
- [ ] **2 × USB flash drives**, 16 GB+ — $8–12
- [ ] Powered USB extension 3–5 m $5–10 (a passive cable fails beyond ~5 m) · gravel/sand $3–6 · matte black sheet or card $2–4 · powdered clay or fine soil $1–2 · white translucent plastic for a diffuser (milk jug, baking paper) $1–2 · PVC pipe + zip ties $4–8 · towels + floor sheeting $3–5
- [ ] **Write every item, price, shop and date in [`../hardware/Purchase_Log.md`](../hardware/Purchase_Log.md)** — the cost slide is 3 points. Core spend should land at **$62–96** inside the **$100** ceiling.
- [x] ~~Submersion test~~ — **not applicable.** Nothing we own goes in the water. Keep the webcam and every cable well clear of spills.
- [ ] Hand the camera to S2 and confirm Linux sees it: `v4l2-ctl --list-devices`. Note the number in `/dev/videoN` — the built-in webcam is usually `0`, so the Logitech is probably `1` or `2`. That number goes into the app's Real-time Monitoring tab.

## Tue 15 September — build the tank and the lighting

- [ ] Line the **far wall and floor with matte black** card or plastic. Fill with water, add gravel and the four creatures.
- [ ] Stand the webcam **against the outside of the glass**, lens as close to the glass as it will go. Fix it so it is **rigid** — motion blur kills small-target detection. Shade the front of it: the room reflects in the glass straight back into the lens, and that is the number-one reason a tank shot comes out unusable.
- [ ] **Light from the side, never from beside the lens.** Put the torch **20–40 cm to the side**, angled onto the creatures, and tape the white translucent plastic over it as a diffuser. Front light bounces off the glass and blinds the shot.
- [ ] Set the camera **10–25 cm** from the creatures. Find the distance where **3–6 targets** are visible and stop there.
- [ ] With S2, **lock the camera settings** (see below) and copy the numbers into the Purchase_Log table.
- [ ] Film **2–3 minutes of footage** of the rig working. This is raw material for S2 and your insurance.
- [ ] Read your script minutes 00:00–06:30 aloud once, with a timer.

## Wed 16 September — 🎬 record the backup video, rehearse

- [ ] **Record one perfect full run, start to finish.** This is what you play if everything dies on stage. Desktop **and** USB stick.
- [ ] Rehearse the **turbidity ladder**: stir one spoon of clay in live, then two, then three. ⚠️ Practise the amount — too much clay and nothing is visible, which is a boring demo. Say out loud where it stops working.
- [ ] Practise the **pre-flight checklist** out loud (it is in `presentation/Operation_Script_v2.docx`): seal checked, lens wiped, floor dry, laptop on battery.
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
