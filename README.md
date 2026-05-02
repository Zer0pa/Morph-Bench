# Gnosis Morph Bench

> Live window into the Zer0pa lab. Benchmark methods are useful now, with live Indus replay blockers kept visible.

## What This Is

Morph-Bench is a Gnosis benchmark-method lane: neutral route scoring, null metrics, stability battery, deterministic replay, and explicit Indus replay blockers.

`gnosis-morph-bench` is the benchmark-first methods lane of the Gnosis extraction program. It owns neutral route scoring, permutation-null metrics, a five-mode stability battery, deterministic replay, and SHA-256 reference-freeze helpers — without owning Indus or cuneiform scientific verdicts. Domain corpora connect through admitted adapters; the Indus Phase 4 v1 adapter is the first in-scope family.

**Headline metric (repo-custody, clone-reproducible):** `37 passed` pytest in a clean Python 3.11 venv + byte-equality cross-environment smoke (macOS 3.11.15 ↔ Linux/RunPod 3.11.13) + `0/6` forbidden-monorepo-pattern lint hits + `9/9 ADAPTER_CONTRACT_v1` MUST-clause coverage. Evidence path: [`artifacts/blind_clone/`](artifacts/blind_clone/) and [`tests/`](tests/). Live Indus Phase 4 measured values (NMI 0.5793, Sigma 5.65, Jaccard 0.4351, Replay 3/3) are source-authority citations only — see [`docs/PROMOTION_READINESS.md`](docs/PROMOTION_READINESS.md) trust boundary.

**Honest blocker:** Live Indus Phase 4 reproduction is blocked on admitted Phase 3c manifest access (`Blocked-1`); heavy-data release policy for image-bearing assets is open (`Blocked-3`). The synthetic smoke is what runs end-to-end today. See `## Readiness` below and [`docs/PROMOTION_READINESS.md`](docs/PROMOTION_READINESS.md).

## Method Mechanics

| Field | Value |
| --- | --- |
| Architecture | GNOSIS_BENCHMARK_METHOD |
| Method | `BenchmarkManifest` route scoring, permutation nulls, stability battery, deterministic replay |
| Adapter | Indus Phase 4 v1 adapter |
| Runtime Surface | `src/gnosis_morph_bench/` + CLI smoke/replay commands |
| Trust Boundary | synthetic smoke runs end-to-end; live Indus Phase 4 rerun remains blocked |

## Key Metrics

| Metric | Value | Baseline |
| --- | --- | --- |
| Pytest surface | 37 passed | clean Python 3.11 venv |
| Forbidden-monorepo-pattern lint | 0 / 6 hits | adapter-contract lint |
| Adapter contract coverage | 9 / 9 MUST clauses | `ADAPTER_CONTRACT_v1.md` |
| Cross-environment smoke byte-equality | PASS | macOS 3.11.15 vs Linux/RunPod 3.11.13 |

> Source: `artifacts/blind_clone/`, `tests/`, `docs/family/ADAPTER_CONTRACT_v1.md`, and `docs/PROMOTION_READINESS.md`.

## Repo Identity

| Field | Value |
| --- | --- |
| Identifier | Morph-Bench |
| Repository | https://github.com/Zer0pa/Morph-Bench |
| Portfolio | Gnosis |
| Visibility | PUBLIC |
| Default Branch | main |
| Authority Source | `docs/PROMOTION_READINESS.md`; `artifacts/blind_clone/` |
| License | Apache-2.0 code; CC-BY-4.0 docs |

## Readiness

| Field | Value |
| --- | --- |
| Verdict | STAGED |
| Posture | `benchmark_methods_active_with_named_blockers` |
| Checks | 37 pytest checks; lint-clean adapter contract |
| Authority | `docs/PROMOTION_READINESS.md` |

### Honest Blocker

Live Indus Phase 4 reproduction is blocked on admitted Phase 3c manifest access, and heavy-data image-bearing release policy remains open.

## What We Prove

