---
title: Computer-Use Agents Landscape
source: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool
purpose: Landscape of agents that operate a GUI from screen observations - first-party Claude computer use, other vendors' tools, open models, the OSWorld benchmark family, the pixel versus accessibility-tree trade-off, and safety guidance.
created: 2026-11-19
updated: 2026-11-19
validated_links: 2026-11-19
status: reference
---

**Details:** informational landscape; vendor docs read 2026-11-19, no hands-on testing

Evidence levels: **documented** (vendor docs state it), **paper** (arXiv abstract or paper text),
**vendor claim** (self-reported score or ranking we did not reproduce), **our reading** (inference).
Browser agents are a separate topic and are not covered here beyond pointers.

## TL;DR

- A computer-use agent loops: take a screenshot, let a model propose GUI actions (click, type,
  scroll), run them in an environment you control, return the next screenshot. Anthropic, OpenAI
  and Google all document this client-executed loop (documented).
- Claude's computer use is a client-side tool whose current version needs no beta header; earlier
  versions still need one. Claude Desktop also exposes it to end users (documented, beta).
- The OSWorld family splits in two: OSWorld-Verified (fixed original tasks, scores near 80% are
  vendor claims) and OSWorld 2.0 (long-horizon, best published binary score 20.6% in the paper,
  21.3% in a vendor claim). Scores from the two are not one trend.
- Screenshot-only versus accessibility-tree input is a real design axis, not a settled one: 2024
  evidence favoured structured input, current vendor tools are screenshot-first, and a 2026 paper
  uses the accessibility tree for security rather than perception.
- Every vendor says the same about safety: isolate the environment, treat screen content as
  untrusted, confirm consequential actions.

## First-party Claude computer use

**Claude API tool (documented, page read 2026-11-19).** Per the [computer use tool docs][claude-cu]:

