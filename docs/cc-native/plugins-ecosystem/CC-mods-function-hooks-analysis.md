---
title: CC Mods (Function Hooks) Analysis
source: https://code.claude.com/docs/en/plugins/mods/overview, https://code.claude.com/docs/en/plugins/mods/admin, https://code.claude.com/docs/en/plugins/mods/reference
purpose: Analysis of Claude Code mods — in-process JavaScript/TypeScript event handlers, shipped as plugins, that redraw or rewrite how Claude Code behaves — for extensibility, governance, and the agent substrate rubric.
created: 2026-10-02
updated: 2026-10-02
validated_links: 2026-10-02
status: generally-available
---

**Details:** Requires Claude Code v2.1.287+; on by default

## What a Mod Is

A mod is a [plugin](CC-official-plugins-landscape.md) whose code is JavaScript or TypeScript functions, called hooks, that Claude Code calls directly inside its own process when an event happens — a tool call, a submitted prompt, part of the interface being drawn, and more ([source][mods-overview]). Anthropic explicitly distinguishes a mod's handlers from the settings-file hooks this corpus already documents in [CC-hooks-system-analysis.md](../configuration/CC-hooks-system-analysis.md): "A settings hook runs a shell command for each event and passes JSON over stdin and stdout. A mod's handlers are functions that run inside Claude Code instead" ([source][mods-overview]). Both are called "hooks" by Anthropic; this doc follows the docs' own disambiguation and calls the settings-file kind a "settings hook."

