---
title: OpenAI Apps, Plugins and the GPT Store — Manifest, Marketplace and Review Compared
purpose: Compare OpenAI's current unified ChatGPT + Codex plugin system against CC plugin packaging and the Agent Plugins standard, and answer the plugins-topic Reproducible question for a second first-party vendor
source: https://developers.openai.com/plugins
created: 2026-09-30
updated: 2026-09-30
validated_links: 2026-09-30
status: assess
---

## What It Is

OpenAI ships one current plugin system shared by ChatGPT and Codex: "Plugins are the packages
people discover, install, share, and publish in ChatGPT and Codex... ChatGPT and Codex share one
universal plugin directory. When you publish a public plugin, people can discover the same listing
from supported surfaces in either product" ([Plugin architecture][concepts-plugins]). A plugin
bundles **skills** (Markdown workflow instructions, same `SKILL.md` shape as Claude Code and the
Agent Plugins standard), an optional **MCP server** (called an "App" in the end-user-facing docs —
see [Moving your custom GPT workflows to plugins][migrate-gpts]: "**Apps** connect ChatGPT to other
services for information or supported actions"), and optional lifecycle hooks.

This doc keeps three OpenAI eras apart, since the source list mixes them:

| Era | System | Status (2026-09-30) |
|---|---|---|
| 2023 | ChatGPT plugins beta (`ai-plugin.json` / OpenAPI manifest) | Named as a predecessor only. `help.openai.com`'s own wind-down article returned HTTP 403 to both WebFetch and polyfetch (patchright tier), so its retirement date is **not independently verified here** — do not cite a date for it |
| 2024-01-10 | GPT Store (custom GPTs, `chatgpt.com/gpts`) | **Legacy.** The announcement page itself now carries a live banner: "This page covers the GPT Store launch. For the current ChatGPT experience and workspace capabilities: Try ChatGPT / Explore ChatGPT Work" ([gpt-store][gpt-store], fetched 2026-09-30). Retirement is in progress: "We're transitioning custom GPTs to plugins... before custom GPTs are retired" ([migrate-gpts][migrate-gpts]) — no retirement date stated |
| Current | Unified ChatGPT + Codex plugin system (`plugin.json` + `mcp.json`, reviewed public directory) | **Current.** This doc's subject |

The "Apps SDK" name from the source list survives only as identifiers inside the current system —
an MCP-connection ID is literally `plugin_asdk_app_...` ([build-plugins][build-plugins]), the
domain-verification path is `/.well-known/openai-apps-challenge`, and an org role is "Apps
Management Write" ([submission guide][submission]) — not as a separately branded product.

## Manifest

A portable manifest declares the Agent Plugins schema directly:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "Bundle reusable skills and MCP servers.",
  "license": "MIT"
}
```

"For a portable Agent Plugins package, add `plugin.json` at the plugin root and declare the Agent
Plugins schema... OpenAI also accepts legacy and Claude-compatible manifests, but new packages
should use this format" ([Package your plugin][build-plugins]). OpenAI-specific presentation, MCP
registration and hooks go under an `extensions.com.openai` object in that same root manifest; a
separate `.codex-plugin/plugin.json` "is optional and serves as a compatibility fallback when that
object is absent." `mcp.json` likewise declares the Agent Plugins MCP schema
(`https://agent-plugins.org/schemas/1.0.0/mcp.schema.json`).

**This is documented first-party support for the Agent Plugins standard by a Technical Steering
Committee member**, not just committee membership: OpenAI's packaging docs tell new packages to declare
the schema and say OpenAI accepts it. [agent-plugins-standard-analysis.md][agent-plugins] had found no
confirmed TSC-member client integration as of 2026-09-24 (only the third-party Mitosis plugin, found
2026-09-30). It is documented support, not yet observed adoption: none of OpenAI's own example plugins
declares the schema (checked 2026-09-30; see below).

In practice the example repo has not caught up to this guidance: every one of the 62 example plugins
in [openai/plugins][gh-plugins] (checked via `plugins/notion`, 2026-09-30) ships only
`.codex-plugin/plugin.json` at its root — no root `plugin.json` — even though the docs describe that
manifest as the "compatibility fallback," not the primary path. The example repo's own README still
describes `.codex-plugin/plugin.json` as "a required ... manifest."

## Distribution — three things named "marketplace"

Keep these apart; the source list conflates them:

