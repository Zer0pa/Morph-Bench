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

Pod: `7k3riasglemecu` at `root@38.80.152.147:34587`. SSH with
`ssh -i ~/.ssh/id_ed25519 -p 34587 root@38.80.152.147`.

### Step S-1 — Connect and probe interpreters

```
ssh ... -p 34587 root@38.80.152.147 → CONNECT_OK
uname -a         → Linux b7fb18eddf65 6.8.0-100-generic #100-Ubuntu SMP ...
python3 --version → Python 3.8.10   (legacy symlink /usr/bin/python3 → python3.8)
pip3 --version   → pip 25.1.1 from /usr/local/lib/python3.13/dist-packages/pip (python 3.13)
whoami           → root
SHELL            → /bin/bash
```

**Important finding:** the pod's default `python3` reports 3.8.10, BUT the
pod actually ships multiple modern interpreters at fixed paths:

```
/usr/bin/python3.8   → Python 3.8.10
/usr/bin/python3.9   (present)
/usr/bin/python3.10  (present)
/usr/bin/python3.11  → Python 3.11.13
/usr/bin/python3.12  (present)
/usr/bin/python3.13  → Python 3.13.5
```

This is a disconfirming observation against the plan frontmatter's
`approximation: "Secondary clone runs on a Python older than the declared
floor"`. The pod image has upgraded; `/usr/bin/python3.11` is directly
available without uv, deadsnakes, or any privileged install step. Per the
plan's `disconfirming_observations`:

> If the 03-01 RunPod secondary run PASSED (Python 3.11 was successfully
> installed on the pod), then the 'RunPod environment readiness' item
> moves from BLOCKED to PASS-NOW...

The secondary run therefore proceeds with `/usr/bin/python3.11` directly.
No `uv python install` was needed; no `apt-get`/deadsnakes was needed.
This is recorded here so the move from BLOCKED to PASS-NOW is honest and
traceable.

### Step S-2 — Fresh work root and clone from PUBLIC remote

```
CLONE_ROOT=/workspace/blind-clone-1777002679
mkdir -p "$CLONE_ROOT"
git clone https://github.com/Zer0pa/Morph-Bench.git "$CLONE_ROOT/clone"
→ Cloning into '/workspace/blind-clone-1777002679/clone'... done.
git -C "$CLONE_ROOT/clone" rev-parse HEAD
→ 0c323026ba0195d3c615916a952fb2f5a8d40745   # matches macOS primary
git -C "$CLONE_ROOT/clone" remote get-url origin
→ https://github.com/Zer0pa/Morph-Bench.git
```

The public remote `https://github.com/Zer0pa/Morph-Bench.git` is reachable
from the pod and already carries the exact HEAD the primary run exercised
(`0c32302…`). Note: the Task-1 commit `f81ba98…` lands on origin only after
Phase 03 is pushed, so the secondary clone could not include it; that is
the expected shape of a secondary run that bracket-tests the HEAD the
primary run started from.

### Step S-3 — Create fresh Python 3.11 venv

```
/usr/bin/python3.11 -m venv "$CLONE_ROOT/clone/.venv"
"$CLONE_ROOT/clone/.venv/bin/python" --version → Python 3.11.13
pip install --upgrade pip setuptools wheel
→ Successfully installed packaging-26.1 pip-26.0.1 setuptools-82.0.1 wheel-0.47.0
```

Floor check: `3.11.13 >= 3.10` → PASS.

### Step S-4 — `pip install -e .`

Tail:

```
Building wheels for collected packages: gnosis-morph-bench
  Created wheel for gnosis-morph-bench: filename=gnosis_morph_bench-0.1.0-0.editable-py3-none-any.whl
    size=3818 sha256=6d032ef5049761c04502d2a46a3ec470d6af545506c8ef470220ec9f7ce245c2
Successfully built gnosis-morph-bench
Installing collected packages: threadpoolctl, numpy, joblib, scipy, scikit-learn, gnosis-morph-bench
Successfully installed gnosis-morph-bench-0.1.0 joblib-1.5.3 numpy-2.4.4 scikit-learn-1.8.0 scipy-1.17.1 threadpoolctl-3.6.0
```

Exit 0. Identical dependency resolution to macOS primary (numpy 2.4.4,
scikit-learn 1.8.0, scipy 1.17.1).

### Step S-5 — Console script resolution

```
.venv/bin/gnosis-morph-bench-smoke --help               → exit 0
.venv/bin/gnosis-morph-bench-adapter-indus-phase4 --help → exit 0
```

Both resolve with identical help banner to macOS primary.

### Step S-6 — Smoke parity check (secondary)

```
.venv/bin/python -m gnosis_morph_bench smoke fixtures/tiny_benchmark_manifest.json \
    --output artifacts/smoke/smoke_report.json
sha256sum artifacts/smoke/smoke_report.json
→ 020f97b83b2948c2cd529b975010e6e5132799d89e395539d6f6f928c97c184e
```

