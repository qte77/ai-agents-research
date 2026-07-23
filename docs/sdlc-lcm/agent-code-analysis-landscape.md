---
title: Agent Code Analysis Landscape — SCA & DCA for AI Coding Agents
purpose: Static (SCA) and dynamic (DCA) code-analysis for AI coding agents — both directions (analysis OF agent-produced code, and agents PERFORMING analysis), the tooling, the GitHub/GitLab/Codeberg CI matrix, and sandboxing as an analysis boundary.
category: landscape
status: assess
created: 2026-07-23
updated: 2026-07-23
validated_links: 2026-07-23
---

**Status**: Assess

## What It Is

Two analysis modes bound a non-deterministic coding agent: **static code analysis (SCA)**
— inspecting source/config without running it — and **dynamic code analysis (DCA)** —
observing behavior at runtime. Both apply in **two directions**:

1. **Analysis _of_ agents** — scanning agent-generated code, skills, and MCP tool
   surfaces for vulnerabilities before they reach the host or the repo.
2. **Agents _performing_ analysis** — LLM agents used as the vulnerability-discovery
   engine (agent-as-scanner).

The ICLR 2026 paper [_A Framework for Formalizing LLM Agent Security_][iclr-formalize]
(Siu, He, Montgomery et al.) argues **why both modes are needed, not either alone**: it
decomposes agent security into four properties (task alignment, action alignment,
authorized instruction following, data isolation) and notes "the same action can
represent legitimate behavior or a security violation depending on who commanded it."
Static oracle-verification classifies an action pre-execution; dynamic monitoring is
required because single-shot benchmarks "miss temporal violations by resetting context
between evaluations" — provenance and information flow must be tracked _across_ turns.

This doc catalogs the tool mechanics and CI integration. For the vulnerability
_scoring/taxonomy_ layer (AIVSS, MITRE ATLAS) see
[agentic-ai-vulnerability-landscape.md](agentic-ai-vulnerability-landscape.md); for the
agent-config scanner (AgentSeal) and governance frameworks see
[ai-security-governance-analysis.md](ai-security-governance-analysis.md); for MAESTRO
multi-agent threat modeling see [mas-security-framework.md](mas-security-framework.md).
This landscape cross-references those rather than duplicating them.

## 1. Static Analysis (SCA) — analyzing agent code

