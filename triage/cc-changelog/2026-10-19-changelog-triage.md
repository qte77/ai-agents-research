# CC Changelog & Native Sources: New Uncovered Features Detected

## Changelog Monitor Report

Last scanned version: **2.1.296**
New versions detected: **5**

### New Versions Summary

| Version | Features | Covered | Uncovered |
|---------|----------|---------|-----------|
| 2.1.303 | 1 | 0 | 1 |
| 2.1.302 | 63 | 0 | 63 |
| 2.1.301 | 51 | 0 | 51 |
| 2.1.300 | 88 | 0 | 88 |
| 2.1.299 | 190 | 2 | 188 |

### Feature Coverage Details

#### v2.1.303 — released 2026-10-18

- **[UNCOVERED]** - Bug fixes and reliability improvements

#### v2.1.302 — released 2026-10-16

- **[UNCOVERED]** - Added `CLAUDE_CODE_AUTO_MODE_MODEL` to choose the model the client-side auto mode classifier uses; it does not change the model for server-side auto mode
- **[UNCOVERED]** - Added an `Idle compaction` row to `/config` for turning idle compaction off or back on; the notices shown after an idle compaction now say how to turn it off
- **[UNCOVERED]** - Added a notice to `/design-sync` and `/design-login` that standalone Claude Design (claude.ai/design) closes by December 14, 2026
- **[UNCOVERED]** - Fixed a "Prompt is too long" error when stopping a turn while the conversation was being compacted
- **[UNCOVERED]** - Fixed requests failing with "diagnostics: Extra inputs are not permitted" after switching to Vertex or Bedrock mid-session
- **[UNCOVERED]** - Fixed the Read tool loading an image file of any size, or a pipe or device named like an image, entirely into memory; image sources over 128 MB are now refused
- **[UNCOVERED]** - Fixed `/autocompact` and `/effort` saving to the wrong model when a gateway names Opus 4 or 4.1 with a prefix, such as `anthropic/claude-opus-4-1`
- **[UNCOVERED]** - Fixed a prompt cache miss when a tool added mid-session was loaded again through ToolSearch or after compaction
- **[UNCOVERED]** - Fixed `claude plugin` and other subcommands sometimes exiting before a queued settings or config write finished, which could lose the change or leave a `.tmp` file behind
- **[UNCOVERED]** - Fixed plugin marketplaces re-cloning on every refresh, and newly installed git plugins showing version "unknown", when git defaults to the reftable ref format
- **[UNCOVERED]** - Fixed the PowerShell tool not finding commands in a plugin's `bin/` folder, and reporting an error when a search that finds nothing (rg, grep, findstr, git grep) is piped into `Select-Object` or another formatting cmdlet
- **[UNCOVERED]** - Fixed Claude in the desktop app pointing you to claude.ai settings or `/mcp` to authorize or reconnect an MCP server where that option isn't available
- **[UNCOVERED]** - Fixed artifact publishes sometimes failing when Claude sent an empty list of edits, and Claude retrying an artifact update the wrong way after a newer version of the artifact turned it away
- **[UNCOVERED]** - Fixed `classifier_category` missing from OpenTelemetry `tool_decision` events for most auto mode classifier blocks, and new `tool_decision` attributes pushing out `tool_use_id`, `tool_source` and `tool_parameters` when `OTEL_LOGRECORD_ATTRIBUTE_COUNT_LIMIT` is low
- **[UNCOVERED]** - Fixed rows in the agents view staying blank after moving down a long list or folding a section
- **[UNCOVERED]** - Fixed `claude remote-control --help` not printing its usage and exiting when not signed in
- **[UNCOVERED]** - Fixed `/design consent` and `/design revoke` suggesting `/design-login` when they fail in a cloud session, where it isn't available; the message now points to claude.ai/design/settings
- **[UNCOVERED]** - Fixed MCP servers showing no tools, or every tool call failing, when the server negotiates protocol version 2026-07-28 but omits `resultType`, `ttlMs` or `cacheScope`
- **[UNCOVERED]** - Fixed prompt suggestions spending usage credits on models your plan pays for only with credits: they are now skipped after a reply billed to credits
- **[UNCOVERED]** - Fixed URLs written in backticks being clickable only on their first row when they wrap; the whole URL is now one link in terminals that support hyperlinks
- **[UNCOVERED]** - Fixed `claude plugin details <name>@builtin` suggesting `claude plugin list`, which never shows built-in plugins, when the plugin isn't found; it now points to `/plugin`
- **[UNCOVERED]** - Fixed an emoji that a link starts inside wrapping one column too wide, which hid it in question previews and turned tables into lists
- **[UNCOVERED]** - Fixed worktree isolation refusing to create or resume worktrees under git 2.56 or later when a stray `.git` file points at a directory that doesn't exist
- **[UNCOVERED]** - Fixed a cloud session's cost and usage restarting from zero after the session resumed in a new process
- **[UNCOVERED]** - Self-hosted runner: Fixed git fetches failing with "bad object refs/heads" in sessions that reuse a checkout stored in git's reftable format
- **[UNCOVERED]** - Windows: Fixed every file write being refused or asked about for projects on exFAT or FAT32 drives, including in sessions started with `--plugin-dir`
- **[UNCOVERED]** - Improved startup time with many plugins enabled: plugin command and agent files now take far fewer file system calls to load, most of all on Windows
- **[UNCOVERED]** - Improved auto mode with the server-side classifier: a conversation too long for the safety check is now compacted, instead of every checked tool call being denied
- **[UNCOVERED]** - Improved the message when a background session reopened from another folder has no LLM gateway: it now says why, instead of "Not logged in"
- **[UNCOVERED]** - Changed `claude -p` and Agent SDK sessions with no permission mode to start in `default` mode on third-party providers, with telemetry off or on a fresh install; `--permission-mode auto` keeps auto
- **[UNCOVERED]** - Changed fork subagents (`subagent_type: "fork"`) to be on by default in `claude -p`, the Agent SDK, the desktop app and VS Code, as they already are in the terminal; `CLAUDE_CODE_FORK_SUBAGENT=0` turns them off, and `claude mcp serve` never offers them
- **[UNCOVERED]** - Changed the desktop app and VS Code to always run the main conversation's subagents in the background, as the terminal does, rather than let Claude choose; a subagent's own Agent calls in `claude -p`, the Agent SDK, the desktop app and VS Code now run in the foreground by default
- **[UNCOVERED]** - Changed the `← for agents` footer hint to hide 10 seconds after a session opens; the count of agents waiting on you still shows
- **[UNCOVERED]** - Changed where the Claude in Chrome instructions sit in the system prompt so that new conversations can read them from the shared prompt cache
- **[UNCOVERED]** - Changed prompt and agent hooks so that at most 12 of one event run at a time; the rest wait their turn
- **[UNCOVERED]** - Changed the message shown when your organization's policy turns off `/feedback`: it now points to GitHub issues instead of an organization admin
- **[UNCOVERED]** - [VSCode] Fixed text after an unclosed code block in a list showing as plain text while a reply streams, then turning into code
- **[UNCOVERED]** - [VSCode] Fixed MCP server sign-in from the panel opening a broken authorization page when the server URL contains a query string
- **[UNCOVERED]** - [VSCode] Fixed the `@browser` banner saying "Browser connected" when no browser with the Claude extension can be reached
- **[UNCOVERED]** - [Cloud sessions] Added a banner on a routine's page that says why its last run didn't start, such as your organization reaching its limit on concurrent cloud sessions
- **[UNCOVERED]** - [Cloud sessions] Fixed "Rewind to here" failing on every message except the newest in cloud sessions; self-hosted runners need Claude Code v2.1.246 or later
- **[UNCOVERED]** - [Cloud sessions] Fixed the pull request status bar in cloud sessions flipping a pull request with merge conflicts back to ready while GitHub rechecked it
- **[UNCOVERED]** - [Cloud sessions] Fixed routine runs showing as Completed after their cloud session stopped unexpectedly, and as Cancelled when archived before they started, instead of failed
- **[UNCOVERED]** - [Cloud sessions] Fixed the diff view in cloud sessions missing changes or failing to load after the session's GitHub repository was renamed or moved
- **[UNCOVERED]** - [Cloud sessions] Fixed a scheduled routine run that failed partway being run again from the start an hour or more later, which could repeat work such as posting the same report twice
- **[UNCOVERED]** - [Cloud sessions] Fixed an open cloud session sometimes not showing messages sent from another device until you reloaded the page or clicked away and back
- **[UNCOVERED]** - [Cloud sessions] Improved the error shown when a cloud session fails to start: it now says "Connection lost" or "Server error" instead of "Something went wrong"
- **[UNCOVERED]** - [Remote Control] Fixed a subagent's pane spinning forever in a Remote Control session after your computer goes offline; it now says Remote Control is disconnected
- **[UNCOVERED]** - [Claude Tag] Fixed "is thinking…" staying up under a mention in a Slack channel or DM after Claude answered it by editing one of its earlier messages
- **[UNCOVERED]** - [Claude Tag] Fixed URLs in code blocks under a numbered or bulleted step of Claude's Slack replies being wrapped in angle brackets, which broke copied commands
- **[UNCOVERED]** - [Claude Tag] Fixed HEIC, SVG, TIFF and BMP images attached in Slack never reaching Claude; they now arrive as files in its working files, like other file types
- **[UNCOVERED]** - [Claude Tag] Fixed new channel managers losing access to Claude in Slack in organizations that restrict Claude Tag by role; the manager role now also grants Claude Tag in Slack
- **[UNCOVERED]** - [Claude Tag] Fixed custom connectors whose MCP servers share one host showing as a single connector in Claude Tag admin settings; each server is now its own connector
- **[UNCOVERED]** - [Claude Tag] Fixed Claude in Slack sometimes answering a direct message with "DMs are temporarily unavailable" and dropping it when a single Slack lookup stalled; it now retries first
- **[UNCOVERED]** - [Claude Tag] Fixed direct messages with Claude on a Slack Enterprise Grid ignoring Slack's workspace dropdown; they now run under the connected workspace you last opened Claude in
- **[UNCOVERED]** - [Claude Tag] Fixed Claude in Slack's notice for a channel's monthly spend limit saying a channel manager can raise it; it now names an organization owner and links the usage page
- **[UNCOVERED]** - [Claude Tag] Fixed links in Claude's Slack replies absorbing the closing bold or italic marks, or full-width punctuation, right after them, which broke the link and the formatting
- **[UNCOVERED]** - [Claude Tag] Improved repository search in Claude Tag admin settings to cover up to 100 connected GitHub accounts and find private repositories past the first 5,000 of a GitHub App install
- **[UNCOVERED]** - [Claude Tag] Improved Add place in Claude Tag admin settings to list a channel you type or paste right away, instead of only after your organization's full channel list has loaded
- **[UNCOVERED]** - [Claude Tag] Improved Add > Domain on a workspace's or channel's page in Claude Tag admin settings to be available once that page loads, not only after every channel has loaded
- **[UNCOVERED]** - [Claude Tag] Changed Claude Tag admin settings to organize Claude's access into four tabs: Bundles, Connectors, Skills and plugins, and Channels
- **[UNCOVERED]** - [Claude Tag] Changed the Roles page in organization settings to group the roles created for Claude Tag channel managers in a collapsed section below your organization's own roles
- **[UNCOVERED]** - [Code Review] Fixed Code Review setup not resuming after you leave to connect GitHub; back in admin settings, it now reopens at the repository picker

