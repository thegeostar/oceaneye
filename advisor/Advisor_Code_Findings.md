# What the advisor sent, and what of it we can actually run

← [README.md](../README.md) · **Owner: S2** · *Rewritten 15 Sept 2026, after the report and thesis arrived.*

> **TL;DR**
> - The model **runs**, 1.12 s/image, and reproduces the author's own published detections **byte for byte**.
> - The deck describes a **two-stage system**. We hold **one stage**, and not the full version of it — §3.
> - **Quote 0.867.** It is the only accuracy figure we hold a file for.
> - Their ONNX export is broken (tested) and their prebuilt CUDA operator cannot load on this GPU (tested). Both are closed.

Everything marked ✅ was run and observed on this laptop.

---

## 1. Inventory

| Item | Where | State |
|---|---|---|
| Trained weights | `software/advisor_code/output_dir/mscoco/mambayolo_n/weights/best.pt`, 139 MB | ✅ **runs** |
| Flask app | `software/advisor_code/app/` | ✅ runs, UI fully English |
| Cambodia report deck, 18 slides, bilingual | `advisor/OceanEye-Cambodia-Report.pdf` | ✅ read — §3 |
| Li Kaixuan's thesis, 83 pp, Chinese | `advisor/【7】…研究1.pdf` | ✅ read — §3 |
| Their 45-s test footage | `advisor/videos/` | ✅ 1280×720, 10 fps |
| URPC config | `software/advisor_code/URPC/URPC.yaml` | ✅ 4 classes, correct order |
| Original drop (866 files) | deleted 15 Sept · `advisor/Original_Drop_MANIFEST.txt` records every path + SHA256 | — |
| The training images | — | ❌ **never sent.** We can quote their numbers, never reproduce them |
| ONNX export | deleted | ❌ broken — §5 |

**Classes, in the order the model outputs them:**
`0 holothurian (sea cucumber) · 1 echinus (sea urchin) · 2 starfish · 3 scallop`

---

## 2. What the model actually is

**Mamba-YOLO-L** — YOLOv8's detection head and PANet neck with every `C2f` block replaced by a `VSSBlock` (Vision State-Space / Mamba). Confirmed from `args.yaml`: `Mamba-YOLO-L.yaml`, data `URPC.yaml`, 640×640, batch 6, 300 epochs requested.

**Say on stage:** *"Mamba-YOLO — a YOLOv8 architecture in which the feature blocks are replaced with Mamba state-space blocks."* True, matches the code, matches the patent title.

---

## 3. ⚠️ The deck describes more than we have

The thesis proposes two contributions and the deck presents both as one pipeline. Verified by grep against our copy:

| Their claim | In our code? |
|---|---|
| **Stage 1 — FSCIN** super-resolution: SFAM module (FFT + dual-branch Swin Transformer on amplitude and phase), texture-structure joint loss. 30.04 dB PSNR on USR-248 ×2, 0.55 M params | ❌ **nothing.** No FSCIN, no SFAM, no super-resolution of any kind |
| **Stage 2 — "improved YOLOv8"**: C2f replaced by FFEM = **CAEM** (channel-spatial attention) + **VSSM** (Mamba) + **MCFM** (multi-scale cross fusion) | ⚠️ **VSSM only.** No CAEM, no MCFM, no FFEM anywhere in `ultralytics/` |

So "improved YOLOv8" in the thesis and "Mamba-YOLO-L" in our folder are **related but not the same model**. Ours has one of their three modules.

### Their numbers, and why ours differs

Thesis Table 4.2, URPC2021 — **theirs, cite them, do not claim them:**

| Model | mAP50 | mAP50-95 | APs |
|---|---|---|---|
| YOLOv8 baseline | 0.855 | 0.516 | 0.166 |
| Improved YOLOv8 (CAEM+VSSM+MCFM) | **0.873** | 0.530 | 0.177 |

Thesis §4.5, the cascade — ×4 bicubic-downsampled input, **their measurement, on degraded images they created:**

