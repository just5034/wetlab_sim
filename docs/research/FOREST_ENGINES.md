# Forest ecosystem engines: survey

Research note, 2026-10-06. Input for the team's domain decision. Nothing here is decided. Companion to `docs/research/AQUATIC_ENGINES.md`, judged by the same criteria.

## Question

Which existing engines can simulate or emulate a forest, are free to use, and can run on players' machines inside our setup? Our setup is a Python 3.11+ sim core frozen with PyInstaller, launched by Unity, on Windows, Intel macOS, and Apple Silicon macOS (see `docs/ARCHITECTURE.md`, "Platforms").

## How each candidate was judged

- What it simulates and at what level (landscape, patch, cohort, individual tree).
- How mature it is (last release, maintenance, scientific use).
- License, and what bundling it in a distributed game would oblige us to do. GPL code inside our sim bundle means the sim must be released under the GPL with source. Non-commercial licenses rule out any paid release.
- Python access: a pip wheel for `win_amd64`, `macosx arm64`, and `macosx x86_64`, or does it need .NET, Java, R, conda, Qt, or a Fortran compiler.
- Stepping: can it advance one `tick` at a time, or does it only run as a batch job.
- Inputs: climate series, soils, species parameters, GIS rasters.

Sources were primary (PyPI, GitHub LICENSE files, project sites) where possible. Items marked "unverified" could not be confirmed. Nothing was benchmarked or frozen with PyInstaller yet.

## Headline finding

The pattern matches the aquatic survey. The best-known forest models are GPL (iLand, SORTIE-ND, ForClim), non-commercial (TreeMig, SIBYLA), not redistributable (FORMIND, Biome-BGC), or Windows/.NET (LANDIS-II). The core should again be a model we write ourselves.

Forests do have more permissive building blocks than water: US government public-domain code (FVS growth, Behave fire), Landlab (MIT) for soil water and grid vegetation, and small MIT or CC0 helpers for evapotranspiration and soil carbon. Forest models also suit games well: the classic JABOWA/FORET gap model is simple, steps once per simulated year, and is cheap to run.

## 1. Tree growth and forest dynamics

| Engine | Simulates | License | Python / platforms | Fit |
|---|---|---|---|---|
| FVS (USDA Forest Service) | Individual-tree growth, mortality, harvest, fuels. 20+ US regional variants. 5 or 10 year cycles. Tree list plus site index, no climate needed. | Public domain | Fortran. | Most authoritative growth engine we may legally ship. |
| PyFVS | Wrapper over a fork of official FVS, with a step API. | MIT | Wheels for Windows and Linux only. No macOS. One maintainer. | Needs our own Fortran build for both Mac architectures. |
| fvs-python | Pure-Python reimplementation of 10 FVS variants. | MIT | Pure wheel, all platforms. **Needs Python 3.12+.** Heavy deps (pandas, matplotlib, seaborn). | Easiest real growth model. Young, one developer, fidelity to FVS unverified. |
| Pure-Python JABOWA gap models (forestPatchSimulation, rbb_jabowa) | Patch of trees: growth, shading, age mortality, regeneration. Annual steps. | CC0 / MIT | Pure Python. | Small scaffolds or references for our own model. Parameter sources unclear. |
| 4C (PIK) | Process-based stand: carbon, water, heat. | BSD-2 | Fortran, unsupported, needs daily climate. | Permissive but would need wrapping and climate data. |
| LPJ-GUESS | Climate-driven vegetation and carbon on grid cells. | MPL-2.0 (file-level copyleft, commercial bundling allowed) | C++, no Python bindings. | Only if climate-driven carbon is central. Substantial wrapping. |
| ED2 | Size and age cohorts, carbon, water, energy. Sub-daily. | CC-BY-4.0 | Fortran plus HDF5. Windows build unverified. | Too expensive and data hungry. |
| 3-PG (r3PG) | Stand carbon allocation, water, growth. Monthly. | GPL-3 (R) | R with Fortran. | Equations are published. Reimplement if wanted. |
| iLand | Individual trees with light field over 10,000+ ha, regeneration, fire, wind, bark beetle. Best science here. | GPL-3.0 | C++/Qt binaries for Windows, macOS, Linux. | GPL. Reference only. |
| LANDIS-II v8 | Species age cohorts on rasters, succession, fire, wind, harvest. | Apache-2.0 (extensions vary) | C#, .NET 8, Windows and Linux. No macOS build. Batch. | License fine, platform and stepping not. |
| SORTIE-ND, ForClim, pyMANGA | Individual-tree or cohort gap models. | GPL | C++/Java, registration, Python (pyMANGA). | GPL. Reference only. |
| TreeMig, SIBYLA | Landscape cohorts, Central European growth. | Non-commercial | Fortran on request, Windows/MS Access. | Excluded. |
| FORMIND, Biome-BGC, PICUS, CENTURY/DayCent | Tropical gap, biogeochemistry, succession, soil. | No redistribution, or no public license | Various. | Excluded. |
| FATES | Cohort vegetation inside a host land model. | Modified BSD | Runs only inside CTSM/E3SM on HPC. | Infeasible. |

