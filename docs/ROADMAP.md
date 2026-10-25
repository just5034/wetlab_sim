# Roadmap

[ ] not started, [~] in progress, [x] done

## M0 Tooling [x]
Python venv with pytest and ruff. Unity 6 LTS 3D URP project in `unity/`. Git ignores for both.
Checkpoint: `pytest sim` runs with zero tests; Unity project opens clean.
Block A Python done 2026-09-21. Block B Unity done 2026-09-22 (Universal 3D, 6000.0.84f1). Block C git done 2026-09-22 (commit 53753b9, pushed). M0 closed 2026-09-22.

## M1 Sim core, no networking [x]
World state, `set_value`, `tick`, seeded RNG, tests. GitHub Actions runs the tests on Windows and macOS.
Checkpoint: a script ticks the world 10 times and prints the snapshots. CI is green on both OSes.
M1-A world and M1-B actions done 2026-09-23. M1-C demo committed (32a800a). M1-D CI green on Windows and macOS (run 35929303103). M1 closed 2026-09-23.

## M2 Bridge [x]
Python WebSocket server. Unity client that connects and logs snapshots.
Checkpoint: press Play, snapshots appear in Unity Console.
Blocks M2-A protocol, M2-B server, M2-C Unity client written and verified 2026-09-23. M2-A done 2026-10-03 (commit 3a4ef52, CI green). M2-B done 2026-10-03 (commit e1e31d9, CI run 37171861832 green). M2-C done 2026-10-05 (commit ff1996c, CI run 37401893559 green): Play shows the snapshot in the Console, Send tick advances `t`. M2 closed 2026-10-05. Next: M3, blocks not yet written.

## Plan from M3 on (accepted by Justin 2026-10-25)

Replaces the old M3 (one placeholder object) and M4 (cross-platform build). Claude Code is the main developer. The domain is a lake ecosystem from one published single-lake model.

## M3 Lake core (Python) [ ]
Stocks-and-fluxes framework (`docs/research/SIM_FRAMEWORK_PROPOSAL.md`) plus the chosen lake model from `docs/research/LAKE_MODEL_PAPERS.md`. Replaces the random-walk placeholder.
Checkpoint: a script runs the model for the paper's period and plots it next to the paper's figure. Tests check mass conservation, determinism, and key values.

## M4 Sandbox (dev dashboard) [ ]
A lightweight, good-looking app in the browser where the team pokes the real Python world: watch stocks change, drag parameters and forcings, fire player actions, reset, compare runs. No Unity and no game art needed. See "Sandbox" in `docs/ARCHITECTURE.md`. Built first against the M3 model, then kept current with every model or action change.
Checkpoint: start the sim, open the sandbox, change a parameter, see the plots and lake drawing respond within a second.

## M5 Lake view (Unity) [ ]
Unity parses the snapshot (likely Newtonsoft JSON) and shows the lake in a 2.5D scene with placeholders, swapped for team art as it arrives. One or two player actions (for example nutrient loading).
Checkpoint: press Play, tick, see values and visuals change.

## M6 Cross-platform build [ ]
Windows and macOS builds that start the Python sim themselves and connect. Needs the Mac Build Support module in Unity Hub and a Mac (or a macOS CI runner) to package the Python side. The sandbox is a dev tool and is not shipped.
Checkpoint: on a Mac, double-click the app, click, the lake changes. Same on Windows.
