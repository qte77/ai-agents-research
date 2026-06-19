---
title: Amazon Q Developer (CLI + IDE Agent) Analysis
source: https://aws.amazon.com/q/developer/
purpose: Assess Amazon Q Developer as a CLI and IDE coding agent, including its deprecation timeline and transition to Kiro.
created: 2026-06-16
updated: 2026-06-16
validated_links: 2026-06-16
---

**Status**: Hold

## What It Is

Amazon Q Developer is AWS's generative AI–powered coding assistant, covering two
agent surfaces: **IDE plugins** (VS Code, JetBrains, Visual Studio, Eclipse) and
a **CLI agent** (`q`) that embeds agentic chat, natural-language-to-bash
translation, and shell autocompletion in the terminal. It is built on [Amazon
Bedrock][q-bedrock-note] and augmented with AWS-specific content for architectural
guidance, code generation, security scanning, and agentic task execution.

**Hold rationale (as of 2026-06-16):** AWS announced end-of-support for Q
Developer IDE plugins and paid subscriptions on [April 30, 2026][q-eos-blog],
with the support deadline set for **April 30, 2027**. New Q Developer Free Tier
account creation and new subscriptions have been blocked since **May 15, 2026**.
The CLI has already been rebranded: the [AWS docs CLI page][q-cli-page] now reads
"The Q CLI has become the Kiro CLI," and the [open-source CLI repo][q-cli-repo]
(Apache-2.0 + MIT) states it "receives only critical security fixes" with new
features exclusively in Kiro. Existing installations continue to work through the
support window, but all forward investment is in [kiro.dev][kiro-dev].

Compare: [GitHub Copilot CLI](github-copilot-cli-analysis.md), the closest
actively-maintained proprietary CLI peer.

## How It Works

### CLI agent surface (`q`)

The `q` binary provides three capabilities in the terminal:

| Capability | Command | What it does |
|---|---|---|
| Agentic chat | `q chat` (or bare `q`) | Multi-turn agent that reads/edits files, runs shell commands, scaffolds projects; powered by Amazon Bedrock (Claude 3.7 Sonnet noted in third-party sources) |
| Natural-language translation | `q translate` | Converts plain-English descriptions ("copy all files to S3") into executable shell snippets |
| Inline autocomplete | shell integration | Ghost-text completions for 250+ CLIs including `git`, `aws`, `docker`, `npm` in bash, zsh, and fish |

Agent sub-modes are available via `q chat --agent <name>` (e.g., `front-end`,
`back-end`). The CLI was distributed as a single Rust binary (macOS DMG, Homebrew,
Ubuntu/Debian packages, AppImage for Linux). Version v1.19.7 was the [last
release][q-cli-releases] (November 17, 2025; verified 2026-06-16 from the repo).

### IDE agent surface

Plugins for VS Code, JetBrains, Visual Studio, and Eclipse (preview) deliver:

- Inline code completions (snippets to full functions, triggered by comments)
- Agentic chat panel: reads project files, suggests diffs, generates shell commands
- Security vulnerability scanning (Java, Python, JavaScript)
- Code transformation: Java language upgrades (up to 4,000 lines/month on Pro), .NET porting

AWS Console, AWS Documentation website, Microsoft Teams, and Slack integrations
are **not** in the deprecation scope — those continue operating unchanged per the
[end-of-support announcement][q-eos-blog].

### Model and data handling

Built on Amazon Bedrock. Free Tier users' content may be used for service
improvement; Pro Tier users are automatically opted out. The underlying model is
not stated in first-party sources reviewed (2026-06-16).

### Pricing (access date 2026-06-16; subject to change during wind-down)

| Tier | Cost | Agentic requests | Code transformation |
|---|---|---|---|
| Free | $0 | 50/month | 1,000 lines/month |
| Pro | $19/user/month | 10,000 inference calls/month | 4,000 lines/month (pooled) |

Pro overage for code transformation: $0.003 per line submitted beyond the
monthly allocation. New Pro subscriptions are no longer available (blocked May 15,
2026).

## Adoption Decision

