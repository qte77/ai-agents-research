# CC Changelog & Native Sources: New Uncovered Features Detected

## Changelog Monitor Report

Last scanned version: **2.1.185**
New versions detected: **18**

### New Versions Summary

| Version | Features | Covered | Uncovered |
|---------|----------|---------|-----------|
| 2.1.207 | 24 | 1 | 23 |
| 2.1.206 | 27 | 0 | 27 |
| 2.1.205 | 23 | 0 | 23 |
| 2.1.204 | 1 | 0 | 1 |
| 2.1.203 | 37 | 0 | 37 |
| 2.1.202 | 18 | 0 | 18 |
| 2.1.201 | 1 | 0 | 1 |
| 2.1.200 | 17 | 0 | 17 |
| 2.1.199 | 24 | 0 | 24 |
| 2.1.198 | 33 | 0 | 33 |
| 2.1.197 | 1 | 0 | 1 |
| 2.1.196 | 27 | 0 | 27 |
| 2.1.195 | 12 | 0 | 12 |
| 2.1.193 | 15 | 0 | 15 |
| 2.1.191 | 20 | 0 | 20 |
| 2.1.190 | 1 | 0 | 1 |
| 2.1.187 | 21 | 0 | 21 |
| 2.1.186 | 33 | 0 | 33 |

### Feature Coverage Details

#### v2.1.207

- **[covered]** - Changed Bedrock, Vertex, and Claude Platform on AWS to default to Claude Opus 4.8
  - Covered by: `cc-native/configuration/CC-model-provider-configuration.md`
