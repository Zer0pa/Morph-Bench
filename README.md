# Gnosis Morph Bench

> **Benchmark and replay framework for the Gnosis methods lane.** This repo
> packages the neutral benchmark surface: route scoring, permutation-null
> metrics, stability checks, deterministic replay, SHA-256 reference freezes,
> and the first Indus Phase 4 adapter. It does not own Indus or cuneiform
> scientific verdicts.

## Current Authority

| Field | Current state |
|---|---|
| Commercial readiness | `STAGED` |
| Posture | `benchmark_methods_active_with_named_blockers` |
| Repo-local gate | `pytest -q` passes on Python 3.11 with 37 tests |
| Blind-clone replay evidence | Historical PASS: macOS 3.11.15 and Linux/RunPod 3.11.13 produced byte-identical synthetic smoke output |
| Coupling guard | PASS: `0 / 6` forbidden monorepo-pattern hits in `src/gnosis_morph_bench/` |
| Adapter-contract coverage | PASS: `9 / 9` `ADAPTER_CONTRACT_v1` MUST clauses mapped to tests |
| Live Indus Phase 4 values | Source-authority citations only: NMI 0.5793, Sigma 5.65, Jaccard 0.4351, replay 3/3 |

The live Indus values above are not claimed as Morph-Bench repo-custody proof.
They remain blocked on admitted Phase 3c manifest access. The proof boundary is
spelled out in [`docs/PROMOTION_READINESS.md`](docs/PROMOTION_READINESS.md) and
[`PUBLIC_AUDIT_LIMITS.md`](PUBLIC_AUDIT_LIMITS.md).

## Licensing

This repository is part of the Zer0pa Gnosis Portfolio.

**Code** is licensed under the Apache License 2.0. See [`LICENSE`](LICENSE).
SPDX identifier: `Apache-2.0`.

**Documentation, reports, and written materials** are licensed under Creative
Commons Attribution 4.0 International. SPDX identifier: `CC-BY-4.0`.

**Data, fixtures, corpora, image-bearing cultural-heritage assets, private HF
artifacts, model weights, endpoint logs, and operational transcripts** are not
licensed by the code or documentation licenses. Their boundary is governed by
[`DATA_POLICY.md`](DATA_POLICY.md), artifact-specific notices, and any future
owner admission record.

**Trademarks** - "Gnosis", "Zer0pa Gnosis", and distinctive sub-marks are
trademarks of Zer0pa. Apache-2.0 and CC-BY-4.0 do not grant trademark rights.
See [`TRADEMARKS.md`](TRADEMARKS.md).

Public visibility is a separate repository-setting action. The license files
define the intended open code/docs posture; they do not publish rights-gated
data.

## What This Repo Owns

- Neutral benchmark manifest schema and reference-freeze helpers.
- Route scoring with NMI, permutation nulls, sigma, and silhouette.
- Five-mode stability battery: deterministic replay, leave-fraction-out,
  noise injection, k-sensitivity, and seed variance.
- Indus Phase 4 v1 adapter shape, tested against synthetic Phase-4-like
  fixtures.
- SHA-pinned HF fetch helper for future admitted artifacts.
- Public-audit and promotion-readiness boundaries for what this repo can and
  cannot prove.

## What We Prove

- The package installs from repo custody and exposes the expected CLI entry
  points.
- The tiny synthetic benchmark fixture runs end-to-end through scoring,
  stability, replay, and reference freeze.
- The Indus Phase 4 v1 adapter satisfies every current MUST clause in
  [`docs/family/ADAPTER_CONTRACT_v1.md`](docs/family/ADAPTER_CONTRACT_v1.md).
- The package code is free of the forbidden hidden-import and path-coupling
  patterns named by the adapter contract.
- The historical blind-clone evidence shows synthetic smoke and replay output
  reproducible across macOS and Linux at the documented Python 3.11 floor.

## What We Do Not Claim

- We do not claim that Morph-Bench has reproduced the live Indus Phase 4
  measured values from repo custody. That requires an admitted Phase 3c feature
  manifest with SHA-256.
- We do not claim that synthetic smoke output proves any live Indus or
  cuneiform scientific finding.
