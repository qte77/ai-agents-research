### Fixed

- `docs/non-cc/reference/system-1-decision-models-landscape.md`: edgextract's library default
  decision model is `nimble` (Bespoke Labs), not `tev1` — the entry had the quickstart's explicit
  `--model tev1` and the README's actual stated default backwards. The JevEval (DeepEval) quote
  is corrected to the source's own wording and capitalization ("You define the logic, Jev makes
  the decisions, and DeepEval calculates the score," not "does the calculation"). The gold-set
  pricing comparison ("about 6× Jev's") is corrected to match the doc's own earlier pricing
  paragraph ("roughly 5.7×" — Clef is 5.7× Jev's rate, not 6×; 6× was only true of Clef-flash).
- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md`: the Strands Agents entry
  quoted AWS's AgentCore page as saying agents are "built on any framework" — that exact phrase
  appears nowhere on AgentCore's marketing or FAQ pages. Replaced with the page's actual hero-text
  quote, "Build with any framework, any model."
- `docs/non-cc/protocols/ag-ui-protocol-landscape.md`: the AWS Strands Agents / Bedrock AgentCore
  row said the TypeScript AG-UI integration "is still an open PR" — `ag-ui-protocol/ag-ui#1681`
  merged on 2026-05-26, six months before this row's own "checked 2026-11-11" stamp, and ships as
  the `@ag-ui/aws-strands` npm package. Strands' own docs page still says "This feature is only
  supported in Python," which the row now cites directly instead of the stale PR-status claim.
- `docs/cc-community/CC-community-plugins-landscape.md`: the lot-map entry said the Hooks-station
  row removed in 0.4.0 was "restored in 0.5.1" — the repo's own CHANGELOG shows it was restored in
  0.5.0 (0.5.1 only restored a demo video file). Also softened the privacy-claim attribution: the
  verbatim "makes no network requests..." sentence is the README's wording; `PRIVACY.md` states
  the same substance across separate bullets in different wording, not verbatim.

All other checked claims across #782, #786, #787, #788, #795, #797, #779 and #784 (licenses,
star/fork counts, benchmark numbers against the `decision-model-eval.yaml` run artifacts, and
every other quoted sentence) were confirmed against first-party sources and left unchanged.
