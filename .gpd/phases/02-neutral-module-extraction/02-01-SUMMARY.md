---
phase: 02-neutral-module-extraction
plan: 01
status: completed
executed_on: 2026-04-24
plan_contract_ref: ".gpd/phases/02-neutral-module-extraction/02-01-PLAN.md"
tasks_completed: 6
tasks_total: 6
commits: 6
tests_total: 16
tests_passed: 16
tests_failed: 0
tests_xfailed: 0
---

# Summary: Plan 02-01 — Indus Phase 4 v1 Adapter

## One-liner

Indus Phase 4 v1 adapter and its repo-local utility module are implemented,
wired as a console entrypoint, validated against synthetic Phase-4-shaped
fixtures through a 16-case pytest suite, and enforced to be free of the six
forbidden monorepo-coupling patterns by a live lint with a positive-control
case.

## Tasks completed

| Task | Name                                                                    | Commit      |
| ---- | ----------------------------------------------------------------------- | ----------- |
| 1    | Scaffold adapter subpackage and `_utils.py`                              | `ccbee89`   |
| 2    | Implement `adapters/indus_phase4.py` + console entrypoint                | `e61cb0c`   |
| 3    | Synthetic Phase-4-like fixtures and pytest `conftest.py`                 | `7a7457d`   |
| 4    | Adapter behavior tests (CLI surface, round-trip, freeze, NaN, labels)    | `6abe835`   |
| 5    | Forbidden-pattern lint with positive control                             | `9664e5d`   |
| 6    | ADAPTER_CONTRACT_v1 MUST-clause coverage map                              | `9a5ad6b`   |

## Files created

- `src/gnosis_morph_bench/adapters/__init__.py`
- `src/gnosis_morph_bench/adapters/indus_phase4.py`
- `src/gnosis_morph_bench/_utils.py`
- `tests/__init__.py`
- `tests/conftest.py`
- `tests/fixtures/phase4_like_feature_manifest.json`
- `tests/fixtures/phase4_like_reference_frozen.json`
- `tests/fixtures/phase4_like_reference_frozen_mismatch.json`
- `tests/test_adapter_indus_phase4.py`
- `tests/test_forbidden_patterns.py`
- `tests/test_adapter_contract_coverage.py`

## Files modified

- `pyproject.toml` — added `gnosis-morph-bench-adapter-indus-phase4` console
  script and a `dev` optional-dependency set pinning pytest.
- `.gitignore` — ignore the local `.venv/`.

## Test inventory

```
$ pytest tests/ -q
................                                                         [100%]
16 passed in 1.48s
```

Breakdown:

- `tests/test_adapter_indus_phase4.py` — 11 tests
  - `test_adapter_cli_surface`
  - `test_required_flags_marked_required`
  - `test_adapter_roundtrip`
  - `test_freeze_parity`
  - `test_freeze_mismatch_exit_code`
  - `test_label_surface_carried`
  - `test_label_surface_dropped`
  - `test_nan_strict_default`
  - `test_drop_item_with_nan_flag`
  - `test_include_route_whitelist`
  - `test_output_defaults_under_artifacts_adapters`
- `tests/test_forbidden_patterns.py` — 2 tests
  - `test_forbidden_patterns_absent_from_src`
  - `test_positive_control_lint_is_live`
- `tests/test_adapter_contract_coverage.py` — 3 tests
  - `test_every_must_clause_is_covered`
  - `test_coverage_map_has_no_stale_slugs`
  - `test_coverage_map_includes_core_acceptance_tests`

Live-checks performed during development:

- Injected `from phase3_common import x` into `_utils.py` → lint failed with
  pinpointed file and line; reverted.
- Appended a synthetic uncovered `MUST` line to `ADAPTER_CONTRACT_v1.md` →
  contract-coverage test failed naming the new slug; reverted.

## Contract coverage

All nine unique `MUST` slugs in `docs/family/ADAPTER_CONTRACT_v1.md` are
mapped to at least one acceptance-test id in
`tests/test_adapter_contract_coverage.py::MUST_COVERAGE`. No `xfail`
markers are needed: every MUST clause is satisfied by the implementation
and exercised by at least one runtime test. No unsatisfied clauses.

## Forbidden-pattern scan

Six patterns scanned over every `*.py` file under
`src/gnosis_morph_bench/` (including the new adapter and utils modules).
Zero hits. The lint's positive-control test confirms all six pattern ids
fire on a synthetic string that carries each forbidden construct.

The one place `Path(__file__).parent` appears is in the test file
`tests/test_forbidden_patterns.py` itself, to resolve the scan root
repo-locally. That usage is outside the `src/` scan and is not a
forbidden pattern in the ledger (only depth-indexed `.parents[N]` is).

