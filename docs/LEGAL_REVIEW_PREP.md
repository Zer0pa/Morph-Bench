# Legal Review Preparation — Zer0pa/Morph-Bench

**Audience:** Zer0pa legal (or its authorized agent).
**Author:** Lane E closeout (Morph-Bench) per `GNOSIS_REPO_CLOSEOUT_BRIEF_2026-04-24.md`.
**Date:** 2026-04-24.
**Status of this document:** a compact preparation pack. Not legal advice. Not a commitment to any license choice. Not public.

Do not use this document to authorize any public release, any license grant, or any data redistribution. Its only purpose is to give Zer0pa legal a single page from which to make the release-matrix decisions that currently block public promotion.

---

## 1. One-pager: what Morph-Bench is

- **Repo:** `Zer0pa/Morph-Bench` (INTERNAL / private on GitHub).
- **Purpose:** neutral benchmark-first methods lane for the Gnosis extraction program. Owns route scoring, permutation-null metrics, stability and Jaccard checks, deterministic replay, and reference-freeze helpers.
- **Non-purpose:** does NOT own Indus or cuneiform scientific verdicts; does NOT vendor heavy corpora; does NOT ship claims.
- **Phase status:** all four GPD phases (00 / 01 / 02 / 03) complete on `main`. 37 tests pass. Blind-clone verified on macOS + Linux (RunPod) with byte-identical smoke output.
- **Current blockers to public promotion** (enumerated in `docs/PROMOTION_READINESS.md`):
  1. **Blocked-1** — admitted Indus Phase 3c feature manifest access.
  2. **Blocked-2** — canonical `LICENSE` text (THIS DOCUMENT exists to unblock this item).
  3. **Blocked-3** — heavy-data release policy for image-bearing assets.
- **HF custody:** two private HF dataset repos exist and are verified under the production token; see `docs/HF_CUSTODY_REGISTER.md`. Both are empty placeholders until Blocked-1 / Blocked-3 clear.
- **Third-party runtime dependencies:** `numpy` (BSD-3-Clause), `scikit-learn` (BSD-3-Clause). No third-party code is vendored; both libraries are declared as PyPI dependencies in `pyproject.toml`.

---

## 2. The seven questions from the closeout brief, Morph-Bench-annotated

Questions are verbatim from `GNOSIS_REPO_CLOSEOUT_BRIEF_2026-04-24.md` §Legal. Annotation under each question names the specific answer Morph-Bench needs for its release decision.

### Q1. Code licensing

> Should public code be Apache-2.0, MIT, source-available, or proprietary? Apache-2.0 is stronger for patent/contribution clarity; proprietary/source-available preserves more control.

**Morph-Bench-specific annotation.** The code base has no patent-sensitive algorithms, no ML model weights, and depends only on BSD-3-Clause OSS. Apache-2.0 would be straightforward and compatible. MIT would also be compatible but offers no patent grant. Source-available / proprietary is a strict subset of the above and requires no license-compatibility analysis.

**Recommendation (non-binding):** Apache-2.0 if Zer0pa intends the code to be a credible external benchmark reference; source-available otherwise. The code itself does NOT constrain the decision.

### Q2. Documentation licensing

> Should public docs be all-rights-reserved, CC-BY-4.0, CC-BY-NC, or repo-specific?

**Morph-Bench-specific annotation.** Documentation in this repo includes: PRD, adapter contract, stability-battery spec, promotion-readiness doc, blind-clone transcripts, and internal plans/summaries. Of those, some are operational (plans, transcripts) and should arguably remain non-public even if the code is published. Others (PRD, adapter contract, stability battery) are science-facing and benefit from citation under CC-BY.

**Recommendation (non-binding):** split the docs. CC-BY-4.0 for the science-facing contracts and specs; all-rights-reserved for plans/transcripts/governance; keep an internal-only carveout for `STARTUP_PROMPT.md` / `UNIVERSAL_STARTUP_PROMPT.md`.

### Q3. Dataset licensing

> Which artifacts are raw, derived, synthetic, metadata-only, or checksummed manifests? Which may be redistributed?

