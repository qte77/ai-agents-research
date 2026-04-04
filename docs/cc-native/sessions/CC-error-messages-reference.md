---
title: CC Error Messages Reference
purpose: Catalog of Claude error messages with triggers, resolutions, and community workarounds
source: https://support.claude.com/en/articles/12466728-troubleshoot-claude-error-messages
created: 2026-04-04
updated: 2026-04-04
validated_links: 2026-04-04
---

**Status**: Assess

## What It Is

Reference of user-facing error messages in Claude and Claude Code, sourced from Anthropic's official [troubleshooting article][err-article] and supplemented with community-reported workarounds. Covers usage limits, length limits, login errors, capacity constraints, service incidents, and the BUDDY companion feature.

## Error Categories

### Usage Limits

<!-- markdownlint-disable MD013 -->

| Message | Trigger | Resolution |
|---------|---------|------------|
| "Approaching 5-hour limit." | Approaching plan's limit within a 5-hour window | Review [usage limit best practices][err-article] |
| "5-hour limit reached - resets [time]." | Plan limit exceeded | Wait for reset timer |
| "5-hour limit resets [time] - continuing with extra usage." | Paid user with extra usage enabled hits limit | Consult extra usage docs for plan type |

<!-- markdownlint-enable MD013 -->

Community perspectives on limits and workarounds:

- [Usage limits megathread][mega] — ongoing community discussion with workaround strategies
- [Nicholas Rhodes — usage limits fix][rhodes] — configuration-level mitigations
- [Artificial Corner — Claude limits fix][artcorner] — practical limit management
- [Michelle James — bypass message limits][medium] — conversation memory and context strategies

### Length Limits

| Message | Trigger | Resolution |
|---------|---------|------------|
| "Your message will exceed the length limit for this chat..." | Input exceeds maximum length | Break into smaller chunks, summarize key sections, start new conversation |

### Login Errors

| Message | Trigger | Resolution |
|---------|---------|------------|
| "There was an error logging you in" | Authentication failure | Disable VPN, turn off browser extensions, clear cache/cookies, check [status.claude.com][status] |

### Capacity Constraints

| Message | Trigger | Resolution |
|---------|---------|------------|
| "Due to unexpected capacity constraints, Claude is unable to respond..." | High system-wide demand | Retry in a few minutes (temporary, not an outage) |

### Service Incidents

| Trigger | Resolution |
|---------|------------|
| Complete unavailability or severe degradation | Check [status.claude.com][status] for real-time incident updates |

## BUDDY / Companion

The BUDDY companion (Glitch) is a Tamagotchi-style pet displayed beside the input box. Users looking to disable it:

- `/buddy off` — works per-session but [reappears after 1-2 minutes][gh-42348]
- No persistent disable exists — no settings.json key, no env var, no CLI flag (verified 2026-04-04)
- Hooks cannot invoke `/buddy off` (slash commands run inside REPL, hooks run shell scripts outside it)
- Tracked in [anthropics/claude-code#42506][gh-42506] (dupes: [#42348][gh-42348], [#42287][gh-42287], [#41942][gh-41942])
- Community guide: [How to disable the BUDDY pet][buddy-guide]

## Cross-References

- [CC-session-keepalive-analysis.md](CC-session-keepalive-analysis.md) — session timeout overlaps with capacity errors
- [CC-print-mode-gotchas.md](CC-print-mode-gotchas.md) — headless mode error handling
- [CC-session-lifecycle-analysis.md](CC-session-lifecycle-analysis.md) — session state and limit resets

## Sources

| Source | Content |
|---|---|
| [Troubleshoot Claude error messages][err-article] | Official Anthropic support article (1st-party) |
| [anthropics/claude-code#42506][gh-42506] | Feature request: disable companion pets (1st-party) |
| [anthropics/claude-code#42348][gh-42348] | Feature request: remove /buddy prefix (1st-party) |
| [r/ClaudeAI][reddit] | Community subreddit (2nd-party) |
| [Usage limits megathread][mega] | Ongoing community limits discussion (2nd-party) |
| [Nicholas Rhodes — usage limits fix][rhodes] | Substack: limit mitigations (2nd-party) |
| [Artificial Corner — Claude limits fix][artcorner] | Limit management guide (2nd-party) |
| [Michelle James — bypass message limits][medium] | Medium: conversation memory strategies (2nd-party) |
| [Orbisius — disable BUDDY pet][buddy-guide] | Blog: BUDDY disable guide (2nd-party) |

[err-article]: https://support.claude.com/en/articles/12466728-troubleshoot-claude-error-messages
[gh-42348]: https://github.com/anthropics/claude-code/issues/42348
[gh-42506]: https://github.com/anthropics/claude-code/issues/42506
[gh-42287]: https://github.com/anthropics/claude-code/issues/42287
[gh-41942]: https://github.com/anthropics/claude-code/issues/41942
[reddit]: https://www.reddit.com/r/ClaudeAI/
[mega]: https://www.reddit.com/r/ClaudeAI/comments/1s7fcjf/claude_usage_limits_discussion_megathread_ongoing/
[rhodes]: https://nicholasrhodes.substack.com/p/claude-usage-limits-fix
[artcorner]: https://artificialcorner.com/p/claude-limits-fix
[medium]: https://michellejamesina.medium.com/how-to-bypass-claudes-message-limits-complete-guide-to-ai-conversation-memory-2025-b3d5f0685f39
[buddy-guide]: https://orbisius.com/blog/how-to-disable-the-buddy-pet-in-claude-code-p8198
[status]: https://status.claude.com
