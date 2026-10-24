### Fixed

- `docs/non-cc/infrastructure/jev-analysis.md`: feelings v0.10.0 figures re-read from `results.json`/
  `ytdlp.json` at the tag — Opus 5.5 averaged 0.96 ROC-AUC (was 0.97), yt-dlp per-question AUC 0.76–0.99
  across both Jev runners (was 0.77); adds the Claude-baseline harness disclosure (tool-less `claude -p`)
  and a measurement caveat on cue leakage in mutation-built benchmarks. Closes #622.
