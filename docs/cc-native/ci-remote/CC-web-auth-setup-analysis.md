---
title: CC Web Setup, Authentication & API Key Usage
source: https://code.claude.com/docs/en/claude-code-on-the-web, https://code.claude.com/docs/en/authentication, https://code.claude.com/docs/en/cli-usage, https://code.claude.com/docs/en/setup
purpose: How to set up Claude Code on the web, connect GitHub, authenticate with API keys for non-interactive usage, and connect remote sessions.
created: 2026-03-24
updated: 2026-03-24
validated_links: 2026-03-24
---

**Status**: Research preview (web), GA (CLI auth)

## Scope

This document covers **authentication and setup** for Claude Code across web, terminal, and headless modes. For cloud VM execution mechanics, environment configuration, network policy, and session handoff details, see [CC-cloud-sessions-analysis.md](CC-cloud-sessions-analysis.md). For remote monitoring of local sessions, see [CC-remote-control-analysis.md](CC-remote-control-analysis.md). For print mode pitfalls, see [CC-print-mode-gotchas.md](../sessions/CC-print-mode-gotchas.md).

## 1. Claude Code on the Web — GitHub Setup

### Prerequisites

- Claude Pro, Max, Team, or Enterprise account ([source][cc-web])
- GitHub-hosted repository (GitLab/other providers not supported) ([source][cc-web])

### Setup Steps

