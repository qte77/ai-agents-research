### Added

- `docs/non-cc/infrastructure/semantic-layers-data-catalog-landscape.md` § Agent-native ontology
  tools: rubric-scores **Utopia** (deeplethe, Apache-2.0), a bottom-up bitemporal ontology platform
  whose `docs/decisions/` folder documents real extraction failures (reversed edges, transitive-
  closure explosions) behind its append-only correction ledger; cross-references and adds
  CHANGELOG-verified compliance-bug evidence (silent empty causal chains, a SHACL validator
  matching no data, dropped RDF provenance metadata — all from Semantica's own v0.6.7 release) for
  the already-documented Semantica entry (§7 of `agent-frameworks-infrastructure-landscape.md`),
  plus the EU AI Act Article 12 record-keeping deadline (now 2027-12-02 for Annex III).
- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` § 4 Agent Memory
  Infrastructure: rubric-scores **HydraDB** (AGPL-3.0), an object-store-native distributed graph
  database trading RAM ($65–146/GB-mo) for S3-compatible storage (~$0.023/GB-mo) via a
  compare-and-swap writer lease fenced by SlateDB write epochs. § 1: adds a first-party-verified
  addendum (Cordis DI framework's "spatiotemporal composability" paper, the `.agents/notes/`
  decision-record tree) to the existing DeepSeek Harness (`dsh`) profile in
  `docs/non-cc/coding-agents/deepseek-harness-analysis.md`, cross-referenced rather than duplicated.
- `docs/cc-community/CC-community-tooling-landscape.md` § abide: adds complementary,
  independently-verified migration-validation evidence — SWE Refactor Bench (arXiv:2608.23564,
  520 agent migrations, the "Blindness" failure mode), the GAO-25-107795 federal legacy-system
  report, and FreshBrew (arXiv:2510.04852) — cross-referencing the corpus's existing American
  Express Locksmith Loop analysis (`docs/sdlc-lcm/agentic-legacy-migration-validation-analysis.md`)
  rather than restating it.
- Design-lens citations throughout from André Lindenberg's *Artificial Engineering* newsletter
  (five issues: *The Change of Mind Is Information*, *Audit the Auditor*, *The Graph Doesn't Need
  RAM Anymore*, *Everything Is a Plugin, Proven*, *Complete and Correct*), cited as opinion/design
  framing only — every factual claim traces to its own primary source (repo, CHANGELOG, arXiv
  abstract, or GAO report), independently re-verified rather than taken from the article's own
  numbers.
- `docs/_topics/knowledge-graphs.md`, `docs/_topics/memory.md`, `docs/_topics/harness.md`: pointer
  rows/updates for the new entries above.