- The neutral benchmark contract (`BenchmarkManifest`) round-trips cleanly through `load_manifest` / `evaluate_route` / `freeze_reference` / `deterministic_replay` / `leave_fraction_out` / the four added stability modes.
- The Indus Phase 4 v1 adapter satisfies every MUST clause of [`docs/family/ADAPTER_CONTRACT_v1.md`](docs/family/ADAPTER_CONTRACT_v1.md), enforced by [`tests/test_adapter_contract_coverage.py`](tests/test_adapter_contract_coverage.py).
- The forbidden-pattern lint catches the hidden-import / path-coupling patterns named by the adapter contract, self-tested via a positive control in [`tests/test_forbidden_patterns.py`](tests/test_forbidden_patterns.py).
- The smoke and replay outputs are byte-identical across macOS and Linux at the documented Python 3.11 floor — verified end-to-end through fresh-clone install, see [`artifacts/blind_clone/`](artifacts/blind_clone/).

## What We Don't Claim

- That the live Indus Phase 4 measured values have been reproduced from repo custody. They have not. Live rerun is blocked on admitted Phase 3c manifest access (`Blocked-1`). Those values are source-authority citations, not Morph-Bench-proven values.
- That the synthetic smoke path constitutes proof of any live finding.
- That the heavy-data image-bearing asset release is unblocked. It is not; `Blocked-3` (heavy-data release policy) remains open. See `## Readiness` and [`docs/PROMOTION_READINESS.md`](docs/PROMOTION_READINESS.md).
- That the cuneiform benchmark family is in scope for the v1 adapter contract. It is explicitly deferred to a separate future contract once the first real Indus replay lands.
- That this repo carries any descriptor, kernel, image-preprocessing, or domain-verdict ownership. Those belong to other Gnosis lanes.

## Verification Status

| Code | Check | Verdict |
| --- | --- | --- |
| V_01 | Clean Python 3.11 pytest: 37 passed | PASS |
| V_02 | Adapter contract coverage: 9/9 MUST clauses | PASS |
| V_03 | Forbidden-pattern lint with positive control | PASS |
| V_04 | Cross-environment blind-clone byte equality | PASS |
| V_05 | Live Indus Phase 4 rerun from repo custody | BLOCKED |

## Proof Anchors

| Path | State |
| --- | --- |
| `PRD_GNOSIS_MORPH_BENCH_2026-04-23.md` | VERIFIED |
| `docs/family/ADAPTER_CONTRACT_v1.md` | VERIFIED |
| `docs/family/STABILITY_BATTERY_v1.md` | VERIFIED |
| `docs/PROMOTION_READINESS.md` | VERIFIED |
| `artifacts/blind_clone/03-01_transcript.md` | VERIFIED |
| `tests/test_adapter_contract_coverage.py` | VERIFIED |

## Repo Shape

| Field | Value |
| --- | --- |
| Proof Anchors | 6 display anchors |
| Portfolio | Gnosis |
| Package | gnosis-morph-bench |
| Primary Source | `src/gnosis_morph_bench/` |
| Tests | `tests/` |
| Artifacts | `artifacts/blind_clone/`; `artifacts/smoke/` |
| Support Sections | Licensing; Quick Start; Upcoming Workstreams |

| Field | Value |
| --- | --- |
| Proof Anchors | 6 display anchors |
| Portfolio | Gnosis |
| Package | gnosis-morph-bench |
| Primary Source | `src/gnosis_morph_bench/` |
| Tests | `tests/` |
| Artifacts | `artifacts/blind_clone/`; `artifacts/smoke/` |
| Support Sections | Licensing; Quick Start; Upcoming Workstreams |

```
.
├── NOTICE                          # Apache-2.0 code and CC-BY-4.0 docs posture
├── PRD_GNOSIS_MORPH_BENCH_2026-04-23.md
├── README.md
├── pyproject.toml                     # Python ≥ 3.10, deps: numpy, scikit-learn
├── .github/workflows/ci.yml           # pytest on Ubuntu / Python 3.11
├── .gpd/                              # GPD orchestration state, plans, summaries
├── src/gnosis_morph_bench/
│   ├── adapters/indus_phase4.py       # v1 adapter (CLI: gnosis-morph-bench-adapter-indus-phase4)
│   ├── benchmark.py                   # route scoring, NMI + null + sigma + silhouette
│   ├── stability.py                   # 5-mode stability battery
│   ├── replay.py                      # ReplayRecord emission
│   ├── schema.py                      # BenchmarkManifest, freeze_reference
│   ├── cli.py / __main__.py           # smoke + replay subcommands
│   ├── hf_cache.py                    # SHA-pinned HF dataset fetch
│   └── _utils.py                      # repo-local JSON / hash helpers
├── tests/                             # 37 tests across 9 files
├── fixtures/tiny_benchmark_manifest.json
├── artifacts/
│   ├── smoke/smoke_report.json        # committed byte-reference (SHA-pinned)
│   ├── replay/                        # default replay output dir (gitignored content)
│   └── blind_clone/                   # cross-env blind-clone transcripts
├── docs/                              # promotion readiness, HF custody, legal prep, family contracts
└── code/                              # code-facing surface notes and current limits
```

