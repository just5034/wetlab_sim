# Architecture

Python owns simulation state and rules. Unity owns rendering, input, and UI. They talk over a WebSocket with JSON messages. Unity never computes simulation logic. Python never draws.

Why split: the scientific libraries the team may choose later are Python. The core can be tested without Unity. The same core can later drive other clients or automated harnesses.

```
+------------------+     intents ->      +------------------+
|  Unity client    | <----------------> |  Python sim core |
|  unity/  (game)  |  <- snapshots       |  sim/  (truth)   |
+------------------+                     +------------------+
                                                  ^
+------------------+     same protocol            |
|  Sandbox         | <----------------------------+
|  sandbox/ (dev)  |
+------------------+
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
- Render pipeline is URP 3D (template `Universal 3D`), chosen 2026-09-22. The look is 2.5D: hand-drawn black and white 2D sprites in a 3D scene with a tilted perspective camera, like West of Loathing and Don't Starve Together (see `docs/VISION.md`).

## Sandbox (`sandbox/`, dev tool, M4)

Directive (Justin, 2026-10-25): the team needs a low-overhead way to see, touch, and experiment with the simulation mechanics without booting Unity or loading game art. It should be visually appealing. Unlike the game, Claude does all the drawing here.

Design (proposed by Claude, adjust as needed):
- A browser app served locally by the Python sim. It connects to the same WebSocket server and speaks the same JSON protocol as Unity, so what we test is the real world state, not a copy. Unity and the sandbox are two clients of one truth.
- Plain HTML, CSS, and JavaScript with no build step. Any library is pinned and vendored into the repo, so it works offline and on Windows and macOS with only Python installed.
- Views: time-series plots of every stock, a drawn lake diagram (layers, flows between stocks with arrow width by rate), and a readout of the current snapshot.
- Controls: play, pause, step, speed; sliders for parameters and forcings; buttons for every player action in `ACTIONS`; reset with a seed; save and load scenarios; compare two runs side by side; export a run to CSV.
- The sandbox builds its controls from what the sim reports (a "describe" message listing stocks, parameters, and actions with units and ranges), so a new model or action shows up in the sandbox with little or no sandbox code.
- Low compute: the sim does the math, the browser only draws. Runs at many ticks per second on a laptop.
- Not shipped with the game. Sandbox-only messages (set parameter, reset, fast-forward, history) can be turned off in builds.
- Style: its own clean look, may borrow the game's ink-on-paper feel. Color is allowed here because it is a tool, not the game.

Rule: every change to the model or to the actions also updates the sandbox, so the team can try it before it reaches Unity.

## Art assets

All final art is hand-drawn by the team. Claude never generates final art. Claude imports what the team provides and places it as Justin directs. Conventions accepted by Justin 2026-10-25:

- Drop folder: artists put source files (for example `.psd`, `.kra`, high-res `.png`) in `art/source/` at the repo root. It is outside Unity so source files do not slow the editor. Everything under `art/` is stored in Git LFS (decided 2026-10-25, see `.gitattributes`).
- In Unity: exported sprites go in `unity/client/Assets/Art/`, split by use (`Characters/`, `Props/`, `Environment/`, `UI/`). Claude creates these folders when the first asset arrives.
- Git LFS also covers image, audio, and video files under `unity/client/Assets/Art/`. Their `.meta` files stay normal text. Each teammate runs `git lfs install` once after cloning. GitHub's free LFS storage and bandwidth are limited, so watch usage as art grows.
- Export format: PNG with transparency. One consistent pixels-per-unit value and canvas scale across all assets so sizes match in the scene. Values to agree with the artists.
- Naming: lowercase with underscores, describing the thing and its state, for example `algae_bloom_heavy.png`, `fish_idle_01.png`. Sim-driven variants share a stem so code can pick the sprite by state.
- Import settings (texture type Sprite, filtering, compression) are set the same way for every sprite. Claude applies them through Unity import presets or by editing `.meta` files, then Justin confirms in the Editor.
- Each sprite-to-sim mapping (which sprite shows for which state) lives in data or one mapping script, not scattered through code, so art can change without touching sim logic.

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

- Simulation framework, accepted 2026-10-25: models expressed as stocks and fluxes, assembled into one NumPy derivative function, stepped by our own integrator inside `tick`. No external simulation software at runtime. See `docs/research/SIM_FRAMEWORK_PROPOSAL.md`.
- Sandbox as a second client of the same sim server, directive from Justin 2026-10-25. See "Sandbox".

- Unity WebSocket library: `System.Net.WebSockets.ClientWebSocket`, decided 2026-09-23. Built into the .NET profile Unity ships, so there is no package to install. Works in Windows and macOS standalone players (Mono). After `await`, code resumes on Unity's main thread, so no message queue is needed. Not supported in WebGL builds, which are not a target. The alternative was NativeWebSocket, a git URL package that needs a per-frame dispatch call.