## 2. Disturbance

| Tool | Does | License | Python / platforms | Fit |
|---|---|---|---|---|
| Behave (USFS Fire Lab) | Rothermel surface fire and crown fire, the core of BehavePlus and FlamMap. | Public domain | C++, no Python bindings of its own. | Best licensing for fire. |
| pyrothermel | Python bindings to Behave. Point calculations per call. | MIT | Wheel only for cp312 win_amd64. Mac and 3.11 need a source build. API may change. | Use if we build wheels ourselves (for example cibuildwheel in CI). |
| Hand-written fire cellular automaton | "Trees grow, lightning burns", or Rothermel spread rate per cell. About 50 lines of NumPy. | Ours | Any. | Often the best choice for interactive play. |
| pyretechnics | Rothermel fire spread. | Community license is non-commercial. Commercial use needs a paid license. | sdist only, needs GDAL. | Avoid. |
| Cell2Fire, C2F-W, ELMFIRE | Grid fire growth. | GPL-3 / AGPL-3 with "no right to sell" | C++ / Fortran. | Avoid. |
| FARSITE, FlamMap | Fire growth apps. | Free apps, no public source | Windows desktop. | Not embeddable. Use Behave. |
| Insects, wind, drought | iLand covers all three (GPL). ForestGALES windthrow is R, license unverified. | | | No permissive Python package found. Write simple rules (for example a stress index from soil water deficit). |

## 3. Soil, water, carbon

| Tool | Does | License | Python / platforms | Fit |
|---|---|---|---|---|
| Landlab | Grid framework with components for soil moisture, potential evapotranspiration, radiation, cellular-automaton plant competition (VegCA), vegetation, fire generator, infiltration. Designed to couple. | MIT | cp311 to cp313 wheels for all three platforms. | Strongest building block found in either survey. Catch: its dependency py-richdem is GPL-3.0-only. It is imported lazily (one flow router only), so exclude it from the bundle and confirm `import landlab` still works. Heavy deps (xarray, pandas, netCDF4, matplotlib). Copying only the needed MIT component source is an alternative. |
| pyet | Evapotranspiration (Penman-Monteith, Hargreaves, and others). | MIT | Pure wheel, needs pandas and xarray. | Water demand per tick. |
| PyETo | Simple evapotranspiration functions. | BSD-3 | Pure Python, not on PyPI, last commit 2022. | Small enough to vendor. |
| pyRothC | RothC soil carbon model. | CC0 | Pure wheel. Monthly step. | Drop-in soil carbon. |
| hydrobricks, PCSE, Yasso | Hydrology, crop models, soil carbon. | MIT (no Intel Mac wheel) / EUPL copyleft / no permissive Python port | | Poor fits. |

## 4. Wildlife

No mature, permissively licensed Python package for forest wildlife or deer browsing was found. Small PyPI packages (ecodyn, PySpecies) have no license, which means no rights to use them. Write predator-prey and browsing equations ourselves with SciPy, or use Mesa (Apache-2.0, Python 3.12+) for individual animals. Same conclusion as the aquatic survey.

## 5. Plant form and Unity-side trees

- L-Py (OpenAlea): the best L-system engine. CeCILL-C (LGPL-like), conda only, depends on PlantGL and Qt. Too heavy to freeze. Not needed: tree shape is a Unity concern, not sim state.
- GroIMP: GPL or commercial, Java. Avoid.
- Writing our own: an L-system string rewriter is about 30 lines, space colonization about 100.
- Unity's built-in Tree Editor still exists in Unity 6 but works only with the Built-In Render Pipeline. We use URP, so it is out. Unity points URP users to SpeedTree.
- mattatz/unity-procedural-tree: MIT, runtime meshes, last updated 2022. URP compatibility unverified.
- ez-tree: MIT, three.js. Algorithm reference, or export meshes.
- With the 2D-sprites-in-3D art direction in `docs/VISION.md`, hand-drawn tree sprites may make procedural meshes unnecessary.

