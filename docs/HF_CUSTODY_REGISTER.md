# Hugging Face Custody Register

**Consuming GitHub repo:** `Zer0pa/Morph-Bench`
**Register reissued:** 2026-04-27 (full canonical-store migration)
**Verification token:** user `Architect-Prime`, scope `fineGrained`, org membership `Zer0pa` confirmed via `whoami-v2`.
**Spelling convention:** `artifact` (US English) for this lane. Do NOT create `artefact`-spelled duplicates here.

## Current Posture

**As of 2026-04-27, no Morph-Bench HF dataset repos live under the `Zer0pa` org namespace.** The two `Zer0pa/*` repos that previously existed have been **deleted**. All canonical artefact custody for this lane is now under the `Architect-Prime` HF user namespace. This is mission-critical operational safety: between GitHub (`Zer0pa/Morph-Bench`) and Hugging Face (`Architect-Prime/gnosis-morph-bench-{artifacts, authority-bundle}`), a local-machine catastrophic loss is fully recoverable.

The operator directive that drove this migration:

> "1) Move artefacts from Zer0pa org space on Hugging Face to Architect-Prime
> 2) Ensure that between Hugging Face and Github we have saved code and all artefacts/data/checkpoints of value
> 3) Working assumption = local mac is unstable and can die unrecoverable at any moment
> 4) There is no need to use Zer0pa org storage space on Hugging Face — I don't want you to"
> — operator, 2026-04-27

## Active Register

| HF repo ID | type | visibility | exists? | last_commit_sha | files | usedStorage | rights_class | consuming_github_repo | role |
|---|---|---|---|---|---|---|---|---|---|
| `Architect-Prime/gnosis-morph-bench-artifacts` | dataset | private (indefinitely) | **YES — VERIFIED 2026-04-27 (post-mirror pass)** | `985d39d71368...` | 5 (`.gitattributes`, `MANIFEST.json`, `README.md`, `snapshots/morph_evidence_snapshot_2026-04-27T00-43-33Z.tar.gz`, `snapshots/morph_workstream_package_2026-04-27T10-29-06Z.tar.gz`) | 145,984 bytes | internal / owner-deferred-license | `Zer0pa/Morph-Bench` | canonical custody for adapter run records, replay-output bundles, evidence-tree snapshots, and the local-only workstream-parent governance pack |
| `Architect-Prime/gnosis-morph-bench-authority-bundle` | dataset | private (indefinitely) | **YES — VERIFIED 2026-04-27** | `d1d1b3bb5f17...` | 3 (`.gitattributes`, `MANIFEST.json`, `README.md`) | 4,930 bytes | source-authority / restricted | `Zer0pa/Morph-Bench` | canonical custody for the read-only mirror of the live Phase 4 authority bundle (admission pending `Blocked-3`) |

## Retired Repos (Deleted 2026-04-27)

| Former HF repo ID | Disposition | Reason |
|---|---|---|
| `Zer0pa/gnosis-morph-bench-artifacts` | deleted | operator directive: do not use Zer0pa org for this lane |
| `Zer0pa/gnosis-morph-bench-authority-bundle` | deleted | operator directive: do not use Zer0pa org for this lane |
| `Architect-Prime/zeropa-org-gnosis-morph-bench-artifacts` | deleted | duplicate auto-redirect target from prior namespace migration; superseded by `Architect-Prime/gnosis-morph-bench-artifacts` |
| `Architect-Prime/zeropa-org-gnosis-morph-bench-authority-bundle` | deleted | duplicate auto-redirect target; superseded by `Architect-Prime/gnosis-morph-bench-authority-bundle` |

All four return HTTP 404 to direct path GETs as of 2026-04-27 verification.

## Operational-Safety Snapshot Inventory

Snapshots are non-credential tarballs of the consuming GitHub repo's evidence and state trees. They make local-machine catastrophic loss recoverable from `GitHub clone + AP snapshot fetch` alone. Each snapshot is a complete recovery base.

