---
title: Trae (ByteDance Agentic IDE)
source: https://www.trae.ai/
purpose: Evaluate Trae, ByteDance's VS Code-based agentic IDE, for adoption as a coding agent alternative to Cursor or GitHub Copilot.
created: 2026-06-16
updated: 2026-06-16
validated_links: 2026-06-16
---

**Status**: Assess

## What It Is

Trae ("The Real AI Engineer") is a proprietary AI-native IDE built and distributed by
ByteDance (Singapore entity: SPRING(SG)PTE.LTD), based on a fork of Code OSS (the open
source base of Visual Studio Code). It launched in January 2025 and reached
[general availability of its SOLO autonomous agent][trae-blog] in November 2025, followed
by Trae Work (a general-purpose AI work assistant) in June 2026. As of access date
2026-06-16, [pricing][trae-pricing] spans Free → Lite ($3/mo) → Pro ($10/mo) → Pro+
($30/mo) → Ultra ($100/mo), with token-based usage allocations per tier introduced
February 24, 2026.

Trae runs on macOS and Windows; a browser-based Cloud IDE is available. Linux support is
not yet released as of 2026-06-16.

## How It Works

Trae exposes two primary interaction modes inside the IDE:

**Builder Mode** — an autonomous agent that accepts a natural-language project
description, breaks it into implementation steps, and scaffolds a full project tree
(frontend, backend, config files) with a live preview before applying changes. It uses a
Context Understanding Engine (CUE) that builds semantic repository graphs and supports
dynamic file indexing up to approximately 5,000 files (third-party claim; not stated in
first-party docs accessed 2026-06-16). Multimodal input—screenshot or mockup to code—is
also documented in third-party reviews.

**SOLO Mode** — a redesigned developer environment (introduced GA November 2025) centered
on an AI panel and a unified tool panel. A "Flow" feature automatically switches the tool
panel context based on active AI work (e.g., PRD view while generating docs, Editor view
while generating code). SOLO is available on Pro plans and above. A standalone SOLO
desktop/web product entered free beta on March 31, 2026.

**Agent 2.0** (released June 17, 2025) introduced a reengineered architecture with
unified modes and long-term memory capabilities.

**MCP** — Trae supports the [Model Context Protocol][mcp-spec] for extensibility,
enabling integrations with databases (Supabase, Neon, PlanetScale), deployment platforms
(Vercel, Netlify, Railway), and self-hosted PaaS (Kamal, Coolify). Custom agents with
specific tools and logic are also configurable.

**Models** — Free-tier access to frontier models is a headline differentiator: Claude
3.7 Sonnet (200k context), GPT-4o, DeepSeek V3, and local models via Ollama are cited in
third-party reviews. Tier limits govern how many fast vs. slow requests are available
per month.

Trae has no documented headless or CLI mode; it is a GUI desktop/web IDE only.

## Adoption Decision

**Recommend Assess** — Trae is a capable, free-tier agentic IDE with genuine
differentiation (multi-model access, MCP extensibility, autonomous Builder/SOLO modes)
and rapid iteration velocity. However, two hard blockers exist for most professional
engineering contexts:

1. **Telemetry and data sovereignty** — Independent security research
   ([Unit 221B][unit221b], July 2025; [The Register][register], July 2025) documented
   ~500 network calls in 7 minutes, persistent ByteDance server connections every ~30
   seconds even when idle, and permanent device fingerprinting via `machineId`. ByteDance
   confirmed the VS Code telemetry toggle does not suppress all data collection. A "Privacy
   Mode" was later introduced but its scope is narrow (chat/code not used for model
   training); background telemetry to ByteDance domains is not fully opt-out-able.
   Personal data is retained for 5 years after account closure. No SOC 2 Type II or ISO
   certification is documented as of 2026-06-16.

2. **Proprietary closed source with ByteDance ownership** — The underlying VS Code fork
   is open source but Trae's AI layer and telemetry infrastructure are closed. ByteDance's
   regulatory exposure (TikTok precedent) introduces enterprise procurement and data
   residency risk for US and EU teams.

For personal experimentation on non-sensitive codebases, Trae's free model access and
autonomous Build/SOLO modes make it worth evaluating. For teams with strict data
governance, proprietary IP, or enterprise compliance requirements, the telemetry posture
places it on Hold until ByteDance publishes a verifiable audit or compliant enterprise
offering.

Compare with [GitHub Copilot CLI][copilot-cli-ref], which operates in a headless/terminal
context with clear Microsoft privacy commitments and enterprise audit controls.

## Action Items

- Monitor ByteDance for SOC 2 Type II certification or enterprise data residency options.
- Re-evaluate telemetry posture if a verifiable Privacy Mode covering background
  collection is published.
- Track Linux support GA — currently unscheduled as of 2026-06-16.
- For teams trialing: run on air-gapped dev machines or network-monitored environments;
  avoid committing proprietary IP via Trae until telemetry scope is clarified.

## Sources

| Source | Content |
|---|---|
| [Trae homepage][trae-home] | Product overview, TRAE Work and TRAE IDE landing (accessed 2026-06-16) |
| [Trae pricing][trae-pricing] | Five-tier token-based pricing, effective 2026-02-24 (accessed 2026-06-16) |
| [Trae blog index][trae-blog] | GA dates: SOLO GA Nov 4 2025, SOLO beta Mar 31 2026, Trae Work Jun 9 2026 (accessed 2026-06-16) |
| [Unit 221B telemetry report][unit221b] | ByteDance device tracking, persistent connections, JWT exposure analysis |
| [The Register, Jul 28 2025][register] | ~500 calls/7 min, 26 MB telemetry, ByteDance official response |
| [vibecoding.app review, Mar 17 2026][vibecoding] | Platform support, pricing table, privacy mode scope |
| [DevRadar open research][devradar] | CUE engine details, MCP integrations, model list (third-party) |

[trae-home]: https://www.trae.ai/
[trae-pricing]: https://www.trae.ai/pricing
[trae-blog]: https://www.trae.ai/blog
[unit221b]: https://blog.unit221b.com/dont-read-this-blog/unveiling-trae-bytedances-ai-ide-and-its-extensive-data-collection-system
[register]: https://www.theregister.com/2025/07/28/bytedance_trae_telemetry/
[vibecoding]: https://vibecoding.app/blog/trae-review
[devradar]: https://devradar-dev.github.io/open-research/ai-tools/trae/
[mcp-spec]: https://modelcontextprotocol.io/
[copilot-cli-ref]: github-copilot-cli-analysis.md
