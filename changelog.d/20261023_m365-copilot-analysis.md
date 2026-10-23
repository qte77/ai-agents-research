### Added

- `docs/non-cc/agents/microsoft-365-copilot-analysis.md`: new analysis doc — a first-party
  challenge pass fact-checking an AI assistant's self-description and a practitioner how-to for
  the Microsoft 365 Copilot ecosystem (Copilot in SharePoint Skills and structured document
  generation, Microsoft Copilot Studio model selection and BYO MCP, Work IQ, Microsoft Agent 365
  governance/licensing/APIs, the EU Data Boundary/Flex Routing/Multi-Geo residency story including
  Claude-on-Foundry's own lack of an EU Data Zone deployment type, Claude's three contractual
  postures across this family, and a documented Customer-Key-vs-Double-Key-Encryption trade-off
  for Copilot access). 85 claims split by verdict × bucket (3 refuted, 24 partly, 47 supported, 11
  unverifiable); disambiguates "Microsoft 365 Copilot" from GitHub Copilot and separates "Copilot
  in SharePoint Skills" from "custom skills in declarative agents," two distinct features sharing
  a name. Adds a generic, vendor-sourced feasibility table for eight recurring operational/
  automation scenarios, and a numbers-free pointer to each surface's current pricing page, a
  "Lockdown limits" section and a feed table for Message center, Service health and the roadmap.
- `docs/non-cc/README.md`: Agents-table row for the new doc.
- `docs/_topics/skills.md`: hub row for Copilot in SharePoint Skills (non-cc bucket).

### Changed

- `docs/cc-native/agents-skills/CC-skills-adoption-analysis.md`: confirmed no spec-defined
  `evals/` directory and re-confirmed `allowed-tools` (Experimental) against a live fetch of
  agentskills.io; added a Claude Code ↔ OpenAI Codex CLI SKILL.md/MCP/AGENTS.md parity table to
  Ecosystem Context. Bumped `updated:`/`validated_links:`. (7 of the fact-check pass's 93 claims;
  an 8th, unrelated to either this file or the new doc, is excluded from both and tracked only in
  the companion issue's notes.)
- `.claude/skills/adding-research-source/SKILL.md`: extended Guardrails with five rules learned
  from the Microsoft 365 Copilot fact-check pass — "not found" vs. "refuted," naming the bucket
  alongside the verdict, a scope-stretch check, treating a vendor self-description as a claim not
  a source, and preferring a vendor's per-item roadmap feed over a mirror or search snippet for
  timeline claims.
