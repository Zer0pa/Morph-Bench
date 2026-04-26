# Hugging Face Custody Register

**Consuming GitHub repo:** `Zer0pa/Morph-Bench`
**Register authored:** 2026-04-24
**Verification token:** `Zer0pa HF Storage` — user `Architect-Prime`, org membership `Zer0pa`, scope `fineGrained`
**Spelling convention for this lane:** `artifact` (US English). Do NOT create `artefact`-spelled duplicates under this workstream. (Note: `Zer0pa/glyph-engine-artefacts` and `Zer0pa/cuneiform-control-artefacts` use British spelling under separate lanes — leave those to their owning lanes. Do not rename across lanes without cross-lane coordination.)

## Purpose

This register is the single authoritative record of which Hugging Face repos are claimed by the Morph-Bench lane, whether they are real on the HF API, what their current state is, and what rights class applies. The reviewer's closeout brief (`GNOSIS_REPO_CLOSEOUT_BRIEF_2026-04-24.md` §HF) noted that these repos were NOT visible to the reviewer's token. This register records the verification result against the production token specified above and pinpoints the likely cause of the reviewer's discrepancy.

## Register

| HF repo ID | type | visibility | exists? | last_commit_sha | file_count | rights_class | consuming_github_repo | notes |
|---|---|---|---|---|---|---|---|---|
| `Zer0pa/gnosis-morph-bench-artifacts` | dataset | private | **YES — VERIFIED 2026-04-26** | `f8bf149a15d78d738221a3b00469fdc2b8572de5` | 3 | internal / owner-deferred-license | `Zer0pa/Morph-Bench` | Placeholder only. Files: `.gitattributes`, `MANIFEST.json` (literal `{"artifacts": []}`), `README.md`. `cardData.license=other`. Card updated 2026-04-26 to HF Lane Execution Brief §5 template (Gnosis family rules, no SAL wording). Intended for adapter run records + admitted Phase 3c manifests once Blocked-1 clears. |
| `Zer0pa/gnosis-morph-bench-authority-bundle` | dataset | private | **YES — VERIFIED 2026-04-26** | `094eb8c95b5e2758303fc4771cb04e30ef014e11` | 3 | source-authority / restricted (mirror of live Phase 4 authority bundle) | `Zer0pa/Morph-Bench` | Placeholder only. Files: `.gitattributes`, `MANIFEST.json`, `README.md`. `cardData.license=other`. Card updated 2026-04-26 to HF Lane Execution Brief §5 template; documents that admitted artefacts inherit BOTH Zer0pa private-internal posture AND each upstream artefact's rights class (whichever is more restrictive controls). Intended as a read-only mirror of `governing_route_selection.json`, `stability_report.json`, `dt05_replay.json`, `icit_reference_frozen.json` once Blocked-3 (heavy-data release policy) clears. |

## Reviewer Discrepancy Analysis

The reviewer's brief reports that the production HF token could not see these repos. The production token used here DOES see them (HTTP 200 on both `GET /api/datasets/Zer0pa/{repo}`). Likely causes of the reviewer's result:

1. **Token scope mismatch.** The reviewer may have used a token with default `read` scope or a narrower fine-grained scope that excludes private org datasets. The production token used for this register has scope `fineGrained` with org `Zer0pa` visibility confirmed via `GET /api/whoami-v2`.
2. **Token belonged to a different account.** The reviewer's brief does not name the token used. The production token authenticates as `Architect-Prime` with verified org membership `Zer0pa` (21 datasets visible under that author, including these two).
3. **API case-sensitivity for `author` query.** `GET /api/datasets?author=Zer0pa` returns 21 entries; `?author=zer0pa` (lowercase) returns a different result. Direct `GET /api/datasets/Zer0pa/{repo}` (path-based) always works when the path case matches the actual repo ID.

**Remediation:** owner issues a dedicated production-read HF token scoped to org `Zer0pa` with `dataset:read` on private repos and pins it to the reviewer's machine. Until then, reviewers relying on `GET /api/datasets?author=Zer0pa` must be instructed to also hit the path-based endpoint directly for each named repo in this register.

## Full Inventory (author=Zer0pa, 2026-04-24)

21 datasets visible under author `Zer0pa` with the production token. Of those, two belong to this lane (see table above). The remaining 19 belong to other lanes and are NOT in Morph-Bench's custody:

- Other Gnosis lanes: `gnosis-indus-artifacts`, `glyph-engine-artefacts` (note artefact spelling — other lane), `cuneiform-control-artefacts` (other lane)
- Unrelated ZPE project repos: `ZPE-Robotics-artifacts`, `Zer0paShip-artifacts`, `ZPE-Video-artifacts`, `ZPE-Neuro-artifacts`, `ZPE-Bio-artifacts`, `ZPE-IoT-artifacts`, `ZPE-Geo-artifacts`, `ZPE-Ink-artifacts`, `ZPE-FT-artifacts`, `ZPE-Prosody-artifacts`, `ZPE-Mocap-artifacts`, `ZPE-Cipher-artifacts`, `ZPE-XR-artifacts`, `zpe-image-codec-artifacts`, `DM3-artifacts`, `DM3-binary`

Morph-Bench does NOT own or consume any of those other repos.

## Rights Class Definitions

