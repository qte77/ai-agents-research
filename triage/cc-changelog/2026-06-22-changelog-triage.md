# CC Changelog & Native Sources: New Uncovered Features Detected

## Changelog Monitor Report

Last scanned version: **2.1.176**
New versions detected: **5**

### New Versions Summary

| Version | Features | Covered | Uncovered |
|---------|----------|---------|-----------|
| 2.1.185 | 1 | 0 | 1 |
| 2.1.183 | 17 | 0 | 17 |
| 2.1.181 | 39 | 1 | 38 |
| 2.1.179 | 9 | 1 | 8 |
| 2.1.178 | 24 | 0 | 24 |

### Feature Coverage Details

#### v2.1.185

- **[UNCOVERED]** - The stream-stall hint now reads "Waiting for API response · will retry in …" instead of "No response from API · Retrying in …", and triggers after 20s of silence instead of 10s

#### v2.1.183

- **[UNCOVERED]** - Improved auto mode safety: destructive git commands (`git reset --hard`, `git checkout -- .`, `git clean -fd`, `git stash drop`) are now blocked when you didn't ask to discard local work, `git commit --amend` is blocked when the commit wasn't made by the agent this session, and `terraform destroy`/`pulumi destroy`/`cdk destroy` are blocked unless you asked for the specific stack
- **[UNCOVERED]** - Added a warning when the requested model is deprecated or automatically updated to a newer model, shown on stderr in print mode (`-p`) and now also covering models set in agent frontmatter
- **[UNCOVERED]** - Added `attribution.sessionUrl` setting to omit the claude.ai session link from commits and PRs in web and Remote Control sessions
- **[UNCOVERED]** - Added `/config --help` to list all available shorthand keys for `/config key=value`
- **[UNCOVERED]** - Changed `/config` toggle behavior: Enter and Space both change the selected setting, and Esc now saves and closes instead of reverting
- **[UNCOVERED]** - Removed the startup "setup issues" line under the logo — run `/doctor` to see configuration issues or use `--debug`
- **[UNCOVERED]** - Fixed `thinking.disabled.display: Extra inputs are not permitted` 400 errors on subagent spawns and session-title generation for affected configurations
- **[UNCOVERED]** - Fixed WebSearch returning empty results in subagents
- **[UNCOVERED]** - Fixed the terminal cursor being stranded above the prompt after navigating history in vim mode with the native cursor enabled
- **[UNCOVERED]** - Fixed fullscreen TUI corruption (statusline mid-screen, duplicated spinner rows, merged text) in Windows Terminal under heavy nested-subagent load
- **[UNCOVERED]** - Fixed turns silently completing with no visible output when the model returned only a thinking block; Claude now re-prompts once
- **[UNCOVERED]** - Fixed user-level skills appearing multiple times in slash-command autocomplete when multiple plugins are enabled
- **[UNCOVERED]** - Fixed MCP servers requiring authentication exposing auth-stub tools to the model in headless/SDK mode
- **[UNCOVERED]** - Fixed tmux teammate panes failing to launch when the shell has slow rc-file initialization, and keystrokes typed during agent spawn leaking into the new tmux pane instead of the leader prompt
- **[UNCOVERED]** - Fixed background tasks started by a teammate being killed when the teammate finishes a turn
- **[UNCOVERED]** - Fixed scheduled task and webhook trigger deliveries being treated as keyboard input; they now classify as task notifications and can no longer approve a pending action or set the session title in auto mode
- **[UNCOVERED]** - Fixed focus mode showing "Ran N PostToolUse hooks" timing lines under each response

#### v2.1.181

- **[covered]** - Added `CLAUDE_CLIENT_PRESENCE_FILE` environment variable: point it at a marker file to suppress mobile push notifications while you're at the machine
  - Covered by: `cc-native/ci-remote/CC-remote-control-analysis.md`
