---
title: Software Factory Landscape
purpose: Disambiguates three unrelated meanings of "software factory" — historical, DevSecOps-vendor, and agentic-AI — and rubric-scores the agentic implementations with concrete artefacts.
created: 2026-09-30
updated: 2026-11-19
validated_links: 2026-11-19
status: assess
---

## What It Is

"Software factory" is reused across three unrelated eras and communities. Conflating them loses the
point of each. This page keeps them apart, then focuses on the third — the one active in this corpus's
agentic-SDLC research ([agentic-sdlc-patterns.md](agentic-sdlc-patterns.md)).

## (a) Historical: two industrial lineages

**Japanese industrial movement.** Hitachi was the first company to adopt the term, in 1969 with its
Hitachi Software Works,
followed by System Development Corporation (1975), then NEC, Toshiba and Fujitsu (1976–1977). Cusumano's
framework traces six phases from the mid-1960s to the late 1980s — basic organization, technology
standardization, process mechanization, then refinement — applying manufacturing-style reuse and
standardization to control-systems, nuclear-reactor and turbine software ([Wikipedia][wp-sf]).

**Microsoft's "Software Factories" methodology (Greenfield & Short, 2004).** A later, distinct lineage:
"a software factory is a software product line that configures extensive tools, processes and content
using a template based on a schema" — factory schemas, reference implementations, DSLs and model-driven
assembly rather than industrial-era process mechanization ([Wikipedia, "Description" section][wp-sf]).
The Apress book chapter "Software Factory Schema: Architecture" (in *Practical Software Factories in
.NET*, Apress, 2006 — metadata via Crossref, `doi.org/10.1007/978-1-4302-0181-6_4`) belongs to this
lineage. The chapter itself is paywalled: `link.springer.com` redirects every request (including the PDF
route) to `idp.springer.com` for institutional login (observed 2026-09-30), so only the DOI metadata
above is citable, not the content.

Wikipedia presents the two as parallel traditions addressing the same problem from different
organizational philosophies, not a single genealogy ([Wikipedia][wp-sf]).

## (b) DevSecOps / defense-vendor framing

Two large vendors reuse the term for their own delivery organizations. Treat both as **self-reported**
marketing framing, not independent evidence.

**Lockheed Martin** describes its "Software Factory" as a DevSecOps-driven engineering operation for
aerospace and defense, embedding security at every stage, using Kubernetes containerization, GitOps
(version-controlled IaC with automated rollback) and microservices, demonstrated on F-35 software
upgrades, Cognitive Mission System Products and the SmartSat platform. Its own framing claims builds "systems in
minutes, not days" — unverified, self-reported ([Lockheed Martin][lockheed]).

**VMware/Broadcom**'s `vmware.com/topics/software-factory` page is a client-rendered single-page app — the
server response is an empty `<div id="root">` with no static body text, so only the page's own
server-rendered `<meta name="description">` is citable as first-party content: "A software factory is an
organized approach to software development that provides software design and development teams a
repeatable, well-defined path to create and update software" ([VMware][vmware]).

## (c) Agentic software factory — the focus

The AI-coding-agent sense: a pipeline where agents write, test, and (in every source below) ship code
under **human gates that stay at specification and merge**, not a fully autonomous "lights-off" system.

**CircleCI** (published 2026-09-18) defines it as "a system for turning engineering intent into
production software through repeatable, increasingly automated workflows," and argues agents move the
bottleneck from writing code to validating it. Concrete practices: inner/outer-loop validation (fast
targeted checks, then full independent verification before merge), test intelligence (selective,
change-scoped testing), short-lived OIDC auth and least-privilege secrets, and CI feedback agents can
read directly through an API (a CircleCI MCP server and CLI) ([CircleCI][circleci]).

