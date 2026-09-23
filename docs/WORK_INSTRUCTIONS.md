# Work instructions

Rewritten by `/today` each session. Finished blocks move to "Done".

Milestone: M1 Sim core, no networking. Blocks M1-A and M1-B done (2026-09-23). Resume at M1-C step 1.

Why M1: the Python sim core is the brain of the project. Every number Unity ever shows comes from it, and Unity only displays and asks. Building it first, with no networking and no Unity, means you can prove the rules are correct with fast automated tests. Later, when something looks wrong on screen, passing tests tell you the bug is in the bridge or the client, not the rules. Debugging all three layers at once is much harder than debugging one.

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

## Block M1-C: Demo and commit

Why: tests check pieces in isolation. The demo runs the whole core end to end the way a real consumer will: build a world, apply actions, read snapshots. It is the M1 roadmap checkpoint and your first `python -m` entry point, the same pattern `server.py` uses at M2. Running it twice and getting identical output is the visible proof of determinism. Committing here locks in a known good core before networking adds new ways for things to break.

Goal: `python -m labsim.demo` prints ten snapshots, identical on every run.

Concepts you will need:
- **`__name__`.** Every module has this built in variable. When you run a file directly, Python sets it to `"__main__"`. When the file is imported, it is the module's name instead. The `if __name__ == "__main__":` guard makes code run only when launched on purpose.
- **`python -m package.module`.** Runs a module found by its import name, from any folder, thanks to the editable install.

### Step 1. Create `sim/labsim/demo.py` from this skeleton

```python
"""Run a seeded world for 10 ticks and print each snapshot."""

from labsim.actions import set_value, tick
from labsim.world import World


def main() -> None:
    """Build World(seed=1), add "a" at 0.0 then "b" at 10.0, then tick 10
    times, printing the snapshot after each tick."""
    # TODO: Implement using only World, set_value, tick, and print.
    raise NotImplementedError


if __name__ == "__main__":
    main()
```

### Step 2. Run it twice

```bash
python -m labsim.demo
python -m labsim.demo
```

The reference implementation prints this as its first line:

```
{'type': 'snapshot', 't': 1, 'objects': {'a': {'value': -0.7312715117751976}, 'b': {'value': 10.694867473874465}}}
```

If yours matches character for character, your `tick` does exactly what the docstring specifies, on a different machine. If both of your runs are identical to each other but differ from this line, your code is deterministic but uses a different random call or order than the docstring asks for. Reread the `tick` docstring.

### Step 3. Commit and push

```bash
git status
git add -A
git commit -m "M1: world state, actions, tests, demo"
git push
```

Read `git status` before adding. You should see only your new files under `sim/`.

Checkpoint: 10 snapshots with `t` from 1 to 10, the first line matches the reference, both runs identical, and `git status` clean after the push.

### Check your understanding

1. Change `seed=1` to `seed=2` and run the demo. What changes and what stays the same? Change it back.
2. Why does the demo not need its own test?

## Block M1-D: Tests on Windows and macOS with GitHub Actions

Why: the game must run on macOS, but you develop on Windows. Code can pass on your machine and still fail on a Mac, for example through a hardcoded backslash path, a Windows only call, or a Python version difference. GitHub Actions runs your tests on fresh Windows and macOS machines on every push, so a Mac breaking change shows a red X on the commit right away instead of surfacing weeks later on a teammate's laptop. It is the team's official check that the sim works on both platforms. It also becomes the foundation for M4, where the same mechanism builds the Mac version of the sim.

Goal: every push runs ruff and pytest on Windows and macOS, and you have seen both a passing and a failing run.

Concepts you will need:
- **CI (continuous integration):** automatically testing every change as it is pushed.
- **Workflow:** a YAML file in `.github/workflows/` that tells GitHub what to run and when.
- **Trigger:** the event that starts a workflow, listed under `on:`.
- **Job and steps:** a job runs on one machine; its steps are commands run in order. If a step fails, the job stops and turns red.
- **Runner:** the fresh virtual machine GitHub creates for each job and destroys afterwards. It starts empty, without your code.
- **Action:** a reusable, prebuilt step, referenced with `uses: owner/name@version`.
- **Matrix:** runs the same job once per combination of values.
- **Expression:** `${{ ... }}` fills in a value at run time, such as `${{ matrix.os }}`.
- **YAML:** configuration text where indentation is structure. Use spaces, never tabs. `key: value` pairs, and `- item` for list entries.
- Docs: https://docs.github.com/en/actions/writing-workflows/quickstart and the full reference at https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions

