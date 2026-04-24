# Gnosis Morph Bench

Neutral benchmark and replay scaffold for the Gnosis methods lane. Own route
comparison, permutation-null metrics, stability and Jaccard checks,
deterministic replay, and reference-freeze helpers — without pretending to
own Indus or cuneiform scientific verdicts.

## Phase Completion Status

All four GPD phases defined in
[`PRD_GNOSIS_MORPH_BENCH_2026-04-23.md`](PRD_GNOSIS_MORPH_BENCH_2026-04-23.md)
are complete on `main`.

| Phase | Title | Status |
|---|---|---|
| `00` | workstream-bootstrap | COMPLETE |
| `01` | source-admission-and-replay-design | COMPLETE |
| `02` | neutral-module-extraction | COMPLETE |
| `03` | blind-clone-and-promotion-review | COMPLETE |

Per-phase summaries live under [`.gpd/phases/`](.gpd/phases/). The
blind-clone disposition is **PASS** (primary macOS + secondary RunPod on
Python 3.11) — see
[`.gpd/phases/03-blind-clone-and-promotion-review/03-01-SUMMARY.md`](.gpd/phases/03-blind-clone-and-promotion-review/03-01-SUMMARY.md).

## What Is Promotable Today

The single source of truth for "what passes repo-custody vs what is blocked
vs what is scope-deferred" is
[`docs/PROMOTION_READINESS.md`](docs/PROMOTION_READINESS.md). That doc
enumerates four named blockers (Blocked-1 through Blocked-4) and three
owner decisions still pending. Every promotion question should anchor
there rather than inferring from this README.

**Passes today, clone-reproducible:** standalone `pip install -e .` on a
blind clone; the 32-case pytest suite plus 5 hf_cache tests (37 total);
the synthetic smoke benchmark byte-reference; the neutral `ReplayRecord`
shape; the zero-forbidden-monorepo-pattern lint; both
`console_scripts` entrypoints; the adapter and five-mode stability
battery against synthetic fixtures; cross-environment (macOS + Linux)
byte-identical smoke and replay output.

**Blocked on owner / external input:** admitted Indus Phase 3c feature
manifest access (Blocked-1); canonical `LICENSE` text (Blocked-2);
heavy-data release policy for image-bearing assets (Blocked-3).
Blocked-4 (committed smoke byte-reference re-freeze) closed on
2026-04-24.

## Current Authority

