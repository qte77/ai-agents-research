---
title: Software Factory Landscape
purpose: Disambiguates three unrelated meanings of "software factory" — historical, DevSecOps-vendor, and agentic-AI — and rubric-scores the agentic implementations with concrete artefacts.
created: 2026-09-30
updated: 2026-09-30
validated_links: 2026-09-30
---

**Status**: Assess

## What It Is

"Software factory" is reused across three unrelated eras and communities. Conflating them loses the
point of each. This page keeps them apart, then focuses on the third — the one active in this corpus's
agentic-SDLC research ([agentic-sdlc-patterns.md](agentic-sdlc-patterns.md)).

## (a) Historical: two industrial lineages

**Japanese industrial movement.** Hitachi coined the term in 1969 with its Hitachi Software Works,
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
upgrades, Cognitive Mission System Products and the SmartSat platform. Its own framing claims builds "in
minutes rather than days" — unverified, self-reported ([Lockheed Martin][lockheed]).

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

**Augment Code**'s guide defines an agentic software factory as "an AI-driven delivery system in which
agents write, test, and ship code inside a pipeline whose specifications and merge approvals stay under
human control," identifying verification as "the factory's binding constraint." Its five stages — Intake,
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
directories (`github.com/ai-that-works/ai-that-works`) contains only `README.md`, `email.md`, `meta.md`
and `transcript.txt` — no source files. The repo itself carries no LICENSE file
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
- **2026-09-01, "Code Mode for Extensible Software"**: agents write executable code against an API
  instead of many discrete tool calls (bash itself is cited as an existing "code mode"); HumanLayer's
  example edits a YJS CRDT via generated JavaScript sandboxed in QuickJS (not Node.js, filesystem/shell
  access denied) ([ep. #72][aiw-3]).
- **2026-09-08, "Hands-On with Real Builders"**: two named practitioners, both self-reported and without
  a linked repo — Tyler Brown (a HIPAA-compliant chat startup reporting ARR growth from roughly $270K to
  $400K over three months after restructuring around agents and a plan-do-verify loop) and Cole Murray
  (maintainer of "Open Inspect," described as an open-source background-agent system deployed at
  companies with up to 500 engineers; no repository link is given in the episode)
  ([ep. #73][aiw-4]).

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
durable, resumable TypeScript agents — no GitHub repository or license could be found for it as of
2026-09-30, so it is cited as a vendor claim only, not rubric-scored; and **triagebot-action**
(`github.com/withastro/triagebot-action`), a real, forkable GitHub Action other teams have adopted — no
LICENSE file (`license: null`, 220 stars, last pushed 2026-08-28), rubric-scored below
([Cloudflare][cf-astro]).

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
code are scored — the `ai-that-works` episodes and Flue are cited above as sources, not scored here, for
lack of a verifiable shipped artefact.

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
| `gh api repos/humanlayer/advanced-context-engineering-for-coding-agents/commits?path=wsff.md`, 2026-09-30 | First commit 2026-07-22 (publish date); `contents/LICENSE` 404 (no license) |
| [Cloudflare: Astro issue triage][cf-astro] | Concrete production case; Flue and triagebot-action, published 2026-08-04 |
| `gh api repos/withastro/triagebot-action`, 2026-09-30 | `license: null`, 220 stars, pushed 2026-08-28 |
| [flueframework.com][flue] | Vendor claim only — no GitHub repo or license found |
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
[hlyr-ace-xref]: ../cc-native/context-memory/CC-memory-system-analysis.md#context-engineering-workflow-ace-fca
