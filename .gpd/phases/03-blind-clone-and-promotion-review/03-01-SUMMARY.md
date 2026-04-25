---
phase: 03-blind-clone-and-promotion-review
plan: 01
plan_contract_ref: .gpd/phases/03-blind-clone-and-promotion-review/03-01-PLAN.md
disposition: PASS
commits:
  - f81ba98  # primary macOS run, carry-back artifacts
  - 746799a  # secondary RunPod run, transcript close-out
artifacts:
  - artifacts/blind_clone/03-01_transcript.md
  - artifacts/blind_clone/03-01_smoke_report.clone.json
  - artifacts/blind_clone/03-01_replay_record.clone.json
  - artifacts/blind_clone/03-01_pytest.txt
  - artifacts/blind_clone/03-01_forbidden_pattern_scan.txt
  - artifacts/blind_clone/03-01_env.txt
primary_commit_sha_of_clone_source: 0c323026ba0195d3c615916a952fb2f5a8d40745
primary_python_version: Python 3.11.15
secondary_python_version: Python 3.11.13
secondary_env: RunPod pod <RUNPOD_POD_ID> (root@<RUNPOD_HOST>:<RUNPOD_PORT>)
contract_results:
  claims:
    - id: claim-clean-install
      verdict: verified
      evidence: "Primary macOS clone: pip install -e . exit 0 on python3.11.15 venv; numpy 2.4.4, scikit-learn 1.8.0, scipy 1.17.1 resolved from pyproject. Both console_scripts resolved with --help exit 0. Secondary RunPod clone: same install succeeded on python3.11.13 venv using /usr/bin/python3.11 directly. See 03-01_transcript.md Steps 4, 5, S-4, S-5."
    - id: claim-smoke-parity
      verdict: verified_via_fallback
      evidence: "Byte-equality against committed reference FAILED (clone 020f97b8… vs committed 19d49d6b…). Three drift sources named: json key sort order; trailing newline; additive mode/repeats fields introduced after the reference was frozen. Numeric-fallback parser PASSED — every scalar within 1e-6, every SHA-256 and every label assignment exact match. Both blind clones (macOS and RunPod) produce IDENTICAL smoke output (same 020f97b8… sha), strengthening reproducibility beyond the numeric fallback alone. See 03-01_transcript.md Steps 6, S-6."
    - id: claim-replay-record-wellformed
      verdict: verified
      evidence: "record_type=replay_record_v1, schema_version=1, five canonical modes present under stability.modes (deterministic_replay, leave_fraction_out, noise_injection, k_sensitivity, seed_variance per STABILITY_BATTERY_v1.md). reference_freeze.sha256=ebfffd56…60c populated. deterministic_replay.all_identical=True on both macOS and RunPod. Replay records byte-identical across envs modulo generated_utc. See 03-01_transcript.md Steps 7, S-7."
    - id: claim-pytest-clean
      verdict: verified
      evidence: "Primary: 32 passed in 3.53s. Secondary: 32 passed in 9.50s. 0 failed, 0 xfailed, 0 skipped on both envs. Logs: 03-01_pytest.txt (primary); inline in transcript (secondary)."
    - id: claim-forbidden-pattern-free-under-src
      verdict: verified
      evidence: "External grep over 10 python files under src/gnosis_morph_bench/ returned empty stdout (grep exit 1 = no matches = PASS) on both macOS and RunPod. Independent of in-repo tests/test_forbidden_patterns.py. Log: 03-01_forbidden_pattern_scan.txt."
    - id: claim-runpod-gap-reported
      verdict: verified
      evidence: "Transcript Step S-10 records starting python3 version (3.8.10), full interpreter inventory (3.8, 3.9, 3.10, 3.11, 3.12, 3.13 all at /usr/bin/), exact command used to satisfy floor (/usr/bin/python3.11 -m venv — no uv, no deadsnakes, no privilege escalation), and the full green outcome. Matches the plan's disconfirming_observations clause that, if the pod was lifted above 3.10, the RunPod readiness item moves from BLOCKED to PASS-NOW."
  deliverables:
    - id: deliv-transcript
      status: produced
      path: artifacts/blind_clone/03-01_transcript.md
    - id: deliv-smoke-clone
      status: produced
      path: artifacts/blind_clone/03-01_smoke_report.clone.json
    - id: deliv-replay-clone
      status: produced
      path: artifacts/blind_clone/03-01_replay_record.clone.json
    - id: deliv-pytest-log
      status: produced
      path: artifacts/blind_clone/03-01_pytest.txt
    - id: deliv-forbidden-scan
      status: produced
      path: artifacts/blind_clone/03-01_forbidden_pattern_scan.txt
    - id: deliv-env-capture
      status: produced
      path: artifacts/blind_clone/03-01_env.txt
  acceptance_tests:
    - id: test-install-success
      outcome: PASS
      evidence: "Step 4 install tail exit 0; Step S-4 install tail exit 0."
    - id: test-entrypoints-resolve
      outcome: PASS
      evidence: "Both --help exit 0 on both envs (Steps 5, S-5)."
    - id: test-smoke-byte-equal
      outcome: FAIL
      evidence: "Clone sha 020f97b8… vs committed 19d49d6b…. Three drift sources named explicitly — this is the honest-report shape the plan's fp-numeric-equality-as-default forbids silently downgrading from."
    - id: test-smoke-numeric-fallback
      outcome: PASS
      evidence: "Field-by-field parser: all scalars within 1e-6, all SHA-256 and labels exact (Steps 6, S-6)."
    - id: test-replay-record-shape
      outcome: PASS
      evidence: "Five canonical modes present on both envs (Steps 7, S-7)."
    - id: test-replay-all-identical
      outcome: PASS
      evidence: "deterministic_replay.all_identical=True on both envs."
    - id: test-pytest-32-pass
      outcome: PASS
      evidence: "32 passed on both envs."
    - id: test-forbidden-scan-zero-hits
      outcome: PASS
      evidence: "Empty stdout, grep exit 1 on both envs."
    - id: test-runpod-env-reported
      outcome: PASS
      evidence: "Step S-10: full interpreter inventory reported; command used to satisfy floor named; pod upgraded state acknowledged; outcome (PASS-NOW, not BLOCKED) recorded."
  forbidden_proxies:
    - id: fp-inside-working-dir
      status: rejected
      evidence: "All work under /tmp/blind-clone-<epoch>/ and /workspace/blind-clone-<epoch>/; no reuse of 05_repo_scaffold/.venv."
    - id: fp-vendored-live-data
      status: rejected
      evidence: "Only fixtures/tiny_benchmark_manifest.json (repo-custody synthetic) fed to the replay CLI. No Phase 3c live feature manifest was introduced into the clone."
    - id: fp-numeric-equality-as-default
      status: rejected
      evidence: "Byte-equality check ran FIRST. FAIL recorded. Three drift sources named explicitly before numeric-fallback was invoked. Both test IDs appear distinctly in the acceptance table."
    - id: fp-pytest-green-without-forbidden-scan
      status: rejected
      evidence: "External grep from shell (not from pytest) ran independently on both envs. The in-repo test was not treated as the sole proof."
    - id: fp-runpod-gap-softened
      status: rejected
      evidence: "Transcript records the actual pod interpreter inventory (3.8 through 3.13 present), not a generic 'skipped due to env mismatch'. Movement from expected-BLOCKED to actual-PASS-NOW is named."
    - id: fp-repo-root-polluted
      status: rejected
      evidence: "Committed artifacts/smoke/smoke_report.json untouched (git status clean before Phase 03 writes; only additions under artifacts/blind_clone/). Clone outputs kept in /tmp and /workspace."
  must_surface_references:
    - id: ref-pyproject
      status: satisfied
      note: "pyproject.toml cited; requires-python=>=3.10 and the two console_scripts exercised directly."
    - id: ref-committed-smoke
      status: satisfied
      note: "artifacts/smoke/smoke_report.json compared sha-by-sha; diff exhaustively enumerated; additive/format-only changes identified."
    - id: ref-smoke-tests-doc
      status: satisfied
      note: "SMOKE_TESTS.md documented smoke command executed verbatim in the clone."
    - id: ref-stability-battery-doc
      status: satisfied
      note: "docs/family/STABILITY_BATTERY_v1.md canonical mode names (deterministic_replay, leave_fraction_out, noise_injection, k_sensitivity, seed_variance) used as the shape contract."
    - id: ref-path-rewrite-ledger
      status: satisfied
      note: "All six forbidden patterns from PATH_REWRITE_LEDGER.md enumerated in the external grep regex."
    - id: ref-02-02-summary
      status: satisfied
      note: "02-02-SUMMARY.md's 32/32 pytest and 5-mode battery baseline reproduced."