- We do not claim that raw corpora, image-bearing payloads, private HF
  artifacts, or operational transcripts are public-release assets.
- We do not claim cuneiform adapter coverage under the v1 Indus adapter
  contract.
- We do not claim ownership of descriptors, kernels, image preprocessing, or
  domain verdicts. Those belong to other Gnosis lanes.

## Quick Start

```bash
git clone https://github.com/Zer0pa/Morph-Bench.git
cd Morph-Bench
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
pytest -q
```

Run the synthetic smoke path:

```bash
python -m gnosis_morph_bench smoke fixtures/tiny_benchmark_manifest.json \
  --output artifacts/smoke/smoke_report.json
```

Run the replay battery:

```bash
python -m gnosis_morph_bench replay fixtures/tiny_benchmark_manifest.json \
  --output artifacts/replay/replay_record.json
```

Inspect the Indus adapter interface:

```bash
gnosis-morph-bench-adapter-indus-phase4 --help
```

## Evidence Map

| Need | Path |
|---|---|
| Governing scope | [`PRD_GNOSIS_MORPH_BENCH_2026-04-23.md`](PRD_GNOSIS_MORPH_BENCH_2026-04-23.md) |
| Fast audit path | [`AUDITOR_PLAYBOOK.md`](AUDITOR_PLAYBOOK.md) |
| Promotion readiness | [`docs/PROMOTION_READINESS.md`](docs/PROMOTION_READINESS.md) |
| Public audit limits | [`PUBLIC_AUDIT_LIMITS.md`](PUBLIC_AUDIT_LIMITS.md) |
| Architecture map | [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) |
| Code-facing surface | [`code/README.md`](code/README.md) |
| Data and artifact boundary | [`DATA_POLICY.md`](DATA_POLICY.md) |
| Legal boundary summary | [`docs/LEGAL_BOUNDARIES.md`](docs/LEGAL_BOUNDARIES.md) |
| HF custody register | [`docs/HF_CUSTODY_REGISTER.md`](docs/HF_CUSTODY_REGISTER.md) |
| Blind-clone evidence | [`artifacts/blind_clone/`](artifacts/blind_clone/) |
| Adapter contract | [`docs/family/ADAPTER_CONTRACT_v1.md`](docs/family/ADAPTER_CONTRACT_v1.md) |
| Stability contract | [`docs/family/STABILITY_BATTERY_v1.md`](docs/family/STABILITY_BATTERY_v1.md) |

## Repo Shape

```text
.
├── README.md
├── LICENSE                         # Apache-2.0 code license
├── NOTICE                          # Apache-2.0 code / CC-BY-4.0 docs notice
├── DATA_POLICY.md                  # data and artifact admission boundary
├── PRD_GNOSIS_MORPH_BENCH_2026-04-23.md
├── pyproject.toml                  # Python >= 3.10, numpy, scikit-learn
├── .github/workflows/ci.yml        # hygiene scan + pytest on Ubuntu / Python 3.11
├── .gpd/                           # GPD orchestration state and historical phase records
├── src/gnosis_morph_bench/
│   ├── adapters/indus_phase4.py
│   ├── benchmark.py
│   ├── stability.py
│   ├── replay.py
│   ├── schema.py
│   ├── hf_cache.py
│   └── cli.py / __main__.py
├── tests/
├── fixtures/tiny_benchmark_manifest.json
├── artifacts/
│   ├── smoke/
│   ├── replay/
│   └── blind_clone/
└── docs/
```

## Active Gates

| Gate | State | Unblock |
|---|---|---|
| Phase 3c manifest admission | OPEN | Consumable feature manifest JSON with SHA-256 admitted to repo custody |
| Heavy-data/image-bearing release policy | OPEN | Owner policy naming admitted asset classes, terms, size bounds, and storage path |
| Cuneiform adapter contract | DEFERRED | Plan after the Indus live replay lands or a second-family adapter is explicitly authorized |
| Ops-Gates CI consumption | DEFERRED | Adopt after `Gnosis-Ops-Gates` self-CI is green and a Morph-compatible profile exists |

Open gates are surfaced because they matter. They do not convert the current
repo-local methods framework into a failure; they bound what can be claimed
from this repo today.
