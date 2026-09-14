# CC Changelog & Native Sources: New Uncovered Features Detected

## Changelog Monitor Report

Last scanned version: **2.1.215**
New versions detected: **45**

### New Versions Summary

| Version | Features | Covered | Uncovered |
|---------|----------|---------|-----------|
| 2.1.270 | 1 | 0 | 1 |
| 2.1.269 | 98 | 2 | 96 |
| 2.1.268 | 96 | 0 | 96 |
| 2.1.267 | 53 | 0 | 53 |
| 2.1.266 | 1 | 0 | 1 |
| 2.1.265 | 50 | 1 | 49 |
| 2.1.263 | 1 | 0 | 1 |
| 2.1.261 | 67 | 0 | 67 |
| 2.1.260 | 66 | 1 | 65 |
| 2.1.259 | 37 | 0 | 37 |
| 2.1.258 | 2 | 0 | 2 |
| 2.1.257 | 104 | 2 | 102 |
| 2.1.252 | 4 | 0 | 4 |
| 2.1.251 | 71 | 1 | 70 |
| 2.1.250 | 1 | 0 | 1 |
| 2.1.248 | 49 | 0 | 49 |
| 2.1.247 | 33 | 0 | 33 |
| 2.1.246 | 61 | 3 | 58 |
| 2.1.245 | 1 | 0 | 1 |
| 2.1.243 | 60 | 1 | 59 |
| 2.1.241 | 1 | 0 | 1 |
| 2.1.240 | 1 | 0 | 1 |
| 2.1.239 | 59 | 0 | 59 |
| 2.1.238 | 39 | 1 | 38 |
| 2.1.237 | 2 | 0 | 2 |
| 2.1.236 | 33 | 0 | 33 |
| 2.1.235 | 19 | 0 | 19 |
| 2.1.234 | 51 | 0 | 51 |
| 2.1.233 | 20 | 0 | 20 |
| 2.1.232 | 49 | 1 | 48 |
| 2.1.231 | 1 | 0 | 1 |
| 2.1.229 | 32 | 1 | 31 |
| 2.1.228 | 18 | 0 | 18 |
| 2.1.227 | 5 | 0 | 5 |
| 2.1.226 | 1 | 0 | 1 |
| 2.1.225 | 14 | 0 | 14 |
| 2.1.224 | 31 | 0 | 31 |
| 2.1.223 | 19 | 0 | 19 |
| 2.1.222 | 21 | 1 | 20 |
| 2.1.221 | 39 | 1 | 38 |
| 2.1.220 | 1 | 0 | 1 |
| 2.1.219 | 24 | 1 | 23 |
| 2.1.218 | 36 | 0 | 36 |
| 2.1.217 | 20 | 0 | 20 |
| 2.1.216 | 40 | 0 | 40 |

### Feature Coverage Details

#### v2.1.270

- **[UNCOVERED]** - Fixed read-only git commands in Bash unexpectedly asking for permission after a session had been running for a while (regression in 2.1.269)

#### v2.1.269

- **[covered]** - Fixed the git status Claude is told after a compaction: it is now the current status, not the one from the start of the session
  - Covered by: `cc-native/sessions/CC-session-lifecycle-analysis.md`
- **[covered]** - Fixed synced plugin MCP servers not connecting when a remote session resumes
  - Covered by: `cc-native/configuration/CC-env-vars-reference.md`
- **[UNCOVERED]** - Added `claude plugin eval`: run a plugin's eval suite against Claude Code and get scored, reproducible results (JSON + HTML report); see `claude plugin eval --help`
- **[UNCOVERED]** - Added `/output-style [name]` to list and switch output styles, including over Remote Control and in cloud and other headless sessions
- **[UNCOVERED]** - Added a diff of the files a Bash command changed to the Bash tool result when the Bash tool handles file edits (setting `bashEditDiffEnabled`)
- **[UNCOVERED]** - Added `OTEL_METRICS_INCLUDE_REPOSITORY` to tag OpenTelemetry metrics and events with `vcs.*` repository attributes; commit events get `vcs.ref.head.*` with `OTEL_LOG_TOOL_DETAILS`
- **[UNCOVERED]** - Added `CLAUDE_CODE_GATEWAY_MODEL_DISCOVERY_TIMEOUT_MS` to extend the LLM gateway `/v1/models` discovery timeout (default 3s)
- **[UNCOVERED]** - Added a spinner tip suggesting `/focus` for a view with just your prompt, a one-line work summary, and the response
- **[UNCOVERED]** - Added `CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS` (1–256) to raise the Workflow tool's per-run concurrent agent limit for inference-bound fan-outs
- **[UNCOVERED]** - Fixed the prompt cache being partially invalidated on the turn after a response was cut off at the output-token limit and automatically resumed
- **[UNCOVERED]** - Fixed a case where resuming a session after interrupting Claude mid-thought could change how earlier context was re-sent, hurting prompt-cache reuse
- **[UNCOVERED]** - Fixed F1/F2/F4 not working in kitty-protocol terminals and Delete in st, Alt+arrows acting as Escape in rxvt-unicode, and Shift+punctuation typing the unshifted key in WezTerm (regression in 2.1.247)
- **[UNCOVERED]** - Fixed remote and headless sessions reporting "waiting for your input" while background agents were still running (set `CLAUDE_CODE_BG_TASKS_REPORT_RUNNING=0` to restore the old behavior)
- **[UNCOVERED]** - Fixed the terminal's replies to capability queries (`^[[?1;2c`) appearing as stray text at startup in some terminals
- **[UNCOVERED]** - Fixed rows at the top or bottom of the transcript going blank in fullscreen after resizing the terminal
- **[UNCOVERED]** - Fixed a deny or ask permission rule starting with `!` applying beyond the settings source that wrote it; such a rule now applies only within its own source, and a bare `!` negation is ignored
- **[UNCOVERED]** - Fixed resumed headless sessions losing a turn's replies when the model was switched or a request was retried mid-turn
- **[UNCOVERED]** - Fixed terminal escape codes, line breaks and oversized text from a background task's on-disk record reaching the task list and task notifications when work is resumed
- **[UNCOVERED]** - Fixed CMYK JPEG images failing to attach with "cannot decode"; they are now converted and resized like other JPEGs
- **[UNCOVERED]** - Fixed the managed settings approval dialog not naming the collector for a gRPC telemetry endpoint set without a scheme
- **[UNCOVERED]** - Fixed plugin `headersHelper` consent prompts showing a URL path that could be misread as a different host
- **[UNCOVERED]** - Fixed plugin errors showing `[redacted URL]` in place of a relative Windows path with a folder name that starts with `@`
- **[UNCOVERED]** - Fixed missing cursor in the permission-rule, auto-mode-rule, add-directory, session-rename and feedback-review text fields when the terminal's native cursor is enabled
- **[UNCOVERED]** - Fixed repeated clicks on a `/fork` receipt, each under a second apart, never backgrounding the session right away while it waited for the current tool to finish
- **[UNCOVERED]** - Fixed plugin LSP servers that reject `shutdown` params (e.g. rust-analyzer) being left running at session end; `exit` is now sent even if `shutdown` fails
- **[UNCOVERED]** - Fixed the attribution reminder overriding a CLAUDE.md or memory rule against commit and pull request attribution; lines set by managed settings still apply
- **[UNCOVERED]** - Fixed prompt suggestions being dropped for text in Japanese, Chinese, Thai and other languages written without spaces between words
- **[UNCOVERED]** - Fixed synchronized output being assumed from the terminal's name in GNOME Terminal and Konsole versions that do not support it
- **[UNCOVERED]** - Fixed `permission_denials` in `--output-format stream-json` results omitting Read, Edit and Write calls blocked by a path-scoped deny rule
- **[UNCOVERED]** - Fixed sessions run through the SDK or the desktop app showing an unknown status in other sessions' agent list
- **[UNCOVERED]** - Fixed `/insights` failing on Bedrock, Vertex, Foundry, and gateway deployments whose account can't reach the default Opus model by using the session model there instead
- **[UNCOVERED]** - Fixed organization policy limits not loading for the session when another Claude Code process refreshed the login at the same moment
- **[UNCOVERED]** - Fixed Claude Desktop sessions using Bedrock, Vertex, or a gateway not getting the contextual "what Claude needs" turn-end notification text
- **[UNCOVERED]** - Fixed MCP servers reconnecting when an updated config only changed the order of the server URL's query parameters
- **[UNCOVERED]** - Fixed the prompt box's top border splitting into extra lines when viewing a background agent whose name or description has line breaks or is wider than the terminal
- **[UNCOVERED]** - Fixed sessions getting permanently stuck on "Prompt is too long" when auto-compaction had no complete earlier exchange to summarize (mostly Agent SDK sessions with very large prompts)
- **[UNCOVERED]** - Fixed `/goal` runs silently stalling after API errors, network drops, or token limits: the goal now retries with backoff, or pauses and says why, including until a usage limit resets
- **[UNCOVERED]** - Fixed prompt cache misses in cloud sessions by waiting briefly for server configuration before the first request
- **[UNCOVERED]** - Fixed `/btw` answers that contained made-up tool calls and output: the side question is now told not to write them, and any that appear are flagged as not executed
- **[UNCOVERED]** - Fixed `CLAUDE_CODE_RESUME_INTERRUPTED_TURN` re-running a turn that had failed with an API error over 6 hours earlier, or longer ago than `CLAUDE_CODE_RESUME_INTERRUPTED_TURN_MAX_AGE_MS` when set
- **[UNCOVERED]** - Fixed organization plugins enabled through managed settings not loading in headless sessions and on Claude Desktop (once Desktop bundles this CLI version); they load from the next session
- **[UNCOVERED]** - Fixed plugin archives extracted for a session being readable by other local users, extracted files keeping world-writable bits from the archive, and stale files surviving re-extraction
- **[UNCOVERED]** - Fixed `Edit()` deny rules and the write-path check not applying to the file a Bash `tee` command writes; a `Bash(tee:*)` allow rule no longer covers destinations outside the working directories
- **[UNCOVERED]** - Fixed stray characters like `22c`, or a terminal's color or version reply, being typed into the prompt at startup over slow connections (ssh, browser terminals)
- **[UNCOVERED]** - Fixed the terminal's block cursor showing under the interface in rxvt-unicode after leaving or re-entering fullscreen
- **[UNCOVERED]** - Fixed the cursor block staying visible after returning from an external editor in fullscreen mode on rxvt-unicode
- **[UNCOVERED]** - Fixed the interface being drawn twice after returning from an external editor (Ctrl+G) outside fullscreen mode
- **[UNCOVERED]** - Fixed the interface being drawn twice in Konsole after returning from an external editor
- **[UNCOVERED]** - Windows: Fixed PowerShell tool commands sent to the background stopping when Claude Code exits
- **[UNCOVERED]** - Improved the `/diff` panel to open fully rendered in one step instead of showing a loading state first
- **[UNCOVERED]** - Improved prompt suggestion filtering for Japanese, Chinese and Korean text: mixed-script and single-word suggestions are kept, and meta or evaluative text is dropped as it is for English
- **[UNCOVERED]** - Improved the Skill tool's "Unknown skill" error to name the plugin skill's full name when a bare name matches exactly one plugin skill
- **[UNCOVERED]** - Improved keyboard support over SSH and in unrecognized terminals: terminals that answer the kitty keyboard query (such as foot and Alacritty 0.16+) now get Shift+Enter and Ctrl+Shift shortcuts
- **[UNCOVERED]** - Improved responsiveness in long sessions: transcript updates no longer re-process the whole conversation to build the collapsed tool-use summaries
- **[UNCOVERED]** - Improved first-party sessions with telemetry disabled: an `alwaysLoad` MCP server that finishes connecting mid-conversation is usable on the next turn without a tool-search round trip
- **[UNCOVERED]** - Changed `/ultrareview --post` to post the PR comment directly when the findings arrive and print the comment link, instead of starting a second cloud session to post it
- **[UNCOVERED]** - Changed artifact database reads that save into the session scratchpad so they no longer stop for working-folder approval
- **[UNCOVERED]** - Changed skills synced from claude.ai in cloud sessions to be named `anthropic-skills:<name>`, matching Claude Desktop; the bare name still works when nothing else uses it
- **[UNCOVERED]** - [VSCode] Added an agent map: an "N agents" footer pill opens a map of the session's sub-agents with per-agent cards, Stop agent, and read-only transcripts
- **[UNCOVERED]** - [VSCode] Added a Hooks dialog to the command menu for viewing hooks and adding, editing, or removing them in user, project, and local settings; managed, plugin, and session hooks stay read-only
- **[UNCOVERED]** - [VSCode] Added live progress rows for running subagents under the tool-call groups in Focus view
- **[UNCOVERED]** - [VSCode] Added a Permission rules dialog that lists permission rules and adds or removes them in user, project, and local settings; startup-option, session-only, and managed rules stay read-only
- **[UNCOVERED]** - [VSCode] Added a Cancel button to the Switch account screen that returns to your session as the current account
- **[UNCOVERED]** - [VSCode] Fixed Focus view showing a turn started by a delivered plain-text prompt, such as a scheduled task's, as part of the previous turn
- **[UNCOVERED]** - [VSCode] Fixed the footer's prompt cache clock hiding its minutes when the panel is narrow
- **[UNCOVERED]** - [VSCode] Fixed the session list keeping sessions from the default folder when `CLAUDE_CONFIG_DIR` is set in a settings file or the `environmentVariables` setting
- **[UNCOVERED]** - [VSCode] Fixed a plan preview that finished loading late sometimes hiding its comment box or showing an older plan
- **[UNCOVERED]** - [VSCode] Fixed a plan preview accepting comments that went nowhere after its Claude tab closed
- **[UNCOVERED]** - [VSCode] Fixed the prompt cache clock and reopen notice for a session compacted after its last reply and then closed, which now reads as cold when reopened
- **[UNCOVERED]** - [VSCode] Fixed a session renamed in the extension while Remote Control is on keeping its old name on claude.ai/code
- **[UNCOVERED]** - [VSCode] Fixed the "Enable Remote Control for all sessions" toggle keeping its last position after the setting was reset to default from a terminal
- **[UNCOVERED]** - [VSCode] Fixed restored Claude tabs not counting as open in the session list after a window reload until clicked, and their row opening a second tab
- **[UNCOVERED]** - [VSCode] Fixed Switch account making a tab forget its dismissed usage-limit warnings when you sign back in as the same account
- **[UNCOVERED]** - [VSCode] Fixed a session rename being replaced by the generated name after a window reload when the session was renamed during a long turn
- **[UNCOVERED]** - [VSCode] Fixed the sidebar usage meter keeping a stale per-model weekly limit row after the account loses that limit
- **[UNCOVERED]** - [VSCode] Fixed a rare case where an @-mention sent with the keyboard shortcut while a new chat view was still starting could be inserted into the input long after the keystroke
- **[UNCOVERED]** - [VSCode] Fixed the session list jumping down when the Account & usage header appeared a moment after opening the Claude side bar
- **[UNCOVERED]** - [VSCode] Improved documents and messages written for someone other than the user: Claude now writes them for that audience and names it at the top of its reply
- **[UNCOVERED]** - [VSCode] Improved screen reader and keyboard accessibility in the slash-command menu, @-mention menu, output-style picker, Send/Stop button, permission and question cards, and onboarding checklist
- **[UNCOVERED]** - [VSCode] Changed the current-file chip in the message box: an X now removes it, replacing the Hide toggle
- **[UNCOVERED]** - [VSCode] Removed the Claude Code items from a session tab's right-click menu and the editor title bar's "..." menu; they could not act on the tab the menu was opened on
- **[UNCOVERED]** - [Claude Code on the web] Added taking back a queued message in a cloud session before Claude reads it: remove it from the queue, or press Esc or Up, and the text returns to the message box
- **[UNCOVERED]** - [Claude Code on the web] Fixed `/model default` in a cloud session leaving every later message failing in organizations that restrict which models Claude Code can use
- **[UNCOVERED]** - [Claude Code on the web] Fixed one-off scheduled routines occasionally running a second time after a transient server error
- **[UNCOVERED]** - [Claude Code on the web] Fixed routine runs that use subagents sometimes being treated as finished too early, which could skip the retry after a real failure or start a duplicate run
- **[UNCOVERED]** - [Claude Code on the web] Fixed file links in cloud session transcripts opening a GitHub 404 when Claude was working from a subfolder of the repository
- **[UNCOVERED]** - [Claude Code on the web] Changed the Cloud environments admin page to list every environment instead of capping each table at five rows behind a Show more control that could be unreachable
- **[UNCOVERED]** - [Claude Code on the web] Changed claude.ai/code for Free-plan users to open the plans page with a path to upgrade, instead of a "Disabled by org admin" page with no way forward
- **[UNCOVERED]** - [Claude Tag] Added a confirmation dialog before Connect all or Disconnect on a GitHub installation in admin settings, to guard against accidental organization-wide changes
- **[UNCOVERED]** - [Claude Tag] Fixed threads occasionally going silent after a failed turn because the failure notice was dropped when Slack briefly rate-limited it; the notice is now retried
- **[UNCOVERED]** - [Claude Tag] Fixed Claude accepting a switch to a model your organization hasn't enabled and then quietly answering with a fallback model; it now declines and says an admin can enable it
- **[UNCOVERED]** - [Claude Tag] Fixed a table posting as raw pipe text when Claude attached files to the same message; the table now posts as a normal reply and the files follow with a plain caption
- **[UNCOVERED]** - [Claude Tag] Fixed `@Claude !restart` at the top level of a channel where Claude isn't active starting an unrelated conversation; it now privately says there is nothing to restart
- **[UNCOVERED]** - [Claude Tag] Fixed plugin rows in Slack access settings showing an unlabeled raw ID with no way to turn the plugin off; they now show its name and link to the bundle that manages it
- **[UNCOVERED]** - [Claude Tag] Fixed the shared-session banner and Share dialog on sessions started from Slack claiming the whole organization could open the link; they now name the Slack channel's audience
- **[UNCOVERED]** - [Claude Tag] Improved load time of the admin settings page and its Slack channel picker, most noticeably for organizations with many channels or several connected workspaces
- **[UNCOVERED]** - [Claude Tag] Improved scheduled routines in Slack channels: a routine run can now reply in an existing thread instead of always posting a new top-level channel message
- **[UNCOVERED]** - [Claude Tag] Improved the timestamp on Claude's live progress checklists to show each reader's local time and how long ago it was updated, instead of a fixed UTC time

#### v2.1.268

- **[UNCOVERED]** - Added to the Claude apps gateway: with `pricing:` set in `gateway.yaml`, signed-in Claude Code clients receive the same rates through managed settings, so `/cost` and telemetry match the spend meter
- **[UNCOVERED]** - Added a startup warning for gateways when `access_control.allow_cidrs` is empty, and a one-time warning the first time a request arrives from a public address
- **[UNCOVERED]** - Added the `gatewayInternalNetworks` managed setting, letting administrators allow `/login` to a Claude apps gateway on their organization's own public IPv4 block
- **[UNCOVERED]** - Added `claude self-hosted-runner --remove-session-state` (default off): delete each session's per-session directories under `<base-dir>/_sessions/` when the session ends
- **[UNCOVERED]** - Added `configDirectory` to the output of `claude auth status --json`
- **[UNCOVERED]** - Added `--json` to `claude plugin install`, `uninstall`, `update`, `enable` and `disable`, and `errorDetails`/`noteDetails` to each row of `claude plugin list --json`
- **[UNCOVERED]** - Added browser-tab icons for published artifacts, chosen by Claude to match each page
- **[UNCOVERED]** - Fixed every turn failing with HTTP 400 on third-party Anthropic-compatible endpoints (`ANTHROPIC_BASE_URL`) since 2.1.265: a regex in the Artifact tool's input schema that those endpoints reject
- **[UNCOVERED]** - Fixed WebFetch hanging indefinitely on a server that keeps the response open without finishing; a fetch now fails after 300 seconds. Set `CLAUDE_CODE_WEBFETCH_DEADLINE_MS` to override the deadline (0 turns it off)
- **[UNCOVERED]** - Fixed a respawned in-process teammate picking up tools or a system prompt from a same-named agent file in a folder you have not trusted
- **[UNCOVERED]** - Fixed sustained high CPU usage: a busy loop in long-running idle sessions no longer pins a CPU core, and rapid terminal focus reports during a session recap no longer keep the CPU high
- **[UNCOVERED]** - Fixed Claude sometimes replying "your message came through empty" after an MCP tool call
- **[UNCOVERED]** - Fixed deny and ask permission rules on symlinked directories (`/etc`, `/tmp`, `/var` on macOS; `/bin` on Linux) not applying when a path was given by its real location, and Bash commands ignoring deny rules written on a symlinked path spelling
- **[UNCOVERED]** - Fixed a case where a Read or Edit deny rule did not apply when an `env -C`, `eval` or similar command the permission checker cannot analyze was on the same line
- **[UNCOVERED]** - Fixed plugin and marketplace errors showing a token or password from a git source URL
- **[UNCOVERED]** - Fixed `/mcp` and `/plugin` server details, `claude mcp list`/`get`, and MCP login errors showing secrets resolved from `${VAR}` placeholders in MCP configs
- **[UNCOVERED]** - Fixed prompt caching and extended thinking breaking mid-session for SDK sessions using `excludeDynamicSections`: the first message is no longer re-rendered each request
- **[UNCOVERED]** - Fixed entitled users being told a model is restricted after restart or in the Desktop Code tab when a cached model-access denial was stale
- **[UNCOVERED]** - Fixed a running session silently switching to the organization's default model when another Claude Code process refreshed a stale model-access entry
- **[UNCOVERED]** - Fixed long-context 429s on Fable models showing the usage-credits consent prompt instead of the 1M-context message on Pro and Team plans
- **[UNCOVERED]** - Fixed workload identity federation via a profile (as claude-code-action configures it): processes sharing the profile could fail mid-run with `401 … jti reused`
- **[UNCOVERED]** - Fixed MCP server OAuth sign-in failing with "No available ports for OAuth redirect" when the local callback port range can't be bound
- **[UNCOVERED]** - Fixed the conversation summary produced by `/compact` and auto-compact mangling text that contained `$` sequences
- **[UNCOVERED]** - Fixed resuming a conversation that ended with `/compact`: its restored-file notes now load in the same order on every resume
- **[UNCOVERED]** - Fixed SDK prompt suggestions, side questions and `/rename` sending the conversation from before a compaction
- **[UNCOVERED]** - Fixed `@` file and `/` command suggestions not appearing after recalling a previous prompt with the up arrow and editing it
- **[UNCOVERED]** - Fixed `claude agents`: pressing ← again at a natural pace to go back to the agent list no longer gets ignored until you pause for over a second
- **[UNCOVERED]** - Fixed `claude agents` session delete getting stuck when a worktree can't be removed: the message names the cause and next step, and for a git worktree ctrl+x again deletes the directory anyway
- **[UNCOVERED]** - Fixed background agent and workflow rows in the agents panel expanding to many lines when their text contained line breaks
- **[UNCOVERED]** - Fixed Claude in Slack sessions losing their Slack tools when org managed settings set an MCP allowlist
- **[UNCOVERED]** - Fixed Claude in Chrome asking to allow the host "https" when a navigation URL had a scheme but a host that could not be parsed
- **[UNCOVERED]** - Fixed the spinner wrapping onto several lines when the current task's label is long; the label and the "Next:" task line now stay within one terminal row
- **[UNCOVERED]** - Fixed the `/bug` and `/feedback` description field showing no cursor when the terminal's native cursor is enabled
- **[UNCOVERED]** - Fixed Remote Control sessions served by `claude remote-control` showing a generated name instead of their session title in `ListAgents`
- **[UNCOVERED]** - Fixed `claude plugin validate` rejecting plugin paths whose directory name begins with two dots, which the plugin loader accepts
- **[UNCOVERED]** - Fixed plugins silently skipping a default monitors file or root SKILL.md that could not be checked
- **[UNCOVERED]** - Fixed WebFetch's error for localhost and other dotless hostnames to explain why the URL is refused and suggest curl
- **[UNCOVERED]** - Fixed PermissionRequest hooks not firing in `--print` mode
- **[UNCOVERED]** - Fixed policy-helper warnings not printing on headless (`-p`) runs
- **[UNCOVERED]** - Fixed `/resume` listing a `/fork` background session under its parent's name instead of its own `⑂` fork name
- **[UNCOVERED]** - Fixed `/remote-control` and other claude.ai-gated commands to suggest `/login` when signed out instead of showing a Claude for Enterprise migration message
- **[UNCOVERED]** - Fixed `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` not extending SessionEnd hooks that have no per-hook `timeout` (they were still cancelled after 1.5 seconds)
- **[UNCOVERED]** - Fixed `/autofix-pr` and other cloud-session commands saying to retry or install the Claude GitHub App when no GitHub account is connected; they now point to `/web-setup` or the web connect page
- **[UNCOVERED]** - Fixed cloud-session commands such as `/teleport` and `/remote-env` to explain when an organization policy turns them off, instead of answering "Unknown command"
- **[UNCOVERED]** - Fixed Bash sandbox instructions over-stating confinement: no unenforced path lists when filesystem isolation is off, and strict mode no longer claims commands can never run unsandboxed
- **[UNCOVERED]** - Improved fullscreen mode: adding or removing a prompt line (Shift+Enter) now repaints as fast as typing a character instead of re-rendering the visible transcript
- **[UNCOVERED]** - Improved `--continue` / `--resume`: the conversation appears immediately instead of waiting for SessionStart hooks, and the first message no longer re-reads the whole transcript
- **[UNCOVERED]** - Improved responsiveness during tool-heavy turns by no longer redrawing the transcript for a hidden per-tool-batch reminder
- **[UNCOVERED]** - Improved startup time in projects with `.claude/workflows/` scripts: listing them no longer parses each script
- **[UNCOVERED]** - Improved auto mode denials: the message Claude receives now names the rule that blocked the action and asks Claude to try a safer method and finish unrelated work before stopping to ask you
- **[UNCOVERED]** - Improved Claude in Chrome: long page reads now stay inline instead of being saved to a file and read back
- **[UNCOVERED]** - Improved the MEMORY.md truncation warning to say how many lines were cut and where the cut starts
- **[UNCOVERED]** - Improved the terminal permission prompt for artifacts: it now leads with the ask's question
- **[UNCOVERED]** - Improved the prompt footer: an editor or `/diff` selection now shows inside the prompt input, and fullscreen mode shows Remote Control status in the header instead of the footer
- **[UNCOVERED]** - Improved the "Usage credits required for 1M context" message to say that usage credits turned on mid-session take effect after restarting Claude Code
- **[UNCOVERED]** - Improved `/plugin`: installing, enabling or disabling a plugin now takes effect when you close the menu; `/reload-plugins` is no longer needed afterwards
- **[UNCOVERED]** - Changed the system prompt on Bedrock, Vertex and Foundry to deliver environment, model and settings details as attachments, matching first-party sessions
- **[UNCOVERED]** - Changed Bedrock, Vertex and Foundry sessions to keep the tool list byte-stable across a conversation (late-connecting tools load deferred instead of rewriting it), matching first-party sessions
- **[UNCOVERED]** - Changed the task-tracking tools (TaskCreate/Get/Update/List, TodoWrite) to be offered only on Claude 3.x, Opus 4.0–4.7, Sonnet 4.0–4.6, Haiku 4.5; set `CLAUDE_CODE_ENABLE_TODO_TOOLS=1` elsewhere
- **[UNCOVERED]** - Changed the artifact data-edit permission prompt in the terminal to a card that shows the document count and who can open the artifact
- **[UNCOVERED]** - Changed local Cowork sessions set to skip all approvals: the Artifact tool now refuses a local file outside the session's folders, or behind a symlink, instead of reading it without asking
- **[UNCOVERED]** - Changed plain `WebFetch` deny and ask rules to no longer apply to Artifact tool reads and updates; use an `Artifact` rule (or `WebFetch(domain:claude.ai)`) to block or gate them
- **[UNCOVERED]** - Changed the "N MCP servers need authentication" startup notice to announce each server once instead of at every launch
- **[UNCOVERED]** - [VSCode] Fixed the session list, settings toggles, and chat tabs when `CLAUDE_CONFIG_DIR` is set in a settings file or the `environmentVariables` setting
- **[UNCOVERED]** - [VSCode] Fixed the model pill, model picker and command menu going blank in open tabs for a few seconds after a login, logout or account switch
- **[UNCOVERED]** - [VSCode] Fixed Auto disappearing from the mode picker in new-tab or just-reloaded conversations when a project or local setting overrides the model named in `~/.claude/settings.json`
- **[UNCOVERED]** - [VSCode] Fixed session names reverting to the last prompt after a window reload when a SessionStart hook is configured
- **[UNCOVERED]** - [VSCode] Fixed the footer's model pill and Remote Control pill waiting for the new tab's Claude process to start when another tab in the window is already up
- **[UNCOVERED]** - [VSCode] Fixed a second Claude process running through its full startup when a session tab's launch arrived more than half a second after its config read
- **[UNCOVERED]** - [VSCode] Fixed resuming a session from the session list ignoring `claudeCode.preferredLocation: "sidebar"` (it always opened a panel), and programmatic opens resetting that setting to "panel"
- **[UNCOVERED]** - [VSCode] Fixed Windows issues: the WSL install prompt no longer appears on machines without WSL installed, and IDE diagnostics are now returned correctly for Windows files when WSL is installed
- **[UNCOVERED]** - [VSCode] Fixed the custom style builder saving a User level style in a folder the CLI does not read when `CLAUDE_CONFIG_DIR` is set through settings
- **[UNCOVERED]** - [VSCode] Added Left and Right arrow keys to change where an always-allow permission rule is saved, for keyboard and screen reader users
- **[UNCOVERED]** - [VSCode] Added a "Claude Code: Focus last message" command that moves keyboard focus to the newest message in the conversation, for keyboard and screen reader users
- **[UNCOVERED]** - [VSCode] Changed the Manage plugins dialog to apply installs, enables, disables and uninstalls to open sessions without a restart
- **[UNCOVERED]** - [VSCode] Changed some artifact permission prompts to omit the "don't ask again" choice, matching the terminal
- **[UNCOVERED]** - [Claude Code on the web] Fixed cloud sessions running longer than about six hours silently losing files saved to persisted session folders; saves now persist for up to a day
- **[UNCOVERED]** - [Claude Code on the web] Fixed "Invalid effort level" errors when a routine resumes a session, or a session starts with no set effort, in orgs where an admin caps a model's effort
- **[UNCOVERED]** - [Claude Code on the web] Improved routine creation from a conversation: when the new routine has no connectors, Claude now says so and how to add them instead of only confirming it
- **[UNCOVERED]** - [Claude Tag] Fixed the admin settings page hanging on a loading skeleton or going blank after a transient load failure; a section that fails to load now shows a Retry button
- **[UNCOVERED]** - [Claude Tag] Added a link from a Slack channel's configure page back to the organization's Claude in Slack admin settings
- **[UNCOVERED]** - [Claude Tag] Fixed a Slack Enterprise Grid channel losing its Claude settings (repository, environment, access) after a Slack admin moved it to another workspace
- **[UNCOVERED]** - [Claude Tag] Improved how Claude explains a blocked action: it now says whether a permission check, its own decision to confirm first, or missing access stopped it
- **[UNCOVERED]** - [Claude Tag] Improved reply speed: Claude now runs several read-only lookups (searching Slack, reading a thread, finding people) at once instead of one after another
- **[UNCOVERED]** - [Claude Tag] Improved formatting of comparisons: sentence-length comparisons now come as lists instead of wide tables that scroll sideways, and long table cells wrap
- **[UNCOVERED]** - [Claude Tag] Fixed `@Claude !restart` in a thread with its own session sometimes also posting a contradictory "this thread is handled by the channel session" notice
- **[UNCOVERED]** - [Claude Tag] Improved the message shown when your Claude account is in a different organization than the Slack workspace: it now explains how to connect the workspace to your org
- **[UNCOVERED]** - [Claude Tag] Fixed Markdown links whose URL is wrapped in angle brackets showing as literal bracket text in Slack instead of a clickable link
- **[UNCOVERED]** - [Claude Tag] Fixed a workspace guest's top-level @mention in a channel where guests may use Claude sometimes getting a "your Slack account isn't connected" reply instead of an answer
- **[UNCOVERED]** - [Claude Tag] Fixed a channel's long-running session being replaced with a fresh one mid-conversation; the scheduled refresh now waits until the channel and its threads are quiet
- **[UNCOVERED]** - [Claude Tag] Fixed channel-settings cards clicked more than once telling the proposing session the change was refused after it had already applied; the outcome is now sent once
- **[UNCOVERED]** - [Claude Tag] Changed memory in public channels: each channel now keeps its own notes, and Claude no longer recalls notes it saved in other public channels; workspace notes stay shared
- **[UNCOVERED]** - [Code Review] Added a note under the still-open findings list in follow-up reviews: resolving a finding's thread, not just replying to it, stops later reviews from counting it as open
- **[UNCOVERED]** - [Code Review] Fixed reviews sometimes ending as incomplete when one of the agents verifying a finding failed midway; the review now replaces that agent and reaches a verdict
- **[UNCOVERED]** - [Code Review] Fixed a push-triggered review that was queued behind a running review still posting after the pull request had been converted to draft
- **[UNCOVERED]** - [Code Review] Fixed reviews ignoring a directory's CLAUDE.md conventions when the PR edited a root file (e.g. README.md) that only shares a name with a file that CLAUDE.md lists

