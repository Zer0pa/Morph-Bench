# Decisions

| Date | Phase | Decision | Rationale | Rollback Trigger | Status |
| ---- | ----- | -------- | --------- | ---------------- | ------ |
| `2026-04-23` | `00` | Keep a synthetic smoke fixture in the staged repo | Needed for a real standalone install gate | a better minimal real-source fixture exists without rights drift | `ACTIVE` |
| `2026-04-23` | `00` | Keep heavy corpora and review packs outside the staged repo | Prevents false completeness and rights drift | explicit publish/fetch policy closes and the asset is required for a real gate | `ACTIVE` |
| `2026-04-23` | `00` | Treat live Phase 4 artifacts as source authority only | Avoids overclaiming repo-custody proof | full reruns are generated from this repo | `ACTIVE` |
