---
title: Computer-Use Agents Landscape
source: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool
purpose: "Landscape of agents that operate a GUI from screen observations: Claude computer use, other vendors' tools, open models, the OSWorld benchmark family, pixel vs accessibility-tree, and safety."
created: 2026-11-19
updated: 2026-11-27
validated_links_on: 2026-11-19
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
  versions still need one. Claude Desktop also exposes it to end users (documented, research
  preview).
- The OSWorld family splits in two: OSWorld-Verified (original tasks, fixed; its published
  workbook lists rows above 85%) and OSWorld 2.0 (long-horizon; the site's results file, updated
  2026-11-14, lists a best official full-set binary score of 44.33%). Scores from the two are not
  one trend.
- Screenshot-only versus accessibility-tree input is a real design axis, not a settled one: 2024
  evidence favoured structured input, the vendor computer-use tools documented here take screenshots as their main input (our reading), and a 2026 paper
  uses the accessibility tree for security rather than perception.
- A third route skips the screen: an MCP server drives the app through its scripting API, as MCP for
  Blender does and community bridges do for Bonsai (IFC/BIM); exact control, but the main tool runs
  code in the live session (see [App bridges](#app-bridges-instead-of-screens-blender-and-bonsai-checked-2026-11-24)).
- Every vendor says the same about safety: isolate the environment, treat screen content as
  untrusted, confirm consequential actions.

## First-party Claude computer use

**Claude API tool (documented, page read 2026-11-19).** Per the [computer use tool docs][claude-cu]:

| Item | Documented state |
| ---- | ---------------- |
| Current version | `computer_toolset_20260801`; the request "needs no beta header" |
| Models on the current toolset | Claude Fable 5.2, Mythos 5.2, Opus 5.5, Sonnet 5.5, Haiku 5.5 are named in the details; the page's `supportedModels` list also names Fable 5.1 and 5, Mythos 5.1, 5 and Preview, Opus 5, Sonnet 5 and Opus 4.8 (several of these are also listed for `computer_20251124`) |
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

**Claude Desktop (documented, research preview).** The [Claude Code desktop docs][claude-desktop]
call computer use a "research preview" on macOS and Windows for Pro, Max and Ultra plans, not
available on Team or Enterprise, off by default, with macOS 14 or later plus Accessibility and
Screen Recording permissions. Access is per app, with fixed control tiers by app category (view
only for browsers and trading platforms, click only for terminals and IDEs, full control for the
rest). The docs state that, unlike the sandboxed Bash tool, it runs on your actual desktop. The
support article [Let Claude use your computer in Cowork][claude-cowork-cu] says Claude tries
connectors first, then a browser, and uses screen control only if neither works; it also states
there is no sandbox between Claude and your apps, that Team and Enterprise do not have computer
use, and that background-window operation needs macOS 15 or later (a separate feature from the
macOS 14 minimum above, not a conflict). For the Cowork product and enterprise controls see the
[Cowork enterprise analysis][cowork-ent].

**Pointer only:** Claude in Chrome (browser extension) is a browser agent and is covered under the
[browser-agents topic](browser-agents-landscape.md), not here.

## Other vendors

| Vendor | What the docs say (read 2026-11-19) | Level |
| ------ | ----------------------------------- | ----- |
| OpenAI | [Computer use guide][openai-cu]: a `computer` tool in the Responses API; model returns a `computer_call` with an ordered action list, your code executes and returns a screenshot via `computer_call_output`. For its newest model the page recommends code execution instead and keeps the computer tool "as an alternative". No benchmark numbers on the page | documented |
| Google | [Gemini computer use][gemini-cu]: browser, mobile and desktop action sets; coordinates normalised so you do not send display size; each step can carry a `safety_decision` (allowed, require confirmation, blocked); prompt-injection screening is opt-in | documented |
| Microsoft | Researcher's Computer Use, Copilot Studio computer use and the Foundry computer-use tool are already compared in [Microsoft 365 Copilot analysis, Computer-using agents][ms-cua]; not repeated here | documented (see that doc) |
| Open models | See next section | mixed |

The OpenAI page does not state a deprecation date for the older `computer-use-preview` model and
does not mention the former Operator or ChatGPT agent products; we did not verify their current
status, so this table makes no claim about them.

## Open models and frameworks

| Project | State read 2026-11-19 | Level |
| ------- | --------------------- | ----- |
| [OpenCUA][opencucode] ([paper][opencua-paper]) | MIT-licensed models (7B, 32B, 72B), the AgentNet dataset and tools; the abstract of the current version (v3, 2025-10-04) reports 45.0% for the 72B model on OSWorld-Verified (v1, 2025-08-12, predates the 72B result) | authors' claim |
| [Agent S][agent-s] (Simular) | Apache-2.0 framework; README lists Agent S4 (2026-10-20) and claims 21.3% on OSWorld V2 with an open model, quoting 20.6% for Claude Opus 4.8 and 13.0% for GPT-5.5; the README also claims 72.60% on OSWorld for Agent S3 (2025-12-15) as the first above human performance, and a 2026-08-28 entry saying Simular's production agent Sai tops OSWorld 2.0 with an unexplained "(73%)". The leaderboard file lists Sai with Opus 5 at 41.67% binary and 79.38% partial (no official flag), so the 73% matches neither; we could not reconcile it | vendor claim |
| [UI-TARS-desktop][ui-tars] (ByteDance) | Apache-2.0 desktop app on UI-TARS models; archived (read-only), about 39,600 stars, last push 2026-10-09 (GitHub API, 2026-11-22), so treat as frozen | documented |
| [Qwen-UI-Agent report][qwenui] | Abstract reports 79.5% on OSWorld-Verified and 40.0% partial-progress on OSWorld-v2 (submitted 2026-07-30) | authors' claim |
| [Nod][nod] (n8n) | Scope note: a personal agent that also drives websites in a browser container, listed here because it acts on apps and sites for the user; whether it works from screenshots was not verified. Apache-2.0 personal agent that runs on your machine with a model you choose; it works Gmail, Calendar, Slack, Notion and websites through a server-side sandbox container and a Chromium browser container, and asks before it acts. README status badge: research preview; created 2026-09-25, about 4,200 stars, latest release `nod-v0.10.0` (GitHub API, read 2026-11-27). The README builds on the Pi agent runtime, agent-browser, Composio and MCP, and runs a trust check on each app action and each website step that can change something. It reports 98% of 226 errands finished (3 runs each) and 0 unsafe actions in those 678 runs, in simulated accounts and sites with one model in October 2026. Whether its browser agent works from screenshots or page structure we did not verify | documented (project); vendor claim (benchmarks) |

We read none of the weights or code; scores are as reported (the Nod figures are n8n's own, from its README). "First above human" and "SOTA" are
the vendors' words and are not independently verified.

## The OSWorld family

This doc is the home for dated OSWorld scores; the benchmark table in [evaluation-data-resources
§ 2][eval-bench] keeps the description and one top figure and links here.

| Benchmark | What it is | Scores (as of) | Level |
| --------- | --------- | -------------- | ----- |
| [OSWorld][osworld-paper] | 369 real-computer tasks; paper v1 2024-04-11 | Humans above 72.36%, best model then 12.24% (2024-04-11) | paper |
| OSWorld-Verified | The original tasks with community-reported fixes, announced 2025-07-28 on the [OSWorld site][osworld-site]; the site notice dated 2026-06-26 points to 2.0 as the latest version | The site's published [results workbook][osworld-verified-xlsx] (1,076 rows, newest row dated 2026-08-01, read 2026-11-19) lists, by success rate at a 100-step budget: Intelligence-Indeed Agent 90.19% (2026-07-25, uses coding actions), claude-fable-5 85.96% and claude-opus-5 83.39% (both 2026-08-01, no extra coding or a11y tree), Pointer Agent with Opus 4.7 83.64%. The workbook has no official or verified column, so the review status of each row is unknown to us. Earlier claims: OpenCUA-72B 45.0% (authors' claim, 2025-10-04); Qwen-UI-Agent 79.5% (authors' claim, 2026-07-30) | leaderboard file (rows as listed) |
| [OSWorld 2.0][osworld2] | 108 long-horizon workflows, humans take a median of about 1.6 hours; paper v2 2026-07-13 reports Claude Opus 4.8 at 20.6% binary and 54.8% partial, GPT-5.5 near 13% | The site's [results file][osworld2-json] (reported `updatedAt` 2026-11-14, read 2026-11-19), 500-step default. Official end-to-end rows: Claude Opus 5 at max reasoning 44.33% binary / 77.67% partial on the full set (release v2.1), and 48.65% / 79.2% on the "offline" subset; MuseSpark 1.3 39.25% full. Rows without the official flag: Darwinx with Opus 4.8 44.44% / 75.97% (Salesforce AI Research, paper-linked), Sai with Opus 5 41.67% / 79.38% (Simular). Agent S4's 21.3% claim (README, 2026-10-20) predates these rows | paper; leaderboard file (official flag as given) |

Our reading: the Verified and 2.0 scores measure different task sets and are not one trend. The
2.0 best moved from about 20% in the paper to above 44% in the file within months, so quote a 2.0
figure only with its release version, model, reasoning setting and official flag. We did not rerun
anything. Related benchmarks from the 2026-09/10 paper wave, all single-paper results:

- [OSWorld-Science][osworld-science] (2026-09-30): 146 tasks in scientific software; the authors
  report that strong VLMs with a strong harness still struggle (paper).
- [cua-speedrun][cua-speedrun] (2026-09-30): standardises speed and cost measurement across four
  CUA benchmarks; reports that no model family leads every metric and open-weight models do not yet
  reach the frontier (paper).
- [VeriCUA][vericua] (2026-10-29, marked work in progress): treats task-completion verification as
  agentic exploration; relevant because verifier quality bounds every score above (paper).

## Pixels versus accessibility tree

| Observation | Strength | Weakness | Evidence |
| ----------- | -------- | -------- | -------- |
| Screenshot only | Works on any app, no OS integration; the OSWorld authors call it the long-run goal | In 2024 the weakest setting (GPT-4V 5.26%); coordinate errors | [OSWorld paper][osworld-html] Table 5, section 4.2 |
| Accessibility tree only | Exact element handles; in 2024 it led (GPT-4 12.24%) | Trees can reach tens of thousands of tokens; not always exposed by apps | same |
| Screenshot plus tree | Combines both; no clear winner across models in 2024 | Larger context | same |
| Set-of-Mark overlays | Numbered boxes ease grounding | Dense OS elements added noise for one model | same |

The 2024 numbers are old models and old data; they show the trade-off shape, not a current
ranking. In the docs read here, Claude and Gemini describe screenshot-driven loops with model-predicted
coordinates, and OpenAI's loop returns screenshots too (our reading: screenshot-centred). The counter-design is accessibility-only tooling such as
[agent-desktop][agent-desktop], described in the [scraping catalog][scrape-agent-desktop]. A 2026
paper, [Towards Safe Autonomy for Computer Use][sacua], uses the tree differently: it derives
deterministic rules from it to separate trusted screen regions from untrusted ones, and reports an
attack success rate of zero on its own evaluation (paper abstract, not reproduced). Our reading:
pixels buy generality, trees buy precision and a trust signal; hybrid is the likely direction but
we found no current head-to-head across vendors.

### App bridges instead of screens: Blender and Bonsai (checked 2026-11-24)

A third option skips the screen and the tree: an MCP (Model Context Protocol) server talks to the application's own
scripting API. [MCP for Blender][blender-mcp] (`ahujasid/mcp-for-blender`, formerly
`blender-mcp`; MIT, 35,524 stars, last push 2026-11-18, GitHub API 2026-11-24) is the widely used
example. A Blender add-on opens a local socket and the MCP server sends commands to it; the README
lists nine tools, led by `execute_blender_code` ("Run Python in your live Blender"), plus scene
inspection, viewport images and asset import. Its own warnings: the tool runs arbitrary Python, and
the socket "has no authentication or encryption", so it should stay on `localhost`. It also records
a minimal anonymous usage event by default; content collection is opt-in (README).

[Bonsai][bonsai-docs] is the add-on for IFC (Industry Foundation Classes, the open building information modelling, or BIM, exchange standard) in Blender, part of
[IfcOpenShell][ifcopenshell] (repo 2,988 stars; Bonsai's folder is GPL-3.0, the libraries LGPL-3.0;
latest stable release `bonsai-0.9.0`, 2026-09-29). Its docs landing page mentions no AI or MCP feature (read
2026-11-24). Two small community MCP bridges add IFC tools on top of the Blender
pattern; both are early, with about 70 stars each:

- [Bonsai_mcp][bonsai-mcp] (MIT, last push 2026-09-06): a fork of the Blender MCP server that keeps
  its code-execution tool and adds IFC inspection tools (project info, entities, properties, spatial
  structure, relationships, quantities).
- [ifc-bonsai-mcp][ifc-bonsai-mcp] (MIT, last push 2026-07-10): claims over 50 tools for IFC
  analysis and parametric creation, and a local RAG (retrieval-augmented generation) index over the IFC and IfcOpenShell docs
  (vendor claim, not tested here).

The same app-API route appears in [CLI-Anything][cli-anything] (a generated CLI per app, Blender via
`bpy`). For evaluation, [IFC-MCQ][ifc-mcq] (arXiv, submitted 2026-10-21) generates multiple-choice
benchmarks from IFC files and tests two agent set-ups using tool- and code-based retrieval. Our
reading: an app bridge gives exact, scriptable control without coordinate errors, but its main tool is
code execution in the user's live session, so the [Safety](#safety) guidance applies at least as
strongly as for screen agents.

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

- The OSWorld-Verified workbook has no official or verified column and was read from one
  download; re-read the live leaderboard before quoting a rank. The Sai "(73%)" README figure is
  unreconciled.
- OpenAI Operator/ChatGPT agent status and the Gemini model GA state were not verified.

## Sources

| Source | Content |
| ------ | ------- |
| [Claude computer use tool docs][claude-cu] | Versions, models, headers, limits, security (read 2026-11-19) |
| [Claude Code desktop docs][claude-desktop] | Desktop computer use: research preview, plans, macOS 14, permission tiers, not sandboxed |
| [agent-desktop][agent-desktop] | Accessibility-tree desktop CLI; latest release v1.3.1 published 2026-11-13 (GitHub API, 2026-11-19) |
| [Cowork enterprise analysis][cowork-ent] | Existing corpus coverage of Cowork |
| [Let Claude use your computer in Cowork][claude-cowork-cu] | Desktop computer use, permissions, no-sandbox statement |
| [MCP for Blender][blender-mcp] | Socket add-on, nine tools, code-execution and socket warnings, telemetry defaults (README; GitHub API 2026-11-24) |
| [Bonsai docs][bonsai-docs] · [IfcOpenShell][ifcopenshell] | Bonsai Studio as the IFC authoring add-on; licences from the `COPYING` files; release `bonsai-0.9.0` (GitHub API 2026-11-24) |
| [Bonsai_mcp][bonsai-mcp] · [ifc-bonsai-mcp][ifc-bonsai-mcp] | Community IFC MCP bridges (READMEs; GitHub API 2026-11-24) |
| [IFC-MCQ][ifc-mcq] | Multiple-choice benchmarks generated from IFC files for LLM agents (abstract, read 2026-11-24) |
| [OpenAI computer use guide][openai-cu] | Loop, safety guidance |
| [Gemini computer use][gemini-cu] | Actions, safety decisions |
| [OSWorld paper][osworld-paper], [HTML][osworld-html] | Original benchmark, observation-type results |
| [OSWorld site][osworld-site], [Verified workbook][osworld-verified-xlsx], [OSWorld 2.0][osworld2], [2.0 results file][osworld2-json] | Verified announcement and results, 2.0 results |
| [OpenCUA][opencucode], [paper][opencua-paper] | Open models, 45.0% claim |
| [Agent S][agent-s] | README claims, dated |
| [UI-TARS-desktop][ui-tars] | Archived repo |
| [Qwen-UI-Agent][qwenui] | OSWorld-Verified claim |
| [n8n Nod][nod] | README, LICENSE and release (GitHub API, read 2026-11-27) |
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
[opencucode]: https://github.com/xlang-ai/OpenCUA
[opencua-paper]: https://arxiv.org/abs/2508.09123
[agent-s]: https://github.com/simular-ai/Agent-S
[ui-tars]: https://github.com/bytedance/UI-TARS-desktop
[qwenui]: https://arxiv.org/abs/2607.28227
[nod]: https://github.com/n8n-io/nod
[osworld-science]: https://arxiv.org/abs/2609.39903
[cua-speedrun]: https://arxiv.org/abs/2609.40284
[sacua]: https://arxiv.org/abs/2610.18508
[vericua]: https://arxiv.org/abs/2610.40578
[agent-desktop]: https://github.com/vercel-labs/agent-desktop
[scrape-agent-desktop]: ../infrastructure/web-scraping-extraction-landscape.md
[eval-bench]: ../../sdlc-lcm/evaluation-data-resources-landscape.md#2-benchmarks
[osworld-verified-xlsx]: https://osworld-v1.xlang.ai/static/data/osworld_verified_results.xlsx
[osworld2-json]: https://osworld-v2.xlang.ai/static/data/leaderboard/official-results.json
[claude-desktop]: https://code.claude.com/docs/en/desktop.md
[cowork-ent]: ../../cc-native/plugins-ecosystem/CC-cowork-plugins-enterprise-analysis.md
[vuln-landscape]: ../../sdlc-lcm/agentic-ai-vulnerability-landscape.md
[blender-mcp]: https://github.com/ahujasid/mcp-for-blender
[bonsai-docs]: https://docs.bonsaibim.org/
[ifcopenshell]: https://github.com/IfcOpenShell/IfcOpenShell
[bonsai-mcp]: https://github.com/JotaDeRodriguez/Bonsai_mcp
[ifc-bonsai-mcp]: https://github.com/Show2Instruct/ifc-bonsai-mcp
[ifc-mcq]: https://arxiv.org/abs/2610.30533
[cli-anything]: ../../cc-native/agents-skills/CC-cli-anything-analysis.md
