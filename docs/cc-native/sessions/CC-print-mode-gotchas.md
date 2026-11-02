---
title: CC Print Mode Gotchas
source: empirical testing (cc-recursive-team-mode integration tests, 2026-03-23)
purpose: Document undocumented requirements and pitfalls when using claude -p for headless/CI execution.
created: 2026-03-23
updated: 2026-10-24
validated_links: 2026-10-24
status: verified
---

**Details:** CC v2.1.81

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

## 4. Unattended Headless Lanes (2026-10-24)

Observations from running `claude -p` as an unattended/scripted lane, distinct from the interactive-session gotchas above.

**Project allow rules wait for workspace trust.** Running `claude -p` in a repository prints a line such as "Ignoring N permissions.allow entries from .claude/settings.json: this workspace has not been trusted…" (CC 2.1.310, Codespaces, 2026-10-24). This matches documented behavior, not a bug: Claude Code applies a project's `permissions.allow` rules and `permissions.additionalDirectories` entries only after the workspace trust dialog is accepted for that folder, and "Claude Code shows the trust dialog in interactive sessions only. A `claude -p` run or an SDK session never shows it" ([source][cc-permissions]). A headless lane that needs those allow rules must get trust some other way — e.g. a prior interactive run in the same checkout, or starting from an already-trusted configuration home — not by committing more rules to the project file.

**A stale `GH_TOKEN`/`GITHUB_TOKEN` shadows a working `gh` login.** When either variable is set in the environment but stale or scoped wrong, `gh` calls inside a headless run fail GitHub operations even though `gh auth login` succeeds outside that environment (CC 2.1.310, Codespaces, 2026-10-24). Strip them for the child process: `env -u GH_TOKEN -u GITHUB_TOKEN claude -p …`.

**`--permission-prompts none` exists in 2.1.310.** Confirmed directly against `claude --help` (CC 2.1.310, 2026-10-24), verbatim: `--permission-prompts <target>  Who answers permission prompts with --print: "host" (the SDK host or --permission-prompt-tool) or "none"`. Paired with `--permission-mode auto` (also a valid `--help`-listed choice), a `-p` run can avoid waiting on any permission prompt at all.

**A `/goal` headless run can report `success` with an empty `result`.** A `claude -p` run driving [`/goal`](CC-goal-analysis.md) ended with `subtype: success` and an empty `result` field even after it had shipped PRs (CC 2.1.310, Codespaces, 2026-10-24). Read the PRs or the session transcript to confirm what happened — the `result` field in the `stream-json`/`json` output is not a reliable completion summary for this flow.

## Summary Table

See [CC-cli-reference.md](../configuration/CC-cli-reference.md) for canonical flag definitions. This table covers behavioral gotchas only.

| Flag | Purpose | Gotcha |
|---|---|---|
| `--output-format stream-json` | Structured per-event output | Requires `--verbose` in `-p` mode |
| `--bare` | Skip all project config | Breaks OAuth/keychain auth |
| `--setting-sources user` | Skip project settings only | Can cause hangs (inconsistent) |
| `--verbose` | Enable verbose output | Required for stream-json in `-p` mode |
| `--permission-prompts none` | Skip permission prompts in `-p` mode | Pair with `--permission-mode auto` for a fully unattended run |

## Sources

| Source | Content |
|---|---|
| CC 2.1.81, empirical testing, 2026-03-23 | Original findings (§1–3): `stream-json`/`--verbose`, `--bare` auth, `--setting-sources` hangs |
| [CC permissions docs][cc-permissions] | "Project allow rules and workspace trust" — confirms `permissions.allow` rules wait for the trust dialog, which a `claude -p` run never shows |
| CC 2.1.310, Codespaces, 2026-10-24 | Owner observations (§4): workspace-trust warning text, stale `GH_TOKEN`/`GITHUB_TOKEN`, and `/goal` reporting an empty `result` |
| CC 2.1.310, `claude --help`, 2026-10-24 | `--permission-prompts` and `--permission-mode auto` flag text, confirmed directly against this version |

[cc-permissions]: https://code.claude.com/docs/en/permissions#project-allow-rules-and-workspace-trust