1. Visit [claude.ai/code](https://claude.ai/code)
2. **Connect GitHub account** — OAuth flow, grants CC read/write access to selected repos
3. **Install Claude GitHub App** — per-repo or org-wide; handles cloning, branch pushing, PR creation
4. **Select default environment** — configure network access, env vars, setup script (see [cloud sessions](CC-cloud-sessions-analysis.md#environment-configuration))
5. Submit task

### Connecting GitHub

#### OAuth via claude.ai (Required)

The web UI at `claude.ai/code` prompts you to connect your GitHub account via OAuth. This installs the **Claude GitHub App** which provides:

- Repository cloning into isolated VMs
- Branch pushing (restricted to working branch)
- PR creation

**GitHub App permissions** (managed by Anthropic, not user-configurable):

- Repository contents: read/write (clone, push branches)
- Pull requests: read/write (create PRs)
- Metadata: read

The GitHub App is installed per-repository or org-wide. You choose which repos to grant access to during installation.

#### No Separate GitHub Token Needed

For terminal-initiated web sessions (`claude --remote`), CC uses your existing Claude.ai OAuth session — not a separate GitHub token. The flow:

1. Run `claude` → browser OAuth → logged into Claude.ai
2. Connect GitHub in `claude.ai/code` settings (one-time)
3. From terminal: `claude --remote "task description"` creates a cloud session

**No separate GitHub token or `gh auth login` is needed for CC web sessions.** The Claude GitHub App handles all git operations in the cloud VM through a dedicated proxy with scoped credentials ([source][cc-web]).

#### GitHub Proxy — How Git Auth Works in Cloud

Inside the cloud VM sandbox, the git client does **not** have your GitHub credentials directly. Instead:

- A **scoped credential** is injected into the sandbox
- All git operations go through a **dedicated GitHub proxy** service
- The proxy verifies the scoped credential and translates it to your actual GitHub auth token
- Push operations are **restricted to the current working branch** ([source][cc-web])

Sensitive credentials (GitHub tokens, signing keys) are never inside the sandbox.

## 2. Authentication Methods — Full Picture

### Authentication Precedence (Terminal CLI)

When multiple credentials are present, CC chooses in this order ([source][cc-auth]):

| Priority | Method | Use Case |
| -------- | ------ | -------- |
| 1 | Cloud provider env vars (`CLAUDE_CODE_USE_BEDROCK`, `_VERTEX`, `_FOUNDRY`) | Organizations using AWS/GCP/Azure |
| 2 | `ANTHROPIC_AUTH_TOKEN` env var | LLM gateway/proxy with bearer tokens |
| 3 | `ANTHROPIC_API_KEY` env var | Direct API access (headless/CI) |
| 4 | `apiKeyHelper` script | Dynamic/rotating credentials from vault |
| 5 | Subscription OAuth (`/login`) | Default for Pro/Max/Team/Enterprise |

**Key insight**: `ANTHROPIC_API_KEY` takes precedence over subscription OAuth once approved. If the key belongs to a disabled org, CC auth fails even if you have a valid subscription. Fix: `unset ANTHROPIC_API_KEY` ([source][cc-auth]).

**Web sessions always use subscription credentials** — `ANTHROPIC_API_KEY` and `ANTHROPIC_AUTH_TOKEN` in the sandbox environment do not override them ([source][cc-auth]).

### Interactive Login

```bash
# Default OAuth login (opens browser)
claude auth login

# Force SSO authentication
claude auth login --sso

# Login with Console credentials (API billing)
claude auth login --console

# Pre-fill email
claude auth login --email user@example.com

# Check auth status
claude auth status        # JSON output
claude auth status --text # Human-readable
```

## 3. API Key for Non-Interactive / Headless Usage

### Creating an Anthropic API Key

1. Go to [platform.claude.com](https://platform.claude.com)
2. Sign up or log in
3. Navigate to **API Keys** section
4. Click **Create Key**
5. Name the key (e.g., `cc-headless-ci`)
6. Copy the key immediately (shown only once)
7. Key format: `sk-ant-api03-...`

**Billing**: API key usage is billed per-token through the Console, separate from Claude Pro/Max subscription. You need credits or a payment method on the Console account.

### Using API Key with Claude Code

```bash
# Set env var
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# Non-interactive (print mode) — runs task and exits
claude -p "Explain the auth module in src/auth/"

# With output format
claude -p --output-format json "List all TODO comments"

# With budget cap
claude -p --max-budget-usd 5.00 "Refactor the logger"

# With turn limit
claude -p --max-turns 10 "Fix failing tests"

# Pipe input
cat error.log | claude -p "What's causing these errors?"

# Continue previous conversation
claude -c -p "Now fix the issue you identified"
```

For stream-json and `--bare` gotchas with API keys, see [CC-print-mode-gotchas.md](../sessions/CC-print-mode-gotchas.md).

### Interactive Mode with API Key

When `ANTHROPIC_API_KEY` is set and you run `claude` interactively, CC prompts once to approve or decline the key. Your choice is remembered. Change later via `/config` → "Use custom API key" toggle ([source][cc-auth]).

### Console-Based Team Setup (API Billing)

For teams that want API-based billing instead of per-seat subscriptions ([source][cc-auth]):

1. Create/use a [Console](https://platform.claude.com) account
2. **Settings → Members → Invite** (or set up SSO)
3. Assign roles:
   - **Claude Code** role — can only create CC API keys
   - **Developer** role — can create any API key
4. Each user: accept invite → install CC → `claude auth login --console`

### apiKeyHelper for Dynamic Credentials

For rotating keys (e.g., from HashiCorp Vault):

```json
{
  "apiKeyHelper": "/path/to/script.sh"
}
```

- Called after 5 minutes or on HTTP 401
- Custom TTL: set `CLAUDE_CODE_API_KEY_HELPER_TTL_MS` env var
- Warning shown if script takes >10 seconds
- **Only applies to terminal CLI** — not Desktop or remote sessions ([source][cc-auth])

## 4. Credential Storage

| Platform | Location |
| -------- | -------- |
| macOS | Encrypted macOS Keychain |
| Linux | `~/.claude/.credentials.json` (mode `0600`) |
| Windows | `~/.claude/.credentials.json` (user profile ACL) |
| Custom | `$CLAUDE_CONFIG_DIR/.credentials.json` |

## Decision Matrix — Which Auth Method to Use

| Scenario | Auth Method | Setup |
| -------- | ----------- | ----- |
| Web sessions (cloud VMs) | OAuth subscription + GitHub App | `claude.ai/code` → Connect GitHub |
| Terminal interactive (personal) | OAuth subscription | `claude auth login` |
| Terminal interactive (team, API billing) | Console credentials | `claude auth login --console` |
| CI/CD headless (print mode) | `ANTHROPIC_API_KEY` | Console → API Keys → Create |
| CI/CD with rotating keys | `apiKeyHelper` script | Settings JSON + vault script |
| AWS/GCP/Azure backend | Cloud provider env vars | Provider-specific setup |
| LLM gateway/proxy | `ANTHROPIC_AUTH_TOKEN` | Gateway provides bearer token |
| Remote Control (mobile monitoring) | OAuth subscription | `claude remote-control` (must be logged in) |

## See Also

- [CC-cloud-sessions-analysis.md](CC-cloud-sessions-analysis.md) — cloud VM execution, environment config, network policy, session handoff
- [CC-remote-control-analysis.md](CC-remote-control-analysis.md) — local execution with remote monitoring
- [CC-remote-access-landscape.md](CC-remote-access-landscape.md) — third-party remote access tools comparison
- [CC-print-mode-gotchas.md](../sessions/CC-print-mode-gotchas.md) — `--bare`, `stream-json`, and `--verbose` pitfalls

## References

- [CC on the Web docs][cc-web]
- [CC Authentication docs][cc-auth]
- [CC CLI Reference][cc-cli]
- [CC Setup docs][cc-setup]
- [CC Security docs][cc-sec]
- [Anthropic Console][console]

[cc-web]: https://code.claude.com/docs/en/claude-code-on-the-web
[cc-auth]: https://code.claude.com/docs/en/authentication
[cc-cli]: https://code.claude.com/docs/en/cli-usage
[cc-setup]: https://code.claude.com/docs/en/setup
[cc-sec]: https://code.claude.com/docs/en/security
[console]: https://platform.claude.com