1. **The universal Plugins Directory** (also "ChatGPT Directory" / "Plugins Directory" depending on
   the page) — the single public catalog shared by ChatGPT and Codex, reached at
   `platform.openai.com/plugins` (JS-shell + Cloudflare challenge; blocked both to WebFetch, HTTP 403,
   and to polyfetch's patchright tier, HTTP 403 — cited here only through the public docs that
   describe it, never fetched directly). Submission requires review (see below).
2. **Local, repo and personal marketplace catalogs** — a JSON file at `$REPO_ROOT/.agents/plugins/marketplace.json`
   (repo-scoped) or `~/.agents/plugins/marketplace.json` (personal), each `plugins[]` entry naming a
   `source` (`local`, `url`, `git-subdir`, or `npm`) and a `policy`. These get **no OpenAI review** —
   "these local sources are separate from the universal public directory and support authoring,
   testing, and private distribution" ([build-plugins][build-plugins]). The reader also accepts "a
   legacy-compatible marketplace at `$REPO_ROOT/.claude-plugin/marketplace.json`" — CC's own
   marketplace path, read as a compatibility source.
3. **OpenAI Marketplace** (`openai.com/business/marketplace`, fetched 2026-09-30) — an unrelated
   partner/procurement program: "Discover tools for the business you run today... Use part of your
   existing OpenAI commitment toward eligible partner products," listing partners such as Adobe,
   Datadog, CrowdStrike, Notion and Replit with a **Request to buy** / **Join our partner waitlist**
   flow. This is a spend-commitment marketplace for third-party SaaS, not a plugin channel, and
   `platform.openai.com/marketplace/` (also JS-shell-blocked, HTTP 403 both tools) appears to be the
   developer-dashboard view of the same program, not the Plugins Directory under another name.

