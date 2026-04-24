# 03-01 Blind-Clone Transcript

Plan: `.gpd/phases/03-blind-clone-and-promotion-review/03-01-PLAN.md`
Date: 2026-04-24

## Clone provenance

- commit_sha: `0c323026ba0195d3c615916a952fb2f5a8d40745`
- source (primary clone): `"/Users/zer0palab/Gnosis Portfolio/workstreams/gnosis-morph-bench/05_repo_scaffold"` (local file URL, per PRD note that the public remote is still deferred; remote origin points at `https://github.com/Zer0pa/Morph-Bench.git`)
- primary clone root: `/tmp/blind-clone-1777002228/clone`
- primary venv: `/tmp/blind-clone-1777002228/clone/.venv` (python3.11)
- python_version: `Python 3.11.15`
- secondary clone root: `/workspace/blind-clone-<epoch>/clone` on RunPod pod `7k3riasglemecu`
- remote declared by clone: `https://github.com/Zer0pa/Morph-Bench.git`

## Primary (macOS) run

### Step 1 — Work root

```
CLONE_ROOT=/tmp/blind-clone-1777002228
mkdir -p "$CLONE_ROOT"
```

### Step 2 — Clone source HEAD

```
git -C "/Users/zer0palab/Gnosis Portfolio/workstreams/gnosis-morph-bench/05_repo_scaffold" rev-parse HEAD
→ 0c323026ba0195d3c615916a952fb2f5a8d40745
git clone "/Users/zer0palab/Gnosis Portfolio/workstreams/gnosis-morph-bench/05_repo_scaffold" "$CLONE_ROOT/clone"
→ Cloning into '/tmp/blind-clone-1777002228/clone'... done.
git -C "$CLONE_ROOT/clone" rev-parse HEAD
→ 0c323026ba0195d3c615916a952fb2f5a8d40745   # matches source
```

### Step 3 — Create fresh Python 3.11 venv

```
/usr/local/bin/python3.11 --version → Python 3.11.15
/usr/local/bin/python3.11 -m venv "$CLONE_ROOT/clone/.venv"
.venv/bin/python -m pip install --upgrade pip setuptools wheel
→ Successfully installed packaging-26.1 setuptools-82.0.1 wheel-0.47.0 (plus pip 26.0.1 preinstalled)
```

Environment capture appended to `artifacts/blind_clone/03-01_env.txt` under `## primary`.

### Step 4 — `pip install -e .`

```
.venv/bin/pip install -e .
```

Tail:

```
Building wheels for collected packages: gnosis-morph-bench
  Building editable for gnosis-morph-bench (pyproject.toml): finished with status 'done'
  Created wheel for gnosis-morph-bench: filename=gnosis_morph_bench-0.1.0-0.editable-py3-none-any.whl size=3819
Successfully built gnosis-morph-bench
Installing collected packages: threadpoolctl, numpy, joblib, scipy, scikit-learn, gnosis-morph-bench
Successfully installed gnosis-morph-bench-0.1.0 joblib-1.5.3 numpy-2.4.4 scikit-learn-1.8.0 scipy-1.17.1 threadpoolctl-3.6.0
```

Exit code: 0. Resolver installed `numpy-2.4.4` (major bump over the `numpy>=1.26` pin) and `scikit-learn-1.8.0` (above the `>=1.5` pin). This is relevant to the smoke byte-equality outcome below.

### Step 5 — Console script resolution

```
.venv/bin/gnosis-morph-bench-smoke --help
→ usage: gnosis-morph-bench [-h] {smoke,replay} ...
  Neutral morph-bench CLI. `smoke` runs the minimal synthetic smoke path;
  `replay` runs the full five-mode stability battery and emits a ReplayRecord.
  ...
  exit_code=0

.venv/bin/gnosis-morph-bench-adapter-indus-phase4 --help
→ usage: gnosis-morph-bench-adapter-indus-phase4 [-h] --feature-manifest ...
  Translate an admitted Indus Phase 4 source family into a neutral BenchmarkManifest.
  ...
  exit_code=0
```

Both console scripts resolve. Both `--help` invocations exit 0.

### Step 6 — Smoke parity check

```
.venv/bin/python -m gnosis_morph_bench smoke fixtures/tiny_benchmark_manifest.json \
    --output artifacts/smoke/smoke_report.json
→ "artifacts/smoke/smoke_report.json"

shasum -a 256 artifacts/smoke/smoke_report.json              (clone)
→ 020f97b83b2948c2cd529b975010e6e5132799d89e395539d6f6f928c97c184e
shasum -a 256 <repo-root>/artifacts/smoke/smoke_report.json  (committed)
→ 19d49d6b9837770f04cc8a8be6da9c3bc37fa0b3dfb17afa08fe068b94ef0349
```

Byte-equality (`test-smoke-byte-equal`): **FAIL**.

Drift sources (each named explicitly per the plan's forbidden-proxies
`fp-numeric-equality-as-default` constraint):

1. **JSON key ordering.** The committed reference uses insertion order;
   the clone output sorts keys alphabetically (`json.dumps(..., sort_keys=True)`
   was introduced in the serializer path between the artifact commit and now).
2. **Trailing newline.** Committed reference has no terminal `\n`; clone
   output has one.
3. **Extra schema fields in stability-mode payloads.** The clone's
   `replay` sub-object carries `"mode": "deterministic_replay"` and
   `"repeats": 3`; the clone's `leave_fraction_out` sub-object carries
   `"mode": "leave_fraction_out"`. These `mode` fields are mandated by
   `docs/family/STABILITY_BATTERY_v1.md` (every per-mode payload carries a
   `"mode"` string that matches the function name). The committed artifact
   predates that convention; the field is purely additive and carries no
   numeric content.

