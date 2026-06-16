---
title: Windsurf Analysis (now Devin Desktop, by Cognition)
source: https://devin.ai/
purpose: Analysis of Windsurf as an agentic IDE product — acquired by Cognition in 2025, rebranded Devin Desktop June 2026.
created: 2026-06-16
updated: 2026-06-16
validated_links: 2026-06-16
---

**Status**: Trial | **Proprietary** (No open-source license) | **GA**: as Windsurf (pre-acquisition); as Devin Desktop: June 2, 2026 | **Owner**: Cognition AI (acquired December 2025)

## What It Is

Windsurf was an **agentic IDE** built by Codeium — a VS Code-compatible editor
with a proprietary AI layer (Cascade) offering inline completions, multi-file
edits, and autonomous agent "flows." As of **June 2, 2026**, the Windsurf IDE has
been rebranded **Devin Desktop** by Cognition AI, which acquired the product in
December 2025 for approximately $250 million (accessed 2026-06-16, first-party via
[Cognition acquisition blog][cognition-windsurf-blog]).

The product retains backward compatibility with VS Code extensions and continues
under active development. Pricing, plans, and extensions carried over without
change at the rebrand date ([Devin Desktop launch post][devin-desktop-blog]). See also [devin-cli-analysis.md](devin-cli-analysis.md) — Cognition's terminal Devin CLI in the same product family.

**Ownership chain** (as of 2026-06-16, via [cognition.ai][cognition-windsurf-blog]):