A workspace can also **publish a local plugin privately** to selected roles inside one organization,
distinct from both the public directory and the local marketplace files ([build-plugins][build-plugins]:
"Publishing a local plugin to your workspace doesn't publish it to the universal public Plugins
Directory").

## Versioning and pinning (the topic's open Reproducible question)

[Plan 0009][plan0009]'s Top-10 coverage-gap list (gap 10) flagged Plugins · Reproducible as open;
[CC-plugin-packaging-research.md][cc-plugin-packaging]'s own rubric scores CC's packaging docs
partial-Reproducible (sha/sha256 pinning exists, opt-in). OpenAI's current system shows the same
shape, with more concrete detail once you look inside a shipped package:

- **Manifest `version`**: semantic versioning, e.g. `"version": "0.1.7"` in the live
  `plugins/notion/.codex-plugin/plugin.json` ([source][gh-notion-manifest], fetched via GitHub
  contents API 2026-09-30).
- **Git-backed marketplace entries**: "Git-backed entries may use `ref` or `sha` selectors"
  ([build-plugins][build-plugins]) — `sha` pins to an exact commit, `ref` (branch/tag) is mutable,
  same opt-in split as CC's own `ref`/`sha` pair.
- **npm-backed entries**: `version` "accepts package versions, distribution tags, and version
  ranges" ([build-plugins][build-plugins]) — a range or tag is not a pin; only an exact version
  string is.
- **A per-plugin lockfile exists, and is only partially wired**: `plugins/notion/plugin.lock.json`
  ([source][gh-notion-lock], fetched 2026-09-30) pins each vendored skill to an exact 40-character
  commit `ref` in `openai/skills` — real, content-addressable pinning — but its `generatedBy` field
  reads `"codex plugin pack (draft)"`, and every skill's `integrity` field is the literal
  placeholder string `"sha256-<fill-during-pack>"`, not a computed hash. The lockfile's own
  `pluginVersion` (`0.1.0`) also disagrees with the live manifest's `version` (`0.1.7`) in the same
  package — the lock was not regenerated when the manifest was bumped.
- **OpenAI's own official catalog doesn't exercise the pinned path**: the curated marketplace
  shipped in the same repo, `.agents/plugins/marketplace.json` ([source][gh-marketplace], fetched
  2026-09-30), lists 65 entries: 62 use `"source": "local"`, but 3 (`crowdstrike-falcon-foundry`,
  `crowdstrike-falcon-fusion` as `"source": "url"`; `qodo` as `"source": "git-subdir"`) point at
  external git repos. None of those three sets a `ref`/`sha` pin field, so the marketplace still
  gives no example of the pin actually being exercised — but the catalog is not all-`local`.
- **The published-directory path is the least reproducible of all**: "After initial publication,
  changes to your MCP server are picked up automatically, and eligible updates go live once they
  pass automated checks. There's no need to upload a new plugin ZIP" ([submission][submission]) — a
  fixed manifest `version` does not freeze a published plugin's live MCP tool set, because OpenAI
  rescans the connected server daily and can update tool metadata server-side with no version bump.
  "Publishing an update replaces the previous package version" for skills/metadata changes, i.e. no
  package version history remains installable.
- **Local installs get a version tag, not a version history**: the local-marketplace cache path is
  `~/.codex/plugins/cache/$MARKETPLACE_NAME/$PLUGIN_NAME/$VERSION/`, but "for local plugins,
  `$VERSION` is local" — a literal string, not a semantic version, so each reinstall overwrites the
  same cache slot ([build-plugins][build-plugins]).

Net: the same "pinning primitive exists, default path is mutable" pattern as CC, plus two OpenAI-specific
weak points CC's docs don't show an equivalent of — an unfilled integrity-hash placeholder in a
shipped lockfile, and daily silent MCP-server rescans that can change a published plugin's behavior
without any version change at all.

## Review and trust

The universal directory has a documented, two-stage review pipeline that CC's own marketplace docs
have no equivalent of:

1. **Automated checks** on upload: metadata/skill scans, an MCP tool scan, and (for the MCP host)
   domain verification via a `.well-known/openai-apps-challenge` token
   ([submission][submission]).
2. **Human review**: reviewer credentials (a dedicated test account, "should work immediately
   without MFA approval"), five required positive test cases and three negative test cases, a video
   walkthrough, and release notes per submission; feedback is returned by email; a rejected
   submission can be appealed by replying to that email ([submission][submission]).
3. **Ongoing, automated re-review**: "OpenAI scans your hosted MCP server daily," diffing a tool's
   currently-approved ("Live definition") metadata against newly observed ("Held update") metadata,
   with its own appeal path scoped to "the held tool changes from that scan" only
   ([submission][submission]).
4. **Bundled hooks are untrusted by default**: "Installing or enabling a plugin doesn't automatically
   trust its hooks... Codex skips them until the user reviews and trusts the current hook definition"
   ([build-plugins][build-plugins]).
5. **Plugin guidelines** set content/behavior policy for anything in the directory — no
   impersonation, no OpenAI-endorsement implication, "Trial or demo plugins will not be accepted,"
   general-audience content only ([plugin-guidelines][plugin-guidelines]).

Local, repo and personal marketplace catalogs get **none of this** — they are unreviewed by design,
same trust model as a CC marketplace source (whoever controls the marketplace file controls what
loads).

## Interop with Claude Code is one-directional

OpenAI's docs include a dedicated conversion guide, [Submit your Claude Code plugin to
OpenAI][submit-claude], that reads CC's own formats: `.claude-plugin/plugin.json` ("Keep the
manifest for a direct Claude archive upload. The portal converts it to
`.codex-plugin/plugin.json`"), rejects `.claude-plugin/marketplace.json` as non-portable ("A
skills-only upload excludes MCP server configuration, and you can't submit an existing MCP server
integration by reference"), maps CC's `commands/`/`agents/` to skills; separately,
[build-plugins][build-plugins] documents that Codex sets `CLAUDE_PLUGIN_ROOT`/`CLAUDE_PLUGIN_DATA`
alongside `PLUGIN_ROOT`/`PLUGIN_DATA` for hook-script compatibility. It states plainly: **"Claude marketplace listings and approvals don't transfer."**
Nothing in CC's own plugin docs ([CC-plugin-packaging-research.md][cc-plugin-packaging]) describes
the reverse — CC does not ingest a Codex-format `.codex-plugin/plugin.json` package.

## Comparison

| | OpenAI (current) | Claude Code | Agent Plugins standard |
|---|---|---|---|
| **Manifest** | Root `plugin.json` (Agent Plugins v1.0.0 schema) + `mcp.json`; OpenAI extras under `extensions.com.openai`; `.codex-plugin/plugin.json` as compat fallback [build-plugins] | `.claude-plugin/plugin.json`, optional — standard paths auto-discovered [cc-plugin-packaging] | `plugin.json` + optional `mcp.json`, extensible per-client namespaces [agent-plugins] |
| **Distribution** | Universal reviewed directory + unreviewed local/repo/personal `marketplace.json` + admin-gated workspace publish; separate unrelated "OpenAI Marketplace" partner program [build-plugins, submission] | `marketplace.json` sources: `github`/`url`/`git-subdir`/`npm`/local; no public review pipeline documented [cc-plugin-packaging] | Left entirely to each client; the spec defines no marketplace [agent-plugins] |
| **Pinning** | `version` (semver); git `ref`(mutable)/`sha`(pin); npm version/range/tag; a per-plugin lockfile exists but ships an unfilled integrity placeholder in the one example inspected; published MCP servers rescanned daily, independent of version [build-plugins, submission, gh-notion-lock] | `version` field; marketplace `ref`(mutable)/`sha`(pin); archive `sha256`(pin) — all opt-in, default path mutable [cc-plugin-packaging §5] | No pinning primitive defined at the standard level — client-specific [agent-plugins, inferred] |
| **Review / trust** | Automated + human review, domain verification, daily re-scan with held-vs-live diffing, appeals, hooks untrusted until reviewed [submission, build-plugins] | No documented public review pipeline; trust is per-marketplace-source; symlink handling is security-scoped [cc-plugin-packaging] | Undefined by the standard; each client sets its own trust model [agent-plugins] |

## Rubric

`scored 2026-09-30`, OpenAI's current unified ChatGPT + Codex plugin system as shipped (per
[agent-substrate-rubric.md][rubric]):

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| yes [concepts-plugins] ("ChatGPT and Codex share one universal plugin directory... people can discover the same listing from supported surfaces in either product") | partial [build-plugins] (published MCP servers must be public HTTPS endpoints reachable from any client, but the installed plugin artifact itself is cached per-machine at `~/.codex/plugins/cache/...`, and "installing a plugin on the web doesn't deploy" bundled hook scripts) | partial [build-plugins, submission, gh-notion-lock] (sha/exact-version pinning exists opt-in; the one shipped lockfile inspected has an unfilled integrity placeholder and a stale `pluginVersion`; OpenAI's own official marketplace catalog is mostly unpinned `local` sources, and the 3 of 65 git-backed entries set no `ref`/`sha` pin either; published MCP servers are rescanned daily independent of the manifest version) | yes [build-plugins, submit-claude] (`extensions.com.openai` namespace, `.codex-plugin` compat fallback, skills-only/MCP-only/both shapes, a documented CC-plugin conversion path) | yes [build-plugins, submission] (semver `version` field; git-backed marketplace sources; "Update your published plugin... creates a package version with its own checks and review outcome") | partial [submission] ("Held update" vs "Live definition" diffing per MCP tool, required release notes per submission, email-recorded review/appeal history — publisher-facing lifecycle traceability, not an end-user-facing citation trail) |

`scored 2026-09-30`

## Unverifiable / Hedged

- The 2023 ChatGPT plugins beta's retirement date is not verified here: `help.openai.com`'s own
  wind-down article returned HTTP 403 to both WebFetch and polyfetch (patchright tier, three
  attempts). Do not cite a specific date for that retirement from this doc.
- `platform.openai.com/apps` and `platform.openai.com/marketplace/` are a client-rendered SPA shell
  behind a Cloudflare challenge (`4,875` bytes of boot HTML each, no server-rendered content) —
  confirmed blocked to WebFetch (HTTP 403) and to polyfetch's patchright tier (HTTP 403 after 3
  attempts). Everything said about the developer-dashboard Plugins/Marketplace UI in this doc comes
  from the public docs that describe it, never from a direct fetch of that dashboard.
