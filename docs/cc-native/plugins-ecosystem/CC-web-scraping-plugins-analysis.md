---
title: CC Web Scraping Plugins — Firecrawl & Playwright MCP vs Built-in Tools
source: https://docs.firecrawl.dev/mcp-server
purpose: Evaluate Firecrawl and Playwright MCP plugins for web scraping in Claude Code, compared to built-in WebFetch/WebSearch tools.
created: 2026-03-12
updated: 2026-11-26
validated_links_on: 2026-11-19
status: research
---

## Context

Claude Code provides built-in web tools (WebSearch, WebFetch) for basic web access. Two prominent Model Context Protocol (MCP) plugins — **Firecrawl** and **Playwright** — extend these capabilities significantly. This analysis evaluates when each option is the right tool and whether the plugins justify their setup cost over the built-in tools.

## CC Plugin vs Raw MCP Server

Both Firecrawl and Playwright are available in **two forms**. The underlying MCP tools are identical — the plugin wraps them with slash commands and auto-activation hooks.

| | CC Plugin (`/plugin install`) | Raw MCP Server (`claude mcp add`) |
|---|---|---|
| **Install** | `/plugin` → search → install | `claude mcp add <name> npx ...` or `.claude/settings.json` |
| **Slash commands** | Yes (`/firecrawl:scrape`, `/firecrawl:agent`, etc.) | No — tools are model-invoked only |
| **Auto-activation** | Hooks trigger on web-related tasks | Manual invocation or model decides |
| **Bundled CLI** | Firecrawl plugin requires `npm install -g firecrawl-cli` | npx handles dependency |
| **Distribution** | Single installable unit (skills + MCP + hooks) | MCP server config only |
| **Portability** | Follows CC plugin system (per-user or per-project) | `.claude/settings.json` or `.mcp.json` |

**Rule of thumb**: Use the plugin for interactive development (slash commands, auto-activation). Use raw MCP for CI/headless (`claude -p`) or when you need fine-grained config control.

## Built-in Tools: WebSearch & WebFetch

### WebSearch

- Accepts a search query, returns page titles + URLs ([source][cc-webfetch-docs])
- Same backend as Claude.ai web search ([source][cc-plugins-docs])
- Supports `allowed_domains` and `blocked_domains` filtering
- Returns only titles and URLs — no page body content ([source][cc-webfetch-docs])
- **US-only** availability ([source][cc-system-prompts])
- No additional cost beyond standard token pricing ([source][webfetch-api-docs])

### WebFetch

**CC wrapper vs API tool**: CC's built-in WebFetch accepts a URL + question prompt and returns a **summarized answer** via a small model (likely Haiku). The API-level `web_fetch_20250910` tool returns **full document content** (text or base64 PDF) with optional citations ([source][webfetch-api-docs]).

- **Architecture**: HTTP fetch → HTML-to-markdown conversion → LLM summarization ([source][cc-system-prompts]). Specific HTML-to-markdown library not disclosed; community reimplementations use Mozilla Readability + Turndown or html2text ([source][openclaude-gh])
- **Security**: Claude cannot dynamically construct URLs — can only fetch URLs from user messages or prior search/fetch results ([source][webfetch-api-docs])
- **Cache**: 15-minute self-cleaning cache ([source][cc-system-prompts])
- **Size limit**: `maxContentLength: 10485760` (10MB) ([source][webfetch-pdf-issue])
- **HTTPS**: Automatic HTTP → HTTPS upgrade ([source][cc-system-prompts])
- **PDF fetching**: API tool returns base64-encoded PDF data with automatic text extraction ([source][webfetch-api-docs]). **CC's wrapper has a known bug**: returns raw binary for PDFs, causing model hallucination from binary fragments ([source][webfetch-pdf-issue]). Workaround: `curl` + `pdftotext` + `Read`
- **Dynamic filtering** (`web_fetch_20260209`; the latest version is `web_fetch_20260318`, which adds `response_inclusion`, and `web_fetch_20260309` adds cache bypass): Claude can write and execute code to filter fetched content before it enters context, reducing token consumption. Requires code execution tool. Available with Claude 4.6 and later models and Claude Mythos Preview; Microsoft Foundry deployments on Azure support only `web_fetch_20250910` (checked 2026-11-26) ([source][webfetch-api-docs])
- **No additional cost** beyond standard token pricing ([source][webfetch-api-docs]). Typical token usage: avg web page ~2,500 tokens, large doc ~25K, PDF ~125K ([source][webfetch-api-docs])

### Read Tool: PDF & Image Parsing

The built-in Read tool handles local PDFs and images natively:

