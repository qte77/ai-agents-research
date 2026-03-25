---
title: TODO - ai-agents-research
description: Research task backlog, active work, and deferred items for ai-agents-research
category: implementation
created: 2026-03-22
updated: 2026-03-22
---

# TODO: ai-agents-research

## Done

**CC-native deep dives:**

- [x] Agents and skills system (`docs/cc-native/agents-skills/`)
  - Recursive spawning patterns, agent teams orchestration, skills adoption, ralph enhancement
- [x] Sandboxing and CI execution (`docs/cc-native/ci-execution/`)
  - Sandboxing analysis, Codespaces friction, permissions bypass, GitHub Actions, cloud sessions, sandbox platforms
- [x] Context and memory (`docs/cc-native/context-memory/`)
  - Extended context, memory system, llms.txt
- [x] Plugins and ecosystem (`docs/cc-native/plugins-ecosystem/`)
  - Official plugins, community plugins, cowork API, connectors, plugin packaging, web scraping
- [x] Configuration features
  - Fast mode, hooks system, model/provider config, bash mode, loop/cron
- [x] CC changelog feature scan (`docs/cc-native/CC-changelog-feature-scan.md`)

**Non-CC agent analyses:**

- [x] JetBrains AI Assistant / Air (`docs/non-cc/air/`)
- [x] agent-era/devteam (`docs/non-cc/devteam/`)

**Automated monitors:**

- [x] CC status monitor (outage archive)
- [x] CC changelog monitor (triage PRs)
- [x] Community monitor (triage PRs)

**Foundational docs:**

- [x] UserStory.md
- [x] architecture.md
- [x] TODO.md (this file)

---

## Next

- [ ] Update feature comparison matrix for latest agent releases (post-CC 1.x)
- [ ] Document CC 1.x session artifact schema changes (new fields in `raw_stream.jsonl`)
- [ ] Add Gemini CLI analysis to `docs/non-cc/` (invocation methods, tool schema, session artifacts)

---

## Backlog

- [ ] Codebuff analysis (`docs/non-cc/`)
- [ ] opencode analysis (`docs/non-cc/`)
- [ ] aider analysis (`docs/non-cc/`)
- [ ] CC Agent SDK deep dive — tool registration, permissions model, MCP integration (`docs/cc-native/agents-skills/`)
- [ ] Cross-agent orchestration comparison — CC teams vs. CrewAI vs. LangGraph patterns (`docs/cc-native/comparisons/`)
- [ ] Kiro analysis (`docs/non-cc/`) — spec-driven dev, agent hooks, SDD alignment with RAPID+Ralph
- [ ] Antigravity analysis (`docs/non-cc/`) — multi-agent orchestration, built-in browser
- [ ] Cursor/Windsurf analysis (`docs/non-cc/`) — agentic IDE comparison

---

## Deferred

- [ ] Automated comparison matrix generation — requires stable agent APIs; defer until landscape settles
- [ ] CI validation for doc conventions (frontmatter linting, format checks) — low ROI for research repo
- [ ] Research-to-PRD traceability automation — manual cross-reference is sufficient at current volume

---

## Cross-Reference: Docs to Downstream Repos

| Doc / Directory | Feeds Into |
|---|---|
| `docs/cc-native/agents-skills/CC-recursive-spawning-patterns.md` | cc-recursive-team-mode (spawning implementation) |
| `docs/cc-native/session-analysis/` | cc-recursive-team-mode (artifact parser schema) |
| `docs/cc-native/comparisons/`, `docs/non-cc/` | coding-agent-eval (agent feature matrices) |
| `docs/cc-native/features/`, invocation method docs | coding-agent-eval (invocation harness design) |
| `docs/cc-native/meta/` quality methodology notes | multi-tasking-quality-benchmark (metric selection) |
