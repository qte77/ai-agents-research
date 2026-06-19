# CC Changelog & Native Sources: New Uncovered Features Detected

## Changelog Monitor Report

Last scanned version: **2.1.168**
New versions detected: **7**

### New Versions Summary

| Version | Features | Covered | Uncovered |
|---------|----------|---------|-----------|
| 2.1.176 | 22 | 2 | 20 |
| 2.1.175 | 1 | 0 | 1 |
| 2.1.174 | 13 | 1 | 12 |
| 2.1.173 | 2 | 0 | 2 |
| 2.1.172 | 30 | 0 | 30 |
| 2.1.170 | 2 | 0 | 2 |
| 2.1.169 | 31 | 0 | 31 |

### Feature Coverage Details

#### v2.1.176

- **[covered]** - Fixed Remote Control connecting from web/mobile silently switching the session's model
  - Covered by: `cc-native/ci-remote/CC-remote-control-analysis.md`, `cc-native/configuration/CC-env-vars-reference.md`
- **[covered]** - Fixed `claude --bg -cn <name>` not seeding the session name
  - Covered by: `cc-native/sessions/CC-session-lifecycle-analysis.md`
- **[UNCOVERED]** - Session titles are now generated in the language of your conversation (set the `language` setting to pin a specific language)
- **[UNCOVERED]** - Added `footerLinksRegexes` setting for regex-matched link badges in the footer row, configurable via user or managed settings
- **[UNCOVERED]** - Improved Bedrock credential caching: credentials from `awsCredentialExport` are now cached until their `Expiration` instead of a fixed 1 hour
- **[UNCOVERED]** - Fixed `availableModels` enforcement: alias model picks can no longer be redirected to a blocked model via `ANTHROPIC_DEFAULT_*_MODEL` environment variables, and `/fast` now refuses to toggle when it would switch to a model outside the allowlist
- **[UNCOVERED]** - Fixed auto mode failing on Fable 5 for organizations without Opus 4.8 enabled — the classifier now falls back to the best available Opus model
- **[UNCOVERED]** - Fixed hook `if` conditions for Read/Edit/Write tool paths: documented patterns like `Edit(src/**)`, `Read(~/.ssh/**)`, and `Read(.env)` now match correctly
- **[UNCOVERED]** - Fixed Linux sandbox failing to start when `.claude/settings.json` is a symlink with an absolute target
- **[UNCOVERED]** - Fixed `/copy` and mouse-selection copy not reaching the system clipboard inside tmux over SSH, and tmux paste buffer not loading on versions older than 3.2
- **[UNCOVERED]** - Fixed Remote Control disconnect notifications showing a bare numeric code instead of a human-readable reason, and connection failures adding a duplicate line to the conversation transcript
- **[UNCOVERED]** - Fixed Remote Control sessions not disconnecting when you sign in to a different account
- **[UNCOVERED]** - Fixed `/cd` and worktree moves leaving the session reporting the previous directory's git branch
- **[UNCOVERED]** - Fixed `claude agents`: pressing back in one window no longer detaches other windows attached to the same session
- **[UNCOVERED]** - Fixed backgrounded sessions showing "Working" forever when `/bg` mid-turn had nothing left to continue
- **[UNCOVERED]** - Fixed background agent search by PR URL: PRs opened during scheduled wakeups or while a job was blocked now appear in `claude agents` search
- **[UNCOVERED]** - Fixed the agents view input showing no text cursor on Windows
- **[UNCOVERED]** - Fixed background sessions to neutralize Windows network paths in persisted state before respawn
- **[UNCOVERED]** - Fixed background-session respawn rejecting malformed resume IDs from corrupted state files
- **[UNCOVERED]** - Fixed the Windows background-service daemon not starting when `~/.claude/daemon` has the ReadOnly attribute set
- **[UNCOVERED]** - Fixed cloud sessions failing with "Could not resolve authentication method" when idle for too long before being claimed
- **[UNCOVERED]** - Background sessions now show clearer guidance when a window left open across an auto-update can't submit a reply, and `claude daemon status` explains version-skew behavior

#### v2.1.175

- **[UNCOVERED]** - Added `enforceAvailableModels` managed setting — when enabled, the `availableModels` allowlist also constrains the Default model (a Default that would resolve to a disallowed model now falls back to the first allowed model), and user or project settings can no longer widen a managed `availableModels` list

#### v2.1.174

