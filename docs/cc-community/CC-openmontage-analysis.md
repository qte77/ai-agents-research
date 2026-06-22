---
title: "OpenMontage: Agentic Video Production as a CLAUDE.md-Driven Workspace"
source: https://github.com/calesthio/OpenMontage
purpose: Analyze OpenMontage's CLAUDE.md-as-domain-controller architecture (and the parallel Palmier pivot signal) for the agent-workspace patterns this corpus tracks
created: 2026-06-22
updated: 2026-06-22
validated_links: 2026-06-22
platform_scope: [claude-code, cursor, copilot, windsurf, codex]
---

**Status**: Trial

## What It Is

[OpenMontage][repo] is an open-source (AGPL-3.0) "agentic video production system" that runs *inside*
an AI coding assistant rather than as a standalone app. A user opens the repo in a Claude Code (or
Cursor / Copilot / Windsurf / Codex) workspace and describes a video; the agent reads routing rules from
`AGENT_GUIDE.md` and orchestrates the full research-to-render workflow. The corpus-relevant interest is
**not** the video output — it is the **CLAUDE.md-as-domain-controller** pattern: a one-line `CLAUDE.md`
delegates all behavior to [`AGENT_GUIDE.md`][guide], turning a general coding agent into a domain pipeline
engine. That makes it a direct sibling to the genome-analysis case study in
[CC-domain-claudemd-showcase.md][showcase].

Basics (first-party, figures hedged): author [calesthio][author] — also Crucix and the SessionAnchor
CC-session-memory tool; AGPL-3.0; ~10.5 k stars; Python ~89 % / TypeScript ~9 %; first commits ~2026-04-08;
**no tagged releases (unversioned)**.

## How It Works

The novel core is a **three-layer knowledge architecture** the agent reads at runtime:

1. **Tool registry** — *what exists*: ~52 production tools (video/image generation, TTS, music, audio
   mixing, subtitles) discoverable at runtime via `capability_catalog()` / `provider_menu_summary()` —
   no hardcoded provider lists.
2. **Stage-director skills** — *how to use them*: ~12 pipelines (explainers, documentaries, trailers,
   clip factories, localization, …) expressed as YAML manifests.
3. **Vendor skills** — *provider-specific prompting* (FAL.ai, ElevenLabs, Runway, Kling, Suno, …).

Execution is **checkpoint-gated**: canonical JSON artifacts flow brief → script → scene_plan →
asset_manifest → edit_decisions → render_report, with quality gates (e.g. slideshow-risk detection) and an
explicit composition-runtime choice (Remotion vs HyperFrames — never a silent default). A **zero-cost path**
(Piper TTS + open archives such as Archive.org / NASA / Wikimedia + free composition) lets the pipeline run
with no API keys, and a 7-dimension provider-scoring step ranks tools before selection.

## Related Pattern & Market Signal: Palmier

[Palmier Pro][palmier] is a second 2026 take on agent-driven media production. Its **product** (a macOS
video editor) is out of scope here, but two of its **concepts** transfer directly to the agent-integration
patterns this corpus tracks:

- **Timeline-as-MCP-workspace** — Palmier embeds a local MCP server (`127.0.0.1:19789/mcp`) that exposes
  its project state to any MCP client (Claude Desktop, Cursor, Codex), which can then read and mutate the
  timeline. Generalizes to: *expose your app's domain state as a local MCP server so any agent can drive it.*
- **Control-plane-open / generation-plane-monetized** — the editor, MCP server, and in-app agent chat are
  GPLv3; only the generative compute is paid. A clean split between the (open) agent control surface and the
  (paid) heavy compute.

**Market signal — a coding-agent startup left coding agents.** Palmier ([YC S24][palmier-yc]) launched in
2024 as "AI that understands any codebase" — a coding-agent/sandbox platform that powered SWE-agent (its
`SWE-ReX` fork still sits on [the org][palmier-org]) — then **pivoted to video in 2025** (reported reason:
it kept dogfooding its own tooling to cut launch videos and found more pull there). A coding-agent company
walking away from coding agents is a notable differentiation-pressure signal for the space this corpus
tracks. The pivot rationale is reported, not independently audited.

Cross-ref: the MCP/agent-integration surface in [CC-connectors-overview.md][connectors] and the
generative-UI layer in [ag-ui-protocol-landscape.md][agui]; OpenMontage's domain-controller sibling is
[CC-domain-claudemd-showcase.md][showcase].

## Adoption Decision

**Trial.** OpenMontage is genuinely novel (declarative three-layer skill system, runtime capability
discovery, checkpoint-gated orchestration) and AGPL-3.0 with a zero-cost path lowers the barrier — but it
is young (~2 months, no tagged releases) and `AGENT_GUIDE.md` is Claude-Code-idiomatic, so its cross-assistant
claims are unverified. Trial it as a reference implementation of the CLAUDE.md-as-domain-controller pattern.
The transferable Palmier patterns (timeline-as-MCP-workspace; control/generation-plane split) are reusable
for our own agent integrations regardless of the video domain.

## Sources

| Source | Content |
|---|---|
| [calesthio/OpenMontage (GitHub)][repo] | Primary repo — README, `CLAUDE.md`, AGPL-3.0, ~10.5 k stars, language split |
| [AGENT_GUIDE.md][guide] | Routing rules, three-layer architecture, checkpoint protocol |
| [calesthio (author)][author] | Bio + sibling projects (Crucix, SessionAnchor) |
| [Palmier Pro (GitHub)][palmier] | Concepts + pivot — GPLv3 macOS video editor with an embedded MCP server |
| [Palmier YC profile][palmier-yc] | YC S24; founder + pivot history (coding-agent → video) |

[repo]: https://github.com/calesthio/OpenMontage
[guide]: https://github.com/calesthio/OpenMontage/blob/main/AGENT_GUIDE.md
[author]: https://github.com/calesthio
[showcase]: CC-domain-claudemd-showcase.md
[connectors]: ../cc-native/plugins-ecosystem/CC-connectors-overview.md
[agui]: ../non-cc/ag-ui-protocol-landscape.md
[palmier]: https://github.com/palmier-io/palmier-pro
[palmier-yc]: https://www.ycombinator.com/companies/palmier
[palmier-org]: https://github.com/palmier-io
