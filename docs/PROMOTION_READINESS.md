# Promotion Readiness

**Updated:** 2026-04-28.

This is the current promotion-readiness surface for Morph-Bench. It describes
what is true from repo custody today, what remains source-authority only, and
which gates must stay open for public or website-facing copy.

## Current Verdict

| Field | Value |
|---|---|
| Verdict | `STAGED` |
| Posture | `benchmark_methods_active_with_named_blockers` |
| Website-sync posture | ready for repo-orchestrator review after branch verification passes |
| Code/docs license posture | Apache-2.0 code, CC-BY-4.0 docs |
| Data/artifact release posture | separate gate; no image-bearing payload admitted today |

## Pass Now

- **Standalone package install.** `pip install -e '.[dev]'` succeeds on the
  Python 3.11 verification floor.
- **Repo-local test suite.** `pytest -q` passes with 37 tests on the Python
  3.11 verification floor.
- **Synthetic smoke path.** The tiny fixture at
  [`fixtures/tiny_benchmark_manifest.json`](../fixtures/tiny_benchmark_manifest.json)
  runs end-to-end and emits a deterministic smoke report.
- **Replay battery.** The five-mode stability battery emits a
  `ReplayRecord` with deterministic replay, leave-fraction-out,
  noise-injection, k-sensitivity, and seed-variance payloads.
- **Adapter contract.** The Indus Phase 4 v1 adapter satisfies the current
  MUST-clause map in
  [`docs/family/ADAPTER_CONTRACT_v1.md`](family/ADAPTER_CONTRACT_v1.md).
- **Coupling guard.** The package source is free of the six forbidden
  monorepo/path-coupling patterns enforced by
  [`tests/test_forbidden_patterns.py`](../tests/test_forbidden_patterns.py).
- **Historical cross-environment smoke.** Blind-clone evidence under
  [`artifacts/blind_clone/`](../artifacts/blind_clone/) records matching
  macOS and Linux/RunPod smoke output for the synthetic path at the Phase 03
  closeout baseline. Current branch review still requires a fresh local/CI
  verification pass.
- **Code/docs license posture.** Root `LICENSE`, `NOTICE`, `README.md`, and
  [`docs/LEGAL_BOUNDARIES.md`](LEGAL_BOUNDARIES.md) now agree on Apache-2.0
  code and CC-BY-4.0 docs.

## Open Gates

### Blocked-1: Indus Phase 3c Feature Manifest Admission

- **Blocker:** No admitted consumable Phase 3c feature manifest JSON is present
  in this repo.
- **Owner:** owner / repo researcher.
- **Unblock produces:** `artifacts/replay/indus_phase4_live_<date>.json` and
  an adapter-run record naming input SHA-256.
- **Unblock condition:** a real JSON manifest path with SHA-256 is admitted to
  Morph-Bench custody. Prose or PDF reference is not enough.

### Blocked-3: Heavy-Data And Image-Bearing Release Policy

- **Blocker:** No public repo admission policy exists for image-bearing or
  rights-gated payloads.
- **Owner:** owner.
- **Unblock produces:** a `DATA_POLICY.md` appendix naming admitted asset
  classes, rights class, storage path, size bounds, and review owner.
- **Unblock condition:** owner decision plus artifact-specific admission record.

### Deferred: Cuneiform Adapter Contract

- **State:** deferred by scope, not a hidden failure.
- **Unblock produces:** a separate cuneiform adapter contract and
  fixture-backed tests.
- **Unblock condition:** explicit Phase 04 plan or second-family authorization.

### Deferred: Ops-Gates CI Consumption

- **State:** deferred because `Gnosis-Ops-Gates` must first be green on its own
  canonical CI and expose a Morph-compatible profile.
- **Unblock produces:** Morph CI job consuming a pinned green Ops-Gates SHA.
- **Unblock condition:** Ops-Gates self-CI green plus stable invocation surface.

## Trust Boundary

| Consumers Can Trust From This Repo | Source Authority Only / Not Proven Here |
|---|---|
| Package install and CLI surfaces | Live Indus Phase 4 NMI `0.5793` |
| Synthetic smoke fixture behavior | Live Indus Phase 4 Sigma `5.65` |
| Synthetic replay record shape | Live Indus Phase 4 Jaccard `0.4351` |
| Adapter-contract v1 coverage | Live 3/3 replay on the production feature manifest |
| Forbidden-pattern lint over package source | Contents of private or upstream authority bundles |
| Apache-2.0 code / CC-BY-4.0 docs posture | Public rights for corpora, image payloads, endpoint logs, or private HF artifacts |

Reading rule: the left column can be checked from a clone. The right column
requires an admitted upstream artifact or a separate domain-lane authority.

## Website-Sync Notes

Use the README wording and Commercial Readiness row. Do not market Morph-Bench
as a completed Indus reproduction. The website-safe one-line version is:

> Morph-Bench is the Gnosis benchmark/replay framework: clone-reproducible on
> synthetic fixtures today, with live Indus replay explicitly gated on admitted
> Phase 3c manifest custody.

## Owner Decisions Still Needed

1. Admit the Phase 3c feature manifest or keep the live replay gate open.
2. Decide the heavy-data/image-bearing release policy before any such payload
   enters a public repo.
3. Decide public visibility timing. This is a repository-setting action, not a
   substitute for the scientific or data gates above.

## Change Log

- 2026-04-28 - Refreshed for repo-orchestrator review: code/docs license
  posture settled, 37-test repo-local baseline current, public-ready language
  separated from data/artifact gates, and Ops-Gates adoption marked deferred
  until the internal gate repo is green.
- 2026-04-24 - Initial promotion-readiness document anchored to the blind-clone
  transcript. Historical phase plans under `.gpd/phases/` preserve the earlier
  license-pending and 32-test wording as history, not current operating truth.
