# Work instructions

Rewritten by `/today` each session. Finished blocks move to "Done".

Milestone: M2 Bridge. Blocks M2-A to M2-C written 2026-09-23. Start at M2-A step 1.

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

## Block M2-A: Message handling

Why: the server has two jobs. One is moving bytes over the network. The other is deciding what a message means and what to answer. Mixed together, every test would need a real network connection. This block writes the second job as a plain function: text in, reply out. You can test every bad message Unity might ever send, in milliseconds, with no network. The server in M2-B then becomes a thin wrapper around this function. It also enforces an important rule: a bad message gets an error reply, never a crash, so one buggy click in Unity cannot take the sim down.

Goal: `handle_message` turns any text into either a snapshot or an error reply, and 12 new tests pass.

Concepts you will need:
- **Protocol.** The agreed rules for which messages two programs exchange. Ours is the "Messages" section of `docs/ARCHITECTURE.md`: intents go in, snapshots or errors come out.
- **JSON.** A text format for data that almost every language can read. A JSON object `{...}` becomes a Python `dict`, an array `[...]` becomes a `list`, and `true`, `false`, `null` become `True`, `False`, `None`. Docs: https://docs.python.org/3/library/json.html
- **`json.loads` and `json.dumps`.** `loads` reads JSON text into Python values ("load string"). `dumps` writes Python values out as JSON text ("dump string"). `loads` raises `json.JSONDecodeError` when the text is not valid JSON.
- **`try` / `except`.** Runs code and catches a named exception if it is raised, instead of crashing. `except (A, B) as exc:` catches either type and names the exception object `exc`. `str(exc)` gives its message. Catch only the exceptions you expect, so real bugs still show up. Docs: https://docs.python.org/3/tutorial/errors.html
- **`dict.get(key, default)`.** Returns the value for `key`, or `default` if the key is missing. Without a default it returns `None`. It never raises, unlike `d[key]`.
- **`X | None` in a type hint.** Means "an X, or None". Used in the test helper.

### Step 1. Create `sim/labsim/protocol.py` from this skeleton

Why: this is the "what does a message mean" half of the server, kept separate so it can be tested without a network.

```python
"""Turn one incoming message into one reply. No networking here."""

import json

from labsim.actions import apply
from labsim.world import World


def make_error(message: str) -> dict:
    """Return an error reply: {"type": "error", "message": message}."""
    # TODO: Return the dict described in the docstring.
    raise NotImplementedError


def handle_message(world: World, text: str) -> dict:
    """Parse one intent from JSON text, apply it to `world`, return the reply.

    A valid intent is a JSON object such as
        {"type": "intent", "action": "tick", "args": {"steps": 1}}
    "args" may be left out, which means no arguments ({}).

    Returns:
        world.snapshot() if the intent was applied.
        make_error(...) otherwise, with these messages:
          - text is not valid JSON: "invalid JSON"
          - the JSON is not an object, "type" is not "intent", or "action"
            is not a string: "expected an intent"
          - "args" is present but is not an object: "args must be an object"
          - apply() raises TypeError or ValueError: str() of that exception

    Never raises. The server must survive any message a client sends.
    """
    # TODO 1: Parse the text. json.loads raises json.JSONDecodeError on bad
    #   JSON. Catch that one exception and return the matching error.
    # TODO 2: Check the shape. A JSON object becomes a Python dict.
    # Hint: isinstance(x, dict), and dict.get(key) returns None instead of
    #   raising when the key is missing.
    # TODO 3: Get args with a default of {}, then check that it is a dict.
    # Hint: dict.get(key, default)
    # TODO 4: Call apply inside try/except (TypeError, ValueError).
    # Hint: `except (A, B) as exc:` gives you the exception object as exc.
    # TODO 5: Return the snapshot.
    raise NotImplementedError
```

### Step 2. Create `sim/tests/test_protocol.py` from this skeleton

Why: the provided tests pin down the exact replies Unity will rely on. The two TODO tests are yours to write.

