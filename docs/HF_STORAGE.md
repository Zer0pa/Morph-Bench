# Hugging Face Storage Strategy

This doc specifies how the Gnosis Morph-Bench project divides storage
between GitHub and Hugging Face, following the working agreement
**"GitHub for code, HF for large datasets and artefacts"**. It is
authoritative for where any given artifact class lives, how it is
pinned, and how consumers fetch it. It does NOT override
[`DATA_POLICY.md`](../DATA_POLICY.md) or the workstream-level
[`../../06_handover/DATA_POLICY.md`](../../../06_handover/DATA_POLICY.md);
every storage choice here must be consistent with those policies and
with [`PROMOTION_READINESS.md`](PROMOTION_READINESS.md).

## Split

Storage is a three-tier model (per the Gnosis HF Storage Execution
Brief 2026-04-26 §1.2 + §3):

- **GitHub** ([`https://github.com/Zer0pa/Morph-Bench`](https://github.com/Zer0pa/Morph-Bench))
  carries all code, docs, tests, tiny synthetic fixtures, neutral
  adapter-run records that fit within the DATA_POLICY's "may-carry"
  list, and the committed smoke byte-reference. Upper size ceiling
  is enforced implicitly by the DATA_POLICY.
- **Hugging Face `Zer0pa/*` (lightweight discovery surface)** carries
  manifests, indices, README cards, schema files, comparator tables,
  proof indexes, and small curated artefacts useful for review and
  discovery. This is the first place a reviewer looks. SHA-256 pinning
  applies to every admitted file.
- **Hugging Face `Architect-Prime/*` (canonical heavy private store)**
  carries the heavy bytes — adapter run records against admitted
  production inputs, replay-output bundles, raw or bulky evidence
  payloads, the read-only mirror of the live Phase 4 authority
  bundle, and any artefact meeting the routing thresholds below.
  Created on first heavy admission; not yet created today (no heavy
  content has been admitted). **Hard rule: never made public** per
  brief §1.3.

Neither HF tier stores raw corpora or image-bearing payloads while
Blocked-3 from [`PROMOTION_READINESS.md`](PROMOTION_READINESS.md) is
open.

## Routing Thresholds

Per Gnosis HF Storage Execution Brief 2026-04-26 §4. Default to these
when in doubt:

- single file > 1 MB → heavy tier (`Architect-Prime/*`);
- lane payload > 100 MB total → heavy tier;
- model weight of any size → heavy tier;
- many-file directory with meaningful aggregate weight → heavy tier;
- small JSON / Markdown / schema / manifest / index → lightweight
  (`Zer0pa/*`);
- if a payload is small AND useful for discovery, dual-host on both
  tiers (org for discovery, AP for canonical custody) when the byte
  cost of duplication is trivial.

## HF Dataset Repos

### Lightweight tier — `Zer0pa/*` (org discovery surface)

Two private dataset repos are provisioned under the `Zer0pa` HF org.
Both currently hold lightweight cards + empty `MANIFEST.json` only.

#### `Zer0pa/gnosis-morph-bench-artifacts`

- URL: [https://huggingface.co/datasets/Zer0pa/gnosis-morph-bench-artifacts](https://huggingface.co/datasets/Zer0pa/gnosis-morph-bench-artifacts)
- Tier: **lightweight discovery surface**.
- Visibility: **private** until orchestrator approval AND Blocked-2.
- **Stores:** the manifest index, README card, schema descriptors, and
  small curated proof summaries that point a reviewer at the heavy
  bytes living in `Architect-Prime/gnosis-morph-bench-artifacts`. May
  also dual-host particularly important small artefacts where the byte
  cost is trivial.
- **Does NOT store:** heavy adapter run records, replay-output
  bundles, raw corpora, image-bearing payloads, training data, or
  anything meeting the routing-threshold "heavy" criteria above.

#### `Zer0pa/gnosis-morph-bench-authority-bundle`

- URL: [https://huggingface.co/datasets/Zer0pa/gnosis-morph-bench-authority-bundle](https://huggingface.co/datasets/Zer0pa/gnosis-morph-bench-authority-bundle)
- Tier: **lightweight discovery surface for the authority mirror**.
- Visibility: **private** until orchestrator approval AND Blocked-2.
- **Stores:** the manifest index and README card describing the
  intended mirror of the live Phase 4 authority bundle. The actual
  mirror bytes (`governing_route_selection.json`,
  `stability_report.json`, `dt05_replay.json`,
  `icit_reference_frozen.json`) live in
  `Architect-Prime/gnosis-morph-bench-authority-bundle` once admitted,
  per the brief's heavy-tier routing for sensitive content regardless
  of byte size.
- **Does NOT store:** any image payload, any artefact the
  `DATA_POLICY.md` "must NOT yet carry" list excludes, any file the
  source authority has not explicitly cleared for mirror.

### Heavy tier — `Architect-Prime/*` (canonical private store)

Two `Architect-Prime` dataset repos are reserved by the routing
contract but **not yet created** (no heavy artefacts have been
admitted). Both will be created on first heavy admission per brief
§6 Step 4.

#### `Architect-Prime/gnosis-morph-bench-artifacts` (planned)

- Tier: **canonical heavy private store**.
- Visibility: **private indefinitely** per brief §1.3 hard rule.
- **Will store:** adapter run records against admitted production
  inputs (`artifacts/replay/indus_phase4_live_<date>.json` and run
  records); replay-output bundles; bulky benchmark dumps; future
  cuneiform-family heavy artefacts when that adapter ratifies.
- **Will NOT store:** raw image-bearing corpora until Blocked-3
  rights-class clears; any artefact bypassing the SHA-256 manifest
  pin.

#### `Architect-Prime/gnosis-morph-bench-authority-bundle` (planned)

- Tier: **canonical heavy private mirror of upstream authority**.
- Visibility: **private indefinitely** per brief §1.3 hard rule.
- **Will store:** SHA-pinned mirror of the four upstream Phase 4
  authority bundle files once owner-admitted; companion
  upstream-parity SHA records.
- **Will NOT store:** any artefact the upstream authority chain
  has not cleared for mirror.

## SHA-256 Pinning

Every artifact pushed to either HF repo carries a SHA-256 recorded at
the repo root `MANIFEST.json`. The manifest shape is:

```json
{
  "artifacts": [
    {
      "path": "<relative path inside the HF repo>",
      "sha256": "<hex SHA-256 of the file bytes>",
      "source_authority": "<workstream-local source path the file mirrors, if applicable>",
      "admitted_utc": "<ISO-8601 admission timestamp>"
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

- Fetched artifacts land in `artifacts/hf_cache/<repo_name>/<artifact_path>`
  under repo custody.
- `artifacts/hf_cache/` is gitignored — HF fetches are a local
  materialization, never a repo-custody commit.
- Fetch scripts verify the SHA-256 before declaring the fetch
  successful; mismatch is a hard failure.
- Authentication uses `HF_TOKEN` from env (or
  `~/.cache/huggingface/token`, which is what the `huggingface-cli login`
  flow writes). No token is ever committed to either repo.

## Private-Until-License Posture

Both HF repos remain **private** until Blocked-2 (canonical LICENSE)
from [`PROMOTION_READINESS.md`](PROMOTION_READINESS.md) closes. Making
either HF repo public before a canonical LICENSE exists would violate
the license posture of the GitHub repo and of the workstream
DATA_POLICY. Flipping either HF repo to public therefore requires the
same owner decision that produces a canonical `LICENSE` file.

## Consumer Authentication

```bash
# one-time setup on a new workstation
export HF_TOKEN="$(cat ~/.cache/huggingface/token)"

# or, if the HF CLI is installed
huggingface-cli login   # writes ~/.cache/huggingface/token
```

The staged repo never ships an `HF_TOKEN`. Token rotation is handled
by the HF user-settings page for `Architect-Prime`; the `Zer0pa` org
carries no bot token today.

## Out Of Scope

This doc does NOT admit new storage back-ends (S3, GCS, Zenodo, etc.)
without a governance decision. If a future phase needs one, it must be
added to this doc, to `DATA_POLICY.md`, and to `PROMOTION_READINESS.md`
together.
