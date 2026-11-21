---
title: Web Scraping and Data Extraction — Tool Landscape
source: https://github.com/qte77/polyfetch-scrape/blob/main/docs/scraping-landscape.md
purpose: Single-source-of-truth catalog of scraping, crawling, and extraction tooling for agent/RAG pipelines across the qte77 ecosystem
created: 2026-04-23
updated: 2026-11-19
validated_links: 2026-11-09
status: reference
---

**Details:** informational catalog

## What It Is

Survey of available tools for HTTP requests, browser automation, AI-native
scraping, search APIs, managed platforms, document extraction, and anti-bot
bypass. Focused on what's actively maintained and relevant as of 2025–2026.

> **Single source of truth.** This catalog is the authoritative home for
> scraping / crawling / extraction tooling across the qte77 ecosystem. It was
> migrated here from `polyfetch-scrape` on 2026-06-16; that repo now
> [points here][polyfetch] for the landscape and keeps its own
> implementation docs (usage contract, scripting cookbook, API reference,
> architecture, probe findings). This catalog stays the source of truth for the
> landscape. Tool facts below reflect the 2026-04 snapshot unless re-validated,
> except where an entry gives its own date (e.g. polyfetch, v0.11.0, 2026-11-12)
> — verify before relying.

## Claude Code Built-in Web Tools

Claude Code provides two built-in tools for web access — no setup required.

| Tool | What it does | Limitations |
|------|-------------|-------------|
| **WebSearch** | Search query → titles + URLs (Claude.ai backend) | US-only; returns URLs only, not content |
| **WebFetch** | URL → HTML-to-markdown → LLM summary | No JS rendering; 10MB limit; PDF bug (returns binary); 15-min cache |
| **Read** | Local PDF/image parsing (poppler-utils) | Max 20 pages/request; not a web tool |

**Key gaps**: no JS rendering, no browser state/auth, no batch ops, no anti-bot bypass, PDF fetching broken in CC wrapper (works in API). For anything beyond simple URL fetching, use an external tool below.

See [CC Web Scraping Plugins Analysis](../../cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md) for detailed comparison of CC built-in vs Firecrawl MCP vs Playwright MCP.

## HTTP Clients

