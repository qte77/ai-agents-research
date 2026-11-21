---
title: Claude Chrome Extension Analysis
source: https://claude.com/claude-for-chrome
purpose: Evaluate the Claude Chrome extension (Claude in Chrome) for relevance to CC-based workflows.
created: 2026-03-07
updated: 2026-11-19
validated_links: 2026-11-19
status: assess
---

**Details:** Generally available; all paid plans; first-party pages read 2026-11-19, no hands-on testing

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
- **Availability limits (documented, two pages differ)**: the GA post (2026-08-26) says the extension
  "doesn't run on other Chromium browsers or on mobile yet", while the Claude Code docs page (read
  2026-11-19) lists Brave, Arc, Vivaldi and Opera alongside Chrome and Edge and says Claude Code sets
  up the connection. We do not rule which is current. Not supported in WSL. Off under Zero Data Retention in
  Claude Code; off by default in HIPAA organizations, and outside the BAA ([Claude Code docs][chrome-cc], [safety article][chrome-safe]).
- **Permission modes (documented)**: Manually approve, Automatically approve (a classifier checks each
  action; default in the Cowork side panel) and Skip all approvals (no checks). Per the permissions guide, entering
  sensitive data asks "Regardless of your permission mode", Skip included; downloads are documented
  as asking in Manual and under "Always allow actions on this site". Admins on Team and Enterprise set site allow
  and block lists ([permissions guide][chrome-perm]).
- **Status wording differs**: the GA post and product page say generally available. The safety
  article, marked "Updated this week" when read, says it is available in Claude Cowork and Claude
  Code "and in beta in the Chrome browser", so beta is its current label for the browser surface
  ([safety article][chrome-safe]); the permissions guide carries no beta label.

### Safety

Anthropic names prompt injection from page content as the main risk, and the safety article states
"The risk is not zero" ([safety article][chrome-safe]). Layers listed: training, a content classifier, an action
classifier, site blocklists, confirmations and red teaming. Reported attack-success numbers are
vendor-internal (vendor claim): "less than 0.08%" with Claude Opus 4.8 in the safety article; in the
GA post no attack succeeded against Sonnet 5 or Opus 5 with probes plus action classifiers and 0.3%
succeeded against Fable 5; the 2025-11-24 [post][chrome-pi] gave about 1% for its then-current
configuration.
Comparison with other agent browsers and the injection landscape:
[browser-agents-landscape.md](../../non-cc/agents/browser-agents-landscape.md#safety-prompt-injection-from-web-content).

## Applicability

| Aspect | Fit | Rationale |
| ------ | --- | --------- |
| Browser automation for API/CLI workflows | None | API/CLI-based pipelines have no browser interaction surface |
| Testing and debugging a web app you build | Moderate | `claude --chrome` reads console errors and DOM in your own browser; Chrome DevTools MCP and Playwright MCP (Model Context Protocol servers) are the alternatives (see the [comparison](../../non-cc/agents/browser-agents-landscape.md#claude-in-chrome-vs-devtools-mcp-vs-playwright-mcp)) |
| Cross-platform integration with CC | Weak | Interactive only; API-key sessions are documented as unsupported, and headless `claude -p` use is unlikely to benefit (our reading) |
| Form filling / web scraping | Conditional | Relevant only where data sits behind your own login; for bulk or unattended extraction see [CC-web-scraping-plugins-analysis.md](CC-web-scraping-plugins-analysis.md) |
| End-to-end workflows with Cowork | Conditional | Side panel runs as a Cowork session on several plans (see [CC-cowork-plugins-enterprise-analysis.md](CC-cowork-plugins-enterprise-analysis.md)) |

### Decision Rule

**The Chrome extension targets browser work in sessions where you are already signed in (form filling, web navigation, checking a UI you just built). Projects whose CC usage is entirely API/CLI-driven or unattended gain no benefit and need no adoption action; for headless or isolated browser automation use Playwright MCP.**

## Sources

| Source | Content |
| ------ | ------- |
| [Claude Chrome extension][chrome-product] | Product page, availability, safeguards summary |
| [Claude in Chrome is generally available][chrome-ga] | GA date 2026-08-26, safety evaluation, browser limits |
| [Use Claude Code with Chrome][chrome-cc] | `--chrome`, `/chrome`, prerequisites, ZDR, HIPAA |
| [Use Claude in Chrome safely][chrome-safe] | Risks, safeguards, beta wording, 0.08% figure |
| [Claude in Chrome permissions guide][chrome-perm] | Approval modes, protected actions |
| [Mitigating prompt injections in browser use][chrome-pi] | 2025-11-24 robustness post |

[chrome-product]: https://claude.com/claude-for-chrome
[chrome-ga]: https://claude.com/resources/articles/claude-in-chrome-generally-available
[chrome-cc]: https://code.claude.com/docs/en/chrome
[chrome-safe]: https://support.claude.com/en/articles/12902428-using-claude-for-chrome-safely
[chrome-perm]: https://support.claude.com/en/articles/12902446-claude-for-chrome-permissions-guide
[chrome-pi]: https://www.anthropic.com/research/prompt-injection-defenses
