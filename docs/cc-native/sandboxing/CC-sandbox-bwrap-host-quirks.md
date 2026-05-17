---
title: CC Sandbox bwrap Host Quirks — Phantom Files and AppArmor Friction
description: bwrap-on-Linux friction independent of execution context (local, WSL2, Codespaces) — phantom dotfile leakage and AppArmor user-namespace prerequisites.
source: https://github.com/anthropics/claude-code/issues/17727, https://github.com/anthropics/claude-code/issues/17087, https://github.com/anthropic-experimental/sandbox-runtime/issues/139
category: analysis
created: 2026-05-02
updated: 2026-05-17
validated_links: 2026-05-17
---

**Status**: Active upstream bug — `claude-code#17727` open; `claude-code#17087` closed-as-completed but recurring; `sandbox-runtime#139` is the upstream fix tracker.

## Scope

Friction caused by `bubblewrap` itself, independent of host class. Reproduces on:

- Local Linux (Fedora 43, Arch, Ubuntu 24.04 LTS)
- WSL2 (Ubuntu)
- GitHub Codespaces (Azure-hosted devcontainer)

This file is the bwrap-on-Linux friction reference. Codespace-specific
double-isolation issues live in
[CC-sandbox-codespaces-friction.md](CC-sandbox-codespaces-friction.md). Sandbox
internals (`denyWithinAllow` semantics, bind-mount model) live in
[CC-sandboxing-analysis.md](CC-sandboxing-analysis.md).

## Friction 1 — Phantom Dotfiles in CWD

### Symptom

After any Bash tool call, the project root accumulates files mirroring `$HOME`
dotfiles, plus git internals leaked from `denyWithinAllow`:

```text
.bash_profile  .bashrc  .gitconfig  .gitmodules  .idea  .mcp.json
.profile       .ripgreprc            .vscode  .zprofile  .zshrc
.claude/agents .claude/commands      .claude/skills
HEAD  config  hooks  objects  refs
```

### File morphology (varies by host)

