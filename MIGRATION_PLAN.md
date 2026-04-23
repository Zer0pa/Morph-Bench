# Migration Plan

## Goal

Move `gnosis-morph-bench` from a source-attributed scaffold to a standalone
private repo candidate that owns neutral benchmark logic without overclaiming
domain truth.

## Phases

| Phase | Objective | Exit condition |
|---|---|---|
| 1. Boundary freeze | Keep only benchmark-first methods scope | `SOURCE_BOUNDARY.md` and `DATA_POLICY.md` stay coherent |
| 2. Neutral module extraction | Port route scoring, null metrics, stability, replay, and reference-freeze helpers | no hidden imports from live monorepo remain |
| 3. Schema conversion | Add adapters from admitted live manifests into the neutral schema | at least one real source manifest can be converted without hardcoded paths |
| 4. Replay from repo custody | Reproduce live route/stability/replay logic from this repo | source-custody rerun artifacts exist |
| 5. Blind-clone gate | Fresh clone installs and runs smoke plus admitted replay path | clean temp clone passes |
| 6. Promotion review | Close license and data-release blockers | private remote ready; public still optional |

## Immediate Work Items

1. keep the synthetic smoke path green
2. port the live route-scoring math out of `scripts/indus/phase4_route_selection.py`
3. split generic stability logic from image-domain helpers in
   `scripts/indus/stability_tester.py`
4. factor reusable matrix/classification helpers out of the cuneiform common
   modules without pulling in domain-specific benchmark custody
5. add a converter contract for the cuneiform benchmark manifest family

## Stop Conditions

- extraction starts pulling in glyph preprocessing or domain papers just to make
  the repo look complete
- the repo can only run by reaching back into the live monorepo through hidden
  path assumptions
- the README starts promoting live-source results as if they were rerun here
