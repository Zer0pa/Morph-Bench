# AGENTS.md

## Scope

This repo owns only the neutral benchmark and replay surface for
`gnosis-morph-bench`.

## Read First

1. `README.md`
2. `PRD_GNOSIS_MORPH_BENCH_2026-04-23.md`
3. `SOURCE_BOUNDARY.md`
4. `DATA_POLICY.md`
5. `.gpd/PROJECT.md`
6. `.gpd/REQUIREMENTS.md`
7. `.gpd/ROADMAP.md`
8. `.gpd/STATE.md`

## Governing Rules

- Benchmark-first posture is sovereign.
- Runtime truth and artifact truth outrank prose.
- Do not narrate the live Phase 4 result into repo-custody proof unless it is
  rerun here.
- Keep domain-specific scientific verdicts in their consuming repos.
- Do not vendor heavy corpora or review packs to make the repo look complete.
- Do not revert unrelated work or edit sibling staged repos.

## Acceptance Gates

1. The repo installs without the live monorepo layout.
2. The smoke path runs on the local synthetic fixture.
3. Full extraction closes only when the real route-scoring, stability, replay,
   and reference-freeze helpers are ported and rerun from repo custody.
4. Public promotion remains blocked until license and data boundaries close.

## Preferred Engineering Direction

- Use corpus-neutral interfaces and explicit manifest inputs.
- Keep code shallow, documented, and package-importable.
- If a helper really belongs to glyph-engine or a domain repo, depend on it or
  exclude it instead of copying it silently.
