### Added

- `docs/sdlc-lcm/agentic-engineering-disciplines-landscape.md` § 1 "-engineering" ladder: new
  **Graph engineering** row (Hamel Husain's coining post, verified via Turing Post's independent
  account and its debunking of viral Microsoft/Stanford/Anthropic misattribution) plus two design-lens
  paragraphs — graph engineering as the wiring already present in shipped software factories, and
  three 2026 data points on the Harness-engineering Verification axiom's cost: Dan Shapiro's
  five-levels framework, METR's RCT (developers estimated 20% faster, measured 19% slower), Faros
  AI's telemetry (+242.7% incidents/PR, +54% bugs/developer, re-verified at source), **Specula**
  (arXiv:2607.25333 — 48 projects, 249 bugs/207 new/68 confirmed/24 fixed, $19–168 median $57,
  93%/47% Sonnet-4.6/Haiku-4.5 spec quality, all figures pulled directly from the paper PDF), and
  **Bend 2** (Apache-2.0, 23,165★, README-quoted proof-gating mechanism) against Martin Kleppmann's
  seL4 formal-verification cost anchor (8,700 LOC / 20 person-years / 200,000 Isabelle lines), and
  SysMoBench's own SIGOPS write-up (~46%/41% conformance/invariant aggregate + 3 named LLM modeling
  failure modes). All quotes and figures verified against their primary source (arXiv PDF, `gh api`
  repo/README fetch, vendor's own published page) in this same session, including two corrections
  made after an adversarial advisor pass: Shapiro's Level 3/4 quotes were re-fetched verbatim rather
  than taken from the newsletter's paraphrase, and Bend's mechanism description was re-grounded in
  its own README instead of the newsletter's framing.
- `docs/sdlc-lcm/software-factory-landscape.md` § (c): one-sentence cross-reference tying the
  graph-engineering framing to the existing four-source human-gate convergence already documented
  there.
- `docs/_topics/harness.md`: one pointer row for the new Graph-engineering/Verification-axiom
  content above.
- Design-lens citations from André Lindenberg's *Artificial Engineering* newsletter (four issues:
  *From Loops to Graphs*, *The Most Expensive Rung on the Ladder*, *The Half We Don't Budget For*,
  *Laws Instead of Diffs*), cited as opinion/design framing only — every factual claim traces to its
  own primary source (arXiv abstract/PDF, `gh api`, a vendor's own published telemetry, or a named
  blog post), independently re-verified rather than taken from the article's own numbers.
