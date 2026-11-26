---
title: Multi-Agent Onboarding Outlook
purpose: How multiple coding agents (CC, Kiro, Antigravity, Cursor, etc.) integrate with SDLC/LCM lifecycle management.
created: 2026-03-24
updated: 2026-11-26
validated_links_on: 2026-11-21
status: assess
---

## Multi-Agent Onboarding Outlook

> **Legacy note:** RAPID is legacy — the `RAPID-spec-forge` repo was archived 2026-04-26 and superseded by [qte77/qte77](https://github.com/qte77/qte77). RAPID references below are retained for historical SDLC/LCM-pattern context.

How the SDLC/LCM framework supports onboarding any coding agent — not just
Claude Code — onto projects in the qte77 ecosystem.

## The Context Fragmentation Problem

Each coding agent reads a different config file for project context:

| Agent | Config File | Format |
|-------|------------|--------|
| Claude Code | `CLAUDE.md` | Markdown |
| Cursor | `.cursor/rules/*.mdc`, `AGENTS.md` (the current rules page does not mention `.cursorrules`) | Markdown |
| Windsurf | `.devin/rules/*.md` (`.windsurf/rules/*.md` and `.windsurfrules` are legacy but still imported); also reads `AGENTS.md` | Markdown |
| Kiro | `.kiro/steering/*.md`; also reads `AGENTS.md` ([steering docs](https://kiro.dev/docs/steering/), checked 2026-11-26) | Markdown |
| Gemini CLI / Antigravity | `GEMINI.md` | Markdown |
| GitHub Copilot | `.github/copilot-instructions.md`; also reads `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` (github.com; the CLI part is unverified: the repository-instructions page does not mention it; checked 2026-10-24 — see [github-copilot-cloud-agent-analysis.md](../non-cc/agents/github-copilot-cloud-agent-analysis.md#repository-custom-instructions)) | Markdown |
| OpenAI Codex | `AGENTS.md` | Markdown |
| General | `llms.txt` | Plain text |

All describe the same thing (stack, conventions, rules) in different locations.
They go out of sync when one is updated and the rest forgotten.

## AGENTS.md Convergence

**AGENTS.md** (originated by OpenAI; "Aug 2025" unverified) is becoming the universal standard:

- Adopted by Linux Foundation's **Agentic AI Foundation** (AAIF) alongside Model Context Protocol (MCP, contributed by Anthropic) and Goose (contributed by Block — see [goose-analysis](../non-cc/agents/goose-analysis.md))
- 60,000+ repos (agents.md: "over 60k open-source projects"), supported by Codex, Cursor, Windsurf, Zed, Jules, Gemini CLI and many others
- **Claude Code**: reads CLAUDE.md first; since v2.1.277 it falls back to AGENTS.md when no CLAUDE.md exists (default `/config` Project instructions mode `claude-md-or-agents-md`; [memory docs](https://code.claude.com/docs/en/memory#agents-md); long-running request [#6235](https://github.com/anthropics/claude-code/issues/6235), now closed, 5,197 thumbs-up, checked 2026-11-26)
- MCP Dev Summit North America was held 2026-04-02 to 04-03 in New York

**Implication for qte77**: current `AGENTS.md` + `CLAUDE.md` dual approach covers
both CC-specific and standard agent contexts. CC now reads AGENTS.md as a fallback (v2.1.277+), so the open choice is
whether to consolidate (a CLAUDE.md that imports `@AGENTS.md`, or AGENTS.md alone).

## Agent-Agnostic Artifact Design

The sdlc-lcm framework communicates via **file artifacts**, not code imports.
Any agent that reads files can participate:

```text
pyproject.toml [tool.lcm]     <- phase metadata (any agent reads TOML)
.lcm/status.json              <- machine-readable phase state (any agent reads JSON)
prd.json                      <- task tracking (Ralph convention, readable by any agent)
CHANGELOG.md                  <- release history (universal)
```

No agent-specific dependency. No Python imports required.

## Per-Agent Integration Path

| Agent | How It Consumes LCM | Config Location |
|-------|---------------------|-----------------|
| **Claude Code** | CC plugin skill reads `[tool.lcm]` + `.lcm/status.json` | `.claude/skills/` |
| **Kiro** | Steering doc references phase constraints | `.kiro/steering/lifecycle.md` |
| **Cursor** | Rules file includes phase-aware constraints | `.cursor/rules/*.mdc` |
| **Gemini CLI** (status 2026-11-18: [replaced by Antigravity CLI](../non-cc/coding-agents/gemini-cli-analysis.md) for non-enterprise users; Antigravity CLI's migration docs say `GEMINI.md` and `AGENTS.md` keep working) | GEMINI.md references phase metadata | `GEMINI.md` |
| **Codex/AGENTS.md** | AGENTS.md includes phase section | `AGENTS.md` |

Each agent gets the same information via its own config convention. The source
of truth is always `pyproject.toml [tool.lcm]` and `.lcm/status.json`.

## Kiro / SDD Alignment

Kiro's spec-driven development (requirements → design → tasks → code) maps
directly to the existing RAPID + Ralph pipeline:

| Kiro Concept | qte77 Equivalent |
|-------------|-----------------|
| Spec generation | RAPID BRD → PRD → FRD |
| Task breakdown | Ralph prd.json |
| Agent hooks (event-driven) | Ralph pre/post-loop gates |
| Human-editable specs | PRD.md, UserStory.md |

This alignment means the SDLC/LCM framework is already compatible with SDD-style
agents. No architectural changes needed to support Kiro-like workflows.

## Key Protocols

| Protocol | Owner | Purpose | Relevance |
|----------|-------|---------|-----------|
| **MCP** | Anthropic / AAIF | Tool access standardization | CC plugins, Gemini CLI tools |
| **A2A** (Agent-to-Agent Protocol) | Linux Foundation (originated by Google) | Agent-to-agent collaboration | Multi-agent orchestration (future) |
| **ACP** | now part of A2A under the Linux Foundation (its site) | Enterprise governance | Compliance/audit (Phase 3) |
| **AG-UI** (Agent-User Interaction Protocol) | CopilotKit-originated (per its docs) | Human-in-the-loop UX | RAPID cockpit — *RAPID is legacy (archived 2026-04-26, superseded by [qte77/qte77](https://github.com/qte77/qte77))* |

The frontend / agent / tool **protocol triangle** (AG-UI · A2A · MCP) is mapped in detail in [ag-ui-protocol-landscape.md](../non-cc/protocols/ag-ui-protocol-landscape.md).

## Summary

The sdlc-lcm-manager design is already agent-agnostic by using file artifacts
as the interface. Multi-agent onboarding requires:

1. **Per-agent config stubs** — one-time setup of phase constraints in each agent's config format
2. **Shared artifact contracts** — `[tool.lcm]` in pyproject.toml, `.lcm/status.json`
3. **No code coupling** — agents read files, don't import libraries

## Sources

- [Gemini API: coding agents](https://aistudio.google.com/docs/coding-agents)
- [Kiro: steering](https://kiro.dev/docs/steering/)
- [AI context management across Claude, Cursor, Kiro, Gemini and custom agents (dev.to, secondary)](https://dev.to/madeburo/ai-context-management-across-claude-cursor-kiro-gemini-and-custom-agents-2n1f)
- [AGENTS.md: AI coding agent configuration (Particula, secondary)](https://particula.tech/blog/agents-md-ai-coding-agent-configuration)
