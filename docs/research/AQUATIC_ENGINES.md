# Aquatic ecosystem engines: survey

Research note, 2026-10-06. Input for the team's domain decision. Nothing here is decided.

## Question

Which existing engines can simulate or emulate an aquatic ecosystem, are free to use, and can run on players' machines inside our setup? Our setup is a Python 3.11+ sim core frozen with PyInstaller, launched by Unity, on Windows, Intel macOS, and Apple Silicon macOS (see `docs/ARCHITECTURE.md`, "Platforms").

## How each candidate was judged

- What it simulates and at what level (whole lake, species group, individual).
- How mature it is (last release, maintenance, scientific use).
- License, and what bundling it in a distributed game would oblige us to do. GPL code inside our sim bundle means the sim must be released under the GPL with source.
- Python access: a pip wheel for `win_amd64`, `macosx arm64`, and `macosx x86_64`, or does it need R, Java, .NET, Julia, conda, or a Fortran compiler.
- Speed: can it advance fast enough between clicks.
- Inputs: does it need weather series, bathymetry, months of calibration.

Sources were primary (PyPI, GitHub LICENSE files, project sites) where possible. Items marked "unverified" could not be confirmed. Nothing was benchmarked or frozen with PyInstaller yet.

## Headline finding

No established scientific ecosystem engine drops cleanly into our bundle on all three platforms. Each one fails at least one test: GPL or AGPL license, a runtime we do not ship (R, Java, .NET, Julia, MATLAB), Windows-only, conda-only, or batch-only (cannot be stepped one tick at a time).

The workable path is a model we write ourselves in Python with NumPy and SciPy, built from published equations. The scientific engines become references and offline validation tools. This also matches the project goal that Justin understands every line.

## 1. Process models (nutrients, plankton, oxygen, temperature)

| Engine | Simulates | License | Python / platforms | Fit |
|---|---|---|---|---|
| FABM + pyfabm | Framework for aquatic biogeochemistry. Ships NPZD-type models, ERSEM, PCLake port. 0D to 3D. v3.0.1, active. | GPL-2.0-only | pyfabm 3.0.1 on conda-forge for win-64, osx-64, osx-arm64. PyPI copy is stale (2018). | Best real engine. Steppable per tick from Python. Forces the sim core to be GPL and conda-based. |
| GOTM | 1D water column physics. Biology via FABM. | GPL-2.0 | Fortran exe, needs NetCDF and weather forcing. | Physics only. Poor. |
| GLM + AED (glm-py) | 1D lake: stratification, ice, oxygen, nutrients, plankton, macrophytes. Widely used. | GPL-3.0 | glm-py 0.5.0 wheels for macOS arm64 and x86_64. No Windows wheel. | Batch executable, not tick-steppable. Needs weather and bathymetry. |
| PCLake / PCLake+ | Shallow lake: nutrients, plankton, fish, macrophytes, clear vs turbid regime shifts. | Unverified (license is a PDF agreement) | R, C++, FABM, Delwaq versions. | Most game-like science model. Good equation source if terms allow. |
| AQUATOX (US EPA) | Full aquatic food web: nutrients, algae, plants, invertebrates, fish, oxygen, toxicants. | Source offered by EPA. License wording unverified (reports conflict). | Delphi, Windows only, no Python API. | Cannot ship. Its Technical Documentation is the best equation reference. |
| CE-QUAL-W2 | 2D reservoir hydrodynamics and water quality. | MIT | Fortran, Windows-oriented. macOS unverified. | Legally safe, but heavy setup and not interactive. |
| Delft3D / D-Water Quality | Comprehensive 1D to 3D water quality. | AGPL-3.0 / GPL-3.0 engines | Windows prebuilt, others self-compile. | Overkill. |
| Simstrat, MyLake, WASP, QUAL2K, ERSEM, BFM, LakeEnsemblR | Lake physics, river or marine water quality. | GPL, or no license stated | Fortran, MATLAB, R, Excel, or GUI apps. | Poor. |
| phydra | Pure-Python NPZD plankton models. | BSD-3 | conda or git, "early stages". | Structural reference only. |

## 2. Food webs, fish populations, agents

