# CC Changelog & Native Sources: New Uncovered Features Detected

## Changelog Monitor Report

Last scanned version: **2.1.185**
New versions detected: **6**

### New Versions Summary

| Version | Features | Covered | Uncovered |
|---------|----------|---------|-----------|
| 2.1.195 | 12 | 0 | 12 |
| 2.1.193 | 15 | 0 | 15 |
| 2.1.191 | 20 | 0 | 20 |
| 2.1.190 | 1 | 0 | 1 |
| 2.1.187 | 21 | 0 | 21 |
| 2.1.186 | 33 | 0 | 33 |

### Feature Coverage Details

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
- Entries fetched: 12
- New uncovered: 1

| Entry | Section | Description |
|-------|---------|-------------|
| ProductJun 23, 2026Introducing Claude TagClaude Tag is a new | Anthropic Blog | ProductJun 23, 2026Introducing Claude TagClaude Tag is a new way for teams to wo |

### cc-issues-enhancement

- Source: CC GitHub Issues labeled 'enhancement'
- Entries fetched: 300
- New uncovered: 1

| Entry | Section | Description |
|-------|---------|-------------|
| [FEATURE] Add whittling as spinner verb | GitHub Issues (enhancement) | ### Preflight Checklist - [x] I have searched [existing requests]( and this feat |

### cc-discussions-feature-request

- Source: CC GitHub Discussions in feature-request category
- Entries fetched: 0
- New uncovered: 0

---
Total new uncovered entries: **2**

_Generated by `.github/scripts/native-sources-monitor.py`_