Proposed publicly by a contributor (`poteat`) in [claude-code#91870][issue-91870] (2026-09-03, "Mods - make Claude 10x more extensible," 230 comments and 218 reactions as of this check), iterated in public under the feature flag `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS`, then made the default in **Claude Code v2.1.287**, which also makes the flag a no-op ([source][mods-overview], [source][mods-admin]). Whether `poteat` is an Anthropic employee is unverified: a GitHub public-membership check against the `anthropics` org returns 404 for that username, which GitHub returns both for "not a member" and for "a private member" (`gh api orgs/anthropics/public_members/poteat`, checked 2026-10-02 — the 404 itself is the evidence, so this is not a dead link to fix); the issue's `author_association` field reads `CONTRIBUTOR`, not `OWNER` or `MEMBER`. Treat the issue as a community-filed proposal Anthropic adopted, not as an Anthropic announcement in its own voice.

### How a Mod Is Built

A mod's minimal file layout ([source][mods-reference]):

| File | Required | Contents |
|---|---|---|
| `.claude-plugin/plugin.json` | Yes | Standard plugin [manifest](CC-plugin-packaging-research.md) — mods add no required fields |
| `hooks/hooks.json` | Yes | `{"modules": ["./register.js"]}` — points at the entry file |
| The hooks module | Yes | Exports `register(on, options)`; an ES module (`.js`/`.ts`/etc.) |
| `types/index.d.ts` | When using `$.state` or a custom namespace | Declares `PluginState` and any namespace the mod adds |
| `*.test.ts` | No | Run by `claude plugin test` |

Inside `register`, `on(event, matcher?, hook)` registers a hook. Hooks chain like middleware: a hook can **observe** (`await next(e)`, then look), **rewrite** (`next({...e, field})`), or **answer** (return `{deny: reason}` without calling `next`) ([source][mods-overview]). `claude plugin validate <dir>` statically reports exactly which events a mod hooks and which `$` methods it calls, before it is ever installed ([source][mods-admin]) — a worked tutorial example's output: `hooks: session.start, turn.complete, ui.render{component=AbovePrompt}` / `calls: $.session.usage, $.state.get, $.state.set, $.ui.resolve` ([source][claudedev-mods-blog]).

### The `$` API Surface

`$` groups about 20 namespaces, among them `$.ui` (draw panes/bands, buttons, toasts), `$.session` (`usage`, `cwd`, `send`/`receive` between sessions), `$.state` (reactive, per-session), `$.store` (a key-value store "every session **on the machine** shares" — explicitly scoped to one machine, not synced further), `$.fs`/`$.process`/`$.http` (files, subprocesses, network, all with the user's own permissions), `$.model` (call a model directly), and `$.telemetry` ([source][mods-reference]). A mod is **not sandboxed**: "It can read and write your files, start processes, and make network requests" with the installing user's full access, and a mod can approve a tool call before any permission prompt, including one a `deny` rule would otherwise refuse, unless an organization's built-in guard blocks that ([source][mods-overview], [source][mods-admin]).

### Governance

A built-in guard mod, `sec-default@builtin`, loads ahead of every user-installed mod on any machine with managed settings or a Team/Enterprise sign-in, and protects what an organization manages (its own hooks, managed CLAUDE.md, managed MCP servers) from being overridden by a user's mod ([source][mods-admin]). An organization can go further: `allowManagedModsOnly` blocks every mod a user installs, `disableSideloadFlags` blocks `--plugin-dir`, and a custom policy mod in `prependPlugins` can inspect another mod's declared `$` calls (via the `plugin.register` event) and refuse it before it loads ([source][mods-admin]).

### AGENTS.md Support as a Mod

One of Claude Code's own built-in mods, listed in `/plugin` as `cc-plugin-agents-md`, is what "loads `AGENTS.md` as project instructions" ([source][mods-overview]) — confirming plan 0010's owner-lead hypothesis that this ships as a mod rather than engine code. Its source, with tests, is public at [`mods/agents-md`][gh-agents-md] in `anthropics/claude-code`. The module hooks `session.start` (announces its mode), `prompt.context` (answers `AGENTS.md` files as `project`-kind instruction files when no `CLAUDE.md` exists on the path), `agent.spawn` (a fork shares its parent's already-delivered files), and `tool.call` on `Read` (attaches a subdirectory's `AGENTS.md` the way CC attaches a nested `CLAUDE.md`) ([source][gh-agents-md-readme]). `tests/register.test.ts` asserts, among other things, that a project with only an `AGENTS.md` gets it loaded as a `project`-kind instruction file with one debug-log line (`no CLAUDE.md found; AGENTS.md loaded: <path>`) and nothing added to the visible transcript, and that a project with its own `CLAUDE.md` is left to the engine untouched ([source][gh-agents-md-tests]). See [CC-memory-system-analysis.md's AGENTS.md row](../context-memory/CC-memory-system-analysis.md#agentsmd-as-a-cross-agent-instruction-file-new-row) for the rubric scoring of AGENTS.md itself; this section only establishes that the *mechanism* is a mod.

### Two More Built-In Mods, and a Sample Set

`cc-plugin-diff` (the `/diff` pane) and `cc-plugin-telemetry` are also built-in mods with public source under [`mods/`][gh-mods-dir] ([source][mods-overview]). Anthropic's own tutorial for writing a mod ([claude.dev, Addy Osmani, 2026-10-01][claudedev-mods-blog]) walks through three sample mods shared, unsupported, in a separate `claude-code-playground` repository: `token-weather` (a context-window forecast band above the prompt), `blast-radius` (holds a destructive Bash command — `rm -rf`, `git reset --hard`, a force push — in a pane with Proceed/Cancel until approved), and `replay-theater` (steps through a turn's file edits as a diff). None of the three is an official product; they are worked examples, and Anthropic's own docs link the same three from [the mods overview page][mods-overview].

## Scored on the Agent Substrate Rubric

Scored 2026-10-02, from [code.claude.com/docs/en/plugins/mods/overview, /admin and /reference][mods-overview] only.

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| partial [mods-reference][mods-reference] (`$.store` is explicitly "a key-value store that every session **on the machine** shares" — a defined, documented multi-session read/write) | no [mods-reference][mods-reference] (the same `$.store` description scopes sharing to one machine; nothing in the mods docs describes a mod's *own* state syncing across machines — org-wide *policy* distribution via managed settings is a separate, admin-side mechanism, not mod state) | partial [mods-reference][mods-reference] (a mod's own `plugin.json` carries a `version` a marketplace can pin by `ref`/`sha`/`sha256`, per [CC-plugin-packaging-research.md §5][packaging-pinning] — but the mods API itself is not pinned across CC releases: "The copy on GitHub can be older than the Claude Code version you have installed. When the two disagree, trust the copy Claude Code writes for your version") | yes [mods-admin][mods-admin] (four independent admin policies — `allowManagedModsOnly`, `allowManagedHooksOnly`, `disableAllHooks`, `disableSideloadFlags` — plus per-mod `userConfig` options and `prependPlugins`/`appendPlugins` ordering, all without changing a mod's code) | yes [mods-overview][mods-overview] ("Put the mod in a GitHub repo with a marketplace file... you can update it with a normal push" — a mod ships and updates as ordinary git-hosted plugin source) | partial [mods-admin][mods-admin] (`claude plugin validate` gives static, pre-install transparency — exactly which events and `$` calls a mod's code can reach — but there is no default runtime audit log of what a mod actually did in a session; building one is a worked example an organization must write itself, as the admin page's own sample policy mod shows) |

No CONTRIBUTING file, PR template, or README "how to contribute" section was found in `anthropics/claude-code` (mods' home repo) for mods specifically; `claude-plugins-official`'s own README documents a contribution flow only for its `external_plugins/` tier, not for a built-in CC mod. That absence does not change the scores above, which rest on the mods API's own documented runtime behavior (`$.store`'s machine scope), not on rule 6's git-governance framing.

## Sources

| Source | Content |
|---|---|
| [Mods overview][mods-overview] | What a mod is, built-in mods table, install/update, trust model |
| [Manage mods for your organization][mods-admin] | Governance: built-in guard, managed-settings policies, policy-mod example |
| [Mods reference][mods-reference] | Full event list, `$` API namespaces, render sites, limits |
| [anthropics/claude-code `mods/agents-md`][gh-agents-md] | The built-in AGENTS.md mod's source directory |
| [`mods/agents-md/README.md`][gh-agents-md-readme] | What the mod hooks and how its modes work |
| [`mods/agents-md/tests/register.test.ts`][gh-agents-md-tests] | What the mod's own tests assert about its behavior |
| [claude-code#91870][issue-91870] | The mod proposal's origin, iteration history, and author association |
| `gh api orgs/anthropics/public_members/poteat`, 2026-10-02 | Returns 404 (ambiguous: not a member, or a private one) — no URL, the API response itself is the observation |
| [Getting started with Claude Code mods][claudedev-mods-blog] | Anthropic's own tutorial (claude.dev), Addy Osmani, 2026-10-01; three worked sample mods |
| [CC-plugin-packaging-research.md §5][packaging-pinning] | Marketplace version-pinning mechanics (`ref`/`sha`/`sha256`), reused for Reproducible above |

[mods-overview]: https://code.claude.com/docs/en/plugins/mods/overview
[mods-admin]: https://code.claude.com/docs/en/plugins/mods/admin
[mods-reference]: https://code.claude.com/docs/en/plugins/mods/reference
[gh-agents-md]: https://github.com/anthropics/claude-code/tree/main/mods/agents-md
[gh-agents-md-readme]: https://github.com/anthropics/claude-code/blob/main/mods/agents-md/README.md
[gh-agents-md-tests]: https://github.com/anthropics/claude-code/blob/main/mods/agents-md/tests/register.test.ts
[gh-mods-dir]: https://github.com/anthropics/claude-code/tree/main/mods
[issue-91870]: https://github.com/anthropics/claude-code/issues/91870
[claudedev-mods-blog]: https://claude.dev/blog/getting-started-with-claude-code-mods
[packaging-pinning]: CC-plugin-packaging-research.md#5-version-pinning-for-reproducible-installs