**Morph-Bench-specific annotation.** Morph-Bench itself produces NO raw data. What lives in or is claimed by this repo:
- **Synthetic fixtures** (`fixtures/tiny_benchmark_manifest.json`, `tests/fixtures/phase4_like_*.json`) — fabricated numeric content. Safe to publish under any license Zer0pa chooses for code.
- **Adapter run records** (planned, not yet produced) — metadata-only; shapes/hashes/paths, no image content.
- **Source-authority mirrors** (planned HF dataset `gnosis-morph-bench-authority-bundle`) — derived metadata from the live Indus Phase 4 bundle; rights govern elsewhere.

**Question for legal specific to this lane:** may synthetic fixtures be published under the same license as the code, or do they require a separate grant?

### Q4. Model weights

> Can weights trained on restricted corpora be distributed at all, even privately to collaborators?

**Morph-Bench-specific annotation.** Morph-Bench ships NO ML model weights. Not applicable to this repo.

### Q5. Third-party provenance

> What obligations attach to Indus images, cuneiform manifests, OSCAR/Tamil/Sanskrit assets, hellosindh data, or any borrowed CV libraries?

**Morph-Bench-specific annotation.**
- This repo vendors ZERO third-party source code and ships ZERO third-party data.
- Runtime dependencies are `numpy` and `scikit-learn`, both BSD-3-Clause, consumed from PyPI at install time.
- When Blocked-1 clears, the Indus Phase 3c feature manifest will land in the HF `gnosis-morph-bench-artifacts` dataset under whatever rights chain `../../01_prd_and_authority/AUTHORITY_CHAIN.md` records for that source. The obligation attaches to THAT data, not to this repo's code.

**Question for legal specific to this lane:** confirm that a BSD-3-Clause attribution line in a future public README is sufficient for the `numpy` + `scikit-learn` dependency surface.

### Q6. Agent-authored code and copied authority docs

> What contributor/IP representation should Zer0pa make before public release?

**Morph-Bench-specific annotation.** Approximately all commits on `main` (32 of 33) are authored by an autonomous Claude executor under GPD orchestration, co-authored with `Claude Opus 4.7 (1M context) <noreply@anthropic.com>`. The repo contains no human-authored source code from anyone outside Zer0pa. Copied authority material (from `../../01_prd_and_authority/` etc.) is cited, not vendored, except for `PRD_GNOSIS_MORPH_BENCH_2026-04-23.md` which is the sovereign PRD for this lane and was authored within the workstream.

**Question for legal specific to this lane:** is "agent-authored under Zer0pa-owned instruction with human-in-the-loop approval at each phase gate" sufficient IP provenance for public release, or is a separate IP assignment needed?

### Q7. Brand/trademark

> Should `Gnosis`, `Zer0pa`, and repo names carry trademark or attribution notices?

**Morph-Bench-specific annotation.** Repo is named `Zer0pa/Morph-Bench`. The package is `gnosis_morph_bench`. README top section says "Gnosis Morph Bench". No trademark / ™ / ® notices currently appear anywhere.

**Recommendation (non-binding):** add a short brand/attribution notice to README if Zer0pa holds or intends to register any of `Gnosis`, `Zer0pa`, or `Morph-Bench` as trademarks. If not, no action.

### Q8. Internal systems

> Confirm that operational prompts, RunPod/Comet/HF custody details, private endpoint transcripts, and repo-gate internals remain non-public.

**Morph-Bench-specific annotation.** All operational paths and endpoints in this repo have been parameterized on 2026-04-24 (commit `695f43e` — chore(scrub)). Symbolic labels `<LOCAL_MONOREPO_ROOT>`, `<RUNPOD_HOST>`, `<RUNPOD_POD_ID>`, `<OPERATOR_SSH_KEY>`, etc. replace the original values. Provenance (SHA-256 values, test counts, authority values, commit SHAs) was preserved.

