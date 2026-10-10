# CC Changelog & Native Sources: New Uncovered Features Detected

## Changelog Monitor Report

Last scanned version: **2.1.283**
New versions detected: **6**

### New Versions Summary

| Version | Features | Covered | Uncovered |
|---------|----------|---------|-----------|
| 2.1.289 | 27 | 0 | 27 |
| 2.1.288 | 89 | 1 | 88 |
| 2.1.287 | 106 | 1 | 105 |
| 2.1.286 | 88 | 0 | 88 |
| 2.1.285 | 136 | 1 | 135 |
| 2.1.284 | 100 | 0 | 100 |

### Feature Coverage Details

#### v2.1.289 — released 2026-10-03

- **[UNCOVERED]** - Fixed a deny or ask rule on a nested part of a compound shell command not holding over a user-installed mod's approval on managed machines
- **[UNCOVERED]** - Fixed the terminal freezing on short code blocks with many unclosed `<script>` tags or deeply nested `${` substitutions
- **[UNCOVERED]** - Fixed `Read` deny rules not applying to files @-mentioned, changed, or selected in the IDE through a symlink
- **[UNCOVERED]** - [VSCode] Reverted a 2.1.288 change to `claude auth status` that may have made sign-outs more frequent
- **[UNCOVERED]** - Improved how quickly large files open in a plugin code pane by laying the highlighted view out once at its final width
- **[UNCOVERED]** - Fixed `plugin list`, `plugin eval` and `plugin update` showing a stale copy of a plugin installed from a local folder marketplace, and hot reload for a symlinked `--plugin-dir`
- **[UNCOVERED]** - Fixed installed mods not loading in the first session after an upgrade
- **[UNCOVERED]** - Fixed a plugin's rows above the prompt showing a stale row while the Background tasks dialog was open in fullscreen
- **[UNCOVERED]** - Fixed plugin panes drawing nothing when a link used a localhost address, an `@` in its path, an uppercase host or a `file:` path
- **[UNCOVERED]** - Fixed a user-installed plugin being able to rewrite the descriptions of an organization-managed MCP server's sign-in tools
- **[UNCOVERED]** - Fixed a freeze or forced quit at launch when a plugin drew a Box with a border style the terminal does not know
- **[UNCOVERED]** - Fixed supervised and background sessions ending when a plugin's on-screen handler threw asynchronously
- **[UNCOVERED]** - Fixed sessions ending with an interface error when a plugin region with no height kept growing
- **[UNCOVERED]** - Fixed Bash deny and ask rules missing a command behind an environment variable prefix with an expanded value (e.g. `TZ="$HOME" rm -rf build`) when the sandbox auto-allows commands
- **[UNCOVERED]** - Fixed a Bash deny or ask rule being skipped under sandbox auto-allow when a bare variable assignment came before the command
- **[UNCOVERED]** - Fixed `claude plugin validate` skipping the plugin when the folder also holds a marketplace manifest
- **[UNCOVERED]** - Added `agent.spawn` for teammates, one agent id across plugin hook events, and idle and waiting states in `$.agent.list()`
- **[UNCOVERED]** - Fixed sessions ending with "unrecoverable interface error" when a value a mod's `ui.render` hook wrote made a row throw while drawn; the engine now draws its own row instead
- **[UNCOVERED]** - Fixed text with a tab, a stray escape and a C1 control, or a short text with a tab and CRLF line endings, drawing over the rows below it
- **[UNCOVERED]** - Fixed right-aligned content in a mod's pane or band drawing under the close mark or `[-]`, which now also keep one column in from the terminal's edge
- **[UNCOVERED]** - Fixed a mod's `Client` that fails while drawn taking down everything the mod drew around it; it now fails alone and raises `ui.fault`
- **[UNCOVERED]** - Fixed `claude plugin validate` failing an Anthropic marketplace's own plugin and listing a clean `plugin.json` in `--json`
- **[UNCOVERED]** - Fixed a mod's band that fails to draw briefly telling the cards under it to step aside
- **[UNCOVERED]** - Fixed a failed plugin component showing `Error` or nothing as its reason when the failure carried no message
- **[UNCOVERED]** - Improved the line a mod's author sees when its band or pane fails to draw: it names the mod and says nothing was drawn
- **[UNCOVERED]** - Fixed published artifact pages freezing or crashing the reader's browser tab on short code blocks with many unclosed `<script>` tags
- **[UNCOVERED]** - Fixed a mod's Client region staying failed for the whole session after the terminal threw while drawing it

#### v2.1.288 — released 2026-10-02

- **[covered]** - Fixed `--resume` sometimes dropping files and other context that a compaction had just restored
  - Covered by: `cc-native/sessions/CC-session-lifecycle-analysis.md`
