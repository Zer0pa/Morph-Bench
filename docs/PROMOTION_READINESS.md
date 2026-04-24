# Promotion Readiness

This document is the documentation subset of PRD-P4 ("Promotion Readiness")
for `05_repo_scaffold/`. It is anchored to the blind-clone evidence in
[`artifacts/blind_clone/03-01_transcript.md`](../artifacts/blind_clone/03-01_transcript.md)
(Disposition: PASS on HEAD `0c323026ba0195d3c615916a952fb2f5a8d40745`,
primary macOS + secondary RunPod both green). The repo remains private
until canonical license text lands and the image-bearing-asset release
boundary is written. This document enumerates what passes repo-custody
today, what is blocked on external or owner input, and what is scope-
deferred. It does not fabricate a license, does not promote any live
Phase 4 numeric value as repo-custody proof, and does not soften any
blocker.

## Purpose And Scope

- **What this doc is.** The single promotion-readiness statement for the
  staged repo: the truthful enumeration of gates that pass today, gates
  waiting on external input, and items deferred by scope.
- **What this doc is not.** It is not a release note, not a changelog,
  not a license, and not a claim of public readiness.
- **Where the actual release protocol lives.** See
  [`RELEASING.md`](../RELEASING.md) for release types, required checks,
  the live sync sequence, and the owner inputs still pending.
- **Where the audit boundary lives.** See
  [`PUBLIC_AUDIT_LIMITS.md`](../PUBLIC_AUDIT_LIMITS.md) for what a public
  audit of this clone can and cannot establish.
- **Governing PRD sections.** PRD-P3 (Replay And Blind Clone) covers the
  executable subset proved here; PRD-P4 (Promotion Readiness) covers the
  documentation subset this file completes. See
  [`PRD_GNOSIS_MORPH_BENCH_2026-04-23.md`](../PRD_GNOSIS_MORPH_BENCH_2026-04-23.md)
  §4 and §5.

## Pass Now

Every bullet cites at least one repo-local artifact path. No bullet cites
a source-authority path as repo-custody proof.

- **Standalone install from a blind clone.** `pip install -e .` succeeds
  on Python 3.11 into a fresh venv outside this working directory.
  Evidence:
  [`artifacts/blind_clone/03-01_transcript.md`](../artifacts/blind_clone/03-01_transcript.md)
  Steps 4 and S-4 (primary macOS + secondary RunPod);
  [`artifacts/blind_clone/03-01_env.txt`](../artifacts/blind_clone/03-01_env.txt)
  capturing both environments;
  [`pyproject.toml`](../pyproject.toml) `requires-python=">=3.10"` and
  `[project.scripts]`.

- **Synthetic smoke benchmark reproduces under repo custody (numeric).**
  The clone output matches the committed reference on every numeric field
  within 1e-6 and on every SHA-256 and every label assignment exactly.
  The byte-equality check failed with three explicitly named additive /
  format drift sources (JSON key sort order; trailing newline; additive
  `mode` and `repeats` fields added to stability-mode payloads after the
  reference was frozen). Both blind clones (macOS and RunPod) produce
  identical `sha256 020f97b8…c184e` output, which is the stronger cross-
  environment reproducibility evidence than either env alone.
  Evidence:
  [`artifacts/blind_clone/03-01_smoke_report.clone.json`](../artifacts/blind_clone/03-01_smoke_report.clone.json)
  vs
  [`artifacts/smoke/smoke_report.json`](../artifacts/smoke/smoke_report.json);
  [`artifacts/blind_clone/03-01_transcript.md`](../artifacts/blind_clone/03-01_transcript.md)
  Steps 6 and S-6; `test-smoke-byte-equal` FAIL + `test-smoke-numeric-fallback` PASS.

- **Neutral `ReplayRecord` shape matches the stability battery contract.**
  `record_type="replay_record_v1"`, `schema_version=1`, all five canonical
  stability modes (`deterministic_replay`, `leave_fraction_out`,
  `noise_injection`, `k_sensitivity`, `seed_variance`) present under
  `stability.modes`, populated `reference_freeze.sha256`, and
  `deterministic_replay.all_identical is True`. Cross-env replay records
  are byte-identical modulo `generated_utc`.
  Evidence:
  [`artifacts/blind_clone/03-01_replay_record.clone.json`](../artifacts/blind_clone/03-01_replay_record.clone.json);
  [`docs/family/STABILITY_BATTERY_v1.md`](family/STABILITY_BATTERY_v1.md) §Modes.

