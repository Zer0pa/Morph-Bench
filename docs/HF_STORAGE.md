# Hugging Face Storage Strategy

This doc specifies how the Gnosis Morph-Bench project divides storage
between GitHub and Hugging Face. It is authoritative for where any
given artifact class lives, how it is pinned, and how consumers
fetch it. It does NOT override [`DATA_POLICY.md`](../DATA_POLICY.md)
or [`PROMOTION_READINESS.md`](PROMOTION_READINESS.md); every storage
choice here must be consistent with both.

**As of 2026-04-27, the Zer0pa org is NOT used for Morph-Bench HF
storage.** Per operator directive, all canonical artefact custody for
this lane lives under the `Architect-Prime` HF user namespace. The
two `Zer0pa/*` dataset repos that previously existed have been
deleted. This is mission-critical operational safety: GitHub holds
code, `Architect-Prime/*` holds artefact and evidence custody, and
between the two a local-machine catastrophic loss is recoverable.

## Two-Source Recovery Posture

Working assumption: the local Mac may die unrecoverably at any time.
Everything of value MUST live on at least one remote that survives
that loss.

| Asset class | Authoritative remote | Recovery procedure |
|---|---|---|
| Code, tests, docs, configs, .gpd state, plans, summaries, transcripts, fixtures | GitHub `Zer0pa/Morph-Bench` (private) | `git clone https://github.com/Zer0pa/Morph-Bench.git` |
| Adapter run records, replay-output bundles, periodic evidence-tree snapshots, future heavy artefacts | HF `Architect-Prime/gnosis-morph-bench-artifacts` (private, canonical) | `huggingface-cli download` against pinned SHAs in `MANIFEST.json` |
| Source-authority mirror of live Phase 4 bundle (when admitted under `Blocked-3`) | HF `Architect-Prime/gnosis-morph-bench-authority-bundle` (private, canonical) | `huggingface-cli download` against pinned SHAs |
| HF token, SSH keys, machine-local operational state | NOT replicated; not stored anywhere remotely | regenerate per `docs/HF_CUSTODY_REGISTER.md` and operator guidance |

No third storage tier. No Zer0pa-org HF presence. No machine-local-only
asset of recovery value.

## HF Dataset Repos

Two private dataset repos under `Architect-Prime` carry all HF custody
for this lane.

### `Architect-Prime/gnosis-morph-bench-artifacts`