- **[UNCOVERED]** - Added `$.ui.selection()` for mods: returns the text you last selected in fullscreen mode and, when the selection lies within one transcript row, that row
- **[UNCOVERED]** - Added a built-in `gh api` to cloud sessions whose image has no GitHub CLI, and fixed the built-in sending control characters from file names, jq filters or GitHub errors to the terminal
- **[UNCOVERED]** - Added recovery for a prompt cleared with Ctrl+C: pressing Up on the empty prompt brings the draft back, including pasted text and images
- **[UNCOVERED]** - Added a re-authenticate prompt when an MCP server asks for more OAuth scope during a tool call
- **[UNCOVERED]** - Added `--max-findings <n>|all` to /code-review to report more or fewer findings than the usual limit; the choice is reused until you pass `--max-findings default`
- **[UNCOVERED]** - Added Ctrl+F to find a session by name and Alt+↑/↓ to jump between groups in the agents view; both, and rename, can be rebound in keybindings.json
- **[UNCOVERED]** - Added a screen reader mode announcement of the new permission mode when you approve a plan, including with Shift+Tab
- **[UNCOVERED]** - Fixed mid-response API timeouts failing the turn: non-interactive sessions and subagents now continue from the partial response, and thinking-only responses are retried
- **[UNCOVERED]** - Fixed long conversations failing with "Prompt is too long" instead of auto-compacting when the last reply reported zero token usage
- **[UNCOVERED]** - Fixed a resumed session sometimes not saving the last response of a turn, so that the next `--resume` showed the prompt unanswered
- **[UNCOVERED]** - Fixed resume occasionally loading a transcript cut short when the same session rewrote the file during the load
- **[UNCOVERED]** - Fixed resuming a conversation started on 2.1.286 or earlier dropping the model's earlier thinking
- **[UNCOVERED]** - Fixed session titles, memory recall and prompt hooks failing on Mantle or behind gateways that reject structured outputs; added `CLAUDE_CODE_DISABLE_STRUCTURED_OUTPUTS` to turn structured outputs off
- **[UNCOVERED]** - Fixed auto mode denials pointing Claude at a Bash permission rule when the blocked tool was not Bash
- **[UNCOVERED]** - Fixed auto mode on Bedrock and Mantle switching to the local classifier for the rest of the session after a request to an older model, such as a WebFetch summary or a `sonnet` subagent
- **[UNCOVERED]** - Fixed cloud sessions that restarted on a newly picked model replying with that model after the server refused it
- **[UNCOVERED]** - Fixed Cowork cloud sessions staying marked as waiting for input after a WebFetch permission prompt for an unapproved URL went unanswered for five minutes
- **[UNCOVERED]** - Fixed prompt suggestions not appearing on a phone that joins a Cowork cloud session started on another device
- **[UNCOVERED]** - Fixed a mod's button sometimes running a different button's action when pressed on a view drawn before Claude Code restarted
- **[UNCOVERED]** - Fixed a plugin's pane showing nothing when one `Code` element held a diff that does not parse; it now draws as plain code
- **[UNCOVERED]** - Fixed plugin LSP servers receiving literal `${user_config.*}` and `${CLAUDE_PLUGIN_ROOT}` placeholders in `initializationOptions` and `settings` instead of substituted values or manifest defaults
- **[UNCOVERED]** - Fixed a plugin's `tool.call` hook making Bash fail and file searches read the wrong folder in subagents that run in a worktree
- **[UNCOVERED]** - Fixed `git-subdir` plugin installs failing, or caching an incomplete plugin, on older git (before 2.39, e.g. Ubuntu 22.04's 2.34)
- **[UNCOVERED]** - Fixed plugins loaded with `--plugin-dir` not showing "Configure options" in `/plugin`
- **[UNCOVERED]** - Fixed background sessions ending when a plugin was reloaded or disabled while one of its timers or reads was still running
- **[UNCOVERED]** - Fixed sandboxed heredocs with an unquoted delimiter (`python3 <<EOF`) asking for approval on every run under sandbox auto-allow when the body holds only plain text and simple `$VAR` references
- **[UNCOVERED]** - Fixed Bash tool permission check to prompt before a `BASHPID` assignment whose value the shell would evaluate as arithmetic, instead of allowing it silently
- **[UNCOVERED]** - Fixed fullscreen sessions exiting with "unrecoverable interface error" when opening the background tasks dialog while a plugin or mod showed rows above the prompt
- **[UNCOVERED]** - Fixed Claude reporting a message to another session as delivered when that session held it: the notice now says it wasn't delivered and names the session, and in SDK sessions Claude can now learn of it mid-turn
- **[UNCOVERED]** - Fixed OpenTelemetry `claude_code.tool.blocked_on_user` spans reporting `unknown` source or decision in `-p` and SDK sessions and for PreToolUse hook approvals
- **[UNCOVERED]** - Fixed permission asks that ended unanswered, in `-p` or on an interrupted turn, emitting no `tool_decision` event
- **[UNCOVERED]** - Fixed Edit and Retry in Cowork cloud sessions refusing a message sent before `/compact` even though its history was still saved
- **[UNCOVERED]** - Fixed unattended sessions (`CLAUDE_CODE_RETRY_WATCHDOG`) retrying for hours after a very long response stream failed; Claude Code now streams again, and gives up after three timeouts
- **[UNCOVERED]** - Fixed `/login` reporting "Login successful" when credentials could not be saved to secure storage; it now shows the failure, and offers a retry when the new login didn't take effect (anthropics/claude-code#73861)
- **[UNCOVERED]** - Fixed a Stop during Bedrock credential lookup sometimes moving the session to a fallback model instead of ending the request
- **[UNCOVERED]** - Fixed a second `gcpAuthRefresh`/`awsAuthRefresh` browser sign-in opening when a laptop wakes from sleep while another Claude Code process is signing in
- **[UNCOVERED]** - Fixed agent teams: a plugin-defined agent spawned by name now runs with its own prompt, tools, disallowedTools and effort instead of the defaults
- **[UNCOVERED]** - Fixed headless (`-p` / SDK) sessions occasionally ignoring SIGTERM when a supervisor such as `timeout` or systemd sends SIGCONT alongside it
- **[UNCOVERED]** - Fixed restarted cloud sessions restoring a model that the organization's enforced model list refuses
- **[UNCOVERED]** - Fixed MCP tool calls sometimes running twice when a remote server's result was over 16 MB or could not be parsed
- **[UNCOVERED]** - Fixed subagents in Claude Desktop's Code tab getting none of the tools of a user-configured MCP server named `memory`
- **[UNCOVERED]** - Fixed Claude in Chrome asking before every screenshot and page read on a site you allowed when auto mode is unavailable (such as with `disableAutoMode` or an older model); typing, navigation and JavaScript still ask
- **[UNCOVERED]** - Fixed `claude plugin install` failing for GitHub-source plugins on macOS and Linux machines with no GitHub SSH key: the clone now falls back to HTTPS and prints a notice
- **[UNCOVERED]** - Fixed `sandbox.credentials.files` entries on git config files not taking effect while `permissions.blockReadsOutsideWorkingDirectories` is on
- **[UNCOVERED]** - Fixed Claude leaving out your organization's design systems when starting slides or a design with the Artifact tool on Team and Enterprise plans or machines with managed settings
- **[UNCOVERED]** - Fixed the keyboard not working on Windows after Claude Code restarts itself (first sign-in to a Claude apps gateway, provider setup, `/tui`)
- **[UNCOVERED]** - Fixed a stall when launching an agent whose `tools:` lists very many `Agent(...)` entries
- **[UNCOVERED]** - Fixed sessions on Claude 3 Opus and Claude 3 Sonnet failing on every turn after a whole PDF entered the conversation
- **[UNCOVERED]** - Fixed the npm auto-updater reporting success when the platform-native binary failed to download and only the placeholder `claude` stub was installed
- **[UNCOVERED]** - Fixed Remote Control cleanup archiving a session that is still connected or was just re-attached by another Claude Code process
- **[UNCOVERED]** - Fixed `owner/repo` plugin marketplaces showing only the second attempt's error when both the SSH and HTTPS fetch fail; both errors are now shown, with the transport tried first on top
- **[UNCOVERED]** - Fixed path-scoped `.claude/rules` and nested CLAUDE.md files not loading when Write or Edit creates or changes a file in their scope (previously only Read loaded them)
- **[UNCOVERED]** - Fixed a dangerous `rm` (such as one on `/` or the home directory) inside a `bash -c` or `sh -c` script running without a prompt in bypassPermissions mode or under a shell allow rule (anthropics/claude-code#96300)
- **[UNCOVERED]** - Fixed LSP tool calls hanging indefinitely when a language server uses dynamic capability registration or stops responding; requests now time out after 60s (per-server `requestTimeout`)
- **[UNCOVERED]** - Fixed `idle_prompt` notification hooks firing while background agents are still running (anthropics/claude-code#93672)
- **[UNCOVERED]** - Fixed PreToolUse and PermissionRequest hooks being skipped when matching them failed or the tool's input could not be serialized to JSON; the call is now blocked
- **[UNCOVERED]** - Fixed the first request in a fresh environment or after a model switch using the built-in output limit and auto-compact window, not the server's; that request may now wait up to 1.5 seconds
- **[UNCOVERED]** - Fixed the "What should Claude do instead?" hint showing on the Interrupted row after sending queued messages with ctrl+enter
- **[UNCOVERED]** - Fixed `/login` in a `--bare` session running a sign-in the session never reads, which could replace your saved login; it now says which credentials work
- **[UNCOVERED]** - Fixed the InstructionsLoaded hook omitting agent_id and agent_type when a subagent's file access loads a rule or nested CLAUDE.md; rules and nested CLAUDE.md files loaded on file access now also report effort
- **[UNCOVERED]** - Fixed the Agent tool in `claude mcp serve` always reporting no available agents and rejecting every subagent_type
- **[UNCOVERED]** - Fixed the terminal cursor not following the typed text in the fullscreen transcript viewer's search and in `/theme`'s custom color search
- **[UNCOVERED]** - Fixed `/permissions` in screen reader mode: typing a rule's number now picks it instead of opening the search box
- **[UNCOVERED]** - Improved auto mode: when a conversation grows too long for the client-side safety classifier to review, it is now compacted instead of prompting for, or failing, every tool call
- **[UNCOVERED]** - Improved screen reader mode: short announcements, such as a deleted word, now stay on screen until your next key press or until something above them on screen changes
- **[UNCOVERED]** - Improved screen reader mode: answered questions in question dialogs now say "answered" beside their box
- **[UNCOVERED]** - Improved the `/usage-credits` message shown to Team and Enterprise members whose organization has turned off usage credit requests
- **[UNCOVERED]** - Improved cloud sessions: a new conversation's first turn no longer waits for a stdio MCP server whose config sets `alwaysLoad: false`
- **[UNCOVERED]** - Improved "You should know" notes to say "we", "the main agent" or "you" depending on who was responsible for a decision
- **[UNCOVERED]** - Improved the error for an artifact database write refused at the database's size limit: it now states the limit and what frees space
- **[UNCOVERED]** - Improved Bash permission prompts to give a shorter reason when part of a command can't be checked before it runs
- **[UNCOVERED]** - Self-hosted runner: Improved the built-in `gh api`: a refused gh command now prints its `gh api` equivalent, `--paginate` follows every page of a repository's lists, and a nested `claude` no longer removes it
- **[UNCOVERED]** - Improved Remote Control's recovery from an expired server credential: sessions stay connected during renewal and are kept if it gives up after a server outage
- **[UNCOVERED]** - Changed the background command time limit to apply only in unattended sessions (`-p`, Agent SDK, CI, cloud); terminal, desktop app and VS Code sessions have no limit
- **[UNCOVERED]** - Changed the client-side auto mode classifier to ignore an `ANTHROPIC_DEFAULT_SONNET_MODEL` pin that names Claude Sonnet 5.5 or Opus 5.5 and use Claude Sonnet 5 instead
- **[UNCOVERED]** - Changed `claude project purge` to `claude purge`; the old name still works and prints a notice
- **[UNCOVERED]** - Changed the agents view `n:` filter (and Ctrl+F search) so Enter opens the session whose name matches best instead of the top row
- **[UNCOVERED]** - Changed `/autocompact` to save the auto-compact window per model, so each model keeps its own setting when you switch
- **[UNCOVERED]** - Changed MCP URL prompts from servers that can't report when you're done to wait for "I'm done, continue" before the tool call continues, so you can finish in the browser first
- **[UNCOVERED]** - [VSCode] Fixed a claude.ai connector staying on "Needs authentication" after you authorize it: the MCP servers dialog now offers Check connection
- **[UNCOVERED]** - [VSCode] Fixed the opt-in New Conversation shortcut (Cmd/Ctrl+N) starting a conversation in every visible Claude view instead of only the one you are in
- **[UNCOVERED]** - [VSCode] Fixed the chat view resuming the next saved session after you archive the one it shows; it now starts a new conversation instead
- **[UNCOVERED]** - [Cloud sessions] Fixed the Cloud sessions switch in Claude Code admin settings staying locked off while an unrelated security setting was loading or had failed to load
- **[UNCOVERED]** - [Cloud sessions] Fixed pressing Stop while a self-hosted runner was still starting not cancelling the queued message, which could then run once the runner was up
- **[UNCOVERED]** - [Claude Tag] Fixed Claude Tag admin settings offering a "Remove this scope" option, which always failed, on channels whose settings were created automatically
- **[UNCOVERED]** - [Claude Tag] Improved Claude to also follow a related Slack thread in another channel that it only read, so updates there reach the conversation that depends on them
- **[UNCOVERED]** - [Claude Tag] Improved save errors on a channel's Configure page: too-long channel instructions now say to shorten them, and a save refused for lost access no longer says to try again
- **[UNCOVERED]** - Fixed `claude plugin test` reporting mods as turned off remotely when it had only read an out-of-date saved setting

#### v2.1.287 — released 2026-10-01

- **[covered]** - Changed Opus 4.7+ and Fable to use a 1M context window by default on Bedrock, Vertex, Foundry and the Claude apps gateway, with no `[1m]` suffix (`CLAUDE_CODE_DISABLE_1M_CONTEXT=1` keeps 200K)
  - Covered by: `cc-native/configuration/CC-model-provider-configuration.md`
- **[UNCOVERED]** - Added Claude Mods: plugins may now modify deeper behavior
- **[UNCOVERED]** - Added You should know, a built-in mod where a side agent watches your back and flags things you or Claude might miss. Turn it on with `/plugin enable cc-plugin-you-should-know@builtin` (for first-party sessions with telemetry on)
- **[UNCOVERED]** - Added an `n:<text>` filter to the agents view that matches session names and tasks; a filter now shows matches in collapsed sections and Enter opens the first match
- **[UNCOVERED]** - Added `prompt_text` to the OpenTelemetry `user_prompt` event, a copy of `prompt` for backends that nest dotted keys; drop or mask it wherever you drop or mask `prompt` (anthropics/claude-code#70763)
- **[UNCOVERED]** - Added URL prompts from MCP servers on the 2025-11-25 protocol, for example to sign in. If a server no longer connects after this update, add "bareElicitationCapability": true to its MCP config entry
- **[UNCOVERED]** - Windows: Added a startup warning when denying the Bash tool also turns off the PowerShell tool, so Claude has no shell tool
- **[UNCOVERED]** - Self-hosted runner: Added a built-in `gh api` (REST only) for sessions that use Anthropic-managed git on macOS and Linux machines where the GitHub CLI is not installed
- **[UNCOVERED]** - Fixed fast mode staying off in remote sessions owned by an agent with no user account, even when the organization allows it
- **[UNCOVERED]** - Fixed Remote Control not receiving messages for minutes at a time when a reconnect request got no response; it now gives up after 30 seconds and retries
- **[UNCOVERED]** - Fixed hooks configured with `asyncRewake` waking Claude over and over with "found issues" notifications when the hook's script file is missing; the broken hook is now reported once
- **[UNCOVERED]** - Fixed tool heartbeats not reaching SDK hosts while the model's response stream was stalled with no data arriving
- **[UNCOVERED]** - Fixed Bedrock and Vertex startup model checks ignoring an enforced `availableModels` list, which could collapse `/model` to one Opus row
- **[UNCOVERED]** - Fixed the Claude in Chrome browser picker showing a JSON parse error when Chrome could not be reached
- **[UNCOVERED]** - Fixed picking Fable in `/model` on a claude.ai login saving the current version's id, so your saved default now follows the newest Fable like Opus and Sonnet do
- **[UNCOVERED]** - Fixed switching between Opus 5.5 and Sonnet 5.5 (`/model`, `opusplan`) rewriting earlier MCP tool announcements, which could drop earlier extended thinking
- **[UNCOVERED]** - Fixed Amazon Bedrock Guardrails blocks that arrive mid-response ending the turn with an API error instead of the guardrail's message when the reply began with thinking
- **[UNCOVERED]** - Fixed a dangerous `rm` (such as one on `/` or the home directory) losing its always-ask safeguard when the same command also redirected output to a `~` or wildcard path
- **[UNCOVERED]** - Fixed `claude -p` and SDK sessions repeating a model fallback on every later message after the model was switched while a reply was running
- **[UNCOVERED]** - Fixed a folder's CLAUDE.md being attached a second time after resuming a session or after a compaction
- **[UNCOVERED]** - Fixed background sessions that could not be reopened from `claude agents` after the agent exited and removed the worktree the session was started in
- **[UNCOVERED]** - Fixed `/advisor` pairing checks: Sonnet 5.5 can now advise Opus 4.7 and 4.8, and advisors the API would refuse are flagged up front instead of being silently dropped
- **[UNCOVERED]** - Fixed Bash permission prompts showing internal parser names such as "Contains simple_expansion" instead of a plain explanation
- **[UNCOVERED]** - Fixed a cause of fullscreen sessions on slow or busy machines exiting with "Claude Code exited after an unrecoverable interface error" while a scroll key was held in a long conversation
- **[UNCOVERED]** - Fixed organization per-tool permission ceilings being silently dropped for an MCP tool named `__proto__`
- **[UNCOVERED]** - Fixed Claude being told to page large MCP results saved as JSON with Read's offset and limit, which cannot split one long line
- **[UNCOVERED]** - Fixed the commit attribution reminder being delivered inside a tool result after a compaction
- **[UNCOVERED]** - Fixed screen reader mode leaving the cursor away from the typed text in search boxes (such as /resume and /permissions) and sign-in code fields
- **[UNCOVERED]** - Fixed screen reader mode refusing Enter with nothing typed on /rewind's summarize options, whose added context is optional
- **[UNCOVERED]** - Fixed screen reader mode showing a "Tab to amend" hint on approval prompts, where Tab does nothing
- **[UNCOVERED]** - Fixed screen reader mode listing arrow keys that do nothing in /permissions and /mcp, and saying "Select with numbers" in empty menus or while a search box has the keys
- **[UNCOVERED]** - Fixed screen reader mode leaving out the changed lines in file edit approval prompts and other diffs
- **[UNCOVERED]** - Fixed screen reader mode sending the `claude --teleport` progress screen, and an MCP form field while it is being checked, to the screen reader again on every spinner frame
- **[UNCOVERED]** - Fixed `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` not removing the structured-output format from session-title and prompt-hook requests, which Bedrock-backed gateways reject
- **[UNCOVERED]** - Fixed screen reader mode leaving out the top lines of a second approval prompt, a changed /config row or the rejected-plan line when the previous screen was taller than the terminal window
- **[UNCOVERED]** - Fixed `--include-partial-messages` sending a cut-short reply's `message_stop` late or never, so apps could show the reply as still in progress
- **[UNCOVERED]** - Fixed `claude agents` sometimes not showing the permission prompt a background session is waiting on
- **[UNCOVERED]** - Fixed `/ultrareview` giving advice about `.git/info/attributes` when the upload stops on a committed `.gitattributes` it cannot read, such as one saved as UTF-16
- **[UNCOVERED]** - Fixed `claude remote-control` failing to register behind an HTTP proxy with a misleading "Check your organization permissions" error (anthropics/claude-code#97352)
- **[UNCOVERED]** - Fixed sandboxed Bash commands on Linux inheriting an open handle on the Claude Code executable
- **[UNCOVERED]** - Fixed the running-tool dot and three spinners still moving with the "Reduce motion" setting on, and /rewind's confirm screen updating its "ago" time while you type a note
- **[UNCOVERED]** - Fixed times in `claude agents` changing every second in screen reader mode; they now change at most every 10 seconds
- **[UNCOVERED]** - Fixed a revoked claude.ai login showing a generic `API Error: 401` instead of "OAuth token revoked"; in `-p` mode the error now starts with "Failed to authenticate"
- **[UNCOVERED]** - Fixed `/ultrareview` upload refusals advising you to copy a variable named by a repository's settings file into your own user settings
- **[UNCOVERED]** - Fixed `--output-format stream-json` and the SDK not streaming the turns of a `context: fork` skill run by typing `/<skill>` as the prompt, as they do for the Skill tool's fork
- **[UNCOVERED]** - Fixed /feedback and /bug: the pre-filled GitHub issue no longer includes your recent error messages, and the confirmation screen now lists them as part of the report
- **[UNCOVERED]** - Fixed `claude plugin marketplace add --sparse` and `git-subdir` plugin installs failing with "transport 'http' not allowed" when the repository is served over plain http
- **[UNCOVERED]** - Fixed cloud sessions sometimes losing the earlier conversation when the session restarted while it was being compacted
- **[UNCOVERED]** - Fixed a plugin reload that overlapped the startup `--plugin-url` download corrupting the session's cached copy of the plugin archive
- **[UNCOVERED]** - Fixed `/desktop` quoting partial output when opening Claude Desktop timed out or printed too much output; the error now names the cause
- **[UNCOVERED]** - Fixed an MCP connector tool call occasionally running twice, or the connector's calls failing until restart, when its server changed which MCP protocol version it supports
- **[UNCOVERED]** - Fixed SessionStart hooks from synced plugins not running in new cloud sessions
- **[UNCOVERED]** - Fixed the transcript's "N hooks ran" summary and the verbose debug log's matched-hooks count including Claude Code's internal callbacks, so one configured hook no longer shows as two
- **[UNCOVERED]** - Fixed files Claude sends from cloud and Remote Control sessions failing when the upload finished just after the 30-second timeout; it now waits 35 seconds
- **[UNCOVERED]** - Fixed repositories added mid-session in cloud and SDK sessions not loading their skills and plugins, and loading CLAUDE.md late, after Claude changed directory
- **[UNCOVERED]** - Fixed PNG, JPEG and WebP images over 8,000 pixels on a side failing to send from a remote session; Claude now sends a scaled-down copy
- **[UNCOVERED]** - Fixed messages sent from the Claude apps with 17 to 20 attached files delivering only the first 16
- **[UNCOVERED]** - Fixed headless sessions reporting an MCP server as needing authentication after one refused call, even though later calls succeed
- **[UNCOVERED]** - macOS: Fixed Remote Control sessions started with `claude remote-control` stopping mid-turn when the Mac went to idle sleep
- **[UNCOVERED]** - Windows: Fixed interactive `claude` hanging or crashing with "Raw mode is not supported" when its input is piped or redirected; it now says why and exits (use `-p` for piped input)
- **[UNCOVERED]** - Bedrock, Vertex, Mantle: Fixed model availability checks under `CLAUDE_CODE_SKIP_*_AUTH` sending a different `Authorization` header than real requests when `ANTHROPIC_CUSTOM_HEADERS` repeats it
- **[UNCOVERED]** - Improved `/config`: settings that cycle show ‹ › and step both ways with ←/→, narrow terminals stack each value under its label, and PgUp/PgDn page the list
- **[UNCOVERED]** - Improved plugin marketplace errors to say in plain words why a marketplace was ignored or refused, and what to do
- **[UNCOVERED]** - Improved plugin listings to note when a plugin's dependencies were not installed, and updating a plugin now retries an install that did not finish
- **[UNCOVERED]** - Improved the Claude apps gateway's error when Amazon Bedrock rejects a model ID: developers now see which model is unavailable, and the gateway log names the ID that was sent
- **[UNCOVERED]** - Improved SDK sessions so a message sent with priority "now" no longer cancels a running web fetch or web search; it keeps loading in the background
- **[UNCOVERED]** - Improved `/memory`: the left and right arrow keys now flip its on/off settings, such as Auto-memory
- **[UNCOVERED]** - Improved `/skill` names typed mid-message: Claude is now told they are skills, including `disable-model-invocation` ones
- **[UNCOVERED]** - Improved the contrast of the prompt input border in light themes and of the ❯ before your earlier messages
- **[UNCOVERED]** - Improved delivery of files Claude sends from cloud sessions and Remote Control: an upload that fails on a timeout, a network error or a 502, 503 or 504 is now retried once
- **[UNCOVERED]** - Improved what Claude says when a file cannot be sent for a reason that may be temporary: it now mentions that you can ask for the file again in a few minutes
- **[UNCOVERED]** - Improved the prompt for a held message from another session to show the message between dashed lines, matching other permission prompts
- **[UNCOVERED]** - Improved MCP and other tool permission prompts to show the tool call between dashed lines, matching file edit prompts
- **[UNCOVERED]** - Improved MCP startup in headless mode: a remote server whose first connect fails transiently is now retried without waiting for the slowest server to finish connecting
- **[UNCOVERED]** - Improved files Claude sends from a remote session: large files now stream from disk instead of being read into memory, and a file over the size limit is refused with the server's limit named
- **[UNCOVERED]** - Improved the explanation Claude gives when the server refuses a file it sends from a Remote Control or cloud session, such as an oversized image
- **[UNCOVERED]** - Improved handling of large MCP tool results: less memory, smaller session files, and no extra upload to count tokens for results far over the limit
- **[UNCOVERED]** - Windows: Improved Bash tool speed by removing a subshell that ran before every command
- **[UNCOVERED]** - Changed a shell write through a repo-committed symlink onto a sensitive file or out of the working tree to name where it lands and wait for a person, on lines with a `~` target too
- **[UNCOVERED]** - Changed replies from `claude agents` to arrive as queued messages; slash commands other than `/stop` sent while a turn is running now run when it ends
- **[UNCOVERED]** - Changed whole-tool `Bash` allow rules and allowing hooks to prompt for, not run, shell writes to files Claude Code's file tools refuse outright (the Anthropic profile store, the host credentials file)
- **[UNCOVERED]** - Changed right-click paste on Windows and Linux, and middle-click paste on Linux, to happen when the button is released; moving the pointer away before releasing cancels it
- **[UNCOVERED]** - Changed MCP server `alwaysLoad: false` to defer all of that server's tools behind tool search
- **[UNCOVERED]** - Changed screen reader mode to write new or changed lines without first pausing with the cursor at the start of the line; set `CLAUDE_AX_PREPARK_MS=50` to restore the pause
- **[UNCOVERED]** - Changed automatic model switches after a flagged message to keep your current effort level instead of the new model's default
- **[UNCOVERED]** - Changed waiting permission prompts to show oldest first, so a new prompt no longer covers the one you're reading (prompts with a countdown still open on top)
- **[UNCOVERED]** - [VSCode] Added "Run in background" to a running command or sub-agent, to move it to the background and keep working
- **[UNCOVERED]** - [VSCode] Added the output of background shells and Monitors to their cards in the agent map
- **[UNCOVERED]** - [VSCode] Fixed settings dialogs blaming a timeout when Claude Code's reply was too large to confirm a save
- **[UNCOVERED]** - [VSCode] Fixed reopening a cloud session that the side bar already brought to this machine opening it again in a new tab; the side bar is shown instead
- **[UNCOVERED]** - [VSCode] Fixed the side bar's Web tab not listing cloud sessions started after the window loaded; a failed load now says "Remote server is not connected" instead of "No web sessions yet"
- **[UNCOVERED]** - [VSCode] Fixed a tab restored after a reload starting a second Claude process on a conversation the side bar already has open; it now shows the "still open somewhere else" notice
- **[UNCOVERED]** - [VSCode] Fixed tool-row file links, session-list links and two hints showing in plain text
- **[UNCOVERED]** - [VSCode] Fixed a background agent's still-running command showing as failed once the main turn ended
- **[UNCOVERED]** - [VSCode] Fixed a user's own `/usage` or `/context` command opening the extension's dialog instead of running when picked from the command menu
- **[UNCOVERED]** - [VSCode] Fixed file links in the plan preview tab doing nothing when clicked; they now open the file like links in chat replies
- **[UNCOVERED]** - [VSCode] Fixed opening a tool's input or output in an editor tab failing with "Timeout waiting after 1000ms" on remote hosts such as WSL when the tab is slow to appear
- **[UNCOVERED]** - [VSCode] Improved the Manage plugins dialog: a failed marketplace add, remove or refresh now says what went wrong
- **[UNCOVERED]** - [VSCode] Changed the Claude in Chrome "Enabled by default" switch to also connect the editor's own sessions, which still ask before browser actions
- **[UNCOVERED]** - [Cloud sessions] Fixed occasional failures to fetch from or push to GitHub when GitHub briefly refused a newly issued access token
- **[UNCOVERED]** - [Claude Tag] Fixed Claude posting a failure warning, such as a spend limit notice, in a Slack thread when a background event like GitHub activity woke it and nobody was waiting on a reply
- **[UNCOVERED]** - [Claude Tag] Fixed Claude Tag's spend limits page in admin settings leaving out recently created and private channels in organizations with many channels
- **[UNCOVERED]** - [Claude Tag] Improved Claude's task list in long Slack threads: background work no longer reposts it as a new message on its own, so people following the thread aren't notified
- **[UNCOVERED]** - [Code Review] Fixed finding comments and their "Why this was flagged" text stopping mid-sentence; they now end on a complete sentence
- **[UNCOVERED]** - [Code Review] Fixed Code Review skipping a pull request after a new push when its review had failed twice on the previous commit; it now reviews the latest commit
- **[UNCOVERED]** - [Code Review] Improved the failed-review card on a pull request whose conversation is locked: it now says the lock blocked the review and that nothing was posted or charged

#### v2.1.286 — released 2026-09-30

- **[UNCOVERED]** - Added a count such as "2 of 5" to the permission prompt when several permission requests stack up
- **[UNCOVERED]** - Added mouse support for the "N more" rows of lists in fullscreen mode: click one to jump to that end of the list, with hover and pressed states
- **[UNCOVERED]** - Fixed several Claude Code processes and IDE extensions each opening a login browser when gcpAuthRefresh or awsAuthRefresh credentials expire
- **[UNCOVERED]** - Fixed `claude --resume` and `--continue` sometimes losing every turn after a batch of parallel tool calls when the earlier session crashed or was killed
- **[UNCOVERED]** - Fixed API 400 errors after a tool or hook returned an object, number or boolean instead of text, including in resumed sessions
- **[UNCOVERED]** - Fixed cloud sessions with very large histories never waking up because the container was stopped while the transcript was still loading
- **[UNCOVERED]** - Fixed the Claude apps gateway's spend meter pricing 1-hour prompt cache writes at the cheaper 5-minute rate, and counting only the first model call's input tokens on streamed turns that run a server-side tool such as web search
- **[UNCOVERED]** - Fixed macOS sessions still showing "Not logged in" or "Login expired" after `/login` succeeds in another Claude Code window when a leftover `~/.claude/.credentials.json` exists
- **[UNCOVERED]** - Fixed every turn failing when the Anthropic API refuses the model your default or a model alias resolves to: Claude Code now retries once on the previous model of the same tier
- **[UNCOVERED]** - Fixed Remote Control sessions (including `claude remote-control`) staying connected after your organization's policy turns Remote Control off; they now disconnect with a notice
- **[UNCOVERED]** - Fixed refusal and `--fallback-model` retries failing when the fallback model can't run fast; they now run at standard speed, with a one-time notice in interactive sessions
- **[UNCOVERED]** - Fixed headless sessions repeating the "MCP servers require authentication" reminder after a successful re-authentication when the MCP discovery cache is enabled
- **[UNCOVERED]** - Fixed `claude auth status` reporting a Console sign-in's stored API key as `claude.ai`; it now reports `api_key`, and the VS Code extension treats that session as an API key session
- **[UNCOVERED]** - Fixed `/status` listing an Anthropic profile beside an API key as if both were in effect; the profile is now marked as not in use
- **[UNCOVERED]** - Fixed Claude not being told when a file attached to a message sent over Remote Control did not arrive, and a file sometimes getting only 10 seconds for its last download try
- **[UNCOVERED]** - Fixed a Remote Control message that arrived while Claude Code was exiting being marked delivered and then never answered; it now stays queued for the session's next run
- **[UNCOVERED]** - Fixed MCP error messages showing a credential's value when "Bearer" or "Basic" came before its key name
- **[UNCOVERED]** - Fixed percent-encoded Bearer tokens being only partly masked in error messages
- **[UNCOVERED]** - Fixed redacted logs and transcripts showing a secret whose key name has an invisible character inside, such as a zero-width space
- **[UNCOVERED]** - Fixed logs and transcripts showing part of a URL password that contains punctuation such as `)`, quotes, `]`, `&` or a second `@`, or that runs past a `/` to a bracketed host such as `[::1]` in an ssh URL
- **[UNCOVERED]** - Fixed the session transcript in the zip that `/feedback` saves to disk containing invalid JSON lines after secret redaction
- **[UNCOVERED]** - Fixed MCP connectors listing no tools for up to a day after their server dropped the older MCP handshake
- **[UNCOVERED]** - Fixed a repeat MCP sign-in request from Claude replacing the pending sign-in link, which could stop that link from working
- **[UNCOVERED]** - Fixed `/usage` not crediting an MCP server for a tool call made while that server was still connecting or had only just connected, such as right after a restart
- **[UNCOVERED]** - Fixed plugins enabled on claude.ai occasionally going missing from Claude Code for a session after a transient server error
- **[UNCOVERED]** - Fixed a message typed into a running subagent showing twice in its transcript after the subagent read it
- **[UNCOVERED]** - Fixed subagent hand-back messages showing a raw task id instead of the agent's name when the subagent had no registered name
- **[UNCOVERED]** - Fixed foreground subagents sometimes missing the task-tracking tools (TaskCreate/Get/Update/List, TodoWrite) in sessions that have them enabled
- **[UNCOVERED]** - Fixed subagents spawned with worktree isolation loading the project CLAUDE.md and its imports a second time from the worktree copy on their first file read
- **[UNCOVERED]** - Fixed Workflow tool subagents being restarted from their original prompt when a connection stalled for a few minutes mid-response
- **[UNCOVERED]** - Fixed `/compact`, `/clear`, and `/rewind` typed while viewing a background agent's or teammate's transcript silently acting on the main conversation: a dialog now names the target and asks first
- **[UNCOVERED]** - Fixed background jobs showing done while waiting for your approval
- **[UNCOVERED]** - Fixed the commit attribution reminder being re-sent inside tool output when a model fallback lasts only one turn
- **[UNCOVERED]** - Fixed a click on the space between words of a collapsed row (such as "Thought for 4s") highlighting the row without expanding it in fullscreen mode
- **[UNCOVERED]** - Fixed a row with no details, such as an action row with a long name, pushing every other row's details to the right in list screens
- **[UNCOVERED]** - Fixed files with very long names not reaching a cloud session when attached to it
- **[UNCOVERED]** - Fixed plugin errors for a marketplace Claude Code refuses to load: they now say why and how to fix it instead of "not found"
- **[UNCOVERED]** - Fixed `/plugin`'s Discover tab showing a marketplace name unquoted in its "Checking … for new plugins" line when its rows already show that name in quotes
- **[UNCOVERED]** - Improved commit guidance: when your project or user skills include one named `verify`, Claude is now told to run it right before committing, except for docs-only and tests-only commits
- **[UNCOVERED]** - Improved send now (ctrl+enter) in a subagent's view: it now moves the subagent's running command to the background so your message is read right away
- **[UNCOVERED]** - Improved replies from background agents to your messages so they no longer open with a separate recap of what you said
- **[UNCOVERED]** - Improved claude.ai artifact link reads: WebFetch now asks the same questions as the Artifact tool's read (no artifact prompt while the session's network access is on, one per artifact while it is off), and an auto-mode yes no longer counts where only you can answer
- **[UNCOVERED]** - Improved fetch, skill, file read, sandbox network, Claude in Chrome, workflow script and notebook edit permission prompts to match the look of file edit prompts
- **[UNCOVERED]** - Improved Bash, PowerShell and Monitor permission prompts to show the command between dashed lines, matching file edit prompts
- **[UNCOVERED]** - Improved list scrollbars in fullscreen mode: in most lists the bar no longer shifts as the "N more" rows come and go, and it now has ↑/↓ arrows you can click or hold to scroll
- **[UNCOVERED]** - Improved the external editor (Ctrl+G): editors that take a line number now open on the line your cursor is on in the prompt
- **[UNCOVERED]** - Improved slash command suggestion responsiveness while typing when many skills or plugin commands are installed; command descriptions now match by word prefix
- **[UNCOVERED]** - Improved the output style picker: it now opens on your current style instead of Default, with each style's description on the line under its name; number keys no longer pick a style
- **[UNCOVERED]** - Improved `/hooks`: the closing line of a hook's detail screen now says "this hook" instead of "it"
- **[UNCOVERED]** - Improved the model fallback notice and the autocompact-thrashing error to say when a fallback dropped the context window from 1M to 200K tokens
- **[UNCOVERED]** - Improved responsiveness of SDK and `-p` sessions when a host re-sends an MCP server enable for a server that is already connected
- **[UNCOVERED]** - Improved the protocol page a Claude apps gateway serves at `/protocol`: it now says not to reject unknown input and matches what Claude Code sends today
- **[UNCOVERED]** - Changed prompts sent while nothing is running or queued to show in the normal text color right away instead of gray
- **[UNCOVERED]** - Changed how failed API requests are retried: one limit now covers a whole model call, so with the default retry settings a failing call sends at most 14 requests
- **[UNCOVERED]** - Changed `--bare` to connect only the MCP servers named on the command line, send the model no system reminders, and start no background tasks; under `--bare`, a shell command that reaches its timeout now stops instead of moving to the background
- **[UNCOVERED]** - Changed the send-now key (ctrl+enter) to move a skill's own shell command to the background instead of ending it
- **[UNCOVERED]** - Changed the WebFetch error for a rate-limited domain safety check to tell Claude not to retry it in a loop
- **[UNCOVERED]** - Changed plugin installs to refuse npm sources that are git repositories or folders, and to install plugin dependencies only from registry packages
- **[UNCOVERED]** - Changed list screens (`/artifacts`, `/mcp`, `/skills`, `/hooks` and others) to always line up each row's details in one column after the names
- **[UNCOVERED]** - Changed the overflow rows of lists to read "↑ N more" / "↓ N more" instead of "N more above" / "N more below"
- **[UNCOVERED]** - Changed `/hooks` to open on one list of your configured hooks grouped by event, so viewing a hook takes one Enter instead of three
- **[UNCOVERED]** - Changed the theme picker to a scrolling list that fits your terminal instead of pushing the preview off screen; number keys no longer pick a theme
- **[UNCOVERED]** - Changed `/exit`'s Remove worktree to run after Claude Code stops the servers and shells it started there, which on Windows could keep the folder from being deleted
- **[UNCOVERED]** - Changed the `claude-api` skill's Managed Agents examples to create environments with limited networking
- **[UNCOVERED]** - Removed the browser link from `/ultrareview` and `claude ultrareview` output
- **[UNCOVERED]** - Windows: Fixed `claude --bg` and the agents view refusing a folder that `claude` already trusts when its trust record was saved with different letter case
- **[UNCOVERED]** - [VSCode] Added bookmarks: save Claude's responses and keep them in view in a Bookmarks side panel
- **[UNCOVERED]** - [VSCode] Added the questions Claude asks and your answers to the conversation: after you answer a question card, a Questions row shows each question with your picks
- **[UNCOVERED]** - [VSCode] Added option previews to question cards in the chat panel: the highlighted choice's mockup or snippet shows beside or under the options
- **[UNCOVERED]** - [VSCode] Added rows under a message that open to the terminal output, browser tab, browser instructions and selected code sent with it
- **[UNCOVERED]** - [VSCode] Fixed a second copy of a conversation opening in a tab when it was already open in the side bar; the side bar now switches to it
- **[UNCOVERED]** - [VSCode] Fixed settings dialogs reporting a failed save, without re-checking, when Claude Code printed more than 1 MB of output
- **[UNCOVERED]** - [VSCode] Fixed an endless "Teleporting session…" spinner when the extension stops responding
- **[UNCOVERED]** - [VSCode] Improved the Manage plugins dialog: it says when a turned-off plugin is still on because of other settings, and explains a plugin folder clash
- **[UNCOVERED]** - [VSCode] Changed Stop and Escape to end only the current turn; background agents keep running and can be stopped one by one from the agent map
- **[UNCOVERED]** - [VSCode] Changed the "✻ Claude Code" status bar item to show in every window, so you can open Claude when no file is open
- **[UNCOVERED]** - [Cloud sessions] Fixed an answered question card or approved tool call getting no reply when the session had gone idle after Claude sent a message
- **[UNCOVERED]** - [Cloud sessions] Fixed clearing an organization environment's setup script in admin settings leaving new cloud sessions still running the old script
- **[UNCOVERED]** - [Cloud sessions] Fixed the Runner actions menu on the self-hosted environments admin page closing on its own a few seconds after it opened
- **[UNCOVERED]** - [Cloud sessions] Fixed routine runs whose cloud session never started showing as Succeeded in the Runs pane, the routine's page and the sidebar; they now show as Failed
- **[UNCOVERED]** - [Cloud sessions] Fixed clicking an audio or video file in a cloud session's Outputs card opening an empty file search instead of playing the file
- **[UNCOVERED]** - [Cloud sessions] Changed a routine's page to read "Due" with the scheduled time, instead of a next run time in the past, when a scheduled run is late and hasn't started
- **[UNCOVERED]** - [Claude Tag] Added an Add channel button to Claude Tag's spend limits page in admin settings, so a limit can be set on any channel, including a private one, from its channel ID or Slack link
- **[UNCOVERED]** - [Claude Tag] Fixed memory recall finding nothing in organizations that cannot use the default Sonnet model
- **[UNCOVERED]** - [Claude Tag] Fixed a Slack channel losing its Claude settings when an Enterprise Grid admin moves it to another workspace and the first post afterward doesn't mention Claude
- **[UNCOVERED]** - [Claude Tag] Fixed Claude in a Slack thread occasionally starting over on a fresh machine, losing work it hadn't pushed, when your reply answered a question it had just asked
- **[UNCOVERED]** - [Claude Tag] Fixed public channel names on Claude Tag's spend limits page in admin settings showing as raw Slack IDs in larger organizations
- **[UNCOVERED]** - [Claude Tag] Improved the titles of sessions started from Slack as shown on claude.ai: they now read as the words you typed, without Slack user IDs or escape codes

#### v2.1.285 — released 2026-09-29

- **[covered]** - [VSCode] Fixed the editor tab keeping an old name after a session was renamed with /rename, by a SessionStart hook, or on claude.ai
  - Covered by: `cc-native/sessions/CC-session-lifecycle-analysis.md`
- **[UNCOVERED]** - Added `CLAUDE_CODE_DISABLE_WEB_FETCH` environment variable to turn off the WebFetch tool
- **[UNCOVERED]** - Added `claude --desktop` to open the Claude desktop app on the current directory, or on a session with `--continue` / `--resume <id>`
- **[UNCOVERED]** - Added `claude plugin configure <plugin>` to show a plugin's options and which are unset, or save new values read from stdin with `--values-stdin`
- **[UNCOVERED]** - Added `<server>.<key>=<value>` to `claude plugin install --config`, so a bundled `.mcpb` MCP server's own settings can be set at install time and it starts without visiting `/plugin` → Configure
- **[UNCOVERED]** - Added `allowedProviders` managed setting to limit which API providers a machine may use (Anthropic API, a custom endpoint, Bedrock, Mantle, Vertex AI, Foundry, Claude Platform on AWS, or a Cloud gateway)
- **[UNCOVERED]** - Added `CLAUDE_CODE_NONSTREAMING_TIMEOUT_RETRIES` environment variable to cap re-sends of a non-streaming fallback request that timed out
- **[UNCOVERED]** - Fixed `claude -p` with `CLAUDE_CODE_FORK_SUBAGENT=1`: a subagent's own Agent call now runs in the foreground, so the subagent gets the child's result
- **[UNCOVERED]** - Fixed plugin and marketplace installs and updates over SSH ignoring the ssh program set in `GIT_SSH` or in your git config's `core.sshCommand`
- **[UNCOVERED]** - Fixed Claude Code refusing to start when the OS denies reading the managed settings file; it now warns and starts without that file's policies. Other read errors and unparseable files stop every session
- **[UNCOVERED]** - Fixed cloud sessions that restarted after their conversation was compacted refusing the next update to an artifact the session had already read or published
- **[UNCOVERED]** - Fixed `claude plugin disable` and `enable` with a full `name@marketplace` id changing a settings entry in another letter case instead of the installed plugin's own
- **[UNCOVERED]** - Fixed files attached to a message sent over Remote Control being left out after a single failed download; a network error, timeout or server error is now retried up to twice
- **[UNCOVERED]** - Fixed switching models mid-session with a `set_model` request (such as the Agent SDK's `setModel`) leaving the new model on the built-in output-token limit and auto-compact window until restart
- **[UNCOVERED]** - Fixed redacted logs and transcripts showing part of a URL password that contains `@`, or all of it when the URL writes its `@` as `%40`
- **[UNCOVERED]** - Fixed SSH passphrase and new-host prompts from worktree and `/teleport` fetches taking over the terminal; these fetches now fail fast instead of asking
- **[UNCOVERED]** - Fixed switching off an MCP server added mid-session in SDK and `-p` sessions leaving its tools available
- **[UNCOVERED]** - Fixed `claude -p --permission-prompt-tool`: a background subagent's permission request now goes to the prompt tool instead of being auto-denied
- **[UNCOVERED]** - Fixed `claude mcp list` and `claude mcp get`, and the not-found error of `claude mcp remove`, `login` and `logout`, printing line breaks and terminal escape sequences from MCP server names and values
- **[UNCOVERED]** - Fixed sandbox auto-allow asking for approval on every run of many inline scripts (`python3 -c`, `node -e`) just because they contain `=`
- **[UNCOVERED]** - Fixed fork subagents not keeping the session's plan mode or `dontAsk` mode: a fork now runs under its parent's permission mode and cannot exit plan mode
- **[UNCOVERED]** - Fixed `claude remote-control --help` saying `--[no-]chrome` defaults to the machine's `/chrome` setting; spawned sessions keep Claude in Chrome off unless `--chrome` is passed
- **[UNCOVERED]** - Fixed background subagents in auto mode prompting a second, redundant reply after each report
- **[UNCOVERED]** - Fixed cloud session creation and `/remote-env` reading only the newest 20 of an account's environments
- **[UNCOVERED]** - Fixed Remote Control marking a message as read as soon as it arrived instead of when Claude started on it, and losing a message still queued when the terminal quit (it now arrives on the next resume)
- **[UNCOVERED]** - Fixed installing a plugin with `claude plugin install` or `/plugin` putting it into an installed plugin's cache or data folder when their ids differ only in `.`, `-`, `@` or (macOS, Windows) capitals; the install is now refused
- **[UNCOVERED]** - Fixed hooks and SDK permission callbacks seeing a missing or outdated plan on ExitPlanMode when the plan was written in the same response
- **[UNCOVERED]** - Fixed the first reply in cloud sessions arriving tens of milliseconds late, a regression in 2.1.283
- **[UNCOVERED]** - Fixed sessions that authenticate with `ANTHROPIC_AUTH_TOKEN` against the Anthropic API never loading the organization's policy
- **[UNCOVERED]** - Fixed a failed `agent()`, `parallel()` or `pipeline()` call that a workflow script awaits later, or not at all, being treated as an unhandled promise rejection, which could end a background session
- **[UNCOVERED]** - Fixed synchronous hooks hanging Claude Code while a background process the hook started (for example `some-daemon &`) kept its output open; the hook now finishes shortly after its own process exits
- **[UNCOVERED]** - Fixed WebFetch reporting a rate-limited domain safety check as a network or enterprise policy block
- **[UNCOVERED]** - Fixed the fullscreen ctrl+o transcript freezing briefly when opened on turns with hundreds of file reads or searches; tool calls still running when the transcript opens now show their results when they finish
- **[UNCOVERED]** - Fixed Amazon Bedrock mid-stream `modelTimeoutException` and `serviceUnavailableException` errors showing a raw JSON body instead of the error message
- **[UNCOVERED]** - Fixed `/autofix-pr` and `/schedule` saying the Claude GitHub App is not installed on a repository whose install status had not been checked yet
- **[UNCOVERED]** - Fixed dismissing a row (x) in `/artifacts` unlinking its file from the artifact, so publishing the same file again created a new artifact instead of updating it
- **[UNCOVERED]** - Fixed Artifact tool publishes after a conversation rewind (Esc Esc) overwriting a file's newer content that Claude had read only in the rewound turns; the publish is now refused until Claude re-reads the file
- **[UNCOVERED]** - Fixed an `Artifact` allow rule ("don't ask again") letting the Artifact tool publish a file outside the working directories without asking; add the file's folder with `--add-dir` for the rule to cover it
- **[UNCOVERED]** - Fixed `/cost` and SDK `modelUsage` reporting a turn under the wrong model when the server answered a refusal with a different fallback model than the client expected
- **[UNCOVERED]** - Fixed the Artifact tool so that publishing a page no longer lets Claude overwrite its source file without re-reading it when Claude's earlier read was cut short or the file had changed since
- **[UNCOVERED]** - Fixed auto mode skipping its classifier for Artifact tool asset uploads and reads of someone else's artifact when you had approved that artifact earlier in another permission mode
- **[UNCOVERED]** - Fixed a misleading "core.worktree is set" error from `/ultrareview` when the project folder briefly could not be read
- **[UNCOVERED]** - Fixed `/ultrareview` on macOS and Linux failing to upload the working tree from a git worktree whose per-worktree config sets `core.longpaths`
- **[UNCOVERED]** - Fixed the Artifact tool sometimes reporting a publish as a conflict with another session after retrying a temporary server error, when the first attempt had actually succeeded
- **[UNCOVERED]** - Fixed `/ultrareview` uploads including uncommitted changes to credential files whose name has a colon before the extension, such as `server:8443.key`
- **[UNCOVERED]** - Fixed a rare auth failure when two sessions recover a login refresh lock left by a crashed process at the same time
- **[UNCOVERED]** - Fixed the PowerShell tool's permission check skipping deny and ask rules, and caching that failure for later checks, when its command parser failed to start (for example when the machine was out of memory)
- **[UNCOVERED]** - Fixed `/ultrareview` uploads on macOS and Linux running slowly on some unusual file names, and their credential-file check missing file or folder names with many backup or editor marks
- **[UNCOVERED]** - Fixed a cancelled shell command or hook still starting, and running to its end, when the cancel arrived while it was being set up
- **[UNCOVERED]** - Fixed vim mode: after editing in the external editor (Ctrl+G), `x` or `r` in NORMAL mode no longer breaks a pasted-text placeholder at the end of the prompt
- **[UNCOVERED]** - Fixed responses blocked by the API's output content filter being re-sent and retried, sometimes for minutes, instead of showing the filter's error right away
- **[UNCOVERED]** - Fixed plugins silently skipping a bundled `.mcpb` MCP server that still needs configuration: `/plugin`, the install message and `claude plugin install` now say so and point to Configure
- **[UNCOVERED]** - Fixed compacting or resuming a session failing, opening without its history, or crashing when its saved transcript holds a compaction marker or loop wakeup entry with missing or malformed fields
- **[UNCOVERED]** - WSL: Fixed `/ultrareview` refusing to upload a checkout on a Linux volume when a changed file's name has a colon or ends in a dot or space
- **[UNCOVERED]** - Fixed `CLAUDE_CODE_RESUME_INTERRUPTED_TURN` re-running a turn that had ended at `--max-turns`
- **[UNCOVERED]** - Fixed sign-in that could wait forever after the browser showed success
- **[UNCOVERED]** - Windows: Fixed `/ultrareview` uploading a linked worktree of a repository rooted at your home folder in some cases
- **[UNCOVERED]** - Fixed cloud sessions reporting the uploads folder as missing before any file had been uploaded
- **[UNCOVERED]** - Fixed a reply sent from `claude agents` to a background session waiting on a permission prompt sometimes approving the pending command
- **[UNCOVERED]** - Fixed `claude attach`, `logs`, `stop`, `respawn` and `rm` starting a new session with the command name as its prompt when options came before it, such as from a shell alias
- **[UNCOVERED]** - Fixed `claude mcp list` leaving out WebSocket (`ws`) MCP servers; each is now listed with its URL and health status
- **[UNCOVERED]** - Fixed `claude mcp get` showing no Type, Command, Args, or Environment for stdio servers whose config entry omits the `type` field
- **[UNCOVERED]** - Fixed `.claude/settings.local.json` allow rules being held back outside a git repository when git's trace2 output is configured
- **[UNCOVERED]** - Fixed the `/claude-api` eval runner scaffold and report builder writing through a symlink or hard link planted at an output file
- **[UNCOVERED]** - Fixed the `/claude-api` eval runner scaffold counting responses cut off at `max_tokens` in the score averages; they are now marked truncated and counted separately
- **[UNCOVERED]** - Fixed `&nbsp;` showing as literal text in the terminal when a reply uses it to indent text, such as row labels in a markdown table
- **[UNCOVERED]** - Fixed a brief freeze (up to a second) partway through long sessions outside fullscreen mode, which came back after `/clear` or `/compact`
- **[UNCOVERED]** - Fixed an approved Edit never going through when its target is a device, such as a file symlinked to /dev/null, and the approval came from the IDE diff view or changed the edit
- **[UNCOVERED]** - Fixed a failing API request being retried up to 21 times when streaming kept failing; the non-streaming fallback now shares the request's retry budget instead of getting a fresh set of retries
- **[UNCOVERED]** - Improved Claude in Chrome: the native host now reports your computer's name, so connected browsers can be labeled by computer instead of "Browser 1" / "Browser 2"
- **[UNCOVERED]** - Improved Bedrock and Vertex AI sessions to switch to an older available model of the same tier, instead of failing, when an admin removes access to the default model; session titles and summaries now fall back with it
- **[UNCOVERED]** - Improved plugin marketplace errors to name why a git address is refused instead of citing enterprise policy
- **[UNCOVERED]** - Improved validation of git URLs for plugins, marketplaces and the current repository's remote
- **[UNCOVERED]** - Improved Artifact tool results: they now suggest publishing in the same step as writing or editing the page, which can save a round trip
- **[UNCOVERED]** - Improved Remote Control: a `/btw` side question asked of a session hosted by an app such as Claude Desktop now sees the turn in progress, not only the last finished one
- **[UNCOVERED]** - Improved pictures Claude sends as BMP, HEIC, HEIF, AVIF or TIFF files: the Claude apps now show a preview where Claude Code can convert them
- **[UNCOVERED]** - Improved subagents in auto mode: a subagent's run now ends as soon as it hands its report back to its caller, instead of taking extra turns that reach no one
- **[UNCOVERED]** - Improved Bedrock and Vertex start-up model checks: models your account cannot use are now remembered for up to a day instead of being re-checked on every launch
- **[UNCOVERED]** - Improved Artifact tool publish results to use fewer tokens: the note on updating an artifact is shorter, and where to find your artifacts is no longer repeated after every publish
- **[UNCOVERED]** - Improved SDK liveness during a non-streaming fallback request: with partial messages on, a `ping` stream event is now sent every 30 seconds on the Anthropic API, Claude Platform on AWS and gateways
- **[UNCOVERED]** - Improved `/resume` and `claude --resume` on a session that is running in the background: they now open that session instead of refusing, and a prompt given with `claude --resume <id> "prompt"` is sent to it as its next turn
- **[UNCOVERED]** - Improved per-turn performance when many permission deny rules and MCP tools are configured
- **[UNCOVERED]** - Improved responsiveness when leaving the ctrl+o transcript view in long sessions when fullscreen rendering is off
- **[UNCOVERED]** - Improved Bedrock, Vertex and Mantle start-up model checks to send the same User-Agent, x-app and session ID headers as regular requests
- **[UNCOVERED]** - Changed MCP tools so a tool that sets its own `_meta['anthropic/alwaysLoad']` to false stays deferred when its `--mcp-config`, Agent SDK or plugin server is set to `alwaysLoad`
- **[UNCOVERED]** - Changed background Bash and PowerShell commands to stop after a time limit (their `timeout` with `run_in_background`, default 30 min, max 2 h); Claude is notified when one is stopped
- **[UNCOVERED]** - Changed Code Review's pull request reviews and `/ultrareview` to run when `disableWorkflows` is on, unless the machine running the review has it set by its own administrator (MDM or the managed-settings file)
- **[UNCOVERED]** - Changed sessions behind a custom `ANTHROPIC_BASE_URL` to use the 1M context window of models that have one (Opus 4.7+, Sonnet 5+, Fable); run `/autocompact 200k` if your gateway stops at 200K
- **[UNCOVERED]** - Changed Team and Enterprise sessions, and sessions whose sign-in plan Claude Code can't determine, to withhold WebFetch until the organization policy loads if it couldn't be loaded at startup
- **[UNCOVERED]** - Changed /memory so that Auto-memory can no longer be turned on from a background session or from a session one of Claude Code's own tools started; turning it off there still works
- **[UNCOVERED]** - Changed the one-time offer to make auto mode your default permission mode to also show on third-party providers and with telemetry off, when your user settings default to another mode
- **[UNCOVERED]** - Changed `claude -p` and Python Agent SDK sessions on third-party providers or with telemetry off to start in auto mode when no permission mode is configured, like interactive sessions; `--permission-mode` still overrides it
- **[UNCOVERED]** - Changed Bedrock, Mantle and Claude Platform on AWS requests to a base URL with a non-default port to include the port in the SigV4-signed Host header
- **[UNCOVERED]** - Changed the MCP server name `widgets` to be reserved in cloud sessions and on self-hosted runners: your own server under it, or a close spelling such as `widgets_`, no longer loads, so rename it
- **[UNCOVERED]** - Changed `/ultrareview` on macOS and Linux to leave symbolic refs out when uploading a local checkout; a checkout whose current branch is a symbolic ref is now refused with an explanation
- **[UNCOVERED]** - Windows: Changed project and local settings `env` to no longer set `ALLUSERSPROFILE`, `SystemDrive`, or the `CommonProgramFiles` variables; set them in user or managed settings instead
- **[UNCOVERED]** - Changed `/tasks` to fold background work Claude Code runs for itself under one "System tasks" row; press Enter on it to show those tasks
- **[UNCOVERED]** - Changed `/ultrareview` on macOS and Linux to require git 2.31 or newer to upload a local repository; checkouts made with `--separate-git-dir` are now refused instead of being uploaded with an older method
- **[UNCOVERED]** - Changed `/ultrareview` uploads on macOS and Linux to send a partial clone as a working-tree snapshot on git 2.31 or newer, instead of falling back or refusing when git's version looked too old
- **[UNCOVERED]** - Changed `/ultrareview` uploads on macOS and Linux to refuse, instead of fetching, a partial clone missing some of its working tree's files on older git versions; a clone made without `--filter` uploads
- **[UNCOVERED]** - Changed Bedrock, Vertex and Mantle start-up model checks to identify themselves as Claude Code, like other Claude Code requests
- **[UNCOVERED]** - Changed `claude mcp get` to hide the command, arguments, and environment values of stdio MCP servers provided by plugins; variable names are still shown
- **[UNCOVERED]** - Changed `/claude-api` so it can no longer be run from Remote Control clients
- **[UNCOVERED]** - Changed `/config chrome=true` to direct you to the /config panel instead of enabling Claude in Chrome by default; `/config chrome=false` still turns it off when it was on
- **[UNCOVERED]** - Changed sandbox settings so project settings cannot widen or turn off an admin-required sandbox, replace the proxy behind a managed deny list, extend a strict allowlist, or reopen managed read-denies
- **[UNCOVERED]** - [VSCode] Added a note under a restored tab's last message when a window reload interrupted it and no reply will follow
- **[UNCOVERED]** - [VSCode] Added a plugin options form to Manage plugins: installing a plugin that has options asks for the unset ones, and a gear on its row changes them later
- **[UNCOVERED]** - [VSCode] Added an on-demand diagnostics tool so Claude in the panel can read the Problems panel's current errors and warnings at any time, not only right after it edits a file
- **[UNCOVERED]** - [VSCode] Fixed pressing Enter after typing a slash command running an unrelated menu item picked by fuzzy match, or doing nothing
- **[UNCOVERED]** - [VSCode] Fixed an open agent transcript losing the agent's newer messages during a long session
- **[UNCOVERED]** - [VSCode] Fixed a message that quotes a Claude Code or IDE tag losing the rest of its text in the chat
- **[UNCOVERED]** - [VSCode] Fixed a message sent while Claude was working disappearing from the conversation after the session was reopened
- **[UNCOVERED]** - [VSCode] Fixed the session list's Web tab showing the previous account's sessions after an account switch
- **[UNCOVERED]** - [VSCode] Fixed restored tabs re-running an interrupted turn when VS Code was started with `CLAUDE_CODE_RESUME_INTERRUPTED_TURN` set, even with Continue After Reload off
- **[UNCOVERED]** - [VSCode] Fixed Escape stopping the running turn instead of closing the command menu after clicking one of its rows
- **[UNCOVERED]** - [VSCode] Fixed opening Past conversations replacing a live conversation with its saved copy
- **[UNCOVERED]** - [VSCode] Fixed a Claude tab reloaded after an extension restart staying blank instead of saying how to recover
- **[UNCOVERED]** - [VSCode] Fixed opening a conversation that is already open in another window or app starting a second copy of it without warning; it now asks first
- **[UNCOVERED]** - [VSCode] Fixed a hook's reason for blocking or stopping a prompt disappearing after a window reload
- **[UNCOVERED]** - [VSCode] Fixed tabs stuck on a conversation that can't be resumed: the error now says so and offers to start a new conversation
- **[UNCOVERED]** - [VSCode] Fixed every file Read, Write and Edit stalling for ten minutes and then being skipped when the editor stops responding to the extension's automatic save before the tool runs
- **[UNCOVERED]** - [VSCode] Fixed the agent map labeling a sub-agent with the session's model instead of the model it actually ran on (e.g. under `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` or an agent's own `model`)
- **[UNCOVERED]** - [VSCode] Fixed uninstalling a plugin from the Manage plugins dialog, which removed the wrong installation or failed for a plugin installed for the project
- **[UNCOVERED]** - [VSCode] Fixed sign-in staying on the authorization-code step after going back and choosing the same sign-in method again
- **[UNCOVERED]** - [VSCode] Fixed the chat panel stalling when a long session trims its oldest rows
- **[UNCOVERED]** - [VSCode] Fixed the conversation disappearing from a session when many agents run
- **[UNCOVERED]** - [VSCode] Fixed the agent map's transcript view leaving out messages sent to a running agent
- **[UNCOVERED]** - [VSCode] Improved the Manage plugins dialog: a failed plugin action now opens a popup that explains it and, where there is one, offers the fix
- **[UNCOVERED]** - [VSCode] Changed the Manage plugins dialog to ask before removing a marketplace or turning off a plugin that your project's shared `.claude/settings.json` turns on
- **[UNCOVERED]** - [Cloud sessions] Fixed Run now on a routine showing internal error text when the run is refused before it starts; it now shows the same explanation as the routine's failure notification
- **[UNCOVERED]** - [Cloud sessions] Changed `MCP_DISCOVERY_CACHE=1`, when set in your cloud environment's variables rather than a settings file, to reuse your connectors' tool lists after a session restart; other MCP servers are no longer cached and connect at startup
- **[UNCOVERED]** - [Claude Tag] Added direct messages with Claude for members on an Enterprise plan Standard or Usage-Based Chat seat who also have Cowork; a seat that includes Claude Code is no longer required
- **[UNCOVERED]** - [Claude Tag] Fixed the Default model setting in admin settings and a channel's Configure page offering models your organization can't use, which made saves or new sessions fail
- **[UNCOVERED]** - [Claude Tag] Fixed the note under Claude's Slack messages saying it answered on a fallback model, and why, disappearing when Claude later edited that message
- **[UNCOVERED]** - [Code Review] Fixed the organization menu in Code Review's "Add a repository" dialog showing only a few of your GitHub organizations; it now loads more as you scroll
- **[UNCOVERED]** - [Code Review] Improved the Code Review check run to say when your repository's REVIEW.md wasn't applied, for example on a very large pull request or when REVIEW.md is a symbolic link

#### v2.1.284 — released 2026-09-28

- **[UNCOVERED]** - Added Claude Sonnet 5.5 (`claude-sonnet-5-5`), now the default Sonnet model on the Anthropic API — 1M context, $2/$10 per Mtok with $0.20/Mtok cache reads
- **[UNCOVERED]** - Added a "Yes, but ask again next time" answer to auto mode's prompt before a read outside the working directories, so you can allow that one read and still be asked about later ones
- **[UNCOVERED]** - Added dollar amounts to the Claude apps gateway spend limit in `/usage` and the status line (for example "$271.40 / $500.00 spent this month") when the gateway runs this version or later; the status line's `rate_limits.spend_limit` also gains `used_usd`, `limit_usd` and `period`
- **[UNCOVERED]** - Added `effortSlider:decreaseEffort`, `increaseEffort` and `toggleUltracode` keybinding actions, so the `/effort` slider's arrow and Tab keys can be rebound in `keybindings.json`
- **[UNCOVERED]** - Added `/rate-limit-options` to `/help` and the command menu for claude.ai subscribers, so the usage-limit notices that mention it point to a command you can find
- **[UNCOVERED]** - Added `/mcp reconnect all` in the interactive terminal to retry every MCP server that failed to connect or needs authentication at once
- **[UNCOVERED]** - Added Claude apps gateway startup warnings when a managed policy's `availableModels` is empty, or leaves out the model Claude Code starts on without setting `model` or `enforceAvailableModels`
- **[UNCOVERED]** - Added `auth: { google: {} }` for Claude apps gateway `telemetry.forward_to` destinations, so telemetry can be exported straight to Google Cloud's OTLP endpoint using the gateway's Google Cloud credentials
- **[UNCOVERED]** - Added certificate client authentication (`private_key_jwt`) between the Claude apps gateway and its identity provider, for identity providers that issue certificate credentials instead of client secrets
- **[UNCOVERED]** - Fixed a damaged response stream showing raw errors such as "JSON Parse error" or "undefined is not an object", or writing the word "undefined" into an answer, instead of being retried or reported as an interrupted response
- **[UNCOVERED]** - Fixed an overloaded or server error arriving right after a thinking block ending the turn with an error instead of being retried
- **[UNCOVERED]** - Fixed "Prompt is too long" errors that persisted after compacting: when the compacted request is still too long, Claude Code now compacts once more, keeping less of the recent conversation
- **[UNCOVERED]** - Fixed a session whose model is unavailable, with no fallback model left, showing a bare "is currently unavailable" message (or "Something went wrong" in cloud sessions) instead of the model-unavailable notice and its Learn more link
- **[UNCOVERED]** - Fixed Agent SDK sessions crashing when a user message contains an image with a malformed `source`, and failing on every later turn after a malformed document block; a malformed image is now replaced with an explanatory note
- **[UNCOVERED]** - Fixed MCP tool calls in a resumed session failing with "No such tool available" while their server was still connecting; the call now waits up to 10 seconds for the server
- **[UNCOVERED]** - Fixed repeated calls to the plan-usage endpoint after it rate-limits or rejects your login: `/usage`, `/extra-usage` and IDE usage views now back off instead of re-asking
- **[UNCOVERED]** - Fixed `claude mcp add` reporting success when managed settings restrict MCP servers to plugins; it now refuses and says what to do, instead of saving a server that never loads
- **[UNCOVERED]** - Fixed the `/plugin` configure screen: boolean options are now a true/false choice instead of free text, number options refuse invalid input, and ←/→ change an options field instead of switching tabs
- **[UNCOVERED]** - Fixed `ANTHROPIC_FOUNDRY_RESOURCE` being interpolated into the Foundry endpoint host unvalidated; a value that is not a plain resource name is now refused
- **[UNCOVERED]** - Fixed Claude Desktop behind a Claude apps gateway offering no 1M context option: the gateway now marks each 1M-capable model for Desktop automatically
- **[UNCOVERED]** - Fixed ↓ in shell mode selecting a hidden background-tasks pill, which stopped Backspace and Ctrl+U from editing the prompt
- **[UNCOVERED]** - Fixed Bash tool failing on Windows with many plugins enabled: plugin `bin/` directories that don't exist are no longer added to PATH, and inherited entries aren't added twice
- **[UNCOVERED]** - Fixed `sparsePaths` plugin marketplaces cloning empty and replacing a working local copy on older git (before 2.39), which failed every refresh with "marketplace.json file is no longer present"
- **[UNCOVERED]** - Fixed fullscreen rendering erasing the terminal output above the session when `[` in transcript mode writes the conversation to scrollback (macOS and Linux)
- **[UNCOVERED]** - Fixed fullscreen scroll position jumping to the previous message or to the bottom when a reply finished streaming while scrolled up
- **[UNCOVERED]** - Fixed tab bars in dialogs such as `/config` and `/plugin` breaking the title and tab labels mid-word in a narrow terminal; a tab that doesn't fit now moves to the next line whole
- **[UNCOVERED]** - Fixed the `/model` picker showing "+1 model" below the list after scrolling to the last model; the count now covers only the models below the visible rows
- **[UNCOVERED]** - Fixed `/keybindings` writing Backspace and Delete bindings for a footer action that does nothing into the generated `keybindings.json`
- **[UNCOVERED]** - Fixed a rebound agent panel close key (`footer:close`) typing "x" instead of itself on the row of the agent you're viewing
- **[UNCOVERED]** - Fixed vim mode `.` not repeating text typed very fast (for example over ssh or in tmux) or pasted without bracketed paste, and leaving the prompt in INSERT mode after repeating a change with nothing typed (such as `cw` then Esc)
- **[UNCOVERED]** - Fixed vim mode leaving the cursor on an image placeholder's opening bracket after `dd` on the last line or `yy` at the end of the prompt, where `r` or `x` would break or delete the image
- **[UNCOVERED]** - Fixed a key pressed the instant the terminal regained focus answering the Remote Control enable prompt before its short safety delay restarted
- **[UNCOVERED]** - Fixed the workspace trust dialog appearing a second time after switching renderers or updating when Claude Code was started in the home directory
- **[UNCOVERED]** - Fixed rules symlinked into `.claude/rules` from outside the project being skipped without ever showing the external-imports approval prompt; a `.claude` directory symlinked from outside the project now asks for the same approval
- **[UNCOVERED]** - Fixed plugins from marketplaces, claude.ai and npm pre-approving their own tools via `allowed-tools` under managed `allowManagedPermissionRulesOnly`; only plugins from an official Anthropic source or a source that managed settings vouch for keep that pre-approval
- **[UNCOVERED]** - Fixed a failed first `claude plugin install` leaving the plugin enabled and recorded when a dependency's version range could not be met
- **[UNCOVERED]** - Fixed the debug log dropping a failed hook's stderr when the hook also wrote to stdout, and logging nothing for a failed hook with no output; failed hooks now also log their status code
- **[UNCOVERED]** - Fixed `{"decision":"block"}` returned by Elicitation and ElicitationResult hooks being ignored; it now declines the MCP elicitation, as exit code 2 does
- **[UNCOVERED]** - Fixed sessions launched without the `SendMessage` tool (such as by Claude Desktop) still being told to message other sessions with it
- **[UNCOVERED]** - Fixed a photo sent from the Claude app over Remote Control being lost when its queued message was pulled back into the terminal prompt to edit, and the cursor moving one character for a photo with no caption
- **[UNCOVERED]** - Fixed typing a message during an automatic usage-limit wait taking the wait out of the "Continue automatically at usage limit" setting's control when that turn hit the limit again
- **[UNCOVERED]** - Fixed usage-limit warnings suggesting `/upgrade` to users already on the highest Max plan; the warnings and `/upgrade` itself now point at `/usage-credits` when it is available
- **[UNCOVERED]** - Fixed the Explore subagent switching to Opus on the Claude API when the session runs a model ID Claude Code doesn't recognize, such as a custom model behind a proxy; Explore now inherits that model
- **[UNCOVERED]** - Fixed `/loop` status updates in self-paced mode often not being shown because Claude wrote them only in its reasoning; Claude now writes each update, and the outcome when the loop stops, as visible text
- **[UNCOVERED]** - Fixed `/ultrareview` failing to upload the working tree when started from a git worktree that the Claude desktop app created on macOS or Linux
- **[UNCOVERED]** - Fixed sandboxed Bash commands failing to start on Linux when the working directory is write-denied and contains a read-denied directory
- **[UNCOVERED]** - Fixed artifact database write results telling Claude that every viewer sees a write to a viewer's private `data/users/` subtree, and added a "view" level to `as_level`
- **[UNCOVERED]** - Fixed the Claude apps gateway answering `431 Request Header Fields Too Large` to every request from a sign-in whose identity provider lists many groups; it now accepts request headers up to 256 KiB
- **[UNCOVERED]** - Improved the usage-limit wait: the limit's state and the countdown with the usage-credits option now show as one block under the prompt, and limit messages no longer repeat the countdown
- **[UNCOVERED]** - Improved the "No such tool available" error for Claude in Chrome tools called without their prefix: it now names the tool to call
- **[UNCOVERED]** - Improved Monitor event rows to show what each event printed instead of repeating the description, and stopped repeating an unchanged "Waiting for N … to finish" line after every event
- **[UNCOVERED]** - Improved Workflow tool sandbox hardening for errors thrown by async script hooks
- **[UNCOVERED]** - Improved startup time and memory use by building only the parts of the settings schema that your settings files actually use
- **[UNCOVERED]** - Improved `/claude-api`: `hillclimb` no longer spends rounds on prompt rewordings too small for the eval to measure, and an extra page you ask for beside `report.html` is built as one local file that loads nothing from the network
- **[UNCOVERED]** - Improved lists such as `/tasks`, `/copy` and `/hooks`: the details after each name now line up in one column when they fit, and otherwise sit at the right edge
- **[UNCOVERED]** - Improved `claude plugin marketplace add` to say when it replaces a marketplace already added under the same name from a different source, and how to undo it
- **[UNCOVERED]** - Improved the startup refusal when managed settings require a sign-in (`forceLoginMethod` or `forceLoginOrgUUID`) and an API key, token or `apiKeyHelper` is configured: it now names the credential in use, where it is set, and how to remove it
- **[UNCOVERED]** - Improved auto-memory loading: invisible characters and tags that imitate Claude Code's own markup are neutralized in `MEMORY.md` and recalled memory notes before they reach Claude
- **[UNCOVERED]** - Improved `claude remote-control`: in a folder you haven't trusted yet, it now asks for workspace trust on the terminal instead of exiting
- **[UNCOVERED]** - Improved artifact pages: Claude writes its design plan into the page instead of the reply, and uses the name you already gave something as the page title
- **[UNCOVERED]** - Improved the Artifact tool so that when Claude is given a claude.ai chat or project link, an artifact from a chat, or an artifact id on its own, it asks for the right link or the content instead of stopping
- **[UNCOVERED]** - Changed interactive terminal and VS Code sessions to start in auto mode when no permission mode is configured, on every plan and provider; `permissions.defaultMode` still overrides it
- **[UNCOVERED]** - Changed Ultracode into its own toggle in `/effort` (Tab, or `/effort ultracode [on|off]`): it no longer forces xhigh effort and stays on at any effort level
- **[UNCOVERED]** - Changed retries after a dropped connection mid-response to share one budget with the rest of the request's retries, so a failing request gives up sooner
- **[UNCOVERED]** - Changed the notice shown when a Sonnet model's safeguards flag a message to explain why it happened and to offer editing and retrying
- **[UNCOVERED]** - Changed safety-related model switches in sessions that pin an Opus model with `ANTHROPIC_DEFAULT_OPUS_MODEL` or `modelOverrides`: on the Anthropic API, the API now picks the model to switch to for each kind of flag, not the pinned model
- **[UNCOVERED]** - Changed the non-interactive first turn to still wait up to 2s for connecting MCP servers named by `--allowedTools` or an `mcp_tool` hook, even when `CLAUDE_CODE_MCP_STARTUP_WAIT_MS` is `0`
- **[UNCOVERED]** - Changed `/recap` to decline with a short notice when it arrives relayed from a chat thread (your own included) or from a routine or webhook; typed in the terminal, the Claude apps, Remote Control, `-p` or an SDK host, it runs as before
- **[UNCOVERED]** - Changed `/artifacts` to show its filter tabs beside the title with one-word labels (All, Mine, Shared), using the same tab bar as `/config` and `/plugin`
- **[UNCOVERED]** - Changed artifact publishing to refuse a file on a network share (a `\\host\share` path or a `/net` automount) unless it is on a mapped network drive added with `--add-dir`
- **[UNCOVERED]** - [VSCode] Added an optional time above each prompt and response, with a date line where the day changes (Claude Code: Show Message Timestamps setting, off by default)
- **[UNCOVERED]** - [VSCode] Added plugin load errors and notes to the Manage plugins rows, with a popup to disable, uninstall or copy the error
- **[UNCOVERED]** - [VSCode] Added an Ultracode on/off switch under the Effort slider, replacing the slider's Ultracode stop; the model pill shows "· Ultracode" at any effort level
- **[UNCOVERED]** - [VSCode] Fixed Reload Claude from the Memory dialog restarting before an edited file was saved
- **[UNCOVERED]** - [VSCode] Fixed a restored tab opening a conversation another Claude process still has open; it now asks first
- **[UNCOVERED]** - [VSCode] Fixed Focus view sections you expanded closing on their own while a sub-agent is working or when the section's first step is trimmed from view
- **[UNCOVERED]** - [VSCode] Fixed typing `/model` and Enter printing usage text into the chat instead of opening the model selector
- **[UNCOVERED]** - [VSCode] Fixed `/feedback` on Vertex, Bedrock and Foundry being refused after you pressed Send; the report is now saved on this computer, as the terminal does
- **[UNCOVERED]** - [VSCode] Fixed sign-in waiting up to a minute for the Python extension after a window reload
- **[UNCOVERED]** - [VSCode] Fixed Claude Code tabs that stopped responding after Restart Extensions: they now reopen on their conversation
- **[UNCOVERED]** - [VSCode] Fixed a message from another agent with no recorded sender showing as raw XML in the chat
- **[UNCOVERED]** - [VSCode] Fixed messages from other agents, sessions or channels disappearing after a reload
- **[UNCOVERED]** - [VSCode] Fixed a user's own `/mcp`, `/config` or `/settings` command being shadowed by the extension's dialog
- **[UNCOVERED]** - [VSCode] Fixed Escape stopping every background agent when no turn was running
- **[UNCOVERED]** - [VSCode] Fixed plugin install links replacing a marketplace you already have that uses the same name
- **[UNCOVERED]** - [VSCode] Fixed "Prompt is too long" errors after compaction when a large text file is attached to a message
- **[UNCOVERED]** - [VSCode] Fixed chat links to files with non-ASCII characters, spaces or brackets in their path not opening
- **[UNCOVERED]** - [VSCode] Changed `CLAUDE_CONFIG_DIR` in the `claudeCode.environmentVariables` setting to apply only when it is an absolute path, and passed it to terminals that continue the chat
- **[UNCOVERED]** - [Cloud sessions] Fixed a routine's Edit and Duplicate controls saying the routine was still loading while you were offline; they now tell you you're offline
- **[UNCOVERED]** - [Claude Tag] Added model family choices such as "Opus (latest)" for a thread, a channel default or your DM, so the choice follows the newest model in that family
- **[UNCOVERED]** - [Claude Tag] Added the spend that counts toward your organization-wide limit to the analytics spend projection chart, with how much of the limit is used
- **[UNCOVERED]** - [Claude Tag] Fixed the earlier Claude in Slack app's progress card and link previews omitting the repository and Create PR button when a GitHub Enterprise host name contains an underscore
- **[UNCOVERED]** - [Claude Tag] Fixed Claude staying silent in a channel whose environment declines to start it; it now posts one notice asking you to contact an admin, and retries when @-mentioned
- **[UNCOVERED]** - [Claude Tag] Changed Claude to post its private sign-in notice at every @mention from someone who hasn't connected their Claude account, instead of going quiet after the first
- **[UNCOVERED]** - [Claude Tag] Improved "Notify members now" in admin settings: one press reaches every workspace your organization claimed in an Enterprise Grid, and more members in large workspaces
- **[UNCOVERED]** - [Claude Tag] Improved Claude's wait notice on self-hosted environments with on-demand runners: it now says whether a runner is starting, a start will be retried, or no runner will start
- **[UNCOVERED]** - [Claude Tag] Improved the error shown when adding a channel manager fails because the channel's Slack workspace can't be confirmed as connected to your organization
- **[UNCOVERED]** - [Claude Tag] Improved a channel's access lists in admin settings to show the connectors, repositories and plugins an auto-join pattern attaches, and where each comes from
- **[UNCOVERED]** - [Claude Tag] Improved adding repositories as a channel manager: when your GitHub sign-in can't confirm you're a repository admin, the page asks you to sign in with GitHub
- **[UNCOVERED]** - [Code Review] Fixed Code Review giving up without posting a finished review when an unsubmitted review under its GitHub App was open on the pull request; it now retries the post first

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
| Oct 2, 2026AnnouncementsAnthropic invests $100 million to tr | Anthropic Blog | Oct 2, 2026AnnouncementsAnthropic invests $100 million to train 10,000 engineers |

### cc-issues-enhancement

- Source: CC GitHub Issues labeled 'enhancement'
- Entries fetched: 300
- New uncovered: 1

| Entry | Section | Description |
|-------|---------|-------------|
| [Feature Request] Add validation warnings for configuration  | GitHub Issues (enhancement) | **Bug Description** no considero esto un bug porque yo tuve parte de culpa pero  |

### cc-discussions-feature-request

- Source: CC GitHub Discussions in feature-request category
- Entries fetched: 0
- New uncovered: 0

---
Total new uncovered entries: **2**

_Generated by `.github/scripts/native-sources-monitor.py`_