- **[UNCOVERED]** - Added `/config key=value` syntax to set any setting from the prompt (e.g. `/config thinking=false`) — works in interactive, `-p`, and Remote Control
- **[UNCOVERED]** - Added `sandbox.allowAppleEvents` opt-in setting that lets sandboxed commands send Apple Events on macOS
- **[UNCOVERED]** - Upgraded the bundled Bun runtime to 1.4
- **[UNCOVERED]** - Improved streaming of long paragraphs: text now appears line-by-line instead of waiting for the first line break
- **[UNCOVERED]** - Improved auto-retry: API connection drops mid-thinking now automatically retry instead of showing "Connection closed while thinking"
- **[UNCOVERED]** - Improved the subagent panel: idle subagents auto-hide after 30s, the list caps at 5 rows with scroll hints, and keyboard hints now show in the footer
- **[UNCOVERED]** - Improved the MCP OAuth browser page to match Claude Code's visual style and auto-close on success
- **[UNCOVERED]** - Changed fullscreen mode URL opening to require Cmd+click (macOS) / Ctrl+click, matching native terminal behavior
- **[UNCOVERED]** - Changed the `Improved N memories` line to no longer list individual files outside verbose mode
- **[UNCOVERED]** - Fixed prompt caching not reading on custom `ANTHROPIC_BASE_URL` and on Foundry due to a per-request attestation token changing every turn
- **[UNCOVERED]** - Fixed Write/Edit producing 0-byte or truncated files on network drives and cloud-synced folders
- **[UNCOVERED]** - Fixed `open`, `osascript`, and browser-based auth flows failing with error -600 on macOS by adding the Apple Events entitlement
- **[UNCOVERED]** - Fixed a startup regression (~120ms per launch in fresh environments, introduced in 2.1.169): the first prompt no longer waits for the managed-settings fetch when no MCP servers are configured
- **[UNCOVERED]** - Fixed startup blocking with a blank terminal for up to 15 seconds when the account settings fetch is slow on a degraded network
- **[UNCOVERED]** - Fixed startup crash (`TypeError: Cannot read properties of null`) when `.claude.json` contains corrupted null project entries
- **[UNCOVERED]** - Fixed macOS TUI freezing at session start (Ctrl+C unresponsive) when Spotlight is busy reindexing
- **[UNCOVERED]** - Fixed long-running idle sessions losing their history when another Claude Code process ran the 30-day transcript cleanup
- **[UNCOVERED]** - Fixed foreground subagents spawning unbounded nested chains; they now respect the same 5-level depth limit as background subagents
- **[UNCOVERED]** - Fixed `/recap` and conversation forks using the previous model immediately after a model switch
- **[UNCOVERED]** - Fixed subagent "Thinking" duration showing the parent agent's elapsed time instead of the subagent's own
- **[UNCOVERED]** - Fixed subagents blocked on a nested agent showing a ticking elapsed time instead of "waiting" in the agent panel
- **[UNCOVERED]** - Fixed the API retry indicator ("Retrying in 0s · attempt N/10") staying on screen after the retry succeeded
- **[UNCOVERED]** - Fixed AWS `awsCredentialExport` credentials with a short remaining lifetime causing credential refreshes every minute, and now accepts the JSON shape from `aws configure export-credentials`
- **[UNCOVERED]** - Fixed `claude mcp get`/`list` showing `✓ Connected` when tools/list fails; they now show `! Connected · tools fetch failed` with the error detail
- **[UNCOVERED]** - Fixed `/remote-control` leaving a stale "connecting…" line; it now confirms in the transcript once connected
- **[UNCOVERED]** - Fixed ExitWorktree refusing to remove a clean worktree with "Could not verify worktree state" when bare `git` cannot be resolved on Windows
- **[UNCOVERED]** - Fixed settings changes (such as `/effort` or `/model`) failing with ENOENT when `~/.claude/settings.json` is a relative symlink under a symlinked `~/.claude`
- **[UNCOVERED]** - Fixed IDE selection line numbers in context reminders being off by one (IntelliJ and VS Code)
- **[UNCOVERED]** - Fixed Ctrl+C in fullscreen after a native terminal selection (modifier+drag) overwriting the clipboard with the app's prior selection
- **[UNCOVERED]** - Fixed Ctrl+V showing "No image found in clipboard" instead of pasting when the clipboard contains text
- **[UNCOVERED]** - Fixed agent creation failing with "EEXIST: file already exists" when the agents directory already exists (Windows/OneDrive)
- **[UNCOVERED]** - Fixed AskUserQuestion preview content being cut off at the dialog edge instead of word-wrapping
- **[UNCOVERED]** - Fixed AskUserQuestion multi-select questions silently dropping a typed "Other" free-text answer when submitting
- **[UNCOVERED]** - Fixed `/stats` "Most active day" and daily token chart dates showing one day early in UTC-negative timezones
- **[UNCOVERED]** - Fixed `/copy` and copy-on-select on Linux not detecting a clipboard utility installed after Claude Code started
- **[UNCOVERED]** - Fixed tab-indented code rendering with incorrect indentation in the Write (create-file) preview
- **[UNCOVERED]** - Fixed user prompts queued mid-turn not showing a full-width background highlight in the transcript
- **[UNCOVERED]** - Fixed the activity spinner's pulse dwelling on the wrong glyph size in Ghostty

#### v2.1.179

- **[covered]** - Improved plugin loading performance in remote sessions
  - Covered by: `cc-native/configuration/CC-env-vars-reference.md`
- **[UNCOVERED]** - Fixed mid-stream connection drops: partial responses are now preserved instead of showing a raw error, and the spinner no longer gets stuck at "running tool"
- **[UNCOVERED]** - Fixed mouse-wheel scrolling in WSL2 under Windows Terminal and VS Code (regression in 2.1.172)
- **[UNCOVERED]** - Fixed a sandbox `denyRead`/`allowRead` glob over a large directory tree making the Bash tool description enormous and the session unusable on Linux
- **[UNCOVERED]** - Fixed the feedback survey capturing a single-digit reply as a session rating immediately after a turn completes
- **[UNCOVERED]** - Fixed the welcome screen stacking multiple promotional banners — at most one promo now shows per session
- **[UNCOVERED]** - Fixed Ctrl+O not showing the subagent's transcript when viewing a subagent
- **[UNCOVERED]** - Fixed clicking the prompt input not returning focus from the subagent/footer panel
- **[UNCOVERED]** - Fixed remote session background tasks appearing stuck as "still running" between turns

