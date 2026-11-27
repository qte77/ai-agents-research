---
title: Hypergraphs and layered graphs, GitHub platform and alternatives, 2026-11-27 sources
status: approved
issue: "#1071"
created: 2026-11-27
updated: 2026-11-27
---

Tracking issue: #1071 (kept from plan 0017). Successor to
[plan 0017](2026-11-26-0017-graph-encoding-enterprise-apis.md): its open rows moved here unchanged
and keep their IDs, so there is one live plan, and `make reconcile`, which reads only the newest plan,
checks all of it.

## Current status

**Read this first: what to do next and how.**

- **Shipped before this plan:** every plan 0017 agent row (#1110 to #1117, #1120), and release
  v0.28.0 (#1118).
- **Opened 2026-11-27** from the owner's three asks of that day: (1) deepen hypergraphs and
  multi-dimensional, layered relationships in graphs; (2) GitHub capabilities and its competition;
  (3) fold in a list of sources, plus three Pydantic AI coding-agent sources sent later that day. Defaults for every open decision are in
  [§ Owner decisions](#owner-decisions-2026-11-27); the owner can override any of them.
- **In flight:** nothing.

**Next, in order** (rows in [§ Remaining work](#remaining-work)):

1. **Wave 1, three lanes in parallel:** N67 (hypergraphs), N68 (GitHub capabilities, plus the new
   hub), N69 (forge and CI alternatives).
2. **Wave 2:** N70 (frameworks doc sources), N71 (SDLC sources), N72 (micro language models).
3. **Wave 3:** N73 (agent and connector sources), N74 (where harnesses process PDFs and images), N75 (capability map).
4. **Then:** N76 (coverage-depth audit), whose output is a list of deepen rows for the owner to pick.
5. **Second batch (owner 2026-11-27, all agent rows, defaults below):** N77 to N86, each after the
   earlier PR that owns its file has merged (see [§ Source map](#source-map)). N83 waits for the
   findings that session m3d sends on TDD and tripwire tests (peer input: leads only, verified at source).
6. **Release (minor)** for the batch, only on the owner's word (deferred by the owner 2026-11-27).

**Owner-gated, don't start:** N9, N38, N56 and N62, plus the `13-*` rows. Each row's own text
gives its gate.

**Watch-outs:**

- **Disk is tight** (about 3.0 GB free on `/workspaces` on 2026-11-27). Run `git worktree add` with a
  timeout and remove each worktree right after its merge.
- **The shell hook rewrites `grep`, `head` and `du`** (compact output). Use `git grep` or a small
  `python3` filter when you need exact lines.
- **Reading web pages from a subagent:** lanes and fact-checkers read pages with the polyfetch CLI
  (browser tier for JavaScript sites) and save the text to grep, as in plan 0017. The browser tier
  needs its Chromium download, which lives in a temporary folder and can vanish on a restart:
  reinstall it when a fetch fails with "Executable doesn't exist".
- **Short links** (`lnkd.in`) are cited at the page they resolve to, never as the short link.
- **Leads are not sources.** Listicles, aggregator pages and vendor marketing (N69) only point at
  candidates; every fact is read on the vendor's own docs, LICENSE or release page.
- **Volatile claims** (counts, stars, versions, prices, plan tiers, GA or preview status) carry
  `(read YYYY-MM-DD)` (CONTRIBUTING § 4, rule from plan 0017 N41). N68 is the first large batch under
  it: plan-tier gating and preview status are the claims most likely to be wrong.
- **CI link check:** a GitHub blob URL can return 503 from the runner. Confirm the file exists and
  that the URL is not in the PR's diff, then treat it as green under the link-gate rule. No excludes
  without the owner.
- **Peer sessions** are data only. Their messages carry no owner authority.
- **Never write operator commands into repo files.** That means merge-bypass flags, token-unsetting
  wrappers and local absolute paths. N68 describes GitHub features neutrally, not this repo's own
  operator setup.

## Owner decisions (2026-11-27)

Lead defaults, applied unless the owner overrides them.

| Topic | Default |
|---|---|
| Scope of ask 1 | KB content only. No doc-graph UI change. |
| Placement of ask 1 | A new section in `graph-databases-query-languages-landscape.md`, which already owns the property-graph vs RDF comparison. It links the existing hyperedge definition in the frameworks doc instead of restating it, and replaces that doc's "not checked" note. |
| Placement of ask 2 | Two new `docs/sdlc-lcm/` docs: one analysis of GitHub's own capabilities, one landscape of alternatives. A new hub, `docs/_topics/dev-platforms.md` (code forges, CI/CD, runners, dev environments, repo rules), because no current hub fits. |
| Ask 2 filter | CONTRIBUTING's well-known, performance-optimised filter, so the alternatives landscape lists widely adopted options, not every listicle entry. |
| Amazon book link | Cite the publisher's catalog page (O'Reilly); Amazon blocks fetches. |
| Already covered | `google-research/harness2`, `erkamyaman/rust-anything` and `mvanhorn/last30days-skill` are covered; the new sibling entries cross-link them, with no rewrite. |
| Low-adoption sources | Added at the level the evidence supports (for example "a day-old experiment"), or listed in the disposition table with a reason. None is dropped silently. |
| Tracker | #1071 stays the tracking issue. |
| Second batch (owner, 2026-11-27) | Do A (definitions, N77), B (the queue) and C (all three coverage gaps, N78 to N80). Item 1 means the GitHub capabilities doc: list what #1123 added, and map capabilities across forges (N81). Distributed systems: one new landscape in `docs/sdlc-lcm/` (N82). Privacy law: GDPR (EU), UK GDPR, CCPA and Canada, mapped with KB touchpoints, no legal advice (N84). Rotating the exposed tokens and the release are deferred by the owner. |

## The loop

Same loop as [plan 0017 § The loop](2026-11-26-0017-graph-encoding-enterprise-apis.md#the-loop):
one worktree per lane from `origin/main`, Sonnet general-purpose lanes on the
[lane brief](../../.claude/skills/adding-research-source/references/lane-brief.md), two
[falsifier passes](../../.claude/skills/adding-research-source/references/falsifier-briefs.md) per
content PR, the lead adds hub, index and glossary rows, one PR per row, the row struck in its own PR,
serial merges pinned to the reviewed head commit, a progress comment on #1071 after each merge.

No two lanes edit the same file. Each row below owns its files; a source that fits a file another
row owns moves to that row.

## Source map

| Row | Files the row owns | Existing text to link, not repeat |
|---|---|---|
| N67 | `docs/non-cc/infrastructure/graph-databases-query-languages-landscape.md` | § Property Graph vs RDF (edge data, RDF 1.2 triple terms); § Not Verified line on hyperedges (replace); frameworks doc § GraphRAG vs vector RAG and KG construction evidence (hypergraph RAG and memory papers, hyperedge definition); `minigraf-analysis.md` (bi-temporal); frameworks doc § Temporal knowledge-graph memory; `semantic-layers-data-catalog-landscape.md` § Formal Ontologies; Graphify's hyperedges in `CC-code-tooling-landscape.md` |
| N68 | new `docs/sdlc-lcm/github-platform-capabilities-analysis.md`; new hub `docs/_topics/dev-platforms.md` (lead) | `CC-github-actions-analysis.md`, `github-copilot-cloud-agent-analysis.md`, `agent-code-analysis-landscape.md` § 4 CI-Forge Integration, the Codespaces and devcontainer mentions (`git grep -il devcontainer -- docs`) |
| N69 | new `docs/sdlc-lcm/code-forge-ci-alternatives-landscape.md` | `oss-alm-landscape.md` (GitLab CE as an ALM option), N68's doc for GitHub itself |
| N70 | `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` | § 4 Agent memory infrastructure; § GraphRAG vs vector RAG; § 3 Lightweight and specialized frameworks (Harness², rust-anything already there); the PydanticAI bullet in § 1 and the archived `pydantic-ai-harness` Sources row |
| N71 | `docs/sdlc-lcm/agentic-legacy-migration-validation-analysis.md`, `docs/non-cc/reference/weco-aide-recursive-self-improvement-analysis.md`, `docs/sdlc-lcm/agent-evaluation-metrics-landscape.md`, `docs/non-cc/knowledge-management/repo-to-docs-tools-landscape.md` | weco doc § Harness²; frameworks doc rust-anything bullet |
| N72 | new `docs/non-cc/reference/micro-language-models-landscape.md` | `system-1-decision-models-landscape.md` (typed-output classifiers, § Train your own: Unsloth), `on-device-semantic-search-landscape.md` |
| N74 | `docs/non-cc/coding-agents/coding-agents-comparison-landscape.md` | § Input by harness and § Input notes (what each harness accepts); `CC-web-scraping-plugins-analysis.md` § Read Tool: PDF & Image Parsing (Claude Code, poppler-utils); `CC-vlm-screen-sharing-landscape.md` § Claude Code Image Token Economics; `codex-cli-analysis.md` model list (GPT-6.2 Astra) |
| N75 | `docs/cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md` § Cross-Harness Matrix | Its six mechanic rows (tools, sandbox, permissions, compaction, hooks, resume) checked 2026-11-15; `CC-web-auth-setup-analysis.md` § Other Coding CLIs (headless sign-in, billing); the per-harness analysis docs |
| N76 | this plan (audit table), then rows the owner picks | `docs/non-cc/coding-agents/` (25 docs), `docs/cc-native/` (72 docs), `docs/cc-community/` (19 docs) |
| N77 | frameworks doc § RAG patterns at a glance and the hypergraph bullet; `semantic-layers-data-catalog-landscape.md` § Choosing a Structure; `docs/glossary.md` (lead) | Glossary rows for RAG and GraphRAG; § Property Graph vs RDF |
| N78 | `CC-agentic-harness-patterns-analysis.md` § Cross-Harness Matrix (after N75) | The N76 audit table below; each harness's analysis doc |
| N79 | `workflow-frameworks-landscape.md` § Checkpoint and resume matrix | Codex, Gemini CLI and OpenCode rows already there |
| N80 | `coding-agents-comparison-landscape.md`, new § Configuration and policy by harness (after N74) | `CC-managed-settings-fleet-analysis.md`, `CC-env-vars-reference.md` and the other `cc-native/configuration/` docs for Claude Code |
| N81 | `code-forge-ci-alternatives-landscape.md`, new § Capability map (after N69) | `github-platform-capabilities-analysis.md` (GitHub column); `agent-code-analysis-landscape.md` § 4 (code-analysis rows, linked, not repeated) |
| N82 | new `docs/sdlc-lcm/distributed-systems-concepts-landscape.md` | `mas-design-principles.md`, `mas-security-framework.md`, the protocol docs (MCP, A2A), `workflow-frameworks-landscape.md` (durable execution) |
| N83 | new `docs/sdlc-lcm/test-eval-driven-development-landscape.md` | `agent-evaluation-metrics-landscape.md`, `evaluation-data-resources-landscape.md`, `spec-driven-frameworks-landscape.md`, `agentic-engineering-disciplines-landscape.md`, the OpenAI Agents SDK tripwire guardrails in `openai-agents-sdk-analysis.md` |
| N84 | new `docs/sdlc-lcm/privacy-law-touchpoints-landscape.md` | `ai-security-governance-analysis.md` (EU AI Act and frameworks), `agentic-enterprise-os-landscape.md` § Enterprise data APIs for agents, memory and telemetry docs |
| N85 | `agent-skill-evolution-research-landscape.md`, `moss-self-evolving-agent-analysis.md`, `weco-aide-recursive-self-improvement-analysis.md` (after N71) | The weco doc's harness search results table |
| N86 | `agentic-engineering-disciplines-landscape.md`, new § Diverge and converge | The audit of where the KB already uses the idea |
| N73 | `docs/non-cc/agents/computer-use-agents-landscape.md`, `docs/non-cc/orchestrators/orchestrators-landscape.md`, `docs/non-cc/agents/openresearch-analysis.md`, `docs/cc-native/plugins-ecosystem/CC-connectors-overview.md`, `docs/non-cc/agents/ibm-agent-stack-analysis.md` | `agentic-engineering-disciplines-landscape.md` (names IBM Bob once) |

### Source disposition (owner list, 2026-11-27)

Every URL from the owner's list ends in one row, or in "covered".

| Source | Row | Note |
|---|---|---|
| blacksmith.sh; openalternative.co "top 12 alternatives to GitHub"; spacelift.io "GitHub Actions alternatives"; alternativeto.net GitHub Actions | N69 | Leads only, except Blacksmith's own docs for Blacksmith |
| bob.ibm.com (IBM Bob) | N73 | `ibm-agent-stack-analysis.md` |
| github.com/mitkox/qwen38-27b-baremetal-os | N72 | MIT, created 2026-11-26: an experiment, stated as such |
| github.com/awslabs/codekb | N71 | `repo-to-docs-tools-landscape.md` |
| github.com/caviri/rete | N67 | RDF graph in one file, queried with SPARQL |
| arXiv 2611.23476 (GUARD) and 2611.18856 (self-improvement memory) | N71 | Weco recursive self-improvement doc, next to Harness² |
| arXiv 2611.34875 (coding agents' unneeded edits) | N71 | `agent-evaluation-metrics-landscape.md` |
| lnkd.in/d-VG8gCM, resolves to the PandaDoc community post on its Claude connector | N73 | `CC-connectors-overview.md`; a community post, so the connector facts come from PandaDoc's docs |
| anthropic.com/research/migrating-api-to-rust | N71 | Legacy migration validation doc |
| github.blog Scientist (2016; now at `github.blog/developer-skills/application-development/scientist/`) | N71 | Same doc: the shadow-comparison method |
| Amazon listing of *Agentic GraphRAG* (Alcaraz, Julien) | N70 | Cite the O'Reilly catalog page |
| spread.ai Nemotron engineering model story | N72 | Vendor claim |
| arXiv 2604.19642 (micro language models) | N72 | |
| trigma.com micro models guide | N72 | Agency blog: secondary at best |
| gist cedrickchee llama2.c | N72 | Commentary; cite `karpathy/llama2.c` for facts |
| github.com/vectorize-io/hindsight | N70 | § 4 Agent memory infrastructure |
| github.com/erkamyaman/rust-anything | covered | frameworks doc § 3; N71 cross-links it |
| github.com/n8n-io/nod | N73 | `computer-use-agents-landscape.md` |
| lnkd.in/gu5j5cJB, resolves to an OpenResearch shared project ("packing-problems") | N73 | `openresearch-analysis.md` |
| github.com/mvanhorn/last30days-skill | covered | `CC-community-skills-landscape.md` § last30days |
| docs.docker.com/ai/docker-agent | N70 | |
| github.com/google-research/harness2 | covered | weco doc § Harness² and frameworks doc § 3; N71 cross-links it |
| lnkd.in/e5U-gMX6, resolves to Hugging Face's "Scaling Swarms to Thousands of Agents" report | N73 | `orchestrators-landscape.md` |
| martinfowler.com "Building your own CLI Coding Agent with Pydantic-AI" (sent later the same day) | N70 | Next to the Pydantic AI harness entry |
| pydantic.dev docs: Pydantic AI harness, Coder | N70 | Same place |
| pydantic.dev article: Pax, the Pydantic AI coding agent for the terminal (beta) | N70 | Same place; beta status dated |

## Lane tasks

### N67: hypergraphs and layered relationships

Add a section "Higher-order and layered relationships" to the graph-databases doc. Defaults:

- **Data models for relations among more than two things:** hypergraphs (link the existing hyperedge
  definition), property-graph edge properties and intermediate nodes, RDF reification, named graphs
  and RDF 1.2 triple terms (link § Property Graph vs RDF), and databases with native n-ary relations
  (for example TypeDB). One table: model, how an n-ary fact is stored, what queries it.
- **Multi-layer and multiplex graphs:** one node set with several edge types or layers, and how the
  common stores model it (edge labels, named graphs, separate graphs).
- **Time as a layer:** temporal and bi-temporal edges; link minigraf and the temporal KG memory
  section, don't restate them.
- **Libraries** for hypergraph and multi-layer analysis, only well-known ones with a LICENSE read.
- **`caviri/rete`** as a row in the databases table or the section, at its evidence level.
- Replace the § Not Verified line on hyperedges with what was checked.

### N68: GitHub platform capabilities

New analysis doc, every cell from `docs.github.com` or `github.blog` changelog, each plan tier and
preview status with `(read YYYY-MM-DD)`. Sections:

- **Actions and workflows:** hosted and self-hosted runners, larger runners, reusable workflows,
  composite actions, environments and deployment protection, OIDC to clouds, concurrency, merge
  queue.
- **Dev environments:** Codespaces and dev containers (`devcontainer.json`, prebuilds, policies).
- **Rules and enforcement:** branch protection, repository and organization rulesets, push rules,
  required status checks and required workflows, CODEOWNERS, signed commits, custom properties.
- **Org, business and enterprise features:** plan tiers (Free, Pro, Team, Enterprise Cloud,
  Enterprise Server), enterprise managed users, audit log and streaming, policies at enterprise
  level, Advanced Security (secret scanning push protection, code scanning, Dependabot), Copilot
  policies.
- **Agent surfaces:** what an agent can drive (REST and GraphQL APIs, `gh`, the official MCP server,
  Copilot cloud agent); link the existing docs.

The lead creates `docs/_topics/dev-platforms.md` in the same PR and fills it from the existing docs.

### N69: forge and CI alternatives

New landscape doc. Three tables, each row from the vendor's own docs and LICENSE:

- **Code forges:** for example GitLab, Bitbucket, Azure DevOps Repos, Gitea, Forgejo (Codeberg),
  SourceHut, Gerrit.
- **CI/CD systems:** for example GitLab CI, CircleCI, Buildkite, Jenkins, Azure Pipelines,
  Woodpecker, Dagger, TeamCity; IaC-focused ones (for example Spacelift) noted as a separate kind.
- **Faster runners for GitHub Actions:** Blacksmith and its peers (for example Depot, Namespace,
  RunsOn, Ubicloud). Speed and price claims are vendor claims, `(read YYYY-MM-DD)`.

Columns: licence or hosting model, self-hosted option, agent surface (API, MCP server, coding-agent
integration), migration path from GitHub. The well-known, performant filter decides inclusion; the
four lead pages are cited as leads, not as evidence.

### N70: frameworks doc sources

- **Hindsight** (`vectorize-io/hindsight`) in § 4 Agent memory infrastructure.
- **Docker Agent** (Docker docs) in § 3 or the closest section; say which.
- ***Agentic GraphRAG*** (O'Reilly) as a book pointer in § GraphRAG vs vector RAG; catalog facts
  only (authors, publisher, date as listed).
- **Pydantic AI coding agents:** the harness's Coder docs, the Pax beta article and Martin Fowler's
  article on building a CLI coding agent with Pydantic AI, next to the existing Pydantic AI harness
  entry (archived `pydantic/pydantic-ai-harness`, development moved into `pydantic/pydantic-ai`).
  Beta status dated; Fowler's article cited as a practitioner write-up.

### N71: SDLC sources

- **Legacy migration doc:** Anthropic's Messages API migration to Rust and GitHub's Scientist as a
  method (run old and new side by side, compare results); cross-link rust-anything.
- **Weco recursive self-improvement doc:** GUARD (2611.23476) and the self-improvement memory paper
  (2611.18856), each as its own dated section like the existing ones; cross-link Harness².
- **Evaluation metrics landscape:** the over-edit study (2611.34875) in the closest coding-agent
  quality section; say which.
- **Repo-to-docs landscape:** `awslabs/codekb`.

### N72: micro language models

New landscape doc: what micro and small language models are for in agent systems (instant replies,
on-device, edge, routing), with arXiv 2604.19642, SPREAD's fine-tuned Nemotron (vendor claim),
`karpathy/llama2.c` (via the cedrickchee gist, cited as commentary), `mitkox/qwen38-27b-baremetal-os`
(experiment) and the Trigma guide only if it adds a fact a primary source backs. Link the System-1
decision models doc instead of repeating it.

### N73: agent and connector sources

- **n8n nod** in `computer-use-agents-landscape.md`.
- **Hugging Face swarms report** in `orchestrators-landscape.md`.
- **OpenResearch shared project** as an example in `openresearch-analysis.md`.
- **PandaDoc's Claude connector** in `CC-connectors-overview.md`, facts from PandaDoc's docs.
- **IBM Bob** in `ibm-agent-stack-analysis.md`.

### N74: where harnesses process PDFs and images

Owner questions 2026-11-27: where do Claude Code, Codex and Gemini CLI parse PDFs and process images
(on the user's machine or on the provider's servers), with which packages; and does OpenAI's GPT-6.2
Astra take video as well as images? New section "Where media is processed" in the comparison
landscape. Defaults:

- **Sources:** vendor docs first; for open-source harnesses (Codex CLI, Gemini CLI, OpenCode, Cline,
  Aider) the source code at a named release tag (manifest files such as `Cargo.toml` and
  `package.json`, and the code that reads an image or PDF). Claude Code is closed source: use its docs
  and the corpus's leak provenance standard; mark anything else unverified.
- **Per harness:** what happens locally (resize, re-encode, text extraction, page rendering) and what
  is sent to the model API as an image or document block; the package that does the local step.
- **Model side:** which API input types the harness's default models accept (images, PDFs, video),
  from the provider's model pages; GPT-6.2 Astra's modalities from OpenAI's own model page, dated.

### N75: capability map

Extend the Cross-Harness Matrix with rows for the mechanics it lacks, keeping its five columns
(Claude Code, Codex CLI, Gemini CLI, OpenCode, Pi): instruction and memory files, skills, plugins or
extensions, subagents, MCP configuration, headless and CI mode, cloud or remote runs. Cells from
vendor docs, dated; "not documented" where the docs are silent. Don't refresh the existing rows.

### N76: coverage-depth audit

Owner question 2026-11-27: does the KB cover Codex, Gemini CLI and the other top coding harnesses
as deeply as Claude Code? One table in this plan: harness × the topic areas the `cc-native/` folders
cover (configuration, context and memory, agents and skills, plugins, sandboxing, sessions, CI and
remote), each cell the doc or section that covers it, or a gap. Top-10 by the comparison landscape's
rows. Done when the table is in the plan and each gap the owner picks is its own row.

**Audit result (2026-11-27).** Claude Code has 5 to 19 docs per `cc-native/` area; Codex CLI and Gemini CLI
come next through shared matrices plus one doc each; the other eight top harnesses get one analysis doc each
plus the compaction and auth tables. Cell key: **M** = [Cross-Harness Matrix](../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md#cross-harness-matrix-checked-2026-11-15)
(CC, Codex, Gemini, OpenCode, Pi only); **CMP** = [comparison landscape § Context compaction by harness](../non-cc/coding-agents/coding-agents-comparison-landscape.md);
**AUTH** = [CC-web-auth-setup-analysis.md § Other Coding CLIs](../cc-native/ci-remote/CC-web-auth-setup-analysis.md);
**CKPT** = [workflow frameworks § Checkpoint and resume matrix](../non-cc/frameworks/workflow-frameworks-landscape.md);
**own** = the harness's own analysis doc. "Gap" = no hit in the scopes searched (headings of the ten harness
docs, keyword counts, harness-name hits across `docs/`); counts are rough, so a gap is a lead, not a proof.

| Harness | configuration | context-memory | agents-skills | plugins-ecosystem | sandboxing | sessions | ci-remote | cc-community |
|---|---|---|---|---|---|---|---|---|
| Codex CLI | M (hooks 14, settings); own § Key features, Providers; `CC-model-provider-configuration.md` (8 mentions) | M (AGENTS.md, compaction); CMP | M (`/plan`, subagents "isolation not verified"); own 2 subagent and 1 skill mentions (thin) | thin: M (MCP via config.toml); `non-cc/protocols/openai-apps-plugins-analysis.md` covers the OpenAI plugin side | **own § Approval modes and sandboxing**; M | M (resume); CKPT ("restore unstated, unverified"); own § Interactive vs headless | AUTH; own § Interactive vs headless; `CC-github-actions-analysis.md` (OpenAI Codex Action row); `CC-remote-access-landscape.md` (8 mentions) | Dedicated: `CC-codex-plugin-cc-analysis.md`; also `CC-community-tooling-landscape.md`, `CC-memory-tooling-landscape.md`, `CC-community-skills-landscape.md` |
| Gemini CLI | M (hooks 11); own § Architecture and model access, Release cadence | M (GEMINI.md, `/compress`); own § Context and memory; CMP | M ("`/agents` exists, isolation not verified"); gap in own doc (0 subagent or skill mentions) | thin: own (1 MCP line); M | thin: M (opt-in `-s`); own has 1 mention; `CC-sandbox-platforms-landscape.md` lists it under "Documented integrations" | M; CKPT (`~/.gemini/tmp/.../chats`, 30-day cleanup); own § Headless | AUTH; own § Headless / scripting mode | thin: `CC-community-skills-landscape.md` (5 mentions) |
| GitHub Copilot CLI (doc at `non-cc/agents/github-copilot-cli-analysis.md`) | thin: own § Install and invoke | CMP (~80% background compaction); own § Sessions, memory, auth | own § Built-in agents, Extensibility (MCP, custom agents, instructions); not in M | own § Extensibility; own § Copilot SDK | own § Permissions, sandboxing, autonomy | own § Sessions, memory, auth; gap in CKPT | AUTH; own; `CC-github-actions-analysis.md` (Copilot Coding Agent row, line 340); `non-cc/infrastructure/cloud-agent-platforms-landscape.md`; `non-cc/sdlc-lcm/github-platform-capabilities-analysis.md` | thin: `CC-community-tooling-landscape.md`, `CC-memory-tooling-landscape.md` (3 to 4 mentions) |
| VS Code Copilot Chat | gap (0 settings or config mentions in own doc) | CMP; own: no memory section (0 mentions) | thin: own § Agent Mode (1 skill line) | own § Interfaces (MCP, extensions) | gap (0) | thin: own (session mentions only); gap in CKPT | thin: own § Headless / CLI Surface (points to the separate Copilot CLI doc); `CC-github-actions-analysis.md` (1 mention) | gap |
| Cursor | thin: own § Model selection; AUTH covers only the CLI | CMP ("not documented"); own § Extensibility (rules) | own § Extensibility (rules, skills, SDK with nested subagents); `CC-skills-adoption-analysis.md` (1 mention) | own § Extensibility (MCP, marketplace); `non-cc/protocols/agent-plugins-standard-analysis.md` (Cursor plugin manifest namespace); `CC-community-skills-landscape.md` (14 mentions) | thin: own (headless "lacks the sandboxing and permissions model") | own § Agent mode (checkpoints); gap in CKPT | AUTH; own § CLI (`agent`); `CC-remote-access-landscape.md` (5 mentions) | Several: `CC-code-tooling-landscape.md` (16 mentions), `CC-community-skills-landscape.md` (14), `CC-memory-tooling-landscape.md` (10) |
| Cline | gap | CMP; own § How It Works (`.clinerules`) | thin: own § How It Works (Plan/Act, kanban board "unverified"); no subagent coverage (0) | own § How It Works (MCP) | thin: own (approval prompt per destructive action only) | gap | thin: AUTH (2 mentions); own (cron-based scheduling) | thin: `CC-code-tooling-landscape.md` (4 mentions) |
| Aider | thin: own § Additional capabilities | CMP; own § Codebase mapping (repo map) | gap | gap (0 MCP or plugin mentions) | thin: own comparison table ("None built-in") | thin: own (`/clear`, `/reset` only); own: no cross-session memory | gap in AUTH; own § Additional capabilities | thin: `CC-code-tooling-landscape.md` (2 mentions) |
| OpenCode | M; own § Configuration and extensibility; `CC-model-provider-configuration.md` (12 mentions) | M (AGENTS.md, auto compaction); CMP | M (`subagent` permission, `general` and `explore` agents); own § Dual-agent system; `CC-agent-teams-orchestration.md` (4 mentions) | own § MCP support; own § Configuration and extensibility | gap in own doc (0 sandbox); M (per-resource permission rules) | CKPT (DB path only, "resume unverified"); gap in own doc (1 mention) | AUTH; own § Headless / non-interactive mode; `CC-remote-access-landscape.md` (4 mentions) | Several: `CC-community-tooling-landscape.md` (10), `CC-memory-tooling-landscape.md` (11), `CC-code-tooling-landscape.md` (9) |
| Amp | thin: own § Pricing model | CMP ("not documented" on all three columns); own has an AGENTS.md mention | thin: own § Architecture and modes (1 subagent mention) | own § Extensibility (MCP, TypeScript plugins) | gap | gap | own § CLI and headless operation; gap in AUTH | gap (`CC-1x-session-schema.md` has 8 "amp" hits but not about this harness; I did not read them) |
| Windsurf | gap (0 settings mentions) | CMP ("not documented"); gap in own doc (0 memory mentions) | own § Agent Command Center (multiple local and cloud agents); thin on subagents | thin: own (extension mentions) | gap | thin: 2 mentions | own § Headless / CLI mode; gap in AUTH | gap (`CC-memory-tooling-landscape.md` has 3 mentions, not read) |

Gaps and where they went (owner decision 2026-11-27, "do C"): (1) matrix lacks seven harnesses → N78;
(2) sessions and resume weakest → N79; (5) configuration and policy uneven → N80. The rest stay open for
the owner to pick: per-harness sandboxing depth (3), hooks, skills and subagents in the harnesses' own docs (4),
auth-table and community coverage (5) → row N87.

### N86 audit: diverge and converge

Where the KB describes (M) or itself does (D) a broad exploratory phase followed by a narrow one, found
2026-11-27 by `git grep -i` over `docs/` for converg, diverg, fan-out, fan-in, best-of, MCTS, tree search,
brainstorm, Propose-Probe-Compose, plan mode, self-consistency and majority vote. About 45 of 100 "converg"
hits use the word in another sense (convergence of practice, git "diverged") and are left out. No hits for
beam search, tree of thought, breadth-first or depth-first. Phases named = the doc labels both halves.

| Place | M or D | Phases named |
|---|---|---|
| `cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md` Explore-Plan-Act; Fork-Join | M | yes |
| `cc-native/agents-skills/CC-dynamic-workflows-analysis.md` `/deep-research` fan-out, cross-check, vote | M | yes |
| `cc-native/agents-skills/CC-output-verification-analysis.md` adversarial verify, per-claim voting | M | partly |
| `non-cc/knowledge-management/research-agents-landscape.md` fan-out, cross-check, synthesis | M | yes |
| `non-cc/frameworks/workflow-frameworks-landscape.md` parallelization, orchestrator-workers | M | yes |
| `cc-community/CC-community-skills-landscape.md` Superpowers stages; `idea-refine` (the only use of "divergent/convergent" for this pattern); fan-out research skill | M | partly to yes |
| `cc-community/CC-office-worker-workflows.md` Vibe Kanban attempts (best-of-N); claude-session-driver fan-out | M | yes; no |
| `cc-community/CC-community-plugins-landscape.md` `/seo` audit fan-out | M | no |
| `cc-native/sandboxing/CC-sandbox-platforms-landscape.md` sandboxes for agent fan-out | M | no |
| `cc-native/configuration/CC-changelog-feature-scan.md` `/batch` fan-out | M | no |
| `non-cc/reference/weco-aide-recursive-self-improvement-analysis.md` Propose-Probe-Compose; HarnessFlow MCTS | M | yes |
| `non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` self-consistency (sample-N, majority vote) | M | partly |
| `non-cc/infrastructure/kv-cache-serving-landscape.md` prefix cache for branching (tree search) | M | no |
| `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`; `non-cc/coding-agents/goal-loops-landscape.md` plan mode | M | partly; no |
| `.claude/skills/adding-research-source/SKILL.md` enrich a topic: gap survey, lanes, falsification passes | D | yes |

The section's table in the disciplines landscape keeps the clearest cases.

### Second batch (owner 2026-11-27)

- **N77, definitions.** Knowledge graph: replace the inference-only definition with a first-party
  one (for example Hogan et al., "Knowledge Graphs", arXiv 2003.02320). Hypergraph and hyperedge: add
  a first-party definition source to the frameworks doc's bullet. HybridRAG (knowledge graph plus
  vector retrieval, Sarmah et al., arXiv 2408.04948) as a row in RAG patterns at a glance, told
  apart from hybrid search. Glossary rows (lead): hybrid search, HybridRAG, hypergraph and hyperedge,
  n-ary relation, multilayer network.
- **N78, capability table.** Add Copilot CLI, VS Code Copilot Chat, Cursor, Cline, Aider, Amp and
  Windsurf to the Cross-Harness Matrix, all 13 mechanics, cells from vendor docs, dated. If the
  table gets too wide, split it into two tables with the same rows rather than drop mechanics.
- **N79, session save and resume.** Rows for the same seven harnesses in the checkpoint and resume
  matrix, and re-check the "unverified" cells of the Codex, Gemini CLI and OpenCode rows.
- **N80, configuration and policy.** One table: settings files and precedence, environment
  variables, managed or enterprise policy, per-project overrides, for Claude Code and the top-10
  harnesses; link the Claude Code docs instead of repeating them.
- **N81, forge capability map.** One table, rows = capabilities (CI, hosted runners, merge queue,
  rulesets and branch protection, required checks, code owners, dev environments, secret scanning,
  code scanning, package registry, enterprise SSO and audit log, official MCP server, coding-agent
  integration), columns = GitHub, GitLab, Codeberg/Forgejo, Gitea, Bitbucket, Azure DevOps. Each
  cell from the vendor's docs, dated.
- **N82, distributed systems.** Concept space with an agent lens: the fallacies of distributed
  computing (owner sources: the Wikipedia article, the APNIC 2025 post and the AlgoMaster page are
  leads; cite the original statements where readable), system borders (bounded contexts, trust
  boundaries), contracts (interface and schema contracts, consumer-driven contract tests),
  communication (sync and async, messaging, delivery semantics, idempotency, backpressure), key
  papers and a dated timeline (for example Lamport clocks, FLP, Paxos, the end-to-end argument, CAP,
  Raft), layers, topologies and patterns (retry with backoff, circuit breaker, saga, outbox,
  event sourcing). Then where these show up for agents (MCP and A2A as contracts, multi-agent
  failure modes, durable execution). Well-known items only.
- **N83, test- and eval-driven development.** TDD, BDD (Gherkin, Cucumber), property-based testing
  (Hypothesis), eval-driven development (arXiv 2411.13768, LangChain, Airbnb, the Medium post as a
  practitioner write-up) and tripwire tests and evals (similar concepts: canaries, guardrail
  tripwires, assertion monitors). Session m3d's findings are leads only.
- **N84, privacy law.** GDPR (EUR-Lex), UK GDPR and the Data Protection Act 2018 (ICO,
  legislation.gov.uk), CCPA as amended by CPRA (California OAG, CPPA), and Canada (PIPEDA from the
  Office of the Privacy Commissioner; Quebec's Law 25). What each requires, from first-party text,
  then a table of where each touches KB topics (agent memory, logs and telemetry, training-data
  terms, cross-border transfer, automated decisions, enterprise data APIs). Not legal advice; say so.
- **N85, self-evolving and meta-learning.** Gap survey of the three docs first; then add the
  well-known missing lines (for example meta-learning, learned optimizers, self-referential agents,
  automated agent design), each from its paper's abstract page.
- **N86, diverge and converge.** Audit where the KB describes or uses a broad exploratory phase
  followed by a narrow vertical one (the audit result goes in this plan), then one short section
  with first-party sources (for example the Design Council's Double Diamond) and links to the
  places found.

## Remaining work

| Row | Item | Gate | Done when |
|---|---|---|---|
| ~~N67~~ | ~~Hypergraphs and multi-layer relationships in `graph-databases-query-languages-landscape.md`, plus `caviri/rete` ([§ Lane tasks](#n67-hypergraphs-and-layered-relationships))~~ | agent | Shipped 2026-11-27 (this PR): § Higher-order and layered relationships in the graph-databases doc (n-ary table, multilayer, time as a layer, libraries, rete), the frameworks doc's hyperedge note now points to it, knowledge-graphs hub row; two fact-check passes |
| ~~N68~~ | ~~GitHub platform capabilities analysis and the `dev-platforms.md` hub ([§ Lane tasks](#n68-github-platform-capabilities))~~ | agent | Shipped 2026-11-27 (this PR): github-platform-capabilities-analysis.md (Actions, dev environments, rules and enforcement, org and enterprise features, agent surfaces; every tier and status dated), new dev-platforms.md hub, sdlc-lcm index row; two fact-check passes |
| ~~N69~~ | ~~Code forge, CI/CD and GitHub Actions runner alternatives landscape ([§ Lane tasks](#n69-forge-and-ci-alternatives))~~ | agent | Shipped 2026-11-27 (this PR): code-forge-ci-alternatives-landscape.md (forges, CI/CD systems, GitHub Actions runner services, Codeberg and SourceHut rules on agent-written code; leads cited as leads), cross-linked with the GitHub capabilities doc, dev-platforms hub row; two fact-check passes |
| ~~N70~~ | ~~Hindsight, Docker Agent, *Agentic GraphRAG* and the Pydantic AI coding-agent sources (Coder, Pax, Fowler) in the frameworks doc ([§ Lane tasks](#n70-frameworks-doc-sources))~~ | agent | Shipped 2026-11-27 (this PR): Hindsight (§ 4), Docker Agent (§ 3), Pydantic AI coding agents (Coder, Pax beta, Fowler-site walkthrough) and the Agentic GraphRAG book pointer in the frameworks doc; memory and harness hub rows; two fact-check passes |
| ~~N71~~ | ~~Rust migration and Scientist, GUARD and self-improvement memory, the over-edit study, and codekb ([§ Lane tasks](#n71-sdlc-sources))~~ | agent | shipped (legacy migration: Anthropic Rust migration, GitHub Scientist; Weco GUARD and SIM; Code Necessity; codekb) |
| ~~N72~~ | ~~Micro language models landscape ([§ Lane tasks](#n72-micro-language-models))~~ | agent | Shipped 2026-11-27 (this PR): micro-language-models-landscape.md (arXiv 2604.19642 on-device openers, SPREAD's fine-tuned Nemotron as a vendor claim, llama2.c, a bare-metal inference experiment; Trigma not included), non-cc index and harness hub rows; two fact-check passes |
| ~~N73~~ | ~~n8n nod, Hugging Face swarms report, OpenResearch example, PandaDoc connector and IBM Bob ([§ Lane tasks](#n73-agent-and-connector-sources))~~ | agent | shipped (Nod, PyBot field report, OpenResearch shared projects, PandaDoc connector, IBM Bob) |
| ~~N74~~ | ~~Where Claude Code, Codex CLI, Gemini CLI and other open-source harnesses process PDFs and images (local or server, which packages), and GPT-6.2 Astra's input modalities ([§ Lane tasks](#n74-where-harnesses-process-pdfs-and-images))~~ | agent | shipped (comparison landscape § Where media is processed; GPT-6.2 Astra video not supported; CC Read-tool line corrected) |
| ~~N75~~ | ~~Capability map: new mechanic rows in the Cross-Harness Matrix ([§ Lane tasks](#n75-capability-map))~~ | agent | shipped (seven Cross-Harness Matrix rows: OpenCode subagents, Gemini built-in agents, A2A, resume flags) |
| ~~N76~~ | ~~Coverage-depth audit of the top coding harnesses against Claude Code ([§ Lane tasks](#n76-coverage-depth-audit))~~ | agent, then owner | shipped (audit table in § N76; gaps 1, 2 and 5 went to N78 to N80, the rest to owner row N87) |
| N87 | Owner pick from the N76 audit: per-harness sandboxing, hooks, skills and subagents in the harnesses' own docs, auth-table and community coverage ([§ N76](#n76-coverage-depth-audit)) | owner | Owner names which become rows; default: none until N78 to N80 have shipped |
| N77 | Definitions: knowledge graph, hypergraph and hyperedge, HybridRAG vs hybrid search, plus glossary rows ([§ Second batch](#second-batch-owner-2026-11-27)) | agent | Each term has a first-party definition source; glossary rows added; two fact-check passes |
| N78 | Capability table: Copilot CLI, VS Code Copilot Chat, Cursor, Cline, Aider, Amp and Windsurf added to the Cross-Harness Matrix | agent | All 13 mechanics filled or marked not documented, dated; two passes |
| ~~N79~~ | ~~Session save and resume for the same seven harnesses; re-check the unverified rows~~ | agent | shipped (checkpoint and resume rows for seven harnesses; Codex, Gemini CLI and OpenCode re-checked) |
| N80 | Configuration and policy by harness | agent | Table merged; two passes |
| N81 | Forge capability map: GitHub, GitLab, Codeberg/Forgejo, Gitea, Bitbucket, Azure DevOps | agent | Table merged; two passes |
| N82 | Distributed systems concepts landscape (fallacies, borders, contracts, communication, papers, timeline, layers, topologies, patterns, agent lens) | agent | New doc merged with hub and index rows; two passes |
| ~~N83~~ | ~~Test- and eval-driven development landscape (TDD, BDD, property-based testing, EDD, tripwires)~~ | agent | shipped (test- and eval-driven development landscape) |
| ~~N84~~ | ~~Privacy law touchpoints: GDPR (EU), UK GDPR, CCPA/CPRA, Canada (PIPEDA, Quebec Law 25)~~ | agent | shipped (privacy law touchpoints: GDPR, UK GDPR, CCPA/CPRA, PIPEDA; Quebec unverified) |
| N85 | Self-evolving and meta-learning: survey the three docs, add what is missing | agent | Gap survey in the PR body; additions merged; two passes |
| ~~N86~~ | ~~Diverge and converge: audit and one section~~ | agent | shipped (§ Diverge and converge; audit in § N86 audit) |
| N9 | Assess YouTube videos (ai-that-works playlist, Cole Medin channel) as research leads (owner 2026-11-22; #1009) | owner | **ai-that-works part done 2026-11-22** (owner narrowed it to the companion repo's transcripts): all 86 episode dirs triaged from the repo (github.com/ai-that-works/ai-that-works, no licence, so read and cited only), 47 with transcripts; 3 strong, 18 possible and 38 dropped leads, list and reasons in the session triage notes. Shipped, each re-checked at first-party sources with two fact-check passes: #1031 GEPA, #1032 SlopCodeBench, #1033 HumanLayer status, #1034 lethal trifecta. **Concept pass** (owner 2026-11-22: concepts, how-tos and best practices count, not only tools): about 225 ideas triaged, 24 kept, each cited as a single-source practitioner claim with outside corroboration where it exists: #1039 harness patterns, #1040 eval practices, #1041 memory, skills, observability and event-log projections; five LLM-application patterns held for lack of a fitting doc. **Open, owner-gated:** Cole Medin's channel, once the owner picks a transcript route (from this Codespace, yt-dlp and headless browsers hit YouTube's sign-in bot check) |
| N38 | paperverse: make the weekly real-feed sync mergeable, add `triage/kb-papers` as a source, then one catch-up sync (D2) | agent in a paperverse session; owner if the fix needs a setting or an App | The sync PR gets every required check and merges without help; paperverse `main` holds all weekly files and `arxiv-kb.jsonl`; deployed page shows them |
| N56 | Compare `scripts/cc_cache_usage.py` with Claude Code `/usage` "Prompt cache (main)" and with a cachemiss run on one session (residual of N55) | owner | The owner pasted the `/usage` section on 2026-11-25 (46 main-thread requests, 99% of input from cache, no misses); still waits on approval to run cachemiss (external code); the three sets of numbers agree or the differences are explained in `CC-prompt-caching-behavior.md`; offer the prediction column to cachemiss only if they agree |
| N62 | Owner calls left by the N61 refresh, each with the doc text already hedged: `status:` for `codebuff-analysis.md` and `opennote-analysis.md` (both shutting down) and `frognano-analysis.md` (code and weights now public); the "cleanroom" label for clawcodex in `CC-community-reimplementations-landscape.md` (its README says "ported from the TypeScript reference"); re-scoring the redis-iris Shared and Distributed rubric cells, which were scored on the old Context Retriever wording | owner | Lead default: keep `status: assess` and the hedged text until the owner decides. Done when the owner has decided each one and the decision is applied |
| 13-A5 | Labels from `decide()` in issue triage at a measured threshold (moved from plan 0012's Deferred list) | data | About 50 issues across the shadowed repos carry the shadow section; then sweep `hi` against the labels the existing triage set and decide |
| 13-A7 | Drift checks for the decision models: (1) a monthly scheduled run of `decision-model-eval.yaml` on the gold sets, flagged against the 2026-11-10/11 baseline (AUC drop above about 0.03, Brier rise, recommended `hi` moving by 0.05 or more); (2) store each weekly paper run's decided / fallback / escalated counts (the artifact summary already prints "Decided via decide()") and flag a sustained fall in the decided share or a rise in escalations; (3) on about 10% of papers also run the chat call and track the disagreement rate. Pin model versions (`jev-1.13.0`, `clef`) and re-run the gold sets before any bump; set thresholds on one half of a gold set and report on the other. **Part (1) shipped 2026-11-12** (`#813`: `decision-model-eval.yaml` monthly on the 1st, `data/gold/baseline.json`, `decision-drift` issue; Brier shown, not flagged). A manual run the same day reproduced the Clef and Clef-flash baseline exactly, so run-to-run noise for Clef is nil on this evidence (Jev not re-run). **Part (2) shipped 2026-11-17** (`#875`): the committed triage reports already store each run's "Decided via decide()" line, so `lib/decide_counts.py` reads them and the monthly `decision-model-eval.yaml` run appends a per-run table to its summary and a note to `drift.md` (the `decision-drift` issue) when each of the last 3 runs' decided share is more than 0.10 below the earlier mean; it needs 6 runs before it can flag. First data point: W45, 88 of 100 decided. Escalations are not printed separately in the summary, so they are counted as fallbacks. Left: (3) the chat-call disagreement sample — ask the owner whether it earns its cost; the split-half thresholds belong to A8 | owner (deferred) | Monthly workflow live with a baseline file; counts stored per run; disagreement sample in the summary. **Part (3) deferred by the owner 2026-11-22** (not built now); parts (1) and (2) ship. Resume only on an owner go |
| 13-A8 | Gold-set refresh against the in-sample caveat: add a second paper week as a held-out set, a human spot-check of about 20 items, and real (not planted) off-topic issues | agent + owner spot-check | Second paper set and an issue set with real negatives in `.github/scripts/data/gold/`; H1 numbers re-reported out of sample |
| 13-O5 | Stale token variables. **Done 2026-11-13 as far as the container allows:** `GH_TOKEN` comes from this codespace's devcontainer mapping of an expired PAT secret; the mapping was already dropped upstream on 2026-07-22, but the codespace was never rebuilt. It is now removed from the machine's environment file and unset for new shells. Running processes keep it until a container rebuild, which is the full fix. `GITHUB_TOKEN` is the Codespaces-issued token and the commit signer uses it, so it stays; network calls to other repos keep needing the per-session workaround | owner | **Deferred by the owner 2026-11-22.** When resumed: Codespace rebuilt (owner) |
| 13-O10 | Cloudflare account details in public repos (owner audit 2026-11-13, checked at source). Shipped: `qte77/ldnmxx-hack#373` and `#374` (the account id is no longer pinned in the repo; `.env.example` carries a placeholder), `qte77/qte77.github.io#62` (a draft link removed). The open decisions (git history, the live Worker hostname, CI secrets) and the step-by-step removal guide sit in the owner's private notes, not in this public plan, so it doesn't point at where the old values still are. An account id itself can't be changed; a new one means a new account | owner | **Deferred by the owner 2026-11-22.** When resumed: Owner closes the private checklist |
