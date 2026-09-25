# Session log

One entry per session, newest first. Written on "save progress". Read the latest entry at session start.

## 2026-09-23

### Done
- Rewrote M1 blocks A to D as skeleton handoffs: imports, signatures, docstrings, TODO comments with hints. Provided acceptance tests; 5 tests in `test_actions.py` left for Justin to write. Added "Concepts you will need" lists with doc links.
- Updated `CLAUDE.md` role and rules 3, 3a, 4, 5; `/today` step 5; `/review` step 2.
- M1-A and M1-B done by Justin: `pytest sim` 14 passed, `ruff check sim` clean.
- M1-C done: `sim/labsim/demo.py`, committed as `32a800a`.
- M1-D done, guided in chat: Justin wrote `.github/workflows/tests.yml` (commit `77c0ea5`). First run failed on ruff, fixed in `84822f0`. Bumped `actions/checkout` and `actions/setup-python` to `@v7` in `3219413` to clear the Node.js 20 deprecation warning. Deliberate failure on branch `ci-check` went red with `assert 3 == 4`; branch deleted locally and remotely. Status badge added to `README.md` (`fbbbd2b`). Run 35929303103 on `main`: 4 green jobs, no warnings.
- Justin answered the M1-D check questions: the runner starts empty, so checkout is needed; failures on both macOS jobs point at an OS problem. The OS vs Python version vs combination reasoning was explained.
- M1 closed. Moved M1-C and M1-D to Done in `docs/WORK_INSTRUCTIONS.md`, marked M1 `[x]` in `docs/ROADMAP.md`.
- Wrote M2 blocks: M2-A `protocol.py` (`make_error`, `handle_message`, 12 tests, 2 for Justin), M2-B `server.py` (`handle_connection`, `make_server`, `serve_forever`, `main`, 3 provided tests over a real connection), M2-C Unity `SimClient.cs` (ClientWebSocket, Console logging, `[ContextMenu("Send tick")]`).
- Verified M2 in the scratchpad: Python reference passes all 29 tests and ruff; skeletons fail the 15 new tests cleanly with only the expected F401s. C# reference and skeleton both compile against Unity stubs on .NET 8 with C# 9. The reference client ran against the reference server: `t` 0 then 1 with `a` = `-0.7312715117751976`, then 2. Server log clean on client exit. Doc skeleton text checked to match the verified files exactly.
- Justin committed and pushed the docs (`3dd28c1`) and removed the leftover skeleton comments in `demo.py` and the `Hint` line in `actions.py` (`b67f60e`).
- Updated `docs/ARCHITECTURE.md` (protocol module, server behaviour, Unity WebSocket decision, JSON parsing moved to open decisions) and `docs/ROADMAP.md` (M2 `[~]`). Added two Machine notes (port 8765 in use, Input System only).

### Decisions
- Instruction style is a staff engineer skeleton handoff. Hints escalate one step at a time on request. Reference solutions live only in the scratchpad.
- Unity WebSocket library: .NET built-in `ClientWebSocket`, not NativeWebSocket. No package install, works on Windows and macOS standalone, resumes on the main thread after `await`. No WebGL, which is not a target.
- Message handling lives in its own module, `protocol.py`, separate from `server.py`, so every message case is tested without a network.
- One `World` per server process, shared by all connections. The server sends a snapshot on connect. It binds to `127.0.0.1:8765` and logs with `logging` rather than `print` (Git Bash can buffer `print`).
- The server treats a client leaving without a close handshake as normal (INFO line). Found during verification: without this, every Unity Play stop printed a traceback.
- M2-C sends intents from a `[ContextMenu]` instead of a key press, because the project uses the new Input System only and input handling belongs to M3.
- Unity JSON parsing deferred to M3. `JsonUtility` cannot read the `objects` dictionary.

### Deviations from the instructions
- `demo.py` calls `apply(...)` instead of `set_value` and `tick` directly. Output is identical.
- `tests.yml` uses 4 space indentation (the skeleton used 2). Valid and consistent.
- Action versions are `@v7`, not the `@v4` and `@v5` in the skeleton, to avoid the Node.js 20 deprecation.

### Open issues
- `actions.py` `apply` still has the comment "Reject unknown names, then look up the function and call it." It reads fine as a normal comment, so keeping it is Justin's call.
- `world.py`, `actions.py`, and `demo.py` have not been through `/review`.
- Two M2-C details are unconfirmed on Justin's editor `6000.0.84f1`: the exact menu path `Create > Scripting > MonoBehaviour Script` (a fallback is written into the step), and ClientWebSocket behaviour under Unity's Mono. It was verified on .NET 8 only.
- Unknown whether Ctrl+C from Git Bash lets Python print `server stopped`. M2-B step 4 asks Justin to report it for Machine notes.

### Where we stopped
- M1 done and pushed. M2 blocks written and pushed. Last commit `b67f60e`. Working tree clean apart from this save.
- M2 not started. Next action is M2-A step 1.

### Next
- Open Git Bash at the repo root and run `source .venv/Scripts/activate`.
- Commit this save: `git add docs` then `git commit -m "Docs: save progress"`, then push.
- Start M2-A step 1: create `sim/labsim/protocol.py` from the skeleton.

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
