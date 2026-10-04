# Work instructions

Rewritten by `/today` each session. Finished blocks move to "Done".

Milestone: M2 Bridge. Blocks M2-A to M2-C written 2026-09-23. M2-A and M2-B done 2026-10-03. Start at M2-C step 1.

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

## Block M2-C: Unity client

Why: this is Unity's end of the bridge. A C# script on an empty GameObject connects when you press Play, logs everything the sim sends into the Console, and can send a tick. Nothing is drawn yet; drawing is M3. This is your first C# and your first Unity script. Keeping it to Console output means you learn C# and the Unity script lifecycle without also fighting scenes and UI. It also proves the chosen WebSocket approach works on your machine before anything depends on it.

Goal: press Play, and snapshots from Python appear in the Unity Console. Send a tick from the Inspector and watch `t` go up.

Concepts you will need:
- **C# compared to Python.** Braces `{ }` instead of indentation, and `;` ends each statement. Types come before names: `string url`. `using X;` is like `import`. `//` starts a comment, and `///` starts a doc comment, the C# version of a docstring. Tour: https://learn.microsoft.com/dotnet/csharp/tour-of-csharp/
- **GameObject and component.** Everything in a Unity scene is a GameObject. What it does comes from the components attached to it. Your script becomes a component once you attach it.
- **MonoBehaviour.** The base class for scripts you attach to GameObjects. Unity calls certain methods by name at set moments: `Start` runs once when Play begins, and `OnDestroy` runs when the object goes away, which includes leaving Play mode. Docs: https://docs.unity3d.com/Manual/class-MonoBehaviour.html and the order of calls: https://docs.unity3d.com/Manual/execution-order.html
- **Attributes.** Tags in square brackets that other code reads, similar to Python decorators. `[SerializeField]` shows a private field in the Inspector so you can edit it there. `[ContextMenu("Send tick")]` adds a menu item to the component that runs that method.
- **`async`, `await`, and `Task` in C#.** The same idea as in Python. A `Task` is the result of an async method; `Task<string>` finishes with a string. `async void` is only for methods that nobody awaits, like Unity's `Start` or a context menu item. In Unity, code after an `await` continues on the main thread, so calling `Debug.Log` there is safe.
- **`ClientWebSocket`.** The WebSocket client built into .NET, in `System.Net.WebSockets`. Unity ships it, so there is nothing to install. Docs: https://learn.microsoft.com/dotnet/api/system.net.websockets.clientwebsocket
- **Bytes and UTF-8.** The network carries bytes, not text. `Encoding.UTF8` converts text to bytes and back. A `MemoryStream` is a growable byte container, used here to collect the pieces of one message.
- **`CancellationToken`.** A stop signal you pass to operations that wait. Cancelling its `CancellationTokenSource` makes a waiting `ReceiveAsync` give up. Without it, the receive keeps waiting after you leave Play mode.
- **`null` and `?.`.** `null` is C#'s `None`. `x?.Method()` calls `Method` only when `x` is not `null`.
- **`Debug.Log` and `Debug.LogWarning`.** Write a white or yellow line to the Unity Console.

### Step 1. Set your code editor

In Unity: `Edit > Preferences > External Tools > External Script Editor`, choose `Visual Studio Code` (on a Mac: `Unity > Settings > External Tools`). In VS Code, install the extension "Unity" by Microsoft. It pulls in C# Dev Kit.

Why: you get autocomplete and red underlines for C# mistakes before Unity even compiles. If you use a different editor, pick it here instead.

### Step 2. Create a Scripts folder

In the Project window, right-click `Assets`, then `Create > Folder`, and name it `Scripts`.

Why: keeps your code apart from the template's assets.

### Step 3. Create `SimClient.cs` from this skeleton

Right-click `Scripts`, then `Create > Scripting > MonoBehaviour Script` (if your menu has no `Scripting` entry, use `Create > MonoBehaviour Script`). Name it exactly `SimClient` and press Enter. Double-click it to open it in your editor, replace everything with the skeleton, and save.

Why: Unity matches the file name to the class name. `SimClient.cs` must contain `class SimClient`, or Unity cannot attach it.