| Snapshot | kind | sha256 | bytes | consuming GitHub commit | admitted_utc | location |
|---|---|---|---|---|---|---|
| `morph_evidence_snapshot_2026-04-27T00-43-33Z.tar.gz` | evidence_tree (artifacts/, docs/, .gpd/, fixtures, root governance from inside the GitHub repo) | `9b104a0c85c520eb14fd41a47de3d1beefbf1b5d5afb6c4248ca3fa02bd4ae43` | 121,119 | `d533d198784c04c3170614c6da9908059da70f87` | 2026-04-27T00:43:33Z | `Architect-Prime/gnosis-morph-bench-artifacts/snapshots/` |
| `morph_workstream_package_2026-04-27T10-29-06Z.tar.gz` | workstream_package (00_brief, 01_prd_and_authority, 02_source_inventory, 03_data_policy, 04_evidence_manifest, 06_handover — sibling dirs to the GitHub repo, NOT tracked by git, were Mac-only before this snapshot) | `77e6672c0911dc2031c0924581630fb3ed3adc49bd8079eebeb04f4d90b88b9d` | 13,542 | `bac604f72cb7450a3f75e1d9ea31cc8398bc2b57` | 2026-04-27T10:29:06Z | `Architect-Prime/gnosis-morph-bench-artifacts/snapshots/` |

Snapshot integrity verification (HF round-trip):

```text
evidence_tree (2026-04-27T00-43-33Z):
  local sha256:           9b104a0c85c520eb14fd41a47de3d1beefbf1b5d5afb6c4248ca3fa02bd4ae43
  hf-roundtrip sha256:    9b104a0c85c520eb14fd41a47de3d1beefbf1b5d5afb6c4248ca3fa02bd4ae43
  integrity:              PASS (re-verified 2026-04-27 post-mirror pass; prior snapshot still intact)

workstream_package (2026-04-27T10-29-06Z):
  local sha256:           77e6672c0911dc2031c0924581630fb3ed3adc49bd8079eebeb04f4d90b88b9d
  hf-roundtrip sha256:    77e6672c0911dc2031c0924581630fb3ed3adc49bd8079eebeb04f4d90b88b9d
  integrity:              PASS
```

Snapshot trigger cadence and procedure documented in `docs/HF_STORAGE.md` §Operational-Safety Snapshot Protocol.

## Recovery Procedure (Mac-Loss Drill)

1. On a new machine: install git, Python 3.11, `huggingface-cli`.
2. `git clone https://github.com/Zer0pa/Morph-Bench.git` → restores all code, tests, docs, fixtures, `.gpd/` state, configs, blind-clone transcripts.
3. `huggingface-cli login` → paste a fresh token with org-Zer0pa visibility (token is operator-supplied).
4. `huggingface-cli download Architect-Prime/gnosis-morph-bench-artifacts --repo-type dataset --local-dir <recovery-dir>` → restores the latest evidence-tree snapshot tarball.
5. `tar -xzf <recovery-dir>/snapshots/morph_evidence_snapshot_<latest>.tar.gz` → restores any artefact-tree state that drifted past the GitHub commit at snapshot time.
6. `python3.11 -m venv .venv && .venv/bin/pip install -e '.[dev]'` → restores the runtime.
7. `.venv/bin/pytest -q` → expect `37 passed`.
8. Fetch any future admitted live artefacts: `huggingface-cli download Architect-Prime/gnosis-morph-bench-authority-bundle --repo-type dataset --local-dir <recovery-dir>`.

If GitHub is unavailable AND the local Mac is dead, the AP snapshot tarball alone reconstitutes the evidence and `.gpd/` state up to the snapshot commit; the runtime side requires waiting for GitHub to recover or rebuilding the package from the tarball's `pyproject.toml` + `src/` (note: snapshot does NOT include `src/` — that lives only on GitHub by design, since the BSD-3-Clause numpy/sklearn dependencies plus our own code are reproducible from a `pip install` against PyPI given the tarball's pyproject).