- **[covered]** - Fixed Workflow tool `agent()` subagents missing per-agent attribution headers
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-dynamic-workflows-analysis.md`
- **[UNCOVERED]** - Added `wheelScrollAccelerationEnabled` setting to disable mouse-wheel scroll acceleration in fullscreen mode
- **[UNCOVERED]** - Fixed the `/model` picker hiding the model family that Default resolves to — Opus now appears as its own row on Max/Team Premium/Enterprise plans, Sonnet on Pro/Team plans, and Opus on pay-as-you-go API accounts
- **[UNCOVERED]** - Fixed `/model` picker showing a hardcoded Sonnet version label when `ANTHROPIC_DEFAULT_SONNET_MODEL` pins a different Sonnet
- **[UNCOVERED]** - Fixed the "Fable 5 is now consuming usage credits" banner incorrectly showing for enterprise accounts with usage-based billing
- **[UNCOVERED]** - Fixed Bedrock GovCloud regions (`us-gov-*`) deriving the wrong inference profile prefix (`global` instead of `us-gov`), causing 400 errors on derived model IDs
- **[UNCOVERED]** - Fixed background sessions inheriting another session's `ANTHROPIC_*` provider env (gateway URL, custom headers, `/model` aliases) from the shell that started the background daemon
- **[UNCOVERED]** - Fixed a 1-2 second pause when exiting Claude Code shortly after a shell command was interrupted or killed on macOS and Linux
- **[UNCOVERED]** - Fixed git commit co-author attribution showing an incorrect model name for some models
- **[UNCOVERED]** - Fixed the `/advisor` dialog pre-selecting a saved advisor model that is blocked by the `availableModels` allowlist
- **[UNCOVERED]** - Fixed skill hot-reload re-sending the entire skill listing when a single skill changed; only changed skills are now re-announced
- **[UNCOVERED]** - [VSCode] Added usage attribution to the Account & usage dialog (`/usage`) showing cache misses, long context, subagents, and per-skill/agent/plugin/MCP breakdowns over the last 24h or 7d
- **[UNCOVERED]** - Fixed pre-warmed background workers failing with "Could not resolve authentication method" when claimed after sitting idle

#### v2.1.173

- **[UNCOVERED]** - Fixed Fable 5 model names with a `[1m]` suffix not being normalized — Fable 5 includes 1M context by default, so the suffix is now stripped automatically
- **[UNCOVERED]** - Fixed a spurious "sandbox dependencies missing" startup warning on Windows when sandbox was enabled in settings

#### v2.1.172

- **[UNCOVERED]** - Sub-agents can now spawn their own sub-agents (up to 5 levels deep)
- **[UNCOVERED]** - Amazon Bedrock now reads the AWS region from `~/.aws` config files when `AWS_REGION` isn't set, matching AWS SDK precedence; `/status` shows where the region came from
- **[UNCOVERED]** - Added a search bar when browsing a marketplace's plugins in `/plugin`
- **[UNCOVERED]** - Added `model` attribute to the `claude_code.lines_of_code.count` OTEL metric
- **[UNCOVERED]** - Fixed sessions using 1M context without usage credits getting permanently stuck — the session now automatically compacts back under the standard context limit
- **[UNCOVERED]** - Fixed a repeating "an image in the conversation could not be processed and was removed" error when the conversation contained multiple images
- **[UNCOVERED]** - Fixed the agents view keeping a session under Working with a busy spinner for up to 30 seconds after the worker replied
- **[UNCOVERED]** - Fixed background agents potentially reading another directory's project settings (`.mcp.json` approvals, trust) when dispatched onto a pre-warmed worker
- **[UNCOVERED]** - Fixed background-session attach failing with EAUTH for sessions started on an older version after the daemon auto-updated
- **[UNCOVERED]** - Fixed a background sub-agent staying stuck as "active" in the agent panel after a nested agent it spawned was stopped
- **[UNCOVERED]** - Fixed `/model` suggestions in the `claude agents` dispatch input rendering with a misleading slash prefix and showing models disabled for your org
- **[UNCOVERED]** - Fixed `availableModels` restrictions not being applied to subagent model overrides, the agent dispatch model picker, and the advisor model
- **[UNCOVERED]** - Fixed `availableModels` allowlists hiding the `/model` picker's Opus and Sonnet 1M rows when entries use version-specific IDs like `claude-opus-4-8`
- **[UNCOVERED]** - Fixed the `/model` picker on Bedrock offering models the provider doesn't serve — selecting one silently switched the session model and lit the selection marker on multiple rows
- **[UNCOVERED]** - Fixed model IDs getting a doubled 1M-context suffix (e.g. `[1M][1m]`) when `ANTHROPIC_DEFAULT_OPUS_MODEL` already includes one
- **[UNCOVERED]** - Fixed `opusplan` model setting not shipping with 1M context in plan mode for entitled users; the `opusplan[1m]` workaround now also correctly switches to Opus in plan mode
- **[UNCOVERED]** - Fixed `WebFetch(domain:*.example.com)` wildcard domain rules never matching subdomains in allow, deny, and ask position, and file permission rules with mid-pattern wildcards (e.g. `Read(secrets-*/config.json)`) being rejected at startup
- **[UNCOVERED]** - Fixed up-arrow prompt history showing the main agent's prompts while a subagent's chat tab is open
- **[UNCOVERED]** - Fixed memory recall not finding mounted team memory stores (`CLAUDE_MEMORY_STORES`) in remote sessions
- **[UNCOVERED]** - Fixed workflow validation rejecting scripts whose prompt strings or comments merely mention `Date.now()`/`Math.random()`
- **[UNCOVERED]** - Disable mouse tracking on Windows consoles that don't fully support it
- **[UNCOVERED]** - Fixed the `/plugin` marketplace list losing its cursor after backing out of a long plugin list, and Esc from the plugin browser returning to the wrong tab
- **[UNCOVERED]** - Improved performance in long conversations by removing redundant message normalization and avoiding full message-history transforms when streaming tool-use state is unchanged
- **[UNCOVERED]** - Reduced idle CPU usage: `/goal` status chip no longer re-renders the terminal at 5 Hz while idle, and fewer UI re-renders while subagents run in parallel
- **[UNCOVERED]** - Improved Claude in Chrome tool loading: browser tools now load in a single batched call instead of one per tool
- **[UNCOVERED]** - Improved the non-interactive Usage Policy refusal message to suggest starting a new session or changing your model
- **[UNCOVERED]** - `/code-review` now keeps the `ultra` option visible when you're not signed in to claude.ai, with an explanation that the cloud review requires a claude.ai account
- **[UNCOVERED]** - Shortened the Remote Control footer indicator to "/rc active" and hid it on narrow terminals
- **[UNCOVERED]** - Stopped promoting `/loop` in remote sessions, where pending loops don't keep the container alive
- **[UNCOVERED]** - [VSCode] Fixed PowerShell tool calls rendering as raw JSON instead of a proper command display and permission dialog, and stripped ANSI escape codes from displayed shell output

#### v2.1.170

- **[UNCOVERED]** - Introducing Claude Fable 5: a Mythos-class model that we’ve made safe for general use. Fable’s capabilities exceed those of any model we’ve ever made generally available. Update to version 2.1.170 for access. https://www.anthropic.com/news/claude-fable-5-mythos-5
- **[UNCOVERED]** - Fixed sessions not saving transcripts (and not appearing in --resume) when launched from the VS Code integrated terminal or any shell that inherited Claude Code environment variables.

#### v2.1.169

- **[UNCOVERED]** - Self-hosted runner: added a `post-session` lifecycle hook that runs after the session ends and before the workspace is deleted, so you can snapshot uncommitted work or export logs; also made the child-process SIGTERM→SIGKILL window configurable (default unchanged at 5s)
- **[UNCOVERED]** - Added `--safe-mode` flag (and `CLAUDE_CODE_SAFE_MODE`) to start Claude Code with all customizations (CLAUDE.md, plugins, skills, hooks, MCP servers) disabled for troubleshooting
- **[UNCOVERED]** - Added `/cd` command to move a session to a new working directory without breaking the prompt cache mid-session
- **[UNCOVERED]** - Added a `disableBundledSkills` setting and `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS` environment variable to hide bundled skills, workflows, and built-in slash commands from the model
- **[UNCOVERED]** - Fixed Up/Down arrows jumping to command history past the wrapped rows of a long input line — they now move through each visual row first, and history recall enters at the near edge
- **[UNCOVERED]** - Fixed enterprise managed MCP policies (`allowedMcpServers`/`deniedMcpServers`) not being enforced on reconnect, IDE-typed configs, `--mcp-config` servers during the first session after install, or before remote settings loaded; also fixed slow cold starts for orgs without remote settings
- **[UNCOVERED]** - Fixed a ~30-50ms UI stall at the start of each turn for macOS users logged in with claude.ai credentials
- **[UNCOVERED]** - Fixed `claude -p` being slow or appearing to hang on Windows while waiting for the slash-command/skill scan (regression in 2.1.161)
- **[UNCOVERED]** - Fixed Remote Control getting stuck on "reconnecting" after resuming a session when an OAuth token refresh happened at the same time
- **[UNCOVERED]** - Fixed Git Credential Manager's "Connect to GitHub" popup appearing on Windows at startup when background git commands ran without cached credentials
- **[UNCOVERED]** - Fixed footer hints (e.g. "esc to interrupt") not showing for users with a custom statusline
- **[UNCOVERED]** - Fixed stale permission and dialog prompts reappearing every time you reattached to a remote session whose worker had died while waiting on them
- **[UNCOVERED]** - Fixed `claude agents --json` omitting blocked and just-dispatched background sessions; added `--all` to include completed sessions, plus new `id` and `state` fields
- **[UNCOVERED]** - Fixed agents view leaving a stale/garbled frame after navigating back from an agent on WSL in Windows Terminal
- **[UNCOVERED]** - Fixed background agents ignoring project-level settings `env` values (e.g. `ANTHROPIC_MODEL`) when dispatched onto a pre-warmed worker
- **[UNCOVERED]** - Fixed MCPB plugin cache being spuriously invalidated on Windows, causing unnecessary re-extraction
- **[UNCOVERED]** - Fixed plugin `.in_use` PID lock files accumulating without bound; stale markers from crashed sessions are now swept once per day
- **[UNCOVERED]** - Fixed untrusted project settings being able to set OTEL client-certificate paths without trust confirmation
- **[UNCOVERED]** - `/workflows` now opens immediately even while a turn is in progress
- **[UNCOVERED]** - Improved `TaskCreate` reliability: malformed inputs are repaired automatically and validation errors for unloaded tools include the schema
- **[UNCOVERED]** - Improved the error message shown when your organization has disabled API key authentication, with guidance based on where the active API key comes from
- **[UNCOVERED]** - Reduced CPU usage while responses stream and during spinner animations
- **[UNCOVERED]** - Restored a default 5-minute idle timeout on Vertex/Foundry so a stalled stream aborts instead of hanging indefinitely; set `API_FORCE_IDLE_TIMEOUT=0` to opt out
- **[UNCOVERED]** - Remote-managed settings with an invalid entry now apply their remaining valid policies and surface the validation error, instead of silently dropping the whole payload
- **[UNCOVERED]** - Background sessions now preserve `--ide`, `--chrome`, `--bare`, `--remote-control`, and other flags across retire→wake, and respawn state validation was hardened
- **[UNCOVERED]** - Background sessions are now told that shared-checkout edits are blocked until they enter a worktree, avoiding a wasted rejected edit before `EnterWorktree`
- **[UNCOVERED]** - The "CLAUDE.md is too long" warning threshold now scales with the model's context window
- **[UNCOVERED]** - Auto-updater on Windows now stops retrying within a session once `claude.exe` is held by another process
- **[UNCOVERED]** - Improved color contrast for skill tags in the slash-command menu
- **[UNCOVERED]** - Promo credit claims for Apple/Google-billed subscribers without a payment method now explain where to add one
- **[UNCOVERED]** - Added a tip suggesting `claude agents` when running multiple concurrent sessions

---
_Generated by `.github/scripts/changelog-compare.py`_
## Native Sources Monitor Report

Sources checked: **3**

### anthropic-blog

- Source: Anthropic Blog — announcements and product updates
- Entries fetched: 12
- New uncovered: 1

| Entry | Section | Description |
|-------|---------|-------------|
| Jun 12, 2026AnnouncementsTCS and Anthropic partner to bring  | Anthropic Blog | Jun 12, 2026AnnouncementsTCS and Anthropic partner to bring Claude to regulated  |

### cc-issues-enhancement

- Source: CC GitHub Issues labeled 'enhancement'
- Entries fetched: 300
- New uncovered: 2

| Entry | Section | Description |
|-------|---------|-------------|
| Comandos com model: haiku no frontmatter não forçam execução | GitHub Issues (enhancement) | ## Descrição do problema Comandos definidos com `model: haiku` no frontmatter YA |
| [Feature Request] Optimize token consumption and response sp | GitHub Issues (enhancement) | **Bug Description** EXPERIANCE SUPER JUSTE LA VITESSE ET LA CONSOMATION DE TOKEN |

### cc-discussions-feature-request

- Source: CC GitHub Discussions in feature-request category
- Entries fetched: 0
- New uncovered: 0

---
Total new uncovered entries: **3**

_Generated by `.github/scripts/native-sources-monitor.py`_
