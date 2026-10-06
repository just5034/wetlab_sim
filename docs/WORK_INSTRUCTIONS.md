# Work instructions

Rewritten by `/today` each session. Finished blocks move to "Done".

Milestone: M2 Bridge closed 2026-10-05. M2-A, M2-B, and M2-C all done. Next: M3 Minimal client. Its blocks are not written yet. Run `/today` to write them.

Why M2: the M1 sim only runs inside Python. Unity is a separate program in a different language and cannot call Python functions. M2 builds the bridge: a small server that holds the one true world and speaks JSON over a WebSocket, and a Unity script that connects and prints what it hears. Nothing is drawn yet. Keeping M2 to "messages go back and forth and show up in the Console" means that when M3 adds visuals, any bug is in the drawing, not the plumbing. Without the bridge, Unity would have to copy the rules in C#, and two copies of the same rules always drift apart.

## Machine notes

Recorded so you do not re-check these every session.

- Python 3.13.1 at `C:\Python313`. Clears the 3.11+ bar.
- Unity 6 LTS is `6000.0.84f1`, already installed. Editors 2022.3.42f1 and 2022.3.62f1 are also present. Ignore them. Unity Hub may default the Editor Version dropdown to a 2022 editor, so always check it.
- Git identity is set.
- The doc's Unix `python3` is `python` or `py -3` here.
- Terminal: use Git Bash for every command. All commands in this file are written for Git Bash. Paths use forward slashes.
- The PowerShell prompt showed `(base)` because conda auto-activates there. Git Bash may too. Either way, activate `.venv` before any `pip` or `pytest` work.
- In Git Bash the venv activates with `source .venv/Scripts/activate` (Windows layout). On a Mac the same venv would be `source .venv/bin/activate`.
- Target platforms are Windows and macOS. See "Platforms" in `docs/ARCHITECTURE.md`.
- The repo lives inside OneDrive. If Unity hangs or reports locked files, pause OneDrive syncing while the editor is open.
- Justin has a separate Unity project also named `client` elsewhere. In Unity Hub, tell them apart by path.
- The sim server uses port 8765. `[Errno 10048]` on Windows or `[Errno 48] Address already in use` on macOS means another server is still running. Stop it with Ctrl+C in its terminal.
- Ctrl+C on `python -m labsim.server` in Git Bash on Windows shuts down cleanly. It prints `server closing`, `server closed`, then `INFO:__main__:server stopped`, with no traceback (checked 2026-10-03).
- VS Code's C# extension can auto-insert `using System.Diagnostics;` when you type `Debug`. That makes `Debug` ambiguous with `UnityEngine.Debug` (error `CS0104`). Delete the stray `using` line.
- Unity created `unity/client/ProjectSettings/SceneTemplateSettings.json` when the scene was edited. It is a normal Unity settings file. Committed in `ff1996c`.
- `System.Net.WebSockets.ClientWebSocket` works under Unity's Mono on `6000.0.84f1` in the Editor (confirmed 2026-10-05). Connect, receive, send, cancel, and dispose all behave as on .NET 8.
- Server log lines start with `INFO:__main__:`, not `INFO:labsim.server:`, because `python -m labsim.server` runs the module as `__main__` and the logger uses `__name__`.
- Unity's Active Input Handling is the new Input System only (`activeInputHandler: 1`). The old `Input.GetKeyDown` API throws in this project.

## How these handoffs work

Each block is written like a handoff from a senior engineer. You get the structure: file names, imports, class and function signatures, and docstrings that state exactly what each piece must do. The bodies are `TODO` comments with hints. You write the logic.

Your loop for every file:
1. Create the file yourself and type in the skeleton exactly, including docstrings.
2. Read the docstrings and TODOs. They are the requirements.
3. Replace each `raise NotImplementedError` (or `pytest.fail(...)`) with your code. Delete each `TODO` and `Hint` comment once it is done. Keep the docstrings.
4. Run the tests. Red means not done yet. Read the failure from the bottom up.

