# Single-lake model papers: candidates

Research note, 2026-10-25. **Decided 2026-10-25: Justin chose Lake Washington (Arhonditsis and Brett 2005).** No model work has started.

## Question

Which published paper models one specific, named lake ecosystem well enough that we can rebuild it in our own stocks-and-fluxes code (`docs/research/SIM_FRAMEWORK_PROPOSAL.md`)?

Criteria, most important first: one named lake; full equations and parameter values published; ecosystem scope (nutrients, plankton, ideally fish or oxygen); about 4 to 30 state variables, 0D or two-layer; observations or figures to validate against; open access is a plus.

DOIs below were checked against Crossref. Elsevier full text could not be opened, so claims about what the papers contain are marked "unverified" where they come from abstracts or secondary sources.

## Candidates

| # | Paper | Lake | Model | Equations and parameters | Access | Verdict |
|---|---|---|---|---|---|---|
| 1 | Arhonditsis and Brett 2005, Ecological Modelling 187: 140-178 (Part I, model description), doi:10.1016/j.ecolmodel.2005.01.040. Part II calibration, 187: 179-200, doi:10.1016/j.ecolmodel.2005.01.039 | Lake Washington, Seattle. Deep, stratified, mesotrophic. Famous recovery from eutrophication after sewage diversion. | Two layers (epilimnion, hypolimnion). C, N, P, Si cycles, oxygen, 3 phytoplankton groups (diatoms, greens, cyanobacteria), 2 zooplankton (copepods, cladocerans). Roughly 15 per layer (count unverified). | Part I is a dedicated description paper. Full parameter tables expected but unverified. | Paywalled | Best overall fit |
| 2 | Omlin, Reichert and Forster 2001, Ecological Modelling 141: 77-103, doi:10.1016/S0304-3800(01)00256-3. Companion: Omlin, Brun and Reichert 2001, 141: 105-123, doi:10.1016/S0304-3800(01)00257-5 | Lake Zurich. Deep, mesotrophic. | 1D in depth, about 13 state variables: P, N, oxygen, organic particles, 1 phytoplankton, 1 zooplankton. Later collapsed by its authors into the BELAMO box model (2 water boxes, 2 sediment boxes). | Title says "model equations". Every parameter value printed: unverified. | Paywalled | Runner-up: smaller, cleaner |
| 3 | Carpenter, Brock, Cole, Kitchell and Pace 2008, Ecology Letters 11: 128-138, doi:10.1111/j.1461-0248.2007.01131.x. Experiment: Carpenter et al. 2011, Science 332: 1079-1082, doi:10.1126/science.1203672 (free preprint from the Cary Institute) | Peter and Paul Lakes, Wisconsin. Small, oligotrophic. Whole-lake experiment: bass added to Peter, Paul kept as reference. | 0D food chain, about 4 to 6 variables: piscivores (adult, juvenile), planktivores, zooplankton, phytoplankton (unverified). | Short, in the paper (unverified). | Copy on Notre Dame CurateND | Fastest prototype, has tipping points. No nutrients or oxygen. Two lakes, not one. |
| 4 | Snortheim et al. 2017, Ecological Modelling 343: 39-53 (free PDF on the Carey lab site). Ladwig et al. 2021, HESS 25: 1009-1032, doi:10.5194/hess-25-1009-2021 (open access) | Lake Mendota, Wisconsin. Dimictic, eutrophic. | GLM-AED, 1D, many variables. | In GLM-AED docs and config files, not the papers. Setup archived on EDI. | Open | Poor to rebuild from. Excellent forcing and observation data (NTL-LTER, decades). |
| 5 | Chen et al. 2014, Ecological Modelling 273 (DOI unverified) | Meiliang Bay, Lake Taihu, China | SALMO, two layers, 3 algal groups, cladocerans, 128 parameters | Original equations in Benndorf and Recknagel 1982, hard to obtain | Paywalled | Good structure, hard sourcing |

Dropped: PCLake (about 100 variables, calibrated across many lakes, no single-lake paper found), Lake Kinneret DYRESM-CAEDYM (equations in model docs, large), Lake Victoria Ecopath (static mass balance, not ODEs). No open-access single-lake NPZD paper with full parameter tables was found.

## Recommendation

1. **Start from Lake Washington (Arhonditsis and Brett 2005, Parts I and II).** It is the only candidate meeting all the main criteria: one named lake, a description paper written to be reimplemented, nutrients plus several plankton groups plus oxygen, a two-layer box structure that maps directly onto a per-tick ODE step, and a calibration paper with observed vs simulated figures. Lake Washington also has a strong story for a game: a lake that went green and was brought back.
2. **Runner-up: Lake Zurich (Omlin et al. 2001).** Smaller and cleaner, but one plankton group each and a depth grid to collapse.
3. **Optional companion: Peter and Paul Lakes (Carpenter et al. 2008).** Its fish layer can sit on top of either model later. Also usable as a tiny first model to prove the framework end to end.

Suggested path if Lake Washington is chosen: build one layer with one phytoplankton and one zooplankton group first, check it, then add the second layer and the other groups.

## To do before starting

- PDFs go in `papers/` at the repo root, which is in `.gitignore` (publisher PDFs are not redistributed). Each teammate keeps their own copy. Have: `papers/arhonditsis_brett_2005_lake_washington_part1.pdf` (title confirmed as the Lake Washington eutrophication model; Part I vs Part II to confirm on first read). Still need: the other part (calibration, pp. 179-200).
- Confirm Part I lists every equation and parameter value.
- Find the forcing data the model needs (layer temperatures, light, inflow nutrient loads, mixing) and the monitoring data for validation (King County and University of Washington records).
- Check the terms for any data we would ship inside the game.