| Input | Recall | mAP@0.5 |
|---|---|---|
| Low-resolution | 71.4 | 76.2 |
| Original resolution | 77.9 | 83.2 |
| FSCIN-restored | **82.5** | **87.7** |

> 🔴 **Our 0.867 sits between their baseline 0.855 and their improved 0.873.** Never let those three numbers be conflated in a slide or an answer. Ours is a different run of a different model.

**What we quote:** `mAP50 = 0.867`, best epoch 135 of `results.csv` — a file we hold and can show a judge. Final epoch 235 reads 0.856. If asked about 0.873: *"that is the published figure for the authors' full three-module model; the weights we were given measure 0.867."*

**Q&A gold from §4.5:** *"does image enhancement actually help detection, or only human viewing?"* → their own experiment answers it: mAP 76.2 → 87.7 on degraded input. Restoration recovers discriminative features, it is not beautification. Cite it as theirs.

---

## 4. What the deck gives S3

`OceanEye-Cambodia-Report.pdf` is **bilingual** — the long-promised English deck, effectively. Six chapters: Cambodia policy → pain points → FSCIN → detection → application → innovations & IP.

Usable directly: Pentagonal Strategy Phase I · Digital Economy and Society Policy Framework 2021–2035 · Circular Strategy on Environment 2023–2028 (CLEAN/GREEN/SUSTAINABLE) · **516 community fisheries (472 freshwater / 44 marine)** · four Cambodian scenarios incl. Tonlé Sap aquaculture · slide 17's award, copyright and patent certificates.

⚠️ Slides 7, 9, 10 and 14 are the FSCIN stage. **Present them as the research behind the system, not as our pipeline.** The part dividers say "Presenter A" and "Presenter B" — we have three speakers.

---

## 5. Two closed dead ends — do not reopen

**ONNX export.** ✅ Tested: loads, correct output shape, ~550 ms/frame, and the highest confidence over all 8,400 candidate boxes was **0.000** on four images, including one their `.pt` detects at 0.78–0.83. The custom Mamba operator does not survive export.

**The prebuilt CUDA operator.** ✅ Tested: the shipped `.so` files are built against torch 2.2 + CUDA 11; the RTX 5060 is sm_120 and needs torch ≥2.7 + CUDA 12.8, and all 39 libtorch symbols the `.so` imports were removed in between (checked with `nm`). **Replaced by a pure-PyTorch reimplementation** in `selective_scan_fallback.py` — same maths, same weights, verified two ways: against a naive loop (3e-06) and against their published result on `000013.jpg` (byte-identical). This is real engineering work and a strong answer to a judge.

---

## 6. What we changed, and the three things never to claim

Our copy is `software/advisor_code/`. Every edit is commented `# OceanEye:` — `grep -rn "OceanEye:" software/advisor_code/`. Hardcoded `E:/URPC/…` Windows paths, a font bug that capped the feed at 5 fps, a per-image reload of the 139 MB checkpoint, and a JS error that silently disabled half the web page are all fixed. Detail: [HOW_TO_RUN.md](../software/advisor_code/HOW_TO_RUN.md) §8.

Never claim on stage:

1. **Login is a placeholder.** Any username and password are accepted; `user.py` is never imported. Not authentication.
2. **There is no tracking.** Counts are per-frame — one animal visible for 100 frames counts 100 times.
3. **"Real-time Monitoring" originally played a recorded file** while labelled real-time. Fixed; a recorded fallback is opt-in and stamped on screen. Professional Conduct is 10 points.

---

## 7. Still worth asking them

1. 🔴 **Written permission** to demonstrate the model and footage publicly with attribution. Worth real rubric points; not yet in hand.
2. The URPC2021 dataset or the link — only to show a labelled sample, not to retrain.
3. Available online 20–22 Sept?

*Answered by the documents, do not ask again:* their environment (thesis Table 4.1 — Python 3.10.19, PyTorch 2.1.0, CUDA 11.8, Ultralytics 8.4.24), the dataset identity (URPC2021), the English deck (it is bilingual), and whether enhancement helps detection (§4.5).