### Step 1. Check repo visibility

On the repo's GitHub page, look for "Public" or "Private" next to the name.

Why: public repos get unlimited free Actions minutes. Private repos get a monthly allowance, and macOS minutes count 10 times. If private, test only Python "3.11" in the matrix.

### Step 2. Create `.github/workflows/tests.yml` from this skeleton

Create the folders at the repo root (note the dot in `.github`). This skeleton is not valid YAML until the TODOs are filled in.

```yaml
# Runs lint and tests on Windows and macOS for every push and pull request.
name: tests

on:
  # TODO: Three triggers: every push, every pull request, and a manual
  #   "Run workflow" button.
  # Hint: the manual one is called workflow_dispatch. A trigger with default
  #   settings is written as just its name and a colon.

jobs:
  test:
    # TODO: Pick the runner from the matrix below instead of hardcoding one.
    # Hint: ${{ matrix.<key> }}
    runs-on: TODO
    strategy:
      # TODO: Let every job finish even if another fails, so you can tell
      #   whether a failure is Mac only or everywhere. Look up fail-fast.
      matrix:
        # TODO: os: windows-latest and macos-latest
        # TODO: python-version: "3.11" (the minimum in pyproject.toml) and
        #   "3.13" (what you use locally). Quote them: YAML reads 3.10 as 3.1.
    defaults:
      run:
        shell: bash  # Git Bash on Windows runners, so commands match yours.
    steps:
      # TODO 1: Check out the repo. The runner starts empty.
      #   Action: actions/checkout@v4
      # TODO 2: Install the Python version from the matrix.
      #   Action: actions/setup-python@v5, with input python-version.
      #   Inputs to an action go under `with:`.
      # TODO 3: run: pip install -e "sim[dev]"
      # TODO 4: run: ruff check sim   (fast, so it fails first on typos)
      # TODO 5: run: pytest sim
      # Hint: give every step a `name:` so the log is readable.
```

### Step 3. Push and read the run

```bash
git add .github
git commit -m "CI: run ruff and pytest on Windows and macOS"
git push
```

On GitHub, open the `Actions` tab, click the newest "tests" run, then click one of the jobs and expand its steps. If the run fails with a YAML error, the message names the line; fix it, commit, push again.

Why: reading these logs is how you will diagnose every future CI failure.

### Step 4. See a failure on purpose

```bash
git switch -c ci-check
```

In `sim/tests/test_actions.py`, change `assert world.t == 3` to `assert world.t == 4`. Then:

```bash
git commit -am "Deliberately break a test"
git push -u origin ci-check
```

Watch the run fail in the `Actions` tab and find the assert in the "pytest" step log. Then clean up:

```bash
git switch main
git branch -D ci-check
git push origin --delete ci-check
```

What these do: `switch -c` creates a **branch** (a separate line of commits) and moves onto it. `commit -am` stages all modified tracked files and commits. `push -u origin ci-check` sends the branch to GitHub. `switch main` returns to main, where the test is still correct. The last two delete the branch locally and on GitHub.

Why: a check you have never seen fail is a check you cannot trust. A branch keeps `main` history clean.

### Step 5 (optional). Status badge

`Actions` tab, click "tests" in the left sidebar, `...` menu at the top right, `Create status badge`, copy the Markdown into the top of `README.md`, commit, push.

Checkpoint: the run on `main` shows 4 green jobs (2 OS x 2 Python). The `ci-check` run showed red with `assert 3 == 4` in the log.

### Check your understanding

1. If a job fails only on `macos-latest` with Python 3.11, name two different things that could explain it.
2. Why does the workflow need a checkout step when the workflow file itself is already in the repo?

Say "M1 done" to get M2.

## Done

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
