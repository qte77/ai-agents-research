---
title: AI Crawlers and Discoverability Landscape
purpose: Which AI crawlers and fetchers exist, what each robots.txt token controls, publisher-side controls (Cloudflare AI Crawl Control, Content Signals), and what answer engines say on appearing in answers.
created: 2026-10-24
updated: 2026-11-18
validated_links_on: 2026-11-14
status: research
---

**Details:** Every row was fetched from the operator's own documentation on 2026-10-24 and re-checked
by an independent falsification pass (14 of 15 claims confirmed; one misquoted phrase corrected).
llms.txt itself is covered in
[CC-llms-txt-analysis.md](../../cc-native/context-memory/CC-llms-txt-analysis.md).

## What It Is

Being found by AI assistants depends on three separate switches that site owners often treat as
one: whether a crawler may **train** on your pages, whether it may **index** them for AI search, and
whether an assistant may **fetch** a page when a user asks. Each operator exposes these as different
robots.txt tokens, and they don't all honour robots.txt the same way.

## Crawler tokens

| Operator | Token | What it is for | robots.txt | Source |
|---|---|---|---|---|
| OpenAI | `GPTBot` | Training — disallowing it "indicates a site's content should not be used in training generative AI foundation models" | Honoured | [OpenAI bots][openai-bots] |
| OpenAI | `OAI-SearchBot` | ChatGPT search — opted-out sites "will not be shown in ChatGPT search answers", though they "can still appear as navigational links" | Honoured | [OpenAI bots][openai-bots] |
| OpenAI | `ChatGPT-User` | User-triggered fetches | "Because these actions are initiated by a user, robots.txt rules may not apply" | [OpenAI bots][openai-bots] |
| Anthropic | `ClaudeBot`, `Claude-SearchBot`, `Claude-User` | Training, search indexing, user-triggered fetches | All three "respect 'do not crawl' signals by honoring industry standard directives in robots.txt"; Anthropic also supports "the non-standard Crawl-delay extension" (page dated April 7, 2026) | [Anthropic crawlers][anthropic-bots] |
| Google | `Google-Extended` | A product token for Gemini Apps, the Vertex AI API for Gemini and grounding; it "doesn't have a separate HTTP request user agent string" and "does not impact a site's inclusion in Google Search nor is it used as a ranking signal" | Token only | [Google crawlers][google-crawlers] |
| Perplexity | `PerplexityBot` | Search — "It is not used to crawl content for AI foundation models" | Honoured | [Perplexity bots][perplexity-bots] |
| Perplexity | `Perplexity-User` | User-triggered fetches — "this fetcher generally ignores robots.txt rules" | Generally ignored | [Perplexity bots][perplexity-bots] |
| Apple | `Applebot`, `Applebot-Extended` | Search; `Applebot-Extended` is a training opt-out and "does not crawl webpages". If rules name Googlebot but not Applebot, "the Apple robot will follow Googlebot instructions" | Honoured | [Applebot][applebot] |
| Common Crawl | `CCBot` | Open web corpus used by many model trainers; user agent `CCBot/2.0 (https://commoncrawl.org/faq/)` | Honoured | [CCBot][ccbot] |

**The gap is user-triggered fetching.** OpenAI ("may not apply") and Perplexity ("generally ignores")
say their user-initiated fetchers can bypass robots.txt; Anthropic says all three of its agents honour
it. Blocking training (`GPTBot`, `Google-Extended`, `Applebot-Extended`) does not remove a site from AI
search, and blocking a search bot does not stop a user's assistant from fetching a page.

## Publisher-side controls (Cloudflare)

- **AI Crawl Control** — "AI Crawl Control (formerly AI Audit) gives you visibility into which AI
  services are accessing your content", with per-crawler policies; "Available on all plans"
  ([docs][cf-ai-crawl-control]).