```python
import json

import pytest
from labsim.protocol import handle_message, make_error
from labsim.world import World


def intent(action: str, args: dict | None = None) -> str:
    """Helper, not a test: build intent JSON text the way Unity will."""
    message = {"type": "intent", "action": action}
    if args is not None:
        message["args"] = args
    return json.dumps(message)


# Provided
def test_make_error_shape():
    assert make_error("boom") == {"type": "error", "message": "boom"}


# Provided
def test_tick_intent_returns_snapshot():
    world = World()
    reply = handle_message(world, intent("tick", {"steps": 2}))
    assert reply["t"] == 2
    assert reply == world.snapshot()


# Provided
def test_args_can_be_left_out():
    world = World()
    reply = handle_message(world, intent("tick"))
    assert reply["t"] == 1


# Provided
def test_invalid_json_is_an_error():
    world = World()
    assert handle_message(world, "{not json") == make_error("invalid JSON")


# Provided
@pytest.mark.parametrize(
    "text",
    [
        "[]",
        '"hello"',
        '{"type": "snapshot"}',
        '{"type": "intent"}',
        '{"type": "intent", "action": 5}',
    ],
)
def test_not_an_intent_is_an_error(text):
    world = World()
    assert handle_message(world, text) == make_error("expected an intent")


# Provided
def test_unknown_action_is_an_error_and_world_unchanged():
    world = World()
    reply = handle_message(world, intent("fly"))
    assert reply["type"] == "error"
    assert world.t == 0


# TODO: write this test
def test_args_must_be_an_object():
    """Sending "args": [1, 2] gives make_error("args must be an object")."""
    # Hint: intent() takes a dict, but json.dumps accepts a list too, so you
    #   can pass [1, 2] to it anyway, or write the JSON text by hand.
    pytest.fail("not written yet")


# TODO: write this test
def test_bad_argument_is_an_error_and_world_unchanged():
    """tick with steps 0 gives an error reply, and world.t stays 0."""
    # Hint: which exception does tick raise for steps 0, and what does
    #   handle_message turn it into?
    pytest.fail("not written yet")
```

### Step 3. Fill in the TODOs and run the tests

```bash
pytest sim/tests/test_protocol.py
```

Why: red to green, one TODO at a time. Start with `make_error`, since every error case depends on it. Then write your two tests. Watch each one fail before you make it pass.

Checkpoint: `pytest sim` reports `26 passed`. `ruff check sim` reports `All checks passed!`.

Design notes:
- `protocol.py` knows nothing about networks, and `server.py` (M2-B) knows nothing about message rules. Each can change without touching the other.
- Errors are replies, not exceptions. An exception inside the server would drop the client's connection. An error reply keeps the conversation going and tells Unity what went wrong.
- "World unchanged on error" holds because your `set_value` and `tick` validate their arguments before changing anything. Keep it that way for every future action.

### Check your understanding

1. `handle_message` promises to never raise. What would happen to the connection if it did raise on a bad message?
2. Experiment: in `python`, run `import json`, then `json.loads("3.10")` and `json.loads('"3.10"')`. What type comes back from each? Which lesson from the CI YAML does this echo?

## Block M2-B: WebSocket server

Why: now the network half. The server owns the one `World`, listens on a port, and answers every message with the reply from `handle_message`. It sends a snapshot the moment a client connects, so Unity can show the world before it has asked anything. During development you start this process by hand in a terminal before pressing Play in Unity (see "Open decisions" in `docs/ARCHITECTURE.md`). Without it, `protocol.py` is a library Unity has no way to reach.

Goal: `python -m labsim.server` listens on `127.0.0.1:8765`, and 3 provided tests prove it over a real connection.