Numeric-fallback comparison (`test-smoke-numeric-fallback`) — independent
field-by-field check at 1e-6 tolerance on every scalar, exact match on
every SHA-256 and every label assignment:

```
extra keys in clone.replay: ['mode', 'repeats']
extra keys in clone.leave_fraction_out: ['mode']
committed ends with newline: False
clone ends with newline: True
key-order identical: False
=== numeric-field comparison errors ===
all numeric fields match within 1e-6; all SHA-256 and labels match exactly
```

`test-smoke-numeric-fallback`: **PASS**.

Carried back as `artifacts/blind_clone/03-01_smoke_report.clone.json`
(byte-for-byte copy of the clone output; not reformatted).

### Step 7 — Replay record check

```
.venv/bin/python -m gnosis_morph_bench replay fixtures/tiny_benchmark_manifest.json \
    --output artifacts/replay/replay_record.json
→ "artifacts/replay/replay_record.json"
```

Structure probe:

```
top-level keys: ['best_route', 'config', 'generated_utc', 'manifest_name',
                 'record_type', 'reference_freeze', 'reference_key',
                 'route_results', 'schema_version', 'stability']
stability.modes keys: ['deterministic_replay', 'k_sensitivity',
                       'leave_fraction_out', 'noise_injection',
                       'seed_variance']
record_type: 'replay_record_v1'
schema_version: 1
reference_freeze.sha256: 'ebfffd56bf433200c646f8d215a4832385f7ab80ed55ab78655495aa56aa360c'
stability.modes.deterministic_replay.all_identical: True
stability.modes.deterministic_replay.hashes[0]:
  '8128468760997c55454b7e2d4abaa7d39767cf293721989abbd41942b5dc7a31'
```

Per-assertion:

- `record_type == "replay_record_v1"`: PASS.
- `schema_version == 1`: PASS.
- Exactly five stability modes present under `stability.modes`: PASS. The
  canonical names per `docs/family/STABILITY_BATTERY_v1.md §Modes` are
  `deterministic_replay`, `leave_fraction_out`, `noise_injection`,
  `k_sensitivity`, `seed_variance`. The plan frontmatter calls the first
  mode `replay` as shorthand; the canonical artifact name is
  `deterministic_replay` and both test IDs `test-replay-record-shape` and
  `test-replay-all-identical` read against it directly.
- `reference_freeze.sha256` populated: PASS (`ebfffd56…60c`).
- `stability.modes.deterministic_replay.all_identical is True`: PASS.

`test-replay-record-shape`: PASS.
`test-replay-all-identical`: PASS.

Carried back as `artifacts/blind_clone/03-01_replay_record.clone.json`.

### Step 8 — Pytest

```
.venv/bin/pip install pytest
→ Successfully installed iniconfig-2.3.0 pluggy-1.6.0 pygments-2.20.0 pytest-9.0.3

.venv/bin/pytest -q tests/
→ ................................                                         [100%]
→ 32 passed in 3.53s
```

`test-pytest-32-pass`: **PASS** (final line `32 passed`; 0 failed, 0 xfailed,
0 skipped).

Carried back as `artifacts/blind_clone/03-01_pytest.txt`.

### Step 9 — External forbidden-pattern scan

```
grep -rnE "(phase3_common|stroke_|sys\.path\.insert|parents\[|workspace/artifacts|^from workspace\.|^from scripts\.)" src/gnosis_morph_bench/
→ (empty stdout)
exit 1   # grep-no-match == acceptance PASS
```

10 Python files scanned under `src/gnosis_morph_bench/`. Zero hits across
all six forbidden patterns from
`../../02_source_inventory/PATH_REWRITE_LEDGER.md`.

`test-forbidden-scan-zero-hits`: **PASS**.

Carried back as `artifacts/blind_clone/03-01_forbidden_pattern_scan.txt`
(empty file is the PASS shape).

## Secondary (RunPod) run

See Task 2 below. This section is authored after the RunPod secondary run
attempt; until Task 2 extends it, the secondary is not yet reported.

## Acceptance test results

| Test id                             | Status    | Evidence                                             |
|-------------------------------------|-----------|------------------------------------------------------|
| `test-install-success`              | PASS      | Step 4 tail + `03-01_env.txt` `## primary` section   |
| `test-entrypoints-resolve`          | PASS      | Step 5 `--help` outputs, both exit 0                 |
| `test-smoke-byte-equal`             | FAIL      | Step 6 sha mismatch; drift sources named             |
| `test-smoke-numeric-fallback`       | PASS      | Step 6 numeric-field parser; 0 mismatches at 1e-6    |
| `test-replay-record-shape`          | PASS      | Step 7 structure probe; five canonical modes present |
| `test-replay-all-identical`         | PASS      | Step 7 `deterministic_replay.all_identical is True`  |
| `test-pytest-32-pass`               | PASS      | Step 8 `32 passed`                                   |
| `test-forbidden-scan-zero-hits`     | PASS      | Step 9 empty stdout, grep exit 1                     |
| `test-runpod-env-reported`          | see Task 2| Appended below                                        |

Primary-run disposition: **PASS with named numeric fallback on smoke parity.**

## Environment gaps and unblock items

(Filled by Task 2 once the RunPod secondary attempt runs.)

## Disposition

(Final line written at the end of Task 2.)