| Engine | Simulates | License | Python / platforms | Fit |
|---|---|---|---|---|
| Ecopath with Ecosim | The standard food-web model: biomass of functional groups over time. | GPL-2 | .NET, Windows desktop. | Cannot ship. |
| Rpath (NOAA) | Ecopath and Ecosim in R and C++. Active. | US public domain, permissive abroad | Needs R. | Clean, permissive equation reference. |
| PyPath | Pure-Python port of Rpath. | MIT | conda or source. One developer, 2 stars. | Could be read or vendored after review. Not a dependency to trust as-is. |
| ATNr, EcologicalNetworksDynamics.jl | Body-size-based food-web ODEs. | GPL / AGPL | R / Julia. | Offline reference only. |
| mizer | Multi-species size spectrum fish model. | GPL-3 | R. No Python port. | Offline reference only. |
| OSMOSE | Individual-based fish schools on a 2D grid. | GPL-3 | Java core, R driver. | Heavy, not interactive. |
| Atlantis | End-to-end marine ecosystem. | No open license | C, code on request. | Not usable. |
| Mesa | Agent-based framework (individual fish). | Apache-2.0 | Pure-Python wheel, all platforms. **Needs Python 3.12+.** | Good if we want individuals. Raise our floor to 3.12 or write a small agent loop ourselves. |
| NetLogo, Repast4Py, AgentPy | Agent frameworks. | GPL / BSD | Java runtime, MPI, or unmaintained. | Poor. |
| InVEST | Static GIS ecosystem-service maps. | Apache-2.0 | No macOS arm64 wheel. | Not a population sim. Irrelevant. |
| Thrive (game) | Evolution game with population "auto-evo". | GPL-3 code, CC BY-SA assets | Godot/C#. | Ideas only. |
| pond-evolution | Python pond: algae, worms, evolving fish. | MIT | Pure Python. | Good small game-scale reference. |

## 3. Water chemistry, physics, building blocks

| Tool | Does | License | Python / platforms | Fit |
|---|---|---|---|---|
| SciPy (`solve_ivp`) | ODE solver. Steps a 5 to 50 variable model in about a millisecond (estimate). | BSD-3 | Wheels for all three platforms. PyInstaller hook exists. | The core building block. |
| PHREEQC via `phreeqc` (PyPI) | Standard water chemistry: pH, hardness, ammonia, CO2, mineral saturation. | USGS public domain (ship the notice, credit USGS). Bindings MIT. | Wheels for all three platforms. One maintainer. | Best chemistry option, mainly for tanks and aquaria. Native library needs explicit PyInstaller collection and macOS signing. Call on slow ticks. |
| PhreeqPython | Friendlier PHREEQC API. | Apache-2.0 | Newest release: Python 3.12 only, no Intel Mac wheel. 1.5.7 is a universal pure wheel. | Alternative to `phreeqc`. |
| gsw (TEOS-10) | Seawater density, freezing point. | BSD-3 style | Wheels for all three platforms. | Only if the setting has seawater. |
| PySD | Runs Vensim/XMILE stock-and-flow models. | MIT | Pure wheel, heavy deps. | Only if a designer wants visual authoring. Translate at build time. |
| libRoadRunner | Fast SBML model runner. | Apache-2.0 | Intel Mac wheel needs macOS 15+. | Only to import SBML models. |
| PyCO2SYS | Marine carbonate chemistry. | GPL-3 | Pure wheel. | Avoid. Use PHREEQC or the equations. |
| Reaktoro | Chemical equilibrium. | LGPL-2.1 | conda only. | Overkill. |
| Parcels, Oceananigans.jl | Ocean particle tracking, ocean/lake fluid dynamics. | MIT | Heavy deps / Julia runtime. | Offline only, to bake data. |

Unity side: Crest water is paid. Unity's water system needs HDRP and we use URP. A Shader Graph water surface is free and enough for tanks and ponds. The physics lives in Python anyway.

## Recommendation

1. **Our own model, NumPy and SciPy.** Start with a small set of stocks (for example nutrient, algae, grazer, fish, oxygen) as ODEs, stepped per `tick`. Take equations from AQUATOX's Technical Documentation, PCLake, classic NPZD papers (Franks, Fasham), and Rpath/PyPath for food-web terms. We own the code, it freezes cleanly on all three platforms, and it fits the existing `world` / `tick` design.
2. **PHREEQC via `phreeqc`** if the domain is tanks or aquaria and water chemistry is part of play. Public domain, all three platforms.
3. **Mesa** if individual animals matter. Requires raising `requires-python` to 3.12.
4. **FABM/pyfabm, GLM-AED, mizer, Rpath as offline references.** Run them on a dev machine to check our model behaves plausibly. Do not ship them.

Shipping FABM directly is the one real-engine option. It means the sim core is GPL-2.0 and the build uses conda. That is a team decision, not a technical blocker.

## Open questions for the team

- Setting: lab tank or aquarium, pond, lake, or ocean? This decides whether chemistry (PHREEQC), stratification (GLM), or salinity (gsw) matter.
- Scale: populations (ODEs) or individuals (agents)?
- Fidelity: scientifically defensible, or "feels right" for play?
- Licensing: is a GPL sim core acceptable?
- Is raising the Python floor to 3.12 acceptable (Mesa, newest PhreeqPython)?

## To verify before relying on any of this

- Freeze SciPy and `phreeqc` with PyInstaller on Windows and macOS (M4 territory).
- AQUATOX and PCLake license terms.
- Benchmark one tick of a draft model.