---

# Plan 03-01 Summary

**Disposition:** PASS (primary macOS + secondary RunPod both green; smoke
byte-equality against the committed reference FAILED with three named
additive/format drift sources, numeric-fallback PASSED by plan-sanctioned
secondary path, cross-env byte-equality between clones PASSED).

**Clone provenance:** commit SHA `0c323026ba0195d3c615916a952fb2f5a8d40745`.
Primary environment: macOS Darwin 24.6.0 x86_64, `/usr/local/bin/python3.11`
(`Python 3.11.15`), fresh venv at `<TMP_BLIND_CLONE_ROOT>/clone/.venv`.
Secondary environment: RunPod pod `<RUNPOD_POD_ID>`, Linux Ubuntu
`6.8.0-100-generic`, `/usr/bin/python3.11` (`Python 3.11.13`), fresh venv
at `<RUNPOD_BLIND_CLONE_ROOT>/clone/.venv`.

## Acceptance test results (with evidence paths)

| Test                                  | Primary | Secondary | Evidence                                                                |
|---------------------------------------|---------|-----------|-------------------------------------------------------------------------|
| `test-install-success`                | PASS    | PASS      | `03-01_transcript.md` Steps 4, S-4; `03-01_env.txt`                     |
| `test-entrypoints-resolve`            | PASS    | PASS      | `03-01_transcript.md` Steps 5, S-5 `--help` exit 0                      |
| `test-smoke-byte-equal` (vs committed)| FAIL    | FAIL      | Clone `020f97b8…` ≠ committed `19d49d6b…`; drift named                  |
| `test-smoke-numeric-fallback`         | PASS    | PASS      | Field-by-field parser: all scalars within 1e-6, SHAs + labels exact      |
| `test-replay-record-shape`            | PASS    | PASS      | Five canonical modes under `stability.modes`; `record_type=replay_record_v1` |
| `test-replay-all-identical`           | PASS    | PASS      | `deterministic_replay.all_identical is True` on both envs                |
| `test-pytest-32-pass`                 | PASS    | PASS      | `03-01_pytest.txt` → `32 passed`                                         |
| `test-forbidden-scan-zero-hits`       | PASS    | PASS      | `03-01_forbidden_pattern_scan.txt` empty (grep exit 1)                   |
| `test-runpod-env-reported`            | —       | PASS      | Step S-10 full interpreter inventory + command + outcome                 |

