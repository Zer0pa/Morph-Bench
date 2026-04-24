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

- **GitHub** ([`https://github.com/Zer0pa/Morph-Bench`](https://github.com/Zer0pa/Morph-Bench))
  carries all code, docs, tests, tiny synthetic fixtures, neutral
  adapter-run records, and the committed smoke byte-reference. Upper
  size ceiling is enforced implicitly by the DATA_POLICY's
  "may-carry" list.
- **Hugging Face (org `Zer0pa`)** carries adapter run records against
  admitted production inputs, and a read-only mirror of the live
  Phase 4 authority bundle — both guarded by SHA-256 pinning. Neither
  HF repo stores raw corpora or image-bearing payloads while Blocked-3
  from [`PROMOTION_READINESS.md`](PROMOTION_READINESS.md) is open.

## HF Dataset Repos

Two private dataset repos are provisioned under the `Zer0pa` HF org.

### `Zer0pa/gnosis-morph-bench-artifacts`

- URL: [https://huggingface.co/datasets/Zer0pa/gnosis-morph-bench-artifacts](https://huggingface.co/datasets/Zer0pa/gnosis-morph-bench-artifacts)
- Visibility: **private** until Blocked-2 (canonical LICENSE) closes.
- **Stores:** adapter run records (`artifacts/replay/indus_phase4_live_<date>.json`
  and sibling `indus_phase4_live_<date>_run.json`) once Blocked-1 admits
  a consumable Phase 3c feature manifest; future cuneiform adapter run
  records once that family is admitted per
  [`SOURCE_BOUNDARY.md`](../SOURCE_BOUNDARY.md).
- **Does NOT store:** raw corpora; image-bearing benchmark payloads;
  training data; review-pack artifacts; anything covered by the
  DATA_POLICY "must NOT yet carry" list.

### `Zer0pa/gnosis-morph-bench-authority-bundle`

- URL: [https://huggingface.co/datasets/Zer0pa/gnosis-morph-bench-authority-bundle](https://huggingface.co/datasets/Zer0pa/gnosis-morph-bench-authority-bundle)
- Visibility: **private** until Blocked-2 (canonical LICENSE) closes.
- **Stores:** a read-only mirror of the live Phase 4 authority bundle
  once owner-admitted, specifically
  `governing_route_selection.json`, `stability_report.json`,
  `dt05_replay.json`, `icit_reference_frozen.json` — each with a
  companion SHA-256 in the repo-root `MANIFEST.json`.
- **Does NOT store:** raw corpora, image payloads, any artifact the
  `DATA_POLICY.md` section "must NOT yet carry" lists, any file that
  the source authority has not explicitly cleared for mirror.

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