#### v2.1.267

- **[UNCOVERED]** - Added `maxEffortLevel` setting (top-level or per model under `modelSettings`): caps the effort level on every provider, including Bedrock, Vertex and Foundry; users can still pick a lower level
- **[UNCOVERED]** - Added `--system-prompt-snapshot off` to render the system prompt fresh on every request instead of reusing the conversation's recorded prompt (for iterating on prompt text)
- **[UNCOVERED]** - Fixed Cowork scheduled tasks in the cloud failing at startup for organizations whose managed settings require sandboxing
- **[UNCOVERED]** - Fixed `/context` and other local command output rendering blank on mobile clients
- **[UNCOVERED]** - Fixed shift+enter and option+backspace not working after reconnecting to a tmux or ssh session inside an agent view
- **[UNCOVERED]** - Fixed the dim last-prompt header not appearing at the top of the conversation when scrolling up in fullscreen mode
- **[UNCOVERED]** - Fixed Workflow `agent()` calls with large output schemas being refused in auto mode instead of being checked by the safety classifier
- **[UNCOVERED]** - Fixed a case where a marketplace entry path containing a backslash could bypass the containment check for fetched marketplaces on macOS and Linux
- **[UNCOVERED]** - Fixed expired AWS or Google Cloud credentials under a host app such as Claude Desktop retrying ten times with a generic "request failed" before the re-authenticate error appeared
- **[UNCOVERED]** - Fixed resuming a session after `/compact` or another slash command ran via `-p --resume`: a spurious "Continue from where you left off." turn is no longer inserted
- **[UNCOVERED]** - Fixed resuming a large session (transcript over 5 MB): parallel tool calls and their hook output are no longer dropped from the reloaded conversation
- **[UNCOVERED]** - Fixed managed `allowedHttpHookUrls`, `httpHookAllowedEnvVars` and `allowedChannelPlugins` to admit nothing, not everything, when unreadable
- **[UNCOVERED]** - Fixed `/login` on machines whose managed settings require Claude apps gateway sign-in: Esc now closes the dialog instead of doing nothing
- **[UNCOVERED]** - Fixed artifact publishes cut off by a dropped connection mid-upload: they now retry once when Claude Code can tell the upload never completed, instead of reporting an unknown outcome
- **[UNCOVERED]** - Fixed `effort:` frontmatter on custom commands, skills, and subagents being ignored on models whose default effort is still pinned (Opus 4.7, Opus 4.8, Fable 5)
- **[UNCOVERED]** - Fixed artifact publish failing with an unhelpful error when the page file isn't valid UTF-8 or contains a replacement character (U+FFFD); the error now names the line and column to fix
- **[UNCOVERED]** - Fixed `claude agents` `@` directory menu not listing repositories created after the session started
- **[UNCOVERED]** - Fixed Remote Control clients that join a Claude Desktop or VS Code session showing a stale permission mode until it was changed again
- **[UNCOVERED]** - Fixed `claude remote-control` exiting and dropping every attached session when its server credential expires (about 30 days after start); the host now re-registers and keeps going
- **[UNCOVERED]** - Fixed the usage-limit warning flickering on and off during a session when requests for different models or modes report different limit windows
- **[UNCOVERED]** - Fixed earlier reasoning being dropped when an MCP server re-sends, or a built-in tool re-renders, a tool the model already loaded
- **[UNCOVERED]** - Fixed a tool that disappears mid-conversation, from a disconnected MCP server or an upgrade, rewriting the tool list and discarding earlier thinking
- **[UNCOVERED]** - Fixed a background worker forked from a conversation adding EnterWorktree to the conversation's tool block mid-session, which broke prompt-cache reuse
- **[UNCOVERED]** - Fixed mid-session MCP and plugin tools being added to the tool list in sessions without ToolSearch, which broke prompt-cache reuse; supported models now receive them as deferred definitions
- **[UNCOVERED]** - Fixed switching models with /model re-sending every tool definition (a prompt-cache miss); commit and PR attribution text now arrives as a conversation note that updates on model changes
- **[UNCOVERED]** - Fixed resumed sessions rewriting the inline tool set when an MCP connector reconnects at a different moment than before
- **[UNCOVERED]** - Fixed resumed sessions re-rendering tool descriptions instead of replaying the recorded ones when the first turn ran a tool
- **[UNCOVERED]** - Fixed prompt-cache misses and dropped extended thinking when a claude.ai connector's tools change between a session and its resume
- **[UNCOVERED]** - Fixed resumed sessions rewriting earlier MCP tool announcements (and dropping extended thinking) before their connectors reconnect
- **[UNCOVERED]** - Fixed a prompt-cache break when a print-mode (`-p`) conversation is resumed interactively: the system prompt prefix no longer changes
- **[UNCOVERED]** - Improved the `/diff` panel: it no longer flashes "0 files changed" and a spinner before settling, and its empty state is centered in the panel
- **[UNCOVERED]** - Improved the Bash tool's description guidance so Claude describes what a command does in plain words instead of echoing the command
- **[UNCOVERED]** - Improved sandbox guidance so Claude suggests `/copy` when clipboard commands such as `pbcopy` fail inside the sandbox
- **[UNCOVERED]** - Improved `--resume` first-render time for sessions with many Bash tool calls
- **[UNCOVERED]** - Improved prompt input responsiveness: keystrokes no longer occasionally wait a frame behind spinner or streaming repaints
- **[UNCOVERED]** - Improved prompt-cache stability: subagents and sessions started with `--system-prompt` or `--append-system-prompt` now record the system prompt and tool definitions once instead of re-rendering them
- **[UNCOVERED]** - Improved Artifact tool publish errors: when a publish is refused, the message now says why and what to do about it
- **[UNCOVERED]** - Self-hosted runner: Changed `--use-anthropic-git-proxy` to be reported to the server at registration and to print a warning for each session that still clones through the legacy git proxy
- **[UNCOVERED]** - Gateway: Changed `forward_user_identity` upstreams to return a 429 as-is to a developer whose email was forwarded, instead of failing over to the next upstream, so the proxy's per-user limits hold
- **[UNCOVERED]** - [VSCode] Fixed the extension host hanging at 100% CPU when forking, editing an earlier message, or rewinding in a conversation whose saved transcript contains a cyclic parent link
- **[UNCOVERED]** - [VSCode] Fixed pasting a screenshot on WSL2/WSLg inserting raw image bytes into the chat input; the image is now attached when the clipboard provides it, otherwise the paste is ignored
- **[UNCOVERED]** - [VSCode] Fixed chat diff blocks always rendering with a dark editor theme; they now follow the active VS Code color theme, including high contrast
- **[UNCOVERED]** - [VSCode] Fixed mixed right-to-left and English text rendering in the wrong order while typing in the message input
- **[UNCOVERED]** - [VSCode] Fixed accepting an edit in the diff view on a file with Windows (CRLF) line endings failing with "String not found in file"
- **[UNCOVERED]** - [VSCode] Fixed @-mentions dropping files whose paths contain spaces
- **[UNCOVERED]** - [VSCode] Fixed the sessions list view failing to load in windows connected over Remote-SSH when the workspace folder exists only on the remote host
- **[UNCOVERED]** - [VSCode] Fixed runaway ripgrep processes when viewing files in large or symlink-heavy workspaces
- **[UNCOVERED]** - [Claude Code on the web] Fixed GitHub Enterprise Server sessions showing your GitHub account as disconnected once its token expired; PR and issue operations now refresh it automatically
- **[UNCOVERED]** - [Claude Code on the web] Fixed `gh` and GitHub API calls failing in organizations without the Claude GitHub App; they now use your connected GitHub account and say so when none is connected
- **[UNCOVERED]** - [Claude Tag] Added a "Use a custom connector" link to the preset connection forms in Claude Tag admin settings, so you can switch to a custom connection without starting over
- **[UNCOVERED]** - [Claude Tag] Fixed Claude replying "The API rejected the request as invalid" when the organization has run out of usage credits; the reply now says so and explains how to add more
- **[UNCOVERED]** - [Claude Tag] Fixed thread requests to edit or delete a message Claude posted at the channel's top level being answered with a correction instead of reaching the session that posted it
- **[UNCOVERED]** - [Claude Tag] Fixed **Connect** on Tool access requests under Admin settings > Review requests failing with "Authorization failed" or showing the requested access bundle as deleted

#### v2.1.266

- **[UNCOVERED]** - Fixed a 2.1.265 regression affecting LLM-gateway and proxy setups: the undocumented `CLAUDE_CODE_USE_GATEWAY` environment variable, previously ignored unless `ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN` were both set, began forcing Cloud-gateway sign-in on its own in 2.1.265, so configurations that set it alongside an API key, `apiKeyHelper`, or custom auth headers failed every request with "Not signed in to the Cloud gateway". The variable on its own is ignored again; no configuration change is needed

#### v2.1.265

- **[covered]** - Updated the `.claude` folder permission option to say what it actually allows: editing files in the project's `.claude` folder (or `~/.claude`) for the session
  - Covered by: `cc-native/sessions/CC-session-lifecycle-analysis.md`
- **[UNCOVERED]** - Added `user.email` and `user.groups` to the telemetry Claude Desktop and Cowork send through a Claude apps gateway, matching terminal sessions
- **[UNCOVERED]** - Added support for pointing `--plugin-dir` at a folder of plugins: each child folder with a manifest loads, and children added or removed while running are picked up
- **[UNCOVERED]** - Added a 1 GB cap on tool results saved to disk; the in-conversation preview says when a saved file was truncated
- **[UNCOVERED]** - Fixed resuming a foreground-spawned subagent changing its tool list and system prompt prefix, which broke prompt-cache reuse for that agent
- **[UNCOVERED]** - Fixed agent teammates and resumed subagents moving SubagentStart hook context and preloaded skills out of the prompt prefix on later turns, which broke prompt-cache reuse
- **[UNCOVERED]** - Fixed resume after the previous process died while a tool was running: the last prompt is no longer rewritten, and the interrupted tool call is kept and marked interrupted
- **[UNCOVERED]** - Fixed `/model opusplan[1m]` being rejected with "Model not found"
- **[UNCOVERED]** - Fixed syntax-highlighted code in permission prompts and messages sometimes omitting a character after a Ruby `?`, Erlang `$`, or Perl `$` sigil
- **[UNCOVERED]** - Fixed the fullscreen transcript jumping by one row whenever the slash-command or @-file suggestion list opened or closed
- **[UNCOVERED]** - Fixed a plugin path containing a backslash bypassing the symlink containment check on macOS and Linux
- **[UNCOVERED]** - Fixed plugin directories whose names begin with two dots being wrongly refused as outside the plugin root
- **[UNCOVERED]** - Fixed VS Code and SDK sessions occasionally requiring re-login when a session was closed while refreshing its token
- **[UNCOVERED]** - Fixed Remote Control sessions sending the end-of-turn signal before the reply's last message, which could show a reply as finished in the Claude app before its last part arrived
- **[UNCOVERED]** - Fixed background (`--bg`) sessions occasionally being retired mid-turn when a message arrived just before the idle timeout
- **[UNCOVERED]** - Fixed Claude Code's own git status and diff probes running clean filters configured by a nested repository inside the working tree
- **[UNCOVERED]** - Fixed the advisor tool and its instructions being re-decided per request from the request's model; the decision is now made once and announced in the conversation when it changes
- **[UNCOVERED]** - Fixed artifact publish accepting connector tool names the connector doesn't expose; the publish is now refused when none of the declared tools exist, and warned when only some don't
- **[UNCOVERED]** - Fixed `/add-dir <subdirectory>` refusing to load a subdirectory's agents when managed settings lock only skills to plugins, and promising agents when only agents are locked
- **[UNCOVERED]** - Fixed two-key keyboard shortcuts cancelling silently when the second key arrived more than a second later, as happens inside tmux; they now wait 3 seconds and show a notice when they time out
- **[UNCOVERED]** - Fixed forked skills (`context: fork`) not streaming their kickoff prompt and, with `--forward-subagent-text`, their text turns as progress events in stream-json
- **[UNCOVERED]** - Fixed a plugin's default component folder that the OS cannot check, such as a symlink loop, being silently skipped; it is now reported in `/plugin` with the error code
- **[UNCOVERED]** - Fixed the Claude apps gateway's OTLP telemetry relay pausing all forwarding to a collector for 30 seconds after it rejected a few payloads as malformed or too large
- **[UNCOVERED]** - Fixed `/plugin` Discover/Browse and `claude plugin list --json --available` showing no description or display name for marketplace plugins whose metadata lives only in their `plugin.json`
- **[UNCOVERED]** - Fixed `/login` showing "no gateway URL is configured" when re-run in a session that signed in to a Claude apps gateway set by managed settings
- **[UNCOVERED]** - Fixed `/model` claiming a model was "saved as your default" when the settings file couldn't be written; it now says the save failed and why
- **[UNCOVERED]** - Fixed `/clear` from Remote Control waiting on SessionStart hooks and on open terminal dialogs before completing
- **[UNCOVERED]** - Fixed the `/config` dialog changing height when switching between its tabs
- **[UNCOVERED]** - Fixed resuming a workflow run after its container restarted; a resume whose run journal is missing now fails with a clear error instead of rerunning every agent
- **[UNCOVERED]** - Fixed the `claude-api` skill's error-code reference: model access failures return 404 and unavailable beta headers return 400, not 403
- **[UNCOVERED]** - Fixed non-interactive sessions (`-p` with stream-json input, Agent SDK, cloud sessions) resetting the shell working directory at each new user message; a `cd` now persists across turns
- **[UNCOVERED]** - Fixed MCP servers configured as `http` that only speak the legacy HTTP+SSE transport never connecting; Claude Code now falls back to SSE as the MCP spec describes
- **[UNCOVERED]** - Fixed some claude.ai connectors in cloud sessions showing as needing authentication even though they are connected in claude.ai (servers that answer an unsupported request with HTTP 401)
- **[UNCOVERED]** - Fixed remote sessions keeping their sandbox container alive while a connector approval or sign-in link waits for you
- **[UNCOVERED]** - Fixed resumed sessions showing long model-facing recovery instructions in "background task didn't finish" notices instead of a short status line
- **[UNCOVERED]** - Windows: Fixed Read, Write and Edit refusing every file ("symlink resolution changed after permission was checked") when running inside an AppContainer or restricted-token sandbox
- **[UNCOVERED]** - Improved `--worktree` startup on large repositories: the new worktree is now checked out in parallel (git 2.32+)
- **[UNCOVERED]** - Improved `/workflows` agent detail: tool calls are marked running, failed or done, the subagent's task list is shown when it has one, and Enter unfolds the listed calls with their inputs and results
- **[UNCOVERED]** - Improved slash commands typed mid-prompt: matches now show in a list (Tab opens it outside fullscreen) instead of a single suggestion, and a plugin skill is now found by its bare name
- **[UNCOVERED]** - Improved remote MCP servers that need sign-in: Claude Code no longer registers an OAuth client with them until you actually authenticate
- **[UNCOVERED]** - Improved the time to resume long sessions that read many files
- **[UNCOVERED]** - Improved the error shown when an image over the size limits cannot be decoded: it now names the cause and how to fix it instead of only citing the limit
- **[UNCOVERED]** - Improved the Artifact tool's read of an artifact someone else wrote: the summary now treats the page as untrusted content and flags embedded instructions rather than relaying them
- **[UNCOVERED]** - Changed machines with `forceLoginGatewayUrl` in managed settings to be Claude apps gateway sessions from startup, like `forceLoginMethod: "gateway"`; a leftover claude.ai login or API key is not used
- **[UNCOVERED]** - Changed image processing to use the runtime's built-in image support; the CLI no longer extracts a native image module to the temp directory
- **[UNCOVERED]** - Changed plugin display metadata to prefer the marketplace entry over `plugin.json` on the Installed tab and `claude plugin details`, filling gaps from `plugin.json`
- **[UNCOVERED]** - Changed Claude apps gateway sessions to export OpenTelemetry directly to a collector the gateway's managed settings name in `OTEL_EXPORTER_OTLP_ENDPOINT`, instead of through the gateway's relay; sessions without a named collector still use the relay
- **[UNCOVERED]** - [VSCode] Added automatic archiving of sessions inactive for a set period (new "Archive inactive sessions" setting, default 14 days)
- **[UNCOVERED]** - [VSCode] Fixed the sidebar chat coming back blank after Reload Window or a restart when the conversation had been open for more than 10 minutes
- **[UNCOVERED]** - [VSCode] Fixed the timeline dot sitting below the text on the "Remote Control is active" message

#### v2.1.263

- **[UNCOVERED]** - Bug fixes and reliability improvements

#### v2.1.261

- **[UNCOVERED]** - Added an "Organization policy" line to `/status` and `claude doctor` that says why your organization's policy could not be loaded, such as a proxy not passing the endpoint through
- **[UNCOVERED]** - Added `bashOutputMaxChars` and `taskOutputMaxChars` settings to raise how much command and background-task output Claude receives inline before it is saved to a file, up to 128K characters
- **[UNCOVERED]** - Added `--append-subagent-system-prompt-file` to read the subagent system prompt from a file, for prompts too large to pass on the command line
- **[UNCOVERED]** - Added `/skill-doctor` to show which loaded skills go unused and what they cost in context, so you can prune them
- **[UNCOVERED]** - Fixed typed or pasted characters occasionally landing out of order or being dropped during fast input or key repeat
- **[UNCOVERED]** - Fixed `/add-dir <subdirectory>` printing a false "couldn't be resolved" error when the working directory is on a `/net` automount
- **[UNCOVERED]** - Fixed the Bedrock setup wizard hanging when AWS or an AWS credential helper never responds (it now times out with a clear error), and its model checks failing behind a TLS-inspecting proxy
- **[UNCOVERED]** - Fixed cloud sessions discarding a plugin synced from claude.ai when managed settings force-enable it in `enabledPlugins`, then falling back to a marketplace clone that could fail
- **[UNCOVERED]** - Fixed being unable to delete the character immediately before an inline `[Image #N]` chip in the prompt input
- **[UNCOVERED]** - Fixed resuming a session losing hook output and other context around parallel tool calls, which changed the resumed request
- **[UNCOVERED]** - Fixed Remote Control showing a stale permission mode when a phone, browser, or claude.ai app attaches to a terminal session or after the mode changes in the terminal
- **[UNCOVERED]** - Fixed Remote Control sessions showing as still working (stuck spinner and Stop button) after stopping a turn from a connected phone or browser, or after a local slash command like `/clear`
- **[UNCOVERED]** - Fixed SDK and cloud sessions ignoring a Stop or interrupt sent just after the first prompt, before the turn had started; the turn now stops instead of running to completion
- **[UNCOVERED]** - Fixed Remote Control uploading a session pulled with `/teleport` into the connected session, which appeared appended to the original on phone and web
- **[UNCOVERED]** - Fixed Remote Control's inbound event stream failing behind TLS-inspecting corporate proxies on native Windows
- **[UNCOVERED]** - Fixed Remote Control sessions showing the default effort level on claude.ai when the effort comes from settings
- **[UNCOVERED]** - Fixed `gcpAuthRefresh` opening a browser at startup when the Google credential check was slow, even though the credential was still valid
- **[UNCOVERED]** - Fixed claude.ai connectors staying absent for the whole session when the startup connector fetch timed out — the CLI now retries in the background
- **[UNCOVERED]** - Fixed sustained high CPU usage when a background agent could not be resumed and its wake-up was retried in a tight loop
- **[UNCOVERED]** - Fixed feature flags gated to a newer version occasionally applying to an older Claude Code version running on the same machine
- **[UNCOVERED]** - Fixed `/usage` and the VS Code usage panel dropping a model-specific weekly limit row when the usage endpoint is rate limited or when opened right after startup
- **[UNCOVERED]** - Fixed `claude -p --resume <file>` adopting a malformed session ID recorded in the transcript; it now resumes under a fresh session ID instead
- **[UNCOVERED]** - Fixed the terminal progress indicator (iTerm2, Ghostty, ConEmu) showing the session as finished while a background workflow or agent was still running
- **[UNCOVERED]** - Fixed a rare layout glitch where a box could render with the wrong height after its container switched between row and column direction
- **[UNCOVERED]** - Fixed Claude apps gateway client IP when a trusted proxy appends a port to `X-Forwarded-For`; with an access list set, an unreadable entry now gets 403
- **[UNCOVERED]** - Fixed Claude apps gateway telling Claude Desktop to export OpenTelemetry as JSON even when the terminal CLI uses protobuf, so protobuf-only collectors rejected Desktop's data
- **[UNCOVERED]** - Fixed Desktop and web showing a session as busy while it only watches an artifact for updates
- **[UNCOVERED]** - Fixed Claude in Chrome `file_upload` failing with "paths: expected array, received undefined" in local Cowork sessions run from the Claude Desktop app
- **[UNCOVERED]** - Fixed `SendMessage` to an offline Remote Control session on another machine reading as delivered; the result now says delivery is queued until that machine reconnects
- **[UNCOVERED]** - Fixed plugin install hints from CLIs run in background Bash commands: they are now detected, and the raw `<claude-code-hint>` tag no longer leaks into the conversation
- **[UNCOVERED]** - Fixed in-process agent-team teammates re-sending their first-turn tool and skill announcements on the second turn, which changed the request prefix and missed the prompt cache
- **[UNCOVERED]** - Improved the `/model` picker and the VS Code model pill to show a model's name instead of its raw Bedrock, Vertex AI, or LLM gateway ID when Claude Code recognizes it
- **[UNCOVERED]** - Improved startup on Google Vertex AI when `GOOGLE_APPLICATION_CREDENTIALS` is set: API client creation no longer re-runs Google Cloud project discovery or spawns extra `gcloud` processes
- **[UNCOVERED]** - Improved streaming performance: already-rendered blocks are no longer re-checked by layout on each update
- **[UNCOVERED]** - Improved the dangerous-`rm` safety prompt to also catch `rm -rf` on positional parameters and inside double-quoted `sh -c` scripts
- **[UNCOVERED]** - Improved handling when the API sends no response headers: the retry now waits up to `API_TIMEOUT_MS` (10 minutes by default) instead of another 3 minutes, and the messages say what to change
- **[UNCOVERED]** - Changed a Claude apps gateway 403 on the managed settings load (at startup or after `/login`) to say Claude Code may not be enabled for the organization, instead of advising a new sign-in
- **[UNCOVERED]** - Changed machines whose managed settings pin `forceLoginMethod: "gateway"` to ignore a leftover API key or claude.ai login and ask for `/login`; Bedrock, Vertex AI, and Foundry sessions are unaffected
- **[UNCOVERED]** - Changed auto mode to treat a link that packs content into a public diagram renderer's URL as an upload to that site: no longer auto-approved unless you asked for it
- **[UNCOVERED]** - Changed the prompt's word-editing keys to match Bash: Ctrl+W deletes back to whitespace, Alt+F and Alt+D stop at word end, punctuation separates words; `keybindingFlavor` no longer has any effect
- **[UNCOVERED]** - Changed `/context` token counting to use a local estimate when the token-counting API is unavailable, instead of extra small-model requests
- **[UNCOVERED]** - [VSCode] Added a "Build a custom style" walkthrough to the Output styles menu that writes a custom output style file and lists it right away
- **[UNCOVERED]** - [VSCode] Added an Add server form and a Remove action to the MCP servers dialog, so MCP servers can be added and removed without leaving the IDE
- **[UNCOVERED]** - [VSCode] Added a hollow ring in the session list for sessions open in a terminal, another VS Code window, or Claude Desktop, so they no longer look closed
- **[UNCOVERED]** - [VSCode] Added a fold button to permission and question prompts so the conversation behind them can be read without dismissing them; the space beside the prompt now scrolls the conversation
- **[UNCOVERED]** - [VSCode] Added "Archive session" to the session list's right-click menu and gave Unarchive its own icon
- **[UNCOVERED]** - [VSCode] Fixed a session teleported from Claude Code on the web treating a question that was cut off when the cloud session shut down as declined
- **[UNCOVERED]** - [VSCode] Fixed the session tab's Rename box opening empty for a tab restored with the window; it now starts with the current name
- **[UNCOVERED]** - [VSCode] Fixed collapsed sections in the session list panel briefly showing expanded each time the panel loaded
- **[UNCOVERED]** - [VSCode] Fixed Focus view showing a tool call as still running after Claude had moved on, such as while a question waited for your answer
- **[UNCOVERED]** - [VSCode] Fixed the session list's active-row highlight going stale when an unfocused Claude tab's session ID is corrected
- **[UNCOVERED]** - [VSCode] Fixed Cmd/Ctrl+Shift+T reopen and deep-link opens placing the Claude tab outside the Claude editor group when a Claude tab has focus
- **[UNCOVERED]** - [VSCode] Fixed the session tab's "Add to group" putting a session opened from Claude Code on the Web in two groups; it now moves the entry the session list shows
- **[UNCOVERED]** - [VSCode] Fixed the model picker showing models an organization has since disabled until the window was reloaded twice
- **[UNCOVERED]** - [VSCode] Fixed a tab opened from the session list jumping back to that session, and a tab opened from a Web session restarting its teleport or staying empty, after VS Code reloads the tab's view
- **[UNCOVERED]** - [VSCode] Fixed `/btw` side-question history from earlier sessions being overwritten when a question is asked right after a window reload or while a settings file has errors
- **[UNCOVERED]** - [VSCode] Fixed the pending question card not reappearing after the Claude panel reloads when signed in with a Claude.ai or Console account
- **[UNCOVERED]** - [VSCode] Fixed claude.ai-only features staying visible in a window's other Claude panels after one panel picked up a third-party provider from a settings file
- **[UNCOVERED]** - [VSCode] Fixed the sign-in screen appearing despite the Disable Login Prompt setting when Claude Code reports no login or a request fails for lack of one
- **[UNCOVERED]** - [VSCode] Fixed the next queued permission prompt keeping text typed on the previous prompt and accepting an immediate second click
- **[UNCOVERED]** - [VSCode] Fixed install-plugin links opening the Claude sidebar without the install dialog in a window where only the session list had been shown
- **[UNCOVERED]** - [VSCode] Fixed the sidebar usage meter staying empty on a new window until the Account & usage dialog was opened, and a 0% usage limit being left out of the meter
- **[UNCOVERED]** - [VSCode] Fixed "Start new session in this group" losing the group after New conversation, and a missing unread dot for a session that finished before the sidebar's unread list loaded
- **[UNCOVERED]** - [VSCode] Fixed the editor tab badge showing unread during a running turn or missing on a tab opened from the session list, and "Add Session Tab to Group" doing nothing for an archived session
- **[UNCOVERED]** - [VSCode] Fixed "Enable Remote Control for all sessions" so flipping it also applies right away to sessions open in other VS Code windows
- **[UNCOVERED]** - [VSCode] Fixed the session list's Open filter for sessions continued from claude.ai whose tab was still recorded under the web session, and labeled the filter menu's sections for screen readers
- **[UNCOVERED]** - [VSCode] Changed the model picker to one flat list of every model, with rows kept for older model spellings listed last

