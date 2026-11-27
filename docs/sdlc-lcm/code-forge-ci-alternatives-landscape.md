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
the jobs when the workflows are GitHub Actions (a **runner service**). This doc keeps the three apart. It does not
describe GitHub's own features. GitLab Community Edition as an application lifecycle management (ALM) option is
covered in [oss-alm-landscape.md](oss-alm-landscape.md), so GitLab appears here only for what that doc lacks: agent
surface and migration path.

**Leads, not evidence.** Four pages pointed us at candidates: [Blacksmith's home page][bs-home],
[openalternative.co's list][lead-oa], [Spacelift's Actions-alternatives article][lead-sp] and
[alternativeto.net's Actions page][lead-at]. They are aggregators or vendors with a stake. Every fact below comes from
the product's own docs, repository or licence file, except where a row says otherwise.

## 1. Code forges

"Agent surface" means what a coding agent can drive: the documented API and any official Model Context Protocol (MCP)
server. "Not read" means we did not find or fetch a page that settles it, not that the feature is absent.

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
| Gitea Actions and Forgejo Actions | With the forge | As the forge | GitHub Actions-style YAML | Largely, with documented gaps: Gitea's comparison page lists unsupported syntax, including complex `runs-on` values ([compare][gitea-cmp]); Forgejo says compatibility is not a goal ([docs][fj-gha]) | Forge API |
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

Our synthesis, not a sourced finding. Teams that only want faster or cheaper builds can change the `runs-on` label and
keep everything else, which is the lowest-risk move and the only one in this doc that leaves workflows untouched.
Teams that want a different CI system keep GitHub as the forge and add a pipeline definition elsewhere. Teams that
move the forge carry the biggest cost: the CI definition changes too, since only Gitea Actions and Forgejo Actions keep
the workflow format close, and neither promises full compatibility. For agent-driven work, check three things before
choosing: an official MCP server for the forge and for the CI system, how the platform's terms treat agent-written
code ([§ 1](#1-code-forges), Codeberg and SourceHut note), and whether the migration tool carries over issues and
reviews or only Git history.

## Not included

Pruned under the [well-known, performance-optimised filter](../../CONTRIBUTING.md#pruning-entries-well-known-performance-optimised-filter)
or deferred (named, not yet read first-party).

| Name | Reason | Date | Link |
|---|---|---|---|
| Agola | 1,632 stars; last push 2025-09-24, older than 12 months (`gh api`) | 2026-11-27 | [repo][agola] |
| WarpBuild | Adoption evidence: product page and docs read, but only vendor claims; no open code or named independent users read | 2026-11-27 | [docs][wb-docs] |
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
| Leads: [openalternative.co][lead-oa] · [Spacelift][lead-sp] · [alternativeto.net][lead-at] | Candidate discovery only, not evidence |
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
[lead-at]: https://alternativeto.net/software/github-actions/
