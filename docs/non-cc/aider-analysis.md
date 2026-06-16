---
title: Aider — Terminal AI Pair Programmer
source: https://aider.chat/
purpose: OSS terminal coding agent with git-native workflow and multi-LLM support
created: 2026-06-16
updated: 2026-06-16
validated_links: 2026-06-16
---

**Status**: Adopt

## What It Is

Aider is an **open-source, terminal-based AI pair-programming tool** ("AI pair
programming in your terminal") maintained by the [Aider-AI][aider-gh] organization.
It pairs a developer's local shell session with any supported LLM to plan and
apply code changes across an entire repository, committing the results directly
via git.

Key facts (accessed 2026-06-16):

- **License**: Apache-2.0 ([confirmed][aider-license])
- **Stars**: 46.3 k (GitHub, 2026-06-16)
- **Latest release**: v0.86.0 (2025-08-09, per [GitHub releases][aider-releases])
- **Install count**: 6.8 M total pip installs (aider.chat homepage, 2026-06-16)
- **Active throughput**: ~15 B tokens/week (aider.chat homepage, 2026-06-16)
- **Self-hosted**: Aider wrote 88 % of the code in v0.86.0 itself

Aider is fully headless — it runs entirely in the terminal with no GUI
dependency, making it suitable for SSH sessions, CI pipelines, and any
environment where a browser-based IDE is unavailable.

## How It Works

### Installation and entry-point

```bash
python -m pip install aider-install
aider-install
```

Then invoke `aider` in a git repository with an LLM API key set in the
environment (e.g. `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`).

### Codebase mapping

Aider builds a **repo map** — a compressed, token-efficient index of all
files, classes, and functions — so the LLM can reason about large codebases
without loading every file into context. The map is regenerated incrementally
as files change ([aider.chat docs][aider-repomap]).

### Edit loop

1. Developer describes a change in the chat prompt.
2. Aider sends the repo map plus relevant file contents to the LLM.
3. The LLM returns a structured diff in one of Aider's **edit formats**
   (unified diff, whole-file, or search-replace); Aider applies it locally.
4. Aider runs any configured linters or test commands and feeds failures back
   to the LLM for self-correction.
5. On success, Aider creates a **git commit** with an auto-generated message.

### Supported LLMs

Aider supports virtually any LLM via API, including:

| Provider | Example models |
|---|---|
| Anthropic | Claude 3.7 Sonnet, Claude 4.x (main-branch aliases, 2026-06-16) |
| OpenAI | GPT-5, o3-mini, GPT-4o |
| DeepSeek | R1, Chat V3, Reasoner |
| Google | Gemini 2.5 Pro/Flash |
| Local/self-hosted | Any model via OpenAI-compatible endpoint |

Model selection: `aider --model <model-id>`.

### Git-native design

Every successful edit becomes a git commit. Aider never modifies files outside
the working tree, and the diff history serves as a full audit trail. This
distinguishes it from cloud-based agents that apply changes without a local
commit record.

### Polyglot benchmark (leaderboard)

Aider publishes an open [LLM leaderboard][aider-leaderboard] that evaluates
models on 225 Exercism exercises across C++, Go, Java, JavaScript, Python, and
Rust. As of 2025-11-20 (last leaderboard update per the page, accessed
2026-06-16), the top result was gpt-5 (high) at 88.0 % correct — the benchmark
is used to guide model selection recommendations.

### Additional capabilities

- **Watch mode**: IDE integration via a file-watcher so edits from any editor
  trigger Aider in the background.
- **Voice-to-code**: Microphone input transcribed to chat prompts.
- **Image context**: Paste screenshots or diagrams as context.
- **Web page context**: Fetch a URL and include its content in the prompt.
- **Web chat copy/paste mode**: Use any LLM web interface without an API key.

## Adoption Decision

| Dimension | Assessment |
|---|---|
| **License** | Apache-2.0 — fork, embed, and redistribute freely |
| **Cost** | Tool is free; pay only for LLM API tokens consumed |
| **Model flexibility** | Any LLM with an OpenAI-compatible API |
| **Git integration** | First-class — auto-commits, clean diff history |
| **Headless/CI** | Yes — pure terminal, scriptable, no GUI required |
| **Maturity** | 46 k stars, 6.8 M installs, active releases (v0.86.0, 2025-08-09) |
| **Self-improvement** | Aider uses itself to write its own code (88 % of v0.86.0) |
| **Sandboxing** | None built-in — runs linters/tests via shell; trust model |

**Strengths**: Apache-2.0 with no subscription gate. Repo-map context strategy
scales to large codebases. Automatic git commits give a natural audit trail.
Multi-LLM support means teams can switch providers without changing workflow.
The public polyglot leaderboard makes model selection transparent and
reproducible.

**Risks**: No built-in sandboxing — Aider executes shell commands for lint/test
runs, so a hostile or buggy LLM output could trigger unintended side-effects.
Relies on the developer to supply and manage LLM API keys and budget. The web
chat copy/paste mode (for keyless use) is manual and not scriptable.

**Compared to proprietary terminal peers** (e.g., [GitHub Copilot CLI][copilot-cli-analysis]):
Aider is the OSS, bring-your-own-key alternative — lower per-session cost
ceiling, fully auditable, no subscription lock-in, but also no built-in
cross-session memory or cloud sandbox.

## Action Items

- **Evaluate** as the default terminal coding agent for teams that want
  Apache-2.0 tooling and direct control over LLM provider and cost.
- **Run the polyglot benchmark** on the team's preferred model before adopting
  to confirm acceptable pass rates at the target cost point ([leaderboard][aider-leaderboard]).
- **Scope lint/test permissions** explicitly: configure `--test-cmd` and
  `--lint-cmd` to only the commands you trust Aider to run automatically.
- **Pin the model alias** in team dotfiles (`~/.aider.conf.yml`) — provider
  model aliases change across releases (confirmed by main-branch changelog,
  2026-06-16).

## Cross-References

- [github-copilot-cli-analysis.md](github-copilot-cli-analysis.md) — proprietary terminal peer;
  comparison point for subscription vs bring-your-own-key models

## Sources

| Source | Content |
|---|---|
| [aider.chat homepage][aider-home] | Tagline, install count, token throughput, supported models (accessed 2026-06-16) |
| [Aider-AI/aider GitHub repo][aider-gh] | License, star count, release v0.86.0 date, installation, LLM list (accessed 2026-06-16) |
| [Aider releases page][aider-releases] | Latest release v0.86.0, 2025-08-09 (accessed 2026-06-16) |
| [Aider LLM leaderboard][aider-leaderboard] | Polyglot benchmark methodology, top scores, last updated 2025-11-20 (accessed 2026-06-16) |
| [Aider HISTORY][aider-history] | v0.86.0 self-authorship stat (88 %), main-branch Claude 4.x aliases (accessed 2026-06-16) |

[aider-home]: https://aider.chat/
[aider-gh]: https://github.com/Aider-AI/aider
[aider-license]: https://github.com/Aider-AI/aider/blob/main/LICENSE.txt
[aider-releases]: https://github.com/Aider-AI/aider/releases/latest
[aider-leaderboard]: https://aider.chat/docs/leaderboards/
[aider-history]: https://aider.chat/HISTORY.html
[aider-repomap]: https://aider.chat/docs/repomap.html
[copilot-cli-analysis]: github-copilot-cli-analysis.md