#### v2.1.260

- **[covered]** - Improved idle CPU usage of non-interactive (`-p` / SDK) sessions
  - Covered by: `cc-native/ci-remote/CC-web-auth-setup-analysis.md`, `cc-native/plugins-ecosystem/CC-cowork-skills-api-workflows.md`, `cc-native/sessions/CC-session-cost-analysis.md`
- **[UNCOVERED]** - Added a diff panel that opens beside the conversation in fullscreen mode and shows your uncommitted changes as Claude edits; toggle it with `/diff`
- **[UNCOVERED]** - Added a likely cause for prompt-cache misses (e.g. tool definitions or system prompt changed, idle past the TTL) to `/cost` and the status line's `prompt_cache` field
- **[UNCOVERED]** - Added `/reload-plugins` to headless sessions, so it appears in the Claude Code Desktop and SDK command lists
- **[UNCOVERED]** - Added a text form of `/advisor` (`/advisor`, `/advisor <model>`, `/advisor off`) for the desktop app, Remote Control, and other headless (`-p`/Agent SDK) sessions
- **[UNCOVERED]** - Added `oidc.scope_on_refresh` to the Claude apps gateway for IdPs that return an id_token on refresh only when asked for `openid` again
- **[UNCOVERED]** - Added Claude apps gateway support for newer Claude Desktop keys in `desktop` policy blocks, including `userPluginMarketplacesEnabled` and `userPluginUploadsEnabled`
- **[UNCOVERED]** - Fixed `Edit`/`Write`/`Read` permission rules whose path contains parentheses being dropped as invalid or ignored by the Bash sandbox, which left "read-only" folders writable
- **[UNCOVERED]** - Fixed one file permission rule with an uncompilable pattern (e.g. an unclosed `[`) making every file edit fail with `Invalid regular expression`; such a deny rule now guards the literal path it spells
- **[UNCOVERED]** - Fixed Bash permission checks auto-approving zsh commands that hide a command substitution in a REPORTTIME, REPORTMEMORY or DIRSTACKSIZE assignment; these now prompt for approval
- **[UNCOVERED]** - Fixed Bedrock model discovery, token counting and AWS SSO/STS credential calls failing with "unable to get local issuer certificate" when the corporate root CA is only in the OS certificate store
- **[UNCOVERED]** - Fixed `permissions.blockReadsOutsideWorkingDirectories` on macOS hiding the user's git config from sandboxed git and hiding a worktree-isolated sub-agent's own checkout
- **[UNCOVERED]** - Fixed managed settings not loading for claude.ai Enterprise/Team users who also had a leftover API key from an earlier `/login`
- **[UNCOVERED]** - Fixed `/status` listing a signed-in claude.ai account and a configured API key as if both were in effect; the credential not in use is now marked
- **[UNCOVERED]** - Fixed managed `skillOverrides` entries keyed on a bundled skill's alias (e.g. `checkup` for `/doctor`) not applying, and `Skill(name)` deny rules not covering a nested skill listed as `<dir>:name`
- **[UNCOVERED]** - Fixed `model: fable` agents ignoring the `[1m]` tag on an `ANTHROPIC_DEFAULT_FABLE_MODEL` pin and silently running with a 200K context window
- **[UNCOVERED]** - Fixed the `/model` picker not showing Fable 5.1 for organizations that can use it, which was only accepted when typed as `/model claude-fable-5-1`
- **[UNCOVERED]** - Fixed prompt caching on Claude Fable 5.1 not covering the context attached after tool results, so it was re-sent as uncached input on every tool-call turn
- **[UNCOVERED]** - Fixed model switching staying blocked for the rest of the session after a plugin hook load failure; each switch now re-checks and the refusal names the cause
- **[UNCOVERED]** - Fixed model switching being blocked for the session when an organization-managed plugin's marketplace could not be loaded
- **[UNCOVERED]** - Fixed SDK-provided MCP servers (e.g. Desktop connectors) sometimes missing from the first turn and only appearing on the next one
- **[UNCOVERED]** - Fixed Claude in Chrome tools failing with "Not connected" mid-task in cloud-hosted claude.ai sessions when a connector was added or removed
- **[UNCOVERED]** - Fixed flags, joined emoji and accented letters splitting across wrapped lines, and stale text staying on screen when a flag or joined emoji falls in the terminal's last two columns (now shown as `…`)
- **[UNCOVERED]** - Fixed Remote Control accepting a model pick that is not a valid model name; it is now refused with an error instead of failing on the next message
- **[UNCOVERED]** - Fixed `/rewind` and `--rewind-files` reporting success when checkpoint backup files were missing and nothing was actually restored
- **[UNCOVERED]** - Fixed `/rewind` leaving stale file-read tracking from the rewound-away turns, which caused "File unchanged since last read" stubs and full-file re-injection after external edits
- **[UNCOVERED]** - Fixed `-p --resume`/`--continue` (as used by the desktop app) failing on every retry once a session's worktree directory lost its git metadata; it now fails once, then resumes without the worktree
- **[UNCOVERED]** - Fixed a subagent that resumed another agent via SendMessage never being woken by that agent's completion (the notification went to the main conversation instead)
- **[UNCOVERED]** - Fixed agent teams: an in-process teammate's transcript losing messages, or going blank, during long API retry waits (e.g. under `CLAUDE_CODE_RETRY_WATCHDOG`) as retry notices evicted real messages
- **[UNCOVERED]** - Fixed a session that moved to the background appearing twice in ListAgents (once as a phantom "interactive" twin with the same name) and receiving SendMessage deliveries in the viewer
- **[UNCOVERED]** - Fixed intermittent "task output swap refused" errors when many sessions share a project directory
- **[UNCOVERED]** - Fixed Ctrl+Z in fullscreen leaving the shell on the alternate screen, drawn over the paused interface
- **[UNCOVERED]** - Fixed Workflow tool subagents being restarted as stalled while a long context compaction was still in progress
- **[UNCOVERED]** - Fixed plugins from a URL marketplace failing to install with "marketplace entry path does not stay inside the marketplace directory" when a host app (e.g. Claude Desktop) stores it as a directory
- **[UNCOVERED]** - Fixed an extra browser tab opening when an artifact is published in a session you're driving from claude.ai, the desktop app, or mobile (Remote Control)
- **[UNCOVERED]** - Fixed the Artifact tool's first call failing with an "Invalid tool parameters" validation error in some Cowork sessions
- **[UNCOVERED]** - Fixed IDE line selections being dropped when running a skill or slash command (the "N lines selected" context now reaches Claude)
- **[UNCOVERED]** - Fixed repository detection for GitLab projects in nested subgroups (e.g. `gitlab.com/group/subgroup/project`)
- **[UNCOVERED]** - Fixed `owner/repo#123` issue references in rendered output linking to github.com when working in a GitLab repository; they now link to the gitlab.com issue
- **[UNCOVERED]** - Glob/Grep: Fixed the search path being probed on disk before the permission check; a missing path is now reported after permission is decided, as Read does
- **[UNCOVERED]** - Reverted the 2.1.259 change applying `Read()` deny rules to Bash arguments; it denied `npm run build` under a `Read(./**/build/**)` rule in every mode and made `cd … && grep` prompt even in auto mode
- **[UNCOVERED]** - Improved structured output: Workflow `agent({schema})` rejects a JSON Schema that can never be satisfied up front, and retry-cap errors now include the last validation failure
- **[UNCOVERED]** - Improved deleting a background session whose worktree has unpushed commits: the message now names the branch and commit count, and deleting again discards the worktree
- **[UNCOVERED]** - Improved the Claude apps gateway's refresh-failure log to name the step that failed
- **[UNCOVERED]** - Improved the Claude apps gateway on Amazon Bedrock: input tokens for an aborted request are now counted with AWS's free CountTokens API (grant `bedrock:CountTokens`) instead of a one-token request
- **[UNCOVERED]** - Improved the settings error for rules such as `Edit(C:\dir\(name)\**)`, where `\(` is read as an escaped parenthesis rather than a path separator, to suggest an unambiguous spelling
- **[UNCOVERED]** - Improved auto-compact for 1M-context models: Opus and Fable sessions now compact shortly before the 1M-token limit, and recovery compaction on very large contexts no longer times out at 10 minutes
- **[UNCOVERED]** - Improved `/ultrareview` and `claude ultrareview` to wait up to 45 minutes (previously 30) for long-running cloud reviews
- **[UNCOVERED]** - Improved `/effort` on Claude Fable 5.1 so changing effort mid-session no longer invalidates the prompt cache
- **[UNCOVERED]** - Updated the bundled `claude-api` skill so its Go, Java, and C# samples use current-generation model IDs, and clarified that cheaper worker or sub-agent models should be current-generation too
- **[UNCOVERED]** - Changed `ctrl+l` / `cmd+k` in fullscreen mode to clear the transcript view like a terminal `clear`; scroll up to see earlier messages
- **[UNCOVERED]** - Changed permission rules with text after the closing parenthesis (e.g. `Bash(ls) x`), which never matched anything, to be reported as invalid settings instead of being silently ignored
- **[UNCOVERED]** - Changed server-managed settings so a managed CLAUDE.md (`claudeMd`) no longer triggers the security approval dialog; hooks, shell-command, sandbox, and unsafe `env` settings still require approval
- **[UNCOVERED]** - Changed Claude in Chrome to follow your organization's Claude in Chrome admin setting; when an admin turns it off, `--chrome`, `/chrome` and the browser tools are unavailable
- **[UNCOVERED]** - Changed Claude apps gateway to send `orgPluginSettings` in the list form read by Claude Desktop 1.15200.0 and later; older desktops ignore it
- **[UNCOVERED]** - Changed Claude apps gateway to also refuse to start, naming the field, when a `desktop` policy misspells a field in a nested object of a `managedMcpServers` or `orgPluginSettings` entry
- **[UNCOVERED]** - Changed commands typed at the `!` bash-mode prompt to run outside the sandbox even when strict sandbox mode (`sandbox.allowUnsandboxedCommands: false`) is on, like typing into your own terminal
- **[UNCOVERED]** - Changed self-hosted runner `--kill-session-after-min` to release a session that is only waiting on its user (paused, resumable on the next message) instead of killing it and reporting a failure
- **[UNCOVERED]** - Removed the one-hour time limit on background commands started by subagents; they now run until they exit or are stopped, matching the main session
- **[UNCOVERED]** - [VSCode] Added the selected effort level to the footer model pill, fixed a stale effort level after switching models, and returned the footer pills to their earlier compact size
- **[UNCOVERED]** - [VSCode] Added Open and Closed to the session list's status filter menu
- **[UNCOVERED]** - [VSCode] Fixed the welcome screen disappearing in a new session when Remote Control turns on automatically
- **[UNCOVERED]** - [VSCode] Fixed the session history picker loading a session a second time when it is already open in another tab; it now switches to that tab
- **[UNCOVERED]** - [VSCode] Fixed the session tab's Rename command silently doing nothing while the tab's view was reloading; it now always applies
- **[UNCOVERED]** - [VSCode] Fixed a half-finished message, an empty tool card or an extra "Thought for" line staying on screen after Claude Code retried a dropped response
- **[UNCOVERED]** - [VSCode] Fixed "Enable Remote Control for all sessions" not applying to a session tab that was still starting when the toggle was flipped

#### v2.1.259

- **[UNCOVERED]** - Added `managedMcpServers` managed setting: organizations can provide HTTP/SSE MCP servers to every user (same entry shape as `.mcp.json`); entries that name a command to run are skipped
- **[UNCOVERED]** - Added `--permission-prompts none` for unattended headless hosts: anything that would prompt is denied automatically while the active permission mode (including auto mode) keeps deciding
- **[UNCOVERED]** - Added recognition of `glab mr create/merge/close/reopen/note/update` so GitLab merge requests show as `MR !N` in the collapsed tool summary and refresh the footer MR badge
- **[UNCOVERED]** - Added `--json` to `claude plugin validate` for a machine-readable validation report
- **[UNCOVERED]** - Fixed concurrent sessions silently reverting each other's `~/.claude.json` changes — workspace trust no longer resets and MCP/project state is no longer lost when running many sessions at once
- **[UNCOVERED]** - Fixed a conversation whose thinking was rejected once being rejected again on every later turn
- **[UNCOVERED]** - Fixed Bash `Read()` deny rules not covering files given as option values (`--ignore-revs-file=.env`, `-f.env`, `@file`), `git diff`/`git grep` file operands, or `cd DIR && cat FILE` compounds; `grep -r`/`cp -r` over a directory holding a denied file now asks
- **[UNCOVERED]** - Fixed the prompt cache being invalidated when the OAuth token refreshed in sessions with telemetry disabled
- **[UNCOVERED]** - Fixed fullscreen mode showing a blank conversation after a long turn with hundreds of tool calls
- **[UNCOVERED]** - Fixed auto mode running a turn on a model it doesn't support when a command or skill's frontmatter `model:` named one; the turn now keeps the session model
- **[UNCOVERED]** - Fixed `CLAUDE_CODE_MAX_CONTEXT_TOKENS` being ignored for Vertex-style model IDs (`@YYYYMMDD` suffix) of model versions Claude Code doesn't recognize
- **[UNCOVERED]** - Fixed the live output preview of a running shell command hiding its newest lines when an earlier line wrapped
- **[UNCOVERED]** - Fixed a background GitHub connection check that ran on every launch for claude.ai users; the result is now remembered across launches
- **[UNCOVERED]** - Fixed `--resume` failing (and `--continue` opening an empty conversation) when a saved session contains an attachment entry with no payload
- **[UNCOVERED]** - Fixed frontmatter `model:` on custom commands and skills being ignored in interactive sessions
- **[UNCOVERED]** - Fixed Artifact publishing failing once with an "unexpected parameter `note`" error in conversations continued from an older version
- **[UNCOVERED]** - Fixed managed `forceRemoteSettingsRefresh` being ignored at startup when a policy helper configured by MDM or the managed settings file had already run
- **[UNCOVERED]** - Fixed worktree isolation refusing hook-created worktrees on machines where `git rev-parse` fails with a message other than "not a git repository"
- **[UNCOVERED]** - Fixed OpenTelemetry metrics and events from cloud sessions missing the `user.email`, `organization.id`, and `user.account_uuid` attributes
- **[UNCOVERED]** - Fixed MCP servers that disconnect while their tools are being listed at startup showing as connected with no tools instead of reporting the error
- **[UNCOVERED]** - Fixed the file edit permission dialog sometimes showing a changed line cut short with no indication
- **[UNCOVERED]** - Fixed repository detection dropping a known repo identity after a transient git probe failure
- **[UNCOVERED]** - Fixed managed settings silently going unenforced when the managed-settings file, a drop-in, the MDM plist, or the HKLM value cannot be parsed: Claude Code now refuses to start and names the source
- **[UNCOVERED]** - Fixed Stop not actually stopping background agents and workflows in remote-control sessions: killed tasks now stay visible and re-stoppable until their processes exit
- **[UNCOVERED]** - Fixed resuming a workflow run while its previous stopped run was still exiting, which could run duplicate copies of its agents
- **[UNCOVERED]** - Fixed marketplace repo URLs on github.com with a trailing slash or dangling `?`/`#` producing an unusable `.git` clone URL
- **[UNCOVERED]** - Fixed blocking Stop hooks causing the turn after a block to lose the model's reasoning from that turn and, on some models, miss the prompt cache
- **[UNCOVERED]** - Fixed remote (claude.ai) sessions taking 60 seconds to start a turn after a browser-hosted MCP server's page had gone away
- **[UNCOVERED]** - Fixed worktree-isolated sessions refusing common Bash loops, xargs pipelines and launcher-wrapped commands that cannot reach the main checkout
- **[UNCOVERED]** - Improved terminal resize and first-render performance for long responses by reusing text measurements
- **[UNCOVERED]** - Improved `/workflows` agent detail: JSON outcomes are pretty-printed with syntax colors and real line breaks, and long outcomes fold behind an expand toggle
- **[UNCOVERED]** - Improved headless/SDK session start: the first turn begins up to 50 ms sooner when MCP servers finish connecting
- **[UNCOVERED]** - Improved `/install-github-app` to explain it is GitHub-only and point to the GitLab CI/CD docs when run inside a GitLab repository
- **[UNCOVERED]** - Improved nested background subagent results to be saved in the parent subagent's transcript, so resumed subagents keep them and shared transcripts show the delivery
- **[UNCOVERED]** - Changed `allowedMcpServers` to govern only servers users add: a literal `managed-mcp.json` server your allowlist used to filter out now loads on upgrade; use `deniedMcpServers` to keep it off
- **[UNCOVERED]** - [VSCode] Added an Active quick filter and a status filter menu (Needs input, Working, Completed) to the session list sidebar
- **[UNCOVERED]** - Fixed remote and scheduled sessions doing nothing after a connector-tool permission prompt was approved while the session was paused

#### v2.1.258

- **[UNCOVERED]** - Fixed Claude Code failing to launch on macOS 12 (Monterey), a regression introduced in 2.1.255
- **[UNCOVERED]** - Fixed remote and scheduled sessions failing with "user messages must have non-empty content" after a re-sent permission approval could not be applied

#### v2.1.257

- **[covered]** - Added Claude Fable 5.1 (`claude-fable-5-1`), now the default Fable model — 1M context, $10/$50 per Mtok with $0.25/Mtok cache reads
  - Covered by: `cc-native/configuration/CC-model-provider-configuration.md`
- **[covered]** - Removed the Ctrl+E command explanation on Bash and PowerShell permission prompts
  - Covered by: `cc-native/configuration/CC-bash-mode-analysis.md`
- **[UNCOVERED]** - Added "Time format" (`timeFormat`) and `timeZone` settings: 12-hour, 24-hour, 24-hour UTC, or a strftime pattern for the turn-end clock and transcript-view timestamps
- **[UNCOVERED]** - Added a Containment Escape rule to auto mode so cloud metadata-credential fetches, egress evasion, and cross-tenant reach are no longer auto-approved unless your environment marks them expected
- **[UNCOVERED]** - Added `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` to apply `CLAUDE_CODE_SUBAGENT_MODEL` (or the main model) to every subagent, ignoring per-spawn and agent-definition model overrides
- **[UNCOVERED]** - Added `s` in `/effort` to change effort for the current session only, matching `/model`
- **[UNCOVERED]** - Added a `/doctor` warning for stale sandbox mask files left by a killed session
- **[UNCOVERED]** - Added a one-time prompt in auto mode before the first file read outside the working directories, with the option to block such reads (`permissions.blockReadsOutsideWorkingDirectories`)
- **[UNCOVERED]** - Added support for a gateway-supplied `description` on discovered `/model` picker entries (`CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY`); entries without one still read "From gateway"
- **[UNCOVERED]** - Fixed settings in a `.claude/` folder created after startup not being picked up until restart
- **[UNCOVERED]** - Fixed sessions dispatched from an agent view opened with `←` always starting in the original session's permission mode, overriding the target directory's `defaultMode` and the agent's `permissionMode`
- **[UNCOVERED]** - Fixed `keybindings.json` rebinds of Ctrl+G being ignored in `claude agents`; its Ctrl+S / Ctrl+T are now rebindable via the new `Agents` context
- **[UNCOVERED]** - Fixed background sessions failing to start on macOS npm installs during a self-update, and on Windows when a stale daemon lock file pointed at a reused process id
- **[UNCOVERED]** - Fixed the working spinner stopping while a response streams behind a slash-command panel
- **[UNCOVERED]** - Fixed a background session's `state.json` `detail` repeating its own dispatch prompt after a scheduled wake-up
- **[UNCOVERED]** - Fixed `claude agents` keeping a background session you re-prompted buried in Completed after it finished again; Completed now orders by the latest finish
- **[UNCOVERED]** - Fixed `claude --bg` from a directory that was just deleted reporting "backgrounded" and leaving a crashed session row; it now prints the reason and exits 1
- **[UNCOVERED]** - Fixed Remote Control connecting mid-session re-sending the Bash tool definition, causing a prompt-cache miss
- **[UNCOVERED]** - Fixed a doubly-listed custom `Authorization` header overriding the configured credential on Bedrock, Mantle, Vertex, and WIF, and the Vertex setup wizard picking up a leftover Anthropic profile from `~/.config/anthropic`
- **[UNCOVERED]** - Fixed Claude apps gateway sending stray host `Authorization` or profile headers to Foundry, Vertex, and Bedrock, and Foundry Entra ID upstreams not starting when `ANTHROPIC_FOUNDRY_API_KEY` is set
- **[UNCOVERED]** - Fixed a leftover Anthropic API key or auth token being sent alongside your Foundry subscription key in API-key mode
- **[UNCOVERED]** - Fixed `/schedule` routines whose prompt was saved without a message role and then ran with nothing to do
- **[UNCOVERED]** - Fixed `claude agents` not saying that a background session is waiting for you to approve a message from another session, or who sent it
- **[UNCOVERED]** - Fixed a prompt stashed with Ctrl+S inside an opened background session being lost when the session went idle or was stopped and then reopened
- **[UNCOVERED]** - Fixed telemetry (OTEL) settings pushed through server-managed settings being ignored on warm starts, including desktop-app Code sessions
- **[UNCOVERED]** - Fixed a teammate permission request being answered twice when the leader's mailbox write was briefly locked
- **[UNCOVERED]** - Fixed a phantom duplicate slash-command row rendering below the in-flight turn while a command's auto-continued response streamed
- **[UNCOVERED]** - Fixed `policyHelper` `timeoutMs` and `refreshIntervalMs` values above the timer maximum (2147483647) causing failures or re-runs every millisecond; they are now clamped
- **[UNCOVERED]** - Fixed the token counter freezing or crawling after switching to another subagent's transcript, and made background subagents' and teammates' counters update live while a response streams
- **[UNCOVERED]** - Fixed sandbox network hosts written with a trailing dot (`example.com.`): a `deniedDomains` entry didn't block the host inside the sandbox, and "don't ask again" for such a host kept prompting
- **[UNCOVERED]** - Fixed dismissing the Remote Control consent prompt (Esc, or `n` at `claude remote-control`) counting as consent, so the next request connected without asking
- **[UNCOVERED]** - Fixed `/mcp` reconnect and enable still connecting a settings-file MCP server that a managed MCP allow/deny list or `strictPluginOnlyCustomization` loaded after startup should block
- **[UNCOVERED]** - Fixed `claude mcp remove` leaving a remote server's stored OAuth credentials behind when `strictPluginOnlyCustomization` locks MCP to plugin-only servers
- **[UNCOVERED]** - Fixed Remote Control (`claude remote-control`) sessions started from the Claude app ignoring the selected model and running on the machine's default instead
- **[UNCOVERED]** - Fixed `--disallowedTools` and session deny rules being dropped after the first settings reload when `allowManagedPermissionRulesOnly` is enabled
- **[UNCOVERED]** - Fixed `--resume` listing a backgrounded conversation twice and `--continue` reopening its stalled pre-background copy; `--continue` now also opens finished background sessions
- **[UNCOVERED]** - Fixed fullscreen mode not letting you click `!` shell command output to expand it
- **[UNCOVERED]** - Fixed background sessions left running an older Claude Code binary piling up across auto-updates instead of being retired
- **[UNCOVERED]** - Fixed `claude agents --json` briefly switching the terminal to raw mode and undoing another program's terminal settings on exit
- **[UNCOVERED]** - Fixed Proactive output style sessions busy-looping with filler messages and repeated log reads instead of idling while a background command or Monitor they started is still running
- **[UNCOVERED]** - Fixed subagents stopping when a response was cut off mid-stream by a computer sleep, dropped connection, or server error; they now automatically continue instead of ending with an incomplete response
- **[UNCOVERED]** - Fixed `←` doing nothing in the `/btw` panel inside a `claude agents` session: it now returns to the agents list (even mid-answer), and the panel comes back when you reopen the session
- **[UNCOVERED]** - Fixed sessions with an advisor model set missing the prompt cache on background requests (compaction, `/recap`, prompt suggestions) and re-sending the full conversation uncached each time
- **[UNCOVERED]** - Fixed `claude -p` exiting about 5 seconds after its final result while a Monitor the model armed was still running; it now waits for the watch to fire or time out
- **[UNCOVERED]** - Fixed a `permissions.ask` rule being skipped in auto mode when the matching command ran inside a compound command or subshell, letting it run without the confirmation prompt
- **[UNCOVERED]** - Fixed plugins being able to read files outside their own directory through a declared command, agent, skill, hooks or other component path that is a symlink; such paths are now refused with an error
- **[UNCOVERED]** - Fixed `/add-dir` rejecting a directory inside the current working directory; it now loads that directory's skills, commands, and agents like `--add-dir` does at startup
- **[UNCOVERED]** - Fixed the main agent not being told when you resume a subagent you had stopped from its transcript view
- **[UNCOVERED]** - Fixed a crash when pasting ANSI-colored text (e.g. a CI log) into dialogs like `/feedback`
- **[UNCOVERED]** - Fixed `claude mcp add/remove` hanging or exhausting memory when the project's `.mcp.json` is a FIFO or a device-file symlink; it now fails fast with an actionable message
- **[UNCOVERED]** - Fixed unbounded memory growth when non-JSONL data is piped into `claude -p --input-format stream-json`; it now fails fast with a clear error
- **[UNCOVERED]** - Fixed backgrounding a turn (`←` or Ctrl+B) while a subagent or other tool was running occasionally making the background session treat that tool as rejected instead of re-running it
- **[UNCOVERED]** - Fixed Bash `Read()`/`Edit()` deny rules not applying to `< file` redirects and reader commands like `tac` and `egrep`; a deny rule on any argument or redirect target now refuses the command
- **[UNCOVERED]** - Fixed resuming or messaging a subagent whose transcript had grown past 5 MB (for example after reading many images) failing with "No transcript found"
- **[UNCOVERED]** - Fixed worktree-isolated sessions refusing Bash loops, `$VAR` reads, `"$(…)"` and heredocs that never touch git as "too complex to verify that it stays inside the worktree"
- **[UNCOVERED]** - Fixed `/model` and `/effort` showing a prompt-cache warning after rewinding a conversation back to empty
- **[UNCOVERED]** - Fixed prompt-cache misses on every turn in long screenshot-heavy sessions once images exceeded the per-request size cap
- **[UNCOVERED]** - Fixed the Edit permission prompt's diff view rendering emoji and multi-code-point characters with incorrect widths
- **[UNCOVERED]** - Fixed WebSocket MCP server connection failures being logged as "[object ErrorEvent]" instead of the underlying error
- **[UNCOVERED]** - Fixed background sessions failing to open with "Couldn't start the background service" while another Claude Code process was downloading an npm update; the start now waits for it
- **[UNCOVERED]** - Fixed background commands that detach from their shell (for example under `timeout` or `setsid`) surviving a task stop or Claude Code exit
- **[UNCOVERED]** - Fixed Claude not being told when you stop a background command from the tasks panel or a connected client
- **[UNCOVERED]** - Fixed stopping a background subagent leaving its monitors running
- **[UNCOVERED]** - Fixed sandboxed git commands in a linked worktree losing write access to the repository's common `.git` directory after `cd` into a subdirectory
- **[UNCOVERED]** - Fixed Bedrock and Bedrock Mantle requests going silent during long hidden-thinking phases on Opus 4.7 and later, which let idle timeouts cut the connection; the stream now carries progress events
- **[UNCOVERED]** - Fixed launching Claude Code after a Claude apps gateway expired or revoked your session: it now says the session ended and offers `/login` instead of reporting a network error
- **[UNCOVERED]** - Fixed cloud sessions losing git/GitHub credentials for the rest of the session when the session's network proxy failed to start at launch; it now retries in the background and recovers
- **[UNCOVERED]** - Fixed leftover `cc-daemon-*` folders in the system temp directory after an interrupted background daemon start; the `cleanupPeriodDays` retention sweep now removes them
- **[UNCOVERED]** - Fixed Bash permission checks auto-approving certain `[[ ]]` conditionals that zsh parses differently from bash; these commands now prompt for approval
- **[UNCOVERED]** - Fixed the managed-settings approval prompt showing the generic warning instead of its telemetry wording when the settings also turn detailed tracing or raw API body logging off, or trace export on
- **[UNCOVERED]** - Fixed agent-team teammates in tmux/iTerm2 panes sometimes staying open after acknowledging a shutdown request
- **[UNCOVERED]** - Fixed the keyless Console sign-in ("Sign in with your Console account") not applying your organization's server-managed settings, and `/status` not showing the Organization for that sign-in
- **[UNCOVERED]** - Improved rendering performance: less re-render work per turn in long conversations, streaming no longer slows down as the reply grows, and background-agent updates no longer re-render the whole screen
- **[UNCOVERED]** - Improved prompt input responsiveness by reducing per-keystroke rendering work
- **[UNCOVERED]** - Improved policy helper diagnostics — refresh failures now show in `/status`, declining the managed-settings dialog prints why Claude Code exited, and helper timeouts are reported as timeouts
- **[UNCOVERED]** - Improved `/code-review --comment` to post findings on GitLab merge requests via `glab mr note` instead of reporting the target as unsupported
- **[UNCOVERED]** - Improved notifications: an MCP elicitation or permission ask queued under another dialog now sends its idle desktop notification at the same delay as a visible ask
- **[UNCOVERED]** - Improved verbose/transcript output: async hook completion notices that arrive together now appear on one line instead of one line per hook
- **[UNCOVERED]** - Improved `claude self-hosted-runner --configure-git` to also enable git push negotiation, so the first push of a new branch from a stale clone uploads only the new commits instead of the whole tree
- **[UNCOVERED]** - Improved liveness reporting to SDK hosts while a response is held open by gateway keep-alives, so long waits under a raised `CLAUDE_STREAM_IDLE_TIMEOUT_MS` are not mistaken for a hung session
- **[UNCOVERED]** - Improved MCP connection and OAuth debug/error logs so credentials carried in a server's URL or request headers are redacted
- **[UNCOVERED]** - Improved `/fork` to keep the original conversation's prompt cache in the new background session: its worktree briefing now arrives as a message instead of a system-prompt change
- **[UNCOVERED]** - Improved emoji autocomplete to accept the remaining GitHub/Slack shortcode aliases (`:satisfied:`, `:telephone:`, `:collision:`, …)
- **[UNCOVERED]** - Changed `--effort` to lift a new model's default-effort hold for that session only rather than permanently; an effort picked on claude.ai for a Remote Control session now applies during the hold
- **[UNCOVERED]** - Changed a `policyHelper` in MDM or `managed-settings.json` shadowed at launch by cached server-managed settings to run (or exit) as soon as the fetch reports them removed, not at the next launch
- **[UNCOVERED]** - Changed `managedSourcesBehavior: "merge"` to take `sandbox.credentials.awsPairs` and `sandbox.ripgrep` whole from the highest managed source that sets them instead of combining the sources' values
- **[UNCOVERED]** - Changed gateway model discovery (`CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1`) to run even when `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` is set, since it only queries your gateway
- **[UNCOVERED]** - Changed `claude --resume <session-id> --bg` to continue that session under its own ID when nothing is running it, instead of silently starting a copy; a copy is now announced
- **[UNCOVERED]** - Changed `/btw` history browsing from `←`/`→` to `Shift+←`/`Shift+→` (or `[`/`]`), stepping through your recent side questions and back to the live answer
- **[UNCOVERED]** - Changed `defaultMode: "bypassPermissions"` in `.claude/settings.json` or `.claude/settings.local.json` to be ignored, like `"auto"`; set it in user or managed settings, or pass `--permission-mode`
- **[UNCOVERED]** - Changed `fable` and `best` in Claude apps gateway sessions to keep resolving to Fable 5 for now, since gateways not yet configured for Fable 5.1 reject it; pick Fable 5.1 in `/model` to use it
- **[UNCOVERED]** - Changed `--add-dir`, `/add-dir`, and `additionalDirectories` to refuse network paths (UNC shares, `/net/<host>` automounts) with a message before touching them; on Windows use a mapped drive letter
- **[UNCOVERED]** - Changed Claude apps gateway sign-in and token refresh requests to verify the gateway's pinned TLS certificate, as the managed settings fetch already does
- **[UNCOVERED]** - Changed Cowork and claude.ai cloud sessions: reading an artifact that isn't yours now always asks you first, even in auto mode
- **[UNCOVERED]** - [VSCode] Added collapsible ACCOUNT & USAGE and SESSION MANAGER section headers to the session list panel, with the account email, the usage meter, and a View details link opening the usage dialog
- **[UNCOVERED]** - [VSCode] Added a model pill to the input footer that shows the current model and opens the model picker, with an Effort row and a "More models" page
- **[UNCOVERED]** - [VSCode] Added a collapse toggle to the Ungrouped section of the session list
- **[UNCOVERED]** - [VSCode] Added output style selection to the command menu, including custom styles
- **[UNCOVERED]** - [VSCode] Fixed third-party provider deployments (Bedrock, Vertex, and others) still showing claude.ai-only features (remote sessions, dictation, usage) and calling claude.ai with a leftover login
- **[UNCOVERED]** - [VSCode] Fixed the session list panel's usage meter staying blank after the panel loads; it now shows the last known usage immediately
- **[UNCOVERED]** - [VSCode] Fixed the "Enable Remote Control for all sessions" toggle so turning it on or off applies to sessions that are already open, not only to new ones
- **[UNCOVERED]** - [VSCode] Fixed screen reader announcements: a control character before a fence or heading no longer drops visible lines from speech, and bold markers spanning a heading are no longer mis-paired
- **[UNCOVERED]** - [VSCode] Changed the action menu to list slash commands in a filterable "Slash commands" dialog instead of inline; picking one runs it; the MCP servers dialog gained the same filter box
- **[UNCOVERED]** - [VSCode] Changed "Delete session" to "Archive session": archived sessions move to a collapsible "Archived sessions" group at the bottom of the list with an Unarchive action