| Host | Type | Mode | Owner |
| ---- | ---- | ---- | ----- |
| Arch ([#17087][gh-17087], 2026-01) | regular file, 0 bytes | `0444` | user |
| Ubuntu 24.04 ([poltimmer on #17727][gh-17727]) | char-special `/dev/null` (1,3) | `0666` | nogroup |
| WSL2 Ubuntu ([kosei-w90607 on #29316][gh-29316]) | char-special `/dev/null` (1,3) | `0666` | nobody:nogroup |
| Fedora 43 (local, 2026-05) | char-special, 0 bytes | `0666` | nobody:nobody (UID 65534) |

### Root cause (poltimmer's analysis on [#17727][gh-17727])

In the minified runtime, the function building the auto-deny list resolves the
home-dotfile list against `process.cwd()` instead of `os.homedir()`:

```js
// Bug
O = [...oiH.map(j => path.resolve(_, j)), ...z.map(j => path.resolve(_, j))]
// where _ = process.cwd()
// and oiH = [".gitconfig", ".gitmodules", ".bashrc", ".bash_profile",
//            ".zshrc", ".zprofile", ".profile", ".ripgreprc",
//            ".mcp.json", ".claude.json"]
```

This emits `--ro-bind /dev/null $PROJECT/.bashrc`. Because the project dir is
in the writable bind-mount region, `mknod` propagates the device node through
to the host filesystem. Cleanup is best-effort and skipped when other
sandboxes are active (`Deferring mount point cleanup — N sandbox(es) still
active`), so phantom files persist across sessions.

The git-internals leak (`HEAD`, `config`, `hooks`, `objects`, `refs` at
project root) has the same shape: `denyWithinAllow` auto-generation drops the
`.git/` prefix when resolving against CWD.

Upstream fix tracker: [`anthropic-experimental/sandbox-runtime#139`][sr-139].

### Side effects (beyond cosmetic git noise)

- `git log HEAD` / `git rev-list HEAD` fail with "ambiguous argument" because
  the phantom `HEAD` collides with the ref ([gnprice on #29316][gh-29316]).
- `EnterWorktree` tool unusable — `.git/worktrees/<name>/HEAD` is blocked by
  `denyWithinAllow` matching `HEAD` as a bare suffix, with no negation
  syntax ([qte77 on #17374][gh-17374], [#29316][gh-29316]).
- CMake `FetchContent` / `CPM.cmake` blocked by `.git` write deny
  ([danra on #17727][gh-17727]).
- `.gitignore` directory patterns (e.g., `.vscode/`) do not match phantom
  files (created as files, not directories) — rooted file patterns required.

### Mitigations (none fix root cause)

**Rooted-pattern `.gitignore` block:**

```gitignore
# bwrap phantom files (anthropics/claude-code#17727, sandbox-runtime#139)
/.bash_profile
/.bashrc
/.profile
/.zprofile
/.zshrc
/.gitconfig
/.gitmodules
/.ripgreprc
/.mcp.json
/.idea
/.vscode
/.claude/agents
/.claude/commands
/.claude/skills
# git internals leaked by denyWithinAllow .git/ prefix loss
/HEAD
/config
/hooks
/objects
/refs
```

**Other options:**

- Disable sandbox entirely (`sandbox.enabled: false`) — loses network
  isolation.
- Cleanup outside sandbox: `rm -f` from a non-sandboxed shell. Char-device
  phantoms owned by `nobody`/`nogroup` may need elevated removal on some
  hosts.
- Avoid project-scoped `.mcp.json` while bug is live — the phantom shadows
  any real config placed there.

### What does NOT work (don't waste time on these)

- **Editing `permissions.deny` or `sandbox.filesystem.denyRead`** — the
  `$HOME`-dotfile deny list is built by an internal runtime function
  (`Rx4`'s hardcoded `oiH` array per [poltimmer on #17727][gh-17727]),
  not from user settings. There is nothing to remove.
- **`submodule.recurse=false`** or other submodule git config — git probes
  `.gitmodules` to discover submodules regardless of recurse settings, so
  the `unable to access ... .gitmodules: Permission denied` warning during
  `git fetch` persists.
- **`touch .gitmodules`** (or any other affected file) to pre-create a real
  file — bwrap mounts `/dev/null` over it during the session, and
  cleanup-on-exit is best-effort and skipped when concurrent sandboxes are
  active. Real content can be lost.

The only working mitigations are gitignore (cosmetic), full sandbox disable,
or waiting for [`sandbox-runtime#139`][sr-139].

### Version timeline

| Version | Observation |
| ------- | ----------- |
| 2.1.2 (2026-01) | First reported ([#17087][gh-17087]) |
| 2.1.47 (Codespaces) | Reproduces ([qte77 on #17727][gh-17727]) |
| 2.1.52 — 2.1.97 | Repeated confirmations across reporters on #17727 |
| 2.1.120 (2026-04-25) | Reproduces ([nathanschram on #17727][gh-17727]) |
| 2.1.123 | One reporter sees no recurrence ([gnprice on #29316][gh-29316]) — unconfirmed |
| current (2026-05-02) | Reproduces locally on Fedora 43 |

## Friction 2 — AppArmor `userns` Prerequisite (Ubuntu 24.04+)

### Symptom

Claude Code refuses to start with sandbox enabled:

```text
Error: sandbox required but unavailable: ${j$}
sandbox.failIfUnavailable is set — refusing to start without a working sandbox.
```

(The unrendered `${j$}` template literal is a separate UX bug filed as
[#53081][gh-53081].)

### Root cause

Ubuntu 24.04 LTS ships with `kernel.apparmor_restrict_unprivileged_userns=1`.
bwrap requires unprivileged user namespaces to create its sandbox; AppArmor
blocks them by default unless the binary has an explicit profile granting
`userns`.

### Fix ([3f6a][gh-17727], [nathanschram][gh-17727] on #17727)

```bash
sudo tee /etc/apparmor.d/bwrap <<'EOF'
abi <abi/4.0>,
include <tunables/global>
profile bwrap /usr/bin/bwrap flags=(unconfined) {
  userns,
}
EOF
sudo apparmor_parser -r /etc/apparmor.d/bwrap
```

After applying, `bwrap --bind / / /bin/echo ok` runs as the unprivileged user
and Claude Code starts cleanly.

### Status

Hard startup-blocker as of v2.1.120 — first-time Ubuntu 24.04 users hit a
wall with no actionable error message. Tracking: [#17727][gh-17727].

## Friction 3 — Bind-Mount-Held Files Block `git unlink`

### Symptom

`git switch`, `git restore`, `git pull --ff-only`, and `gh pr merge` (which
runs `git pull` internally) fail with:

```text
error: unable to unlink old 'CHANGELOG.md': Device or resource busy
error: unable to unlink old 'README.md': Device or resource busy
error: unable to unlink old 'Makefile': Device or resource busy
```

Server-side `gh pr merge` succeeds (`origin/main` advances), but the
local-side `git pull` aborts mid-flight — leaving the local branch behind
origin and the working tree partially stale.

### Affected files (project-dependent)

The set is stable per project but varies across projects. Observed:

- **`qte77/analyze-stock-kpi`**: `CHANGELOG.md`, `README.md`, `pyproject.toml`, `Makefile`
- **`qte77/ai-agents-research`**: `.claude/settings.json`, `Makefile`, `README.md`

Pattern: project-root config/context files CC reads at session start.
Distinct symptom class from Friction 1 — that one *creates* extra files;
this one makes *existing* files temporarily un-`unlink(2)`-able.

### Root cause

Related bug class to Friction 1 ([`claude-code#17727`][gh-17727]). Open file
descriptors against the sandbox's bind-mount targets block `unlink(2)`,
which is what git calls on every checkout/restore to swap file content.
Cleanup is best-effort and skipped while other sandboxes are active.
Distinct from Friction 1's `--ro-bind /dev/null` phantom-creation: here the
bind-mount holds real files open via fd.

### Side effects

- After `git switch <branch>`: HEAD ref moves but busy files stay at the
  prior branch's content. `git status` reports them "Modified" on a
  freshly-switched branch — confusing.
- After `gh pr merge --delete-branch`: server-side merge completes,
  `origin/<branch>` advances, but the local `git pull` step inside `gh`
  aborts. Local main desyncs from origin.
- Subagents launched mid-session inherit the sandbox state — they see the
  same busy-lock.

### Recovery workaround

```bash
# 1. Ensure remote ref is current
git fetch origin

# 2. Move local branch pointer to remote without touching working tree
git update-ref refs/heads/main refs/remotes/origin/main

# 3. Refresh the index from new HEAD (working tree untouched)
git reset HEAD -- .

# 4. Restore files NOT on the busy list (normal git path)
git restore <unlocked-files>

# 5. For files ON the busy list: overwrite in place via Claude Code's
#    Edit/Write tool. open(O_WRONLY|O_TRUNC) bypasses unlink(2), so the
#    bind-mount lock doesn't block it. Source the desired content via:
git show HEAD:<file> > "$TMPDIR/<file>.head"
#    Then Edit the working-tree file to match.
```

### Data-safety guards

- **Pre-flight**: `git rev-parse HEAD origin/main` — confirm the SHA you're
  about to `update-ref` to is what you want. The SHA the server reported on
  the merge is the truth source.
- **WIP detection**: `git diff HEAD -- <busy-files>` before any step. If the
  diff is only stale-branch leftovers, proceed. If it shows pending edits
  you care about, stage them first via `git add` (index updates bypass the
  unlink lock).
- **Source from HEAD, not working tree**: when overwriting via Edit/Write,
  dump `git show HEAD:<file> > $TMPDIR/<file>.head` and eyeball before
  applying. The stuck working-tree copy is, by definition, stale.
- **Recovery net**: `git reflog` records every `update-ref` for 90 days;
  objects persist until `gc`. Mistakes are reversible.

### What does NOT work

- `git restore <busy-file>` — hits the same `unlink(2)` path.
- `git checkout -- <busy-file>` — same.
- `git reset --hard` — same, with worse failure mode: partial reset state
  plus the unlink error.
- `git update-index --skip-worktree <busy-file> && git restore` — `restore`
  still tries to `unlink` before `skip-worktree` takes effect.
- `rm -f <busy-file>` from inside the sandbox — same unlink failure. Only
  `rm` from a non-sandboxed shell works.

### Version timeline

| Version | Observation |
| ------- | ----------- |
| 2.1.123 — 2.1.127 (2026-05) | Reproduces on Fedora 43 across multiple PR-merge cycles in `qte77/analyze-stock-kpi` and `qte77/ai-agents-research` |

## See Also

- [CC-sandbox-codespaces-friction.md](CC-sandbox-codespaces-friction.md) —
  codespace double-isolation friction
- [CC-sandboxing-analysis.md](CC-sandboxing-analysis.md) — sandbox internals,
  `denyWithinAllow` semantics, bind-mount model
- [CC-permissions-bypass-analysis.md](CC-permissions-bypass-analysis.md) —
  permission bypass patterns
- [CC-sandbox-platforms-landscape.md](CC-sandbox-platforms-landscape.md) —
  external sandbox platforms

## References

- [#17087 — Original phantom dotfiles report (closed, claimed fixed)][gh-17087]
- [#17727 — Linux sandbox broken — canonical active discussion][gh-17727]
- [#17374 — Sandbox fails in worktrees due to .git file structure][gh-17374]
- [#29316 — `/sandbox` creates empty stub files in project root (worktrees)][gh-29316]
- [#17258 — Closed-as-dup phantom report (Arch, chezmoi)][gh-17258]
- [#40133 — Sibling `.claude/skills` symlink EISDIR (closed-as-dup)][gh-40133]
- [#28730 — `excludedCommands` doesn't bypass bwrap][gh-28730]
- [`sandbox-runtime#139` — Upstream fix tracker][sr-139]
- [#53081 — `${j$}` template literal not rendered in startup error][gh-53081]

[gh-17087]: https://github.com/anthropics/claude-code/issues/17087
[gh-17727]: https://github.com/anthropics/claude-code/issues/17727
[gh-17374]: https://github.com/anthropics/claude-code/issues/17374
[gh-29316]: https://github.com/anthropics/claude-code/issues/29316
[gh-17258]: https://github.com/anthropics/claude-code/issues/17258
[gh-40133]: https://github.com/anthropics/claude-code/issues/40133
[gh-28730]: https://github.com/anthropics/claude-code/issues/28730
[gh-53081]: https://github.com/anthropics/claude-code/issues/53081
[sr-139]: https://github.com/anthropic-experimental/sandbox-runtime/issues/139
