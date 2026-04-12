---
title: Multi-Agent Onboarding Outlook
purpose: How multiple coding agents (CC, Kiro, Antigravity, Cursor, etc.) integrate with SDLC/LCM lifecycle management.
created: 2026-03-24
sources:
  - https://ai.google.dev/gemini-api/docs/coding-agents
  - https://dev.to/madeburo/ai-context-management-across-claude-cursor-kiro-gemini-and-custom-agents-2n1f
  - https://lushbinary.com/blog/ai-coding-agents-comparison-cursor-windsurf-claude-copilot-kiro-2026/
  - https://particula.tech/blog/agents-md-ai-coding-agent-configuration
---

## Multi-Agent Onboarding Outlook

How the SDLC/LCM framework supports onboarding any coding agent — not just
Claude Code — onto projects in the qte77 ecosystem.

## The Context Fragmentation Problem

Each coding agent reads a different config file for project context:

| Agent | Config File | Format |
|-------|------------|--------|
| Claude Code | `CLAUDE.md` | Markdown |
| Cursor | `.cursorrules` | Markdown |
| Windsurf | `.windsurf/rules/*.md` | Markdown |
| Kiro | `.kiro/steering/*.md` | Markdown |
| Gemini CLI / Antigravity | `GEMINI.md` | Markdown |
| GitHub Copilot | `.github/copilot-instructions.md` | Markdown |
| OpenAI Codex | `AGENTS.md` | Markdown |
| General | `llms.txt` | Plain text |

All describe the same thing (stack, conventions, rules) in different locations.
They go out of sync when one is updated and the rest forgotten.

## AGENTS.md Convergence

**AGENTS.md** (originated by OpenAI, Aug 2025) is becoming the universal standard:

- Adopted by Linux Foundation's **Agentic AI Foundation** (AAIF) alongside MCP and Goose (MCP co-creator — see [goose-analysis](../non-cc/goose-analysis.md))
- 60,000+ repos, supported by Codex, Cursor, Windsurf, Zed, Jules, Gemini CLI
- **Exception**: Claude Code uses CLAUDE.md (open issue with 3,000+ upvotes)
- MCP Dev Summit (April 2026, NYC) may bring further governance updates

**Implication for qte77**: current `AGENTS.md` + `CLAUDE.md` dual approach covers
both CC-specific and standard agent contexts. When CC adopts AGENTS.md (if ever),
consolidate.

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
| **Cursor** | Rules file includes phase-aware constraints | `.cursorrules` |
| **Gemini CLI** | GEMINI.md references phase metadata | `GEMINI.md` |
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
| **A2A** | Google | Agent-to-agent collaboration | Multi-agent orchestration (future) |
| **ACP** | IBM | Enterprise governance | Compliance/audit (Phase 3) |
| **AG-UI** | Community | Human-in-the-loop UX | RAPID cockpit (future) |

## Summary

The sdlc-lcm-manager design is already agent-agnostic by using file artifacts
as the interface. Multi-agent onboarding requires:

1. **Per-agent config stubs** — one-time setup of phase constraints in each agent's config format
2. **Shared artifact contracts** — `[tool.lcm]` in pyproject.toml, `.lcm/status.json`
3. **No code coupling** — agents read files, don't import libraries