Concepts you will need:
- **WebSocket.** A network connection that stays open, so either side can send a message at any time. A normal web request is one question and one answer, then the connection closes. Addresses look like `ws://host:port`.
- **Host and port.** `127.0.0.1` means "this computer" (called loopback). A port is a numbered door on that computer. Ours is 8765. Only one program can listen on a given port at a time.
- **`async def`, `await`, and the event loop.** A server spends most of its time waiting for messages. `async def` defines a coroutine: a function that can pause. `await` pauses it until the awaited thing is done, and lets other work run meanwhile. The event loop is the scheduler that resumes coroutines when their wait is over. `asyncio.run(...)` starts the loop. This lets one Python process serve several clients without threads. Docs: https://docs.python.org/3/library/asyncio-task.html
- **`async with` and `async for`.** The waiting versions of `with` and `for`. `async for message in connection:` waits for each message and ends when the client disconnects.
- **Closure.** A function defined inside another function can use the outer function's variables, even after the outer function has returned. You use one to hand the world to the connection handler.
- **`logging`.** Python's standard way for programs to report what they are doing, with levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`). `logging.basicConfig(level=logging.INFO)` shows INFO and above. `logging.getLogger(__name__)` gives each module its own named logger. Why not `print`: in Git Bash, Python can hold printed text in a buffer, so lines show up late or only at exit. Logging writes to stderr, which shows up right away, and the `websockets` library already logs this way. Docs: https://docs.python.org/3/howto/logging.html
- **`KeyboardInterrupt`.** The exception Python raises when you press Ctrl+C.
- **The `websockets` library.** Already installed as a dependency since M0. You use its asyncio server: `serve(...)` creates a server, and each connected client arrives in your handler as a `ServerConnection`. `connection.send(text)` sends one message. Docs: https://websockets.readthedocs.io/en/stable/reference/asyncio/server.html

### Step 1. Create `sim/labsim/server.py` from this skeleton

Why: this is the process Unity talks to. It is also your second `python -m` entry point, following the same pattern as `demo.py`.

```python
"""WebSocket server. Unity connects here, sends intents, gets snapshots.

Run it with:  python -m labsim.server
Stop it with: Ctrl+C
"""

import asyncio
import json
import logging

from websockets.asyncio.server import ServerConnection, serve
from websockets.exceptions import ConnectionClosedError

from labsim.actions import set_value
from labsim.protocol import handle_message
from labsim.world import World

HOST = "127.0.0.1"  # This machine only. Other computers cannot connect.
PORT = 8765

logger = logging.getLogger(__name__)


async def handle_connection(connection: ServerConnection, world: World) -> None:
    """Serve one client until it disconnects.

    First send world.snapshot() as JSON, so the client can draw right away.
    Then, for every message received: log it at INFO level, pass it to
    handle_message, and send the reply back as JSON.
    Returns when the client disconnects. If the client vanishes without
    closing properly (Unity does this when you stop Play mode), log
    "client left without closing" at INFO level and return normally.
    """
    # TODO 1: Send the first snapshot.
    # Hint: `await connection.send(some_string)`, and json.dumps turns a
    #   dict into a JSON string.
    # TODO 2: Loop over incoming messages until the client leaves.
    # Hint: `async for message in connection:` ends by itself on disconnect.
    # TODO 3: Inside the loop: logger.info("<- %s", message), then reply.
    # TODO 4: Wrap the loop in try/except ConnectionClosedError. Without it,
    #   websockets prints a full traceback every time you stop Play mode.
    raise NotImplementedError


def make_server(world: World, host: str = HOST, port: int = PORT) -> serve:
    """Return a server, not yet started, that serves `world` to every client.

    Start it with:  async with make_server(world) as server: ...
    Every connection shares the same `world`.
    Port 0 asks the operating system for any free port. The tests use that.
    """
    # TODO: Call serve(handler, host, port) and return the result.
    #   serve calls handler(connection) with one argument, but
    #   handle_connection also needs the world.
    # Hint: define a small `async def handler(connection)` inside this
    #   function that awaits handle_connection(connection, world). The inner
    #   function can see `world` because it is defined inside make_server.
    raise NotImplementedError


async def serve_forever(world: World) -> None:
    """Start the server on HOST:PORT and keep it running until stopped."""
    # TODO: Start make_server(world) with `async with ... as server:`, then
    #   `await server.serve_forever()` inside it.
    raise NotImplementedError


def main() -> None:
    """Turn on INFO logging, build World(seed=1) holding "a" at 0.0, and run
    serve_forever until Ctrl+C. On Ctrl+C, log "server stopped" and return
    without a traceback."""
    # TODO 1: logging.basicConfig(level=logging.INFO)
    # TODO 2: Build the world with set_value.
    # TODO 3: asyncio.run(serve_forever(world)) inside try/except.
    # Hint: Ctrl+C raises KeyboardInterrupt.
    raise NotImplementedError


if __name__ == "__main__":
    main()
```