Rules of thumb:
- Tests marked "Provided" are the acceptance criteria. Do not edit them to make them pass; change your code instead.
- While TODOs remain, `ruff check sim` will report imports as unused (`F401`). That is expected. Never run `ruff check --fix` on an unfinished skeleton: it deletes those imports.
- Stuck for more than 15 minutes on one TODO? Ask me for the next hint on that TODO. Hints come in steps, from a nudge to nearly the answer, so you only take as much as you need.
- When a file passes, run `/review sim/labsim/<file>.py` for feedback on style and correctness.

## Next: M3 Minimal client

Not written yet. `/today` writes the M3 blocks at the start of the next session. M3 is the first block with real C# logic beyond plumbing (JSON parsing, a scene object, input), so every C# TODO is walked through in chat per `CLAUDE.md` rule 12.

## C# and Unity already covered

Rule 12 in `CLAUDE.md`: anything not on this list gets a full walkthrough in chat (why, background, the code, line by line, checkpoint, check questions). Anything on this list can be referenced briefly. Add to it after each C# TODO.

Covered in M2-C (2026-10-03 to 2026-10-05), all in `unity/client/Assets/Scripts/SimClient.cs`:
- C# vs Python basics: `using` as import, braces instead of indentation, `;` ends statements, types before names, `public` / `private`, `///` doc comments vs `//` comments, case sensitivity (`cancel` vs `Cancel`).
- Classes and fields vs local variables. Fields start as `null`. Locals must be assigned before use (`CS0165`). Shadowing: `var x = ...` in a method makes a new local that hides the field. Assign a field with `x = ...`.
- `string` concatenation with `+`, escaped quotes `\"` inside strings (`BuildIntent`).
- `static` methods: use no fields, called by name.
- `void`, `return;`, `return null;`, `return value;`.
- `null`, `NullReferenceException`, the null-conditional `?.`.
- `if`, `==`, `!=`, `!`, `||` with short-circuit order (`socket == null` first).
- `while` and `do { } while (...);`, and why `do`/`while` fits "read, then check".
- Arrays: `new byte[8192]`, `byte[]`, `var`.
- Bytes and UTF-8: `Encoding.UTF8.GetBytes` and `GetString`. `MemoryStream`, `stream.Write(buffer, 0, count)`, `ToArray()`.
- `using var` for automatic cleanup (like Python `with`).
- `async`, `await`, `Task`, `Task<string>`, `async void` (only for methods Unity calls: `Start`, context menu items). Missing `await` gives `CS0029`.
- `try` / `catch (Exception e)`, `e.Message`.
- `new` to create objects. `new Uri(url)`.
- `CancellationTokenSource`, `.Token`, `.Cancel()`, `.IsCancellationRequested`. Cancel before Dispose.
- `ClientWebSocket`: `ConnectAsync`, `ReceiveAsync` (+ `WebSocketReceiveResult`: `MessageType`, `Count`, `EndOfMessage`), `SendAsync` (four arguments), `State` / `WebSocketState.Open`, `Dispose()`. `ArraySegment<byte>` as packaging.
- WebSocket close handshake vs abrupt disconnect ("client left without closing").
- Unity: `MonoBehaviour`, Unity calls `Start` and `OnDestroy` by name, `[SerializeField]`, `[ContextMenu]` and the Inspector ⋮ menu, `Debug.Log` / `Debug.LogWarning`, reading the Console and stack traces (including `<Start>d__N:MoveNext`), Play and stop, temporary `Debug.Log` as a checkpoint, compile errors `CS0104`, `CS0162`, `CS1002`.
- Unity editor: Create a folder and script in the Project window, create an empty GameObject, attach a script, `Window > General > Console`, `.meta` files must be committed with their asset.

Not yet covered (walk through when first used): parsing JSON into C# objects, packages (Package Manager), GameObject transforms and components from code, `Update` and the frame loop, the Input System, UI and text, prefabs, events and delegates, generics beyond `Task<T>` and `ArraySegment<T>`, `List<T>` and `Dictionary<K, V>`, properties (`{ get; set; }`), classes in separate files.