## Licensing

This repository is part of the Zer0pa Gnosis Portfolio.

**Code** in this repository is licensed under the Apache License 2.0. See
`LICENSE` for the full text. SPDX identifier: `Apache-2.0`.

**Documentation, reports, and written materials** are licensed under Creative
Commons Attribution 4.0 International. SPDX identifier: `CC-BY-4.0`. Canonical
terms: <https://creativecommons.org/licenses/by/4.0/>.

**Data and fixtures** are handled per dataset and artifact family. See
`DATA_POLICY.md` for this repository's data boundary. The code license does not
license raw corpora, image-bearing cultural-heritage assets, private HF
artifacts, model weights, endpoint logs, or operational transcripts.

**Trademarks** - "Gnosis", "Zer0pa Gnosis", and distinctive sub-marks are
trademarks of Zer0pa. Apache-2.0 and CC-BY-4.0 do not grant trademark rights.
See `TRADEMARKS.md`.

Public visibility is a separate repository-setting action. The license files in
this repo define the intended open-source/open-documentation terms for released
Gnosis code and written materials; they do not publish rights-gated data.

## Quick Start

```bash
git clone https://github.com/Zer0pa/Morph-Bench.git
cd Morph-Bench
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'

# repo-local pytest suite
pytest -q

# synthetic smoke (deterministic, byte-stable)
python -m gnosis_morph_bench smoke fixtures/tiny_benchmark_manifest.json \
    --output artifacts/smoke/smoke_report.json

# full 5-mode stability + replay
python -m gnosis_morph_bench replay fixtures/tiny_benchmark_manifest.json \
    --output artifacts/replay/replay_record.json

# Indus Phase 4 v1 adapter (against fixture inputs only until Blocked-1 clears)
gnosis-morph-bench-adapter-indus-phase4 --help
```

For the full audit walkthrough: [`AUDITOR_PLAYBOOK.md`](AUDITOR_PLAYBOOK.md).

For what is and is not promotable today: [`docs/PROMOTION_READINESS.md`](docs/PROMOTION_READINESS.md).

For governance and status semantics: [`GOVERNANCE.md`](GOVERNANCE.md).

For release protocol and owner inputs: [`RELEASING.md`](RELEASING.md).

## Upcoming Workstreams

Open work across four categories. "Useful now, improving continuously" — every item here is surfaced honestly, not an apology.

### Operations / External Dependency

- **Blocked-1 — Phase 3c manifest admission:** live Indus Phase 4 rerun from repo custody cannot proceed without an admitted Phase 3c feature manifest JSON with SHA-256. Owner-gated. When clear: produces `artifacts/replay/indus_phase4_live_<date>.json`.
- **Blocked-3 — Heavy-data release policy:** image-bearing benchmark payloads cannot enter the repo until the release boundary is written (which asset classes, under what terms, storage location and size bound). Owner-gated. When clear: produces `DATA_POLICY.md §Image-Bearing Release` appendix.

### Active Engineering

- Cuneiform benchmark family adapter: deferred to a separate future contract per current scope decision; no active engineering until Blocked-1 live rerun lands and the v1 adapter is validated against a second source family.
- Smoke byte-reference re-freeze: local housekeeping only; re-run smoke and commit the new byte-reference when convenient. Not a promotion gate.

### Research-Deferred — Investigation Underway

_(none currently — all research surface is defined by the v1 adapter contract and the 5-mode stability battery)_

### Zero-Base Scientific Thinking — GPD Research and Planning Pending

_(none currently — the Phase 04 cuneiform contract is the next planned GPD unit; not yet initiated)_
