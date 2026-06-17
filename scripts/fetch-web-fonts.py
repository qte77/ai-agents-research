#!/usr/bin/env python3
"""Download self-hosted web fonts (Inter + JetBrains Mono, latin woff2) into
ui/assets/fonts/.

Mirrors the qte77/brand fonts-on-demand convention: the woff2 files are
gitignored and fetched when needed (before `make graph-publish`). The site's
@font-face falls back to system-ui if they are absent, so this step is optional
but recommended for true brand rendering.

Stdlib only. Run from the repo root, or via `make graph-fonts`.
  --force   re-download even if the file already exists
"""
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pages_build import FONT_FILES, is_woff2  # noqa: E402

DEST = Path("ui/assets/fonts")
TIMEOUT = 30


def main() -> int:
    force = "--force" in sys.argv[1:]
    DEST.mkdir(parents=True, exist_ok=True)
    failures = 0
    for name, url in FONT_FILES.items():
        out = DEST / name
        if out.exists() and not force:
            print(f"skip  {name} (exists; --force to refresh)")
            continue
        if not url.startswith("https://"):  # never fetch fonts over plaintext
            print(f"FAIL  {name}: refusing non-HTTPS URL {url}")
            failures += 1
            continue
        try:
            with urllib.request.urlopen(url, timeout=TIMEOUT) as resp:
                data = resp.read()
        except Exception as e:
            print(f"FAIL  {name}: {e}")
            failures += 1
            continue
        if not is_woff2(data):  # reject redirects/error pages/tampered bodies
            print(f"FAIL  {name}: not a woff2 file ({len(data)} bytes) — not written")
            failures += 1
            continue
        out.write_bytes(data)
        print(f"ok    {name} ({len(data):,} bytes)")
    if failures:
        print(f"\n{failures} font(s) failed — site falls back to system-ui until refetched")
        return 1
    print(f"\nFonts ready in {DEST}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