- **32-case pytest suite passes from a blind clone.**
  `pytest -q tests/` on both macOS and RunPod clones reports
  `32 passed`, zero failures, zero xfails, zero skips.
  Evidence:
  [`artifacts/blind_clone/03-01_pytest.txt`](../artifacts/blind_clone/03-01_pytest.txt);
  [`.gpd/phases/02-neutral-module-extraction/02-02-SUMMARY.md`](../.gpd/phases/02-neutral-module-extraction/02-02-SUMMARY.md).

- **Zero forbidden monorepo patterns under `src/`.** External `grep` for
  the six forbidden patterns
  (`phase3_common`, `stroke_*`, `sys.path.insert`, `parents[`,
  `workspace/artifacts`, `from workspace./from scripts.`) returns empty
  on both environments — independently of the in-repo
  `tests/test_forbidden_patterns.py` lint.
  Evidence:
  [`artifacts/blind_clone/03-01_forbidden_pattern_scan.txt`](../artifacts/blind_clone/03-01_forbidden_pattern_scan.txt) (empty is PASS);
  [`../02_source_inventory/PATH_REWRITE_LEDGER.md`](../../02_source_inventory/PATH_REWRITE_LEDGER.md).

- **Two console_scripts resolve after blind install.**
  `gnosis-morph-bench-smoke --help` and
  `gnosis-morph-bench-adapter-indus-phase4 --help` both exit 0 in both
  environments.
  Evidence:
  [`pyproject.toml`](../pyproject.toml) `[project.scripts]`;
  [`artifacts/blind_clone/03-01_transcript.md`](../artifacts/blind_clone/03-01_transcript.md)
  Steps 5 and S-5.

- **Adapter and five-mode stability battery implemented under repo
  custody against synthetic fixtures.** The adapter that translates an
  admitted Indus Phase 4 source family into a neutral
  `BenchmarkManifest` is implemented, as is the full five-mode battery
  that emits the `ReplayRecord`. Both are exercised end-to-end by the
  repo-custody test suite.
  Evidence:
  [`src/gnosis_morph_bench/adapters/indus_phase4.py`](../src/gnosis_morph_bench/adapters/indus_phase4.py);
  [`src/gnosis_morph_bench/stability.py`](../src/gnosis_morph_bench/stability.py);
  [`src/gnosis_morph_bench/replay.py`](../src/gnosis_morph_bench/replay.py);
  [`docs/family/ADAPTER_CONTRACT_v1.md`](family/ADAPTER_CONTRACT_v1.md).

- **Blind-clone transcript itself as audit evidence.** A fresh clone into
  a clean work directory outside this tree reaches the full test battery
  without any file outside the clone being required.
  Evidence:
  [`artifacts/blind_clone/03-01_transcript.md`](../artifacts/blind_clone/03-01_transcript.md)
  Disposition line (**PASS**).

- **RunPod pod environment-readiness flipped from expected-BLOCKED to
  actual-PASS-NOW.** The plan anticipated the pod's default
  `python3 --version = 3.8.10` as a Python-floor gap. In reality, the pod
  image now ships `/usr/bin/python3.11` (and 3.9, 3.10, 3.12, 3.13)
  alongside 3.8; the secondary run therefore proceeded with
  `/usr/bin/python3.11` directly and reproduced the full green battery
  without uv, deadsnakes, or any privileged install step.
  Evidence:
  [`artifacts/blind_clone/03-01_transcript.md`](../artifacts/blind_clone/03-01_transcript.md)
  §Secondary (RunPod) run and Step S-10.

## Blocked On External Dependencies

Every entry below carries four markers: `Blocker:`, `Owner:`,
`Unblock produces:`, and `Unblock condition:` — so a reader can act on it
without reinterpretation. No soft "pending" or "we are reviewing"
language. Three mandatory named blockers are present; a fourth
housekeeping item is included because it surfaced from the 03-01
transcript and is honest to name.

### Blocked-1: Indus Phase 3c feature manifest access

- **Blocker:** No admitted copy of the Indus Phase 3c feature manifest is
  present on this Mac, in this repo, or on the RunPod pod. The live
  Phase 4 rerun from repo custody (PRD-P3 "admitted live replay"
  subset) cannot proceed without it. This is the boundary the PRD
  carves out of Phase 03 on purpose.
- **Owner:** `OWNER_DEFERRED`, with authority pointer
  [`../../01_prd_and_authority/AUTHORITY_CHAIN.md`](../../01_prd_and_authority/AUTHORITY_CHAIN.md).
