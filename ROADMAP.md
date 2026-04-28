# Roadmap

## How To Read This File

This roadmap states the extraction and promotion sequence. It is not proof of
the live Indus benchmark result. Evidence lives in the paths named by the
README and promotion-readiness docs.

## Current Position

| Area | State |
|---|---|
| Package and synthetic smoke path | `DONE` |
| Indus Phase 4 v1 adapter against synthetic Phase-4-like fixtures | `DONE` |
| Five-mode stability battery and replay record | `DONE` |
| Blind-clone install and synthetic replay proof | `DONE` |
| License posture for code/docs | `DONE` - Apache-2.0 code, CC-BY-4.0 docs |
| Live Indus Phase 4 rerun from Morph custody | `BLOCKED` on admitted Phase 3c manifest |
| Heavy-data/image-bearing release | `BLOCKED` on data admission policy |
| Cuneiform adapter | `DEFERRED` until the first real Indus replay or explicit second-family authorization |
| Ops-Gates CI consumption | `DEFERRED` until `Gnosis-Ops-Gates` self-CI is green and a Morph-compatible profile exists |

## Next Work

| Priority | Item | Evidence Needed | Status | Owner |
|---|---|---|---|---|
| P0 | Admit a consumable Phase 3c feature manifest | SHA-256 pinned JSON path and adapter-run record | `BLOCKED` | owner / repo researcher |
| P1 | Run live Indus Phase 4 replay through Morph-Bench | `artifacts/replay/indus_phase4_live_<date>.json` plus run record | `BLOCKED` on P0 | repo researcher |
| P2 | Finalize heavy-data/image-bearing release boundary | `DATA_POLICY.md` appendix naming asset classes and terms | `BLOCKED` | owner |
| P3 | Add cuneiform adapter contract v2 | GPD plan and fixture-backed contract tests | `DEFERRED` | repo researcher |
| P4 | Consume Ops-Gates in CI | Green Ops-Gates SHA plus Morph-compatible repo profile | `DEFERRED` | repo + ops-gates maintainers |

## Status Rules

- Use `DONE`, `BLOCKED`, `DEFERRED`, or `IN_PROGRESS`.
- If a priority depends on owner input, name the input.
- A synthetic smoke win is not equivalent to the live-source replay gate.