**Augment Code**'s guide defines an agentic software factory as "an agentic software-delivery operating
model in which AI agents write, test, and ship code inside a pipeline whose specifications and merge
approvals stay under human control," identifying verification as "the factory's binding constraint." Its five stages — Intake,
Specification (human-approved before coding: "reviewing a plan takes minutes. Reviewing a 2,000-line pull
request built on a misread requirement takes days"), Build (isolated parallel agent environments),
Verification (automated + human judgment), Shipping (human-owned governance and audit trail) — keep human
gates at spec and ship ([Augment Code][augment]).

**freeCodeCamp**'s Claude Code tutorial gives the same shape concrete tooling: a five-layer stack
(Context, Knowledge, Agent, Workflow, Delivery), a `CLAUDE.md` kept to "100 to 300 lines," reusable
`.claude/skills/<name>/SKILL.md` procedures, seven narrow-scoped subagents (codebase-researcher,
story-writer, spec-writer, backend-builder, frontend-builder, test-verifier,
implementation-validator), hook-enforced gates, and an orchestrator that routes
Explore→Story→Brief→Build→Test→Validate→PR with human approval after the story and technical-brief
stages ([freeCodeCamp][fcc]).

**The `ai-that-works` episodes are conversations, not shipped code.** Each of the four episode
directories (`github.com/ai-that-works/ai-that-works`) also contains an `email.json` (plus, in two of
the four, a stray `Untitled` file or a `whiteboard-1.png` image) alongside `README.md`, `email.md`,
`meta.md` and `transcript.txt` — no source/code files. The repo itself carries no LICENSE file
(`license: null` via the GitHub API, verified 2026-09-30), so nothing here is reusable beyond citation.
Read as design-lens sources, self-reported claims flagged:

- **2026-06-23, "Software Factory for Agent Tools"**: a nightly self-improving loop — an agent attempts a
  task, a second agent analyzes failures ("trophies"), dedupes them, files Linear tickets, and a third
  agent opens PRs validated by CI instead of local runs (self-reported: cuts test cycles from
  15–20 minutes to 2–4). Humans approve findings and direction, not code ([ep. #63][aiw-1]).
- **2026-08-25, "Software Factory Design Patterns"**: a four-layer architecture — Compute, Dev
  Environment, Harness (Claude Code / Codex / Pi), Orchestration — argued as "composition over
  inheritance" over monolithic vendor stacks; notes that no harness yet standardizes lifecycle hooks
  despite protocols like ACP and AG-UI existing ([ep. #71][aiw-2]).
- **2026-09-01, "Code Mode for Extensible Software"** (not Claude Code's experimental Code Mode; see [CC-tools-inventory.md](../cc-native/configuration/CC-tools-inventory.md#code-mode-v21323)): agents write executable code against an API
  instead of many discrete tool calls (bash itself is cited as an existing "code mode"); HumanLayer's
  example edits a YJS CRDT via generated JavaScript sandboxed in QuickJS (not Node.js, filesystem/shell
  access denied) ([ep. #72][aiw-3]).
- **2026-09-08, "Hands-On with Real Builders"**: two named practitioners, both self-reported and without
  a linked repo — Tyler Brown (a HIPAA-compliant chat startup reporting ARR growth from roughly $270K to
  $400K over three months after restructuring around agents and a plan-do-verify loop) and Cole Murray
  (maintainer of "Open Inspect," described as an open-source background-agent system deployed at
  companies with up to 500 engineers; no repository link is given in the episode)
  ([ep. #73][aiw-4]). A public repo of that name exists, [`open-inspect/background-agents`][open-inspect], but the episode does not link it, so tying the two together is our inference.

**HumanLayer's dissent: "Why Software Factories Fail" (`wsff.md`, Dex Horthy).** First published
2026-07-22 in `github.com/humanlayer/advanced-context-engineering-for-coding-agents` (also unlicensed —
`contents/LICENSE` 404s, verified 2026-09-30; not the same document as this repo's separately-cited
[ACE-FCA blog post][hlyr-ace-xref], by the same author but a different piece). It defines a 2022 baseline
"software factory" as people deciding, tracking, implementing, reviewing by PR, shipping, monitoring and
feeding user input back in a loop, and a "lights-off factory" as that same loop with human code review
removed. Its central argument: current coding models optimize for passing tests (a seconds-scale signal)
while codebase maintainability erodes over weeks or months, because "there is no penalty for eroding
codebase maintainability" in how these models are trained or rewarded — so a fully autonomous factory
degrades a codebase even while every generated test passes. Its proposed alternative keeps a human-in-the
loop across four phases (Product Requirements → System Architecture → Program Design → Vertical Slices),
claiming (self-reported, unbenchmarked here) 2–3x faster delivery without the quality loss
([wsff.md][wsff]).

**Cloudflare's Astro issue triage — the concrete production case.** Published 2026-08-04: an automated
pipeline of isolated subagents running in GitHub Actions, driven as a label-based state machine through
four phases — reproduce (clone and confirm), diagnose (instrument and log), verify (cross-check tests,
comments, docs), fix (convert the reproduction into a failing test, then a patch). A found fix generates
a preview build via `pkg.pr.new`, posts findings to the issue, and opens a PR once a human confirms.
Reported result (first-party operator observation, not a benchmark): open issues fell from over 200 to
roughly 30, on track for the repository's first zero-open-issue month in 5+ years. Cloudflare generalized
the pipeline into two artefacts: **Flue**, described on its own site as "The Open Agent Framework" for
durable, resumable TypeScript agents — its own site links a public GitHub repo
([`github.com/withastro/flue`][flue-repo], Apache-2.0, ~8,400 stars as of 2026-09-30); unlike
triagebot-action it has not yet been rubric-scored here; and **triagebot-action**
(`github.com/withastro/triagebot-action`), a real, forkable GitHub Action other teams have adopted — no
LICENSE file (`license: null`, 220 stars, last pushed 2026-08-28), rubric-scored below
([Cloudflare][cf-astro]).

**Anthropic's own source-control migration — the vendor's own internal case.** Published 2026-10-13
(updated 2026-10-15): Anthropic's engineering blog reports that daily merged code changes to its monorepo
rose from "around 2,500 code changes merged per day" in May 2026 to "over 30,000 per day" by September
2026, and that it fully migrated the monorepo off git, in five months, to an in-house version control
system called **Scion**. The post frames this as the same bottleneck shift the sources above argue for,
stating "The bottleneck, now, is all of the developer infrastructure built for human scale: source
control, builds, and CI" — infrastructure that could not keep up once agents, not humans, were
generating most of the diffs; it also cites on the order of 25 million code checkouts per day for CI.
Alongside Scion,
Anthropic built a code-review surface (**Antique**) and a source-control IAM system in the same window.
Scion is explicitly scoped as a monorepo-specific replacement, not a general git substitute, and no
rubric row is added here: this is vendor-reported internal tooling with no independently verifiable
shipped artefact (unlike triagebot-action above) ([Anthropic][anthropic-scion]).

**The 2026 company wave: named in-house or open-sourced pipelines.** Several companies now describe a named agent pipeline for their own code, each first-party (fetched 2026-11-14):

- **Stripe Minions**: "Stripe’s homegrown coding agents. They’re fully unattended and built to one-shot tasks." Part 1 reported "over a thousand pull requests merged each week" that are "completely minion-produced"; Part 2 (published 2026-02-19) updates this to "Over 1,300 Stripe pull requests (up from 1,000 as of Part 1) merged each week", still human-reviewed with no human-written code. The agent loop runs on a fork of Block’s goose ([Part 1][minions]; [Part 2][minions2]). Vendor claim, self-reported; see the evidence subsection below for the pipeline's CI and review limits.
- **Ramp Inspect** (2026-10-27): in the past month "99% of our engineering, design, and product teams used Inspect, and Inspect now accounts for 74% of merged PRs" ([Ramp][inspect]). An unaffiliated open-source take, `open-inspect/background-agents` (MIT), describes itself as "inspired by Ramp’s Inspect" ([repo][open-inspect]).
- **WorkOS Horizon** (2026-05-06): "an internal code factory" that spawns long-running agent sessions in a cloud sandbox on external events; "no code gets merged without explicit human approval" ([WorkOS][horizon]).
- **OpenAI Symphony**: an open-source orchestrator that "turns a project-management board like Linear into a control plane for coding agents"; OpenAI writes that among some teams "we saw the number of landed PRs increase by 500% in the first three weeks" ([OpenAI][symphony]; [`openai/symphony`][symphony-repo], Apache-2.0).
- **Delinea (StrongDM) Software Factory**: agents "generate code, validate it against real-world behavior, and iterate until it converges, without hand-tuning or human review" — "validation replaces code review" ([Delinea][delinea]). Delinea announced its acquisition of StrongDM on 2026-03-05 ([press release][delinea-news]). Its agent spec is open: [`strongdm/attractor`][attractor] (Apache-2.0), "a non-interactive Coding Agent sufficient for use in a Software Factory".
- **Templates**: Vercel Labs’ [`eve-software-factory-template`][eve] (MIT) describes itself only as "Meet Foreman, an eve Software Factory"; its README was not reviewed here.

Vocabulary differs: only Delinea and Vercel’s template use "software factory"; WorkOS says "code factory", and Stripe, Ramp and OpenAI use neither. Only Delinea claims validation replaces human review; Stripe, Ramp and WorkOS keep a human reviewer. The productivity figures are each company’s own, unaudited.

### Economics, failure and verification evidence

Two evidence classes, kept apart. **Company claims** are self-reported, unaudited and unreplicated. **Measured studies** are arXiv papers (abstract pages read 2026-11-19); the abstract is the only part checked here, so sample details beyond it are not claimed. A merged PR is a proxy for output, not for delivered value.

**Company claims (vendor claim, self-reported).**

- **Throughput.** Stripe: over 1,300 minion-produced PRs merged per week, as of the Part 2 post (2026-02-19; Part 1 said about 1,000). The pipeline allows one iteration against the full CI suite; if failures remain after a second push and CI run, the branch returns to its human operator ([Stripe Part 2][minions2]).
- **Cost.** Uber (post dated 2026-08-27): "cost per session is down 52% from its June peak", with the model held constant over February to July and cost data starting at end of May; total AI spend "relatively stabilized since April" while weekly active users across agentic offerings grew 7x and weekly agentic requests 9.4x over February to August 2026. More than 70% of PRs are "attributed to local or cloud agents" (attribution method not stated), and uReview "handles AI code review for all pull requests" ([Uber][uber-sf]). Cost per session is not cost per merged PR: neither Uber nor Stripe publishes a throughput-per-dollar figure, so that question is open in this corpus.

**Measured studies.**

| Question | Study (date) | Finding | Caveat |
|---|---|---|---|
| Base data | [AIDev][aidev], 2026-02-09 | 932,791 agent-authored PRs across 116,211 repositories and 72,189 developers (five agents: Codex, Devin, Copilot, Cursor, Claude Code); curated subset of 33,596 PRs in 2,807 repositories with over 100 stars | Public GitHub only; a dataset, not an outcome measure |
| Throughput at one firm | [Microsoft CLI-agent rollout][ms-cli], 2026-07-01 | Adopters merged "roughly 24% more pull requests", lift persisting over the four-month window | Merged PRs are the authors' own proxy; "tens of thousands of engineers", no exact n in the abstract |
| Review bottleneck | [Code review agents in PRs][cra-study], 2026-04-03 | In 3,109 AIDev PRs reviewed by review agents, agent-only-reviewed PRs merged at 45.20% vs 68.37% human-only-reviewed (23.17 points lower); 12 of 13 review agents average a signal ratio under 60% | Association, not cause; the signal analysis covers only 98 closed agent-reviewed PRs |
| Post-merge maintenance | [Post-merge fate][postmerge], 2026-07-10 | Over 182 repositories overall maintenance rates are similar, but agentic code needs significantly more corrective maintenance and adds more security weaknesses and dependency vulnerabilities; each 10-point rise in a project's no-review rate goes with roughly 6% more agentic maintenance burden | Observational; association with the no-review rate is not proof that review prevents the burden |
| Policy compliance | [SWE-CC][swecc], 2026-10-05 | Across 12 repositories, 823 policies, 500 tasks, four LLMs and two scaffolds, functionally correct patches still violate 43.1% of applicable policies, with nearly half of violations in intermediate execution steps | Benchmark built from SWE-bench Verified tasks, not production traffic |
| Compounding failure | [FeatureArc][featurearc], 2026-10-27 | Ten agents on 73 tasks: pooled success 62.7% at the first stage but 28.5% when the whole feature is tested on final code; 72.9% of failed later stages involve inherited defects, and agents leave an earlier error unnoticed about 95% of the time | Benchmark with curated tasks; pooled figures hide per-agent spread |
| Verification gate | [FlowAgent][flowagent], 2026-10-05 | Google's pre-submit repair agent: 67.18% correct on 195 manually evaluated failures; fixes suggested on 295,508 changes, previewed on 65,069 and applied on 28,554, with pre- and post-execution abstention filters | Google-internal deployment; "applied" is not "correct"; no numbers are given for the filters' effect |

Reading across them, without claiming more than the caveats allow:

- **Review is where the evidence is thinnest.** Stripe keeps a human reviewer and Uber runs uReview on every PR (both vendor claims), while the post-merge study links a higher no-review rate to more agentic maintenance and the review-agent study sees lower merge rates for PRs reviewed only by agents. None of these measures review quality or what review catches.
- **Passing tests is not enough.** SWE-CC (correct patches still breaking repository policy) and FeatureArc (errors inherited across stages) both say a green test run at one stage is weak evidence for the whole feature. This supports the "gate at specification and at merge" convergence below, but is benchmark evidence, not a field study.
- **Abstention is a verification design.** FlowAgent's filters decline to suggest rather than guess; the abstract gives the funnel (suggested, previewed, applied) but not rollback outcomes.
- **Rollback and incident evidence is absent.** None of the sources above reports revert rates or incidents for agent merges; the post-merge study's corrective-maintenance rate is the nearest proxy. Treat factory failure-rate claims as unmeasured until such data appears.

Review products that sell the gate side are in [code-review-products-landscape.md](../non-cc/infrastructure/code-review-products-landscape.md); the lifecycle patterns it feeds are in [agentic-sdlc-patterns.md](agentic-sdlc-patterns.md).

### The convergence — and why it matters

Four independent sources (CircleCI, Augment Code, freeCodeCamp, and HumanLayer's own dissent) land on the
same design: agents build fast; humans gate at **specification** and at **merge/ship**, not in between.
`wsff.md`'s argument for *why* — training rewards test-passing, not long-horizon maintainability — is the
mechanism that makes the other three's gate placement load-bearing rather than merely cautious.

This independently reproduces the phase shape this repo's own unattended-execution discipline already
encodes: front-load everything agent-runnable into one phase, batch every owner-gated decision into a
single sitting, then let the agent resume once gates clear. Neither side cites the other, so the overlap
is a convergence of practice, not a derivation — suggestive that the gate placement is not merely a house
style, though four sources are not proof.

André Lindenberg's *From Loops to Graphs* (LinkedIn, 2026-07-25; `linkedin.com/pulse/from-loops-graphs-andré-lindenberg-m8jae`) names this same convergence from the opposite direction — "graph engineering", a weeks-old and
contested coinage (not an established industry term; see the ladder-rung entry's own hedge) for wiring
already-loop-shaped agents into exactly the graph these four sources each ship — with the full
ladder-rung treatment in [agentic-engineering-disciplines-landscape.md §1][disciplines-graph].

**Design lens.** An owner-surfaced opinion sharpens the stakes: rUv (Reuven Cohen), in a 2026-09-29
LinkedIn post (`linkedin.com/posts/reuvencohen_there-is-no-moat-anything-you-can-build-ugcPost-7510686171975458816-6I5W`,
short link `lnkd.in/p/eB5D2kMw`; written as plain text, not a link — LinkedIn blocks lychee), argues that
software stops shipping discrete versions and instead evolves continuously, and that the advantage shifts
to whoever understands and adapts to a change fastest. That is opinion, not evidence, but it composes with
the finding above: the faster software factories iterate, the more the four sources' human gates — and
this corpus's own Traceable/Versionable emphasis (commit-per-change, audited history, replayable runs) —
matter, precisely because understanding "what changed" is only possible if every change is recorded.
Human-in-the-loop review is not in tension with a fluid, fast-moving factory; it is what makes fast change
legible.

## Rubric

Scored 2026-09-30, first-party sources only, tool as shipped (rubric method:
[agent-substrate-rubric.md](agent-substrate-rubric.md)). Only artefacts with independently verifiable
code are scored — the `ai-that-works` episodes are cited above as sources, not scored here, for lack of
a verifiable shipped artefact; Flue has one (see above) but has not yet been rubric-scored here.

`subject: long-running`

| Tool | Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|---|
| triagebot-action (Cloudflare's Astro triage GitHub Action) | no data — no multi-agent/multi-user concurrency documented [[cf-astro]][cf-astro] | yes — runs on GitHub Actions runners, forked and run by other teams' own infra [[cf-astro]][cf-astro] | partial — deterministic label-driven state machine, but no pinned model/version stated [[cf-astro]][cf-astro] | yes — label-driven config, already adopted and forked outside Cloudflare [[cf-astro]][cf-astro] | partial — git-backed Action; release/tag versioning not independently confirmed [[triagebot-repo]][triagebot-repo] | yes — findings posted to the source issue before any PR opens, forming an audit trail [[cf-astro]][cf-astro] |

## Sources

| Source | Content |
|---|---|
| [Wikipedia: Software factory][wp-sf] | Historical lineages (a): Japanese industrial movement + Microsoft's 2004 methodology |
| DOI `10.1007/978-1-4302-0181-6_4` (Crossref metadata) | "Software Factory Schema: Architecture", *Practical Software Factories in .NET* (Apress, 2006) — chapter itself paywalled |
| [Lockheed Martin Software Factory][lockheed] | DevSecOps vendor framing (b), self-reported |
| [VMware: What's a software factory?][vmware] | DevSecOps vendor framing (b); JS-rendered SPA, meta description only |
| [CircleCI: Software factory][circleci] | Agentic definition + concrete CI practices, published 2026-09-18 |
| [Augment Code: What is a software factory][augment] | Five-stage agentic pipeline with human gates |
| [freeCodeCamp: Claude Code software factory][fcc] | Concrete CC tooling: CLAUDE.md, skills, subagents, hooks |
| [ai-that-works ep. #63, "Software Factory for Agent Tools"][aiw-1] | Self-improving nightly issue/PR loop |
| [ai-that-works ep. #71, "Software Factory Design Patterns"][aiw-2] | Four-layer architecture (compute/dev-env/harness/orchestration) |
| [ai-that-works ep. #72, "Code Mode for Extensible Software"][aiw-3] | Agents writing code against APIs instead of tool calls |
| [ai-that-works ep. #73, "Hands-On with Real Builders"][aiw-4] | Practitioner interviews, self-reported metrics |
| `gh api repos/ai-that-works/ai-that-works`, 2026-09-30 | Confirms `license: null` for the ai-that-works repo |
| [wsff.md, HumanLayer][wsff] | "Why Software Factories Fail" — dissent on lights-off automation |
| [Stripe: Minions][minions] · [Part 2][minions2] | Unattended one-shot coding agents; >1,000 merged PRs/week (Part 1), >1,300 (Part 2, 2026-02-19), human-reviewed; vendor claim |
| [Uber: efficient software factory][uber-sf] | Vendor claims, 2026-08-27: cost per session -52% from June peak, spend stable since April, uReview on all PRs |
| [AIDev, arXiv 2602.09185][aidev] · [code review agents, 2604.03196][cra-study] | Agent-PR dataset (932,791 PRs); review-agent merge rates (45.20% vs 68.37%) |
| [Post-merge fate, 2607.09902][postmerge] · [Microsoft CLI rollout, 2607.01418][ms-cli] | Corrective-maintenance gap; ~24% more merged PRs (proxy) |
| [FlowAgent, 2610.07289][flowagent] · [SWE-CC, 2610.06193][swecc] · [FeatureArc, 2610.37434][featurearc] | Abstention-gated repair funnel; 43.1% policy violations by correct patches; 62.7% to 28.5% staged success |
| [Ramp: Introducing Inspect][inspect] | Collaborative coding agent; 74% of merged PRs (self-reported, 2026-10-27) |
| [WorkOS: Project Horizon][horizon] | "Internal code factory"; human approval before merge (2026-05-06) |
| [OpenAI: Symphony][symphony] · [`openai/symphony`][symphony-repo] | Board-driven agent orchestrator; +500% landed PRs on some teams (self-reported) |
| [Delinea: Software Factory][delinea] · [acquisition][delinea-news] · [`strongdm/attractor`][attractor] | Validation instead of code review; StrongDM acquired by Delinea (announced 2026-03-05) |
| [`vercel-labs/eve-software-factory-template`][eve] · [`open-inspect/background-agents`][open-inspect] | Factory template; open-source background-agent system |
| `gh api repos/humanlayer/advanced-context-engineering-for-coding-agents/commits?path=wsff.md`, 2026-09-30 | First commit 2026-07-22 (publish date); `contents/LICENSE` 404 (no license) |
| [Cloudflare: Astro issue triage][cf-astro] | Concrete production case; Flue and triagebot-action, published 2026-08-04 |
| [Anthropic: Redesigning source control][anthropic-scion] | Vendor-reported internal case: Scion/Antique, 2,500→30,000 merges/day, published 2026-10-13 |
| `gh api repos/withastro/triagebot-action`, 2026-09-30 | `license: null`, 220 stars, pushed 2026-08-28 |
| [flueframework.com][flue] | Vendor claim; site links a public GitHub repo |
| [github.com/withastro/flue][flue-repo] | Apache-2.0, ~8,400 stars (`gh api`, 2026-09-30); not yet rubric-scored here |
| [agent-substrate-rubric.md](agent-substrate-rubric.md) | Rubric method used above |

Cross-refs: [agentic-sdlc-patterns.md](agentic-sdlc-patterns.md) (the "no review agent" gap this
convergence bears on), [mas-design-principles.md](mas-design-principles.md) (12-Factor Agents /
HumanLayer's separate approval-gate SDK),
[CC-memory-system-analysis.md § Context Engineering Workflow (ACE-FCA)](../cc-native/context-memory/CC-memory-system-analysis.md#context-engineering-workflow-ace-fca)
(HumanLayer/Dex's other, unrelated ACE-FCA post),
[CC-agentic-harness-patterns-analysis.md](../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md)
(HumanLayer's approval-gate SDK in harness terms),
[CC-community-tooling-landscape.md § human-review](../cc-community/CC-community-tooling-landscape.md#human-review-petergyang)
(a concrete tool for the spec-review gate: comments on the artifact go straight back to the agent).

[wp-sf]: https://en.wikipedia.org/wiki/Software_factory
[lockheed]: https://www.lockheedmartin.com/en-us/capabilities/digital-transformation/software-factory.html
[vmware]: https://www.vmware.com/topics/software-factory
[circleci]: https://circleci.com/blog/software-factory/
[augment]: https://www.augmentcode.com/guides/what-is-a-software-factory
[fcc]: https://www.freecodecamp.org/news/how-to-build-software-factory-with-claude-code
[aiw-1]: https://github.com/ai-that-works/ai-that-works/tree/main/2026-06-23-software-factory-for-agent-tools
[aiw-2]: https://github.com/ai-that-works/ai-that-works/tree/main/2026-08-25-software-factory-design-patterns
[aiw-3]: https://github.com/ai-that-works/ai-that-works/tree/main/2026-09-01-code-mode-extensible-software
[aiw-4]: https://github.com/ai-that-works/ai-that-works/tree/main/2026-09-08-hands-on-software-factories
[wsff]: https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/wsff.md
[cf-astro]: https://blog.cloudflare.com/astro-issue-triage/
[triagebot-repo]: https://github.com/withastro/triagebot-action
[flue]: https://flueframework.com/
[flue-repo]: https://github.com/withastro/flue
[anthropic-scion]: https://www.anthropic.com/engineering/redesigning-source-control
[hlyr-ace-xref]: ../cc-native/context-memory/CC-memory-system-analysis.md#context-engineering-workflow-ace-fca
[disciplines-graph]: agentic-engineering-disciplines-landscape.md
[minions]: https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents
[inspect]: https://ramp.com/blog/introducing-inspect
[open-inspect]: https://github.com/open-inspect/background-agents
[horizon]: https://workos.com/blog/project-horizon
[symphony]: https://openai.com/index/open-source-codex-orchestration-symphony/
[symphony-repo]: https://github.com/openai/symphony
[delinea]: https://delinea.com/blog/the-delinea-software-factory-building-software-with-ai
[delinea-news]: https://delinea.com/news/delinea-acquires-strongdm-to-secure-ai-with-continuous-authorization
[attractor]: https://github.com/strongdm/attractor
[eve]: https://github.com/vercel-labs/eve-software-factory-template
[minions2]: https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2
[uber-sf]: https://www.uber.com/us/en/blog/efficient-software-factory/
[aidev]: https://arxiv.org/abs/2602.09185
[cra-study]: https://arxiv.org/abs/2604.03196
[postmerge]: https://arxiv.org/abs/2607.09902
[ms-cli]: https://arxiv.org/abs/2607.01418
[flowagent]: https://arxiv.org/abs/2610.07289
[swecc]: https://arxiv.org/abs/2610.06193
[featurearc]: https://arxiv.org/abs/2610.37434
