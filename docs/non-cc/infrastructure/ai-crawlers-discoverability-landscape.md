---
title: AI Crawlers and Discoverability Landscape
purpose: Which AI crawlers and fetchers exist, what each robots.txt token controls (training, search, user-triggered fetch), the publisher-side controls (Cloudflare AI Crawl Control, pay per crawl, Content Signals), and what answer-engine operators actually say about appearing in AI answers.
created: 2026-10-24
updated: 2026-10-24
validated_links: 2026-10-24
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
  with pricing; "Pay per crawl is currently in closed beta" ([docs][cf-pay-per-crawl]). The identity
  side (signed agents via Web Bot Auth) is in
  [agent-identity-auth-landscape.md § 3](../../sdlc-lcm/agent-identity-auth-landscape.md#3-personhood--the-bot-vs-authorized-agent-distinction).
- **Content Signals in managed robots.txt** — three purposes, `search`, `ai-input` and `ai-train`,
  plus an optional `use=` key: `immediate` ("Interact, but store and reuse nothing"), `reference`
  ("Index, excerpt, and link back") and `full` ("Summarize and reproduce"). Cloudflare is explicit
  that "`robots.txt` compliance is voluntary" ([docs][cf-managed-robots]).

## What answer engines say about appearing in AI answers

- **Google:** "There are no additional requirements to appear in AI Overviews or AI Mode, nor other
  special optimizations necessary", and "You don't need to create new machine readable files, AI
  text files, or markup to appear in these features" ([AI features][google-ai-features]). The controls
  are the ordinary snippet and indexing ones (`nosnippet`, `max-snippet`, `noindex`).
- **Microsoft (Bing Ads blog, 2025-10-08):** "Use schema, clear headings, and modular layouts" and
  "Make answers snippable" ([post][bing-ai-answers]) — more prescriptive than Google, and the two
  disagree on whether schema helps.
- **OpenAI, Perplexity:** beyond the crawler tokens above, no first-party content-optimisation guidance
  was found on the pages checked (OpenAI's publisher FAQ returned 403 to automated fetches).

"GEO"/"AEO" playbooks from third parties go beyond what any of these operators state; treat them as
hypotheses. A score-based view of agent readiness (Ora, Lightsage) is in
[evaluation-data-resources-landscape.md § Agent-readiness scoring](../../sdlc-lcm/evaluation-data-resources-landscape.md).

## Practical checklist (our synthesis)

1. Decide the three switches separately: training, AI search, user-triggered fetch.
2. Write robots.txt per token from the table, not one rule for "AI bots".
3. Don't rely on robots.txt for user-triggered fetchers that say they may ignore it; use server-side
   controls (Cloudflare policies, signed-agent verification) if it matters.
4. For visibility, follow ordinary search guidance; Google says no special files or markup are needed.

## Sources

| Source | Content |
|---|---|
| [OpenAI bots][openai-bots] | GPTBot, OAI-SearchBot, ChatGPT-User |
| [Anthropic crawler article][anthropic-bots] | ClaudeBot, Claude-SearchBot, Claude-User; Crawl-delay |
| [Google common crawlers][google-crawlers] | Google-Extended scope and non-impact on Search |
| [Perplexity bots][perplexity-bots] | PerplexityBot, Perplexity-User |
| [Applebot][applebot] | Applebot, Applebot-Extended, Googlebot fallback |
| [CCBot][ccbot] | Common Crawl user agent |
| [Cloudflare AI Crawl Control][cf-ai-crawl-control] · [pay per crawl][cf-pay-per-crawl] · [managed robots.txt][cf-managed-robots] | Publisher controls, 402, Content Signals |
| [Google AI features][google-ai-features] | No special markup or files for AI Overviews / AI Mode |
| [Microsoft Bing Ads blog][bing-ai-answers] | Schema, headings, snippable answers |
| Falsification pass, 2026-10-24 | 15 claims re-checked: 14 confirmed, 1 misquote fixed |

[openai-bots]: https://developers.openai.com/api/docs/bots
[anthropic-bots]: https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
[google-crawlers]: https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers
[perplexity-bots]: https://docs.perplexity.ai/guides/bots
[applebot]: https://support.apple.com/en-us/119829
[ccbot]: https://commoncrawl.org/ccbot
[cf-ai-crawl-control]: https://developers.cloudflare.com/ai-crawl-control/
[cf-pay-per-crawl]: https://developers.cloudflare.com/ai-crawl-control/features/pay-per-crawl/what-is-pay-per-crawl/
[cf-managed-robots]: https://developers.cloudflare.com/bots/additional-configurations/managed-robots-txt/
[google-ai-features]: https://developers.google.com/search/docs/appearance/ai-features
[bing-ai-answers]: https://about.ads.microsoft.com/en/blog/post/october-2025/optimizing-your-content-for-inclusion-in-ai-search-answers
