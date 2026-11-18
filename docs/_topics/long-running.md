# Topic Hub: Long-Running

Hands-off, offloaded, multi-hour or scheduled agent work: durability, resume, remote execution across
the corpus. Pointers only; see [the hub index](README.md).

| Doc / section | What it covers | Bucket |
|---|---|---|
| [CC-cloud-sessions-analysis.md](../cc-native/ci-remote/CC-cloud-sessions-analysis.md) | Claude Code on the Web: cloud VMs, self-hosted runners, teleport | cc-native |
| [CC-web-scheduled-tasks-analysis.md](../cc-native/ci-remote/CC-web-scheduled-tasks-analysis.md) | Cloud scheduled tasks (formerly routines): schedule, API and GitHub triggers; permission posture in unattended runs | cc-native |
| [workflow-frameworks-landscape.md § Checkpoint and resume matrix](../non-cc/frameworks/workflow-frameworks-landscape.md#checkpoint-and-resume-matrix) | What a resume restores across Claude Code, Codex, Gemini CLI, OpenCode and durable-execution engines (Temporal, DBOS, Restate, Inngest) | non-cc |
| [workflow-frameworks-landscape.md § Watchdog and liveness design](../non-cc/frameworks/workflow-frameworks-landscape.md#watchdog-and-liveness-design) | Heartbeats, turn and budget caps, stuck-on-prompt runs, green-but-idle detection; long-run failure evidence from 2026 papers | non-cc |
| [CC-session-keepalive-analysis.md](../cc-native/sessions/CC-session-keepalive-analysis.md) | Keeping CC sessions alive locally, in containers, in Codespaces | cc-native |
| [CC-goal-analysis.md](../cc-native/sessions/CC-goal-analysis.md) | `/goal`: keep a session working until a completion condition holds; one of three documented keep-running mechanisms with `/loop` and Stop hooks | cc-native |
| [goal-loops-landscape.md](../non-cc/coding-agents/goal-loops-landscape.md) | Goal loops across coding agents: who judges completion, bounds, and Stop-style hooks in Codex, Antigravity, Kiro, Copilot, Cursor, VS Code, Devin, Amp | non-cc |
| [CC-cowork-skills-api-workflows.md § Long-Running Tasks Without Keep-Alive](../cc-native/plugins-ecosystem/CC-cowork-skills-api-workflows.md#long-running-tasks-without-keep-alive) | Durable scheduling via GitHub Actions as a keep-alive alternative | cc-native |
| [orcareplay-analysis.md](../non-cc/reference/orcareplay-analysis.md) | Byte-for-byte deterministic replay and model-fork of a recorded long-running agent run — direct evidence for reproducible/traceable offloaded work | non-cc |
| [agent-frameworks-infrastructure-landscape.md §1](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#1-multi-agent-orchestration-frameworks) | google/ax `ax suspend` / `ax resume` (checkpoint and resume an idle agent); Paperclip's heartbeat-scheduled 24/7 agents with state persisting across reboots | non-cc |
| [software-factory-landscape.md](../sdlc-lcm/software-factory-landscape.md) | Cloudflare's nightly, GHA-hosted issue-triage pipeline (reproduce/diagnose/verify/fix) as a hands-off long-running agent workflow | sdlc-lcm |
| [CC-claude-science-analysis.md](../cc-native/plugins-ecosystem/CC-claude-science-analysis.md) | Claude Science: remote jobs on SSH/Slurm hosts or Modal GPUs; sessions pause and resume at usage limits | cc-native |
| [CC-remote-access-landscape.md](../cc-native/ci-remote/CC-remote-access-landscape.md) | Monitoring and steering long-running CC sessions from phone or web (Remote Control, Happy Coder, Omnara, CloudCLI, Emdash, DIY tmux + Tailscale incl. Tailnet Preview) | cc-native |
| [CC-web-auth-setup-analysis.md § Terms That Apply to Scripted Runs](../cc-native/ci-remote/CC-web-auth-setup-analysis.md#terms-that-apply-to-scripted-runs) | Sign-in, billing and terms for unattended `claude -p`, Agent SDK and scheduled runs, with Codex, Gemini CLI, Copilot CLI, Cursor CLI and opencode compared | cc-native |

Related hubs: [harness.md](harness.md).
