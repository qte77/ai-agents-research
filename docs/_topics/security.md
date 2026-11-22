# Topic Hub: Security

Agent security: threat models and frameworks, prompt injection, guardrails, sandboxes and permissions,
vulnerability discovery and offensive agents. Pointers only; see [the hub index](README.md).

## Threat models and frameworks

| Doc / section | What it covers | Bucket |
|---|---|---|
| [ai-security-governance-analysis.md](../sdlc-lcm/ai-security-governance-analysis.md) | OWASP MAESTRO, MITRE ATLAS, NIST AI RMF, ISO/IEC 42001 and 23894 | sdlc-lcm |
| [mas-security-framework.md](../sdlc-lcm/mas-security-framework.md) | MAESTRO layers with threats, mitigations and a security checklist | sdlc-lcm |
| [agentic-ai-vulnerability-landscape.md § 1. Scoring & classification standards](../sdlc-lcm/agentic-ai-vulnerability-landscape.md#1-scoring--classification-standards) | OWASP AIVSS, MITRE ATLAS as a knowledge base, MITRE AI incident sharing | sdlc-lcm |

## Attacks and defenses

| Doc / section | What it covers | Bucket |
|---|---|---|
| [agentic-ai-vulnerability-landscape.md § Prompt injection: attacks and defenses](../sdlc-lcm/agentic-ai-vulnerability-landscape.md#prompt-injection-attacks-and-defenses) | Attack taxonomy, defenses, benchmarks, Claude Code's documented surface | sdlc-lcm |
| [agentic-ai-vulnerability-landscape.md § 6. Novel attack & defense research](../sdlc-lcm/agentic-ai-vulnerability-landscape.md#6-novel-attack--defense-research) | Guardrail DoS, defensive misdirection, ContextLeak, Mind Viruses | sdlc-lcm |
| [ai-security-governance-analysis.md § MCP Ecosystem Security](../sdlc-lcm/ai-security-governance-analysis.md#mcp-ecosystem-security) | MCP threats mapped to MAESTRO and ATLAS, with mitigations | sdlc-lcm |
| [browser-agents-landscape.md § Safety: prompt injection from web content](../non-cc/agents/browser-agents-landscape.md#safety-prompt-injection-from-web-content) | Prompt injection from web content for browser agents | non-cc |
| [computer-use-agents-landscape.md § Safety](../non-cc/agents/computer-use-agents-landscape.md#safety) | Computer-use safety guidance | non-cc |
| [detokenization-leaks-analysis.md](../sdlc-lcm/detokenization-leaks-analysis.md) | Cache-timing side channel that reconstructs local LLM output | sdlc-lcm |

## Guardrails and permissions

| Doc / section | What it covers | Bucket |
|---|---|---|
| [agentic-ai-vulnerability-landscape.md § Guardrail layers: a comparison](../sdlc-lcm/agentic-ai-vulnerability-landscape.md#guardrail-layers-a-comparison) | Guardrail layers vs Claude Code's own, auto-mode error rates, adaptive-attack gap, approval fatigue | sdlc-lcm |
| [agent-frameworks-infrastructure-landscape.md § Guardrails / policy](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#guardrails--policy) | Guardrail libraries (Guardrails AI, NeMo Guardrails and others) | non-cc |
| [CC-permissions-bypass-analysis.md § Auto Mode: Availability, Classifier and Defaults (read 2026-11-18)](../cc-native/sandboxing/CC-permissions-bypass-analysis.md#auto-mode-availability-classifier-and-defaults-read-2026-11-18) | Auto mode: availability, classifier, fallback thresholds, admin controls | cc-native |
| [CC-managed-settings-fleet-analysis.md § Managed-only keys and invalid values](../cc-native/configuration/CC-managed-settings-fleet-analysis.md#managed-only-keys-and-invalid-values) | Locks only a managed source can set; restrictive keys that fail closed | cc-native |
| [agentic-database-access-landscape.md § Write safety](../non-cc/infrastructure/agentic-database-access-landscape.md#write-safety) | Read-only roles, branching, incident evidence for agent database writes | non-cc |
| [agent-probabilistic-verification-analysis.md](../sdlc-lcm/agent-probabilistic-verification-analysis.md) | Datalog runtime verification with probabilistic bounds on policy violation | sdlc-lcm |
| [sovereign-execution-brokers-analysis.md](../sdlc-lcm/sovereign-execution-brokers-analysis.md) | Certificate-bound authority before an agent can change production infrastructure | sdlc-lcm |
| [ledger-state-tool-calling-analysis.md](../sdlc-lcm/ledger-state-tool-calling-analysis.md) | Ledger-state tracking and pre-execution policy gating for tool calls | sdlc-lcm |

## Sandboxes

| Doc / section | What it covers | Bucket |
|---|---|---|
| [CC-sandboxing-analysis.md § Security Model](../cc-native/sandboxing/CC-sandboxing-analysis.md#security-model) | What Claude Code's sandbox protects against, and its limits | cc-native |
| [CC-sandbox-platforms-landscape.md § Platform Comparison](../cc-native/sandboxing/CC-sandbox-platforms-landscape.md#platform-comparison) | Built-in sandbox vs OpenSandbox, E2B, Sprites.dev, Maritime, Daytona | cc-native |
| [nvidia-openshell-analysis.md](../non-cc/infrastructure/nvidia-openshell-analysis.md) | NVIDIA OpenShell: kernel-enforced policy runtime for agent fleets | non-cc |
| [microsoft-mxc-analysis.md](../non-cc/infrastructure/microsoft-mxc-analysis.md) | Microsoft MXC: policy-driven sandbox SDK for agent-generated code | non-cc |
| [CC-sandbox-bwrap-host-quirks.md](../cc-native/sandboxing/CC-sandbox-bwrap-host-quirks.md) | bwrap friction on Linux: dotfile leakage, AppArmor user-namespace prerequisites | cc-native |
| [CC-sandbox-codespaces-friction.md](../cc-native/sandboxing/CC-sandbox-codespaces-friction.md) | Sandbox friction in Codespaces and devcontainers, with mitigations | cc-native |

## Vulnerability discovery and offensive agents

| Doc / section | What it covers | Bucket |
|---|---|---|
| [agentic-ai-vulnerability-landscape.md § 2. Vendor discovery & remediation systems](../sdlc-lcm/agentic-ai-vulnerability-landscape.md#2-vendor-discovery--remediation-systems) | MDASH, Vuln.AI, Uber ADR, SkillSpector | sdlc-lcm |
| [agentic-ai-vulnerability-landscape.md § 7. Offensive-security agents (authorized testing)](../sdlc-lcm/agentic-ai-vulnerability-landscape.md#7-offensive-security-agents-authorized-testing) | ARTEX, Claude-BugHunter, cross-tool observations | sdlc-lcm |
| [CC-community-skills-landscape.md § cloudflare/security-audit-skill](../cc-community/CC-community-skills-landscape.md#cloudflaresecurity-audit-skill) | Community security-audit skill | cc-community |
| [rea-analysis.md](../non-cc/infrastructure/rea-analysis.md) | REA: reverse-engineering tools for native binaries, JS/Electron apps, .NET assemblies and websites | non-cc |

Related hubs: [harness.md](harness.md), [management.md](management.md), [agentic-web.md](agentic-web.md), [evals-benchmarks.md](evals-benchmarks.md), [plugins.md](plugins.md).
