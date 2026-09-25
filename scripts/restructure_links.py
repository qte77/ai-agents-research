"""Move docs into subdirectories and rewrite every relative markdown link
repo-wide to match (#309 Phase 1: docs/non-cc/ subdir restructure).

Given a set of (old_repo_path, new_repo_path) moves, this:

1. Rewrites every relative markdown link in every tracked ``*.md`` file that
   resolves to a moved file — inline ``[x](path)`` links and reference-style
   ``[x]: path`` definitions, anchors kept, fenced code blocks left alone.
   This includes links *inside* a moved file itself (to siblings that move
   with it, and to files elsewhere that don't).
2. ``git mv``s the files.
3. Lists (does not edit) tracked non-markdown files that literally mention an
   old path, so a human can repoint globs/generated data by hand.

Pure link-rewriting logic (no filesystem/subprocess access) is kept separate
from IO so it is unit-testable — see tests/test_restructure_links.py. Same
split as .github/scripts/lib/doc_status.py / check-doc-status.py.

Usage:
    # Explicit moves file (old_path<TAB>new_path per line):
    python3 scripts/restructure_links.py --moves-file moves.tsv

    # Derive moves for one section from the filename->subdir map:
    python3 scripts/restructure_links.py \\
        --from-map docs/non-cc/.restructure-map.tsv --section orchestrators

    # Preview without writing/moving anything:
    python3 scripts/restructure_links.py --from-map ... --section ... --dry-run
"""
from __future__ import annotations

import argparse
import posixpath
import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Pure functions — no filesystem/subprocess access, fully unit-testable.
# ---------------------------------------------------------------------------

_URI_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
_FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})")
_INLINE_LINK_RE = re.compile(r'(!?\[[^\]]*\]\()([^)\s]+)((?:\s+"[^"]*")?\))')
_REF_DEF_RE = re.compile(r"^(\s{0,3}\[[^\]]+\]:\s*)(\S+)(.*)$")


def is_local_path_link(target: str) -> bool:
    """True if `target` is a relative filesystem path worth rewriting.

    False for empty/anchor-only targets ('#foo'), repo-absolute paths
    ('/foo'), and anything with a URI scheme (http:, mailto:, ...).
    """
    if not target or target.startswith(("#", "/")):
        return False
    return not _URI_SCHEME_RE.match(target)


def split_anchor(target: str) -> tuple[str, str]:
    """Split 'path#anchor' into (path, '#anchor'); anchor is '' if absent."""
    path, sep, anchor = target.partition("#")
    return path, (sep + anchor)


def resolve_repo_path(link_path: str, from_dir: str) -> str:
    """Resolve a relative link path against from_dir into a normalized
    repo-root-relative POSIX path."""
    return posixpath.normpath(posixpath.join(from_dir or ".", link_path))


def relative_link(target_repo_path: str, from_dir: str) -> str:
    """Compute the relative link from from_dir to target_repo_path."""
    return posixpath.relpath(target_repo_path, start=from_dir or ".")


def rewrite_link_target(
    target: str,
    from_dir_old: str,
    from_dir_new: str,
    moves: dict[str, str],
    known_paths: frozenset[str],
) -> str:
    """Return `target` repointed for a from_dir_old -> from_dir_new move.

    Leaves `target` untouched unless the move actually concerns it: either
    the target itself moved, or the referencing file itself moved (so every
    one of ITS relative links needs recomputing against its new directory).
    A link between two files neither of which moved is left byte-for-byte
    alone, even if it's written in a non-canonical form (e.g. a redundant
    '../non-cc/' or './' prefix) — this tool repoints a move, it does not
    canonicalize unrelated pre-existing links.

    Also leaves `target` untouched when it isn't a local path link, or when
    the resolved path is neither a moved file nor a known repo file — the
    latter guards against mangling reference-definition prose like
    '[Note]: some text' (not a link to a real file).
    """
    if not is_local_path_link(target):
        return target
    path_part, anchor = split_anchor(target)
    if not path_part:
        return target
    old_abs = resolve_repo_path(path_part, from_dir_old)
    target_moved = old_abs in moves
    if not target_moved and old_abs not in known_paths:
        return target
    referencer_moved = from_dir_old != from_dir_new
    if not target_moved and not referencer_moved:
        return target
    new_abs = moves.get(old_abs, old_abs)
    return relative_link(new_abs, from_dir_new) + anchor


