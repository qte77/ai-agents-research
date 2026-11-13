### Changed

- `docs/cc-native/configuration/CC-models-reference.md`: dated note on the hardware Claude runs on, cited to Anthropic's S-1/A (filed 2026-11-10: four chip families, one fungible compute pool, Claude used to bring up new chip platforms) and AMD's 2026-07-22 release (up to 2 GW of MI450 Series GPUs, builds on existing MI355X use). A time figure for Mythos on AMD hardware, shared on X, is left out: the filing's text gives only the old "many months" baseline, and its source wasn't traced (plan 0013 O7).
- `lychee.toml`: exclude Anthropic PBC's SEC EDGAR filings path (`sec.gov/Archives/edgar/data/2130357/`). SEC returns 403 to clients without a contact user agent; owner-approved.
