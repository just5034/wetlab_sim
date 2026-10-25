# Vision

Covers look and feel. Domain direction (2026-10-25): a lake ecosystem. See `CLAUDE.md`.

## Art direction (decided by Justin, 2026-10-25)

- **Style:** hand-drawn, black and white.
- **Made by humans.** The team draws every visual asset. Claude does not generate, trace, or substitute final art. Claude imports the team's assets and wires them into the game as Justin directs.
- **Camera and space:** 2.5D. Flat hand-drawn sprites placed in a 3D scene with a tilted perspective camera, like West of Loathing and Don't Starve Together. Depth comes from placement, layering, scale, and shadows, not from 3D models.

Primary references: West of Loathing, Don't Starve Together.

Earlier wider list (2026-09-22): Deadly Days: Roadtrip, Octopath Traveler 0, Paper Mario. Kept for ideas on camera and depth only. The black and white hand-drawn look above overrides their color and pixel styles.

## What this means for the build

- Sprites are 2D images on flat quads or `SpriteRenderer`s inside the URP 3D scene. Characters and props usually face the camera (billboarding). Ground and water can lie flat.
- Black and white art means sim state cannot rely on color alone. Changes in the lake (algae, clarity, oxygen) should show through which sprite is shown, line density, opacity, animation, or added props. Any color or tint is a design decision for Justin, not a default.
- Until real art exists, Claude uses obvious placeholders (plain grey quads, labeled boxes) so nobody mistakes them for final art. Placeholders are swapped for team art without code changes where possible.
- How sim values map to visuals (which sprite for which state) is decided by Justin and recorded here or in `docs/ARCHITECTURE.md`.

Asset handling conventions are in "Art assets" in `docs/ARCHITECTURE.md`.