- **PDFs**: Page-by-page text and visual content extraction. `pages` parameter required for >10 pages (e.g., `pages: "1-5"`), max 20 pages per request. Page-range reads render pages with `pdftoppm` from `poppler-utils` ([tools reference][cc-tools-reference], read 2026-11-27); earlier sources described poppler as used for text extraction ([source][webfetch-pdf-issue], [source][cc-system-prompts]); where a short PDF is parsed is not documented (see [Where media is processed](../../non-cc/coding-agents/coding-agents-comparison-landscape.md#where-media-is-processed))
- **Images**: Presented visually to the multimodal model (PNG, JPG, etc.). Input methods: drag-and-drop, Ctrl+V paste, or file path reference ([source][cc-common-workflows])
- **Jupyter notebooks**: Returns all cells with outputs, combining code, text, and visualizations ([source][cc-system-prompts])
- **Defaults**: 2,000 lines from start, 2,000 chars/line max ([source][cc-system-prompts])

### Limitations

| Limitation | Impact |
|---|---|
| No JavaScript rendering | Cannot scrape SPAs or dynamic content |
| No raw content output (CC wrapper) | Always summarized through LLM — API tool returns full content |
| No browser state | Cannot authenticate, fill forms, or navigate multi-step flows |
| No batch operations | One URL at a time |
| Two-step workflow | Must search, then fetch each result separately |
| Protected sites blocked | Anti-bot measures and CAPTCHAs block requests |
| PDF via WebFetch broken in CC | Returns raw binary, model hallucinates ([#23694][webfetch-pdf-issue]) |
| WebSearch US-only | Not available outside the United States |

### Native web stack as a pair — and its constraint floor

WebSearch and WebFetch are a **pair**: WebSearch *discovers* (result blocks — titles + URLs/snippets, no page body), WebFetch *reads* one URL. To read a result you hand its URL to WebFetch — so every WebFetch fetch-side limit applies the moment you follow a search result. Both are **model-mediated** (output is summarized markdown, not raw HTML — see the WebFetch architecture above) and **cached ~15 min per URL**. Beyond that, they share a constraint floor that no input can configure around — the gap the heavier tiers exist to fill: Firecrawl / Playwright (below).

| Constraint (beyond the Limitations table above) | Detail | Source |
|---|---|---|
| No request-header control | Inputs are only `url` + `prompt` — no custom `User-Agent`, `Referer`, or `Accept`, so header/UA-gated blocks can't be coaxed past | [tools reference][cc-tools-reference] |
| No anti-bot bypass | Bot-protected sites return `403`; with no header control (and TLS/JA3 fingerprinting in play) there is no way around it | observed; [tools inventory][cc-tools-inventory] |
| Auth/private URLs fail | Errors on authenticated/private URLs — use an authenticated tool (e.g. `gh`) instead | [tools reference][cc-tools-reference] |
| Cross-host redirects not followed | Returned to you to re-invoke WebFetch with the new URL | [system prompt][cc-system-prompts] |
| HTTP → HTTPS upgrade | Plain-HTTP URLs are auto-upgraded before fetch | [system prompt][cc-system-prompts] |

WebSearch adds two of its own: **US-only** region-locking (the API `web_search` tool exposes a `user_location` parameter; the Claude Code built-in does not), and **domain filtering as the only operator** (`allowed_domains` / `blocked_domains`; no other query operators beyond the search string). Both per the [web search tool][websearch-api-docs] docs.

## Firecrawl MCP Server

### What It Is

A cloud-hosted (or self-hostable) web scraping API exposed as an MCP server. Turns any website into clean, LLM-ready markdown or structured JSON with automatic anti-bot handling and proxy rotation ([source][firecrawl-mcp-docs]).

### Setup

**As CC Plugin** (recommended for interactive use):

```bash
# /plugin → search "firecrawl" → install, then:
npm install -g firecrawl-cli    # required CLI dependency
/firecrawl:setup                # configure API key interactively
```

Slash commands: `/firecrawl:scrape`, `/firecrawl:crawl`, `/firecrawl:search`, `/firecrawl:map`, `/firecrawl:agent` ([source][firecrawl-plugin], [source][firecrawl-plugin-gh]).

**As raw MCP server** (for CI/headless or config control):

```bash
claude mcp add firecrawl -e FIRECRAWL_API_KEY=your-api-key -- npx -y firecrawl-mcp
```

```json
{
  "mcpServers": {
    "firecrawl-mcp": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

([source][firecrawl-mcp-gh])

### Available Tools

| Tool | Purpose | Returns |
|---|---|---|
| `firecrawl_scrape` | Single-page content extraction | JSON / markdown / raw HTML |
| `firecrawl_map` | Discover all URLs on a site (sitemap + crawl) | URL array |
| `firecrawl_crawl` | Multi-page async crawling with depth control | Markdown / HTML array |
| `firecrawl_search` | Web search with optional result scraping | Search results array |
| `firecrawl_agent` | Autonomous multi-source research agent | Structured JSON |
| `firecrawl_interact` / `firecrawl_interact_stop` | Interactive browser session and its shutdown (replaces the former `firecrawl_browser`) | Live session control |

Checked 2026-11-26: the hosted tools page and the local server README no longer list `firecrawl_batch_scrape`, `firecrawl_extract` or `firecrawl_browser`, and the hosted page says the former Extract tool is deprecated. The surface also includes `firecrawl_parse`, `firecrawl_check_crawl_status`, `firecrawl_agent_status`, research, monitor and credit-usage tools, and varies by connection mode, plan and team policy ([source][firecrawl-mcp-docs], [source][firecrawl-mcp-gh]).

### Key Features

- **Anti-bot handling**: Automatic proxy rotation, JavaScript rendering, CAPTCHA handling ([source][firecrawl-mcp-docs])
- **Clean output**: Strips ads, navigation, footers — returns only content ([source][firecrawl-ai-mcps])
- **Self-hosted option**: Set `FIRECRAWL_API_URL` for private instances ([source][firecrawl-mcp-gh])
- **Credit monitoring**: Warning at 1000, critical at 100 credits (configurable; unverified) ([source][firecrawl-mcp-gh])
- **Retry with backoff**: Configurable max attempts, delay, backoff factor ([source][firecrawl-mcp-gh])

### Pricing

- **Free tier**: 1,000 credits per month, no credit card required, described as monthly rather than lifetime (checked 2026-11-26) ([source][firecrawl-pricing])
- **Rate limits (free)**: 10/min each for scrape, map and search, 2/min for crawl, and 2 concurrent browsers (checked 2026-11-26) ([source][firecrawl-pricing])
- **Paid tiers** (checked 2026-11-26): Hobby $19 (5,000 credits), Standard $99 (100,000), Growth $399 (500,000), Scale $749 (1,000,000), Enterprise custom; annual billing is cheaper ([source][firecrawl-pricing])
- **Self-hosted**: No credit cost; requires Docker Compose (5 containers: API, Redis, RabbitMQ, PostgreSQL, Playwright-service) ([source][firecrawl-self-host])

### Hosted Connector Route (ChatGPT and Claude)

Besides the local `firecrawl-mcp` server and the plugin, Firecrawl ships hosted connectors that sign in with a Firecrawl account instead of an API key (evidence: documented and shipped per Firecrawl's own pages, read 2026-11-24; Firecrawl's claims, not independently tested):

- **Claude**: a connector in Claude's directory (listed as Firecrawl-made marked "Anthropic verified", added July 2026, per the [Claude connector listing][firecrawl-claude-connector]). Connect, sign in in the browser, pick a team, approve; no API key ([Claude integration page][firecrawl-claude-integration]). The listing shows 13 tools while the integration page says eight (search, scrape, Alexandria (Firecrawl's data-provider layer) discovery, Developer Index search, four paper-research tools), so treat the count as unstable. Alexandria in Claude was announced 2026-09-24 ([changelog][firecrawl-alexandria-claude]).
- **ChatGPT**: a Firecrawl plugin, announced 2026-08-05 ([blog][firecrawl-chatgpt-plugin]; tools: search, scrape, crawl, interact, monitor, Alexandria), with Alexandria added 2026-09-29 ([blog][firecrawl-alexandria-chatgpt]). The blog says it installs "directly inside ChatGPT" and links a chatgpt.com plugin page, which we could not load to confirm.
- **Other harnesses (MCP)**: the hosted server takes either OAuth sign-in or an API key as bearer token; both reach the full tool set on the team's plan ([MCP docs][firecrawl-mcp-docs], [Alexandria page][firecrawl-alexandria-site]). Endpoints are on the vendor's pages.
- **Billing**: credits, as with the API (about 1 credit per scraped page, +4 for JSON format, per the Claude integration page). Alexandria needs an authenticated account (no keyless access); discovering tools is free and each call is charged at the tool's listed credit price; some providers need an org admin to accept their terms first.
- **Provider count**: Firecrawl's own figures differ by page and date; see [Universal Scrape in the landscape](../../non-cc/infrastructure/web-scraping-extraction-landscape.md#aillm-native-scrapers).

### Cloud vs Self-Hosted vs firecrawl-simple

| Feature | Cloud | Self-hosted | firecrawl-simple |
|---|---|---|---|
| `/scrape`, `/crawl` | Yes | Yes | Yes |
| `/map`, `/search` | Yes | Yes | No |
| `/extract` (LLM) | Yes | Needs external LLM | No |
| `/agent`, `/browser` | Yes | **No** (cloud-only) | No |
| Fire-engine (anti-bot, proxy rotation) | Yes | **No** (cloud-only) | No (uses Hero browser) |
| CAPTCHA solving | Yes | No | Via 2captcha config |
| API key required | Yes | Buggy — [still enforced][firecrawl-key-bug] | No |
| Billing/auth | Built-in | Optional | Removed |
| Infra | Managed | Docker (5 containers) | Docker (Redis + API + workers) |

**Key gap**: Fire-engine (anti-bot, IP rotation) and `/agent` + `/browser` endpoints are **cloud-exclusive**. Self-hosted is effectively scrape + crawl + map with Playwright rendering. [firecrawl-simple][firecrawl-simple] is a community fork ([devflowinc][firecrawl-simple]) that strips billing, AI, and heavy dependencies — scrape + crawl only ([source][firecrawl-self-host], [source][firecrawl-simple]).

### Limitations

- **API key required for the REST API** — the hosted MCP server also accepts OAuth sign-in or keyless connections limited to search, scrape and parse within daily limits (checked 2026-11-26); self-hosted has a [persistent bug][firecrawl-key-bug] enforcing it. Workaround: dummy key (`api_key="no-key"`)
- **Credit consumption** — the free allowance (1,000 credits per month, checked 2026-11-26) can exhaust quickly during development
- **Latency** — cloud round-trip adds overhead vs local tools
- **Privacy** — page content passes through Firecrawl's cloud (unless self-hosted)

### Prometheus (natural-language collector builder)

[Prometheus][firecrawl-prometheus] is Firecrawl's agent-style layer over the scrape/crawl API: describe the data you want in plain English and it generates **reproducible Firecrawl SDK "collector" code plus sample output**, which you can run standalone or deploy on Firecrawl's infrastructure on a schedule with automated maintenance. The flow is three steps — **Ask** (describe the data), **Keep** (get collector code + sample data), **Deploy** (optional scheduled runs) — and requires a connected Firecrawl account ([source][firecrawl-prometheus]).

**vs the MCP tools above**: the `firecrawl_*` MCP tools are imperative calls Claude makes per request; Prometheus is a higher-level *codegen + scheduling* layer that emits durable SDK collectors (distinct from the request-time `firecrawl_agent` tool). For Claude Code, the MCP server stays the integration surface — Prometheus is relevant when you want a maintained, scheduled pipeline rather than ad-hoc scrapes. Pricing, endpoints, and GA status are not stated on the landing page.

## Playwright MCP Server

### What It Is

Microsoft's official MCP server that provides full browser automation using Playwright. Interacts with pages through structured accessibility snapshots — no vision model needed. **Runs a local Chromium process** on your machine — no cloud service, no API key, no credit cost. Optional remote mode via `--port` for Docker/server setups, or `--cdp-endpoint` to attach to an existing browser ([source][playwright-mcp-gh]).

**2026-11-19:** Apache-2.0, 39,884★, latest release `v0.0.86` (2026-11-18) (`gh api`; was 38,557★ and `v0.0.83` on 2026-10-24). Flags are in the options table below (it also has `--extension` to attach to a running Chrome or Edge). Side-by-side with Claude in Chrome and DevTools MCP: [browser-agents-landscape.md](../../non-cc/agents/browser-agents-landscape.md#claude-in-chrome-vs-devtools-mcp-vs-playwright-mcp). It is one of the two MCP servers "enabled by default" for GitHub's Copilot cloud agent ([github-copilot-cloud-agent-analysis.md § MCP servers](../../non-cc/agents/github-copilot-cloud-agent-analysis.md#mcp-servers)). Its README now states "Playwright MCP is not a security boundary" and that "Modern coding agents increasingly favor CLI–based workflows exposed as SKILLs over MCP" ([source][playwright-mcp-gh]).

### Setup

**As CC Plugin** (118k+ installs, by Microsoft):

```bash
# /plugin → search "playwright" → install
# No API key, no CLI dependency — works immediately
```

Ask Claude naturally: "navigate to example.com and take a screenshot" ([source][playwright-plugin]).

**As raw MCP server** (for config control, headless, codegen):

```bash
claude mcp add playwright npx @playwright/mcp@latest

# Headless mode
claude mcp add playwright npx @playwright/mcp@latest --headless
```

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

([source][playwright-mcp-gh])

### Capabilities (Tool Groups)

| Capability | Description | Tools |
|---|---|---|
| `core` (default) | Navigation, clicks, form fill, snapshots, tabs, file ops | ~20 tools |
| `vision` | Coordinate-based mouse interactions (click x,y) | Mouse click/move/drag/wheel at coordinates |
| `pdf` | PDF generation from pages | Save as PDF |
| `devtools` | Console access, network monitoring | DevTools interaction |

Enable via `--caps=core,vision,pdf` or config file ([source][playwright-mcp-gh]).

### Key Features

- **Accessibility tree snapshots**: 2-5KB structured data vs screenshots — 10-100x less tokens ([source][playwright-mcp-gh])
- **No vision model needed**: Operates on structured data, not pixels ([source][playwright-mcp-gh])
- **Deterministic references**: Element references are unique and stable — no coordinate ambiguity ([source][playwright-mcp-gh])
- **Full browser control**: Navigation, form filling, authentication, file upload/download
- **Multiple browsers**: `--browser` takes chrome, firefox, webkit or msedge ([source][playwright-mcp-gh])
- **Persistent profiles**: Reuse browser profiles with cookies/storage across sessions ([source][playwright-mcp-gh])
- **Code generation**: Pass `--codegen typescript` to generate Playwright test scripts as Claude navigates ([source][simonwillison-til])
- **Local execution**: No API key, no cloud dependency, no credit cost
- **Browser extension mode**: Connect to existing browser tabs with logged-in sessions ([source][playwright-mcp-gh])

### Configuration Options

| Option | Description | Default |
|---|---|---|
| `--browser` | chrome / firefox / webkit / msedge | not stated in the README table (2026-11-19) |
| `--headless` | Run without visible window | false (headed) |
| `--viewport-size` | Browser dimensions | 1280x720 |
| `--device` | Emulate device (e.g., "iPhone 15") | — |
| `--user-data-dir` | Browser profile path | README option table: temp dir if unset; README prose: persistent per-workspace cache profile (inconsistent) |
| `--isolated` | Keep profile in memory only | false |
| `--storage-state` | Load cookies/storage from file | — |
| `--config` | JSON config file for complex setups | — |
| `--timeout-action` | Action timeout (ms) | 5000 |
| `--timeout-navigation` | Navigation timeout (ms) | 60000 |

([source][playwright-mcp-gh])

### Limitations

- **Token cost**: Complex pages produce large accessibility trees (though still much smaller than screenshots)
- **Local resource usage**: Runs a real browser — CPU/memory cost
- **No anti-bot bypass**: No proxy rotation or CAPTCHA solving — blocked by protected sites
- **Privacy**: All page content Claude sees goes to Anthropic's API ([source][simonwillison-til])
- **Headless restrictions**: Some sites detect headless browsers

## Using the Plugins

### Firecrawl Plugin Usage

**Slash commands** invoke specific operations; **natural language** lets Claude pick the right tool automatically.

| Method | Example |
|---|---|
| `/firecrawl:scrape` | Prompts for a URL, extracts clean markdown |
| `/firecrawl:crawl` | Prompts for a URL, recursively extracts an entire site |
| `/firecrawl:search` | Prompts for a query, searches web + scrapes results |
| `/firecrawl:map` | Prompts for a URL, discovers all URLs on the site |
| `/firecrawl:agent` | Describe what you need in plain language — no URLs required |
| Natural language | "Scrape <https://docs.stripe.com> and explain webhook setup" |

**Agent mode**: Claude evaluates your request and selects the right Firecrawl tool automatically. You describe the goal; it handles tool selection, pagination, and multi-site navigation.

**Output**: Results save to `.firecrawl/` directory (e.g., `search-query.json`, `domain-name.md`) to avoid cluttering context.

**Example workflows**:

```text
# Research aggregation
"Search for 'AI agent frameworks 2026' and compile the top 5 with pros/cons"

# Structured extraction
"Scrape all event listings from https://luma.com/discover and structure as JSON
 with title, date, location, url"

# Site-wide ingestion
"Crawl https://docs.pydantic.dev and summarize the validation patterns"

# Autonomous research
/firecrawl:agent → "Find all upcoming SF tech meetups across luma, meetup, and
eventbrite. Return title, date, venue, and registration URL."
```

### Playwright Plugin Usage

**No slash commands** — interact via natural language. Claude opens a browser and performs actions through accessibility tree snapshots (not screenshots).

**Example prompts**:

```text
# Navigation + extraction
"Navigate to meetup.com/find/?keywords=san+francisco, take a snapshot of the
 event listings"

# Form filling
"Go to luma.com, click 'Explore Events', type 'San Francisco' in the location
 filter, and list the results"

# Auth flow
"Navigate to meetup.com/login, fill email with X and password with Y, click
 Sign In, then go to my groups page"

# Testing + debugging
"Navigate to localhost:3000, fill the contact form with test data, submit,
 and check the console for errors"

# Screenshot capture
"Take a screenshot of https://example.com after the page fully loads"
```

**Key behavior**: Playwright operates on the accessibility tree (structured element data), not pixels. Claude sees element roles, labels, and refs — then issues deterministic click/type commands. This means ~2-5KB per page snapshot vs ~100KB+ for screenshots.

### Combined Workflow

For event scraping across multiple sites:

1. **Firecrawl** `/firecrawl:map` → discover all event URLs on luma.com
2. **Firecrawl** `/firecrawl:agent` → "extract structured event data from these URLs"
3. **Playwright** → log into Meetup, navigate to private group events, extract listings
4. **Firecrawl** `/firecrawl:scrape` → grab individual event detail pages for full descriptions

## Comparison Matrix

| Capability | WebFetch/WebSearch | Firecrawl MCP | Playwright MCP |
|---|---|---|---|
| **Setup complexity** | None (built-in) | Low (API key + npx, or hosted OAuth) | Low (npx, no key) |
| **JavaScript rendering** | No | Yes (cloud) | Yes (local browser) |
| **Raw content access** | No (summarized only) | Yes (markdown, JSON, HTML) | Yes (accessibility tree, HTML) |
| **Batch scraping** | No | Yes (crawl; `batch_scrape` no longer listed) | No (one page at a time) |
| **Site crawling/mapping** | No | Yes (crawl, map tools) | No |
| **Structured extraction** | No | Extract tool deprecated (checked 2026-11-26) | No |
| **Form filling / auth** | No | Via interact tool | Yes (full browser control) |
| **Anti-bot / CAPTCHA** | No | Yes (proxy rotation, anti-bot) | No |
| **Search integration** | Yes (WebSearch) | Yes (firecrawl_search) | No |
| **Cost** | Free (included) | Credits (1,000 free per month, checked 2026-11-26) | Free (local) |
| **API key required** | No | Yes (REST API, cloud) / OAuth or limited keyless (hosted MCP) / No (self-hosted) | No |
| **Privacy** | Content → Anthropic | Content → Firecrawl + Anthropic | Content → Anthropic |
| **Self-QA (localhost)** | Limited | No (cloud can't reach localhost) | Yes (local browser) |
| **Test code generation** | No | No | Yes (--codegen) |
| **Token efficiency** | Low (LLM-summarized) | Medium (clean markdown) | Good (accessibility tree) |

## Decision Framework

### Use Built-in WebFetch/WebSearch When

- Checking documentation or static pages occasionally
- Quick searches during development
- No extra setup desired
- Content is static and publicly accessible

### Use Firecrawl MCP When

- **Batch scraping** multiple URLs or crawling entire sites
- **Structured data extraction** from web pages (via schemas)
- Need **anti-bot bypass** (proxy rotation, CAPTCHA handling)
- **Research agents** that autonomously gather multi-source data
- Content is behind JavaScript rendering but not login walls
- Willing to use cloud API (or self-host)

### Use Playwright MCP When

- **Interactive workflows**: form filling, multi-step navigation, authentication
- **Self-QA**: testing your own app on localhost
- **Dynamic content** that requires a real browser
- **Test code generation** from exploratory navigation
- Need **full browser control** without API key or cloud dependency
- Working with **logged-in sessions** (browser extension mode)

### Combined Approach (Recommended)

The tools are complementary, not competing:

1. **WebFetch** for quick doc lookups (zero setup)
2. **Firecrawl** for bulk scraping and research (API key, credits)
3. **Playwright** for interactive testing and auth-gated content (local, free)

## Is Firecrawl/Playwright Better Than Just Using Claude Code?

**For basic web access**: No. Built-in WebFetch + WebSearch handles 80% of developer web needs — checking docs, verifying APIs, searching for solutions. No setup required.

**For scraping at scale**: Yes, Firecrawl is significantly better. Batch operations, site crawling, anti-bot handling, and structured extraction are capabilities WebFetch simply doesn't have.

**For interactive/dynamic content**: Yes, Playwright is significantly better. JavaScript rendering, form interaction, authentication, and localhost testing are impossible with WebFetch.

**For research workflows**: Firecrawl's autonomous agent (`firecrawl_agent`) can independently browse and extract from multiple sources — a capability neither WebFetch nor Playwright offers out-of-the-box.

**Bottom line**: The built-in tools are sufficient for casual web access during coding. The plugins unlock fundamentally different capabilities — bulk data extraction (Firecrawl) and interactive browser automation (Playwright) — that the built-in tools cannot replicate.

## Alternative MCP Options (Brief)

Beyond Firecrawl and Playwright MCP, several agent-browser tools are worth noting. License/language are first-party (GitHub repo metadata, checked 2026-07-10); token-efficiency figures are one community benchmark ([source][devto-browser-tools]) — indicative, not first-party. The load-bearing axis is **representation**: most converge on the **accessibility tree** — the same structured role/name view Playwright MCP uses (see *Key behavior* and the Comparison Matrix above), which is why their per-page token cost lands well below a screenshot-driven agent.

| Tool | License (lang) | Representation | Token eff. (community) | Best for |
|---|---|---|---|---|
| [agent-browser][agent-browser-gh] (Vercel) | Apache-2.0 (Rust CLI + MCP) | Accessibility tree (`@e1` refs) | 3–5K tokens/page | Backup browser automation; standalone CLI |
| [Chrome DevTools MCP][chrome-devtools-mcp-gh] (Google) | Apache-2.0 (TS) | A11y-tree snapshot over raw CDP | ~10K tokens/page | Raw DevTools access; perf traces; latest release v1.14.0 (2026-11-24, checked 2026-11-26), `--autoConnect` to a local Chrome 144+ (README/config, 2026-11-19) |
| [Stagehand][stagehand-gh] (Browserbase) | MIT (TS + Python) | Accessibility tree + DOM hybrid | n/a | `act()`/`extract()`/`observe()` over a browser |
| [browser-use][browser-use-gh] | MIT (Python) | Custom numbered-DOM map (**not** the native a11y tree) | ~10K tokens/page | Complex autonomous form-filling |
| [jev-ultrafast][jev-ultrafast-gh] (browser-use) | MIT (Python) | Indexed element table (operations + targets), no a11y tree | n/a — one [Jev][typesafe-jev-web] decision request per step, not a token-cost model | Fast, cheap DOM-action selection with no per-step LLM reasoning |
| PinchTab | unverified | unverified | ~800 tokens/page (best) | Daily lightweight browsing |

**jev-ultrafast** is a separate browser-use project, not a browser-use option/flag: each step asks
TypeSafe's Jev decision model to pick an operation (`CLICK`, `TYPE_TEXT`, `SELECT`, `SCROLL_UP`,
`SCROLL_DOWN`, `WAIT`, `DONE`, `BLOCKED`) and a target from the current element table in one
request; a small LLM writes text only when the operation is `TYPE_TEXT`. Its own README reports a
Google Flights search completed in 7.1 s from first prediction to the accepted DONE choice (browser
setup, initial navigation and independent post-run verification are excluded from the clock) and a
25% median task-time reduction over an earlier, unoptimized build of jev-ultrafast itself (both
versions already used TypeSafe's Jev decision model and Mercury), but hedges this is "three repeats
of one task on one browser profile, not a general reliability benchmark." It is not open-weight — it is a client of the
hosted Jev API plus a hosted text LLM (OpenRouter). See the wider comparison in
[system-1-decision-models-landscape.md § Tools built on Jev][decision-models-landscape].

**Counterexamples (not a11y-tree-based):** Anthropic Computer Use and OpenAI Operator drive the browser from **screenshots + pixel coordinates**, not structured element data — no dependency on the page exposing a clean a11y tree, at higher token/latency cost. For the raw-library API behind the accessibility-tree representation (Playwright 1.57 `aria_snapshot`, Patchright version gate), see the [scraping-landscape catalog](../../non-cc/infrastructure/web-scraping-extraction-landscape.md#accessibility-tree-page-representation).

## Actionable Recommendations

### Immediate (Tier 1)

- **Add Playwright MCP** to development setup — free, no API key, enables self-QA and interactive debugging. Setup: `claude mcp add playwright npx @playwright/mcp@latest --headless`

### Short-term (Tier 2)

- **Add Firecrawl MCP** when research or data extraction tasks arise — free tier (1,000 credits per month, checked 2026-11-26) sufficient for evaluation. Setup: `claude mcp add firecrawl -e FIRECRAWL_API_KEY=key -- npx -y firecrawl-mcp`

### Deferred (Tier 3)

- **Self-host Firecrawl** if scraping volume exceeds free tier or privacy requirements mandate it
- **Evaluate PinchTab** as a lighter-weight Playwright alternative for token-constrained contexts

## Engine-layer view (added 2026-04-26 per #132)

For the Python-library landscape behind web crawling and source connectors (polyfetch-scrape, trafilatura, scrapy, httpx, watchdog, plus SharePoint/Confluence/Drive/S3/IMAP connectors), see [doc-pipeline-engine / landscape/ingest.md](https://github.com/qte77/doc-pipeline-engine/blob/main/docs/landscape/ingest.md). This file covers the CC orchestration layer above those tools.

## References

### First-Party

- [Firecrawl MCP Docs][firecrawl-mcp-docs]
- [Firecrawl MCP Server (GitHub)][firecrawl-mcp-gh]
- [Firecrawl Claude Plugin (Marketplace)][firecrawl-plugin]
- [Firecrawl Claude Plugin (GitHub)][firecrawl-plugin-gh]
- [Firecrawl Pricing][firecrawl-pricing]
- [Firecrawl Use Cases — AI MCPs][firecrawl-ai-mcps]
- [Firecrawl Prometheus][firecrawl-prometheus]
- [Firecrawl Claude connector listing][firecrawl-claude-connector] · [Claude integration page][firecrawl-claude-integration] · [Alexandria in Claude (changelog, 2026-09-24)][firecrawl-alexandria-claude]
- [Firecrawl ChatGPT plugin (blog, 2026-08-05)][firecrawl-chatgpt-plugin] · [Alexandria in ChatGPT and Codex (blog, 2026-09-29)][firecrawl-alexandria-chatgpt] · [Alexandria catalog][firecrawl-alexandria-site]
- [Playwright MCP (GitHub)][playwright-mcp-gh]
- [Playwright Claude Plugin (Marketplace)][playwright-plugin]
- [agent-browser (GitHub)][agent-browser-gh]
- [Chrome DevTools MCP (GitHub)][chrome-devtools-mcp-gh]
- [Stagehand (GitHub)][stagehand-gh]
- [browser-use (GitHub)][browser-use-gh]
- [jev-ultrafast (GitHub)][jev-ultrafast-gh]
- [CC Plugins Docs][cc-plugins-docs]
- [CC WebFetch Docs][cc-webfetch-docs]
- [WebFetch API Docs][webfetch-api-docs]
- [Web Search API Docs][websearch-api-docs]
- [CC Tools Reference][cc-tools-reference]
- [CC Common Workflows — Images][cc-common-workflows]
- [WebFetch PDF issue #23694][webfetch-pdf-issue]

### Third-Party

- [Simon Willison — Playwright MCP with Claude Code][simonwillison-til]
- [Browser tools comparison (DEV.to)][devto-browser-tools]
- [Morph — CC Plugins Guide][morph-plugins]
- [CC built-in web tools analysis][cc-web-tools]
- [Built-in vs MCP search comparison][apiyi-comparison]
- [Zyte: Claude skills vs MCP vs Web Scraping Copilot][zyte-comparison]

[firecrawl-mcp-docs]: https://docs.firecrawl.dev/mcp-server
[firecrawl-mcp-gh]: https://github.com/firecrawl/firecrawl-mcp-server
[firecrawl-plugin]: https://claude.com/plugins/firecrawl
[firecrawl-plugin-gh]: https://github.com/firecrawl/firecrawl-claude-plugin
[firecrawl-pricing]: https://www.firecrawl.dev/pricing
[firecrawl-ai-mcps]: https://www.firecrawl.dev/use-cases/ai-mcps
[firecrawl-prometheus]: https://www.firecrawl.dev/prometheus
[firecrawl-self-host]: https://docs.firecrawl.dev/contributing/self-host
[firecrawl-key-bug]: https://github.com/firecrawl/firecrawl-mcp-server/issues/126
[firecrawl-simple]: https://github.com/devflowinc/firecrawl-simple
[playwright-mcp-gh]: https://github.com/microsoft/playwright-mcp
[playwright-plugin]: https://claude.com/plugins/playwright
[agent-browser-gh]: https://github.com/vercel-labs/agent-browser
[chrome-devtools-mcp-gh]: https://github.com/ChromeDevTools/chrome-devtools-mcp
[stagehand-gh]: https://github.com/browserbase/stagehand
[browser-use-gh]: https://github.com/browser-use/browser-use
[jev-ultrafast-gh]: https://github.com/browser-use/jev-ultrafast
[typesafe-jev-web]: https://docs.typesafe.ai/
[decision-models-landscape]: ../../non-cc/reference/system-1-decision-models-landscape.md#tools-built-on-jev
[cc-plugins-docs]: https://code.claude.com/docs/en/plugins
[cc-webfetch-docs]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool
[simonwillison-til]: https://til.simonwillison.net/claude-code/playwright-mcp-claude-code
[devto-browser-tools]: https://dev.to/minatoplanb/i-tested-every-browser-automation-tool-for-claude-code-heres-my-final-verdict-3hb7
[morph-plugins]: https://www.morphllm.com/claude-code-plugins
[cc-web-tools]: https://mikhail.io/2025/10/claude-code-web-tools/
[apiyi-comparison]: https://help.apiyi.com/en/claude-code-web-search-websearch-mcp-guide-en.html
[zyte-comparison]: https://www.zyte.com/blog/claude-skills-vs-mcp-vs-web-scraping-copilot/
[webfetch-api-docs]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool
[cc-common-workflows]: https://code.claude.com/docs/en/common-workflows#work-with-images
[cc-system-prompts]: https://github.com/Piebald-AI/claude-code-system-prompts
[webfetch-pdf-issue]: https://github.com/anthropics/claude-code/issues/23694
[openclaude-gh]: https://github.com/Twigpine/openclaude
[cc-tools-reference]: https://code.claude.com/docs/en/tools-reference
[websearch-api-docs]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool
[cc-tools-inventory]: ../configuration/CC-tools-inventory.md
[firecrawl-claude-connector]: https://claude.com/connectors/firecrawl
[firecrawl-claude-integration]: https://www.firecrawl.dev/integrations/claude
[firecrawl-alexandria-claude]: https://www.firecrawl.dev/changelog/alexandria-claude
[firecrawl-chatgpt-plugin]: https://firecrawl.dev/blog/firecrawl-official-chatgpt-plugin
[firecrawl-alexandria-chatgpt]: https://firecrawl.dev/blog/alexandria-chatgpt-codex
[firecrawl-alexandria-site]: https://alexandria.firecrawl.dev/