def _toggle_fence(line: str, state: tuple[bool, str]) -> tuple[bool, str]:
    """Update (in_fence, marker) for a line already known to be a fence line
    (matched by _FENCE_RE)."""
    in_fence, marker = state
    fence_char = line.strip()[0]
    if not in_fence:
        return True, fence_char * 3
    if line.strip().startswith(marker):
        return False, ""
    return state


def _rewrite_line_links(
    line: str,
    from_dir_old: str,
    from_dir_new: str,
    moves: dict[str, str],
    known_paths: frozenset[str],
) -> str:
    """Rewrite the reference-definition or inline links on one non-fence
    line. A line is either a ref-def or prose with inline links, never both
    in practice, so ref-def takes precedence."""
    ref = _REF_DEF_RE.match(line)
    if ref:
        prefix, target, suffix = ref.group(1), ref.group(2), ref.group(3)
        new_target = rewrite_link_target(target, from_dir_old, from_dir_new, moves, known_paths)
        return f"{prefix}{new_target}{suffix}"

    def _sub_inline(m: re.Match[str]) -> str:
        prefix, target, suffix = m.group(1), m.group(2), m.group(3)
        new_target = rewrite_link_target(target, from_dir_old, from_dir_new, moves, known_paths)
        return f"{prefix}{new_target}{suffix}"

    return _INLINE_LINK_RE.sub(_sub_inline, line)


def rewrite_markdown_links(
    text: str,
    file_old_path: str,
    file_new_path: str,
    moves: dict[str, str],
    known_paths: frozenset[str],
) -> str:
    """Rewrite every relative markdown link in `text` for a file that moves
    from file_old_path to file_new_path (pass the same path for both if the
    file itself doesn't move). Fenced code blocks are left untouched.
    Idempotent: re-running on already-rewritten text is a no-op.
    """
    from_dir_old = posixpath.dirname(file_old_path)
    from_dir_new = posixpath.dirname(file_new_path)
    in_fence, marker = False, ""
    out_lines: list[str] = []
    for line in text.split("\n"):
        if _FENCE_RE.match(line):
            in_fence, marker = _toggle_fence(line, (in_fence, marker))
            out_lines.append(line)
            continue
        if in_fence:
            out_lines.append(line)
            continue
        out_lines.append(
            _rewrite_line_links(line, from_dir_old, from_dir_new, moves, known_paths)
        )
    return "\n".join(out_lines)


# ---------------------------------------------------------------------------
# IO / CLI — subprocess + filesystem. Thin wrappers, not unit-tested (mirrors
# .github/scripts/check-doc-status.py's split from lib/doc_status.py), except
# the simple TSV parsers below which are pure enough to test directly.
# ---------------------------------------------------------------------------


def load_moves_tsv(path: Path) -> dict[str, str]:
    """Parse a TSV of `old_repo_path<TAB>new_repo_path` moves. Blank lines,
    '#' comments, and a bare header row are skipped."""
    moves: dict[str, str] = {}
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        old, _, new = line.partition("\t")
        if not new or old in ("old_path", "filename"):
            continue
        moves[old.strip()] = new.strip()
    return moves


def derive_moves_from_map(map_path: Path, section: str, base_dir: str) -> dict[str, str]:
    """Derive {old: new} moves for one subdir from the filename->subdir map
    (docs/non-cc/.restructure-map.tsv): rows whose subdir column == `section`."""
    moves: dict[str, str] = {}
    for raw in map_path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        filename, _, subdir = line.partition("\t")
        filename, subdir = filename.strip(), subdir.strip()
        if filename == "filename" or subdir != section:
            continue
        moves[f"{base_dir}/{filename}"] = f"{base_dir}/{subdir}/{filename}"
    return moves


