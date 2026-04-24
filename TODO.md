# TODO

> Promotion-related items are now tracked in
> [docs/PROMOTION_READINESS.md](docs/PROMOTION_READINESS.md).

- Add real manifest adapters for the Indus and cuneiform source families. → see docs/PROMOTION_READINESS.md (Blocked-1 for Indus live manifest access; cuneiform listed under `## Deferred By Scope`).
- Replace all remaining owner-deferred repo metadata once a private remote and
  license text exist. → see docs/PROMOTION_READINESS.md (Blocked-2: canonical LICENSE; Blocked-3: heavy-data release policy).

## Superseded (tracked in PROMOTION_READINESS.md)

Items below are preserved verbatim for traceability. They are now fully
enumerated in `docs/PROMOTION_READINESS.md` and should be read against
that document rather than acted on from here.

- Port live route-scoring logic into `src/gnosis_morph_bench/`.
  (Superseded by `docs/PROMOTION_READINESS.md §Pass Now` — "Adapter and
  five-mode stability battery implemented under repo custody against
  synthetic fixtures." Implementation landed in Phase 02:
  `src/gnosis_morph_bench/benchmark.py`, `adapters/indus_phase4.py`.)
- Port live stability and replay logic into corpus-neutral helpers.
  (Superseded by `docs/PROMOTION_READINESS.md §Pass Now` — "Neutral
  `ReplayRecord` shape matches the stability battery contract." Five
  canonical modes live under `src/gnosis_morph_bench/stability.py` and
  `src/gnosis_morph_bench/replay.py` per
  `docs/family/STABILITY_BATTERY_v1.md`.)
- Run a blind-clone verification pass after the first real extraction wave.
  (Superseded by `docs/PROMOTION_READINESS.md §Pass Now` — "Standalone
  install from a blind clone" and "Blind-clone transcript itself as audit
  evidence." The pass ran as Plan 03-01 on HEAD
  `0c323026ba0195d3c615916a952fb2f5a8d40745`; transcript at
  `artifacts/blind_clone/03-01_transcript.md`, Disposition PASS on both
  macOS primary and RunPod secondary.)