- **Unblock produces:** a rerun record at a repo-custody path like
  `artifacts/replay/indus_phase4_live_<date>.json` whose numeric fields
  (NMI, Sigma, null_mean, null_std, silhouette, mean_jaccard, replay
  hashes) reproduce the live Phase 4 quadruple, with an adapter-run
  record at `artifacts/replay/indus_phase4_live_<date>_run.json`
  documenting the admitted-input SHA-256.
- **Unblock condition:** admitted access to a Phase 3c feature manifest
  file path on-host to this repo, with a SHA-256 stated in the admission
  so the adapter can verify it matches the upstream record. Mere PDF or
  prose reference is insufficient — an actual consumable JSON path is
  required.

### Blocked-2: Canonical LICENSE text

- **Blocker:** No `LICENSE` file exists at repo root. The current state
  is a placeholder marker at
  [`LICENSE_PLACEHOLDER.md`](../LICENSE_PLACEHOLDER.md), which explicitly
  says it is not the legal authority. The repo cannot be promoted
  publicly until canonical license text lands.
- **Owner:** `OWNER_DEFERRED`, with authority pointer
  [`RELEASING.md §Owner Inputs`](../RELEASING.md) line
  `license identity: OWNER_DEFERRED`.
- **Unblock produces:** a real `LICENSE` file at the repo root
  containing canonical text, plus coherent updates to
  [`README.md`](../README.md),
  [`GOVERNANCE.md`](../GOVERNANCE.md),
  [`RELEASING.md`](../RELEASING.md), and
  [`docs/LEGAL_BOUNDARIES.md`](LEGAL_BOUNDARIES.md) that all cite the
  same license identity.
- **Unblock condition:** owner supplies canonical license text (MIT,
  Apache-2.0, a proprietary license, or whatever the owner chooses) AND
  authorizes removal of `LICENSE_PLACEHOLDER.md` or its retention as
  migration history.

### Blocked-3: Heavy-data release policy for image-bearing assets

- **Blocker:** The repo's
  [`DATA_POLICY.md`](../DATA_POLICY.md) says image-bearing benchmark
  payloads must not be carried yet, and that public promotion is
  blocked "until canonical license text is supplied and the release
  boundary for image-bearing assets is written explicitly." That
  release boundary has not been written. Therefore even with a LICENSE,
  any image-bearing corpus would still be blocked until this policy
  exists.
- **Owner:** `OWNER_DEFERRED`, with authority pointer
  [`RELEASING.md §Owner Inputs`](../RELEASING.md) (release notes
  location / versioning scheme surface).
- **Unblock produces:** a named appendix to
  [`DATA_POLICY.md`](../DATA_POLICY.md) (proposed
  `DATA_POLICY.md §Image-Bearing Release`) that states which image-
  bearing classes may enter the repo, under what redaction or license
  terms, and how the payload is bounded (max size, checksum expectation,
  storage location, review workflow).
- **Unblock condition:** owner decision naming the admitted image-
  bearing classes and the per-class release terms. Without this policy,
  no Indus or cuneiform image payload can be vendored here even if the
  LICENSE question closes.

### Blocked-4: Committed `artifacts/smoke/smoke_report.json` byte-reference re-freeze

- **Blocker:** The committed byte-reference at
  [`artifacts/smoke/smoke_report.json`](../artifacts/smoke/smoke_report.json)
  was produced before two serializer changes landed: (a) key-sorted JSON
  output, and (b) the additive `mode` / `repeats` fields in each
  stability-mode payload per
  [`docs/family/STABILITY_BATTERY_v1.md`](family/STABILITY_BATTERY_v1.md).
  Blind clones now emit a different SHA (`020f97b8…c184e`) that carries
  no numeric divergence but fails the byte-equality check of the
  current plan contract.
- **Owner:** repo researcher (not OWNER_DEFERRED). This is an internal
  housekeeping item.
- **Unblock produces:** a re-frozen `artifacts/smoke/smoke_report.json`
  whose sha256 matches `020f97b83b2948c2cd529b975010e6e5132799d89e395539d6f6f928c97c184e`, plus an
  explicit note in `docs/family/STABILITY_BATTERY_v1.md` that the
  current reference is post-`mode`-field and post-`sort_keys`.
- **Unblock condition:** a single researcher decision to re-run the
  smoke command and commit the new byte-reference. Not a promotion
  gate on its own — the numeric-fallback PASS in the 03-01 transcript
  already proves the pipeline is deterministic across envs. Recorded
  here for transparency.

## Deferred By Scope

