---
phase: 02-neutral-module-extraction
plan: 02
status: completed
executed_on: 2026-04-24
plan_contract_ref: ".gpd/phases/02-neutral-module-extraction/02-02-PLAN.md"
tasks_completed: 5
tasks_total: 5
commits: 5
tests_total: 32
tests_passed: 32
tests_failed: 0
tests_xfailed: 0
---

# Summary: Plan 02-02 — Phase-4-Style Stability Battery + Replay Record

## One-liner

The neutral morph-bench package now exposes a complete five-mode stability
battery (replay, leave-fraction-out, noise-injection, k-sensitivity,
seed-variance) plus an aggregator, a `run_replay_record(...)` assembler that
emits a neutral `ReplayRecord` JSON, a two-subcommand CLI (`smoke` +
`replay`) with a backward-compatible single-positional shim, and a
`STABILITY_BATTERY_v1.md` binding spec — exercised end-to-end through a
32-case pytest suite including an adapter→replay Phase-4-like flow, all
with zero forbidden-pattern hits under `src/gnosis_morph_bench/`.

## Tasks completed

| Task | Name                                                                    | Commit     |
| ---- | ----------------------------------------------------------------------- | ---------- |
| 1    | Expose `cluster_labels` + publish `STABILITY_BATTERY_v1.md`             | `3c32730`  |
| 2    | Add `noise_injection`, `k_sensitivity`, `seed_variance`, `stability_battery` | `cdf0092`  |
| 3    | Add `replay.py` emitting neutral `ReplayRecord`                         | `eba153d`  |
| 4    | Refactor `cli.py` into `smoke` + `replay` subcommands                    | `5fb7e51`  |
| 5    | Tests: battery modes, replay record, CLI flows, lint scope              | `61e455e`  |

Task 1 resumed from a previously-interrupted executor session: the partial
`benchmark.py` diff and the draft `STABILITY_BATTERY_v1.md` both matched
the plan's first task and were committed as-is after confirming the 16
existing 02-01 tests stayed green.

## Files created

- `src/gnosis_morph_bench/__main__.py` (enables `python -m gnosis_morph_bench <cmd>`)
- `src/gnosis_morph_bench/replay.py` (new `run_replay_record` module)
- `docs/family/STABILITY_BATTERY_v1.md` (binding spec)
- `artifacts/replay/.gitkeep` (default output directory under repo custody)
- `tests/test_stability_modes.py` (9 tests)
- `tests/test_replay_record.py` (2 tests)
- `tests/test_cli_smoke.py` (2 tests)
- `tests/test_cli_phase4_like.py` (1 end-to-end test)

## Files modified

- `src/gnosis_morph_bench/benchmark.py` — private `_cluster_labels` renamed
  to public `cluster_labels(matrix, n_clusters, *, seed=42)`; callsite in
  `evaluate_route` updated.
- `src/gnosis_morph_bench/stability.py` — three new modes and the
  `stability_battery(...)` aggregator; `deterministic_replay` and
  `leave_fraction_out` gained a top-level `"mode"` key.
- `src/gnosis_morph_bench/cli.py` — refactored into `smoke` + `replay`
  subcommands with a legacy-invocation shim.
- `tests/test_forbidden_patterns.py` — two new tests confirming
  `replay.py` is scanned and a positive-control bad-`replay.py` line
  trips `phase3_common_import`.

## Test inventory

```
$ .venv/bin/pytest -q
................................                                         [100%]
32 passed in 4.23s
```

Breakdown (plan 02-01 + plan 02-02 combined):

- `tests/test_adapter_indus_phase4.py` — 11 tests (02-01)
- `tests/test_forbidden_patterns.py` — 4 tests (02-01: 2, 02-02: +2)
- `tests/test_adapter_contract_coverage.py` — 3 tests (02-01)
- `tests/test_stability_modes.py` — 9 tests (02-02)
- `tests/test_replay_record.py` — 2 tests (02-02)
- `tests/test_cli_smoke.py` — 2 tests (02-02)
- `tests/test_cli_phase4_like.py` — 1 test (02-02)

