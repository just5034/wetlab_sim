# Roadmap

[ ] not started, [~] in progress, [x] done

## M0 Tooling [x]
Python venv with pytest and ruff. Unity 6 LTS 3D URP project in `unity/`. Git ignores for both.
Checkpoint: `pytest sim` runs with zero tests; Unity project opens clean.
Block A Python done 2026-09-21. Block B Unity done 2026-09-22 (Universal 3D, 6000.0.84f1). Block C git done 2026-09-22 (commit 53753b9, pushed). M0 closed 2026-09-22.

## M1 Sim core, no networking [~]
World state, `set_value`, `tick`, seeded RNG, tests. GitHub Actions runs the tests on Windows and macOS.
Checkpoint: a script ticks the world 10 times and prints the snapshots. CI is green on both OSes.
M1-A world and M1-B actions done 2026-09-23 (14 tests pass, uncommitted). M1-C demo and M1-D CI remain.

## M2 Bridge [ ]
Python WebSocket server. Unity client that connects and logs snapshots.
Checkpoint: press Play, snapshots appear in Unity Console.

## M3 Minimal client [ ]
One scene object showing a value. Click sends `tick`. Value updates from the snapshot.
Checkpoint: click, number changes, Python log shows the intent.

## M4 Cross-platform build [ ]
Windows and macOS builds that start the Python sim themselves and connect. Needs the Mac Build Support module in Unity Hub and a Mac (or a macOS CI runner) to package the Python side.
Checkpoint: on a Mac, double-click the app, click, number changes. Same on Windows.

## After M4
Team decides the domain. Replace placeholder objects and rules with real ones. Roadmap is rewritten then.
