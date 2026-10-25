# Simulation framework

Status: proposed 2026-10-06. Accepted by Justin 2026-10-25 ("seems fine for now"). Built in M3. Open decision 1 is settled (lake ecosystem) and 2 is settled (framework is M3, see `docs/ROADMAP.md`). The small questions in 4 are Claude's call unless Justin weighs in.

## Goal (Justin, 2026-10-06)

For compute and customizability, build one world-development framework inside our own sim core. Each mathematical model of a system (for now aquatic or marine) is translated into code in that framework. No separate simulation software is installed or launched per ecosystem or per model.

Background: `docs/research/AQUATIC_ENGINES.md` and `docs/research/FOREST_ENGINES.md` found that no existing engine can be bundled cleanly on Windows and both Mac architectures under a permissive license. The surveys recommended writing our own model in NumPy and SciPy. This proposal generalizes that into a framework. FABM (GPL, Fortran) uses the same pattern. We copy the idea, not the code.

## Core idea: stocks and fluxes

Most aquatic models (NPZD, AQUATOX, PCLake, Ecosim) and the Iowa State rain forest carbon model reduce to:

- **Stocks:** named quantities that change over time (nutrient, phytoplankton, zooplankton, fish, oxygen, carbon).
- **Fluxes:** transfers from one stock to another, each with a rate function of state, parameters, and environment (uptake, grazing, mortality, respiration).
- **Forcings:** inputs the model does not compute (light, temperature, player actions such as feeding or dosing).

A paper's derivatives are sums of fluxes: dP/dt = uptake - grazing - mortality. Storing fluxes rather than hand-written derivatives gives:

1. Mechanical translation from paper to code: draw the box (Odum) diagram, list stocks, write one function per arrow.
2. Mass conservation by construction: each flux subtracts from its source and adds to its sink. Testable.
3. Composition: adding a fish model to a plankton model adds stocks and fluxes, no rewrite.

## Layers

| Layer | Holds | Why separate |
|---|---|---|
| Model definition | Stocks, fluxes (Python functions), parameter names | Written once per model, mirrors the paper |
| Parameters | YAML or JSON data files | Tune and swap scenarios or species without code changes |
| Assembler | Builds one vectorized NumPy derivative function from the stocks and fluxes | Fast. Model authors never touch it |
| Integrator | Fixed-step RK4 by default, SciPy `solve_ivp` for stiff models, several substeps per `tick` | Separates game time from model time |
| Events | Discrete changes between steps (player actions, harvests, die-offs) | Keeps smooth math apart from game rules |
| Space (later) | Same stocks on a grid of cells. Mixing and drift are extra fluxes | Tank to reef map with no model changes |
| Snapshot | Projects state to what Unity needs | Unity still sees only the snapshot |

Illustrative shape (not final, not code to copy):

```python
model.stock("N")  # nutrient
model.stock("P")  # phytoplankton
model.stock("Z")  # zooplankton

model.flux("uptake", source="N", sink="P",
           rate=lambda s, p, env: p.mu_max * env.light * s.N / (p.k_N + s.N) * s.P)
model.flux("grazing", source="P", sink="Z", rate=...)
model.flux("mortality", source="P", sink="N", rate=...)
```

## Compute notes

- One tank (5 to 50 stocks) is well under a millisecond per step in NumPy (estimate, not benchmarked).
- Grids (for example 100 x 100 cells x 10 stocks) are fine if every rate function works on whole arrays at once, not cell by cell. Design for this from the start.
- Numba (BSD, wheels on all three platforms) is the later escape hatch. Not needed early.
- Individual animals later: NumPy arrays of individuals, coupled to bulk stocks through fluxes (fish eat zooplankton in their cell).

## Fit with the current architecture

- Unchanged: Python owns rules, `tick` advances time, Unity draws the snapshot, same seed gives same snapshots.
- Changes inside `World`: from named objects with one `value` to a state array plus a model definition. Replaces the placeholder rule in `actions.py`.
- Every model gets the same tests: conservation, determinism, steady state vs the paper, outputs vs a published figure. FABM and GLM-AED stay useful offline for cross-checks.

## Open decisions (to settle next session)

1. Domain. Justin leans aquatic or marine "for now". `CLAUDE.md` says the domain is a team decision. Record it as Justin's tentative pick, or keep it out of the docs until the team agrees?
2. Timing. Claude's recommendation: finish M3 (minimal client) and M4 (cross-platform build) first, then make the framework M5, built as skeleton blocks Justin writes: stocks and fluxes, assembler, integrator, parameters, first real model (likely NPZ). Alternative: start the framework before M3.
3. If accepted, move this into `docs/ARCHITECTURE.md` and add the milestone to `docs/ROADMAP.md`.
4. Smaller questions for later: equations as Python functions (proposed) vs equations as data strings (designer friendly, needs a parser); units handling; how a `tick` maps to model time.
