---
title: "Google agents-cli — Skill Layer for Building ADK Agents"
source: https://github.com/google/agents-cli
purpose: Analysis of Google's agents-cli, a CLI plus skill pack that turns a coding agent (Claude Code, Antigravity, Codex) into an expert at scaffolding, evaluating and deploying ADK agents.
platform_scope: [claude-code, antigravity, codex]
created: 2026-07-08
updated: 2026-11-26
validated_links_on: 2026-11-26
status: assess
---

**Details:**. Also runs on or integrates with: `google-adk`.

## What It Is

[agents-cli][repo] (PyPI `google-agents-cli`; Apache-2.0; ~6.4k stars, latest release `v1.16.0` published 2026-11-24 (checked 2026-11-26); `v1.0.0` was published 2026-07-01,
repo created 2026-04-08) is, in its own README's words, *"a tool **for** coding agents, not a coding
agent itself."* It is a CLI plus a bundled skill-pack that turns an existing coding agent — **Claude
Code**, Antigravity CLI, Codex, or any other — into an expert at scaffolding, evaluating, deploying,
and publishing agents built on Google's **Agent Development Kit (ADK)**, targeting the **Gemini
platform** (the README's current wording; earlier "Gemini Enterprise Agent Platform") / Google Cloud. It also runs standalone from a terminal.

**Maturity caveat (historical):** at the 2026-07-08 snapshot the README flagged it as **Pre-GA / Preview** ("subject
to the 'Pre-GA Offerings Terms'… available 'as is'"). The README checked 2026-11-26 carries no such wording, only a Terms of Service note pointing to the Google Cloud Service Terms; current status is unverified, so do not read the 1.x version string as a GA guarantee.

It is distinct from everything already in the corpus: not a coding agent (unlike
[gemini-cli-analysis.md](../coding-agents/gemini-cli-analysis.md), which is **Hold**), not a host IDE (unlike
[antigravity-analysis.md](../coding-agents/antigravity-analysis.md), a *named host* for agents-cli), and a level up
from the one-line **Google ADK** entry in
[agent-frameworks-infrastructure-landscape.md](agent-frameworks-infrastructure-landscape.md). ADK is
the agent *framework*; agents-cli is the lifecycle tooling around it.

## How It Works

Two install/use modes:

- **With a coding agent** (`npx skills add google/agents-cli`, skills only): prompt the host agent,
  e.g. *"Use agents-cli to build a caveman-style agent…"* — the 7 bundled skills
  (`…-workflow`, `-adk-code`, `-scaffold`, `-eval`, `-deploy`, `-publish`, `-observability`) drive it.
- **Standalone** (`uvx google-agents-cli setup`, full CLI): `agents-cli create <name> --prototype`,
  `install`, `playground`.

Core commands span the ADK-agent lifecycle: `scaffold` (+ `enhance`/`upgrade`), `run`,
`eval` (`generate`/`grade`/`dataset synthesize`/`compare`/`analyze`/`optimize`), `deploy`,
`publish gemini`, `lint`, `infra` (`single-project`/`cicd`; `datastore` and `data-ingestion` are not in the README checked 2026-11-26 and are unverified). Prereqs:
Python 3.11+, `uv`, Node.js; Google Cloud creds or an AI Studio API key (local `create`/`run`/`eval`
work without GCP; only deploy needs the Cloud SDK/Terraform).

## Adoption Decision

**Assess.** Research interest for this corpus is twofold: (1) it's a concrete instance of the
**"skill layer for coding agents"** pattern — a vendor shipping *skills that ride inside Claude Code
et al.* to specialize them for a target platform, rather than building yet another agent; and (2) it
names **Claude Code as a first-class host**, a data point on cross-vendor skill portability. Not
something to adopt (it's Google-Cloud/ADK-specific and was Pre-GA at the 2026-07 snapshot), but worth tracking as the pattern of
"agent-building tooling delivered as portable skills" matures. Contrast with the OpenAI Codex→CC
plugin ([../cc-community/CC-codex-plugin-cc-analysis.md](../../cc-community/CC-codex-plugin-cc-analysis.md)),
which delegates *between* agents; agents-cli instead *upskills* the host agent for ADK work.

Cross-ref: [agent-frameworks-infrastructure-landscape.md](agent-frameworks-infrastructure-landscape.md) (Google ADK) ·
[gemini-cli-analysis.md](../coding-agents/gemini-cli-analysis.md) · [antigravity-analysis.md](../coding-agents/antigravity-analysis.md)

## Sources

| Source | Content |
|---|---|
| [google/agents-cli][repo] | Repo: README, skills, commands, releases (Apache-2.0, v1.16.0, 2026-11-24) |
| [agents-cli getting started][getstarted] | Install + usage modes |
| [agents-cli docs][docs] | Scope: "CLI and skills for building agents on Gemini Enterprise Agent Platform" (the README now says "Gemini platform") |

[repo]: https://github.com/google/agents-cli
[getstarted]: https://google.github.io/agents-cli/guide/getting-started/
[docs]: https://google.github.io/agents-cli/