| Dimension | Assessment |
|---|---|
| **Status** | **Deprecated** — new signups blocked 2026-05-15; IDE + subscription EOS 2027-04-30 |
| **CLI** | Rebranded to Kiro CLI; open-source repo maintenance-only |
| **IDE plugins** | Active through 2027-04-30; no new features |
| **License (CLI repo)** | Apache-2.0 + MIT (open source, but maintenance-only) |
| **License (service)** | Proprietary (AWS managed service) |
| **Model flexibility** | AWS Bedrock only; no provider switching |
| **AWS integration** | Deep — Console, Slack/Teams, IAM, AWS Builder ID free login |
| **Cost** | Free tier (50 agentic req/month); Pro $19/user/month (no new subs) |

**Strengths** (historical / for existing users): Deep AWS ecosystem integration
with AWS Builder ID (no AWS account required for free tier). Broad language
support (Python, Java, JavaScript, TypeScript, C#, Go, Rust, PHP, Ruby, Kotlin,
C, C++, shell, SQL, Scala, JSON, YAML, HCL). Free tier is genuinely useful for
individual AWS builders. Open-source CLI (Apache-2.0 + MIT) was community-forkable.

**Risks / why Hold**: Product is in active wind-down. No new subscriptions
available. The successor (Kiro) is a closed-source, proprietary product — teams
adopting Q Developer today are on a forced migration path with no OSS fallback
from the upstream repo. Bedrock-only model lock-in contrasts with multi-provider
peers (see [GitHub Copilot CLI](github-copilot-cli-analysis.md)'s `/model` switch).

## Action Items

- **Existing Q Developer Free / Pro users**: Evaluate [kiro.dev][kiro-dev]
  migration before May 2027; the [upgrade guide][q-upgrade-kiro] describes the
  in-place rebrand path.
- **Do not onboard new teams** to Q Developer — new Free Tier account creation
  and new subscription creation are blocked since May 15, 2026.
- **AWS Console / chat-app users** (Teams, Slack): No action required — these
  surfaces are not in the deprecation scope.
- **Track Kiro** as a separate entry once it reaches GA and first-party pricing
  and feature docs stabilize.

## Sources

| Source | Content |
|---|---|
| [Amazon Q Developer product page][q-product] | Feature overview, IDE list, CLI description, Free/Pro pricing (access 2026-06-16) |
| [Amazon Q Developer docs — What Is][q-docs-what-is] | Architecture (Bedrock), IDE setup, pricing tiers, access methods |
| [Amazon Q Developer pricing page][q-pricing] | Free tier limits (50 agentic req, 1,000 lines), Pro $19/user/month, overage rates (access 2026-06-16) |
| [Q Developer CLI docs page][q-cli-page] | "The Q CLI has become the Kiro CLI" — confirms CLI rebrand (access 2026-06-16) |
| [Upgrade to Kiro docs][q-upgrade-kiro] | Rebrand mechanics, admin migration, Kiro console (access 2026-06-16) |
| [EOS announcement blog][q-eos-blog] | Dates: signup block 2026-05-15, IDE+sub EOS 2027-04-30, blog posted 2026-04-30 |
| [amazon-q-developer-cli GitHub repo][q-cli-repo] | License (Apache-2.0 + MIT), v1.19.7 last release 2025-11-17, maintenance-only status (access 2026-06-16) |
| [Amazon Q Developer FAQs][q-faqs] | CLI shell support (bash/zsh/fish), 250+ CLI completions, language list (access 2026-06-16) |

[q-product]: https://aws.amazon.com/q/developer/
[q-docs-what-is]: https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/what-is.html
[q-pricing]: https://aws.amazon.com/q/developer/pricing/
[q-cli-page]: https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line.html
[q-upgrade-kiro]: https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/upgrade-to-kiro.html
[q-eos-blog]: https://aws.amazon.com/blogs/devops/amazon-q-developer-end-of-support-announcement/
[q-cli-repo]: https://github.com/aws/amazon-q-developer-cli
[q-cli-releases]: https://github.com/aws/amazon-q-developer-cli/releases
[q-faqs]: https://aws.amazon.com/q/developer/faqs/
[q-bedrock-note]: https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/what-is.html
[kiro-dev]: https://kiro.dev/docs/
