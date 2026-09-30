# Topic Hub: Long-Running

Hands-off, offloaded, multi-hour or scheduled agent work: durability, resume, remote execution across
the corpus. Pointers only; see [the hub index](README.md).

| Doc / section | What it covers | Bucket |
|---|---|---|
| [CC-cloud-sessions-analysis.md](../cc-native/ci-remote/CC-cloud-sessions-analysis.md) | Claude Code on the Web: cloud VMs, self-hosted runners, teleport | cc-native |
| [CC-web-scheduled-tasks-analysis.md](../cc-native/ci-remote/CC-web-scheduled-tasks-analysis.md) | Cloud-native scheduled tasks for recurring autonomous work | cc-native |
| [CC-session-keepalive-analysis.md](../cc-native/sessions/CC-session-keepalive-analysis.md) | Keeping CC sessions alive locally, in containers, in Codespaces | cc-native |
| [CC-cowork-skills-api-workflows.md § Long-Running Tasks Without Keep-Alive](../cc-native/plugins-ecosystem/CC-cowork-skills-api-workflows.md#long-running-tasks-without-keep-alive) | Durable scheduling via GitHub Actions as a keep-alive alternative | cc-native |
| [orcareplay-analysis.md](../non-cc/reference/orcareplay-analysis.md) | Byte-for-byte deterministic replay and model-fork of a recorded long-running agent run — direct evidence for reproducible/traceable offloaded work | non-cc |
| [agent-frameworks-infrastructure-landscape.md §1](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#1-multi-agent-orchestration-frameworks) | google/ax `ax suspend` / `ax resume` (checkpoint and resume an idle agent); Paperclip's heartbeat-scheduled 24/7 agents with state persisting across reboots | non-cc |
| [software-factory-landscape.md](../sdlc-lcm/software-factory-landscape.md) | Cloudflare's nightly, GHA-hosted issue-triage pipeline (reproduce/diagnose/verify/fix) as a hands-off long-running agent workflow | sdlc-lcm |

Related hubs: [harness.md](harness.md).
