# CC Changelog & Native Sources: New Uncovered Features Detected

## Changelog Monitor Report

Last scanned version: **2.1.310**
New versions detected: **4**

### New Versions Summary

| Version | Features | Covered | Uncovered |
|---------|----------|---------|-----------|
| 2.1.316 | 55 | 0 | 55 |
| 2.1.314 | 119 | 1 | 118 |
| 2.1.312 | 39 | 0 | 39 |
| 2.1.311 | 92 | 1 | 91 |

### Feature Coverage Details

#### v2.1.316 — released 2026-10-31

- **[UNCOVERED]** - Added `CLAUDE_CODE_DISABLE_ULTRATHINK`, which turns the `ultrathink` keyword off
- **[UNCOVERED]** - Added pooled group budgets to the Claude apps gateway: one monthly budget that a group's members share, on top of each member's own limit, set with `pooled_budget` on the spend limits admin API
- **[UNCOVERED]** - Added `CLAUDE_CODE_DISABLE_LOOPED_CROSS_CERT_DROP` to keep system cross-certificates that certify each other in a loop, for servers whose private CA needs one
- **[UNCOVERED]** - Added `CLAUDE_CODE_SUBAGENT_EFFORT` to set the effort level subagents run at when nothing else names one, instead of inheriting the session's
- **[UNCOVERED]** - Added `managed.policy_mode: layered` to the Claude apps gateway: every policy that matches a developer applies, each merged over the ones listed below it, not only the first
- **[UNCOVERED]** - Added `guardrail.input_tagging` on Claude apps gateway Bedrock upstreams, which wraps prompts in the input tags that an Amazon Bedrock guardrail's prompt attacks filter needs; `all_messages_and_system` also tags the system prompt
- **[UNCOVERED]** - Deprecated fast mode for Opus 4.8 as of October 30, 2026; it will be removed on November 30, 2026. After removal, fast mode requests on Opus 4.8 return an error and do not fall back to standard Opus 4.8. Migrate to Opus 5.5 to keep the speedup
- **[UNCOVERED]** - Fixed shell commands being left running on macOS and Linux when Claude Code exits by itself, for example when credentials are refused or a cloud session is archived
- **[UNCOVERED]** - Fixed bash aliases with line breaks in their value (except in Git Bash), and functions whose names start with a dash, being garbled or lost in the Bash tool's shell
- **[UNCOVERED]** - Fixed bash scripts started from the Bash tool stopping after their first command when `SHELLOPTS` is exported
- **[UNCOVERED]** - Fixed PowerShell hooks not blocking on exit code 2 when the command begins with a type cast, `param`, `using` or an attribute
- **[UNCOVERED]** - Fixed some network requests hanging when a compressed response was cut off or corrupted
- **[UNCOVERED]** - Fixed `sonnet`, `opus` and `haiku` on Vertex AI and Amazon Bedrock showing an error mid-session instead of switching to an older model when the newest is not yet available to the account or region
- **[UNCOVERED]** - Fixed the Claude apps gateway not checking every model a request names against `availableModels`, `deniedModels` and `models`; a request that names a blocked model now gets a 400 naming the field
- **[UNCOVERED]** - Fixed `claude auth login` refusing to run where managed settings require a Claude apps gateway; in a terminal it now shows the gateway sign-in
- **[UNCOVERED]** - Fixed `--restricted` sessions uploading files from outside the working directories when a Read allow rule covered them
- **[UNCOVERED]** - Fixed prompts containing invisible characters needing a second Enter to send; plain prompts now send cleaned on the first Enter, and commands still wait for review
- **[UNCOVERED]** - Fixed sub-agents that inherited a parent sub-agent's model moving to the main model when a background job or message woke them
- **[UNCOVERED]** - Fixed a managed `autoMode.allow` list without `"$defaults"` getting the built-in exceptions back from a host app's `--settings`, a first rule added in `/permissions`, or `/auto-mode-setup`
- **[UNCOVERED]** - Fixed cloud sessions and cloud scheduled tasks not being marked as failed when auto mode stopped a turn because the server returned no safety verdict
- **[UNCOVERED]** - Fixed `claude -p` text output sometimes not saying why auto mode stopped a turn when a background agent was still running
- **[UNCOVERED]** - Fixed `CLAUDE_CODE_AUTO_MODE_SERVER=1` being ignored in sessions started by a host application (such as Claude Desktop) behind a proxy or LLM gateway with experimental betas turned off
- **[UNCOVERED]** - Fixed plugin MCP `headersHelper` scripts receiving a corrupted `CLAUDE_PLUGIN_ROOT` and server URL when a credential-named environment variable was set to a switch value such as `1`
- **[UNCOVERED]** - Fixed the SDK `register_repo_root` control request not loading the CLAUDE.md of a directory outside the working directory (with `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`)
- **[UNCOVERED]** - Fixed the Artifact tool showing `?` for artifact database access rules at the `self` level, and not quoting those rules back when it refuses a republish that would drop them
- **[UNCOVERED]** - Fixed `/model <id>` not warning when the model isn't recognized by this version and auto-compact will assume a 200K context window
- **[UNCOVERED]** - Fixed the "hold space to speak" hint using up its three showings in one session, and showing an empty key when push-to-talk is unbound
- **[UNCOVERED]** - Fixed Grep and Glob never returning when the search process is killed at the timeout but does not exit, seen on Windows
- **[UNCOVERED]** - Fixed a rare case where resuming a conversation did not restore its plan, when `/clear` or `/resume` had been run while part of that conversation was still being saved
- **[UNCOVERED]** - Fixed first-run setup dropping words from the security notes and the terminal-setup explanation in narrow terminals
- **[UNCOVERED]** - Fixed the Enterprise survey card taking a typed 1 or 0 after a short pause; a typed answer now needs Enter
- **[UNCOVERED]** - Self-hosted runner: Fixed a message sent while Claude was working being answered after a Stop, once the session's process had been replaced
- **[UNCOVERED]** - Self-hosted runner: Fixed an MCP server's on/off switch sometimes being lost when a session moved to a new machine
- **[UNCOVERED]** - Windows: Fixed the Bash tool losing your aliases and functions in Git Bash when the rc file sets errexit and pipefail and only winpty aliases, or none, are defined
- **[UNCOVERED]** - Improved `/code-review` started from the Code tab in Claude Desktop or on the web: cloud and `claude remote-control` sessions now show the findings card, not a plain-text list
- **[UNCOVERED]** - Improved `/diff` on large repositories: each refresh usually runs one fewer full-repository git command, and refreshes are spaced out when git is slow
- **[UNCOVERED]** - Improved the messages shown when `/ultrareview`, a cloud session or a cloud agent finds no GitHub remote: they now say to create a repository at https://github.com/new, and `/ultrareview` no longer suggests a `gh` command that `gh` rejects
- **[UNCOVERED]** - Improved SSL certificate errors to name the likely causes, among them a server that leaves out an intermediate certificate, and the fix for each
- **[UNCOVERED]** - Changed auto mode so that an `autoMode.allow` list without `"$defaults"` no longer removes the built-in rule on scheduled-task prompts
- **[UNCOVERED]** - Changed server-managed settings for Team and Enterprise logins: settings fetched from Anthropic's API now apply without an approval prompt, and a stored copy that doesn't verify is refused
- **[UNCOVERED]** - [VSCode] Added sign-in to a Claude apps gateway from the chat panel, with no terminal needed
- **[UNCOVERED]** - [VSCode] Changed `ultrathink` to run its turn at `xhigh` effort and show in a rainbow in the chat box, as in the terminal
- **[UNCOVERED]** - [VSCode] Fixed the missing Effort slider, Ultracode switch and model name when the model setting has the `[1m]` tag, such as `opus[1m]`
- **[UNCOVERED]** - [VSCode] Fixed saved `/btw` side-question history being deleted too early while a settings file has errors
- **[UNCOVERED]** - [VSCode] Fixed a conversation coming back in Auto mode after a reload or restart when its plan was approved with "Yes, and manually approve edits"
- **[UNCOVERED]** - [Cloud sessions] Added a form card to cloud sessions, so you can fill in or decline a form an MCP server asks for instead of the request being canceled without you seeing it
- **[UNCOVERED]** - [Cloud sessions] Added a "Catching up…" line that shows while a cloud or Remote Control session you switch back to is still bringing its messages up to date
- **[UNCOVERED]** - [Cloud sessions] Changed network secrets so Enterprise members can add and delete them on their own cloud environments, instead of only viewing them
- **[UNCOVERED]** - [Cloud sessions] Improved the Changes pane for cloud sessions: the note about what the list leaves out is now a badge beside the branch name, not a row above the diff
- **[UNCOVERED]** - [Cloud sessions] Fixed file search in a cloud session's Files pane showing folders as ../.. paths after Claude changed directory; results now show their path from the project's root
- **[UNCOVERED]** - [Claude Tag] Fixed Claude refusing to edit or append to a canvas it made in a Slack channel, from that channel, once the canvas was also shared to another channel or a DM
- **[UNCOVERED]** - [Claude Tag] Fixed untagged replies going unanswered in a Slack Connect thread when both organizations have installed Claude and Slack delivered the reply to the other organization's app
- **[UNCOVERED]** - [Claude Tag] Fixed a cloud scheduled task's live status checklist in Slack staying half-done; a run can now edit the top-level messages it posted during that run
- **[UNCOVERED]** - [Claude Tag] Changed a Slack channel's Respond automatically switch to a "How Claude participates" choice on the channel's Configure page and in Claude Tag admin settings
- **[UNCOVERED]** - [Code Review] Added a findings-by-severity card to the Code Review analytics page, showing the period's total findings, a daily chart stacked by severity, and each severity's count

