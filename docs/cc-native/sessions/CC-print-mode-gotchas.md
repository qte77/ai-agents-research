---
title: CC Print Mode Gotchas
purpose: Document undocumented requirements and pitfalls when using claude -p for headless/CI execution.
created: 2026-03-23
updated: 2026-11-26
validated_links_on: 2026-11-09
status: reference
---

**Details:** CC v2.1.81. Found by empirical testing (cc-recursive-team-mode integration tests, 2026-03-23).

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

The official [headless page](https://code.claude.com/docs/en/headless#stream-responses) shows the pairing in its examples (`--output-format stream-json --verbose --include-partial-messages`) but does not state that `--verbose` is required; the exit-code-1 behaviour below is an empirical CC 2.1.81 finding that the docs do not restate (checked 2026-11-26).

**Impact**: Any harness using `stream-json` for structured output parsing (tokens,
cost, tool calls) must include `--verbose` or all runs silently fail.

**Workaround**: Always pair `--output-format stream-json` with `--verbose`.

## 2. `--bare` Breaks OAuth/Keychain Auth

The `--bare` flag is documented (CLI reference, checked 2026-11-26) as "Minimal mode: skip auto-discovery of your hooks and of skills, custom commands, subagents, installed plugins, MCP servers, auto memory, and CLAUDE.md so scripted calls start faster". The critical detail, per the headless page, is that bare mode never reads OAuth credentials or the system keychain, so tokens stored there are not read. The headless page also says `--bare` will become the default for `-p` in a future release.

```bash
# FAILS in Codespaces — "Not logged in · Please run /login"
claude --bare -p "say hi" --output-format stream-json --verbose

# WORKS — only if ANTHROPIC_API_KEY env var is set
ANTHROPIC_API_KEY=sk-ant-... claude --bare -p "say hi" --output-format stream-json --verbose

# WORKS — without --bare, keychain auth is used
claude -p "say hi" --output-format stream-json --verbose
```

The headless page states that bare mode never reads OAuth credentials or the system keychain; for the Anthropic API, set `ANTHROPIC_API_KEY` or supply an `apiKeyHelper` in the `--settings` JSON, while Bedrock, Google Cloud's Agent Platform and Microsoft Foundry still read their own provider credentials, and bare mode "doesn't use your subscription login". This is easy to miss.

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

**Project allow rules wait for workspace trust.** Running `claude -p` in a repository prints a line such as "Ignoring N permissions.allow entries from .claude/settings.json: this workspace has not been trusted…" (CC 2.1.310, Codespaces, 2026-10-24). This matches documented behavior, not a bug: Claude Code applies a project's `permissions.allow` rules and `permissions.additionalDirectories` entries only after the workspace trust dialog is accepted for that folder, and "Claude Code shows the trust dialog in interactive terminal sessions, but not in `claude -p` or SDK sessions" ([source][cc-permissions]). A headless lane that needs those allow rules must get trust some other way — e.g. a prior interactive run in the same checkout, or starting from an already-trusted configuration home — not by committing more rules to the project file.

**A stale `GH_TOKEN`/`GITHUB_TOKEN` shadows a working `gh` login.** When either variable is set in the environment but stale or scoped wrong, `gh` calls inside a headless run fail GitHub operations even though `gh auth login` succeeds outside that environment (CC 2.1.310, Codespaces, 2026-10-24). Unset them only for the `gh` and git network commands inside the run, not for the whole `claude -p` process: other tooling may need `GITHUB_TOKEN`. In Codespaces the commit signer does; without it, `git commit` fails with `gpg: skipped "GitHub <noreply@github.com>": No secret key` (observed 2026-10-29). Fix the token in your environment rather than encoding a workaround in the repo.

**`--permission-prompts none` exists in 2.1.310** (documented as requiring v2.1.259 or later; `claude -p` starts in Manual mode from v2.1.302). Confirmed directly against `claude --help` (CC 2.1.310, 2026-10-24), verbatim: `--permission-prompts <target>  Who answers permission prompts with --print: "host" (the SDK host or --permission-prompt-tool) or "none"`. Paired with `--permission-mode auto` (also a valid `--help`-listed choice), a `-p` run can avoid waiting on any permission prompt at all.

**A `/goal` headless run can report `success` with an empty `result`.** A `claude -p` run driving [`/goal`](CC-goal-analysis.md) ended with `subtype: success` and an empty `result` field even after it had shipped PRs (CC 2.1.310, Codespaces, 2026-10-24). Read the PRs or the session transcript to confirm what happened — the `result` field in the `stream-json`/`json` output is not a reliable completion summary for this flow.

## Summary Table

See [CC-cli-reference.md](../configuration/CC-cli-reference.md) for canonical flag definitions. This table covers behavioral gotchas only.

| Flag | Purpose | Gotcha |
|---|---|---|
| `--output-format stream-json` | Structured per-event output | Requires `--verbose` in `-p` mode |
| `--bare` | Skip auto-discovery of hooks, skills, plugins, MCP servers, auto memory and CLAUDE.md | Breaks OAuth/keychain auth |
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
