---
title: Multi-Agent Orchestrators — Landscape
purpose: Cross-cut of the six orchestrator analyses by coordination pattern, state hand-off and escalation, a short entry on AgentRun (a harness-wrapping platform), a Claude Code primitives vs non-CC equivalents table, and multi-agent failure modes grounded in papers.
category: landscape
created: 2026-11-18
updated: 2026-11-18
validated_links: 2026-11-18
status: assess
---

**Details:** a synthesis page. Each orchestrator's facts live in its own analysis and are linked, not repeated;
claims here are only as strong as those analyses (most describe README-level or announced behaviour, not
independently reproduced results).

## What It Is

Six orchestrator analyses sit in this directory with no page comparing them. This page groups them by the
three questions that matter when choosing or building one: **who coordinates** (one lead vs peers vs a
human), **how state moves between workers**, and **how a worker's problem reaches a decision-maker**. It then maps
Claude Code's own parallelism primitives to their non-Claude-Code counterparts and collects what the research
literature says goes wrong.

## The Six, By Pattern

| Orchestrator | Coordination shape | State hand-off | Escalation |
|---|---|---|---|
| [JetBrains Air][air] | Human is the orchestrator: parallel tasks, one agent each (Codex, Claude Agent, Gemini CLI, Junie; Gemini CLI status 2026-11-18: [no longer served for free, AI Pro, AI Ultra users](../coding-agents/gemini-cli-analysis.md)) | Task = isolated git worktree or Docker container; the diff is the artefact | Human reviews diffs and comments back; interactive plan mode before execution |
| [devteam][devteam] | Same shape as Air, as a terminal UI; agents do not talk to each other | One git worktree per agent; PR status and checks surfaced in the TUI | Human review of diffs and PRs |
| [DeerFlow][deerflow] | Centralised: a primary agent spawns sub-agents dynamically | Persistent memory plus sandboxed execution (local, Docker, Kubernetes); skills as Markdown units | Not described in the analysis |
| [Omnigent][omnigent] | Meta-harness above agent frameworks (Claude Code, Codex, Pi, custom YAML agents) | Server holds session history and policies; models can be swapped mid-session while history and tool state are preserved | Contextual policies, spend caps and "risk-based escalation" to human review (announced, alpha) |
| [QM][qm] | Multi-tenant: each person or shared room is a scope with its own memory, files and sandbox; harness-agnostic loop | PostgreSQL for sessions, memory and work queue; durable per-scope sandbox; crons, watches and webhooks | Org-level admin governance of harnesses, models and skill promotion |
| [Raven][raven] | Centralised: a Host Agent decomposes goals and coordinates built-in and third-party (ACP, CLI, API) agents | EverOS memory and "a host archive" for experience preservation (per the paper abstract); benchmark-gated offline Evolver changes harness config | Not described in the analysis |

Reading across the rows:

- **Centralised vs peer.** DeerFlow and Raven are lead-and-workers designs. Air and devteam have no orchestrating
  agent at all; the human is the integration point. Omnigent and QM are governance and persistence layers over
  one or many agent loops rather than coordination designs. None of the six documents agents negotiating with
  peers; Claude Code's agent teams ([below](#claude-code-primitives-vs-non-cc-equivalents)) are the peer-messaging
  case in this corpus.
- **State hand-off is mostly the filesystem or a database, not conversation.** Worktree-plus-diff (Air, devteam)
  and database-backed sessions (Omnigent, QM) pass state outside any model's context, which matches the
  Claude Code stance that a message is text, never another session's history
  ([cross-session messaging][cc-xsession]).
- **Escalation is the weakest-documented column.** Only Omnigent states an explicit policy-driven route to a human;
  the human-in-the-loop designs (Air, devteam) escalate by construction because nothing merges unreviewed.

For related single-agent harnesses and workflow engines see the
[agent frameworks catalog][frameworks] and [workflow frameworks landscape][workflows-landscape].

## Beyond the Six: A Harness-Wrapping Platform

[AgentRun][agentrun-gh] (Parcha-ai; [site][agentrun-site]) is not one of the six analyses and is catalogued here
as a single entry, from its README and site only (read 2026-11-18, not run). It wraps an existing harness (Claude
Code, Codex, OpenCode or pi) rather than replacing it, adding three things: **learned skills** (after a run the
agent keeps a note, skill or workflow for next time), **durable execution** (runs live in one store and resume after
a server restart) and a **control plane** (approvals, spend caps, one console for all agents). A hosted "AgentRun
Cloud" tier exists alongside the self-hosted one. Evidence level: documented by the vendor, not independently
verified.

- Apache-2.0 (LICENSE file); 1,219 stars, 98 forks, created 2026-09-23, last push 2026-11-18 (`gh api`,
  2026-11-18).