These items are NOT blocked on external inputs. They are scope decisions
carried from upstream planning that a later phase or workstream will pick
up.

- **Cuneiform adapter work.** The cuneiform source family is listed as an
  admitted-for-extraction family in
  [`SOURCE_BOUNDARY.md §Live Source Families Admitted For Extraction`](../SOURCE_BOUNDARY.md),
  but the live extraction is scheduled for a later phase, not Phase 03.
  No blocker exists today; this is deferred until the Indus Phase 4 live
  rerun lands (Blocked-1 above) so the adapter-contract v1 can be
  validated against a second source family. Listing this as "blocked"
  would be wrong — cuneiform is a scope decision, not a data-access gate.
  Phase pointer:
  [`PRD_GNOSIS_MORPH_BENCH_2026-04-23.md`](../PRD_GNOSIS_MORPH_BENCH_2026-04-23.md)
  §Phase P2/P3 boundaries;
  [`docs/family/ADAPTER_CONTRACT_v1.md`](family/ADAPTER_CONTRACT_v1.md).

- **Public promotion (publishing this repo publicly).** PRD-P4's exit
  gate is `private remote ready; public still optional`. Public
  promotion is intentionally kept optional and deferred — it cannot
  happen before Blocked-2 (LICENSE) and Blocked-3 (heavy-data policy)
  close regardless. Listing "public promotion" as blocked would double-
  count the LICENSE and data-policy blockers; it is a scope decision by
  the owner, gated on those.
  Phase pointer: PRD-P4 exit gate.

- **Additional stability-battery modes.** STABILITY_BATTERY_v1 is
  complete. v2 (for example, wider `k_offsets`, alternative clustering
  backends, non-Gaussian noise kernels) is out of scope for Phase 03 and
  would be planned in a new phase after the three promotion blockers
  close.
  Phase pointer:
  [`docs/family/STABILITY_BATTERY_v1.md §Non-Claims`](family/STABILITY_BATTERY_v1.md).

## License Posture

The repo remains **private** until canonical license text lands.

No fabricated license is admitted by this document.
[`LICENSE_PLACEHOLDER.md`](../LICENSE_PLACEHOLDER.md) is the current
terminal marker and is preserved unchanged by Plan 03-02. Per
[`RELEASING.md §Owner Inputs`](../RELEASING.md), `license identity:
OWNER_DEFERRED` is the real state. This posture means:

- No permissive, source-available, or commercial terms are claimed as
  final.
- No `LICENSE` file at repo root.
- Public promotion cannot proceed under any interpretation of this
  document until Blocked-2 closes.
- A future `LICENSE` file landing MAY or MAY NOT remove
  `LICENSE_PLACEHOLDER.md`; that decision is part of the unblock and
  belongs to the owner.

## Data Release Posture

The repo's data boundary is governed by
[`DATA_POLICY.md`](../DATA_POLICY.md) and
[`SOURCE_BOUNDARY.md`](../SOURCE_BOUNDARY.md).

- **May carry today:** docs and migration metadata; neutral package code
  under `src/gnosis_morph_bench/`; tiny synthetic fixtures under
  `fixtures/`; adapter-run records under `artifacts/replay/` and
  `artifacts/smoke/` that reference only synthetic fixtures or whose
  input paths are admitted.
- **May cite today but NOT yet vendor:** live Phase 4 authority
  artifacts under `workspace/artifacts/indus/phase4/*`; the cuneiform
  benchmark manifest family.
- **Must NOT yet carry:** raw corpora; image-bearing benchmark payloads;
  review-pack artifacts.
- **Minimum standalone install gate:** the synthetic smoke fixture at
  [`fixtures/tiny_benchmark_manifest.json`](../fixtures/tiny_benchmark_manifest.json)
  is sufficient for a blind-clone install to reach a known-good
  numerical output. See
  [`SMOKE_TESTS.md`](../SMOKE_TESTS.md).
- **Heavy-data release blocked on policy (Blocked-3).** Even with a
  LICENSE, no image-bearing corpus may enter the repo until the release
  boundary is written.

## Trust Boundary

Per [`PUBLIC_AUDIT_LIMITS.md`](../PUBLIC_AUDIT_LIMITS.md), a clone of
this repo can establish only what its visible docs, code, and local
artifacts support. The table below makes that explicit.

