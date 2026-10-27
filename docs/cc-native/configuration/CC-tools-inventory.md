---
title: CC Tools Inventory
purpose: Point-in-time snapshot of all CC built-in tools, slash commands, and configuration surfaces with permission requirements and categories.
created: 2026-03-27
updated: 2026-10-26
validated_links: 2026-10-26
status: adopt
---

## What It Is

CC 2.1.83 ships 28 built-in tools. This is a categorized snapshot linking to the [official tools reference][tools-ref] as the authoritative source. Check that page for current descriptions — tools are added across CC releases.

## Tool Inventory (CC 2.1.83, 2026-03-27)

### File Operations

| Tool | Permission | Purpose |
|---|---|---|
| `Read` | No | Read file contents (text, images, PDFs, notebooks) |
| `Edit` | Yes | Targeted edits to files |
| `Write` | Yes | Create or overwrite files |
| `NotebookEdit` | Yes | Modify Jupyter notebook cells |
| `Glob` | No | Find files by pattern |
| `Grep` | No | Search file contents by regex |

### Execution

| Tool | Permission | Purpose |
|---|---|---|
| `Bash` | Yes | Execute shell commands |
| `PowerShell` | Yes | Execute PowerShell (Windows, opt-in preview) |

### Agent & Task Management

| Tool | Permission | Purpose |
|---|---|---|
| `Agent` | No | Spawn subagent with own context window |
| `TaskCreate` | No | Create task in task list |
| `TaskGet` | No | Get task details |
| `TaskList` | No | List all tasks |
| `TaskUpdate` | No | Update task status/dependencies |
| `TaskStop` | No | Kill background task |
| `TaskOutput` | No | (Deprecated) Read background task output — use `Read` instead |
| `TodoWrite` | No | Session task checklist (non-interactive / Agent SDK) |

### Planning & Navigation

| Tool | Permission | Purpose |
|---|---|---|
| `EnterPlanMode` | No | Switch to plan mode |
| `ExitPlanMode` | Yes | Present plan for approval |
| `EnterWorktree` | No | Create isolated git worktree |
| `ExitWorktree` | No | Exit worktree session |
| `LSP` | No | Code intelligence via language servers |

### Scheduling

| Tool | Permission | Purpose |
|---|---|---|
| `CronCreate` | No | Schedule recurring prompt in session |
| `CronDelete` | No | Cancel scheduled task |
| `CronList` | No | List scheduled tasks |

### External & MCP

| Tool | Permission | Purpose |
|---|---|---|
| `WebFetch` | Yes | Fetch URL content |
| `WebSearch` | Yes | Web search |
| `ListMcpResourcesTool` | No | List MCP server resources |
| `ReadMcpResourceTool` | No | Read MCP resource by URI |
| `ToolSearch` | No | Search/load deferred tools (MCP tool search) |

#### `WebFetch` behavior notes

Documented and empirically observed behaviors researchers should know before relying on `WebFetch`:

- **Minimal schema, no header customization.** The tool takes only `url` and `prompt` — there is no parameter for `User-Agent`, `Accept`, `Accept-Language`, or `Referer`. The permission specifier is `WebFetch(domain:...)` only ([permissions][permissions]).
- **Cross-host redirects do not auto-follow.** When a fetched URL redirects to a different host, `WebFetch` returns the redirect target in a special format and asks the caller to issue a new `WebFetch` request — protecting against unintended cross-domain fetches without an explicit re-confirmation.
- **GitHub URLs: prefer the `gh` CLI.** The tool's own description explicitly recommends `gh` CLI (`gh pr view`, `gh issue view`, `gh api`) for GitHub content — the API surface returns richer, structured data than HTML scraping.
- **Two caches, not one.** A ~15-minute self-cleaning **content cache** is documented in the tool's Anthropic-authored description (per-URL, holds fetched body). A separate **5-minute per-hostname safety-preflight cache** is documented in [data-usage][data-usage] (caches domain-allow decisions, not content). Don't conflate them when reasoning about cache hits.
- **Default User-Agent is a bot token, not a browser.** `WebFetch` sends `Claude-User (claude-code/<version>; +https://support.anthropic.com/)` — observed as `Claude-User (claude-code/2.1.185; +https://support.anthropic.com/)` (`CC 2.1.185, Codespaces, 2026-06-22`, cross-verified against `postman-echo.com/headers` and `ifconfig.me/ua`). There is **no override**: no `User-Agent` parameter (per the minimal-schema note above) and no documented env var. CC identifies itself honestly (no browser spoofing), which is exactly why anti-bot WAFs reject it.
- **Bot-block behavior is bimodal.** WAF-protected hosts return HTTP `403` to the bot UA; separately, a CC-side denylist refuses some hosts before any request leaves (`Claude Code is unable to fetch from <host>`). A `403` here means *the bot UA was rejected*, not necessarily a dead link — verify in a browser before adding a host to `lychee.toml` excludes.

