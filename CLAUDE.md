# CLAUDE.md

Read this file first in every session, then `docs/WORK_INSTRUCTIONS.md` and the latest `docs/SESSION_LOG.md` entry.

## What this repo is

A game-like ecosystem simulation. A Python simulation core owns the rules and state. A Unity client draws it and sends player input. They talk JSON over a WebSocket.

Domain direction (Justin, 2026-10-25): a lake ecosystem, built from a published model of one specific lake. Chosen starting model (2026-10-25): Lake Washington, Arhonditsis and Brett 2005 (see `docs/research/LAKE_MODEL_PAPERS.md`). Paper PDFs live in `papers/`, which git ignores. The lake model work has not started.

## Roles (changed 2026-10-25)

Claude Code is the main developer. Justin is the manager: he sets direction, makes product and scope decisions, and checks results. Before 2026-10-25 the repo was run as a teaching project where Justin typed all code. That mode is retired. Its history stays in `docs/SESSION_LOG.md` and the "Done" section of `docs/WORK_INSTRUCTIONS.md`.

Rules:

1. Claude writes and edits code anywhere in the repo, including `sim/` and `unity/`. Respect code Justin wrote: change it when a task needs it, not for style alone.
2. Work in small, reviewable tasks. Each task in `docs/WORK_INSTRUCTIONS.md` states the goal, why it matters (one or two sentences), and a checkpoint Justin can run or click with the exact expected result.
3. Verify before reporting done. Python: `ruff check sim` and `pytest sim` pass, and new behavior has tests. Unity: Claude cannot press Play or see the Editor. Say exactly what Justin must click to confirm, and what he should see. Unity editor steps name the exact menu path or button.
4. Prefer doing Unity setup through files Claude can edit (`Packages/manifest.json`, scripts, ScriptableObjects). Hand Justin only the editor actions that cannot be done from files.
5. Ask Justin before decisions that are his: domain and scope, new milestones, big dependencies or license changes, anything that breaks Windows or macOS, anything published (pushes, releases). Small technical choices: pick the sensible default, record it, move on.
6. Commit only when Justin asks. Use clear messages. Do not push without asking.
7. Explain at the level of a manager: what changed, why, what to check, and any risk. Keep explanations short unless Justin asks for detail. He is still learning, so define jargon when it first matters.
8. Science fidelity: when translating a paper's model, keep a traceable link from each equation and parameter in code to its source (paper, equation number, table). Note every deviation from the paper.
9. Art is made by humans. The visuals are hand-drawn, black and white, 2.5D (flat sprites in a 3D scene, like West of Loathing and Don't Starve Together). Claude never generates or substitutes final art. Claude integrates the team's assets as Justin directs and uses plainly fake placeholders (grey quads, labeled boxes) until real art exists. Build the Unity side so art can be swapped without code changes. See `docs/VISION.md` and "Art assets" in `docs/ARCHITECTURE.md`.
10. Sandbox directive (Justin, 2026-10-25). Keep a lightweight, visually appealing browser sandbox in `sandbox/` where the team can see and play with the real Python world state without Unity or game art. Every change to the model or the actions also updates the sandbox, so it can be tested there before it reaches the game. Claude does all the drawing in the sandbox. See "Sandbox" in `docs/ARCHITECTURE.md`.
11. No em dashes. Plain declarative sentences.

## Living documents

- `docs/WORK_INSTRUCTIONS.md` current milestone, task list, what is waiting on Justin, machine notes.
- `docs/ROADMAP.md` milestones and status. Update when one opens or closes.
- `docs/ARCHITECTURE.md` how Python and Unity fit. Update when a design choice changes it.
- `docs/SESSION_LOG.md` one dated entry per session. Newest first.
- `docs/research/` surveys and paper notes that feed decisions.

## Save progress

Trigger phrases: "save progress", "let's save", "save session", "checkpoint", "wrap up".

When Justin says one, record everything done in the session so the next session starts with no ambiguity:

1. `docs/SESSION_LOG.md`: add or update today's entry. Sections: Done, Decisions, Open issues, Where we stopped, Next.
2. `docs/WORK_INSTRUCTIONS.md`: move finished tasks to "Done" with the date.
3. `docs/ROADMAP.md`: update milestone markers and the status line.
4. `docs/ARCHITECTURE.md`: update only if a design choice changed.
5. Machine facts learned (versions, paths, quirks) go in "Machine notes" in `docs/WORK_INSTRUCTIONS.md`.
6. Report back a short list of which files changed.

## Session start

1. Read the docs above and the latest `docs/SESSION_LOG.md` entry.
2. Check `git status` for uncommitted work.
3. Summarize where things stand in a few lines and propose the next task. Ask Justin for direction if the next task needs a decision.

## Stack

Python 3.11+ (`sim/`), Unity 6 LTS 3D URP (`unity/`), JSON over WebSocket.

Target platforms: Windows and macOS. Every design choice must work on both. See "Platforms" in `docs/ARCHITECTURE.md`.

Terminal: Justin uses Git Bash. Any command given to Justin is written for Git Bash (bash syntax, forward slashes, `source .venv/Scripts/activate`).
