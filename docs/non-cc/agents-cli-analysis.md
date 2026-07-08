---
title: "Google agents-cli — Skill Layer for Building ADK Agents"
source: https://github.com/google/agents-cli
purpose: Analysis of Google's agents-cli — a CLI + skill-pack that turns a coding agent (Claude Code, Antigravity, Codex) into an expert at scaffolding, evaluating, and deploying ADK agents on the Gemini Enterprise Agent Platform.
category: analysis
platform_scope: [claude-code, antigravity, codex, google-adk]
created: 2026-07-08
updated: 2026-07-08
validated_links: 2026-07-08
---

**Status**: Assess

## What It Is

[agents-cli][repo] (PyPI `google-agents-cli`; Apache-2.0; ~4.9k stars; `v1.0.0` published 2026-07-01,
repo created 2026-04-08) is, in its own README's words, *"a tool **for** coding agents, not a coding
agent itself."* It is a CLI plus a bundled skill-pack that turns an existing coding agent — **Claude
Code**, Antigravity CLI, Codex, or any other — into an expert at scaffolding, evaluating, deploying,
and publishing agents built on Google's **Agent Development Kit (ADK)**, targeting the **Gemini
Enterprise Agent Platform** / Google Cloud. It also runs standalone from a terminal.

**Maturity caveat:** despite the `v1.0.0` tag, the README flags it as **Pre-GA / Preview** ("subject
to the 'Pre-GA Offerings Terms'… available 'as is'"). Treat the 1.0 as a version string, not a GA
guarantee.

It is distinct from everything already in the corpus: not a coding agent (unlike
[gemini-cli-analysis.md](gemini-cli-analysis.md), which is **Hold**), not a host IDE (unlike
[antigravity-analysis.md](antigravity-analysis.md), a *named host* for agents-cli), and a level up
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
`publish gemini-enterprise`, `infra` (`single-project`/`cicd`/`datastore`), `data-ingestion`. Prereqs:
Python 3.11+, `uv`, Node.js; Google Cloud creds or an AI Studio API key (local `create`/`run`/`eval`
work without GCP; only deploy needs the Cloud SDK/Terraform).

## Adoption Decision

**Assess.** Research interest for this corpus is twofold: (1) it's a concrete instance of the
**"skill layer for coding agents"** pattern — a vendor shipping *skills that ride inside Claude Code
et al.* to specialize them for a target platform, rather than building yet another agent; and (2) it
names **Claude Code as a first-class host**, a data point on cross-vendor skill portability. Not
something to adopt (it's Google-Cloud/ADK-specific and Pre-GA), but worth tracking as the pattern of
"agent-building tooling delivered as portable skills" matures. Contrast with the OpenAI Codex→CC
plugin ([../cc-community/CC-codex-plugin-cc-analysis.md](../cc-community/CC-codex-plugin-cc-analysis.md)),
which delegates *between* agents; agents-cli instead *upskills* the host agent for ADK work.

Cross-ref: [agent-frameworks-infrastructure-landscape.md](agent-frameworks-infrastructure-landscape.md) (Google ADK) ·
[gemini-cli-analysis.md](gemini-cli-analysis.md) · [antigravity-analysis.md](antigravity-analysis.md)

## Sources

| Source | Content |
|---|---|
| [google/agents-cli][repo] | Repo: README, skills, commands, releases (Apache-2.0, v1.0.0, 2026-07-01) |
| [agents-cli getting started][getstarted] | Install + usage modes |
| [agents-cli docs][docs] | Scope: "CLI and skills for building agents on Gemini Enterprise Agent Platform" |

[repo]: https://github.com/google/agents-cli
[getstarted]: https://google.github.io/agents-cli/guide/getting-started/
[docs]: https://google.github.io/agents-cli/