## Done

### Block M2-C: Unity client (2026-10-05)

- Justin wrote `unity/client/Assets/Scripts/SimClient.cs` (`BuildIntent`, `OnDestroy`, `ReceiveMessage`, `ReceiveLoop`, `Start`, `SendIntent`, `SendTick`) on the `SimClient` GameObject in `SampleScene`. Walked through one TODO at a time in chat, with the real code and a line-by-line explanation for each from `OnDestroy` onward.
- Checkpoints passed in Play mode on `6000.0.84f1`: server off gives one yellow "Is the server running?" warning. Server on gives `Connected to ws://127.0.0.1:8765` and the `t: 0` snapshot. Send tick gives `t: 1` with `a` = `-0.7312715117751976`, then `t: 2` with `-0.03640403790073221`. Stopping Play prints nothing in Unity and `client left without closing` in Git Bash. Ctrl+C on the server during Play gives "Server closed the connection" in Unity.
- Committed as `ff1996c` "Unity SimClient connection with snapshot logs and send tick mechanism" (script, both `.meta` files, scene, `SceneTemplateSettings.json`, docs) and pushed. CI run 37401893559 green.
- Justin answered the per-TODO check questions in chat, with corrections taught for shadowing (compiles, fails at run time) and the `CS0029` location.
- Open: the block's two "Check your understanding" questions (`t` after replaying Play without restarting the server; changing `Url` to port 9999), plus the `SendIntent` ones (why `socket == null` comes first; `t` after a Play restart).

### Block M2-B: WebSocket server (2026-10-03)

- Justin wrote `sim/labsim/server.py` (`handle_connection`, `make_server`, `serve_forever`, `main`) and added the provided `sim/tests/test_server.py` (3 tests). Done one TODO at a time in chat, with concept explanations for async, `async for`, closures, `async with`, `asyncio.run`, and logging.
- Checkpoint passed: `pytest sim` 29 passed, `ruff check sim` all checks passed. Verified by Claude on 2026-10-03. `python -m labsim.server` prints the listening line. Ctrl+C prints `server closing`, `server closed`, `INFO:__main__:server stopped`, no traceback.
- Committed as `e1e31d9` "websocket server and tests" and pushed. CI run 37171861832 on `main` green.
- Deviation: the snapshot send is inside the `try` in `handle_connection`, with a comment saying why. Chosen by Justin after discussing the tradeoff.
- Not yet reviewed with `/review`.
- The block's two "Check your understanding" questions were not answered: (1) what goes wrong if the tests used port 8765 while a server runs in another terminal; (2) two clients connected, one sends `tick`: does the other see the new snapshot right away, and why or why not.

### Block M2-A: Message handling (2026-10-03)

- Justin wrote `sim/labsim/protocol.py` (`make_error`, `handle_message`) and `sim/tests/test_protocol.py` (10 provided, 2 written by Justin: `test_args_must_be_an_object`, `test_bad_argument_is_an_error_and_world_unchanged`).
- Checkpoint passed: `pytest sim` 26 passed, `ruff check sim` all checks passed. Verified by Claude on 2026-10-03.
- Committed as `3a4ef52` and pushed. CI run 37108975814 on `main` green.
- Not yet reviewed with `/review`.
- The two "Check your understanding" questions were not answered: (1) what happens to the connection if `handle_message` raises; (2) `json.loads("3.10")` vs `json.loads('"3.10"')`.

### Blocks M1-C and M1-D: Demo, commit, and CI (2026-09-23)

