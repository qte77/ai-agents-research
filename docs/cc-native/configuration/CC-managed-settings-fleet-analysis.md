---
title: CC Managed Settings and Fleet Policy
source: https://code.claude.com/docs/en/managed-settings
purpose: How an organization distributes Claude Code policy to a fleet of developer machines and cloud sessions — the four delivery channels, how they rank and combine, Enterprise group configurations, fail-closed startup, managed-only keys, and how to check that a policy is in force.
category: analysis
created: 2026-11-20
updated: 2026-11-20
validated_links: 2026-11-20
status: available
---

## What It Is

Claude Code reads policy from a **managed tier** that sits above user, project and local settings
(precedence in [CC-env-vars-reference.md § Configuration Methods][env-precedence]). This doc covers how that
tier reaches a fleet. What each managed key enforces is documented where the key lives: permission
locks in [CC-permissions-bypass-analysis.md][perm-bypass], managed hooks and the built-in guard in
[CC-mods-function-hooks-analysis.md][mods], managed CLAUDE.md in
[CC-memory-system-analysis.md][memory]. The first-party "decide what to enforce" checklist is on
[Set up Claude Code for your organization][cc-admin-setup]. All facts below are documented, read
2026-11-20.

## Four delivery channels

| Channel | Delivered through | When Claude Code reads it |
|---|---|---|
| Server-managed | claude.ai admin console, or a self-hosted Claude apps gateway | Fetched at startup, polled hourly |
| MDM / OS policy | macOS configuration profile (`com.anthropic.claudecode`) or Windows `HKLM\SOFTWARE\Policies\ClaudeCode` | Startup, then checked every 30 minutes |
| File | `managed-settings.json` plus optional `managed-settings.d/*.json` drop-ins in a system directory (`/etc/claude-code/` on Linux and WSL) | Startup, reloaded when a file changes |
| HKCU registry (Windows, WSL) | `HKCU\SOFTWARE\Policies\ClaudeCode` | Startup, then every 30 minutes; used only when no admin document is present above it and no host-supplied parent settings supply a restrictive key |

Source: [Deploy managed settings][cc-managed]. Anthropic ships starter MDM templates (Jamf, Iru,
Intune, Group Policy) in the [claude-code examples][cc-mdm-examples].

**Reach.** Terminal, IDE extensions, the desktop Code tab and Agent SDK sessions read every channel;
SDK sessions load managed settings even when `settingSources` excludes user and project files.
Sessions in Anthropic-hosted cloud environments can't see a device's MDM profile or file, so their
policy must come from server-managed settings; a self-hosted environment also reads the managed file in
its runner image. Cowork sessions never fetch server-managed settings: on the user's machine they read
the device's MDM policy and managed file, while remote Cowork VMs have no device policy. Claude Tag
sessions don't receive server-managed settings either, but in a self-hosted environment they read the
runner image's file ([Where and when a policy applies][cc-managed-where]).

## Ranking and combining

Rank, highest first: remote (server or gateway), MDM/OS, file, HKCU. The HKCU value is user-writable,
so it doesn't count as an admin source.

- **Default `managedSourcesBehavior: "first-wins"`**: the highest-ranked source that delivers at least
  one policy key wins and the others are ignored, not merged. A short list of keys is still read from
  every admin source ([Keys read from every admin source][cc-managed-every]).
- **`"merge"`** (v2.1.242+): every admin source applies; the higher source wins per key, lists union,
  and locks take the strictest value.
- **Drop-ins** inside the file channel always merge: `managed-settings.json` first, then
  `managed-settings.d/*.json` alphabetically, so teams can own separate files (`10-telemetry.json`,
  `20-security.json`).
- **`policyHelper`**: an executable named by the MDM or file source that computes the policy at
  startup; its output then becomes the only managed settings for the session.

## Server-managed specifics

From [Configure server-managed settings][cc-server-managed]:

- **Plans and roles**: Claude for Teams or Enterprise; Owner or Primary Owner edits; machines need
  network access to `api.anthropic.com`.
- **Group configurations (Enterprise only)**: one configuration per group, ranked; a member of several
  groups gets only the highest-ranked one; an "Everyone else" catch-all covers the rest. Configurations
  don't merge with each other or with the organization-wide one, so each must carry every setting.
  Not yet available with HIPAA enabled. On a Team plan one configuration applies to everyone.
- **Startup and failure**: on a sign-in at startup, Claude Code waits up to five seconds for the fetch.
  If a fetch fails, it falls back to the cached copy from the last successful fetch until that expires,
  then starts without server policy and warns. `forceRemoteSettingsRefresh: true` makes startup fail
  closed: the CLI exits instead of running without a freshly fetched policy.
- **Limits**: `managed-mcp.json` can't be distributed this way (use `allowedMcpServers` /
  `deniedMcpServers`, or `managedMcpServers` from v2.1.259); OS-only keys such as `policyHelper` and
  `wslInheritsWindowsSettings` are not honored from the server.

**Choosing.** Anthropic's own guidance: endpoint-managed settings give stronger guarantees on
MDM-enrolled devices, because the OS protects the file from the user; server-managed settings suit
organizations without MDM and are the only channel that reaches Anthropic-hosted cloud sessions, so
an MDM fleet whose developers also run cloud sessions configures server-managed settings as well.

