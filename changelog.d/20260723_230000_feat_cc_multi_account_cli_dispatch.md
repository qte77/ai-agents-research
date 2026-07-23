### Added

- `scripts/cc-multi-account.sh`: direct-execution dispatch — `./cc-multi-account.sh <profile>` launches, `list`/`ls` lists profiles, `usage <profile>` shows per-account stats, and `-h`/`--help`/no-args print the usage header (unknown options exit 2 with help on stderr). Sourcing is unchanged and still defines `ccp`/`ccu`/`ccl`; the header now documents both modes and why sourcing is required for the short commands.