#### v2.1.301 — released 2026-10-15

- **[UNCOVERED]** - Added `CLAUDE_CODE_RETRY_WATCHDOG_MAX_USAGE_LIMIT_WAIT_MS` so unattended retry mode (`CLAUDE_CODE_RETRY_WATCHDOG`) ends a request at a usage limit that resets too far away instead of waiting
- **[UNCOVERED]** - Added OpenTelemetry tracing guidance to the `claude-api` skill, including setting up trace destinations with the `ant` CLI
- **[UNCOVERED]** - Added the `%` motion to vim mode: jump to the matching bracket, alone or with d/c/y
- **[UNCOVERED]** - Added `rows` to a mod's `Input`: a text field of several lines in the terminal, where Enter submits and Shift+Enter or a backslash before Enter starts a new line
- **[UNCOVERED]** - Added `classifier_verdict` and `permission_mode` to OpenTelemetry `tool_decision` events, so auto mode classifier decisions can be told apart from permission rules
- **[UNCOVERED]** - Added `classifier_category` to OpenTelemetry `tool_decision` events, naming the built-in rule a classifier block matched, when `OTEL_LOG_TOOL_DETAILS=1`
- **[UNCOVERED]** - Fixed quitting removing a worktree made by a `WorktreeCreate` hook without asking when it may hold unpushed commits
- **[UNCOVERED]** - Fixed the `fable` (and `best`) model alias erroring on the Anthropic API when the newest Fable model is not available to your organization: Claude Code now retries once on the previous Fable model
- **[UNCOVERED]** - Fixed a misleading "Please run /login" error when a full disk keeps the login from being refreshed; the error now names the disk and says to delete files
- **[UNCOVERED]** - Fixed Grep and Glob reporting no matches when the search program failed unexpectedly before returning any results; they now return an error saying the search failed
- **[UNCOVERED]** - Fixed workflow agents sometimes skipping their step, and the run still reporting success, after reading the harness note that their task text carries no user authority
- **[UNCOVERED]** - Fixed artifact updates being refused where a PreToolUse hook covers Edit or Write; Claude now edits the file and then republishes instead of changing it in the publish call
- **[UNCOVERED]** - Fixed skills and commands with very many or very long argument names stalling for seconds when invoked; only the first 64 names, each up to 64 characters, are now filled in
- **[UNCOVERED]** - Fixed skills, commands and hooks using very large amounts of memory when their arguments fill many placeholders
- **[UNCOVERED]** - Fixed stray characters such as `>0q` covering the folder trust prompt, and `>4m` before the shell prompt at exit, in terminals built on VTE older than 0.53 such as MATE Terminal on RHEL 8
- **[UNCOVERED]** - Fixed stray `GOK` text appearing in the prompt at startup in some versions of iTerm2
- **[UNCOVERED]** - Fixed switching to a model whose name contains `application-inference-profile` running your `awsAuthRefresh` command and delaying model-switch hooks when the provider is not Bedrock
- **[UNCOVERED]** - Fixed sign-in refresh timeouts and unexpected sign-outs after a short command such as `claude auth status` or `claude plugin list` exited in the middle of a token refresh
- **[UNCOVERED]** - Fixed a tool call cut off by a message sent mid-turn during its permission check being reported to the model as rejected by the user
- **[UNCOVERED]** - Fixed a case where switching to a model with a smaller context window could spend usage credits on a summary by the previous model without asking first
- **[UNCOVERED]** - Fixed conversations being compacted over and over, on a model you didn't pick, behind an LLM gateway whose responses name a different model than the one requested
- **[UNCOVERED]** - Fixed vim mode sometimes staying in INSERT after Escape on a slow or busy machine
- **[UNCOVERED]** - Fixed Esc discarding a typed AskUserQuestion answer in vim mode: the free-text field now supports vim NORMAL mode, and Esc cancels only from NORMAL
- **[UNCOVERED]** - Fixed the Read tool reading binary files such as .xlsm, .parquet, .epub and .heic as text
- **[UNCOVERED]** - Fixed a Markdown table with only a header row drawing nothing when too wide for the terminal, including in plans on the plan approval card
- **[UNCOVERED]** - Fixed the /claude-api skill saying CMEK external-key endpoints aren't available on Claude Platform on AWS
- **[UNCOVERED]** - Fixed skills no longer being listed to the model after using `/rewind`
- **[UNCOVERED]** - Fixed the compaction row in a resumed session offering ctrl+o for history that is not loaded; it now says where the earlier messages are saved, and also shows in fullscreen
- **[UNCOVERED]** - Fixed the "new task? /clear to save tokens" hint coming back right after you interrupt a response
- **[UNCOVERED]** - Fixed the permission prompt for a plugin or skill hook's `ask` decision not showing which plugin or skill the hook comes from
- **[UNCOVERED]** - Fixed `/diff` not noticing a conflicted cherry-pick or revert in reftable repositories when one of its git checks timed out or failed
- **[UNCOVERED]** - Fixed workflow scripts asking for permission or being refused when read, edited or re-run after a Bash `cd` in the same session
- **[UNCOVERED]** - Fixed dim text on the dark ANSI theme and 16-color terminals: faint inside filled boxes, not faint under selection and search highlights, and list descriptions dimmed like other secondary text
- **[UNCOVERED]** - Fixed a mod's `$.model.fork` returning `nothing-to-fork` when called before the first response of a new Claude Code process had finished, as in `claude -p` runs and cloud sessions
- **[UNCOVERED]** - Fullscreen mode: Fixed `/compact` and auto-compact briefly freezing the UI while the visible transcript is rebuilt
- **[UNCOVERED]** - Self-hosted runner: Fixed sessions started from Slack being unable to find or attach a repository when managed settings restrict MCP servers; use `deniedMcpServers` to keep those tools off
- **[UNCOVERED]** - Self-hosted runner: Fixed sessions being reported as having a deleted source branch, and not retried, when an unrelated setup or session failure quoted git's missing-ref wording
- **[UNCOVERED]** - Self-hosted runner: Fixed the log promising a retry of a failed or declined session release for a session that is ending; repeated failures now show a count
- **[UNCOVERED]** - Windows: Fixed stopped background PowerShell commands missing the closing `[killed]` line in their output file
- **[UNCOVERED]** - Improved switching to a model with a smaller context window: a conversation too long for the new model is now summarized by the previous model first
- **[UNCOVERED]** - Improved rendering performance while a long-running subagent works: its progress trail now updates incrementally instead of being reprocessed in full on every render
- **[UNCOVERED]** - Improved artifacts: pages Claude writes now paint the band above a sticky header, so scrolled text no longer shows there in the mobile apps
- **[UNCOVERED]** - Improved mods: in VS Code and the desktop and mobile apps, a tree drawn above the question dialog can now hold Markdown and up to 48 rows; the terminal keeps 12 plain rows
- **[UNCOVERED]** - Changed a mod hook's `.catch` handler to run only when the hook throws or times out; events raised beneath the hook's own calls now skip that hook without asking its `.catch`
- **[UNCOVERED]** - Changed a mod's `$.env.set` to resolve with `{}` once the variable is set or unset, or with `{ deny }` saying why when the write is not made
- **[UNCOVERED]** - [VSCode] Added LaTeX math rendering in Claude's responses, including `$$` and multi-line `\[ … \]` blocks and inline `$…$` and `\(…\)` math
- **[UNCOVERED]** - [VSCode] Added a "Get more usage" link to the usage-limit banner for Pro and Max plans in the VS Code and JetBrains panels
- **[UNCOVERED]** - [VSCode] Fixed a conversation that crashes or freezes the panel being reopened on every reload
- **[UNCOVERED]** - [VSCode] Fixed the chat panel slowing down during long thinking: it no longer re-parses the whole thinking text on every update
- **[UNCOVERED]** - [VSCode] Fixed diagnostics showing "[object Object]" instead of the rule code (e.g. MD013) for some language servers
- **[UNCOVERED]** - [VSCode] Fixed the native dictation audio module being loaded, to check microphone permission, where dictation is not offered (non-claude.ai sign-ins, remote windows)

