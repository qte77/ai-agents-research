---
title: GitHub Copilot Cloud Agent Analysis
purpose: Analysis of Copilot on github.com — the cloud agent, its automations, MCP server configuration, repository custom instructions, automatic code review and the responsible-use mitigations — as the cloud counterpart to the Copilot CLI.
created: 2026-10-24
updated: 2026-10-24
validated_links: 2026-10-24
status: assess
---

**Details:** Proprietary, GitHub-hosted. Automations launched 2026-06-02 ([changelog][cl-automations]);
Copilot code review is generally available, Copilot approvals are public preview
([code review concepts][cr-concepts]). Every claim below was fetched first-party on 2026-10-24 and
re-checked by an independent falsification pass (19 of 19 confirmed, none wrong). The terminal
agent is covered separately in [github-copilot-cli-analysis.md](github-copilot-cli-analysis.md).

## What It Is

GitHub's docs list four Copilot surfaces on github.com — "Chat", "Agentic experiences", "Code
review" and "Automations" ([Copilot on GitHub][surfaces]). This doc covers the agentic ones: the
**cloud agent**, which works in a GitHub-hosted environment and opens pull requests; **automations**,
which start the cloud agent without a person; and **code review**, which shares the cloud agent's
MCP configuration.

## Automations

Automations make the cloud agent "run automatically, either on a schedule or in response to an
event in a repository" ([create automations][automations]):

- **Triggers:** "On a schedule", "When an issue is created", "When a pull request is opened", "When a
  pull request is synchronized". Schedules use "a recurring interval, either hourly, daily, or
  weekly". A later changelog entry, "Trigger Copilot automations with comments"
  ([2026-08-03][cl-comments]), adds comment triggers, which the docs page's trigger list doesn't
  yet show.
- **Where:** "Automations are not available in public repositories." The launch entry says they are
  "supported in private and internal repositories, with support for public repositories coming
  soon" ([changelog][cl-automations]).
- **Plans:** "GitHub Copilot Pro, GitHub Copilot Pro+, GitHub Copilot Max, … GitHub Copilot Business,
  and GitHub Copilot Enterprise"; Business and Enterprise need the cloud-agent policy enabled by an
  admin ([create automations][automations]). The page carries no preview label.
- **Visibility:** "The Copilot cloud agent sessions started by an automation are visible to others
  with access to the repository. Don't include secrets or other sensitive information in your
  prompt"; the page points to repository secrets instead.

## MCP servers

Per [configure MCP servers][mcp-config]:

- "The GitHub MCP server and Playwright MCP server are enabled by default, and you can add your own
  servers alongside them."
- Configuration is JSON with an `mcpServers` object, set in the repository's Copilot settings.
- "Only Agents secrets and variables with names prefixed with `COPILOT_MCP_` will be available to
  your MCP configuration."
- "Remote MCP servers that use OAuth for authentication and authorization are not currently
  supported. Only MCP tools are supported. Resources and prompts from the MCP server are not
  currently supported."
- "The repository MCP configuration is shared by Copilot cloud agent and Copilot code review."
  Code review only uses read-only tools: it "excludes tools when this [`annotations.readOnlyHint`]
  annotation is missing or set to `false`."