#### v2.1.252

- **[UNCOVERED]** - Fixed Bash commands failing with "task output swap refused (tasks dir moved or linked)" on some Macs
- **[UNCOVERED]** - Fixed "always allow" not saving in a project that has no .claude/settings.local.json yet
- **[UNCOVERED]** - Fixed Remote Control sessions hosted by Claude Desktop or VS Code stalling for minutes after a tool finished when the connection to claude.ai was degraded
- **[UNCOVERED]** - Fixed background task notifications with very large failure output (for example git errors on a full disk) making the conversation exceed the API request size limit

#### v2.1.251

- **[covered]** - Improved retry when the model's tool call is malformed: the broken output is now dropped from the retry context, including on Bedrock, Vertex, and Foundry
  - Covered by: `cc-native/configuration/CC-model-provider-configuration.md`
- **[UNCOVERED]** - Added `PreModelSwitch` and `PostModelSwitch` hook events (block, confirm, or annotate a model switch); `SessionStart` resume hooks now receive session staleness and the estimated re-cache cost
- **[UNCOVERED]** - Added live streaming of a foreground subagent's tool calls and results to Remote Control clients (background subagents, the default, still show status only)
- **[UNCOVERED]** - Added a Spend limit bar to `/usage` and a `rate_limits.spend_limit` status line field for developers behind a Claude apps gateway with spend limits
- **[UNCOVERED]** - Added a per-session prompt-cache line to `/cost` (hit ratio, misses, tokens re-cached, warm/cold) and a matching `prompt_cache` object for status line scripts
- **[UNCOVERED]** - Added `attach`, `logs`, `stop`, `respawn`, and `rm` to `claude --help`; the `--resume` message for a running background session now names the exact `claude attach <id>` command
- **[UNCOVERED]** - Fixed file tools (Read, Write, Edit) following a symlink swapped inside the working directory after the permission check, which could read or write outside the approved location
- **[UNCOVERED]** - Fixed plugin commands declared in a marketplace entry being able to point outside the plugin directory; such paths are now rejected with a path-traversal error
- **[UNCOVERED]** - Fixed project settings being able to enable detailed beta tracing or raw API body logging, and a lower-scope beta tracing endpoint bypassing an OTLP collector pinned by managed settings or a host app
- **[UNCOVERED]** - Fixed the Workflow tool reading (and quoting in errors) a `scriptPath` outside what the session may read before the permission check ran
- **[UNCOVERED]** - Fixed Grep and Glob not applying `Read(...)` deny rules to files reached through a symlinked search path
- **[UNCOVERED]** - Fixed conversations getting stuck on "text content blocks must be non-empty" errors after a turn where the model produced only thinking
- **[UNCOVERED]** - Fixed the first launch on a fresh install starting in default mode instead of auto mode for accounts whose startup default is auto mode
- **[UNCOVERED]** - Fixed Opus 5 requests failing with "effort … is not supported when thinking is disabled" when effort was xhigh/max and thinking was turned off; effort is now sent as `high` in that case
- **[UNCOVERED]** - Fixed replying to a message Claude Desktop delivered from another session: `SendMessage` to that session id now delivers through Claude Desktop instead of failing with "not reachable"
- **[UNCOVERED]** - Fixed TUI lag with many parallel subagents: per-second progress ticks now replace their predecessor instead of piling up in the transcript
- **[UNCOVERED]** - Fixed agent teams: a teammate's final answer not reaching the team lead — it now arrives in the idle notification instead of a content-free "available" notice
- **[UNCOVERED]** - Fixed background subagents being unable to reply to a message from an unnamed sibling or parent agent (`from` was the agent type, which is not an address)
- **[UNCOVERED]** - Fixed managed-settings `disableAutoMode` arriving mid-session not moving an already-running auto-mode session back to default mode
- **[UNCOVERED]** - Fixed a "switch to Opus 1M for 5x more context" tip that appeared even when the current Opus model already has a 1M context window
- **[UNCOVERED]** - Fixed Claude apps gateway sessions treating a stored Anthropic profile (e.g. a Console sign-in) as active: listing it in `/status` and retrying gateway 401s with it, though requests never use it
- **[UNCOVERED]** - Fixed cloud sessions telling Claude the model had changed when the host was only setting the session's initial model
- **[UNCOVERED]** - Fixed Remote Control reporting a failure when an organization's policy disables it; it now shows a single quiet notice instead
- **[UNCOVERED]** - Fixed `/mcp reconnect` on Remote Control showing a generic withheld-detail error instead of the real remedy when a server was disabled in another session
- **[UNCOVERED]** - Fixed `--input-format stream-json`: client-injected assistant tool calls sent without a message id were merged into the first one and their results lost, including when resuming older sessions
- **[UNCOVERED]** - Fixed session transcripts being silently overwritten when a directory change relocated a session onto an existing same-ID transcript
- **[UNCOVERED]** - Fixed background sessions and their subagents being unable to edit files inside a git worktree they created with `git worktree add`
- **[UNCOVERED]** - Fixed background sessions occasionally starting without any plugin skills (and staying that way) when another Claude Code process was refreshing the plugin marketplace at the same moment
- **[UNCOVERED]** - Fixed selecting text in an opened background session inside tmux over SSH: it now copies to the tmux buffer like a foreground session instead of falling back to OSC 52
- **[UNCOVERED]** - Fixed SDK and cloud sessions hanging indefinitely when an SDK MCP server's handshake acknowledgment was lost; the wait now times out after 70 seconds and marks only that server failed
- **[UNCOVERED]** - Fixed self-hosted runner leaving a stuck session's Bash tool processes running after the session was force-stopped
- **[UNCOVERED]** - Fixed `/usage-credits` for Team and Enterprise members whose admin set the org's usage-credit limit to $0: it now offers to ask the admin instead of saying a cap was reached
- **[UNCOVERED]** - Fixed `--worktree --tmux` with a merge-request number on a gitlab.com origin trying a doomed GitHub-style fetch first instead of fetching the GitLab ref directly
- **[UNCOVERED]** - Fixed Ctrl+G failing with "Emacs quit unexpectedly" in background sessions for editors that open `/dev/tty`, such as `emacs -nw` and `micro`
- **[UNCOVERED]** - Fixed an `additionalDirectories` entry containing a null byte crashing startup, or breaking `/add-dir` and later settings updates when it came from an SDK host, IDE, or hook; it is now skipped
- **[UNCOVERED]** - Fixed the MCP server menu's copy shortcut: it now says how the sign-in URL was copied instead of always claiming success
- **[UNCOVERED]** - Fixed italic text (such as the session recap line) rendering as highlighted blocks in GNU screen and in tmux sessions using a `screen` terminal type
- **[UNCOVERED]** - Fixed `claude mcp add --header` and `claude mcp add-json` help text naming the wrong transports
- **[UNCOVERED]** - Fixed `claude ultrareview` and `/ultrareview` waiting the full 30 minutes when the cloud session fails to start; they now stop early and report the reason
- **[UNCOVERED]** - Fixed Bash permission checks auto-approving commands that assign an arithmetic expression to an integer shell variable (e.g. `OPTIND=1/0`, `RANDOM=2+2`); these now prompt for approval
- **[UNCOVERED]** - Fixed backgrounded sessions (`←`, `/background`, `--bg`) losing a Vertex/Bedrock gateway (`ANTHROPIC_*_BASE_URL` + `CLAUDE_CODE_SKIP_*_AUTH`) exported in the shell, so every request failed
- **[UNCOVERED]** - Fixed `claude --bg --model fable` on Max plans stopping to ask for usage credits while the interactive session on the same account still had Fable allowance
- **[UNCOVERED]** - Fixed the one-time "make auto mode your default" offer appearing in unattended sessions (e.g. agent-team teammate panes), where a stray keypress could accept it unread
- **[UNCOVERED]** - Fixed the managed-settings approval prompt re-appearing after signing in again to the same Claude apps gateway when the settings are unchanged
- **[UNCOVERED]** - Fixed disabled `/bug` and `/share` reporting that `/feedback` was disabled; tips, `/help`, and refusal messages no longer suggest `/feedback` when an org policy or env var turns it off
- **[UNCOVERED]** - Fixed cloud session creation advising GitHub setup after a transient GitHub connection failure — the message now says to retry instead
- **[UNCOVERED]** - Improved CPU usage during turns in interactive sessions by cutting redundant UI re-renders
- **[UNCOVERED]** - Improved install size: the native binary is about 5 MB smaller
- **[UNCOVERED]** - Improved cloud sessions: when the session's network proxy drops a connection during a Bash command, the tool result now names the host and reason instead of only "connection reset"
- **[UNCOVERED]** - Improved `/schedule` to explain that MCP servers configured in Claude Code can't be attached to cloud routines, instead of a bare "No MCP connectors" message
- **[UNCOVERED]** - Improved framing of messages from your own subagents: Claude is told the sender is a worker inside this session, not an unrelated Claude session
- **[UNCOVERED]** - Improved the prompt placeholder to read "Message @name…" while viewing a background subagent or fork transcript opened from the subagent panel or `/tasks`
- **[UNCOVERED]** - Improved sanitization of MCP server names in error messages, menus, and command results
- **[UNCOVERED]** - Improved Amazon Bedrock session start under `CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST` (e.g. Claude Desktop): a session given a Bedrock model ID or ARN no longer waits for inference-profile discovery
- **[UNCOVERED]** - Improved the managed settings approval dialog to list only the settings that changed since you last approved them
- **[UNCOVERED]** - Changed `/radio` to be available on Bedrock, Vertex AI, Foundry, and Claude Platform on AWS, and when telemetry is disabled
- **[UNCOVERED]** - Changed Claude in Chrome so browser actions always go through Claude Code's permission checks, including in sessions with telemetry disabled, which previously used the Chrome extension's own prompts
- **[UNCOVERED]** - Changed `CLAUDE_CODE_SUBAGENT_MODEL` to set the default subagent model rather than override everything: an agent definition's `model:` and an explicit per-spawn model now take precedence over it
- **[UNCOVERED]** - Changed the default commit trailer to `Co-Authored-By: Claude Code` when the active model isn't a recognized Claude model (e.g. third-party models behind a custom `ANTHROPIC_BASE_URL`)
- **[UNCOVERED]** - Changed the default model for seat-based Enterprise subscriptions to Opus 5, matching other premium plans
- **[UNCOVERED]** - Changed `/effort` to save your default effort level per model, so each model keeps its own setting when you switch
- **[UNCOVERED]** - Changed analytics to no longer turn off before sign-in solely because managed settings force gateway login (or cannot be read); they stay off once signed in to the gateway or via `DISABLE_TELEMETRY`
- **[UNCOVERED]** - Changed the footer PR badge on Bedrock, Vertex, and Foundry, and when telemetry is off, to call the GitHub API directly (via `gh auth token`, `GH_TOKEN`, or `GITHUB_TOKEN`) instead of `gh pr view`
- **[UNCOVERED]** - Changed how Bash command output files are created and read back when commands run in the sandbox, so a sandboxed command cannot redirect or replace them
- **[UNCOVERED]** - Changed plugin/LSP install suggestions and the auto-mode default offer to wait until you've sent or cleared what you're typing, so the Enter that sends your prompt can't answer them
- **[UNCOVERED]** - Changed server-managed settings that terminate sandbox TLS, route sandbox traffic through your own proxy, inject credentials, or weaken sandbox isolation to require approval before they apply
- **[UNCOVERED]** - Changed `ANTHROPIC_CUSTOM_HEADERS` from managed or project settings to require approval when it sets a credential, org/tenant, routing, or API-behavior header (e.g. `Authorization`, `Host`)
- **[UNCOVERED]** - Changed project-level `.claude/settings.json` `env` to no longer set `CLAUDE_CONFIG_DIR`, `CLAUDE_CODE_TMPDIR`, or `TMPDIR`/`TMP`/`TEMP`; set them in your shell, user, or managed settings instead
- **[UNCOVERED]** - Removed syntax highlighting for six rarely used languages (1c, gml, isbl, mathematica, maxima, sqf); the binary is 2.5 MB smaller
- **[UNCOVERED]** - [VSCode] Fixed the sign-in screen's "Bedrock, Foundry, or Vertex" button opening the docs at the top of the page instead of the third-party provider setup section
- **[UNCOVERED]** - [VSCode] Changed the Remote Control banner to a footer pill (shown while Remote Control is on or has failed) that opens the session on claude.ai/code; turn it on or off with `/remote-control`

#### v2.1.250

- **[UNCOVERED]** - Bug fixes and reliability improvements

#### v2.1.248

- **[UNCOVERED]** - Added `--restricted` (or `CLAUDE_CODE_RESTRICTED=1`): removes the built-in tools that run commands or code and `WebFetch` (unless named in `--tools`), keeps file tools inside the working directory, refuses `bypassPermissions`, and ignores user, project and local settings files
- **[UNCOVERED]** - Added `experimental.cacheTtl` (`"5m"` or `"1h"`) to agent frontmatter: a per-agent prompt cache TTL used when no subagent TTL setting is configured
- **[UNCOVERED]** - Added `claude self-hosted-runner --client-label <label>` (or `SELF_HOSTED_RUNNER_CLIENT_LABEL`) to override the label the runner registers with (default: hostname)
- **[UNCOVERED]** - Added server-managed settings diagnostics: a startup warning when the settings fail to load, and a `/doctor` and `/status` line explaining a load failure or why they weren't fetched (Bedrock/Vertex/third-party provider, custom `ANTHROPIC_BASE_URL`)
- **[UNCOVERED]** - Added a warning in `/web-setup` when the GitHub CLI token lacks the `workflow` scope, since pushes to very large repositories can be rejected without it
- **[UNCOVERED]** - Added `/usage-credits` for Enterprise organizations billed through AWS Marketplace, self-serve Enterprise, and Enterprise trials, so members can request a higher usage limit from their admin
- **[UNCOVERED]** - Added cross-session messaging (`SendMessage` / `ListAgents`) between sessions on the same machine on Bedrock, Vertex, and Foundry, and when telemetry is disabled
- **[UNCOVERED]** - Fixed a prompt-cache miss (and lost extended-thinking context) roughly once an hour in long sessions, caused by tool definitions being re-rendered after an OAuth token refresh
- **[UNCOVERED]** - Fixed the `ScheduleWakeup` tool definition changing between a session and its `--resume` when the account had entered usage overage, causing a full prompt-cache miss on the resumed session's first turn
- **[UNCOVERED]** - Fixed Claude Desktop and Cowork sessions disappearing after 30 days: the transcript cleanup now keeps desktop-written sessions while they are in the app (unless org policy manages retention); the new `desktopSessionCleanupPeriodDays` setting caps the exemption
- **[UNCOVERED]** - Fixed being sent to the login screen when another Claude Code process held the token refresh lock while the session token had expired; the request now fails with a retryable error instead
- **[UNCOVERED]** - Windows: Fixed the `claude agents` list not responding to the keyboard after detaching from a session, or when launched in a terminal tab left in win32-input-mode
- **[UNCOVERED]** - Fixed the recommended Console sign-in in `/login` failing with an OAuth error before showing a sign-in URL on machines where it can't be used (for example when `ANTHROPIC_API_KEY` or an API key helper is set); it now falls back to the API-key sign-in
- **[UNCOVERED]** - Fixed model names in `/model` and fast-mode switch notices to render as code, so suffixes like `[1m]` display literally instead of as a link
- **[UNCOVERED]** - Fixed `claude agents` skipping the workspace trust prompt when the `CI` environment variable is set
- **[UNCOVERED]** - Fixed `claude agents` crashing on launch when the PR-status cache held a malformed entry
- **[UNCOVERED]** - Fixed agent view resurrecting a weeks-old background session after the machine was off: such a session now shows as stopped at its real end, and opening it asks before resuming its saved conversation
- **[UNCOVERED]** - Fixed agent view sometimes opening an older conversation, and dropping the typed prompt, when starting a new session
- **[UNCOVERED]** - Fixed `claude agents`: opening a stopped session that you already resumed in another terminal no longer starts a second process on that conversation; the row now says it is open in a terminal
- **[UNCOVERED]** - Fixed `claude agents` and `claude rm` refusing to delete a session ("has commits that are not pushed anywhere") when its worktree branch was already merged into your checked-out default branch (e.g. local `main`) but not yet pushed
- **[UNCOVERED]** - Fixed background sessions waiting silently when a `PermissionRequest` or `PreToolUse` hook prints an invalid answer: the `claude agents` row now names the hook and the schema error
- **[UNCOVERED]** - Fixed hooks silently treating a stdout `{…}` object that isn't valid JSON as plain text; it's now reported as a hook error with the parse message
- **[UNCOVERED]** - Fixed `/mcp` listing a project `.mcp.json` entry that declares the claude.ai connector type under the trusted "claude.ai" heading; it now appears under its real scope
- **[UNCOVERED]** - Fixed MCP servers whose `headersHelper` supplies the `Authorization` header falling into OAuth discovery on a 401 instead of re-running the helper and retrying the call as documented
- **[UNCOVERED]** - Fixed `/login` to a Claude apps gateway hanging when the managed-settings security approval dialog was required
- **[UNCOVERED]** - Fixed gateway model discovery (`CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY`) never running when `apiKeyHelper` is the only credential
- **[UNCOVERED]** - Fixed `claude logs` leaving mouse tracking, bracketed paste and the alternate screen switched on in the terminal it was run from
- **[UNCOVERED]** - Fixed the trust dialog's list of repo permission rules showing a garbled character when a long rule was cut off in the middle of an emoji
- **[UNCOVERED]** - Fixed the permission mode indicator staying hidden behind the "Press Ctrl-C again to exit" hint when you press shift+tab right after ctrl+c
- **[UNCOVERED]** - Fixed `/ultrareview` and locally seeded cloud sessions uploading uncommitted edits to `prod.env`-style and `*.tfvars` files, or to editor swap, temp, and backup copies of credential files (e.g. `key.pem.tmp`, `id_rsa.swo`); they now stay on your machine
- **[UNCOVERED]** - Fixed Remote Control sessions occasionally never showing a permission prompt or the latest messages on the connected device after the CLI silently reconnected
- **[UNCOVERED]** - Fixed cloud sessions occasionally failing at startup when the container's session credentials were not yet readable
- **[UNCOVERED]** - Fixed `claude remote-control` rejecting its own flags (e.g. `--spawn`, `--name`) when a global flag or a wrapper-injected option precedes the subcommand
- **[UNCOVERED]** - Fixed startup warnings (e.g. "N MCP servers need authentication") rendering one column right of the rest of the transcript
- **[UNCOVERED]** - Fixed a backgrounded worktree session losing its checkout: the background session now holds the worktree's lock while it runs, so cleanup and `git worktree remove` leave it alone
- **[UNCOVERED]** - Fixed @-mentions of other sessions not matching names typed with non-Latin characters (for example Korean entered through an IME)
- **[UNCOVERED]** - Fixed an invalid `crossSessionInbound` value being silently ignored: it now warns and holds cross-session messages (user settings) or refuses them (managed settings) until fixed
- **[UNCOVERED]** - Fixed rate-limit, usage, and fast-mode messages telling you to run `/usage-credits` when that command isn't available for your organization (e.g. hidden with `DISABLE_EXTRA_USAGE_COMMAND`)
- **[UNCOVERED]** - [VSCode] Fixed a chat tab getting stuck on "No conversation found" when its session was never saved; it now starts a new conversation instead
- **[UNCOVERED]** - Improved the Workflow tool's prompt footprint: its description is now about 1k tokens instead of 5.7k, with the script-writing reference moved into a bundled `workflow-authoring` skill
- **[UNCOVERED]** - Improved the prompt-footer PR badge to check GitHub less often while the pull request is unchanged; a push or a `gh pr` command still refreshes it right away
- **[UNCOVERED]** - Improved managed settings: client-side timeout, MCP startup-mode, and stream-watchdog env vars no longer trigger the settings-approval prompt
- **[UNCOVERED]** - Improved `/ultrareview <PR#>` to check before launch that the GitHub account connected to your Claude account can access the repository, and to explain how to fix it, instead of failing after the cloud session starts
- **[UNCOVERED]** - Improved cross-session messaging: falls back to a private per-user `/tmp` directory when the default one can't be used, and the notice and `/status` name the directory to fix
- **[UNCOVERED]** - Changed shift+enter in the agent view dispatch input to insert a newline (matching the prompt); ctrl+enter now dispatches and attaches
- **[UNCOVERED]** - Changed `/loop`: self-paced dynamic mode and the no-prompt autonomous default are now always available, including on Bedrock/Vertex/Foundry
- **[UNCOVERED]** - Changed Anthropic telemetry export failures to log at debug level as `[Anthropic telemetry]` instead of `[3P telemetry] OTEL diag error`, so they are not mistaken for your OTel collector failing
- **[UNCOVERED]** - Changed cross-session messaging in Linux user namespaces: root-equivalent trust for unmapped owners is limited to canonical system directories
- **[UNCOVERED]** - Changed `SendMessage` from a subagent to another session: the result now notes that any reply is delivered to the parent session's conversation, not to the subagent