#### v2.1.314 — released 2026-10-30

- **[covered]** - Fixed `--resume`, and rewinding past a switch to another model after a refusal, moving a session on a model name Claude Code doesn't recognize to a different model
  - Covered by: `cc-native/sessions/CC-session-lifecycle-analysis.md`
- **[UNCOVERED]** - Added `permissions.blockWritesOutsideWorkingDirectories`: Write, Edit and NotebookEdit refuse paths outside the working directories in every permission mode
- **[UNCOVERED]** - Added an optional `groups` list to Claude apps gateway upstreams: only developers in the listed IdP groups are sent to that upstream, on failover too
- **[UNCOVERED]** - Added `guardrail_trace` to Claude apps gateway Bedrock upstreams, to log which Amazon Bedrock guardrail filter fired on a request, without the matched text
- **[UNCOVERED]** - Added idle compaction to VS Code and Claude Desktop's Code tab: a 200K+ token conversation left idle is summarized, and the summary is used on your next message if the prompt cache has expired
- **[UNCOVERED]** - Fixed sessions failing turn after turn with "Invalid effort level" when an organization's admin caps a model's effort: Claude Code now lowers the effort, retries, and says which level it uses
- **[UNCOVERED]** - Fixed `claude -p` exiting with code 0 and no output when startup failed; it now prints the error and exits 1
- **[UNCOVERED]** - Fixed Bedrock sessions with many images failing every turn and `/compact` with "400 Input is too long." instead of removing older images and compacting
- **[UNCOVERED]** - Fixed Microsoft Foundry sessions failing when the resource has no deployment for the default Sonnet, Opus or Haiku model: Claude Code now falls back to an older model of that family
- **[UNCOVERED]** - Fixed repeated refused requests behind a gateway that doesn't accept tool search's `tool_reference` blocks: the request is sent again once without tool search, and the session remembers
- **[UNCOVERED]** - Fixed TLS connections failing with `UNABLE_TO_GET_ISSUER_CERT` when the system certificate store holds a renewed root certificate that is cross-signed with its predecessor
- **[UNCOVERED]** - Fixed MCP servers that also work without sign-in showing "needs authentication" after their stored sign-in stopped working; they are now used signed out
- **[UNCOVERED]** - Fixed `claude mcp logout` reporting success when the MCP sign-in was not removed, for example while the macOS keychain is locked over SSH
- **[UNCOVERED]** - Fixed extra sign-in renewals when several sessions share an Anthropic profile login and the credentials lock is busy
- **[UNCOVERED]** - Fixed `claude ultrareview` and `claude remote-control` asking the workspace trust question in a CI job that has a terminal; with `CI` set they now refuse an untrusted folder at once
- **[UNCOVERED]** - Fixed an administrator's TLS trust settings in managed settings not being applied in Claude Desktop sessions
- **[UNCOVERED]** - Fixed model switching being refused on machines with managed plugin settings when one of your own `--plugin-dir` or `--plugin-url` plugins had a broken manifest or failed to download
- **[UNCOVERED]** - Fixed the Bedrock and Vertex model upgrade offer coming back at every start when managed settings pin the model
- **[UNCOVERED]** - Fixed `forceRemoteSettingsRefresh` set only in remote managed settings no longer applying once the stored copy had expired, which let sessions start without policy when the server could not be reached
- **[UNCOVERED]** - Fixed "Continue automatically at usage limit" continuing more than three times without a prompt from you when a task restarted itself between waits (a /goal check-in, a background or scheduled task)
- **[UNCOVERED]** - Fixed background and cloud sessions started with Ultracode turning it back on at their next start after it had been switched off
- **[UNCOVERED]** - Fixed the last broken reply and its retry prompts staying in the conversation after Claude gave up on a tool call that could not be parsed
- **[UNCOVERED]** - Fixed a PreCompact hook with very large output making compaction fail or repeat; each hook's output is now cut at 10,000 characters
- **[UNCOVERED]** - Fixed background diff refreshes briefly taking the repository's index lock, which could make a git command run at the same moment fail with "Unable to create '.git/index.lock': File exists"
- **[UNCOVERED]** - Fixed markdown tables jumping between grid and stacked layouts on half-typed rows while streaming, and long tables falling back to raw pipes
- **[UNCOVERED]** - Fixed the /resume picker showing the text of CLAUDE.md or CLAUDE.local.md as a session's title when the session only ran slash commands
- **[UNCOVERED]** - Fixed `/btw` answering from the main conversation when asked from a subagent's open transcript
- **[UNCOVERED]** - Fixed pasting an image over SSH to a Linux machine doing nothing silently; the prompt now says to copy the file over and paste its path
- **[UNCOVERED]** - Fixed `claude remote-control` sessions that failed to start when the session service was slow for a moment: the worker's registration is now retried with growing waits
- **[UNCOVERED]** - Fixed model switches over Remote Control that take over 8 seconds getting a "still pending" error instead of the final result
- **[UNCOVERED]** - Fixed the `sandbox.excludedCommands` setting description saying listed commands always run outside the sandbox; it now says every command in a call must match an entry
- **[UNCOVERED]** - Fixed shell and MCP calls that auto mode, a deny rule or a PreToolUse hook blocked, or that otherwise did not run, reading as if they ran in a collapsed tool group
- **[UNCOVERED]** - Fixed sandbox protections not applying to a worktree entered by `claude -p --resume` or `--continue`
- **[UNCOVERED]** - Fixed hooks matching Bash not running on shell commands started by the Monitor tool; such hooks can block or ask, but not approve or rewrite those commands
- **[UNCOVERED]** - Fixed a settings file excluded with `--setting-sources` still supplying some settings, such as auto mode rules and saved permission consents
- **[UNCOVERED]** - Fixed auto mode reporting a call as blocked, and listing it in `/permissions`, when its safety check gave no verdict
- **[UNCOVERED]** - Fixed a Claude apps gateway Vertex upstream hanging for minutes when a Google token endpoint accepts the connection and never answers
- **[UNCOVERED]** - Fixed the Claude apps gateway's start-up warning for a deprecated Claude Desktop key that it still serves as written saying "stops being accepted" after the key's end date
- **[UNCOVERED]** - Fixed `/upgrade` opening the browser and starting a new login for plans billed through the App Store or Google Play; it now says where to change the plan
- **[UNCOVERED]** - Fixed requests failing when a gateway or cloud provider refuses one of Claude Code's beta headers by name: the request is sent again without it
- **[UNCOVERED]** - Fixed model IDs spelled with a dot behind an LLM gateway, such as `claude-opus-4.8`, being treated as an older model with the wrong context window, output limit, effort, thinking mode and cost
- **[UNCOVERED]** - Fixed Remote Control clients showing a stray "Compacted (ctrl+o to see full summary)" row after /compact
- **[UNCOVERED]** - Fixed the cloud sessions tip and the Remote Control idle notice showing when an organization's policy turns those features off
- **[UNCOVERED]** - Fixed a resumed claude.ai cloud session making a model call nobody asked for when the previous worker stopped just after receiving a new chat's files
- **[UNCOVERED]** - Fixed WebFetch in Cowork cloud sessions silently dropping a PDF's text past 100,000 characters; it now says how much was unread and where to read on
- **[UNCOVERED]** - Fixed Claude being told only that a command was declined after you stopped it with Esc or Stop in a cloud session or the IDE; it now also hears that the command may have run
- **[UNCOVERED]** - Fixed blank lines at the top of a code block disappearing when the code block opens a quote
- **[UNCOVERED]** - Fixed a blank line appearing above some `⎿` rows in the transcript view (Ctrl+O)
- **[UNCOVERED]** - Fixed vim mode `dw`, `dW`, `yw` and `yW` carrying on past the end of the line, and made `w` and `W` stop on empty lines
- **[UNCOVERED]** - Fixed x and Enter in the agent panel sometimes acting on the wrong agent when another agent started or finished
- **[UNCOVERED]** - Fixed pasted text and dragged-in files being lost in Claude's question dialog unless the "Other" row had focus
- **[UNCOVERED]** - Fixed pasted text being lost when a row in the prompt footer was selected
- **[UNCOVERED]** - Fixed vim mode `p` over a character selection ignoring whether the yanked text was whole lines
- **[UNCOVERED]** - Fixed vim mode `aw` and `iw` taking the line break at the end of a line
- **[UNCOVERED]** - Fixed ↓ selecting footer items hidden by the ? help menu, the command list or a paste hint
- **[UNCOVERED]** - Fixed Esc on a command's panel, such as `/btw`, also interrupting the subagent whose transcript is open
- **[UNCOVERED]** - Fixed the welcome header in fullscreen mode showing the session's model while viewing a subagent or teammate that runs on a different model
- **[UNCOVERED]** - Fixed the fullscreen transcript being left mid-conversation after "Restore conversation" in the rewind menu while scrolled up
- **[UNCOVERED]** - Fixed a rare case where a deleted session could reappear in the resume list as an almost empty entry
- **[UNCOVERED]** - Fixed prompts containing tags such as `<bash-stdout>` or `<local-command-stdout>` not being acknowledged to a local stream-json host
- **[UNCOVERED]** - Fixed sessions staying untitled when the first prompt failed (for example on a usage limit) and the conversation continued afterward
- **[UNCOVERED]** - Fixed the skill file watcher checking every removed skill kept in `~/.claude/skills/.trash`, which added file system load that grew with each removal
- **[UNCOVERED]** - Fixed the session name from /rename disappearing while Claude asks for permission or a plan decision, so side-by-side sessions stay identifiable
- **[UNCOVERED]** - Fixed background sessions that fail to start being reported as a deleted daemon binary when the binary is still on disk
- **[UNCOVERED]** - Fixed the tip and idle reminder about push notifications appearing when the push settings in `/config` are hidden or your organization has turned off Remote Control
- **[UNCOVERED]** - Fixed `~/.claude/skills/.trash` and `~/.claude/plugins/.trash` growing without limit: each now holds about 1024 entries, whatever `cleanupPeriodDays` says
- **[UNCOVERED]** - Fixed the Bash edit diff listing a whole file as changed when a CRLF file under git's line-ending conversion was re-saved unchanged or had one line edited
- **[UNCOVERED]** - Self-hosted runner: Fixed an idle session moving to another runner instead of pausing when the runner's request to pause it lost its connection before Anthropic answered
- **[UNCOVERED]** - Improved memory use in long headless and SDK turns that run many subagents: the parent session no longer keeps each subagent's tool results until the turn ends
- **[UNCOVERED]** - Improved prompt history: Ctrl+R now matches text inside collapsed `[Pasted text]` pills
- **[UNCOVERED]** - Improved the `/design-sync` upload prompt to show the folder, the project and the files it will upload or delete
- **[UNCOVERED]** - Improved `/permissions` review tab, now called Recently blocked: the footer says what Esc will do with marked rows
- **[UNCOVERED]** - Improved auto mode's blocked calls: messages name the command, say Claude may retry and auto mode checks again, and point to `/permissions` to review
- **[UNCOVERED]** - Improved permission prompts: a long reason takes fewer rows, so it pushes the command being approved off the screen on fewer terminals
- **[UNCOVERED]** - Improved the cloud session error shown while a request refused for your claude.ai login is still being retried: it now also suggests `claude auth login`
- **[UNCOVERED]** - Improved the behavior of stored claude.ai, Team, and Enterprise logins when MDM and remote settings differ on base URL or `apiKeyHelper`
- **[UNCOVERED]** - Improved `/config` in agent view to say how to stop agent view opening by default
- **[UNCOVERED]** - Improved session auto-titles: a session that starts with a skill or a prompt-based command such as `/security-review` now gets a title from it instead of staying untitled
- **[UNCOVERED]** - Improved `--resume` speed and memory use on damaged transcripts
- **[UNCOVERED]** - Improved `/context` speed in sessions with ten thousand or more MCP tools
- **[UNCOVERED]** - Self-hosted runner: Improved the error shown when a session's branch isn't on the git remote: it now covers a never-pushed branch, says how to fix each case, and no longer suggests retrying
- **[UNCOVERED]** - Updated the `/claude-api` skill: its Datadog setup for API tracing now sends the `dd-llmobs-enabled: true` header, as the Console does, and its `ant` install instructions drop the outdated macOS `xattr` step
- **[UNCOVERED]** - Updated the bundled dataviz skill to advise printing y-axis tick labels in full under 10,000, and horizontal ones in full under a million where they fit
- **[UNCOVERED]** - Updated the bundled dataviz skill to answer donut and pie chart requests with ranked bars or a segmented bar that prints its values
- **[UNCOVERED]** - Changed Claude's file tools to ask before editing the local copy of your organization's server-managed settings, as they do for your settings files
- **[UNCOVERED]** - Changed `/ultrareview` to check workspace trust before it runs git, as `claude ultrareview` does
- **[UNCOVERED]** - Changed the Bash tool's shell to clear any inherited `which` alias or function and to stop passing exported `which`/`unsetenv` functions to commands, so `which` is the system command or zsh builtin
- **[UNCOVERED]** - Changed `/permissions` Recently blocked to refuse approving a call you can't read in full, including one the terminal is too short to show
- **[UNCOVERED]** - Changed auto mode in Cowork cloud sessions: a hook's allow of an MCP tool call now counts as no answer, so the classifier or a permission prompt decides
- **[UNCOVERED]** - Changed hook `if` conditions such as `Monitor(tail *)` to match the Monitor tool's shell commands as `Bash(tail *)` matches Bash's
- **[UNCOVERED]** - Changed the `claude-api` skill to ask to read a Managed Agents workflow run's workflow before changing the agent to improve that run
- **[UNCOVERED]** - Changed flagged requests to retry on another model, not end in a refusal, when `ANTHROPIC_DEFAULT_OPUS_MODEL`, `availableModels` or `deniedModels` leaves only an older Opus model, or none
- **[UNCOVERED]** - Changed idle compaction to also run for subscribers with telemetry turned off, and on Bedrock, Vertex, Foundry and LLM gateways once the one-hour prompt cache is on
- **[UNCOVERED]** - Changed `FORCE_HYPERLINK=false` (also `no` and `off`) to turn hyperlinks off instead of on
- **[UNCOVERED]** - macOS: Changed `git grep` in most commands that Claude runs to use the C locale, to avoid a reported memory leak in macOS's regex library on files that aren't valid UTF-8
- **[UNCOVERED]** - [VSCode] Fixed "Clear authentication" for MCP servers reporting success when the saved sign-in could not be removed
- **[UNCOVERED]** - [VSCode] Fixed missing spinner and Stop button while a queued message's hooks run
- **[UNCOVERED]** - [VSCode] Fixed session group changes that cannot be saved, such as a delete, failing silently; an error notification now appears
- **[UNCOVERED]** - [VSCode] Fixed Cmd+F / Ctrl+F not opening the find widget in the plan preview tab
- **[UNCOVERED]** - [VSCode] Fixed the voice dictation shortcut (Ctrl+D) doing nothing under non-Latin keyboard layouts such as Russian, Greek or Hebrew
- **[UNCOVERED]** - [VSCode] Fixed missed one-time saved scheduled tasks being deleted without asking when the extension opened without a chat
- **[UNCOVERED]** - [VSCode] Changed `CLAUDE_CODE_DISABLE_CFC_PROMPT` to also stop the extension adding the Claude in Chrome instructions to a session's messages; the browser tools stay available
- **[UNCOVERED]** - [Cloud sessions] Added an Include completed button to the Scheduled tasks page when finished one-off tasks are the only ones hidden, so you can show them without opening the Sort menu
- **[UNCOVERED]** - [Cloud sessions] Fixed recently used self-hosted environments never appearing among the recent environments on the new session card
- **[UNCOVERED]** - [Cloud sessions] Fixed cloud sessions reporting uncommitted changes every turn after Claude moved a branch to a commit it had pushed from another worktree
- **[UNCOVERED]** - [Cloud sessions] Fixed the self-hosted environment details dialog in admin settings squeezing its content out of view in very short windows or at high zoom; the dialog now scrolls
- **[UNCOVERED]** - [Cloud sessions] Fixed the permission mode picker staying on Auto after a running cloud or Remote Control session refused the switch; it now shows the mode in use and tells you
- **[UNCOVERED]** - [Cloud sessions] Improved scheduled tasks: runs in Anthropic's cloud now load the plugins enabled on your claude.ai account
- **[UNCOVERED]** - [Cloud sessions] Improved Test connection for GitHub Enterprise in admin settings to also connect the way cloud sessions do, and to warn you when that second test fails
- **[UNCOVERED]** - [Cloud sessions] Improved cloud session transcripts: a rename row now names the new title, and repository and environment lists show as a table instead of one line of JSON
- **[UNCOVERED]** - [Cloud sessions] Changed cloud sessions from the web, desktop and mobile apps to start even when a setup script exits with an error, instead of failing to start
- **[UNCOVERED]** - [Remote Control] Fixed the permission mode button in Remote Control sessions showing the wrong mode until you typed; while your computer is online it now shows the real mode on open
- **[UNCOVERED]** - [Claude Tag] Added a dismissible link to the Claude Tag API docs on the Bundles and Channels tabs in admin settings, for Enterprise organizations with Slack connected
- **[UNCOVERED]** - [Claude Tag] Fixed `@Claude !restart` giving up after one failed workspace check in channels shared across Enterprise Grid workspaces; it now retries, then asks you to run it again
- **[UNCOVERED]** - [Claude Tag] Fixed a second confirmation DM and channel note when you connect your Claude account from Slack twice from the same link within a few minutes
- **[UNCOVERED]** - [Claude Tag] Fixed follow-up messages in Slack showing no sign of progress while Claude's session waits for a self-hosted runner; Claude now posts a wait notice in the thread
- **[UNCOVERED]** - [Claude Tag] Fixed Claude sometimes not answering a tag in its own thread in Slack Connect channels where both organizations have installed Claude
- **[UNCOVERED]** - [Claude Tag] Fixed Retry on plugin and skill pages in Claude Tag admin settings discarding unsaved access changes after a failed load; your edits now stay in place
- **[UNCOVERED]** - [Claude Tag] Fixed the repositories control in Claude Tag admin settings showing the same action twice; its menu now lists only what the button doesn't already do

