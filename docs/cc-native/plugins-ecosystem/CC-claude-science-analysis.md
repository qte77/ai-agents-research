---
title: Claude Science Analysis
source: https://claude.com/docs/claude-science/overview
purpose: Record what Anthropic's Claude Science desktop workbench is, how it runs analyses, and how its provenance and reviewer features relate to Claude Code and Cowork.
created: 2026-10-03
updated: 2026-10-06
validated_links: 2026-10-06
status: beta
---

**Details:** beta; Pro, Max, Team and Enterprise plans; separate desktop app (docs, fetched 2026-10-03)

## What It Is

Claude Science is "a desktop application that pairs Claude with an analysis environment on your computer" ([docs][overview]). Anthropic's launch post (Jun 30, 2026) calls it "an AI workbench for scientists" ([news][news]). It is installed separately from the Claude desktop app ([docs][overview]).

How it works, per the docs ([docs][overview]):

- **Execution**: Claude "writes and runs Python, R, or shell code in a sandbox, reads the folders you grant it, pulls data from scientific databases through connectors". The user approves "each new folder, network host, and remote job before Claude can use it".
- **Provenance**: results are saved "as versioned artifacts with a full provenance record". Per the [artifacts page][artifacts], every artifact version opens a Provenance view with five tabs: Messages, Code ("a reproducible script, downloadable as a script or notebook"), Execution Log ("every command that ran"; "the authoritative record of what ran"), Environment ("every installed package with its version") and Review. Versions have a stepper and a diff view, and links Claude puts in the conversation "point to the specific version that existed at the time".
- **Reviewer**: "A background reviewer can check Claude's claims against the work that was actually run." The docs bound it: "The reviewer reduces, but doesn't eliminate, errors. It checks claims against the execution record and doesn't re-run analyses." The launch post describes it as "a reviewer agent checks citations and calculations, flagging and correcting errors" ([news][news]). On Pro, auto-review is off by default: "turn it on from the session settings, and it stays off until you do" ([changelog][changelog] 0.1.16, Jul 7, 2026).
- **Remote compute**: jobs can run on "a workstation or Slurm cluster you reach over SSH, or on cloud GPUs through your own Modal account". On Team and Enterprise plans the org admin decides whether SSH hosts and Modal are allowed.
- **Connectors and skills**: the launch post counts "over 60 curated skills and connectors pre-configured for genomics, single-cell, proteomics, structural biology, cheminformatics, and more" ([news][news]). The docs say it is not limited to the life sciences and list fields from computer science to the social sciences.
- **Scope limit**: "Claude Science is a research tool and isn't intended for clinical or diagnostic use."

## Plans and Platforms

- **Plans**: Pro, Max, Team or Enterprise; not Free. On Team and Enterprise an Owner must enable it for the organization first ([docs][overview], [support][support]).
- **Usage**: "Your Claude Science usage counts toward the same usage limits as the rest of your Claude plan, including Claude Code and Cowork" ([docs][overview]).
- **Platforms — a timeline, not a conflict.** The [changelog][changelog] dates both steps: "Public launch of Claude Science" (0.1.14, Jun 30, 2026) and "Claude Science is now available for Windows" (0.1.47, Sep 10, 2026). The sources simply predate or postdate Windows:

| Source | Date | Platforms stated |
|---|---|---|
| [Launch post][news] | Jun 30, 2026 | "available in beta on macOS and Linux" |
| [Support article][support] | updated Aug 21, 2026 (before Windows) | "macOS 13 or later, and Linux x64" |
| [Docs overview][overview] | fetched 2026-10-03 | "macOS, Windows, and Linux"; requirements list Windows 11 (x64) |

Linux also needs socat, bubblewrap 0.8.0 or later and unprivileged user namespaces ([docs][overview]); 0.1.43 (Aug 31, 2026) fixed Linux commands breaking after "bubblewrap's recent security update" ([changelog][changelog]). For bubblewrap behaviour in Claude Code itself see [CC-sandbox-bwrap-host-quirks.md](../sandboxing/CC-sandbox-bwrap-host-quirks.md).

## Relation to Claude Code and Cowork

Claude Science shares plan limits with Claude Code and Cowork but is a separate app with its own sandbox, connectors and skills ([docs][overview]). Its sandboxed execution plus a versioned, provenance-recorded artifact store and a reviewer that checks claims against the execution record makes it a first-party agent workbench that keeps the run record next to the result.

**Export, sharing and replay** (documented):

- *Export: yes.* An artifact's menu offers **Download**, **Export Metadata** and **Export to Cloud**, and the project folder under `~/.claude-science` can be copied ([artifacts][artifacts]).
- *Sharing: no.* "Anthropic doesn't sync your projects, artifacts, or conversation history to your Claude account"; each computer "keeps its own projects", and a file saved with **Export session** "can't be loaded into Claude Science on another computer" ([multiple computers][multi]). The documented way to reach the same projects from several computers is one install on a Linux server reached over an SSH tunnel.
- *Replay: partial.* The Code tab gives a downloadable script or notebook and the Environment tab the package versions, but the reviewer "doesn't re-run analyses" ([docs][overview]), and the docs do not document pinning the model or random seeds.

No rubric score is given. Under the gap-driven policy (plan 0011, O1), a score would only matter if it could change a cell of the [reference architecture](../../sdlc-lcm/agent-substrate-reference-architecture.md). At best this is `partial` on Reproducible for harness and long-running, which those subjects already reach. It is not a context layer, so it does not bear on the open context·Reproducible cell.

Cross-ref: [research-agents-landscape.md](../../non-cc/knowledge-management/research-agents-landscape.md) (third-party research agents and workbenches, e.g. OpenScience), [CC-cowork-skills-api-workflows.md](CC-cowork-skills-api-workflows.md) (Cowork), [CC-mcp-hardware-standard-analysis.md](CC-mcp-hardware-standard-analysis.md) (agents operating lab hardware).

## Sources

| Source | Content |
|---|---|
| [Claude Science docs overview][overview] | Description, sandbox, provenance, reviewer, remote compute, requirements, plans and usage |
| [Anthropic news: Claude Science][news] | Launch post (Jun 30, 2026): workbench framing, curated skills/connectors, reviewer agent, macOS + Linux beta |
| [Support: Get started with Claude Science][support] | Plan enablement, supported OS (updated Aug 21, 2026) |
| [Claude Science product page][product] | Product page |
| [Artifacts in Claude Science][artifacts] | Provenance tabs, versions, Download / Export Metadata / Export to Cloud |
| [Use Claude Science on more than one computer][multi] | No cloud sync; per-computer projects; Export session not loadable elsewhere |
| [Claude Science changelog][changelog] | 0.1.14 public launch (Jun 30), 0.1.16 Pro auto-review off by default, 0.1.43 bubblewrap fix, 0.1.47 Windows (Sep 10) |

[overview]: https://claude.com/docs/claude-science/overview
[news]: https://www.anthropic.com/news/claude-science-ai-workbench
[support]: https://support.claude.com/en/articles/16563838-get-started-with-claude-science
[product]: https://claude.com/product/claude-science
[artifacts]: https://claude.com/docs/claude-science/artifacts
[multi]: https://claude.com/docs/claude-science/multiple-computers
[changelog]: https://claude.com/docs/claude-science/changelog
