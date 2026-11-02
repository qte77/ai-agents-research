# CC Changelog & Native Sources: New Uncovered Features Detected

## Changelog Monitor Report

Last scanned version: **2.1.303**
New versions detected: **7**

### New Versions Summary

| Version | Features | Covered | Uncovered |
|---------|----------|---------|-----------|
| 2.1.310 | 26 | 0 | 26 |
| 2.1.309 | 79 | 1 | 78 |
| 2.1.308 | 1 | 0 | 1 |
| 2.1.307 | 43 | 0 | 43 |
| 2.1.306 | 2 | 0 | 2 |
| 2.1.305 | 38 | 0 | 38 |
| 2.1.304 | 76 | 0 | 76 |

### Feature Coverage Details

#### v2.1.310 — released 2026-10-23

- **[UNCOVERED]** - Added the Monitor tool and plugin monitors on Bedrock, Vertex, and Foundry, and when telemetry or nonessential traffic is disabled; long foreground sleeps are now blocked there too
- **[UNCOVERED]** - Fixed requests failing behind some gateways and compatible servers that reject the `effort-2025-11-24` beta value or mid-conversation system messages; Claude Code now retries without them
- **[UNCOVERED]** - Fixed background cleanup deleting some recent files, such as pasted images, when `cleanupPeriodDays` is set to a very large value
- **[UNCOVERED]** - Fixed compaction after a "Prompt is too long" error keeping too much of a conversation with dense text, such as base64 or SVG, so the next request could fail again
- **[UNCOVERED]** - Fixed file read permission prompts not showing where a symbolic link leads
- **[UNCOVERED]** - Fixed a question's auto-continue timeout firing the moment the external editor closed after a long edit
- **[UNCOVERED]** - Windows: Fixed PreToolUse and PermissionRequest hooks letting a tool call through when Git Bash is missing and the hook's command is only quoted strings, such as a quoted path
- **[UNCOVERED]** - Improved auto mode's prompt before the first read outside the working directories: it now says when blocking those reads makes shell commands ask for permission
- **[UNCOVERED]** - Improved memory use of non-interactive sessions (`-p`, Agent SDK) during compaction when the transcript file is very large
- **[UNCOVERED]** - Improved a mod's `Image` to draw inside tmux with `allow-passthrough` and `focus-events` on, in kitty, Ghostty, and iTerm2 3.5+ with fullscreen rendering, where it showed only its `alt` text
- **[UNCOVERED]** - Linux: Improved `/sandbox` and the sandbox startup warning to name Ubuntu's AppArmor restriction on user namespaces, and how to lift it, when it keeps bubblewrap from starting the sandbox
- **[UNCOVERED]** - Changed the error for an MCP tool call that times out in a non-interactive session while the server's elicitation is unanswered: it now tells Claude that no answer came and not to repeat the call
- **[UNCOVERED]** - [VSCode] Fixed pressing Enter on the plan review card's "Send feedback and keep planning" button approving the plan instead of sending your comments back
- **[UNCOVERED]** - [VSCode] Fixed the panel showing "Something went wrong" after "Switch branch & continue" on a cloud session opened from Session history's Web tab
- **[UNCOVERED]** - [Cloud sessions] Added Claude Code cloud sessions and Remote Control permissions to Enterprise custom roles, so Owners can control access to each by role
- **[UNCOVERED]** - [Cloud sessions] Added a Choose file button to load a cloud environment's setup script from a file
- **[UNCOVERED]** - [Cloud sessions] Fixed failed saves and archives in the cloud environment edit dialog showing no error inside the dialog
- **[UNCOVERED]** - [Cloud sessions] Fixed failed routine API token actions showing only a toast; the error now appears in the routine edit dialog
- **[UNCOVERED]** - [Cloud sessions] Improved the session start checklist to show a cloud environment's setup script output in a scrolling box
- **[UNCOVERED]** - [Cloud sessions] Changed turning on Cloud sessions or Remote Control in admin settings to ask for confirmation and list the custom roles that have that permission
- **[UNCOVERED]** - [Cloud sessions] Changed the cloud environment dialog to open network access, setup script and environment variables from rows instead of listing every editor at once
- **[UNCOVERED]** - [Claude Tag] Fixed Claude Tag treating `!` commands such as `!restart` and `!help` as ordinary messages when sent in bold, italic or strikethrough
- **[UNCOVERED]** - [Claude Tag] Fixed Claude Tag admin channel and workspace pages being replaced by a load error when a background refresh of the bundle list fails
- **[UNCOVERED]** - [Claude Tag] Fixed Claude Tag's spend limits page in admin settings reporting that no channels match a filter while channel names are still loading
- **[UNCOVERED]** - [Code Review] Fixed the Code Review admin section hiding its repositories and switches after a failed refresh of the repository list
- **[UNCOVERED]** - [Code Review] Improved the Code Review admin section to retry the first load and show one Try again banner when it still fails

#### v2.1.309 — released 2026-10-22

- **[covered]** - Fixed sessions renamed with `/rename` appearing to other sessions under a generated name after a VS Code window reload or a non-interactive `--resume`
  - Covered by: `cc-native/sessions/CC-session-lifecycle-analysis.md`