| Item | Current Truth |
|---|---|
| Product lane | `gnosis-morph-bench` |
| GitHub repo | [https://github.com/Zer0pa/Morph-Bench](https://github.com/Zer0pa/Morph-Bench) (private) |
| Default branch | `main` |
| HF org | `Zer0pa` — see [`docs/HF_STORAGE.md`](docs/HF_STORAGE.md) |
| Acquisition surface | `workstreams/gnosis-morph-bench/05_repo_scaffold/` inside the migration package |
| Current authority artifact | Source-repo Phase 4 bundle: `workspace/artifacts/indus/phase4/{publishable_finding.md, phase4_governing_verdict.md, governing_route_selection.json, stability_report.json, dt05_replay.json, icit_reference_frozen.json}` |
| Evidence status | `PARTIAL` |
| License | `OWNER_DEFERRED` — see [`LICENSE_PLACEHOLDER.md`](LICENSE_PLACEHOLDER.md) |
| Primary contact | `OWNER_DEFERRED` |

## CLI Surface

The package installs two console scripts plus a module-invocable CLI.

### `gnosis-morph-bench smoke`

Runs the minimal synthetic smoke pipeline against a `BenchmarkManifest`
JSON and emits a `SmokeReport`. The committed byte-reference at
[`artifacts/smoke/smoke_report.json`](artifacts/smoke/smoke_report.json)
has SHA-256
`020f97b83b2948c2cd529b975010e6e5132799d89e395539d6f6f928c97c184e`
(re-frozen 2026-04-24 against the current serializer; see
[`docs/family/STABILITY_BATTERY_v1.md`](docs/family/STABILITY_BATTERY_v1.md)).

```bash
# module form
python -m gnosis_morph_bench smoke fixtures/tiny_benchmark_manifest.json \
    --output artifacts/smoke/smoke_report.json

# equivalent console_script form
gnosis-morph-bench-smoke fixtures/tiny_benchmark_manifest.json \
    --output artifacts/smoke/smoke_report.json
```

This synthetic smoke is NOT a Phase 4 proof. It establishes that the
pipeline is deterministic and installs cleanly — nothing about the live
Indus verdict.

### `gnosis-morph-bench replay`

Runs the full five-mode stability battery (`deterministic_replay`,
`leave_fraction_out`, `noise_injection`, `k_sensitivity`,
`seed_variance`) and writes a `ReplayRecord` per
[`docs/family/STABILITY_BATTERY_v1.md`](docs/family/STABILITY_BATTERY_v1.md).

```bash
python -m gnosis_morph_bench replay fixtures/tiny_benchmark_manifest.json \
    --output artifacts/replay/replay_record.json \
    --clusters 3 \
    --null-repeats 200 \
    --replay-repeats 3 \
    --fraction 0.25 --fraction-repeats 6 \
    --noise-sigma 0.05 --noise-repeats 5 \
    --k-offsets=-1,1 \
    --seeds 7,11,19
```

### `gnosis-morph-bench-adapter-indus-phase4`

Translates an admitted Indus Phase 4 source family (feature manifest +
frozen-reference JSON) into a neutral `BenchmarkManifest`. Pending
Blocked-1; runs today against fixture inputs only.

```bash
gnosis-morph-bench-adapter-indus-phase4 \
    --feature-manifest <admitted-phase3c-manifest.json> \
    --reference-frozen <admitted-icit-reference-frozen.json> \
    --output artifacts/adapters/indus_phase4_benchmark_manifest.json \
    --run-record artifacts/adapters/indus_phase4_benchmark_manifest_run.json
```

The adapter contract is specified at
[`docs/family/ADAPTER_CONTRACT_v1.md`](docs/family/ADAPTER_CONTRACT_v1.md).

### `gnosis_morph_bench.hf_cache.fetch_artifact`

Stdlib-only SHA-256-pinned fetch-back from HF dataset repos per
[`docs/HF_STORAGE.md`](docs/HF_STORAGE.md). Hard-fails on SHA mismatch;
no artifact is trusted without a pin.

## Anti-Overclaim Stance

- The synthetic smoke path is NOT Phase 4 proof. Live Phase 4 rerun is
  blocked on admitted Phase 3c manifest access (Blocked-1).
- This repo does NOT claim the live Indus NMI / Sigma / Jaccard / replay
  quadruple as repo-custody evidence. Those remain source-authority
  numbers — see
  [`PUBLIC_AUDIT_LIMITS.md`](PUBLIC_AUDIT_LIMITS.md).
- This repo ships no canonical `LICENSE` file. The
  [`LICENSE_PLACEHOLDER.md`](LICENSE_PLACEHOLDER.md) is not legal
  authority.
- This repo does not vendor heavy corpora, image-bearing benchmark
  payloads, or review-pack artifacts. HF dataset repos are provisioned
  but remain empty placeholders until the blockers close.

## Read Next

| Need | File |
|---|---|
| What is promotable / blocked | [`docs/PROMOTION_READINESS.md`](docs/PROMOTION_READINESS.md) |
| Fastest outsider audit path | [`AUDITOR_PLAYBOOK.md`](AUDITOR_PLAYBOOK.md) |
| Public-audit boundaries | [`PUBLIC_AUDIT_LIMITS.md`](PUBLIC_AUDIT_LIMITS.md) |
| Data-release policy | [`DATA_POLICY.md`](DATA_POLICY.md) |
| HF storage strategy | [`docs/HF_STORAGE.md`](docs/HF_STORAGE.md) |
| Adapter contract v1 | [`docs/family/ADAPTER_CONTRACT_v1.md`](docs/family/ADAPTER_CONTRACT_v1.md) |
| Stability battery v1 | [`docs/family/STABILITY_BATTERY_v1.md`](docs/family/STABILITY_BATTERY_v1.md) |
| First replay target decision | [`docs/family/FIRST_REPLAY_TARGET_DECISION.md`](docs/family/FIRST_REPLAY_TARGET_DECISION.md) |
| Architecture and truth map | [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) |
| Governance and status semantics | [`GOVERNANCE.md`](GOVERNANCE.md) |
| Release protocol and owner inputs | [`RELEASING.md`](RELEASING.md) |
| Sovereign execution contract | [`PRD_GNOSIS_MORPH_BENCH_2026-04-23.md`](PRD_GNOSIS_MORPH_BENCH_2026-04-23.md) |
| Smoke instructions | [`SMOKE_TESTS.md`](SMOKE_TESTS.md) |

## Current Gaps

Gaps that will close when owner inputs land:

- Live Phase 4 rerun from repo custody — gated on Blocked-1.
- Public promotion — gated on Blocked-2 and Blocked-3.
- Cuneiform adapter work — deferred by scope; picked up after Blocked-1
  closes so adapter-contract v1 can be validated against a second source
  family.

All such items are enumerated, with unblock conditions, in
[`docs/PROMOTION_READINESS.md`](docs/PROMOTION_READINESS.md).
