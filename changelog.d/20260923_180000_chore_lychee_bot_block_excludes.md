### Changed

- `lychee.toml`: exact-URL excludes for the pwc.com PDF, the beyondtrust.com glossary page and the producthunt amp page (403 bot-blocks), plus `ampcode.com` (persistent HTTP/2 protocol error to lychee). All four return 200 via polyfetch (2026-09-23).