- **[UNCOVERED]** - Fixed sandboxed Bash commands on macOS and Linux running the shell's startup files outside the sandbox before each command
- **[UNCOVERED]** - Fixed macOS sandbox `denyWrite` glob patterns not applying at a path's real location when the pattern's folder is reached through a symlink
- **[UNCOVERED]** - Fixed sandboxed commands and auto-accepted edits being able to modify the MCP config file passed with `--mcp-config`
- **[UNCOVERED]** - Fixed a disabled MCP server being reconnected by a later permission prompt in print and SDK sessions
- **[UNCOVERED]** - Fixed the Bash permission check trusting a variable set by a command whose redirect can fail to open
- **[UNCOVERED]** - Fixed Bash permission checks not prompting for some compound commands that change directory before running git when the `cd` is wrapped or prefixed, as they do for a plain `cd`
- **[UNCOVERED]** - Fixed an `Edit(path)` deny rule not blocking a Bash redirect to that path in some commands that also held a subshell
- **[UNCOVERED]** - Fixed worktree-isolated sessions accepting some locale-prefixed commands the isolation guard should refuse
- **[UNCOVERED]** - Fixed worktree-isolated sessions on zsh accepting some arithmetic commands that the isolation guard should refuse
- **[UNCOVERED]** - Fixed worktrees and branch checkouts that Claude Code creates so they ignore git replace refs, as its other git operations already do
- **[UNCOVERED]** - Fixed profile store write protection not applying when the config directory is reached through a symlink
- **[UNCOVERED]** - Fixed sessions compacting repeatedly after reading files under a very large nested CLAUDE.md; a nested CLAUDE.md over the size limit now loads only its start
- **[UNCOVERED]** - Fixed ctrl+enter (send now) only queuing a message when pressed before the response had started, and restarting a prompt's hooks while leaving the message queued when pressed while those hooks were running
- **[UNCOVERED]** - Fixed key-bound slash commands running in the shell from `!` mode
- **[UNCOVERED]** - Fixed ctrl+o not showing messages from other agents and sessions that are still waiting to be delivered; they now appear in full under the transcript, marked as waiting
- **[UNCOVERED]** - Fixed long tool output previews being cut through an emoji, leaving session transcripts that `jq` could not parse
- **[UNCOVERED]** - Fixed Read reporting "File does not exist" for PDF page ranges in Linux sandboxes that share the parent's `/proc`
- **[UNCOVERED]** - Fixed messages from a Claude Desktop-hosted session sometimes being lost when its connection refreshed
- **[UNCOVERED]** - Fixed features missing from Claude Code sessions in the Claude desktop app when the terminal on the same computer was signed in to a different account or organization
- **[UNCOVERED]** - Fixed the `claude remote-control` status line showing `HEAD` as the branch for a folder that is not in a git repository
- **[UNCOVERED]** - Fixed split-pane agent teammates not inheriting the tool deny and `--tools` rules given on the leader's command line
- **[UNCOVERED]** - Fixed the `/rewind` list showing "No code changes" for a turn that changed checkpointed files through `/code-review --fix`, a subagent or a shell command
- **[UNCOVERED]** - Fixed `/privacy-settings` showing an out-of-date "Help improve our AI models" value; it now also says when the setting can't be fetched
- **[UNCOVERED]** - Fixed feedback saying "try again later" when your organization does not accept feedback; it now shows the server's reason and where to report a bug
- **[UNCOVERED]** - Fixed oversized /feedback reports failing instead of being resent without the transcript
- **[UNCOVERED]** - Fixed a skill in an `--add-dir` folder being unreachable when another skill already held its name; it is now offered as `<folder>:<name>`
- **[UNCOVERED]** - Fixed `/verify` and `/code-review` not finding a nested package's own skill when its files were changed from the shell
- **[UNCOVERED]** - Fixed the /claude-api skill saying that `ant beta:worker poll --on-work` passes trace context to the command
- **[UNCOVERED]** - Fixed the /claude-api skill's C# tracing setup missing spans from the cloud platform clients
- **[UNCOVERED]** - Fixed the /claude-api skill saying that API spans for requests to Claude Platform on AWS can't join the caller's trace
- **[UNCOVERED]** - Fixed hooks that run in PowerShell not blocking when the hook's program exits with code 2, and on Windows `PreToolUse` and `PermissionRequest` hooks with `"shell": "powershell"` failing open when Git for Windows isn't installed
- **[UNCOVERED]** - Fixed a mod's `turn.step` hook that names a model by alias, such as `haiku`, failing every request with a model error: the alias now resolves to its model
- **[UNCOVERED]** - Fixed plugins and skills synced from claude.ai being removed, sometimes mid-session, after a disk read error
- **[UNCOVERED]** - Fixed artifact publishes and updates being refused for some ordinary pages, such as pages with certain minified scripts or artifacts Claude could not read first
- **[UNCOVERED]** - Fixed Claude asking for permission on each artifact update for the rest of a turn after the conversation was compacted in that turn
- **[UNCOVERED]** - Fixed fine-grained tool streaming staying off on Amazon Bedrock when `ANTHROPIC_BEDROCK_BASE_URL` is set to the default `bedrock-runtime.<region>.amazonaws.com` endpoint
- **[UNCOVERED]** - Fixed the "Waiting for API response" hint flickering behind gateways that send only keepalive pings: routes off Anthropic's backend now wait 45 seconds
- **[UNCOVERED]** - Fixed Claude notifying unrelated GitHub users by writing role names and placeholders as mentions in PRs, issues and comments
- **[UNCOVERED]** - Linux: Fixed sandbox write denies lifting when a background command outlived the session
- **[UNCOVERED]** - Windows: Fixed PowerShell permission checks auto-approving some `Set-Location` or `cd` commands that target the current directory and carry extra arguments; these now prompt for approval
- **[UNCOVERED]** - macOS: Fixed the "Install Command Line Developer Tools" dialog opening each time Claude Code starts on a Mac without Xcode or the Command Line Tools
- **[UNCOVERED]** - Self-hosted runner: Fixed `--startup-timeout-min` stopping a session whose first prompt, such as `/code-review`, was still working in a subagent; a frozen process is still stopped
- **[UNCOVERED]** - Improved the speed of many git commands Claude Code runs for itself on Windows; on every platform, errors from those commands now show in English even when git is set to another language
- **[UNCOVERED]** - Improved the error when a hooks module is nested too deep to load: it now names the file instead of showing a bare stack-overflow message
- **[UNCOVERED]** - Improved disk-full handling: a Bash command cut off by a full disk now says so and names the folder to free up, and starting on a full temp volume prints a clear message, not a raw ENOSPC error
- **[UNCOVERED]** - Improved the /claude-api skill to offer API tracing alongside SDK tracing when asked to add OpenTelemetry
- **[UNCOVERED]** - Improved the /claude-api skill to check the live docs before saying a feature is unsupported
- **[UNCOVERED]** - Self-hosted runner: Improved sessions that move to a new runner: Claude now sees the tool call that was interrupted, marked as outcome unknown
- **[UNCOVERED]** - Updated the bundled dataviz skill to accept APCA as a text-contrast measure (keeping WCAG 2 ratios where AA conformance is required), add an `apca(text, background)` function to its palette validator scripts, and say whether a label inside a colored chart fill should be white or near-black
- **[UNCOVERED]** - Updated the /claude-api skill: service account keys and Workload Identity Federation tokens can now manage OpenTelemetry destinations
- **[UNCOVERED]** - Changed `sed -i` to get the standard Bash prompt and run as written, not a simulated file-edit preview; like other Bash edits, it is no longer restored by `/rewind`
- **[UNCOVERED]** - Changed `claude ultrareview` to require workspace trust: it asks on a terminal, else refuses; scripts pass `--trust-workspace`, which takes no value (put a PR number or base branch before it), or set `CLAUDE_CODE_DISABLE_ULTRAREVIEW_TRUST_CHECK=1`
- **[UNCOVERED]** - Changed the dangerous `rm` and `rmdir` prompt in bypass permissions mode in the Desktop app and VS Code to deny the command at once with a rewrite hint, so unattended sessions keep going
- **[UNCOVERED]** - Changed commands the settings exclude from the sandbox to ask before writing to its write-list paths while the sandbox is enabled but cannot run; the unsandboxed fallback is refused there
- **[UNCOVERED]** - Changed worktree creation and reuse so git no longer fetches objects on demand, in ordinary clones and in partial clones with a Bash sandbox configured; such a partial clone fetches them first
- **[UNCOVERED]** - Changed the `/claude-api` skill to build Managed Agents subagent teams on `multiagent_20261001` with dynamic workflows on by default, instead of `coordinator`
- **[UNCOVERED]** - [VSCode] Added a log warning that says what to do when dictation or the extension's own requests fail certificate verification, such as behind a TLS-inspecting proxy
- **[UNCOVERED]** - [VSCode] Fixed the Claude panel staying blank after the editor cached an incomplete copy of its files; it now recovers by itself, or says what went wrong and how to fix it
- **[UNCOVERED]** - [VSCode] Fixed Session history filling up with empty "Untitled" sessions each time you start a new session without sending a message
- **[UNCOVERED]** - [VSCode] Fixed long slash-command messages such as `/goal` filling the chat panel; they now fold behind Show more like other prompts (anthropics/claude-code#97469)
- **[UNCOVERED]** - [VSCode] Fixed long messages not folding behind Show more after the chat panel is made narrower
- **[UNCOVERED]** - [VSCode] Fixed Ctrl+J in the chat input always inserting a newline: it is now left to VS Code and the OS when "ctrl+j" is set to null in the Chat context of ~/.claude/keybindings.json
- **[UNCOVERED]** - [VSCode] Fixed a mod's "From the … plugin" label above the prompt being drawn over the slash command and @-mention menus (anthropics/claude-code#102981)
- **[UNCOVERED]** - [VSCode] Fixed an empty list item, paragraph or code block, and list items renumbered from 1, when pasting copied LaTeX math
- **[UNCOVERED]** - [VSCode] Fixed the feedback error showing only an HTTP status when your organization does not accept feedback
- **[UNCOVERED]** - [VSCode] Improved Edit and Write speed in the chat panel: the wait for new problems after each edit is now 0.75 seconds in most cases, down from 1 to 1.5 seconds
- **[UNCOVERED]** - [Cloud sessions] Fixed the Add connector list in routine forms saying no connectors were available while they were still loading
- **[UNCOVERED]** - [Cloud sessions] Fixed the cloud environment editor shuffling environment variables and adding backslashes to values that contain both kinds of quote
- **[UNCOVERED]** - [Cloud sessions] Fixed the self-hosted environment details dialog in admin settings so its title, tabs and buttons stay in view while only the content scrolls
- **[UNCOVERED]** - [Cloud sessions] Fixed the "read documentation" tool row in cloud sessions, which showed escaped JSON instead of a readable page
- **[UNCOVERED]** - [Cloud sessions] Improved a cloud session's Changes pane, which now says when it lists only pushed commits or only Claude's edits
- **[UNCOVERED]** - [Claude Tag] Fixed Claude in Slack posting a draft you approved for a channel into your DM by mistake; a post with no channel is now refused so it can go to the approved channel
- **[UNCOVERED]** - [Claude Tag] Fixed Allow and Deny on Claude's approval cards in Slack doing nothing when the session had stopped; your answer now restarts the session
- **[UNCOVERED]** - [Claude Tag] Fixed Claude ignoring untagged messages in a Slack channel after its workspace moved to a different Claude organization, including unshared channels on Enterprise Grid
- **[UNCOVERED]** - [Claude Tag] Fixed Claude in a Slack channel posting a threaded reply before reading a newer message someone had just added to that thread
- **[UNCOVERED]** - [Claude Tag] Fixed the Slack page in Claude Tag admin settings saying no workspaces were connected when the list failed to load; it now shows an error with a Retry button
- **[UNCOVERED]** - [Code Review] Fixed a finished review showing no check on the pull request when earlier tries to create it failed; a final try now adds a completed check
- **[UNCOVERED]** - [Code Review] Fixed a push queued behind a running review still starting a review after `@claude review stop`; its check now closes and says why

#### v2.1.308 — released 2026-10-22

- **[UNCOVERED]** - Bug fixes and reliability improvements

#### v2.1.307 — released 2026-10-21

- **[UNCOVERED]** - Added `/claude-api api-version` to move Claude API code to API version `2026-10-21`
- **[UNCOVERED]** - Added the `claude_code.safety_event` OpenTelemetry event for each tool call a permission rule, auto mode, a safety check, a hook or the sandbox stopped, prompted or sent back
- **[UNCOVERED]** - Fixed requests failing with a model-not-found error when `CLAUDE_CODE_DISABLE_1M_CONTEXT` is set and the model is an alias with the `[1m]` suffix, such as `opus[1m]`
- **[UNCOVERED]** - Fixed the `prompt-caching-scope` beta header being sent behind custom `ANTHROPIC_BASE_URL` gateways and on Foundry, where it has no effect
- **[UNCOVERED]** - Fixed MCP servers showing "needs authentication" in `claude -p` on macOS while the login keychain was locked; they now say why, and the next run after an unlock connects without a new sign-in
- **[UNCOVERED]** - Fixed MCP servers being reported as timed out, and staying failed in headless runs, when a macOS or Linux computer went to sleep while they were connecting
- **[UNCOVERED]** - Fixed HTTP MCP tool calls being sent twice when the connection closed mid-call; only read-only or idempotent tools are now retried
- **[UNCOVERED]** - Fixed a turn sometimes starting without an SDK MCP server's latest tools when a background task was running
- **[UNCOVERED]** - Fixed some "Autocompact is thrashing" errors in turns that read many PDF pages, images or other large tool results
- **[UNCOVERED]** - Fixed `/autocompact` in cloud sessions going back to the default window after the session restarted
- **[UNCOVERED]** - Fixed a conversation cleared with `/clear` sometimes coming back when a cloud or self-hosted runner session restarted
- **[UNCOVERED]** - Fixed `CLAUDE_STREAM_FIRST_BYTE_TIMEOUT_MS` being ignored in Claude apps gateway sessions
- **[UNCOVERED]** - Fixed telemetry from Claude Desktop sessions behind a Claude apps gateway being rejected when `OTEL_EXPORTER_OTLP_HEADERS` is set
- **[UNCOVERED]** - Fixed `/permissions` > Recently denied not showing the denied shell command, and auto mode's local classifier ignoring an approval from there when it checks a retried command; approving a row now names the command, not its description
- **[UNCOVERED]** - Fixed `/help` and the `/` command menu showing long model-facing descriptions for bundled skills such as `/claude-api` instead of their short descriptions
- **[UNCOVERED]** - Fixed subagent transcripts recording placeholder token usage and an empty stop reason for streamed responses
- **[UNCOVERED]** - Fixed model switches through the Agent SDK's `setModel()`, and apps built on it, being refused when the API took more than 5 seconds to confirm the model; Claude Code now waits up to 15 seconds
- **[UNCOVERED]** - Fixed a background command stopped through a connected app (such as the desktop app archiving an idle session) being reported to Claude as stopped by the user; the notice now names its output file
- **[UNCOVERED]** - Fixed WebFetch in Cowork cloud sessions reporting a tool error when a site answered with a 4xx status or a robots.txt refusal; it is now a normal result, as in local sessions
- **[UNCOVERED]** - Fixed write tools on a directly configured GitHub MCP server showing a form that closed without creating anything in the desktop app's Code tab
- **[UNCOVERED]** - Fixed Artifact tool reads failing with a connection reset when the server had closed a reused connection
- **[UNCOVERED]** - Self-hosted runner: Fixed sessions with `--use-anthropic-git-proxy` committing a `.claude/settings.local.json` left in the clone by an earlier session
- **[UNCOVERED]** - Self-hosted runner: Fixed archiving or requeueing a session, or stopping the runner, during its checkout hook leaving the hook's processes running and the runner's slot held
- **[UNCOVERED]** - Improved recovery from unparseable tool calls: Claude Code now retries the call up to twice before ending the turn with an error
- **[UNCOVERED]** - Improved fork subagents launched together: each is now told which launch is its own, so forks are much less likely to try to start each other's work
- **[UNCOVERED]** - Improved browser sign-in: the success page now appears as soon as sign-in completes, without waiting for your account profile to load
- **[UNCOVERED]** - Improved web search errors in cloud and self-hosted runner sessions: a search refused with a 403 that gives a reason now shows that reason instead of a generic "Authentication error"
- **[UNCOVERED]** - Improved the time to the first reply in cloud sessions when one of the desktop app's MCP servers can't connect
- **[UNCOVERED]** - Improved Remote Control connect time for sessions whose transcript contains large pasted images or PDF reads
- **[UNCOVERED]** - Changed the notice Claude gets when the WebSearch budget is used up to also tell it not to query search engines in a browser or through computer use
- **[UNCOVERED]** - Changed the `axScreenReader` setting and `CLAUDE_AX_SCREEN_READER` in a settings `env` block to apply only from user, managed or `--settings` settings (since 2.1.305)
- **[UNCOVERED]** - Self-hosted runner: Changed checkout hooks to be stopped after 30 minutes by default, failing the session's setup; if yours needs longer, raise `--checkout-hook-timeout-min` or set it to `0`
- **[UNCOVERED]** - Self-hosted runner: Changed the certificate file built for Anthropic-managed git to filter its trusted certificates as the CLI does; a `[runner:warn]` line gives the number left out
- **[UNCOVERED]** - [VSCode] Added a notice on the microphone button when voice dictation stops by itself (15 seconds without recognized speech, or the 2-minute limit), saying why and that the text so far is kept
- **[UNCOVERED]** - [VSCode] Fixed a long prompt expanded with Show more covering the whole chat panel: a pinned prompt is now capped at 40% of the panel and scrolls
- **[UNCOVERED]** - [VSCode] Fixed part of a list item or table cell with LaTeX math pasting as a new list or table in rich text editors
- **[UNCOVERED]** - [VSCode] Fixed dictation failing behind a TLS-inspecting proxy when `NODE_EXTRA_CA_CERTS` is set only in `~/.claude/settings.json`; it now also follows `CLAUDE_CODE_CERT_STORE`
- **[UNCOVERED]** - [VSCode] Changed the "still open somewhere else" notice to also cover a Claude process left over from an extension restart, which usually ends on its own within about 10 minutes
- **[UNCOVERED]** - [VSCode] Changed voice dictation to filter its trusted certificates as the CLI does
- **[UNCOVERED]** - [VSCode] Changed the extension's own requests to filter their trusted certificates as the CLI does, and to trust the `NODE_EXTRA_CA_CERTS` file named in the environment or in user settings
- **[UNCOVERED]** - [Cloud sessions] Fixed the repository picker saying "No repositories match" while a search was still running; it now shows "Searching…" until the results arrive
- **[UNCOVERED]** - [Cloud sessions] Fixed the "Waiting for a runner" status on self-hosted environments being cut off; with on-demand runners it now counts up from your last message and shows failed attempts
- **[UNCOVERED]** - [Code Review] Added `@claude review stop` (also `off` and `pause`) to Code Review, ending an `@claude review always` subscription on a pull request without starting a new review

#### v2.1.306 — released 2026-10-21

- **[UNCOVERED]** - Fixed `claude -p` inside cloud sessions reporting "Not logged in" when started without the session's environment variables
- **[UNCOVERED]** - Fixed an API error being replaced by "prompt is too long", and an unneeded compaction, in sessions with many MCP tools

#### v2.1.305 — released 2026-10-20

- **[UNCOVERED]** - Added `sandbox.allowNestedUserNamespaces` so sandboxed commands on Linux can create user namespaces (Chromium, rootless podman); this lets them get around the sandbox's file protections
- **[UNCOVERED]** - Added `CLAUDE_CODE_RETRY_WATCHDOG_USAGE_LIMIT_RECHECK_MS` so unattended retry mode (`CLAUDE_CODE_RETRY_WATCHDOG`) notices a usage limit that was lifted before its reset
- **[UNCOVERED]** - Fixed every request failing on Vertex, Bedrock and other providers when the endpoint or a gateway rejects tool search, and behind gateways with ToolSearch disallowed or left out of `--tools` (a 2.1.304 regression): Claude Code now retries without it
- **[UNCOVERED]** - Fixed `/effort` and `/autocompact` settings not applying when the model name differed from a `modelOverrides` value by letter case or a `[1m]` tag
- **[UNCOVERED]** - Fixed new worktrees in a bare repository sometimes starting from local HEAD instead of the default branch, and unchanged subagent worktrees sometimes not being cleaned up
- **[UNCOVERED]** - Fixed Bash commands on a full disk failing with a raw `ENOSPC` file path: the error now says the disk is full and that nothing ran
- **[UNCOVERED]** - Fixed an MCP server passed by a cloud session or by the SDK's `setMcpServers` being replaced later in the session by a same-named server from your own settings
- **[UNCOVERED]** - Fixed Claude naming the wrong model for a subagent's work after the subagent switched to a fallback model
- **[UNCOVERED]** - Fixed cloud sessions and teammates not telling Claude when a compaction had to leave the oldest messages out of its summary to fit
- **[UNCOVERED]** - Fixed more cases of scheduled Cowork cloud sessions waiting five minutes for each subagent whose WebFetch needed a URL approval that nobody was there to give
- **[UNCOVERED]** - Fixed Workflow resume re-running already-completed `pipeline()` and `parallel()` agents instead of serving them from the run's journal
- **[UNCOVERED]** - Fixed Remote Control leaving empty "(session)" entries in `/resume` after switching conversations with `/resume`
- **[UNCOVERED]** - Fixed `/usage` rows being cut off in narrow terminals
- **[UNCOVERED]** - Fixed startup warnings printing as raw text above the logo: they now go to the debug log, and permission rules that restrict nothing show as warning rows under the banner
- **[UNCOVERED]** - Fixed screen reader mode: search boxes now say "Search:" instead of a symbol VoiceOver read as "telephone recorder", and highlighted prompt text, such as Ctrl+R search matches and "ultrathink", no longer has spaces inside words
- **[UNCOVERED]** - Self-hosted runner: Fixed a start script that shares only its stdout with the runner or orchestrator failing with `Resource temporarily unavailable` when `TERM` is set (a 2.1.300 regression)
- **[UNCOVERED]** - Self-hosted runner: Fixed repository access failing since 2.1.296 when a git credential helper or askpass program reads its settings through `GIT_CONFIG`
- **[UNCOVERED]** - Self-hosted runner: Fixed the orchestrator reporting a spawn-runner hook as timed out when a runner it started in the background kept its output open
- **[UNCOVERED]** - Improved `/usage`: each warning is now a one-line fix that names its source, and `f` applies the fixes; the same fixes appear in VS Code and `/doctor`
- **[UNCOVERED]** - Improved MCP consent dialogs so an Enter meant for the prompt is less likely to be taken as Accept
- **[UNCOVERED]** - Improved a mod's `Image` to draw its picture in iTerm2 3.5 and later with fullscreen rendering, where it showed only its `alt` text
- **[UNCOVERED]** - Remote Control: Improved the spawn-mode messages: pressing `w` now says the new mode is saved for the folder, and a later `claude remote-control` start that uses the saved mode says where it came from
- **[UNCOVERED]** - Changed `allowedMcpServers` to stop filtering `managed-mcp.json` stdio servers that use `${VAR}` only in `env`: one your allowlist left out now loads on upgrade; use `deniedMcpServers` to keep it off
- **[UNCOVERED]** - Changed plugins that Claude Desktop mounts by path to no longer keep their `allowed-tools` when your organization's managed settings set `allowManagedPermissionRulesOnly`
- **[UNCOVERED]** - Changed the `/artifacts` delete confirmation to take 1 or Enter to keep, 2 to delete, and Esc to cancel; `y` and `n` no longer answer it
- **[UNCOVERED]** - Changed a mod's docked pane to stay within 45% of the terminal's width, including a width kept from a wider terminal
- **[UNCOVERED]** - [VSCode] Added a "Running start-up hooks" spinner status, with a screen reader announcement, while SessionStart or Setup hooks run
- **[UNCOVERED]** - [VSCode] Fixed the spinner cutting off "Compacting..." when your `spinnerVerbs` setting replaces the built-in verbs with short ones
- **[UNCOVERED]** - [VSCode] Changed the message shown when a session does not start in time and no hook is running: it now leads with the output logs and lists causes instead of pointing to sign-in and network first
- **[UNCOVERED]** - [Cloud sessions] Fixed the Cloud environments admin page wrongly refusing to save an existing environment with an "installs packages" error
- **[UNCOVERED]** - [Cloud sessions] Improved deleting a self-hosted environment so the dialog and error messages say what blocks the delete and what it will affect
- **[UNCOVERED]** - [Claude Tag] Added public Slack channels Claude hasn't joined to the Claude Tag admin Add place search, so admins can set one up from there
- **[UNCOVERED]** - [Claude Tag] Fixed Claude Tag access bundles so a repository that moved to another GitHub account can be added again
- **[UNCOVERED]** - [Claude Tag] Fixed a routine set up in a Slack DM thread no longer posting after another routine in that thread restarted the conversation; both now keep posting there
- **[UNCOVERED]** - [Claude Tag] Fixed routines set up in a Slack thread reporting success without posting after the conversation ended; those runs are now skipped and the creator is told
- **[UNCOVERED]** - [Claude Tag] Improved Claude Tag admin pages in large organizations so plugin, skill and bundle edits work while the channel list is still loading
- **[UNCOVERED]** - [Code Review] Fixed Code Review sometimes not reviewing the newest commit when several pushes landed on a pull request during a review
- **[UNCOVERED]** - [Code Review] Changed Code Review re-reviews so they no longer open with LGTM while earlier blocking findings are still open

#### v2.1.304 — released 2026-10-19

- **[UNCOVERED]** - Added a transcript line when a plugin that runs first skips one of your mod's hooks, naming the event and the plugin
- **[UNCOVERED]** - Added `decider: "person"` to a mod's `tool.check` answer: only the permission dialog or a host's callback can approve the ask, and it is refused with the mod's reason where nobody can be asked
- **[UNCOVERED]** - Added `e.isReadOnly` to a mod's `tool.check` event, set when the tool call is read-only
- **[UNCOVERED]** - Added `/auto-mode-setup`: a guided setup that reads your project and recent sessions to teach auto mode about your environment, now also available on Bedrock, Vertex, Foundry, Claude apps gateway and telemetry-disabled sessions
- **[UNCOVERED]** - Added `/claude-api managed-agents-secure`, which compares a Managed Agents agent's settings with Anthropic's published security guide, without changing anything
- **[UNCOVERED]** - Added the names of the tools called earlier to the compaction summary in the transcript view (Ctrl+O)
- **[UNCOVERED]** - Added a warning on Pro and Max plans when resuming an inactive conversation would use a noticeable share of your 5-hour usage limit: resume anyway, or start a new conversation and Claude can look up the previous one if you refer to it
- **[UNCOVERED]** - Fixed the organization policy not refreshing until the hourly check after approving an `ANTHROPIC_API_KEY` at startup or switching "Use custom API key" in `/config`
- **[UNCOVERED]** - Fixed sandboxed commands failing to start on Linux when a `sandbox.filesystem.denyRead` glob contains brackets that are not a character class, such as a `[user-id]` route folder
- **[UNCOVERED]** - Fixed `rm -r` of a mounted drive or a folder at its top level (`/Volumes`, `/media`, WSL's `/mnt/c`) not getting the safety prompt that `rm -rf /Applications` gets
- **[UNCOVERED]** - Fixed `CLAUDE_CODE_TRANSCRIPT_LOCAL_GC` dropping messages from the saved transcript when the disk filled up while the file was being trimmed
- **[UNCOVERED]** - Fixed a plugin keeping a headless run going past `--max-turns`, Stop, or ended input by spawning subagents or re-running a finished one
- **[UNCOVERED]** - Fixed a failed mod reload removing the tools and commands of the version that stays loaded, and its messages being wrong or silent about whether the previous version is still loaded
- **[UNCOVERED]** - Fixed a click on a mod's button being lost when buttons with the same label and no `key` were redrawn unchanged
- **[UNCOVERED]** - Fixed mod sharing in the built-in `plugin-authoring` skill stopping at the secret scan on machines with managed settings and on Team and Enterprise plans
- **[UNCOVERED]** - Fixed scheduled Cowork cloud sessions waiting five minutes again for each subagent whose WebFetch needed a URL approval that nobody was there to give
- **[UNCOVERED]** - Fixed Write results and rejected edits showing a file outside the working directory as `../../…`; they now show `~/…` or the full path
- **[UNCOVERED]** - Fixed a claude.ai Directory plugin's skills not running as commands when picked from the "/" menu in Cowork cloud sessions
- **[UNCOVERED]** - Fixed Remote Control permanently withholding a desktop conversation's history when a different account was signed in to the terminal
- **[UNCOVERED]** - Fixed Remote Control failing to start from Claude Desktop when DISABLE_TELEMETRY or DO_NOT_TRACK is set on a paid plan
- **[UNCOVERED]** - Fixed model switches, messages and interrupts waiting behind a context usage check in SDK and desktop sessions
- **[UNCOVERED]** - Fixed `context_management: Extra inputs are not permitted` errors behind LLM gateways; Claude Code now resends the request without that field
- **[UNCOVERED]** - Fixed OpenTelemetry settings delivered through server-managed settings being ignored for the whole session after signing in during first-run setup or the first start after /logout
- **[UNCOVERED]** - Fixed unsandboxed Bash commands in Claude Desktop Code tab sessions on macOS and Linux not seeing environment variables exported in shell startup files such as ~/.zshrc
- **[UNCOVERED]** - Fixed the Consumer Terms notice being skipped for a day or longer after a server error
- **[UNCOVERED]** - Fixed `/privacy-settings` offering choices that may not apply to you after a network or server error
- **[UNCOVERED]** - Fixed a "Context limit reached" or "Prompt is too long" error after stopping a turn while Claude Code was compacting a conversation the API had rejected as too long
- **[UNCOVERED]** - Fixed subagents sometimes forgetting their most recent work when they were messaged or resumed right after finishing
- **[UNCOVERED]** - Fixed `claude --help` text for `--tools`, `--resume`, `--debug`, `--json-schema`, `--disable-slash-commands`, `--system-prompt-snapshot` and `claude update` to match actual behavior
- **[UNCOVERED]** - Fixed `claude --worktree` removing the worktree and its branch without asking at exit when HEAD was detached or on another branch, which could lose commits
- **[UNCOVERED]** - Fixed resumed and cloud sessions sending Claude the whole skill list again each time plugins reloaded at startup
- **[UNCOVERED]** - Fixed an interrupt not ending a Read that waits on an idle pipe or device named like an image
- **[UNCOVERED]** - Fixed `/effort status`, `/effort ultracode` and the prompt's effort indicator showing a guessed effort level when `CLAUDE_CODE_EFFORT_LEVEL` is `auto` or `unset` and no level is sent
- **[UNCOVERED]** - Fixed a PreToolUse hook's deny reason being replaced by a timeout error when an Agent SDK callback hook on the same tool call timed out
- **[UNCOVERED]** - Fixed Bash and PowerShell deleting a large command's output file when it could not be copied to the session's tool-results folder, unless the disk is full
- **[UNCOVERED]** - Fixed notes typed into a multiple-choice question with previews being cut off with "…" in terminals under about 100 columns, hiding what was typed (anthropics/claude-code#82768)
- **[UNCOVERED]** - Fixed self-paced `/loop` wakeups scheduled at the 1-hour maximum firing just after the 1-hour prompt cache expired, so those wakeups no longer re-read the conversation uncached
- **[UNCOVERED]** - Fixed agent teams: approving a shutdown request from the main session no longer exits the whole CLI
- **[UNCOVERED]** - Fixed a skill's `once` hook also removing another skill's identical hook after it ran
- **[UNCOVERED]** - Fixed transcript mode's `{` and `}` landing the prompt on an inconsistent row, or off screen, instead of the transcript's first row
- **[UNCOVERED]** - Fixed `CLAUDE_CODE_AUTO_COMPACT_WINDOW=200k` silently setting a 100K window: the variable now accepts `k` and `M` suffixes like `--autocompact`, and warns when a value is out of range or ignored
- **[UNCOVERED]** - Fixed Ctrl+C in the agents view clearing a text selection without copying it when pressed before the mouse button was released
- **[UNCOVERED]** - Improved `/usage` to say when a rate limit on usage data ends instead of "try again in a moment"
- **[UNCOVERED]** - Improved the lines shown when a mod written in the session loads, reloads or fails to load
- **[UNCOVERED]** - Improved artifacts with several views: when you ask for links to them, Claude now writes out each view's link and explains that the address bar stays the same as you switch views
- **[UNCOVERED]** - Improved cloud sessions: a new conversation's first turn no longer waits for the local (stdio) MCP servers of plugins synced from claude.ai, unless a server sets `alwaysLoad: true`
- **[UNCOVERED]** - Improved how a remote session recovers its status when the server refuses a status update that carried other session data
- **[UNCOVERED]** - Improved session file size in auto mode: the safety classifier's context is no longer stored with every request
- **[UNCOVERED]** - Improved the `claude -p` invalid-settings warning: a file that did not load lists only what stopped it, and long lists are capped per file
- **[UNCOVERED]** - Improved resume of large compacted sessions in SDK and headless mode: the first request after resuming is sent sooner
- **[UNCOVERED]** - Improved responsiveness and throughput when many subagents are running at the same time
- **[UNCOVERED]** - Improved memory use when sending requests in long or resumed conversations
- **[UNCOVERED]** - Self-hosted runner: Improved the error shown when the git host answers "not found" for a session's repository: it now names the repository and whom to ask
- **[UNCOVERED]** - Windows: Improved git command start-up with a standard Git for Windows install by running its git.exe directly instead of through its cmd launcher
- **[UNCOVERED]** - Changed mods' `settings.read` hooks to receive each settings layer and rewrite the merged settings, so a managed mod can make an organization's setting a ceiling, including the `cleanupPeriodDays` the retention sweep uses
- **[UNCOVERED]** - Changed the `/artifacts` delete confirmation to show numbered choices: 1 or Enter keeps the artifact, 2 deletes it, and y, n and Esc still work
- **[UNCOVERED]** - Changed the question that turns on the mods Claude writes in a session to plain text with no link or session id; it stays up when a new turn starts, and Claude tells you what loaded when you turn them on
- **[UNCOVERED]** - Changed tool search to be on by default behind a custom `ANTHROPIC_BASE_URL`; a 400 or 422 from the gateway is retried without it
- **[UNCOVERED]** - Changed compaction to send Claude the skill list again afterwards; `/reload-skills` now sends only new or changed skills
- **[UNCOVERED]** - Changed skill hooks: the skills of one source (a repo, your own folder, or a plugin) can register at most 1,024 hooks and 16,384 matcher characters per session
- **[UNCOVERED]** - Changed skills under a policy that allows hooks from plugins only: a skill used in the main conversation whose hooks are kept out no longer gets its `allowed-tools`
- **[UNCOVERED]** - Updated the /claude-api skill to use the `ant` CLI on Claude Platform on AWS instead of falling back to the SDK or curl
- **[UNCOVERED]** - Removed the notes from `claude plugin validate` that predicted where a mod's hooks would run
- **[UNCOVERED]** - Removed the "(research preview)" label from the `/fast` dialog title on Opus 5.5
- **[UNCOVERED]** - [VSCode] Added mod drawing in the chat panel for sessions on Amazon Bedrock, Google Vertex AI and Microsoft Foundry, behind an LLM gateway, or with telemetry turned off
- **[UNCOVERED]** - [VSCode] Fixed one cause of sessions failing to start with "Subprocess initialization did not complete within 60000ms": time a SessionStart command hook spends running no longer counts toward the limit, up to 10 minutes in total
- **[UNCOVERED]** - [VSCode] Fixed a session closed while it was starting keeping its Claude Code process running until the start ended
- **[UNCOVERED]** - [VSCode] Fixed a mod's drawings disappearing from a long-open panel until the next turn on machines that also run an older Claude Code
- **[UNCOVERED]** - [VSCode] Fixed Past conversations hiding sessions when `claudeCode.claudeProcessWrapper` is set
- **[UNCOVERED]** - [VSCode] Changed background sub-agents to show as one status line under their Agent card instead of streaming every step into the chat; the full transcript stays in /tasks
- **[UNCOVERED]** - [Cloud sessions] Fixed folders in the composer's @ list showing no name in cloud sessions, where picking one added only a space instead of a mention
- **[UNCOVERED]** - [Claude Tag] Fixed Claude going silent in a thread when its channel becomes shared across Enterprise Grid workspaces mid-task; it now posts a one-time note to @-mention it in a new thread
- **[UNCOVERED]** - [Claude Tag] Fixed `@Claude !fork` typed outside a thread getting no visible reply; Claude now shows you a private note saying to run it from inside a thread
- **[UNCOVERED]** - [Code Review] Added review levels to Code Review: Owners choose Quick, Standard (the default), or Deep for the organization, and can give individual repositories their own level
- **[UNCOVERED]** - [Code Review] Added an option in Code Review admin settings to review every repository in a GitHub organization, including ones added later, without selecting them one by one
- **[UNCOVERED]** - [Code Review] Fixed pull requests opened within a minute or two of an admin turning on Code Review being silently skipped; they are now retried and reviewed

---
_Generated by `.github/scripts/changelog-compare.py`_
## Native Sources Monitor Report

Sources checked: **3**

### anthropic-blog

- Source: Anthropic Blog — announcements and product updates
- Entries fetched: 26
- New uncovered: 3

| Entry | Section | Description |
|-------|---------|-------------|
| Announcements | Anthropic Blog | Announcements |
| Preparing for the 2026 US midterms | Anthropic Blog | Preparing for the 2026 US midterms |
| Partnerships | Anthropic Blog | Partnerships |

### cc-issues-enhancement

- Source: CC GitHub Issues labeled 'enhancement'
- Entries fetched: 300
- New uncovered: 3

| Entry | Section | Description |
|-------|---------|-------------|
| [Feature Request] Alternative to Persona ID verification for | GitHub Issues (enhancement) | **Bug Description** Je suis en train de faire travail dans un cadre pedagogique  |
| Code tab: AskUserQuestion card is much narrower than the cha | GitHub Issues (enhancement) | Im Code-Tab der Desktop-App ist die Rückfrage-Kachel (AskUserQuestion) deutlich  |
| [Feature Request] Desktop Code tab: add filter/section to li | GitHub Issues (enhancement) | **Bug Description** Sugestao: filtro de sessoes arquivadas no app desktop (aba C |

### cc-discussions-feature-request

- Source: CC GitHub Discussions in feature-request category
- Entries fetched: 0
- New uncovered: 0

---
Total new uncovered entries: **6**

_Generated by `.github/scripts/native-sources-monitor.py`_
