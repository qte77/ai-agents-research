---
title: Claude Code Sandboxing and Security Analysis
purpose: Analysis of CC sandboxing mechanics, configuration options, security model, and sandbox configuration options.
source: https://code.claude.com/docs/en/sandboxing
created: 2026-03-07
updated: 2026-11-26
validated_links_on: 2026-09-23
status: research
---

## Summary

Claude Code sandboxing uses OS-level primitives to enforce filesystem and network
isolation on bash commands ([source][cc-sandboxing]). This replaces approval
fatigue with automated enforcement — in auto-allow mode, commands that stay within
sandbox boundaries run without prompts (auto-allow needs
`sandbox.autoAllowBashIfSandboxed: true`; see "Changes in v2.1.321–325").

**Both layers required**: Without network isolation, a compromised agent could
exfiltrate files (e.g., SSH keys). Without filesystem isolation, it could
backdoor system resources to gain network access ([source][cc-security]).

## Platform Support

| Platform | Mechanism | Setup |
| -------- | --------- | ----- |
| macOS | Seatbelt (built-in) | Works out of the box |
| Linux/WSL2 | bubblewrap + socat | `make setup_sandbox` or `sudo apt-get install bubblewrap socat` |
| WSL1 | Not supported | bubblewrap requires WSL2 kernel features |
| Windows | Not supported | not supported: on native Windows Claude Code runs commands unsandboxed, and the sandbox needs a WSL2 distribution ([source][cc-sandboxing], checked 2026-11-26). Microsoft lists Claude Code among agents that "will be releasing support" for its MXC sandbox (announcement only, unconfirmed by Anthropic): [microsoft-mxc-analysis.md](../../non-cc/infrastructure/microsoft-mxc-analysis.md) |

([source][cc-sandboxing])

## Example Configuration

From `.claude/settings.json` ([source][cc-sandbox-settings]):

```json
"sandbox": {
  "enabled": true,
  "autoAllowBashIfSandboxed": true,
  "allowUnsandboxedCommands": false,
  "enableWeakerNestedSandbox": false,
  "network": {
    "allowLocalBinding": true,
    "allowedDomains": ["api.github.com"]
  },
  "filesystem": {
    "allowWrite": ["/tmp/claude-1000", ".git"]
  }
}
```

**Key choices:**

- [x] Sandbox enabled with auto-allow (`sandbox.autoAllowBashIfSandboxed: true`, no longer the default)
- [x] Unsandboxed escape hatch disabled (`allowUnsandboxedCommands: false`)
- [x] Weaker nested sandbox disabled
- [x] Network restricted to `api.github.com` only
- [x] Filesystem writes restricted to `/tmp/claude-1000` and `.git`
- [ ] `raw.githubusercontent.com` not in `allowedHosts` — needed if fetching
  raw GitHub content
- [ ] No `allowedDomains` for PyPI/npm — package install commands must run
  outside sandbox or with `excludedCommands`

Setup on Linux/WSL2 ([source][cc-sandboxing]):

```bash
sudo apt-get install bubblewrap socat
```

Or via a Makefile recipe if your project defines one. Not typically bundled with
the default dev setup — must be run separately.

## Configuration Reference

> **Note**: This section reflects the doc's original 2026-03 snapshot. Several
> additive sandbox settings have shipped since and are not yet covered here,
> including `sandbox.filesystem.disabled` (v2.1.216+),
> `sandbox.credentials.files`/`envVars` (v2.1.187+), `envVars` `mode: mask` plus
> `sandbox.network.tlsTerminate` (v2.1.199+), per-session host-approval
> persistence (v2.1.191+), a plan-mode ask-rule behavior change (v2.1.212+), and
> `allowAppleEvents`, `allowManagedReadPathsOnly`, `network.deniedDomains`,
> `filesystem.allowRead` ([source][cc-sandboxing]).

### Core Settings

