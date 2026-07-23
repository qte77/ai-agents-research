---
title: Kiro Analysis
source: https://kiro.dev/
purpose: Analysis of Kiro, AWS's spec-driven agentic IDE, as a coding agent platform distinct from conversational AI coding assistants.
created: 2026-06-16
updated: 2026-07-23
validated_links: 2026-06-16
---

**Status**: Trial | **Vendor**: Amazon Web Services | **License**: Proprietary (AWS Customer Agreement) | **Preview**: 2025-07-14 | **GA**: 2025-11-17 | **CLI version**: 2.7.0 (2026-06-12) | Requires AWS Builder ID

## What It Is

Kiro is an **agentic IDE** from Amazon Web Services, launched in public preview on 2025-07-14 (at AWS Summit New York) and reaching general availability on 2025-11-17. It is positioned as the successor to Amazon Q Developer (new Q Developer signups blocked 2026-05-15; IDE plugins and paid subscriptions retired by 2027-04-30). It positions itself between "vibe coding" (unstructured prompt-to-code) and disciplined software engineering through a **spec-driven development** model: before any agent writes code, it produces three structured planning documents (requirements, design, tasks) that drive parallel agentic execution.

The product ships three surfaces — a desktop IDE (Code OSS-based, compatible with VS Code settings and extensions), a CLI (macOS/Linux/Windows), and a browser interface at `app.kiro.dev`. Models default to **Claude Sonnet 4.5**; Pro Max and Power tiers add **Claude Opus 4.8** (1M context window). Copyright is held by ©2026 Amazon.com, Inc. or its affiliates; the software is proprietary (accessed 2026-06-16).

**Key distinction vs peers** (GitHub Copilot CLI, Cursor, Windsurf): Kiro's differentiator is the mandatory spec phase — requirements, design, and tasks are first-class artifacts, not ephemeral chat history. This makes it the closest production IDE analogue to the structured-agent patterns documented in this research repo.

## How It Works

### Spec-Driven Workflow

Specs are the core primitive. Running `/spec` (or selecting "New Spec") triggers a three-phase pipeline:

1. **requirements.md** — user stories and acceptance criteria (structured notation, not free-form)
2. **design.md** — technical architecture, sequence diagrams, implementation approach
3. **tasks.md** — discrete, trackable implementation tasks with dependency graph analysis

The agent builds a dependency graph across tasks, groups independent tasks into concurrent execution **waves**, and runs them in parallel while sequencing dependent tasks. Real-time status (in-progress / completed) is visible per task. Specs are also available in the browser for planning before switching to the IDE for code generation (as of 2026-05-28 docs update).

A separate **"Vibe" mode** (agentic chat without a spec) is available for exploratory work where structure is premature.

### Hooks (Event-Driven Automation)

Hooks automate repetitive agent actions by triggering on IDE events:

| Trigger category | Examples |
|---|---|
| File operations | save, create, delete |
| Agent lifecycle | prompt submission, agent turn completion |
| Tool lifecycle | before/after tool invocations |
| Spec execution | before/after spec task completion |
| Manual | on-demand activation |

Actions are either **agent prompts** (Kiro interprets instructions) or **shell commands**. Hooks are configured in natural language (Kiro generates the config) or via a manual form specifying title, event type, file patterns, and action.

### Steering (Persistent Context)

Steering files (`.kiro/steering/*.md`) provide persistent markdown guidance that Kiro loads into interactions to enforce team conventions, patterns, and library choices. Unlike `AGENTS.md` (which lacks inclusion modes), steering supports four loading strategies:

- **Always** — loaded into every interaction
- **Conditional** — loaded when file patterns match (e.g., `components/**/*.tsx`)
- **Manual** — referenced explicitly via `#steering-file-name` in chat
- **Auto** — intelligently included when the request matches the file's description

**Scope hierarchy**: workspace steering (`.kiro/steering/`) overrides global steering (`~/.kiro/steering/`), which can be distributed to teams via MDM.

### MCP Integration

Kiro supports [MCP (Model Context Protocol)][kiro-mcp] servers enabled via Settings (Cmd+, / Ctrl+,). The **AWS Documentation MCP server** is the highlighted first-party example, providing inline access to AWS docs from within the IDE. Additional MCP servers extend Kiro's tool surface with external services and knowledge bases.

### Autopilot Mode

An **autopilot** mode (equivalent to "yolo" in peers) allows fully autonomous task execution without per-action approval. The `/goal` command (added CLI 2.7.0, 2026-06-12) enables iterative task completion with built-in verification loops. **Queue Steering** (`Ctrl+S`) allows mid-turn course corrections without stopping the agent.

### Pricing (accessed 2026-06-16)

| Plan | Monthly | Credits | Notes |
|---|---|---|---|
| Free | $0 | 50 | Claude Sonnet 4.5 + open-weight models only |
| Pro | $20 | 1,000 | Premium models; $0.04/credit overage |
| Pro+ | $40 | 2,000 | Premium models |
| Pro Max | $100 | 5,000 | Launched 2026-06-10 |
| Power | $200 | 10,000 | Highest individual tier |
| Team / Enterprise | Same base pricing | Same | Adds SAML/SCIM SSO via AWS IAM Identity Center, centralized billing, usage analytics |
| GovCloud | ~20% higher | — | Free tier unavailable |

Credits reset monthly; unused credits do not roll over. Overage billing is disabled by default and must be enabled in settings. Subscriptions process on the 1st of each month.

## Adoption Decision

