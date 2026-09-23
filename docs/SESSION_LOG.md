# Session log

One entry per session, newest first. Written on "save progress". Read the latest entry at session start.

## 2026-09-22

### Done
- Session start review of docs and repo state.
- Added the "Save progress" procedure to `CLAUDE.md` and created this log.
- Added the list of paths `.gitignore` must cover to Block C in `docs/WORK_INSTRUCTIONS.md`.

- Created `docs/VISION.md` recording Justin's art direction (West of Loathing, Don't Starve Together, Deadly Days: Roadtrip, Octopath Traveler 0, Paper Mario).
- Switched the Unity template from Universal 2D to Universal 3D in `CLAUDE.md`, `docs/ROADMAP.md`, `docs/WORK_INSTRUCTIONS.md`, `docs/ARCHITECTURE.md`.

### Decisions
- "Save progress" and similar phrases now trigger a full write-up across the living docs. Procedure lives in `CLAUDE.md`.
- Unity template is Universal 3D (URP 3D). Reason: the references mostly put 2D sprites in a 3D world with lighting, shadows, and depth of field. 3D also covers flat 2D, and switching later is costly.

- Block B done. `unity/client` created on `6000.0.84f1` from Universal 3D, URP 17.0.4. First attempt used editor 2022.3.62f1 and the Built-In 3D template, so it was deleted and redone.
- Kept the project name `client` even though Justin has another Unity project named `client` elsewhere. Hub tracks projects by path, so it is harmless.
- Wrote Block C with the exact `.gitignore` patterns.

### Where we stopped
- M0 Tooling. Blocks A and B done. Block C (git) not started.
- Nothing committed since `553a67d Initial commit`. `CLAUDE.md`, `.claude/`, `docs/`, `sim/` are untracked. `README.md` is modified.

### Next
- Block C step 1: type the `.gitignore`, then first commit.

## 2026-09-21

Reconstructed from `docs/WORK_INSTRUCTIONS.md` "Done" section.

### Done
- Repo restructure. Promoted the template from `instructions/labsim-template/labsim/` to the repo root and deleted `instructions/`.
- Block A (Python). `.venv` at the repo root, `sim/pyproject.toml`, empty `__init__.py` files in `sim/labsim` and `sim/tests`, `pip install -e "sim[dev]"`. Checkpoint passed.

### Deviations from the instructions
- `websockets` is a runtime dependency rather than a `dev` extra, because `server.py` needs it at M2.