#### v2.1.178

- **[UNCOVERED]** - Agent teams: removed the `TeamCreate` and `TeamDelete` tools. With `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` set, every session now has one implicit team — spawn teammates directly with the Agent tool's `name` parameter, no setup step needed. The `team_name` parameter on the Agent tool is still accepted but ignored.
- **[UNCOVERED]** - Added `Tool(param:value)` syntax for permission rules to match a tool's input parameters (with `*` wildcard), e.g. `Agent(model:opus)` to block Opus subagents
- **[UNCOVERED]** - Skills in nested `.claude/skills` directories now load when working on files there; on a name clash, the nested skill appears as `<dir>:<name>` so both stay available
- **[UNCOVERED]** - Nested `.claude/` directories: the agent, workflow, and output-style closest to the working directory now wins when names collide; project-scope workflow saves now target the closest existing `.claude/workflows/`
- **[UNCOVERED]** - Improved auto mode: subagent spawns are now evaluated by the classifier before launch, closing a gap where a subagent could request a blocked action without review
- **[UNCOVERED]** - Improved `/doctor` with consistent flat tree layout across all sections, clearer section status icons, and highlighted command names
- **[UNCOVERED]** - Improved the skill listing truncation warning to show how many skill descriptions are affected
- **[UNCOVERED]** - Changed the workflow prompt keyword to use a purple shimmer highlight and trigger only on explicit phrases like "run a workflow" or "workflow:", not on any mention of the word
- **[UNCOVERED]** - Improved Remote Control error messages: connection failures now show a persistent red "/rc failed" indicator in the footer, and the "not yet enabled" error now explains whether it's a gate, a check failure, stale entitlement, or org policy
- **[UNCOVERED]** - `/bug` now requires a description before submitting, and no longer uses model-refusal text as the GitHub issue title
- **[UNCOVERED]** - Fixed a crash (out-of-memory) when the CLI inherits a stale websocket/OAuth file-descriptor environment variable from a parent process
- **[UNCOVERED]** - Fixed Claude in Chrome silently failing to connect when the OAuth token belongs to a different account than the Claude Code login
- **[UNCOVERED]** - Fixed nested `.claude/skills` skills with directory-qualified names being blocked by permission prompts in non-interactive runs
- **[UNCOVERED]** - Fixed several subagent issues: viewing a subagent's transcript now shows tool results and live progress, messages sent while it finishes its turn are no longer dropped, and backgrounding a running subagent (ctrl+b) no longer restarts it from scratch
- **[UNCOVERED]** - Fixed `claude agents` workers failing with `401 Invalid bearer token` when the daemon was started from a shell with a custom API gateway via `ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN`
- **[UNCOVERED]** - Fixed compaction not honoring `--fallback-model`: compaction now falls back to the configured fallback model chain on overload or model-availability errors
- **[UNCOVERED]** - Fixed model requests continuing to fail with auth errors after credentials were refreshed outside the session, due to a stale cached request configuration
- **[UNCOVERED]** - Fixed background sessions created with `/bg` or `←←` after a turn finished showing "Working" forever in the agents list
- **[UNCOVERED]** - Fixed Linux sandbox failing to start when `.claude/skills` or `.claude/hooks` is a symlink
- **[UNCOVERED]** - Fixed `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1` preventing fresh marketplace installs from cloning
- **[UNCOVERED]** - Fixed MCP server-level specs (`mcp__server`, `mcp__server__*`, `mcp__*`) in subagent `disallowedTools` being silently ignored
- **[UNCOVERED]** - Fixed vim mode undo: `u` now steps through NORMAL/VISUAL-mode commands one at a time instead of merging commands in quick succession into a single undo step
- **[UNCOVERED]** - Fixed statusline links with custom URI schemes (e.g. `vscode://`) not opening when clicked in `claude agents`
- **[UNCOVERED]** - [VSCode] Fixed pressing Esc to dismiss a CJK IME candidate window canceling the running Claude task

---
_Generated by `.github/scripts/changelog-compare.py`_
## Native Sources Monitor Report

Sources checked: **3**

### anthropic-blog

- Source: Anthropic Blog — announcements and product updates
- Entries fetched: 12
- New uncovered: 0

### cc-issues-enhancement

- Source: CC GitHub Issues labeled 'enhancement'
- Entries fetched: 300
- New uncovered: 1

| Entry | Section | Description |
|-------|---------|-------------|
| [Feature Request] Add VAD auto-send on silence for native vo | GitHub Issues (enhancement) | **Bug Description** Demande de fonctionnalité : envoi automatique sur silence (V |

### cc-discussions-feature-request

- Source: CC GitHub Discussions in feature-request category
- Entries fetched: 0
- New uncovered: 0

---
Total new uncovered entries: **1**

_Generated by `.github/scripts/native-sources-monitor.py`_
