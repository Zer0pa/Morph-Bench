# Auditor Playbook

**Last reviewed:** 2026-04-28 against GitHub `main` baseline `098c7c65`.

## Goal

Verify what Morph-Bench proves from repo custody without confusing cited
source authority, private HF custody, or future roadmap work for a closed
scientific claim.

## Fast Path

1. Read the authority table and non-claims in [`README.md`](README.md).
2. Run the repo-local verification:

   ```bash
   python3.11 -m venv /tmp/gnosis-morph-audit
   source /tmp/gnosis-morph-audit/bin/activate
   python -m pip install -e '.[dev]'
   pytest -q
   python -m gnosis_morph_bench smoke fixtures/tiny_benchmark_manifest.json \
     --output /tmp/gnosis-morph-smoke.json
   ```

3. Inspect [`docs/PROMOTION_READINESS.md`](docs/PROMOTION_READINESS.md) for
   the pass-now list and the named open gates.
4. Inspect [`PUBLIC_AUDIT_LIMITS.md`](PUBLIC_AUDIT_LIMITS.md) before promoting
   any portfolio-level or scientific statement.
5. Inspect [`DATA_POLICY.md`](DATA_POLICY.md) before moving any data, image,
   transcript, or HF artifact into a public surface.

## Claim Replay Map

| Claim | Evidence path | Audit result | Caveat |
|---|---|---|---|
| Package installs from repo custody | `pyproject.toml`, `src/gnosis_morph_bench/`, `pytest -q` | `VERIFIED` | Python 3.11 is the closeout/runtime floor used by CI and blind-clone proof |
| Synthetic benchmark path works | `fixtures/tiny_benchmark_manifest.json`, `SMOKE_TESTS.md`, `artifacts/smoke/` | `VERIFIED` | Synthetic fixture only |
| Adapter contract is covered | `docs/family/ADAPTER_CONTRACT_v1.md`, `tests/test_adapter_contract_coverage.py` | `VERIFIED` | Covers the v1 Indus adapter contract, not future cuneiform contracts |
| Forbidden monorepo coupling is guarded | `tests/test_forbidden_patterns.py`, `artifacts/blind_clone/03-01_forbidden_pattern_scan.txt` | `VERIFIED` | Scope is package source; repo-wide hygiene is also checked in CI |
| Live Indus Phase 4 measured values exist | `docs/PROMOTION_READINESS.md`, `docs/STATUS_REPORT_2026-04-24.md` | `SOURCE_AUTHORITY_ONLY` | Not rerun from Morph-Bench custody until `Blocked-1` clears |
| Heavy-data/image-bearing release is safe | `DATA_POLICY.md` | `BLOCKED` | No image-bearing payload is admitted to the public repo today |

## Interpretation Rules

- `VERIFIED` means a repo-local artifact or command supports the statement.
- `SOURCE_AUTHORITY_ONLY` means the statement is cited from upstream authority
  and must not be promoted as Morph-Bench proof.
- `BLOCKED` means the required input or policy is not present.
- `DEFERRED` means scope was intentionally held for a later phase.

## Falsification Checks

Use these checks before giving a website-sync or repo-orchestrator greenlight:

```bash
pytest -q
git grep -ni "priniven" -- . ':!LICENSE' ':!.github/workflows/ci.yml' ':!AUDITOR_PLAYBOOK.md' && exit 1 || true
git grep -nE '/Users/|38\.80\.152\.147|7k3riasglemecu|AKIA[0-9A-Z]{16}|xox[abp]-|sk-[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----' -- . ':!.github/workflows/ci.yml' ':!AUDITOR_PLAYBOOK.md' && exit 1 || true
rg -n "canonical license text absent|license.*OWNER_DEFERRED|OWNER_DEFERRED.*license|32 passed|repo remains private until canonical license" README.md DATA_POLICY.md RELEASING.md ROADMAP.md PUBLIC_AUDIT_LIMITS.md docs/PROMOTION_READINESS.md docs/LEGAL_BOUNDARIES.md .gpd/STATE.md .gpd/state.json
```

The final `rg` command is a stale-language audit. It should return no
current-facing stale license/test-count blockers. Non-license owner-deferred
data gates and historical phase artifacts
under `.gpd/phases/` may preserve older wording and should be read as history.

## If You Find A Problem

- Use the evidence dispute issue template for claim/evidence disagreements.
- Use the bug report template for reproducible implementation defects.
- Downgrade overreach to `PARTIAL`, `UNKNOWN`, `UNVERIFIED`, `BLOCKED`, or
  `SOURCE_AUTHORITY_ONLY`. Do not narrate around the contradiction.