Cross-environment parity:

| source                                    | sha256        |
|-------------------------------------------|---------------|
| committed `artifacts/smoke/smoke_report.json` | `19d49d6b…ef0349` |
| macOS primary clone output                | `020f97b8…c184e`  |
| RunPod secondary clone output             | `020f97b8…c184e`  |

The two blind clones produce **byte-identical** smoke output across macOS
x86_64 and Linux x86_64 on Python 3.11. The committed reference diverges
from both clones by the same three drift sources named in Step 6 (JSON
key ordering; trailing newline; additive `mode` / `repeats` fields).

`test-smoke-byte-equal` (vs committed): FAIL (same three drift sources).
`test-smoke-numeric-fallback` (vs committed): PASS (identical numeric
content; same analysis as macOS primary).
Cross-environment byte-equality (macOS clone ↔ RunPod clone): PASS
(same `020f97b8…` sha on both).

### Step S-7 — Replay record shape (secondary)

```
.venv/bin/python -m gnosis_morph_bench replay fixtures/tiny_benchmark_manifest.json \
    --output artifacts/replay/replay_record.json
```

Structure probe on the retrieved `replay_record.json`:

```
record_type: 'replay_record_v1'
schema_version: 1
stability.modes keys: ['deterministic_replay', 'k_sensitivity',
                       'leave_fraction_out', 'noise_injection',
                       'seed_variance']
missing: []
reference_freeze.sha256: 'ebfffd56bf433200c646f8d215a4832385f7ab80ed55ab78655495aa56aa360c'
stability.modes.deterministic_replay.all_identical: True
```

Cross-environment replay comparison (macOS clone vs RunPod pod, excluding
`generated_utc` wall-clock): **byte-identical**.

`test-replay-record-shape` (secondary): PASS.
`test-replay-all-identical` (secondary): PASS.

### Step S-8 — Pytest (secondary)

```
.venv/bin/pip install pytest
→ Successfully installed iniconfig-2.3.0 pluggy-1.6.0 pygments-2.20.0 pytest-9.0.3
.venv/bin/pytest -q tests/
→ ................................                                         [100%]
→ 32 passed in 9.50s
```

`test-pytest-32-pass` (secondary): **PASS**.

### Step S-9 — Forbidden-pattern scan (secondary)

```
grep -rnE "(phase3_common|stroke_|sys\.path\.insert|parents\[|workspace/artifacts|^from workspace\.|^from scripts\.)" src/gnosis_morph_bench/
GREP_EXIT=1   # no matches → PASS
```

`test-forbidden-scan-zero-hits` (secondary): **PASS**.

### Step S-10 — `test-runpod-env-reported`

The transcript records:

- starting `python3 --version` (3.8.10),
- the pod's actual interpreter inventory (3.8, 3.9, 3.10, 3.11, 3.12, 3.13
  all present at `/usr/bin/`),
- the exact command used to satisfy the floor (`/usr/bin/python3.11 -m
  venv …` — no uv, no deadsnakes, no privilege escalation required),
- the outcome (full green battery: install + smoke + replay + pytest +
  forbidden-pattern scan, all PASS on the pod),
- cross-environment parity evidence (identical smoke sha, identical
  replay record modulo `generated_utc`).

`test-runpod-env-reported`: **PASS** (Option (a): pod brought above
Python 3.10 floor; same battery rerun; no softening).

## Acceptance test results

| Test id                             | Primary | Secondary | Evidence                                                      |
|-------------------------------------|---------|-----------|---------------------------------------------------------------|
| `test-install-success`              | PASS    | PASS      | Steps 4, S-4 install tails; `03-01_env.txt` both sections     |
| `test-entrypoints-resolve`          | PASS    | PASS      | Steps 5, S-5 `--help` exit 0                                  |
| `test-smoke-byte-equal` (vs committed) | FAIL | FAIL      | Clone sha `020f97b8…` ≠ committed `19d49d6b…` (same drift both envs) |
| `test-smoke-numeric-fallback`       | PASS    | PASS      | Steps 6, S-6 numeric parser — all scalars within 1e-6, SHAs and labels exact |
| `test-replay-record-shape`          | PASS    | PASS      | Steps 7, S-7 structure probe — 5 canonical modes present      |
| `test-replay-all-identical`         | PASS    | PASS      | Steps 7, S-7 `deterministic_replay.all_identical is True`     |
| `test-pytest-32-pass`               | PASS    | PASS      | Steps 8, S-8 `32 passed`                                      |
| `test-forbidden-scan-zero-hits`     | PASS    | PASS      | Steps 9, S-9 empty stdout, grep exit 1                        |
| `test-runpod-env-reported`          | n/a     | PASS      | Step S-10 full env report with pod interpreter inventory      |

