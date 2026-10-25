# Session log

One entry per session, newest first. Written on "save progress". Read the latest entry at session start.

## 2026-10-25

### Done
- Explored the repo end to end. State: M0 to M2 done, placeholder random-walk world, Unity client logs snapshots. The 2026-10-06 research docs were never committed.
- Switched the project from teaching mode to Claude as main developer and Justin as manager. Rewrote `CLAUDE.md` (new "Roles" section and rules), rewrote `/today` as a status-and-plan command, removed `/review`, restructured `docs/WORK_INSTRUCTIONS.md` (status, waiting on Justin, next tasks; machine notes and teaching-era history kept), updated `README.md`.
- Researched single-lake model papers. Wrote `docs/research/LAKE_MODEL_PAPERS.md`: Lake Washington (Arhonditsis and Brett 2005), Lake Zurich (Omlin et al. 2001), Peter and Paul Lakes (Carpenter et al. 2008), Lake Mendota GLM-AED, Lake Taihu SALMO.
- Recorded the art direction in `docs/VISION.md`: hand-drawn, black and white, made by the team, 2.5D like West of Loathing and Don't Starve Together. Claude integrates art as directed, never generates final art. Added "Art assets" conventions to `docs/ARCHITECTURE.md`.
- Added the sandbox directive: a lightweight, good-looking browser app on the real Python world state, for testing model changes and actions without Unity. Design in "Sandbox" in `docs/ARCHITECTURE.md`. Rule 10 in `CLAUDE.md`.
- Set up Git LFS: `.gitattributes` covers `art/**` and media files under `unity/client/Assets/Art/`. Ran `git lfs install --local`.
- Moved the Lake Washington PDF from the repo root to `papers/arhonditsis_brett_2005_lake_washington_part1.pdf`. `papers/` is gitignored.
- Fixed a stray null byte in this file (2026-10-05 entry) that made git treat it as binary.

### Decisions
- Claude is main developer; Justin directs and checks (Justin).
- Domain: a lake ecosystem. Starting model: Lake Washington, Arhonditsis and Brett 2005 (Justin).
- Milestones from M3: M3 lake core (Python), M4 sandbox, M5 Unity lake view, M6 cross-platform build (Justin accepted).
- Stocks-and-fluxes framework accepted "for now" (Justin).
- Art conventions accepted. Git LFS for art (Justin).
- Publisher PDFs are not committed.

### Open issues
- Only one of the two Lake Washington parts is in `papers/`. Which part it is gets confirmed on first read.
- Teaching-era carry-overs (unanswered check questions, no `/review`) are dropped. `SendIntent` still has no `try`/`catch` around `SendAsync`; fix when Unity work resumes in M5.

### Where we stopped
- Docs restructured, committed as `6ce7a66`, pushed to `origin/main`. CI run 40224392016 green. A follow-up commit added "New computer setup" to `README.md`.
- M3 not started. Justin has not said go.
- Context lives in the repo, not in Claude's local memory (`~/.claude/`, per machine). Everything needed to continue is in `CLAUDE.md` and `docs/`. The paper PDF is not in git: copy `papers/` by hand to a new computer.

### Next
- Justin says go on M3. First task: read the paper and write `docs/research/LAKE_WASHINGTON_MODEL.md`.

## 2026-10-06

### Done
- Session start: read the living docs. Repo clean at `4d87a3a`, last session's save was committed. M3 blocks still unwritten. The question "What did you finish since last time?" was asked but not answered.
- Research only, no code. Surveyed simulation engines Justin could use, judged on license (can a possibly commercial game bundle it), Windows plus Intel and Apple Silicon Mac support, Python 3.11 access, PyInstaller fit, per-tick stepping, and input data needs.
- Wrote `docs/research/AQUATIC_ENGINES.md`: lake and water-quality models (FABM, GLM-AED, PCLake, AQUATOX, and others), food-web and fish models (Ecopath with Ecosim, Rpath, PyPath, mizer, OSMOSE), agent frameworks (Mesa), chemistry and physics (PHREEQC, gsw, Parcels). Finding: none ships cleanly. Recommendation: our own NumPy/SciPy model, with PHREEQC (`phreeqc` package) for water chemistry if needed.
- Wrote `docs/research/FOREST_ENGINES.md` at Justin's request: FVS, iLand, LANDIS-II, SORTIE-ND, gap models, Landlab, Behave fire, pyet, pyRothC, and others, plus a forest vs aquatic comparison table. Same finding, more permissive building blocks (public-domain FVS and Behave, MIT Landlab).
- Added the Iowa State University Rain Forest Simulation Model (Ann E. Russell) as section 6 of the forest doc. ExtendSim, Windows only, archived, no license. Useful as a precedent and for its published Odum diagrams and parameters. Ask the author before copying parameter values.
- Discussed Justin's goal: one world-development framework where each mathematical model (aquatic or marine for now) is translated into code inside our own simulator, instead of launching separate software per ecosystem. Claude proposed a stocks-and-fluxes design (FABM pattern, our own code). Recorded in `docs/research/SIM_FRAMEWORK_PROPOSAL.md`.

