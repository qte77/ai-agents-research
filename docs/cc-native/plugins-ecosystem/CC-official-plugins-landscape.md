---
title: CC Official Plugins Landscape
source: https://www.firecrawl.dev/blog/best-claude-code-plugins
purpose: Catalog the official CC plugin ecosystem, assess coverage gaps in this research repo, and provide adoption guidance per plugin.
created: 2026-03-12
updated: 2026-11-22
validated_links: 2026-10-18
status: reference
---

**Details:** living catalog — update as ecosystem evolves

## Overview

The CC plugin ecosystem has grown to 9,000+ plugins across the marketplace, ClaudePluginHub, and Claude-Plugins.dev ([source][firecrawl-blog]). This document catalogs the top official plugins, maps coverage in this research repo, and provides adoption guidance.

## Plugin Coverage Matrix

| # | Plugin | Installs | This Repo Coverage | Action |
|---|---|---|---|---|
| 1 | [Frontend Design](#frontend-design) | 96.4k | None | Brief section (UI-focused, skip unless frontend) |
| 2 | [Context7](#context7) | 71.8k | None | Full section (actively used via MCP) |
| 3 | [Code Review](#code-review) | 50k | Name-only mention | Moderate section (multi-agent scoring) |
| 4 | Firecrawl | — | Full ([web-scraping analysis](CC-web-scraping-plugins-analysis.md)) | Cross-ref only |
| 5 | Playwright | 28.1k | Full ([web-scraping analysis](CC-web-scraping-plugins-analysis.md)) | Cross-ref only |
| 6 | [Security Guidance](#security-guidance) | 25.5k | Name-only mention | Full section (three review layers, hooks, switches; v2.0.21) |
| 7 | Chrome DevTools MCP | 20k | Full ([web-scraping analysis](CC-web-scraping-plugins-analysis.md)) | Cross-ref only |
| 8 | [Figma MCP](#figma-mcp) | 18.1k | None | Brief section (design-focused, skip unless UI) |
| 9 | [Linear](#linear) | 9.5k | None | Brief section (adopt if using Linear PM) |
| 10 | Ralph Loop | — | Full ([ralph enhancement research](../agents-skills/CC-ralph-enhancement-research.md)) | Cross-ref only |
| — | CLI-Anything | — | Full ([CLI-Anything analysis](../agents-skills/CC-cli-anything-analysis.md)) | Cross-ref only |

**Coverage summary**: 3 fully covered, 3 now documented below, 5 cross-referenced to existing analysis (including CLI-Anything as a notable community plugin).

## Plugin Details

### Context7

**What it does**: Injects real, up-to-date library documentation into Claude's context via Model Context Protocol (MCP), reducing hallucinations from stale training data ([source][firecrawl-blog]).

**Installation**: `/plugin install context7@claude-plugins-official`

**How it works**:

1. `resolve-library-id` — search for a library by name, get a Context7-compatible ID
2. `get-library-docs` — fetch documentation by library ID, with optional `topic` filter and `tokens` budget

**Setup in this project**: Configured as an MCP server in `.claude/settings.json`. Available libraries include PydanticAI, Pydantic, pytest, Streamlit, loguru, scikit-learn, and others (see [CONTRIBUTING.md context7 section][contributing-c7]).

**Fit assessment**: **Strong adopt.** Already in daily use. Context7 solves the stale-docs problem for rapidly evolving libraries (PydanticAI, Streamlit). The MCP integration means it works in both interactive and headless CC sessions.

**Example usage**:

```bash
# Search for a library
mcp__context7__resolve-library-id --libraryName "pydantic-ai"

# Get focused documentation
mcp__context7__get-library-docs \
  --context7CompatibleLibraryID "/pydantic/pydantic-ai" \
  --topic "agents" --tokens 5000
```

### Code Review

**What it does**: Runs multiple specialized review agents in parallel to analyze code quality, tests, error handling, and type design. Produces structured summaries with confidence scores ([source][firecrawl-blog]).

**Installation**: `/plugin install code-review@claude-plugins-official`

**Author / version**: the two first-party files disagree. `.claude-plugin/plugin.json` lists the author as "Anthropic" (`support@anthropic.com`) and has no version field ([source][cr-plugin-json]); the README's own `## Author` / `## Version` sections instead give "Boris Cherny (`boris@anthropic.com`)" and "1.0.0" ([source][cr-plugin-readme]).

**Usage**: the plugin ships its own `commands/code-review.md` command file, also named `code-review` (frontmatter `description: Code review a pull request`). Because a plugin command is namespaced as `/plugin-name:command-name`, it runs alongside — not in place of — the bundled `/code-review` command documented in [§ `/code-review` command and ultrareview](#code-review-command-and-ultrareview): `claude plugin list` confirms `code-review@claude-plugins-official` is installed here, and the available-skills list (CC 2.1.302, Codespaces, 2026-10-18) carries both `code-review` (the bundled command, long description) and `code-review:code-review` ("Code review a pull request" — this plugin's own description) as separate entries, so the plugin's review runs as `/code-review:code-review`, not bare `/code-review`.

**How it works** ([source][cr-plugin-readme]): a GitHub-PR-only reviewer, requiring the `gh` CLI — distinct from the bundled command, which also reviews a local diff, branch, or path with no GitHub dependency.

- Skips closed, draft, trivial, or already-reviewed PRs
- Gathers `CLAUDE.md` guideline files from the repository
- Launches 4 parallel agents: 2 for CLAUDE.md-compliance auditing, 1 scanning for obvious bugs in the diff, 1 analyzing git blame/history for context
- Scores each issue 0–100 for confidence and filters out anything below 80
- Posts a single review comment with the surviving (≥80-confidence) issues, linking each to `file#Lstart-Lend` at the full commit SHA

**Fit assessment**: **Moderate adopt.** The multi-agent scoring approach aligns with the parallel review pattern documented in [CC-agent-teams-orchestration.md](../agents-skills/CC-agent-teams-orchestration.md). Consider using alongside the bundled `/code-review` (and `ultrareview` for higher-stakes changes) for defense-in-depth — the two don't conflict since they run under different command names.

**Interaction with CC's bash layer**: The plugin's review agents use CC's Bash tool ([source][sdk-bash]) to run linters, type checkers, and test suites as part of their analysis. The persistent bash session (245 input tokens per tool use) means agents can chain `git diff`, `ruff check`, and `pyright` in sequence while maintaining working directory state.

### /code-review command and ultrareview

**Not a plugin.** `/code-review` is a [bundled skill][code-review-local] — built into Claude Code itself, available on any plan, with no `/plugin install` step and no `SKILL.md` on disk to edit. Verified against the live [code-review-local][code-review-local], [ultrareview][ultrareview], and [code-review (managed)][code-review-managed] pages (CC 2.1.302, Codespaces, 2026-10-18). Three distinct offerings share the "code review" name; don't conflate them:

| | Bundled `/code-review` | `code-review@claude-plugins-official` plugin | Managed [Code Review][code-review-managed] service |
|---|---|---|---|
| What it is | Built into Claude Code | Marketplace plugin (above) | GitHub App + Anthropic-hosted pipeline |
| Invocation | `/code-review` (alias `/review`) | `/code-review:code-review` (namespaced) | Automatic on PR activity, or `@claude review` comment |
| Targets | Diff, PR, branch, or path | GitHub PR only | GitHub PR only |
| Who can use it | Anyone, any plan | Anyone who installs the plugin | Team/Enterprise orgs, once an Owner turns it on |
| Depth control | Effort level `low`–`max`, or `ultra` | 4-agent pipeline, confidence≥80 threshold (editable in the command file) | Quick / Standard / Deep review level |
| Reads `REVIEW.md` | No | Not documented in its README | Yes |

**What `/code-review` does**: reviews the current diff, a PR, a branch, or a path for correctness bugs (plus reuse/simplification/efficiency cleanup, depending on model and effort level), and reports findings in the conversation; `--fix` applies them, `--comment` posts them to the GitHub PR or GitLab MR. It follows the project's `CLAUDE.md` but does not read `REVIEW.md` (that file configures the managed service below). `/review` is an alias since **CC v2.1.223**; before that it was a separate single-pass read-only GitHub-PR reviewer. The command was named **`/simplify`** before **CC v2.1.147**; `/simplify` still exists as a narrower, correctness-blind cleanup command. Full targets table, effort levels, and flags: [CC-tools-inventory.md § `/code-review`, `/review`, `/simplify`, and ultrareview](../configuration/CC-tools-inventory.md#code-review-review-simplify-and-ultrareview).

**`ultrareview`** (`/code-review ultra`, alias `/ultrareview`) escalates to a **research-preview** cloud review. "Ultrareview is a deep code review that runs as a cloud session on Anthropic's infrastructure." It launches a fleet of reviewer agents whose findings are independently reproduced and verified before they're reported — higher signal than the local review's effort-level scaling, at the cost of a cloud round trip. It is **user-started only**: Claude never launches it on its own, and a scheduled `/code-review` task never escalates to `ultra`. It bills against usage credits once the three free runs on Pro and Max are used, "typically $5 to $25 in usage credits depending on the size of the change". "A review typically takes 15 to 25 minutes." A branch review defaults to up to 500 changed files / 8,000 changed lines; a PR review targets a `github.com` PR number. It is unavailable on Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, Zero Data Retention, and HIPAA-configured orgs (falls back to a local review in those cases), and organizations using customer-managed encryption keys (CMEK) can't run it at all — no automatic fallback is documented for CMEK. Details: [CC-tools-inventory.md § ultrareview](../configuration/CC-tools-inventory.md#code-review-review-simplify-and-ultrareview).

**Fit assessment**: **Adopt by default for `/code-review`** — it needs no install and runs on any plan, so there's no reason not to use it alongside, or instead of, the `code-review@claude-plugins-official` plugin above. **Escalate to `ultrareview` selectively** for substantial, pre-merge changes, given its cost and ~15–25 minute turnaround; it is not a substitute for the fast local loop. Adopt the managed [Code Review][code-review-managed] service separately if this org is on Team/Enterprise and wants review to run automatically on every PR without a local session.

### Security Guidance

**What it does** (v2.0.21, checked at source 2026-11-22; Apache-2.0; author David Dworken, Anthropic): three review layers for code Claude writes ([README][sg-readme], [hooks.json][sg-hooks]):

1. **Pattern warnings**: regex reminders on about 25 known-dangerous patterns (for example `yaml.load`, `pickle.load` on untrusted data, raw `innerHTML`, hardcoded secrets). They run as a `PostToolUse` hook on `Edit`, `Write`, `MultiEdit` and `NotebookEdit`, so they warn after the edit lands; they don't block it. Each pattern warns once per file per session. No credentials needed.
2. **LLM diff review on Stop**: when a turn ends, the diff since the prompt goes to a model (the newest Opus by default) and high-severity findings come back to Claude as a background (`asyncRewake`) message.
3. **Agentic commit and push review**: after `git commit`, `git push` or Graphite's `gt create` / `gt modify`, an Agent SDK reviewer reads related files (`Read`/`Grep`/`Glob`) to trace data flow across files (IDOR, auth bypass, cross-file SSRF). Capped at 20 commit and 20 push reviews per session per rolling hour by default (`MAX_COMMIT_REVIEWS_PER_HOUR`).

The README names the classes covered as common web vulnerabilities: injection, XSS, SSRF, hardcoded secrets, IDOR, auth bypass, unsafe deserialization and path traversal, among others.

**Installation**: `/plugin install security-guidance@claude-plugins-official`. Needs Claude Code 2.1.144 or later and Python 3.8+ on `PATH`.

**Hooks on every session, not only on edits** ([hooks.json][sg-hooks], [hook source][sg-hook-src]): `SessionStart` bootstraps the Agent SDK (180 s timeout); `UserPromptSubmit` runs on every prompt and records a git baseline commit, plus a snapshot of untracked files that only the Stop review reads; `PostToolUse` matches edits and `git` commands; `Stop` starts the diff review. The baseline is taken even with the reviews off, because the `Write` pattern filter reads it; `ENABLE_STOP_REVIEW=0` or `ENABLE_CODE_SECURITY_REVIEW=0` skips the untracked snapshot.

**Credentials and cost**: the two LLM layers use the first credential that reaches the plugin: a cloud provider config (Bedrock, Vertex, Foundry), `ANTHROPIC_API_KEY` or `ANTHROPIC_AUTH_TOKEN`, the Claude Code sign-in, or a Claude apps gateway sign-in. Claude Code passes no sign-in to plugins in a session started with `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, `DISABLE_TELEMETRY` or `DO_NOT_TRACK`; with no credentials the LLM reviews are skipped and only the pattern warnings run. Reviews cost tokens or subscription usage on top of the session; on the Anthropic API path the Stop review calls the API directly, so it doesn't show in Claude Code's own cost figures. Each review writes a `Review usage:` line with an estimated cost to `~/.claude/security/log.txt`. Cheaper models: `SECURITY_REVIEW_MODEL` (diff review) and `SG_AGENTIC_MODEL` (commit review). Diffs, related file contents and `claude-security-guidance.md` policy files go to the configured model endpoint.

**Switches** (environment variables, [README][sg-readme]):

| Variable | Effect |
|---|---|
| `SECURITY_GUIDANCE_DISABLE=1` | Turns the whole plugin off |
| `ENABLE_PATTERN_RULES=0` | Turns off the pattern warnings |
| `ENABLE_CODE_SECURITY_REVIEW=0` | Turns off both LLM reviews (Stop and commit/push) and the no-credentials notice |
| `ENABLE_STOP_REVIEW=0` | Stop review only; the README suggests it for multi-agent or shared-worktree setups, where another agent can move `HEAD` between turns |
| `ENABLE_COMMIT_REVIEW=0` | Commit/push review only |

**Owner observation (2026-11-22, one Codespace, not a benchmark)**: only the pattern warnings worked. The plugin's log reported "no API credentials and no Claude apps gateway sign-in" for the LLM reviews, and the Agent SDK bootstrap had timed out. The `UserPromptSubmit` hook still ran on every prompt: 67 runs on 2026-11-22, median 0.6 s, slowest 7.8 s. Across the session transcripts, 68 runs timed out in all, most of them between 2026-11-11 and 2026-11-15 and 3 since 2026-11-16, so it is not a current hotspot. The snapshot works on a temporary copy of the git index, so lock contention with other sessions is unlikely; the cause of the earlier timeouts is not known.

**Fit assessment**: **Adopt the pattern warnings; turn the LLM reviews on per repo.** Where no credentials reach the plugin, set `ENABLE_CODE_SECURITY_REVIEW=0`: the reviews can't run there, and the switch also drops the per-prompt untracked-file listing (the per-prompt baseline of tracked files still runs). Where several agents share a worktree, the README's switch is `ENABLE_STOP_REVIEW=0`, which keeps the commit and push reviews. Where the reviews do run, they catch multi-file issues that regexes miss, at the cost of a model call when a turn ends and one review per commit or push (Opus by default; set a cheaper model to spend less). It complements, not replaces, tests and SAST (the README's own limitation). The earlier version of this section described a `PreToolUse` hook that blocked edits on 9 patterns with no cost outside edits ([Firecrawl blog][firecrawl-blog]); v2.0.21 does none of these.

**Interaction with CC's bash layer**: the pattern layer covers edit tools only, not `Bash`; the `Bash` hooks start commit and push reviews and don't block commands. For blocking dangerous commands, use CC's permission model (`Bash(pattern:*)` syntax, see [CC-bash-mode-analysis.md](../configuration/CC-bash-mode-analysis.md)).

### Figma MCP

**What it does**: Reads Figma design files directly and generates functional front-end code from design data — frames, components, and layout ([source][firecrawl-blog]).

**Installation**: `/plugin install figma@claude-plugins-official`

**Fit assessment**: **Skip unless UI work.** Targets design-to-code workflows for front-end projects. Not relevant for CLI/API/backend projects. Adopt if the project adds a web UI with Figma-designed components.

### Frontend Design

**What it does**: Applies stronger design judgment to Claude's UI generation — intentional typography, distinctive palettes, professional spacing. Avoids generic AI-generated defaults ([source][firecrawl-blog]).

**Installation**: `/plugin install frontend-design@claude-plugins-official`

**Fit assessment**: **Skip unless frontend project.** A skills-based plugin that adjusts Claude's design sensibility. No backend or API relevance. Adopt if building user-facing web interfaces where visual quality matters.

**Disambiguation — three Anthropic "design" offerings.** Don't conflate: **`frontend-design`** (the CC plugin above — adjusts UI-generation sensibility); the **`design`** plugin ([claude.com/plugins/design][design-cowork]), a **Claude Cowork** plugin for design critique, UX microcopy, WCAG 2.1 AA accessibility audits, research synthesis, and dev handoff; and **Claude Design** (`claude.ai/design`), an Anthropic Labs research-preview *product* (Opus 4.7 vision; designs, prototypes, slides) that packages a build bundle for handoff to Claude Code ([announced 2026-04-17][labs-design]). The first two are plugins; the third is a standalone product, not a plugin.

### Linear

**What it does**: Connects Claude to Linear issue tracker — pull issues, summarize tickets, mark in-progress, break into subtasks ([source][firecrawl-blog]).

**Installation**: `/plugin install linear@claude-plugins-official`

**Fit assessment**: **Adopt if using Linear for project management.** Enables issue-driven development without leaving CC. The auto-status-update (mark in-progress when starting work) reduces context switching. Not relevant if using GitHub Issues, Jira, or other PM tools.

### Code Modernization

**What it does**: Guided, command-driven modernization of a legacy codebase: an assessment, an interactive dependency/data-flow map, business rules mined as Given/When/Then cards with `file:line` citations, a phased plan a person approves, then a same-version uplift, a rewrite, or a clean-architecture rebuild — each followed by an independent proof step that computes a PROVEN / PARTLY PROVEN / NOT PROVEN verdict per module from files a script parses itself, not from the model's own report ([source][cm-readme]).

**Installation**: `/plugin install code-modernization@claude-plugins-official`

**Author / version / license**: Anthropic; version 1.0.0; Apache 2.0, verified from the plugin's own `LICENSE` file, not marketing copy ([source][cm-plugin-json], [source][cm-license]).

**How it works** — 9 commands, each writing only to `analysis/<name>/` or `modernized/` and never editing the legacy source (a `.claude/settings.json` deny rule the plugin's own `preflight` step checks for) ([source][cm-readme]):

| Step | Command | Output |
|---|---|---|
| 0 | `modernize` | `INTENT.md` — the front door every later command reads |
| 1 | `modernize-preflight` | Five person-answered questions, a build smoke test, missing-source check |
| 2–4 | `modernize-assess`, `-map`, `-extract-rules` | Assessment, dependency/data-flow map, business-rule cards |
| 4b | `modernize-review` | A person confirms or corrects flagged rules |
| 5 | `modernize-brief` | The phased plan — **nothing is built before a person approves it** |
| 6 | `uplift` / `transform` / `reimagine` | The build, by the chosen track |
| 7 | `modernize-verify` | The independent proof, one verdict per module |
| 8 | `modernize-harden` | A security scan with a reviewed, hand-applied patch |

**Proof, not self-report**: `modernize-verify` re-runs the full test suite from a clean build, re-runs old and new code on the same inputs with a script comparing every byte (a declared tolerance for floating-point output), invents at least ten new inputs nobody used, and requires a deliberate one-line "canary" break to prove the tests can fail before trusting them. `scripts/proof_pack.py` computes the verdict from those result files; "every verdict is computed again from current evidence each time; none is carried over from an earlier run" ([source][cm-readme]).

**What it has been tried on**: the README lists real, headless, public-codebase runs with their own numbers — AWS CardDemo (COBOL→Java), Eclipse Jetty (Java 8→17, 946/996 matching tests on both versions), osCommerce (PHP→Python/FastAPI), AngularJS RealWorld, JPetStore, beets (Python 2→3), Spring PetClinic, Redmine/eShop/Jenkins, NetHack/KISS FFT/BSD numbers, and a deliberately booby-trapped codebase whose planted prompt-injection attempts were logged and never acted on ([source][cm-readme]). These are the plugin's own self-reported runs, not independently reproduced here.

**Telemetry**: whole-number usage counts only (which command ran, how far a system got, OS/python status, failure-kind codes) through Claude Code's own telemetry setting — nothing is sent when that is off — and separately switchable via the plugin's own **Usage counts** option or `CODE_MODERNIZATION_TELEMETRY=0` ([source][cm-readme]).

**Fit assessment**: **Adopt for a scoped legacy-modernization pilot, not a whole-estate migration** — the README itself says to start with one module or unit. The proof step (re-run-from-clean, adversarial new inputs, a required canary) stands out: it targets exactly the "passes the tests someone wrote, differs on the ones nobody wrote" failure mode other migration tooling in this corpus doesn't check for. See [code-migration-kit-with-claude-code][cm-related] for a lower-level prompt/template toolkit Anthropic ships separately for the same problem space.

**Rubric** (scored 2026-10-02, from the plugin's own README, CHANGELOG, LICENSE, and `.claude-plugin/plugin.json`):

`subject: plugins`

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
|  no data (no CONTRIBUTING file or PR template found in `claude-plugins-official`; its README's own "Contributing" section documents a submission flow for `external_plugins/` only — `code-modernization` is an internal plugin, "developed by Anthropic team members," with no equivalent external contribution flow documented) | no data (same reason as Shared) | partial [cm-readme][cm-readme] (the proof step is deterministic: verdicts are computed by `scripts/proof_pack.py` and "Every verdict is computed again from current evidence each time; none is carried over from an earlier run". But the analysis and the rewrite run "as agents" with no pinned model, the rubric's "pinned code but unpinned model" case; re-scored 2026-10-02) | yes [cm-plugin-json][cm-plugin-json] (six `userConfig` options — `system`, `track`, `panel`, `xray`, `commandPrefix`, `legacyDir`, `telemetry` — change behavior with no code edit) | partial [cm-readme][cm-readme] ("the commands never commit to your repository, so commit `analysis/` and `modernized/` yourself" — the plugin's outputs are explicitly meant to be git-tracked, but nothing in the plugin commits or versions them itself) | yes [cm-readme][cm-readme] (business rules cite `file:line` in the legacy source; the proof step's masked fields, accepted differences, and verdicts are all listed in the output rather than asserted; a booby-trapped test codebase's planted instructions were "listed in the report" rather than silently followed)  |

## Applicability Decision Framework

| Project Type | Recommended Plugins | Skip |
|---|---|---|
| **Backend/API** | Context7, Code Review, Security Guidance | Figma, Frontend Design |
| **Full-stack web** | Context7, Code Review, Security Guidance, Figma, Frontend Design | — |
| **Data science/ML** | Context7, Code Review | Figma, Frontend Design, Linear |
| **Open-source library** | Context7, Code Review, Security Guidance | Figma, Frontend Design |
| **Enterprise team** | All above + Linear (if using Linear) | Per project type |

### Decision Rule

**Install Context7 and Code Review for all projects. Add Security Guidance for projects with security-sensitive code (its LLM reviews need credentials that reach the plugin; see [§ Security Guidance](#security-guidance)). Everything else is conditional on project type and tooling choices.**

## Full Ecosystem Inventory

**Source**: [anthropics/claude-plugins-official][cpp-gh] | **Docs**: [plugin-marketplaces][cpp-docs]

The repository has a two-tier structure: `plugins/` (35 Anthropic-internal plugins) and `external_plugins/` (15 partner/community plugins).

### Additional Internal Plugins Not Covered Above

**LSP language servers** (13): `clangd-lsp`, `csharp-lsp`, `gopls-lsp`, `jdtls-lsp`, `kotlin-lsp`, `lua-lsp`, `php-lsp`, `pyright-lsp`, `ruby-lsp`, `rust-analyzer-lsp`, `swift-lsp`, `typescript-lsp` — per-language LSP integrations; install the one matching your stack.

**Dev workflow** (13): `agent-sdk-dev`, `claude-code-setup`, `claude-md-management`, [`code-modernization`](#code-modernization), `code-simplifier`, `commit-commands`, `feature-dev`, `hookify`, `mcp-server-dev`, `mcp-tunnels`, `playground`, `plugin-dev`, `pr-review-toolkit` — scaffolding, migration, hook authoring, MCP development, and PR tooling.

**Session & reporting** (2): `session-report`, `skill-creator` — session summaries and guided skill authoring.

**Output style** (3): `cwc-makers`, `explanatory-output-style`, `learning-output-style` — response style profiles for different audiences.

**Other**: `math-olympiad` — competitive math problem solving.

### External Partners (15)

`asana`, `context7`, `discord`, `fakechat`, `firebase`, `github`, `gitlab`, `greptile`, `imessage`, `laravel-boost`, `linear`, `playwright`, `serena`, `telegram`, `terraform`

### Skill-Bundle Packaging Format

Repos shipping `SKILL.md` files without a `plugin.json` can use `"strict": false` alongside an explicit `skills` array in their plugin manifest. Each skill registers as `<plugin-name>:<skill-name>` inside CC.

### Discovery and Submission

- Browse the marketplace: `/plugin > Discover` in CC
- Submit a third-party plugin: [clau.de/plugin-directory-submission][cpp-submit]

[cpp-gh]: https://github.com/anthropics/claude-plugins-official
[cpp-docs]: https://code.claude.com/docs/en/plugin-marketplaces
[cpp-submit]: https://clau.de/plugin-directory-submission

## Already Covered Plugins

These plugins have full analysis elsewhere in this repo:

- **Firecrawl** — [CC Web Scraping Plugins Analysis](CC-web-scraping-plugins-analysis.md)
- **Playwright** — [CC Web Scraping Plugins Analysis](CC-web-scraping-plugins-analysis.md)
- **Chrome DevTools MCP** — [CC Web Scraping Plugins Analysis](CC-web-scraping-plugins-analysis.md)
- **Ralph Loop** — [CC Ralph Enhancement Research](../agents-skills/CC-ralph-enhancement-research.md)
- **CLI-Anything** (community) — [CC CLI-Anything Analysis](../agents-skills/CC-cli-anything-analysis.md)

## Community Resources

### Official Documentation

- [CC Best Practices][cc-best-practices]
- [CC Plugins docs][cc-plugins]
- [CC Skills docs][cc-skills]

### Community Guides and Catalogs

- [awesome-claude-code][awesome-cc] — skills, hooks, commands, and plugins catalog
- [CC Ultimate Guide][cc-ultimate] — beginner to power user guide with templates and quizzes
- [45 CC Tips (ykdojo)][cc-tips] — custom statusline, system prompt reduction, dx plugin
- [CC Best Practice][cc-best-practice-gh] — curated best practices collection
- [Everything Claude Code][everything-cc] — battle-tested configs and patterns

## Not included

Entries removed under the [pruning rule](../../../CONTRIBUTING.md#pruning-entries-well-known-performance-optimised-filter).

| Name | Reason | Date | Link |
|---|---|---|---|
| Cuttlesoft Advanced Tips | Criterion 3: a single vendor blog post (per its URL and this list's own description), with no standards-body, named-user or measured-benefit evidence found; its content was not read, since the page returned 403 to automated fetches on 2026-11-22 | 2026-11-22 | [Cuttlesoft blog post](https://cuttlesoft.com/blog/2026/02/03/claude-code-for-advanced-users/) |

## References

- [Firecrawl blog — Best CC Plugins][firecrawl-blog]
- [CC Plugins docs][cc-plugins]
- [Agent SDK Bash tool][sdk-bash]
- [CC Bash Mode Analysis](../configuration/CC-bash-mode-analysis.md)
- [CC Web Scraping Plugins Analysis](CC-web-scraping-plugins-analysis.md)
- [CC Plugin Packaging Research](CC-plugin-packaging-research.md)
- [code-modernization plugin README][cm-readme]
- [code-modernization plugin.json][cm-plugin-json]
- [code-modernization LICENSE][cm-license]
- [CC code-review-local docs][code-review-local] — bundled `/code-review` command: targets, effort, flags, `/review`/`/simplify` alias history
- [CC ultrareview docs][ultrareview] — ultrareview scope, billing, limits, platform restrictions, research-preview status
- [CC code-review (managed) docs][code-review-managed] — the separate GitHub-App PR-review service (Team/Enterprise)
- [code-review plugin README][cr-plugin-readme] — 4-agent / confidence-scoring architecture, author, version
- [code-review plugin.json][cr-plugin-json] — plugin manifest (name, description, author)
- [security-guidance plugin README][sg-readme] — three layers, credentials, switches, privacy, review cost log (v2.0.21, 2026-11-22)
- [security-guidance hooks.json][sg-hooks] — hook events, matchers and timeouts (v2.0.21, 2026-11-22)
- [security-guidance hook script][sg-hook-src] — `UserPromptSubmit` baseline and untracked-snapshot gating (v2.0.21, 2026-11-22)
- Owner observation, 2026-11-22 — the plugin's local debug log and hook timings in one Codespace
- CC 2.1.302, this session, 2026-10-18 — observed that the installed `code-review` plugin's skill is listed separately as `code-review:code-review` alongside the bundled `code-review` skill

[firecrawl-blog]: https://www.firecrawl.dev/blog/best-claude-code-plugins
[cc-plugins]: https://code.claude.com/docs/en/plugins
[cc-skills]: https://code.claude.com/docs/en/skills
[cc-best-practices]: https://code.claude.com/docs/en/best-practices
[sdk-bash]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool
[contributing-c7]: https://github.com/qte77/Agents-eval/blob/main/CONTRIBUTING.md#context7-mcp-documentation-access
[awesome-cc]: https://github.com/hesreallyhim/awesome-claude-code
[cc-ultimate]: https://github.com/FlorianBruniaux/claude-code-ultimate-guide
[cc-tips]: https://github.com/ykdojo/claude-code-tips
[cc-best-practice-gh]: https://github.com/shanraisshan/claude-code-best-practice
[everything-cc]: https://github.com/affaan-m/everything-claude-code
[design-cowork]: https://claude.com/plugins/design
[sg-readme]: https://github.com/anthropics/claude-plugins-official/blob/main/plugins/security-guidance/README.md
[sg-hooks]: https://github.com/anthropics/claude-plugins-official/blob/main/plugins/security-guidance/hooks/hooks.json
[sg-hook-src]: https://github.com/anthropics/claude-plugins-official/blob/main/plugins/security-guidance/hooks/security_reminder_hook.py
[labs-design]: https://www.anthropic.com/news/claude-design-anthropic-labs
[cm-readme]: https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-modernization/README.md
[cm-plugin-json]: https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-modernization/.claude-plugin/plugin.json
[cm-license]: https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-modernization/LICENSE
[cm-related]: https://github.com/anthropics/code-migration-kit-with-claude-code
[code-review-local]: https://code.claude.com/docs/en/code-review-local
[ultrareview]: https://code.claude.com/docs/en/ultrareview
[code-review-managed]: https://code.claude.com/docs/en/code-review
[cr-plugin-readme]: https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-review/README.md
[cr-plugin-json]: https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-review/.claude-plugin/plugin.json