#### v2.1.300 — released 2026-10-14

- **[UNCOVERED]** - Added `virtualText` to a mod's prompt decorations: text drawn in the prompt box that never enters the draft or the submitted prompt
- **[UNCOVERED]** - Added `cache_creation_5m_tokens` and `cache_creation_1h_tokens` to the OpenTelemetry `api_request` event, splitting cache writes by lifetime
- **[UNCOVERED]** - Added `$.ui.view({ agentId })` for mods: shows an agent's transcript in the main view when you ask, and `$.ui.view({})` goes back
- **[UNCOVERED]** - Added a `dir` prop on a mod's `Text` for right-to-left text: on Windows and in VS Code's terminal its rows read in that direction and sit flush right
- **[UNCOVERED]** - Added `/advisor` on Claude Platform on AWS; no advisor runs until you pick one with `/advisor`, `advisorModel` or `--advisor`, and `CLAUDE_CODE_DISABLE_ADVISOR_TOOL=1` turns it off
- **[UNCOVERED]** - Added OpenTelemetry GenAI semantic-convention attributes to trace spans, such as `gen_ai.provider.name`, `gen_ai.conversation.id`, `gen_ai.tool.name` and `error.type`
- **[UNCOVERED]** - Added support for rewriting a workflow agent's `prompt` and `model` in the `agent.spawn` mod hook, which could only refuse workflow agents before
- **[UNCOVERED]** - Added the `prompt.change` mod hook, raised when the prompt box's text changes without a typed edit: a recalled history entry, a clear, an undo, or a plugin's fill
- **[UNCOVERED]** - Fixed cloud sessions telling Claude that an organization policy blocked a host when the session's own network settings did
- **[UNCOVERED]** - Fixed `/autocompact` warning about high token usage when you choose a smaller auto-compact window
- **[UNCOVERED]** - Fixed SessionEnd hooks sometimes not running when you exit while a background command is still running
- **[UNCOVERED]** - Fixed `claude --help` naming a removed tool in its description of `--restricted`
- **[UNCOVERED]** - Fixed `claude agents` not refreshing any pull request's status when the data for one of them came back incomplete
- **[UNCOVERED]** - Fixed Claude being told a background agent was lost, not resumable, after a cloud session's container was replaced, when the agent had already been resumed once
- **[UNCOVERED]** - Fixed subagents you had typed messages to disappearing from `/tasks` shortly after finishing, leaving no way back to the conversation
- **[UNCOVERED]** - Fixed a completed parent agent dropping off the breadcrumb (its child shown re-rooted at top level) while you were viewing the child
- **[UNCOVERED]** - Fixed the agents view taking a typed word such as "up", "down" or "escape" for that key when input arrived in a burst, which could move the peek mid-reply or clear a draft
- **[UNCOVERED]** - Fixed automatic tool search (`ENABLE_TOOL_SEARCH=auto`) turning off part-way through a conversation, for example while MCP servers reconnect after a resume
- **[UNCOVERED]** - Fixed a login refused by `forceLoginOrgUUID` leaving the refused organization's token stored, or live after `/login`
- **[UNCOVERED]** - Fixed the diff view in Claude Desktop and Remote Control sessions not noticing a conflicted cherry-pick or revert in reftable repositories
- **[UNCOVERED]** - Fixed the Artifact tool's verbose and ctrl+o line reading `Artifact("(unprintable path)")` while a call's input arrives; its row now shows "Waiting…" and "Running…" as Bash's does
- **[UNCOVERED]** - Fixed the first transcript entry written after resuming a session being lost when a crash had cut the transcript's last line short
- **[UNCOVERED]** - Fixed `/branch` dropping messages, and `claude purge` skipping subfolder projects, when they contain a Unicode line or paragraph separator (U+2028, U+2029)
- **[UNCOVERED]** - Fixed plugin `WorktreeCreate` and `WorktreeRemove` hooks not running when Claude Code starts with `--worktree` (not yet with `--tmux`)
- **[UNCOVERED]** - Fixed OpenTelemetry `tool_result` events missing `git_commit_id` after `git commit -q` in repositories using reftable ref storage
- **[UNCOVERED]** - Fixed a prompt that a mod's `prompt.submit` hook rewrote or dropped still being recorded as typed in the OpenTelemetry `user_prompt` event and interaction span, and in session title requests
- **[UNCOVERED]** - Fixed a note meant for Claude about mod hot-reloading appearing in the transcript as if you had typed it
- **[UNCOVERED]** - Fixed agent hooks ignoring their `model`: aliases like `haiku` now resolve, a subagent's model no longer overrides it, and an unavailable model falls back to the caller's instead of allowing the action
- **[UNCOVERED]** - Fixed `--worktree` sessions sometimes starting from the wrong commit when a tag or branch was named like a commit ID, and their starting git status naming a branch other than the new worktree's
- **[UNCOVERED]** - Fixed the branch showing as ".invalid" and `--worktree` failing to reopen a worktree in repositories using git's reftable ref storage
- **[UNCOVERED]** - Fixed Claude naming files in the session scratchpad by a bare filename or relative path instead of their full path
- **[UNCOVERED]** - Fixed `claude remote-control` servers giving up on renewing their connection after a brief sign-in error, such as a locked keychain; they now retry, and warn when you need to run `claude /login`
- **[UNCOVERED]** - Fixed `--worktree` failing in a worktree of a bare repository when origin's default branch can't be fetched; the fallback base is now the current checkout's HEAD, not the main repository's
- **[UNCOVERED]** - Fixed starting Claude Code in a VS Code, Cursor or Devin Desktop integrated terminal launching the editor's command-line tool twice to check for the extension; it now launches it once
- **[UNCOVERED]** - Fixed a mod's `prompt.edit` hook not being raised for a newline entered with the `chat:newline` keybinding (Ctrl+J, or a rebound Enter)
- **[UNCOVERED]** - Fixed a conversation failing on every turn with a 400 error when the API rejected an MCP tool's input schema; Claude Code now sends that tool without parameters for the rest of the conversation
- **[UNCOVERED]** - Fixed resuming a headless or Agent SDK session losing the recent messages a compaction had kept, when the compaction followed a reply cut at the output token limit (compactions from this version on)
- **[UNCOVERED]** - Fixed Claude not being told about an MCP server's tools and instructions until its next tool call, when the server finished connecting after a compaction
- **[UNCOVERED]** - Fixed Remote Control sessions being marked stopped while still running, on a computer serving several sessions at once
- **[UNCOVERED]** - Fixed resuming a headless or Agent SDK session losing its compaction summary or bringing back pre-compaction history, when the compaction followed a retried or unfinished reply in the same turn
- **[UNCOVERED]** - Fixed Claude polling a background command's output file or sleeping while it runs
- **[UNCOVERED]** - Fixed feature flags and staged rollouts staying stale behind a TLS-inspecting proxy whose certificate is trusted only through the OS certificate store
- **[UNCOVERED]** - Fixed `claude daemon stop --any` printing "stopped" while a stuck background service kept running: it now waits, force-kills the service, and says so with exit 1 if it is still there
- **[UNCOVERED]** - Fixed `claude daemon stop` exiting with no output, and leaving sessions listed as running, when telemetry is turned off
- **[UNCOVERED]** - Fixed Write, Edit and NotebookEdit in Cowork cloud sessions reporting success for a path on your own computer, where the file never arrived
- **[UNCOVERED]** - Fixed Claude searching for deferred tools already loaded earlier in the conversation when a session resumes a history that never listed them
- **[UNCOVERED]** - Fixed secondary (dim) text looking the same as normal text under the dark ANSI theme and on 16-color terminals
- **[UNCOVERED]** - Fixed cloud sessions hanging 5 minutes per turn when the organization's policy can't be read; the turn now ends promptly and says why
- **[UNCOVERED]** - Fixed a cloud session sometimes running an already answered message a second time after the session restarted during a long reply
- **[UNCOVERED]** - Self-hosted runner: Fixed the runner and orchestrator freezing (no polls, `/healthz` or `SIGTERM` shutdown) while nobody reads their output; logs keep the latest 256 KiB and count drops (not on Windows)
- **[UNCOVERED]** - Improved WebFetch in Cowork cloud sessions to tell Claude that a page failed moments ago instead of fetching it again
- **[UNCOVERED]** - Improved mod sharing in the built-in `plugin-authoring` skill: Claude scans a mod's files for keys before opening them, and asks before scanning a folder outside the project
- **[UNCOVERED]** - Improved the note Claude 3 models get about an @-mentioned PDF, so they less often answer without reading it
- **[UNCOVERED]** - Improved artifact updates: Claude now applies a small change and republishes the artifact in one call, and makes larger edits and republishes within a single response
- **[UNCOVERED]** - Changed `CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST` sessions to ignore CA-bundle, tool-proxy, git TLS and git config variables like `SSL_CERT_FILE` in settings; under Claude Desktop, only in project settings
- **[UNCOVERED]** - Changed exit to force-kill background commands still running 1.5 seconds after being asked to stop; in fullscreen mode they could previously be left running
- **[UNCOVERED]** - Changed Claude Desktop's Code tab to apply managed settings when `forceLoginGatewayUrl` names an Anthropic-operated gateway that serves the session's hostname; that gateway must be reachable at start
- **[UNCOVERED]** - Changed `claude gateway` to stop at start, naming the key, on a `desktop:` policy key that Claude Desktop cannot use from a gateway, where it earlier started with a warning
- **[UNCOVERED]** - Changed large requests to api.anthropic.com to use gzip compression even when telemetry is disabled; set `CLAUDE_CODE_GZIP_REQUEST_BODIES=0` to turn it off
- **[UNCOVERED]** - Changed the `claude-api` skill to leave Managed Agents sessions in place unless you ask to archive or delete them
- **[UNCOVERED]** - Changed background sessions to resume a carried workflow through the Workflow tool's approval instead of running it from the handoff file
- **[UNCOVERED]** - Changed local session transcripts to also record each API request's system prompt, tools and parameters, so a transcript you choose to share can reproduce a request exactly
- **[UNCOVERED]** - Changed the `/sandbox` mode options to read "Sandbox commands" instead of "Sandbox BashTool"
- **[UNCOVERED]** - Changed `PermissionRequest` hooks in Cowork cloud sessions: a `setMode` update in a hook's allow is now ignored; the rest of the approval still applies
- **[UNCOVERED]** - Changed hooks: `updatedInput` from PreToolUse and PermissionRequest hooks is now validated like Claude's own input: unknown keys are dropped, and input the tool rejects denies the call
- **[UNCOVERED]** - Removed the `--sandbox` and `--no-sandbox` flags from `claude remote-control`, which had no effect; passing either now exits with an error. Set `sandbox.enabled` in settings to sandbox sessions
- **[UNCOVERED]** - [VSCode] Added the `claudeCode.attachSelection` setting to stop text selected in the editor from being added to your messages
- **[UNCOVERED]** - [VSCode] Fixed fast mode staying on after usage credits ran out, which made each request be refused and re-sent; it now turns off until you turn it back on, with an error notice
- **[UNCOVERED]** - [VSCode] Fixed the Thinking toggle switching to Off on models that always think; the toggle is no longer shown for those models
- **[UNCOVERED]** - [VSCode] Fixed "Edit prompt" on a flagged message opening the file or command menu over the restored prompt; Enter now sends it as written
- **[UNCOVERED]** - [VSCode] Fixed Shift+dragging a file onto the prompt on Windows inserting an unreadable `/c:/…` path instead of a mention relative to the working directory
- **[UNCOVERED]** - [VSCode] Fixed changes to VS Code's chat font size settings needing a window reload or being undone by a theme change; diffs and the plan preview now follow them too
- **[UNCOVERED]** - [VSCode] Fixed "Resume session" and tabs restored after a reload opening an empty new conversation instead of one that had moved into a git worktree
- **[UNCOVERED]** - [VSCode] Fixed ↑ then Enter on a recalled slash command running it without its arguments; the command and file menus no longer open over a recalled prompt until you edit it
- **[UNCOVERED]** - [VSCode] Fixed Shift+dragging a file from the Explorer or an editor tab onto the prompt inserting nothing in WSL, SSH and Dev Container windows
- **[UNCOVERED]** - [VSCode] Fixed Ctrl+Alt+F toggling Focus view instead of opening Find in the Explorer, other tree views, or the Debug Console on Windows and Linux
- **[UNCOVERED]** - [VSCode] Fixed the check for sessions open in other windows or terminals creating extra processes on macOS: it now starts `/bin/ps` directly instead of searching PATH for `ps` on every check
- **[UNCOVERED]** - [VSCode] Windows: Fixed a conversation showing "still open somewhere else" after a crash or power loss, when Windows had since restarted and given the old process ID to another program
- **[UNCOVERED]** - [Cloud sessions] Fixed "Allow for this task" missing from Cowork's approval prompts for connector tools where an organization turns off "Always allow" (regression in 2.1.292)
- **[UNCOVERED]** - [Cloud sessions] Fixed most commands in the / menu losing their descriptions in cloud sessions once you sent a second message
- **[UNCOVERED]** - [Remote Control] Fixed the diff view in Remote Control sessions on claude.ai and the desktop app showing deleted and renamed files as modified; requires Claude Code v2.1.296 or later on your machine
- **[UNCOVERED]** - [Claude Tag] Added support for Slack Connect channels: an Owner or Claude Tag admin can let Claude in Slack answer in channels shared with another organization; it's off by default
- **[UNCOVERED]** - [Claude Tag] Added a private Allow once / Deny card in Slack threads for connector actions that need your approval, so Claude asks instead of refusing; others only see that it's waiting on you
- **[UNCOVERED]** - [Claude Tag] Added support for Slack voice clips in Claude in Slack: Claude reads Slack's transcript of a clip when Slack has one
- **[UNCOVERED]** - [Claude Tag] Fixed Claude in Slack not answering another app that tags it in a thread under a message Claude itself posted to the channel
- **[UNCOVERED]** - [Claude Tag] Changed access bundles an admin attached to a Slack channel to keep applying once the channel becomes a Slack Connect channel, with no need to remove and re-attach them
- **[UNCOVERED]** - [Code Review] Fixed Code Review ignoring `@claude review` comments from people with write access whose GitHub organization membership is private; their comments now start a review
- **[UNCOVERED]** - [Code Review] Fixed Code Review's "paused for this repository" comment sending admins to Code Review settings; it now says who can fix it and links the Git providers page