### Step 2. Create `sim/tests/test_server.py` (Provided, whole file)

Why: these tests start a real server and connect a real client, so they prove the network half works. `talk` is a helper that does the connecting. Port 0 lets the operating system pick a free port, so the tests never collide with a server you have running.

```python
import asyncio
import json

from labsim.server import make_server
from labsim.world import World
from websockets.asyncio.client import connect


def talk(world: World, messages: list[str]) -> list[dict]:
    """Helper, not a test: start a real server on a free port, connect as a
    client, send each message, and return every reply as a dict. The first
    reply is the snapshot the server sends on connect."""

    async def scenario() -> list[dict]:
        async with make_server(world, port=0) as server:
            port = server.sockets[0].getsockname()[1]
            async with connect(f"ws://127.0.0.1:{port}") as client:
                replies = [json.loads(await client.recv())]
                for message in messages:
                    await client.send(message)
                    replies.append(json.loads(await client.recv()))
        return replies

    return asyncio.run(scenario())


# Provided
def test_sends_snapshot_on_connect():
    replies = talk(World(), [])
    assert replies == [{"type": "snapshot", "t": 0, "objects": {}}]


# Provided
def test_intent_gets_snapshot_reply():
    tick = json.dumps({"type": "intent", "action": "tick", "args": {"steps": 1}})
    replies = talk(World(), [tick])
    assert replies[1]["type"] == "snapshot"
    assert replies[1]["t"] == 1


# Provided
def test_bad_message_gets_error_and_connection_survives():
    tick = json.dumps({"type": "intent", "action": "tick"})
    replies = talk(World(), ["not json", tick])
    assert replies[1] == {"type": "error", "message": "invalid JSON"}
    assert replies[2]["t"] == 1
```

### Step 3. Fill in `handle_connection` and `make_server`, then run the tests

```bash
pytest sim/tests/test_server.py
```

Why: the tests only use these two functions. Get them green first, then do `serve_forever` and `main` in step 4, which you check by hand.

### Step 4. Fill in `serve_forever` and `main`, then run the server by hand

```bash
python -m labsim.server
```

Why: this is how you will start the sim every time you work in Unity.

Expected output:

```
INFO:websockets.server:server listening on 127.0.0.1:8765
```

The command does not return. The server is waiting for clients. Press Ctrl+C to stop it. You should see `INFO:__main__:server stopped` and get your prompt back. If Git Bash ends Python too abruptly for that line to print, that is fine as long as no traceback appears. Tell me which one you saw, so I can record it in Machine notes.

If you see `OSError: [Errno 10048] ... only one usage of each socket address` (on macOS: `[Errno 48] Address already in use`), a server is already running in another terminal. Stop that one first.

### Step 5. Commit and push

```bash
git status
git add sim
git commit -m "M2: protocol and websocket server"
git push
```

Why: this is the first test that opens a network connection. CI proves it also works on a fresh macOS machine.

Checkpoint: `pytest sim` reports `29 passed`, `ruff check sim` is clean, the server prints the listening line, and the Actions run shows 4 green jobs.

Design notes:
- One `World` per server process, shared by every connection. The snapshot is the whole truth, so there must be exactly one world.
- `HOST` is `127.0.0.1`, not `0.0.0.0`. Only programs on this computer can connect. That is safer, and it avoids firewall prompts on Windows and macOS.
- `make_server` returns a server that has not started yet. The caller decides the port and when to start it. That is what lets the tests use port 0.
- A client that vanishes without a proper goodbye is normal. Unity does it every time you stop Play mode. Catching `ConnectionClosedError` turns that into one INFO line instead of a traceback.

### Check your understanding

1. The tests use port 0 instead of 8765. What would go wrong if they used 8765 while your own server was running in another terminal?
2. Two clients are connected and one sends `tick`. Read `handle_connection`. Does the other client see the new snapshot right away? Why or why not?

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
