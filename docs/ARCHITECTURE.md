# Architecture

Python owns simulation state and rules. Unity owns rendering, input, and UI. They talk over a WebSocket with JSON messages. Unity never computes simulation logic. Python never draws.

Why split: the scientific libraries the team may choose later are Python. The core can be tested without Unity. The same core can later drive other clients or automated harnesses.

```
+------------------+     intents ->      +------------------+
|  Unity client    | <----------------> |  Python sim core |
|  unity/          |  <- snapshots       |  sim/            |
+------------------+                     +------------------+
```

## Python (`sim/labsim`)

- `world.py` holds state: a clock and a dictionary of named objects, each with a numeric `value`.
- `actions.py` the verbs. Template ships with two: `set_value(name, value)` and `tick(steps)` which advances the clock and applies a rule to each object.
- `server.py` WebSocket server. Receives intents, applies actions, sends back a snapshot.
- `tests/` pytest for each action.

## Unity (`unity/client`)

- `SimClient.cs` opens the WebSocket, sends intents, receives snapshots.
- `WorldView.cs` stores the latest snapshot and raises a C# event on change.
- One placeholder scene object that displays an object's `value` and sends an intent on click.
- Render pipeline is URP 3D (template `Universal 3D`), chosen 2026-09-22. The target look is 2D sprites in a 3D scene (see `docs/VISION.md`). The 3D renderer also covers flat orthographic 2D, so it does not rule out the flatter references.

## Messages

Intent (Unity to Python):
```json
{"type": "intent", "action": "tick", "args": {"steps": 1}}
```

Snapshot (Python to Unity):
```json
{"type": "snapshot", "t": 3, "objects": {"a": {"value": 1.5}}}
```

Error (Python to Unity):
```json
{"type": "error", "message": "unknown action"}
```

Rules:
- The snapshot is the whole truth. Unity keeps no separate state.
- Only the sim advances time. Unity asks.
- The world has a seed. Same seed and same intent sequence give the same snapshots.

## Open decisions

- Unity WebSocket library (NativeWebSocket vs other). Decide at M2.
- Whether builds bundle Python. Decide later.