- **internal / owner-deferred-license:** content is internal to Zer0pa, no redistribution rights granted to anyone outside Zer0pa, license to be decided as part of `Blocked-2` (canonical LICENSE) per `docs/PROMOTION_READINESS.md`.
- **source-authority / restricted:** content is a read-only mirror of live-source authority artifacts whose rights are governed by the originating data-rights chain documented in `../../01_prd_and_authority/AUTHORITY_CHAIN.md`. Redistribution blocked on `Blocked-3` (heavy-data release policy).

## SHA-256 Pinning Posture

Per `docs/HF_STORAGE.md` §SHA-256 pinning, every artifact committed to either HF repo MUST have its SHA-256 recorded in the repo's `MANIFEST.json`. Both current `MANIFEST.json` files are literal `{"artifacts": []}` — no artifacts pinned because no artifacts have been admitted.

When Blocked-1 or Blocked-3 clear and artifacts are admitted, the admission protocol is:

1. Compute SHA-256 on the source file.
2. Append to the target repo's `MANIFEST.json` with the file path, size, SHA-256, source provenance, and admission date.
3. Upload the file under the same path.
4. Record the admission in `artifacts/blind_clone/` or `artifacts/replay/` as appropriate.
5. Update this register's `file_count` and `last_commit_sha` columns.

## Verification Protocol

To reproduce the verification recorded here:

```bash
HF_TOKEN=$(cat <HF_TOKEN_PATH>)
curl -s -H "Authorization: Bearer $HF_TOKEN" https://huggingface.co/api/whoami-v2
curl -s -w "HTTP:%{http_code}\n" -H "Authorization: Bearer $HF_TOKEN" \
  "https://huggingface.co/api/datasets/Zer0pa/gnosis-morph-bench-artifacts"
curl -s -w "HTTP:%{http_code}\n" -H "Authorization: Bearer $HF_TOKEN" \
  "https://huggingface.co/api/datasets/Zer0pa/gnosis-morph-bench-authority-bundle"
```

HTTP 200 + payload indicates the repo exists and is visible to the token. HTTP 404 indicates the repo does not exist OR is invisible to the token (HF API does not distinguish between "doesn't exist" and "exists but you can't see it" for privacy reasons).

## Architect-Prime Posture (Storage Routing)

The Gnosis HF Storage Execution Brief 2026-04-26 supersedes the earlier "Architect-Prime is a cleanup target" framing. Architect-Prime is now the **canonical heavy private store** for Gnosis lanes (brief §1.2). Re-verified state for the Morph-Bench lane on 2026-04-26 with the production token:

- `GET /api/datasets/Architect-Prime/gnosis-morph-bench-artifacts` → HTTP 404 (does not exist).
- `GET /api/datasets/Architect-Prime/gnosis-morph-bench-authority-bundle` → HTTP 404 (does not exist).
- `GET /api/datasets?author=Architect-Prime&limit=200` → 18 datasets visible, all ZPE-lane (zpe-video, zpe-neuro, zpe-robotics, etc.); **0 morph/bench matches**. The earlier "0 total" reading from the Wave 3 register was a token-visibility artefact at that scan time, not a fact about the namespace.

**Routing decision for this lane:** the two `Architect-Prime/*` heavy-tier repos remain **not-yet-created** because no heavy content has been admitted. Per brief §3 ("if a repo does not yet exist on Architect-Prime, create it only if the lane actually has heavy content worth storing there"), both will be created on first heavy admission only. Both Zer0pa cards now document the routing rule so reviewers understand the planned split.

**Storage-routing register:**

| GitHub repo | Lightweight tier (Zer0pa) | Heavy tier (Architect-Prime) | Heavy-tier status |
|---|---|---|---|
| `Zer0pa/Morph-Bench` | `Zer0pa/gnosis-morph-bench-artifacts` (private, exists) | `Architect-Prime/gnosis-morph-bench-artifacts` | **planned, not yet created** — create on first heavy admission |
| `Zer0pa/Morph-Bench` | `Zer0pa/gnosis-morph-bench-authority-bundle` (private, exists) | `Architect-Prime/gnosis-morph-bench-authority-bundle` | **planned, not yet created** — create when upstream rights-class clears under Blocked-3 |

## Change Log

- **2026-04-24** — first authored. Both repos verified present on HF under the production token. Reviewer-side invisibility flagged as a likely token-scope issue rather than a custody failure.
- **2026-04-26** — HF Lane Execution Brief 2026-04-26 pass. Updated both HF dataset cards to the §5 template (Gnosis family rules: no SAL wording, no open-source claims, blockers/no-go context preserved). New `last_commit_sha` recorded above for each repo. Architect-Prime namespace confirmed empty for this lane. Visibility decisions: both repos remain PRIVATE per Wave 2 non-negotiables and §4.4 Gnosis table ("first plausible public candidate later", not now).
- **2026-04-26 (later same day)** — Gnosis HF Storage Execution Brief 2026-04-26 pass. Re-verified: `Architect-Prime/{gnosis-morph-bench-artifacts, gnosis-morph-bench-authority-bundle}` both return HTTP 404 (do not exist). Re-uploaded both Zer0pa cards with the §5.1 "Heavy artefacts" routing block stating the canonical heavy store is `Architect-Prime/*` once heavy admission occurs. New HF SHAs: artifacts → `b47d7c555eae...`, authority-bundle → `c6ecefedd4b7...`. No Architect-Prime repos created in this pass (no heavy content to admit). `docs/HF_STORAGE.md` rewritten to reflect the three-tier model (GitHub / Zer0pa lightweight / Architect-Prime heavy) and the brief's routing thresholds.
