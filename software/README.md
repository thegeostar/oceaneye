# Software — OceanEye

> **← [README.md](../README.md)** · **Owner: S2**

Everything that runs on stage lives in **`advisor_code/`**, and it has one page:

## 👉 **[advisor_code/HOW_TO_RUN.md](advisor_code/HOW_TO_RUN.md)**

That page covers the environment trap, the install, the acceptance test, the web app, the camera, what to do when something fails, and why it takes 1.1 s per image.

---

### What used to be here

A second, independent pipeline of ours (`oceaneye/`, `oceaneye_demo.py`, `profiles/`, `train_oceaneye.py`) built in the days when the advisor's model would not run. Its detector was a mock colour-blob stand-in, so it could never have gone on stage — it existed to keep the project moving while the real model was blocked.

**Retired 15 September 2026 (decision D18)**, once the real model reached 1.12 s/image with a smooth live camera feed. Keeping two codebases was costing navigation, not buying insurance. The files were deleted from disk the same day.

It is not lost — it is in git history:

```bash
git log --oneline -- software/oceaneye/          # find the last commit that had it
git show <commit>:software/oceaneye/vision.py    # read a file
git checkout <commit> -- software/oceaneye/      # bring it all back
```

The one piece worth keeping came across already: the CLAHE contrast step now lives in `app/predict_video.py` as `enhance()`. Its gray-world white-balance partner was measured and found worse at every turbidity level, so it was deliberately left behind.
