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
- `protocol.py` turns one incoming message into one reply (`handle_message`). No networking, so every message case is unit tested. Bad messages get an error reply, never an exception.
- `server.py` WebSocket server on `127.0.0.1:8765` (library `websockets`, asyncio API). One `World` per server process, shared by every connection. Sends a snapshot as soon as a client connects, then answers each message with the reply from `handle_message`. Logs with `logging` (stderr), not `print`. A client that disconnects without a close handshake (Unity leaving Play mode) is logged at INFO, not as an error.
- `tests/` pytest for each action.

## Unity (`unity/client`)

- `SimClient.cs` opens the WebSocket, sends intents, receives snapshots. Uses .NET's built-in `System.Net.WebSockets.ClientWebSocket` (decided 2026-09-23 at M2). At M2 it logs raw JSON to the Console and builds intents by string concatenation. Parsing arrives at M3.
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

## Platforms

Targets: Windows and macOS (Intel and Apple Silicon). Decided 2026-09-22. About half the team has Macs, so Mac testing and Mac packaging can happen on a teammate's machine. GitHub Actions is the official cross-platform check: `.github/workflows/tests.yml` runs ruff and pytest on Windows and macOS for every push (added in M1-D). It is also the likely path for automated Mac builds at M4.

What that means for each side:
- Python: pure Python only, no Windows-only calls. Build paths with `pathlib`, never hardcoded backslashes. Bind the server to `127.0.0.1`. Any future dependency must ship macOS wheels for both `arm64` and `x86_64`.
- Unity: the Mac player needs the "Mac Build Support (Mono)" module for `6000.0.84f1`. With Mono, Unity can build a Mac app from Windows. IL2CPP for Mac would need a Mac.
- Packaging the Python side: tools like PyInstaller do not cross-compile. A Mac sim executable must be built on a Mac or on a macOS CI runner (for example GitHub Actions).
- Distribution: an app built without Apple signing and notarization gets blocked by Gatekeeper. Players can bypass it with right-click Open. Clean distribution needs an Apple Developer account and a Mac.
- Unity launching an embedded executable on Mac must handle the `.app` bundle path, the executable permission bit, and the quarantine flag.

## Open decisions

- Unity JSON parsing. Decide at M3. Unity's `JsonUtility` cannot read the snapshot's `objects` dictionary. Likely candidate: the `com.unity.nuget.newtonsoft-json` package.
- Whether builds bundle Python. Decide later. During development the server is started by hand (`python -m labsim.server`) before pressing Play. Options for a shipped build: (a) freeze the sim into an exe (for example PyInstaller) that Unity launches with `System.Diagnostics.Process` on startup and stops on quit, (b) host the sim on a remote server, (c) embed a Python runtime inside Unity. (a) is the likely default. It needs a separate Python build per OS (see Platforms). (b) avoids per-OS Python packaging entirely. (c) works against the process split and is not preferred. Proven at M4.

## Decided

- Unity WebSocket library: `System.Net.WebSockets.ClientWebSocket`, decided 2026-09-23. Built into the .NET profile Unity ships, so there is no package to install. Works in Windows and macOS standalone players (Mono). After `await`, code resumes on Unity's main thread, so no message queue is needed. Not supported in WebGL builds, which are not a target. The alternative was NativeWebSocket, a git URL package that needs a per-frame dispatch call.
