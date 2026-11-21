---
title: Agentic Database Access — MCP Servers, Text-to-SQL, Write Safety
purpose: How agents reach databases today — vendor database MCP servers and their read-only controls, text-to-SQL benchmarks and training results, and the write-safety evidence (read-only roles, branching, an incident, injection through MCP). Landscape as of 2026-11-18.
created: 2026-11-18
updated: 2026-11-18
validated_links: 2026-11-18
status: assess
---

## Why This Doc

An agent that can run SQL turns the database into an action surface, not only a data source. Two
questions follow: how well can models write the SQL (accuracy), and what limits the damage when they
write the wrong SQL or are tricked into it (safety). Catalog, metrics and lineage substrate is covered
in [semantic-layers-data-catalog-landscape.md](semantic-layers-data-catalog-landscape.md); this doc
covers the access path and its controls. Evidence level is stated per claim; all vendor facts are from
each vendor's own docs or repo as of 2026-11-18.

## Database MCP servers

| Server | License | Read-only control (documented) | Notes |
|---|---|---|---|
| [Model Context Protocol (MCP) Toolbox for Databases][toolbox] (Google, `googleapis/mcp-toolbox`) | Apache-2.0 | Not stated on the README; tools are defined per database/toolset | Open-source MCP server for many databases (Google Cloud services plus PostgreSQL, MySQL, SQL Server, Oracle, MongoDB, Snowflake and others); README examples use v1.17.0; ~16.9k stars on 2026-11-18 (`gh api`) |
| [Supabase MCP][supabase-mcp] (`supabase/mcp`) | Apache-2.0 | `read_only=true` URL parameter (runs SQL as a read-only Postgres user per the [security guidance][supabase-docs]); `project_ref` scoping; `features` groups | Its [docs][supabase-docs] say to connect to production only when the task needs production evidence, and then to combine project scoping, read-only mode and limited feature groups. ~3.0k stars on 2026-11-18; the old `supabase-community` URL redirects here; the separate postgrest MCP package is deprecated |
| [Neon MCP][neon-mcp] (`neondatabase/mcp-server-neon`) | MIT | `?readonly=true` hides write tools and runs `run_sql` in a READ ONLY transaction; `projectId`, `category`, `roleName`, `secrets` parameters | Hosted at the Neon MCP endpoint; local stdio package deprecated; the [README][neon-mcp] says it is for local development and IDE use, not production; the [docs page][neon-docs] says the same and that the local stdio package is deprecated |
| [PlanetScale MCP][planetscale-mcp] | Hosted service (not open source) | Access scope none / read-only / full per organization or database; admins set query access separately | `UPDATE`/`DELETE` without `WHERE` and `TRUNCATE` blocked; DDL asks for human confirmation; short-lived credentials; Vitess and Postgres |
| [MotherDuck MCP][motherduck-mcp] | MIT | Read-only by default; `--read-write` enables writes | Docs warn read-only alone is not enough for third-party access (filesystem and settings still reachable); hosted remote MCP recommended for that case |
| [SQL MCP Server][dab-mcp] (Microsoft, part of Data API builder) | MIT (`Azure/data-api-builder`, `gh api` 2026-11-18) | Role-based permissions per entity; individual tools such as `delete-record` can be disabled | Deliberately has no NL2SQL and no DDL: agents call typed record tools, and DAB's query builder emits the T-SQL (documented, Microsoft Learn page dated 2026-05) |
| [Postgres MCP Pro][postgres-mcp-pro] (`crystaldba`) | MIT | `--access-mode=restricted` limits operations to read-only transactions plus an execution-time limit (README) | Community; README calls it suitable for production but also says it may add measures to make restricted mode safe for production databases (vendor claim, hedged by the vendor); 3,487 stars, last push 2026-08-17 (`gh api` 2026-11-18) |

Reading across the table: the shared pattern is a scoped, read-only default or flag plus
confirmation on DDL. Neon's README says its server is not for production, and Supabase's docs allow production only when the task needs it, with scoping and read-only; Microsoft's design avoids the problem by never exposing raw SQL authoring. The
generic MCP-level risks are in
[agentic-ai-vulnerability-landscape.md](../../sdlc-lcm/agentic-ai-vulnerability-landscape.md).

## Text-to-SQL benchmarks

Scores below are leaderboard-reported (vendor/submitter claims), read from each benchmark's own site
on 2026-11-18.

