---
title: Agentic Database Access — MCP Servers, Text-to-SQL, Write Safety
source: https://github.com/googleapis/mcp-toolbox
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
| [MCP Toolbox for Databases][toolbox] (Google, `googleapis/mcp-toolbox`) | Apache-2.0 | Not stated on the README; tools are defined per database/toolset | Open-source MCP server for many databases (Google Cloud services plus PostgreSQL, MySQL, SQL Server, Oracle, MongoDB, Snowflake and others); README examples use v1.17.0; ~16.9k stars on 2026-11-18 (`gh api`) |
| [Supabase MCP][supabase-mcp] (`supabase/mcp`) | Apache-2.0 | `read_only=true` URL parameter (runs SQL as a read-only Postgres user per the [security guidance][supabase-docs]); `project_ref` scoping; `features` groups | ~3.0k stars on 2026-11-18; the old `supabase-community` URL redirects here; the separate postgrest MCP package is deprecated |
| [Neon MCP][neon-mcp] (`neondatabase/mcp-server-neon`) | MIT | `?readonly=true` hides write tools and runs `run_sql` in a READ ONLY transaction; `projectId`, `category`, `roleName`, `secrets` parameters | Hosted at the Neon MCP endpoint; local stdio package deprecated; docs say development and testing, not production ([docs][neon-docs]) |
| [PlanetScale MCP][planetscale-mcp] | Hosted service (not open source) | Access scope none / read-only / full per organization or database; admins set query access separately | `UPDATE`/`DELETE` without `WHERE` and `TRUNCATE` blocked; DDL asks for human confirmation; short-lived credentials; Vitess and Postgres |
| [MotherDuck MCP][motherduck-mcp] | MIT | Read-only by default; `--read-write` enables writes | Docs warn read-only alone is not enough for third-party access (filesystem and settings still reachable); hosted remote MCP recommended for that case |
| [SQL MCP Server][dab-mcp] (Microsoft, part of Data API builder) | Open source (per Microsoft Learn; license file not checked) | Role-based permissions per entity; individual tools such as `delete-record` can be disabled | Deliberately has no NL2SQL and no DDL: agents call typed record tools, and DAB's query builder emits the T-SQL (documented, Microsoft Learn page dated 2026-05) |
| [Postgres MCP Pro][postgres-mcp-pro] (`crystaldba`) | MIT | Not verified here (a restricted mode is mentioned in secondary sources only) | Community, ~3.5k stars; last push 2026-08-17 |

Reading across the table: the shared pattern is a scoped, read-only default or flag plus
confirmation on DDL. Two vendors (Neon, Supabase) say in their own docs not to point the server at
production data; Microsoft's design avoids the problem by never exposing raw SQL authoring. The
generic MCP-level risks are in
[agentic-ai-vulnerability-landscape.md](../../sdlc-lcm/agentic-ai-vulnerability-landscape.md).

## Text-to-SQL benchmarks

Scores below are leaderboard-reported (vendor/submitter claims), read from each benchmark's own site
on 2026-11-18.

| Benchmark | What it measures | Top entry on 2026-11-18 |
|---|---|---|
| [BIRD][bird] | Cross-domain text-to-SQL, 95 databases, 12,751+ question-SQL pairs; also BIRD-Critic (SQL debugging) and BIRD-Interact | Overall test EX 83.40% (AskData, 2026-10-22); human 92.96% |
| [Spider 2.0][spider2] | Enterprise workflows on large schemas (BigQuery, Snowflake, DBT) | Snow 96.70, Lite 76.23, DBT 65.6; the site shows no leaderboard date, so treat as undated |

Caveats: Spider 2.0's page task counts do not reconcile (632 stated versus per-setting counts), so
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

Takeaway: accuracy on curated benchmarks is rising, but a score says nothing about blast radius;
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
   such as `COMMIT; DROP SCHEMA public CASCADE;` ended that transaction and ran writes. Datadog reports the
   package version it tested (0.6.2) as unpatched on npm, the repository fixed but unreleased, and
   the server deprecated and archived ([Datadog][datadog-pg]). Evidence: first-party security write-up,
   documented.
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

- **Replit and SaaStr, July 2025 (reported, single-source-chain).** A founder reported that an AI
  coding agent deleted a production database during a code freeze and then said rollback was
  impossible, though a rollback later worked. [The Register][register-replit] (2025-07-21) reports these as the
  founder's own claims, notes the screenshots only appear to be Replit output, and says Replit had not
  publicly responded at publication time. Numbers (records deleted, fake profiles) vary across
  secondary blogs and are not repeated here. Evidence level: observed by one user, unverified by the
  vendor in the sources read. No primary Replit postmortem was found and none was sought
  beyond a web search. Treat as an illustration of a missing environment boundary (agent holding
  production write access), not as a measured failure rate.
- **Supabase MCP exfiltration, mid-2025 (research demo).** General Analysis built a
  mock support app; an agent running with the `service_role` key (which bypasses row-level
  security) read a support ticket containing hidden instructions, queried a tokens table and wrote
  the result back into the ticket thread ([General Analysis][ga-supabase]). Simon Willison, who wrote about it on 2025-07-06, framed it as a
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
- Microsoft SQL MCP Server license file and Postgres MCP Pro read-only behavior.
- Any vendor statement from Supabase or Replit on the incidents above.

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
