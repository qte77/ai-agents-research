---
title: Code Forge, CI/CD and Runner Alternatives to GitHub Landscape
purpose: Dated survey of the well-known code forges, CI/CD systems and GitHub Actions runner services that compete with or sit next to GitHub, with licence, hosting, agent surface and migration path per row.
created: 2026-11-27
updated: 2026-11-27
validated_links_on: 2026-11-27
status: assess
---

**Details:** survey of products read from their own docs, release pages and licence files on 2026-11-27. Volatile facts
(versions, stars, prices, plan names, preview or GA labels) carry `(read 2026-11-27)`. Abbreviations are expanded in
[../glossary.md](../glossary.md).

Three separate choices hide behind "alternatives to GitHub", and teams make them independently: where the Git
repositories and reviews live (a **code forge**), what runs the builds (a **CI/CD system**), and which machines run
the jobs when the workflows are GitHub Actions (a **runner service**). This doc keeps the three apart. GitHub's own
features, by plan tier, are in [github-platform-capabilities-analysis.md](github-platform-capabilities-analysis.md). GitLab Community Edition as an application lifecycle management (ALM) option is
covered in [oss-alm-landscape.md](oss-alm-landscape.md), so this doc does not repeat its ALM assessment; GitLab's row here adds the agent surface and
migration path that doc lacks. How GitHub, GitLab and Codeberg/Forgejo compare as hosts for code analysis in CI is in
[agent-code-analysis-landscape.md § 4](agent-code-analysis-landscape.md#4-ci-forge-integration-verified-first-party).

**Leads, not evidence.** Four pages pointed us at candidates: [Blacksmith's home page][bs-home],
[openalternative.co's list][lead-oa], [Spacelift's Actions-alternatives article][lead-sp] and
alternativeto.net's GitHub Actions page (plain-text URL in Sources: it returns 403 to the link checker). They are aggregators or vendors with a stake. Every fact below comes from
the product's own docs, repository or licence file, except where a row says otherwise.

## 1. Code forges

"Agent surface" means what a coding agent can drive: the documented API and any official Model Context Protocol (MCP)
server. "Not read" means we did not find or fetch a page that settles it, not that the feature is absent. Feature-by-feature comparison of the main forges: [Capability map](#capability-map-across-forges).

| Forge | Hosting | Licence | Built-in CI | Agent surface | Migration from GitHub |
|---|---|---|---|---|---|
| GitLab | SaaS (GitLab.com), self-managed, Dedicated | Community Edition code MIT; Enterprise Edition under a separate licence with more restrictions ([licensing][gl-lic]) | GitLab CI/CD (see [§ 2](#2-cicd-systems)) | Official GitLab MCP server, generally available since 19.5 and in the Free tier since 19.2 (read 2026-11-27) ([docs][gl-mcp]) | Built-in GitHub importer for projects; groups and organisations are not imported; UI imports only from github.com, GitHub Enterprise Server needs the import API ([docs][gl-import]) |
| Bitbucket (Atlassian) | Cloud; Data Center self-managed | Commercial (Atlassian) | Bitbucket Pipelines (YAML in `bitbucket-pipelines.yml`, self-hosted runners) ([docs][bb-ci]) | Atlassian Rovo MCP server lists Bitbucket Cloud tools with separate read and write scopes; they only appear when the workspace is linked to an organisation ([tools][bb-tools]) | Import-repository dialog takes a GitHub or GitLab URL plus a personal access token ([docs][bb-import]). Data Center: Atlassian says Bitbucket and Bamboo Data Center will not end of life in 2029 but move to a hybrid licence (read 2026-11-27) ([page][bb-dc]) |
| Azure DevOps Repos (Microsoft) | Azure DevOps Services; Azure DevOps Server self-hosted | Commercial (Microsoft) | Azure Pipelines (integrates with GitHub as well as Azure Repos) ([docs][ado-pipe]) | Azure DevOps MCP server, remote (Microsoft Entra only, recommended) and local (needed for clients without dynamic client registration, e.g. Claude Code); local repo `microsoft/azure-devops-mcp` MIT, 2,097 stars (read 2026-11-27) ([docs][ado-mcp], [repo][ado-mcp-repo]) | Imports a Git repository from GitHub, Bitbucket, GitLab or elsewhere into a new or empty repo ([docs][ado-import]) |
| Gitea | Self-hosted; vendor-run Gitea Cloud and Enterprise offerings exist | MIT, 59,308 stars, v28.4.0 on 2026-11-15 (read 2026-11-27) ([repo][gitea-repo]) | Gitea Actions, designed to be compatible with GitHub Actions with listed differences ([docs][gitea-cmp]) | Official `gitea/gitea-mcp` server, 113 stars (read 2026-11-27) ([repo][gitea-mcp]) | Built-in migration form for GitHub; issues and pull requests need at least a username ([docs][gitea-mig]) |
| Forgejo | Self-hosted; [Codeberg](#codeberg-and-agent-written-code) runs a public instance | GPL v3 or later from v9.0, MIT up to v8.0 ([FAQ][fj-faq]); v17.0.2 released 2026-11-18 (read 2026-11-27) ([releases][fj-rel]) | Forgejo Actions, "familiar", explicitly not designed to be compatible with GitHub Actions ([docs][fj-gha]) | REST API documented in the user guide; official MCP server: none found in the docs we read | "New migration" in the web UI keeps history and tags ([docs][fj-first]) |
| Harness Open Source | Self-hosted container | Apache-2.0, 38,985 stars, v2.28.3 on 2026-11-26 (read 2026-11-27) (`gh api`) | Built-in pipelines; README says Drone parity is still a goal ([README][harness-repo]) | Not read | Not read |
| SourceHut | Hosted public service; software is free and open source per its home page | Licence file not read | builds.sr.ht, YAML build manifests submitted via API ([docs][sh-builds]) | GraphQL API ([git.sr.ht docs][sh-git]); the site says it has no AI features | No importer found in the docs read; the documented route is pushing to git.sr.ht. The service states it is a public alpha (read 2026-11-27) ([home][sh-home]) |
| Gerrit | Self-hosted | Apache-2.0 ([licences][ger-lic]) | None; integrates Jenkins, Zuul and webhooks ([site][ger-home]) | REST API ([site][ger-home]) | None found; Gerrit is a patch-set review layer over Git, not a hosting migration target. Used by Android and Chromium per its site |

### Codeberg and agent-written code

Codeberg e.V. members voted in July 2026 to change the
terms of use to prohibit "vibe-coded projects". Separately, the post's informal guidelines say projects created by
autonomous LLM agents, projects written and maintained with heavy LLM use, and LLM-ecosystem tools "might no longer be
welcome", and it says nothing will be mass-deleted ([Codeberg blog, 2026-07-23][cb-llm]). SourceHut announced on 2026-08-27 that its terms would prohibit
original content written with or facilitating generative AI for new projects, effective after a two-week notice period, i.e. 2026-09-10, with no retroactive enforcement against existing projects
([SourceHut blog][sh-llm]). For agent-heavy teams this is a selection criterion in its own right:
GitLab, Gitea, Bitbucket and Azure DevOps do not carry such a clause in the pages we read, but we did not search their
terms of service.

## Capability map across forges

One row per capability, one column per forge, so a team can see where a feature exists, what plan unlocks it and where
the docs we read say nothing. Plan tiers, prices and preview, beta or general-availability status are all
`(read 2026-11-27)`. "Not documented on the pages read" means exactly that: we read the pages linked in the row, found no statement, and infer nothing. It is not a claim that the feature is absent. The
GitHub column points at [github-platform-capabilities-analysis.md](github-platform-capabilities-analysis.md) instead of
re-sourcing facts that doc already holds; the three code-analysis rows match
[agent-code-analysis-landscape.md § 4](agent-code-analysis-landscape.md#4-ci-forge-integration-verified-first-party)
and stay minimal. Codeberg is a public Forgejo instance, so the Forgejo column covers both and names Codeberg only where
its own docs differ. The Gitea column mixes the open-source docs with the vendor's Enterprise product page, and says which.

| Capability | GitHub | GitLab | Codeberg / Forgejo | Gitea | Bitbucket Cloud | Azure DevOps |
|---|---|---|---|---|---|---|
| Built-in CI | Actions ([§][gh-actions]) | GitLab CI/CD ([docs][cm-gl-ci]) | Forgejo Actions ([docs][fj-gha]) | Gitea Actions ([docs][cm-gt-actions]) | Bitbucket Pipelines ([docs][bb-ci]) | Azure Pipelines ([docs][ado-pipe]) |
| Vendor-hosted runners | GitHub-hosted, larger runners on Team and Enterprise Cloud ([§][gh-actions]) | Hosted runners for Linux and GPU, macOS and Windows in beta; Free, Premium, Ultimate listed ([docs][cm-gl-hosted]) | Codeberg: Woodpecker at `ci.codeberg.org` by request; Actions runners are self-hosted ([docs][cb-ci]) | Not documented on the pages read | Atlassian cloud runners; Free plan 50 build minutes ([pricing][cm-bb-price]) | Microsoft-hosted agents; one free job, 1,800 minutes a month, organization linked to an Azure subscription ([docs][cm-ado-hosted], [pricing][cm-ado-price]) |
| Self-hosted runners | Free to use ([§][gh-actions]) | GitLab Runner ([docs][cm-gl-runner]) | Forgejo Runner ([docs][cm-fj-runner]) | Gitea Runner ([docs][cm-gt-runner]) | Runners, no build minutes charged ([docs][cm-bb-runners]) | Self-hosted agents; one free job, $15 per extra ([docs][cm-ado-self], [pricing][cm-ado-price]) |
| Merge queue or merge trains | Public org repos; private needs Enterprise Cloud ([§][gh-actions]) | Merge trains, Premium and Ultimate ([docs][cm-gl-trains]) | Not documented on the pages read | Merge queues ticked in Gitea's own comparison page ([docs][cm-gt-cmp]) | Merge queues; paid Standard or Premium, needs Pipelines ([docs][cm-bb-mq]) | Not documented on the pages read |
| Branch protection and rulesets | Protected branches; repo and org rulesets, org ones on Team or Enterprise ([§][gh-rules]) | Protected branches Free; user and group allowlists Premium ([docs][cm-gl-protected]) | Per-repo branch and tag protection ([docs][cm-fj-protect]); org level not documented | Per-repo protected branches ([docs][cm-gt-protected]); org-wide inheritance is an Enterprise feature ([page][cm-gt-ent]) | Branch restrictions per branch or pattern ([docs][cm-bb-branch]) | Branch policies per branch ([docs][cm-ado-policies]); project-wide scope not read |
| Required status checks | Ruleset rule, strict or loose ([§][gh-rules]) | Pipelines-must-succeed on Free; external status checks Ultimate ([docs][cm-gl-merge], [docs][cm-gl-checks]) | Not documented on the pages read | Status checks section on the protected-branches page ([docs][cm-gt-protected]) | Merge checks; blocking a merge needs Premium, lower plans only warn ([docs][cm-bb-checks]) | Build validation and status-check policies ([docs][cm-ado-policies]) |
| Code owners | `CODEOWNERS`; private repos on Pro, Team, Enterprise ([§][gh-rules]) | Code owners, Premium and Ultimate ([docs][cm-gl-owners]) | `CODEOWNERS` file requests reviews on a pull request ([docs][cm-fj-pr]) | `CODEOWNERS` file in three documented paths ([docs][cm-gt-owners]) | `.bitbucket/CODEOWNERS` adds suggested reviewers ([docs][cm-bb-owners]) | Path-based auto-included reviewers; no `CODEOWNERS` file on the pages read ([docs][cm-ado-owners]) |
| Dev environments | Codespaces ([§][gh-dev]) | Workspaces, Premium and Ultimate ([docs][cm-gl-ws]) | Not documented on the pages read | Not documented on the pages read | Not documented on the pages read | Not documented on the pages read |
| Secret scanning with push protection | Secret Protection, bought on Team or Enterprise ([§][gh-org]) | Secret push protection blocks a push, Free to Ultimate ([docs][cm-gl-secret]) | None native ([§ 4][aca-4]) | Not documented on the pages read | Not documented on the pages read | GitHub Secret Protection for Azure DevOps, $19 per committer a month ([docs][cm-ado-ghas], [pricing][cm-ado-price]) |
| Code scanning and SAST | Code Security with CodeQL ([§][gh-org], [§ 4][aca-4]) | SAST; Advanced SAST Ultimate ([docs][cm-gl-sast], [§ 4][aca-4]) | None native ([§ 4][aca-4]) | Not documented on the pages read | Not documented on the pages read | Code Security for Azure DevOps, CodeQL, $30 per committer a month ([docs][cm-ado-ghas]) |
| Dependency updates | Dependabot alerts on all plans ([§][gh-org], [§ 4][aca-4]) | Dependency scanning Ultimate ([docs][cm-gl-dep], [§ 4][aca-4]); update pull requests not documented | None native ([§ 4][aca-4]) | Dependency scanning in Enterprise ([page][cm-gt-ent]); update pull requests not documented | Not documented on the pages read | Dependency scanning alerts ([docs][cm-ado-ghas]); update pull requests not documented |
| Package registry | GitHub Packages: container (Docker), npm, Maven, Gradle, NuGet, RubyGems ([docs][cm-gh-pkg]) | Package registry, Free and above ([docs][cm-gl-pkgreg]) | Built-in, many package types ([docs][cm-fj-pkgs]) | Built-in, many package types ([docs][cm-gt-pkgs]) | Bitbucket Packages: containers, npm, Maven; PyPI and NuGet "coming soon" ([page][cm-bb-pkgs]) | Azure Artifacts: npm, NuGet, Maven, Python, Cargo, Universal; 2 GiB free ([docs][cm-ado-art]) |
| Enterprise SSO and SCIM | Enterprise Cloud Managed Users: SAML or OIDC, SCIM ([§][gh-org]) | SAML SSO and SCIM for GitLab.com groups, Premium and Ultimate ([docs][cm-gl-saml], [docs][cm-gl-scim]) | LDAP and an OAuth2 provider documented; SAML, SCIM not found ([docs][cm-fj-auth]) | OAuth2, OpenID Connect, LDAP in docs ([docs][cm-gt-auth]); SAML 2.0 in Enterprise ([page][cm-gt-ent]) | SAML SSO and SCIM 2.0 need Atlassian Guard Standard, Atlassian-wide ([docs][cm-bb-sso], [docs][cm-bb-scim]) | Microsoft Entra ID sign-in ([docs][cm-ado-entra]); SCIM not documented on the pages read |
| Audit log | Streaming on Enterprise Cloud ([§][gh-org]) | Audit events Free; group and project events Premium and Ultimate ([docs][cm-gl-audit]) | Not documented on the pages read | Documented, recording off by default ([docs][cm-gt-audit]); Enterprise page also lists it | Organization audit log, access by subscription plan ([docs][cm-bb-audit]) | Public preview, 90-day retention, streaming ([docs][cm-ado-audit]) |
| Official MCP server | GitHub MCP server, MIT ([§][gh-agent]) | GitLab MCP server, generally available ([§ 1](#1-code-forges)) | None found in the docs read ([§ 1](#1-code-forges)) | `gitea/gitea-mcp` ([§ 1](#1-code-forges)) | Rovo MCP server lists Bitbucket Cloud tools ([§ 1](#1-code-forges)) | Remote server (Entra only) and local server ([§ 1](#1-code-forges)) |
| Vendor's own coding agent | Copilot cloud agent ([doc][gh-copilot-agent]) | Duo Agent Platform, Premium and Ultimate, generally available in 18.8 ([docs][cm-gl-duo]) | Not documented on the pages read | Not documented on the pages read | Rovo Dev through Agentic Pipelines, needs paid Rovo Dev Standard; Claude Code and Codex also supported ([docs][cm-bb-agentic]) | Boards work items hand off to Copilot coding agent; GitHub repos only, not Azure Repos ([docs][cm-ado-copilot]) |

## 2. CI/CD systems

Separate from the forge: most of these run against GitHub repositories too. "Runs GitHub Actions workflows?" is only
"yes" where the vendor documents it.

| System | Hosting | Licence | Config format | Runs GitHub Actions workflows? | Agent surface |
|---|---|---|---|---|---|
| GitLab CI/CD | With GitLab (SaaS or self-managed) | As GitLab ([§ 1](#1-code-forges)) | `.gitlab-ci.yml` ([ref][gl-ci]) | No, own format | GitLab MCP server ([§ 1](#1-code-forges)) |
| CircleCI | SaaS; self-hosted runners | Commercial | `.circleci/config.yml` ([ref][circle-cfg]) | No, own format | Hosted MCP server and a CLI-based MCP server (read 2026-11-27); the older npx server is deprecated ([docs][circle-mcp]) |
| Buildkite | SaaS control plane; agents on Buildkite-hosted or your own infrastructure | Agent MIT, 1,111 stars (read 2026-11-27) (`gh api`); platform commercial | `pipeline.yml` or steps stored in Buildkite ([docs][bk-steps]) | No, own format | Official open-source MCP server (`buildkite/buildkite-mcp-server`, MIT, 56 stars (read 2026-11-27)), remote OAuth or local ([docs][bk-mcp]) |
| Jenkins | Self-hosted | MIT, 26,821 stars (read 2026-11-27) (`gh api`) | `Jenkinsfile` ([docs][jk-file]) | No, own format | MCP Server plugin on the plugin index; `jenkinsci/mcp-server-plugin`, MIT, 121 stars (read 2026-11-27) ([plugin][jk-mcp]) |
| Azure Pipelines | With Azure DevOps (Services or Server) | Commercial | Not read | No | Azure DevOps MCP server ([§ 1](#1-code-forges)) |
| Woodpecker CI | Self-hosted; Codeberg runs `ci.codeberg.org` ([docs][cb-ci]) | Apache-2.0, 8,295 stars (read 2026-11-27) (`gh api`) | Own YAML workflow syntax ([docs][wp-syntax]) | No, own syntax | Not read |
| Gitea Actions and Forgejo Actions | With the forge | As the forge | GitHub Actions-style YAML | Gitea: largely, with documented gaps; its comparison page lists unsupported syntax, including complex `runs-on` values ([compare][gitea-cmp]). Forgejo: a familiar format, but compatibility is not a goal ([docs][fj-gha]) | Forge API |
| Dagger | Engine runs on your machine or on a shared remote engine | Apache-2.0, 16,655 stars (read 2026-11-27) (`gh api`); docs show version 1.0-beta (read 2026-11-27) | Typed modules instead of YAML ([intro][dagger]) | No; it can sit under any CI that calls it | Positioned by its docs for coding agents; no MCP server claim read |

IaC-focused platforms are a different kind of CI/CD: they run Terraform, OpenTofu and similar plans and applies with
policy and state handling rather than general builds. [Spacelift][sl-docs] (commercial; its docs list a Spacelift MCP
server) and [Atlantis][atlantis] (open source pull-request automation for Terraform, Apache-2.0, 9,374 stars (read
2026-11-27) (`gh api`)) are the examples we read; neither replaces a general CI system.

## 3. Faster or cheaper runners for GitHub Actions

These keep GitHub as the forge and the workflow format and change only where jobs run. Every speed and price figure
below is a **vendor claim**, not a measurement of ours, `(read 2026-11-27)`.

| Service | How it plugs in | Where jobs run | Pricing model | Vendor claims |
|---|---|---|---|---|
| Blacksmith | GitHub App on the org, then `runs-on: blacksmith-<n>vcpu-ubuntu-<version>` ([docs][bs-docs]) | Blacksmith bare-metal gaming CPUs in us-east, us-west, eu-west, eu-central ([docs][bs-docs]) | Per minute: Ubuntu x64 2-vCPU runner listed at $0.004/min, 3,000 free minutes per month; add-ons for Docker layer cache and static IPs ([pricing][bs-price]) | Its pages disagree with each other: "60% less" than GitHub runners on the home page ([home][bs-home]) versus "33% cheaper per minute" and "67% total cost savings" on the pricing page, the latter assuming a 2x faster runtime. Also 2x faster hardware, 4x faster cache downloads, 12,000+ teams |
| Depot | `runs-on: depot-ubuntu-24.04` label ([docs][dp-docs]) | Depot cloud, or your own AWS account; ephemeral EC2 instance per job ([docs][dp-docs]) | $0.006/min for the base 2-vCPU Linux runner, 2,000 minutes included on the Developer plan (read 2026-11-27) ([pricing][dp-price]) | Up to 3x faster than GitHub-hosted runners, 10x faster cache |
| Namespace | Connect the GitHub org in the dashboard, create a runner profile, set `runs-on: namespace-profile-<name>` ([docs][ns-docs]) | Namespace-managed | "Unit minutes"; Team plan $100/month with 100,000 unit minutes, Business $250/month with 250,000 (read 2026-11-27) ([pricing][ns-price]) | No numeric speed claim read; its docs only say larger shapes may be faster and smaller ones cheaper |
| RunsOn | CloudFormation stack in your AWS account | Your AWS account; EC2, EBS and S3 at cost on your AWS bill | Flat annual licence from EUR 300 (under 50,000 jobs per month), free for open source and non-commercial use with a link back ([pricing][ro-price]) | "4-15x cheaper than GitHub"; per-instance price tables on its site. Licence caveat: the public repo's MIT licence covers only CloudFormation assets and supporting files, while the server and agent are commercially licensed ([README][ro-repo]) |
| Ubicloud | Change the label to `ubicloud-standard-2` after linking the GitHub account ([docs][ub-docs]) | Ubicloud-managed | Per-minute; see its pricing page ([docs][ub-price]) | "7x cheaper" and faster because of newer hardware than GitHub's Azure VMs ([docs][ub-price]). Open source, AGPL-3.0, 12,428 stars (read 2026-11-27) ([repo][ub-repo]) |

## When teams move off GitHub (or keep it and swap CI)

Our synthesis, not a sourced finding. Teams that only want faster or cheaper builds keep GitHub and the workflow files, change the
`runs-on` label in each job and install the vendor's GitHub App (or, for RunsOn, deploy its stack in their own AWS
account); of the three moves this one changes the least.
Teams that want a different CI system keep GitHub as the forge and add a pipeline definition elsewhere. Teams that
move the forge carry the biggest cost: the CI definition changes too, since Gitea Actions is the only system here that aims at the GitHub
Actions format (with documented gaps) and Forgejo Actions keeps it familiar without aiming at compatibility. For agent-driven work, check three things before
choosing: an official MCP server for the forge and for the CI system, how the platform's terms treat agent-written
code ([§ 1](#1-code-forges), Codeberg and SourceHut note), and whether the migration tool carries over issues and
reviews or only Git history.

## Not included

Each reason names its criterion: pruned under the [well-known, performance-optimised filter](../../CONTRIBUTING.md#pruning-entries-well-known-performance-optimised-filter)
or deferred (named, not yet read first-party).

| Name | Reason | Date | Link |
|---|---|---|---|
| Agola | 1,632 stars; last push 2025-09-24, older than 12 months (`gh api`) | 2026-11-27 | [repo][agola] |
| WarpBuild | Deferred: product page and docs read, but no row written in this pass | 2026-11-27 | [docs][wb-docs] |
| TeamCity (JetBrains) | Deferred: well-known, but its licence and agent-surface pages were not read first-party in this pass (they load as of 2026-11-27) | 2026-11-27 | [docs][tc-docs] |
| Gogs | Deferred: 48,007 stars, active MIT project (`gh api`), but its docs were not read first-party in this pass | 2026-11-27 | [repo][gogs] |
| Octopus Deploy, Devtron, Northflank, Travis CI, AWS CodePipeline, Launchpad, SourceForge, RhodeCode | Scope: deployment, Kubernetes or hosting-platform products rather than forges or CI (Octopus Deploy, Devtron, Northflank, AWS CodePipeline); deferred, not read first-party in this pass (Travis CI, Launchpad, SourceForge, RhodeCode) | 2026-11-27 | [Spacelift lead][lead-sp], [openalternative lead][lead-oa] |

## Sources

| Source | Content |
|---|---|
| [GitLab licensing][gl-lic] · [package licence][gl-pkg] | CE MIT, EE separate licence |
| [GitLab MCP server][gl-mcp] · [GitHub import][gl-import] · [CI reference][gl-ci] | Agent surface, importer, config |
| [Bitbucket Pipelines][bb-ci] · [GitHub import][bb-import] · [Rovo MCP tools][bb-tools] · [Data Center note][bb-dc] | Atlassian forge facts |
| [Azure Pipelines][ado-pipe] · [Azure DevOps MCP][ado-mcp] · [repo import][ado-import] · [MCP repo][ado-mcp-repo] | Microsoft forge facts |
| [Gitea repo][gitea-repo] · [Actions comparison][gitea-cmp] · [migration][gitea-mig] · [gitea-mcp][gitea-mcp] | Gitea |
| [Forgejo FAQ][fj-faq] · [releases][fj-rel] · [Actions vs GitHub Actions][fj-gha] · [first repository][fj-first] | Forgejo |
| [Codeberg CI docs][cb-ci] · [Codeberg LLM post][cb-llm] | Codeberg hosting and LLM policy |
| [SourceHut home][sh-home] · [builds][sh-builds] · [git][sh-git] · [LLM terms post][sh-llm] | SourceHut |
| [Gerrit site][ger-home] · [licences][ger-lic] · [Harness README][harness-repo] | Gerrit, Harness |
| [CircleCI config][circle-cfg] · [CircleCI MCP][circle-mcp] · [Buildkite steps][bk-steps] · [Buildkite MCP][bk-mcp] · [Jenkinsfile][jk-file] · [Jenkins MCP plugin][jk-mcp] · [Woodpecker syntax][wp-syntax] · [Dagger][dagger] | CI systems |
| [Spacelift docs][sl-docs] · [Atlantis][atlantis] | IaC platforms |
| [Blacksmith docs][bs-docs] · [pricing][bs-price] · [home][bs-home] · [Depot][dp-docs] · [Depot pricing][dp-price] · [Namespace][ns-docs] · [pricing][ns-price] · [RunsOn pricing][ro-price] · [README][ro-repo] · [Ubicloud][ub-docs] · [price-performance][ub-price] · [repo][ub-repo] | Runner services, vendor claims |
| Leads: [openalternative.co][lead-oa] · [Spacelift][lead-sp] · alternativeto.net (`https://alternativeto.net/software/github-actions/`, plain text: 403 to the link checker, read with a browser fetch 2026-11-27) | Candidate discovery only, not evidence |
| Capability map: [GitLab docs][cm-gl-ci] · [GitHub Packages][cm-gh-pkg] · [Forgejo docs][cm-fj-protect] · [Gitea docs][cm-gt-protected] · [Gitea Enterprise][cm-gt-ent] · [Bitbucket pricing][cm-bb-price] · [Bitbucket merge queues][cm-bb-mq] · [Bitbucket Packages][cm-bb-pkgs] · [Atlassian Guard SAML][cm-bb-sso] · [Azure DevOps policies][cm-ado-policies] · [Azure DevOps pricing][cm-ado-price] · [Boards Copilot][cm-ado-copilot] | Per-capability cells (full URLs in the link definitions below) |
| `gh api` repository, licence and release endpoints, 2026-11-27 | Stars, licences, latest releases |

[gl-lic]: https://docs.gitlab.com/development/licensing/
[gl-pkg]: https://docs.gitlab.com/administration/package_information/licensing/
[gl-mcp]: https://docs.gitlab.com/user/model_context_protocol/mcp_server/
[gl-import]: https://docs.gitlab.com/user/project/import/github/
[gl-ci]: https://docs.gitlab.com/ci/yaml/
[bb-ci]: https://support.atlassian.com/bitbucket-cloud/docs/get-started-with-bitbucket-pipelines/
[bb-import]: https://support.atlassian.com/bitbucket-cloud/docs/import-a-repository-from-github-or-gitlab/
[bb-tools]: https://support.atlassian.com/atlassian-rovo-mcp-server/docs/supported-tools/
[bb-dc]: https://www.atlassian.com/migration/assess/journey-to-cloud
[ado-pipe]: https://learn.microsoft.com/en-us/azure/devops/pipelines/get-started/what-is-azure-pipelines?view=azure-devops
[ado-mcp]: https://learn.microsoft.com/en-us/azure/devops/mcp-server/mcp-server-overview?view=azure-devops
[ado-import]: https://learn.microsoft.com/en-us/azure/devops/repos/git/import-git-repository?view=azure-devops
[ado-mcp-repo]: https://github.com/microsoft/azure-devops-mcp
[gitea-repo]: https://github.com/go-gitea/gitea
[gitea-cmp]: https://docs.gitea.com/usage/actions/comparison
[gitea-mig]: https://docs.gitea.com/usage/migration
[gitea-mcp]: https://gitea.com/gitea/gitea-mcp
[fj-faq]: https://forgejo.org/faq/
[fj-rel]: https://codeberg.org/forgejo/forgejo/releases
[fj-gha]: https://forgejo.org/docs/latest/user/actions/github-actions/
[fj-first]: https://forgejo.org/docs/latest/user/getting-started/first-repository/
[cb-ci]: https://docs.codeberg.org/ci/
[cb-llm]: https://blog.codeberg.org/protecting-our-floss-commons-from-llms.html
[sh-home]: https://sourcehut.org/
[sh-builds]: https://man.sr.ht/builds.sr.ht/
[sh-git]: https://man.sr.ht/git.sr.ht/
[sh-llm]: https://sourcehut.org/blog/2026-08-27-tos-changes-and-llms/
[ger-home]: https://www.gerritcodereview.com/
[ger-lic]: https://gerrit-review.googlesource.com/Documentation/licenses.html
[harness-repo]: https://github.com/harness/harness
[circle-cfg]: https://circleci.com/docs/reference/configuration-reference/
[circle-mcp]: https://circleci.com/docs/guides/toolkit/circleci-mcp-overview/
[bk-steps]: https://buildkite.com/docs/pipelines/configure/defining-steps
[bk-mcp]: https://buildkite.com/docs/apis/mcp-server
[jk-file]: https://www.jenkins.io/doc/book/pipeline/jenkinsfile/
[jk-mcp]: https://plugins.jenkins.io/mcp-server/
[wp-syntax]: https://woodpecker-ci.org/docs/usage/workflow-syntax
[dagger]: https://docs.dagger.io/
[sl-docs]: https://docs.spacelift.io/
[atlantis]: https://www.runatlantis.io/
[bs-home]: https://www.blacksmith.sh/
[bs-docs]: https://docs.blacksmith.sh/blacksmith-runners/overview
[bs-price]: https://www.blacksmith.sh/pricing
[dp-docs]: https://depot.dev/docs/github-actions/overview
[dp-price]: https://depot.dev/pricing
[ns-docs]: https://namespace.so/docs/solutions/github-actions
[ns-price]: https://namespace.so/pricing
[ro-price]: https://runs-on.com/pricing/
[ro-repo]: https://github.com/runs-on/runs-on
[ub-docs]: https://www.ubicloud.com/docs/github-actions-integration/quickstart
[ub-price]: https://www.ubicloud.com/docs/github-actions-integration/price-performance
[ub-repo]: https://github.com/ubicloud/ubicloud
[agola]: https://github.com/agola-io/agola
[wb-docs]: https://docs.warpbuild.com/
[tc-docs]: https://www.jetbrains.com/help/teamcity/teamcity-documentation.html
[gogs]: https://github.com/gogs/gogs
[lead-oa]: https://openalternative.co/blog/top-12-alternatives-to-github
[lead-sp]: https://spacelift.io/blog/github-actions-alternatives
[gh-actions]: github-platform-capabilities-analysis.md#actions-and-workflows
[gh-rules]: github-platform-capabilities-analysis.md#rules-and-enforcement
[gh-dev]: github-platform-capabilities-analysis.md#dev-environments
[gh-org]: github-platform-capabilities-analysis.md#org-business-and-enterprise-features
[gh-agent]: github-platform-capabilities-analysis.md#agent-surfaces
[gh-copilot-agent]: ../non-cc/agents/github-copilot-cloud-agent-analysis.md
[aca-4]: agent-code-analysis-landscape.md#4-ci-forge-integration-verified-first-party
[cm-gl-ci]: https://docs.gitlab.com/ci/
[cm-gl-hosted]: https://docs.gitlab.com/ci/runners/hosted_runners/
[cm-gl-runner]: https://docs.gitlab.com/runner/
[cm-gl-trains]: https://docs.gitlab.com/ci/pipelines/merge_trains/
[cm-gl-protected]: https://docs.gitlab.com/user/project/repository/branches/protected/
[cm-gl-merge]: https://docs.gitlab.com/user/project/merge_requests/auto_merge/
[cm-gl-checks]: https://docs.gitlab.com/user/project/merge_requests/status_checks/
[cm-gl-owners]: https://docs.gitlab.com/user/project/codeowners/
[cm-gl-ws]: https://docs.gitlab.com/user/workspace/
[cm-gl-secret]: https://docs.gitlab.com/user/application_security/secret_detection/
[cm-gl-sast]: https://docs.gitlab.com/user/application_security/sast/
[cm-gl-dep]: https://docs.gitlab.com/user/application_security/dependency_scanning/
[cm-gl-pkgreg]: https://docs.gitlab.com/user/packages/package_registry/
[cm-gl-saml]: https://docs.gitlab.com/user/group/saml_sso/
[cm-gl-scim]: https://docs.gitlab.com/user/group/saml_sso/scim_setup/
[cm-gl-audit]: https://docs.gitlab.com/user/compliance/audit_events/
[cm-gl-duo]: https://docs.gitlab.com/user/duo_agent_platform/
[cm-fj-runner]: https://forgejo.org/docs/latest/admin/actions/
[cm-fj-protect]: https://forgejo.org/docs/latest/user/repository/protection/
[cm-fj-pr]: https://forgejo.org/docs/latest/user/collaboration/pull-requests-and-git-flow/
[cm-fj-pkgs]: https://forgejo.org/docs/latest/user/packages/
[cm-fj-auth]: https://forgejo.org/docs/latest/admin/setup/authentication/
[cm-gt-actions]: https://docs.gitea.com/usage/actions/overview/
[cm-gt-runner]: https://docs.gitea.com/usage/actions/runner/
[cm-gt-protected]: https://docs.gitea.com/usage/access-control/protected-branches/
[cm-gt-owners]: https://docs.gitea.com/usage/repository/code-owners/
[cm-gt-pkgs]: https://docs.gitea.com/usage/packages/overview/
[cm-gt-auth]: https://docs.gitea.com/administration/authentication/
[cm-gt-audit]: https://docs.gitea.com/administration/audit-logging/
[cm-gt-ent]: https://about.gitea.com/products/gitea-enterprise/
[cm-gt-cmp]: https://docs.gitea.com/installation/comparison
[cm-bb-price]: https://www.atlassian.com/software/bitbucket/pricing
[cm-bb-runners]: https://support.atlassian.com/bitbucket-cloud/docs/runners/
[cm-bb-mq]: https://support.atlassian.com/bitbucket-cloud/docs/manage-pull-requests-with-merge-queues/
[cm-bb-branch]: https://support.atlassian.com/bitbucket-cloud/docs/use-branch-permissions/
[cm-bb-checks]: https://support.atlassian.com/bitbucket-cloud/docs/suggest-or-require-checks-before-a-merge/
[cm-bb-owners]: https://support.atlassian.com/bitbucket-cloud/docs/set-up-and-use-code-owners/
[cm-bb-pkgs]: https://www.atlassian.com/software/bitbucket/features/packages
[cm-bb-sso]: https://support.atlassian.com/security-and-access-policies/docs/configure-saml-single-sign-on-with-an-identity-provider/
[cm-bb-scim]: https://support.atlassian.com/provisioning-users/docs/understand-user-provisioning/
[cm-bb-audit]: https://support.atlassian.com/security-and-access-policies/docs/monitor-and-audit-activity-in-your-organization/
[cm-bb-agentic]: https://support.atlassian.com/bitbucket-cloud/docs/agentic-pipelines/
[cm-ado-hosted]: https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/hosted?view=azure-devops
[cm-ado-self]: https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/agents?view=azure-devops
[cm-ado-price]: https://azure.microsoft.com/en-us/pricing/details/devops/azure-devops-services/
[cm-ado-policies]: https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies?view=azure-devops
[cm-ado-owners]: https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies-overview?view=azure-devops
[cm-ado-ghas]: https://learn.microsoft.com/en-us/azure/devops/repos/security/configure-github-advanced-security-features?view=azure-devops
[cm-ado-art]: https://learn.microsoft.com/en-us/azure/devops/artifacts/start-using-azure-artifacts?view=azure-devops
[cm-ado-entra]: https://learn.microsoft.com/en-us/azure/devops/organizations/accounts/connect-organization-to-azure-ad?view=azure-devops
[cm-ado-audit]: https://learn.microsoft.com/en-us/azure/devops/organizations/audit/azure-devops-auditing?view=azure-devops
[cm-ado-copilot]: https://learn.microsoft.com/en-us/azure/devops/boards/github/work-item-integration-github-copilot?view=azure-devops
[cm-gh-pkg]: https://docs.github.com/en/packages/learn-github-packages/introduction-to-github-packages