#### v2.1.299 — released 2026-10-14

- **[covered]** - Fixed `claude mcp add <name> -- <command> --background` being started as a background session
  - Covered by: `cc-native/sessions/CC-session-lifecycle-analysis.md`
- **[covered]** - Self-hosted runner: Improved what `setup` and `doctor` say when the runner's machine has no git credentials
  - Covered by: `cc-native/ci-remote/CC-version-pinning-resilience.md`, `cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md`
- **[UNCOVERED]** - Added `CLAUDE_CODE_DISABLE_FILE_MENTIONS` environment variable: Claude gets the paths of `@` file mentions to read with its file tools, not the files' contents
- **[UNCOVERED]** - Added idle compaction in the terminal: a 200K+ token conversation left idle for about 54 minutes is compacted before its one-hour prompt cache expires, so your next message doesn't reprocess it all
- **[UNCOVERED]** - Added `CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS` to change idle compaction's 200K-token minimum; `"idleCompaction": false` in settings.json turns it off. Both need v2.1.290 or later
- **[UNCOVERED]** - Added `$.prompt.media` so a `prompt.submit` hook of a mod installed by managed settings can read the bytes of an image or document attached to the prompt
- **[UNCOVERED]** - Added `$.session.identity()` for mods installed by managed settings: how the session is signed in, and its organization and email when managed `forceLoginOrgUUID` lists that organization
- **[UNCOVERED]** - Added `size`, `weight`, `mono` and `tabular` to a mod's `Text` and named spacing steps (`xs` to `xl`) to its `Box`; `bold` is deprecated in favor of `weight`
- **[UNCOVERED]** - Added `--shutdown-drain-sec` to `claude self-hosted-runner orchestrator`: on SIGTERM it stops polling and gives the poll in flight and running spawn hooks up to that many seconds to finish
- **[UNCOVERED]** - Added the skill's frontmatter, source, plugin name and file path to what a mod's `skill.prompt` hook receives
- **[UNCOVERED]** - Added `/effort` and `/fast` in agent view to set what new sessions start with; a bare `/model`, `/effort` or `/fast` there now opens a picker
- **[UNCOVERED]** - Added a "safe mode" line to the agents view peek panel for background sessions started with `--safe-mode`
- **[UNCOVERED]** - Added a one-time note when plan mode won't ask before most edits or commands because bypass permissions is available
- **[UNCOVERED]** - Added `--disallow-tools` and a `disallowed_tools` case field to `claude plugin eval` to keep specific built-in tools, such as Agent, out of eval runs
- **[UNCOVERED]** - Added support for turning off the attribution block in Claude Desktop's Code tab: set `CLAUDE_CODE_ATTRIBUTION_HEADER=0` in the `env` of a Claude apps gateway's `code` policy
- **[UNCOVERED]** - Added a field to the attribution block in Claude Code sessions behind a Claude apps gateway; remove the block with `CLAUDE_CODE_ATTRIBUTION_HEADER=0`
- **[UNCOVERED]** - Added a `queue` door to the `session.append` mod hook, so a mod can make the transcript's queue records differ from the prompt as sent
- **[UNCOVERED]** - Added a note in `/plugin` and `claude plugin validate` naming a mod's hooks that are skipped where an organization manages Claude Code
- **[UNCOVERED]** - Added `/usage` warnings for max effort, workflows, always-on context and large tool results
- **[UNCOVERED]** - Fixed the error for a denied cloud session, which could point to the wrong organization when a key from `apiKeyHelper` was in use
- **[UNCOVERED]** - Fixed sessions on a gateway-specific model name behind a custom `ANTHROPIC_BASE_URL` ending with "Prompt is too long · automatic compaction failed" near 200K tokens instead of sending the request
- **[UNCOVERED]** - Fixed a mod that submits a prompt at the end of every turn keeping a headless run going past `--max-turns`, `--max-budget-usd`, an interrupt, or the end of the host's conversation
- **[UNCOVERED]** - Fixed cloud sessions sometimes showing the model's follow-up text after a tool group's one-line label
- **[UNCOVERED]** - Fixed the Write and Edit tools creating a mod in a session's mods folder without asking in accept-edits mode when the config directory's path has no `.claude` in it
- **[UNCOVERED]** - Fixed installed mods that kept running in an open session after being turned off remotely; they now unload between turns
- **[UNCOVERED]** - Fixed Edit and Retry in Cowork and claude.ai cloud sessions failing on a message stopped while its `UserPromptSubmit` or mod `prompt.submit` hooks were still running (regression in 2.1.296)
- **[UNCOVERED]** - Fixed an agent teammate started without a description keeping part of a credential from its prompt in the task description shown for it
- **[UNCOVERED]** - Fixed the claude.ai view of a Remote Control or cloud session freezing when a large batch of events could not finish uploading over a slow connection
- **[UNCOVERED]** - Fixed a sandboxed shell command being able to write into a `--plugin-dir` folder, whose code Claude Code reloads and runs outside the sandbox
- **[UNCOVERED]** - Fixed memory growth under heavy debug logging (`--debug`, `--debug-file`), and a hang on exit when the debug log is on a disk or network mount that stops accepting writes
- **[UNCOVERED]** - Fixed memory growing without bound when debug output goes to stderr and the parent process stops reading it
- **[UNCOVERED]** - Fixed rm prompts on shell `-c` scripts that don't run `rm`. An rm built at run time in a script Claude Code can't read no longer prompts unless `CLAUDE_CODE_STRICT_INLINE_SHELL_RM_PROMPT=1`
- **[UNCOVERED]** - Fixed double-clicking a word in an expanded transcript row in fullscreen mode collapsing the row instead of selecting the word
- **[UNCOVERED]** - Fixed `claude mcp list`, `claude doctor` and `/status` reporting an empty `.mcp.json` as invalid
- **[UNCOVERED]** - Fixed `/btw` jumping the transcript to the bottom when asked while scrolled up in fullscreen
- **[UNCOVERED]** - Fixed sandboxed commands failing on WSL2 with `bwrap: Can't mkdir /mnt/c/Program Files/ClaudeCode` when the sandbox can write to the Windows drive
- **[UNCOVERED]** - Fixed scheduled wakeups (ScheduleWakeup) not firing while a background task was running in Agent SDK, IDE and `claude remote-control` sessions
- **[UNCOVERED]** - Fixed a mod's `prompt.submit` rewrite being silently dropped, sending the prompt as typed, for some prompts with a pasted image or an image that can't be read
- **[UNCOVERED]** - Fixed a Remote Control prompt being lost when another queued prompt in the same batch failed to deliver
- **[UNCOVERED]** - Fixed a Remote Control prompt that had passed its hooks being dropped from prompt history when Stop interrupted the next queued prompt's hook
- **[UNCOVERED]** - Fixed sign-in, MCP servers and project trust appearing lost on Linux after a sandboxed command left an empty `.config.json` in the config directory
- **[UNCOVERED]** - Fixed `/sandbox` reporting success when its setting could not be saved because the project folder is not writable; it now says nothing changed and why
- **[UNCOVERED]** - Fixed SDK and headless sessions staying in auto mode after the host switched to a model that doesn't support auto mode
- **[UNCOVERED]** - Fixed MCP servers named `constructor` or `prototype` in an MCP config never being connected
- **[UNCOVERED]** - Fixed tools of an MCP server named `constructor` or `toString` asking for permission in auto mode and bypass permissions mode
- **[UNCOVERED]** - Fixed a spurious "synced[0] commands path not found" plugin error at startup when another Claude Code process had just updated a claude.ai-synced plugin
- **[UNCOVERED]** - Fixed the Artifact tool advising a retry when a publish that requests connectors or other access was refused by the server or a proxy (HTTP 403); it now says so and what to tell the user
- **[UNCOVERED]** - Fixed Cowork cloud sessions staying on an old account plugin after a plugin reload that timed out or a restart that reused a recent sync
- **[UNCOVERED]** - Fixed document blocks being dropped from your own message sent while Claude is working
- **[UNCOVERED]** - Fixed Claude in Chrome asking for permission while no browser is connected; it now says the extension is not connected
- **[UNCOVERED]** - Fixed the fullscreen "Update installed" notice being hidden behind the idle "/clear to save tokens" hint; it now shows beside the hint
- **[UNCOVERED]** - Fixed a mod hook, with or without a `.catch`, being run again without end when it waits on another mod's noun that does its work outside the call
- **[UNCOVERED]** - Fixed the Claude apps gateway serving models that a policy's `availableModelsMatch: exact` or `deniedModels` blocks; it now answers 400 and leaves them out of its model lists
- **[UNCOVERED]** - Fixed the server-managed settings request to Anthropic carrying a third-party gateway's API key when a managed settings file sets `ANTHROPIC_BASE_URL`
- **[UNCOVERED]** - Fixed streams through a custom `ANTHROPIC_BASE_URL` being aborted after 180 seconds with no data arriving; they now wait 300 seconds, whether or not feature flags are loaded
- **[UNCOVERED]** - Fixed a mod's `tool.describe` or `prompt.section` answer that changed after `$.ui.invalidate` never reaching Claude; the new answer is now sent on the next turn
- **[UNCOVERED]** - Fixed a settings file being ignored when `enabledMcpjsonServers` or `disabledMcpjsonServers` held a single server name (letters, digits, - or _) as a plain string
- **[UNCOVERED]** - Fixed `claude plugin test` pausing a hook's time budget while a served `$` method it had called kept making `$` calls after answering
- **[UNCOVERED]** - Fixed high memory use after resuming a cloud or Remote Control session that had run many subagents
- **[UNCOVERED]** - Fixed plugin hooks being skipped when they pass a very deeply nested tool input or message on with next()
- **[UNCOVERED]** - Fixed a value a mod's hook passes to `next()`, returns, or sends to a `$` method being refused whole when one of its getters throws a `RangeError`; now only that key is refused
- **[UNCOVERED]** - Fixed `/usage`, the approaching-limit warning (terminal and VS Code) and the status line sometimes showing more than 100% used (anthropics/claude-code#92238)
- **[UNCOVERED]** - Fixed wrapped text mixing CJK or emoji with Latin words losing its last line or leaving a blank row at some terminal widths
- **[UNCOVERED]** - Fixed a cloud session sometimes ignoring the answer to a permission prompt or a question when the answer was given while the session's worker was being replaced
- **[UNCOVERED]** - Fixed bold, italic and other nested text styles running over table borders or being lost on wrapped rows
- **[UNCOVERED]** - Fixed Cowork cloud sessions running the old version of an account plugin changed, removed or disabled from another device until the session restarted
- **[UNCOVERED]** - Fixed deny and ask rules for an MCP server (`mcp__<server>`) not applying when the server's normalized name contains a double underscore
- **[UNCOVERED]** - Fixed long conversations losing newly attached images on every turn after one oversized image was refused by the API
- **[UNCOVERED]** - Fixed the `plugin_loaded` telemetry event reporting `has_hooks` as false for plugins whose hooks are a hooks module, built-in plugins included
- **[UNCOVERED]** - Fixed images attached while Claude is working (VS Code, desktop app, SDK) being sent at full size, which led to repeated image errors in long conversations
- **[UNCOVERED]** - Fixed the image coordinate hint being missing or slightly off for large near-square images on newer models
- **[UNCOVERED]** - Fixed feature flag, startup, fast mode, profile and feedback requests to Anthropic carrying the API key configured for a third-party gateway (`ANTHROPIC_BASE_URL`); Anthropic API keys are still sent
- **[UNCOVERED]** - Fixed a mod's hot reload ignoring a fix saved right after a failed reload; saving a mod file without changing it no longer reloads the mod
- **[UNCOVERED]** - Fixed mods loaded from source files being refused when a hook hands `$` to a function declaration imported from another file of the mod
- **[UNCOVERED]** - Fixed a regression in 2.1.296 where cloud and headless sessions could run an approved tool call twice if a new message arrived as the session resumed after a restart
- **[UNCOVERED]** - Fixed scheduled tasks being announced for the wrong minute: the scheduling tools now report each job's actual next run time
- **[UNCOVERED]** - Fixed mods' hooks being handed values with `__proto__` keys silently removed, which could skip a `tool.check` guard on a tool call another mod made
- **[UNCOVERED]** - Fixed `claude -p` saying nothing when a settings file fails validation: text-output runs now list the file and the invalid entry on stderr
- **[UNCOVERED]** - Fixed long pastes in terminals without bracketed paste losing all text after an invisible control character, such as a mis-decoded curly quote
- **[UNCOVERED]** - Fixed managed settings and organization policy not being fetched when the stored login's plan was changed locally on machines whose MDM or managed-settings file sets `forceLoginOrgUUID`
- **[UNCOVERED]** - Fixed MCP connections over HTTP hanging for 30 seconds and failing when a server never ends the body of its reply to a notification (anthropics/claude-code#99014)
- **[UNCOVERED]** - Fixed MCP servers added to a running headless or SDK session being connected before some policy checks ran; a blocked server is now reported as failed without being contacted
- **[UNCOVERED]** - Fixed `claude mcp list`, `claude mcp get` and subagent MCP servers starting a server that a policy check blocks; it is now reported as blocked without being started
- **[UNCOVERED]** - Fixed `/reload-plugins` not loading a plugin installed from another terminal a moment earlier
- **[UNCOVERED]** - Fixed blank rows appearing under CJK and emoji text squeezed into a one-cell column, as in a very narrow terminal
- **[UNCOVERED]** - Fixed text cut in the middle beside wide characters leaving a cell unused or being cut twice, and an emoji vanishing where a color changed inside it
- **[UNCOVERED]** - Fixed bare mode notices in background sessions telling you to restart without `--bare`, which keeps the mode; they now name `/stop` and `claude --resume`, as safe mode ones do
- **[UNCOVERED]** - Fixed `←` not saying why it stayed put over a queued message while Remote Control is on
- **[UNCOVERED]** - Fixed `$.http.fetch` in mods refusing a `304`, `204` or `205` response that declares a `Content-Length` over the 4 MiB body limit
- **[UNCOVERED]** - Fixed `/config` push notification toggles sending your account the previous setting instead of the one you just chose
- **[UNCOVERED]** - Fixed a cloud session leaving a reply unfinished when its worker was replaced just after the reply hit the output token limit
- **[UNCOVERED]** - Fixed Read failing on PDF page ranges in remote sessions on Linux that run without elevated privileges
- **[UNCOVERED]** - Fixed Enter answering a question or permission prompt that had been held back while you typed an unsent message
- **[UNCOVERED]** - Fixed a file attached to a message in a remote session being left out when its download stalled part way; the download is now tried again
- **[UNCOVERED]** - Fixed queued prompts sent as content blocks over `--input-format stream-json` running together without a line break when merged into one turn
- **[UNCOVERED]** - Fixed self-hosted runner sessions shutting down MCP servers added through an `--exec-path` wrapper's own `--mcp-config` when connectors change mid-session
- **[UNCOVERED]** - Fixed `claude plugin eval` passing runs that the API refused: a run that ends on an API error now scores 0 without grading and makes the suite exit 1
- **[UNCOVERED]** - Fixed permission prompts cutting off or wrapping too early when the reason text contains keycap or joined emoji
- **[UNCOVERED]** - Fixed `forceLoginOrgUUID` and `forceLoginMethod` from MDM or the managed-settings file being hidden or replaced by server-managed settings
- **[UNCOVERED]** - Fixed `--bare` sessions leaving out an MCP server named `constructor` or `prototype` that `--channels` asked for
- **[UNCOVERED]** - Fixed resuming a conversation from before `/clear` reattaching to the Remote Control session of the conversation after it
- **[UNCOVERED]** - Fixed a prompt starting with `/`, sent with the Agent SDK's `verbatimPrompts` option, running as a slash command when `CLAUDE_CODE_RESUME_INTERRUPTED_TURN` re-ran it after a restart
- **[UNCOVERED]** - Fixed background sessions started with `--safe-mode` silently leaving safe mode when the session was woken or restarted
- **[UNCOVERED]** - Fixed scheduled tasks and loops firing again after every turn, or firing early, during the repeated hour when daylight saving time ends
- **[UNCOVERED]** - Fixed the diff view listing a new file whose name begins or ends with a space under the wrong name
- **[UNCOVERED]** - Fixed MCP tool calls in headless and SDK sessions sometimes failing or running twice when a background reconnect closed the connection they were running on
- **[UNCOVERED]** - Fixed `/btw` side questions in non-interactive sessions not being cancelled when the session ends, and running a second time when the same request arrived again mid-run
- **[UNCOVERED]** - Fixed sandboxed commands on macOS being able to read or write a denied path by its real location when the denied path passes through a symlink
- **[UNCOVERED]** - Fixed sandbox `denyRead` and `allowRead` globs with braces, parentheses or backslashes in a folder's name being read differently by Claude Code's settings checks than by the sandbox
- **[UNCOVERED]** - Fixed sandbox glob `allowRead` and `allowWrite` entries not being re-checked when the directory they start from is replaced by a symlink
- **[UNCOVERED]** - Fixed worktree-isolated sessions accepting some awk programs the isolation guard should refuse
- **[UNCOVERED]** - Fixed a prompt or reply of `--bg` or `--background` to a background session being taken for the flag, which could start new sessions over and over instead of delivering it
- **[UNCOVERED]** - Fixed a custom slash command's embedded shell line running twice when a newer message interrupted the command while its prompt was being checked
- **[UNCOVERED]** - Fixed `--worktree` sessions leaving a folder behind in `.git/worktrees` in repositories using git's reftable ref storage
- **[UNCOVERED]** - Fixed `claude self-hosted-runner` sessions using Anthropic-managed git showing tracked files as staged deletions when starting in a reused clone whose remote is still empty
- **[UNCOVERED]** - Fixed Ultracode not being announced to scheduled tasks and other delivered headless turns when `ultracode` is on in settings
- **[UNCOVERED]** - Fixed MCP OAuth sign-in, token refresh and sign-out not sending configured `headers`/`headersHelper` values, which broke servers behind an authenticating proxy
- **[UNCOVERED]** - Fixed the Artifact tool reporting a spurious one-line difference against the live page, and refusing the publish, when a large page with a line break after `<head>` is published again unchanged
- **[UNCOVERED]** - Fixed `$.ui.open` reporting a mod's pane as placed in sessions where no surface draws it, such as Claude Code for VS Code and `claude -p`
- **[UNCOVERED]** - Fixed the `agent.spawn` mod hook not running when a finished subagent or a killed teammate is resumed: the hook's event now carries `resume`, and a mod can refuse it
- **[UNCOVERED]** - Fixed `claude plugin validate` rejecting a mod's `$.state` references when `plugin.json` has no `types` key and the contract is at `./types/index.d.ts`
- **[UNCOVERED]** - Fixed a mod's `dimColor` text looking the same as plain text under the dark ANSI theme and on 16-color terminals
- **[UNCOVERED]** - Fixed plan mode running a write (an MCP tool's, a file's, a shell command's) that a `PreToolUse` hook or a mod's `tool.check` hook allowed
- **[UNCOVERED]** - Fixed background subagents in auto mode sometimes sending their final report twice, once as the result and once as a message
- **[UNCOVERED]** - Fixed `SendMessage` not finding a subagent by name after the CLI restarted and resumed the session (names given before the last compaction still need the agent ID)
- **[UNCOVERED]** - Fixed replies cut off at the output token limit ending the turn silently, with no retry or error, after a request fell back to non-streaming mode
- **[UNCOVERED]** - Fixed Read garbling UTF-16LE files with a byte-order mark, and Write dropping byte-order marks or silently converting Windows-1252, Shift-JIS, GBK or UTF-16BE files to UTF-8 (now refused)
- **[UNCOVERED]** - Fixed cloud sessions sometimes leaving a message unanswered when the worker was replaced right after a compaction
- **[UNCOVERED]** - Fixed cloud sessions and `CLAUDE_CODE_RESUME_INTERRUPTED_TURN` sometimes answering a finished turn again after a restart, when a tool ended the turn and a skill loaded in the same step
- **[UNCOVERED]** - Fixed photos sent over Remote Control being dropped when their copy could not be saved on your computer; Claude now still sees the photo
- **[UNCOVERED]** - Fixed files sent over Remote Control sometimes not arriving in long-running sessions
- **[UNCOVERED]** - Fixed files of 30 to 35 MiB sent over Remote Control or to a cloud session not arriving
- **[UNCOVERED]** - Fixed a user-installed mod's `$.env.set` changing the environment or shell prefix that command hooks from managed settings start with
- **[UNCOVERED]** - Windows: Fixed the process-liveness check leaving orphaned PowerShell processes behind on busy machines until memory ran out
- **[UNCOVERED]** - Windows: Fixed PreToolUse and PermissionRequest hooks that set no shell failing open when Git for Windows isn't installed; a guard that fails now blocks the call
- **[UNCOVERED]** - Windows: Fixed Bash commands failing with "command not found" for a whole session when Git Bash did not report its PATH at startup
- **[UNCOVERED]** - Self-hosted runner: Fixed sessions that wrote output before their first turn being left with no release timer, ignoring `--retire-at` and delaying shutdown
- **[UNCOVERED]** - Improved the error shown when a cloud session is refused because your claude.ai login was rejected or has expired: it now tells you to sign in again with `claude auth login`
- **[UNCOVERED]** - Improved enforcement of managed permission rules, managed hooks and organization MCP tool names against user-installed mods
- **[UNCOVERED]** - Improved memory and disk use when PDFs are @-mentioned: their bytes are no longer kept in the session transcript
- **[UNCOVERED]** - Improved sandboxed Bash on Linux: Esc and Ctrl-C now work while wildcard read rules are being expanded for a command
- **[UNCOVERED]** - Improved the startup warning for an unrecognized model ID: it is now one short line under the welcome banner with a docs link, instead of a long raw message
- **[UNCOVERED]** - Improved the plugin-authoring skill's steps for sharing a mod: Claude asks public or private and checks the files before creating a GitHub repository
- **[UNCOVERED]** - Improved the Skill tool's "Unknown skill" error to suggest a skill's listed name when Claude wrongly adds the `anthropic-skills:` prefix to it
- **[UNCOVERED]** - Improved `/reload-skills` to say it re-sends the full skill list to Claude, which is how to get skills back after compaction
- **[UNCOVERED]** - Improved the error shown when a worktree cannot be created because its base commit does not resolve: it now says how the lookup ended and the likely reasons, such as a repository without a commit
- **[UNCOVERED]** - Improved the error for creating a worktree at a bare-repository layout's root: it now explains the layout instead of an unrelated git error
- **[UNCOVERED]** - Improved artifact watching: a local session can now watch up to 25 published artifacts at once, up from 10
- **[UNCOVERED]** - Improved background agent notifications: they now say when an agent is only waiting on its own background work, got a message too late for its result, or was stopped by a usage limit
- **[UNCOVERED]** - Changed plugin hooks and workflow scripts to refuse values they hand back that nest deeper than 28,000 levels, with an error naming the limit (workflow scripts allowed 100,000)
- **[UNCOVERED]** - Changed actions a plugin hook can block to be refused, not let through, when the hook cannot be handed them or cannot hand back its answer; a tool that already ran has its result withheld
- **[UNCOVERED]** - Changed requests to claude.ai's connector proxy and to Anthropic-hosted MCP servers to no longer follow HTTP redirects; redirects by a connector's own server are unaffected
- **[UNCOVERED]** - Changed MCP requests in cloud and self-hosted runner sessions to no longer follow HTTP redirects from the session's MCP proxy
- **[UNCOVERED]** - Changed skill and command loading: one whose file or folder name has hidden, direction-changing or blank-like characters, `<` or `>` is no longer offered until renamed; such a `name:` is ignored
- **[UNCOVERED]** - Changed `ui.render` trees in `claude plugin test`: each mod's Box or Text root now carries `part: { plugin }` naming the mod, so exact-tree assertions must include it
- **[UNCOVERED]** - Changed WebFetch page reads to pick their effort as web searches do: the caller's level on the caller's own model, otherwise the level settings give the small model
- **[UNCOVERED]** - Changed `claude plugin test` to fail a call to a mod's served `$` method that has not answered within ten seconds, as a session does
- **[UNCOVERED]** - Changed MCP allow rules to reach only the server they name: `mcp__a` no longer allows a server named `a__b` or `a_`; write `mcp__<server>__*` with the server's whole normalized name
- **[UNCOVERED]** - Changed agent `tools:` lists to take only the named MCP server's tools; list a server whose name contains `__` as `mcp__<whole name>__*`
- **[UNCOVERED]** - Changed Claude in Chrome in Cowork cloud sessions outside auto mode: an approved-site action the safety classifier flags now asks you instead of being refused, unless managed settings apply
- **[UNCOVERED]** - Changed cloud session and Remote Control MCP connectors to negotiate MCP protocol version 2026-07-28 by default on installs that fetch no flags; `MCP_PROTOCOL_NEGOTIATION=legacy` opts out
- **[UNCOVERED]** - Changed MCP tool descriptions and server instructions from Anthropic's first-party MCP servers at `api.anthropic.com` to reach Claude in full instead of being cut at 4,096 characters
- **[UNCOVERED]** - Changed auto mode in Cowork cloud sessions: a `PermissionRequest` hook can no longer approve shell commands or subagents; those prompts wait or are denied
- **[UNCOVERED]** - Changed the resume command printed at exit: it names the session by its ID and no longer by its name, so that nothing in a session name can run when the line is pasted
- **[UNCOVERED]** - Changed the resume command printed at exit of a worktree session: it uses `-w` and `-r` if the long flags do not fit the terminal. If neither fits a kept worktree, rows above it say where to run it
- **[UNCOVERED]** - Changed `/btw` side questions in non-interactive sessions to return a timeout error when still unanswered after 11 minutes
- **[UNCOVERED]** - Changed `UserPromptSubmit` hooks to run before a skill or custom slash command expands, so a hook that blocks the prompt now also stops its embedded shell commands
- **[UNCOVERED]** - Changed a skill's own front-matter `UserPromptSubmit` hook to first run on the prompt after the one that invokes the skill
- **[UNCOVERED]** - Changed the `turn.start` mod hook to also hear subagents' and teammates' turns, not only the main loop's; tell them apart by `e.agentId` (absent on the main loop)
- **[UNCOVERED]** - Changed the errors shown when `/ultrareview` can't upload a repository to stop suggesting `git add .`, which could stage or commit untracked files such as `.env`
- **[UNCOVERED]** - Changed the cyber safeguard notice to no longer ask people to apply to the Cyber Verification Program
- **[UNCOVERED]** - [VSCode] Fixed an unsent prompt and its attachments being lost when switching to another session and back
- **[UNCOVERED]** - [VSCode] Fixed unused blank chats keeping a background Claude process running after starting a new conversation
- **[UNCOVERED]** - [VSCode] Fixed the mic button showing an internal error message when you are signed out of claude.ai; it now offers to sign you in
- **[UNCOVERED]** - [VSCode] Improved startup time in workspaces without a Python environment by starting Claude while the Python extension loads
- **[UNCOVERED]** - [VSCode] Improved startup: the model picker and slash command menu now fill in right away in a new window on a folder you've opened before
- **[UNCOVERED]** - [Cloud sessions] Fixed a memory spike that could crash a session when many of its existing output files were re-sent to it at once
- **[UNCOVERED]** - [Cloud sessions] Fixed saving an edited routine silently moving it to a different environment when its own had been deleted or wasn't in the list; the routine now keeps its environment
- **[UNCOVERED]** - [Cloud sessions] Fixed Sessions search in a self-hosted environment's admin details finding nothing when you paste the session ID from a session's link
- **[UNCOVERED]** - [Cloud sessions] Fixed the Sessions and Runners lists in a self-hosted environment's admin details saying the list is empty when a search just has no matches
- **[UNCOVERED]** - [Cloud sessions] Improved the deploy command shown when you create a self-hosted environment or environment key: it shows in full, wraps between arguments, and has a visible copy button
- **[UNCOVERED]** - [Cloud sessions] Changed deleting a self-hosted environment to turn off its routines right away, with the reason shown on each routine, instead of leaving their runs to fail
- **[UNCOVERED]** - [Remote Control] Fixed Remote Control sessions whose computer can't be reached still appearing to send your messages; your text now stays in the box and Send is off until it reconnects
- **[UNCOVERED]** - [Claude Tag] Added the ability for Claude in Slack to delete a canvas it created in a channel when someone asks it to
- **[UNCOVERED]** - [Claude Tag] Fixed Claude in Slack staying silent on untagged posts that a channel's own instructions tell it to answer, such as posts that tag someone else, in channels with guests
- **[UNCOVERED]** - [Claude Tag] Fixed Claude in Slack reporting a reply to another channel's thread as posted when it isn't a member there; it now says the reply wasn't delivered and how to fix that
- **[UNCOVERED]** - [Claude Tag] Fixed Claude in Slack sometimes ending a turn without posting its answer when a self-hosted runner's image has no python3
- **[UNCOVERED]** - [Claude Tag] Changed how Claude in Slack corrects a message it got wrong: it edits the message in place and adds a short "Edited" note instead of striking through the old text
- **[UNCOVERED]** - [Claude Tag] Changed Claude in Slack to join channels with more than 100 members quietly, with no intro message
- **[UNCOVERED]** - [Code Review] Fixed Code Review's monthly spend-limit comment and check-run card sending admins to Claude Code settings; they now link the Usage page, where that limit is set

---
_Generated by `.github/scripts/changelog-compare.py`_
## Native Sources Monitor Report

Sources checked: **3**

### anthropic-blog

- Source: Anthropic Blog — announcements and product updates
- Entries fetched: 10
- New uncovered: 1

| Entry | Section | Description |
|-------|---------|-------------|
| Oct 14, 2026PolicyPreparing for the 2026 US midterms | Anthropic Blog | Oct 14, 2026PolicyPreparing for the 2026 US midterms |

### cc-issues-enhancement

- Source: CC GitHub Issues labeled 'enhancement'
- Entries fetched: 300
- New uncovered: 0

### cc-discussions-feature-request

- Source: CC GitHub Discussions in feature-request category
- Entries fetched: 0
- New uncovered: 0

---
Total new uncovered entries: **1**

_Generated by `.github/scripts/native-sources-monitor.py`_