No xfails. No skips. Zero failures.

## Contract coverage

### Claims

- `claim-battery-complete` — **covered** by `test_modes_present`,
  `test_mode_payload_shape`,
  `test_noise_injection_zero_noise_is_identity`,
  `test_noise_injection_large_noise_perturbs`,
  `test_k_sensitivity_offsets_recorded`,
  `test_k_sensitivity_clips_at_lower_bound`,
  `test_seed_variance_payload`,
  `test_seed_variance_detects_real_seed_sensitivity`.
- `claim-replay-record` — **covered** by `test_replay_record_shape`,
  `test_replay_record_deterministic`.
- `claim-cli-phase4-like` — **covered** by `test_cli_smoke_subcommand`,
  `test_cli_smoke_legacy_path`, `test_phase4_like_adapter_to_replay`.
- `claim-forbidden-pattern-free` — **covered** by
  `test_forbidden_patterns_absent_from_src`,
  `test_positive_control_lint_is_live`,
  `test_replay_module_is_in_scan_set`,
  `test_positive_control_bad_replay_line_is_detected`.
- `claim-nan-policy-uniform` — **covered** by
  `test_nan_policy` (battery aborts on a NaN-injected manifest; the
  exception propagates with enough context to identify the failing row).

### Deliverables

- `deliv-stability-module` — produced at `src/gnosis_morph_bench/stability.py`.
  Contains `noise_injection`, `k_sensitivity`, `seed_variance`, and
  `stability_battery`, plus the existing `deterministic_replay`,
  `leave_fraction_out`, and `pairwise_jaccard`.
- `deliv-benchmark-module` — modified at
  `src/gnosis_morph_bench/benchmark.py`. Contains public `cluster_labels(...)`.
- `deliv-replay-module` — produced at `src/gnosis_morph_bench/replay.py`.
  Contains `run_replay_record(...)` and the `REPLAY_SCHEMA_VERSION` /
  `REPLAY_RECORD_TYPE` constants.
- `deliv-cli-module` — modified at `src/gnosis_morph_bench/cli.py` with
  two subparsers under `build_parser()`.
- `deliv-stability-doc` — produced at `docs/family/STABILITY_BATTERY_v1.md`.
- `deliv-replay-output-default` — `artifacts/replay/.gitkeep` created.

### Acceptance tests

- `test-modes-present` — **passed** (six symbols all callable).
- `test-mode-payload-shape` — **passed** (every mode + aggregator shape
  validated against fixture).
- `test-noise-injection` — **passed** (sigma=0 ⇒ Jaccard=1.0; sigma=5 ⇒
  min_jaccard<1.0 on 4 repeats).
- `test-k-sensitivity` — **passed** (effective_k values 2 and 4 recorded;
  a separate clipping test verifies lower-bound clipping at 2 with the
  `clipped` flag surfacing).
- `test-seed-variance` — **passed** (len(jaccards)==4; all summary fields
  finite; a sibling primitive test confirms `pairwise_jaccard` surfaces
  disagreement).
- `test-replay-record-shape` — **passed** (all required top-level keys;
  five stability modes; JSON-serializable).
- `test-replay-record-deterministic` — **passed** (back-to-back runs
  produce byte-identical JSON excluding `generated_utc`).
- `test-cli-smoke-regression` — **passed** (`smoke` subcommand + legacy
  shim).
- `test-cli-phase4-like-end-to-end` — **passed** (adapter-emitted
  manifest flows through `replay`; all five modes present;
  reference-freeze SHA matches).
- `test-nan-policy` — **passed** (battery aborts on NaN-injected manifest).
- `test-forbidden-patterns` — **passed** (zero hits; positive controls
  fire).

### Forbidden proxies

All four forbidden proxies in the plan are honored. Noise / k-sensitivity /
seed-variance are implemented in-package, not as wrappers around a live
script. No test asserts a recovered Phase 4 numeric value. No mode
silently zero-fills NaN (the battery inherits `extract_route_dataset` +
`cluster_labels` semantics and lets the exception propagate). No new
`workspace/artifacts/` default exists; the CLI defaults to repo-local
`artifacts/smoke/` and `artifacts/replay/`.

