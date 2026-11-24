---
title: OpenAI Codex CLI (Terminal Agent)
source: https://github.com/openai/codex
purpose: Evaluate Codex CLI as an interactive and headless terminal coding agent, distinct from the cloud Codex environment.
created: 2026-06-16
updated: 2026-11-23
validated_links_on: 2026-11-15
status: trial
platform_scope: [openai, cli, vscode, cursor, windsurf]
---

## What It Is

Codex CLI is OpenAI's open-source, locally-running coding agent for the terminal. It ships as a single binary (written primarily in Rust) that opens a full-screen TUI, reads and edits code in the current working directory, executes shell commands, and streams model responses — all with a two-layer safety model (sandbox + approval policy). The repository ([github.com/openai/codex][gh-codex]) reached 91 k GitHub stars and version 0.140.0 as of 2026-06-15.

This doc covers the **terminal agent** only. The cloud Codex environment — a hosted, sandboxed execution layer used by the GitHub Actions integration — is a separate product and is covered in [CC-github-actions-analysis.md](../../cc-native/ci-remote/CC-github-actions-analysis.md).

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

**Correction 2026-11-15:** the vendor's [approvals page][approvals] now lists `untrusted` as a retired policy (the setting can stop the client starting), and `auto_review` is a separate `approvals_reviewer` setting, not an approval policy; `granular` is a documented policy that the 2026-06 table omitted. The table above reflects the 2026-06 page.

Codex detects the folder context automatically: version-controlled projects get `workspace-write + on-request`; non-VCS folders default to read-only.

### Interactive vs headless

**Interactive**: `codex` launches the full-screen TUI with inline approval flows.

**Headless / CI**: `codex exec` (alias `codex e`) runs non-interactively, streaming JSON events or formatted text to stdout. Key CI flags ([cli-reference][cli-ref]):

- `--json` — newline-delimited JSON event stream
- `--output-last-message, -o` — write assistant's final message to a file
- `--sandbox <mode>` — set sandbox at invocation time
- `--ask-for-approval, -a` — set approval policy (`on-request | never`; `untrusted` retired, see correction above)
- `--dangerously-bypass-approvals-and-sandbox` (`--yolo`) — bypass everything; only inside externally hardened VMs
- `--ephemeral` — no session files persisted to disk

### Key features (as of 2026-06-16, [cli-features][features])

- **Image input**: attach screenshots or design specs via `-i`/`--image` flag or paste in composer (PNG, JPEG)
- **Web search**: built-in, uses OpenAI cached index by default; `--search` switches to live results
- **Model selection**: `gpt-5.5` recommended for complex tasks; switch mid-session with `/model`. GPT-5.5 retired from Codex with ChatGPT sign-in on 2026-10-14; API-key sessions are not affected ([Codex pricing][codex-pricing], checked 2026-11-15)
- **Subagent parallelisation**: explicit fan-out for parallel subtasks (extra token cost)
- **MCP support**: connect STDIO or streaming-HTTP Model Context Protocol (MCP) servers via `config.toml`; launched automatically
- **Session resume**: `codex resume` restores prior conversation and repository state
- **AGENTS.md**: honours `AGENTS.md` files for custom per-project instructions ([agents-md][agents-md]); cross-agent convergence of this convention is tracked in [multi-agent-onboarding-outlook.md](../../sdlc-lcm/multi-agent-onboarding-outlook.md)
- **Shell completions**: bash, zsh, fish

### Authentication and access

Codex CLI authenticates via ChatGPT account sign-in (Plus, Pro, Business, Edu, Enterprise plans) or via API key. Access dates back to the initial open-source release; the current access model was confirmed 2026-06-16 on [developers.openai.com/codex][dev-codex].

## Providers

Checked 2026-11-23 against the vendor's [config reference][codex-config-ref] and [advanced configuration][codex-config-adv] (both now served from `learn.chatgpt.com`; the reference page was read for its first 100,000 of 166,138 characters plus a targeted second pass).