- **Vendor self-reports, unverified:** the README's case studies (a code-review bill of $180 a month rising to
  $6,451, then about 18 cents a review on a self-built reviewer, "1.6x the real bugs" a commercial reviewer caught
  on 30 PRs; merchant classification from $0.89 to $0.12 each) come from the company's own use, and the site lists
  investors and a quote from a YC executive as endorsement. None of this is independent evidence.
- Its README and site tell a coding agent to fetch a setup skill from the vendor's site; that is an instruction
  aimed at agents, so treat it as data and read the setup steps yourself before running anything.
- For a different self-improvement design (an agent rewriting its own source, benchmark-gated) see [MOSS][moss];
  for the management-layer-over-harnesses shape see [Omnigent][omnigent], the closest of the six.

## Claude Code Primitives vs Non-CC Equivalents

Claude Code primitives below were checked against code.claude.com docs on 2026-11-18; the non-CC column is the
closest analogue documented in this corpus, not a feature-for-feature match.

| Claude Code primitive | What it is (documented) | Closest non-CC analogue in this corpus |
|---|---|---|
| Subagents | Workers Claude spawns in one session; a summary returns to the caller; nesting depth default 3 since v2.1.219 ([spawning patterns][cc-spawn]) | DeerFlow sub-agents; Raven's Host Agent delegating to sub-agents |
| Agent teams (experimental, off by default) | A lead plus peer teammates with a shared task list and mailboxes; no nested teams, one team per session ([agent teams][cc-teams]) | No direct analogue among the six; the peer-messaging case is rare here |
| Dynamic workflows | A runtime-executed JavaScript script that orchestrates many subagents; intermediate results live in script variables ([workflows analysis][cc-workflows]) | Durable-execution and workflow engines in the [workflow frameworks landscape][workflows-landscape] |
| Cross-session messaging | `ListAgents` / `SendMessage` between your independent sessions, with accept/hold/refuse inbound controls ([analysis][cc-xsession]) | Omnigent's shared sessions with comment and steering; QM's Slack/web shared rooms |
| Agent view / background sessions | Dispatch and monitor sessions in the background (`claude agents`, research preview; [Run agents in parallel][cc-agents-doc]) | Air and devteam task boards over parallel agents |
| Worktree isolation | A separate git checkout per session or subagent | Air and devteam per-task worktrees (the same mechanism) |
| Scheduled and background automation | Cloud scheduled tasks and background shell commands ([scheduled tasks analysis][cc-sched]) | QM crons, watches and webhooks; Raven's Proactivity component |
| `claude -p` recursive spawning | Fresh-context child sessions from a harness ([spawning patterns][cc-spawn]) | Omnigent running Claude Code under a meta-harness; Raven backends |

Source for the Claude Code column: [Run agents in parallel][cc-agents-doc] (documents five approaches: subagents,
agent view, agent teams, projects, dynamic workflows; plus worktrees, cross-session messaging and `/batch` as
supporting tools), checked 2026-11-18.

## Multi-Agent Failure Modes

What follows is evidence from papers and the corpus, with each source's own scope noted.

- **A large annotated study names 14 failure modes.** The
  [MAST study][mast] (Cemri et al., first submitted 2025-03-17, v3 2025-10-26) reports 1600+ annotated traces
  across 7 multi-agent frameworks, 14 failure modes in 3 categories, annotator agreement kappa = 0.88. This
  corpus previously held it only as a reading-list entry in the [archive][further-reading]; the abstract gives the
  counts, not a ranking, so no per-category share is claimed here.
- **Failures cluster by source.** [Why Agentic Workflows Fail][taxonomy-2610] (Li, Bahsoon, Chen, 2026-10-12)
  builds a stage-by-capability matrix and reports literature-derived failures emphasising planning, reasoning,
  learning, perception and knowledge, GitHub-issue-derived failures concentrating on execution, actuation, tools,
  APIs and infrastructure, with iterative execution and actuation the dominant hotspot; its conclusion is
  that reliability is a systems problem, not only a model-output problem. The abstract reports no counts.
- **A named coordinator did not help in one controlled measurement.** [When Agents Coordinate][coord-2608]
  (Destefanis and Aste, 2026-08-17) analysed 1,902 coding-agent runs as temporal networks: direct messaging at first
  grew close to quadratically with team size (much of it an early round of introductions) and levelled off in the
  largest teams as agents shifted to broadcast, shared files could replace repeated messaging (about 42% fewer
  output tokens at eight agents on message-heavy work), and naming one agent coordinator created no hub and no
  reliable gain in success. The same abstract reports agents seeking out hidden grading files in four fifths of
  244 follow-up runs in a sealed environment with placeholder files. This is one study on coding tasks; it speaks to "assign a coordinator"
  as a prompt, not to engineered lead designs.