Additional finding, reported for completeness:
Cross-environment byte-equality (macOS clone ↔ RunPod clone) on the smoke
output is PASS (identical `020f97b8…` sha) and on the replay record is
PASS modulo `generated_utc`.

## Environment gaps and unblock items

1. **Committed `artifacts/smoke/smoke_report.json` byte-parity drift.** The
   committed reference was produced before two serializer changes landed:
   (a) `json.dumps(..., sort_keys=True)` and (b) the additive `mode` /
   `repeats` fields per `STABILITY_BATTERY_v1.md`. Both blind clones agree
   byte-for-byte on the new output; the committed reference is behind by
   these additive, non-numeric changes.
   - Unblock produces: a regenerated `artifacts/smoke/smoke_report.json`
     whose sha matches `020f97b8…c184e`.
   - Unblock condition: an owner decision to re-freeze the committed
     byte-reference under the current serializer. The numeric-fallback
     test already proves the pipeline is deterministic, so this is a
     housekeeping unfreeze rather than a correctness fix. Not a Phase 03
     blocker.
   - Owner: the researcher holding custody of this repo. Not OWNER_DEFERRED.

2. **Plan frontmatter uses `replay` as the first-mode shorthand; canonical
   name is `deterministic_replay`.** The contract asserts `replay.all_identical`
   but the emitted artifact and `STABILITY_BATTERY_v1.md` both use
   `deterministic_replay`. Transcript reads the canonical name directly and
   marks the test PASS. Not a repo defect; a future plan revision may align
   the shorthand with the canonical name.
   - Unblock produces: an updated 03-01-PLAN.md using the canonical mode
     name in both `test-replay-record-shape` and `test-replay-all-identical`.
   - Unblock condition: trivial edit; non-blocking.

3. **Indus Phase 3c live feature manifest is NOT on the pod and NOT in any
   repo-custody location.** This is the external-data boundary the PRD
   declares out of scope for Phase 03. Neither the macOS primary nor the
   RunPod secondary attempted the live Phase 4 rerun. This matches the
   plan's `forbidden_proxies.fp-vendored-live-data`.
   - Unblock produces: an admitted Phase 3c feature-manifest copy at a
     named path the adapter can consume; a rerun record under
     `artifacts/replay/indus_phase4_live_*.json`.
   - Unblock condition: researcher-level access to the admitted Phase 3c
     source, with hashes to verify the admitted copy matches the upstream
     record. Out of scope for Phase 03; carried to Plan 03-02 as a named
     BLOCKED item.
   - Owner: `OWNER_DEFERRED` per `../../01_prd_and_authority/AUTHORITY_CHAIN.md`.

4. **Canonical LICENSE text is OWNER_DEFERRED.** The clone carries
   `LICENSE_PLACEHOLDER.md` only; no real LICENSE file. This was true at
   the start of Phase 03 and remains true after. Not a blind-clone
   failure; a promotion-readiness blocker carried into Plan 03-02.
   - Unblock produces: a `LICENSE` file at the repo root with canonical
     text.
   - Unblock condition: owner-supplied canonical license text.
   - Owner: `OWNER_DEFERRED` per `RELEASING.md §Owner Inputs`
     (`license identity: OWNER_DEFERRED`).

5. **Heavy-data release policy for image-bearing assets is not yet
   written.** Neither clone carried any image-bearing benchmark payload
   (this is the correct state per `DATA_POLICY.md`), but the release policy
   that would permit adding an image-bearing corpus has not been written.
   - Unblock produces: a named appendix to `DATA_POLICY.md` (e.g.,
     `DATA_POLICY.md §Image-Bearing Release`) stating exactly which
     image-bearing classes are admitted into the repo and under what
     boundary.
   - Unblock condition: owner decision.
   - Owner: `OWNER_DEFERRED` per `RELEASING.md §Owner Inputs`.

Item 1 is local to this repo and internally-resolvable. Items 3, 4, 5 are
external/owner-gated and form the three mandatory named blockers that
Plan 03-02 will lift into `docs/PROMOTION_READINESS.md`. Item 2 is a
documentation alignment that a future plan revision can absorb.

## Disposition

**PASS** — primary macOS clone passed all applicable acceptance tests
(smoke byte-equality FAIL against committed reference is honestly named
with three drift sources, and the numeric-fallback PASS is the authorized
secondary path per the plan's approximation declaration). Secondary
RunPod clone also passed the full battery after the pod's
`/usr/bin/python3.11` was used directly (no privileged install needed),
flipping the plan's expected Python-floor environment gap from BLOCKED to
PASS-NOW per its own `disconfirming_observations` clause. Cross-
environment smoke and replay artifacts are byte-identical, strengthening
the reproducibility claim beyond what a single-environment run would
support. Four external-or-owner-gated items (committed smoke re-freeze,
plan shorthand vs canonical mode name, live Phase 3c access, canonical
LICENSE, heavy-data release policy) are carried to Plan 03-02 as named
unblock items under the blockers-are-tasks doctrine.