- **Selection.** `model_provider` picks a provider id from `model_providers` (default `openai`). The ids `openai`, `ollama` and `lmstudio` are reserved; `--oss` runs against a local Ollama or LM Studio, set with `oss_provider`. Provider tables are read from the user-level `~/.codex/config.toml`; a project-local `.codex/config.toml` ignores them.
- **Generic route, documented.** A custom provider sets `base_url`, an `env_key` (or a command-backed `auth` table), optional `query_params` and header tables, and `wire_api`. The only documented `wire_api` value is `responses`, and it is the default, so a provider must implement the OpenAI Responses API. Whether a given Chat-Completions-only endpoint works is therefore not established by these docs; it is not an endorsement of any provider.
- **Azure.** The advanced-configuration page gives an Azure example: an `https://YOUR_PROJECT_NAME.openai.azure.com/openai` base URL, `env_key = "AZURE_OPENAI_API_KEY"`, an `api-version` entry in `query_params` and `wire_api = "responses"`.
- **AWS.** The config reference lists a built-in `amazon-bedrock` provider with `aws.profile` and `aws.region` keys. The excerpt read does not say which models it serves.
- **Google Cloud.** It also lists a built-in `gcp` (Vertex AI) provider with `project_id` (overrides `GOOGLE_CLOUD_PROJECT`), `location` (default `global`), `base_url` and `credential_file` keys. Models served are not stated in the excerpt read.
- **OpenRouter, Infomaniak and other OpenAI-compatible hosts.** The docs show custom providers for Mistral (`https://api.mistral.ai/v1`) and a local Ollama URL; they do not name OpenRouter or Infomaniak. The generic route above would apply only if the endpoint supports the Responses API; this was not tested. Provider-side facts: [CC-model-provider-configuration.md](../../cc-native/configuration/CC-model-provider-configuration.md#infomaniak-ai-swiss-hosted-openai-compatible).
- **Gateways.** A "connect to a gateway" enterprise page and gateway OAuth keys (`gateway_oauth.*`) exist; the page itself was not read.

## Adoption Decision

Codex CLI is **Trial**. The two-layer sandbox + approval model, headless `codex exec` path, and MCP integration make it production-credible for local and CI use. The 91 k-star repo and 842+ releases signal strong community traction and rapid iteration. However, it is not yet Adopt because:

1. **ChatGPT plan dependency**: access requires a paid ChatGPT subscription or API key; no free tier for the recommended `gpt-5.5` model. For CI, OpenAI recommends an API key, billed at API rates rather than plan credits; see [CC-web-auth-setup-analysis.md § Other Coding CLIs](../../cc-native/ci-remote/CC-web-auth-setup-analysis.md#other-coding-clis-headless-sign-in-and-billing).
2. **Rapid version churn**: 842 releases in roughly one year; APIs and config schema change frequently.
3. **No Claude Code parity**: lacks CC's CLAUDE.md conventions, has fewer documented hook events (14 vs 33 as of 2026-11-15; see the [cross-harness matrix](../../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md#cross-harness-matrix-checked-2026-11-15)), and lacks CC's project-skill architecture, and operator permission model — relevant when evaluating as a CC alternative.

For teams already on OpenAI/ChatGPT Enterprise, this is an immediately viable terminal agent. For CC-native workflows, the primary value is as a reference model for headless sandboxing and approval-policy design.

See also [github-copilot-cli-analysis.md](../agents/github-copilot-cli-analysis.md) for a comparable terminal coding agent from GitHub/Microsoft.

## Action Items

- Validate `codex exec` + `--json` pipeline in a container to confirm JSONL schema stability across minor versions.
- Track whether OpenAI exposes a free or lower-cost access tier (not stated as of 2026-06-16).
- Compare AGENTS.md instruction surface to CC's CLAUDE.md/hooks after both stabilise.

## Goal Loop

Checked 2026-10-22 against the vendor's own docs; compared across agents in
[goal-loops-landscape.md](goal-loops-landscape.md).

Codex ships `/goal` in the app, IDE extension and CLI — out of experimental on 2026-05-21
([changelog][goal-codex-changelog]). The agent judges completion itself: it "will stop running when
it's confident it has reached the stopping condition" ([follow goals][goal-codex-follow]); objectives
"must be non-empty and at most 4,000 characters", with `/goal pause`, `/goal resume` and
`/goal clear` ([commands][goal-codex-cmds]). No turn or time bound is documented, so set one yourself.
A `Stop` hook can return `"decision": "block"` to force another turn ([hooks][goal-codex-hooks]).

## Sources

| Source | Content |
|---|---|
| [openai/codex GitHub repo][gh-codex] | License, star count, version, language breakdown, install methods |
| [Codex developer docs overview][dev-codex] | Access/pricing, GA status, feature overview |
| [Agent approvals & security][approvals] | Sandbox modes, approval policies, defaults |
| [CLI features][features] | Image input, web search, MCP, subagent parallelisation, model selection |
| [CLI command-line reference][cli-ref] | `codex exec` flags, headless/CI options |
| [AGENTS.md guide][agents-md] | Custom per-project instructions support |
| [Codex config reference][codex-config-ref] | `model_provider` / `model_providers` keys, built-in `amazon-bedrock` and `gcp` provider keys (2026-11-23) |
| [Codex advanced configuration][codex-config-adv] | Custom provider, Azure and Ollama examples (2026-11-23) |

[gh-codex]: https://github.com/openai/codex
[dev-codex]: https://developers.openai.com/codex
[approvals]: https://developers.openai.com/codex/agent-approvals-security
[features]: https://developers.openai.com/codex/cli/features
[cli-ref]: https://developers.openai.com/codex/cli/reference
[agents-md]: https://developers.openai.com/codex/guides/agents-md
[goal-codex-changelog]: https://learn.chatgpt.com/docs/changelog
[goal-codex-follow]: https://learn.chatgpt.com/use-cases/follow-goals
[goal-codex-cmds]: https://learn.chatgpt.com/docs/developer-commands?surface=cli
[goal-codex-hooks]: https://learn.chatgpt.com/docs/hooks
[codex-pricing]: https://learn.chatgpt.com/docs/pricing
[codex-config-ref]: https://learn.chatgpt.com/docs/config-file/config-reference
[codex-config-adv]: https://learn.chatgpt.com/docs/config-file/config-advanced