| Consumers Can Trust (repo-custody, clone-reproducible)                                                      | Source Authority Only (NOT provable from this clone)                                                             |
|-------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| Standalone install from a blind clone (`pip install -e .`) on Python 3.11                                   | Live Phase 4 NMI value `0.5793`                                                                                  |
| Synthetic smoke artifact [`artifacts/smoke/smoke_report.json`](../artifacts/smoke/smoke_report.json) numeric content | Live Phase 4 Sigma value `5.65`                                                                                  |
| The 32-case pytest suite under `tests/`                                                                     | Live Phase 4 mean Jaccard value `0.4351`                                                                         |
| The two console_scripts `gnosis-morph-bench-smoke` and `gnosis-morph-bench-adapter-indus-phase4`            | Live Phase 4 replay quadruple (`3/3` identical hashes on a live feature manifest)                                |
| The five-mode `ReplayRecord` shape per [`docs/family/STABILITY_BATTERY_v1.md`](family/STABILITY_BATTERY_v1.md) | Contents of `workspace/artifacts/indus/phase4/*`                                                                 |
| The forbidden-monorepo-pattern lint over `src/gnosis_morph_bench/`                                          | The cuneiform benchmark manifest family                                                                          |
| Blind-clone reproducibility across macOS and Linux on Python 3.11 (same smoke sha, same replay shape)       | Any scientific verdict about Indus or cuneiform corpora per [`PUBLIC_AUDIT_LIMITS.md`](../PUBLIC_AUDIT_LIMITS.md) |
| The adapter contract v1 per [`docs/family/ADAPTER_CONTRACT_v1.md`](family/ADAPTER_CONTRACT_v1.md)           | Live extraction of production data through the adapter (requires Blocked-1)                                      |

Reading rule: the left column is established by running `pip install -e
.` and the 32-case test suite from a blind clone. The right column
requires access to files outside the clone and is carried as Blocked-1
above.

## Unblock Conditions Summary

One-line digest of every Blocked item above so a reader scanning only
this section sees the full unblock checklist:

- **Blocked-1 (Phase 3c manifest):** Owner-admitted access to a
  consumable Phase 3c feature manifest JSON with a stated SHA-256. →
  produces `artifacts/replay/indus_phase4_live_<date>.json`.
- **Blocked-2 (LICENSE):** Owner-supplied canonical license text. →
  produces `LICENSE` at repo root plus coherent updates across README,
  GOVERNANCE, RELEASING, and LEGAL_BOUNDARIES.
- **Blocked-3 (heavy-data release policy):** Owner decision naming
  admitted image-bearing classes and per-class terms. → produces
  `DATA_POLICY.md §Image-Bearing Release` appendix.
- **Blocked-4 (committed smoke byte-reference):** Researcher decision to
  re-freeze under the current serializer. → produces refreshed
  `artifacts/smoke/smoke_report.json` with sha256 `020f97b8…c184e`.

Blocked-1, -2, -3 are external/owner-gated. Blocked-4 is local and does
not gate promotion — it is listed here only so the blind-clone drift
source is named on a single canonical page.

## Owner Decisions Needed

Three explicit decisions are needed from the owner before public
promotion becomes feasible. Each points at
[`RELEASING.md §Owner Inputs`](../RELEASING.md) as the authoritative
surface for the decision.

1. **License identity** (resolves Blocked-2).
   [`RELEASING.md §Owner Inputs`](../RELEASING.md) line
   `license identity: OWNER_DEFERRED`.

2. **Heavy-data release policy** (resolves Blocked-3). The authoritative
   surface for the decision is
   [`RELEASING.md §Owner Inputs`](../RELEASING.md) together with
   [`DATA_POLICY.md`](../DATA_POLICY.md).

3. **Public-promotion go/no-go timing** (resolves the Deferred-by-scope
   "public promotion" item).
   [`RELEASING.md §Owner Inputs`](../RELEASING.md) plus the outcome of
   decisions 1 and 2.

These three decisions collapse the PRD-P4 gate from "private remote
ready; public still optional" to "public promotion authorized under
named terms."

## Change Log

- 2026-04-24 — Initial authoring against blind-clone transcript HEAD
  `0c323026ba0195d3c615916a952fb2f5a8d40745`. Plan 03-01 disposition was
  **PASS** (primary macOS + secondary RunPod both green on the full
  battery; smoke byte-equality FAIL vs committed reference recorded
  honestly with three named drift sources; numeric-fallback PASS is the
  plan-authorized alternate path). Three mandatory external blockers
  (Phase 3c manifest, LICENSE, heavy-data release policy) enumerated;
  one local housekeeping blocker (smoke byte-reference re-freeze)
  enumerated for transparency. No LICENSE file fabricated.
  `LICENSE_PLACEHOLDER.md` preserved unchanged.