| Tool | License | TLS Fingerprinting | Differentiator |
|------|---------|-------------------|----------------|
| [curl_cffi](https://github.com/lexiforest/curl_cffi) | MIT | Yes (JA3/HTTP2/HTTP3) | Impersonates Chrome 99-146; fastest TLS bypass |
| [tls_client](https://github.com/FlorianREGAZ/Python-Tls-Client) | MIT | Yes (JA3) | Go-based, simpler API, Python bindings |
| [httpx](https://github.com/encode/httpx) | BSD-3 | No | Modern async/sync client, HTTP/2; no anti-bot |
| [aiohttp](https://github.com/aio-libs/aiohttp) | Apache-2.0 | No | High-performance async; no TLS spoofing |

**When to use what**: curl_cffi for sites with TLS fingerprinting. httpx for everything else.

## Browser Automation

| Tool | License | Anti-Detection | Differentiator |
|------|---------|---------------|----------------|
| [Playwright](https://playwright.dev/) | Apache-2.0 | None built-in | Fast, modern API, multi-browser |
| [Patchright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright) | Apache-2.0 | CDP leak patches | Undetected Playwright fork; Chromium only |
| [SeleniumBase](https://seleniumbase.io/) (UC Mode) | MIT | Cloudflare, CAPTCHAs | Auto CAPTCHA solving; Playwright bridge |
| [Nodriver](https://github.com/ultrafunkamsterdam/nodriver) | MIT | General anti-bot | No driver binary; avoids detection vectors entirely |
| [Botasaurus](https://github.com/omkarcloud/botasaurus) | MIT | Cloudflare, DataDome | Passes nowsecure.nl + g2.com benchmarks |
| [Camoufox](https://camoufox.com/) | MPL-2.0 | Engine-level fingerprint | Modified Firefox build; C++-level patching; experimental |
| [Selenium](https://www.selenium.dev/) | Apache-2.0 | None built-in | Cross-browser W3C WebDriver; IDE + Grid |
| [Puppeteer](https://pptr.dev/) | Apache-2.0 | None built-in | Google's Chrome/Firefox DevTools control (Node) |
| [Magnitude](https://magnitude.run) | Apache-2.0 | n/a (AI test/automation) | Vision-first: LLM drives the browser via screenshots + pixel coordinates (no selectors); `act()` / `extract()` (Zod schemas); dedicated test runner; Playwright as low-level escape hatch |
| [Lightpanda](https://lightpanda.io) | AGPL-3.0 | None built-in | Built from scratch in Zig — not a Chromium/WebKit fork; CDP-compatible drop-in for Puppeteer/Playwright |
| [polyfetch-scrape][polyfetch-repo] | Apache-2.0 | Via Patchright tier (headed option) | Tiered httpx / curl_cffi / Patchright fetch plus `render_session` scripting API; see subsection below |
| [moli](https://github.com/lexmount/moli) | MIT/Apache-2.0 (dual) | None built-in | Built from scratch in Rust — not a Chromium fork; CLI/CDP/WebDriver Classic/BiDi from one binary; ships agent "skills" (`moli-webfetch`, `moli-websearch`) |

**When to use what**: Playwright for JS rendering without anti-bot. Patchright or Nodriver when detection is an issue. Botasaurus for the hardest targets. Magnitude when selector maintenance (dynamic UIs, canvas, drag-and-drop) is the pain point and you can afford per-step vision-model cost.

**Magnitude — vision-first, two products from `magnitudedev`.** [Magnitude](https://magnitude.run) (`@magnitudedev/browser-agent` + `magnitude-test`, ~4.1 k stars, TypeScript) drives the browser through a visually-grounded LLM (Claude Sonnet 4 recommended; most non-vision OpenAI/Gemini/Llama models unsupported) and works as a Model Context Protocol (MCP) tool in Cline/Cursor/Windsurf — resilient to UI churn that breaks selector-based tools. Do **not** confuse it with [magnitude.dev](https://magnitude.dev), the same org's separate **CLI coding agent** (open-model routing — GLM 5.2 + DeepSeek V4 Flash + Kimi K2.7 Code; pass-through pricing + $5 free credits; license unconfirmed). Selector-based contrast: [CC web-scraping plugins analysis](../../cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md) (Playwright MCP).

**Lightpanda — built-from-scratch, not a Chromium fork.** [Lightpanda](https://lightpanda.io) ([repo](https://github.com/lightpanda-io/browser), AGPL-3.0, 35.5k★ verified 2026-09-24) is a headless browser engine written in Zig from scratch — not a Chromium or WebKit fork — targeting automation/crawling/AI workloads rather than human browsing. It speaks the Chrome DevTools Protocol, so it works as a drop-in replacement in existing Puppeteer/Playwright code. Lightpanda's own site reports (vendor benchmark, not independently reproduced here) ~9x faster crawling than Chrome (5s vs 46s) and ~16x lower peak memory (123MB vs 2GB).

**moli — also built from scratch, Rust instead of Zig.** [moli](https://github.com/lexmount/moli) (dual MIT/Apache-2.0 — confirmed by opening and reading both `LICENSE-MIT` and `LICENSE-APACHE` directly; GitHub's single-value repo API field reports only Apache-2.0; 16,369★, created 2026-08-10, verified 2026-10-11) is a standalone headless-browser kernel built in Rust — not a Chromium or WebKit fork — as a workspace of 95 `moli-*` top-level directories (`moli-dom`, `moli-layout`, `moli-css-parse`, `moli-renderer-v8`, `moli-protocol-cdp`, `moli-protocol-webdriver-bidi`, among others; count confirmed from the repo's own root directory listing, not from `[workspace] members` in `Cargo.toml`). It defaults to `LayoutPolicy::Mock` — reading DOM/style state directly, with no layout or paint — and only runs real layout/screenshots when `--layout` is passed — its own "structure first, pixels on demand" design. One binary serves CDP, WebDriver Classic, and WebDriver BiDi (no separate ChromeDriver/geckodriver), and the repo ships three installable agent skills (`github.com/lexmount/moli/tree/main/skills`: `moli-cdp-server`, `moli-webfetch`, `moli-websearch`) that an agent installs to drive it directly. On Lexmount's own benchmark suite (vendor-authored, not independently reproduced here), moli's README reports beating Lightpanda on both a 192-URL mixed public-web crawl (103 useful pages / 53.6% success vs. Lightpanda's 85 / 44.3%) and the 1,308-task Lexbench-Headless-Browser suite (81.9% vs. Lightpanda's 53.3%, against Chrome's 99.8% reference). Moli is Lexmount's open-source engine; Lexmount Browser is a separate managed cloud layer built on top, and the open-source browser is fully usable standalone.

**Fit as a Patchright replacement (verdict, re-checked 2026-10-24): no.** Evaluated as a drop-in for Patchright in a Python fetch toolkit (polyfetch-scrape, [#665](https://github.com/qte77/ai-agents-research/issues/665)):

- **No Python API.** The README offers "the CLI, CDP, WebDriver Classic, or WebDriver BiDi" only, so a Python stack would attach over CDP (e.g. Playwright's `connect_over_cdp()`) rather than import a library.
- **No anti-detection goal.** Patchright exists to hide automation leaks; moli's README never mentions stealth, and the one related item is a closed issue, [lexmount/moli#371](https://github.com/lexmount/moli/issues/371) ("stealth(renderer): expose Chromium `window.chrome` surface").
- **Distribution:** a prebuilt binary through an installer script piped into the shell (`moli-installer.sh | sh`), not a PyPI or npm package. The README lists Linux, macOS and Windows; musl/Alpine is unverified.
- **Fidelity is the vendor's own number:** 81.9% vs Chrome's 99.8% on Lexmount's Lexbench-Headless-Browser, not independently reproduced.
- **Moving fast:** 20,397★ and `v1.1.19` (2026-10-21) as of this check, so expect API churn.

At most an optional, experimental CDP backend for low-fidelity, structure-first crawling, and only after a spike shows that console and network events, full-page screenshots and typed input work over `connect_over_cdp()`. The verdict is unchanged; note that "console events" is a criterion Patchright itself fails for page-script output (see the polyfetch subsection below), so the spike should compare against that baseline, not against full Playwright behaviour.

### Accessibility-tree page representation

A third way to feed a rendered page to an LLM, between raw DOM/HTML and vision/screenshots (Magnitude, above): the browser's **accessibility (a11y) tree** — a semantic role/name view that runs ~80–90 % smaller than the raw DOM and stays stable across visual redesigns, at the cost of being an assistive-tech-shaped subset (decorative / non-interactive nodes are pruned — not a full-fidelity extraction of body text). It is the representation the agent-browser MCP tools converge on; see the [CC web-scraping plugins analysis](../../cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md) for the MCP-level framing (Playwright MCP, Chrome DevTools MCP).

**Desktop counterpart: agent-desktop.** The same accessibility-tree approach now covers native desktop apps. [vercel-labs/agent-desktop][agent-desktop] (Apache-2.0, v1.2.0 released 2026-11-05; latest release v1.3.1, 2026-11-13) is a Rust CLI and C library that "gives an AI agent computer use without screenshots or pixel matching": it reads a desktop app's accessibility tree through the OS API (AX API on macOS 13+, UI Automation on Windows 10 1809+, AT-SPI on Ubuntu 24.04+) and returns JSON with a ref per element, which the agent then clicks or types on. "The loop lives in your agent; agent-desktop has no model inside." Ref actions are headless by default (no pointer movement or focus change; `--headed` allows physical input), and refs are bound to the snapshot they came from, so a changed UI returns an error instead of a wrong click. Agents use it as a CLI, as a skill (`npx skills add https://github.com/vercel-labs/agent-desktop --skill agent-desktop`), or since v1.2.0 through `agent-desktop mcp`. Its own AGENTS.md draws the line with the browser tool: "It does not automate web pages (use agent-browser)." The README warns that snapshots, clipboard reads and screenshots can contain private desktop content. Screenshot-based computer use (Anthropic's computer-use tool) is the contrasting approach; the pixel versus accessibility-tree trade-off is compared in [computer-use-agents-landscape.md](../agents/computer-use-agents-landscape.md#pixels-versus-accessibility-tree); see also the [CC web-scraping plugins analysis](../../cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md). A decision-model variant, the repo's `jev-desktop` skill, is listed under [system-1-decision-models-landscape.md § Tools built on Jev](../reference/system-1-decision-models-landscape.md#tools-built-on-jev).

**Version-gate before relying on the API — it moved recently.** Playwright removed `page.accessibility.snapshot()` in [1.57](https://playwright.dev/docs/release-notes) (it now points to Axe for a11y *testing*); the LLM-facing replacement is `aria_snapshot` (role/name YAML). The [Patchright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright) 1.58.2 pin exposes only `page.locator("body").aria_snapshot()` (signature `aria_snapshot(*, timeout) -> str`) — no `Page.aria_snapshot` shortcut and no `mode="ai"` option (the AI-optimised snapshot with `[ref=e2]` element refs is a newer upstream Playwright feature, absent from this pin). Re-check against the pinned version before use.

### Rendered-session scripting: polyfetch-scrape

[polyfetch-scrape][polyfetch-repo] (Apache-2.0 per its `LICENSE`; v0.11.0, 2026-11-12, per `pyproject.toml` and the [changelog][polyfetch-changelog]; owner's repo) is a Python tiered fetch engine with a rendered-session scripting API. **Fit:** agent fetch jobs that need an escalating httpx / curl_cffi / Patchright chain, or a scriptable instrumented Patchright page. Everything below is documented by polyfetch itself (maintainer's docs, not re-run here); the feature list and versions are in [USING.md][polyfetch-using], recipes in the [scripting cookbook][polyfetch-scripting], signatures in the [API reference][polyfetch-api].

- **Fetch chain.** httpx, then curl_cffi, then Patchright (third tier since 0.3.0), pinnable or bounded by `--tier` / `--min-tier` / `--max-tier` (0.6.0). Retries cover `429` and `500`/`502`/`503`/`504`; `403` and, since 0.9.0, an empty-body HTML 2xx ("soft block") escalate.
- **Errors.** Typed terminal errors (`AuthRequired`, `GoneError`, `LegalBlock`); other non-2xx/3xx statuses raise `FetchError` (0.10.0, breaking). Errors carry redacted `headers` and a 2 KB `body_excerpt` (0.9.0).
- **Rendered session.** `render_session(url)` (0.6.0) exposes the live Patchright `Page`; console errors and failed requests are captured by default, opt-in `capture_network` adds a capped request log with SSE frames (0.11.0); HAR recording (0.9.0), device/viewport/locale/video emulation (0.7.0), headed launch (0.10.0).
- **Authenticated sessions (0.11.0).** `storage_state`, `cookies`, `extra_http_headers`, and `save_storage_state()`; HAR and storage-state files contain credentials.
- **Discovery.** `discover()` (0.7.0) lists sitemaps, feeds, `llms.txt` and [JSON-LD](../../glossary.md#knowledge-structures) types; an opt-in robots helper (0.10.0). Its SSRF guard covers only the discovery paths (`discover`, sitemap fetching, the robots helper, the `easter-hunt` contrib), never the seed URL or plain `fetch()`.

**Patchright console limits (catalog-level fact).** Patchright's README states it disables the Console API to avoid a detection leak: "console functionality will not work in Patchright" (read in the installed 1.64.4 package metadata, 2026-11-15). Consequence: page-script `console.*` output never reaches `page.on("console")`. That uncaught page exceptions are lost too is an **inference** (the README does not say so): Patchright avoids `Runtime.enable`, and `Runtime.exceptionThrown` needs it. polyfetch's repro (four pages of script errors) saw none of them reach `console_errors` or `pageerror`, while a real CORS failure did (**observed by polyfetch, one environment**). Treat Patchright console/pageerror events as a browser/network signal, not a page-script one; read page state structurally (DOM) and by screenshot. A related caveat: `page.evaluate` runs in an isolated world there, so page-defined globals read back `undefined`.

## Scraping Frameworks

| Tool | License | Language | Differentiator |
|------|---------|----------|----------------|
| [Scrapy](https://scrapy.org/) | BSD-3 | Python | Battle-tested at scale; huge plugin ecosystem |
| [Crawlee](https://crawlee.dev/) | Apache-2.0 | JS/TS + Python | Unified HTTP + browser crawling; Apify integration |
| [Scrapling](https://github.com/D4Vinci/Scrapling) | MIT | Python | Adaptive selectors survive site redesigns; MCP server |
| [ScrapFly](https://scrapfly.io/) | SaaS | API | Managed anti-bot bypass; from $30/mo |
| [ZenRows](https://www.zenrows.com/) | SaaS | API | JS rendering + premium proxies; from $69/mo |

## HTML Parsing & Lightweight Libraries

| Tool | License | JS Rendering | Differentiator |
|------|---------|-------------|----------------|
| [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) | MIT | No | Pythonic HTML/XML parse-tree navigation over lxml/html5lib |
| [MechanicalSoup](https://github.com/MechanicalSoup/MechanicalSoup) | MIT | No | Requests + BeautifulSoup with auto cookie/form handling |
| [Requests-HTML](https://github.com/psf/requests-html) | MIT | Yes (pyppeteer) | HTML parsing + JS rendering; unmaintained since 2019 |

## AI/LLM-Native Scrapers

| Tool | License | Pricing | Differentiator |
|------|---------|---------|----------------|
| [Crawl4AI](https://github.com/unclecode/crawl4ai) | Apache-2.0 | Free | Fully local, no API keys, Markdown/JSON output, MCP server |
| [Firecrawl](https://www.firecrawl.dev/) | AGPL-3.0 | Free–$333/mo | One API call = clean Markdown; self-hostable |
| [ScrapeGraphAI](https://scrapegraphai.com/) | MIT | Free–$500/mo | Natural language prompts build scraping pipelines |
| [Jina Reader](https://jina.ai/reader/) | Apache-2.0 | 50K free/mo | HTML→Markdown via SLM (ReaderLM-v2) |
| [Diffbot](https://www.diffbot.com/) | SaaS | From $299/mo | CV-based auto-extraction; Knowledge Graph API |

**When to use what**: Crawl4AI for free local LLM-ready output. Firecrawl for managed/enterprise. Jina for lightweight HTML→Markdown.

**Firecrawl Universal Scrape** (announced 2026-10-08, [Firecrawl blog](https://www.firecrawl.dev/blog/universal-scrape)): the `/scrape` endpoint now also returns third-party provider data, bringing "more of the data your agents need into the `/scrape` endpoint you already use". Provider calls go through Alexandria, Firecrawl's provider layer, via an `alexandria` object (`provider`, `capability`, `options`); the post says "Alexandria has more than 200 providers", of which Universal Scrape works with "a growing selection", e.g. Apollo, FullEnrich and Data Legion (people and companies), Fiscal.ai and Benzinga (financial data), Particle (podcasts). Provider calls are "billed in Firecrawl credits at each tool's listed price"; some providers need an org admin to accept their terms first. The post states no GA/beta status. Our reading (not a Firecrawl claim): this moves Firecrawl from scraper toward data broker; the same API key now reaches paid third-party datasets, so budget and data-licensing review belong with the integration.

## Search APIs

Prices read from each vendor's pricing page on **2026-11-18**; they change often, so re-check before budgeting.

| Tool | Free Tier | Price per 1K queries (from the pricing page) | Differentiator |
|------|-----------|---------|----------------|
| [Exa](https://exa.ai/pricing) | $10 credit, resets monthly | $4 (Lite, Instant); $7 (Auto/Fast); $12-15 (Deep); results beyond 10 cost +$1 per 1K | Neural/semantic search; free credit equals about 2.5K Lite searches (our arithmetic: $10 / $4 per 1K) |
| [Tavily](https://docs.tavily.com/documentation/api-credits) | 1K credits/mo | Basic search = 1 credit, advanced = 2; $8 per 1K credits pay-as-you-go, $5-7.50 on monthly plans | Agentic search API; Nebius announced an agreement to acquire Tavily on 2026-02-10 ([Nebius newsroom][nebius-tavily]; closing not confirmed in what we read) |
| [Serper](https://serper.dev/) | 2.5K queries, no card | $1.00 (Starter, $50 for 50K) down to $0.30 (Ultimate, $3,750 for 12.5M) | Google SERP proxy with knowledge graphs |
| [SerpAPI](https://serpapi.com/pricing) | 250 searches/mo | $25 (Starter, $25 for 1K), $7.25 at 100K, about $3.75 (Cloud 1M, $3,750 for 1M) | Multi-engine (Google, Bing, Baidu, Yandex) |
| [Brave Search](https://brave.com/search/api/) | $5 credit/mo (page headline also says "up to $20") | $5 (Search plan); Answers plan $4 plus token fees | Own search index (page count not stated on the cited page; Brave's own pages give differing figures); privacy-focused |
| [SearXNG](https://github.com/searxng/searxng) | Self-hosted | Free (AGPL-3.0) | Self-hostable metasearch; docs say "260 search engines of which 81 are enabled by default" ([SearXNG docs](https://docs.searxng.org/user/configured_engines.html), read 2026-11-18); no API keys |

Notes: Serper's table lists credits per plan; we read one credit as one query (the excerpt we read did not say). Per-1K figures for SerpAPI and Serper are our division of plan price by plan quota, not figures the vendors publish.

**When to use what** (a rule of thumb resting on vendor positioning, not on an independent benchmark): Exa for semantic/RAG retrieval, Tavily for agent-oriented search with cited results, Brave for privacy-conscious search. The Decision Flowchart below repeats this.

Cross-ref: [searxng-analysis.md](searxng-analysis.md) — deep-dive on self-hosting SearXNG as a keyless search backend for agent and deep-research workflows.

## Managed Scraping Platforms

| Platform | Entry Price | Self-Hostable | Differentiator |
|----------|-------------|---------------|----------------|
| [Apify](https://apify.com/) | Free; $29/mo | No | 20K+ ready-made Actors; full pipeline platform |
| [Browserbase](https://www.browserbase.com/) | ~$50/mo | No | Hosted browser infra for AI agents |
| [Steel](https://steel.dev/) | Free; $29/mo | Yes (Docker) | OSS browser API; sub-second sessions; MCP integration |
| [ScrapingBee](https://www.scrapingbee.com/) | $49/mo | No | Simple API; 84% success rate |
| [Bright Data](https://brightdata.com/) | $1.50/1K req | No | 98.4% success rate; largest proxy network |
| [Oxylabs](https://oxylabs.io/) | $49/mo | No | 98.1% success rate; Web Scraper AI product |
| [Zyte](https://www.zyte.com/) | Free trial ($200) | No | AI-powered unblock + extraction API |
| [ScraperAPI](https://www.scraperapi.com/) | Free tier; paid | No | Proxy-rotation + JS rendering API at scale |
| [Decodo](https://decodo.com/) | Free tier; from $0.09/1K | No | 125M+ IP network; formerly Smartproxy |
| [Scrape.do](https://scrape.do/) | ~$0.60/1K req | No | 110M+ proxies; HTML/JSON/XML/MD output, JS render; ~98.6% success at low cost |

## Document-Specific Extraction

| Tool | Target | License | Notes |
|------|--------|---------|-------|
| [legislation.gov.uk API](https://www.legislation.gov.uk/developer) | UK legislation | Free | Official REST API; XML/HTML; bypasses PDF download issues |
| [Lex API](https://lex.lab.i.ai.gov.uk/) | UK legislation | Free | AI-oriented API with semantic search + MCP server |
| [eurlex (R)](https://michalovadek.github.io/eurlex/) | EUR-Lex | MIT | SPARQL + REST wrapper; bulk download all EU languages |
| [scrapelex (Python)](https://github.com/bocchilorenzo/scrapelex) | EUR-Lex | OSS | BeautifulSoup-based bulk downloader |
| [paperscraper](https://github.com/jannisborn/paperscraper) | arXiv, PubMed | Apache-2.0 | Full-text download via DOI |
| [arXiv Bulk Access](https://info.arxiv.org/help/bulk_data.html) | arXiv | Free | Official S3/GCS bulk access to source + metadata |
| [USPTO Open Data](https://developer.uspto.gov/) | US patents | Free | Bulk data, PatentsView API, full-text search |
| [EPO Open Patent Services](https://www.epo.org/en/searching-for-patents/data/web-services/ops) | EU patents | Free (fair use) | REST API; bibliographic, legal, full-text data |
| [Google Patents Public Datasets](https://cloud.google.com/blog/topics/public-datasets/google-patents-public-datasets-connecting-public-paid-and-private-patent-data) | Global patents | Free (BigQuery) | 120M+ patents; full text, claims, citations |
| [Lens.org API](https://www.lens.org/) | Patents + scholarly | Free (academic) | Unified patent + scholarly search; bulk export |
| [WIPO PATENTSCOPE](https://patentscope.wipo.int/search/en/structuredSearch.jsf) | PCT patents | Free | International patent search; bulk XML download |

**Key insight**: government legislation portals and patent offices have official APIs that are easier than fighting their anti-bot. Use the API, not the PDF download page.

### Document OCR pipelines

Distinct from the source-specific APIs above: general-purpose OCR/VLM tools that turn arbitrary PDFs and images into LLM-ready text — a document-ingestion front-end for RAG and knowledge bases.

- [olmOCR (AllenAI)](https://github.com/allenai/olmocr) — GPU OCR pipeline converting PDF/PNG/JPEG → Markdown or Dolma JSON via a fine-tuned Qwen2.5-VL 7B model; handles equations, tables, handwriting, multi-column layout and reading-order recovery (<$200 / 1M pages, Apache-2.0). Install `pip install olmocr` (remote inference) or `pip install olmocr[gpu] --extra-index-url https://download.pytorch.org/whl/cu128` for local vLLM (Docker image `alleninstituteforai/olmocr:latest-with-model`). Run `olmocr <workspace> --pdfs … --markdown` — default model `allenai/olmOCR-2-7B-1025-FP8`; point at a remote endpoint with `--server`/`--api_key`, or read/write S3 via `--workspace_profile`/`--pdf_profile` (no env vars; the full ~25-flag reference is in the [repo README](https://github.com/allenai/olmocr)).
- [Docling Graph (docling-project, IBM-sponsored)](https://github.com/docling-project/docling-graph) — extends [Docling](https://github.com/docling-project/docling) with a knowledge-graph layer: converts PDFs, images and Office files into typed Pydantic objects, then a directed graph (NetworkX, stable node IDs) exportable to CSV or Cypher for a graph database. Extraction schemas are Pydantic models that double as graph structure — auto-generated from example documents (`docling-graph template from-docs`: an LLM proposes classes/relationships, a deterministic renderer writes the code) or compiled directly from an existing Web Ontology Language (OWL)/RDFS/Simple Knowledge Organization System (SKOS) ontology with no LLM involved (`docling-graph template from-ontology`). MIT license, 901★ (verified 2026-09-24), part of the LF AI & Data ecosystem.

| Platform | License/Pricing | Differentiator |
|----------|----------------|----------------|
| [Steel](https://steel.dev/) | Apache-2.0 (core); cloud from $29/mo | Sub-second sessions, 24h persistence, anti-bot + CAPTCHA |
| [Hyperbrowser](https://www.hyperbrowser.ai/) | HyperAgent OSS; cloud from $99/mo | Three-tier API (ai/perform/extract), 10K+ concurrent browsers |
| [TinyFish](https://www.tinyfish.ai/) | SaaS from $15/mo | Unified search + fetch + browser + agent under one API key |
| GoWatch | SaaS (YC W25) | AI agent-based web monitoring; pivoting — site down as of 2026-04 |

## Research and Monitoring Products

| Product | Pricing | Differentiator |
|---------|---------|----------------|
| [Exa Websets](https://exa.ai/websets) | From $49/mo | AI agents search 20K+ sources, verify and structure results |
| [Firecrawl Open Scouts](https://github.com/firecrawl/open-scouts) | OSS (self-host) | Scheduled web monitoring with email alerts; uses Firecrawl API |

## Integration: Prefer APIs over MCP

Most tools listed above offer both proper REST/SDK APIs and MCP servers. For production use, prefer the direct API — it's faster, typed, versioned, and doesn't depend on the MCP runtime. MCP is useful for interactive AI agent sessions but adds a layer of indirection.

| Tool | API | MCP available |
|------|-----|---------------|
| [Firecrawl](https://docs.firecrawl.dev/api-reference) | REST + Python/JS SDK | Yes |
| [Exa](https://docs.exa.ai/) | REST + Python/JS SDK | Yes |
| [Steel](https://docs.steel.dev/) | REST + Python/JS SDK | Yes |
| [Scrapling](https://github.com/D4Vinci/Scrapling) | Python library | Yes |
| [Bright Data](https://docs.brightdata.com/) | REST | Yes |
| [Apify](https://docs.apify.com/api) | REST + Python/JS SDK | Yes |
| [Lex API](https://lex.lab.i.ai.gov.uk/) | REST | Yes |

## Anti-Bot Bypass

The tools with stealth or bypass features are already catalogued in their own sections: `curl_cffi` (TLS/JA3 fingerprint impersonation) under [§ HTTP Clients](#http-clients); Nodriver, SeleniumBase UC Mode, Patchright and Botasaurus under [§ Browser Automation](#browser-automation); ScrapFly under [§ Scraping Frameworks](#scraping-frameworks). Which protections each one gets past is the project's own undated claim, and detection vendors change frequently, so this section no longer repeats them as a list (trimmed 2026-11-19). For what defenders document about AI-agent traffic, with dates, see [§ Agent Identity and Vendor Handling](#agent-identity-and-vendor-handling). Prefer identifying yourself honestly to evading detection where a site offers a signed or verified route.

**Headed launch (observed by polyfetch).** Launching Chromium headed instead of headless clears some anti-bot challenges that a headless launch never does ([polyfetch#190][polyfetch-190], as recorded in its [changelog][polyfetch-changelog] and [USING.md][polyfetch-using]; maintainer's observation, no per-site data given there). On a display-less host (CI) a virtual display such as `xvfb-run -a` keeps it unattended. Patchright's own README recommends `launch_persistent_context(channel="chrome", headless=False, no_viewport=True)` with real Chrome as its best practice for staying undetected. polyfetch's probe reads Patchright's Cloudflare claim as holding only with that setup ([`docs/scraping-landscape.md`][polyfetch]). Headless CI cannot provide it.

**Reality check**: open-source anti-bot bypasses have a shelf life of months before detection vendors patch them. Commercial APIs invest continuously but cost $1K-5K/mo at scale.

> **Implementation probes.** Catalog-level findings from polyfetch's probes (the Patchright console limitation and the headed-launch observation) are summarised in this catalog; the detailed point-in-time results of the concrete fallback chain (plain `httpx` → `curl_cffi` → Patchright) stay in the consumer repo, [polyfetch-scrape][polyfetch], because they are specific to that codebase.

## Agent Identity and Vendor Handling

This section describes how the defending side treats automated traffic. It is a landscape, not a how-to for defeating any vendor. For the publisher's own controls see [ai-crawlers-discoverability-landscape.md](ai-crawlers-discoverability-landscape.md#publisher-side-controls-cloudflare); for the identity standards in context see [agent-identity-auth-landscape.md](../../sdlc-lcm/agent-identity-auth-landscape.md).

### Signed requests (Web Bot Auth)

- **Mechanism (documented).** Signature headers follow HTTP Message Signatures, [RFC 9421][rfc9421] (Proposed Standard, February 2024). The operator publishes an Ed25519 public key in a JWKS served at `/.well-known/http-message-signatures-directory`; each request carries `Signature-Input` (with `tag="web-bot-auth"`, `keyid`, `created`, `expires`), `Signature` and `Signature-Agent` ([Cloudflare docs][cf-wba], read 2026-11-18). The key-directory and architecture documents are IETF Internet-Drafts (`draft-meunier-http-message-signatures-directory-03` and `draft-meunier-web-bot-auth-architecture-02` as cited by that page), not RFCs. The page does not state a beta or GA status.
- **Signed agents (announced 2025-08-28).** Cloudflare introduced "signed agents" as a classification extending its verified-bots program, naming ChatGPT agent, Goose, Browserbase, Anchor Browser and its own Browser Rendering ([blog][cf-signed-blog], Cloudflare's own statements). Its docs now say that since 2026-07-01 signed agents are treated as verified, distinguished by a Direct or Intermediary label in BotBase; requirements are honest self-identification (Web Bot Auth, published IPs with a stable user agent, or reverse DNS) and non-abusive behaviour such as following robots.txt ([docs][cf-signed-docs]).
- **Pay per crawl** is the publisher-side payment half of the same idea; status and 2026 changes are tracked in [ai-crawlers-discoverability-landscape.md](ai-crawlers-discoverability-landscape.md#publisher-side-controls-cloudflare). At last read (2026-11-18) Cloudflare's docs page says "closed beta" while its changelog headings say "private beta".
- **Commerce variants.** Visa's Trusted Agent Protocol also uses RFC 9421; see [agentic-payments-landscape.md](../protocols/agentic-payments-landscape.md). Akamai describes Skyfire's Know Your Agent (KYA) as complementary: Web Bot Auth proves where a request comes from, KYA who is behind it ([Akamai blog][akamai-wba]).

### Vendor handling of AI agents (as of 2026-11-18)

Rows are vendor statements, with exceptions marked; none is an independent test of detection quality.

| Vendor | What it documents or announced | Level | Date | Source |
|---|---|---|---|---|
| Cloudflare | Verified bots plus signed agents via Web Bot Auth; agent policy requires self-identification and robots.txt compliance; breaches can revoke verified status | Documented | docs read 2026-11-18 | [signed agents docs][cf-signed-docs] |
| Akamai | Web Bot Auth "already supported" in bot and abuse products; verified requests tagged as validated-bot traffic with customer-chosen action | Announced (live per post) | 2025-11-10 | [Akamai blog][akamai-wba] |
| Akamai | Agentic security framework in Bot & Agent Control: six components (identity and human attribution, user authentication, adaptive trust analysis, edge enforcement, monetization, visibility); partners include Visa, Skyfire, Experian, TollBit; availability not stated | Announced | 2026-06-15 | [press release][akamai-fw] |
| DataDome | AI agent identification with strength levels: high (Web Bot Auth, token verification, trusted IP lists, reverse DNS), medium (network attribution, client fingerprinting), low (server fingerprinting); four categories (crawler, assistant, autonomous agent, agentic browser); an AI Agent Trust Score (calculation not described) | Documented | docs read 2026-11-18 | [DataDome docs][datadome-id] |
| Kasada | "AI Agent Trust": directory of recognised crawlers, assistants and agents, per-agent policy, edge enforcement; designed to support Web Bot Auth; no GA details | Announced | 2026-01-21 | [Kasada release][kasada-ait] |
| HUMAN | AgenticTrust within HUMAN Sightline; a newsroom release on cryptographic verification of Amazon Bedrock AgentCore browser traffic | Announced; unverified (page returned 403 to our fetch, body not read; launch 2025-07-30 and AgentCore release late 2025 come from search listings) | see Level | [HUMAN newsroom][human-agentcore] |

Reading across the rows (our synthesis): the documented vendors converge on identity first (signatures, IP lists, directories) and policy second (allow, challenge or block per agent). For a scraping agent the practical question shifts from "can it get through" to "does it identify itself and follow the published rules". A signed identity is an input to a vendor decision, not an entitlement: Cloudflare's own docs say verified status can be revoked.

## Scrape-Quality Evidence

Few independent measurements exist; most numbers are vendor-run. Treat each as a point-in-time sample on the tester's chosen targets.

| Evidence | What it measured | Result (as-of) | Caveat |
|---|---|---|---|
| [Proxyway Web Scraping API Report 2025][proxyway] | 11 scraping APIs (incl. Firecrawl, Apify, ZenRows, Zyte) against 15 protected sites, mostly e-commerce; about 6,000 URLs per target at 2 and 10 requests/s | Published 2025-12-04, tested mainly October 2025; Zyte led overall, with Decodo, Oxylabs and ScrapingBee next; the report says all four opened targets more than 80% of the time (we did not capture Zyte's own figure); hardest targets averaged 21.88% (Shein), 36.63% (G2), 43.75% (Hyatt) at 2 req/s | Success judged by response code, page size and title, not content correctness; we did not assess the tester's funding or independence |
| [AICC / MinerU-HTML, arXiv 2511.16397][aicc] | Main-content extraction on MainWebBench, 7,887 annotated pages | 81.8% ROUGE-N F1 vs Trafilatura 63.6% (submitted 2025-11-20) | Authors' own benchmark and model; does not test Firecrawl, Jina or Crawl4AI |

Gap: we found no independent head-to-head HTML-to-Markdown quality benchmark of Firecrawl, Jina Reader and Crawl4AI (one web search, 2026-11-18). Comparisons that surfaced were vendor or competitor blog posts with undisclosed methodology and are not cited. Run your own check on your target URLs.

## Legal and Terms Note

Neutral orientation only, not legal advice; law differs by jurisdiction and facts. Sources are secondary law-firm and press summaries, not the court filings.

- **hiQ v. LinkedIn (US, Ninth Circuit).** In April 2022 the Ninth Circuit again held, after remand in light of *Van Buren*, that scraping publicly accessible pages likely falls outside the CFAA; a November 2022 district-court ruling then found for LinkedIn on breach of contract, and a December 2022 consent judgment (court-approved 2022-12-08 per Proskauer's update) set a $500,000 judgment against hiQ, a permanent injunction and deletion of scraped data, with hiQ accepting liability on trespass to chattels and misappropriation ([filed stipulation][hiq-stip], [Proskauer][proskauer-hiq], [ZwillGen][zwillgen-hiq]); we read these via a search summary, not the full stipulation. The circuit ruling binds only the Ninth Circuit, and other claims such as contract remain open.
- **Meta v. Bright Data (N.D. Cal., 2024-01-23).** The court read Meta's terms as covering logged-in activity only, so logged-off scraping of public data did not breach them ([Farella Braun summary][fbm-meta]). On 2024-02-26 TechCrunch reported Meta dropped its remaining claim (tortious interference) and gave up its right to appeal ([TechCrunch][tc-meta-bd]); it said Bright Data reported no settlement. We did not read the filing.
- **Google v. SerpApi (N.D. Cal.).** Filed December 2025 under DMCA section 1201 over circumvention of Google's SearchGuard. Press reports a 2026-07-20 dismissal because section 1201 needs a copyrighted work behind the protection, with 21 days to refile a narrower claim; the report says Google plans to file an amended complaint; later status unconfirmed ([TheNextWeb][tnw-serpapi]). Reports differ on whether any part survived; check the docket.
- **Site terms and robots.txt.** Contract claims over terms of service can survive where the CFAA does not apply (hiQ's limits); robots.txt is a voluntary convention, as [Cloudflare's managed robots.txt docs](https://developers.cloudflare.com/bots/additional-configurations/managed-robots-txt/) say. Honour both and keep personal-data rules in view.

## Decision Flowchart

```text
Need to download a known URL?
  ├─ No anti-bot? → httpx
  ├─ TLS fingerprinting? → curl_cffi
  ├─ Needs JavaScript? → Playwright (or Patchright if detected; console API disabled, headed real Chrome for hardened targets)
  ├─ Government legislation? → Use the official API
  └─ All else fails? → Managed platform (Bright Data, ScrapFly)

Need to find content?
  ├─ Semantic/RAG? → Exa (vendor positioning)
  ├─ Factual accuracy? → Tavily (vendor positioning)
  └─ Privacy? → Brave Search API

Need LLM-ready output?
  ├─ Free/local? → Crawl4AI
  ├─ Managed? → Firecrawl
  └─ Lightweight? → Jina Reader
```

## Sources

Each tool links to its first-party page inline in the tables above. This catalog was migrated from [polyfetch-scrape's `scraping-landscape.md`][polyfetch] (origin 2026-04-23, content snapshot 2026-04-26); see that repo for empirical probe results specific to its fallback chain.

| Source | Content |
|---|---|
| [polyfetch-scrape USING.md][polyfetch-using] | Usage contract: tiers, error schema, soft block, session scripting, headed launch, SSRF scope, Patchright console caveat |
| [polyfetch-scrape CHANGELOG.md][polyfetch-changelog] | Version in which each polyfetch feature shipped (0.3.0 to 0.11.0) |
| [polyfetch-scrape scripting cookbook][polyfetch-scripting] and [API reference][polyfetch-api] | Recipes and exact signatures |
| Patchright README (installed 1.64.4 package metadata, 2026-11-15) | Console API disabled; `Runtime.enable` avoided |
| [RFC 9421][rfc9421] · [Cloudflare Web Bot Auth][cf-wba] · [signed agents blog][cf-signed-blog] · [signed agents docs][cf-signed-docs] | HTTP Message Signatures; Web Bot Auth mechanism; signed agents (2025-08-28; verified merge 2026-07-01) |
| [Akamai blog][akamai-wba] · [Akamai framework release][akamai-fw] · [DataDome docs][datadome-id] · [Kasada release][kasada-ait] · [HUMAN newsroom][human-agentcore] | Vendor agent-handling table, 2026-11-18 |
| Pricing pages: [Exa](https://exa.ai/pricing), [Tavily](https://docs.tavily.com/documentation/api-credits), [Serper](https://serper.dev/), [SerpAPI](https://serpapi.com/pricing), [Brave](https://brave.com/search/api/) | Search API prices, read 2026-11-18 |
| [Proxyway 2025 report][proxyway] · [AICC arXiv 2511.16397][aicc] | Scrape-quality evidence |
| [hiQ stipulation][hiq-stip] · [Nebius newsroom][nebius-tavily] · [TechCrunch 2024-02-26][tc-meta-bd] · [Proskauer][proskauer-hiq] · [ZwillGen][zwillgen-hiq] · [Farella Braun][fbm-meta] · [TheNextWeb][tnw-serpapi] | Legal note (secondary summaries) |

[polyfetch]: https://github.com/qte77/polyfetch-scrape/blob/main/docs/scraping-landscape.md
[polyfetch-repo]: https://github.com/qte77/polyfetch-scrape
[polyfetch-using]: https://github.com/qte77/polyfetch-scrape/blob/main/USING.md
[polyfetch-changelog]: https://github.com/qte77/polyfetch-scrape/blob/main/CHANGELOG.md
[polyfetch-scripting]: https://github.com/qte77/polyfetch-scrape/blob/main/docs/scripting.md
[polyfetch-api]: https://github.com/qte77/polyfetch-scrape/blob/main/docs/api-reference.md
[polyfetch-190]: https://github.com/qte77/polyfetch-scrape/issues/190
[agent-desktop]: https://github.com/vercel-labs/agent-desktop
[rfc9421]: https://datatracker.ietf.org/doc/html/rfc9421
[cf-wba]: https://developers.cloudflare.com/bots/concepts/bot/verified-bots/web-bot-auth/
[cf-signed-blog]: https://blog.cloudflare.com/signed-agents/
[cf-signed-docs]: https://developers.cloudflare.com/bots/concepts/bot/signed-agents
[akamai-wba]: https://www.akamai.com/blog/security/redefine-trust-web-bot-authentication
[akamai-fw]: https://www.akamai.com/newsroom/press-release/akamai-unveils-agentic-security-framework-to-power-trusted-ai-driven-interactions-and-commerce
[datadome-id]: https://docs.datadome.co/docs/ai-agent-identification
[kasada-ait]: https://www.kasada.io/kasada-launches-ai-agent-trust-to-secure-agentic-commerce/
[human-agentcore]: https://www.humansecurity.com/newsroom/human-delivers-cryptographic-verification-amazon-bedrock-agentcore-browser/
[proxyway]: https://proxyway.com/research/web-scraping-api-report
[aicc]: https://arxiv.org/abs/2511.16397
[proskauer-hiq]: https://newmedialaw.proskauer.com/2022/12/08/hiq-and-linkedin-reach-proposed-settlement-in-landmark-scraping-case/
[zwillgen-hiq]: https://www.zwillgen.com/?p=18281
[fbm-meta]: https://www.fbm.com/technology/publications/major-decision-affects-law-of-scraping-and-online-data-collection-meta-platforms-v-bright-data/
[tnw-serpapi]: https://thenextweb.com/news/google-serpapi-dmca-scraping-lawsuit-dismissed
[nebius-tavily]: https://nebius.com/newsroom/nebius-announces-agreement-to-acquire-tavily-to-add-agentic-search-to-its-ai-cloud-platform
[hiq-stip]: https://s3.documentcloud.org/documents/23429042/hiq-stip.pdf
[tc-meta-bd]: https://techcrunch.com/2024/02/26/meta-drops-lawsuit-against-web-scraping-firm-bright-data-that-sold-millions-of-instagram-records/