To make the AP-only recovery path stronger, future snapshots may add `src/` and `tests/` (excluding fixtures already present) to the tarball; this will increase snapshot size but eliminate the GitHub-availability dependency for full recovery.

## Architect-Prime Inventory (2026-04-27)

`GET /api/datasets?author=Architect-Prime&limit=200` returns 20 datasets visible to the production token. Of those, two belong to this lane (table above). The remaining 18 are ZPE-lane datasets owned by other workstreams (`zpe-video-artifacts`, `zpe-neuro-artifacts`, `zpe-robotics-artifacts`, etc.) — Morph-Bench does NOT own or consume any of them.

## Rights Class Definitions

- **internal / owner-deferred-license:** content is internal to Zer0pa, no redistribution rights granted to anyone outside Zer0pa, license to be decided as part of `Blocked-2` (canonical LICENSE) per `docs/PROMOTION_READINESS.md`.
- **source-authority / restricted:** content is a read-only mirror of live-source authority artifacts whose rights are governed by the originating data-rights chain. Redistribution blocked on `Blocked-3` (heavy-data release policy).

## SHA-256 Pinning Posture

Per `docs/HF_STORAGE.md` §SHA-256 pinning, every artefact admitted to either AP repo MUST have its SHA-256 recorded in the repo's `MANIFEST.json`. As of 2026-04-27:

- `Architect-Prime/gnosis-morph-bench-artifacts/MANIFEST.json`: 1 pinned artefact (the operational-safety snapshot above).
- `Architect-Prime/gnosis-morph-bench-authority-bundle/MANIFEST.json`: 0 pinned artefacts (admission pending `Blocked-3`).

When `Blocked-1` or `Blocked-3` clear and live artefacts are admitted, the admission protocol in `docs/HF_STORAGE.md` applies; this register's `last_commit_sha` and snapshot inventory must be updated in the same commit window.

## Verification Protocol

To reproduce the verification recorded here:

```bash
HF_TOKEN=$(cat <HF_TOKEN_PATH>)
curl -s -H "Authorization: Bearer $HF_TOKEN" https://huggingface.co/api/whoami-v2

# Active canonical repos
curl -s -w "HTTP:%{http_code}\n" -H "Authorization: Bearer $HF_TOKEN" \
  "https://huggingface.co/api/datasets/Architect-Prime/gnosis-morph-bench-artifacts"
curl -s -w "HTTP:%{http_code}\n" -H "Authorization: Bearer $HF_TOKEN" \
  "https://huggingface.co/api/datasets/Architect-Prime/gnosis-morph-bench-authority-bundle"

# Retired repos — must return 404
curl -s -w "HTTP:%{http_code}\n" -H "Authorization: Bearer $HF_TOKEN" \
  "https://huggingface.co/api/datasets/Zer0pa/gnosis-morph-bench-artifacts"
curl -s -w "HTTP:%{http_code}\n" -H "Authorization: Bearer $HF_TOKEN" \
  "https://huggingface.co/api/datasets/Zer0pa/gnosis-morph-bench-authority-bundle"
```

HTTP 200 + payload on the first two: pass. HTTP 404 on the last two: pass.

## Change Log

- **2026-04-24** — original register authored when both repos lived under `Zer0pa/*`.
- **2026-04-26** — HF Lane Execution Brief pass: cards rewritten to §5 template; routing decisions captured.
- **2026-04-26 (later)** — Storage Execution Brief pass: three-tier model documented; AP repos planned but not created.
- **2026-04-27** — Operator override pass. Per directive ("do not use Zer0pa org storage for this lane"): created `Architect-Prime/gnosis-morph-bench-artifacts` and `Architect-Prime/gnosis-morph-bench-authority-bundle` as canonical, populated the artefacts repo with the first operational-safety evidence-tree snapshot (SHA-pinned, HF-roundtrip integrity-verified), deleted the two `Zer0pa/*` repos, deleted two `Architect-Prime/zeropa-org-*` duplicate auto-redirect targets. Two-source recovery posture (GitHub `Zer0pa/Morph-Bench` + Architect-Prime/* HF) is now active.
