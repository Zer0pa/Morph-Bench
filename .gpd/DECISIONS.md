# Decisions

| Date | Phase | Decision | Rationale | Rollback Trigger | Status |
| ---- | ----- | -------- | --------- | ---------------- | ------ |
| `2026-04-23` | `00` | Keep a synthetic smoke fixture in the staged repo | Needed for a real standalone install gate | a better minimal real-source fixture exists without rights drift | `ACTIVE` |
| `2026-04-23` | `00` | Keep heavy corpora and review packs outside the staged repo | Prevents false completeness and rights drift | explicit publish/fetch policy closes and the asset is required for a real gate | `ACTIVE` |
| `2026-04-23` | `00` | Treat live Phase 4 artifacts as source authority only | Avoids overclaiming repo-custody proof | full reruns are generated from this repo | `ACTIVE` |
| `2026-04-28` | `03` | Treat Apache-2.0 code and CC-BY-4.0 docs as settled posture | License rollout happened in parallel and the repo now has root license/notice surfaces | root legal surfaces are superseded by owner decision | `ACTIVE` |
| `2026-04-28` | `03` | Keep data/artifact admission separate from code/docs licensing | Prevents license closure from laundering image-bearing assets, private HF custody, logs, or live replay inputs | owner policy explicitly admits an asset class with rights and storage constraints | `ACTIVE` |
| `2026-04-28` | `03` | Defer Ops-Gates CI consumption until Ops-Gates is self-green | A red internal gate repo cannot be load-bearing for Morph greenlight | `Gnosis-Ops-Gates` canonical CI is green and exposes a pinned Morph-compatible profile | `ACTIVE` |