#### v2.1.247

- **[UNCOVERED]** - Added the `SendFeedback` tool: when something goes wrong in a session, Claude can draft a feedback report for you to review and send from `/feedback` (turn off with the `feedbackDrafts` setting)
- **[UNCOVERED]** - Added `{id, text, cooldownSessions, priority}` entries, `tipsFile`, and `label` to `spinnerTipsOverride`, so organizations can rotate their own tips alongside the built-in ones
- **[UNCOVERED]** - Added a tip on Bash permission prompts pointing to auto mode, with a one-keystroke "Yes, and switch to auto mode" option
- **[UNCOVERED]** - Added `/claude-api cost-optimize` to profile an existing project's Claude API spend and work through cost levers (caching, token hygiene, batch, effort, model choice) one measured change at a time
- **[UNCOVERED]** - Updated the `/claude-api` skill with Admin API coverage (organization members, invites, workspaces, API keys, rate limit reports, workload identity federation, CMEK)
- **[UNCOVERED]** - Fixed fast arrow-key + Enter sequences acting on the row above the one you navigated to in history search, `/config`, `/mcp`, `/skills`, background tasks, and `/model`
- **[UNCOVERED]** - Fixed sub-agents dying on a first-call model 404: they now use the session's fallback model chain, and the error returned to the parent includes the error type, status, request id, and model
- **[UNCOVERED]** - Fixed a hook or background agent that printed megabytes of error output being able to overflow the conversation and wedge the session on "Prompt is too long"
- **[UNCOVERED]** - Fixed Ctrl keyboard shortcuts not firing under non-Latin (e.g. Cyrillic) keyboard layouts in kitty-protocol terminals
- **[UNCOVERED]** - Fixed text like `<35;150;7M` being inserted into the prompt when a mouse report arrived split across reads right after the escape prefix
- **[UNCOVERED]** - Fixed the Bash sandbox's after-command cleanup deleting a dotfile-managed `~/.claude/settings.json` symlink (nix/home-manager, stow) when it is repointed outside the sandbox's writable area
- **[UNCOVERED]** - Fixed `/terminal-setup` overwriting your entire Zed `keymap.json` instead of merging in its keybinding
- **[UNCOVERED]** - Fixed `/rename` silently confirming when the session registry could not be updated; it now says other sessions may still show the old name
- **[UNCOVERED]** - Fixed `/compact` and "Summarize from here" in sessions started with `--agent` summarizing under the default system prompt instead of the conversation's own
- **[UNCOVERED]** - Fixed a background session showing "opening…" forever in `claude agents` after its terminal host process died; the row now fails within seconds with the reason, and Enter restarts it
- **[UNCOVERED]** - Fixed unbounded memory growth when a hook's or background task's output file could not be written; the file now notes where output was lost
- **[UNCOVERED]** - Fixed `/install-github-app` over SSH: the copy shortcut now says how the sign-in URL was copied instead of always claiming success, and the URL appears immediately when no browser can open
- **[UNCOVERED]** - Fixed shell commands carried over from the foreground logging an internal error or showing a misleading `[exited with code -1]` line when they finish in background sessions
- **[UNCOVERED]** - Fixed a version-less marketplace plugin's live cache directory being deleted and recreated on a second-scope install, which could disrupt a running session using it
- **[UNCOVERED]** - Fixed Remote Control sessions started with `/remote-control` not reporting the working-tree diff to connected clients
- **[UNCOVERED]** - Fixed self-hosted runner sessions reporting `running` before Claude Code had started, which could trigger a premature "Claude is waiting for your input" notification from the Claude desktop app
- **[UNCOVERED]** - Fixed first-run setup exiting with "Unable to connect to Anthropic services" when managed settings configure Claude apps gateway sign-in and Anthropic endpoints are unreachable
- **[UNCOVERED]** - Fixed cloud sessions (Claude Code on the web, desktop and mobile apps) sometimes showing the previous permission mode when you switch modes right after sending a message
- **[UNCOVERED]** - Fixed cloud sessions going silent when the session's container restarts between turns while a background agent, shell, or monitor is still running — the resumed session now reports the lost work
- **[UNCOVERED]** - Improved plugin marketplace hardening: names containing control or invisible characters are rejected, and marketplace-supplied text in `/plugin` and `claude plugin` output is escape-safe
- **[UNCOVERED]** - Improved Bedrock, Vertex, and Foundry sessions (and any with telemetry disabled): Claude is now told when a configured MCP server failed to connect, instead of concluding its tools don't exist
- **[UNCOVERED]** - Changed Sonnet 5's default auto-compact window to its full 1M context, so sessions on the 1M window now auto-compact at about 967K tokens instead of about 934K
- **[UNCOVERED]** - Changed cross-session peer messages to collapse by default to a one-line `Message from @<sender>: <first line>` preview; Ctrl+O expands the full body
- **[UNCOVERED]** - Changed terminal hyperlinks in rendered markdown: link targets that point at a network or automounter path, contain a control character, or lead with an invisible character now render as plain text
- **[UNCOVERED]** - Changed the prompt-footer PR badge to skip its GitHub re-check on terminal refocus when the last check is under a minute old
- **[UNCOVERED]** - Changed analytics to stay off from startup, not only after login, when managed settings force gateway login or a custom OAuth deployment is configured
- **[UNCOVERED]** - Changed Claude apps gateway sign-in requests to identify Claude Code (a `surface=claude_code` device-authorization parameter and a `claude-code/<version>` User-Agent)
- **[UNCOVERED]** - Changed organization sign-in enforcement to exit at start when the administrator's managed settings cannot be read, even if host-supplied or per-user Windows registry settings exist

#### v2.1.246

- **[covered]** - Added an Auto mode tab to `/permissions` for viewing and editing auto mode classifier rules
  - Covered by: `cc-native/sandboxing/CC-permissions-bypass-analysis.md`
- **[covered]** - Fixed the plugin cache creating duplicate SHA-named directories for the same plugin
  - Covered by: `cc-native/plugins-ecosystem/CC-plugin-packaging-research.md`
- **[covered]** - Fixed the command sandbox's filesystem configuration not respecting `--setting-sources`
  - Covered by: `cc-native/sandboxing/CC-sandboxing-analysis.md`