def _git_ls_files(repo_root: Path, *pathspec: str) -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(repo_root), "ls-files", "--", *pathspec],
        capture_output=True, text=True, check=True,
    ).stdout
    return [line for line in out.splitlines() if line.strip()]


def apply_link_rewrites(
    repo_root: Path, moves: dict[str, str], known_paths: frozenset[str]
) -> list[str]:
    """Rewrite links in every tracked markdown file at its CURRENT on-disk
    location (before any git mv). Returns the list of changed file paths."""
    changed: list[str] = []
    for rel_path in _git_ls_files(repo_root, "*.md"):
        new_path = moves.get(rel_path, rel_path)
        fs_path = repo_root / rel_path
        text = fs_path.read_text()
        new_text = rewrite_markdown_links(text, rel_path, new_path, moves, known_paths)
        if new_text != text:
            fs_path.write_text(new_text)
            changed.append(rel_path)
    return changed


def apply_moves(repo_root: Path, moves: dict[str, str]) -> list[str]:
    """git mv each old->new path. Skips a pair whose old path no longer
    exists and whose new path already does (idempotent re-run)."""
    moved: list[str] = []
    for old, new in moves.items():
        old_fs, new_fs = repo_root / old, repo_root / new
        if not old_fs.exists() and new_fs.exists():
            continue
        new_fs.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "-C", str(repo_root), "mv", old, new], check=True)
        moved.append(f"{old} -> {new}")
    return moved


def find_nonmd_path_mentions(repo_root: Path, moves: dict[str, str]) -> list[str]:
    """List (never edit) tracked non-markdown files that literally mention an
    old path, so a human can repoint globs / generated data by hand."""
    hits: list[str] = []
    old_paths = list(moves)
    for rel_path in _git_ls_files(repo_root):
        if rel_path.endswith(".md"):
            continue
        try:
            text = (repo_root / rel_path).read_text()
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.split("\n"), start=1):
            for old in old_paths:
                if old in line:
                    hits.append(f"{rel_path}:{lineno}: mentions {old}")
    return hits


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--repo-root", default=".", type=Path)
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--moves-file", type=Path, help="TSV of old_path<TAB>new_path")
    src.add_argument("--from-map", type=Path, help="filename->subdir map, e.g. docs/non-cc/.restructure-map.tsv")
    p.add_argument("--section", help="subdir name to move (required with --from-map)")
    p.add_argument("--base-dir", default="docs/non-cc", help="base dir the map's filenames live under")
    p.add_argument("--dry-run", action="store_true", help="print the planned moves, write/move nothing")
    return p


def _load_moves(args: argparse.Namespace) -> dict[str, str]:
    if args.from_map:
        if not args.section:
            raise SystemExit("--section is required with --from-map")
        return derive_moves_from_map(args.from_map, args.section, args.base_dir)
    return load_moves_tsv(args.moves_file)


def main(argv: list[str]) -> int:
    args = build_arg_parser().parse_args(argv)
    repo_root = args.repo_root.resolve()
    moves = _load_moves(args)
    if not moves:
        print("no moves derived — nothing to do", file=sys.stderr)
        return 1

    if args.dry_run:
        for old, new in moves.items():
            print(f"would move: {old} -> {new}")
        return 0

    known_paths = frozenset(_git_ls_files(repo_root))
    changed = apply_link_rewrites(repo_root, moves, known_paths)
    moved = apply_moves(repo_root, moves)
    mentions = find_nonmd_path_mentions(repo_root, moves)

    print(f"rewrote links in {len(changed)} markdown file(s)")
    for m in moved:
        print(f"moved: {m}")
    if mentions:
        print(f"\n{len(mentions)} non-markdown mention(s) to review by hand:")
        for h in mentions:
            print(f"  {h}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