```csharp
using System;
using System.IO;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;

/// <summary>
/// Connects to the Python sim over a WebSocket, logs every message it
/// receives to the Console, and sends intents. It holds no sim state.
/// </summary>
public class SimClient : MonoBehaviour
{
    /// <summary>Server address. Editable in the Inspector.</summary>
    [SerializeField] private string url = "ws://127.0.0.1:8765";

    /// <summary>The connection. Null until Start runs.</summary>
    private ClientWebSocket socket;

    /// <summary>Cancelled in OnDestroy to stop any receive still waiting.</summary>
    private CancellationTokenSource cancel;

    /// <summary>
    /// Unity calls this once when Play starts. Create `cancel` and `socket`,
    /// connect to `url`, log "Connected to " + url, then run ReceiveLoop
    /// until the connection ends.
    /// If anything throws: stay silent when `cancel` has been cancelled
    /// (Play mode is stopping). Otherwise log a warning that includes the
    /// exception message and the words "Is the server running?".
    /// </summary>
    private async void Start()
    {
        // TODO 1: Create a new CancellationTokenSource and a new ClientWebSocket.
        // TODO 2: Inside try: await socket.ConnectAsync(new Uri(url), cancel.Token),
        //   log the connected line with Debug.Log, then await ReceiveLoop(cancel.Token).
        // TODO 3: catch (Exception e) { ... }
        // Hint: cancel.IsCancellationRequested tells you whether Play mode is
        //   stopping. Use Debug.LogWarning for real failures.
        throw new NotImplementedException();
    }

    /// <summary>
    /// While the socket is open, receive one whole message at a time and log
    /// it (format in the TODO below). When ReceiveMessage returns null, log
    /// "Server closed the connection" and return.
    /// </summary>
    private async Task ReceiveLoop(CancellationToken token)
    {
        // TODO: while (socket.State == WebSocketState.Open) { ... }
        //   Log each message as "<- " + message, so replies are easy to spot.
        // Hint: string message = await ReceiveMessage(token);
        throw new NotImplementedException();
    }

    /// <summary>
    /// Receive one complete text message and return it as a string.
    /// A message can arrive in several pieces (frames). Keep reading until
    /// a piece arrives with EndOfMessage set to true.
    /// Returns null if the server sent a close message instead.
    /// </summary>
    private async Task<string> ReceiveMessage(CancellationToken token)
    {
        // TODO 1: var buffer = new byte[8192]; plus a MemoryStream to collect the pieces.
        // TODO 2: Read pieces in a loop:
        //   var result = await socket.ReceiveAsync(new ArraySegment<byte>(buffer), token);
        //   If result.MessageType is WebSocketMessageType.Close, return null.
        //   Otherwise write result.Count bytes from buffer into the stream.
        //   Stop after the piece where result.EndOfMessage is true.
        // Hint: a do { ... } while (condition); loop always runs at least once.
        // TODO 3: Return Encoding.UTF8.GetString(stream.ToArray()).
        throw new NotImplementedException();
    }

    /// <summary>
    /// Build intent JSON text. For example, BuildIntent("tick", "{\"steps\": 1}")
    /// returns {"type": "intent", "action": "tick", "args": {"steps": 1}}
    /// `argsJson` must already be JSON object text.
    /// </summary>
    public static string BuildIntent(string action, string argsJson)
    {
        // TODO: Join the pieces into one string with +.
        // Hint: inside a C# string literal, a double quote is written \"
        throw new NotImplementedException();
    }

    /// <summary>
    /// Send one intent. If not connected, log the warning "Not connected" and
    /// return. Otherwise log the JSON (format in the TODOs below), then send
    /// it as one UTF-8 text message. Log before sending, so the Console
    /// shows the request above its reply.
    /// </summary>
    public async Task SendIntent(string action, string argsJson)
    {
        // TODO 1: Check that socket is not null and socket.State is WebSocketState.Open.
        // TODO 2: Build the JSON and log it as "-> " + json.
        //   Then turn it into bytes with Encoding.UTF8.GetBytes.
        // TODO 3: await socket.SendAsync(new ArraySegment<byte>(bytes),
        //   WebSocketMessageType.Text, true, cancel.Token);
        //   The true means "this is the last piece of the message".
        throw new NotImplementedException();
    }

    /// <summary>
    /// Send a tick of one step. In Play mode, run it from this component's
    /// three-dot menu in the Inspector.
    /// </summary>
    [ContextMenu("Send tick")]
    private async void SendTick()
    {
        // TODO: await SendIntent with action "tick" and args {"steps": 1}.
        throw new NotImplementedException();
    }

    /// <summary>
    /// Unity calls this when Play mode stops. Cancel any receive still
    /// waiting, then dispose the socket. Both fields may still be null.
    /// </summary>
    private void OnDestroy()
    {
        // TODO: Cancel `cancel`, then Dispose `socket`.
        // Hint: x?.Method() calls Method only when x is not null.
        throw new NotImplementedException();
    }
}
```

