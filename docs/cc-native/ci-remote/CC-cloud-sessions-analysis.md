---
title: CC Cloud Sessions (Claude Code on the Web) Analysis
source: https://code.claude.com/docs/en/claude-code-on-the-web
purpose: Analysis of Claude Code cloud execution for parallel baseline collection, remote task offloading, and CI-like autonomous runs.
created: 2026-03-07
updated: 2026-07-23
validated_links: 2026-07-23
---

**Status**: Research preview

**Verified**: code.claude.com docs, 2026-07-23

## What Claude Code on the Web Is

Run Claude Code tasks on Anthropic-managed cloud VMs via `claude.ai/code` or the Claude mobile app ([source][cc-cloud]). Each session clones a GitHub repo into an isolated VM, runs a setup script, executes the task, and pushes results to a branch for PR creation. No local machine needed.

### Key Mechanics

- **GitHub not required**: `/web-setup` (syncing your local `gh` CLI token) starts a cloud session without installing the Claude GitHub App — the App is needed only for Auto-fix PR monitoring. Non-GitHub repos aren't a hard blocker either: `claude --cloud` auto-bundles and uploads a local repo (any non-GitHub or GitHub-disconnected git repo) when GitHub access isn't configured (force with `CCR_FORCE_BUNDLE=1`), though a bundled session can't push results back without GitHub auth ([source][cc-cloud])
- **Isolated VMs**: Each session runs in its own Anthropic-managed VM ([source][cc-cloud])
- **Default image**: Pre-installed Python, Node.js, Ruby, PHP, Java, Go, Rust, C++, PostgreSQL 16, Redis 7.0 ([source][cc-cloud])
- **Setup scripts**: Bash scripts run before Claude Code launches (install deps, configure tools) ([source][cc-cloud])
- **Network policy**: Trusted by default (allowlisted domains), configurable to "None", "Full", or "Custom" ([source][cc-cloud])
- **Diff view**: Review changes inline before creating PR, iterate with comments ([source][cc-cloud])
- **Session sharing**: Team visibility (Enterprise/Teams) or Public (Max/Pro) ([source][cc-cloud])

### Starting Sessions

```bash
# From terminal — creates new cloud session
claude --cloud "Fix the authentication bug in src/auth/login.ts"

# Parallel tasks
claude --cloud "Fix flaky test in auth.spec.ts"
claude --cloud "Update API documentation"
claude --cloud "Refactor logger to structured output"

# Monitor
/tasks
```

**Note**: The flag was renamed from `--remote` to `--cloud`; `--remote` still works as a deprecated alias ([source][cc-cloud]).

### Terminal-to-Web-to-Terminal Flow

| Direction | Method | Details |
| --------- | ------ | ------- |
| Terminal -> Web | `claude --cloud "prompt"` | Creates new cloud session; runs independently |
| Web -> Terminal | `/teleport` or `claude --teleport` | Fetches branch, loads conversation history into terminal |
| Plan -> Execute | `claude --permission-mode plan` then `claude --cloud "Execute plan"` | Plan locally (read-only), execute remotely |

**Teleport requirements**: Clean git state, correct repository (not fork), branch pushed to remote, same Claude.ai account ([source][cc-cloud]).

### Environment Configuration

```bash
# Setup script (runs before Claude Code launches)
#!/bin/bash
apt update && apt install -y gh
npm install
pip install -r requirements.txt
```

- **Setup scripts**: Run only when no cached environment snapshot exists — the first session in an environment, after editing the setup script or allowed network hosts, or after the ~7-day cache expires (never on resume). Non-zero exit = session fails ([source][cc-cloud])
- **SessionStart hooks**: Run on every session start (local + cloud). Use `CLAUDE_CODE_REMOTE` env var to scope ([source][cc-hooks])
- **Environment variables**: Configured in UI as `.env` format key-value pairs ([source][cc-cloud])
- **`/remote-env`**: Selects the default remote environment for cloud sessions started with `--cloud` (or `--remote`); add, edit, and archive environments — including their setup scripts, network policy, and environment variables — from the web interface, not via this command. Was undocumented in CC 2.1.87; documented on the [Claude Code on the web page][cc-cloud], not the commands reference

