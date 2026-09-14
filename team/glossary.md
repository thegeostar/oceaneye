# Word list — every technical term, in plain English

← [README.md](../README.md) · **Don't read this. Search it when you get lost.**

## The AI

| Word | Plain English | Why it matters to us |
|---|---|---|
| **Model** | A file that learned a pattern from examples. Nobody wrote its rules by hand. | The thing that finds the creatures |
| **YOLO** | Our detector family. "You Only Look Once" — one pass per picture, so it's fast enough for live video. | The whole demo |
| **Mamba** | A newer way for an AI to look at a picture: it sweeps across keeping a running summary instead of comparing every part to every other part. Cheaper, and better at faint low-contrast things — which is murky water exactly. | This is what her model uses |
| **Mamba-YOLO** | What we actually run: YOLOv8's skeleton with Mamba blocks inside. | Say **this** name on stage. Not YOLOv5, not plain YOLOv8 |
| **`selective_scan`** | The small hand-written GPU program that does the Mamba sweep. Written in CUDA, so it must be compiled for your exact Python version and graphics card. | The one thing standing between us and a working demo |
| **Weights** / `.pt` | The file holding everything the AI learned. **This file IS the trained AI.** | `best.pt`, 139 MB. Lose it and you lose the week. Back it up 3× |
| **Detection** | Finding *where* a thing is and *what* it is. | "Sea urchin, top-left, 87% sure" |
| **Bounding box** | The rectangle drawn around each creature. | What judges actually see |
| **Confidence** | How sure the AI is, 0 to 1. | Read one aloud on stage — it proves the system is live |
| **Threshold** (`--conf`) | Minimum confidence before a box is drawn. Higher = fewer but surer boxes. | Drop it to 0.20 if nothing shows on stage |
| **Class** | One category it can recognise. We have exactly 4. | Order: holothurian, echinus, starfish, scallop |
| **mAP50** | A 0-to-1 accuracy score. | **Ours is 0.867.** Never say 0.873 |
| **Inference** | *Using* a trained AI. The opposite of training. | What happens on stage. No training at the venue |
| **Tracking** | Giving each creature a number that follows it frame to frame. | Without it, one cucumber seen 100× counts as 100 |
| **ONNX** | A portable model format that runs without PyTorch. | Hers is **broken** — detects nothing. Do not build on it |

## Camera and water

| Word | Plain English | Why it matters to us |
|---|---|---|
| **UVC** | A standard that makes a USB camera work as a plain webcam, no driver. | **No UVC = our code cannot open it.** Check before paying |
| **IP67** | Fully waterproof when submerged. | It's going in water |
| **Backscatter** | Glowing specks and fog, caused by light bouncing off dirt in the water straight back into a lens sitting right next to that light. | Why the torch goes 20–40 cm to the **side**. Biggest cheap win we have |
| **Turbidity** | How cloudy the water is. | Our signature demo — stir clay in live |
| **Exposure** | How long the sensor collects light per frame. | **Lock it** or brightness drifts between frames |
| **White balance** | What the camera thinks "white" is. | **Lock it** or colours drift and detections flicker |
| **Gain** | Electronic brightness boost — also boosts noise. | Keep at 0. Add real light instead |
| **MJPG** | A compressed camera format. | Many cameras default to a raw format stuck at 5 fps. Force MJPG for 30 |
| **FPS** | Pictures processed per second. Above 20 = real-time. | Show it on screen; judges will ask |
| **Enhancement** | Software that fixes underwater colour and contrast. It **redistributes** detail already there — it cannot invent detail the camera never recorded. | Great for humans. Be honest that it helps the AI less |
| **CLAHE** | Contrast boost applied tile-by-tile, so dark corners get fixed separately from the bright middle. | The before/after slide |

## Kit and process

| Word | Plain English | Why it matters to us |
|---|---|---|
| **Endoscope / borescope** | A small camera on a long cable, sold for inspecting pipes and engines. | This is our "robot" |
| **ROV** | A real underwater robot with thrusters. $2,500+. | We are **not** using one. A $30 camera is a *better* story for Cambodia, not a worse one |
| **Tether** | The cable from the underwater camera to the surface. | Ours is the USB cable. Mention it |
| **`.venv`** | A private folder holding this project's Python so it can't clash with the rest of the laptop. | **Never move it** — moving breaks it |
| **Offline** | Runs with no internet. | Hard requirement. Test with Wi-Fi **off** |
| **Cold boot** | Full shutdown, restart, then run. | The test that catches what nothing else catches |
| **Domain shift** | Training on one kind of image and showing it a different kind — accuracy silently collapses. | Use the same image processing in training **and** on stage |
