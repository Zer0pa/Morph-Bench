# Smoke Tests

## Goal

Prove that the staged repo installs and that the neutral smoke benchmark can
run without the live monorepo layout.

## Commands

```bash
python3 -m pip install -e .
gnosis-morph-bench-smoke fixtures/tiny_benchmark_manifest.json --output artifacts/smoke/smoke_report.json
```

## Expected Result

- the command exits successfully
- `artifacts/smoke/smoke_report.json` is created
- the report names both routes from the fixture and records route metrics,
  replay hashes, and leave-out Jaccard

## What This Smoke Path Does Not Prove

- it does not prove the full live Phase 4 source bundle has been rerun here
- it does not prove data-release readiness for real corpora