**Confirm (non-binding):** `STARTUP_PROMPT.md`, `UNIVERSAL_STARTUP_PROMPT.md`, and anything under `artifacts/blind_clone/` or `.gpd/phases/` should remain NON-PUBLIC even if the rest of the repo is published, because they encode the internal operating model even after scrubbing. Recommended: move them to a sibling private repo or to a `private/` subtree excluded from public publication at release time.

---

## 3. Non-claims (not asking legal to bless these here)

These items are outside Lane E's scope. Refer legal to the relevant lane's closeout pack:

- **Indus image and manifest rights, decipherment non-claims, review-pack release posture** — `Zer0pa/Indus-Valley` lane (Lane F per universal prompt).
- **Cuneiform manifest rights, negative-control release framing** — `Zer0pa/Cuneiform` lane (Lane C).
- **Glyph descriptor IP, OSS-baseline scope decision** — `Zer0pa/Glyph-Engine` lane (Lane A).
- **Falsification harness public release framing** — `Zer0pa/Gnosis-Falsification-Harness` lane (Lane B).
- **Operational repo-truth / repo-gates tooling (keep non-public)** — `Zer0pa/Gnosis-Ops-Gates` lane (Lane D).
- **Cross-lane legal consistency** — not this document. This document answers Morph-Bench only.

---

## 4. Minimum decisions needed from legal to unblock Morph-Bench

In priority order. Each is a single yes/no or an instance of "pick one":

1. **Canonical `LICENSE` choice** (Q1). Without this, `Blocked-2` in `docs/PROMOTION_READINESS.md` cannot clear and the repo cannot go public.
2. **Documentation split decision** (Q2). Without this, publishing the code under any license still leaves the docs in a gray state.
3. **BSD-3-Clause attribution method for numpy+sklearn** (Q5). Low-risk, likely a one-line confirmation.
4. **IP provenance ruling on agent-authored commits** (Q6). Without this, a public release could be challenged on contributor representation grounds.
5. **Heavy-data release policy** (Q3 + Blocked-3). Governs the HF `gnosis-morph-bench-authority-bundle` repo's eventual contents. Can be deferred if Zer0pa releases the code first and the authority bundle later.

Items 6 (internal systems confirmation) and 7 (brand/trademark) are lower urgency — the code can go public under Q1's chosen license with the current repo structure and revisit 6/7 in a follow-up pass.

---

## 5. Appendix: third-party provenance in this repo

| Library | Version floor | License | Usage | Vendored? |
|---|---|---|---|---|
| `numpy` | `>=1.26` | BSD-3-Clause | feature matrices, RNG | NO — PyPI dependency |
| `scikit-learn` | `>=1.5` | BSD-3-Clause | clustering, metrics | NO — PyPI dependency |

No other third-party runtime code. Test-time dependency: `pytest` (MIT) — declared as a `[project.optional-dependencies].dev` extra, never installed by default.

No GPL, AGPL, LGPL, CC-BY-NC, CC-BY-SA, or "source-available with field-of-use restriction" code is present.

---

## 6. Appendix: recent commit authorship

| Range | Author(s) |
|---|---|
| All commits on `main` up to `f4e0746` (the STATUS_REPORT commit) | autonomous Claude executor under GPD orchestration, co-authored as `Claude Opus 4.7 (1M context) <noreply@anthropic.com>`. Committer identity: `Zer0pa-Architect-Prime <architects@zer0pa.ai>`. |
| Initial scaffold (`61b2910`) | imported from the workstream-stage scaffold authored during the `SCAFFOLDED_PRIVATE_STAGE` pass. |
| Commit subsequent to `f4e0746` (`695f43e` onward — path scrub + legal prep) | same as above. |

No external / unaffiliated human contributors. No GitHub PRs from outside Zer0pa. No issues from outside Zer0pa (0 open PRs, 0 open issues as of 2026-04-24).

---

## 7. Change log

- **2026-04-24** — authored during Lane E closeout per `GNOSIS_REPO_CLOSEOUT_BRIEF_2026-04-24.md` §5 "Repo Rationale … `Morph-Bench` … Public posture" and §8 "Legal And Licensing Brief".
