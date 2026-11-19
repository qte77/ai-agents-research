---
title: Claude Chrome Extension Analysis
source: https://claude.com/claude-for-chrome
purpose: Evaluate the Claude Chrome extension (Claude in Chrome) for relevance to CC-based workflows.
created: 2026-03-07
updated: 2026-11-19
validated_links: 2026-11-19
status: generally-available
---

**Details:** all paid plans; first-party pages read 2026-11-19, no hands-on testing

## What It Is

A Chrome browser extension that lets Claude read the page you have open, then click, type and fill
forms in your own signed-in browser ([product page][chrome-product]). Anthropic announced general
availability on every paid plan on 2026-08-26, after a pilot ([GA post][chrome-ga]). It can be opened
from the Chrome side panel, from Claude, or from Claude Code ([product page][chrome-product]).

### Key Mechanics

- **Browser automation**: reads pages, clicks, types, navigates, fills forms using your existing logins ([GA post][chrome-ga]).
- **Claude Code integration (documented)**: start with `claude --chrome` or run `/chrome` to check
  status, manage permissions, reconnect and pick a browser; it can be enabled by default but that
  loads the browser tools into context every session ([Claude Code docs][chrome-cc]). Claude opens
  new tabs in a tab group, pauses on login pages and CAPTCHAs, and can read console output, record
  GIFs and upload files up to 10 MB in total ([Claude Code docs][chrome-cc]).
- **Prerequisites (documented)**: extension version 1.0.36 or later, a direct Anthropic plan
  (Pro, Max, Ultra, Team or Enterprise), and `/login` sign-in. With an API key or a `setup-token`
  credential Claude Code keeps Chrome off; it is not available through Amazon Bedrock, Google Cloud's agent platform
  or Microsoft Foundry ([Claude Code docs][chrome-cc]).
- **Availability limits (documented)**: Chrome and Edge are supported; other Chromium browsers are
  detected by Claude Code, but the GA post says the extension does not run on other Chromium browsers
  or mobile yet (the two pages disagree). Not supported in WSL. Off under Zero Data Retention in
  Claude Code; off by default in HIPAA organizations, and outside the BAA ([Claude Code docs][chrome-cc], [safety article][chrome-safe]).
- **Permission modes (documented)**: Manually approve, Automatically approve (a classifier checks each
  action; default in the Cowork side panel) and Skip all approvals (no checks). Downloads and
  entering sensitive data still ask in the first two. Admins on Team and Enterprise set site allow
  and block lists ([permissions guide][chrome-perm]).
- **Status wording differs**: the GA post and product page say generally available, while the safety
  article still says "in beta in the Chrome browser" ([safety article][chrome-safe]). Treat GA as
  the newer statement and the article as lagging (our reading).

### Safety

Anthropic names prompt injection from page content as the main risk, and the safety article states
"The risk is not zero" ([safety article][chrome-safe]). Layers listed: training, a content classifier, an action
classifier, site blocklists, confirmations and red teaming. Reported attack-success numbers are
vendor-internal (vendor claim): under 0.08% for one configuration in the safety article, and no
successful attack against two named models with probes plus action classifiers in the GA post.
Comparison with other agent browsers and the injection landscape:
[browser-agents-landscape.md](../../non-cc/agents/browser-agents-landscape.md#safety-prompt-injection-from-web-content).

## Applicability

| Aspect | Fit | Rationale |
| ------ | --- | --------- |
| Browser automation for API/CLI workflows | None | API/CLI-based pipelines have no browser interaction surface |
| Testing and debugging a web app you build | Moderate | `claude --chrome` reads console errors and DOM in your own browser; Chrome DevTools MCP and Playwright MCP are the alternatives (see the [comparison](../../non-cc/agents/browser-agents-landscape.md#claude-in-chrome-vs-devtools-mcp-vs-playwright-mcp)) |
| Cross-platform integration with CC | Weak | Interactive only; headless `claude -p` runs and API-key sessions cannot use it |
| Form filling / web scraping | Conditional | Relevant only where data sits behind your own login; for bulk or unattended extraction see [CC-web-scraping-plugins-analysis.md](CC-web-scraping-plugins-analysis.md) |
| End-to-end workflows with Cowork | Conditional | Side panel runs as a Cowork session on several plans (see [CC-cowork-plugins-enterprise-analysis.md](CC-cowork-plugins-enterprise-analysis.md)) |

### Decision Rule

**The Chrome extension targets browser work in sessions where you are already signed in (form filling, web navigation, checking a UI you just built). Projects whose CC usage is entirely API/CLI-driven or unattended gain no benefit and need no adoption action; for headless or isolated browser automation use Playwright MCP.**

## References

- [Claude Chrome extension][chrome-product]
- [Claude in Chrome is generally available][chrome-ga]
- [Use Claude Code with Chrome][chrome-cc]
- [Use Claude in Chrome safely][chrome-safe]
- [Claude in Chrome permissions guide][chrome-perm]

[chrome-product]: https://claude.com/claude-for-chrome
[chrome-ga]: https://claude.com/resources/articles/claude-in-chrome-generally-available
[chrome-cc]: https://code.claude.com/docs/en/chrome
[chrome-safe]: https://support.claude.com/en/articles/12902428-using-claude-for-chrome-safely
[chrome-perm]: https://support.claude.com/en/articles/12902446-claude-for-chrome-permissions-guide