Observed status codes (`CC 2.1.185, Codespaces, 2026-06-22`):

| Host | Result | Class |
|---|---|---|
| `clarivate.com` | `403 Forbidden` | WAF block |
| `g2.com` | `403 Forbidden` | WAF block (Cloudflare-class) |
| `crunchbase.com` | `403 Forbidden` | WAF block |
| `reddit.com` | `unable to fetch` | CC-side denylist (no request sent) |
| `langtrace.ai` | `404 Not Found` | reachable; page missing |
| `httpbin.org` | `503` | transient upstream outage |
| `marktechpost.com` | `200 OK` | reachable |
| `postman-echo.com`, `ifconfig.me` | `200 OK` | reachable (header echo) |

### Other

| Tool | Permission | Purpose |
|---|---|---|
| `AskUserQuestion` | No | Multiple-choice questions for requirements |
| `Skill` | Yes | Execute a skill in main conversation |

## Permission Model

- **"No"** = tool runs without user approval
- **"Yes"** = requires permission (configurable via `allow`/`ask`/`deny` rules in [settings][settings])
- Permission rules follow `Tool` or `Tool(specifier)` syntax — see [permission rule syntax][permissions]

## Slash Commands (CC 2.1.87, Binary String Extraction)

Commands extracted via `grep -oP` from CLI binary. **Documented** commands are linked; **undocumented** are marked. The `/code-review`, `/review`, `/simplify`, and `/ultrareview` rows below were re-verified against the live docs at CC 2.1.302, 2026-10-18; the `/advisor` row was added from the live docs, 2026-10-26 — none of these five are binary-extracted.

### Documented