- The GPT Store announcement's "over 3 million custom versions of ChatGPT" figure is OpenAI's own
  January 2024 claim, self-reported, and now two years stale; not re-verified here.
- `gpts-openai.com` was not found referenced by any first-party OpenAI page fetched for this doc. It
  is recorded here only as a standing caution from the plan brief: if it surfaces in future research,
  it is a third-party site, not an OpenAI domain, and should never be cited as OpenAI.
- Repo star/fork/issue counts for `openai/plugins` (7,241 / 937 / 37) are from the GitHub API,
  2026-09-30, and will drift.

## Sources

| Source | Content |
|---|---|
| [Plugin architecture][concepts-plugins] | Current unified ChatGPT + Codex plugin definition, universal directory statement |
| [Package your plugin][build-plugins] | Manifest format, Agent Plugins schema, marketplace formats, pinning (`ref`/`sha`/npm), hooks trust |
| [Upload and submit your plugin][submission] | Review pipeline: upload, automated checks, human review, daily MCP rescans, appeals, publish/update flow |
| [Plugin guidelines][plugin-guidelines] | Content and behavior policy for the universal directory |
| [Submit your Claude Code plugin to OpenAI][submit-claude] | First-party CC-to-OpenAI conversion mapping; "Claude marketplace listings and approvals don't transfer" |
| [Moving your custom GPT workflows to plugins][migrate-gpts] | First-party legacy (GPT)-to-current (plugin) transition statement; "Apps" end-user terminology |
| [Introducing the GPT Store][gpt-store] | 2024-01-10 announcement; live banner marking it historical as of this fetch |
| [openai.com/business/plugins][business-plugins] | Current first-party connector catalog (business-facing) |
| [openai.com/business/marketplace][business-marketplace] | OpenAI Marketplace partner/procurement program — confirmed distinct from the Plugins Directory |
| [openai/plugins][gh-plugins] | Example Codex plugin repo; README, structure |
| GitHub API repo metadata, 2026-09-30 | `openai/plugins`: 7,241 stars / 937 forks / 37 open issues, created 2026-03-04, pushed 2026-09-28, `license: null`, no root LICENSE file |
| [`plugins/notion/.codex-plugin/plugin.json`][gh-notion-manifest] | Live example manifest; per-package `"license": "MIT"` field, no accompanying LICENSE file |
| [`plugins/notion/plugin.lock.json`][gh-notion-lock] | Real per-skill commit-`ref` pinning; unfilled `integrity` placeholder; stale `pluginVersion` vs. the live manifest |
| [`.agents/plugins/marketplace.json`][gh-marketplace] | OpenAI's own curated example marketplace; 62 of 65 entries use unpinned `local` sources, the other 3 are git-backed but unpinned |
| [CC-plugin-packaging-research.md § 5][cc-plugin-packaging] | CC's own manifest/marketplace/pinning system, same rubric, scored 2026-09-30 |
| [agent-plugins-standard-analysis.md][agent-plugins] | The Agent Plugins open standard OpenAI's manifest declares; TSC membership vs. shipped implementation |
| [agent-substrate-rubric.md][rubric] | Scoring method and the Plugins-topic coverage gap this doc extends with a second vendor |
| [Plan 0009][plan0009] | Top-10 coverage-gap list (gap 10: Plugins · Reproducible) |