Cross-environment byte-equality between the two clones (macOS vs RunPod):
smoke `sha256` identical; replay record byte-identical modulo
`generated_utc` wall-clock.

## Handoff to Plan 03-02

Five named unblock items lifted verbatim from
`03-01_transcript.md §Environment gaps and unblock items` for Plan 03-02
to carry into `docs/PROMOTION_READINESS.md`:

1. **Committed `artifacts/smoke/smoke_report.json` byte-reference re-freeze.**
   Local, researcher-owned; not OWNER_DEFERRED. Unblock produces a
   regenerated reference whose sha matches `020f97b8…c184e`. Unblock
   condition: owner decision to re-freeze under the current serializer.
   *Not a promotion blocker* — the numeric-fallback PASS already shows the
   pipeline is deterministic across envs.

2. **Plan frontmatter `replay` shorthand vs canonical `deterministic_replay`.**
   Doc-level alignment; not a repo defect. Unblock produces an updated
   03-01-PLAN.md using the canonical mode name.

3. **Indus Phase 3c live feature manifest (OWNER_DEFERRED).** Out of scope
   for Phase 03; mandatory named blocker for PROMOTION_READINESS.
   Unblock produces `artifacts/replay/indus_phase4_live_*.json` (repo-
   custody rerun of live Phase 4 values). Unblock condition: admitted
   access with hashes. Owner pointer:
   `../../01_prd_and_authority/AUTHORITY_CHAIN.md`.

4. **Canonical LICENSE text (OWNER_DEFERRED).** Mandatory named blocker
   for PROMOTION_READINESS. Unblock produces a real `LICENSE` file at
   repo root. Unblock condition: owner-supplied canonical text. Owner
   pointer: `RELEASING.md §Owner Inputs` (`license identity: OWNER_DEFERRED`).

5. **Heavy-data release policy for image-bearing assets (OWNER_DEFERRED).**
   Mandatory named blocker for PROMOTION_READINESS. Unblock produces a
   named appendix to `DATA_POLICY.md`. Unblock condition: owner decision.
   Owner pointer: `RELEASING.md §Owner Inputs`.

Items 3, 4, 5 are the three mandatory named external blockers that Plan
03-02 carries into `docs/PROMOTION_READINESS.md` per contract test
`test-three-named-blockers-present`.

## Next step

Plan 03-02: author `docs/PROMOTION_READINESS.md` anchored to this
transcript's Disposition line, enumerate PASS-NOW / BLOCKED / DEFERRED
items honestly, preserve `NOTICE.md` unchanged, update
`TODO.md` with cross-references.