### Uncertainty markers honored

- **Seed-variance determinism**: ward linkage is seed-invariant given
  fixed inputs, so `seed_variance` on the tiny fixture returns
  `mean_jaccard == 1.0`. This is the correct, non-pathological outcome
  per `STABILITY_BATTERY_v1.md` and the plan's guidance. The test
  suite asserts Jaccards are in `[0, 1]` and summary fields are finite
  (not strictly below 1.0); a sibling test
  (`test_seed_variance_detects_real_seed_sensitivity`) exercises
  `pairwise_jaccard` on two genuinely different labelings to confirm
  the Jaccard surface would detect real seed sensitivity on a
  non-deterministic backend.
- **Noise-sigma units**: the doc and inline comments are explicit that
  `noise_sigma` is in standardized-feature units (post-StandardScaler),
  not raw-feature units. The tests use `sigma=5.0` specifically as a
  stress test rather than interpreting it as a "realistic perturbation".

## Forbidden-pattern scan

```
$ grep -rnE "(phase3_common|stroke_|sys\.path\.insert|parents\[|workspace/artifacts)" \
      src/gnosis_morph_bench/
(no output)
```

Zero hits across `benchmark.py`, `stability.py`, `replay.py`, `cli.py`,
`__main__.py`, `_utils.py`, `schema.py`, and `adapters/indus_phase4.py`.

## Conventions carried forward

- All outputs default to repo-local `artifacts/` (`artifacts/smoke/` for
  the smoke CLI; `artifacts/replay/` for the replay CLI).
- Schema version remains `1` for both `smoke_report.json` and the new
  `ReplayRecord` (`record_type = "replay_record_v1"`).
- Governing route name and reference key for the Phase-4-like fixtures:
  `pixel_full_concat_31d_single` and `icit_set` — unchanged from 02-01.
- JSON outputs use `sort_keys=True`, `indent=2`, trailing newline (via
  `_utils.write_json`).

## Deviations

One minor additive change not in the original task list: added
`src/gnosis_morph_bench/__main__.py` in Task 4 so the plan's own
verification steps (`python -m gnosis_morph_bench smoke ...` and
`python -m gnosis_morph_bench replay ...`) actually work. Without it the
module-as-script form raises `No module named gnosis_morph_bench.__main__`.
Classified as Deviation Rule 4 (missing component — correctness fix,
not scope change). Documented in the Task 4 commit message.

No other deviations. No physics redirects. No scope changes.

## What's ready for Phase 03 to consume

- A working `replay` subcommand that accepts any
  `BenchmarkManifest` — synthetic fixture or adapter-emitted — and
  emits a deterministic-at-fixed-seed `ReplayRecord` with all five
  stability modes.
- A binding `STABILITY_BATTERY_v1.md` spec that Phase 03's admitted
  replay against live Phase 3c data can cite without reinterpretation.
- A clean console-entrypoint path: `gnosis-morph-bench-smoke` still
  resolves to the smoke pipeline via the legacy shim, and a direct
  `python -m gnosis_morph_bench replay <manifest>` gets Phase 03 to a
  full battery in one step.
- A 32-case pytest suite that will catch regressions introduced by
  Phase 03 edits to benchmark/stability/replay code.
- Confirmed zero forbidden-pattern hits across every module the battery
  touches, so Phase 03's blind-clone install check inherits a clean
  scan.

## What this plan did NOT do

- Did NOT run the battery against admitted Phase 3c feature-manifest
  data (Phase 03 gate).
- Did NOT assert Phase 4 live numeric values (NMI 0.5793, Sigma 5.65,
  Jaccard 0.4351, Replay 3/3) — Phase 03 obligation.
- Did NOT sweep k across a wide range; fixed offsets `(-1, +1)` as
  specified.
- Did NOT add new clustering backends or silhouette variants.
- Did NOT edit `schema.py` or the 02-01 adapter module.
- Did NOT vendor any real Phase 4 data. Every fixture used is synthetic.