| Tool | What | Agent integration | License |
|---|---|---|---|
| [CodeQL][codeql] | GitHub's semantic code-scanning engine | Default or advanced setup; SARIF upload; **Copilot Autofix** proposes AI fixes on alerts | Source-available (GitHub) |
| [Semgrep][semgrep] | 10,000+ rules, CI-job model | GitHub Actions / GitLab CI; findings to GHAS/GitLab dashboards | LGPL-2.1 (OSS engine) |
| [Semgrep Guardian][guardian] | Purpose-built for **AI-agent-generated code** | Bundles Semgrep **MCP server + Hooks + Skills** in one install; hooks "fire on every file write, ensuring a scan regardless of what the agent does"; scans via Semgrep Code + Supply Chain + Secrets | Commercial-tiered |
| [Bandit][bandit] | Python AST security linter | CLI / pre-commit / CI (used in this estate's own CI) | Apache-2.0 |
| [Trivy][trivy] | All-in-one: deps, containers, IaC, secrets, SBOM | CLI / CI action | Apache-2.0 |
| [agent-audit][agent-audit] | Static analyzer for **agent frameworks** | 51 rules mapped to OWASP Agentic Top 10; tool-boundary-aware taint (tracks `@tool` params → `eval`/`subprocess`/`cursor.execute`); LangChain/CrewAI/AutoGen | Not verified (repo LICENSE unchecked) |

**Semgrep Guardian** is the standout for the _analysis-of-agents_ direction: it targets
Claude Code, Codex, Cursor, GitHub Copilot, Kiro, Devin/Windsurf, and any MCP client,
scanning for OWASP Top 10 issues, malicious OSS packages, and hardcoded secrets in
agent-written code. Announced **2026-06-23** ([official blog][guardian-blog]). _Note:
rule-pack names/counts circulating on aggregator sites ("27/122/186 rules") are **not
confirmed on any first-party Semgrep source** and are omitted here._

`SkillSpector` (audits agent **Skills** for vulnerabilities) is a further agent-specific
static analyzer, but its coverage here is from a secondary writeup — treat as unverified
until its own repo is checked.

## 2. Dynamic Analysis (DCA) — observing agent behavior at runtime

- **[garak][garak]** (NVIDIA-backed research project, **Apache-2.0**) — the flagship
  DAST-for-LLMs analogue: a CLI probe/detector scanner that fires adversarial payloads
  at a running model/system and classifies the responses. Invoked e.g.
  `python3 -m garak --target_type openai --target_name gpt-5-nano --probes encoding`.
  Verified probe families (from its README) include `promptinject`, `dan` (jailbreak),
  `encoding` (encoded-payload evasion), `leakreplay` (training-data extraction),
  `malwaregen`, `xss`, `packagehallucination` (hallucinated/slopsquat package specs),
  `atkgen` (automated red-teaming), `realtoxicityprompts`, `glitch`, and `snowball`
  (hallucination escalation). Tests the _model's behavior_, complementing static
  code/config scanners.
- **[AgentSight][agentsight]** (arXiv:2508.02736; OSS `eunomia-bpf/agentsight`) —
  "boundary tracing": eBPF intercepts TLS-encrypted LLM traffic + kernel syscall events
  and causally correlates agent _intent_ to system _action_ across process boundaries,
  <3% overhead, zero-instrumentation, framework-agnostic. Detects prompt injection,
  resource-wasting reasoning loops, and multi-agent bottlenecks.
- **[VIPER-MCP][viper]** (arXiv:2605.21392) — hybrid **static + dynamic**: anchor-query
  taint analysis on MCP server tool handlers, plus dynamic validation via feedback-driven
  prompt evolution that generates concrete PoC exploits. Scanned 39,884 open-source MCP
  repos → **106 zero-days, 67 CVEs** assigned (paper-reported), responsibly disclosed —
  the strongest single result tying static+dynamic analysis to agent tool-call surfaces.
- **GitLab Libbehave** — experimental analyzer in GitLab Dependency Scanning that examines
  dependency **runtime behavior** for suspicious activity (Ultimate tier).
- **ARMO / Metoro** — commercial eBPF-based agent runtime monitoring/enforcement,
  Kubernetes-native, with behavioral-baseline enforcement.

## 3. Agents _Performing_ SCA/DCA (agent-as-scanner)

- **Google Cloud — [A Blueprint for AI-Assisted Vulnerability Management][gcloud-blueprint]**
  (2026-07-16, first-party). A two-track strategy whose Track 2 puts **LLM agents finding
  vulnerabilities in first-party code** via IDE tools + CI/CD runners. Cites **CodeMender**
  (Google DeepMind) for remediation (noted not-yet-public) and Model Armor as a guard
  model. Key stated findings: mean time-to-exploit has gone **negative (−7 days)** — exploited
  before a patch exists; LLM detection is **strongest on memory-unsafe code (C/C++/asm)
  with a binary crash/no-crash oracle**, **weakest on business-logic/authz flaws** and long
  contexts. Recommends reserving agent audits for high-impact components with a clear binary
  oracle and **requiring a deterministic test harness to prove an exploit before human
  review**. _(Single source; no Big Sleep/Project Zero reference in this post.)_
- **VulnAgent-R2** (arXiv:[2603.13384][vulnagent]) — evidence-calibrated multi-agent
  repository-level auditing; hybrid static (graph triage / cross-file dataflow) + dynamic
  (selective compilation + test execution to validate findings); reports 38.3% token
  reduction (paper-claimed).
- **VulnLLM-R** (arXiv:[2512.07533][vulnllm]) — a 7B reasoning-specialized model + agent
  scaffold that reasons about program states; **benchmarks directly against CodeQL (SAST)
  and AFL++ (fuzzing/DAST) and reportedly outperforms both** on real-world projects,
  discovering zero-days (paper-claimed — a signal that agent detection is now measured
  head-to-head against incumbent SCA/DCA tools, not just used alongside them).

## 4. CI-Forge Integration (verified first-party)

| Capability | GitHub | GitLab | Codeberg / Forgejo |
|---|---|---|---|
| Native SAST | CodeQL code scanning (default/advanced) | SAST template (Semgrep, SpotBugs, etc.); "Advanced SAST" (Ultimate) | **None native** |
| Native DAST | None (third-party Action + SARIF) | DAST + API Security analyzer, **Ultimate only** | **None** |
| Dependency scanning | Dependency graph + `dependency-review-action` (PR-gating) + Dependabot | Dependency Scanning (Ultimate; SBOM-based) + experimental Libbehave | **None** |
| AI-assisted remediation | **Copilot Autofix** on scanning alerts | **GitLab Duo**: FP triage + **Agentic SAST Vulnerability Resolution** (auto-MRs, Ultimate) | None |
| Interop | SARIF + webhooks + REST API | Dashboards / MR widgets | N/A |
| CI engine | Actions (GH-hosted runners) | GitLab CI/CD (hosted + self-managed) | **Forgejo Actions** (GH-Actions-syntax-_compatible, not identical_; Codeberg-hosted is **self-hosted-runner only**) or **Woodpecker CI** (`ci.codeberg.org`) |

**Codeberg/Forgejo is genuinely thin** — no native code-scanning/SARIF, SAST, DAST, or
dependency-scanning product on either. Any SCA/DCA there means hand-wiring a CLI
(Semgrep/CodeQL CLI/Trivy) into a self-hosted-runner Forgejo Actions workflow or a
Woodpecker pipeline. _Whether GitHub-marketplace security actions (e.g.
`github/codeql-action`, `aquasecurity/trivy-action`) run unmodified on Forgejo Actions is
**not confirmed** — Forgejo's docs explicitly hedge Actions compatibility; a trial-run
citation is needed before asserting portability._

## 5. Sandboxing as an Analysis Boundary

Isolation and analysis are different jobs. CC's own sandbox (bwrap/Seatbelt — see
[CC-sandboxing-analysis.md](../cc-native/sandboxing/CC-sandboxing-analysis.md)) contains
what agent-run code can _reach_, but its own docs state **"no traffic inspection — allowed
domains can carry any payload"**: it doesn't inspect _what_ the generated code does inside
the boundary. The field's answer to that gap:

