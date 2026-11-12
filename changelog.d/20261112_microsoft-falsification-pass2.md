### Fixed

- `docs/cc-native/plugins-ecosystem/CC-cowork-plugins-enterprise-analysis.md`: second, independent
  adversarial re-check of the Microsoft new-products content (#799) and its first falsification
  pass (#803). Fixes a verbatim-quote mismatch in the Cowork disambiguation note — Microsoft's
  announcement blog says it "integrated the technology behind Claude Cowork into Microsoft 365
  Copilot" (confirmed against the blog), not "built 'integrat[ing] the technology...' into"; the
  stray "built" and the wrong `[ing]` bracket are removed and the quote now matches the sibling doc
  (`microsoft-365-copilot-analysis.md`), which already had it right.
- `docs/non-cc/frameworks/agentic-enterprise-os-landscape.md`: fixes a misattributed citation — the
  Copilot Studio row cited its own `what's new` page for the GitHub→Microsoft Copilot harness
  rename, but that page (fetched fresh, content-dated 2026-11-04) still calls it the "GitHub
  Copilot harness" throughout and never states a rename. The rename is documented on Microsoft's
  billing/licensing FAQ page ("Apps are built with the Microsoft Copilot harness (formerly the
  GitHub Copilot harness)"), which is now cited instead, with a note that the what's-new page
  hasn't caught up.
- `docs/non-cc/agents/microsoft-365-copilot-analysis.md`: two minor quote-fidelity fixes applying
  the bracket convention #803 itself established for a quoted fragment's capitalization — two
  quotes ("a list of objects…", "a plugin can include…") silently lowercase a source sentence's
  capital first letter without the bracket the doc uses everywhere else for this ("[A]n optional…",
  "[c]an be created…"); both now read "[a] list…" / "[a] plugin…" for consistency. Also softens an
  evidence-level overstatement: "Home and Code began rolling out to Frontier" and "Autopilot
  expanded to private preview" stated as completed fact, sourced only to the 2026-09-25 blog post
  that *announces* both for "the coming weeks" / "the end of the month" — now "were slated to"
  with a note that the cited post announces rather than confirms shipping.

All other #803 fixes and a broad sample of #799's "confirmed" claims (Cowork/Code/Managed
Runtime/Researcher/Analyst/Agent 365 SDK model names, dates, caps, and quotes) were re-verified
against freshly fetched first-party Microsoft pages and held up.