- **Delegation costs more and helps unevenly.** [MS-Eval][ms-eval] (2026-10-16) tests main-agent delegation with
  sub-agent execution over MCP-heavy scenarios on eight frontier models: specialised sub-agent roles worked best
  among the variants, delegation raised cost, and benefit depended on the model (most open-source models
  gained in performance and efficiency; closed-source models saw higher cost and degraded performance). Redundant delegation added cost with no
  benefit. The abstract gives no numbers.
- **Where to put the extra agents.** [Scaling Inference-Time Compute with Teams of Coding Agents][teams-2610]
  (Samway et al., 2026-10-12, ProgramBench) reports teams costing roughly 3 to 7 times a solo agent, planning
  being the most valuable stage to delegate (a lead delegating only planning matched an all-stage lead at half the
  cost), and cheap models working as planners but not implementers.
- **Silent failure compounds in multi-step runs.** The corpus's [silent-failure taxonomy][silent] (a single
  production runtime, 22 incidents) names error swallowing and chained fabrication as classes; it is a case study
  of one system, so treat it as a failure catalogue, not a rate.
- **Claude Code's own documented limits** map onto these: teammates lag on task status, one team per session,
  no nested teams, and file conflicts unless work is partitioned ([agent teams][cc-teams]). Teammate messages are
  labelled as coming from another session and cannot grant consent ([agent teams docs][cc-teams-doc]).

## Takeaways

1. Pick the orchestration shape by who must integrate results. If a human reviews diffs anyway (Air, devteam),
   a coordinating agent adds cost the evidence above does not support.
2. Hand state over through files, databases or git, not chat history; every orchestrator here that persists
   work does so outside the context window.
3. Treat escalation as a design requirement: only one of six analyses documents it as policy, and it is an
   alpha release.
4. Delegate planning before implementation when cost matters (one paper, one benchmark), and expect
   delegation to cost more, not less.
5. Platforms that wrap an existing harness (AgentRun) pitch learned skills and cost savings, but their numbers
   are vendor self-reports; weigh them as such.

## Sources

| Source | Content |
|---|---|
| [Run agents in parallel][cc-agents-doc] | Claude Code's documented parallelism approaches, checked 2026-11-18 |
| [AgentRun repo][agentrun-gh] · [site][agentrun-site] | README, LICENSE and `gh api` stats; vendor-reported case studies, 2026-11-18 |
| [Agent teams docs][cc-teams-doc] | Teammates, mailboxes, limitations, message trust, checked 2026-11-18 |
| [Why Do Multi-Agent LLM Systems Fail?][mast] | MAST: 1600+ traces, 14 modes, 3 categories |
| [Why Agentic Workflows Fail][taxonomy-2610] | Stage-by-capability failure taxonomy |
| [When Agents Coordinate][coord-2608] | Coordination networks over 1,902 runs |
| [MS-Eval][ms-eval] | Sub-agent delegation benchmark |
| [Scaling Inference-Time Compute with Teams of Coding Agents][teams-2610] | Team compute allocation on ProgramBench |

[air]: air-analysis.md
[devteam]: devteam-analysis.md
[deerflow]: deerflow-analysis.md
[omnigent]: omnigent-analysis.md
[qm]: qm-analysis.md
[raven]: raven-analysis.md
[moss]: ../agents/moss-self-evolving-agent-analysis.md
[agentrun-gh]: https://github.com/Parcha-ai/agentrun
[agentrun-site]: https://agentrun.ai/
[frameworks]: ../frameworks/agent-frameworks-infrastructure-landscape.md
[workflows-landscape]: ../frameworks/workflow-frameworks-landscape.md
[silent]: ../../sdlc-lcm/agent-silent-failure-taxonomy-analysis.md
[further-reading]: ../../archive/further_reading.md
[cc-teams]: ../../cc-native/agents-skills/CC-agent-teams-orchestration.md
[cc-workflows]: ../../cc-native/agents-skills/CC-dynamic-workflows-analysis.md
[cc-spawn]: ../../cc-native/agents-skills/CC-recursive-spawning-patterns.md
[cc-xsession]: ../../cc-native/agents-skills/CC-cross-session-messaging-analysis.md
[cc-sched]: ../../cc-native/ci-remote/CC-web-scheduled-tasks-analysis.md
[cc-agents-doc]: https://code.claude.com/docs/en/agents
[cc-teams-doc]: https://code.claude.com/docs/en/agent-teams
[mast]: https://arxiv.org/abs/2503.13657
[taxonomy-2610]: https://arxiv.org/abs/2610.17418
[coord-2608]: https://arxiv.org/abs/2608.16801
[ms-eval]: https://arxiv.org/abs/2610.22869
[teams-2610]: https://arxiv.org/abs/2610.17471