- **Codeium** built Windsurf; operated it until mid-2025
- **OpenAI** negotiated acquisition at ~$3B; deal collapsed (not confirmed on
  first-party pages — noted as "not stated" in Cognition's announcement)
- **Google DeepMind** licensed Windsurf technology and hired key founders
  (Varun Mohan, Douglas Chen) in a separate transaction
- **Cognition AI** acquired Windsurf — IP, product, trademark, brand, and ~210
  employees — in December 2025 for ~$250M; Cognition's announcement states
  $82M ARR and 350+ enterprise customers at acquisition time

## How It Works

### Architecture and models

The product shipped under two AI stacks post-acquisition:

- **Cascade** — Windsurf's original multi-file edit and agent-flow engine; still
  the default local engine
- **Devin Local** — a Rust rewrite of Cascade introduced at the June 2026
  rebrand; described as "up to 30% more token efficient" and adds subagent
  support ([Devin Desktop launch post][devin-desktop-blog])
- **SWE-1.6** — Cognition's proprietary coding model, available free on the Pro
  tier; built for agentic tasks rather than general assistance

Model access on Pro and above spans OpenAI, Claude, and Gemini via a
credit/quota system (accessed 2026-06-16 via [devin.ai/pricing][devin-pricing]).

### Agent Command Center

Introduced in **Windsurf 2.0** (April 15, 2026) and carried into the Devin
Desktop rebrand, the Agent Command Center provides a Kanban-style view for
managing multiple local and cloud agents from a single IDE surface. **Spaces**
group sessions, PRs, files, and shared context across agents.

The IDE supports the **Agent Client Protocol (ACP)**, allowing third-party agents
(Claude Code Agent, OpenAI Codex, OpenCode) to run inside Devin Desktop as
first-class participants alongside Devin Cloud agents.

### Codemaps

AI-annotated visual graph of codebase structure: nodes carry AI-generated
explanations, and the view supports feature-implementation mapping, data-flow
tracing, call-site highlighting, and PR-specific structural change visualization.
Described on [nxcode.io][nxcode-acquisition] as targeting "code I did not write"
onboarding — a secondary-source characterization, not stated verbatim on the
first-party page.

### Headless / CLI mode

No dedicated headless or CLI invocation mode was found on first-party pages as of
2026-06-16. The product is **GUI-first** (desktop IDE). Devin Cloud (available on
Pro+) can run autonomous coding tasks in a cloud environment, which is the closest
equivalent to headless execution, but it is browser/API-accessed rather than
terminal-native.

### Platforms and install

VS Code-compatible desktop IDE; backwards-compatible with VS Code extensions.
JetBrains support was noted in earlier reports as continuing under the Windsurf
name, but this was not confirmed on first-party pages as of 2026-06-16 (not
stated). Available on Linux, macOS, and Windows.

## Pricing

Pricing as of 2026-06-16 ([devin.ai/pricing][devin-pricing], accessed 2026-06-16):

| Tier | Price | Key limits |
|---|---|---|
| Free | $0/month | Light quota; unlimited inline edits and Tab completions |
| Pro | $20/month | Full model access (OpenAI, Claude, Gemini); free SWE-1.6; Devin Cloud |
| Max | $200/month | Everything in Pro, significantly higher quotas |
| Teams | $80/month + $40/seat | Centralized billing, admin dashboard, collaboration |
| Enterprise | Custom | SAML/OIDC SSO, dedicated deployment, HIPAA/FedRAMP (not stated on pricing page — "not stated" for compliance tier details) |

Note: an earlier third-party report ([nxcode.io][nxcode-acquisition]) cited a
$15/month Pro price as of May 2026; the current first-party page shows $20/month
(accessed 2026-06-16). Use the first-party figure; prices change frequently.

## Adoption Decision

| Dimension | Assessment |
|---|---|
| **Use case** | Agentic IDE (GUI); multi-agent command center replacing the terminal-only coding agent pattern |
| **Model flexibility** | Multi-provider (OpenAI, Claude, Gemini) + proprietary SWE-1.6 on Pro+ |
| **Extensibility** | ACP for third-party agents; VS Code extension compatibility; Devin Cloud for autonomous tasks |
| **Headless** | No — GUI-first; Devin Cloud is the nearest analog for unattended runs |
| **Maturity** | GA (June 2, 2026 as Devin Desktop); actively developed post-acquisition |
| **License** | Proprietary — no open-source license stated |
| **Cost** | Free tier available; Pro $20/month (2026-06-16); enterprise custom |

**Strengths**: Strong multi-agent surface (ACP, Agent Command Center, Spaces)
positions it ahead of single-agent IDEs for orchestration workflows. Devin Cloud
integration gives autonomous background execution without leaving the IDE.
Proprietary SWE-1.6 model included at no extra cost on Pro. Large enterprise base
($82M ARR, 350+ customers) inherited from Codeium suggests production stability.

**Risks**: Layered acquisition history (Codeium → Google licensing split →
Cognition) creates brand/continuity uncertainty; "Windsurf" branding is now
retired in favor of Devin Desktop. No open-source license — cannot self-host or
fork. GUI-only limits CI/headless workflows compared with terminal peers such as
[GitHub Copilot CLI][github-copilot-cli-analysis]. Ownership by Cognition AI
(private company) adds vendor-lock risk.

**Trial recommendation**: Worth evaluating for teams that want a unified
IDE + multi-agent command center and are comfortable with proprietary tooling.
Hold final adoption until the Cognition/Windsurf integration trajectory stabilizes
(rebrand is less than 30 days old as of this writing).

## Action Items

- **Pilot** on a team already familiar with VS Code-compatible IDEs — zero
  extension migration cost; evaluate ACP and Agent Command Center for
  multi-agent orchestration fit.
- **Benchmark SWE-1.6** against Claude Sonnet 4.5 and GPT-5 on
  representative agentic tasks before committing Pro/Teams spend.
- **Clarify headless story** — if CI/unattended runs are needed, assess Devin
  Cloud API access (not investigated; no first-party CLI docs found 2026-06-16)
  or compare against [GitHub Copilot CLI][github-copilot-cli-analysis] for
  terminal-native workflows.
- **Track branding stability** — the Devin Desktop rebrand is recent; re-verify
  feature parity, pricing, and JetBrains plugin status in 90 days.

## Cross-References

- [github-copilot-cli-analysis.md](github-copilot-cli-analysis.md) — terminal-native alternative; compare for headless/CI workflows

## Sources

| Source | Content |
|---|---|
| [Cognition acquisition blog][cognition-windsurf-blog] | Acquisition announcement: employees, ARR, brand; July 14 2025 |
| [Devin Desktop launch post][devin-desktop-blog] | Rebranding details, ACP, Devin Local, Spaces; June 2 2026 |
| [devin.ai/pricing][devin-pricing] | Pricing tiers; accessed 2026-06-16 |
| [NxCode acquisition report][nxcode-acquisition] | Third-party: SWE-1.5, Codemaps, $250M deal, May 2026 pricing |
| [windsurf.com redirect][windsurf-redirect] | 308 permanent redirect to devin.ai/desktop; accessed 2026-06-16 |

[cognition-windsurf-blog]: https://cognition.ai/blog/windsurf
[devin-desktop-blog]: https://devin.ai/blog/windsurf-is-now-devin-desktop
[devin-pricing]: https://devin.ai/pricing
[nxcode-acquisition]: https://www.nxcode.io/resources/news/cognition-windsurf-acquisition-swe-1-5-codemaps-2026
[windsurf-redirect]: https://windsurf.com/
[github-copilot-cli-analysis]: github-copilot-cli-analysis.md
