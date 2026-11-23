---
title: Browser Agents Landscape
source: https://code.claude.com/docs/en/chrome
purpose: "Landscape of agents that use websites: agentic browsers, Claude in Chrome vs Chrome DevTools MCP vs Playwright MCP, WebMCP, hosted agent browsers, dated benchmarks, and prompt-injection safety."
created: 2026-11-19
updated: 2026-11-22
validated_links: 2026-11-19
status: reference
---

**Details:** informational landscape; vendor docs, READMEs and arXiv abstract pages read 2026-11-19, no hands-on testing

Evidence levels: **documented** (vendor docs or README state it), **announced** (vendor post, no docs yet),
**paper** (arXiv abstract page), **vendor claim** (self-reported score we did not reproduce),
**our reading** (inference). Whole-desktop GUI agents and OSWorld live in
[computer-use-agents-landscape.md](computer-use-agents-landscape.md); scraping and anti-bot
infrastructure live in the [scraping catalog][scrape-cat]. This document covers agents that act on
web pages.

## TL;DR

- Three ways to give a coding agent a browser, all documented: Anthropic's Claude in Chrome (your own
  signed-in Chrome, via an extension), Google's Chrome DevTools MCP (a Chrome the server launches or
  attaches to, aimed at debugging and performance), and Microsoft's Playwright MCP (a Playwright
  browser, optionally attached to your own via an extension). See [the comparison](#claude-in-chrome-vs-devtools-mcp-vs-playwright-mcp).
- WebMCP is a proposal, not a standard: a W3C Web Machine Learning Community Group draft (status
  `CG-DRAFT` in the spec source) with a Chrome 149 origin trial and an Edge 150 origin trial listed
  in its implementation-status file (documented).
- Browser-agent benchmark scores are not one scale. Online-Mind2Web numbers differ by judge (human,
  WebJudge, custom agentic judge); HAL (Princeton) and an aggregator run by Steel list very different
  ranges; only Steel is a hosted-browser vendor, and its rows mix independent and self-reported
  results (vendor claim).
- Every vendor says the same about safety: web content is untrusted, injection is not solved, keep
  sensitive work off agent-driven browsers. Numbers are vendor-internal.

## Agentic browsers and in-browser agents

| Product | State (read 2026-11-19) | Evidence |
| ------- | ----------------------- | -------- |
| [Claude in Chrome][cfc] | Generally available on every paid Claude plan, announced 2026-08-26; also reachable from Claude Code | documented ([GA post][cfc-ga], [Claude Code docs][cc-chrome]) |
| ChatGPT Atlas ([launch post][atlas], 2025-10-21) | Stale, kept as one dated line: the page now says Atlas "has since been deprecated" (no date given) and points readers to ChatGPT Work, read 2026-11-22 | documented (note) |
| [Gemini in Chrome][gem-chrome] | Assistant in Chrome; agentic "auto browse" described as a preview for Google AI Pro and Ultra subscribers in the US | announced (marketing page, not docs) |
| [Perplexity Comet][comet] | Launch post dated 2025-07-09 (Max subscribers first); the [product page][comet-page] (dated 2026-03-11) lists downloads for Mac, Windows, iOS and Android, read 2026-11-22; pricing not confirmed | announced (launch post), documented (download page) |

Our reading: the category is moving fast enough that a product page is a poor long-term anchor
(Atlas is an example). Other agentic browsers (Opera Neon, Dia, Edge Copilot Mode) were not verified
at first party in this pass (the Edge page returned 404) and are left out.

Framework side, from repo metadata on 2026-11-19: [browser-use][bu-gh] (MIT, 121,474 stars),
[Stagehand][stagehand-gh] (MIT, 26,095 stars) and [steel-browser][steel-gh] (Apache-2.0, 7,989
stars). Details of the first two are in the existing
[alternatives table](../../cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md#alternative-mcp-options-brief);
the scraping catalog covers [Magnitude, Lightpanda and the accessibility-tree approach][scrape-cat].

## Claude in Chrome vs DevTools MCP vs Playwright MCP

As of 2026-11-19. Versions and licences from the GitHub API (licence file detected as Apache-2.0 for
both Model Context Protocol (MCP) servers); behaviour from each project's own docs.

| Aspect | Claude in Chrome | Chrome DevTools MCP | Playwright MCP |
| ------ | ---------------- | ------------------- | -------------- |
| Run by | Anthropic | Chrome DevTools team ([`ChromeDevTools` org][dt-gh]) | Microsoft ([`microsoft` org][pw-gh]) |
| Form | Chrome extension (side panel; also tools inside Claude Code and Cowork) | MCP server and CLI, npm `chrome-devtools-mcp`, latest release v1.13.0 (2026-11-11) | MCP server, latest release v0.0.86 (2026-11-18); its README also points coding agents to a separate CLI-plus-skills tool |
| Licence | proprietary extension | Apache-2.0 | Apache-2.0 |
| How it drives the browser | Extension acts in your Chrome tabs; [Claude Code docs][cc-chrome] say it opens new tabs in a tab group | Puppeteer for automation plus DevTools for traces, network, console | Playwright with structured accessibility snapshots; "No vision models needed" per README |
| Session and logins | Your real browser, shares your login state; pauses on login pages and CAPTCHAs (Claude Code docs) | Own profile by default (`$HOME/.cache/chrome-devtools-mcp/chrome-profile`); `--autoConnect` attaches to a local Chrome 144+ with remote debugging on ([config][dt-cfg]) | README describes a persistent profile under a per-workspace cache path (its option table says a temporary directory when `--user-data-dir` is unset, so the README is not consistent); `--isolated` keeps it in memory; `--extension` attaches to a running Chrome or Edge |
| Headless | No; actions run in a visible window (Claude Code docs) | `--headless` option | `--headless` option (headed by default) |
| Browsers | Chrome and Edge; other Chromium browsers are described differently by two Anthropic pages, see the [extension analysis](../../cc-native/plugins-ecosystem/CC-chrome-extension-analysis.md) | Chrome and Chrome for Testing officially | `--browser` values chrome, firefox, webkit, msedge |
| Safety controls | Approval modes, classifiers, site lists: see the [extension analysis](../../cc-native/plugins-ecosystem/CC-chrome-extension-analysis.md#safety) | README disclaimer: exposes browser content to the client; no permission layer described | README says it is "not a security boundary"; origin allow and block flags documented as not security boundaries |
| Needs | Paid Anthropic plan; prerequisites and limits in the [extension analysis](../../cc-native/plugins-ecosystem/CC-chrome-extension-analysis.md) | Chrome | Node, a browser |
| Telemetry | not stated in the docs read | usage statistics on by default, opt out with a flag; CrUX lookups for traces | not checked |

Our reading: pick by the job. Claude in Chrome for work in sessions you are already signed in to;
DevTools MCP for debugging and performance traces of a page you build; Playwright MCP for repeatable
automation and test-like flows, with the profile kept isolated. None of the three is a sandbox.
Existing corpus coverage: [Chrome extension analysis](../../cc-native/plugins-ecosystem/CC-chrome-extension-analysis.md),
[Playwright MCP section](../../cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md#playwright-mcp-server).

## WebMCP

**What it is (documented).** The [WebMCP repository][webmcp-gh] describes a way for a web page to
register JavaScript tools, each with a description and a schema, so that an agent (built into the
browser, in an iframe or in an extension) can call them instead of clicking through the UI. The
README examples use `document.modelContext.registerTool`; a declarative form-based API is listed as
exploration. Chrome's [WebMCP docs][webmcp-chrome] call it "a proposed web standard".

**Who specifies it (documented).** The spec source ([`index.bs`][webmcp-bs]) is marked `CG-DRAFT`
and lists editors from Microsoft and Google; the repository sits in the `webmachinelearning` org
(the W3C Web Machine Learning Community Group). The licence file says reports are under the W3C
Software and Document License (GitHub shows the licence as unrecognised). The spec text points to a
proposed Agentic Web Working Group charter (a draft) for broader agent identity and permission work.
A community group draft is not a W3C Recommendation.

**Status (documented, repo file read 2026-11-19).** Per the [implementation-status file][webmcp-status]:
Chrome origin trial live in Chrome 149 (Chrome's [origin-trial post][webmcp-ot] is dated 2026-06-09), Edge origin trial
in Edge 150, a local flag for development, Brave support in its Leo chat expected in a release
planned for 2027-01-05, ChatGPT Desktop listed as supported, and only standards-position issues for
Firefox and Safari. Chrome's own docs page was last updated 2026-10-07.

**Security (documented).** The [security questionnaire][webmcp-sec] states that malicious tools can
ask for more personal data than needed through their parameters, that the spec "does not include
normative guidance" against misuse of sensitive tools, and that a hint for consequential actions is
planned (issue 176).

**Our reading.** WebMCP shifts effort from the agent (guess what a page does) to the site author
(declare it), the same trade MCP made for backends. It only helps on sites that adopt it; today
that means origin-trial pages, so general browser agents still need the pixel or DOM route.

## Hosted agent browsers

Only items checked at first party here; infrastructure already in the [scraping catalog][scrape-cat]
(Browserbase, Steel, Hyperbrowser, TinyFish pricing and anti-bot detail) is not repeated.

- Open-source cores checked at the GitHub API on 2026-11-19 (licences and stars in the framework
  paragraph above): [Stagehand][stagehand-gh] (Browserbase's SDK), [steel-browser][steel-gh]
  (Steel's browser API) and [browser-use][bu-gh] (its hosted vendor authored the self-reported
  benchmark row below).

Hosted-vendor pricing, concurrency and "anti-detection" claims were not re-verified here; use the
catalog's dated rows.

## Browser benchmarks with dates

| Benchmark | What it measures | Source and date |
| --------- | ---------------- | --------------- |
| WebArena | Self-hosted sites in four domains (e-commerce, forums, software development, content management); functional-correctness checks | [paper][webarena], submitted 2023-07-25 |
| WebVoyager | Real-site tasks on 15 popular websites with an automatic multimodal judge; the paper's own agent reached 59.1% | [paper][webvoyager], 2024-01-25 |
| Online-Mind2Web | 300 tasks on 136 live sites; WebJudge LLM judge with about 85% agreement with human judgement; paper argues earlier results were over-optimistic | [paper][om-paper], 2025-04-02; [repo][om-gh] |
| BrowseComp | 1,266 hard information-finding questions with short checkable answers; browsing persistence, not site operation | [paper][browsecomp], 2025-04-16 |
| VisBrowse-Bench | 169 visual-native search questions; best model in the paper, Claude-4.6-Opus, 47.6% | [paper][visbrowse], 2026-03-17 |
| HyWeBench | 100 hybrid search-and-operate tasks; HyWe-35B 47.0%; same paper reports 59.0% on Online-Mind2Web and 88.3% on WebVoyager | [paper][hywe], 2026-10-12 |

All paper figures are paper-reported (settings in the abstracts, not reproduced here).

**Online-Mind2Web scores are not one scale.** As of 2026-11-19:

- The [HAL leaderboard][hal] (Princeton) lists a top row of SeeAct with GPT-5 Medium at 42.33% and
  notes it has paused adding new models (the page marks its rows as reproduced by the HAL team).
- A [leaderboard aggregator run by Steel][steel-lb] (a hosted-browser vendor; page last updated
  2026-10-11) lists rows from 28.0% to 97.0%. Its top row, Browser Use Cloud at 97.0% (row dated Mar 2026 on the page), is
  self-reported with a custom agentic judge that the page says is not directly comparable to a
  screenshot-based judge (vendor claim). Another row, ChatGPT Atlas agent mode at 71.0% (Mar 2026), is
  OpenAI-reported with no public run data (vendor claim); Atlas is now deprecated per its launch
  page, so the figure is historical.
- The repo's changelog records a 2026-05-23 move to a v2 submission schema and outsourced human
  evaluation, so older leaderboard rows and new ones may not share a protocol.

Our reading: compare only within one judge and harness; treat any 90%-plus Online-Mind2Web figure as
a statement about that vendor's judge until run data is public.

## Safety: prompt injection from web content

- **Claude in Chrome (documented, vendor-internal numbers).** Layers, approval modes and Anthropic's
  reported attack-success figures are in the [extension analysis](../../cc-native/plugins-ecosystem/CC-chrome-extension-analysis.md#safety).
- **ChatGPT Atlas (documented).** OpenAI's [hardening post][atlas-hard] (2025-12-22) describes
  automated red teaming with reinforcement learning and a rapid-response loop, and says
  deterministic guarantees are hard (read via a fallback fetcher; the product is now deprecated).
- **Playwright MCP and DevTools MCP (documented).** Both READMEs disclaim security boundaries:
  origin filters are not boundaries and browser content is exposed to the client.
- **Research (paper).** [Veer][veer] (2026-09-28) targets deceptive interfaces: it changes the page
  state before a risky action instead of blocking the agent, and reports the highest safe task
  completion on two benchmarks it builds or uses (TrickyArena, WebDecept; abstract only).
- **WebMCP** adds a second trust problem: tools declared by a page are page-controlled input (see
  its [security questionnaire][webmcp-sec]).

Operating rule (our reading): use an isolated profile, allow-list sites, and keep banking, health
and credential flows away from any agent-driven browser. Cross-reference:
[vulnerability landscape](../../sdlc-lcm/agentic-ai-vulnerability-landscape.md).

## Sources

| Source | Content |
| ------ | ------- |
| [Claude Code with Chrome docs][cc-chrome] | `--chrome`, `/chrome`, prerequisites, permissions, ZDR/HIPAA (read 2026-11-19) |
| [Claude in Chrome product page][cfc], [GA post][cfc-ga] | Availability, GA date, safety evaluation |
| [Use Claude in Chrome safely][cfc-safe], [permissions guide][cfc-perm], [2025 injection post][pi-post] | Risks, modes, classifiers, internal numbers |
| [Chrome DevTools MCP][dt-gh], [config doc][dt-cfg] | Features, flags, licence, release |
| [Playwright MCP][pw-gh] | Features, flags, licence, release |
| [WebMCP repo][webmcp-gh], [spec source][webmcp-bs], [status][webmcp-status], [security][webmcp-sec], [Chrome docs][webmcp-chrome], [origin trial post][webmcp-ot] | WebMCP proposal and status |
| [Atlas launch][atlas], [Atlas hardening][atlas-hard], [Gemini in Chrome][gem-chrome], [Comet launch][comet], [Comet page][comet-page] | Agentic browser state |
| [browser-use][bu-gh], [Stagehand][stagehand-gh], [steel-browser][steel-gh] | Licence, stars, activity |
| [WebArena][webarena], [WebVoyager][webvoyager], [Online-Mind2Web][om-paper], [repo][om-gh], [BrowseComp][browsecomp] | Benchmarks |
| [HAL][hal], [Steel aggregator][steel-lb] | Online-Mind2Web leaderboards |
| [VisBrowse-Bench][visbrowse], [HyWe][hywe], [Veer][veer] | 2026 paper leads |

[scrape-cat]: ../infrastructure/web-scraping-extraction-landscape.md
[cc-chrome]: https://code.claude.com/docs/en/chrome
[cfc]: https://claude.com/claude-for-chrome
[cfc-ga]: https://claude.com/resources/articles/claude-in-chrome-generally-available
[cfc-safe]: https://support.claude.com/en/articles/12902428-using-claude-for-chrome-safely
[cfc-perm]: https://support.claude.com/en/articles/12902446-claude-for-chrome-permissions-guide
[pi-post]: https://www.anthropic.com/research/prompt-injection-defenses
[dt-gh]: https://github.com/ChromeDevTools/chrome-devtools-mcp
[dt-cfg]: https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/configuration.md
[pw-gh]: https://github.com/microsoft/playwright-mcp
[webmcp-gh]: https://github.com/webmachinelearning/webmcp
[webmcp-bs]: https://github.com/webmachinelearning/webmcp/blob/main/index.bs
[webmcp-status]: https://github.com/webmachinelearning/webmcp/blob/main/implementation-status.md
[webmcp-sec]: https://github.com/webmachinelearning/webmcp/blob/main/security-privacy-questionnaire.md
[webmcp-chrome]: https://developer.chrome.com/docs/ai/webmcp
[webmcp-ot]: https://developer.chrome.com/blog/ai-webmcp-origin-trial
[atlas]: https://openai.com/index/introducing-chatgpt-atlas/
[atlas-hard]: https://openai.com/index/hardening-atlas-against-prompt-injection/
[gem-chrome]: https://gemini.google/overview/gemini-in-chrome/
[comet]: https://www.perplexity.ai/hub/blog/introducing-comet
[comet-page]: https://www.perplexity.ai/comet
[bu-gh]: https://github.com/browser-use/browser-use
[stagehand-gh]: https://github.com/browserbase/stagehand
[steel-gh]: https://github.com/steel-dev/steel-browser
[webarena]: https://arxiv.org/abs/2307.13854
[webvoyager]: https://arxiv.org/abs/2401.13919
[om-paper]: https://arxiv.org/abs/2504.01382
[om-gh]: https://github.com/OSU-NLP-Group/Online-Mind2Web
[browsecomp]: https://arxiv.org/abs/2504.12516
[hal]: https://hal.cs.princeton.edu/online_mind2web
[steel-lb]: https://leaderboard.steel.dev/leaderboards/online-mind2web/
[visbrowse]: https://arxiv.org/abs/2603.16289
[hywe]: https://arxiv.org/abs/2610.16319
[veer]: https://arxiv.org/abs/2609.34974