| Benchmark | What it measures | Top entry on 2026-11-18 |
|---|---|---|
| [BIRD][bird] | Cross-domain text-to-SQL, 95 databases, 12,751+ question-SQL pairs; also BIRD-Critic (SQL debugging) and BIRD-Interact | Overall test EX 83.40% (AskData, 2026-10-22); human 92.96% |
| [Spider 2.0][spider2] | Enterprise workflows on large schemas (BigQuery, Snowflake, DBT) | Snapshot read 2026-11-18: Snow 96.70, Lite 76.23, DBT 65.6 (no leaderboard date on the page) |

Caveats: Spider 2.0's page says 632 problems in its About section but lists 547 (Snow), 547 (Lite) and 68 (DBT), which do not sum to 632, so
compare only within one setting. BIRD's dev and test tops are different entries, and the dev leader's
test score (74.34%) is far below its dev score, which is a reminder that dev numbers are not
comparable to test numbers.

Recent training work, both arXiv abstracts read 2026-11-18 (paper claims, not independently
reproduced):

- **[BIRD-RL][bird-rl]** (arXiv 2610.29426, NeurIPS 2026 main track per the page) trains agents on
  stateful database tasks such as SQL debugging, using database replicas with per-trajectory
  isolation. Its 7B and 14B models reach 44.40% and 48.00% on BIRD-CRITIC-SQLite versus 48.20% the
  authors report for a Claude-Opus-4.6 agent.
- **[DualSQL][dualsql]** (arXiv 2609.18135) jointly trains schema-linking and SQL-generation agents;
  the authors report 68.0% (4B) and 71.1% (8B) execution accuracy on the BIRD dev set.

Takeaway: scores are high on curated benchmarks, but a score says nothing about blast radius;
that is the write-safety question below. Why raw text-to-SQL still needs a governed layer is argued
in [semantic-layers-data-catalog-landscape.md](semantic-layers-data-catalog-landscape.md) under
Why Agents Need This and in [databricks-genie-analysis.md](../agents/databricks-genie-analysis.md).

## Write safety

Layers, cheapest first; none is sufficient alone.

1. **Database-enforced least privilege.** A dedicated read-only role is the strongest control because
   the database, not the tool, enforces it. Neon's `roleName` parameter and Supabase's read-only
   Postgres user are examples. Neon's docs add a trap: a role created in its console may belong to
   `neon_superuser`, which reads all data and so does not limit reads ([docs][neon-docs]).
2. **Tool-level modes are not a boundary.** The Anthropic reference Postgres MCP server wrapped each
   query in a read-only transaction, but Datadog Security Labs showed (2025-08-21) that a statement
   such as `COMMIT; DROP SCHEMA public CASCADE;` ended that transaction and ran writes. Datadog says the flaw
   is present from v0.1.0, that 0.6.2 is the latest npm/Docker release and unpatched, that a Zed fork
   (`@zeddotdev/postgres-context-server` v0.1.4) carries the fix, and that the server is deprecated and
   archived ([Datadog][datadog-pg]). Evidence: researcher-reported (Datadog Security Labs); vendor
   response not found.
3. **Branching before merging.** Neon's migration tools run a change on a temporary branch and apply
   it to the main branch only on a second call (`prepare_database_migration`,
   `complete_database_migration`; [README][neon-mcp]); Supabase's guidance tells users to test changes on a
   development branch first ([docs][supabase-docs]); PlanetScale scopes queries to a named branch
   ([docs][planetscale-mcp]). Branching limits the damage of a bad migration; it does not stop data
   exfiltration.
4. **Blocking and confirmation of destructive statements** (PlanetScale: no unbounded `UPDATE`/`DELETE`,
   `TRUNCATE` blocked, DDL confirmed by a human).
