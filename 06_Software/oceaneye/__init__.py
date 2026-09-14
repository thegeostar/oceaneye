"""OceanEye - underwater detection system, Group 22, RUPP.

The pieces, smallest to largest:

    config   device profiles (.toml) - change hardware here, not in code
    vision   enhancement, turbidity physics, drawing      (pure functions)
    capture  any source: USB camera, file, folder, stream, or synthetic
    detect   YOLO or mock detector, plus per-species counting
    session  CSV log, snapshots, recording, run summary
    runner   the run loop and the pre-flight check

Typical use:

    from oceaneye import config, runner
    cfg = config.load("profiles/endoscope.toml")
    runner.run(cfg, headless=True, max_frames=300)
"""

__version__ = "1.0.0"

from . import capture, config, detect, session, vision   # noqa: F401
