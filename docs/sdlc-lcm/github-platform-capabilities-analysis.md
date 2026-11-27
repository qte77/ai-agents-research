---
title: GitHub Platform Capabilities (Actions, Dev Environments, Rules, Org and Enterprise)
purpose: Map of what the GitHub platform itself offers around code hosting for teams and agents, with the plan tier of each feature, from GitHub's own docs.
created: 2026-11-27
updated: 2026-11-27
validated_links_on: 2026-11-27
status: reference
---

**Details:** descriptive map of GitHub features; plan tiers, limits and preview status are from
`docs.github.com`, read 2026-11-27, and change often. Re-check the linked page before relying on a row.

## What It Is

GitHub is the forge most agent tooling in this corpus assumes. This doc maps the platform
features around it, as neutral reference: Actions (CI/CD), dev environments, rules and
enforcement, and organization, business and enterprise controls. Each row names the plan that
unlocks it, because that gate, not the feature name, decides whether a team can use it.

It complements, and does not repeat:

- [CC-github-actions-analysis.md](../cc-native/ci-remote/CC-github-actions-analysis.md): Claude Code's own GitHub Action, setup and runner sizing.
- [github-copilot-cloud-agent-analysis.md](../non-cc/agents/github-copilot-cloud-agent-analysis.md) and [github-copilot-cli-analysis.md](../non-cc/agents/github-copilot-cli-analysis.md): Copilot products.
- [agent-code-analysis-landscape.md § 4](agent-code-analysis-landscape.md#4-ci-forge-integration-verified-first-party): code-scanning and dependency features per forge.

## Plans at a glance

Plans, per [GitHub's plans][plans] (read 2026-11-27):

| Plan | Notes |
|---|---|
| Free (personal, organization) | Unlimited public and private repositories; private ones with a limited feature set. $12 included monthly compute usage for eligible Actions and cloud sandbox use (read 2026-11-27) |
| Pro (personal) | Adds protected branches, code owners and required reviewers in private repositories; $18 included compute (read 2026-11-27) |
| Team (organization) | Same private-repository tools as Pro plus team reviewers; option to buy Code Security, Secret Protection and Code Quality; $18 included compute (read 2026-11-27) |
| Enterprise | Two deployments: Enterprise Cloud (hosted) and Enterprise Server (self-hosted). Adds SAML SSO, SCIM, internal repositories, GitHub Connect, deployment protection rules for private repositories (read 2026-11-27) |
| Enterprise Cloud only | $300 included compute, 99.9% monthly uptime SLA, enterprise accounts, Enterprise Managed Users, audit log streaming, IP allow list, data residency option (read 2026-11-27) |

## Actions and workflows

| Capability | What it does | Plan or visibility gate (read 2026-11-27) |
|---|---|---|
| [GitHub-hosted runners][hosted] | GitHub-managed VMs (Ubuntu, Windows, macOS); eligible 2-core and 4-core Linux jobs run in a multi-cloud pool on AWS or Azure | Free, Pro and Team use multi-cloud automatically; Enterprise Cloud opts in |
| [Larger runners][larger] | More RAM, CPU and disk, static IPs, Azure private networking, GPU, runner groups, autoscaling | Team and Enterprise Cloud organizations only |
| Custom images | Prebuilt VM images from workflow YAML | Larger runners only |
| [Self-hosted runners][selfhosted] | Machines you run; repository- or organization-level | Actions on self-hosted runners is free ([plans][plans]) |
| [Reusable workflows][reuse] | Called with `jobs.<id>.uses`; up to 10 nesting levels and 50 unique called workflows per file; token permissions can only be reduced down the chain | Private callers can use private and public workflows; public callers only public |
| [Custom actions][custom] | Docker (Linux only), JavaScript or composite actions with an `action.yml` | Sharing publicly needs a public repository |
| [Environments and deployment protection][env] | Required reviewers (up to 6), wait timer (1 to 43,200 minutes), branch and tag restrictions, environment secrets | Required reviewers, wait timers, custom rules: public repositories only on Free, Pro, Team; private needs Enterprise. Environment secrets in private repositories need Pro, Team or Enterprise |
| Custom deployment protection rules | GitHub App-backed gates (up to 6 rules per environment) | Public preview (read 2026-11-27) |
| [OIDC to clouds][oidc] | Per-job short-lived JWT, so workflows get cloud tokens without stored secrets; repository custom properties can be claims | Repositories created after 2026-07-15 use an immutable default `sub` format with owner and repository IDs |
| [Concurrency][conc] | `concurrency` groups; by default one pending run per group, newer pending runs cancel older; queuing is opt-in | No plan gate stated on the page read |
| [Merge queue][mq] | Tests each pull request against the latest base plus queued changes; workflows must also trigger on `merge_group`; cannot be combined with wildcard branch patterns | Public repositories owned by an organization, and private repositories owned by organizations on Enterprise Cloud |
| [Artifact attestations][att] | Signed build provenance (SLSA v1.0 Build Level 2 on their own), verified with `gh attestation verify`; uses Sigstore | Public repositories on Free, Pro, Team; private and internal need Enterprise Cloud |

## Dev environments

- **[Codespaces][cs]:** cloud dev environments in a Docker container on a VM, from 2 cores and 8 GB up to 32 cores and 128 GB (read 2026-11-27); reachable from a browser, VS Code or `gh`.
- **Billing:** two meters, compute time while active and storage while it exists; prebuild creation also uses Actions compute ([billing][csbill]). Included allowance: Free 120 core hours and 15 GB per month, Pro 180 hours and 20 GB (read 2026-11-27, [plans][plans]).
- **Org controls:** spending limits, who pays, restrict machine types, idle timeout, retention period, cap on organization-billed codespaces ([cost management][csorg]). On Team, owners can enable or disable Codespaces for private repositories ([plans][plans]).
- **[Dev containers][dcintro]:** `devcontainer.json` in `.devcontainer/` (or `.devcontainer.json`); several configurations live in subdirectories, and settings are not inherited between files. The properties are defined by the open [Development Containers specification][devcspec] (repository licence CC-BY-4.0, 5,853 stars, read 2026-11-27).
- **[Prebuilds][prebuild]:** a workflow builds the codespace up to `onCreateCommand` and `updateContentCommand` (not `postCreateCommand`) per repository, branch and config file; they cost Actions minutes and storage. Plan gating of prebuilds is not stated on the page read.

Related in this corpus: [CC-sandbox-codespaces-friction.md](../cc-native/sandboxing/CC-sandbox-codespaces-friction.md) (Claude Code sandbox inside Codespaces and dev containers).

## Rules and enforcement

Two systems coexist and layer: all applicable protections apply, and where two define the same rule the most restrictive wins ([about rulesets][rulesets]).

| Mechanism | What it gives | Plan gate (read 2026-11-27) |
|---|---|---|
| [Protected branches][protected] | One rule per branch pattern | Public repositories on Free; private too on Pro, Team, Enterprise Cloud, Enterprise Server |
| [Repository rulesets][rulesets] | Many rulesets per branch or tag; enforcement status (Active, Disabled; Evaluate is documented on the organization-ruleset pages); visible to anyone with read access | Public repositories on Free; public and private on Pro, Team, Enterprise Cloud |
| Push rulesets | Block pushes by file path, path length, extension or size across the whole fork network | Team plan, internal and private repositories |
| [Organization rulesets][orgrules] | One ruleset targets many repositories, selected by name, deployment context or custom properties; Evaluate mode feeds Rule Insights | The dedicated page says Team or Enterprise plans; the repository page says Enterprise. Unresolved, see Not verified |
| [Available rules][avail] | Restrict create, update, delete; linear history; required deployments; signed commits; required pull request (approvals, code owner review, stale-review dismissal, merge method, required reviewer teams by file pattern); required status checks (strict or loose); block force pushes; code scanning, code quality and license compliance gates; metadata rules | Per rule; see next rows |
| Preview rules | Secret scanning results must be resolved; code coverage thresholds; extra approval for pull requests Copilot opens without a person attributed | Public preview (read 2026-11-27) |
| [Code owners][owners] | `CODEOWNERS` file; admins can require code owner approval | Public repositories on Free; private on Pro, Team, Enterprise |
| [Signed commits][signed] | Rule that only verified signatures can land on a branch | Available through rulesets and branch protection |
| [Custom properties][props] | Structured repository metadata set by organization owners; usable to target rulesets and as OIDC claims | Plan gate not stated on the page read |
| Bypass | A ruleset can list roles, teams or GitHub Apps allowed past it; delegated bypass for push rules routes requests to designated reviewers ([organization rulesets][orgrules]) | Per ruleset |

Required status checks report only if the workflow runs for the event that triggers them; with a merge queue, that includes `merge_group` ([merge queue][mq]). The docs read do not list a separate "required workflows" rule; whether the older organization-level required workflows feature still exists was not checked (see Not verified).

## Org, business and enterprise features

| Area | What it is | Gate (read 2026-11-27) |
|---|---|---|
| [Enterprise Managed Users][emu] | Accounts provisioned and authenticated from your identity provider (SAML or OIDC, SCIM); managed accounts cannot create public content or collaborate outside the enterprise | Enterprise Cloud |
| [Audit log streaming][auditstream] | Streams audit and Git events to a SIEM as compressed JSON; 7-day buffer when paused; at-least-once delivery. Streaming Copilot agent session events is in public preview, for enterprises with EMU on GitHub.com or data residency | Enterprise Cloud; configured by enterprise owners |
| [Enterprise policies][policies] | One place to enforce or delegate organization-level settings; by default none are enforced | Enterprise accounts |
| [Advanced Security products][ghas] | **Secret Protection** (secret scanning, push protection, AI-detected secrets, custom patterns, delegated bypass) and **Code Security** (code scanning, CodeQL CLI, Copilot Autofix, dependency review, security campaigns, Dependabot auto-triage rules) | Purchasable on Team or Enterprise; for private repositories you must buy the product |
| Dependabot alerts, dependency graph | Included in all plans per the same page | All plans |
| [Push protection][pushprot] | Blocks a push that contains a detected secret before it reaches the repository | Part of Secret Protection for private repositories; some secret scanning runs by default on public repositories |
| [Copilot policies][copol] | Enterprise or organization policies set which Copilot features, agents and models users get; enable, disable or "let organizations decide"; apply to users on a Copilot Business or Enterprise licence; least restrictive wins across organizations of one enterprise, most restrictive across enterprises | Copilot Business or Copilot Enterprise; set by enterprise owners ([manage][copent]) |

## Agent surfaces

What an agent can drive without a browser:

| Surface | Notes |
|---|---|
| [REST API][rest] and [GraphQL API][gql] | Endpoints per resource; GraphQL has schema introspection and its own rate limits. Rulesets are manageable through both ([rulesets docs][orgrules]) |
| [`gh` CLI][ghcli] | Open source; repositories, issues, pull requests, reviews, merging; `cli/cli` is MIT (read 2026-11-27) |
| [GitHub MCP server][mcp-repo] | Official; MIT, 34,797 stars (read 2026-11-27). Remote server hosted by GitHub (reachable at the `api.githubcopilot.com/mcp/` endpoint per the README) with toolset configuration; GitHub Enterprise Server does not support the hosted remote server, the local one is used (README, read 2026-11-27) |
| Copilot cloud agent | See [github-copilot-cloud-agent-analysis.md](../non-cc/agents/github-copilot-cloud-agent-analysis.md) and [github-copilot-cli-analysis.md](../non-cc/agents/github-copilot-cli-analysis.md) |
| Claude Code in Actions | See [CC-github-actions-analysis.md](../cc-native/ci-remote/CC-github-actions-analysis.md) |
| Review products on top of the PR flow | [code-review-products-landscape.md](../non-cc/infrastructure/code-review-products-landscape.md) |

Agents run under the same gates as people: required checks, rulesets, environments and OIDC trust all apply to a pull request or deployment an agent opens, which is why this doc is organised by gate.

## Not verified

- **Organization rulesets plan gate:** the creating-rulesets page says Team or Enterprise; the repository rulesets page says organizations on the Enterprise plan. Both read 2026-11-27; not reconciled.
- **Required workflows:** not found in the current available-rules page; not checked whether the older feature was retired or moved.
- **Prebuild and custom property plan gating:** the pages read state none.
- **Prices per minute or per seat:** deliberately left out; read the pricing page.
- **Merge queue, attestations for private repositories:** gates are copied from each page's "who can use" box; not tested on an account.

## Sources

| Source | Content |
|---|---|
| [GitHub's plans][plans] | Plan tiers and included allowances |
| [GitHub-hosted runners][hosted], [larger runners][larger], [self-hosted runners][selfhosted] | Runner types and plan gating |
| [Reusable workflows][reuse], [custom actions][custom] | Reuse limits, action types |
| [Deployments and environments][env] | Protection rules and plan gating |
| [OIDC][oidc], [concurrency][conc], [merge queue][mq], [artifact attestations][att] | Actions security and flow control |
| [Codespaces][cs], [billing][csbill], [org cost management][csorg], [prebuilds][prebuild], [dev containers][dcintro], [spec repo][devcspec] | Dev environments |
| [About rulesets][rulesets], [available rules][avail], [organization rulesets][orgrules], [protected branches][protected], [code owners][owners], [signature verification][signed], [custom properties][props] | Rules and enforcement |
| [Enterprise Managed Users][emu], [audit log streaming][auditstream], [enterprise policies][policies], [Advanced Security][ghas], [push protection][pushprot] | Enterprise and security |
| [Copilot policies][copol], [enterprise Copilot policies][copent] | Copilot governance |
| [REST][rest], [GraphQL][gql], [GitHub CLI][ghcli], [github-mcp-server][mcp-repo] | Agent surfaces |

[plans]: https://docs.github.com/en/get-started/learning-about-github/githubs-plans
[hosted]: https://docs.github.com/en/actions/concepts/runners/github-hosted-runners
[larger]: https://docs.github.com/en/actions/concepts/runners/larger-runners
[selfhosted]: https://docs.github.com/en/actions/concepts/runners/self-hosted-runners
[reuse]: https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations
[custom]: https://docs.github.com/en/actions/concepts/workflows-and-actions/custom-actions
[env]: https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments
[oidc]: https://docs.github.com/en/actions/concepts/security/openid-connect
[conc]: https://docs.github.com/en/actions/concepts/workflows-and-actions/concurrency
[mq]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue
[att]: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations
[cs]: https://docs.github.com/en/codespaces/about-codespaces/what-are-codespaces
[csbill]: https://docs.github.com/en/billing/concepts/product-billing/github-codespaces
[csorg]: https://docs.github.com/en/codespaces/managing-codespaces-for-your-organization/managing-the-cost-of-github-codespaces-in-your-organization
[prebuild]: https://docs.github.com/en/codespaces/prebuilding-your-codespaces/about-github-codespaces-prebuilds
[dcintro]: https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers
[devcspec]: https://github.com/devcontainers/spec
[rulesets]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
[avail]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
[orgrules]: https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-organization-settings/creating-rulesets-for-repositories-in-your-organization
[protected]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
[owners]: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
[signed]: https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification
[props]: https://docs.github.com/en/organizations/managing-organization-settings/managing-custom-properties-for-repositories-in-your-organization
[emu]: https://docs.github.com/en/enterprise-cloud@latest/admin/concepts/identity-and-access-management/enterprise-managed-users
[auditstream]: https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/streaming-the-audit-log-for-your-enterprise
[policies]: https://docs.github.com/en/enterprise-cloud@latest/admin/concepts/security-and-compliance/enterprise-policies
[ghas]: https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security
[pushprot]: https://docs.github.com/en/code-security/concepts/secret-security/push-protection
[copol]: https://docs.github.com/en/copilot/concepts/enterprise/policies
[copent]: https://docs.github.com/en/enterprise-cloud@latest/copilot/how-tos/administer-copilot/manage-for-enterprise/manage-enterprise-policies
[rest]: https://docs.github.com/en/rest/about-the-rest-api/about-the-rest-api
[gql]: https://docs.github.com/en/graphql/overview/about-the-graphql-api
[ghcli]: https://docs.github.com/en/github-cli/github-cli/about-github-cli
[mcp-repo]: https://github.com/github/github-mcp-server