| Key | Description | Default |
| --- | ----------- | ------- |
| `sandbox.enabled` | Enable bash sandboxing | `false` |
| `sandbox.autoAllowBashIfSandboxed` | Auto-approve sandboxed bash commands | `false` (CHANGELOG files the change under v2.1.325; the settings reference says "Before v2.1.324, the default was `true`") |
| `sandbox.excludedCommands` | Commands that bypass sandbox entirely | — |
| `sandbox.allowUnsandboxedCommands` | Allow `dangerouslyDisableSandbox` escape hatch | `true` |

([source][cc-sandbox-settings])

### Filesystem

| Key | Description |
| --- | ----------- |
| `sandbox.filesystem.allowWrite` | Additional writable paths |
| `sandbox.filesystem.denyWrite` | Paths blocked from writing |
| `sandbox.filesystem.denyRead` | Paths blocked from reading |

**Defaults**: Write access to the working directory, directories added with `--add-dir` or `permissions.additionalDirectories`, and the per-user temp directory that `$TMPDIR` points to. Reads: access to the entire computer except certain denied directories; this default still allows reading credential files. With `permissions.blockReadsOutsideWorkingDirectories` on, sandboxed commands also lose read access outside the working directory ([source][cc-sandboxing], checked 2026-11-26).

### Network

| Key | Description |
| --- | ----------- |
| `sandbox.network.allowedDomains` | Domains allowed for outbound traffic (supports wildcards) |
| `sandbox.network.allowManagedDomainsOnly` | Only allow managed domains; block others silently |
| `sandbox.network.allowUnixSockets` | Specific Unix socket paths to allow |
| `sandbox.network.allowAllUnixSockets` | Allow all Unix socket connections |
| `sandbox.network.allowLocalBinding` | Allow binding to localhost ports (macOS only) |
| `sandbox.network.httpProxyPort` | HTTP proxy port |
| `sandbox.network.socksProxyPort` | SOCKS5 proxy port |

([source][cc-sandbox-settings])

### Security-Reducing Options

| Key | Description | Default |
| --- | ----------- | ------- |
| `enableWeakerNestedSandbox` | Weaker sandbox for unprivileged Docker (Linux/WSL2) | `false` |
| `enableWeakerNetworkIsolation` | Allow system TLS trust service (macOS) for `gh`, `gcloud`, `terraform` | `false` |

([source][cc-sandbox-settings])

### Path Prefix Conventions

Sandbox filesystem paths use standard conventions (not the `//`/`/` scheme used
by Read/Edit permission rules):

| Prefix | Meaning | Example |
| ------ | ------- | ------- |
| `/` | Absolute from filesystem root | `/tmp/build` is absolute |
| `~/` | Relative to home directory | `~/.kube` → `$HOME/.kube` |
| `./` or no prefix | Relative to the project root (project settings) or `~/.claude` (user settings) | `./build` |

This differs from Read and Edit permission rules, which use `//path` for
absolute and `/path` for project-relative ([source][cc-sandboxing]).

### Array Merging Across Scopes

When `allowWrite`, `denyWrite`, or `denyRead` are defined in multiple settings
scopes (managed, user, project, local), arrays combine across files rather than replace ([source][cc-sandbox-settings]). "Concatenate + deduplicate" and "no scope can remove another scope's entries" are unverified: `allowWrite` also takes paths from `Edit(...)` allow rules and omits repository-settings entries while `permissions.blockReadsOutsideWorkingDirectories` is on, and `denyRead` also takes paths from `Read(...)` deny rules (checked 2026-11-26).

## How It Works

### Filesystem Isolation

Enforced at OS level (Seatbelt on macOS, bubblewrap on Linux/WSL2). Restrictions
apply to **all subprocess commands** — `kubectl`, `terraform`, `npm`, not just
Claude's own file tools ([source][cc-sandboxing]).

### Network Isolation

Controlled through a **proxy server running outside the sandbox**. Only approved
domains pass through. Unapproved domain requests trigger permission prompts depending on the permission mode (see the sandboxing page); `strictAllowlist` (v2.1.219, user, managed or `--settings`) or `allowManagedDomainsOnly` makes the proxy deny hosts outside the allowlist instead of prompting. The proxy decides from the requested hostname and does not inspect TLS by default ([source][cc-sandboxing], checked 2026-11-26).