| Dimension | Assessment |
|---|---|
| **Use case** | Spec-driven feature development; structured agentic coding in complex codebases |
| **Model** | Claude Sonnet 4.5 default; Opus 4.8 (1M context) on paid tiers |
| **Spec workflow** | Mandatory requirements → design → tasks pipeline before code generation |
| **Extensibility** | MCP, steering files, hooks, VS Code plugin compatibility |
| **Autonomy control** | Per-action approval → autopilot; `/goal` + Queue Steering for mid-turn correction |
| **Maturity** | Preview 2025-07-14; GA 2025-11-17; CLI v2.7.0 (2026-06-12); active release cadence |
| **License** | **Proprietary** — AWS Customer Agreement; incorporates OSS components (Chromium/BSD, Bun/MIT, WebKit/LGPL-2) |
| **Cost** | Free tier (50 credits/month); paid tiers $20–$200/month; requires AWS Builder ID |
| **AWS lock-in** | Auth via AWS Builder ID; native AWS Documentation MCP; designed around AWS CDK/Lambda/DynamoDB workflows |

**Strengths**: The three-document spec pipeline is the most structurally disciplined agentic coding workflow of any current IDE — specs become durable artifacts, not ephemeral chat. Parallel task wave execution with dependency graph analysis directly addresses context drift in long agentic runs. Steering's conditional and auto inclusion modes are more sophisticated than flat `AGENTS.md` injection. Native AWS integration (MCP, CDK scaffold, IAM policy generation) is a genuine differentiator for AWS-centric teams.

**Risks**: AWS Builder ID requirement and proprietary license create vendor lock-in at the credential and contract level. Credit-based model makes cost unpredictable on heavy autopilot usage. The spec phase adds upfront friction that may feel bureaucratic for exploratory or prototype work (Vibe mode partially mitigates this). GovCloud users face a 20% premium with no free tier.

## Action Items

- **Trial** for teams building AWS-native services — the AWS Documentation MCP, CDK scaffold, and IAM policy generation justify evaluation over generic agents for this workload.
- **Compare spec artifacts** (requirements.md / design.md / tasks.md) against the structured-agent patterns in this repo to assess portability of the planning workflow to other tools.
- **Evaluate steering** as an alternative to flat `AGENTS.md` for multi-agent shops where conditional context loading per file pattern would reduce noise — compare to [GitHub Copilot CLI][github-copilot-cli-analysis] instruction-file approach.
- **Track credit burn rate** on autopilot workloads before committing to a paid tier; the free 50-credit tier is insufficient for sustained agentic use.
- **Watch the Amazon Q Developer retirement timeline** — Kiro's positioning as a full replacement affects any org with existing Q Developer integrations.

## Cross-References

- [github-copilot-cli-analysis.md](github-copilot-cli-analysis.md) — peer terminal/IDE coding agent with comparable autonomy controls and MCP extensibility; contrast instruction-file approach (copilot-instructions.md) vs Kiro's steering system

## Sources

| Source | Content |
|---|---|
| [Kiro home][kiro-home] | Product overview, vendor (Amazon), surfaces (IDE/CLI/Web), agent features |
| [Kiro docs][kiro-docs] | Specs, hooks, steering, MCP, agentic chat; last updated 2026-05-28 |
| [Kiro pricing][kiro-pricing] | Tier names, costs, credit counts, team/enterprise features, GovCloud; accessed 2026-06-16 |
| [Kiro specs docs][kiro-specs] | Three-phase pipeline, dependency graph, parallel waves; last updated 2026-05-05 |
| [Kiro steering docs][kiro-steering] | Inclusion modes, scope hierarchy, file reference syntax |
| [Kiro MCP docs][kiro-mcp] | MCP enablement, AWS Documentation MCP server example |
| [Kiro license][kiro-license] | AWS Customer Agreement, proprietary status, OSS component list; ©2026 Amazon.com |
| [Kiro changelog][kiro-changelog] | CLI v2.7.0 (2026-06-12), /goal command, Queue Steering, GitLab support, Opus 4.8 |
| [Constellation Research — AWS launches Kiro][constellation] | Preview launch 2025-07-14 at AWS Summit New York; AWS executives Nikhil Swaminathan and Deepak Singh |
| [AWS blog — Kiro GA (2025-11-24 roundup)][aws-kiro-ga] | GA date (week of 2025-11-17); 250k preview users; four GA-launch capabilities including CLI and enterprise plans |
| usage.ai — AWS May 2026 updates (`usage.ai/blogs/aws/monthly-updates/aws-may-2026`, dead as of 2026-07-23 — redirect loop; retained for provenance) | Kiro Web launch; Q Developer retirement timeline; new Q Developer signups blocked 2026-05-15 |

[kiro-home]: https://kiro.dev/
[kiro-docs]: https://kiro.dev/docs/
[kiro-pricing]: https://kiro.dev/pricing/
[kiro-specs]: https://kiro.dev/docs/specs/
[kiro-steering]: https://kiro.dev/docs/steering/
[kiro-mcp]: https://kiro.dev/docs/mcp/
[kiro-license]: https://kiro.dev/license/
[kiro-changelog]: https://kiro.dev/changelog/
[constellation]: https://www.constellationr.com/insights/news/aws-launches-kiro-ide-powered-ai-agents
[aws-kiro-ga]: https://aws.amazon.com/blogs/aws/aws-weekly-roundup-how-to-join-aws-reinvent-2025-plus-kiro-ga-and-lots-of-launches-nov-24-2025
[github-copilot-cli-analysis]: github-copilot-cli-analysis.md
