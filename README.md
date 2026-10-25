[![tests](https://github.com/just5034/wetlab_sim/actions/workflows/tests.yml/badge.svg)](https://github.com/just5034/wetlab_sim/actions/workflows/tests.yml)


# labsim


Python simulation core plus Unity client, connected by WebSocket. Domain direction: a lake ecosystem. Claude Code writes the code; Justin directs.

```
CLAUDE.md                  instructions for Claude Code
.claude/commands/          /today (status and plan)
docs/WORK_INSTRUCTIONS.md  current tasks (living)
docs/research/             surveys and paper notes
docs/ROADMAP.md            milestones
docs/ARCHITECTURE.md       Python and Unity split
sim/                       Python sim core (labsim)
unity/                     Unity client
```

Open Claude Code at the root and type `/today`.

## New computer setup

All project context is in this repo (`CLAUDE.md` and `docs/`). Claude Code's local memory does not sync between computers, so nothing else is needed for Claude to pick up where we left off.

In Git Bash:

```bash
git lfs install                      # once per computer, before or after cloning
git clone https://github.com/just5034/wetlab_sim.git
cd wetlab_sim
python -m venv .venv
source .venv/Scripts/activate        # macOS: source .venv/bin/activate
pip install -e "sim[dev]"
pytest sim                           # should pass
```

Then:
- Copy the reference papers into `papers/` by hand (it is gitignored; publisher PDFs are not redistributed). Currently: `arhonditsis_brett_2005_lake_washington_part1.pdf`.
- Unity: open `unity/client` in Unity Hub with editor `6000.0.84f1`.
- Machine-specific notes for the original Windows machine are in "Machine notes" in `docs/WORK_INSTRUCTIONS.md`.
