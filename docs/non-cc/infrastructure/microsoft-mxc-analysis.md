---
title: Microsoft MXC (Execution Containers) Analysis
source: https://github.com/microsoft/mxc
purpose: Analysis of Microsoft's MXC, a cross-platform, policy-driven sandbox SDK for running agent-generated code and tools, with a Windows-native process container.
platform_scope: [windows, linux, macos]
created: 2026-11-09
updated: 2026-11-12
validated_links: 2026-11-12
status: assess
---

**Details:** MIT; v1.0.0 GA 2026-10-07, latest v1.0.1 (2026-10-17, unchanged); 3,132★ (re-checked
2026-11-12, up from 3,116★).

## What It Is

MXC is Microsoft's containment layer for AI agents. Its README calls it the "Microsoft eXecution Container (MXC)", "a **sandboxed code execution system** for running untrusted code (model output, plugins, and tools) on Windows, Linux, and macOS". The [Windows Developer blog post][blog] of 2026-10-07 names it "Microsoft Execution Containers (MXC), now generally available". It ships as SDKs (Rust `mxc-sdk`, .NET `Microsoft.Mxc.Sdk`, Node `@microsoft/mxc-sdk`) and an executor, `wxc-exec.exe`, that an agent host embeds; it is not an agent and has no MCP server.

For this corpus its main interest is Windows: Claude Code's own sandbox has no native Windows support (see [CC-sandboxing-analysis.md](../../cc-native/sandboxing/CC-sandboxing-analysis.md)), and MXC is a first-party Windows process sandbox aimed at agents.

## How It Works

**Backends.** One request format, several containment backends ([README][repo]):

| Platform | Default backend | Other backends |
|---|---|---|
| Windows 11 x64 / ARM64 | `processcontainer` (AppContainer-based) | `windows_sandbox`\*, `wslc`, `microvm`\*, `hyperlight`\*, `isolation_session` |
| Linux x64 / ARM64 | `bubblewrap` | `lxc`, `hyperlight` |
| macOS | `seatbelt` | — |

\* experimental. The README says "MicroVM is currently available on Windows x64 only"; the blog's table lists MicroVM for "Windows 11 and Linux, experimental". The two disagree; the README is the more specific source. On Windows the process container's network policy is enforced with WFP filters ([networking docs][mxc-networking]), and each backend has a minimum Windows 11 build ([OS-version support][mxc-os]).

**Policy.** A versioned JSON request whose 1.0.0 contract is "Published, immutable, current stable contract" ([policy 1.0.0][mxc-policy]). It is "a closed JSON object": unknown fields are rejected. It covers the process (command, working directory, environment, timeout), filesystem (read-write, read-only and denied path lists), network (egress and ingress, both defaulting to `"deny"`, plus host loopback), UI (clipboard, display) and lifecycle.

**Modes.** The blog describes three: **Enforcement** ("Run the workload with its production policy"), **Learning** (blocks and records ungranted access, to check the policy grants only what's needed) and **Permissive** ("Observe agent activity without enforcing policy"). The repo's audit mode, `wxc-exec.exe --audit policy.json`, records accesses to help write a policy; the README warns it "turns off all sandbox security for the workload being analyzed. Never use it to run untrusted code."

**Management.** "Intune policy will soon be available to manage MXC process containers used by MXC-integrated agents on Windows 11" (blog; announced, not shipped). Windows 365 support for MXC is GA per the blog.

## Agent Support (announced by Microsoft)

The blog says agents and frameworks "already support MXC, including GitHub Copilot, OpenClaw, OpenAI Codex", Replit, LM Studio and Unsloth AI, and that "Many others will be releasing support for MXC: Anthropic Claude Code", along with Box, Egnyte, Heidi Health, Hermes Agent, Manus, Perplexity, Raycast and Simular. Neither the README nor the docs name any agent. **Claude Code support is a Microsoft announcement only**; re-checked 2026-11-12 against the blog post (unchanged — Claude Code is still listed only among those who "will be releasing support," not among those confirmed already supporting it) and against the full text of Claude Code's own sandboxing documentation, which describes macOS/Linux/WSL2 support and contains no mention of MXC or a native-Windows sandbox; still no Anthropic-side source found. NVIDIA, per the blog, "has integrated OpenShell into MXC", adding its own file, inference, network and credential controls (see [nvidia-openshell-analysis.md](nvidia-openshell-analysis.md)).

## Caveats

- **Telemetry.** For the development `1.1.0-alpha` request contract, official builds send Required diagnostic data (four events: execution start and end, categorized failures, process exits). Per the README these "need no user consent or per-request opt-in, and administrative policy does not block them". The published `0.9.0-alpha` and `1.0.0` contracts keep telemetry optional.
- **Experimental backends.** Windows Sandbox, MicroVM and Hyperlight are marked experimental; the GA claim covers the stable contract and default backends.
- **Containment strength varies by backend.** A process container (AppContainer, Seatbelt, Bubblewrap) is a weaker boundary than a VM; the blog positions MicroVM for "Higher-risk workloads that benefit from a hardware-backed virtualized boundary."

## Adoption Decision

**Assess.** Shipped, MIT, cross-platform, with a deny-by-default policy and a learning mode for writing policies. It matters for Claude Code on Windows if Anthropic ships the support Microsoft announced; until then, Claude Code's documented options on Windows remain WSL2-based. Watch: Anthropic confirmation, Intune management, and whether Required telemetry carries into the next stable contract.

## Cross-References

- [nvidia-openshell-analysis.md](nvidia-openshell-analysis.md): NVIDIA's policy runtime, which the blog says is integrated into MXC.
- [CC-sandboxing-analysis.md](../../cc-native/sandboxing/CC-sandboxing-analysis.md): Claude Code's own sandbox (Seatbelt, bubblewrap; no native Windows).

## Sources

| Source | Content |
|---|---|
| [Windows Developer blog, 2026-10-07][blog] | GA announcement, backend table, Enforcement/Learning/Permissive modes, agent support lists, OpenShell integration, Intune plan, Windows 365 GA |
| [microsoft/mxc README][repo] | Name, backends per platform, experimental flags, audit-mode warning, telemetry; `gh api` (MIT `LICENSE.md`, releases v1.0.0 2026-10-07 / v1.0.1 2026-10-17 — no newer release as of re-check, 3,132★), re-read 2026-11-12 |
| [Containment policy 1.0.0][mxc-policy] | Stable contract status, closed JSON request, network deny defaults |
| [Process-container networking][mxc-networking] | WFP-based network enforcement on Windows |
| [OS-version support][mxc-os] | Minimum Windows 11 builds per backend |
| [Claude Code — Sandboxing][code-sandboxing] | Confirms no native-Windows sandbox and no mention of MXC, re-checked 2026-11-12 |

[blog]: https://blogs.windows.com/windowsdeveloper/2026/10/07/microsoft-execution-containers-policy-driven-containment-for-ai-agents/
[repo]: https://github.com/microsoft/mxc
[mxc-policy]: https://github.com/microsoft/mxc/blob/main/docs/containment-policy/1.0.0/policy.md
[mxc-networking]: https://github.com/microsoft/mxc/blob/main/docs/backends/process-container/networking.md
[mxc-os]: https://github.com/microsoft/mxc/blob/main/docs/backends/process-container/os-version-support.md
[code-sandboxing]: https://code.claude.com/docs/en/sandboxing
