### Changed

- `docs/non-cc/reference/system-1-decision-models-landscape.md` § Cloudflare Clef: the gold-set
  results now include Jev 1.13.0 (2026-11-11). On papers Jev scored ROC-AUC 0.968 with a
  recommended `hi` of 0.70 at 91% coverage, overlapping Clef within the bootstrap intervals; on
  issues it scored 62/62. Median call time from a runner was 0.14–0.15 s.
- Plan 0012: H1 and P2 struck. Papers use Clef at `hi` 0.75; issue triage uses Clef in shadow mode.