- **[UNCOVERED]** - Added a startup warning for Bash allow rules with a wildcard before the subcommand (e.g. `Bash(git * main)`), since they also match options inserted before the subcommand
- **[UNCOVERED]** - Added the turn's completion time to the end-of-turn duration line, e.g. `✻ Sautéed for 23s · done 6:05 PM`
- **[UNCOVERED]** - Fixed fullscreen mode showing a blank transcript after resizing the terminal and jumping to the bottom until the next keypress
- **[UNCOVERED]** - Fixed a severe transcript slowdown when a diff contained a very long single line (e.g. a base64 string); such lines now render truncated with a marker
- **[UNCOVERED]** - Fixed erratic fullscreen scrolling when positioned at an earlier message, including jump-to-bottom getting stuck mid-transcript
- **[UNCOVERED]** - Fixed background sessions failing to open after 45 seconds when Claude Code's starting directory had been deleted, the machine had slept, or the host is slow to start processes
- **[UNCOVERED]** - Fixed background sessions failing to open with "Couldn't start the background service … EACCES" when another Claude Code process was re-installing the npm package at that moment
- **[UNCOVERED]** - Fixed markdown rendering being disabled for a whole message when its first 500 characters contained no markdown, and for `+`/`N)` lists and setext headings
- **[UNCOVERED]** - Fixed MCP tool calls interrupted by an incoming message in headless/remote sessions being reported to the model as "completed with no output" instead of an explicit interrupted error
- **[UNCOVERED]** - Fixed MCP tool arguments being sent as JSON strings when the parameter's schema is empty (`{}`), instead of their real type
- **[UNCOVERED]** - Fixed a command interrupted mid-run showing as "Ran 1 shell command" with no sign it was cut
- **[UNCOVERED]** - Fixed pressing ← or running `/background` during a dynamic workflow restarting its finished subagents; it now asks first and says how many subagents would restart
- **[UNCOVERED]** - Fixed opening a just-started session in `claude agents` while its worker was still booting (common on Windows) stopping it with "was stopped while the respawn was in flight"
- **[UNCOVERED]** - Fixed `claude agents` listing a backgrounded named session twice; backgrounding the same conversation again now numbers the new row (e.g. `my-session (2)`)
- **[UNCOVERED]** - Fixed the background retention sweep removing git worktrees under `.claude/worktrees/` that you created yourself when an old background-session record pointed at them
- **[UNCOVERED]** - Fixed auto mode tool calls being denied as "temporarily unavailable" on very large sessions by scaling the safety-check deadline with prompt size
- **[UNCOVERED]** - Fixed plugin skills whose frontmatter `name` already includes the `<plugin>:` prefix showing it doubled in the slash menu (e.g. `/plugin:plugin:skill`)
- **[UNCOVERED]** - Fixed `claude plugin update` failing for an installed plugin given its bare name (only the fully-qualified name worked)
- **[UNCOVERED]** - Fixed plugin installation failing when `plugin.json` was saved with a UTF-8 byte-order mark (BOM)
- **[UNCOVERED]** - Fixed `/reload-plugins` reporting 0 skills for plugins that define skills under `skills/*/SKILL.md`
- **[UNCOVERED]** - Fixed hook error messages showing a literal `${CLAUDE_PLUGIN_ROOT}` instead of the resolved plugin path
- **[UNCOVERED]** - Fixed `/rename` replacing the theme's prompt border color (including a custom theme's `promptBorder`) with the default cyan; the border now keeps your theme's color unless you pick one with `/color`
- **[UNCOVERED]** - Fixed custom theme diff colors (`diffAdded`/`diffRemoved` and their dimmed variants) being ignored in diffs and the `/theme` preview
- **[UNCOVERED]** - Fixed a `keybindings.json` binding with an unknown action name silently deadening that key; it is now skipped so the default binding keeps working, and a warning is logged under `--debug`
- **[UNCOVERED]** - Fixed `/stats` activity heatmap showing each day's activity one cell off (Sunday's count under Monday) in timezones east of UTC
- **[UNCOVERED]** - Fixed `/fork` from an already-forked or backgrounded session starting the new session with an empty conversation
- **[UNCOVERED]** - Fixed prompts beginning with `/--` (e.g. Lean doc comments) being rejected as an unknown slash command instead of being sent to Claude
- **[UNCOVERED]** - Fixed the `@` file picker staying open after the typed text stopped matching a real path
- **[UNCOVERED]** - Fixed the status line's cost and duration resetting to zero after navigating to the agents view and back
- **[UNCOVERED]** - Fixed fullscreen mode moving keyboard focus onto the control under the pointer when you clicked the terminal window only to bring it back into focus
- **[UNCOVERED]** - Fixed path completion failing when the completion token or working directory contained a null byte
- **[UNCOVERED]** - Windows/macOS: Fixed headless sessions not cleaning up stale entries in `~/.claude/sessions` left by sessions that exited uncleanly
- **[UNCOVERED]** - Fixed the UI stopping with a render error on the first tool call when a third-party Anthropic-compatible endpoint (`ANTHROPIC_BASE_URL`) streams a `tool_use` block without an `id`
- **[UNCOVERED]** - Fixed the Write tool reporting "Out of memory" or freezing for a long time after overwriting a very large existing file, even though the file had been written
- **[UNCOVERED]** - Fixed `claude plugin install <name>` exiting silently (or hanging in a terminal) instead of reporting an error when `~/.claude/plugins/known_marketplaces.json` is empty or corrupted
- **[UNCOVERED]** - Fixed resumed sessions failing every turn with a 400 when the saved history contains tool blocks the Anthropic API does not accept (typically written by a third-party API proxy)
- **[UNCOVERED]** - Fixed `curl -fsSL https://claude.ai/install.sh | bash` failing with "Raw mode is not supported" for some Team/Enterprise users with server-managed settings
- **[UNCOVERED]** - Fixed sessions that ended in plan mode resuming outside plan mode in the VS Code extension, and in `claude -p --continue`/`--resume` with a permission prompt tool, when no permission mode was set
- **[UNCOVERED]** - Fixed the `Notification` hook not firing while the sandbox "Network request outside of sandbox" permission prompt is waiting
- **[UNCOVERED]** - Fixed Bash permission checks to always require approval for malformed commands with a dangling `&&` or `||` operator
- **[UNCOVERED]** - Fixed `--strict-mcp-config` sessions prompting to approve `.mcp.json` servers they would never load, which left background sessions waiting at startup
- **[UNCOVERED]** - Fixed telemetry and metrics requests to Anthropic carrying the API key configured for a third-party gateway (`ANTHROPIC_BASE_URL`); a credential is now only sent to its own host
- **[UNCOVERED]** - Fixed a visible API error on the first prompt after idle when `apiKeyHelper` returns short-lived JWTs: an expired cached token is now refreshed before sending, and 401/403 auth errors retry quietly
- **[UNCOVERED]** - Fixed memory growing with session length in the fullscreen and Ctrl+O transcript views: each rendered message row no longer retains a full copy of the transcript-wide tool lookups
- **[UNCOVERED]** - Fixed `/ultrareview` runs and cloud sessions launched at the same time from one repository (e.g. from several worktrees) sometimes starting with another launch's uncommitted changes
- **[UNCOVERED]** - Fixed the task progress count (e.g. `3/5`) shown for background cloud sessions such as `/autofix-pr` occasionally missing a task
- **[UNCOVERED]** - Fixed Remote Control sessions keeping their placeholder name in claude.ai and the Claude app until the second prompt; the auto-generated title now appears after the first prompt
- **[UNCOVERED]** - Fixed MCP tools marked `requiresUserInteraction` still offering "Yes, and don't ask again" in their permission prompt; the option wrote an allow rule the tool then ignored
- **[UNCOVERED]** - Fixed the self-hosted runner ending its live sessions or exiting when a work-poll response is malformed (e.g. an intercepting proxy's HTML page); it now retries the poll
- **[UNCOVERED]** - Improved `/cd`: the new directory's project settings, hooks, `.mcp.json` servers (behind the usual approval prompt), skills, and agents now take effect right after the move instead of on `--resume`
- **[UNCOVERED]** - Improved Bash tool latency on bash shells by replaying snapshot functions without a base64 subshell per function
- **[UNCOVERED]** - Improved subagent results: a subagent that stops at its `maxTurns` limit now returns its output marked as partial, with a hint to continue it via `SendMessage`, instead of appearing finished
- **[UNCOVERED]** - Improved non-interactive sessions (`-p`, SDK, cloud sessions) to automatically continue a response cut off mid-stream by a server error, connection loss, or stall instead of ending with an error
- **[UNCOVERED]** - Improved attribution of usage telemetry to your organization for workload identity federation sessions, events sent while `apiKeyHelper` runs at startup, and after a login token expired while idle
- **[UNCOVERED]** - Changed `/code-review` so Claude can also start it on its own on Bedrock, Vertex AI, and Foundry, through the Claude apps gateway, and when telemetry or non-essential traffic is disabled
- **[UNCOVERED]** - `/goal`: Changed idle sessions to start at most three check-ins on long-running background work per goal; your next message allows three more
- **[UNCOVERED]** - Changed `claude install` and `claude update` to defer a pending managed-settings consent prompt to the next interactive session instead of prompting mid-command
- **[UNCOVERED]** - Changed OpenTelemetry plugin events for plugins synced from claude.ai: `plugin_id_hash` now reflects the plugin's real marketplace, and `enabled_via` is `admin-install` for admin-installed plugins

#### v2.1.245

- **[UNCOVERED]** - Fixed a crash on startup on Linux distributions that ship glibc 2.44 (for example Arch Linux, CachyOS and Fedora Rawhide)

#### v2.1.243

- **[covered]** - Fixed background subagents not waking when their last background Bash task completes
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`
- **[UNCOVERED]** - Added a Loops breakdown to `/usage`: per-loop run count, total tokens, tokens per run, and last run, so runaway or chatty `/loop` tasks are easy to spot
- **[UNCOVERED]** - Added `modelPicker` setting: curate the `/model` picker with an ordered, labeled list of models (any id spelling, including Vertex/Bedrock ids), appended to or replacing the built-in lineup
- **[UNCOVERED]** - Added `promptCacheTtl` and `subagentPromptCacheTtl` settings so API-key and cloud-provider users can keep a 1-hour prompt cache on the main conversation while subagents stay at 5 minutes
- **[UNCOVERED]** - Added `modelPricing` managed setting so an organization's contracted per-model rates and discount multiplier are used for `/cost`, the status line, and telemetry cost figures instead of list price
- **[UNCOVERED]** - Added a keyless sign-in under `/login` → Anthropic Console: "Sign in with your Console account" (recommended) alongside creating an API key, so organizations that don't allow API keys can sign in
- **[UNCOVERED]** - Added a `Skipped sources` line to `/status` that lists managed settings sources (for example `managed-settings.json`) present but not applied because a higher-precedence managed source is active
- **[UNCOVERED]** - Added a `managed` marker in `/mcp` and `/plugins` on claude.ai connectors whose authentication is managed by your organization
- **[UNCOVERED]** - Added a tip pointing claude.ai users who haven't connected GitHub for Claude Code on the web to `/web-setup`
- **[UNCOVERED]** - Added a `/status` line showing whether GitHub is connected for Claude Code on the web (Pro/Max), pointing to `/web-setup` when it isn't
- **[UNCOVERED]** - Added the model (and effort level) each subagent ran on to `/tasks` and the agent detail dialogs
- **[UNCOVERED]** - Fixed remote MCP servers in non-interactive (`-p`) and SDK sessions never recovering after a dropped connection; they now reconnect automatically or report as failed
- **[UNCOVERED]** - Fixed MCP server sign-in started from the desktop app failing with "Invalid redirect URI" on servers that support client ID metadata documents (for example Linear)
- **[UNCOVERED]** - Fixed auto mode staying unavailable at startup when a temporary server-side disable was cached and later flag fetches failed
- **[UNCOVERED]** - Fixed auto mode tool calls being denied as "temporarily unavailable" after about a minute of waiting when the API was briefly overloaded and asked the client to retry
- **[UNCOVERED]** - Fixed the `/model` picker silently ignoring an Ultracode selection; picking Ultracode now applies it to the current session
- **[UNCOVERED]** - Fixed `/resume` only listing the 50 most recent sessions; the picker now loads more as you scroll
- **[UNCOVERED]** - Fixed cloud sessions resuming after a mid-turn restart with a pending hook or background-task notification re-sent as the prompt instead of the normal continuation message
- **[UNCOVERED]** - Fixed cross-session messaging silently turning off inside user namespaces and rootless containers after the 2.1.232 socket-directory hardening
- **[UNCOVERED]** - Fixed text that hangs outside its container (for example the sign-in URL in `/login`) losing its leading columns when another part of the screen repaints
- **[UNCOVERED]** - Fixed `spellcheck` not underlining a misspelled word typed directly after an emoji
- **[UNCOVERED]** - Fixed sessions going silent for 10+ minutes when the Anthropic API never starts a response: the request now times out after ~3 minutes, retries once, then shows `API Error: No response from API`
- **[UNCOVERED]** - Fixed auth, model-availability, and other client-generated error messages rendering like model output instead of as error lines
- **[UNCOVERED]** - Fixed workload identity federation in CI: processes in one job share the exchanged token instead of re-exchanging the single-use token; a rejected exchange fails fast with the server's message
- **[UNCOVERED]** - Fixed server-managed `companyAnnouncements` not showing at startup in a session that began with signing in (for example the first launch after `/logout`)
- **[UNCOVERED]** - Fixed hook `if` conditions like `Bash(cat *)` firing on unrelated Bash commands when the command contained `$()` or backtick command substitution followed by more arguments
- **[UNCOVERED]** - Fixed plugin dependencies declared with a `marketplace` field never resolving when both plugins are loaded together via `--plugin-dir`
- **[UNCOVERED]** - Fixed `/reload-plugins` keeping the LSP tool after the last LSP plugin is disabled; it now also warns before an LSP plugin change that would re-read the conversation
- **[UNCOVERED]** - Fixed `--agents` silently ignoring invalid JSON or invalid agent definitions; it now exits with a clear error, like `--mcp-config`
- **[UNCOVERED]** - Fixed `/status` showing "Found invalid entries in: ." with no filename when `~/.claude.json` has an invalid MCP server entry
- **[UNCOVERED]** - Fixed `/clear` removing the `/rename` session name from the prompt bar even though the name was kept for the new session
- **[UNCOVERED]** - Fixed Ctrl+R history search and up-arrow history breaking when `~/.claude/history.jsonl` contains a malformed entry
- **[UNCOVERED]** - Fixed Ctrl+[ not leaving vim INSERT mode in terminals that encode modified keys (modifyOtherKeys / kitty protocol)
- **[UNCOVERED]** - Fixed the local IDE connection being routed through `HTTPS_PROXY` (and sometimes failing) when `localhost` was listed in `NO_PROXY` but not lowercase `no_proxy`; both casings are now honored
- **[UNCOVERED]** - Fixed sandbox network-violation details being dropped from the Bash tool result when the blocked command still exited 0 (for example `curl` printing the proxy's 403 page)
- **[UNCOVERED]** - Fixed the status line `rate_limits` fields and `/usage` still showing a rate-limit window's pre-reset usage percentage after the window reset while the session was idle
- **[UNCOVERED]** - Fixed `claude --teleport <session>` exiting on uncommitted changes instead of offering to stash them and continue, as the session picker already does
- **[UNCOVERED]** - Fixed `/web-setup` repeatedly asking you to log in when an older GitHub CLI (without `gh auth token`) was already authenticated
- **[UNCOVERED]** - Fixed Claude in Chrome losing its connection to Claude Code after an auto-update cleaned up the version it was set up with; the native host now launches via the stable `claude` launcher
- **[UNCOVERED]** - [VSCode] Fixed sessions started before feature flags were first fetched (for example right after install) opening in the default permission mode instead of auto mode or your configured default mode
- **[UNCOVERED]** - [VSCode] Fixed Focus view sections you expanded collapsing on their own during subagent tool activity
- **[UNCOVERED]** - Improved startup time: sandbox and MCP bring-up no longer block the first frame, bare launches skip subcommand registration, and workflow discovery, settings, and trust-store work is cheaper
- **[UNCOVERED]** - Improved native install and auto-update download size: the binary is now zstd-compressed (about 75 MB instead of 340 MB on Linux x64)
- **[UNCOVERED]** - Improved attribution of usage telemetry to your organization for sessions that authenticate with `ANTHROPIC_AUTH_TOKEN` directly against the Anthropic API, so its data-handling settings apply
- **[UNCOVERED]** - Improved native binary size: about 2 MB smaller by storing the bundled skill and prompt text more compactly
- **[UNCOVERED]** - Improved memory usage of native builds: code is now loaded on demand instead of keeping the whole bundle resident (roughly 40–70 MB less memory per session)
- **[UNCOVERED]** - Improved peak memory usage in long-running sessions (the runtime now garbage-collects sooner as the heap grows)
- **[UNCOVERED]** - Improved `/login` over SSH: the sign-in URL appears immediately, pressing `c` reports how the URL was copied instead of always claiming success, and a hint explains how to select text in fullscreen
- **[UNCOVERED]** - Improved the error when effort `xhigh`/`max` is used with thinking turned off: it now names the level, the setting that disabled thinking, and `/effort high` as the fix
- **[UNCOVERED]** - Improved `/loop`: consecutive wake-ups where Claude has nothing to do now fold into a single line in the terminal instead of printing each one
- **[UNCOVERED]** - Changed the sandboxed Bash tool prompt to no longer list allowed network hosts, so Claude attempts requests (and you can approve new hosts) instead of assuming unlisted hosts are blocked
- **[UNCOVERED]** - Updated the `/model` picker and the bundled `claude-api` skill to show Sonnet 5's $2/$10 per Mtok pricing as its standard list price rather than a limited-time promo
- **[UNCOVERED]** - Changed computer use on macOS so clicking the desktop, Dock, or a Finder window requires granting Finder via the access dialog, like any other app
- **[UNCOVERED]** - Changed `/model`, `/fast`, and `/effort` to also run immediately instead of queueing until the turn ends on Bedrock, Vertex, and Foundry and when telemetry is disabled
- **[UNCOVERED]** - Fixed `claude remote-control` exiting and stranding attached Remote Control sessions when the server drops its environment mid-session; it now recovers
- **[UNCOVERED]** - Fixed Remote Control sessions served by `claude remote-control` sometimes getting stuck after it was stopped and restarted, for Team and Enterprise members without an admin or owner role
- **[UNCOVERED]** - Changed the cross-session messaging inbox socket to close connections that send no complete line within 30 seconds; scripts posting to it should connect once their data is ready
- **[UNCOVERED]** - Improved the notice when resuming a conversation whose Remote Control is held by another terminal: it now says sessions on other machines can't be seen from, or reach, this one
- **[UNCOVERED]** - [VSCode] Improved history trimming in long sessions: older tool-activity rows are dropped first so your messages and Claude's replies stay visible
- **[UNCOVERED]** - [VSCode] Improved attribution of the extension's own usage telemetry to your organization when you are signed in with a Claude account, so its data-handling settings apply

#### v2.1.241

- **[UNCOVERED]** - Bug fixes and reliability improvements

#### v2.1.240

- **[UNCOVERED]** - Bug fixes and reliability improvements

#### v2.1.239

- **[UNCOVERED]** - Cost estimates (`/cost`, status line, `--max-budget-usd`) now include the 1.1× US-only-inference premium for data-residency workspaces
- **[UNCOVERED]** - Added the one-time fullscreen renderer offer on Bedrock, Vertex, Foundry and other previously excluded setups; new installs there now start in fullscreen
- **[UNCOVERED]** - Added `/claude-api upgrade` to migrate Python projects from `anthropic` 0.x to 1.x, and updated the skill's Python reference for 1.x (timeouts use `anthropic.Timeout`, not `httpx.Timeout`)
- **[UNCOVERED]** - Cloud sessions: plugins synced from claude.ai now show as `name@synced`, work with `claude plugin enable/disable <name>@synced`, and never override a same-named plugin you installed
- **[UNCOVERED]** - Alpine/musl builds: native image paste, clipboard, and audio-capture add-ons now load (musl-built binaries instead of glibc ones refused by the runtime)
- **[UNCOVERED]** - The usage-limit message shown when your monthly spend limit is already used up now also says when your session or weekly limit resets
- **[UNCOVERED]** - Fixed Bedrock streaming behind proxies that strip the response Content-Type header, which silently doubled billed API calls by re-running every turn non-streaming
- **[UNCOVERED]** - Fixed Claude Code hanging at startup behind an HTTPS proxy when using Bedrock with an SSO profile and `awsAuthRefresh` — the credential pre-check now honors `HTTPS_PROXY`
- **[UNCOVERED]** - Fixed a raw crash dump when starting Claude Code from a directory that no longer exists; it now prints a clear message
- **[UNCOVERED]** - Fixed Edit and Write calls pausing for about 5 seconds in JetBrains IDE terminals when the Claude Code plugin is connected
- **[UNCOVERED]** - Fixed a race where pressing Esc with a prompt queued could let the next turn finish early, leaving the session idle while Claude was still working and letting a later resubmit repeat actions
- **[UNCOVERED]** - Fixed WebFetch retaining expired page content in memory for the whole session instead of the intended 15 minutes
- **[UNCOVERED]** - Fixed cloud sessions (Claude Code on the web, desktop and mobile apps) resuming out of plan mode after an idle worker restart
- **[UNCOVERED]** - Fixed MCP elicitation forms taller than the terminal being clipped in fullscreen mode: the form now fits the window, with hidden fields reachable by scrolling and Accept/Decline always visible
- **[UNCOVERED]** - Fixed remote MCP servers staying failed after a transient 5xx on a mid-session reconnect in cloud sessions or via SDK `setMcpServers()`
- **[UNCOVERED]** - Fixed custom session titles disappearing from `/resume` after more than ~64 KB of conversation was written following the rename
- **[UNCOVERED]** - Fixed `claude -c`/resume picking up sessions from a different directory whose path differed only by characters like `_`, `-`, or `.`
- **[UNCOVERED]** - Fixed `/resume` and the agents view showing a session as recently changed (and reordering it) when only its file was touched or it was merely reopened
- **[UNCOVERED]** - Fixed `/resume` in all-projects mode telling you to `cd` into a deleted directory (e.g. a removed worktree); such sessions now resume in the current directory
- **[UNCOVERED]** - Fixed the `dark-ansi` theme rendering expanded tool results in fullscreen mode with text the same color as the background
- **[UNCOVERED]** - Fixed the fullscreen renderer prompt reappearing on every launch when it could never be answered; it now stops after being shown on three launches
- **[UNCOVERED]** - Fixed `.worktreeinclude` patterns starting with `**/` silently matching nothing when the target lived in a gitignored directory
- **[UNCOVERED]** - Fixed agents, skills, and commands whose `.md` file starts with a UTF-8 BOM being silently ignored
- **[UNCOVERED]** - Fixed `/insights` echoing literal `<message>` tags in its response on some models
- **[UNCOVERED]** - Fixed marketplace `metadata.pluginRoot` having no effect: bare plugin source names now resolve under it as the docs describe
- **[UNCOVERED]** - Fixed mouse movement in browser-based terminals inserting text like `"35;150;7M"` into the prompt when a mouse report arrived split across writes
- **[UNCOVERED]** - Fixed custom theme overrides for the effort/ultracode status badge colors being ignored
- **[UNCOVERED]** - Fixed OpenTelemetry trace fragmentation: tool executions deferred by a `PreToolUse` hook now resume in the original turn's trace instead of starting a new trace
- **[UNCOVERED]** - Fixed vim mode in the agent view: Escape now switches to NORMAL mode and keeps your text instead of clearing the prompt
- **[UNCOVERED]** - Fixed the `selection:copy` keybinding silently dropping a text selection that had been extended with Shift+Arrow keys
- **[UNCOVERED]** - Fixed the `/voice` startup tip still appearing after voice dictation was enabled via the `voice.enabled` setting
- **[UNCOVERED]** - Fixed shell-mode (`!`) Tab completion dropping the `./` from a `./script` path, which left a command the shell couldn't run
- **[UNCOVERED]** - Fixed fullscreen mode answering a permission prompt or pressing a button when you clicked the terminal window only to bring it back into focus
- **[UNCOVERED]** - Fixed slash-command panels (e.g. `/config`, `/model`) in fullscreen mode covering the latest messages; the conversation now stays pinned above the panel
- **[UNCOVERED]** - Fixed the `/workflows` detail dialog overflowing the terminal and losing its header off-screen when opened while Claude is still responding
- **[UNCOVERED]** - Fixed the Linux sandbox making a nonexistent `.git/config.worktree` unreadable, which broke every sandboxed git command in repos with `extensions.worktreeConfig` set
- **[UNCOVERED]** - Fixed hooks failing with "posix_spawn ENOENT" after the session's working directory was deleted; they now run from the project root or home directory instead
- **[UNCOVERED]** - Fixed `claudeMdExcludes` not excluding a symlinked `.claude/rules` file when the pattern names the rules directory or the symlink rather than its target
- **[UNCOVERED]** - Fixed runaway session-title syncing to Remote Control when two Claude Code processes shared one background job's state (2.1.232 regression); title updates are now deduplicated and rate-limited
- **[UNCOVERED]** - Fixed sessions whose title starts with `/` being unaddressable by `SendMessage` and shown as "(untitled)" in `ListAgents`
- **[UNCOVERED]** - Fixed Ctrl+W, Ctrl+U, Ctrl+K, Option+Backspace, Option+D and vim `df`/`dt` leaving a broken `[Pasted text #N]` placeholder when the cursor was inside it
- **[UNCOVERED]** - Fixed masked (password-style) inputs such as the login code field letting their text be pasted back with Ctrl+Y elsewhere or saved to prompt history when cleared with double Esc
- **[UNCOVERED]** - Fixed Ctrl+Backspace deleting one character instead of a word in search boxes
- **[UNCOVERED]** - Fixed a request rejected by an organization policy check being re-sent before the rejection was shown
- **[UNCOVERED]** - Improved the reminder shown after compaction so a skill's original arguments are not re-run as a new request
- **[UNCOVERED]** - Long file paths on tool-use rows now truncate in the middle to stay on one line
- **[UNCOVERED]** - Remote sessions keep sending keep-alives while a long `SessionStart` or `Setup` hook runs, so the container is not idle-reaped mid-hook
- **[UNCOVERED]** - `/goal`: repeat check-ins on long-running background work now back off (30 min, then 1 h, then every 2 h) instead of repeating every 30 minutes
- **[UNCOVERED]** - `/goal`: resuming a session from the `claude --resume` picker now restores its active goal
- **[UNCOVERED]** - `ListAgents` now tells a session its own name (the one peers use to message it), and `SendMessage` to your own name says so instead of "no agent named …"
- **[UNCOVERED]** - `ListAgents` and `/list-agents` now list your live teammates (previously only subagents and other sessions appeared, so a reachable teammate looked absent)
- **[UNCOVERED]** - `keybindingFlavor: "readline"` now also matches Bash for word keys: Alt+F and Ctrl/Option+→ stop at the end of the word, Alt+D deletes to it (Ctrl+Y pastes it back), and punctuation separates words
- **[UNCOVERED]** - Persistent retry mode (`CLAUDE_CODE_RETRY_WATCHDOG`) now fails immediately on organization spend-limit and out-of-credits errors instead of waiting indefinitely for a reset
- **[UNCOVERED]** - Claude in Chrome: `/clear` now closes the session's Chrome tab group, and empty groups are closed on `/resume` and when Claude Code exits
- **[UNCOVERED]** - Remote sessions: images uploaded from mobile now include their saved file path, so Claude can copy them into files it creates
- **[UNCOVERED]** - Claude Code on the web: requests from Bash and other tools to non-API anthropic.com hosts (e.g. www, docs) now go through the session's network proxy, so your environment's allowed domains apply
- **[UNCOVERED]** - Remote Control: clearer message and `claude doctor` wording when Remote Control isn't enabled for your account
- **[UNCOVERED]** - Windows: cross-session messaging is now available, so Claude Code sessions across your machines can message each other with `SendMessage` and find each other with `ListAgents`, as on macOS and Linux
- **[UNCOVERED]** - [VSCode] "View usage" in the usage-limit banner now sits inline with the warning text instead of floating mid-banner

#### v2.1.238

- **[covered]** - Fixed Remote Control model picks made on a phone or web not updating the model shown in the terminal
  - Covered by: `cc-native/configuration/CC-env-vars-reference.md`
- **[UNCOVERED]** - Added a `keybindingFlavor` setting: set it to `"readline"` to make Ctrl+W in the prompt delete back to the previous whitespace, as in Bash; the default (`"classic"`) is unchanged
- **[UNCOVERED]** - Plugin marketplaces: `headersHelper` on a url marketplace or a catalog entry runs a command that mints HTTP headers (e.g. a short-lived token) for catalog and same-origin archive fetches
- **[UNCOVERED]** - A catalog entry's `headersHelper` runs only when you install or update that plugin, after its command is shown; `claude plugin install/update` ask `[y/N]` (or pass `-y`)
- **[UNCOVERED]** - Added `claude self-hosted-runner --defer-shutdown-max-min <minutes>`: on SIGTERM, keep serving attached sessions, park what is left after that many minutes, then exit
- **[UNCOVERED]** - Added `claude self-hosted-runner --proxy-authorization-command` / `--proxy-authorization-file` for egress proxies that require a freshly issued `Proxy-Authorization` header on every connection
- **[UNCOVERED]** - Fixed unbounded memory growth in long interactive sessions: subagent tool results are now released once they leave the recent display window
- **[UNCOVERED]** - Fixed custom, project, and plugin output styles drifting back to the default voice mid-session
- **[UNCOVERED]** - Fixed `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=true` not keeping prompt suggestions on when your account is near, but not over, its usage limit
- **[UNCOVERED]** - Fixed worktree-isolation Bash refusals telling you to remove a redirect when the command had none
- **[UNCOVERED]** - Fixed self-hosted runners occasionally being removed by the server after a single slow or lost poll request, handing their healthy session to another runner
- **[UNCOVERED]** - Fixed MCP elicitation dialogs showing nothing for URLs longer than 4,096 characters, and permission prompts dropping the "don't ask again" option when the project path didn't fit the terminal width
- **[UNCOVERED]** - Fixed leftover `/tmp/claude-*-cwd` files when a Bash command is killed, times out, or is interrupted
- **[UNCOVERED]** - Fixed held Backspace being ignored on terminals that send Ctrl+H for Backspace when keystrokes arrive in large bursts (slow SSH/mosh links)
- **[UNCOVERED]** - Fixed text-wrapping in permission prompt diffs: lines containing wide multi-code-point characters (such as emoji) or tabs are no longer clipped
- **[UNCOVERED]** - Fixed killing a suspended (Ctrl+Z) session sometimes leaving the terminal in bracketed-paste mode with the cursor hidden
- **[UNCOVERED]** - Fixed stdio MCP servers receiving a `server/discover` request before `initialize`, forcing lazy servers to start their backend on every session open
- **[UNCOVERED]** - Fixed a proxy's refusal of a connection being reported as a generic network error instead of naming the proxy
- **[UNCOVERED]** - Fixed the `/model` and `/effort` cache-miss warning appearing when the prompt cache had already expired
- **[UNCOVERED]** - Fixed per-task Stop from the Remote Control tasks panel doing nothing on CLI-hosted sessions
- **[UNCOVERED]** - Fixed remote sessions exiting when a client delivered a user message without a valid role
- **[UNCOVERED]** - Fixed Remote Control sessions started by `claude remote-control` inheriting session-scoped environment variables from the launching shell
- **[UNCOVERED]** - Fixed a Remote Control session whose process crashed staying unavailable until `claude remote-control` was restarted; it can now be reused when you next message it
- **[UNCOVERED]** - Fixed Remote Control messages sent from the web or Desktop while Claude is mid-turn disappearing from the transcript after the turn finishes
- **[UNCOVERED]** - Fixed Remote Control disconnecting with "login expired" when a brief network hiccup delays renewing your sign-in; it now retries and stays connected
- **[UNCOVERED]** - Fixed Remote Control reporting a failed reconnect on sign-out; signing out now ends the session with a clear message
- **[UNCOVERED]** - Fixed `ListAgents`/`SendMessage` reporting "Remote Control is not connected" in sessions run by `claude remote-control` (server mode) or Desktop/IDE hosts; they now list and reach Remote Control peers
- **[UNCOVERED]** - Fixed `ListAgents` and `SendMessage` exposing the idle worker that the agent view pre-warms for your next background session; it now appears only once a task claims it
- **[UNCOVERED]** - Cross-session messaging: sending to a session on this machine that refuses inbound messages (e.g. `crossSessionInbound: "refuse"`) now reports "refused" to the sender instead of a silent success
- **[UNCOVERED]** - Cross-session messaging: a session whose inbox drops your messages (rate limit or full queue) now tells your session, instead of the messages vanishing silently
- **[UNCOVERED]** - Improved startup: bare `claude` starts sooner on macOS
- **[UNCOVERED]** - Improved Bash tool permission checking for zsh-specific syntax in shell conditionals
- **[UNCOVERED]** - Improved Remote Control connection resilience: brief HTTP 403 refusals from a network edge, VPN, or proxy are now tolerated for up to 3 minutes, with the refusing party named when a block persists
- **[UNCOVERED]** - Improved startup responsiveness: the automatic update check now runs about 10 seconds after launch instead of competing with startup for CPU
- **[UNCOVERED]** - Updated the bundled `claude-api` skill for the Managed Agents Aug 19 release: web search/fetch domain settings and memory stores on self-hosted sandboxes
- **[UNCOVERED]** - Changed Ctrl+L and Cmd+K in fullscreen to always just repaint — the double-press `/clear` shortcut was removed, and 1-row nvim terminals no longer trigger automatic `/clear` loops
- **[UNCOVERED]** - Changed `claude mcp list` and `claude mcp get` to show disabled servers as `⊘ Disabled` instead of connecting to them for a health check
- **[UNCOVERED]** - MCP `headersHelper` in a project `.mcp.json`, and inline MCP servers in project or `--add-dir` agent files, now require that folder's trust dialog to have been accepted (also under `claude -p`)
- **[UNCOVERED]** - MCP `headersHelper` from a project `.mcp.json`, plugin, or agent file runs without inherited credential env vars; user, managed and claude.ai-scope helpers now run from the Claude config dir

#### v2.1.237

- **[UNCOVERED]** - Fixed prompt caching for sessions using an LLM gateway or custom base URL
- **[UNCOVERED]** - Added a built-in "Concise" output style: Claude leads with results and skips preamble and narration, while doing the work just as thoroughly. Select it under Output style in /config.

#### v2.1.236

- **[UNCOVERED]** - Added `ANTHROPIC_DEFAULT_MODEL` environment variable: sets the model new sessions start on, while a `/model` pick still overrides it and persists across restarts (unlike `ANTHROPIC_MODEL`)
- **[UNCOVERED]** - Added `notify_when_idle` to cross-session `SendMessage`: ask another Claude Code session on this machine to send one notice when it next goes idle — opt-in, one-shot, no polling (macOS and Linux)
- **[UNCOVERED]** - Sandbox: on macOS, wildcard read-deny rules (e.g. `**/.env`) now take precedence inside allowed read regions, cover matched directories' contents, and can't be bypassed by renaming the denied file
- **[UNCOVERED]** - Fixed clipboard copy, background housekeeping, background sessions, and local MCP logs breaking after the directory a session had switched into was removed (since 2.1.229)
- **[UNCOVERED]** - Fixed the fullscreen renderer failing permanently after a single failed start: it now falls back to the classic renderer instead of exiting on every subsequent launch
- **[UNCOVERED]** - Fixed the `/model` picker rendering taller than the terminal: it now shows only as many models as fit the window, with the rest reachable by scrolling
- **[UNCOVERED]** - Fixed `SendMessage` calls being rejected when a malformed closing tag left the message text inside the summary field
- **[UNCOVERED]** - Fixed unhandled promise rejections when a subprocess fails to start, for example `powershell.exe` on WSL with Windows interop disabled (regression in 2.1.234)
- **[UNCOVERED]** - Fixed fullscreen mode sometimes not showing a newly sent message until the next update after the terminal was resized
- **[UNCOVERED]** - Fixed a blank band that could remain above the prompt after clearing a multi-line prompt, and panes not repainting after resizing the terminal away and back, in fullscreen mode
- **[UNCOVERED]** - Fixed the managed-settings approval prompt sometimes not appearing at startup while still capturing the first keypress as approval
- **[UNCOVERED]** - Fixed terminal tab titles jumping in tmux (iTerm tmux integration): the title is now written only when its text changes instead of animating every 960ms
- **[UNCOVERED]** - Fixed an unclear error when the cloud environments list came back empty or malformed
- **[UNCOVERED]** - Fixed the Fable 5 first-time usage-credits prompt auto-selecting the fallback model after 60 seconds with no answer when using Remote Control
- **[UNCOVERED]** - Fixed spinner tips never appearing, with a repeated background error, when the cached guest-pass reward in `~/.claude.json` was malformed
- **[UNCOVERED]** - Fixed skills hot-reload in SDK/VS Code sessions raising an error on every skills change after the session's working directory was deleted (2.1.229+)
- **[UNCOVERED]** - Fixed self-hosted runner sessions released on idle, retire, or startup timeout occasionally resuming on another runner before the post-session hook had finished
- **[UNCOVERED]** - Fixed the Clawd mascot's eyes and feet rendering unevenly in iTerm2 at some font sizes
- **[UNCOVERED]** - Fixed occasional runaway session recaps: recap text (automatic and `/recap`) is now capped at 400 characters, cut at a word boundary
- **[UNCOVERED]** - Improved startup performance: the session counter is now written in the background
- **[UNCOVERED]** - Improved auto mode: `Monitor` allow rules are now set aside while auto mode is active, so Monitor commands are reviewed the same way Bash commands are
- **[UNCOVERED]** - Improved auto mode on Bedrock, Vertex AI, and Foundry, and when telemetry is disabled: the classifier now uses the same defaults as on the Claude API, including severity-scored classification
- **[UNCOVERED]** - Improved auto mode: the git status check can no longer be fooled by a repo's `status.showUntrackedFiles=no` setting into reporting a clean tree
- **[UNCOVERED]** - Changed the `/model` picker to highlight only the newest model's name, so the highlight marks the new release rather than an arbitrary subset of the list
- **[UNCOVERED]** - `/goal`: an idle session whose goal is parked behind long-running background work now checks in automatically after 30 minutes (then 1h, 2h) instead of waiting for you to return
- **[UNCOVERED]** - `/usage` now shows the usage-credits spend row for Team and Enterprise members, and shows a capped row at 0% before anything is spent
- **[UNCOVERED]** - SIGTERM in print/SDK mode no longer records an interrupted turn or synthetic tool denials before exiting; running commands are still terminated and the process still exits with code 143
- **[UNCOVERED]** - Pressing Enter on a slash-command typo or a command unavailable in this session now reports it instead of running the closest fuzzy match; prefixes and aliases still run
- **[UNCOVERED]** - Remote Control now marks a session offline within seconds when the CLI exits or its terminal closes
- **[UNCOVERED]** - `SendMessage` now refuses further messages to a session up front once a rapid burst would exceed what that session's inbox accepts, instead of reporting them sent while they were dropped
- **[UNCOVERED]** - Aligned the session title chip on the prompt border with the footer's right edge
- **[UNCOVERED]** - Right-aligned footer items (goal indicator, session state, background agent status) and truncated notices now share a consistent right margin with the rest of the prompt area
- **[UNCOVERED]** - [VSCode] Added screen reader support for the transcript: live announcements for replies, permission requests, errors, and status changes, plus per-turn heading navigation

#### v2.1.235

- **[UNCOVERED]** - Added an optional `spellcheck` setting that underlines misspelled words in the prompt input as you type, using your installed `aspell`, `hunspell`, or `ispell`
- **[UNCOVERED]** - Fixed whole-prompt-cache invalidation when a language server disconnected or reconnected mid-session
- **[UNCOVERED]** - Fixed nested markdown list items misaligning at depth 3+ and added a hanging indent to wrapped list items in the terminal UI
- **[UNCOVERED]** - Fixed prompt input highlights (slash commands, keywords, mentions) appearing shifted by one or more characters in some multi-line prompts
- **[UNCOVERED]** - Fixed Shift+Tab inside the permission prompt's comment field approving the edit and granting session-wide edit permission instead of closing the field
- **[UNCOVERED]** - Fixed the Agent tool advertising a general-purpose default in sessions where that agent is unavailable: an omitted `subagent_type` there now gets a clear error listing the available agents
- **[UNCOVERED]** - Fixed notebook cell delete/replace approval dialogs silently omitting the existing cell content when the notebook or cell could not be read; the dialog now says why
- **[UNCOVERED]** - Fixed slash commands run while Claude is responding showing HTML entities instead of the actual characters
- **[UNCOVERED]** - Fixed the prompt footer not showing the "Update installed" restart notice after a background auto-update
- **[UNCOVERED]** - Fixed the expanded task list (`ctrl+t`) always starting collapsed when resuming or relaunching into a session that still has open tasks
- **[UNCOVERED]** - Improved memory and CPU usage while cloud sessions such as `/ultrareview` or `/autofix-pr` run in the background — their event streams are no longer re-scanned and re-rendered on every update
- **[UNCOVERED]** - Improved permission dialogs: display text and "don't ask again" options now always match what a grant would cover, and "don't ask again" is withheld when contents cannot be fully displayed
- **[UNCOVERED]** - Improved the embedded `grep` in native macOS/Linux builds: pathological patterns now fail fast instead of exhausting memory, and `-m N` with `-A/-C` prints correct context
- **[UNCOVERED]** - Improved the context-limit error to say when auto-compact is off and point to `/config` to re-enable it
- **[UNCOVERED]** - Vim mode: NORMAL mode and cursor position are now preserved when toggling the detailed transcript (ctrl+o) or closing a panel
- **[UNCOVERED]** - Dialogs: arrow keys and Enter pressed in quick succession now select the option you navigated to instead of the previously highlighted one
- **[UNCOVERED]** - `SendMessage` now refuses messages too large for cross-session delivery up front instead of silently dropping them
- **[UNCOVERED]** - Remote Control: `claude rc` now applies the same enterprise-gateway availability check as interactive startup
- **[UNCOVERED]** - [VSCode] Fixed focus jumping between open Claude tabs on its own when a window with several Claude panels is restored or reloaded

#### v2.1.234

- **[UNCOVERED]** - Added the optional `CLAUDE_CODE_PROJECT_DIR_NAME` environment variable: hosts that give each session its own config directory can choose a short name for the per-project transcript directory
- **[UNCOVERED]** - Added the `selection:clear` keybinding action, so a key can be bound to clear an in-app text selection; also works in the agents view
- **[UNCOVERED]** - Added a GitLab merge request badge to the footer and statusline: repos with a GitLab remote and an authenticated glab CLI show MR !N with draft/pending/green states
- **[UNCOVERED]** - Claude Code now continues your session automatically when a claude.ai usage limit resets; turn it off in `/config` ("Continue automatically at usage limit")
- **[UNCOVERED]** - Claude is now told to use your account email only to identify you, and not to send it to unrelated services unless you ask
- **[UNCOVERED]** - Security: remote file reads, session restore, CLAUDE.md includes, workflow scripts and file uploads now reject Windows NT-namespace (`\??\`) paths, hardening the remaining pre-approval file accesses against the NTLM credential-leak vector
- **[UNCOVERED]** - Fixed auto mode in very long sessions repeatedly re-checking and denying sandboxed commands' network access after the conversation had been compacted
- **[UNCOVERED]** - Fixed session-scoped permission answers (including denies) being dropped when answering background subagent tool permission prompts
- **[UNCOVERED]** - Fixed a crash when an API response on the non-streaming fallback path (typically via third-party gateways) contained a thinking block missing its thinking field or a text block missing its text field
- **[UNCOVERED]** - Fixed markdown rendering becoming extremely slow for some messages containing unusual Unicode sequences
- **[UNCOVERED]** - Fixed `SendMessage` rejecting a recipient copied from `ListAgents` when the session name is at the 200-character cap or emoji-heavy
- **[UNCOVERED]** - Fixed repository detection mis-reading the host of git remotes with unusual userinfo, producing links and repo-specific behavior for the wrong host
- **[UNCOVERED]** - Fixed MCP diagnostics printing resolved secrets: scope-conflict warnings now show the configured `${VAR}` form, and connection-failure details show only the server origin
- **[UNCOVERED]** - Fixed `strictKnownMarketplaces` allowlists accepting SCP-style git marketplace sources whose host differs from the one git would actually connect to
- **[UNCOVERED]** - Fixed modal text such as the `/login` OAuth URL losing characters when copied in fullscreen
- **[UNCOVERED]** - Fixed a `---` horizontal rule in rendered markdown running into the line after it
- **[UNCOVERED]** - Fixed consecutive shell commands splitting into multiple "Ran 1 shell command" rows when todo/task updates were interleaved between them
- **[UNCOVERED]** - Fixed dialogs like `/permissions` opened while a `!` shell command was running being dismissed when the command finished
- **[UNCOVERED]** - Fixed a queued `!` shell command being sent to the model as plain text after pressing up-arrow to edit the queued input
- **[UNCOVERED]** - Fixed queued messages reappearing in the prompt history while still queued, Esc while selecting a queued message no longer interrupts the turn, and `!` mode no longer sticks after a mid-turn submit
- **[UNCOVERED]** - Fixed accepting the "Try the new fullscreen renderer?" prompt restarting the session without its permission mode (e.g. `--dangerously-skip-permissions`), tool allow/deny rules, model or effort flags
- **[UNCOVERED]** - Fixed `/tui` dropping launch `--allowed-tools`/`--disallowed-tools` rules when it restarts; it now declines to switch, with the reason, when the session has restrictions a restart can't carry over
- **[UNCOVERED]** - Fixed trust prompts omitting the repository-wide scope warning when the directory was first seen before the repository existed there
- **[UNCOVERED]** - Fixed a case where an IDE diff tab closing during a permission re-prompt could answer the new prompt with the previous input
- **[UNCOVERED]** - Fixed: files sent to the user during Remote Control sessions hosted by Claude Code Desktop or VS Code now upload, so they open on phone and web instead of showing an empty card
- **[UNCOVERED]** - Fixed: after `/login` while `CLAUDE_CODE_OAUTH_TOKEN` is set, the stale-token reminder no longer leaks into Claude's automatically resumed turn — it now appears only to you
- **[UNCOVERED]** - Fixed: permission previews now relay only to channel servers admitted by the inbound trust gate, and a server's explicit permission-capability opt-out is honored
- **[UNCOVERED]** - Fixed: credential masking on relayed permission previews can no longer hide commands, paths, or destinations from the approver; oversized private-key blocks now redact under full-strength redaction
- **[UNCOVERED]** - Fixed: provider API tokens that mask on permission previews now mask even when directly followed by shell delimiters
- **[UNCOVERED]** - Fixed Claude Desktop inter-session messages being silently dropped by the recipient session when cross-session messaging read as disabled, which left the sender's query "thinking" for many minutes
- **[UNCOVERED]** - Remote Control: signing this computer in to a different claude.ai account or organization now stops the running session within seconds and says why, instead of a misleading HTTP 404 hours later
- **[UNCOVERED]** - Remote Control sessions started from Claude Code Desktop or VS Code now keep phones and claude.ai/code updated on the session's permission mode (and claude.ai/code on the model) as they change
- **[UNCOVERED]** - Remote Control: effort picks made on a phone or on claude.ai/code now apply to terminal- and Desktop/VS Code-hosted sessions, and the session publishes its effort level to connected clients
- **[UNCOVERED]** - `SendMessage` and `ListAgents` now say when your account's session list was too long to check completely, instead of treating unseen sessions as absent
- **[UNCOVERED]** - Expired Anthropic profile credential now points you at `/login` when a claude.ai login would take precedence
- **[UNCOVERED]** - Improved the transcript: your own prompts now render markdown (highlighted code blocks, inline code, lists) the same way replies do
- **[UNCOVERED]** - Improved the "API returned an empty or malformed response" error to say what came back (content type, body kind, size, request ID) and why the original streaming request failed
- **[UNCOVERED]** - Improved auto-generated session titles to read as short, specific names (e.g. "Login button bug") rather than sentences restating your request (e.g. "Fix the login button on mobile")
- **[UNCOVERED]** - Reduced the context cost of loading the built-in `claude-api` skill from ~200k+ tokens to ~25k by loading reference docs on demand
- **[UNCOVERED]** - `/permissions` can now be opened while Claude is working — rule changes apply to the rest of the current turn
- **[UNCOVERED]** - `/add-dir <path>` can now be used while Claude is working; `/add-dir`, `/autocompact`, `/theme`, `/help`, `/config` and `/advisor` dialogs open mid-turn in the fullscreen TUI
- **[UNCOVERED]** - `/goal` now clears itself with a notice when a turn dies on an unrecoverable error (e.g. revoked auth, an exhausted credit balance, or a context overflow) instead of staying armed
- **[UNCOVERED]** - `/goal`: when background tasks keep a goal waiting for 30+ minutes, Claude now checks in on them instead of waiting indefinitely (set `CLAUDE_CODE_GOAL_CHECKIN_MINUTES=0` to opt out)
- **[UNCOVERED]** - `claude setup-token` now rejects unexpected extra arguments instead of silently ignoring them
- **[UNCOVERED]** - Changed Esc in fullscreen mode to no longer clear a mouse text selection: it interrupts or dismisses as usual and the selection stays highlighted
- **[UNCOVERED]** - Removed the redundant "Allowed by auto mode classifier" line that auto mode showed under every Agent tool call
- **[UNCOVERED]** - Removed the "Default teammate model" setting from `/config`; agent-team teammates now use the leader's model unless the spawn names one
- **[UNCOVERED]** - Dimmed the elapsed-time counter on the running tool header so it no longer competes with the bold counts
- **[UNCOVERED]** - Background task notifications delivered between turns are now sent to the model inside `<system-reminder>` tags, matching mid-turn delivery
- **[UNCOVERED]** - Mantle: skip the admin-pin availability probe at startup when a main-loop model is already picked
- **[UNCOVERED]** - Windows: startup no longer stalls on repeated rename retries when `~/.claude.json` is read-only

#### v2.1.233

- **[UNCOVERED]** - Added GitLab merge request URL support to the `--worktree` flag and the `claude agents` view (where MRs display as `!N`)
- **[UNCOVERED]** - Added an opt-in `forward_user_identity` apps gateway setting on Anthropic upstreams that sends the signed-in user's identity as headers, so a proxy behind the gateway can attribute spend per user
- **[UNCOVERED]** - Added opt-in memory cgroup support for Bash tool commands on Linux (`CLAUDE_CODE_TOOL_MEMORY_LIMIT`) so a runaway build can't stall the session
- **[UNCOVERED]** - Added `CLAUDE_CODE_WEBFETCH_CACHE_TTL_MS` environment variable to configure the WebFetch session URL cache TTL (default unchanged: 15 minutes)
- **[UNCOVERED]** - Fixed cloud sessions occasionally being marked as lost when the environment shut down while Claude was waiting on a permission prompt
- **[UNCOVERED]** - Fixed MCP v2 connections endlessly reopening the subscriptions/listen stream against servers that terminate long-held streams on a fixed timeout (e.g. serverless hosts)
- **[UNCOVERED]** - Fixed Notification hooks not firing for permission prompts when running under Claude Desktop or VS Code
- **[UNCOVERED]** - Fixed idle sessions on Linux sometimes keeping one CPU core at 100% when sandboxing is enabled
- **[UNCOVERED]** - Fixed bundled skill aliases like `/checkup` and `/review` reporting "Unknown command" in `-p` mode or with plugins/MCP loaded when a user or project skill shadows the bundled skill
- **[UNCOVERED]** - Fixed skill/command argument substitution to prevent argument values from being re-expanded as template markers
- **[UNCOVERED]** - Fixed Windows paths spelled with the NT `\??\` device prefix bypassing UNC path validation, closing an NTLM credential-leak vector
- **[UNCOVERED]** - Improved `claude self-hosted-runner` session start time: the session branch is now created without rewriting the working tree, and two server round trips no longer block the agent's launch
- **[UNCOVERED]** - Improved apps gateway error forwarding: 400/413 errors from Vertex, Foundry, and Claude Platform on AWS upstreams now carry the upstream's own message; fixes a bug with auto-compact on apps gateway
- **[UNCOVERED]** - Improved `claude plugin validate` to check a bare `.claude/skills` directory, reporting SKILL.md files whose frontmatter fails to parse
- **[UNCOVERED]** - Improved screen reader mode: the `/effort` selector renders as a numbered list with a typed-number prompt, and hint and dialog text is no longer clipped
- **[UNCOVERED]** - Improved print mode diagnostics: a `[claude-code:unrecognized_model]` line is written to stderr when a request goes out for a model ID Claude Code doesn't recognize; map it with `modelOverrides` to silence
- **[UNCOVERED]** - Changed the GitHub app setup tip to no longer appear in repositories whose origin remote is on gitlab.com or bitbucket.org; the enterprise marketplace tip now covers non-GitHub internal git hosts
- **[UNCOVERED]** - Todo/task-tracking tools (TaskCreate/Get/Update/List, TodoWrite) are no longer available on Opus 4.8, Sonnet 5, Fable 5, Mythos 5, and newer models; set `CLAUDE_CODE_ENABLE_TODO_TOOLS=1` to bring them back
- **[UNCOVERED]** - Windows: fixed auto mode repeatedly stopping for manual approval on ordinary `cd <dir> && <command> > file` Bash commands (a 2.1.232 regression)
- **[UNCOVERED]** - Reverted the 2.1.232 Bash permission changes for Cygwin-style symlinks on Windows and for input redirections (`< file`); a narrower version will return in a later release

#### v2.1.232

- **[covered]** - Hardened the Linux filesystem sandbox against a protected-path bypass
  - Covered by: `cc-native/sandboxing/CC-sandboxing-analysis.md`
- **[UNCOVERED]** - Subagent forking is now on by default: a `subagent_type: "fork"` subagent inherits the full conversation and prompt cache, and non-teammate agent spawns in interactive sessions now run in the background by default
- **[UNCOVERED]** - Type `@` in the prompt to mention another Claude session by name; Claude then uses `SendMessage` to reach that session directly
- **[UNCOVERED]** - `SendMessage` now delivers to a bare name that exactly matches one live session, instead of asking to confirm with a ref first
- **[UNCOVERED]** - Interactive sessions on one machine now keep unique names: starting or renaming a session to a name another live session already uses gives it a `name-word-word` variant and tells you
- **[UNCOVERED]** - Added `/config` rows for "Dialog expiry" and "Messages from your other sessions" (cross-session inbound accept/hold/refuse)
- **[UNCOVERED]** - Added secret redaction for GitLab token families (`glrt-`, `gloas-`, `glptt-`, `glagent-`, `glimt-`, `glsoat-`, `glcbt-`, `glft-`, `glffct-`) and full redaction of routable `glpat-`/`gldt-` tokens; the `glab` CLI config store gets the same sandbox and credential-path protection as `gh`
- **[UNCOVERED]** - Added GitLab support to plugin marketplaces: bare `gitlab.com` repo URLs (including nested subgroups) now clone like `github.com` URLs, and clone auth-failure hints name your actual git host
- **[UNCOVERED]** - Settings: `additionalMarketplaces` and `allowedMarketplaces` are now accepted as friendlier aliases for `extraKnownMarketplaces` and `strictKnownMarketplaces`
- **[UNCOVERED]** - Enterprise policy: a url-typed `blockedMarketplaces` entry for a bare repo URL keeps blocking that URL when the CLI classifies it as a git clone
- **[UNCOVERED]** - Gateway: the `desktop:` overlay now accepts every released Desktop setting (was 11 hand-listed keys), validated at boot against Desktop's own schema; unknown or invalid keys fail boot
- **[UNCOVERED]** - Gateway: empty `managed.policies[].match.groups`/`admin.admin_groups` entries and malformed `email_domain` values (empty, or containing `@`, whitespace, or commas) now fail at boot instead of silently matching no one or granting admin access
- **[UNCOVERED]** - Fable 5 is offered as an advisor in `/advisor` again for organizations with Fable access, with usage-credits consent set up through `/model fable`
- **[UNCOVERED]** - Fixed a PowerShell permission bypass where variable-writing parameters could silently overwrite `$PSDefaultParameterValues` and redirect later commands' file access
- **[UNCOVERED]** - Fixed a Windows permission bypass where Git Bash followed Cygwin-style symlinks that path validation saw as regular files; writes through them now require permission approval
- **[UNCOVERED]** - Fixed nested git repositories inheriting trust from a parent directory; each repository now requires its own trust confirmation
- **[UNCOVERED]** - Fixed MCP connections hanging for the full 30-second connect timeout when a server fails to answer or sends a malformed reply to the protocol-version probe
- **[UNCOVERED]** - Fixed Remote Control sessions hosted by a bridge inside a cloud session inheriting that session's transcript or credentials
- **[UNCOVERED]** - Fixed Remote Control sessions started from Claude Desktop or an IDE appearing as a new claude.ai session each time the local session was resumed; they now reattach to the existing one
- **[UNCOVERED]** - Fixed Remote Control sessions appearing unreachable to newly attached clients while idle
- **[UNCOVERED]** - Fixed Remote Control bridge sessions not restoring conversation history when the session worker restarts
- **[UNCOVERED]** - Remote Control: resuming a conversation whose session was deleted from claude.ai or the app now starts a replacement instead of failing with a message about your login (regressed in v2.1.227)
- **[UNCOVERED]** - Fixed Cloud gateway `/login` exiting silently or leaving an unresponsive terminal after "Press Enter to continue" when managed settings failed to load; the reason is now shown
- **[UNCOVERED]** - Fixed voice mode on native builds getting stuck on "listening…" when the voice service rejected the connection; the rejection is now shown immediately
- **[UNCOVERED]** - Fixed mTLS client certificate rotation requiring a restart; Claude Code now reloads the rotated cert and key automatically on connection errors
- **[UNCOVERED]** - Fixed malformed AWS or Vertex region values being used to build request URLs; they now fall back to the default region
- **[UNCOVERED]** - Fixed stream idle timeout errors failing the request instead of recovering on Bedrock, Vertex, and gateway deployments
- **[UNCOVERED]** - Fixed content-sized overlays containing truncated text rendering one column too wide, and start-truncated text collapsing to an ellipsis
- **[UNCOVERED]** - Fixed a stray garbled character where a long shell-command or agent-description preview was cut off mid-emoji
- **[UNCOVERED]** - Fixed a startup race that could silently unregister a plugin marketplace due to concurrent writes to `known_marketplaces.json`
- **[UNCOVERED]** - Fixed `/update` and `/tui` refusing to restart while work that survives the relaunch was running
- **[UNCOVERED]** - Fixed usage-limit guidance suggesting unavailable slash commands in SDK and remote sessions
- **[UNCOVERED]** - Fixed the consent message for interactive `--advisor fable` launches, which told you to run `/model fable` in an interactive session that had just exited
- **[UNCOVERED]** - Improved fullscreen streaming: long sessions stay responsive because the whole conversation is no longer re-normalized on every update
- **[UNCOVERED]** - Improved the managed settings approval dialog: shows endpoint URLs, uses clearer wording for telemetry-only changes, skips routine OpenTelemetry options, and requires approval for server-managed sandbox binary overrides (`sandbox.bwrapPath`, `sandbox.socatPath`, `sandbox.ripgrep`)
- **[UNCOVERED]** - `/feedback` and `/bug` now open immediately when invoked while Claude is responding, instead of waiting for the turn to finish
- **[UNCOVERED]** - `/plugin install plugin@marketplace` now refreshes the marketplace first, so newly published plugins install without a manual marketplace update
- **[UNCOVERED]** - `/code-review` at high, xhigh, and max effort now runs in a background agent like the other levels
- **[UNCOVERED]** - Pasted and clipboard images are read without blocking the event loop
- **[UNCOVERED]** - Remote Control now keeps reconnecting for about 30 minutes after a network blip and no longer drops after a few blips spread across an hour
- **[UNCOVERED]** - Remote Control: resuming a conversation no longer silently takes Remote Control away from another Claude Code on the same machine that still has it; run `/remote-control` there to move it
- **[UNCOVERED]** - Updated agent panel: completed subagents hide immediately with a `/tasks` footer hint, and the "↓ N more" overflow indicator moved left for visibility
- **[UNCOVERED]** - Remote Control: the terminal now says whether a session was taken over by another device, ended from another app, or deleted, and stops suggesting a reconnect that would undo it
- **[UNCOVERED]** - Bash input redirections (`< file`) are now permission-checked like their argument spellings on all platforms
- **[UNCOVERED]** - Shortened the message shown when resuming a completed background agent
- **[UNCOVERED]** - Cowork sessions no longer inline external @-imports from user-scope memory files
- **[UNCOVERED]** - Hardened the auto-generated cross-session messaging socket directory on shared `/tmp`: a pre-planted symlink or another user's directory is now refused instead of used
- **[UNCOVERED]** - Changed `sandbox.ripgrep` to be honored only from user, managed, and `--settings` settings; project settings can no longer override the sandbox's ripgrep binary
- **[UNCOVERED]** - Removed the startup tip suggesting you create custom subagents, and the matching nudge in the `/powerup` tour

#### v2.1.231

- **[UNCOVERED]** - Fixed MCP OAuth sign-in failing with a redirect URI mismatch for servers that use a pre-registered OAuth client, such as Slack

#### v2.1.229

- **[covered]** - Documented `claude remote-control --continue` for resuming the most recent Remote Control session
  - Covered by: `cc-native/configuration/CC-env-vars-reference.md`
- **[UNCOVERED]** - Added server-supplied Claude Code hook support for self-hosted runner sessions, matching managed-environment behavior
- **[UNCOVERED]** - Added SSE keepalive pings to gateway streaming responses during long thinking pauses, preventing idle-timeout disconnects on Vertex and Bedrock upstreams
- **[UNCOVERED]** - Added plugin marketplace `command` sources: a local command (e.g. an IDE) prints the plugin directory, which is re-resolved each session and applied without a restart; `mode: "link"` uses it in place
- **[UNCOVERED]** - `ListAgents` now marks disconnected Remote Control sessions as `offline` and labels your cloud sessions as `cloud`
- **[UNCOVERED]** - Fixed long responses partly disappearing while streaming and being printed twice in the terminal
- **[UNCOVERED]** - Fixed a crash to the error screen (including on `--resume` of the affected session) when a tool call had a non-string `glob`, `file_path`, or `command` value
- **[UNCOVERED]** - Fixed a RangeError crash when a progress bar or markdown table rendered in a very narrow terminal window (could also crash `claude --continue`/`--resume` at startup)
- **[UNCOVERED]** - Fixed a crash on Windows when a tool call or message referenced a file by an extended-length (`\\?\`) or UNC path
- **[UNCOVERED]** - Fixed auto mode failing on every tool call for users who disable the attribution header via `CLAUDE_CODE_ATTRIBUTION_HEADER` (direct Anthropic API connections)
- **[UNCOVERED]** - Fixed `/model` rejecting Sonnet/Opus 1M for claude.ai subscribers using a custom `ANTHROPIC_BASE_URL` gateway
- **[UNCOVERED]** - Fixed MCP OAuth with strict authorization servers by using `127.0.0.1` instead of `localhost` in the redirect URI
- **[UNCOVERED]** - Fixed Remote Control clients showing a stuck working spinner after a slash command typed in the laptop terminal
- **[UNCOVERED]** - Fixed the Claude Code Review workflow generated by `/install-github-app` completing without posting its review on the pull request
- **[UNCOVERED]** - Fixed multi-second UI stalls after editing a file with thousands of IDE diagnostics while the IDE extension is connected
- **[UNCOVERED]** - Fixed one-shot `claude plugin` commands leaving a stray liveness file that could prevent cleanup of outdated plugin versions
- **[UNCOVERED]** - Fixed dynamic workflows inside CPU-limited containers using the host machine's core count instead of the container's CPU limit
- **[UNCOVERED]** - Fixed a file-watcher handle leak after atomic file replacements, and an uncaught error on Windows when the scheduled-tasks watcher failed on a network or virtual filesystem
- **[UNCOVERED]** - Fixed SDK and `--input-format stream-json` sessions getting a 400 API error when a whitespace-only message was submitted
- **[UNCOVERED]** - Fixed conversations whose messages alone exceed the API's 32 MB request limit retrying compaction when no images or documents can be stripped; they now fail once with a clear message
- **[UNCOVERED]** - Fixed OpenTelemetry export from Claude Desktop sessions being rejected by the Desktop-managed gateway when that gateway is also the telemetry endpoint
- **[UNCOVERED]** - Fixed self-hosted runner and other remote sessions exiting at startup when `managed-mcp.json` is deployed and the server delivers MCP servers; those servers are now skipped with a warning
- **[UNCOVERED]** - Fixed self-hosted runner repository preparation hanging on a Git Credential Manager prompt; git now fails fast when credentials are missing
- **[UNCOVERED]** - Improved workflow fan-outs to stagger same-prefix sibling agents so subsequent agents read the cached prompt prefix instead of re-paying it (`CLAUDE_CODE_WORKFLOW_PREFIX_STAGGER_MS=0` disables)
- **[UNCOVERED]** - Improved "prompt is too long" errors to explain why automatic compaction could not recover instead of only suggesting `/compact`
- **[UNCOVERED]** - Improved sandbox: IPv6 literals in network domain lists are now bracketed (`[::1]:443`), and ambiguous spellings are enforced fail-closed and flagged by `/doctor`
- **[UNCOVERED]** - Updated `/login` to repeat the `CLAUDE_CODE_OAUTH_TOKEN` override warning after a successful login
- **[UNCOVERED]** - Changed `/commit-push-pr` so git/gh commands with dangerous flags (`--force`, `--amend`, `--no-verify`, etc.) are no longer auto-approved
- **[UNCOVERED]** - Changed self-hosted runner Windows startup to require an explicit `--base-dir`; there is no default checkout directory on Windows
- **[UNCOVERED]** - [VSCode] "Report a problem" and `/bug` now open the built-in feedback dialog instead of a retired survey link
- **[UNCOVERED]** - [VSCode] Made the `/btw` side-question panel resizable by dragging its boundary, in both side-docked and stacked layouts
- **[UNCOVERED]** - [VSCode] Added session groups in the sidebar — right-click to create, rename, or delete; Cmd/Ctrl- or Shift-click to move several sessions at once

#### v2.1.228

- **[UNCOVERED]** - Fixed interactive sessions that could stop redrawing entirely, while the process kept running, after a rare internal layout error
- **[UNCOVERED]** - Fixed `git` / Git Bash not being found on Windows when Claude Code is launched from a parent folder of the git installation
- **[UNCOVERED]** - Fixed `/tui` reverting the session to an earlier model when `/model` had been changed since the last response
- **[UNCOVERED]** - Fixed cross-session messaging sometimes starting without an inbox in the first session after install or upgrade
- **[UNCOVERED]** - Fixed Remote Control `/resume` while connected leaking the resumed conversation's title or history into the connected session
- **[UNCOVERED]** - Fixed `claude self-hosted-runner` sessions failing on every fresh runner when the `checkout` hook fails for a repository the session doesn't push to; that repository is now skipped with a warning
- **[UNCOVERED]** - Fixed self-hosted runners ending sessions in the gap between a background task finishing and the follow-up turn starting
- **[UNCOVERED]** - Fixed session cleanup deleting contents inside a project's memory folder
- **[UNCOVERED]** - Fixed background plugin-cache cleanup deleting a plugin's cache when its only version is a symlinked development checkout
- **[UNCOVERED]** - Fixed a settings-merge issue where a marketplace entry redefined in a higher-precedence settings tier could inherit another tier's custom headers; marketplace entries now merge as whole entries
- **[UNCOVERED]** - Fixed the deferred-tools reminder occasionally being sent to the model twice after a skill invocation
- **[UNCOVERED]** - Hardened skills synced from claude.ai: they no longer shadow local commands or MCP prompts, their descriptions are sanitized and labeled, and on your machine their bodies don't run `!` commands or expand `@` files
- **[UNCOVERED]** - Improved cross-session messages: the sender and body now display inline instead of a collapsed line, and messages to Remote Control sessions on other machines show your Remote Control session name as the sender
- **[UNCOVERED]** - Improved Vertex AI credential handling: expired or missing Google Cloud credentials now fail within seconds instead of retrying for minutes
- **[UNCOVERED]** - Improved compaction progress: the retry countdown and stall hint now appear during compaction instead of only a progress bar
- **[UNCOVERED]** - Updated terminal title busy-spinner glyphs to reduce tab-bar jitter on some terminals
- **[UNCOVERED]** - Changed the Write tool so newer models can overwrite an existing file they haven't read this session, matching the Edit tool's rules; older models still require the read first
- **[UNCOVERED]** - Removed the outdated note about auto mode sessions costing slightly more from the first-use notice for Pro, Max, and Team plans

#### v2.1.227

- **[UNCOVERED]** - Fixed feature flags being evaluated without the user's subscription tier when a session started with an expired login token, which could wrongly prompt Max plan users to enable usage credits for Fable
- **[UNCOVERED]** - Fixed every Bash command failing under `claude-code-action` with `allowed_non_write_users` on GitHub-hosted runners
- **[UNCOVERED]** - Fixed `/tui` bringing back a conversation that had been rewound to before its first message
- **[UNCOVERED]** - Improved slash-command menu: blue now marks only the selected row, matched characters are bolded instead of recolored, and emoji or accented names keep their glyphs
- **[UNCOVERED]** - Improved performance: fewer event-loop stalls on file-not-found suggestions and at-mention size checks

#### v2.1.226

- **[UNCOVERED]** - Bug fixes and reliability improvements

#### v2.1.225

- **[UNCOVERED]** - Added gateway spend-limit support to Claude Code's usage warning; the limit-reached message now names the cap, its reset time, and the operator's message (requires the gateway on 2.1.225)
- **[UNCOVERED]** - Added a workspace trust prompt to `claude agents` for untrusted directories, matching the behavior of `claude`
- **[UNCOVERED]** - Fixed a transient 401 replacing a long-lived `CLAUDE_CODE_OAUTH_TOKEN` with a stored login's short-lived token, breaking headless sessions until restart
- **[UNCOVERED]** - Fixed MCP OAuth servers on macOS intermittently failing with a burst of 401 errors, as if never authenticated, after a keychain read timed out
- **[UNCOVERED]** - Fixed auto mode counting a safety-filter refusal of its own permission check toward the consecutive-block limit; the action is still denied, but the model is now told to move on rather than retry
- **[UNCOVERED]** - Fixed cross-session messages staying parked without a notice or expiry in headless sessions and during startup
- **[UNCOVERED]** - Fixed conversation history breaking on Remote Control session resume after very large conversations were compacted
- **[UNCOVERED]** - Fixed hovering over a session in another project in the agents list changing the directory the next agent starts in
- **[UNCOVERED]** - Fixed `claude self-hosted-runner` registering and then failing every session when `--base-dir` cannot be created or written; it now exits at startup with a clear error
- **[UNCOVERED]** - Fixed Claude Code on the web sessions being misreported as stuck, re-sending a growing event backlog on every reconnect
- **[UNCOVERED]** - Improved Remote Control: photos attached from the Claude app are now shown to Claude directly instead of being read from disk with a separate tool call
- **[UNCOVERED]** - [VSCode] Fixed Focus view folding away the latest to-do list, a pending question's context, and settled answers; thinking-only folds show "Thought for Ns" and re-collapse when their turn completes
- **[UNCOVERED]** - SendMessage can now start a conversation with your Remote Control sessions on other machines by name (`ListAgents` shows them as `name [ref]`), instead of only replying after they message you first
- **[UNCOVERED]** - SendMessage: a Remote Control recipient you already confirmed is never swapped for a same-named session on this machine when its own list couldn't be checked

#### v2.1.224

- **[UNCOVERED]** - Added self-hosted environments: `claude self-hosted-runner` turns your own machines or containers into a place Claude Code web, mobile, and desktop sessions can run, on Team and Enterprise plans
- **[UNCOVERED]** - Added `archive` plugin source: install plugins from a zip over HTTPS without git or npm, with optional SHA-256 pinning
- **[UNCOVERED]** - Added a cancel-and-confirm step when removing an unavailable paste changes a command's text
- **[UNCOVERED]** - Added `ANTHROPIC_BEDROCK_REGION_PREFIX` env var for Bedrock to prefer a specific cross-region inference profile over the `AWS_REGION`-derived one
- **[UNCOVERED]** - Added `crossSessionInbound` and `dialogExpiry` settings: cross-session messages sent to a session running with bypassed permissions are held for your approval, and messages to other sessions auto-deliver
- **[UNCOVERED]** - Added sandbox credential-masking options: `extract` and `onExtractNoMatch` for structured env values, `decode: "jwt"` with `maskClaims` for JWT-aware masking, and `awsPairs`/`sigv4` for AWS SigV4 re-signing; these need `network.tlsTerminate` and are honored only from user, managed, or `--settings` settings
- **[UNCOVERED]** - Added cross-session `SendMessage`: Claude Code sessions can now message each other, on any of your machines, with `ListAgents` to discover them (macOS and Linux)
- **[UNCOVERED]** - Fixed long (>200 char) project paths resolving to another project's session directory under a shared sanitized prefix; session list, rename, fork, delete and `/resume` no longer cross projects
- **[UNCOVERED]** - Fixed `SendMessage` reporting "Message sent" when the write to a teammate's inbox had actually failed; failed deliveries are now reported as errors
- **[UNCOVERED]** - Fixed sandbox filesystem deny entries written with a trailing slash (e.g. `denyRead: "~/.aws/"`) being silently bypassable on Linux and macOS
- **[UNCOVERED]** - Fixed sandbox violation details never appearing in Bash tool results; Claude now sees which file or network access was denied and why
- **[UNCOVERED]** - Fixed MCP tools that connect mid-turn being deferred for tool search without their names announced to the model
- **[UNCOVERED]** - Fixed plugin install records being silently corrupted when the same plugin is installed in multiple projects
- **[UNCOVERED]** - Fixed recalled or restored paste content occasionally attaching wrong data or silently losing text when the paste had aged out or placeholder numbers collided
- **[UNCOVERED]** - Fixed copy-on-select on Wayland sometimes not reaching the clipboard; the two selection writes no longer race
- **[UNCOVERED]** - Fixed the feedback survey's transcript share silently failing on long sessions; a failed share now shows an error instead of a success message
- **[UNCOVERED]** - Fixed Remote Control auto-start intermittently failing with "Remote credentials fetch failed" on a cold start with a stale login token
- **[UNCOVERED]** - Fixed Remote Control and SDK clients showing a blank "(no content)" message after `/clear` and other output-less commands
- **[UNCOVERED]** - Fixed a Remote Control session recreated after its server session expired uploading prior local conversation history into the new session
- **[UNCOVERED]** - Improved fullscreen mode to keep the full pre-compaction history in scrollback across repeated compactions, instead of only the most recent interval
- **[UNCOVERED]** - Improved Remote Control: attached web and mobile clients now see compaction progress and the post-compaction boundary instead of a silent pause; `/clear` resets now propagate to attached clients
- **[UNCOVERED]** - Improved Remote Control: connection failures now show a persistent failure indicator with details and a reconnect shortcut, instead of only an 8-second toast
- **[UNCOVERED]** - Removed the 200-subagent-per-session spawn cap; long-running sessions no longer refuse new agents (concurrency and depth limits still apply)
- **[UNCOVERED]** - Changed managed settings: the approval prompt no longer re-appears after re-login or org switching when the organization's settings are unchanged
- **[UNCOVERED]** - Changed the feedback-survey transcript share: with your consent it now also uploads the last request's model settings — the system prompt (which includes your `CLAUDE.md` instructions), tool definitions, and model parameters. Secrets are redacted as before, and these fields are dropped first if the share is too large
- **[UNCOVERED]** - Changed the Bash tool description to always note that command output is displayed to the model, not reliably to the user
- **[UNCOVERED]** - Changed recalled paste placeholder numbers to renumber when accepted into the input
- **[UNCOVERED]** - Changed Remote Control to archive the stale server session instead of leaving a dead one listed when a fresh session is minted after compaction or `/resume`
- **[UNCOVERED]** - [VSCode] Fixed the extension showing Remote Control as connected after the connection failed
- **[UNCOVERED]** - Fixed a session resume silently reconnecting Remote Control after the user turned it off (`--resume`, SDK hosts, and the VS Code extension)
- **[UNCOVERED]** - [VSCode] Fixed sessions not honoring `remoteControlAtStartup` when explicitly enabled

#### v2.1.223

- **[UNCOVERED]** - Added owner wildcard entries (`"owner/*"`) to the `strictKnownMarketplaces` and `blockedMarketplaces` managed settings for allowing or blocking all marketplace repos under a GitHub org
- **[UNCOVERED]** - Added a warning when workflow agents, forked skills, slash commands, or resumed background agents' requested subagent model is restricted and the parent model runs instead
- **[UNCOVERED]** - Added a `/teleport` hint in cloud sessions showing how to continue locally with `claude --teleport <session id>`
- **[UNCOVERED]** - Fixed a Bash permission bypass where a crafted command could hide parts of itself from permission checks
- **[UNCOVERED]** - Fixed permission prompts so commands padded with tabs or invisible Unicode can no longer hide part of the command from the approval dialog
- **[UNCOVERED]** - Fixed workflow scripts being able to use dynamic `import()` to run code outside the workflow sandbox
- **[UNCOVERED]** - Fixed a permission gap where an agent definition's `bypassPermissions` mode ignored the org bypass-permissions disable policy
- **[UNCOVERED]** - Fixed resuming a session after a mid-session `/cd` coming back empty
- **[UNCOVERED]** - Fixed gateway model discovery hiding Claude models registered under provider-prefixed IDs such as `vertex_ai/claude-*` or `bedrock/anthropic.claude-*`
- **[UNCOVERED]** - Fixed `modelOverrides` keys that aren't Anthropic model IDs being treated as the session's canonical model ID; unknown keys are now ignored as documented
- **[UNCOVERED]** - Fixed managed settings: server-delivered settings no longer disable the env block of a machine-local `managed-settings.json` or MDM profile; admin env now merges per key
- **[UNCOVERED]** - Fixed sandboxed commands failing to start on Linux when `sandbox.filesystem.denyWrite` covers the working directory
- **[UNCOVERED]** - Fixed forked background agents getting stuck "already resuming" for the rest of the session when rebuilding the fork's parent prompt failed during resume
- **[UNCOVERED]** - Fixed a resumed session failing every turn, or leaving the interactive app on an unresponsive error screen, when its history held a malformed diagnostics attachment
- **[UNCOVERED]** - Fixed a rare hang when parsing unusual `git push` output
- **[UNCOVERED]** - Changed `CLAUDE_CODE_DISABLE_1M_CONTEXT` to hold every Claude model with a native 1M window to 200K via auto-compaction, not just a fixed list; a startup warning now appears when auto-compaction isn't holding the session to 200K
- **[UNCOVERED]** - Changed auto-compact to keep sessions on unrecognized model IDs within the assumed context window instead of letting them grow past it; set `CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT=1` to restore the previous behavior
- **[UNCOVERED]** - Changed `/review` to be an alias of `/code-review`, which reviews the current diff or a PR (`/code-review <level> <pr#>`); use `/code-review ultra` for a deep cloud review
- **[UNCOVERED]** - Changed `/code-review` with no effort level to reuse the level you typed last; type a level like `/code-review high` to change it

#### v2.1.222

- **[covered]** - Removed ultraplan feature
  - Covered by: `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[UNCOVERED]** - Fixed worktree-isolated sessions and their subagents being able to run destructive git commands against the main checkout; isolation now applies to file edits and Bash in every session type
- **[UNCOVERED]** - Fixed PreToolUse auto-allow hooks bypassing tool restrictions in background agent tasks (summaries, compaction, renames)
- **[UNCOVERED]** - Fixed `/usage-credits` on Team and Enterprise showing "you've already sent a usage credit request" for members whose earlier request was dismissed, blocking them from sending a new one
- **[UNCOVERED]** - Fixed the startup connectivity check hanging and then failing behind an HTTPS proxy; it now uses the same proxy-aware transport as API requests and times out with a clear message
- **[UNCOVERED]** - Fixed "Connection closed mid-response" errors being reported on responses that had actually completed
- **[UNCOVERED]** - Fixed `/usage` overattributing usage to MCP servers: a server's share now reflects only the requests that actually consumed its tool results, instead of every turn after any call to it
- **[UNCOVERED]** - Fixed sessions not linking to pull requests created after the branch was pushed, including through the GitHub REST API
- **[UNCOVERED]** - Fixed org-restricted `model: opus`-style subagent and teammate family aliases dropping to the parent model instead of stepping down to the newest org-allowed model in the family
- **[UNCOVERED]** - Fixed stream idle timeout firing on custom `ANTHROPIC_BASE_URL` gateways despite server keep-alive pings arriving on the wire
- **[UNCOVERED]** - Fixed claude.ai connectors being falsely marked as needing authorization when the session token is invalid — they now show a `/login` hint instead
- **[UNCOVERED]** - Fixed tool errors not being displayed for tools no longer available locally, for example after an MCP server is removed
- **[UNCOVERED]** - Fixed `SendMessage` rejecting a long summary — it now truncates instead, so sends no longer fail on a character limit
- **[UNCOVERED]** - Fixed the spinner's effort label in a subagent's transcript view showing the session's effort level instead of the subagent's own `effort:` setting
- **[UNCOVERED]** - Fixed rare crashes when a file watcher hit a filesystem error or during file-watcher teardown
- **[UNCOVERED]** - Fixed screen readers re-reading the whole input line on every backspace in `--ax-screen-reader` mode — end-of-line deletions now echo just the deleted characters
- **[UNCOVERED]** - Fixed host model-selection keys not taking precedence over a stale on-disk `managed-settings.json` when `CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST` is set
- **[UNCOVERED]** - Improved auto mode safety: messages sent to other agent sessions via `SendMessage` are now evaluated by the permission classifier before dispatch
- **[UNCOVERED]** - Improved the refusal when Claude tries to invoke a skill with `disable-model-invocation`: Claude is now told to ask you to run the skill instead of replicating its workflow
- **[UNCOVERED]** - Improved the `/diff` view, the Remote Control workspace diff, and file-edit diffs in Claude Code on the web sessions to use raw git blob content, ignoring workspace-configured diff drivers and textconv
- **[UNCOVERED]** - Changed Remote Control auto-start so repo-local settings (`.claude/settings.json` or `.claude/settings.local.json`) can no longer turn it on (they can still turn it off); enable it at user scope via `/config`

#### v2.1.221

- **[covered]** - Improved tool search on Google Vertex AI: re-enabled for Claude 4.5-generation and newer models
  - Covered by: `cc-native/configuration/CC-model-provider-configuration.md`
- **[UNCOVERED]** - [VSCode] Added Focus view: a chat-menu toggle that hides tool activity behind an expandable per-turn summary with a live running-tool indicator, toggled with `Ctrl+Alt+F` or the "Claude Code: Toggle Focus view" command
- **[UNCOVERED]** - Added `mode: "mask"` for sandbox credential files on Linux and WSL — sandboxed commands read a sentinel copy (the whole file, or just the spans captured by an `extract` regex) while the sandbox proxy substitutes the real value on egress; on macOS file masking falls back to `deny`
- **[UNCOVERED]** - Added warnings to `claude plugin validate` when a marketplace or plugin name would be rejected by Claude Desktop's managed marketplace sync
- **[UNCOVERED]** - Added a `prompt-audit` subcommand to the `claude-api` skill for auditing prompts and tool descriptions for patterns written for older models
- **[UNCOVERED]** - Fixed a Bash tool permission-check bypass where zsh could execute hidden commands in `[[ ]]` regex conditionals; affected commands now prompt for permission
- **[UNCOVERED]** - Fixed PowerShell permission checks mishandling paths containing quote characters on Windows; such paths now prompt for approval
- **[UNCOVERED]** - Fixed the thinking toggle having no effect for the rest of a session that started with thinking off; disabling an MCP server mid-connect no longer silently reverts
- **[UNCOVERED]** - Fixed MCP servers from `--mcp-config` not being connected before the first turn in print mode (`-p`), which made the model emit tool calls as literal text
- **[UNCOVERED]** - Fixed @-mentioned files being silently dropped when pressing Esc to retract a prompt and resubmitting it
- **[UNCOVERED]** - Fixed a crash when preparing API requests for SDK MCP tools named after built-in object properties such as `constructor`
- **[UNCOVERED]** - Fixed WebSearch failing with a 400 error at effort `xhigh`/`max` when thinking is disabled
- **[UNCOVERED]** - Fixed sandboxed large uploads failing with TLS errors through the sandbox proxy
- **[UNCOVERED]** - Fixed Team and Enterprise spend-limit message incorrectly blaming the org's monthly limit instead of your individual spend limit
- **[UNCOVERED]** - Fixed Bedrock authentication with AWS SSO named profiles failing in desktop-managed sessions on Windows machines that set a stray `HOME` environment variable
- **[UNCOVERED]** - Fixed `CLAUDE_CODE_RESUME_INTERRUPTED_TURN=0` not disabling interrupted-turn auto-resume; falsy values are now honored
- **[UNCOVERED]** - Fixed a rare wake-from-sleep race where two Claude Code processes could both refresh the same MCP connector or WIF OAuth token at once, forcing re-authentication
- **[UNCOVERED]** - Fixed renaming a session from Claude Code Desktop or claude.ai not updating the CLI's session name; session names from every rename surface are now sanitized
- **[UNCOVERED]** - Fixed plugin- and org-delivered skills named after terminal-only built-ins (e.g. `/help`, `/feedback`) being un-invocable in non-interactive sessions
- **[UNCOVERED]** - Fixed the "Plugins changed" notification lingering after plugins were reloaded instead of clearing
- **[UNCOVERED]** - Fixed Vim mode: the yank register now survives dialogs, history search, and the transcript view instead of being silently emptied
- **[UNCOVERED]** - Fixed Vim mode: undoing back to an empty prompt now arms the "press ← again" confirm before returning to the agent view
- **[UNCOVERED]** - Improved auto mode: permission checks for parallel tool calls are now cache-efficient, and switching modes while a check is pending reliably prompts instead of applying the stale result
- **[UNCOVERED]** - Reduced prompt-cache costs for auto-mode permission checks by reusing the cached conversation prefix across decisions
- **[UNCOVERED]** - Improved Stats panel to count cache tokens in its token totals, with a breakdown by input, output, cache read, and cache write
- **[UNCOVERED]** - Improved `/ultrareview` error messages when a repo shares no history with its base: a checkout with no branches is now refused up front with advice to create one, and refusal hints no longer suggest `git fetch --unshallow` on clones that are already complete
- **[UNCOVERED]** - Improved Windows startup: process creation times are now read via a native kernel32 call instead of spawning PowerShell, so endpoint security tools that gate `powershell.exe` no longer prompt
- **[UNCOVERED]** - Changed background sessions to commit and push to preserve work, open a draft PR only when the task calls for one, follow your CLAUDE.md git instructions, and always end by reporting where the work lives
- **[UNCOVERED]** - Changed `/plugin install` to refresh a stale marketplace catalog and retry before reporting a plugin not found
- **[UNCOVERED]** - Changed plugins installed from `/plugin` to activate immediately when safe, instead of always requiring `/reload-plugins`
- **[UNCOVERED]** - Changed plugins to accept `"."` as a `skills` path, and the root-level `SKILL.md` validation error now suggests using the plugin root
- **[UNCOVERED]** - Changed `/status` to show the session kind: `interactive`, or a background job that is `attached` or `unattended`
- **[UNCOVERED]** - Changed emoji autocomplete to accept common alternate shortcodes like `:thumbsup:`, `:thumbsdown:`, and `:love:`
- **[UNCOVERED]** - Changed sessions forked with `/fork` to create a new worktree of their own instead of working in the original session's checkout
- **[UNCOVERED]** - Changed Claude in Chrome to close the browser tabs it opens once it no longer needs them
- **[UNCOVERED]** - Changed fast mode to report on the stream when usage credits run out mid-session, instead of failing silently
- **[UNCOVERED]** - Changed Monitor: a watch that exits without producing any output now says so instead of reporting "stream ended"
- **[UNCOVERED]** - Changed the Gateway `model` field validation: non-string values are rejected with a 400 instead of being forwarded
- **[UNCOVERED]** - Removed the repeated "Permission mode changed while the auto-mode classifier call was queued" notice from approval prompts

#### v2.1.220

- **[UNCOVERED]** - Bug fixes and reliability improvements

#### v2.1.219

- **[covered]** - Added Claude Opus 5 (`claude-opus-5`), now the default Opus model — 1M context, fast mode at $10/$50 per Mtok
  - Covered by: `cc-native/context-memory/CC-extended-context-analysis.md`
- **[UNCOVERED]** - Added `sandbox.network.strictAllowlist` setting to deny non-allowlisted hosts for sandboxed commands without prompting
- **[UNCOVERED]** - Added `DirectoryAdded` hook that fires after `/add-dir` or the SDK `register_repo_root` control request registers a new working directory mid-session
- **[UNCOVERED]** - Added `mcp_server_errors` to the headless stream-json init event, listing `--mcp-config` entries skipped by config validation; terminal runs print a startup warning
- **[UNCOVERED]** - Added the `workflowSizeGuideline` settings key so the advisory Dynamic workflow size guideline can be set from any settings file; the `/config` row is hidden while one does
- **[UNCOVERED]** - Added nested subagent forwarding in stream-json: subagents spawned at depth-2+ now appear when `--forward-subagent-text` is set, keyed by their spawning Agent `tool_use` id
- **[UNCOVERED]** - Fixed `claude -p` text output dropping the answer already produced when a turn dies on a mid-stream API error
- **[UNCOVERED]** - Added HTTP status and error text to `claude mcp list` and `/mcp` when a server fails to connect, and a warning for MCP config values with hidden leading or trailing whitespace
- **[UNCOVERED]** - Fixed the Fable model row showing "Requires usage credits" for plans that include it, when a stale cache had baked the label in
- **[UNCOVERED]** - Fixed the `/model` picker showing the merged Opus row as plain "Opus" instead of "Opus (1M context)"
- **[UNCOVERED]** - Fixed copy-on-select inside GNU screen printing base64 into the terminal instead of copying the selection
- **[UNCOVERED]** - Fixed Remote Control clients keeping a stale fast-mode status after a model switch, reconnect, or failed org check
- **[UNCOVERED]** - Fixed `CLAUDE_CODE_GIT_BASH_PATH` on Windows exiting or being used as bash when the path isn't a bash/sh binary; it's now ignored with a warning
- **[UNCOVERED]** - Fixed Vim mode: pressing ← on an empty prompt now returns to the agent view from NORMAL mode, not just INSERT
- **[UNCOVERED]** - Fixed screen-reader mode rewriting the entire input line on every keystroke instead of echoing only the typed character
- **[UNCOVERED]** - Improved the "Remote Control is only available via api.anthropic.com" error to name the specific setting that caused it
- **[UNCOVERED]** - Improved `claude --teleport` to show which repo your current checkout points at when it doesn't match the session's repo
- **[UNCOVERED]** - Changed dynamic workflows to default to a medium size guideline (aim for fewer than 15 agents); pick another size or unrestricted with Dynamic workflow size in `/config`
- **[UNCOVERED]** - Changed managed MCP allowlist/denylist `${VAR}` entries to resolve from the startup environment and managed-settings env instead of settings-file env
- **[UNCOVERED]** - Changed the `/model` picker to highlight only the newest model's name, so the highlight marks the new release rather than an arbitrary subset of the list
- **[UNCOVERED]** - Added the current default workflow size to the running-workflow status line, with a pointer to `/config` for changing it
- **[UNCOVERED]** - Removed Opus 4.7 from fast mode; `/fast` now applies to Opus 5 and Opus 4.8
- **[UNCOVERED]** - Updated the claude-api skill to default to Claude Opus 5, with a migration path from Opus 4.8
- **[UNCOVERED]** - Subagents can now spawn nested subagents up to depth 3 by default (was 1); set CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1 to disable nesting

#### v2.1.218

- **[UNCOVERED]** - Changed `/code-review` to run as a background subagent, so review work no longer fills your conversation and keeps stacked slash commands as its review target
- **[UNCOVERED]** - Added screen-reader announcements of deleted text for word and line deletions (`Option+Delete`, `Ctrl+W`, `Cmd+Backspace`, `Ctrl+U`, `Ctrl+K`) in `--ax-screen-reader` mode
- **[UNCOVERED]** - Fixed Windows paths with `\u`-prefixed segments (like `C:\Users\unicorn`) being corrupted into CJK characters in tool inputs, which made those files inaccessible
- **[UNCOVERED]** - Fixed the left arrow key discarding the conversation with no undo: presses right after editing now ask to confirm, and Esc in the agent view returns to the conversation it backgrounded
- **[UNCOVERED]** - Fixed multi-line paste collapsing into one line with `j` in place of newlines in terminals that encode pasted newlines as Ctrl+J
- **[UNCOVERED]** - Fixed `/context` reporting stale pre-compact token usage after compacting from the message picker
- **[UNCOVERED]** - Fixed `/ultrareview` failing on descriptive arguments like "review my auth changes" — they now run a review of your current branch with the text applied as a note to the findings
- **[UNCOVERED]** - Fixed `/code-review ultra` silently running a local review in non-interactive sessions — it now launches the cloud review
- **[UNCOVERED]** - Fixed gateway spend metering to price Bedrock application-inference-profile ARNs and other config-mapped upstream model IDs at the configured model's rates
- **[UNCOVERED]** - Fixed mojibake when a long IDE selection was truncated mid-emoji, and a case where a tool executor error could be silently dropped
- **[UNCOVERED]** - Fixed an engine teardown race that could start and abandon a phantom turn, and made input pushed after close consistently rejected
- **[UNCOVERED]** - Fixed spurious "[Request interrupted by user]" messages after interrupted tool calls, and an unpaired `tool_use` block left in the transcript when a tool aborted mid-response
- **[UNCOVERED]** - Fixed VoiceOver reading "new line" instead of echoing the typed space at the end of the input in `--ax-screen-reader` mode
- **[UNCOVERED]** - Fixed plugin and settings panels not moving the terminal cursor to the focused row, so screen readers and magnifiers can follow arrow-key navigation
- **[UNCOVERED]** - Fixed crashes (maximum call stack exceeded) when a deeply nested watched directory tree was deleted or moved, and when rendering deeply nested UI trees
- **[UNCOVERED]** - Fixed pull request events occasionally being lost when a session exited immediately after creating or linking a PR
- **[UNCOVERED]** - Fixed the Bedrock setup wizard failing profile verification for assume-role profiles in partitioned AWS regions and on proxy-only networks
- **[UNCOVERED]** - Fixed rare negative or incorrect turn duration measurements after a system clock adjustment by timing turns with a monotonic clock
- **[UNCOVERED]** - Fixed the "N MCP servers need authentication" startup notice over-counting claude.ai connectors that aren't connected in claude.ai
- **[UNCOVERED]** - Fixed prompt history entries being dropped or duplicated when history writes raced or failed
- **[UNCOVERED]** - Fixed a retry loop that re-sent identical doomed requests after a context-overflow error with a large thinking budget; `Ctrl+B` backgrounding now applies the same background-shell caps as other paths
- **[UNCOVERED]** - Fixed agent frontmatter hooks running from untrusted folders: hooks now require the agent file's own folder to have accepted workspace trust
- **[UNCOVERED]** - Fixed fork-session lineage being lost after compaction in headless and SDK sessions
- **[UNCOVERED]** - Fixed a resumed session failing every turn, or crashing on resume, when its history held a malformed delta attachment
- **[UNCOVERED]** - Improved `/ultrareview` error feedback so Claude can correct an invalid argument instead of retrying it unchanged
- **[UNCOVERED]** - Improved auto mode: the dangerous-rm, background-`&`, and suspicious-Windows-path checks no longer open permission dialogs; the auto-mode classifier adjudicates them instead
- **[UNCOVERED]** - Improved sandbox command restrictions for IDE interactions
- **[UNCOVERED]** - Improved trust dialogs to name the repository root the grant covers
- **[UNCOVERED]** - Changed `/deep-research` to start only when invoked manually; Claude no longer launches it on its own
- **[UNCOVERED]** - Changed plan mode with auto to no longer prompt for Bash commands the static analyzer can't prove read-only; the auto-mode classifier judges them instead
- **[UNCOVERED]** - Added an announcement when fast mode changes as a result of switching models via `/config model=<x>` or Remote Control
- **[UNCOVERED]** - Changed server-managed settings so benign feature and cost toggles no longer trigger the settings-approval prompt
- **[UNCOVERED]** - Changed agent markdown files to reject agent names containing `:`, which is reserved for plugin namespacing
- **[UNCOVERED]** - Changed skills with `context: fork` to run in the background by default; opt out per skill with `background: false`
- **[UNCOVERED]** - Added `yes`/`no`/`on`/`off`/`1`/`0` (case-insensitive) as accepted values for skill and plugin frontmatter booleans, alongside `true`/`false`
- **[UNCOVERED]** - Fixed remote sessions continuing to send heartbeats after their worker was replaced, which left long-lived desktop and IDE processes retrying a rejected request every few seconds forever

#### v2.1.217

- **[UNCOVERED]** - Added emoji shortcode autocomplete in the prompt input: type `:heart:` to insert ❤️, or `:hea` for suggestions — disable with the `emojiCompletionEnabled` setting
- **[UNCOVERED]** - Added warnings when transcript writes are failing (e.g. disk full) or when session saving is off due to an inherited environment variable, instead of losing transcripts silently
- **[UNCOVERED]** - Fixed a memory leak where truncated MCP tool outputs kept the full untruncated result in memory for the rest of the session
- **[UNCOVERED]** - Fixed Windows auto-update failures that could leave `claude.exe` missing; failed updates now restore the preserved executable automatically
- **[UNCOVERED]** - Fixed background session isolation not canonicalizing symlinked working directories, which could let sessions escape their workspace folder
- **[UNCOVERED]** - Fixed auto-compact never triggering for Claude Opus 4.8 on Bedrock and `/compact` failing once over the limit
- **[UNCOVERED]** - Fixed corporate mTLS, TLS-verify, OAuth scope, and proxy settings being ignored in Claude Desktop sessions
- **[UNCOVERED]** - Fixed screen reader mode's startup announcement being cut off by the first prompt render, and the thinking status row re-rendering every few seconds to update elapsed time and token counts
- **[UNCOVERED]** - Fixed managed settings that set `OTEL_EXPORTER_OTLP_ENDPOINT` not governing all signals — lower-scope signal-specific overrides no longer redirect telemetry away from the managed endpoint
- **[UNCOVERED]** - Fixed `--resume`/`--continue` and `/resume` failing with a TypeError when a transcript has a malformed attachment entry
- **[UNCOVERED]** - Fixed Remote Control sessions not showing a pending permission prompt or dialog to viewers that connected after it appeared
- **[UNCOVERED]** - Fixed background shells sometimes becoming impossible to stop after a session is sent to the background (`/background` or `←`) or when the session exits on a heavily loaded machine, most visible on Windows
- **[UNCOVERED]** - Fixed a `CLAUDE.md` or `SKILL.md` paths frontmatter value with many brace groups OOM-killing or stalling the CLI at startup — brace expansion is now budget-bounded
- **[UNCOVERED]** - Fixed the transcript preview sitting flush against the input area when attaching to a starting background session; it now leaves the same one-line gap as the live layout, so the transcript no longer shifts when the session takes over
- **[UNCOVERED]** - Improved footer PR badge links to be clickable hyperlinks even when terminal support can't be detected (e.g. over ssh/tmux); set `FORCE_HYPERLINK=0` to opt out
- **[UNCOVERED]** - Changed the login-expiry warning to appear 3 days before expiry instead of 5
- **[UNCOVERED]** - Capped the frontend-design plugin suggestion tip at 3 lifetime impressions instead of repeating indefinitely
- **[UNCOVERED]** - Added a cap on concurrently-running subagents (default 20, override with `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`) so one message can't fan out unbounded background agents
- **[UNCOVERED]** - Changed subagents to no longer spawn nested subagents by default; set `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` to allow deeper nesting
- **[UNCOVERED]** - Fixed `--max-budget-usd` not stopping background subagents: once the cap is reached, new spawns are denied and running background agents are halted

#### v2.1.216

- **[UNCOVERED]** - Added `sandbox.filesystem.disabled` setting to skip filesystem isolation while keeping network egress control
- **[UNCOVERED]** - Fixed a slowdown in long sessions where message normalization cost grew quadratically with the number of turns, causing multi-second stalls and slow resumes
- **[UNCOVERED]** - Fixed auto mode denying commands with "HTTP 401" classifier errors after the OAuth token expired or rotated mid-session
- **[UNCOVERED]** - Fixed AskUserQuestion telling Claude to continue even when your answer asked it to wait or explain first — free-text answers now get neutral wording
- **[UNCOVERED]** - Fixed Claude Code on the web re-asking the same question and dropping your answer after the session sat idle for a few minutes
- **[UNCOVERED]** - Fixed @-mentions silently attaching nothing after file-modifying hooks, vim dot-repeat of `c`-operators and paste, statusline running twice on resume, and resume-picker hangs on failure
- **[UNCOVERED]** - Fixed resumed background agent sessions reverting to the default agent: the agent's prompt and tool restrictions are now restored
- **[UNCOVERED]** - Fixed worktree-isolated subagents redirecting git into the shared checkout via `git -C`, `--git-dir`, or `GIT_DIR`/`GIT_WORK_TREE`
- **[UNCOVERED]** - Fixed worktree sessions landing in another project's leftover worktree when the working directory did not match the selected project
- **[UNCOVERED]** - Fixed background sessions whose worktree has no git repository being undeletable
- **[UNCOVERED]** - Fixed `claude daemon stop --any` potentially terminating an unrelated process via a stale legacy daemon lockfile
- **[UNCOVERED]** - Fixed Esc-Esc at an idle prompt not opening the rewind picker in long-running sessions with background tasks
- **[UNCOVERED]** - Fixed Bash command permission checking for compound statements with redirects inside `&&` lists or negations
- **[UNCOVERED]** - Fixed pressing Ctrl+X twice in the agent list failing to delete a session, and deleted sessions reappearing when their background worker had died
- **[UNCOVERED]** - Fixed background subagents getting cancelled when a high-priority message arrives during their startup window
- **[UNCOVERED]** - Fixed mouse and focus garbage in the terminal while a GUI editor from `/memory`, `/plan`, `/keybindings`, or Ctrl+G is open; `/memory` no longer waits for the editor to close
- **[UNCOVERED]** - Fixed Claude-in-Chrome 403-looping on reconnect when the session's OAuth token lacks a required scope
- **[UNCOVERED]** - Fixed workflow saves and scheduled-task writes following a symlink at `.claude`, which could redirect writes outside the project
- **[UNCOVERED]** - Fixed MCP re-authenticate revoking working credentials before the new sign-in succeeds, and the reconnect needs-auth message in background sessions pointing at an unusable command
- **[UNCOVERED]** - Fixed read-only commands on Windows accessing network paths without a permission prompt
- **[UNCOVERED]** - Fixed Bash command parsing of non-ASCII characters to match real shell word boundaries
- **[UNCOVERED]** - Fixed PowerShell tool permission validation of commands containing invisible Unicode characters
- **[UNCOVERED]** - Fixed dialogs in fullscreen mode stretching past the right-hand edge of their panel
- **[UNCOVERED]** - Fixed the `/config` settings list in fullscreen mode clipping its keyboard-hint footer
- **[UNCOVERED]** - Fixed the transcript-mode (Ctrl+O) footer hint wrapping on terminals narrower than 104 columns
- **[UNCOVERED]** - Fixed the Prometheus metrics endpoint (`OTEL_METRICS_EXPORTER=prometheus`) emitting invalid `# UNIT` lines
- **[UNCOVERED]** - Fixed skills and commands changed during a session not appearing in the slash menu until restart
- **[UNCOVERED]** - Fixed plugin skills with a `name` frontmatter field losing their plugin prefix in slash-command autocomplete
- **[UNCOVERED]** - Fixed telemetry misreporting permission denials: failed permission-prompt requests no longer count as user rejections, and user interrupts are now reported as user aborts instead of rejections
- **[UNCOVERED]** - Improved the `/fork` confirmation to one line with the new session's name, `claude attach` id, and a note when the copy shares your checkout
- **[UNCOVERED]** - Improved validation of `git` and `gh` command arguments in the PowerShell tool
- **[UNCOVERED]** - Improved the `/ultrareview` diff-too-large error to show configured limits, measured diff size, and largest contributing files
- **[UNCOVERED]** - Improved `/code-review ultra` empty-diff message to name the exact base ref and suggest passing an explicit base
- **[UNCOVERED]** - Improved the spend limit adjustment prompt to show the server's reason when a spend limit change is rejected
- **[UNCOVERED]** - `/context` now shows an explicit warning when the conversation exceeds the context window, and a failed `/compact` displays as an error
- **[UNCOVERED]** - `/rewind` no longer restores or deletes files through symlinks or hard links at tracked paths and reports how many paths it skipped
- **[UNCOVERED]** - Background sessions: `/mcp` and `/install-github-app` now park a "needs input" request in the agent view when no client is attached
- **[UNCOVERED]** - Updated the bundled dataviz skill: reordered the default chart palette and fixed guidance that suggested direct labels for four-series charts
- **[UNCOVERED]** - [VSCode] Fixed right-to-left text (Arabic, Hebrew, Persian) rendering in the wrong order when mixed with English or code
- **[UNCOVERED]** - Fixed cloud sessions dropping the in-flight message when the session's container restarts mid-turn — the interrupted turn now re-runs on resume instead of leaving the session unresponsive

---
_Generated by `.github/scripts/changelog-compare.py`_
## Native Sources Monitor Report

Sources checked: **3**

### anthropic-blog

- Source: Anthropic Blog — announcements and product updates
- Entries fetched: 11
- New uncovered: 4

| Entry | Section | Description |
|-------|---------|-------------|
| Sep 1, 2026AnnouncementsDeveloping Enterprise Frontier Safeg | Anthropic Blog | Sep 1, 2026AnnouncementsDeveloping Enterprise Frontier Safeguards with our custo |
| Aug 27, 2026Announcements Expanding our support for scientis | Anthropic Blog | Aug 27, 2026Announcements Expanding our support for scientists |
| Aug 25, 2026AnnouncementsFunding better evaluations of AI’s  | Anthropic Blog | Aug 25, 2026AnnouncementsFunding better evaluations of AI’s impact on wellbeing |
| Aug 4, 2026AnnouncementsMariano-Florentino (Tino) Cuéllar to | Anthropic Blog | Aug 4, 2026AnnouncementsMariano-Florentino (Tino) Cuéllar to join Anthropic as C |

### cc-issues-enhancement

- Source: CC GitHub Issues labeled 'enhancement'
- Entries fetched: 300
- New uncovered: 2

| Entry | Section | Description |
|-------|---------|-------------|
| Funktionswunsch: Eingebauter Sprachmodus / Vorlesefunktion f | GitHub Issues (enhancement) | ### Preflight Checklist - [x] I have searched [existing requests]( and this feat |
| [Feature Request] Claude Code lacks proactive assistance and | GitHub Issues (enhancement) | **Bug Description** i`m brasilian and i`ll write in portuguese, sorry about that |

### cc-discussions-feature-request

- Source: CC GitHub Discussions in feature-request category
- Entries fetched: 0
- New uncovered: 0

---
Total new uncovered entries: **6**

_Generated by `.github/scripts/native-sources-monitor.py`_