## 6. Iowa State University Rain Forest Simulation Model

Added 2026-10-06 at Justin's request. Source: https://ecos.nrem.iastate.edu/rfsims

- What it is: an animated, game-like simulation of carbon cycling in a tropical rain forest, built by Ann E. Russell (Iowa State, Natural Resource Ecology and Management) for middle-school students. Bilingual (English and Spanish). Two scenarios: intact rain forest, and conversion to pasture. Players explore "what if" questions about what limits forest production and how land-use change affects carbon and warming.
- Model structure: a stock-and-flow (compartment) carbon model. The site publishes Odum diagrams, parameters, functions, and calibration data in Excel for both scenarios.
- Software: built in ExtendSim, a commercial simulation tool. Distributed as a 250 MB installer that bundles the ExtendSim 9.3.1 Demo. PC (Windows) only. Fixed 1024 x 768 display.
- Status: the site says it "is an archive and no longer receives updates". A related Android app, "The Rainforest Game" (2018), came from the same author.
- License: none stated. Model source files are not offered, only the installer and documentation.
- Fit: cannot be bundled (Windows only, commercial ExtendSim runtime, no license). Its value is as a reference. The published diagrams, parameters, and calibration data describe a small carbon stock-and-flow model of the kind we would write in SciPy, and it is a close precedent for a game-like teaching sim. Before copying any parameter values, ask the author or Iowa State for permission. Equations and published facts are usable, but the data files carry no stated terms.

## 7. Games and projects to learn from

- PolyPine (commercial): forest growth with fire, storms, and bark beetle as game systems. Scope reference.
- Equilinox, Terra Nil: closed source, design reference only.
- Sebastian Lague "Ecosystem-2" (Unity): no license, viewing only.
- Classic forest fire cellular automaton: the minimal "trees grow, lightning burns" loop. A natural first mechanic.

## Recommendation

1. **Our own JABOWA-style gap model in NumPy.** One `tick` is one simulated year. A grid of patches, each with trees that grow, shade each other, die, and regenerate. Take equations from JABOWA/FORET papers and parameters from published species tables (check the license of any parameter dataset). Use forestPatchSimulation (CC0) and rbb_jabowa (MIT) as references.
2. **Add disturbance and soil as separate modules:** a fire cellular automaton (optionally Rothermel spread rates from Behave), a soil water stress index (pyet or PyETo), soil carbon (pyRothC).
3. **Landlab** if the world is a grid with water and vegetation competition. Exclude py-richdem.
4. **fvs-python or PyFVS** only if realistic US tree growth matters more than bundle size and the Python floor. fvs-python needs 3.12. PyFVS needs our own macOS Fortran builds.
5. **iLand, SORTIE-ND, LANDIS-II as offline references** to sanity-check behavior. Do not ship them.

## Forest vs aquatic, for the team

| | Aquatic | Forest |
|---|---|---|
| Ship-ready real engines | None (FABM only if GPL is acceptable) | None complete, but public-domain FVS and Behave cores exist |
| Permissive building blocks | SciPy, PHREEQC, gsw | SciPy, Landlab, pyet, pyRothC, Behave |
| Natural tick | Hours to days (plankton, oxygen change fast) | One year (trees change slowly), with fast events (fire) on top |
| Simplest core model | NPZD-style ODEs (about 4 to 7 equations) | JABOWA gap model (per-tree growth and shading rules) |
| Visible player feedback | Water color, clarity, fish behavior | Canopy growth, clearings, fire spread |
| Shared need | Predator-prey written by us | Predator-prey written by us |

Either domain keeps the current architecture unchanged: Python owns the rules, `tick` advances them, Unity draws the snapshot.

## Open questions for the team

- Scale: one stand, a patch grid, or a landscape?
- Timescale: does one click mean a day, a season, or a year? Forests make players wait years for change unless events (fire, storms, animals) fill the gap.
- Fidelity: scientifically defensible growth, or "feels right"?
- Licensing: is a GPL sim core acceptable? It would open up iLand-class science.
- Python floor: raise to 3.12 for Mesa and fvs-python?

## To verify before relying on any of this

- `import landlab` works without py-richdem, and Landlab freezes with PyInstaller on Windows and macOS.
- pyrothermel builds from source on both Mac architectures and Python 3.11.
- Licenses of any species parameter tables we copy.
- Benchmark one tick of a draft gap model.
