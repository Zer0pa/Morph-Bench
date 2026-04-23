---
phase: 01-source-admission-and-replay-design
plan: 01
type: summary
status: complete
completed_at: 2026-04-24
---

# Plan 01-01 Summary — Freeze The First Real Replay Target

## Objective (recap)

Choose the first real source-manifest replay target and define the adapter
contract needed to port it into the neutral `BenchmarkManifest` schema.

## Outcome

**Target chosen:** Indus Phase 4 family
(`scripts/indus/phase4_route_selection.py` + `phase4_stability.py` +
`stability_tester.py`).

**Rationale (short):** Wins on 5 of 6 extraction-risk axes; only candidate whose
authority bundle carries recoverable numeric targets (NMI vs ICIT Set = 0.5793,
Sigma = 5.65, Leave-10%-out Jaccard = 0.4351, Deterministic replay 3/3) and
whose manifest shape maps almost 1-to-1 onto the existing
`BenchmarkManifest` dataclass. See
`docs/family/FIRST_REPLAY_TARGET_DECISION.md` for the full comparison.

## Deliverables

| Deliverable | Path | Role |
|---|---|---|
| Target decision | `docs/family/FIRST_REPLAY_TARGET_DECISION.md` | frozen choice with 6-axis comparison |
| Adapter contract v1 | `docs/family/ADAPTER_CONTRACT_v1.md` | Indus Phase 4 → `BenchmarkManifest` mapping, explicit exclusions, forbids all six path-rewrite patterns |
| Verification | `.gpd/phases/01-source-admission-and-replay-design/01-VERIFICATION.md` | enumerated sources read and contract-coverage checks |

## Requirements Advanced

- `DATA-03` → in progress (real manifest still needs admission; adapter contract drafted)
- `DERV-03` → in progress (contract v1 drafted; ratification pending first execution)

## Blockers Surfaced For Phase 02

1. **No access to live source scripts or manifests.** `phase4_route_selection.py`,
   `phase4_stability.py`, `stability_tester.py`, and
   `workspace/artifacts/indus/phase3c/prebinarized_feature_manifest.json` are
   not present on this Mac nor on RunPod pod `7k3riasglemecu` (`/workspace`
   searched). Phase 02 execution (code port + real-manifest rerun) cannot start
   until the live Gnosis source repo is admitted to an accessible location.
2. **ICIT Graph reference key handling** is deferred — unclear whether v1 must
   carry both `ICIT_Set` and `ICIT_Graph` or only the primary.
3. **Cuneiform adapter contract is owed** separately before any cuneiform port.
4. **License text still owner-deferred** (pre-existing blocker to public
   promotion; does not block Phase 02 execution).

## Commits (on `origin/main`, Zer0pa/Morph-Bench)

- `9e0a98d` docs(phase-01): choose first replay target
- `363bae2` docs(phase-01): adapter contract v1
- `bd2db44` chore(phase-01): advance state

## Decision Log

- Decision: Indus Phase 4 is the first real replay target; cuneiform deferred.
  - Rationale: only family with recoverable numeric ground-truth plus clean schema fit.
  - Outcome: ADOPTED.
- Decision: adapter contract is scoped to a single target (v1); multi-corpus
  generalization deferred to a later contract version.
  - Rationale: avoid speculative genericity before the first real replay works.
  - Outcome: ADOPTED.