#### v2.1.312 — released 2026-10-27

- **[UNCOVERED]** - Added `oidc.user_id_claim` to the Claude apps gateway, to identify people by an id_token claim other than `sub`, such as Microsoft Entra ID's `oid`
- **[UNCOVERED]** - Added click to send: in fullscreen, clicking the "to send now" hint under a queued message sends it right away, as its key does
- **[UNCOVERED]** - Fixed managed settings and organization policy not being fetched for the rest of the session after signing in from the VS Code extension
- **[UNCOVERED]** - Fixed Claude overwriting a very large CLAUDE.md, rules file or @-included file in a subdirectory after seeing only its start; Write now asks Claude to read it all or edit in place
- **[UNCOVERED]** - Fixed per-directory and `paths:` skills not being found after a Bash `cd` deeper into a git repository
- **[UNCOVERED]** - Fixed a rare case where the first reply after resuming a session in the terminal could be missing the next time the session was resumed
- **[UNCOVERED]** - Fixed a command with an invalid name stopping all commands from loading, which could leave `claude -p` with no output
- **[UNCOVERED]** - Fixed the Read tool sometimes failing on PDF pages with "pdftoppm failed: Could not write image" when the clean-up of old session files ran at the same time
- **[UNCOVERED]** - Fixed the spinner, OpenTelemetry `effort` values and transcripts naming a newly picked effort level during a task before the model applied it; they now show the level in force
- **[UNCOVERED]** - Fixed the `/model` and `/effort` cache warning saying the re-read waits for your next message; a change made while Claude is working can trigger it sooner
- **[UNCOVERED]** - Fixed some sessions showing as waiting on you when the last message only mentioned items waiting on you mid-sentence
- **[UNCOVERED]** - Fixed agent view restoring input text on the next launch after it was cleared with Ctrl+C just before exiting
- **[UNCOVERED]** - Fixed agent view reopening in shell mode after exiting with Ctrl+D from an empty `!` input
- **[UNCOVERED]** - Fixed vim mode `d`, `c` and `y` with a `gj` or `gk` count larger than the lines left deleting or copying text; like Vim, they now only move the cursor
- **[UNCOVERED]** - Fixed `/verify` showing a long description meant for Claude in `/help` and the `/` command menu instead of a short one
- **[UNCOVERED]** - Improved the prompt's effort indicator: a change made mid-task now says it may wait for your next message, and the note clears when it no longer applies
- **[UNCOVERED]** - Improved WebFetch errors in cloud sessions: a host that does not resolve is now explained as possibly outside the allowed network domains, so Claude names the host to allow
- **[UNCOVERED]** - Changed Bedrock, Vertex, Foundry and Mantle to use the shorter system prompt for model names Claude Code doesn't recognize, such as custom deployment names and inference profile ARNs, even when they front Sonnet or Haiku; set `CLAUDE_CODE_SIMPLE_SYSTEM_PROMPT=0` to keep the full prompt
- **[UNCOVERED]** - Changed automatic model switches after a flagged message to also cover model names Claude Code doesn't recognize, such as custom deployment names; set `CLAUDE_CODE_DISABLE_REFUSAL_FALLBACK=1` to turn them off
- **[UNCOVERED]** - Changed usage limit messages to call the 5-hour window the "5-hour limit" instead of the "session limit"
- **[UNCOVERED]** - Changed cloud sessions started from the CLI to get their names and branch names from the server
- **[UNCOVERED]** - Changed prompt and agent hooks to run at most 24 at a time per session, sub-agents included, plus at most 12 that have waited longer than their event's timeout; a `timeout` under 1 second now counts as 1 second
- **[UNCOVERED]** - Changed a subagent's `autoCompactWindow` to lower the window set by `CLAUDE_CODE_AUTO_COMPACT_WINDOW`, where it had no effect before; it still never raises that window
- **[UNCOVERED]** - Changed OpenTelemetry `mcp_server.name` to report the real name of fixed-URL remote MCP servers declared by plugins from the official Anthropic marketplace, instead of `custom`
- **[UNCOVERED]** - Changed Claude Code to stop sending the `claude_code.safety_event` OpenTelemetry event
- **[UNCOVERED]** - [VSCode] Fixed sessions ending on a bare exit code when your organization's settings couldn't be loaded or were refused at startup; the tab now says why and offers Retry or Sign in again
- **[UNCOVERED]** - [VSCode] Changed usage limit resets to show a clock time ("Resets at 3:10 PM") and to say "5-hour limit"
- **[UNCOVERED]** - [Cloud sessions] Added an effort level to the model picker when you create or edit a routine that runs in the cloud
- **[UNCOVERED]** - [Cloud sessions] Added a Bash editor with colors, line numbers and a Copy button to the setup script box in cloud environment settings
- **[UNCOVERED]** - [Cloud sessions] Improved the step shown when Claude adds a repository to a cloud session: opening it now shows a short table of what happened instead of raw JSON
- **[UNCOVERED]** - [Cloud sessions] Fixed resending an unchanged message after a failed send in a cloud session sometimes running it twice
- **[UNCOVERED]** - [Cloud sessions] Fixed a failed cloud environment creation showing its error only as a toast outside the open dialog; it now appears inside the dialog
- **[UNCOVERED]** - [Cloud sessions] Fixed Edit in a routine's menu on the Routines page going to the routine's page without opening its edit dialog
- **[UNCOVERED]** - [Remote Control] Fixed an unarchived Remote Control session showing as working until a computer reconnected; it now shows as idle
- **[UNCOVERED]** - [Claude Tag] Improved Claude Tag's retry notice in Slack to name the model in use, or say rate limits were hit, instead of a generic API error
- **[UNCOVERED]** - [Claude Tag] Fixed a Claude Tag channel's on/off switch and agent settings falling back to workspace defaults when an older private Slack channel goes public and gets a new ID
- **[UNCOVERED]** - [Claude Tag] Fixed Claude in Slack not replying in channels whose environment has network access set to None
- **[UNCOVERED]** - [Claude Tag] Fixed Claude in Slack sometimes posting a file in the wrong thread when it was answering in another thread of the same channel
- **[UNCOVERED]** - [Code Review] Fixed Code Review reviewing an outdated commit, or none at all, when GitHub delivered a push event late; it now reviews the pull request's current commit

