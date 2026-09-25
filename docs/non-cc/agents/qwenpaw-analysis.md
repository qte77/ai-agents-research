---
title: QwenPaw — Self-Hosted Personal AI Assistant on AgentScope
source: https://github.com/agentscope-ai/QwenPaw
purpose: Evaluate QwenPaw's self-hosted, multi-channel personal-assistant architecture and its three-tier memory design
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
---

**Status**: Assess

## What It Is

[QwenPaw][qwenpaw-gh] is a self-hosted personal AI assistant built on **AgentScope**
(`agentscope-ai`, the org that also publishes it) and Alibaba's **Qwen** model family. Its README
tagline: "Your personal AI assistant — deploy locally or in the cloud, extend with Skills &
Plugins, connect across every channel" (accessed 2026-09-24).

**Repository facts** (`gh api repos/agentscope-ai/QwenPaw`, accessed 2026-09-24): 35,255 stars,
3,127 forks, **Apache 2.0** license, created 2026-02-24, latest tagged release `v2.2.1` (published
2026-09-11). Supported Python range is 3.11–<3.14 (per the README's version badge); it is
published to PyPI as `qwenpaw`.

## How It Works

**Three-tier memory.** Per the README: "live working context, full verbatim history, and a
self-evolving personal knowledge base" powered by [ReMe][reme-gh] (also an `agentscope-ai`
project), which converts conversations and resources into readable, editable, searchable, linked
Markdown memory.

**Multi-channel access.** A single agent instance connects to DingTalk, Lark, WeChat, Discord,
Telegram, and iMessage simultaneously, alongside a web console and terminal interface (per the
project's own feature summary, accessed 2026-09-24).

**Security.** Described as five-layer protection: kernel-level sandboxing, tool inspection, file
access controls, skill scanning, and declarative access policies.

**Extensibility.** Built-in skills for scheduling, document processing, and web browsing; a plugin
marketplace; and MCP (Model Context Protocol) integration for external tools.

**Local-model support.** Compatible with QwenPaw-Flash (2B/4B/9B variants), Ollama, and LM Studio
for fully local deployment with no API keys required.

**Installation paths** (per the README, accessed 2026-09-24): pip (Python 3.11+), an automated
install script, Docker, cloud platforms (Alibaba Cloud, AgentScope Platform, ModelScope), or
desktop apps (macOS/Windows, beta).

## Adoption Decision

**Assess.** QwenPaw's traction (35k+ stars, 3.1k forks) and release cadence (a `v2.2.1` tag two
weeks before this review, on a repo created seven months prior) indicate a maturing, actively
maintained project, and the AgentScope/Alibaba backing gives it institutional weight comparable to
other framework-backed assistants in this corpus. The three-tier memory design (working context +
verbatim history + an evolving Markdown knowledge base via ReMe) is a concrete, inspectable memory
architecture worth comparing against memory tooling already tracked in
[`../cc-community/CC-memory-tooling-landscape.md`](../../cc-community/CC-memory-tooling-landscape.md).

Against that: QwenPaw is tightly coupled to the Qwen model family and the DingTalk/Lark/WeChat
channel ecosystem, which are China-market-centric integrations with less direct overlap with this
corpus's Claude Code focus than a harness-agnostic tool would have. No first-party mention of
Claude Code integration was found as of 2026-09-24. **Assess** — a strong project in its own
lane, without yet a clear on-ramp into this corpus's primary (CC-adjacent) research focus.

## Action Items

- If a future pass covers [ReMe][reme-gh] directly (memory-specific), cross-link it from here
  rather than duplicating its description.
- Re-verify Python version support and license at the next refresh — both are stated via README
  badges, which drift faster than prose.
- Watch for any first-party MCP-based Claude Code compatibility notes (none found as of
  2026-09-24).

## Sources

| Source | Content |
|---|---|
| [agentscope-ai/QwenPaw README][qwenpaw-gh] | Feature summary (memory, channels, security, extensibility), install paths, Python version support |
| `gh api repos/agentscope-ai/QwenPaw` | Stars (35,255), forks (3,127), license (Apache-2.0), created (2026-02-24), accessed 2026-09-24 |
| `gh api repos/agentscope-ai/QwenPaw/releases/latest` | Latest tag `v2.2.1`, published 2026-09-11, accessed 2026-09-24 |
| [agentscope-ai/ReMe][reme-gh] | Linked memory-engine project referenced by the QwenPaw README |

[qwenpaw-gh]: https://github.com/agentscope-ai/QwenPaw
[reme-gh]: https://github.com/agentscope-ai/ReMe