## Managed-only keys and invalid values

Some keys are read **only** from a managed source; in user or project files they do nothing. Most are
locks that make Claude Code honor only the managed value of an ordinary key, for example
`allowManagedPermissionRulesOnly`, `allowManagedHooksOnly` and `allowManagedMcpServersOnly`. The full
list is the managed-only table on [Deploy managed settings][cc-managed-only] plus the Scope column of
the settings reference. An unreadable value on a single-value restrictive key, such as
`disableAutoMode`, **fails closed** (it reads as the restrictive value until fixed), and a managed file
that isn't valid JSON stops Claude Code from starting.

## Checking that a policy is in force

- `/status` → the `Setting sources` line names the selected managed source (`remote`, `plist`, `HKLM`,
  `file`, `drop-ins`, `HKCU`, `helper`, or a `…, merged` list); `Skipped sources` (v2.1.242+) names the
  ones it found but didn't use.
- `claude doctor` lists dropped entries and, from v2.1.248, a `Managed settings (remote)` line with the
  fetch outcome.

## Fleet scope: what this doesn't give you

Managed settings distribute **policy**, not an inventory. The pages read for this doc describe no
org-level registry of the agents or subagents a fleet runs. Organizations see agent activity through
telemetry instead: `agent_id` on events and the `agent.name` attribution on cost metrics (see
[CC-monitoring-telemetry-analysis.md § Cost attribution][telemetry-cost]). `claude agents` opens
[agent view][cc-agent-view] (research preview), which manages background sessions on one machine;
admins can turn it off with `disableAgentView`. Agent lifecycle beyond a session lives elsewhere:
agents deployed through the Claude Managed Agents API (`/v1/agents`,
[CC-cowork-plugins-enterprise-analysis.md][cowork-enterprise]), subagents shipped and versioned
inside plugins from managed marketplaces ([CC-mods-function-hooks-analysis.md][mods]), and agent
identity in [agent-identity-auth-landscape.md][agent-identity]. For how Claude Code compares with the enterprise agent registries (AWS, Google,
Microsoft, Salesforce, MCP Registry), see
[agentic-enterprise-os-landscape.md § Agent registries compared][registries].

## Cross-References

- [CC-env-vars-reference.md][env-precedence] — settings precedence and env vars that can be set in the managed `env` block
- [CC-permissions-bypass-analysis.md][perm-bypass] — `disableBypassPermissionsMode`, `disableAutoMode` and other permission locks
- [CC-mods-function-hooks-analysis.md][mods] — managed hooks, marketplaces and the built-in guard
- [CC-monitoring-telemetry-analysis.md][telemetry-cost] — per-user and per-agent cost attribution
- [agentic-enterprise-os-landscape.md § Agent registries compared][registries] — agent registries across vendors

## Sources

| Source | Content |
|---|---|
| [Deploy managed settings][cc-managed] | Delivery channels, ranking, `managedSourcesBehavior`, drop-ins, `policyHelper`, `/status` and `claude doctor`, fail-closed keys, managed-only keys (read 2026-11-20) |
| [Configure server-managed settings][cc-server-managed] | Plans and roles, group configurations, fetch and cache behavior, `forceRemoteSettingsRefresh`, limits (read 2026-11-20) |
| [Set up Claude Code for your organization][cc-admin-setup] | Admin checklist: what to enforce, usage visibility, verification (read 2026-11-20) |
| [Agent view][cc-agent-view] | `claude agents`, research preview, local background sessions, `disableAgentView` (read 2026-11-20) |
| [anthropics/claude-code MDM examples][cc-mdm-examples] | Starter templates for Jamf, Iru, Intune and Group Policy |

[cc-managed]: https://code.claude.com/docs/en/managed-settings
[cc-managed-where]: https://code.claude.com/docs/en/managed-settings#where-and-when-a-policy-applies
[cc-managed-every]: https://code.claude.com/docs/en/managed-settings#keys-read-from-every-admin-source
[cc-managed-only]: https://code.claude.com/docs/en/managed-settings#keys-only-a-managed-source-can-set
[cc-server-managed]: https://code.claude.com/docs/en/server-managed-settings
[cc-admin-setup]: https://code.claude.com/docs/en/admin-setup
[cc-agent-view]: https://code.claude.com/docs/en/agent-view
[cowork-enterprise]: ../plugins-ecosystem/CC-cowork-plugins-enterprise-analysis.md
[agent-identity]: ../../sdlc-lcm/agent-identity-auth-landscape.md
[cc-mdm-examples]: https://github.com/anthropics/claude-code/tree/main/examples/mdm
[env-precedence]: CC-env-vars-reference.md#configuration-methods
[perm-bypass]: ../sandboxing/CC-permissions-bypass-analysis.md
[mods]: ../plugins-ecosystem/CC-mods-function-hooks-analysis.md
[memory]: ../context-memory/CC-memory-system-analysis.md
[telemetry-cost]: CC-monitoring-telemetry-analysis.md#cost-attribution
[registries]: ../../non-cc/frameworks/agentic-enterprise-os-landscape.md#agent-registries-compared