**[github/github-mcp-server][gh-mcp]** — MIT, 33,895★, latest release `v2.0.3` (2026-10-21)
(`gh api`, 2026-10-24). Runs remotely at `https://api.githubcopilot.com/mcp/` or locally (Docker image
or stdio binary). A `--read-only` flag skips write tools ("Read-only mode takes priority"), and
toolsets narrow what is exposed. "GitHub Enterprise Server does not support remote server hosting",
so GHES users run it locally. Playwright MCP's own coverage is in
[CC-web-scraping-plugins-analysis.md § Playwright MCP Server](../../cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md#playwright-mcp-server).

## Repository custom instructions

Per [add repository instructions][repo-instructions], Copilot reads:

- `.github/copilot-instructions.md` (repository-wide);
- `.github/instructions/NAME.instructions.md` files scoped by `applyTo` globs (path-specific);
- "one or more `AGENTS.md` files, stored anywhere within the repository" (nearest wins when nested),
  or "a single `CLAUDE.md` or `GEMINI.md` file stored in the root of the repository".

Repository-wide instructions apply to "all requests made in the context of a repository" and are
enabled for code review by default; "Currently, on GitHub.com, path-specific custom instructions
are only supported for Copilot cloud agent and Copilot code review." When several sets apply,
"Personal instructions take the highest priority. Repository instructions come next, and then
organization instructions are prioritized last", and "all sets of relevant instructions are
provided to Copilot".

For agent-config portability this matters: a repo that already keeps an `AGENTS.md` (or a root
`CLAUDE.md`) for other agents no longer needs a separate Copilot file — see
[multi-agent-onboarding-outlook.md](../../sdlc-lcm/multi-agent-onboarding-outlook.md).

## Automatic code review

- **Setup:** a branch-ruleset rule, "Automatically request Copilot code review", with "Review new
  pushes" and "Review draft pull requests" options ([configure code review][cr-config]).
- **Billing:** for automatic reviews, "AI credits consumption is attributed to the pull request
  author", and reviews also consume GitHub Actions minutes; a manually requested review is
  attributed to the person who requested it ([code review concepts][cr-concepts]).
- **External licences:** "By default, people can use an external license to request a review from
  Copilot" — a licence not provided by the organization that owns the repository. The setting "Only
  allow Copilot code review to be triggered by authorized users" stops that; "Automatic reviews
  configured by repository or organization rulesets still run" ([code review concepts][cr-concepts]).

Other review products are compared in
[code-review-products-landscape.md](../infrastructure/code-review-products-landscape.md).

## Responsible use: stated limits and mitigations

Per [responsible use of agents][responsible]:

- "Copilot cannot push directly to your default branch (for example, `main`)" — work lands in a
  pull request.
- "By default, the cloud agent has a firewall enabled to prevent exfiltration of code or other
  sensitive data."
- For code review, suggested code "may appear to be valid but may not actually be semantically or
  syntactically correct", so a human still reviews suggestions before accepting them.

## Watch-outs

- **Agent-aimed text in the sources.** GitHub's docs pages, a sample cloud-agent onboarding prompt
  and the MCP server's tool descriptions all contain text addressed to AI agents. It was read as
  data; nothing in it was acted on.
- **Automations run without a person.** A scheduled or event-triggered agent acting on issue or PR
  text is exposed to whatever that text says; combine automations with the read-only and secret
  scoping above.
- **Docs vs changelog drift.** The comment trigger shows the docs page can lag the changelog.

## Sources

| Source | Content |
|---|---|
| [Copilot on GitHub][surfaces] | The four surfaces |
| [Create automations][automations] | Triggers, schedules, plans, public-repo exclusion |
| [Changelog 2026-06-02 — automations][cl-automations] | Launch; private/internal repos only |
| [Changelog 2026-08-03 — comment triggers][cl-comments] | Comment-based triggers |
| [Configure MCP servers][mcp-config] | Default servers, `COPILOT_MCP_` secrets, no OAuth, tools only, shared with code review |
| [github/github-mcp-server][gh-mcp] | Licence, release, remote endpoint, read-only mode, GHES limit |
| [Add repository instructions][repo-instructions] | Instruction files, AGENTS.md/CLAUDE.md/GEMINI.md, precedence |
| [Configure code review][cr-config] | Ruleset rule and options |
| [Code review concepts][cr-concepts] | GA status, billing attribution, external licences |
| [Responsible use of agents][responsible] | Default-branch protection, firewall, limitations |
| `gh api repos/github/github-mcp-server`, 2026-10-24 | Stars, licence, latest release |

[surfaces]: https://docs.github.com/en/enterprise-cloud@latest/copilot/concepts/copilot-surfaces/copilot-on-github
[automations]: https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/create-automations
[cl-automations]: https://github.blog/changelog/2026-06-02-schedule-and-automate-tasks-with-copilot-cloud-agent/
[cl-comments]: https://github.blog/changelog/2026-08-03-trigger-copilot-automations-with-comments/
[mcp-config]: https://docs.github.com/en/enterprise-cloud@latest/copilot/how-tos/copilot-on-github/customize-copilot/configure-mcp-servers
[gh-mcp]: https://github.com/github/github-mcp-server
[repo-instructions]: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions
[cr-config]: https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/configure-code-review
[cr-concepts]: https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/code-review
[responsible]: https://docs.github.com/en/copilot/responsible-use/agents