| Command | Purpose | Source |
|---|---|---|
| `/advisor` | Set or clear the advisor model (`/advisor off`) that the advisor tool — a server-executed API tool — consults mid-task; see [CC-advisor-tool-analysis.md](CC-advisor-tool-analysis.md) | [advisor-cc][advisor-cc] |
| `/clear` | Clear conversation | [cli-ref][cli-ref] |
| `/code-review` | Review the current diff, a PR, a branch, or a path for correctness bugs; `ultra` escalates to a cloud multi-agent review. Alias: `/review`. Formerly named `/simplify` before v2.1.147. See [details below](#code-review-review-simplify-and-ultrareview) | [commands][commands], [code-review-local][code-review-local] |
| `/commit` | Commit staged changes | [cli-ref][cli-ref] |
| `/config` | Open interactive config panel (`.claude.json` prefs) | [cli-ref][cli-ref] |
| `/exit` | Exit session | [cli-ref][cli-ref] |
| `/fast` | Toggle fast mode | [fast-mode][fast-mode] |
| `/feedback` | Submit feedback | [cli-ref][cli-ref] |
| `/focus` | Toggle the focus view: only the last prompt, a one-line tool-call summary with edit diffstats (also counting subagents launched and collapsing finished background-task notifications), and the final response. Fullscreen rendering only. The choice persists across sessions; the [`viewMode`][settings-ref-viewmode] setting (`"default"`, `"verbose"` or `"focus"`; allowed in any settings file; default unset, so `verbose` and the last `/focus` choice apply) overrides it. From a Remote Control client, `/focus [on\|off]` applies to the current session only (v2.1.281+). The VS Code extension has its own Focus view toggle, independent of `viewMode`. Introducing version not stated in the docs. Verified 2026-10-23; `viewMode` 2026-10-24 | [commands][commands], [settings-ref-viewmode][settings-ref-viewmode] |
| `/goal` | Set a completion condition; Claude keeps working across turns until it is met. Works in interactive, `-p`, and Remote Control modes. Shows elapsed time, turns, and token usage as a live overlay panel. (v2.1.139) | CHANGELOG v2.1.139 |
| `/login` | Authenticate | [cli-ref][cli-ref] |
| `/logout` | Sign out | [cli-ref][cli-ref] |
| `/loop` | Run on recurring interval | [cli-ref][cli-ref] |
| `/mcp` | Manage MCP servers | [mcp-docs][mcp-docs] |
| `/model` | Switch model | [model-config][model-config] |
| `/remote-control`, `/rc` | Enable Remote Control on current session | [remote-control][remote-control] |
| `/remote-env` | Configure default remote environment for `--remote` web sessions | [commands][commands] |
| `/review` | Alias of `/code-review` (CC v2.1.223+). Before v2.1.223 it was a separate, single-pass, read-only review of a GitHub PR by number | [commands][commands], [code-review-local][code-review-local] |
| `/schedule` | Manage scheduled remote agents | [remote-control][remote-control] |
| `/simplify` | Reviews changed code for reuse/simplification/efficiency/abstraction-level cleanup via 4 parallel agents and applies the fixes; does not look for correctness bugs (use `/code-review` for that). Former name of `/code-review` before v2.1.147 | [commands][commands] |
| `/status` | Show session status | [cli-ref][cli-ref] |
| `/ultrareview` | Alias of `/code-review ultra`, once ultrareview is available to the account — a deep, multi-agent review in a cloud sandbox. Research preview. See [details below](#code-review-review-simplify-and-ultrareview) | [commands][commands], [ultrareview][ultrareview] |

#### `/code-review`, `/review`, `/simplify`, and ultrareview

Verified against the live [code-review-local][code-review-local], [ultrareview][ultrareview], and [commands][commands] pages, cross-checked with `claude plugin list` and the Claude Code CHANGELOG (CC 2.1.302, Codespaces, 2026-10-18). For the separate marketplace plugin (`code-review@claude-plugins-official`, namespaced `/code-review:code-review`) and the managed GitHub PR service, see [CC-official-plugins-landscape.md § `/code-review` command and ultrareview][plugins-code-review] — all three are distinct from the bundled command below.

**`/code-review` targets** — with no target, it reviews the branch's commits ahead of its upstream branch plus any uncommitted changes (or against `main`, or the previous commit, when there's no upstream):

| To review | Type |
|---|---|
| Current branch + uncommitted changes (default) | `/code-review` |
| Last 15 commits | `/code-review HEAD~15..HEAD` |
| One branch against another | `/code-review main...my-feature` |
| A single commit (`abc1234`) | `/code-review abc1234^..abc1234` |
| A PR by number | `/code-review 1234` |
| A file or directory path | `/code-review src/auth` |

**Effort and flags**: an [effort level][model-config] (`low` through `max`) trades confidence for coverage; the level typed last is reused across sessions (not for `ultra`, and not remembered from a non-interactive `-p` run). `--fix` applies findings to the working tree; `--comment` posts them as GitHub inline comments or a single GitLab merge-request note (GitLab requires CC v2.1.257+); `--max-findings <n>|all|default` caps the findings count (CC v2.1.288+); `--post` preselects posting an `ultra` GitHub-PR review's findings to the PR (CC v2.1.227+). The review runs as a background subagent by default (foreground with `-p`, with `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1`, or when run again while one is in progress; ran inline before CC v2.1.218).

**Aliases and renames**: `/review` is an alias of `/code-review` since **CC v2.1.223**; before that it was a separate, single-pass, read-only review of a GitHub PR by number (and from v2.1.186–v2.1.201 ran the same multi-agent engine as `/code-review medium`). The command was named **`/simplify`** before **CC v2.1.147**, when it applied fixes by default; `/simplify` still exists today as a separate, narrower command — 4 parallel agents reviewing reuse, simplification, efficiency, and abstraction level, with no correctness-bug check.

**`ultrareview`** (`/code-review ultra`, alias `/ultrareview` once available to the account) is a **research preview**: "Ultrareview is a research preview feature. The feature, pricing, and availability may change based on feedback." It launches a fleet of reviewer agents as a cloud session on Anthropic's infrastructure, with every finding independently reproduced and verified. "A review typically takes 15 to 25 minutes."

- **User-started only**: the command runs only when invoked as `/code-review ultra` — Claude does not start it on its own. A scheduled task never launches the cloud review (schedule `/code-review` without `ultra`). `claude -p '/code-review ultra'` launches the cloud review and exits before the findings arrive, so it does not return findings; the documented CI/script route is the `claude ultrareview` subcommand, which blocks until the review finishes and prints findings to stdout — but only when a human or script invokes it directly: when Claude runs that subcommand itself (e.g. via the Bash tool), Claude Code refuses the whole-repository-fallback case.
- **Targets**: no argument compares the current branch to the repository's default branch (plus uncommitted/staged changes); a branch name, commit id, or tag can replace the default-branch base; a `github.com` PR number (also `#1234`, `PR 1234`, or a pasted URL) reviews that PR instead. The docs document these three target forms plus a free-text note attached to a branch review; **a file or directory path is not among them** (unlike plain `/code-review`, which does support a path target).
- **Diff handling**: refuses an empty diff (names what it compared against and suggests a fix); reviews the whole repository only on a first commit (after an interactive confirmation; refuses untracked files) or when there is no merge base (again gated on interactive confirmation or the `claude ultrareview` subcommand's own consent).
- **Limits**: a branch review defaults to up to 500 changed files and 8,000 changed lines; the exact values can change, and a refusal names the ones in effect.
- **Billing**: bills against usage credits, not plan-included usage. Pro and Max each get three free runs as a one-time, non-refreshing allotment; after that, "typically $5 to $25 in usage credits depending on the size of the change". A run counts once the cloud session starts, even if stopped early or failed.
- **Platform/compliance restrictions**: unavailable on Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry, and to organizations with Zero Data Retention or the HIPAA configuration applied — in those cases `/code-review ultra` runs a local review instead. "Organizations that use customer-managed encryption keys (CMEK) can't run ultrareview." For CMEK, unlike the other four cases, there is no stated automatic local fallback — the docs say to run `/code-review` directly.

### Undocumented (String Extraction)

| Command | Observed Behavior | Notes |
|---|---|---|
| `/settings` | Routes to `update-config` skill (conversational, modifies `settings.json`) | **Not** an alias for `/config`; confirmed CC 2.1.87 |
| `/update-config` | Same skill as `/settings`, direct invocation | Asks "what would you like to configure?" |
| `/bash` | Unknown | String extraction, CC 2.1.87 |
| `/btw` | Side-question during task ([btw-gist][btw-gist]) | String extraction; community-documented |
| `/chrome` | Chrome extension related | String extraction, CC 2.1.87 |
| `/commit-push-pr` | Combined commit+push+PR workflow | String extraction, CC 2.1.87 |
| `/issue` | Create/reference GitHub issue | String extraction, CC 2.1.87 |

`/ultrareview` was listed here as an undocumented string-extraction finding ("Unknown — enhanced review?", CC 2.1.87). It is now documented: see the [Documented](#documented) table and [details below](#code-review-review-simplify-and-ultrareview).

## Configuration Surface (CC 2.1.87)

CC uses **three distinct configuration layers**. This was confirmed by cross-referencing the CLI binary, extension schema, and interactive `/config` panel.

### Layer 1: `.claude.json` — Interactive Preferences

Written by `/config` panel and UI interactions. Located at `~/.claude/.claude.json` or `.claude/.claude.json` per-project.

| Key | Type | `/config` Label | Source |
|---|---|---|---|
| `fastMode` | boolean | Fast mode (Opus 5.5, Opus 5, Opus 4.8 as of 2026-10-26 — see [CC-fast-mode-analysis.md](CC-fast-mode-analysis.md)) | `/config` panel observation; [fast-mode docs](https://code.claude.com/docs/en/fast-mode) |
| `respectGitignore` | boolean | Respect .gitignore in file picker | `/config` panel observation |
| `theme` | string | Theme | `/config` panel observation |
| `editorMode` | string | (not shown) | File observation |
| `diffTool` | string | (not shown) | File observation |
| `fileCheckpointingEnabled` | boolean | Rewind code (checkpoints) | `/config` panel observation |
| `terminalProgressBarEnabled` | boolean | Terminal progress bar | `/config` panel observation |
| `preferredNotifChannel` | string | Notifications | `/config` panel observation |
| `installMethod` | string | (not shown) | File observation |
| `autoInstallIdeExtension` | boolean | (not shown) | File observation |
| `claudeInChromeDefaultEnabled` | boolean | (not shown) | File observation |

**Not documented** in any first-party page. No dedicated reference exists.

### Layer 2: `settings.json` — Declarative Behavior Config

80+ keys for permissions, hooks, plugins, model, env, statusLine, etc. Documented at [settings][settings]. Written by `/settings` (update-config skill) or manually.

Includes `advisorModel`, the persistent default for the advisor tool — a server-executed API tool, not a local setting; see [CC-advisor-tool-analysis.md](CC-advisor-tool-analysis.md).

Cross-ref: [CC-env-vars-reference.md](CC-env-vars-reference.md), [CC-hooks-system-analysis.md](CC-hooks-system-analysis.md)

### Layer 3: `claudeCode.*` — VS Code Extension Settings

13 IDE-only settings in VS Code `settings.json`. Control how the extension **hosts** Claude, not how Claude **behaves**. Documented at [vs-code][vs-code].

| Setting | Purpose |
|---|---|
| `claudeCode.useTerminal` | Terminal vs native UI |
| `claudeCode.autosave` | Auto-save before read/write |
| `claudeCode.preferredLocation` | Default panel location |
| `claudeCode.initialPermissionMode` | Default permission mode |
| `claudeCode.allowDangerouslySkipPermissions` | Bypass mode |
| `claudeCode.environmentVariables` | Env vars for launch |
| `claudeCode.respectGitIgnore` | File picker gitignore |
| `claudeCode.disableLoginPrompt` | Suppress auth prompts |
| `claudeCode.useCtrlEnterToSend` | Send key behavior |
| `claudeCode.enableNewConversationShortcut` | Cmd+N shortcut |
| `claudeCode.hideOnboarding` | Hide onboarding |
| `claudeCode.claudeProcessWrapper` | Custom launcher |
| `claudeCode.usePythonEnvironment` | Python env |

### Overlap Between Layers

| Key | `.claude.json` | `settings.json` | `claudeCode.*` |
|---|---|---|---|
| `fastMode` | Yes | Yes | No |
| `respectGitignore` | Yes | Yes | Yes (`claudeCode.respectGitIgnore`) |

Precedence unclear. Behavior observed: `/config` panel writes to `.claude.json`; `settings.json` keys may override at runtime.

Cross-ref: [CC-binary-architecture.md](CC-binary-architecture.md)

## Internal and Feature-Gated Tools (Leak-Derived)

The following tools appear in the `@anthropic-ai/claude-code@2.1.88` npm sourcemap exposure (2026-03-31) but are not present in the public tool registry. Categorized by [CLAURST][claurst] analysis. **Unverified — Anthropic has not confirmed these tools.**

### Internal-Only Tools (`USER_TYPE === 'ant'`)

| Tool | Purpose | Gate |
|------|---------|------|
| `ConfigTool` | Modify settings programmatically | `ant` user type |
| `TungstenTool` | Advanced features (undocumented) | `ant` user type |
| `SuggestBackgroundPRTool` | Suggest background pull requests | `ant` user type |

### Feature-Gated Tools

| Tool | Purpose | Feature Gate |
|------|---------|-------------|
| `BriefTool` | Upload/summarize files to claude.ai | — |
| `SendMessageTool` | Inter-agent messaging (UDS Inbox) | `COORDINATOR_MODE` |
| `ListPeersTool` | Discover active CC sessions | `COORDINATOR_MODE` |
| `TeamCreateTool` | Create agent team | `tengu_amber_flint` |
| `TeamDeleteTool` | Delete agent team | `tengu_amber_flint` |
| `MonitorTool` | Monitor MCP servers | — |
| `WorkflowTool` | Execute workflow scripts ([analysis](../agents-skills/CC-dynamic-workflows-analysis.md)) | `WORKFLOW_SCRIPTS` |
| `SleepTool` | Async delays | — |
| `SnipTool` | History snippet extraction | `HISTORY_SNIP` |
| `McpAuthTool` | MCP server authentication | — |
| `SyntheticOutputTool` | Structured output via dynamic JSON schemas | — |
| `VerifyPlanExecutionTool` | Verify plan execution | `CLAUDE_CODE_VERIFY_PLAN` |
| `CtxInspectTool` | Context window inspection | `CONTEXT_COLLAPSE` |
| `TerminalCaptureTool` | Terminal panel capture | `TERMINAL_PANEL` |
| `REPLTool` | Interactive VM shell | `--bare` mode |

### Kairos-Exclusive Tools (Unreleased)

| Tool | Purpose | Feature Gate |
|------|---------|-------------|
| `SendUserFile` | Push files to user devices | `KAIROS` |
| `PushNotification` | Send push notifications | `KAIROS` |
| `SubscribePR` | Monitor and review PRs autonomously | `KAIROS` |

### Compile-Time Feature Flags

| Flag | Gates |
|------|-------|
| `PROACTIVE` / `KAIROS` | Always-on assistant mode |
| `KAIROS_BRIEF` | Brief command for concise output |
| `BRIDGE_MODE` | Remote control via claude.ai |
| `DAEMON` | Background daemon mode |
| `VOICE_MODE` | Voice input |
| `WORKFLOW_SCRIPTS` | Workflow automation |
| `COORDINATOR_MODE` | Multi-agent orchestration |
| `TRANSCRIPT_CLASSIFIER` | AFK mode (ML auto-approval) |
| `BUDDY` | Companion pet system |
| `NATIVE_CLIENT_ATTESTATION` | Client authenticity verification |
| `HISTORY_SNIP` | History snipping |
| `EXPERIMENTAL_SKILL_SEARCH` | Skill discovery |

Runtime feature gating uses GrowthBook with `tengu_`-prefixed flags and `getFeatureValue_CACHED_MAY_BE_STALE()` to avoid blocking the main loop.

Cross-ref: [CC-agent-teams-orchestration.md](../agents-skills/CC-agent-teams-orchestration.md) — UDS Inbox and Coordinator Mode; [CC-community-reimplementations-landscape.md](../../cc-community/CC-community-reimplementations-landscape.md) — CLAURST full tool registry source

## Cross-References

- [CC-bash-mode-analysis.md](CC-bash-mode-analysis.md) — Bash tool and `!` mode deep-dive
- [CC-hooks-system-analysis.md](CC-hooks-system-analysis.md) — PreToolUse/PostToolUse hook events
- [CC-env-vars-reference.md](CC-env-vars-reference.md) — `BASH_DEFAULT_TIMEOUT_MS`, `BASH_MAX_OUTPUT_LENGTH`
- [CC-binary-architecture.md](CC-binary-architecture.md) — Binary analysis methodology
- [CC RE landscape](../../cc-community/CC-reverse-engineering-landscape.md) — Community RE tools

## Sources

| Source | Content |
|---|---|
| [CC tools reference][tools-ref] | Authoritative tool list, descriptions, permission requirements |
| [CC CLI reference][cli-ref] | Official slash command documentation |
| [CC settings — permissions][permissions] | Permission rule syntax and tool-specific patterns |
| [CC VS Code docs][vs-code] | Extension settings (`claudeCode.*`) |
| CC 2.1.83, Codespaces, 2026-03-27 | Tool inventory snapshot version |
| CC 2.1.87 CLI binary string extraction, 2026-03-29 | Slash commands, config keys, undocumented commands |
| CC 2.1.87 `/config` panel observation, 2026-03-29 | `.claude.json` key inventory |
| CC 2.1.185, Codespaces, 2026-06-22 | `WebFetch` default User-Agent + bot-block status codes (observed) |
| [ZhangHanDong /btw gist][btw-gist] | `/btw` command analysis |
| [CLAURST README][claurst] | Internal/gated tool registry, feature flags |
| [CC code-review-local docs][code-review-local] | `/code-review` targets, effort levels, flags, `/review`/`/simplify` alias history |
| [CC ultrareview docs][ultrareview] | Ultrareview scope, billing, limits, platform restrictions, research-preview status |
| CC 2.1.302, Codespaces, 2026-10-18 | CLI commands and reference pages re-verified live for this pass; `claude plugin list` and CHANGELOG search cross-checked the `/code-review` plugin and `/review-pr` disposition |
| [CC advisor docs][advisor-cc] | `/advisor` command and `advisorModel` setting (accessed 2026-10-26); see [CC-advisor-tool-analysis.md](CC-advisor-tool-analysis.md) |

[advisor-cc]: https://code.claude.com/docs/en/advisor
[tools-ref]: https://code.claude.com/docs/en/tools-reference
[commands]: https://code.claude.com/docs/en/commands
[cli-ref]: https://code.claude.com/docs/en/cli-reference
[code-review-local]: https://code.claude.com/docs/en/code-review-local
[ultrareview]: https://code.claude.com/docs/en/ultrareview
[plugins-code-review]: ../plugins-ecosystem/CC-official-plugins-landscape.md#code-review-command-and-ultrareview
[settings]: https://code.claude.com/docs/en/settings
[settings-ref-viewmode]: https://code.claude.com/docs/en/settings-reference#viewmode
[permissions]: https://code.claude.com/docs/en/permissions#tool-specific-permission-rules
[data-usage]: https://code.claude.com/docs/en/data-usage
[vs-code]: https://code.claude.com/docs/en/vs-code
[fast-mode]: https://code.claude.com/docs/en/fast-mode
[mcp-docs]: https://code.claude.com/docs/en/mcp
[model-config]: https://code.claude.com/docs/en/model-config
[remote-control]: https://code.claude.com/docs/en/remote-control
[btw-gist]: https://gist.github.com/ZhangHanDong
[claurst]: https://github.com/Kuberwastaken/claurst
