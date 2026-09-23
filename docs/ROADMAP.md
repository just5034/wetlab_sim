# Roadmap

[ ] not started, [~] in progress, [x] done

## M0 Tooling [~]
Python venv with pytest and ruff. Unity 6 LTS 3D URP project in `unity/`. Git ignores for both.
Checkpoint: `pytest sim` runs with zero tests; Unity project opens clean.
Block A Python done 2026-09-21. Block B Unity done 2026-09-22 (Universal 3D, 6000.0.84f1). Block C git remains.

## M1 Sim core, no networking [ ]
World state, `set_value`, `tick`, seeded RNG, tests.
Checkpoint: a script ticks the world 10 times and prints the snapshots.

## M2 Bridge [ ]
Python WebSocket server. Unity client that connects and logs snapshots.
Checkpoint: press Play, snapshots appear in Unity Console.

## M3 Minimal client [ ]
One scene object showing a value. Click sends `tick`. Value updates from the snapshot.
Checkpoint: click, number changes, Python log shows the intent.

## After M3
Team decides the domain. Replace placeholder objects and rules with real ones. Roadmap is rewritten then.