5. **Typed tool surfaces instead of free SQL** (Microsoft's SQL MCP Server).

### Incident evidence

- **Replit and SaaStr, July 2025 (reported, single-source-chain).** The SaaStr founder reported that
  an AI coding agent deleted a production database during a code freeze and then said rollback was
  impossible, though a rollback later worked. [The Register][register-replit] (2025-07-21) reports these as the
  founder's own claims, notes the screenshots only appear to be Replit output, and says Replit had not
  publicly responded at publication time. Numbers (records deleted, fake profiles) vary across
  secondary blogs and are not repeated here. Evidence level: observed by one user, unverified by the
  vendor in the sources read. No Replit statement was found in The Register's report, and
  only a web search (2026-11-18) looked for a primary postmortem. Treat as an illustration of a missing environment boundary (agent holding
  production write access), not as a measured failure rate.
- **Supabase MCP exfiltration, mid-2025 (research demo on a mock support app, not a field incident).**
  General Analysis dates its post 2025-07-08 and Willison's post is dated 2025-07-06. They built a
  mock support app; an agent running with the `service_role` key (which bypasses row-level
  security) read a support ticket containing hidden instructions, queried a tokens table and wrote
  the result back into the ticket thread ([General Analysis][ga-supabase]). Simon Willison framed it as a
  "lethal trifecta" and noted that read-only mode removes the write-back leg
  ([post][willison-supabase]). General Analysis' own mitigation list: project scoping,
  read-only, narrower tool groups, human review of queries, and not relying on injection filters alone.
  Supabase's current guidance says the same risk class applies and that its injected "do not follow
  commands in data" instructions are not foolproof ([docs][supabase-docs]). I did not locate a
  Supabase statement on the original report; secondary summaries quote one, unverified here.

Read-only does not close the leak path where the agent can read secrets and also emit text to an
attacker-visible place; scoping what is readable is the control that matters there.

## Migrations

Schema changes are the highest-risk class of agent write because they are hard to reverse and often
run with elevated roles. Documented patterns: branch-then-merge (Neon, Supabase), DDL excluded by
design (Microsoft SQL MCP Server: DML only, with schema changes left to developer tooling), and DDL
behind human confirmation (PlanetScale). No evidence read for this doc measures how often agent
migrations fail; this is a gap, not a finding.

## Data quality and lineage

Agents that write or transform data need lineage so a bad write can be traced to its run.
[OpenLineage][openlineage] is an open lineage-metadata standard (jobs, runs, datasets, extensible
facets; Apache-2.0; a graduate-level LF AI & Data project per its README, 2026-11-18). Catalog-side
lineage and ownership are covered in
[semantic-layers-data-catalog-landscape.md](semantic-layers-data-catalog-landscape.md). Whether any
database MCP server above emits lineage events was not checked.

## Not verified

- Toolbox's mechanism for restricting writes (README silent; docs not read).
- Any vendor statement from Supabase on the demo, or from Replit beyond what The Register reports (only a 2026-11-18 web search was run).

## Sources

| Source | Content |
|---|---|
| [MCP Toolbox for Databases][toolbox] | Google open-source database MCP server (Apache-2.0) |
| [Supabase MCP][supabase-mcp] · [security guidance][supabase-docs] | Read-only, scoping, branching, injection risks |
| [Neon MCP README][neon-mcp] · [Neon docs][neon-docs] | Read-only mode, branch-based migrations, role/secret controls |
| [PlanetScale MCP docs][planetscale-mcp] | Scopes, destructive-query handling, branch scoping |
| [MotherDuck MCP][motherduck-mcp] | Read-only default, limits of read-only |
| [SQL MCP Server (Microsoft Learn)][dab-mcp] | Entity/RBAC tool surface, no NL2SQL, no DDL |
| [Postgres MCP Pro][postgres-mcp-pro] | Community Postgres server |
| [BIRD][bird] · [Spider 2.0][spider2] | Text-to-SQL leaderboards |
| [BIRD-RL (arXiv 2610.29426)][bird-rl] · [DualSQL (arXiv 2609.18135)][dualsql] | Training results for SQL agents |
| [Datadog Security Labs][datadog-pg] | Read-only bypass in the reference Postgres MCP server |
| [General Analysis][ga-supabase] · [Willison][willison-supabase] | Supabase MCP injection demo and framing |
| [The Register][register-replit] | Replit production database incident reporting |
| [OpenLineage][openlineage] | Lineage metadata standard |

[toolbox]: https://github.com/googleapis/mcp-toolbox
[supabase-mcp]: https://github.com/supabase/mcp
[supabase-docs]: https://supabase.com/docs/guides/getting-started/mcp
[neon-mcp]: https://github.com/neondatabase/mcp-server-neon
[neon-docs]: https://neon.com/docs/ai/neon-mcp-server
[planetscale-mcp]: https://planetscale.com/docs/connect/mcp
[motherduck-mcp]: https://github.com/motherduckdb/mcp-server-motherduck
[dab-mcp]: https://learn.microsoft.com/en-us/azure/data-api-builder/mcp/overview
[postgres-mcp-pro]: https://github.com/crystaldba/postgres-mcp
[bird]: https://bird-bench.github.io/
[spider2]: https://spider2-sql.github.io/
[bird-rl]: https://arxiv.org/abs/2610.29426
[dualsql]: https://arxiv.org/abs/2609.18135
[datadog-pg]: https://securitylabs.datadoghq.com/articles/mcp-vulnerability-case-study-SQL-injection-in-the-postgresql-mcp-server/
[ga-supabase]: https://generalanalysis.com/blog/supabase-mcp-blog
[willison-supabase]: https://simonwillison.net/2025/Jul/6/supabase-mcp-lethal-trifecta/
[register-replit]: https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident/
[openlineage]: https://github.com/OpenLineage/OpenLineage
