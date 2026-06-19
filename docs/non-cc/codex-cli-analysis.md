---
title: OpenAI Codex CLI (Terminal Agent)
source: https://github.com/openai/codex
purpose: Evaluate Codex CLI as an interactive and headless terminal coding agent, distinct from the cloud Codex environment.
created: 2026-06-16
updated: 2026-06-16
validated_links: 2026-06-16
platform_scope: [openai, cli, vscode, cursor, windsurf]
---

**Status**: Trial

## What It Is

Codex CLI is OpenAI's open-source, locally-running coding agent for the terminal. It ships as a single binary (written primarily in Rust) that opens a full-screen TUI, reads and edits code in the current working directory, executes shell commands, and streams model responses — all with a two-layer safety model (sandbox + approval policy). The repository ([github.com/openai/codex][gh-codex]) reached 91 k GitHub stars and version 0.140.0 as of 2026-06-15.

This doc covers the **terminal agent** only. The cloud Codex environment — a hosted, sandboxed execution layer used by the GitHub Actions integration — is a separate product and is covered in [CC-github-actions-analysis.md](../cc-native/ci-remote/CC-github-actions-analysis.md).

## How It Works

### Architecture

The agent binary is written in Rust (96 % of codebase per GitHub language breakdown, accessed 2026-06-16) with supplementary Python, TypeScript, and shell components. It runs fully on the local machine; the only network call is to the OpenAI API for inference.

### Approval modes and sandboxing

Codex enforces a two-layer protection model ([agent-approvals-security][approvals]):

**Sandbox modes** (controls what the agent can technically access):

| Mode | Scope |
|---|---|
| `workspace-write` (default for VCS folders) | Read/write within workspace; no network |
| `read-only` | Read access only; no edits or network |
| `danger-full-access` | No restrictions; not recommended |

Protected paths (`.git`, `.agents`, `.codex`) are read-only even in `workspace-write` mode.

**Approval policies** (controls when the agent must pause and ask):

| Policy | Behavior |
|---|---|
| `on-request` | Asks before actions that need it (default) |
| `untrusted` | Auto-runs known-safe ops; asks for state-mutating commands |
| `auto_review` | Routes eligible approvals through an automatic reviewer agent |
| `never` | Disables prompts entirely; for hardened environments |

Codex detects the folder context automatically: version-controlled projects get `workspace-write + on-request`; non-VCS folders default to read-only.

### Interactive vs headless

**Interactive**: `codex` launches the full-screen TUI with inline approval flows.

**Headless / CI**: `codex exec` (alias `codex e`) runs non-interactively, streaming JSON events or formatted text to stdout. Key CI flags ([cli-reference][cli-ref]):

- `--json` — newline-delimited JSON event stream
- `--output-last-message, -o` — write assistant's final message to a file
- `--sandbox <mode>` — set sandbox at invocation time
- `--ask-for-approval, -a` — set approval policy (`untrusted | on-request | never`)
- `--dangerously-bypass-approvals-and-sandbox` (`--yolo`) — bypass everything; only inside externally hardened VMs
- `--ephemeral` — no session files persisted to disk

### Key features (as of 2026-06-16, [cli-features][features])

- **Image input**: attach screenshots or design specs via `-i`/`--image` flag or paste in composer (PNG, JPEG)
- **Web search**: built-in, uses OpenAI cached index by default; `--search` switches to live results
- **Model selection**: `gpt-5.5` recommended for complex tasks; switch mid-session with `/model`
- **Subagent parallelisation**: explicit fan-out for parallel subtasks (extra token cost)
- **MCP support**: connect STDIO or streaming-HTTP MCP servers via `config.toml`; launched automatically
- **Session resume**: `codex resume` restores prior conversation and repository state
- **AGENTS.md**: honours `AGENTS.md` files for custom per-project instructions ([agents-md][agents-md])
- **Shell completions**: bash, zsh, fish

### Authentication and access

Codex CLI authenticates via ChatGPT account sign-in (Plus, Pro, Business, Edu, Enterprise plans) or via API key. Access dates back to the initial open-source release; the current access model was confirmed 2026-06-16 on [developers.openai.com/codex][dev-codex].

## Adoption Decision

Codex CLI is **Trial**. The two-layer sandbox + approval model, headless `codex exec` path, and MCP integration make it production-credible for local and CI use. The 91 k-star repo and 842+ releases signal strong community traction and rapid iteration. However, it is not yet Adopt because:

1. **ChatGPT plan dependency**: access requires a paid ChatGPT subscription or API key; no free tier for the recommended `gpt-5.5` model.
2. **Rapid version churn**: 842 releases in roughly one year; APIs and config schema change frequently.
3. **No Claude Code parity**: lacks CC's CLAUDE.md hook system, project-skill architecture, and operator permission model — relevant when evaluating as a CC alternative.

For teams already on OpenAI/ChatGPT Enterprise, this is an immediately viable terminal agent. For CC-native workflows, the primary value is as a reference model for headless sandboxing and approval-policy design.

See also [github-copilot-cli-analysis.md](github-copilot-cli-analysis.md) for a comparable terminal coding agent from GitHub/Microsoft.

## Action Items

- Validate `codex exec` + `--json` pipeline in a container to confirm JSONL schema stability across minor versions.
- Track whether OpenAI exposes a free or lower-cost access tier (not stated as of 2026-06-16).
- Compare AGENTS.md instruction surface to CC's CLAUDE.md/hooks after both stabilise.

## Sources

| Source | Content |
|---|---|
| [openai/codex GitHub repo][gh-codex] | License, star count, version, language breakdown, install methods |
| [Codex developer docs overview][dev-codex] | Access/pricing, GA status, feature overview |
| [Agent approvals & security][approvals] | Sandbox modes, approval policies, defaults |
| [CLI features][features] | Image input, web search, MCP, subagent parallelisation, model selection |
| [CLI command-line reference][cli-ref] | `codex exec` flags, headless/CI options |
| [AGENTS.md guide][agents-md] | Custom per-project instructions support |

[gh-codex]: https://github.com/openai/codex
[dev-codex]: https://developers.openai.com/codex
[approvals]: https://developers.openai.com/codex/agent-approvals-security
[features]: https://developers.openai.com/codex/cli/features
[cli-ref]: https://developers.openai.com/codex/cli/reference
[agents-md]: https://developers.openai.com/codex/guides/agents-md
