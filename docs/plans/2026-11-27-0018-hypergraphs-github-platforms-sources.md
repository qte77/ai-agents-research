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
3. **Wave 3:** N73 (agent and connector sources).
4. **Release (minor)** for the batch, only on the owner's word.

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

## Remaining work

| Row | Item | Gate | Done when |
|---|---|---|---|
| N67 | Hypergraphs and multi-layer relationships in `graph-databases-query-languages-landscape.md`, plus `caviri/rete` ([§ Lane tasks](#n67-hypergraphs-and-layered-relationships)) | agent | Section merged with two fact-check passes; the "not checked" note replaced; hub row in `knowledge-graphs.md` |
| ~~N68~~ | ~~GitHub platform capabilities analysis and the `dev-platforms.md` hub ([§ Lane tasks](#n68-github-platform-capabilities))~~ | agent | Shipped 2026-11-27 (this PR): github-platform-capabilities-analysis.md (Actions, dev environments, rules and enforcement, org and enterprise features, agent surfaces; every tier and status dated), new dev-platforms.md hub, sdlc-lcm index row; two fact-check passes |
| N69 | Code forge, CI/CD and GitHub Actions runner alternatives landscape ([§ Lane tasks](#n69-forge-and-ci-alternatives)) | agent | Doc merged with two fact-check passes; row in `dev-platforms.md` |
| N70 | Hindsight, Docker Agent, *Agentic GraphRAG* and the Pydantic AI coding-agent sources (Coder, Pax, Fowler) in the frameworks doc ([§ Lane tasks](#n70-frameworks-doc-sources)) | agent | Merged with two fact-check passes; hub rows added |
| N71 | Rust migration and Scientist, GUARD and self-improvement memory, the over-edit study, and codekb ([§ Lane tasks](#n71-sdlc-sources)) | agent | Merged with two fact-check passes; hub rows added |
| N72 | Micro language models landscape ([§ Lane tasks](#n72-micro-language-models)) | agent | Doc merged with two fact-check passes; hub and index rows added |
| N73 | n8n nod, Hugging Face swarms report, OpenResearch example, PandaDoc connector and IBM Bob ([§ Lane tasks](#n73-agent-and-connector-sources)) | agent | Merged with two fact-check passes; hub rows added |
| N9 | Assess YouTube videos (ai-that-works playlist, Cole Medin channel) as research leads (owner 2026-11-22; #1009) | owner | **ai-that-works part done 2026-11-22** (owner narrowed it to the companion repo's transcripts): all 86 episode dirs triaged from the repo (github.com/ai-that-works/ai-that-works, no licence, so read and cited only), 47 with transcripts; 3 strong, 18 possible and 38 dropped leads, list and reasons in the session triage notes. Shipped, each re-checked at first-party sources with two fact-check passes: #1031 GEPA, #1032 SlopCodeBench, #1033 HumanLayer status, #1034 lethal trifecta. **Concept pass** (owner 2026-11-22: concepts, how-tos and best practices count, not only tools): about 225 ideas triaged, 24 kept, each cited as a single-source practitioner claim with outside corroboration where it exists: #1039 harness patterns, #1040 eval practices, #1041 memory, skills, observability and event-log projections; five LLM-application patterns held for lack of a fitting doc. **Open, owner-gated:** Cole Medin's channel, once the owner picks a transcript route (from this Codespace, yt-dlp and headless browsers hit YouTube's sign-in bot check) |
| N38 | paperverse: make the weekly real-feed sync mergeable, add `triage/kb-papers` as a source, then one catch-up sync (D2) | agent in a paperverse session; owner if the fix needs a setting or an App | The sync PR gets every required check and merges without help; paperverse `main` holds all weekly files and `arxiv-kb.jsonl`; deployed page shows them |
| N56 | Compare `scripts/cc_cache_usage.py` with Claude Code `/usage` "Prompt cache (main)" and with a cachemiss run on one session (residual of N55) | owner | The owner pasted the `/usage` section on 2026-11-25 (46 main-thread requests, 99% of input from cache, no misses); still waits on approval to run cachemiss (external code); the three sets of numbers agree or the differences are explained in `CC-prompt-caching-behavior.md`; offer the prediction column to cachemiss only if they agree |
| N62 | Owner calls left by the N61 refresh, each with the doc text already hedged: `status:` for `codebuff-analysis.md` and `opennote-analysis.md` (both shutting down) and `frognano-analysis.md` (code and weights now public); the "cleanroom" label for clawcodex in `CC-community-reimplementations-landscape.md` (its README says "ported from the TypeScript reference"); re-scoring the redis-iris Shared and Distributed rubric cells, which were scored on the old Context Retriever wording | owner | Lead default: keep `status: assess` and the hedged text until the owner decides. Done when the owner has decided each one and the decision is applied |
| 13-A5 | Labels from `decide()` in issue triage at a measured threshold (moved from plan 0012's Deferred list) | data | About 50 issues across the shadowed repos carry the shadow section; then sweep `hi` against the labels the existing triage set and decide |
| 13-A7 | Drift checks for the decision models: (1) a monthly scheduled run of `decision-model-eval.yaml` on the gold sets, flagged against the 2026-11-10/11 baseline (AUC drop above about 0.03, Brier rise, recommended `hi` moving by 0.05 or more); (2) store each weekly paper run's decided / fallback / escalated counts (the artifact summary already prints "Decided via decide()") and flag a sustained fall in the decided share or a rise in escalations; (3) on about 10% of papers also run the chat call and track the disagreement rate. Pin model versions (`jev-1.13.0`, `clef`) and re-run the gold sets before any bump; set thresholds on one half of a gold set and report on the other. **Part (1) shipped 2026-11-12** (`#813`: `decision-model-eval.yaml` monthly on the 1st, `data/gold/baseline.json`, `decision-drift` issue; Brier shown, not flagged). A manual run the same day reproduced the Clef and Clef-flash baseline exactly, so run-to-run noise for Clef is nil on this evidence (Jev not re-run). **Part (2) shipped 2026-11-17** (`#875`): the committed triage reports already store each run's "Decided via decide()" line, so `lib/decide_counts.py` reads them and the monthly `decision-model-eval.yaml` run appends a per-run table to its summary and a note to `drift.md` (the `decision-drift` issue) when each of the last 3 runs' decided share is more than 0.10 below the earlier mean; it needs 6 runs before it can flag. First data point: W45, 88 of 100 decided. Escalations are not printed separately in the summary, so they are counted as fallbacks. Left: (3) the chat-call disagreement sample — ask the owner whether it earns its cost; the split-half thresholds belong to A8 | owner (deferred) | Monthly workflow live with a baseline file; counts stored per run; disagreement sample in the summary. **Part (3) deferred by the owner 2026-11-22** (not built now); parts (1) and (2) ship. Resume only on an owner go |
| 13-A8 | Gold-set refresh against the in-sample caveat: add a second paper week as a held-out set, a human spot-check of about 20 items, and real (not planted) off-topic issues | agent + owner spot-check | Second paper set and an issue set with real negatives in `.github/scripts/data/gold/`; H1 numbers re-reported out of sample |
| 13-O5 | Stale token variables. **Done 2026-11-13 as far as the container allows:** `GH_TOKEN` comes from this codespace's devcontainer mapping of an expired PAT secret; the mapping was already dropped upstream on 2026-07-22, but the codespace was never rebuilt. It is now removed from the machine's environment file and unset for new shells. Running processes keep it until a container rebuild, which is the full fix. `GITHUB_TOKEN` is the Codespaces-issued token and the commit signer uses it, so it stays; network calls to other repos keep needing the per-session workaround | owner | **Deferred by the owner 2026-11-22.** When resumed: Codespace rebuilt (owner) |
| 13-O10 | Cloudflare account details in public repos (owner audit 2026-11-13, checked at source). Shipped: `qte77/ldnmxx-hack#373` and `#374` (the account id is no longer pinned in the repo; `.env.example` carries a placeholder), `qte77/qte77.github.io#62` (a draft link removed). The open decisions (git history, the live Worker hostname, CI secrets) and the step-by-step removal guide sit in the owner's private notes, not in this public plan, so it doesn't point at where the old values still are. An account id itself can't be changed; a new one means a new account | owner | **Deferred by the owner 2026-11-22.** When resumed: Owner closes the private checklist |