Back in Unity, wait for the compile spinner at the bottom right to finish. Yellow warnings such as `CS1998` or `CS0169` are expected while TODOs remain, like ruff's `F401`. A red error means a typo.

### Step 4. Put the script in the scene

1. Open `Assets/Scenes/SampleScene` (double-click it in the Project window).
2. In the Hierarchy, click `+`, then `Create Empty`. Right-click the new `GameObject`, choose `Rename`, and type `SimClient`.
3. With it selected, click `Add Component` in the Inspector, type `SimClient`, and pick your script.
4. `File > Save` (Ctrl+S).

Why: a script only runs when it is attached to something in the scene.

### Step 5. Fill in the TODOs

Suggested order: `BuildIntent`, `OnDestroy`, `ReceiveMessage`, `ReceiveLoop`, `Start`, `SendIntent`, `SendTick`.

Why: this order starts with the simplest pieces. `Start` depends on `ReceiveLoop`, which depends on `ReceiveMessage`. Save after each one, and check that the Console shows no red errors.

### Step 6. Run it

1. In Git Bash: `source .venv/Scripts/activate`, then `python -m labsim.server`. Leave it running.
2. In Unity, open the Console with `Window > General > Console`, then press Play.

Expected in the Console:

```
Connected to ws://127.0.0.1:8765
<- {"type": "snapshot", "t": 0, "objects": {"a": {"value": 0.0}}}
```

3. With Play still running, select `SimClient` in the Hierarchy. In the Inspector, click the three-dot menu on the right of the `Sim Client (Script)` header, then `Send tick`. Expected:

```
-> {"type": "intent", "action": "tick", "args": {"steps": 1}}
<- {"type": "snapshot", "t": 1, "objects": {"a": {"value": -0.7312715117751976}}}
```

The Git Bash window shows `INFO:__main__:<- {"type": "intent", "action": "tick", "args": {"steps": 1}}`.

4. Stop Play. The server logs `INFO:websockets.server:connection closed` and then `INFO:__main__:client left without closing`, with no traceback.
5. Stop the server with Ctrl+C and press Play again. Within a few seconds, a yellow warning appears that ends with "Is the server running?". Stop Play.

Why: that is the whole bridge, both directions, plus the two ways a connection can end. The value `-0.7312715117751976` is the same first number as in your demo, because the seed is the same.

### Step 7. Commit and push

```bash
git status
git add unity
git commit -m "M2: Unity SimClient logs snapshots"
git push
```

`git status` should list `Assets/Scripts.meta`, `Assets/Scripts/SimClient.cs`, `Assets/Scripts/SimClient.cs.meta`, and `Assets/Scenes/SampleScene.unity`. Unity may also have touched a file under `ProjectSettings` or `Packages`. Tell me before committing anything else you do not recognize.

Why the `.meta` files matter: each one holds the ID Unity uses for that asset. The scene refers to your script by that ID, not by name. Commit a script without its `.meta` and, on a teammate's machine, the scene shows "Missing script". Always commit a file and its `.meta` together.

Checkpoint: step 6 output matches exactly, stopping Play leaves no traceback in the server window, and the push is on GitHub.

Design notes:
- The client uses .NET's built-in `ClientWebSocket` instead of a package such as NativeWebSocket. It ships with Unity and works in Windows and macOS standalone builds. It needs no package install, and after `await`, code resumes on Unity's main thread, so no message queue is needed. The trade-off is that it does not work in WebGL builds, which are not a target.
- The client logs raw text and does not parse snapshots yet. Unity's built-in `JsonUtility` cannot read the `objects` dictionary, so parsing is decided at M3, when something needs the values.
- `BuildIntent` joins strings by hand. That is fine for two fixed actions. It breaks if a name ever contains a quote, and M3 replaces it along with parsing.
- `SimClient` keeps no copy of the world. It passes messages through, following the rule that the snapshot is the whole truth.

### Check your understanding

1. Stop Play, then press Play again without restarting the server. What `t` does the first snapshot show, and why not 0? Which rule in `docs/ARCHITECTURE.md` explains it?
2. Experiment: outside Play mode, change `Url` in the Inspector to `ws://127.0.0.1:9999` and press Play. What appears? Why could you change it without editing code? Set it back afterwards.

Say "M2 done" to get M3.

## Done

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
