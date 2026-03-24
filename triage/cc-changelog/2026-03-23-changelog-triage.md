## Changelog Monitor Report

Last scanned version: **2.1.79**
New versions detected: **2**

### New Versions Summary

| Version | Features | Covered | Uncovered |
|---------|----------|---------|-----------|
| 2.1.81 | 27 | 25 | 2 |
| 2.1.80 | 17 | 16 | 1 |

### Feature Coverage Details

#### v2.1.81

- **[covered]** - Added `--bare` flag for scripted `-p` calls — skips hooks, LSP, plugin sync, and skill directory walks; requires `ANTHROPIC_API_KEY` or an `apiKeyHelper` via `--settings` (OAuth and keychain auth disabled); auto-memory fully disabled
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Added `--channels` permission relay — channel servers that declare the permission capability can forward tool approval prompts to your phone
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Fixed multiple concurrent Claude Code sessions requiring repeated re-authentication when one session refreshes its OAuth token
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-recursive-spawning-patterns.md`
- **[covered]** - Fixed voice mode silently swallowing retry failures and showing a misleading "check your network" message instead of the actual error
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - Fixed voice mode audio not recovering when the server silently drops the WebSocket connection
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` not suppressing the structured-outputs beta header, causing 400 errors on proxy gateways forwarding to Vertex/Bedrock
  - Covered by: `cc-native/ci-execution/CC-github-actions-analysis.md`, `cc-native/configuration/CC-model-provider-configuration.md`, `cc-native/plugins-ecosystem/CC-cowork-skills-api-workflows.md`
- **[covered]** - Fixed `--channels` bypass for Team/Enterprise orgs with no other managed settings configured
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[covered]** - Fixed unnecessary permission prompts for Bash commands containing dashes in strings
  - Covered by: `cc-native/agents-skills/CC-ralph-enhancement-research.md`, `cc-native/ci-execution/CC-permissions-bypass-analysis.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`
- **[covered]** - Fixed plugin hooks blocking prompt submission when the plugin directory is deleted mid-session
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Fixed a race condition where background agent task output could hang indefinitely when the task completed between polling intervals
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-recursive-spawning-patterns.md`
- **[covered]** - Resuming a session that was in a worktree now switches back to that worktree
  - Covered by: `cc-native/agents-skills/CC-recursive-spawning-patterns.md`, `cc-native/ci-execution/CC-remote-control-analysis.md`
- **[covered]** - Fixed `/btw` not including pasted text when used during an active response
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Fixed a race where fast Cmd+Tab followed by paste could beat the clipboard copy under tmux
  - Covered by: `cc-native/ci-execution/CC-remote-access-landscape.md`, `cc-native/configuration/CC-fast-mode-analysis.md`, `cc-native/context-memory/CC-extended-context-analysis.md`
- **[covered]** - Fixed terminal tab title not updating with an auto-generated session description
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-recursive-spawning-patterns.md`
- **[covered]** - Fixed invisible hook attachments inflating the message count in transcript mode
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed Remote Control sessions showing a generic title instead of deriving from the first prompt
  - Covered by: `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`, `cc-native/ci-execution/CC-remote-access-landscape.md`
- **[covered]** - Fixed `/rename` not syncing the title for Remote Control sessions
  - Covered by: `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`, `cc-native/ci-execution/CC-remote-access-landscape.md`
- **[covered]** - Fixed Remote Control `/exit` not reliably archiving the session
  - Covered by: `cc-native/agents-skills/CC-recursive-spawning-patterns.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`, `cc-native/ci-execution/CC-remote-access-landscape.md`
- **[covered]** - Improved MCP read/search tool calls to collapse into a single "Queried {server}" line (expand with Ctrl+O)
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`
- **[covered]** - Improved `!` bash mode discoverability — Claude now suggests it when you need to run an interactive command
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[covered]** - Improved plugin freshness — ref-tracked plugins now re-clone on every load to pick up upstream changes
  - Covered by: `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`
- **[covered]** - Improved Remote Control session titles to refresh after your third message
  - Covered by: `cc-native/agents-skills/CC-recursive-spawning-patterns.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`, `cc-native/ci-execution/CC-remote-access-landscape.md`
- **[covered]** - Updated MCP OAuth to support Client ID Metadata Document (CIMD / SEP-991) for servers without Dynamic Client Registration
  - Covered by: `cc-native/ci-execution/CC-sandboxing-analysis.md`, `cc-native/configuration/CC-bash-mode-analysis.md`, `cc-native/plugins-ecosystem/CC-cowork-skills-api-workflows.md`
- **[covered]** - Changed plan mode to hide the "clear context" option by default (restore with `"showClearContextOnPlanAccept": true`)
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`
- **[covered]** - [VSCode] Fixed Windows PATH inheritance for Bash tool when using Git Bash (regression in v2.1.78)
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[UNCOVERED]** - Fixed a crash on Node.js 18
- **[UNCOVERED]** - Disabled line-by-line response streaming on Windows (including WSL in Windows Terminal) due to rendering issues