- **eBPF boundary tracing** (AgentSight) and **hybrid taint+PoC validation** (VIPER-MCP)
  run _around_ the execution boundary to supply the behavioral visibility the sandbox
  lacks.
- **Ephemeral CI runners** (GitHub-hosted Actions runners, self-hosted Forgejo runners)
  play the same "isolate untrusted agent output before it touches the host/upstream repo"
  role at the CI layer — same security principle, different layer.
- Google's Blueprint (§3) names the operational form directly: **workload isolation in
  unprivileged containers**, least-privileged just-in-time identities, guard models,
  red-teaming the agents themselves, and toxic-flow runtime monitoring.

No first-party CC doc currently describes deliberately running SCA/DCA tooling _inside_ the
bwrap/Seatbelt sandbox as a pattern (e.g. Guardian's hook in a sandboxed agent loop) — a
synthesis opportunity, not an existing CC feature.

## 6. Frameworks & Standards (cross-ref, not duplicated)

- **OWASP Top 10 for Agentic Applications 2026** ([genai.owasp.org][owasp-agentic-top10],
  released 2025-12-09; OWASP Gen AI Security Project, 100+ contributors) — a peer-reviewed,
  risk-ranked list pivoting "from passive LLM risks to active agent behaviors" (delegation,
  multi-step execution). It is **distinct** from the OWASP LLM Top 10 (2025) and from
  MAESTRO (a multi-agent _threat-modeling methodology_, not a ranked list — covered in
  `mas-security-framework.md`). The corpus does not yet cite this list by name; new
  agent-analysis work should reference it directly. _(The 10 category names are behind a
  gated report PDF and are not enumerated here — verify at source.)_
- Precursor: OWASP ASI **"Agentic AI — Threats and Mitigations"** v1.0 (2025-02-17), a
  threat-modeling reference rather than a ranked top-10.
- MITRE ATLAS + OWASP AIVSS — the scoring/taxonomy layer, in
  [agentic-ai-vulnerability-landscape.md](agentic-ai-vulnerability-landscape.md).

## Adoption & Licensing Notes

- **OSS / free**: garak (Apache-2.0), Semgrep OSS engine, Bandit, Trivy, CodeQL (free on
  public repos), AgentSight/VIPER-MCP (research code).
- **Commercial-tiered**: Semgrep Guardian; GitLab DAST / Dependency-Scanning / Duo auto-fix
  (Ultimate); GitHub Advanced Security (private repos); ARMO/Metoro.
- **Research, not shipped products**: VIPER-MCP, AgentSight, VulnAgent-R2, VulnLLM-R,
  CodeMender (not public at time of Google's post).
- **Unverified**: agent-audit license; SkillSpector (secondary source); Forgejo-Actions
  portability of GitHub-marketplace security actions.

## Sources

| Source | Content |
|---|---|
| [garak][garak] · [NVIDIA/garak README][garak-gh] | LLM red-team probe/detector scanner; probe families, CLI, Apache-2.0 (first-party) |
| [Semgrep Guardian docs][guardian] · [announcement blog][guardian-blog] | Agent-generated-code scanner; launch 2026-06-23 (first-party; rule counts unconfirmable, omitted) |
| [CodeQL][codeql] · [Semgrep][semgrep] · [Bandit][bandit] · [Trivy][trivy] | SCA engines |
| [agent-audit][agent-audit] | Agent-framework static taint analyzer (repo; license unverified) |
| [AgentSight][agentsight] (arXiv:2508.02736) · [VIPER-MCP][viper] (arXiv:2605.21392) | eBPF boundary tracing; hybrid MCP taint+PoC (106 zero-days/67 CVEs, paper-reported) |
| [Google Cloud — AI-Assisted Vulnerability Management][gcloud-blueprint] | Agents-as-scanner blueprint, 2026-07-16, −7-day TTE, binary-oracle finding (first-party, single source) |
| [VulnAgent-R2][vulnagent] (2603.13384) · [VulnLLM-R][vulnllm] (2512.07533) · [ICLR formalization][iclr-formalize] (#10016279) | Agent-based detection papers (arXiv/ICLR-first-party; results paper-claimed) |
| [OWASP Top 10 for Agentic Applications 2026][owasp-agentic-top10] | Ranked agentic-risk list, 2025-12-09 (distinct from MAESTRO / LLM Top 10; categories not enumerated here) |
| [GitLab application security][gitlab-appsec] · [GitHub code scanning][gh-codescan] · [Forgejo Actions][forgejo-actions] | CI-forge SCA/DCA capability, verified per forge |

[iclr-formalize]: https://iclr.cc/virtual/2026/10016279
[codeql]: https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql
[semgrep]: https://semgrep.dev/docs/
[guardian]: https://docs.semgrep.dev/guardian
[guardian-blog]: https://semgrep.dev/blog/2026/introducing-semgrep-guardian-real-time-security-for-ai-written-code/
[bandit]: https://bandit.readthedocs.io/
[trivy]: https://trivy.dev/
[agent-audit]: https://github.com/HeadyZhang/agent-audit
[garak]: https://garak.ai/
[garak-gh]: https://github.com/NVIDIA/garak
[agentsight]: https://github.com/eunomia-bpf/agentsight
[viper]: https://arxiv.org/abs/2605.21392
[gcloud-blueprint]: https://cloud.google.com/blog/topics/threat-intelligence/ai-assisted-vulnerability-management/
[vulnagent]: https://arxiv.org/abs/2603.13384
[vulnllm]: https://arxiv.org/abs/2512.07533
[owasp-agentic-top10]: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
[gitlab-appsec]: https://docs.gitlab.com/user/application_security/
[gh-codescan]: https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning
[forgejo-actions]: https://forgejo.org/docs/latest/user/actions/