## Contract results

### Claims

- `claim-contract-surface` — **covered** by `test_adapter_cli_surface`,
  `test_required_flags_marked_required`, `test_adapter_roundtrip`.
- `claim-forbidden-pattern-free` — **covered** by
  `test_forbidden_patterns_absent_from_src` and
  `test_positive_control_lint_is_live`.
- `claim-reference-freeze-parity` — **covered** by `test_freeze_parity`
  and `test_freeze_mismatch_exit_code`.
- `claim-domain-neutrality` — **covered** by `test_label_surface_carried`
  and `test_label_surface_dropped`.

### Deliverables

- `deliv-adapter-module` — produced at
  `src/gnosis_morph_bench/adapters/indus_phase4.py`.
- `deliv-adapter-package-init` — produced at
  `src/gnosis_morph_bench/adapters/__init__.py`.
- `deliv-utils-module` — produced at `src/gnosis_morph_bench/_utils.py`.
- `deliv-adapter-run-record` — produced by the adapter alongside the
  manifest; schema conforms to the contract's "Adapter Run Record"
  section and is validated by `test_freeze_parity` and
  `test_freeze_mismatch_exit_code`.
- `deliv-entrypoint` — added to `pyproject.toml` under `[project.scripts]`.
- `deliv-phase4-like-fixture`, `deliv-phase4-like-frozen`,
  `deliv-phase4-like-frozen-mismatch` — produced at
  `tests/fixtures/`.

### Acceptance tests

- `test-adapter-cli-surface` — **passed**.
- `test-adapter-roundtrip` — **passed** (NMI=1.0 on the synthetic
  fixture where governing route separates the three label groups
  cleanly; NMI is a finite float in [0, 1]).
- `test-freeze-parity` — **passed** (run-record SHA matches fixture
  SHA byte-for-byte).
- `test-freeze-mismatch-exit-code` — **passed** (exit 2; stderr names
  `icit_set`; run record still written with
  `contract_violation_reason`).
- `test-label-surface-carried` — **passed**.
- `test-label-surface-dropped` — **passed** (no occurrences of
  `provenance_url`, `authorial_note`, `stroke_encoding`, or the two
  broken route names in the emitted manifest bytes).
- `test-forbidden-patterns` — **passed** (zero hits across six
  patterns; positive control fires).
- `test-adapter-contract-coverage` — **passed** (9/9 MUST slugs
  mapped; stale-slug guard green; core-id floor green).

### Forbidden proxies

All three forbidden proxies in the plan are honored. No test in this
plan asserts a recovered Phase 4 numeric value. No code in the
implementation reads live scripts from a sibling repo. The
forbidden-pattern lint scans raw file bytes — comments and docstrings
do not hide matches (verified by injecting and then reverting a bad
`phase3_common` import).

## What's ready for Plan 02-02 to consume

- A working `translate(...)` function that emits a neutral
  `BenchmarkManifest` payload from the Phase-4-shaped upstream JSON
  shape. Plan 02-02's replay CLI can rely on the adapter surface being
  in place.
- A `gnosis_morph_bench._utils` module exposing `read_json`,
  `write_json`, `sha256_file`, and `utc_now_iso`. Plan 02-02 should
  reuse these and NOT add parallel helpers.
- Three synthetic Phase-4-shaped fixtures under `tests/fixtures/`.
  Plan 02-02 can reuse the good fixture for any test that needs a
  neutral-manifest input derivable from an adapter run.
- A `ContractViolation` exception type at
  `gnosis_morph_bench.adapters.indus_phase4.ContractViolation`. Plan
  02-02's stability-battery additions should raise the same type (or
  its sibling) on upstream-shape violations rather than inventing a
  new exception tier.
- A live forbidden-pattern lint that Plan 02-02's new modules
  (`stability.py` additions, `replay.py`, CLI refactor) will be
  scanned against automatically.

## Conventions carried forward

- Output root for adapter artifacts: `artifacts/adapters/` (repo-local).
  No `workspace/...` anywhere.
- Governing route name: `pixel_full_concat_31d_single`.
- Governing reference key in fixtures: `icit_set`.
- Schema version: `1`.
- All JSON emitted with `sort_keys=True`, `indent=2`, trailing newline.

## Deviations

None. Plan executed end-to-end in the order the plan specifies, with
zero scope changes, zero physics/method redirects, and zero unresolved
contract gaps.

## Notes on the Python 3.10+ requirement

The repo declares `requires-python = ">=3.10"`. The execution host has
system Python 3.9. A local `.venv/` was created with `/usr/local/bin/
python3.11` and added to `.gitignore`. This is a runtime-environment
detail and does not affect any checked-in content.
