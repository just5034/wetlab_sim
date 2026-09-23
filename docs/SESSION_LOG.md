# Session log

One entry per session, newest first. Written on "save progress". Read the latest entry at session start.

## 2026-09-23

### Done
- Rewrote M1 blocks A to D as skeleton handoffs: imports, signatures, docstrings, TODO comments with hints. Provided acceptance tests; 5 tests in `test_actions.py` left for Justin to write. Added "Concepts you will need" lists with doc links.
- Verified in the scratchpad: skeletons match the doc, skeleton fails all 14 tests cleanly, a reference solution passes all 14 plus ruff, demo first line recorded.
- Updated `CLAUDE.md` role and rules 3, 3a, 4, 5; `/today` step 5; `/review` step 2.
- Justin completed M1-A and M1-B. Verified at save: `pytest sim` 14 passed, `ruff check sim` clean, no TODOs remaining.
- Moved M1-A and M1-B to Done in `docs/WORK_INSTRUCTIONS.md` and updated the M1 status line in `docs/ROADMAP.md`.

### Decisions
- Instruction style is a staff engineer skeleton handoff. Full written-out code (tried earlier the same day) gave away too much. Hints escalate one step at a time on request.
- Reference solutions live only in the scratchpad, never in the repo or docs.

### Open issues
- While TODOs remain, ruff reports unused imports (F401). Documented in the handoff: never run `ruff check --fix` on an unfinished skeleton.

### Where we stopped
- M1 Sim core. M1-A and M1-B done and verified. M1-C (demo and commit) and M1-D (GitHub Actions) not started.
- Nothing committed since `53753b9`. Uncommitted: Justin's four files under `sim/` (`world.py`, `actions.py`, `test_world.py`, `test_actions.py`) plus today's changes to `CLAUDE.md`, `.claude/commands/`, and `docs/`. `.github/` does not exist yet.
- Neither file has been through `/review` yet.

### Next
- Open Git Bash at the repo root and run `source .venv/Scripts/activate`.
- Optional: `/review sim/labsim/world.py` and `/review sim/labsim/actions.py` before committing.
- M1-C step 1: create `sim/labsim/demo.py` from the skeleton. Step 3 commits everything.
- Then M1-D: `.github/workflows/tests.yml`.

## 2026-09-22

### Done
- Session start review of docs and repo state.
- Added the "Save progress" procedure to `CLAUDE.md` and created this log.
- Added the list of paths `.gitignore` must cover to Block C in `docs/WORK_INSTRUCTIONS.md`.
- Created `docs/VISION.md` recording Justin's art direction (West of Loathing, Don't Starve Together, Deadly Days: Roadtrip, Octopath Traveler 0, Paper Mario).
- Switched the Unity template from Universal 2D to Universal 3D in `CLAUDE.md`, `docs/ROADMAP.md`, `docs/WORK_INSTRUCTIONS.md`, `docs/ARCHITECTURE.md`.
- Block B done. `unity/client` created on `6000.0.84f1` from Universal 3D, URP 17.0.4. First attempt used editor 2022.3.62f1 and the Built-In 3D template, so it was deleted and redone.
- Wrote Block C with the exact `.gitignore` patterns. Justin completed it: commit `53753b9`, pushed to `origin/main`, 73 tracked files. M0 closed.
- Explained what `sim/pyproject.toml`, pytest, and ruff are for, how `import labsim` resolves, and how the server gets started (added shipping options to `docs/ARCHITECTURE.md`).
- Wrote M1 blocks A, B, C. Added a "Why" paragraph to the milestone and each block.

### Decisions
- "Save progress" and similar phrases now trigger a full write-up across the living docs. Procedure lives in `CLAUDE.md`.
- Unity template is Universal 3D (URP 3D). Reason: the references mostly put 2D sprites in a 3D world with lighting, shadows, and depth of field. 3D also covers flat 2D, and switching later is costly.
- Every milestone and block now opens with a "Why" paragraph. Rule 8 in `CLAUDE.md`, step 4 in `/today`.
- Terminal commands are written for Git Bash from now on. Recorded in `CLAUDE.md` Stack section and Machine notes.
- Target platforms are Windows and macOS. Added "Platforms" to `docs/ARCHITECTURE.md` and milestone M4 Cross-platform build to `docs/ROADMAP.md`.
- About half the team has Macs. Explained how GitHub Actions works.
- GitHub Actions is the official check that code works on both OSes. Added Block M1-D (test workflow on Windows and macOS, Python 3.11 and 3.13).
- Teaching style changed: work instructions now give full code, verified in the scratchpad, with part by part explanations and "Check your understanding" questions. `CLAUDE.md` role and rules rewritten, `/today` and `/review` updated. M1 blocks rewritten to match.
- Validation errors use `TypeError` for wrong types and `ValueError` for bad values (ruff rule TRY004 is on by default in ruff 0.16.8). M1 now has 14 tests.
- Kept the project name `client`. Hub tracks projects by path, so a second `client` elsewhere is harmless.

### Where we stopped
- M0 Tooling done and pushed. M1 Sim core not started.

### Next
- M1 blocks written in `docs/WORK_INSTRUCTIONS.md` (M1-A World, M1-B Actions, M1-C Demo, M1-D GitHub Actions). Start at M1-A step 1.

## 2026-09-21

Reconstructed from `docs/WORK_INSTRUCTIONS.md` "Done" section.

### Done
- Repo restructure. Promoted the template from `instructions/labsim-template/labsim/` to the repo root and deleted `instructions/`.
- Block A (Python). `.venv` at the repo root, `sim/pyproject.toml`, empty `__init__.py` files in `sim/labsim` and `sim/tests`, `pip install -e "sim[dev]"`. Checkpoint passed.

### Deviations from the instructions
- `websockets` is a runtime dependency rather than a `dev` extra, because `server.py` needs it at M2.
