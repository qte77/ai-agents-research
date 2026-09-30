---
title: OpenResearch Analysis
source: https://github.com/alphaXiv/OpenResearch
purpose: Evaluate OpenResearch as a local-first, git-native workspace that turns coding agents into autonomous research/experiment agents.
created: 2026-09-30
updated: 2026-09-30
validated_links: 2026-09-30
status: assess
---

## What It Is

[OpenResearch][openresearch] is a **local-first workspace for research agents and autoresearch**
from alphaXiv — the paper-discovery service [Feynman][feynman-analysis] also uses for search — but
OpenResearch itself is a separate desktop app and CLI, not a shared backend with Feynman; the
[about page][openresearch-about] frames alphaXiv only as "a prior project by the same team." It
turns Claude Code, Codex, OpenCode, Cursor, or Google Antigravity into research agents that "review
literature, develop hypotheses, run experiments, and produce research artifacts," keeping every
project, conversation, experiment, run, log, and artifact on the user's own machine ([README][openresearch]).

## How It Works

### Architecture

Rust-core desktop app (Tauri-style; ~74% Rust by byte count) with a TypeScript/React dashboard,
plus a `orx` CLI ([`gh api` languages][openresearch-langs], 2026-09-30). `orx up` starts a local
service bound to `127.0.0.1:4791` with a local SQLite store; creating a project or launching a run
does not publish anything, and an `openresearch.sh` account is required only for "service-owned
capabilities such as organizations and managed compute" ([README][openresearch]).

### Agent integration

`orx install-skills` installs the OpenResearch skill into supported coding agents. Core CLI
surface: `orx projects`, `orx project view`, `orx runs`, `orx logs`, `orx exp run`, `orx discover
keyword <query>`, `orx paper <arxiv-id-or-doi>` — the last two are the visible alphaXiv link,
paper discovery and lookup by arXiv id or DOI ([README][openresearch]).

### Reproducibility and evidence

Every experiment runs inside a **git-native experiment tree**: "every run receives an immutable
archive of its recorded commit," and OpenResearch explicitly frames this as "Reproducible
experiments" — the *code* a run executed is commit-pinned and re-derivable. The agent's own
decisions inside that loop (what to try next, how to read the evidence) remain model-driven and
are not pinned to a model/version. "Evidence in context" keeps logs, diffs, files, results and
artifacts tied to the run that produced them ([README][openresearch]).

### Autoresearch

OpenResearch can run the propose → change code → launch experiment → inspect evidence → decide
loop autonomously, with multiple agents exploring different directions in parallel while "the
experiment tree preserves their lineage" ([README][openresearch]).

### Run anywhere

The same committed source snapshot runs locally, over SSH, or on Slurm, Kubernetes, Ray, Hugging
Face Jobs, Modal, Tinker, or managed OpenResearch compute — "publishing the repository is not
required." Running against a remote host (`orx up --remote user@host`) has a stated security
caveat: "the remote service binds to loopback and has no application-level authentication, so
other users on that host can reach it" ([README][openresearch]).

### Platforms

- **macOS 11+** — signed with a Developer ID and notarized by Apple; the primary download path
- **Windows** — beta, requires [Git for Windows][openresearch-windows-docs]; the installer isn't
  code-signed yet, so Windows shows an unsigned-app warning
- **Linux** — AppImage for x86_64 or aarch64, needs glibc 2.35+ ([Linux docs][openresearch-linux-docs]);
  `linux/OpenResearch.desktop` in the repo is Linux launcher packaging (a `.desktop` entry), not a
  separate platform feature
- **CLI-only install** (`curl -LsSf https://openresearch.sh/install.sh | sh`) is unsigned — device-
  management policy on a work Mac may block it, in which case the signed/notarized app's own
  "Install the `orx` command" menu item is the documented workaround

Telemetry is opt-out on official release builds (installation-ID-scoped events only, no code/
prompts/paths/tokens/emails); `orx telemetry off` disables it, and source/dev builds send nothing
([README][openresearch]).