- URL: [https://huggingface.co/datasets/Architect-Prime/gnosis-morph-bench-artifacts](https://huggingface.co/datasets/Architect-Prime/gnosis-morph-bench-artifacts)
- Visibility: **private indefinitely** per Gnosis HF Storage Execution Brief 2026-04-26 §1.3.
- **Stores:** adapter run records (`artifacts/replay/indus_phase4_live_<date>.json` and run records) once `Blocked-1` admits a consumable Phase 3c feature manifest; replay-output bundles; periodic operational-safety snapshots of the consuming GitHub repo's `artifacts/`, `docs/`, `.gpd/`, `fixtures/`, `tests/fixtures/` trees plus root `NOTICE.md`, `README.md`, PRD, and `pyproject.toml`; future cuneiform-family adapter run records once admitted.
- **Does NOT store:** raw corpora; image-bearing benchmark payloads; training data; review-pack artifacts; anything covered by `DATA_POLICY.md` "must NOT yet carry"; HF tokens or any secrets.

### `Architect-Prime/gnosis-morph-bench-authority-bundle`

- URL: [https://huggingface.co/datasets/Architect-Prime/gnosis-morph-bench-authority-bundle](https://huggingface.co/datasets/Architect-Prime/gnosis-morph-bench-authority-bundle)
- Visibility: **private indefinitely** per Gnosis HF Storage Execution Brief 2026-04-26 §1.3.
- **Stores:** a read-only mirror of the live Phase 4 authority bundle once owner-admitted, specifically `governing_route_selection.json`, `stability_report.json`, `dt05_replay.json`, `icit_reference_frozen.json` — each with a companion SHA-256 in the repo-root `MANIFEST.json` and parity-checked against the upstream-declared SHA.
- **Does NOT store:** raw corpora, image payloads, any artifact `DATA_POLICY.md` excludes, any file the source authority has not explicitly cleared for mirror.

## Operational-Safety Snapshot Protocol

Periodic non-credential snapshots of the consuming GitHub repo's
evidence and state trees go to `Architect-Prime/gnosis-morph-bench-artifacts`
under `snapshots/morph_evidence_snapshot_<UTC-iso-stamp>.tar.gz`.
Snapshot procedure:

```bash
SNAPDATE=$(date -u +%Y-%m-%dT%H-%M-%SZ)
SNAPHEAD=$(git rev-parse HEAD)
tar --no-xattrs \
  --exclude='.venv' --exclude='__pycache__' --exclude='.pytest_cache' \
  --exclude='*.egg-info' --exclude='.gpd/state.json.bak' --exclude='.gpd/.state-write-intent' \
  -czf /tmp/morph_evidence_snapshot_${SNAPDATE}.tar.gz \
  artifacts/ docs/ .gpd/ tests/fixtures/ fixtures/ \
  NOTICE.md README.md PRD_GNOSIS_MORPH_BENCH_2026-04-23.md pyproject.toml
SNAPSHA=$(shasum -a 256 /tmp/morph_evidence_snapshot_${SNAPDATE}.tar.gz | cut -d' ' -f1)
# upload with HfApi.upload_file or huggingface-cli upload, then update MANIFEST.json
```

Trigger cadence:

- after every commit that materially changes `artifacts/`, `.gpd/`, or `docs/`;
- before any potentially destructive local operation;
- at minimum weekly while Mac is the primary work environment;
- on any explicit operator directive.

Each snapshot is a complete recovery base — older snapshots may be
pruned by the operator without losing recoverability, since each one
plus the corresponding GitHub commit fully reconstitutes the working
state.

## SHA-256 Pinning

Every artifact pushed to either AP repo carries a SHA-256 recorded at
the repo root `MANIFEST.json`. The manifest shape is:

```json
{
  "schema_version": 1,
  "consuming_github_repo": "Zer0pa/Morph-Bench",
  "consuming_github_commit": "<full sha at admission time>",
  "manifest_purpose": "<short description>",
  "spelling_convention": "artifact (US English)",
  "artifacts": [
    {
      "path": "<relative path inside the HF repo>",
      "sha256": "<hex SHA-256 of the file bytes>",
      "size_bytes": <int>,
      "kind": "<operational_safety_snapshot | adapter_run_record | replay_bundle | source_authority_mirror | ...>",
      "source_provenance": "<workstream-local source path or build command>",
      "consuming_github_commit": "<sha tying admission to a specific repo state>",
      "admitted_utc": "<ISO-8601 admission timestamp>",
      "rights_class": "<internal / owner-deferred-license | source-authority / restricted | ...>",
      "purpose": "<why this artefact is admitted>"
    }
  ]
}
```

No artifact may be uploaded to an HF repo without a corresponding
`MANIFEST.json` entry. Consumers MUST verify the SHA-256 after fetch
before trusting any artifact; the
[`fetch_hf_artifacts`](../scripts/fetch_hf_artifacts.sh) loader
(or the Python equivalent under
[`src/gnosis_morph_bench/hf_cache.py`](../src/gnosis_morph_bench/hf_cache.py))
enforces this.

## Fetch-Back Convention

- Fetched artifacts land in `artifacts/hf_cache/<repo_name>/<artifact_path>` under repo custody.
- `artifacts/hf_cache/` is gitignored — HF fetches are a local materialization, never a repo-custody commit.
- Fetch scripts verify the SHA-256 before declaring the fetch successful; mismatch is a hard failure.
- Authentication uses `HF_TOKEN` from env (or `~/.cache/huggingface/token`, which is what the `huggingface-cli login` flow writes). No token is ever committed to either repo.

## Privacy Posture

Both AP repos remain **private indefinitely** per Gnosis HF Storage
Execution Brief 2026-04-26 §1.3 hard rule: "never make an
`Architect-Prime` Gnosis repo public." Even if the consuming GitHub
repo flips public after legal review, the AP-side custody store stays
private. There is no scenario in which an `Architect-Prime/*` Gnosis
dataset becomes a public surface.

## Consumer Authentication

```bash
# one-time setup on a new workstation
export HF_TOKEN="$(cat ~/.cache/huggingface/token)"

# or, if the HF CLI is installed
huggingface-cli login   # writes ~/.cache/huggingface/token
```

The staged repo never ships an `HF_TOKEN`. Tokens are owner-managed.

## Out Of Scope

This doc does NOT admit new storage back-ends (S3, GCS, Zenodo, etc.)
without a governance decision. If a future phase needs one, it must be
added to this doc, to `DATA_POLICY.md`, and to `PROMOTION_READINESS.md`
together. The Zer0pa HF org is explicitly not a back-end for this
lane and will not be added back without a written operator reversal.
