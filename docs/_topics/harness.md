# Topic Hub: Harness

The loop around the model: orchestration, tools, sandboxes, self-improving harnesses across the corpus.
Pointers only; see [the hub index](README.md).

| Doc / section | What it covers | Bucket |
|---|---|---|
| [CC-agentic-harness-patterns-analysis.md](../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md) | 12-pattern taxonomy extracted from the CC source leak | cc-native |
| [CC-dynamic-workflows-analysis.md](../cc-native/agents-skills/CC-dynamic-workflows-analysis.md) | Dynamic workflow orchestration tool, ultracode effort setting | cc-native |
| [CC-ralph-enhancement-research.md](../cc-native/agents-skills/CC-ralph-enhancement-research.md) | Autonomous headless CC development loop (Ralph pattern) | cc-native |
| [CC-agent-teams-orchestration.md](../cc-native/agents-skills/CC-agent-teams-orchestration.md) | Agent Teams for parallel review, implementation, debugging | cc-native |
| [CC-recursive-spawning-patterns.md](../cc-native/agents-skills/CC-recursive-spawning-patterns.md) | Recursive `claude -p` invocation and spawning trade-offs | cc-native |
| [CC-cross-session-messaging-analysis.md](../cc-native/agents-skills/CC-cross-session-messaging-analysis.md) | First-party cross-session messaging between independent sessions | cc-native |
| [CC-output-verification-analysis.md](../cc-native/agents-skills/CC-output-verification-analysis.md) | Verifying agentic outputs via hooks, schemas, headless asserts | cc-native |
| [CC-cli-anything-analysis.md](../cc-native/agents-skills/CC-cli-anything-analysis.md) | Generating agent-native CLIs from existing software | cc-native |
| [CC-harnessrouter-analysis.md](../cc-community/CC-harnessrouter-analysis.md) | Unified multi-harness API (Codex, Claude Code, Hermes, DSH, Pi) via the Unified Harness Protocol | cc-community |
| [agent-frameworks-infrastructure-landscape.md §1](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#1-multi-agent-orchestration-frameworks) | Orchestration/harness-builder tools: Archon (deterministic YAML workflow harness), Paperclip (agent-team org-chart orchestration), google/ax (Kubernetes-style declarative agent runtime), OperatingSystem-1 (`mcp-git-coord` multi-agent git coordination), DeepSeek Harness (`dsh`, Cordis-plugin architecture + agent-written decision-record practice, cross-ref to [deepseek-harness-analysis.md](../non-cc/coding-agents/deepseek-harness-analysis.md)) | non-cc |
| [agent-frameworks-infrastructure-landscape.md §1 (Runtype)](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#1-multi-agent-orchestration-frameworks) | `hermes-runtype-otel`: per-turn OpenTelemetry traces (model and tool spans) exported from Hermes to Runtype | non-cc |
| [nvidia-openshell-analysis.md](../non-cc/infrastructure/nvidia-openshell-analysis.md) | Kernel-enforced, formally-verified policy runtime for agent fleets | non-cc |
| [orcareplay-analysis.md](../non-cc/reference/orcareplay-analysis.md) | Record/replay/fork debugger for coding-agent runs; deterministic offline replay | non-cc |
| [weco-aide-recursive-self-improvement-analysis.md](../non-cc/reference/weco-aide-recursive-self-improvement-analysis.md) | Self-improving-harness comparison: AIDE², RRSI (git-worktree versioned harness search), ROFT (retrospection fine-tuning, no harness versioning); plus FineEnvs (RL training one model across unmodified OpenCode/Claude Code/Codex/Mini-SWE-Agent harnesses via OpenEnv+Harbor+TRL, rubric-scored) and agentic meta-reasoning (arXiv 2609.38147, inference-time controller harness, paper only) | non-cc |
| [system-1-decision-models-landscape.md](../non-cc/reference/system-1-decision-models-landscape.md) | System-1 decision models (Jev alternatives) used as in-loop guardrail/routing components: Laya, kev, CLM/CLM-8B, GLiNER2.5-Decide, RuVector, JevK5, SemIf, plus the JEV-as-a-Judge (CMU) paper; rubric-scored | non-cc |
| [CC-community-tooling-landscape.md § abide](../cc-community/CC-community-tooling-landscape.md#abide-coldteadotai) | abide: per-edit/turn AGENTS.md rule enforcement via a Jev decision-model question per rule, across Claude Code/Codex/OpenCode | cc-community |
| [openresearch-analysis.md](../non-cc/agents/openresearch-analysis.md) | OpenResearch (alphaXiv): local-first, git-native workspace turning coding agents (Claude Code, Codex, OpenCode, Cursor, Antigravity) into autonomous research/experiment agents; runs anywhere (local/SSH/Slurm/Kubernetes/Ray/HF Jobs/Modal/Tinker) | non-cc |
| [agent-frameworks-infrastructure-landscape.md §2 (Intent-Router)](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#2-llm-orchestration--routing) | Intent-Router: intent-compiler skill that converges a vague request into a typed, evidence-backed IntentSpec before handoff to a router/agent/workflow — the layer upstream of Jev/Laya-style typed decisions | non-cc |
| [CC-community-tooling-landscape.md § human-review](../cc-community/CC-community-tooling-landscape.md#human-review-petergyang) | human-review: visual HTML/Markdown review skill batching Google-Doc-style comments/edits back to the waiting agent — a concrete tool for the ACE-FCA human-review gate | cc-community |
| [agentic-engineering-disciplines-landscape.md §1](../sdlc-lcm/agentic-engineering-disciplines-landscape.md) | Graph-engineering ladder rung (wiring loop-shaped agents into a topology) + Harness-engineering Verification-axiom evidence: Specula (agentic TLA+ trace/invariant verifier, 249 bugs/48 projects) and Bend 2 (proof-gated compiler, rejects an edit without a machine-checked correctness proof) | sdlc-lcm |

Related hubs: [skills.md](skills.md), [plugins.md](plugins.md), [long-running.md](long-running.md).
