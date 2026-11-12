---
title: Microsoft Skill Recorder Analysis
source: https://github.com/microsoft/skill-recorder
purpose: Analysis of Microsoft's Skill Recorder, a desktop app that turns a recorded (or imported) screen-capture session into a reusable agent Skill or scheduled Automation via the GitHub Copilot CLI.
created: 2026-11-12
updated: 2026-11-12
validated_links: 2026-11-12
status: assess
---

**Details:** MIT; 5,760★/654 forks; created 2026-07-29, last pushed 2026-11-04 (`gh api`,
2026-11-12). Note: the repo's one-line GitHub description says the GitHub **Copilot SDK**; the
README's own body text says the **Copilot CLI** does the reconstruction, and ships with the app —
the README is treated as authoritative per this corpus's convention of preferring body text over
a short description.

## What It Is

Skill Recorder is an Electron desktop app: "Record yourself doing a task once, then turn it into a
skill your AI agent can repeat" (README). It captures a real work session — clicks, app/window
switches, pages visited, an optional recorded terminal's commands and output, and optional spoken
narration — then sends the recording through the **GitHub Copilot CLI** to reconstruct "what you
actually did" as one overall intent plus an ordered list of steps. From an approved reconstruction,
one step generates either a **Skill** (a `SKILL.md` procedure an agent runs on demand) or an
**Automation** (the same procedure on a schedule or trigger). Both prefer the agent's native tools
(e.g. the `gh` CLI, `web_fetch`) over replaying UI clicks, and the README states the result
generalizes from one example — recording one form submission can teach the agent to submit "all of
them."

The generated Skills and Automations are built for **Microsoft's own agent surfaces** — the README
names Microsoft Autopilots such as Scout, Microsoft Copilot Cowork, and Copilot Studio as the
consumers — which is why this entry sits beside, rather than inside,
[microsoft-365-copilot-analysis.md](microsoft-365-copilot-analysis.md): Skill Recorder is the
authoring tool that *produces* skills for that family's surfaces, not a Copilot-in-SharePoint or
Agent 365 feature itself.

## Import path (no live recording required)

Instead of recording, a session can be built from an existing **MP4 or WebM** file (e.g. a
downloaded Teams recording). The bundled Chromium validates the file before import; limits are
512 MiB, 15 minutes, and 3840×2160 (or an equivalent pixel count), one video track and at most one
audio track, mono/stereo audio up to 48 kHz. `Analyze` transcribes audio locally with a bundled
Whisper model (first-use download disclosed) and generalizes from frames, speech, and any typed
details — it "cannot recover hidden clipboard contents or commands that were never visible or
spoken" (README).

## Privacy boundary

The original imported/recorded file is untouched; a local copy and derived artifacts live in the
app's Sessions store, and deleting a session removes only that copy. Choosing a file does not by
itself send it anywhere — **choosing `Analyze` does**: selected frames, transcribed speech, and any
typed details go through the app's "existing privacy-protection pipeline" to GitHub Copilot (a
cloud call). Debug exports carry the same private data as the live session they came from.

## Install

Distributed as a **source release**, not a prebuilt binary: one command (copied from the specific
GitHub release page, not a generic template) downloads a pinned Node.js runtime and builds the
exact release commit locally, producing a "Skill Recorder (Source)" app. Requires a GitHub account
with Copilot access; the Copilot CLI ships with the app. macOS is the primary target; Windows 11
(x64/ARM64) is also supported.

## Adoption Decision

**Assess.** MIT-licensed and genuinely novel in mechanism (reconstruct-then-generalize from a
single demonstrated session, rather than hand-written skill prompts), but entirely tied to GitHub
Copilot as the reconstruction engine and to Microsoft's own Autopilot/Cowork/Copilot Studio
surfaces as the consumer of its output — no Claude Code or other third-party agent integration is
documented. Young project (created 2026-07-29); the memory-use and import-limit figures in its own
README are explicitly self-reported single-platform measurements (Windows ARM64), not independent
benchmarks.

## Cross-References

- [microsoft-365-copilot-analysis.md](microsoft-365-copilot-analysis.md) — the Copilot Studio/Cowork/Scout surfaces Skill Recorder's output targets

## Sources

| Source | Content |
|---|---|
| [microsoft/skill-recorder README][repo] | Capture/import mechanism, privacy boundary, install path, limits |
| [microsoft/skill-recorder][repo] `gh api` metadata + `/license` | MIT, 5,760★/654 forks, created 2026-07-29, pushed 2026-11-04 |

[repo]: https://github.com/microsoft/skill-recorder
