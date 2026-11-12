### Fixed

- `docs/non-cc/agents/microsoft-365-copilot-analysis.md`: adversarial re-check of the 2026-11-12
  Microsoft new-products pass (#799) against every cited first-party page. Corrects two
  misattributed citations (the declarative-agent build-tooling claim cited `da-overview` instead
  of `da-agents-overview`, in both the prose and the Build paths table), an overstated "public
  preview" claim for Microsoft Copilot Managed Runtime that no cited page actually uses (the
  09-25 blog and the overview page both say only "preview"), a wrong structural claim about where
  the manifest's Worker agent object sits relative to `agent_skills` (earlier on the page, not
  "two sections later"), and three small verbatim-quote mismatches (a silently dropped "(Model
  Context Protocol)" expansion, a capitalization change inside a Foundry harness quote, and a
  "This is a preview feature" claim applied to a page that actually reads "This feature is in
  preview"). Also softens an unsupported "FAQ pages" reference for Foundry hosted agents to the
  one Learn page actually fetched.
- `docs/non-cc/frameworks/agentic-enterprise-os-landscape.md`: same "FAQ pages" softening for the
  Foundry hosted-agents caveat.
