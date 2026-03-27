---
title: CC Print Mode Gotchas
source: empirical testing (cc-recursive-team-mode integration tests, 2026-03-23)
purpose: Document undocumented requirements and pitfalls when using claude -p for headless/CI execution.
created: 2026-03-23
updated: 2026-03-23
---

**Status**: Verified (CC v2.1.81)

## 1. `stream-json` Requires `--verbose` in `-p` Mode

When using `--output-format stream-json` with `-p` (print mode), the `--verbose`
flag is **required**. Without it, claude exits immediately with exit code 1 and
an error message on stderr:

```bash
# FAILS — exit code 1, no output
claude -p "say hi" --output-format stream-json
# stderr: "Error: When using --print, --output-format=stream-json requires --verbose"

# WORKS
claude -p "say hi" --output-format stream-json --verbose
```

This is not documented in `claude --help` or the official docs. The `--verbose`
flag description says "Override verbose mode setting from config" with no mention
of stream-json dependency.

**Impact**: Any harness using `stream-json` for structured output parsing (tokens,
cost, tool calls) must include `--verbose` or all runs silently fail.

**Workaround**: Always pair `--output-format stream-json` with `--verbose`.

## 2. `--bare` Breaks OAuth/Keychain Auth

The `--bare` flag is documented as "Minimal mode: skip hooks, LSP, plugin sync,
attribution, auto-memory, background prefetches, keychain reads, and CLAUDE.md
auto-discovery." The critical detail is **keychain reads** — this means OAuth
tokens stored in the system keychain are not read.

```bash
# FAILS in Codespaces — "Not logged in · Please run /login"
claude --bare -p "say hi" --output-format stream-json --verbose

# WORKS — only if ANTHROPIC_API_KEY env var is set
ANTHROPIC_API_KEY=sk-ant-... claude --bare -p "say hi" --output-format stream-json --verbose

# WORKS — without --bare, keychain auth is used
claude -p "say hi" --output-format stream-json --verbose
```

The `--bare` docs do state "Anthropic auth is strictly ANTHROPIC_API_KEY or
apiKeyHelper via --settings (OAuth and keychain are never read)" but this is
easy to miss.

**Impact**: In environments using OAuth (GitHub Codespaces, interactive `claude
auth login`), `--bare` makes claude unable to authenticate. The error appears as
`exit_code=1` with `"error":"authentication_failed"` in the stream-json output.

**Workaround**: Use `--setting-sources user` instead of `--bare` to skip project
config while preserving auth. Or control config isolation via the working
directory (run from a dir without `.claude/`).

## 3. `--setting-sources` Can Cause Hangs

The `--setting-sources user` flag was tested as an alternative to `--bare` for
skipping project-level `.claude/` config while preserving auth. In some cases,
it caused the subprocess to hang indefinitely (>5 minutes) before the timeout
killed it.

This behavior was inconsistent — sometimes it worked, sometimes it hung. The
root cause is unclear (possibly related to plugin sync or LSP initialization
when project settings are partially loaded).

**Recommendation**: For PLAIN vs ENHANCED profile comparison, control the
working directory content rather than using CLI flags. Run PLAIN tests from a
directory without `.claude/`, and ENHANCED tests from a directory with `.claude/`.
This is the most reliable approach.

## Summary Table

| Flag | Purpose | Gotcha |
|---|---|---|
| `--output-format stream-json` | Structured per-event output | Requires `--verbose` in `-p` mode |
| `--bare` | Skip all project config | Breaks OAuth/keychain auth |
| `--setting-sources user` | Skip project settings only | Can cause hangs (inconsistent) |
| `--verbose` | Enable verbose output | Required for stream-json in `-p` mode |