- **[UNCOVERED]** - Auto mode is now available without `CLAUDE_CODE_ENABLE_AUTO_MODE` opt-in on Bedrock, Vertex AI, and Foundry; disable via `disableAutoMode` in settings
- **[UNCOVERED]** - Fixed the terminal freezing and keystrokes lagging while streaming responses containing very long lists, tables, paragraphs, or code blocks
- **[UNCOVERED]** - Fixed remote managed settings from a non-interactive run (`claude -p`, the SDK) being permanently recorded as consented without ever showing the security consent dialog
- **[UNCOVERED]** - Fixed spurious prompt-injection warnings triggered by benign system-generated conversation updates
- **[UNCOVERED]** - Fixed the auto-updater overwriting a custom launcher script or symlink at `~/.local/bin/claude` on every release; `/doctor` now reports an externally managed launcher
- **[UNCOVERED]** - Fixed compound commands with `cd` prompting for permission when the only output redirect was to `/dev/null`
- **[UNCOVERED]** - Fixed the transcript jumping above the start of the answer when a response finishes streaming
- **[UNCOVERED]** - Fixed `extensions.worktreeConfig` being left in the repo's `.git/config` (breaking go-git tools like `tea`) after the last `worktree.sparsePaths` worktree was removed
- **[UNCOVERED]** - Fixed malformed bracket patterns in rules globs, skill paths, `.ignore`, and `.worktreeinclude` breaking file reads, file suggestions, and worktree creation
- **[UNCOVERED]** - Fixed a crash loop in agent teams where a malformed teammate mailbox message caused repeated errors every second until the mailbox file was manually deleted
- **[UNCOVERED]** - Fixed background sessions auto-named by accepting a plan not showing that name on their agent-view row
- **[UNCOVERED]** - Fixed background sessions that entered a git worktree resuming blank after a cold reopen from the agent list
- **[UNCOVERED]** - Fixed Remote Control task status updates being lost when the connection recovered from a network interruption or credential refresh
- **[UNCOVERED]** - Fixed Remote Control sessions hosted by the desktop app not showing background agent and workflow progress on mobile and web
- **[UNCOVERED]** - Fixed Deep research runs labeling every Fetch-phase agent "unknown" — chips now show the source hostname
- **[UNCOVERED]** - Fixed Bedrock repeatedly requesting fresh AWS SSO credentials from IAM Identity Center on every API request
- **[UNCOVERED]** - Improved agent view: pasting the same text again now expands the collapsed `[Pasted text #N]` placeholder instead of adding a second one
- **[UNCOVERED]** - Improved agent view: blocked session peeks now lead with the question and show a worded staleness clock (`waiting 3m`) instead of the same timestamp twice
- **[UNCOVERED]** - Changed auto mode to no longer read `autoMode` from `.claude/settings.local.json` (repo-resident); use `~/.claude/settings.json` instead
- **[UNCOVERED]** - Fixed an indefinite hang on Windows when AWS credential resolution stalls (e.g. a stuck `credential_process`): the 60-second stall guard now fires instead of waiting forever.
- **[UNCOVERED]** - Plugin hooks/monitors/MCP headersHelper: `${user_config.*}` in shell-form commands is now rejected (shell-injection fix). Hooks: use exec form (`args` array) or `$CLAUDE_PLUGIN_OPTION_<KEY>`; monitors and headersHelper: read the value inside the script (config file or the server's `env` block).
- **[UNCOVERED]** - Plugin option values (`pluginConfigs`) are no longer read from project-level `.claude/settings.json`; only user, `--settings`, and managed settings are honored
- **[UNCOVERED]** - Fixed `/usage-credits` amount inputs silently stripping malformed values (e.g. a pasted timestamp) to digits; malformed amounts are now rejected with an error, and amounts over $1,000 require a typed confirmation

#### v2.1.206

- **[UNCOVERED]** - Added directory path suggestions to `/cd`, matching `/add-dir` behavior
- **[UNCOVERED]** - Added a `/doctor` check that proposes trimming checked-in `CLAUDE.md` files by cutting content Claude could derive from the codebase
- **[UNCOVERED]** - `/commit-push-pr` now auto-allows `git push` to the repo's configured push remote (`remote.pushDefault`, or the sole remote when only one is configured) in addition to `origin`
- **[UNCOVERED]** - Gateway: `/login` now supports Anthropic-operated public gateway endpoints
- **[UNCOVERED]** - `EnterWorktree` now asks for confirmation before entering a git worktree outside the project's `.claude/worktrees/` directory
- **[UNCOVERED]** - Background agents now upgrade to a new version in the background right after a Claude Code update, instead of paying a slow stale-session upgrade when you attach
- **[UNCOVERED]** - Fixed an expired login failing every model with a misleading "There's an issue with the selected model" error instead of prompting to run `/login`
- **[UNCOVERED]** - Fixed `claude --resume` and `--continue` not responding to keyboard input on startup
- **[UNCOVERED]** - Fixed MCP servers configured via `--mcp-config` or `.mcp.json` ignoring a per-server `request_timeout_ms`, which caused long-running MCP tool calls to time out at the 60s default in fresh sessions
- **[UNCOVERED]** - Fixed `CLAUDE_CODE_EXTRA_BODY` being silently ignored by `claude agents` / `--bg` background workers; the shell-exported override now follows the dispatching session
- **[UNCOVERED]** - Fixed OAuth MCP servers requiring manual re-authentication after a single failed token refresh
- **[UNCOVERED]** - Fixed `--permission-prompt-tool` pointing at an MCP server crashing with "MCP tool not found" on cold start before the server finishes connecting
- **[UNCOVERED]** - Fixed `/model` picker rows printing a price for a different model than the row named, and stopped quoting first-party list prices on providers that don't bill them
- **[UNCOVERED]** - Fixed server-provided model rows being misplaced in the `/model` picker when an entitlement or allowlist restriction drops the row they were positioned against
- **[UNCOVERED]** - Fixed desktop sessions getting stuck showing "running" after a slash command was sent mid-turn
- **[UNCOVERED]** - Fixed keyboard input being ignored in the agents view when a setup prompt appeared before a bare `claude --resume` on Windows
- **[UNCOVERED]** - Fixed `claude rm` leaving the removed job in the daemon roster, causing the row to reappear in `claude agents`
- **[UNCOVERED]** - Fixed `/remote-control` showing "Unknown command" when logged out — it now explains how to sign in
- **[UNCOVERED]** - Fixed left arrow not stepping back out of a phase or agent in the workflow detail view
- **[UNCOVERED]** - Fixed `/status` listing the same broken-install warning twice
- **[UNCOVERED]** - Fixed false "disused plugin" tips and skewed disuse telemetry for LSP plugins
- **[UNCOVERED]** - Fixed `/doctor`'s update check to compare Homebrew installs against their cask's channel instead of the settings channel
- **[UNCOVERED]** - Fixed the fullscreen jump-to-bottom pill suggesting Ctrl+End on macOS, not showing rebound chords, and wrapping over the transcript
- **[UNCOVERED]** - Bedrock: fixed a multi-minute startup hang when using an `awsCredentialExport` helper on networks with restricted egress
- **[UNCOVERED]** - Improved `/code-review` findings quality on claude-opus-4-8 across all effort levels
- **[UNCOVERED]** - Improved agents view: status column now uses full terminal width instead of truncating at 64 characters
- **[UNCOVERED]** - Changed agents view: Ctrl+X now permanently removes a completed session, and sessions no longer render twice; deleted background jobs stay deleted

#### v2.1.205

- **[UNCOVERED]** - Added an auto mode rule that blocks tampering with session transcript files
- **[UNCOVERED]** - Fixed `--json-schema` silently producing unstructured output when the schema was invalid, and schemas using the `format` keyword being rejected
- **[UNCOVERED]** - Fixed a message sent while Claude was working being silently lost when the turn ended at the `--max-turns` limit
- **[UNCOVERED]** - Fixed Windows worktree removal deleting files outside the worktree when an NTFS junction or directory symlink existed inside it
- **[UNCOVERED]** - Fixed background agents staying shown as "failed" or "completed" in the agent list after being resumed with `SendMessage`
- **[UNCOVERED]** - Fixed background jobs flipping from "needs input" back to "working" in the agent list when the agent's turn contained no readable text
- **[UNCOVERED]** - Fixed `claude attach` erroring when a background agent was mid-upgrade restart instead of waiting for it to come back
- **[UNCOVERED]** - Fixed session-to-PR linking missing a PR created in a Bash call whose output exceeded the 30K inline limit
- **[UNCOVERED]** - Fixed `claude mcp add-from-claude-desktop` getting stuck when a server name contains unsupported characters; invalid names are now reported and remaining servers still import
- **[UNCOVERED]** - Fixed a plugin LSP server that fails to initialize preventing a valid LSP server from another plugin handling the same file extension
- **[UNCOVERED]** - Fixed a Windows crash when the directory Claude was launched from is deleted, locked, or unmounted while a command is running
- **[UNCOVERED]** - Fixed a crash when a file watcher was closed while a directory scan was still in flight
- **[UNCOVERED]** - Fixed project verify skills being rewritten on every session instead of only when a documented command changed
- **[UNCOVERED]** - Fixed the agent view rendering one line too high and clipping its header when the job list slightly overflowed the screen
- **[UNCOVERED]** - Fixed background tasks in the web and mobile Remote Control panels showing stale "Running" status by forwarding full task state on every membership change
- **[UNCOVERED]** - Improved auto mode to ask before running `rm -rf` on a variable it can't resolve from context
- **[UNCOVERED]** - Auto-update binary downloads now stream to disk instead of buffering in memory, cutting the updater's peak memory usage by roughly 400 MB
- **[UNCOVERED]** - Background task notifications now explicitly state that no human input has occurred, preventing fabricated in-transcript approvals from being acted on
- **[UNCOVERED]** - Improved agent view: sessions that edit, merge, comment on, or push to an existing PR now link it in `claude agents`
- **[UNCOVERED]** - Improved agent view: rows now show a colored state word and a classifier-written headline instead of raw tool call text, and the peek opens with full status including the exact ask for blocked sessions
- **[UNCOVERED]** - `/doctor` is now a full setup checkup that can diagnose and fix issues; `/checkup` is its alias
- **[UNCOVERED]** - Reserved the "Claude Browser" MCP server name (alongside "Claude Preview") ahead of the Claude Desktop pane rename; user-configured MCP servers can no longer register under either name
- **[UNCOVERED]** - Fixed Cowork VM-mode local-agent sessions failing to start with "Not logged in · Please run /login" on CLI 2.1.203+

#### v2.1.204

- **[UNCOVERED]** - Fixed hook events not streaming during SessionStart hooks in headless sessions, which could cause remote workers to be idle-reaped mid-hook

#### v2.1.203

- **[UNCOVERED]** - Added a warning when your login is about to expire, so you can re-authenticate before background sessions are interrupted
- **[UNCOVERED]** - Added a grey ⏸ badge to the footer when in manual permission mode, making the active mode always visible
- **[UNCOVERED]** - Added the session's additional working directories to MCP `roots/list`, with `notifications/roots/list_changed` sent when the set changes
- **[UNCOVERED]** - Fixed opening or switching background agent sessions on macOS stalling for 15–20 seconds due to a false low-memory detection (regression in 2.1.196)
- **[UNCOVERED]** - Fixed background sessions becoming permanently unresponsive to attach, replies, and stop when the daemon's session token went stale — the session now recovers automatically
- **[UNCOVERED]** - Fixed returning to `claude agents` silently stopping running subagents and re-running the prompt from scratch — their work now carries over
- **[UNCOVERED]** - Fixed a memory and per-turn CPU regression in interactive sessions: the context-usage indicator no longer re-analyzes the entire transcript after every turn
- **[UNCOVERED]** - Fixed background agents inheriting a stale `PATH` from the daemon instead of the dispatching shell, causing missing tools on Windows
- **[UNCOVERED]** - Fixed background and agent-view sessions dropping a shell-exported `ANTHROPIC_BASE_URL`, which sent API keys to the default endpoint and failed with 401
- **[UNCOVERED]** - Fixed Bash failing with "argument list too long" in repos with many git worktrees
- **[UNCOVERED]** - Fixed worktree-isolated subagents sometimes running shell commands in the parent checkout instead of their own worktree
- **[UNCOVERED]** - Fixed worktree creation rejecting nested repositories in multi-repo workspaces, leaving background sessions unable to isolate and edit
- **[UNCOVERED]** - Fixed background agents crash-looping when their working directory was deleted, replaced by a file, or became an invalid path — they now fail once with a clear error
- **[UNCOVERED]** - Fixed a background daemon auto-upgrade failure silently killing all running background sessions
- **[UNCOVERED]** - Fixed `TaskStop` and `TaskOutput` failing to find background agents spawned by another agent — errors now list running agents by id and description
- **[UNCOVERED]** - Fixed the `claude agents` composer discarding your typed message when a slash command isn't available there
- **[UNCOVERED]** - Fixed the agent list crashing when opening a stopped session whose conversation was already open in another session
- **[UNCOVERED]** - Fixed background sessions showing "Needs input" in the agent list after the question was already answered
- **[UNCOVERED]** - Fixed background agent startup failures showing only "exit_with_message" instead of the actual error
- **[UNCOVERED]** - Fixed background sessions ignoring `effortLevel` changes in settings.json when forked through the daemon
- **[UNCOVERED]** - Fixed attached background sessions ignoring `CLAUDE_CODE_DISABLE_MOUSE` and `CLAUDE_CODE_DISABLE_MOUSE_CLICKS` opt-outs
- **[UNCOVERED]** - Fixed `/exit` incorrectly warning about running background agents after all named agents had completed
- **[UNCOVERED]** - Fixed background sessions started from a non-git directory unable to edit files when a `WorktreeCreate` hook was configured
- **[UNCOVERED]** - Fixed the `@` directory picker in `claude agents` not showing registered git worktrees
- **[UNCOVERED]** - Fixed background task output on Windows being permanently replaced by an empty file after `/clear`
- **[UNCOVERED]** - Fixed content jumping when scrolling up through long transcript history
- **[UNCOVERED]** - Fixed the terminal flickering and jumping while typing in bash mode when a shell-history suggestion was shown
- **[UNCOVERED]** - Fixed literal `^[[I` / `^[[O` escape codes being printed when reattaching to a background session
- **[UNCOVERED]** - Fixed LSP-only plugins being incorrectly flagged for disuse when their language servers deliver diagnostics or answer navigation requests
- **[UNCOVERED]** - Improved responsiveness while long responses stream: live-preview updates no longer re-render the whole screen
- **[UNCOVERED]** - Improved subagent behavior: agents are now less likely to re-delegate their entire task to another subagent
- **[UNCOVERED]** - Reduced binary size by ~7 MB and startup memory by ~7 MB by loading a large bundled dependency lazily instead of inlining it
- **[UNCOVERED]** - Changed left arrow to no longer close the background tasks, diff, and workflow detail views — press Esc instead
- **[UNCOVERED]** - Changed the empty `claude agents` view to always show the organized sections (Needs input / Working / Completed) with descriptions
- **[UNCOVERED]** - Removed the startup "claude command missing or broken" warnings — they now appear in `/doctor` and `/status` instead
- **[UNCOVERED]** - Removed a redundant navigation hint from the `claude agents` footer
- **[UNCOVERED]** - [VSCode] Added a Settings toggle for "Enable Remote Control for all sessions"

#### v2.1.202

- **[UNCOVERED]** - Added a "Dynamic workflow size" setting in `/config` for controlling how large Claude generally makes dynamic workflows (small/medium/large agent counts) — an advisory guideline, not an enforced cap
- **[UNCOVERED]** - Added `workflow.run_id` and `workflow.name` OpenTelemetry attributes to telemetry emitted by workflow-spawned agents, so a workflow run's activity can be reconstructed from OTel data
- **[UNCOVERED]** - Fixed a crash in the inline Ctrl+R history search when accepting or cancelling while the search was still scanning the history file
- **[UNCOVERED]** - Fixed `/rename` on background sessions being reverted when the job restarts, which broke addressing the session by its new name
- **[UNCOVERED]** - Fixed transient mTLS handshake failures when settings were re-applied during an in-place client certificate rotation
- **[UNCOVERED]** - Fixed commands sent from Remote Control (mobile/web) into an interactive session failing with "Unknown command"
- **[UNCOVERED]** - Fixed images and files sent from the Remote Control mobile or web app without a caption being silently dropped
- **[UNCOVERED]** - Fixed the sign-in URL printed by `claude auth login` and `claude mcp login --no-browser` not being reliably clickable when it wraps over SSH — it is now emitted as a single hyperlink
- **[UNCOVERED]** - Fixed opening a chat from `claude agents` sometimes failing with "currently running as a background agent" followed by a worker crash/respawn loop
- **[UNCOVERED]** - Fixed workflow scripts with unicode quote escapes in strings being corrupted before parsing; workflow parse errors now show the offending line instead of always blaming TypeScript
- **[UNCOVERED]** - Fixed voice dictation retrying in an unbounded loop when the microphone or audio recorder fails — repeated capture failures now pause voice input
- **[UNCOVERED]** - Fixed `/remote-control` sessions showing the wrong permission mode in the mobile and web apps
- **[UNCOVERED]** - Fixed resuming a session by name, or opening the resume picker, taking minutes and using a large amount of memory in repositories with many git worktrees
- **[UNCOVERED]** - Fixed installer and updater downloads failing immediately with "aborted" when a proxy or network drops the connection mid-download — transient connection drops now retry
- **[UNCOVERED]** - Fixed re-invoking an already-loaded skill appending a duplicate copy of its instructions to context
- **[UNCOVERED]** - Improved `/workflows` agent list layout: wider titles, a dedicated time column, shorter model names, and no per-row tool-call counts
- **[UNCOVERED]** - Improved MCP error messages: clearer error when a server config has `url` but no `type`, suggesting `"type": "http"` instead of the misleading "command: expected string"
- **[UNCOVERED]** - Changed `/review <pr>` back to a fast single-pass review; use `/code-review <level> <pr#>` for the multi-agent review at a chosen effort level

#### v2.1.201

- **[UNCOVERED]** - Claude Sonnet 5 sessions no longer use the mid-conversation system role for harness reminders

#### v2.1.200

- **[UNCOVERED]** - Changed `AskUserQuestion` dialogs to no longer auto-continue by default; opt into an idle timeout via `/config`
- **[UNCOVERED]** - Changed the "default" permission mode to "Manual" across the CLI, `--help`, VS Code, and JetBrains; `--permission-mode manual` and `"defaultMode": "manual"` are accepted alongside `default`
- **[UNCOVERED]** - Fixed a crash at startup when `disabledMcpServers` or `enabledMcpServers` in `.claude.json` is set to a non-array value
- **[UNCOVERED]** - Fixed background sessions silently stopping mid-turn after sleep/wake or when reopening a stalled session
- **[UNCOVERED]** - Fixed background sessions re-running a turn cancelled with Esc after a stall respawn
- **[UNCOVERED]** - Fixed background agents never starting again after a crash left a stale `daemon.lock` whose PID the OS reused
- **[UNCOVERED]** - Fixed background-agent daemon handover so a reinstalled older build can no longer take over the daemon; build recency is now judged by the version's embedded build timestamp
- **[UNCOVERED]** - Fixed background-agent roster issues: transient corruption permanently disabling orphan cleanup, older binaries not preserving fields written by newer versions, and socket auth tokens being stripped during daemon restarts
- **[UNCOVERED]** - Fixed subagents cut off by a rate limit before producing any text output returning an empty result instead of failing cleanly
- **[UNCOVERED]** - Fixed control bytes from background-agent output reaching the terminal in the agent view
- **[UNCOVERED]** - Fixed `claude agents --plugin-dir <dir>` not showing the plugin's agents and skills in the agent view when the flag is placed after `agents`
- **[UNCOVERED]** - Fixed project-scoped plugins not loading correctly from git worktrees of the same repository
- **[UNCOVERED]** - Fixed `/mcp` server list not tracking focus for screen readers and magnifiers
- **[UNCOVERED]** - Fixed voice dictation showing a misleading "Voice connection failed" message when a recording captures no audio
- **[UNCOVERED]** - Fixed rendering flicker under tmux 3.4+ by enabling synchronized terminal output
- **[UNCOVERED]** - Improved screen-reader output: decorative glyphs are now hidden, transcript symbols read as short labels, and nested tables read as `Header: value.` lines
- **[UNCOVERED]** - Improved the install script to explain when installation is killed by the system running out of memory

#### v2.1.199

- **[UNCOVERED]** - Stacked slash-skill invocations like `/skill-a /skill-b do XYZ` now load all leading skills (up to 5), not just the first
- **[UNCOVERED]** - Fixed SSL certificate errors (TLS-inspecting proxies, missing `NODE_EXTRA_CA_CERTS`, expired certs) burning retries before showing actionable guidance — they now fail immediately with the fix hint
- **[UNCOVERED]** - Fixed streaming responses being discarded when the API emits a mid-stream overloaded/server error after partial output — the partial is now kept with an incomplete-response notice
- **[UNCOVERED]** - Fixed subagents cut off by a rate limit or server error silently failing instead of returning their partial work to the parent
- **[UNCOVERED]** - Fixed subagents reporting API errors (e.g. usage limit reached) as successful results — the error is now reported to the parent agent
- **[UNCOVERED]** - Fixed the background-agent daemon on Linux killing itself and every running agent every ~50 seconds after an unclean shutdown left a corrupted worker record
- **[UNCOVERED]** - Fixed background agents failing to cold-start over SSH on macOS with "Could not switch to audit session" (regression in 2.1.196)
- **[UNCOVERED]** - Fixed `claude stop` being silently undone when it raced a background-agent respawn — the respawn now honors the stop
- **[UNCOVERED]** - Fixed background job progress indicators stalling for minutes while the job ran long commands
- **[UNCOVERED]** - Fixed background sessions on memory-starved machines showing a generic error — they now indicate low memory and suggest freeing resources
- **[UNCOVERED]** - Fixed remote sessions briefly flapping between Working and Idle in the agent view when a background agent completes
- **[UNCOVERED]** - Fixed idle subagents vanishing from the agent panel while other subagents were still working; surplus idle agents now collapse into an expandable summary row
- **[UNCOVERED]** - Fixed typing `/model` or `/fast` while viewing a subagent silently opening the lead's model picker — a notice now explains the command applies to the lead
- **[UNCOVERED]** - Fixed `SessionStart`, `Setup`, and `SubagentStart` hooks silently hiding stderr when exiting with code 2 — the error is now shown in the transcript
- **[UNCOVERED]** - Fixed `claude --dangerously-skip-permissions daemon <subcommand>` being treated as a chat prompt instead of running the subcommand
- **[UNCOVERED]** - Fixed `SendMessage` silently misrouting when a re-spawned agent reuses a previous agent's name — the tool now detects the mismatch and asks the caller to retarget
- **[UNCOVERED]** - Fixed opening or resuming a session with no new messages needlessly growing the transcript file
- **[UNCOVERED]** - Fixed backgrounding a session with `←` or `/background` dropping its `/color` from the agent view row
- **[UNCOVERED]** - Fixed resetting a corrupted config file from the startup recovery dialog destroying it unrecoverably — it now backs up the file first
- **[UNCOVERED]** - Fixed Claude in Chrome repeatedly opening the reconnect page when sessions run from different builds or config directories
- **[UNCOVERED]** - Fixed plan mode not prompting for state-changing browser tool calls; read-only `browser_batch` calls are now correctly auto-allowed
- **[UNCOVERED]** - Transient server rate-limit errors (429s unrelated to your usage limit) are now retried automatically with backoff for subscribers instead of failing the turn
- **[UNCOVERED]** - `CLAUDE_CODE_RETRY_WATCHDOG` now raises the default retry count for non-capacity transient errors to 300 and lifts the cap of 15 on `CLAUDE_CODE_MAX_RETRIES`
- **[UNCOVERED]** - `claude agents` session rows now show pull-request links as bare `#N` without the redundant "PR" label

#### v2.1.198

- **[UNCOVERED]** - Subagents now run in the background by default, so Claude keeps working while they run and is notified when they finish (previously a gradual rollout)
- **[UNCOVERED]** - Claude in Chrome is now generally available
- **[UNCOVERED]** - Added background agent notifications in `claude agents` — sessions that need input or finish now fire the `Notification` hook (`agent_needs_input` / `agent_completed`)
- **[UNCOVERED]** - Added `/dataviz` skill for chart and dashboard design guidance with a runnable color-palette validator
- **[UNCOVERED]** - Gateway: added Claude Platform on AWS (anthropicAws) as an upstream provider; model-not-found responses now advance the failover chain
- **[UNCOVERED]** - Background agents launched from `claude agents` now commit, push, and open a draft PR when they finish code work in a worktree, instead of stopping to ask
- **[UNCOVERED]** - The built-in Explore agent now inherits the main session's model (capped at opus) instead of running on haiku
- **[UNCOVERED]** - Subagents and context compaction now inherit the session's extended thinking configuration, improving output quality on delegated tasks
- **[UNCOVERED]** - Fixed brief network drops mid-response aborting the turn — transient errors like ECONNRESET now retry with backoff instead of failing
- **[UNCOVERED]** - Fixed excessive background classifier requests when sandboxed processes repeatedly accessed the same network host
- **[UNCOVERED]** - Fixed background tasks in web, desktop, and VS Code task panels getting stuck on "Running" after they finish or after resuming a session
- **[UNCOVERED]** - Fixed agent teams: a teammate that dies on an API error now reports "failed" to the lead, and messaging a stuck teammate wakes it to retry immediately
- **[UNCOVERED]** - Fixed the `/diff` panel not refreshing when you switch branches or commit outside the session
- **[UNCOVERED]** - Fixed markdown tables overflowing and wrapping their right border when rendered in fullscreen mode
- **[UNCOVERED]** - Fixed Claude Platform on AWS and Mantle sessions dead-ending with "Please run /login" when the STS token expires — `awsAuthRefresh` now runs automatically
- **[UNCOVERED]** - Fixed "no route to host" for local-network hosts in macOS background agent sessions by declaring Local Network entitlements
- **[UNCOVERED]** - Fixed `/desktop` failing with "Cannot determine working directory" after entering and exiting a worktree
- **[UNCOVERED]** - Fixed background agents repeatedly showing "Reconnecting…" every ~52 seconds on macOS while the agents view was open
- **[UNCOVERED]** - Fixed pressing `←` inside `claude attach <id>` exiting to the shell instead of opening the agent view
- **[UNCOVERED]** - Fixed `claude --bg` silently creating an unattachable session when combined with `--print`/`-p`; the conflicting flags are now rejected up front
- **[UNCOVERED]** - Fixed the workflow progress view dropping the earliest agents from the list while the phase counter stayed correct in SDK and desktop-app sessions
- **[UNCOVERED]** - Fixed `.claude/rules/` conditional rules not loading when the target file is reached via a symlinked path
- **[UNCOVERED]** - Fixed Cmd+click not opening URLs in fullscreen mode in Warp on macOS
- **[UNCOVERED]** - Fixed double-click word selection in fullscreen mode to select the entire URL including the scheme
- **[UNCOVERED]** - Fixed plan mode not auto-allowing read-only tool calls when a session starts in plan mode
- **[UNCOVERED]** - Fixed `/branch` deriving its default fork name from the compaction summary instead of the first real prompt
- **[UNCOVERED]** - Improved focus mode: subagents launched in a turn now appear in its activity summary, and completed background notifications fold into a single count
- **[UNCOVERED]** - Improved syntax highlighting accuracy in code blocks, diffs, and file previews by upgrading to highlight.js 11
- **[UNCOVERED]** - Keyboard shortcut hints now show opt/cmd instead of alt/super when connected from a Mac over SSH
- **[UNCOVERED]** - Improved API retry UX: the error reason is now shown after the second attempt, and a status page link replaces the spinner tip when the API is overloaded
- **[UNCOVERED]** - `/login` now opens the sign-in dialog from the `claude agents` view instead of saying it isn't available
- **[UNCOVERED]** - Subagents now treat messages from the agent that launched them as normal task direction; an agent's message is still never treated as the user's approval
- **[UNCOVERED]** - Removed the `/agents` wizard; ask Claude to create or manage subagents, or edit `.claude/agents/` directly

#### v2.1.197

- **[UNCOVERED]** - Introducing Claude Sonnet 5: now the default model in Claude Code, with a native 1M-token context window and promotional pricing of $2/$10 per Mtok through August 31. Update to version 2.1.197 for access. https://www.anthropic.com/news/claude-sonnet-5

#### v2.1.196

- **[UNCOVERED]** - Added support for organization default models — admins set it in the org console; it shows as "Org default" (or "Role default") in `/model` when you haven't picked one yourself
- **[UNCOVERED]** - Added readable default names for sessions at start, making them easier to identify and message
- **[UNCOVERED]** - Added clickable file attachments in chat — Cmd/Ctrl-click reveals the file in Finder/Explorer
- **[UNCOVERED]** - Security: `claude mcp list`/`get` no longer spawn `.mcp.json` servers that a repo self-approved via a committed `.claude/settings.json`; untrusted workspaces show `⏸ Pending approval`
- **[UNCOVERED]** - Fixed waking a background job permanently deleting its conversation and re-running the original prompt when the transcript probe misread a real transcript; the file is now set aside, never deleted
- **[UNCOVERED]** - Fixed the rate-limit warning flickering off and rate-limit telemetry being over-counted when multiple parallel requests were in flight at the moment a usage limit was hit
- **[UNCOVERED]** - Fixed duplicate recap lines after a background session's turn: a schema-rejected StructuredOutput attempt no longer renders alongside its retry
- **[UNCOVERED]** - Fixed PowerShell `git diff`/`git grep`, `egrep`/`fgrep`, and quoted search patterns containing `|` being reported as failures when they exit 1, matching Bash behavior
- **[UNCOVERED]** - Fixed multiple `claude agents` side panel issues: keyboard focus getting stuck when opening an agent, background jobs losing their subagent types on every open, and sessions showing incorrect status while actively running
- **[UNCOVERED]** - Fixed `claude agents --dangerously-skip-permissions` silently falling back to auto mode instead of showing the bypass disclaimer and applying bypass mode to spawned agents
- **[UNCOVERED]** - Fixed mid-turn crash recovery for Remote sessions — sessions interrupted by a server restart now auto-resume on the next worker
- **[UNCOVERED]** - Fixed sessions moved with `/cd` reappearing in the old directory's resume list after a non-graceful exit when the old path contained special characters
- **[UNCOVERED]** - Fixed `claude plugin validate` skipping local plugins whose source is "." and stopping after the first error class
- **[UNCOVERED]** - Fixed Esc Esc at an idle prompt not opening the rewind menu (regression); use Ctrl+C or Ctrl+X Ctrl+K to stop background agents
- **[UNCOVERED]** - Fixed MCP OAuth requesting the authorization server's full `scopes_supported` catalog when no scope is specified, causing `invalid_scope` failures on GitLab self-hosted and other enterprise IdPs
- **[UNCOVERED]** - Fixed `/context` showing 0 tokens for all tool groups on Bedrock
- **[UNCOVERED]** - Fixed `/deep-research` misreporting verifier failures as "all claims refuted" instead of `unverified`
- **[UNCOVERED]** - Fixed plugin dependency version pins not being honored when the marketplace was added as a local folder path backed by a git repo
- **[UNCOVERED]** - Fixed `claude agents` session status: completed rows no longer flip between "Done" and "Needs your input", stalled agents are now labeled "Needs attention", and results that mention a PR show a clickable link
- **[UNCOVERED]** - Fixed voice dictation swallowing spaces and spuriously starting a recording during very fast typing when voice mode is enabled
- **[UNCOVERED]** - Improved background session reliability: long-running commands and workflows now survive the session's process being stopped, restarted, or updated — including on Windows, where background shells are handed off instead of being killed
- **[UNCOVERED]** - Improved background agents: workers killed by a daemon restart are now automatically resumed from where they left off the next time the agents view opens
- **[UNCOVERED]** - Improved `/code-review` workflow: merged five cleanup finders into one, cutting token usage by roughly 25%
- **[UNCOVERED]** - Reduced per-frame rendering work in the terminal UI by skipping no-op subtree walks during streaming
- **[UNCOVERED]** - The streaming idle watchdog is now on by default for all providers — it aborts and retries when a response stream produces no events for 5 minutes. Set `CLAUDE_ENABLE_STREAM_WATCHDOG=0` to disable.
- **[UNCOVERED]** - Remote Control is now disabled when `ANTHROPIC_BASE_URL` points at a non-Anthropic host, matching the existing behavior under `CLAUDE_CODE_USE_BEDROCK`/`_VERTEX`/`_FOUNDRY`
- **[UNCOVERED]** - Changed opening the agents view from a foreground session to require a single `←` press instead of two, matching the behavior in background sessions

#### v2.1.195

- **[UNCOVERED]** - Added `CLAUDE_CODE_DISABLE_MOUSE_CLICKS` to disable mouse click/drag/hover in fullscreen mode while keeping wheel scroll
- **[UNCOVERED]** - Fixed hook matchers with hyphenated identifiers (e.g. `code-reviewer`, `mcp__brave-search`) accidentally substring-matching — they now exact-match. Use `mcp__brave-search__.*` to match all tools from a hyphenated MCP server.
- **[UNCOVERED]** - Fixed voice dictation on macOS capturing silence in long-running sessions after the default input device changes
- **[UNCOVERED]** - Fixed voice dictation auto-submit never firing for languages written without spaces (Japanese, Chinese, Thai)
- **[UNCOVERED]** - Fixed external plugins enabled only by project `.claude/settings.json` not requiring explicit install consent on every loader path
- **[UNCOVERED]** - Fixed `/plugin` Enable/Disable not working when a plugin's `plugin.json` `name` differs from its marketplace entry name
- **[UNCOVERED]** - Fixed background jobs disappearing from `claude agents` or losing data when written by a newer Claude Code version
- **[UNCOVERED]** - Fixed reopening a crashed background task showing a blank screen for up to 5 seconds instead of its restart
- **[UNCOVERED]** - Fixed background agent daemons running unreachable when the control socket fails to start, blocking restarts
- **[UNCOVERED]** - Improved voice mode on Linux: now distinguishes "no microphone" from "SoX not installed" when SoX is present but no audio capture device exists
- **[UNCOVERED]** - Improved `claude agents` completed list to fill available vertical space; on short terminals the header compacts so live sessions stay visible
- **[UNCOVERED]** - Improved Remote session startup with a provisioning checklist while the container starts

#### v2.1.193

- **[UNCOVERED]** - Added `autoMode.classifyAllShell` setting to route all Bash/PowerShell commands through the auto-mode classifier instead of only arbitrary-code-execution patterns
- **[UNCOVERED]** - Added auto-mode denial reasons to the transcript, the denial toast, and `/permissions` recent denials
- **[UNCOVERED]** - Added `claude_code.assistant_response` OpenTelemetry log event containing the model's response text. Redacted unless `OTEL_LOG_ASSISTANT_RESPONSES=1`; when that var is unset it follows `OTEL_LOG_USER_PROMPTS`, so deployments that already log prompt content will start receiving response content on upgrade — set `OTEL_LOG_ASSISTANT_RESPONSES=0` to keep prompts-only.
- **[UNCOVERED]** - Added live file path autocomplete to bash mode (`!`)
- **[UNCOVERED]** - Added a startup notice when MCP servers need authentication, pointing at `/mcp`
- **[UNCOVERED]** - Added automatic memory-pressure reaping for idle background shell commands (disable with `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1`)
- **[UNCOVERED]** - Fixed `/model` and other client-data-gated UI showing stale/empty state immediately after `/login`
- **[UNCOVERED]** - Fixed backgrounding (←←) spuriously cancelling with "N background tasks would be abandoned" when all running tasks carry over to the new session
- **[UNCOVERED]** - Fixed pinned background agents being re-prompted to "Continue from where you left off" after every auto-update
- **[UNCOVERED]** - Fixed backgrounding the main turn spawning a phantom "general-purpose (resumed)" subagent that re-ran the main conversation
- **[UNCOVERED]** - Fixed agent panel hiding sibling agents when viewing a subagent
- **[UNCOVERED]** - Improved background agents: the launch result no longer instructs Claude to "end your response" — it keeps working on other tasks while the agent runs
- **[UNCOVERED]** - Improved MCP `headersHelper` auth: the helper now re-runs and reconnects automatically when a tool call returns 401/403
- **[UNCOVERED]** - Improved plugin auto-rename: marketplace `renames` maps are now followed automatically, updating your settings to the new name
- **[UNCOVERED]** - Improved `/add-dir` message when the directory is already a working directory

#### v2.1.191

- **[UNCOVERED]** - Added `/rewind` support for resuming a conversation from before `/clear` was run
- **[UNCOVERED]** - Fixed scroll position jumping to the bottom while reading earlier output during a streaming response
- **[UNCOVERED]** - Fixed background agents resurrecting after being stopped — stopping an agent from the tasks panel is now permanent
- **[UNCOVERED]** - Fixed `/voice` showing a generic "not available" message when disabled by an organization's policy — it now explains the restriction
- **[UNCOVERED]** - Fixed `/login` URL opening truncated in Windows Terminal when it wraps across lines
- **[UNCOVERED]** - Fixed Cmd+click on links in fullscreen mode for Ghostty over ssh/tmux
- **[UNCOVERED]** - Fixed `claude agents` sending builtin slash commands like `/usage` to background sessions as prompt text instead of showing a hint
- **[UNCOVERED]** - Fixed `claude agents` job rows showing full filesystem paths for pasted images instead of the `[Image #N]` placeholder
- **[UNCOVERED]** - Fixed hooks with comma-separated matchers (e.g. `"Bash,PowerShell"`) silently never firing
- **[UNCOVERED]** - Fixed `/permissions` Recently-denied tab: approving a denial now persists on close instead of being silently discarded
- **[UNCOVERED]** - Fixed the agent panel jumping by one row when scrolling the roster past the overflow cap
- **[UNCOVERED]** - Fixed the welcome splash art overflowing the default 80×24 macOS Terminal window
- **[UNCOVERED]** - Fixed managed settings: `forceRemoteSettingsRefresh` now takes effect when set via MDM or file policy, and the fetch sends `Cache-Control: no-cache` to prevent proxies from serving stale responses
- **[UNCOVERED]** - Improved sandbox network permission dialog: hosts you allow with "Yes" are now remembered for the rest of the session instead of re-prompting on every connection
- **[UNCOVERED]** - Improved MCP server reliability: capability discovery (`tools/list`, `prompts/list`, `resources/list`) now retries transient network errors with short backoff
- **[UNCOVERED]** - Improved MCP OAuth: discovery and token requests now retry once after transient network errors, and headless environments skip the browser popup and go straight to the paste-the-URL prompt
- **[UNCOVERED]** - Improved MCP error messages: HTTP 404 errors now show the URL and point to your MCP config
- **[UNCOVERED]** - Improved vim mode prompt-history search (NORMAL `/`) to hint how to reach slash commands
- **[UNCOVERED]** - Reduced CPU usage during streaming responses by ~37% by coalescing text updates to 100ms
- **[UNCOVERED]** - Reduced long-session memory growth from terminal output cache

#### v2.1.190

- **[UNCOVERED]** - Bug fixes and reliability improvements

#### v2.1.187

- **[UNCOVERED]** - Added `sandbox.credentials` setting to block sandboxed commands from reading credential files and secret environment variables
- **[UNCOVERED]** - Added org-configured model restrictions to the model picker, `--model`, `/model`, and `ANTHROPIC_MODEL`, with a "restricted by your organization's settings" message when a restricted model is selected
- **[UNCOVERED]** - Added mouse click support to select menus (permission prompts, `/model`, `/config`, etc.) in fullscreen mode
- **[UNCOVERED]** - Fixed `--resume` failing with "No conversation found" when the original `-p` run produced no model turns
- **[UNCOVERED]** - Fixed `--json-schema` and workflow `agent({schema})` structured output: the model can no longer re-call `StructuredOutput` indefinitely after a successful call, and follow-up turns now reliably return structured output
- **[UNCOVERED]** - Fixed remote MCP tool calls that hang with no response for 5 minutes — they now abort with an error instead of blocking indefinitely (override with `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`)
- **[UNCOVERED]** - Fixed Claude Code Remote sessions taking ~2.7s longer to start after the agent proxy CA system-trust install was added
- **[UNCOVERED]** - Fixed pasted Korean/CJK text turning into mojibake in terminals that deliver paste as per-byte extended-key events
- **[UNCOVERED]** - Fixed `/update` over Remote Control hanging when a startup trust dialog would have shown
- **[UNCOVERED]** - Fixed background jobs in the agents view getting stuck in "working" indefinitely when the agent ended a turn without producing structured output
- **[UNCOVERED]** - Fixed channel connections dropping after navigating to the agents view and back, and after `/bg`, `/tui`, or `/update`
- **[UNCOVERED]** - Fixed agent stop notifications not correctly attributing who stopped the agent, and improved wording ("finished"/"stopped" instead of "came to rest")
- **[UNCOVERED]** - Fixed subagent depth tracking: resumed subagents now restore their original spawn depth, and forked subagents now count toward the depth cap
- **[UNCOVERED]** - Fixed leaked agent worktree registrations: locked `.git/worktrees/` entries from killed agents are now cleaned up automatically
- **[UNCOVERED]** - Fixed Cmd+click not opening URLs in fullscreen mode in Ghostty on macOS
- **[UNCOVERED]** - Fixed `claude --help` not listing the `--bg`/`--background` flag
- **[UNCOVERED]** - Fixed Esc, Ctrl-C, and Ctrl-D not working while `/share` is uploading
- **[UNCOVERED]** - Improved `/install-github-app`: GitHub Actions workflow setup is now optional — you can install just the GitHub App and skip the workflow/secret steps
- **[UNCOVERED]** - Improved `/btw` with ←/→ arrow navigation to step through earlier answers
- **[UNCOVERED]** - Improved `/plugin` to surface plugins you haven't used recently so you can clean them up
- **[UNCOVERED]** - [VSCode] Fixed extension becoming unresponsive when resuming a large session

#### v2.1.186

- **[UNCOVERED]** - Added `claude mcp login <name>` and `claude mcp logout <name>` to authenticate MCP servers from the CLI without opening the interactive `/mcp` menu, with `--no-browser` stdin redirect support for completing over SSH
- **[UNCOVERED]** - Added status filtering (press `f`) to the `/workflows` agent detail view
- **[UNCOVERED]** - Added a "Skills" section to the `/plugin` Installed tab
- **[UNCOVERED]** - Added `teammateMode: "iterm2"` setting with a warning when auto mode cannot find the `it2` CLI
- **[UNCOVERED]** - Added "Claude Platform on AWS - refresh credentials" option to `/login` when `awsAuthRefresh` is configured
- **[UNCOVERED]** - `!` bash commands now trigger Claude to respond to the output automatically; set `"respondToBashCommands": false` in settings.json to keep the previous context-only behavior
- **[UNCOVERED]** - Fixed streaming requests failing with "Content block not found" or JSON parse errors after the machine wakes from sleep
- **[UNCOVERED]** - Fixed subagent transcript scroll position bleeding into the main transcript on exit
- **[UNCOVERED]** - Fixed background task previews flashing raw tool names before the agent's plan loaded
- **[UNCOVERED]** - Fixed Chrome tab-group isolation not applying when the in-product permissions gate is off for concurrent CLI sessions
- **[UNCOVERED]** - Fixed background session recaps being duplicated; the agent's own end-of-turn summary now shows as the recap line
- **[UNCOVERED]** - Fixed opening a background session from `claude agents` leaving the previous screen painted behind it
- **[UNCOVERED]** - Fixed `Agent(type)` deny rules and `Agent(x,y)` allowed-types restrictions not being enforced for named subagent spawns
- **[UNCOVERED]** - Fixed Esc and Ctrl+C not responding while background agents are still running after the main turn ends
- **[UNCOVERED]** - Fixed misaligned option numbers in permission prompts when the option text overflows
- **[UNCOVERED]** - Fixed pressing `x` on a finished subagent in the agent panel not dismissing it
- **[UNCOVERED]** - Fixed a misleading "MCP server disconnected" notice for intentionally retired tools when resuming older sessions
- **[UNCOVERED]** - Fixed `/plugin` Installed showing a "more above" indicator when already scrolled to the top
- **[UNCOVERED]** - Fixed `~~strikethrough~~` showing literal tildes in assistant messages instead of rendering as strikethrough
- **[UNCOVERED]** - Fixed `--tools` allowing feature-gated tools to slip through before flags loaded on a cold first launch
- **[UNCOVERED]** - Fixed background job status in `claude agents` showing a stale "needs input" message after replying
- **[UNCOVERED]** - Fixed a dark-theme flash when opening a background session from `claude agents` on a light terminal
- **[UNCOVERED]** - Fixed mouse-selected text staying highlighted after deleting it in `claude agents`
- **[UNCOVERED]** - Fixed session cost not showing for usage-based Enterprise and Team subscribers
- **[UNCOVERED]** - Fixed agent teams: teammates spawned via tmux/pane backends now inherit the leader's `--effort` level
- **[UNCOVERED]** - Fixed Workflow `agent({schema})` subagents looping forever on repeated schema validation failures instead of aborting after 5 attempts
- **[UNCOVERED]** - Improved `claude mcp get` and `claude mcp remove` to suggest the closest configured server name on a typo and truncate long server lists
- **[UNCOVERED]** - Improved memory: the agent is now reminded to compact its `MEMORY.md` index when nearing the size limit
- **[UNCOVERED]** - Improved skill frontmatter: `display-name`, `default-enabled`, `fallback`, and `metadata.*` keys now accept kebab-case, snake_case, and camelCase
- **[UNCOVERED]** - Improved malformed `SKILL.md` YAML frontmatter handling: loads the skill body with empty metadata instead of failing silently
- **[UNCOVERED]** - Changed `CLAUDE_CODE_MAX_RETRIES` to cap at 15; for unattended sessions, use `CLAUDE_CODE_RETRY_WATCHDOG` instead
- **[UNCOVERED]** - Changed background subagents to surface permission prompts in the main session instead of auto-denying; the dialog shows which agent is asking, and Esc denies just that tool
- **[UNCOVERED]** - Changed `/review <pr>` to use the same review engine as `/code-review medium`

---
_Generated by `.github/scripts/changelog-compare.py`_
## Native Sources Monitor Report

Sources checked: **3**

### anthropic-blog

- Source: Anthropic Blog — announcements and product updates
- Entries fetched: 10
- New uncovered: 2

| Entry | Section | Description |
|-------|---------|-------------|
| Jul 9, 2026Case StudyUST is bringing Claude to physical AI | Anthropic Blog | Jul 9, 2026Case StudyUST is bringing Claude to physical AI |
| Jun 23, 2026ProductIntroducing Claude Tag | Anthropic Blog | Jun 23, 2026ProductIntroducing Claude Tag |

### cc-issues-enhancement

- Source: CC GitHub Issues labeled 'enhancement'
- Entries fetched: 300
- New uncovered: 3

| Entry | Section | Description |
|-------|---------|-------------|
| Suporte a outros idiomas (Português) no microfone de ditaé e | GitHub Issues (enhancement) | A funcionalidade de microfone (ditaé) na extensão VSCode do Claude Code transcre |
| Suivi des instructions mémorisées peu fiable dans la durée — | GitHub Issues (enhancement) | Titre proposé : Suivi des instructions mémorisées peu fiable dans la durée — bes |
| [BUG] Claude Cowork/Desktop folder revocation problem ("Hote | GitHub Issues (enhancement) | ### Preflight Checklist - [x] I have searched [existing issues]( and this hasn't |

### cc-discussions-feature-request

- Source: CC GitHub Discussions in feature-request category
- Entries fetched: 0
- New uncovered: 0

---
Total new uncovered entries: **5**

_Generated by `.github/scripts/native-sources-monitor.py`_