#### v2.1.80

- **[covered]** - Added `rate_limits` field to statusline scripts for displaying Claude.ai rate limit usage (5-hour and 7-day windows with `used_percentage` and `resets_at`)
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[covered]** - Added `source: 'settings'` plugin marketplace source — declare plugin entries inline in settings.json
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`
- **[covered]** - Added CLI tool usage detection to plugin tips, in addition to file pattern matching
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Added `effort` frontmatter support for skills and slash commands to override the model effort level when invoked
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`
- **[covered]** - Added `--channels` (research preview) — allow MCP servers to push messages into your session
  - Covered by: `cc-native/CC-changelog-feature-scan.md`, `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`
- **[covered]** - Fixed `--resume` dropping parallel tool results — sessions with parallel tool calls now restore all tool_use/tool_result pairs instead of showing `[Tool result missing]` placeholders
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`
- **[covered]** - Fixed voice mode WebSocket failures caused by Cloudflare bot detection on non-browser TLS fingerprints
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed 400 errors when using fine-grained tool streaming through API proxies, Bedrock, or Vertex
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Fixed `/remote-control` appearing for gateway and third-party provider deployments where it cannot function
  - Covered by: `cc-native/ci-execution/CC-version-pinning-resilience.md`, `cc-native/configuration/CC-model-provider-configuration.md`
- **[covered]** - Improved responsiveness of `@` file autocomplete in large git repositories
  - Covered by: `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/context-memory/CC-llms-txt-analysis.md`
- **[covered]** - Improved `/effort` to show what auto currently resolves to, matching the status bar indicator
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`
- **[covered]** - Improved `/permissions` — Tab and arrow keys now switch tabs from within a list
  - Covered by: `cc-native/ci-execution/CC-github-actions-analysis.md`, `cc-native/ci-execution/CC-remote-control-analysis.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Improved background tasks panel — left arrow now closes from the list view
  - Covered by: `cc-native/ci-execution/CC-github-actions-analysis.md`, `cc-native/ci-execution/CC-remote-control-analysis.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Simplified plugin install tips to use a single `/plugin install` command instead of a two-step flow
  - Covered by: `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - Reduced memory usage on startup in large repositories (~80 MB saved on 250k-file repos)
  - Covered by: `cc-native/configuration/CC-hooks-system-analysis.md`, `cc-native/context-memory/CC-memory-system-analysis.md`, `cc-native/examples/rules/context-management.md`
- **[covered]** - Fixed managed settings (`enabledPlugins`, `permissions.defaultMode`, policy-set env vars) not being applied at startup when `remote-settings.json` was cached from a prior session
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-recursive-spawning-patterns.md`
- **[UNCOVERED]** - Fixed `/sandbox` tab switching not responding to Tab or arrow keys

---
_Generated by `.github/scripts/changelog-compare.py`_

## Native Sources Monitor Report

Sources checked: **3**

### anthropic-blog

- Source: Anthropic Blog — announcements and product updates
- Entries fetched: 13
- New uncovered: 0

### cc-issues-enhancement

- Source: CC GitHub Issues labeled 'enhancement'
- Entries fetched: 300
- New uncovered: 4

| Entry | Section | Description |
|-------|---------|-------------|
| [FEATURE] Add Control-t for transpose characters | GitHub Issues (enhancement) | ### Preflight Checklist

- [x] I have searched [existing requests](https://githu |
| Add Croatian (hr) to voice dictation supported languages | GitHub Issues (enhancement) | ## Feature Request

Voice mode currently supports ~20 languages (Czech, Danish,  |
| Add solarized-light theme | GitHub Issues (enhancement) | ## Feature request

Please add a `solarized-light` theme to complement the exist |
| [FEATURE] Use ''git rev-parse --git-common-dir'' for groupin | GitHub Issues (enhancement) | ### Preflight Checklist

- [x] I have searched [existing requests](https://githu |

### cc-discussions-feature-request

- Source: CC GitHub Discussions in feature-request category
- Entries fetched: 0
- New uncovered: 0

---
Total new uncovered entries: **4**

_Generated by `.github/scripts/native-sources-monitor.py`_

