# Gnosis Morph Bench

> Benchmark and replay framework for the Gnosis methods lane. Website-sync posture: staged/WIP, useful now, with named blockers.

## What This Is

`gnosis-morph-bench` is the benchmark-first methods repo for neutral morphology-route scoring, permutation-null metrics, stability checks, deterministic replay, SHA-256 reference freezes, and the first Indus Phase 4 adapter. It is a benchmark/replay framework, **not** an Indus verdict repo, not a cuneiform verdict repo, and not a descriptor/kernel owner.

Headline metric: `pytest -q` passes with **37 tests**, adapter-contract coverage is **9/9 MUST clauses**, and the package has **0/6 forbidden monorepo-pattern hits** in `src/gnosis_morph_bench/`. The historical blind-clone smoke record is byte-identical across macOS 3.11.15 and Linux/RunPod 3.11.13.

Honest blocker: live Indus Phase 4 values are source-authority citations only until the admitted Phase 3c feature manifest is available with SHA-256 custody. Heavy-data/image-bearing release policy is still separate from the code/docs license.

| Field | Value |
|-------|-------|
| Architecture | SYMBOL_MORPH_BENCHMARK |
| Encoding | MORPH_REPLAY_BENCH_V1 |

## Key Metrics

| Metric | Value | Baseline |
|---|---:|---|
| PYTEST_PASS | 37 passed | pytest |
| ADAPTER_MUST_COVERAGE | 9/9 | contract |
| FORBIDDEN_PATTERN_HITS | 0/6 | monorepo |
| CROSS_ENV_REPLAY | PASS | macOS/RunPod |

> Source: `.github/workflows/ci.yml`, `tests/test_adapter_contract_coverage.py`, `tests/test_forbidden_patterns.py`, `artifacts/blind_clone/`, and `docs/PROMOTION_READINESS.md`.

## What We Prove

- The package installs from repo custody and exposes the expected CLI entry points.
- The tiny synthetic benchmark fixture runs end-to-end through scoring, stability, replay, and reference freeze.
- The Indus Phase 4 v1 adapter satisfies every current MUST clause in `docs/family/ADAPTER_CONTRACT_v1.md`.
- The package code is free of the forbidden hidden-import and path-coupling patterns named by the adapter contract.
- The historical blind-clone evidence shows synthetic smoke and replay output reproducible across macOS and Linux at the documented Python 3.11 floor.

## What We Don't Claim

- We do not claim that Morph-Bench has reproduced the live Indus Phase 4 measured values from repo custody.
- We do not claim that synthetic smoke output proves any live Indus or cuneiform scientific finding.
- We do not claim that raw corpora, image-bearing payloads, private HF artifacts, or operational transcripts are public-release assets.
- We do not claim cuneiform adapter coverage under the v1 Indus adapter contract.
- We do not claim ownership of descriptors, kernels, image preprocessing, or domain verdicts.

## Commercial Readiness

| Field | Value |
|-------|-------|
| Verdict | STAGED |
| Commit SHA | 7f403c307ec8 |
| Source | docs/PROMOTION_READINESS.md |

The repo-local benchmark framework is usable today on synthetic fixtures with a deterministic, cross-environment, lint-clean surface. Public visibility remains separate and depends on admitted artifact/data boundaries and repo-manager review.

## Tests and Verification

| Code | Check | Verdict |
|---|---|---|
| V_01 | `pytest -q` | PASS |
| V_02 | adapter MUST-clause coverage | PASS |
| V_03 | forbidden monorepo-pattern lint | PASS |
| V_04 | historical blind-clone smoke/replay byte equality | PASS |

## Proof Anchors

| Path | State |
|---|---|
| `PRD_GNOSIS_MORPH_BENCH_2026-04-23.md` | VERIFIED |
| `docs/PROMOTION_READINESS.md` | VERIFIED |
| `PUBLIC_AUDIT_LIMITS.md` | VERIFIED |
| `docs/family/ADAPTER_CONTRACT_v1.md` | VERIFIED |
| `docs/family/STABILITY_BATTERY_v1.md` | VERIFIED |
| `artifacts/blind_clone/` | VERIFIED |
| `.github/workflows/ci.yml` | VERIFIED |
| `DATA_POLICY.md` | VERIFIED |

## Repo Shape

| Field | Value |
|---|---|
| Package | `gnosis-morph-bench` |
| Source | `src/gnosis_morph_bench/` |
| Tests | `tests/` |
| Fixture | `fixtures/tiny_benchmark_manifest.json` |
| Evidence | `artifacts/`, `docs/`, `.gpd/` |
| Legal/Data | `LICENSE`, `NOTICE`, `DATA_POLICY.md`, `docs/LEGAL_BOUNDARIES.md` |

## Quick Start

```bash
git clone https://github.com/Zer0pa/Morph-Bench.git
cd Morph-Bench
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
pytest -q
python -m gnosis_morph_bench smoke fixtures/tiny_benchmark_manifest.json   --output /tmp/gnosis_morph_smoke.json
```

## Upcoming Workstreams

> This section captures the active lane priorities — what the next agent or contributor picks up, and what investors should expect. Cadence is continuous, not milestoned.

- **Phase 3c manifest admission** — Operations / External Dependency. Admit the consumable Indus Phase 3c feature manifest with SHA-256 before live Indus Phase 4 values are claimed from Morph-Bench custody.
- **Heavy-data release policy** — Operations / External Dependency. Write the admitted asset classes, terms, size bounds, and storage path for image-bearing or large artifacts.
- **Cuneiform adapter contract** — Research-Deferred — Investigation Underway. Defer until the first real Indus replay lands or a second-family adapter is explicitly authorized.
- **Ops-Gates profile adoption** — Active Engineering. Adopt the Morph-compatible Ops-Gates profile once the provider contract is settled.

## Licensing

This repository is part of the Zer0pa Gnosis Portfolio.

**Code** in this repository is licensed under the Apache License 2.0. See `LICENSE`. SPDX identifier: `Apache-2.0`.

**Documentation, reports, and written materials** are licensed under Creative Commons Attribution 4.0 International. SPDX identifier: `CC-BY-4.0`.

**Data, fixtures, corpora, image-bearing cultural-heritage assets, private HF artifacts, model weights, endpoint logs, and operational transcripts** are not licensed by the code or documentation licenses. Their boundary is governed by `DATA_POLICY.md`, artifact-specific notices, and any future owner admission record.

**Trademarks** - "Gnosis", "Zer0pa Gnosis", and distinctive sub-marks are trademarks of Zer0pa. Apache-2.0 and CC-BY-4.0 do not grant trademark rights. See `TRADEMARKS.md`.

Public visibility is a separate repository-setting action. These license files define the open code/docs posture; they do not publish rights-gated data.