| Item | Documented state |
| ---- | ---------------- |
| Current version | `computer_toolset_20260801`; the request "needs no beta header" |
| Models on the current toolset | Claude Fable 5.2, Mythos 5.2, Opus 5.5, Sonnet 5.5, Haiku 5.5 (the page's `supportedModels` list also names earlier 5.x ids) |
| Earlier versions | `computer_20251124` (header `computer-use-2025-11-24`) and `computer_20250124` (header `computer-use-2025-01-24`), both beta; the page lists which models take which |
| Execution | Client side: Claude never connects to your environment; your application runs each action and returns results |
| Reference implementation | A Docker-based quickstart (virtual display, desktop, Firefox, LibreOffice) |
| Screenshot limits | Up to 2,576 px on the long edge for Opus 4.7 and later; 1,568 px for earlier models; oversized images are rejected, not downscaled |
| Overhead | About 4,500 input tokens for the toolset definition |
| Data retention | ZDR eligible (client-side tool), excluding Covered Models |
| Managed Agents | Not available there |

Changes from the earlier versions that matter for migrations (documented): the toolset accepts
several tool-use blocks per turn and expects them run in order, `zoom` is on by default, and the
toolset rejects the old `display_width_px` / `display_height_px` parameters. The docs list
latency, coordinate hallucination, weak scrolling, spreadsheet interaction and niche apps among
known limitations, and say not to use it for tasks needing perfect precision without human
oversight.

**Claude Desktop (documented, beta).** The support article [Let Claude use your computer in
Cowork][claude-cowork-cu] describes computer use for Pro, Max and Ultra plans on macOS and Windows
in the Desktop app (Cowork and Claude Code). Claude tries connectors first, then a browser, and
uses screen control only if neither works; it asks permission per application, blocks some
categories such as trading and cryptocurrency apps by default, and the article states there is no
sandbox between Claude and your apps. The article contradicts itself on Team and Enterprise
availability, and the Claude Code desktop docs give a different macOS minimum than the support
article for the background-window behaviour, so check both before relying on either.

**Pointer only:** Claude in Chrome (browser extension) is a browser agent and is covered under the
browser-agents topic, not here.

## Other vendors

| Vendor | What the docs say (read 2026-11-19) | Level |
| ------ | ----------------------------------- | ----- |
| OpenAI | [Computer use guide][openai-cu]: a `computer` tool in the Responses API; model returns a `computer_call` with an ordered action list, your code executes and returns a screenshot via `computer_call_output`. For the newest model the page recommends code execution and keeps the computer tool "as an alternative". No benchmark numbers on the page | documented |
| Google | [Gemini computer use][gemini-cu]: browser, mobile and desktop action sets; coordinates normalised so you do not send display size; each step can carry a `safety_decision` (allowed, require confirmation, blocked); prompt-injection screening is opt-in | documented |
| Microsoft | Researcher's Computer Use, Copilot Studio computer use and the Foundry computer-use tool are already compared in [Microsoft 365 Copilot analysis, Computer-using agents][ms-cua]; not repeated here | documented (see that doc) |
| Open models | See next section | mixed |

The OpenAI page does not state a deprecation date for the older `computer-use-preview` model and
does not mention the former Operator or ChatGPT agent products; we did not verify their current
status, so this table makes no claim about them.

## Open models and frameworks

| Project | State read 2026-11-19 | Level |
| ------- | --------------------- | ----- |
| [OpenCUA][opencucode] ([paper][opencua-paper]) | MIT-licensed models (7B, 32B, 72B), the AgentNet dataset and tools; the paper (v1 2025-08-12) reports 45.0% for the 72B model on OSWorld-Verified | paper |
| [Agent S][agent-s] (Simular) | Apache-2.0 framework; README lists Agent S4 (2026-10-20) and claims 21.3% on OSWorld V2 with an open model, quoting 20.6% for Claude Opus 4.8 and 13.0% for GPT-5.5; the README also claims 72.60% on OSWorld for Agent S3 (2025-12-15) as the first above human performance | vendor claim |
| [UI-TARS-desktop][ui-tars] (ByteDance) | Apache-2.0 desktop app on UI-TARS and Seed-1.5-VL models; the repository is archived and read-only per a note dated 2026-11-09, so treat as frozen | documented |
| [Qwen-UI-Agent report][qwenui] | Abstract reports 79.5% on OSWorld-Verified and 40.0% partial-progress on OSWorld-v2 (submitted 2026-07-30) | vendor claim |

We read none of the weights or code; scores are as reported. "First above human" and "SOTA" are
the vendors' words and are not independently verified.

## The OSWorld family

| Benchmark | What it is | Published numbers (as of) | Level |
| --------- | --------- | ------------------------- | ----- |
| [OSWorld][osworld-paper] | 369 real-computer tasks; paper v1 2024-04-11 | Humans above 72.36%, best model then 12.24% (2024-04-11) | paper |
| OSWorld-Verified | The original tasks with community-reported fixes, announced 2025-07-28 on the [OSWorld site][osworld-site] | Leaderboard is client-side rendered and was not readable; reported scores include 45.0% (OpenCUA-72B, paper v3 2025-10-04) and 79.5% (Qwen-UI-Agent, 2026-07-30) | paper / vendor claim |
| [OSWorld 2.0][osworld2] | 108 long-horizon workflows, humans take a median of about 1.6 hours; the original site notice dated 2026-06-26 points to it as the latest version | Claude Opus 4.8 at 20.6% binary completion and 54.8% partial, GPT-5.5 near 13% (paper v2, 2026-07-13) | paper |
| [OSWorld 2.0 site][osworld2-site] | Leaderboard table had no readable rows (client-side) | Not read | - |

Our reading: the near-80% Verified claims and the roughly 20% 2.0 figures measure different task
sets, so they are not a trend line. Related benchmarks from the 2026-09/10 paper wave, all
single-paper results:

- [OSWorld-Science][osworld-science] (2026-09-30): 146 tasks in scientific software; the authors
  report that strong VLMs with a strong harness still struggle (paper).
- [cua-speedrun][cua-speedrun] (2026-09-30): standardises speed and cost measurement across four
  CUA benchmarks; reports that no model family leads every metric and open-weight models do not yet
  reach the frontier (paper).
- [VeriCUA][vericua] (2026-10-29, marked work in progress): treats task-completion verification as
  agentic exploration; relevant because verifier quality bounds every score above (paper).

The dated benchmark status table lives in [evaluation-data-resources-landscape.md § Benchmark
status][eval-bench]; update scores there, not here.

## Pixels versus accessibility tree

| Observation | Strength | Weakness | Evidence |
| ----------- | -------- | -------- | -------- |
| Screenshot only | Works on any app, no OS integration; the OSWorld authors call it the long-run goal | In 2024 the weakest setting (GPT-4V 5.26%); coordinate errors | [OSWorld paper][osworld-html] Table 5, section 4.2 |
| Accessibility tree only | Exact element handles; in 2024 it led (GPT-4 12.24%) | Trees can reach tens of thousands of tokens; not always exposed by apps | same |
| Screenshot plus tree | Combines both; no clear winner across models in 2024 | Larger context | same |
| Set-of-Mark overlays | Numbered boxes ease grounding | Dense OS elements added noise for one model | same |

The 2024 numbers are old models and old data; they show the trade-off shape, not a current
ranking. Current first-party tools (Claude, OpenAI, Gemini above) are screenshot-first with
model-predicted coordinates. The counter-design is accessibility-only tooling such as
[agent-desktop][agent-desktop], described in the [scraping catalog][scrape-agent-desktop]. A 2026
paper, [Towards Safe Autonomy for Computer Use][sacua], uses the tree differently: it derives
deterministic rules from it to separate trusted screen regions from untrusted ones, and reports an
attack success rate of zero on its own evaluation (paper abstract, not reproduced). Our reading:
pixels buy generality, trees buy precision and a trust signal; hybrid is the likely direction but
we found no current head-to-head across vendors.

## Safety

- **Anthropic (documented):** use a dedicated VM or container with minimal privileges, keep
  sensitive data and logins away from the model, limit internet access to an allowlist, and have a
  human confirm consequential decisions. The docs warn Claude may follow commands found in
  webpages or images, and say classifiers scan screenshots for prompt injection and steer the
  model to check with the user; users can opt out by contacting support.
- **OpenAI (documented):** isolated browser or VM, allow lists, untrusted screen content, no
  credentials on screen, confirmation for consequential actions, step/time/cost limits, and
  verification of actual outcomes. Pending API safety checks can halt a run.
- **Google (documented):** per-step `safety_decision` with seven policy categories; injection
  screening is opt-in.
- **Gap (our reading):** all three keep the final defence at the application level (sandbox plus
  confirmation). Desktop products like Claude Desktop trade that isolation for convenience, and
  say so.
- **Evidence of the risk:** screen-borne injection is catalogued with benchmarks in the
  [agentic AI vulnerability landscape][vuln-landscape] (VPI-Bench, WASP); not repeated here.

## Paper leads

| arXiv | Outcome |
| ----- | ------- |
| [2609.39903][osworld-science] | Cited (benchmark) |
| [2609.40284][cua-speedrun] | Cited (speed and cost) |
| [2610.18508][sacua] | Cited (trust separation via accessibility tree) |
| [2610.40578][vericua] | Cited (verification) |

## Open items

- OSWorld-Verified and OSWorld 2.0 leaderboards are client-rendered; current top rows were not
  read. Re-read with a rendered fetch before quoting a leaderboard rank.
- OpenAI Operator/ChatGPT agent status and the Gemini model GA state were not verified.

## Sources

| Source | Content |
| ------ | ------- |
| [Claude computer use tool docs][claude-cu] | Versions, models, headers, limits, security (read 2026-11-19) |
| [Let Claude use your computer in Cowork][claude-cowork-cu] | Desktop computer use, permissions, no-sandbox statement |
| [OpenAI computer use guide][openai-cu] | Loop, safety guidance |
| [Gemini computer use][gemini-cu] | Actions, safety decisions |
| [OSWorld paper][osworld-paper], [HTML][osworld-html] | Original benchmark, observation-type results |
| [OSWorld site][osworld-site], [OSWorld 2.0][osworld2], [site][osworld2-site] | Verified announcement, 2.0 results |
| [OpenCUA][opencucode], [paper][opencua-paper] | Open models, 45.0% claim |
| [Agent S][agent-s] | README claims, dated |
| [UI-TARS-desktop][ui-tars] | Archived repo |
| [Qwen-UI-Agent][qwenui] | OSWorld-Verified claim |
| [OSWorld-Science][osworld-science], [cua-speedrun][cua-speedrun], [Safe Autonomy][sacua], [VeriCUA][vericua] | 2026 paper leads |

[claude-cu]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool
[claude-cowork-cu]: https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork
[openai-cu]: https://developers.openai.com/api/docs/guides/tools-computer-use
[gemini-cu]: https://aistudio.google.com/docs/computer-use
[ms-cua]: microsoft-365-copilot-analysis.md#computer-using-agents
[osworld-paper]: https://arxiv.org/abs/2404.07972
[osworld-html]: https://arxiv.org/html/2404.07972v2
[osworld-site]: http://osworld-v1.xlang.ai/
[osworld2]: https://arxiv.org/abs/2606.29537
[osworld2-site]: https://osworld-v2.xlang.ai/
[opencucode]: https://github.com/xlang-ai/OpenCUA
[opencua-paper]: https://arxiv.org/abs/2508.09123
[agent-s]: https://github.com/simular-ai/Agent-S
[ui-tars]: https://github.com/bytedance/UI-TARS-desktop
[qwenui]: https://arxiv.org/abs/2607.28227
[osworld-science]: https://arxiv.org/abs/2609.39903
[cua-speedrun]: https://arxiv.org/abs/2609.40284
[sacua]: https://arxiv.org/abs/2610.18508
[vericua]: https://arxiv.org/abs/2610.40578
[agent-desktop]: https://github.com/vercel-labs/agent-desktop
[scrape-agent-desktop]: ../infrastructure/web-scraping-extraction-landscape.md
[eval-bench]: ../../sdlc-lcm/evaluation-data-resources-landscape.md
[vuln-landscape]: ../../sdlc-lcm/agentic-ai-vulnerability-landscape.md