- **Pay per crawl** — crawlers without payment intent get an `HTTP 402 Payment Required` response
  with pricing; the docs page says "Pay per crawl is currently in closed beta" ([docs][cf-pay-per-crawl]),
  while the changelog headings say "private beta" (read 2026-11-18). The changelog shows a
  2026-06-16 update adding URI-pattern exemptions and dynamic pricing via an origin header or Worker
  ([changelog][cf-acc-changelog]). TechCrunch reports Cloudflare's 2026-07-01 announcement that pay
  per crawl is "evolving into" Pay Per Use (publishers paid when content creates value; partners
  Ceramic.ai and You.com) and that from 2026-09-15 "mixed-use" crawlers are blocked by default on
  ad-hosting pages for new customers, new sites and free plans ([TechCrunch][tc-cf-2026-07]). That
  is a secondary report; the changelog has no entry for either item, so it is unconfirmed at
  Cloudflare. The identity side (signed agents via Web Bot Auth) is in
  [agent-identity-auth-landscape.md § 3](../../sdlc-lcm/agent-identity-auth-landscape.md#3-personhood--the-bot-vs-authorized-agent-distinction);
  the crawler-side view is in
  [web-scraping-extraction-landscape.md § Agent Identity and Vendor Handling](web-scraping-extraction-landscape.md#agent-identity-and-vendor-handling).
- **Content Signals in managed robots.txt** — three purposes, `search`, `ai-input` and `ai-train`,
  plus an optional `use=` key: `immediate` ("Interact, but store and reuse nothing"), `reference`
  ("Index, excerpt, and link back") and `full` ("Summarize and reproduce"). Cloudflare is explicit
  that "`robots.txt` compliance is voluntary" ([docs][cf-managed-robots]).

## What answer engines say about appearing in AI answers

- **Google:** "There are no additional requirements to appear in AI Overviews or AI Mode, nor other
  special optimizations necessary", and "You don't need to create new machine readable files, AI
  text files, or markup to appear in these features" ([AI features][google-ai-features]). The controls
  are the ordinary snippet and indexing ones (`nosnippet`, `max-snippet`, `noindex`).
  Google's [AI optimization guide][google-ai-guide] (announced May 2026, last updated 2026-07-10) goes
  further and lists what to ignore: llms.txt and similar files "will neither harm nor help your site's
  visibility or rankings in Google Search, as Google Search ignores them"; "Structured data isn't
  required for generative AI search, and there's no special schema.org markup you need to add" (though
  it advises keeping it for SEO); "There's no requirement to break your content into tiny pieces"; and
  "No third-party tool has access to our internal ranking or AI systems."
  Since 2026-08-31 every site can opt out of AI Overviews and AI Mode in Search Console: "Sites that opt
  out will not receive traffic or impressions from our generative AI features", and the control "will
  not be used as a ranking signal" for ordinary results ([Google][google-ai-optout]). Search Console
  also reports impressions in those features ([2026-06-03][google-ai-reports]).
- **Microsoft (Bing Ads blog, 2025-10-08):** "Use schema, clear headings, and modular layouts" and
  "Make answers snippable" ([post][bing-ai-answers]) — more prescriptive than Google, and the two
  disagree on whether schema helps. Microsoft Advertising's [*A Guide to GEO*][ms-geo-guide]
  (2026-01-06, written for retailers) keeps that line: "Deploy Product, Offer, AggregateRating,
  Review, Brand, ItemList, and FAQ schema types", "Provide Q&A blocks AI can reason over and cite", and
  "never serve different HTML to bots". The guide uses "GEO" throughout and never "AEO"; the
  "Answer/Agentic Engine Optimization" gloss seen in trade press is not Microsoft's. Bing Webmaster
  Tools' AI Performance report (public preview, [2026-02-10][bing-ai-performance]) shows how often a
  site is cited across "Microsoft Copilot, AI-generated summaries in Bing, and select partner
  integrations".
- **OpenAI:** no written content-optimisation guidance was found (its publisher FAQ returned 403 to
  automated fetches), but since 2026-11-10 it runs a first-party listing surface. Through
  **Business Hub**, part of "Businesses in ChatGPT" (beta), a business can claim its listing, keep
  profile details current, connect a product feed, and see 28-day insights on mentions and website
  clicks ([announcement][oai-businesses]). The help article sets the limits: "Claiming a profile or
  disputing ownership doesn't change its visibility in ChatGPT", "Connecting a feed doesn't publish an
  agent or guarantee that ChatGPT recommends your products", and for an online business a mention
  counts only when ChatGPT references the business's website: "The brand name alone doesn't count."
  Publishing changes and viewing insights need Persona identity verification; Business Agents are for
  "eligible ecommerce and online service businesses in the US with a website" ([help][oai-business-help]).
  Sponsoring a Business Agent as a ChatGPT Ads destination is announced, labelled separately.
- **Perplexity:** beyond the crawler tokens above, no first-party content-optimisation guidance was
  found on the pages checked.

Google and Microsoft disagree on two points: schema (optional for Google, recommended by Microsoft)
and splitting content into Q&A or FAQ blocks (unneeded for Google, recommended by Microsoft and Bing).
They agree on crawlable, indexable pages, no cloaking, and original content.

"GEO"/"AEO" playbooks from third parties go beyond what any of these operators state; treat them as
hypotheses (what is canonical: [§ GEO and AEO](#geo-and-aeo-what-is-canonical)). A score-based view of agent readiness (Ora, Lightsage) is in
[evaluation-data-resources-landscape.md § Agent-readiness scoring](../../sdlc-lcm/evaluation-data-resources-landscape.md).

## GEO and AEO: what is canonical

- **One academic origin.** "GEO: Generative Engine Optimization" (Aggarwal et al., [arXiv 2311.09735][geo-paper], accepted to KDD 2024) introduced the term and a benchmark, GEO-bench; its abstract reports that "GEO can boost visibility by up to 40% in generative engine responses", measured on that benchmark, not in the field. Code and data: [`GEO-optim/GEO`][geo-repo] (Apache-2.0). AEO, LLMO, ASO and LEO are later labels for the same practice, used by vendors and agencies, with no comparable academic or standards source. ASO has competing expansions, none settled: "Agentic Search Optimization" (Semrush's CMO in [TechRadar][aso-techradar], 2026-04-20), "Agent search optimization" ([Visualping][aso-visualping], 2026), and "AI search optimization"; in mobile marketing ASO already means App Store Optimization. LEO is usually expanded as "LLM Engine Optimization".
- **Optimizing for agents, not answers, is studied under the GEO name.** [Toolflation][toolflation] (arXiv 2610.28454, 2026-10-20) has seller agents rewrite tool descriptions in a simulated tool market; under one of five models "sellers copy one another until the descriptions no longer tell the tools apart", and buyer agents fall back to picking by list position. A position paper titled [*AX is the New AEO*][ax-new-aeo] (arXiv 2609.34951, 2026-09-28) argues the two converge; Netlify's own AX definition (below) is narrower.
- **No standards body owns GEO.** The nearest standards work is the IETF [aipref][aipref] working group: two drafts (`draft-ietf-aipref-vocab-08`, `draft-ietf-aipref-attach-05`), both WG Documents aiming at Proposed Standard as of 2026-11-14. They signal *usage preferences* (training, search, fetch), not visibility or ranking. llms.txt, schema.org, NLWeb and Model Context Protocol (MCP) are existing formats reused for the purpose.
- **"Agent Experience" is a different thing.** Netlify says it "coined the term in 2025" and defines AX as "the holistic experience AI agents will have as the user of a product or platform" ([Netlify][netlify-ax]): agents as *users* of your product, not your brand appearing in AI answers. Some GEO vendors reuse the words for the latter.
- **How it differs from classic SEO.** Crawlability, structured data and being cited by others carry over. What changes is the target: inclusion and prominence inside a generated answer instead of a rank on a results page, often with no click to measure. First-party reporting arrived in 2026: Bing's AI Performance report (February), Search Console's generative-AI reports (June) and ChatGPT Business Hub insights (November), each covering only its own engine. Visibility trackers such as [Peec AI][peec] and [Scrunch][scrunch] run their own prompt panels against each engine; their numbers are vendor-specific.

## What the research shows

Peer-reviewed or workshop work since the GEO paper, each checked against its arXiv record on
2026-11-14. Venues are given only where the arXiv record states them.

| Paper | Finding |
|---|---|
| [C-SEO Bench][c-seo-bench] (Puerto et al., NeurIPS Datasets & Benchmarks 2025) | "most current C-SEO methods are not only largely ineffective but also frequently have a negative impact on document ranking"; effects shrink as more actors adopt them (a zero-sum game) |
| [AutoGEO][autogeo] (Wu et al., CMU, 2025; code: [`cxcscmu/AutoGEO`][autogeo-repo]) | learned rewriting rules give "an average improvement of 35.99% in GEO metrics while maintaining utility" on its benchmarks |
| [E-GEO][e-geo] (Bagga et al., MIT; NeurIPS 2026 E&D) | 13,746 product queries; "under a simple in-prompt defense in our setting, gains from GEO reflect genuine content improvement" |
| [Characterizing Web Search in the Age of Generative AI][kirsten-aio] (Kirsten et al., 2025) | a large share of the domains AI Overviews consult are not in the top-10, or even top-100, organic results |
| [Navigating the Shift][chen-shift] (Chen et al., Toronto; EDBT/ICDT 2026 Workshops) | domain overlap with Google's top 10 is low; "GPT-4o shows the lowest mean overlap at 4.0%" |
| [Adversarial SEO for LLMs][nestaas-aseo] (Nestaas et al., ETH Zürich, 2024) | injected page content makes an adversarial plugin "up to 7.2× more likely to be selected"; when everyone attacks, all lose (a prisoner's dilemma) |
| [Ranking Manipulation for Conversational Search Engines][pfrommer-rank] (Pfrommer et al., Berkeley; EMNLP 2024) | adversarial text in product pages reorders LLM product rankings, with a demonstration on perplexity.ai |
| [What Is Your AI Agent Buying?][aces] (Allouah et al., 2025) | in a simulated shop, "a single iteration produced a statistically significant increase in market share for the focal product in 33% of our experiments"; agents show strong position biases |
| [Tool Preferences in Agentic LLMs are Unreliable][faghih-tools] (Faghih et al., EMNLP 2025) | edited tool descriptions shift agents' tool choice sharply |
| [Advertising to Agents][adv-agents] (Wang, MIT; NeurIPS 2026 workshop) | stacked praise in a tool description "raised a tool's pick rate by about 43 percentage points"; single author, and the abstract says results are "provisional" and "cover two small models" |

Read together: rewriting content for AI answers sometimes helps and sometimes hurts (AutoGEO vs
C-SEO Bench), gains erode as more sites optimize, AI answers draw on sources outside the classic top
results, and both product and tool descriptions can be gamed, which is why Toolflation (above) finds
descriptions converging. No academic study of AI-search referral traffic was found; the figures in
circulation come from analytics vendors.

## Tools: trackers, MCP servers and open-source projects

Commercial visibility trackers ([Peec AI][peec], [Scrunch][scrunch], Profound, Otterly.AI, AthenaHQ,
Semrush AI Toolkit, Ahrefs Brand Radar, Evertune, Goodie and others) all run their own prompt panels
against several engines; their metrics are vendor-defined and not comparable across tools. Several now
expose MCP servers, so an agent can query visibility data directly: Peec's MCP docs list "Claude
(Desktop, Web, Code)" ([docs][peec-mcp]); Profound's hosted MCP is "Available on: the Enterprise plan"
([docs][profound-mcp]).

Open-source projects, checked on GitHub 2026-11-14 (stars at that date). GitLab had nothing
substantive; Codeberg could not be searched (rate-limited).

| Repo | License | What it is |
|---|---|---|
| [`elmohq/elmo`][elmo] | MIT | Self-hosted AEO/GEO tracker with an MCP server |
| [`limelit-co/open`][limelit-open] | Apache-2.0 | Self-hosted visibility tracking, single binary, MCP server |
| [`Auriti-Labs/geo-optimizer-skill`][geo-optimizer] | MIT | Citation-audit engine behind GeoReady; CLI, Python, MCP |
| [`zubair-trabzada/geo-seo-claude`][geo-seo-claude], [`onvoyage-ai/gtm-engineer-skills`][gtm-skills] | MIT | Claude Code skills for GEO/AEO audits (checklists, not measurement) |

The broader SEO skill set `AgriciDaniel/claude-seo` is profiled in [CC-community-plugins-landscape.md](../../cc-community/CC-community-plugins-landscape.md). The two most-starred Claude Code GEO skill repos grew to 10k+ stars within months of creation; treat
star counts in this niche as weak signal. The open-source trackers mostly mirror the commercial ones:
prompt panels across engines, run with your own API keys.

## Practical checklist (our synthesis)

1. Decide the three switches separately: training, AI search, user-triggered fetch.
2. Write robots.txt per token from the table, not one rule for "AI bots".
3. Don't rely on robots.txt for user-triggered fetchers that say they may ignore it; use server-side
   controls (Cloudflare policies, signed-agent verification) if it matters.
4. For visibility, follow ordinary search guidance: indexable pages, original content, no cloaking.
   Google says no special files, markup or chunking are needed; Microsoft recommends schema and Q&A
   blocks. Do both only where they also help human readers.
5. Measure in the engines' own reports (Search Console, Bing AI Performance, ChatGPT Business Hub)
   before buying a third-party tracker; each covers one engine, and no tracker sees ranking internals.
6. To keep normal Google results but leave AI Overviews and AI Mode, use the Search Console opt-out
   rather than `nosnippet`.

## Not included

Entries removed under the [pruning rule](../../../CONTRIBUTING.md#pruning-entries-well-known-performance-optimised-filter) (alive, adopted or proven; checked 2026-11-22).

| Name | Reason | Date | Link |
|---|---|---|---|
| danishashko/geo-aeo-tracker | 334 stars (`gh api` 2026-11-22); no named independent users or measured benefit in its README (criterion 3) | 2026-11-22 | <https://github.com/danishashko/geo-aeo-tracker> |
| yaojingang/GEOInflow | 865 stars (`gh api` 2026-11-22), repo created 2026-10-26; no named independent users or measured benefit in its README (criterion 3) | 2026-11-22 | <https://github.com/yaojingang/GEOInflow> |
| dodopayments/dualmark | 125 stars (`gh api` 2026-11-22); its README names only its maker's own site as a user, pre-1.0 (criterion 3) | 2026-11-22 | <https://github.com/dodopayments/dualmark> |

## Sources

| Source | Content |
|---|---|
| [GEO paper (arXiv 2311.09735)][geo-paper] · [`GEO-optim/GEO`][geo-repo] | The term's academic origin, KDD 2024; benchmark code |
| [IETF aipref WG][aipref] | Usage-preference vocabulary and attachment drafts (WG Documents, 2026-11-14) |
| [Netlify: Agent Experience][netlify-ax] | AX definition; agents as users of a product |
| [Peec AI][peec] · [Scrunch][scrunch] | AI-search visibility tracking vendors (self-described) |
| [OpenAI bots][openai-bots] | GPTBot, OAI-SearchBot, ChatGPT-User |
| [Anthropic crawler article][anthropic-bots] | ClaudeBot, Claude-SearchBot, Claude-User; Crawl-delay |
| [Google common crawlers][google-crawlers] | Google-Extended scope and non-impact on Search |
| [Perplexity bots][perplexity-bots] | PerplexityBot, Perplexity-User |
| [Applebot][applebot] | Applebot, Applebot-Extended, Googlebot fallback |
| [CCBot][ccbot] | Common Crawl user agent |
| [Cloudflare AI Crawl Control][cf-ai-crawl-control] · [pay per crawl][cf-pay-per-crawl] · [managed robots.txt][cf-managed-robots] | Publisher controls, 402, Content Signals |
| [Cloudflare AI Crawl Control changelog][cf-acc-changelog] · [TechCrunch 2026-07-01][tc-cf-2026-07] | Pay per crawl 2026-06-16 update; Pay Per Use and mixed-use default block (secondary, 2026-11-18) |
| [Google AI features][google-ai-features] | No special markup or files for AI Overviews / AI Mode |
| [Microsoft Bing Ads blog][bing-ai-answers] | Schema, headings, snippable answers |
| [Google AI optimization guide][google-ai-guide] · [AI features opt-out][google-ai-optout] · [gen-AI reports][google-ai-reports] | What to ignore; Search Console opt-out and reporting |
| [Microsoft Advertising: A Guide to GEO][ms-geo-guide] · [Bing AI Performance][bing-ai-performance] | Retail GEO guide; Bing citation reporting |
| [Peec AI MCP][peec-mcp] · [Profound MCP][profound-mcp] | Vendor MCP access to visibility data |
| GitHub repos listed in § Tools | Licenses, stars, dates via the GitHub API, 2026-11-14 |
| arXiv records: [C-SEO Bench][c-seo-bench], [AutoGEO][autogeo], [E-GEO][e-geo], [Kirsten et al.][kirsten-aio], [Chen et al.][chen-shift], [Nestaas et al.][nestaas-aseo], [Pfrommer et al.][pfrommer-rank], [ACES][aces], [Faghih et al.][faghih-tools], [Advertising to Agents][adv-agents] | GEO research findings |
| [OpenAI: Businesses in ChatGPT][oai-businesses] · [Business Hub help][oai-business-help] | Business Hub (beta, 2026-11-10): claim, profile, feed, 28-day insights, limits |
| [TechRadar (Semrush CMO)][aso-techradar] · [Visualping][aso-visualping] | ASO expansions in vendor usage |
| [Toolflation (arXiv 2610.28454)][toolflation] · [AX is the New AEO (arXiv 2609.34951)][ax-new-aeo] | Agent-facing optimization research |
| Falsification pass, 2026-10-24 | 15 claims re-checked: 14 confirmed, 1 misquote fixed |

[openai-bots]: https://developers.openai.com/api/docs/bots
[anthropic-bots]: https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
[google-crawlers]: https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers
[perplexity-bots]: https://docs.perplexity.ai/guides/bots
[applebot]: https://support.apple.com/en-us/119829
[ccbot]: https://commoncrawl.org/ccbot
[cf-ai-crawl-control]: https://developers.cloudflare.com/ai-crawl-control/
[cf-pay-per-crawl]: https://developers.cloudflare.com/ai-crawl-control/features/pay-per-crawl/what-is-pay-per-crawl/
[cf-acc-changelog]: https://developers.cloudflare.com/ai-crawl-control/changelog
[tc-cf-2026-07]: https://techcrunch.com/2026/07/01/cloudflares-new-policy-pushes-ai-companies-to-pay-for-publishers-content/
[cf-managed-robots]: https://developers.cloudflare.com/bots/additional-configurations/managed-robots-txt/
[google-ai-features]: https://developers.google.com/search/docs/appearance/ai-features
[bing-ai-answers]: https://about.ads.microsoft.com/en/blog/post/october-2025/optimizing-your-content-for-inclusion-in-ai-search-answers
[geo-paper]: https://arxiv.org/abs/2311.09735
[geo-repo]: https://github.com/GEO-optim/GEO
[aipref]: https://datatracker.ietf.org/wg/aipref/documents/
[netlify-ax]: https://www.netlify.com/agent-experience/
[peec]: https://peec.ai/
[scrunch]: https://scrunch.com/
[oai-businesses]: https://openai.com/index/introducing-businesses-chatgpt/
[oai-business-help]: https://help.openai.com/en/articles/20001635-setting-up-your-business-on-chatgpt
[aso-techradar]: https://www.techradar.com/pro/agentic-search-optimization-reshapes-brand-visibility-in-ai-search
[aso-visualping]: https://visualping.io/blog/agent-search-optimization
[toolflation]: https://arxiv.org/abs/2610.28454
[ax-new-aeo]: https://arxiv.org/abs/2609.34951
[google-ai-guide]: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
[google-ai-optout]: https://blog.google/products-and-platforms/products/search/new-controls-website-owners/
[google-ai-reports]: https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports
[ms-geo-guide]: https://about.ads.microsoft.com/en/blog/post/january-2026/from-discovery-to-influence-a-guide-to-geo
[bing-ai-performance]: https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview
[c-seo-bench]: https://arxiv.org/abs/2506.11097
[autogeo]: https://arxiv.org/abs/2510.11438
[e-geo]: https://arxiv.org/abs/2511.20867
[kirsten-aio]: https://arxiv.org/abs/2510.11560
[chen-shift]: https://arxiv.org/abs/2601.16858
[nestaas-aseo]: https://arxiv.org/abs/2406.18382
[pfrommer-rank]: https://arxiv.org/abs/2406.03589
[aces]: https://arxiv.org/abs/2508.02630
[faghih-tools]: https://arxiv.org/abs/2505.18135
[adv-agents]: https://arxiv.org/abs/2605.23916
[peec-mcp]: https://docs.peec.ai/mcp/introduction
[profound-mcp]: https://docs.tryprofound.com/mcp/overview
[autogeo-repo]: https://github.com/cxcscmu/AutoGEO
[elmo]: https://github.com/elmohq/elmo
[limelit-open]: https://github.com/limelit-co/open
[geo-optimizer]: https://github.com/Auriti-Labs/geo-optimizer-skill
[geo-seo-claude]: https://github.com/zubair-trabzada/geo-seo-claude
[gtm-skills]: https://github.com/onvoyage-ai/gtm-engineer-skills