### Escape Hatch

When a command fails due to sandbox restrictions, Claude may retry with
`dangerouslyDisableSandbox`. These go through the normal permission flow. Disable
with `allowUnsandboxedCommands: false` ([source][cc-sandboxing]).

### Two Sandbox Modes

**Auto-allow** (`/sandbox`): Sandboxed bash commands run without prompts. Requires
`sandbox.autoAllowBashIfSandboxed: true`; the default is now `false`.
Unsandboxable commands fall back to regular permission flow
([source][cc-sandboxing]).

**Regular permissions**: All bash commands go through standard permission flow
even when sandboxed. More control, more approvals.

## Relationship to Skills

Skills (`.claude/skills/`) are not explicitly addressed in sandbox docs.
Based on architecture:

- Skill instructions are processed by the model — not subject to sandbox
- Bash commands **executed by** a skill go through the sandboxed bash tool
- File read/edit operations by skills follow permission rules
- The `allowed-tools` frontmatter restricts which tools a skill can invoke,
  complementing sandbox restrictions

## Security Model

### What Sandbox Protects Against

- Modification of critical config files (`~/.bashrc`, `/bin/`)
- Data exfiltration to attacker-controlled servers
- Malicious dependency scripts (npm postinstall, etc.)
- Prompt injection via compromised build tools
- Unauthorized API calls

([source][cc-security])

### Known Limitations

| Limitation | Risk | Mitigation |
| ---------- | ---- | ---------- |
| No traffic inspection | Allowed domains can carry any payload | Only allow trusted domains |
| Domain fronting | Broad domains (e.g., `github.com`) may enable exfiltration | Use specific subdomains |
| Unix socket escalation | Docker socket grants host access | Avoid `allowAllUnixSockets` |
| Broad `allowWrite` | Write to `$PATH` dirs enables privilege escalation | Restrict to project dirs |
| Weaker nested sandbox | Considerably weakens security in unprivileged Docker | Keep disabled unless externally isolated |

([source][cc-sandboxing], [source][cc-security])

### Incompatible Commands

- `watchman` (used by `jest`) — use `jest --no-watchman`
- `docker` — add to `excludedCommands`

([source][cc-sandboxing])

## Additional Security Features (Non-Sandbox)

| Feature | Description |
| ------- | ----------- |
| Command approval | `curl` and `wget` are not auto-approved by default — they prompt like any other non-read-only Bash command; add to `permissions.deny` to block entirely |
| Web page summaries | For most WebFetch fetches, a separate model call reads the page and Claude receives that call's answer instead of the raw page ([security](https://code.claude.com/docs/en/security), checked 2026-11-26) |
| Trust verification | In an interactive session, a workspace trust dialog appears for untrusted folders (no trust prompt in a `-p` session) |
| Command injection detection | In Manual mode, Claude Code asks before running a Bash command it can't fully analyze; an allow rule for part of a command doesn't skip that prompt, and sandboxed commands in auto-allow mode can run without it |
| Fail-closed matching | In Manual mode, unmatched commands require approval by default |
| Credential storage | API keys/tokens stored in the macOS Keychain when available; on Linux in a file with mode 0600, on Windows in a file that inherits the access controls of the user profile directory |

([source][cc-security])

## Open Source Sandbox Runtime

The sandbox runtime is available as a standalone npm package
([source][sandbox-runtime]):

```bash
npx @anthropic-ai/sandbox-runtime <command-to-sandbox>  # unverified: the sandboxing page shows only `npm install -g @anthropic-ai/sandbox-runtime` (seccomp helper)
```

Enables sandboxing outside Claude Code, including Model Context Protocol (MCP) servers.

## Cross-Repo Write Access Pattern

When a Claude Code session needs to operate on repos outside its CWD (e.g.,
sibling repos under `/workspaces/`), the Bash sandbox blocks writes by default.

**Symptom**: Write/Edit tools work on cross-repo files, but `git add`,
`git commit`, and other Bash commands fail with "Read-only file system."