### Decisions
- None final. Justin's goal (own framework, models translated into code) is recorded as a proposal, not yet in `docs/ARCHITECTURE.md`.
- Justin leans aquatic or marine "for now". Not recorded as the domain, because `CLAUDE.md` makes the domain a team decision. See open decision 1 in the proposal.

### Deviations from the instructions
- No `/today` this session, and no block work. The session was research and design discussion.
- New folder `docs/research/` for survey and proposal notes.

### Open issues
- Research docs are based on web sources. Items marked "unverified" in them still need checking. Nothing was benchmarked or frozen with PyInstaller.
- Carried over: unanswered check questions (M2-A, M2-B, M2-C), no `/review` of the Python files, `SendIntent` has no `try`/`catch`, Unity code editor setting never confirmed.

### Where we stopped
- Discussion of `docs/research/SIM_FRAMEWORK_PROPOSAL.md`. Claude asked three questions, unanswered: (1) record aquatic/marine as Justin's tentative pick or keep it out of the docs, (2) framework after M3 and M4 as M5 (recommended) or before M3, (3) if accepted, write it into `docs/ARCHITECTURE.md` and `docs/ROADMAP.md`.
- M3 blocks still not written.

### Next
- Commit this save: `git add docs`, `git commit -m "Docs: engine surveys and framework proposal"`, `git push`.
- Answer "What did you finish since last time?" and the three open questions in the proposal.
- Then either run `/today` for M3, or write the framework milestone if Justin chooses to start it first.

## 2026-10-05