### Network Access Levels

| Level | Behavior |
| ----- | -------- |
| Trusted (default) | Allowlisted domains only (GitHub, npm, PyPI, Docker, cloud providers, etc.) |
| None | Only Anthropic API communication |
| Full | Unrestricted outbound access |
| Custom | Your own allowlist, optionally including the Trusted defaults |

### Security Model

- **GitHub proxy**: Scoped credentials; push restricted to current working branch ([source][cc-cloud])
- **HTTP/HTTPS proxy**: All outbound traffic through security proxy (rate limiting, content filtering) ([source][cc-cloud])
- **Credential isolation**: Git credentials and signing keys never inside sandbox ([source][cc-cloud])

### Pricing

Shares rate limits with all Claude/Claude Code usage. Parallel tasks consume proportionally more ([source][cc-cloud]).

## Applicability to Common Workflows

| Workflow | Fit | Rationale |
| -------- | --- | --------- |
| Parallel CC baseline collection | Strong | `claude --cloud` can run N tasks simultaneously on cloud VMs; no local resource contention |
| Autonomous development loop execution | Moderate | Could run `claude --cloud "Execute next iteration"` but loses local state files and user-local MCP servers |
| CI/CD integration (PR review) | Strong | Kick off cloud session for automated review; results appear as PR |
| Interactive development | Weak | Latency to clone + setup; better to use local CC or Remote Control |
| Workflows requiring local toolchains | Weak | Custom toolchains (LaTeX, pandoc, etc.) need complex setup scripts to replicate in cloud |

### Decision Rule

**Use cloud sessions for parallel, independent tasks that only need GitHub repo access. Use local CC (+ Remote Control) for workflows requiring local MCP servers, state files, or custom toolchains.** See [CC-remote-control-analysis.md](CC-remote-control-analysis.md#remote-control-vs-claude-code-on-the-web) for detailed comparison.

### Potential Integration

```makefile
# Example (NOT implemented — YAGNI until measured need)
CC_REMOTE_TASKS ?=
cc_run_cloud:
    @for task in $(CC_REMOTE_TASKS); do \
        claude --cloud "$$task"; \
    done
    @echo "Monitor with: /tasks"
```

**Recommendation**: Worth exploring for baseline collection where local resources are constrained. Key blockers for deeper adoption:

1. **GitHub connection recommended, not required** — non-GitHub repos work via local-bundle fallback, but can't push results back without GitHub auth
2. **User-local MCP servers only** — MCP servers added via `claude mcp add` (local user config) are unavailable in cloud; servers declared in the repo's committed `.mcp.json` are part of the clone and remain available
3. **No persistent state** — `~/.claude/teams/` and local state files not available
4. **Setup script complexity** — Would need to install project deps and configure env in a setup script
5. **Research preview** — pricing and availability may change

Revisit when:

1. Cloud sessions support custom Docker images or snapshots
2. MCP server forwarding becomes available
3. Baseline collection needs more parallelism than a local machine can provide

## See Also

For canonical CLI flag definitions (`--cloud` (formerly `--remote`), `--teleport`, `--permission-mode`), see [CC-cli-reference.md](../configuration/CC-cli-reference.md).

For authentication setup (GitHub connection, API keys, headless usage), see [CC-web-auth-setup-analysis.md](CC-web-auth-setup-analysis.md).

For external sandbox platforms (OpenSandbox, E2B, Sprites.dev) that provide
alternative cloud execution environments with different tradeoffs (self-hosted,
ephemeral vs stateful, checkpoint/restore), see
[CC-sandbox-platforms-landscape.md](../sandboxing/CC-sandbox-platforms-landscape.md).

## References

- [CC Cloud Sessions docs][cc-cloud]
- [CC Remote Control docs][cc-rc]
- [CC Hooks docs][cc-hooks]
- [CC Settings docs][cc-settings]

[cc-cloud]: https://code.claude.com/docs/en/claude-code-on-the-web
[cc-rc]: https://code.claude.com/docs/en/remote-control
[cc-hooks]: https://code.claude.com/docs/en/hooks
[cc-settings]: https://code.claude.com/docs/en/settings