#### v2.1.311 — released 2026-10-26

- **[covered]** - Fixed a `--plugin-dir` folder of plugins loading as one plugin when an empty `.mcp.json` was at its top
  - Covered by: `cc-native/plugins-ecosystem/CC-plugin-packaging-research.md`
- **[UNCOVERED]** - Added `--hold-idle-file` and `--max-hold-min` to `self-hosted-runner`, to keep an idle session while your host reports processes it left running
- **[UNCOVERED]** - Added a tip for the Explanatory output style, shown when you ask Claude for explanations
- **[UNCOVERED]** - Fixed long freezes at startup and after reading or editing files when a CLAUDE.md file holds a very long list item
- **[UNCOVERED]** - Fixed interrupting Claude not taking effect until a timeout while an MCP server had not answered a resource read or a skill was still downloading
- **[UNCOVERED]** - Fixed standard-context sessions stopping with "Usage credits required for 1M context" when a request ran over 200K tokens; Claude Code now compacts the conversation and continues
- **[UNCOVERED]** - Fixed Write and Edit stalling for up to 5 seconds after they ran, and reporting 0 lines changed, when changing thousands of lines in a file
- **[UNCOVERED]** - Fixed subagents being unable to use MCP tools from servers that finish connecting after the subagent starts
- **[UNCOVERED]** - Fixed Claude seeing stale MEMORY.md and CLAUDE.md content right after automatic compaction when those files were edited earlier in the session
- **[UNCOVERED]** - Fixed `claude -p` and SDK sessions saving transcript messages out of order or keeping messages that were taken back
- **[UNCOVERED]** - Fixed `SubagentStop` hooks running about twice a minute for each running subagent instead of once when it finishes
- **[UNCOVERED]** - Fixed the @ file picker ignoring `.ignore`/`.rgignore` negation rules that re-include git-ignored files
- **[UNCOVERED]** - Fixed a subagent's isolated worktree being removed while a background subagent it started was still working in it
- **[UNCOVERED]** - Fixed background agents in auto mode that wait on their own shells starting a new main conversation turn on every wake
- **[UNCOVERED]** - Fixed the Bash tool description claiming the working directory always persists between calls
- **[UNCOVERED]** - Fixed the environment block naming a shell commands don't run in, such as fish when the Bash tool uses zsh
- **[UNCOVERED]** - Fixed `claude mcp add`, `claude mcp remove` and `/mcp` naming the current folder instead of the project entry in `~/.claude.json` that holds a local-scope server when run below a repository root
- **[UNCOVERED]** - Fixed `claude mcp list` and `claude mcp get` showing the error code twice on failed-connection lines (for example `ENOENT: ENOENT: …`)
- **[UNCOVERED]** - Fixed Remote Control sessions staying on "Connecting" for about two minutes when a network proxy blocks a startup request
- **[UNCOVERED]** - Fixed messages that Claude sends to a cloud or Remote Control session appearing as your own message in the Claude mobile apps
- **[UNCOVERED]** - Fixed Claude not being told the cause when a file attached to a message sent over Remote Control or to a cloud session could not be saved because the disk was full, or that a message's attachments past the first 20 were left out
- **[UNCOVERED]** - Fixed WebFetch and WebSearch hanging on a stalled response in Cowork cloud sessions; an unfinished request now fails after 300 seconds
- **[UNCOVERED]** - Fixed a background session that crashed between turns not being restarted while it was attached, pinned, or had a scheduled task or wake-up set
- **[UNCOVERED]** - Fixed the "background service did not respond" error suggesting the disabled `claude daemon restart`; it now suggests `claude daemon stop --any` and says it ends background sessions
- **[UNCOVERED]** - Fixed `claude respawn <id>` starting the background service before reporting that no background session matches the id
- **[UNCOVERED]** - Fixed `/effort` not warning about a prompt cache miss in plan mode when the plan model differs from the session model
- **[UNCOVERED]** - Fixed `/ide` saying the VS Code extension was installed before the install finished or when it failed
- **[UNCOVERED]** - Fixed the Write tool's file preview skipping rows and miscounting hidden lines when a line is wider than the terminal
- **[UNCOVERED]** - Fixed ↑ in an agent's chat tab recalling a message that was still waiting to be delivered, so resending it sent a second copy
- **[UNCOVERED]** - Fixed Cowork cloud sessions losing their connectors and most tools after a restart when a plugin or your settings named an `agent`; Cowork cloud sessions now ignore that setting
- **[UNCOVERED]** - Fixed agent teams sessions showing an empty task list when coming back with `--resume`, `--continue`, `/resume` or `--session-id`, including after `/clear` or a crash, and `/branch` writing to the original session's list
- **[UNCOVERED]** - Fixed pasting text that mentions an image file, such as `! open /tmp/shot.png` or `/review look at /tmp/shot.png`, attaching the image and dropping its path from the prompt
- **[UNCOVERED]** - Fixed the feedback draft card showing its 1/2/0 and Esc shortcuts while the prompt has text, when those keys act on the prompt instead of the card
- **[UNCOVERED]** - Fixed a lone backslash in quotes or brackets, like `"\"` or `(\)`, disappearing from Claude's responses
- **[UNCOVERED]** - Fixed agent teammates compacting their history when `DISABLE_COMPACT` is set
- **[UNCOVERED]** - Fixed the rewind menu offering "Summarize from here" and "Summarize up to here" when `DISABLE_COMPACT` is set
- **[UNCOVERED]** - Fixed a finished `/code-review`, or another skill that runs in a sub-agent, running a second time when a cloud or background session restarts
- **[UNCOVERED]** - Fixed long hidden thinking being cut off as idle on Google Vertex AI, Microsoft Foundry and Claude Platform on AWS, where the endpoint sends thinking progress updates
- **[UNCOVERED]** - Fixed `/ide` saying it had installed the JetBrains plugin when nothing was installed
- **[UNCOVERED]** - Fixed Claude Pro and Max subscribers being told to ask their admin when their subscription can't be used; the message now points to billing settings
- **[UNCOVERED]** - Fixed the diff pane opening by itself after an edit in wide fullscreen terminals when it had nothing to show
- **[UNCOVERED]** - Fixed `/mcp` showing a remote server as failed after "Clear authentication" when the server works without sign-in
- **[UNCOVERED]** - Fixed `/mcp` showing "authenticated" for a remote server that Claude Code sends no credentials to
- **[UNCOVERED]** - Fixed `/usage` never showing large prompt-cache misses under "What's contributing to your limits usage?"
- **[UNCOVERED]** - Fixed status line links staying plain text in background sessions after you open them from a terminal that supports links
- **[UNCOVERED]** - Fixed the /rewind confirmation saying the conversation "will be forked" when the later messages are removed from the conversation
- **[UNCOVERED]** - Fixed the /rewind warning that wrongly said manual and Bash edits are never affected by a code restore
- **[UNCOVERED]** - Fixed plan approval in screen reader mode sending feedback you had dismissed with Escape
- **[UNCOVERED]** - Fixed Claude Code retrying requests the API marked not to retry, which could hold a turn for minutes or, in unattended retry mode (`CLAUDE_CODE_RETRY_WATCHDOG`), indefinitely
- **[UNCOVERED]** - Linux: Fixed sandboxed Bash commands failing with `bwrap: Can't create file` when a `--plugin-dir` folder was also an added directory and `permissions.blockReadsOutsideWorkingDirectories` was on
- **[UNCOVERED]** - Self-hosted runner: Fixed a session failing to start when a rate limit (HTTP 429, or a git wrapper that exits 75) blocks an added read-only repository; it now starts without that repository
- **[UNCOVERED]** - Improved startup time for Pro and Max accounts by skipping two network requests on launches within an hour of the last check
- **[UNCOVERED]** - Improved `/teleport` and `claude --teleport` to warn when a compacted cloud session loads from its last compaction, so the messages it summarized aren't in the local copy
- **[UNCOVERED]** - Improved the messages shown when a background session's process exits: they no longer promise a restart that isn't coming, and they say how to resume the session
- **[UNCOVERED]** - Improved artifacts with several views: Claude now routes each view on the link's `#name` and no longer says the address bar stays the same as you switch views
- **[UNCOVERED]** - Improved shell commands that reach their timeout: the result now shows the output so far and says the command is still running in the background
- **[UNCOVERED]** - Improved compaction: when the model's reply has no summary in it, Claude Code now usually asks for the summary once more before it replaces the conversation
- **[UNCOVERED]** - Improved the Artifact tool's choice between a page and a document: explainers and visual or interactive work become artifact pages; documents are for writing people keep editing or pass around
- **[UNCOVERED]** - Improved startup time for launches whose only arguments are options and their values, such as `claude --model opus`
- **[UNCOVERED]** - Improved the "Connection dropped" API error: it now says where to look first (the proxy or gateway in use, else VPN or firewall; Anthropic API only, Bedrock, Vertex and Foundry are unchanged)
- **[UNCOVERED]** - Improved screen reader mode: deleting a rule in /permissions says "Deleted allow rule …" right away
- **[UNCOVERED]** - Improved the message shown when a pasted sign-in code is refused: it now says the code may have expired or been used, and to sign in again
- **[UNCOVERED]** - Improved Slack connector sends: Claude now checks a channel's topic for posting rules before messaging a channel you didn't name
- **[UNCOVERED]** - Improved screen reader mode: Claude's questions are listed as "Questions: Color (answered), Pages", without arrows or symbols
- **[UNCOVERED]** - Changed `ultrathink` in the interactive terminal to run its turn at xhigh effort on Opus 5.5, Sonnet 5.5, Haiku 5.5 and Fable 5.1 through Anthropic's API; typed while Claude is working, it raises the rest of that turn
- **[UNCOVERED]** - Changed the `ultrathink` rainbow to appear only where the keyword can raise effort, and not when the word is quoted or part of a file path
- **[UNCOVERED]** - Changed Ctrl+D in agent view to match the prompt: on an empty input, pressing it twice exits
- **[UNCOVERED]** - Changed `--output-format json` and `stream-json` output to write DEL, C1 control and Unicode format characters inside strings as `\uXXXX` escapes; parsed values are unchanged
- **[UNCOVERED]** - Changed model names and IDs to drop the `[1m]` suffix and its label on models where the suffix has no effect; the suffix is still accepted
- **[UNCOVERED]** - Changed startup warnings about permission rules in settings files to show once per user until the rule changes
- **[UNCOVERED]** - Changed `/code-review` to tell Claude to put the effort level first and use max only when asked
- **[UNCOVERED]** - Changed `DISABLE_COMPACT` in settings files and in a mod's `$.env.set` so they can only turn compaction off, not back on
- **[UNCOVERED]** - Changed Claude Code on Bedrock, Mantle, Vertex, and Foundry to load model settings from a signed file on downloads.claude.ai; set CLAUDE_CODE_MODEL_CATALOG=off to turn this off
- **[UNCOVERED]** - Changed sessions that set `CLAUDE_CODE_SYNC_SKILLS` with feature-flag fetching off to reuse a claude.ai skills list up to 10 minutes old that another session on the machine fetched
- **[UNCOVERED]** - Changed clicks on scrollbar arrows and bars in fullscreen lists to act when the mouse button is released, so moving off the scrollbar before letting go cancels the click
- **[UNCOVERED]** - Changed `claude purge` to say it deletes data only on this computer, not anything stored by Anthropic
- **[UNCOVERED]** - [VSCode] Added syntax coloring to code blocks in Claude's replies, in light, dark and high contrast dark themes
- **[UNCOVERED]** - [VSCode] Added a "Running UserPromptSubmit hooks" spinner status and screen reader announcement for slow UserPromptSubmit hooks
- **[UNCOVERED]** - [VSCode] Fixed custom skills and custom slash commands sent from the VS Code or JetBrains panel leaving out the open file or selected lines that ordinary messages include (anthropics/claude-code#102799)
- **[UNCOVERED]** - [VSCode] Fixed the extension host freezing while the login shell ran its start-up files to read PATH on macOS and Linux
- **[UNCOVERED]** - [VSCode] Fixed clicking an image in a tool result, or closing its preview, also opening the result's text in an editor tab
- **[UNCOVERED]** - [VSCode] Fixed voice dictation continuing to record after a message was sent with the Send button; sending now stops dictation first, as pressing Enter already did
- **[UNCOVERED]** - [VSCode] Changed the extension to start Claude Code sessions with `DISABLE_TELEMETRY` set while VS Code's telemetry setting is off, so they send no usage metrics or error reports and fetch no feature flags
- **[UNCOVERED]** - [VSCode] Changed the session list side bar to load Web sessions when the Web tab is first opened, not at startup
- **[UNCOVERED]** - [Cloud sessions] Fixed routines in Anthropic-hosted environments staying locked after their owner left the organization and rejoined; the owner can now turn them back on
- **[UNCOVERED]** - [Cloud sessions] Fixed a failed routine API token delete or regenerate showing nothing if the edit dialog had already closed; it now shows an error toast
- **[UNCOVERED]** - [Cloud sessions] Fixed cloud environment dialogs, including the admin dialog, accepting duplicate names; they now refuse a name another listed environment already has
- **[UNCOVERED]** - [Claude Tag] Added a Skills view to Claude Tag analytics showing how often Claude runs each attached skill in Slack channels and which go unused, with Usage links in admin settings
- **[UNCOVERED]** - [Claude Tag] Improved Claude Tag routines that run in a new session: a run with nothing to report can now end without posting a throwaway message to the channel
- **[UNCOVERED]** - [Claude Tag] Changed Claude Tag admin settings to show a lock instead of # for private Slack channels that your own Slack account can see
- **[UNCOVERED]** - [Code Review] Improved Code Review's check run to say no further automatic review will start when the model still can't analyze a change on the automatic retry
- **[UNCOVERED]** - [Code Review] Improved Code Review reliability: a review whose session fails to start because of a transient server fault is now retried once automatically, and its check run says so

---
_Generated by `.github/scripts/changelog-compare.py`_
## Native Sources Monitor Report

Sources checked: **3**

### anthropic-blog

- Source: Anthropic Blog — announcements and product updates
- Entries fetched: 26
- New uncovered: 0

### cc-issues-enhancement

- Source: CC GitHub Issues labeled 'enhancement'
- Entries fetched: 300
- New uncovered: 6

| Entry | Section | Description |
|-------|---------|-------------|
| [FEATURE] Soporte de localización de la interfaz (español) e | GitHub Issues (enhancement) | ### Preflight Checklist - [x] I have searched [existing issues]( and this hasn't |
| A horário da última mensagem recebida pode confundir o usuár | GitHub Issues (enhancement) | **What happened** A horário da última mensagem recebida pode confundir o usuário |
| Barre latérale du Code tab : groupes imbriqués et distinctio | GitHub Issues (enhancement) | J'utilise l'app de bureau (onglet Code, Windows) avec une quarantaine de session |
| A gestão está um pouco diferente. Era mais simples quando er | GitHub Issues (enhancement) | **What happened** A gestão está um pouco diferente. Era mais simples quando era  |
| il dettaglio deve essere a destra. | GitHub Issues (enhancement) | **What happened** il dettaglio deve essere a destra. quando apri un markdown da  |
| [Feature Request] Support low-level memory log analysis for  | GitHub Issues (enhancement) | **Bug Description** estoy haciendo revisiones sobre mis propios dispositivos. re |

### cc-discussions-feature-request

- Source: CC GitHub Discussions in feature-request category
- Entries fetched: 0
- New uncovered: 0

---
Total new uncovered entries: **6**

_Generated by `.github/scripts/native-sources-monitor.py`_