### Done
- Session start: confirmed the temporary `Debug.Log(BuildIntent(...))` was already deleted and last session's docs were committed (`70ebda7`, `51730cc`).
- M2-C finished by Justin, one TODO at a time in chat: `OnDestroy`, `ReceiveMessage`, `ReceiveLoop`, `Start`, `SendIntent`, `SendTick`. From `OnDestroy` onward each TODO got the real code plus a line-by-line explanation (see Decisions).
- `OnDestroy` tested with a temporary `Debug.Log("OnDestroy ran")` as its last line: printed on stopping Play, no `NullReferenceException`. Line removed.
- Concepts taught in chat: `cancel` field vs `Cancel` method, `null` and `NullReferenceException`, why cancel before dispose, bytes and UTF-8, frames and `EndOfMessage`, arrays, `MemoryStream`, `using var`, `Task<string>`, `do`/`while`, `try`/`catch`, `async void`, `||` short-circuit, `[ContextMenu]` as an attribute, fields vs locals and shadowing, the WebSocket close handshake.
- Check questions Justin answered: `do`/`while` needed because `result` is empty before the first read (correction: it is a `CS0165` compile error, locals are not `null`); `result.Count` avoids trailing `\0` bytes (added: also stale bytes from earlier messages); polite close returns `null` (added: an abrupt drop throws into `Start`'s `catch`); missing `await` (correction: `CS0029` on the assignment line); `Start` stays quiet on stop because of `IsCancellationRequested`; `var socket` in `Start` (correction: compiles, `ReceiveLoop` throws `NullReferenceException` on the null field, and the local connection is never disposed). The first two `OnDestroy` questions Justin could not answer, so they were taught.
- All checkpoints passed in Play mode: server off gives the yellow warning; server on gives `Connected to ws://127.0.0.1:8765` and the `t: 0` snapshot; Send tick gives `t: 1` (`-0.7312715117751976`) then `t: 2` (`-0.03640403790073221`); stopping Play logs `client left without closing` in Git Bash; Ctrl+C on the server during Play gives "Server closed the connection" in Unity.
- Explained "client left without closing": the client dropped the connection without the close handshake. The server keeps running.
- Justin fixed the two stale "TODO below" docstring lines and committed `ff1996c` "Unity SimClient connection with snapshot logs and send tick mechanism", pushed. CI run 37401893559 green.
- M2 closed. M2-C moved to Done in `docs/WORK_INSTRUCTIONS.md`, M2 marked `[x]` in `docs/ROADMAP.md`.
- Added rule 12 to `CLAUDE.md` and step 6 to `.claude/commands/today.md`: all C# and Unity work is walked through in chat with real code and line-by-line explanations unless already covered. Added the "C# and Unity already covered" list to `docs/WORK_INSTRUCTIONS.md`.

### Decisions
- For C#, give the actual code for each TODO with a line-by-line explanation. Justin types it. No hint ladder for C#. Reason: Justin said he has almost no C# experience and cannot guess .NET or Unity API names ("you need to give me the code"). Python keeps the hint ladder (rule 3a).
- If Justin cannot answer a check question, teach the answer fully instead of hinting.
- "C# and Unity already covered" in `docs/WORK_INSTRUCTIONS.md` is the record of what no longer needs a full walkthrough. Updated after each C# TODO.

### Deviations from the instructions
- Justin's notes inside `SimClient.cs` method bodies use `///` instead of `//`. Works in Unity. Suggested `//` for ordinary comments. His call.
- The commit message differs from the doc's "M2: Unity SimClient logs snapshots". The commit also includes `docs/` and `SceneTemplateSettings.json`.
- Warning text in `Start` is "Lost the sim at ..." as given in the walkthrough.

### Open issues
- Correction to what Claude said in chat: server log lines read `INFO:__main__:...`, not `INFO:labsim.server:...` (module run as `__main__`). Recorded in Machine notes.
- `SendIntent` has no `try`/`catch` around `SendAsync`. If the server dies between the state check and the send, the exception escapes `SendTick` (`async void`). Rare locally. Revisit in M3 when sends come from input.
- Unanswered check questions: M2-C block (replay Play without restarting the server: which `t`; change `Url` to port 9999), `SendIntent` (why `socket == null` first; `t` after Play restart). Carried over: M2-A and M2-B questions, no `/review` of the Python files.
- M2-C step 1 (code editor setting in Unity) was never confirmed. VS Code with the C# extension works.

### Where we stopped
- M2 complete, committed (`ff1996c`), pushed, CI green. Working tree clean apart from this save.
- M3 blocks are not written yet.

### Next
- Commit this save: `git add CLAUDE.md .claude docs`, `git commit -m "Docs: close M2, add C# walkthrough rule"`, `git push`.
- Run `/today` to write M3 Minimal client. Decide Unity JSON parsing (likely `com.unity.nuget.newtonsoft-json`, see `docs/ARCHITECTURE.md`). Walk through every C# TODO per rule 12.

## 2026-10-03 (session 3)

### Done
- Explained loopback: `127.0.0.1` is reserved to mean "this computer" on every machine, traffic never leaves the machine, other computers cannot reach a server bound there, and the LAN address (`ipconfig`) is different. `localhost` usually resolves to it.
- Started M2-C as a one-TODO-at-a-time walkthrough in chat (Justin is new to C#). Gave a C# vs Python orientation table (`using`, classes, braces, `;`, types before names, `public`/`private`, `///` doc comments, `throw`, compile-time type checking).
- Steps 2, 3, and 4 done by Justin: `unity/client/Assets/Scripts/SimClient.cs` created from the skeleton (verified identical before editing), `SimClient` GameObject added to `SampleScene` with the script attached.
- `BuildIntent` done by Justin: builds the string in a local `intent` with `+` and `\"`, then returns it. Checked in Play mode with a temporary `Debug.Log(BuildIntent("tick", "{\"steps\": 1}"))` at the top of `Start`. Console showed exactly `{"type": "intent", "action": "tick", "args": {"steps": 1}}`.
- Debugged on the way: `CS0104 'Debug' is an ambiguous reference` because VS Code had added `using System.Diagnostics;`. Justin deleted it. Also caught the leftover `throw` above his `return` in `BuildIntent` (would have thrown, `CS0162` unreachable code). Fixed.
- Explained the Unity stack trace under a log line, including the compiler-generated `<Start>d__3:MoveNext` names for async methods.
- `OnDestroy` walkthrough was presented in chat (Unity calls methods by name, the Editor is one long-lived process, `null` and `NullReferenceException`, `?.`, `Cancel` then `Dispose`, `Dispose` closes abruptly so the server logs "client left without closing"). Justin has not written it yet.

### Decisions
- M2-C goes one TODO at a time in chat, in the doc's order: `BuildIntent`, `OnDestroy`, `ReceiveMessage`, `ReceiveLoop`, `Start`, `SendIntent`, `SendTick`.
- Use a temporary `Debug.Log` in `Start` as a checkpoint for pieces that cannot run on their own yet. Delete it afterwards.

### Deviations from the instructions
- `BuildIntent` uses a local variable and two blank lines before the closing brace. Works the same.

### Open issues
- Temporary `Debug.Log(BuildIntent(...))` line is still at the top of `Start`, with a blank line above it. Delete it before continuing.
- Nothing from M2-C is committed. Untracked: `Assets/Scripts.meta`, `Assets/Scripts/` (`SimClient.cs` and its `.meta`), `ProjectSettings/SceneTemplateSettings.json`. Modified: `Assets/Scenes/SampleScene.unity`.
- `BuildIntent` check questions unanswered: why it is `static`; what a missing `\` does to the whole script.
- Carried over: M2-B and M2-A check questions; no `/review` of the Python files.

### Where we stopped
- M2-C step 5, `BuildIntent` done. Next TODO is `OnDestroy`. Re-present its walkthrough briefly at the start of next session, since Justin read it but did not start.

### Next
- Commit these docs: `git add docs`, `git commit -m "Docs: save progress"`, `git push`.
- Delete the temporary `Debug.Log` line in `Start`.
- `OnDestroy`, then `ReceiveMessage` (bytes, buffers, `do`/`while`, `MemoryStream`), one TODO at a time.

## 2026-10-03 (session 2)

### Done
- M2-B done by Justin: `sim/labsim/server.py` and `sim/tests/test_server.py`. At his request, walked through every TODO one at a time in chat (he had no async or WebSocket experience). Order: `handle_connection` TODOs 1 to 4, `make_server`, `serve_forever`, `main`.
- Concepts covered in chat: `await` and coroutines, the "never awaited" warning, `async for` over a connection, closing vs vanishing clients and `ConnectionClosedError`, `logging` (levels, named loggers, stderr, no file by default, `filename=` option), callbacks and closures, `async with` starting and stopping the server, async spreading upward to `asyncio.run`, running several coroutines with `asyncio.TaskGroup` or `gather` instead of several `asyncio.run` calls.
- Justin answered the per-TODO check questions in chat: `make_server` runs once and `handler` once per client; the world is shared because `World(...)` is built once in `main` and passed by reference; a missing `await` on `server.serve_forever()` ends the `async with` and stops the server; `serve_forever` is async because it awaits; Ctrl+C exits the `async with`, which frees the port; without the `try/except`, the `KeyboardInterrupt` traceback runs through `main`, `asyncio.run`, and `serve_forever`.
- Verified by Claude: `pytest sim` 29 passed, `ruff check sim` all checks passed.
- Committed `e1e31d9` "websocket server and tests" and pushed. CI run 37171861832 green.
- Added a Machine note: Ctrl+C on the server in Git Bash shuts down cleanly.
- Moved M2-B to Done in `docs/WORK_INSTRUCTIONS.md`. Updated the M2 status line in `docs/ROADMAP.md`.

### Decisions
- Snapshot send moved inside the `try` in `handle_connection`, so a client that vanishes before the snapshot is logged at INFO instead of a traceback. Cost is a slightly wider `try`, acceptable because the `except` only catches `ConnectionClosedError`.
- For new territory, guide one TODO at a time in chat: why, concepts, steps, checkpoint, check questions. Then wait for Justin's code before the next TODO.

### Deviations from the instructions
- Snapshot send is inside the `try` (see Decisions), with a comment in the code.
- Commit message was "websocket server and tests", not "M2: protocol and websocket server".
- Justin removed the `# Provided` markers from `sim/tests/test_protocol.py` (committed in `e1e31d9`). Each removal left three blank lines between tests instead of two. Default ruff rules do not flag it.
- `server.py` style: blank lines inside `try`, `except`, and loop bodies, a leading space in the log format `" <- %s"`, extra blank lines before `if __name__`, and single quotes in `set_value(world=world, name='a', value=0.0)`. All pass `ruff check`. `ruff format` would change most of them.

### Open issues
- Docs from the first 2026-10-03 save were never committed. This save's doc changes are uncommitted too.
- M2-B "Check your understanding" questions unanswered (listed in the Done entry in `docs/WORK_INSTRUCTIONS.md`). M2-A questions still unanswered.
- `protocol.py`, `server.py`, `world.py`, `actions.py`, and `demo.py` have not been through `/review`.
- Carried over: M2-C menu path `Create > Scripting > MonoBehaviour Script` and ClientWebSocket under Unity Mono are unconfirmed on `6000.0.84f1`.

### Where we stopped
- M2-B complete, committed, pushed, CI green.
- Next action is M2-C step 1 (set the code editor in Unity), then step 3 `SimClient.cs` from the skeleton.

### Next
- Commit the docs: `git add docs` then `git commit -m "Docs: save progress"`, then push.
- Optional: answer the M2-B check questions.
- Start M2-C. Walk through the C# TODOs one at a time, the same way as `server.py`. C# `async`/`await` and `ClientWebSocket` are new to Justin.

## 2026-10-03

### Done
- M2-A done by Justin: `sim/labsim/protocol.py` and `sim/tests/test_protocol.py`, including his two tests. `pytest sim` 26 passed, `ruff check sim` clean (verified by Claude).
- Committed `3a4ef52` "M2-A: protocol.py and tests" and pushed. CI run 37108975814 green.
- An accidental edit to `docs/WORK_INSTRUCTIONS.md` (deleted `# TODO: write this test` line) was restored before the commit.
- Discussion, no code: message based vs streamed protocols. Framing (messages vs byte stream) and initiation (request/reply vs push) are separate axes. Our protocol is message based, request/reply. Running the sim on its own clock would add server push and stay message based. At larger scale the fixes are deltas, a lower send rate with interpolation, sending only what Unity needs, binary encoding (MessagePack, Protocol Buffers), and compression. All of these stay message based. A byte stream only fits a single huge transfer.
- Explained `ruff check sim` (lint, what CI runs) vs `ruff format --check sim` / `--diff` / `ruff format sim` (formatter, not in CI).
- Moved M2-A to Done in `docs/WORK_INSTRUCTIONS.md`. Updated the M2 status line in `docs/ROADMAP.md`.

### Decisions
- Keep the protocol message based. Add server push later if the sim needs its own clock. No byte stream. Optimize only after measuring. Python and Unity share `127.0.0.1`, so Python step time or Unity JSON parsing will likely limit first, not bandwidth.
- Formatter (`ruff format`) stays optional and out of CI for now.

### Deviations from the instructions
- `protocol.py` has an extra header comment and a blank line between each `def` and its docstring. The tests do the same. `ruff format` would remove the blank lines.
- `test_bad_argument_is_an_error_and_world_unchanged` compares against a literal dict with the exact message `steps must be at least 1` instead of `make_error(...)` or checking only `"type"`. It passes, but it couples the test to the wording in `actions.py`.
- `protocol.py` has no newline at the end of the file. Default ruff rules do not flag it.

### Open issues
- `protocol.py`, `world.py`, `actions.py`, and `demo.py` have not been through `/review`.
- M2-A "Check your understanding" questions unanswered (listed in the Done entry in `docs/WORK_INSTRUCTIONS.md`).
- Carried over: M2-C menu path `Create > Scripting > MonoBehaviour Script` and ClientWebSocket under Unity Mono are unconfirmed on `6000.0.84f1`. Ctrl+C behaviour from Git Bash for the server is unknown (M2-B step 4 asks).

### Where we stopped
- M2-A complete, committed, pushed, CI green. Working tree clean before this save.
- Next action is M2-B step 1: create `sim/labsim/server.py` from the skeleton.

### Next
- Commit this save: `git add docs` then `git commit -m "Docs: save progress"`, then push.
- Optional: answer the two M2-A check questions; run `/review sim/labsim/protocol.py`.
- Start M2-B step 1.

## 2026-09-23

### Done
- Rewrote M1 blocks A to D as skeleton handoffs: imports, signatures, docstrings, TODO comments with hints. Provided acceptance tests; 5 tests in `test_actions.py` left for Justin to write. Added "Concepts you will need" lists with doc links.
- Updated `CLAUDE.md` role and rules 3, 3a, 4, 5; `/today` step 5; `/review` step 2.
- M1-A and M1-B done by Justin: `pytest sim` 14 passed, `ruff check sim` clean.
- M1-C done: `sim/labsim/demo.py`, committed as `32a800a`.
- M1-D done, guided in chat: Justin wrote `.github/workflows/tests.yml` (commit `77c0ea5`). First run failed on ruff, fixed in `84822f0`. Bumped `actions/checkout` and `actions/setup-python` to `@v7` in `3219413` to clear the Node.js 20 deprecation warning. Deliberate failure on branch `ci-check` went red with `assert 3 == 4`; branch deleted locally and remotely. Status badge added to `README.md` (`fbbbd2b`). Run 35929303103 on `main`: 4 green jobs, no warnings.
- Justin answered the M1-D check questions: the runner starts empty, so checkout is needed; failures on both macOS jobs point at an OS problem. The OS vs Python version vs combination reasoning was explained.
- M1 closed. Moved M1-C and M1-D to Done in `docs/WORK_INSTRUCTIONS.md`, marked M1 `[x]` in `docs/ROADMAP.md`.
- Wrote M2 blocks: M2-A `protocol.py` (`make_error`, `handle_message`, 12 tests, 2 for Justin), M2-B `server.py` (`handle_connection`, `make_server`, `serve_forever`, `main`, 3 provided tests over a real connection), M2-C Unity `SimClient.cs` (ClientWebSocket, Console logging, `[ContextMenu("Send tick")]`).
- Verified M2 in the scratchpad: Python reference passes all 29 tests and ruff; skeletons fail the 15 new tests cleanly with only the expected F401s. C# reference and skeleton both compile against Unity stubs on .NET 8 with C# 9. The reference client ran against the reference server: `t` 0 then 1 with `a` = `-0.7312715117751976`, then 2. Server log clean on client exit. Doc skeleton text checked to match the verified files exactly.
- Justin committed and pushed the docs (`3dd28c1`) and removed the leftover skeleton comments in `demo.py` and the `Hint` line in `actions.py` (`b67f60e`).
- Updated `docs/ARCHITECTURE.md` (protocol module, server behaviour, Unity WebSocket decision, JSON parsing moved to open decisions) and `docs/ROADMAP.md` (M2 `[~]`). Added two Machine notes (port 8765 in use, Input System only).

### Decisions
- Instruction style is a staff engineer skeleton handoff. Hints escalate one step at a time on request. Reference solutions live only in the scratchpad.
- Unity WebSocket library: .NET built-in `ClientWebSocket`, not NativeWebSocket. No package install, works on Windows and macOS standalone, resumes on the main thread after `await`. No WebGL, which is not a target.
- Message handling lives in its own module, `protocol.py`, separate from `server.py`, so every message case is tested without a network.
- One `World` per server process, shared by all connections. The server sends a snapshot on connect. It binds to `127.0.0.1:8765` and logs with `logging` rather than `print` (Git Bash can buffer `print`).
- The server treats a client leaving without a close handshake as normal (INFO line). Found during verification: without this, every Unity Play stop printed a traceback.
- M2-C sends intents from a `[ContextMenu]` instead of a key press, because the project uses the new Input System only and input handling belongs to M3.
- Unity JSON parsing deferred to M3. `JsonUtility` cannot read the `objects` dictionary.

### Deviations from the instructions
- `demo.py` calls `apply(...)` instead of `set_value` and `tick` directly. Output is identical.
- `tests.yml` uses 4 space indentation (the skeleton used 2). Valid and consistent.
- Action versions are `@v7`, not the `@v4` and `@v5` in the skeleton, to avoid the Node.js 20 deprecation.

### Open issues
- `actions.py` `apply` still has the comment "Reject unknown names, then look up the function and call it." It reads fine as a normal comment, so keeping it is Justin's call.
- `world.py`, `actions.py`, and `demo.py` have not been through `/review`.
- Two M2-C details are unconfirmed on Justin's editor `6000.0.84f1`: the exact menu path `Create > Scripting > MonoBehaviour Script` (a fallback is written into the step), and ClientWebSocket behaviour under Unity's Mono. It was verified on .NET 8 only.
- Unknown whether Ctrl+C from Git Bash lets Python print `server stopped`. M2-B step 4 asks Justin to report it for Machine notes.

### Where we stopped
- M1 done and pushed. M2 blocks written and pushed. Last commit `b67f60e`. Working tree clean apart from this save.
- M2 not started. Next action is M2-A step 1.

### Next
- Open Git Bash at the repo root and run `source .venv/Scripts/activate`.
- Commit this save: `git add docs` then `git commit -m "Docs: save progress"`, then push.
- Start M2-A step 1: create `sim/labsim/protocol.py` from the skeleton.

## 2026-09-22

### Done
- Session start review of docs and repo state.
- Added the "Save progress" procedure to `CLAUDE.md` and created this log.
- Added the list of paths `.gitignore` must cover to Block C in `docs/WORK_INSTRUCTIONS.md`.
- Created `docs/VISION.md` recording Justin's art direction (West of Loathing, Don't Starve Together, Deadly Days: Roadtrip, Octopath Traveler 0, Paper Mario).
- Switched the Unity template from Universal 2D to Universal 3D in `CLAUDE.md`, `docs/ROADMAP.md`, `docs/WORK_INSTRUCTIONS.md`, `docs/ARCHITECTURE.md`.
- Block B done. `unity/client` created on `6000.0.84f1` from Universal 3D, URP 17.0.4. First attempt used editor 2022.3.62f1 and the Built-In 3D template, so it was deleted and redone.
- Wrote Block C with the exact `.gitignore` patterns. Justin completed it: commit `53753b9`, pushed to `origin/main`, 73 tracked files. M0 closed.
- Explained what `sim/pyproject.toml`, pytest, and ruff are for, how `import labsim` resolves, and how the server gets started (added shipping options to `docs/ARCHITECTURE.md`).
- Wrote M1 blocks A, B, C. Added a "Why" paragraph to the milestone and each block.

### Decisions
- "Save progress" and similar phrases now trigger a full write-up across the living docs. Procedure lives in `CLAUDE.md`.
- Unity template is Universal 3D (URP 3D). Reason: the references mostly put 2D sprites in a 3D world with lighting, shadows, and depth of field. 3D also covers flat 2D, and switching later is costly.
- Every milestone and block now opens with a "Why" paragraph. Rule 8 in `CLAUDE.md`, step 4 in `/today`.
- Terminal commands are written for Git Bash from now on. Recorded in `CLAUDE.md` Stack section and Machine notes.
- Target platforms are Windows and macOS. Added "Platforms" to `docs/ARCHITECTURE.md` and milestone M4 Cross-platform build to `docs/ROADMAP.md`.
- About half the team has Macs. Explained how GitHub Actions works.
- GitHub Actions is the official check that code works on both OSes. Added Block M1-D (test workflow on Windows and macOS, Python 3.11 and 3.13).
- Teaching style changed: work instructions now give full code, verified in the scratchpad, with part by part explanations and "Check your understanding" questions. `CLAUDE.md` role and rules rewritten, `/today` and `/review` updated. M1 blocks rewritten to match.
- Validation errors use `TypeError` for wrong types and `ValueError` for bad values (ruff rule TRY004 is on by default in ruff 0.16.8). M1 now has 14 tests.
- Kept the project name `client`. Hub tracks projects by path, so a second `client` elsewhere is harmless.

### Where we stopped
- M0 Tooling done and pushed. M1 Sim core not started.

### Next
- M1 blocks written in `docs/WORK_INSTRUCTIONS.md` (M1-A World, M1-B Actions, M1-C Demo, M1-D GitHub Actions). Start at M1-A step 1.

## 2026-09-21

Reconstructed from `docs/WORK_INSTRUCTIONS.md` "Done" section.

### Done
- Repo restructure. Promoted the template from `instructions/labsim-template/labsim/` to the repo root and deleted `instructions/`.
- Block A (Python). `.venv` at the repo root, `sim/pyproject.toml`, empty `__init__.py` files in `sim/labsim` and `sim/tests`, `pip install -e "sim[dev]"`. Checkpoint passed.

### Deviations from the instructions
- `websockets` is a runtime dependency rather than a `dev` extra, because `server.py` needs it at M2.
