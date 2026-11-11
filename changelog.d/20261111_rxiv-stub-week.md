### Fixed

- `.github/workflows/rxiv-paper-eval.yaml`: the week resolver skips feed CSVs under 1 KB. The feed
  now seeds a header-only file for the new ISO week each Monday; on 2026-11-10 the resolver picked
  that stub (W46), loaded 0 papers and finished green, so W45 was never evaluated.
- `docs/cc-native/plugins-ecosystem/CC-plugin-packaging-research.md`: the Plugin Structure skill
  link pointed at a claude-plugins.dev mirror that now returns 402; it points at the skill in
  Anthropic's official plugin marketplace repo.