**Root cause**: Write/Edit tools have their own permission model and bypass the
Bash sandbox entirely. Only Bash tool commands are subject to
`sandbox.filesystem` restrictions.

**Solution**: Add the parent workspace path to `sandbox.filesystem.allowWrite` (no `filesystem.write.allowOnly` key is documented):

```json
"sandbox": {
  "filesystem": {
    "allowWrite": ["/workspaces/qte77"]
  }
}
```

**Alternatives**:

- `sandbox.filesystem.allowWrite` adds paths to the default write set (the wording "additive, merges across scopes" is unverified)
- Set in `~/.claude/settings.json` (user-level) for global cross-repo access
- Use `permissions.additionalDirectories` to expand the overall permission scope

**Security note**: Adding broad paths like `/workspaces/` to `allowWrite`
expands the blast radius. Prefer specific repo paths over parent directories.

## Changes in v2.1.321–325

Changelog entries (CHANGELOG sections 2.1.321 to 2.1.325) unless marked "documented".

- **Auto-allow is no longer the default (v2.1.325).** Sandboxed Bash commands follow the normal permission flow unless `sandbox.autoAllowBashIfSandboxed: true` is set. Managed settings that turn the sandbox on need the key in the highest-ranking managed source to keep commands prompt-free. Documented: the [settings reference](https://code.claude.com/docs/en/settings-reference) gives `false`, "Before v2.1.324, the default was `true`" (the CHANGELOG files the change under 2.1.325 and has no 2.1.324 section; the boundary is unreconciled). The core-settings table above is corrected accordingly.
- **Worktrees (v2.1.323, v2.1.325).** On macOS and Linux `git worktree add|move|remove` fail read-only in the sandbox, as do commits in a worktree the session was not started in or given. An isolated worktree session or agent is refused `git bisect run`, `git maintenance register|start` and `scalar` set-up commands (v2.1.325).
- **Symlinked write grants ignored (v2.1.323).** Write access granted through a symlink in a writable folder that leads elsewhere, or to a missing path, is ignored on macOS, Linux and WSL; grant the real path.
- **Invalid `--settings` stops start-up (v2.1.323).** A `--settings` file that is not valid JSON and has a `sandbox` key stops start-up, even if the key turns the sandbox off.
- **`glab config` (v2.1.323).** `glab config set` without `--global` or `--host`, and `glab config edit --local`, fail read-only in the sandbox; run them outside it.
- **Hosted sessions (v2.1.325).** Claude Code on the web, cloud scheduled tasks and Cowork cloud sessions start despite `sandbox.failIfUnavailable`, because the hosted container has no command sandbox (the settings reference lists the key as "except in an Anthropic-hosted environment").
- **Credential hygiene (v2.1.323, v2.1.325).** Claude Code's own ripgrep and most internal git commands run without most sign-in tokens and API keys in their environment (v2.1.323), as do the sandbox's own helper programs such as its network bridge (v2.1.325); ripgrep, local git and the sandbox runtime helpers also run without the mTLS client key's passphrase (v2.1.325).
- **Untrusted folders (v2.1.325).** `-p` and SDK runs in a worktree or submodule mounted into a container apply `.claude/settings.local.json` allow rules only once the folder is trusted.

## See Also

For external sandbox platforms (OpenSandbox, E2B, Sprites.dev) that provide cloud
execution and stronger isolation (gVisor, Firecracker microVMs) beyond CC's local
bubblewrap/Seatbelt enforcement, see
[CC-sandbox-platforms-landscape.md](CC-sandbox-platforms-landscape.md).

## References

- [CC Sandboxing docs][cc-sandboxing]
- [CC Sandbox settings][cc-sandbox-settings]
- [CC CHANGELOG][cc-changelog-2]
- [CC Security docs][cc-security]
- [Sandbox runtime (open source)][sandbox-runtime]

[cc-sandboxing]: https://code.claude.com/docs/en/sandboxing
[cc-sandbox-settings]: https://code.claude.com/docs/en/settings-reference
[cc-security]: https://code.claude.com/docs/en/security
[sandbox-runtime]: https://github.com/anthropics/sandbox-runtime
[cc-changelog-2]: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