## Rubric

Scored 2026-09-30 against the [agent substrate rubric][rubric].

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| partial [README][openresearch] ("multiple agents can explore different directions in parallel while the experiment tree preserves their lineage" — concurrent multi-agent access to one experiment tree, but single-user by default, not a multi-user shared store) | yes [README][openresearch] ("run locally, on your own infrastructure, or with managed OpenResearch compute" across SSH/Slurm/Kubernetes/Ray/HF Jobs/Modal/Tinker) | partial [README][openresearch] (runs are commit-pinned — "immutable archive of its recorded commit" — but the agent's own propose/decide steps are model-driven with no pinned model/version documented) | yes [README][openresearch] (choice of agent — Claude Code/Codex/OpenCode/Cursor/Antigravity — and choice of compute backend, both swappable per session) | yes [README][openresearch] (git-native experiment tree; immutable per-run commit archives) | yes [README][openresearch] ("Evidence in context": logs, diffs, files, results and artifacts kept tied to the run that produced them) |

## Adoption Decision

| Dimension | Assessment |
|---|---|
| **Use case** | Turning an existing coding agent into an autonomous research/experiment loop, with reproducible, git-native experiment lineage |
| **Runtime** | Local Rust/Tauri desktop app + `orx` CLI; local SQLite store by default |
| **Compute** | Local, SSH, Slurm, Kubernetes, Ray, Hugging Face Jobs, Modal, Tinker, or managed OpenResearch compute |
| **Maturity** | Active: 6,259★/398 forks, v0.2.14, pushed 2026-09-30 (`gh api`, 2026-09-30); GitHub Trending #1 Repository of the Day |
| **License** | MIT (LICENSE file confirmed, `gh api` 2026-09-30) |

**Strengths**: local-by-default with no forced cloud dependency; git-native experiment tree gives a
real, inspectable reproducibility story for the *code* half of a run; agent-agnostic (works with
five different coding-agent harnesses) and compute-agnostic (eight execution targets plus managed
compute); active development and adoption.

**Risks**: `orx up --remote` has no application-level authentication — its own README states other
users on the remote host can reach the bound service; the Windows and CLI-install paths are
unsigned as of this scoring; the autonomous "autoresearch" loop's own decisions are model-driven
and not reproducible in the way the underlying code commits are.

## Cross-References

- [feynman-analysis.md](feynman-analysis.md) — Companion AI's research agent; shares alphaXiv as
  its paper-discovery backend, but is a separate product from OpenResearch
- [orcareplay-analysis.md](../reference/orcareplay-analysis.md) — another git/commit-oriented
  reproducibility approach for agent runs, applied to coding-agent replay rather than research
  experiments

## Sources

| Source | Content |
|---|---|
| [OpenResearch repo][openresearch] | README: architecture, platforms, run-anywhere compute targets, security note, telemetry |
| [OpenResearch about page][openresearch-about] | Positioning vs. alphaXiv (prior project, not a shared backend) |
| [`gh api` languages][openresearch-langs] | Language breakdown (Rust core, TypeScript/JS UI) |
| [Linux docs][openresearch-linux-docs] | glibc 2.35+ requirement |
| [Windows docs][openresearch-windows-docs] | Git for Windows prerequisite |

[openresearch]: https://github.com/alphaXiv/OpenResearch
[openresearch-about]: https://openresearch.sh/about
[openresearch-langs]: https://api.github.com/repos/alphaXiv/OpenResearch/languages
[openresearch-linux-docs]: https://github.com/alphaXiv/OpenResearch/blob/main/docs/linux.md
[openresearch-windows-docs]: https://github.com/alphaXiv/OpenResearch/blob/main/docs/windows.md
[feynman-analysis]: feynman-analysis.md
[rubric]: ../../sdlc-lcm/agent-substrate-rubric.md