- Justin wrote `sim/labsim/demo.py`. Committed M1 as `32a800a` and pushed.
- Wrote `.github/workflows/tests.yml`: triggers `push`, `pull_request`, `workflow_dispatch`; matrix `windows-latest`/`macos-latest` x Python `"3.11"`/`"3.13"`; `fail-fast: false`; bash shell; steps checkout, setup-python, `pip install -e "sim[dev]"`, `ruff check sim`, `pytest sim`. Uses 4 space indentation.
- First CI run (`77c0ea5`) failed on ruff; fixed in `84822f0`.
- Bumped `actions/checkout` and `actions/setup-python` to `@v7` in `3219413` to clear the Node.js 20 deprecation warning.
- Deliberate failure on branch `ci-check` went red with `assert 3 == 4` at `sim/tests/test_actions.py:22`. Branch deleted locally and on GitHub.
- Optional step 5 done: status badge in `README.md` (`fbbbd2b`).
- Checkpoint passed: run 35929303103 on `main` shows 4 green jobs, no Node warnings. Verified by Claude on 2026-09-23.

### Blocks M1-A and M1-B: World state and actions (2026-09-23)

- Justin wrote `sim/labsim/world.py` (`World` dataclass: `seed`, `t`, `objects`, `rng`; `__post_init__`; `snapshot()`) and `sim/labsim/actions.py` (`set_value`, `tick`, `ACTIONS`, `apply`).
- Tests: `sim/tests/test_world.py` (4 provided) and `sim/tests/test_actions.py` (4 provided, 5 written by Justin, one parametrized over 2 values).
- Checkpoint passed: `pytest sim` 14 passed, `ruff check sim` all checks passed, no TODOs left. Verified by Claude on 2026-09-23.
- Not yet committed. M1-C step 3 commits it together with the docs changes.
- Not yet reviewed with `/review`. Optional before committing.
- Validation convention: `TypeError` for wrong types, `ValueError` for bad values (ruff rule TRY004).

### Block C: Git (2026-09-22)

- `.gitignore` at the repo root covers Python artifacts and Unity generated folders (`Library`, `Temp`, `Obj`, `Logs`, `UserSettings`, `.vscode`, `*.csproj`, `*.sln*`).
- Committed as `53753b9` and pushed to `origin/main`.
- Checkpoint passed: clean tree, 73 tracked files, none generated.

### Block B: Unity (2026-09-22)

- Created `unity/` at the repo root.
- Created Unity project `unity/client` from the `Universal 3D` template on editor `6000.0.84f1`. URP package `com.unity.render-pipelines.universal` 17.0.4 present in `Packages/manifest.json`.
- Checkpoint passed: `Assets` and `ProjectSettings` exist, `ProjectVersion.txt` reads `6000.0.84f1`.
- Deviation: the template changed from Universal 2D to Universal 3D to match `docs/VISION.md`.
- First attempt was created on editor 2022.3.62f1 with the Built-In 3D template (no URP). It was removed from Unity Hub, deleted, and recreated. Lesson: set the Editor Version dropdown before picking a template.

### Repo restructure (2026-09-21)

The template shipped nested at `instructions/labsim-template/labsim/`, duplicated byte for byte at `instructions/`. Promoted the complete copy to the repo root and deleted `instructions/`. `CLAUDE.md` and `.claude/commands/` only load from the root, so `/today` and `/review` did not resolve until this was done. The template `README.md` replaced the one line stub.

### Block A: Python (2026-09-21)

- `.venv` created at the repo root and activated.
- `sim/pyproject.toml` written. Package `labsim`, `requires-python >=3.11`, `websockets` as a runtime dependency, `pytest` and `ruff` under the `dev` extra, setuptools backend, `packages.find` limited to `labsim*` so `tests` does not get installed.
- `sim/labsim/__init__.py` and `sim/tests/__init__.py` created, both empty.
- `pip install -e "sim[dev]"` succeeded.
- Checkpoint passed. `pytest sim` collected zero tests, `ruff check sim` reported no issues.
- Verified: `import labsim` resolves to `sim\labsim\__init__.py`, confirming the editable install points at the working tree.

Deviation from the original step 3: `websockets` sits under `dependencies` rather than the `dev` extra, because it is needed to run `server.py` at M2, not just to develop. `pip install -e "sim[dev]"` installs all three either way.