Pages under `developers.openai.com/plugins/` and `learn.chatgpt.com/docs/` were fetched as their
Markdown twin (`.md` suffix) via polyfetch, 2026-09-30, per that site's own documented convention
("Markdown versions of documentation pages are available by appending `.md` to the page URL").

[concepts-plugins]: https://developers.openai.com/plugins/concepts/plugins
[build-plugins]: https://developers.openai.com/plugins/build/plugins
[submission]: https://developers.openai.com/plugins/deploy/submission
[plugin-guidelines]: https://developers.openai.com/plugins/plugin-guidelines
[submit-claude]: https://developers.openai.com/plugins/guides/submit-claude-plugin
[migrate-gpts]: https://learn.chatgpt.com/docs/migrate-custom-gpts
[gpt-store]: https://openai.com/index/introducing-the-gpt-store/
[business-plugins]: https://openai.com/business/plugins/
[business-marketplace]: https://openai.com/business/marketplace/
[gh-plugins]: https://github.com/openai/plugins
[gh-notion-manifest]: https://github.com/openai/plugins/blob/main/plugins/notion/.codex-plugin/plugin.json
[gh-notion-lock]: https://github.com/openai/plugins/blob/main/plugins/notion/plugin.lock.json
[gh-marketplace]: https://github.com/openai/plugins/blob/main/.agents/plugins/marketplace.json
[cc-plugin-packaging]: ../../cc-native/plugins-ecosystem/CC-plugin-packaging-research.md
[agent-plugins]: agent-plugins-standard-analysis.md
[rubric]: ../../sdlc-lcm/agent-substrate-rubric.md
[plan0009]: ../../plans/2026-09-27-0009-focus-shared-memory-context.md
