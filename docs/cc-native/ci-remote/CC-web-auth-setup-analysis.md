---
title: CC Web Setup, Authentication & API Key Usage
source: https://code.claude.com/docs/en/claude-code-on-the-web
purpose: How to set up Claude Code on the web, connect GitHub, authenticate with API keys for non-interactive usage, connect remote sessions, and the Claude Console platform-admin surface (workspaces, rate limits, cost reporting, data retention) a headless org API key touches.
created: 2026-03-24
updated: 2026-11-18
validated_links: 2026-11-15
status: assess
---

**Details:** Research preview (web), GA (CLI auth, Console API keys, workspaces)

## Scope

This document covers **authentication and setup** for Claude Code across web, terminal, and headless modes. For cloud VM execution mechanics, environment configuration, network policy, and session handoff details, see [CC-cloud-sessions-analysis.md](CC-cloud-sessions-analysis.md). For remote monitoring of local sessions, see [CC-remote-control-analysis.md](CC-remote-control-analysis.md). For print mode pitfalls, see [CC-print-mode-gotchas.md](../sessions/CC-print-mode-gotchas.md). For the claude.ai subscription's shared weekly/five-hour usage limit (distinct from the Console org-level limits in §3 below), see [CC-session-cost-analysis.md § Shared plan usage][session-cost].

**Version gate**: the `--cloud`/`--remote` flag naming, `/web-setup` GitHub connection flow, and authentication precedence sections below are anchored to CC v2.1.190–2.1.217+ (fetched 2026-07-23); the doc's original 2026-03-24 baseline predates these changes. The Console platform-admin content added to §3 (workspaces, rate limits, Usage and Cost API, data retention, AUP) is anchored to the `platform.claude.com/docs/en/` pages as fetched 2026-10-15 and is largely CC-version-independent; the one CC-version-gated item in that addition, `ANTHROPIC_CUSTOM_HEADERS`, requires CC v2.1.227+.

## 1. Claude Code on the Web — GitHub Setup

### Prerequisites

- Claude Pro, Max, Team, or Enterprise account ([source][cc-web])
- GitHub-hosted repository (GitLab/other providers not supported) ([source][cc-web])

### Setup Steps

1. Visit [claude.ai/code](https://claude.ai/code)
2. **Connect GitHub account** — OAuth flow, grants CC read/write access to selected repos
3. **Install Claude GitHub App** — per-repo or org-wide; handles cloning, branch pushing, PR creation
4. **Select default environment** — configure network access, env vars, setup script (see [cloud sessions](CC-cloud-sessions-analysis.md#environment-configuration))
5. Submit task

### Connecting GitHub

#### OAuth via claude.ai

The web UI at `claude.ai/code` prompts you to connect your GitHub account via OAuth. This installs the **Claude GitHub App** which provides:

- Repository cloning into isolated VMs
- Branch pushing (restricted to working branch)
- PR creation

**GitHub App permissions** (managed by Anthropic, not user-configurable):

- Repository contents: read/write (clone, push branches)
- Pull requests: read/write (create PRs)
- Metadata: read

The GitHub App is installed per-repository or org-wide. You choose which repos to grant access to during installation.

#### GitHub Connection — Two Methods

GitHub can be connected two ways ([source][cc-web]):

1. **Claude GitHub App via OAuth** — browser-based onboarding at `claude.ai/code`, described above.
2. **`/web-setup`** — run from the terminal. Its first step is authenticating with the GitHub CLI, `gh auth login`, so it can sync your local `gh` token to your Claude account ([source][cc-web-quickstart]).

The terminal-initiated cloud-session flow:

1. Run `claude` → browser OAuth → logged into Claude.ai
2. Connect GitHub via `/web-setup` (`gh auth login` first) or in `claude.ai/code` settings (one-time)
3. From terminal: `claude --cloud "task description"` creates a cloud session — the older `--remote` spelling still works as a deprecated alias for `--cloud` ([source][cc-web])

Once connected, the Claude GitHub App handles all git operations in the cloud VM through a dedicated proxy with scoped credentials ([source][cc-web]).

#### GitHub Proxy — How Git Auth Works in Cloud

Inside the cloud VM sandbox, the git client does **not** have your GitHub credentials directly. Instead:

- A **scoped credential** is injected into the sandbox
- All git operations go through a **dedicated GitHub proxy** service
- The proxy verifies the scoped credential and translates it to your actual GitHub auth token
- Push operations are **restricted to the current working branch** ([source][cc-web])

Sensitive credentials (GitHub tokens, signing keys) are never inside the sandbox.

## 2. Authentication Methods — Full Picture

### Authentication Precedence (Terminal CLI)

When multiple credentials are present, CC chooses in this order ([source][cc-auth]):

| Priority | Method | Use Case |
| -------- | ------ | -------- |
| 1 | Cloud provider env vars (`CLAUDE_CODE_USE_BEDROCK`, `_VERTEX`, `_FOUNDRY`) | Organizations using AWS/GCP/Azure |
| 2 | `ANTHROPIC_AUTH_TOKEN` env var | LLM gateway/proxy with bearer tokens |
| 3 | `ANTHROPIC_API_KEY` env var | Direct API access (headless/CI) |
| 4 | `apiKeyHelper` script | Dynamic/rotating credentials from vault |
| 5 | `CLAUDE_CODE_OAUTH_TOKEN` env var (long-lived token from `claude setup-token`) | CI pipelines where browser login isn't available |
| 6 | Anthropic profile and federation credentials (`ANTHROPIC_PROFILE` / Workload Identity Federation) | `ant auth login` profiles and WIF token exchange — ranks here only when selected via `ANTHROPIC_PROFILE` or the WIF federation variables; an unnamed/active profile otherwise ranks below `/login` |
| 7 | Subscription OAuth (`/login`) | Default for Pro/Max/Team/Enterprise |

Re-fetched 2026-10-24: the live precedence list now has these 7 entries, up from 6 at the doc's last check — the new "Anthropic profile and federation credentials" entry (row 6) is the only addition ([source][cc-auth]).

**Key insight**: `ANTHROPIC_API_KEY` takes precedence over subscription OAuth once approved. If the key belongs to a disabled org, CC auth fails even if you have a valid subscription. Fix: `unset ANTHROPIC_API_KEY` ([source][cc-auth]).

**The `-p` nuance**: in interactive mode you're prompted once to approve or decline a detected `ANTHROPIC_API_KEY`, and the choice is remembered. In non-interactive mode there's no such prompt — per the docs, verbatim: "In non-interactive mode (`-p`), the key is always used when present." ([source][cc-auth]) Consequence: a key merely present in a headless run's environment silently moves that run from subscription billing to Console API billing, with no approval step to catch it — `unset ANTHROPIC_API_KEY` before a `-p` run that should stay on the subscription.

**Web sessions always use subscription credentials** — `ANTHROPIC_API_KEY` and `ANTHROPIC_AUTH_TOKEN` in the sandbox environment do not override them ([source][cc-auth]).

### Interactive Login

```bash
# Default OAuth login (opens browser)
claude auth login

# Force SSO authentication
claude auth login --sso

# Login with Console credentials (API billing)
claude auth login --console

# Pre-fill email
claude auth login --email user@example.com

# Check auth status
claude auth status        # JSON output
claude auth status --text # Human-readable
```

### Confirming Which Credential Is Active, and Scoping a Key to Headless Only

**Observations** (CC 2.1.310, Codespaces, 2026-10-24): with `ANTHROPIC_API_KEY` set, `claude -p` prints a line stating that claude.ai connectors are disabled because `ANTHROPIC_API_KEY` or another auth source is set and takes precedence over the claude.ai login (see [claude.ai Connectors Go Dark Under API-Key Auth](#claudeai-connectors-go-dark-under-api-key-auth) below for the general rule). The `--output-format json` result reports a `total_cost_usd` field, with every `modelUsage.*.costBasis` entry reading `"list"`, on both a subscription session and an API-key session — this is a client-side list-price estimate, not a billing record read back from the Console. In one run, the API key was billed but the Console's own usage page (`platform.claude.com/usage`) showed no token usage after 30+ minutes; this is a single observation with an unknown cause, noted here as such rather than as a general behavior.

**Confirming org/workspace at the HTTP layer**: the Claude API's response headers name the organization and workspace a request resolved to — `request-id`, `anthropic-organization-id`, and `anthropic-workspace-id` (`wrkspc_`-prefixed) ([source][console-api-overview]). On the request side, the same page's authentication-headers table states the `anthropic-workspace-id` request header is "Required with an API key that isn't scoped to a workspace. Optional for other API keys." ([source][console-api-overview]) — consistent with the workspace-header requirement in [§ Select a Workspace](#select-a-workspace--the-anthropic-workspace-id-header) below. Claude Code's own `ANTHROPIC_WORKSPACE_ID` variable is documented only for [Workload Identity Federation][console-workspaces] token exchange ([source][cc-env-vars]) — it is not a general-purpose way to set the header for a plain Console key; don't claim more than the docs state.

**A headless-only key, without touching interactive sessions**: pass the helper through `--settings` on the `claude -p` invocation itself, rather than a settings file every session reads: `claude -p --settings '{"apiKeyHelper": "<cmd>"}'`. `--settings` applies for that one session and "can set any key your user settings file can set" ([source][cc-settings]); `apiKeyHelper` is one such key ([source][cc-auth]). This composition follows from the two pages but was not tested end-to-end — mark it as such. There is no documented `*_API_KEY_FILE` environment variable in the full [env vars reference][cc-env-vars] (checked 2026-10-24).

## 3. API Key for Non-Interactive / Headless Usage

### Two Paths Into Headless Usage, and Why They Collide

Running `claude -p` against an organization can draw on either of two unrelated quota systems, and switching between them is where the friction shows up:

- **Path A — claude.ai subscription login** (`/login`, or an Enterprise seat). Headless requests are metered against the shared weekly/five-hour usage pool described in [CC-session-cost-analysis.md § Shared plan usage][session-cost]. A long unattended run can exhaust this pool and return a plan-level "weekly limit" message with no `ANTHROPIC_API_KEY` involved at all.
- **Path B — a Console API key** (`claude auth login --console`, or exporting `ANTHROPIC_API_KEY` directly). Usage is pay-as-you-go, billed to the organization, and governed by the Console-side rate limits and spend caps in [§ Org-Level Rate Limits and Spend Caps](#org-level-rate-limits-and-spend-caps) below — not the weekly plan pool.

The two paths are not fully separate even when you only ever use `/login`: the first time any member of an organization signs in to Claude Code with a Console account, Anthropic automatically creates a dedicated **Claude Code workspace** in that organization and mints a per-user API key inside it. That key cannot be created manually from the Console, stops working the moment its owner is removed from the workspace or organization, and its usage is rate-limited separately from the organization's other API traffic — admins can cap its share of the organization's limits on the Rate limits page. Per the docs: "Archiving the Claude Code workspace disables Claude Code sign-in through Console billing for the whole organization." ([source][console-workspaces])

**Owner observation** (2026-10-14): running headless against the org's claude.ai login eventually produced a "You've hit your weekly limit" message — the Path A pool, not a Console rate limit or spend cap. Exporting a Console `ANTHROPIC_API_KEY` sidesteps that pool (Path B) but trades the weekly allotment for pay-as-you-go org billing, and — per §§ below — for a workspace-scoping requirement and the loss of claude.ai connectors.

### Creating an Anthropic API Key

1. Go to the API keys page (`platform.claude.com/settings/keys`) in the Claude Console and click **Create key**.
2. Name the key and choose an expiration (a preset of 3 hours/1 day/7 days/30 days, a custom duration, or **Never**; organizations with a maximum-expiration policy cap this choice) ([source][console-auth]).
3. Set **Linked account**: yourself for a **personal key**, or a service account for a **service account key** shared across an automated workload. Optionally scope the key to one workspace now — doing so lets every later request omit the workspace-scoping header described below.
4. Copy the key immediately (shown only once). Standard keys are formatted `sk-ant-api...`; an **Admin API key**, created separately for the Admin API, is formatted `sk-ant-admin01-...` ([source][console-usagecost]).

**Key types.** The Console distinguishes three key types; which one a key is determines what it can do and when it stops working ([source][console-auth]):

| Key type | Acts as | Stops working when |
| --- | --- | --- |
| Personal key | You, with your own roles/permissions | You lose org or (single-workspace key) workspace access; archived if removed from the org |
| Service account key | A [service account][console-workspaces] | The service account is archived, or (single-workspace key) removed from that workspace |
| Workspace key (legacy) | No one — belongs to the workspace it was created in | It expires/is disabled/deleted, or its workspace is archived |

Personal and service-account keys are identity-backed and preferred for new integrations; a shared personal key breaks when its owner leaves, so an automated/CI workload should use a service account key created by an organization admin on the [Service accounts page][console-workspaces] (`platform.claude.com/settings/service-accounts`), not a personal key or a legacy workspace key.

**Billing**: API key usage is billed per-token through the Console, separate from a Claude Pro/Max/Team/Enterprise subscription. You need credits or a payment method on the Console account.

### Select a Workspace — the `anthropic-workspace-id` Header

A key created for one specific workspace only ever runs there, and its requests can omit any workspace header. A key granted access to several workspaces (a multi-workspace personal or service-account key) must instead name the target workspace on every request, in the `anthropic-workspace-id` header — the CLI/SDK equivalent is an `extra_headers`/`default_headers` entry, or (Claude Code specifically, see below) `ANTHROPIC_CUSTOM_HEADERS` ([source][console-auth]).

**Owner observation** (2026-10-14), running `claude -p` headless with an exported Console key: a 400 error reading "This API key is not scoped to a workspace, so this request must include the anthropic-workspace-id header." The current Console docs' own wording for the same condition differs slightly but states the identical requirement — a 400 `invalid_request_error`: "anthropic-workspace-id is required when authenticating with an identity-linked API key; send the id of the workspace this request acts in." ([source][console-auth]) A header value that isn't a valid workspace ID, or that names a workspace the key's owner can't access, returns a different 400/404 ([source][console-auth]).

Two ways to resolve it:

1. **Scope the key to one workspace** at creation time (recommended) — the header requirement disappears entirely.
2. **Send the header on every request.** Claude Code's own CLI/environment surface has no `--workspace-id` flag and no plain `ANTHROPIC_WORKSPACE_ID` variable for this case — per the [CC env vars reference][cc-env-vars], `ANTHROPIC_WORKSPACE_ID` exists only for [Workload Identity Federation][console-workspaces] token exchange, and `ANTHROPIC_AWS_WORKSPACE_ID` is Claude Platform on AWS-only. For a plain Console key, set it instead via `ANTHROPIC_CUSTOM_HEADERS` (CC v2.1.227+): `ANTHROPIC_CUSTOM_HEADERS="anthropic-workspace-id: wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"`. A value that sets a credential, org/tenant, routing, or API-behavior header counts as a setting needing approval when it arrives through server-managed settings rather than your own shell environment ([source][cc-env-vars]) — `anthropic-workspace-id` plausibly falls under "org/tenant," though the docs' own examples (`Authorization`, `Host`) don't name it explicitly.

The [Admin API][console-usagecost] (§ below) inverts this requirement: it accepts a personal or service-account key only when that key is **not** scoped to a specific workspace.

### Using API Key with Claude Code

```bash
# Set env var
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# Non-interactive (print mode) — runs task and exits
claude -p "Explain the auth module in src/auth/"

# With output format
claude -p --output-format json "List all TODO comments"

# With budget cap
claude -p --max-budget-usd 5.00 "Refactor the logger"

# With turn limit
claude -p --max-turns 10 "Fix failing tests"

# Pipe input
cat error.log | claude -p "What's causing these errors?"

# Continue previous conversation
claude -c -p "Now fix the issue you identified"
```

For stream-json and `--bare` gotchas with API keys, see [CC-print-mode-gotchas.md](../sessions/CC-print-mode-gotchas.md).

### Interactive Mode with API Key

When `ANTHROPIC_API_KEY` is set and you run `claude` interactively, CC prompts once to approve or decline the key. Your choice is remembered. Change later via `/config` → "Use custom API key" toggle ([source][cc-auth]).

### claude.ai Connectors Go Dark Under API-Key Auth

Per the CC docs' "Use MCP servers from claude.ai" section: "Connectors from claude.ai are fetched only when your active authentication method is a claude.ai subscription login." They aren't loaded, even after a prior `/login`, whenever one of these is active instead ([source][cc-mcp]):

- `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, or `apiKeyHelper`
- A third-party provider (Amazon Bedrock, Google Cloud's Agent Platform)
- `ANTHROPIC_PROFILE`, a federation variable, or an active Anthropic profile
- `CLAUDE_CODE_OAUTH_TOKEN` (a `claude setup-token` token, which can only make model requests)

Fix: run `/status` to see which authentication method is active, unset the variable (or remove the `apiKeyHelper` setting / switch off the profile), then `/login` to pick the claude.ai account again. Two settings turn connectors off regardless of auth method: `disableClaudeAiConnectors: true` or `ENABLE_CLAUDEAI_MCP_SERVERS=false` ([source][cc-mcp]). This gating is specific to claude.ai-added connectors (the catalog at the [connectors and plugins marketplace][marketplace-connectors]); it has no bearing on project- or user-configured MCP servers.

### Console-Based Team Setup (API Billing)

For teams that want API-based billing instead of per-seat subscriptions ([source][cc-auth]):

1. Create/use a [Console](https://platform.claude.com) account
2. **Settings → Members → Invite** (or set up SSO)
3. Assign roles:
   - **Claude Code** role — can only create CC API keys
   - **Developer** role — can create any API key
4. Each user: accept invite → install CC → `claude auth login --console`

### apiKeyHelper for Dynamic Credentials

For rotating keys (e.g., from HashiCorp Vault):

```json
{
  "apiKeyHelper": "/path/to/script.sh"
}
```

- Called after 5 minutes or on HTTP 401
- Custom TTL: set `CLAUDE_CODE_API_KEY_HELPER_TTL_MS` env var
- Warning shown if script takes >10 seconds
- **Only applies to terminal CLI** — not Desktop or remote sessions ([source][cc-auth])

### Org-Level Rate Limits and Spend Caps

These apply only to Path B (Console API keys); they have no bearing on the claude.ai weekly/five-hour pool in [CC-session-cost-analysis.md][session-cost]. Figures below are fetched 2026-10-15 and will drift — treat the Console's own Rate limits page (`platform.claude.com/usage/limits`) as authoritative ([source][console-ratelimits]).

- **Spend limits** cap monthly org-wide API cost by usage tier: Start $500, Build $1,000, Scale $200,000 USD/month; Custom-tier organizations have no cap. A new or low-history org starts in an **Evaluation** tier below these figures and grows automatically. Past the cap, requests return a 429 `rate_limit_error` with `error.details.error_code: "enforced_spend_limit_reached"` and no `retry-after` header — retries, including SDK auto-retry, fail until the next calendar month or a tier increase.
- **Rate limits** (RPM/ITPM/OTPM) scale by tier per model; e.g., the Start tier allows 1,000 RPM and 2,000,000 ITPM for Sonnet 5. Limits use a token-bucket algorithm (continuously replenished, not reset on a fixed clock), and only *uncached* input tokens count toward ITPM — a high prompt-cache hit rate raises effective throughput well above the stated number.
- **Workspace-level limits** can be set below (never above) the org's limits to protect other workspaces from one noisy workload; the Default Workspace can't have its own limits. The auto-created **Claude Code workspace** (above) is checked separately from the rest of the org's Messages API traffic, and a request over *that* workspace's limit can return a 429 carrying a `retry-after` header — distinct from the spend-cap 429, which never carries one.
- Request a higher tier or cap via **Request tier increase** on the Rate limits page, or Anthropic support for urgent needs ([source][console-ratelimits]).

### Monitoring Org Spend — Usage and Cost Admin API

For visibility into Path B spend across an org's keys and workspaces, the **Usage and Cost Admin API** exposes `/v1/organizations/usage_report/messages` (token counts, filterable/groupable by `api_key_ids[]`, `workspace_ids[]`, `models[]`, `service_tiers[]`) and `/v1/organizations/cost_report` (USD cost, daily buckets only) ([source][console-usagecost]).

- **Auth**: an Admin API key (`sk-ant-admin01-...`), an OAuth token with the `org:admin` scope, or a personal/service-account key **not** scoped to a workspace. Workspace keys don't work here. Claude Enterprise organizations use a separate Analytics API key instead ([source][console-usagecost]).
- **Freshness/polling**: data typically appears within 5 minutes of a request completing; the API supports polling once per minute for sustained monitoring (more often is fine for short paginated bursts).
- **Claude Code specifically**: for per-user Claude Code cost and productivity breakdowns, the docs point to the separate **Claude Code Analytics API** rather than slicing the Usage API by many API keys ([source][console-usagecost]). See [CC-session-cost-analysis.md][session-cost] for the local-transcript alternative that needs no Admin key.

### API Data Retention for Headless/Agent Runs

Two different retention clocks are easy to conflate; they cover different copies of the data ([source][console-retention]):

- **Local transcript files** on disk (`~/.claude/projects/...jsonl`) are governed by the client-side `cleanupPeriodDays` setting (default 30 days) — see [CC-session-cost-analysis.md][session-cost].
- **Anthropic's server-side copy**, independent of that local setting: "Local session transcripts... are stored for 6 years by default, or for your organization's custom conversation retention period when a finite one is set," captured through the Compliance API where enabled. A HIPAA-readiness organization instead gets a 30-day local-session capture window.

Zero data retention (ZDR) for "Claude Code with API keys" applies when the organization is on the Commercial Terms of Service and has a ZDR arrangement enabled (contact Anthropic sales; enablement is per-organization and does not extend automatically to other orgs under the same account). If Claude Code's metrics logging is enabled, productivity/usage-statistics data is exempted from ZDR and may still be retained. Claude Code on **Claude Enterprise** has a separate ZDR offering, not this one. Claude Code is **not** covered by HIPAA readiness at all, and any usage through the **Console itself (including the Playground)** is outside ZDR regardless of the organization's arrangement.

### Acceptable Use Policy (Pointer)

Agentic use is explicitly in scope of Anthropic's Usage Policy, not a gap it leaves unaddressed. Under "Additional Use Case Guidelines," the policy states, verbatim: "Agentic use cases must comply with the Usage Policy." ([source][aup]) This document does not interpret what that requires for any specific automation — read the policy itself.

### Terms That Apply to Scripted Runs

Quoted from the vendor pages, accessed 2026-11-15. This section reports what the pages say; it does not
decide whether a given automation is allowed. For that, the [legal page][cc-legal] points to Anthropic
sales.

- **Which terms.** Claude Code use is subject to the "Commercial Terms of Service - for Team, Enterprise,
  and Claude API users" and the "Consumer Terms of Service - for Free, Pro, Max, and Ultra users"
  ([legal and compliance][cc-legal]). The Agent SDK is governed by the Commercial Terms, "including when
  you use it to power products and services that you make available to your own customers and end
  users," except components under a different license ([Agent SDK overview][cc-sdk]).
- **Plan limits assume individual use.** "Advertised usage limits for Pro, Max, and Ultra plans assume
  ordinary, individual usage of Claude Code and the Agent SDK" ([legal][cc-legal]).
- **Sign-in rules.** "OAuth authentication is intended exclusively for purchasers of Claude Free, Pro,
  Max, Ultra, Team, and Enterprise subscription plans and is designed to support ordinary use of Claude
  Code and other native Anthropic applications." Developers building products, "including those using
  the Agent SDK, should use API key authentication." Anthropic "does not permit third-party developers to
  offer Claude.ai login into their own applications, or to route requests through Free, Pro, Max, or
  Ultra plan credentials on behalf of their users," and developers "may not collect, store, or
  intermediate Claude.ai credentials or session tokens." The same page says this does not prevent "an
  end user from signing in to the unmodified Claude Code binary with their own Claude subscription"
  ([legal][cc-legal]).
- **Consumer Terms on automated access.** The version of the [Consumer Terms][consumer-terms] served to
  us (effective 2025-10-08) applies to consumers "resident in the European Economic Area or Switzerland";
  we did not see the version served elsewhere. It lists as prohibited: "Except when you are accessing our
  Services via an Anthropic API Key or where we otherwise explicitly permit it, to access the Services
  through automated or non-human means, whether through a bot, script, or otherwise."
- **What the pages leave open.** The [authentication docs][cc-auth] offer `claude setup-token` for "CI
  pipelines, scripts, or other environments where interactive browser login isn't available," and the
  [API-credits article][api-credits] says `claude -p` and the Agent SDK on a plan login "still draw from
  your plan's usage limits." No page we read says whether such a run counts as the "explicitly permit"
  exception or as "ordinary, individual usage." Read the pages yourself before relying on either.

### What a Scripted Run Bills

Checked 2026-11-15 against the linked pages.

| Run | Draws on | Source |
|---|---|---|
| `claude -p` or the Agent SDK, signed in with a plan | The plan's usage limits | [api-credits] |
| The same with a `setup-token` token | The plan: the token "authenticates with your Claude subscription" | [cc-auth] |
| `claude -p` or the Agent SDK with an API key from the Console org linked to a plan | That org's monthly API credits, then its purchased credits (sales-invoiced orgs are "billed as usual") | [api-credits] |
| `claude -p` or the Agent SDK with any other Console key | Per-token billing to that Console account (the page says this of API keys generally; it doesn't name `-p` or the SDK) | [cc-usage-metering] |
| The Claude Code GitHub Action, an IDE extension, the desktop app | Claude Code usage; "API credits don't cover them, even with `-p`" | [api-credits] |
| A cloud session | "your plan's usage limits ... there's no separate charge for the cloud VM" | [cc-web] |
| A scheduled task (formerly a routine) | Subscription usage, then metered overage if usage credits are on, plus hourly run caps; see [CC-web-scheduled-tasks-analysis.md § Usage Limits](CC-web-scheduled-tasks-analysis.md#usage-limits) | [cc-routines] |
| Claude Managed Agents | Tokens plus a session-runtime fee; see [CC-session-cost-analysis.md](../sessions/CC-session-cost-analysis.md#price-modifiers-exposed-by-the-usage-object) | [platform-pricing] |

**`setup-token`.** It generates "a one-year OAuth token." It "authenticates with your Claude subscription
and requires a Pro, Max, Ultra, Team, or Enterprise plan. It can only make model requests, so it can't
establish Remote Control sessions or fetch claude.ai connectors" ([authentication][cc-auth]).

**API credits for subscribers.** Per [the help article][api-credits] (last updated 2026-10-30): Max
($100/month), Ultra ($200), and Team ($20 per Standard seat, $100 per Premium seat, pooled and capped at
$500) include monthly credits for the Claude Platform; "Free, Pro, and Enterprise plans aren't eligible."

- **Setup:** you link one Console organization, which receives the credits.
- **What they pay for:** the Claude API, the Console Playground, Managed Agents, and the Agent SDK.
- **What they don't:** "Interactive Claude Code in the terminal, IDE, desktop, or web," extra usage, or
  Claude on Bedrock, Vertex AI or Foundry.
- **Expiry:** they expire at the end of each billing cycle ("Doesn't roll over").
- **Plan limits:** they are "Separate from your plan limits."
- **When they run out:** with no other credits, "API requests stop until your next monthly credits
  arrive. Usage is never charged to your Claude plan."

**`--bare` and plan logins.** "In bare mode, Claude Code never reads OAuth credentials or the system
keychain," so it needs `ANTHROPIC_API_KEY` or an `apiKeyHelper` ([headless docs][cc-headless]; pitfalls
in [CC-print-mode-gotchas.md](../sessions/CC-print-mode-gotchas.md)). The same page says `--bare` "will
become the default for `-p` in a future release," with no date. Our inference: once that ships, a `-p`
script that relies on a plan login will need an explicit opt-out or a key.

### Other Coding CLIs: Headless Sign-In and Billing

Checked 2026-11-15 against each vendor's docs; per-tool detail lives in the linked analysis docs. "No rule
in the docs read" means those pages are silent, not that no rule exists elsewhere.

| CLI | Headless run | Sign-in for scripts | What a scripted run bills | Vendor text on automated or third-party use |
|---|---|---|---|---|
| [Codex CLI](../../non-cc/coding-agents/codex-cli-analysis.md) | `codex exec` | "API keys are still the recommended default for automation"; ChatGPT login in CI is an advanced path; Enterprise access tokens are "intended for trusted scripts, schedulers, and private CI runners" ([auth][codex-auth]) | API key: "standard API pricing instead of included ChatGPT plan credits" ([auth][codex-auth]) | No rule in the Codex docs read; OpenAI's general terms not checked |
| [Gemini CLI](../../non-cc/coding-agents/gemini-cli-analysis.md) | `-p` or a non-TTY run ([headless][gemini-headless]) | Cached login, `GEMINI_API_KEY`, or Vertex AI ([auth][gemini-auth]) | Gemini Code Assist (individual) login: 1,000 requests/day; Google AI Pro 1,500; AI Ultra 2,000; unpaid API key: 250/day, Flash only ([quotas][gemini-quota]) | "Directly accessing the services powering Gemini CLI (for example, the Gemini Code Assist service) using third-party software, tools, or services (for example, using OpenClaw with Gemini CLI OAuth) is a violation of applicable terms and policies" ([terms][gemini-tos]); scripted use of the CLI itself not stated |
| [Copilot CLI](../../non-cc/agents/github-copilot-cli-analysis.md) | `copilot -p` | `COPILOT_GITHUB_TOKEN`, `GH_TOKEN`, or `GITHUB_TOKEN`; classic `ghp_` PATs "Not supported by Copilot CLI" ([auth][copilot-auth]); in Actions, a PAT "if you want usage billed to a specific user's Copilot seat" ([Actions][copilot-actions]) | GitHub AI Credits, "1 AI credit = $0.01 USD" ([billing][copilot-billing]) | No rule in the Copilot CLI docs read |
| [Cursor CLI](../../non-cc/coding-agents/cursor-analysis.md) | `agent -p` (`--force` to skip approvals) | `CURSOR_API_KEY` ([auth][cursor-auth]); team admins can turn on "Disable CLI headless mode" ([headless][cursor-headless]) | Paid plans have "a weekly pool of usage for Cursor models"; third-party models at "API list price, from prepaid credit" on Premium and above ([pricing][cursor-pricing]); the page doesn't name the CLI | No rule in the CLI docs read; Cursor's general terms not checked |
| [opencode](../../non-cc/coding-agents/opencode-analysis.md) Go plan | `opencode run`, "designed for scripts, CI jobs, and other workflows" ([CLI][opencode-cli]) | Provider keys or logins ([providers][opencode-providers]) | Go $10/month, Go Plus $40, Go Teams $20/member; "Service accounts are not covered by Go Teams" ([Go][opencode-go]) | "Go and Go Plus are for workspaces with a single member"; "Traffic is monitored for abuse" ([Go][opencode-go]) |
| Z.ai GLM Coding Plan | Through a supported tool | Plan API key | Plan quota | "may only be used within officially supported tools and products"; "Accounts with more than three violations may be banned" ([usage policy][zai-policy]) |
| MiniMax M Plan | Through a compatible tool | Plan API key | Plan quota | "designed for individual, interactive developer use ... Pay-as-you-go is recommended for production use" ([FAQ][minimax-faq]) |

Gemini CLI row, status 2026-11-18: its free, AI Pro and AI Ultra quotas apply to accounts Google stopped serving on 2026-06-18, so read them as the historical quota ([status and tier reconciliation](../../non-cc/coding-agents/gemini-cli-analysis.md)). The Antigravity CLI replacement signs in via browser OAuth, an API key or ADC and has `agy -p` for headless runs ([antigravity-analysis.md](../../non-cc/coding-agents/antigravity-analysis.md#antigravity-cli-agy-first-party-docs-checked-2026-11-18)); its quotas and terms were not compared here.

Not checked, so left out: OpenAI's and Cursor's general terms of use, and the Kimi Code membership rules.

### Adjacent Platform Building Blocks for Agents

One line each, where they bear on running agents against a Console key:

- **[Batch processing][console-batch]**: the Message Batches API runs large request volumes asynchronously at a 50% cost cut (most batches finish under an hour); it is **not** ZDR-eligible (29-day retention — it is inherently stateful).
- **[Files API][console-files]**: upload once, reference by `file_id` across requests (500 MB/file, 1 TB/org). Files are **workspace-scoped, not per-user**: any key with access to that workspace can read any file in it, so a multi-tenant agent must never accept a `file_id` from an untrusted caller and should give each tenant its own workspace. Not ZDR-eligible.
- **[Agent Skills API][console-skills]**: `/v1/skills` plus the code execution tool; custom Skills uploaded here are shared workspace-wide and run with no network access and no runtime package installation. They are a separate catalog from Claude Code's filesystem-based Skills (`~/.claude/skills/`, `.claude/skills/`) — Skills do not sync across claude.ai, the API, and Claude Code. Not ZDR-eligible.
- **[Playground][support-playground]**: the Console's stateless tool ("How do I use the playground?") for trying models/API features and exporting requests as code; it replaced the legacy Workbench. Console usage, playground included, is outside ZDR per the retention section above.
- **[Connectors and plugins marketplace][marketplace-connectors]**: the catalog of connectors/plugins added to a claude.ai account — the same surface that goes dark under API-key auth (above), not a Console/workspace-key mechanism.

## 4. Credential Storage

| Platform | Location |
| -------- | -------- |
| macOS | Encrypted macOS Keychain |
| Linux | `~/.claude/.credentials.json` (mode `0600`) |
| Windows | `%USERPROFILE%\.claude\.credentials.json` (user profile ACL) |
| Custom | `$CLAUDE_CONFIG_DIR/.credentials.json` |

## Decision Matrix — Which Auth Method to Use

| Scenario | Auth Method | Setup |
| -------- | ----------- | ----- |
| Web sessions (cloud VMs) | OAuth subscription + GitHub App | `claude.ai/code` → Connect GitHub |
| Terminal interactive (personal) | OAuth subscription | `claude auth login` |
| Terminal interactive (team, API billing) | Console credentials | `claude auth login --console` |
| CI/CD headless (print mode) | `ANTHROPIC_API_KEY` | Console → API Keys → Create |
| CI/CD with rotating keys | `apiKeyHelper` script | Settings JSON + vault script |
| AWS/GCP/Azure backend | Cloud provider env vars | Provider-specific setup |
| LLM gateway/proxy | `ANTHROPIC_AUTH_TOKEN` | Gateway provides bearer token |
| Remote Control (mobile monitoring) | OAuth subscription | `claude remote-control` (must be logged in) |
| Headless hit the claude.ai weekly limit | Personal/service-account key, scoped to one workspace | `platform.claude.com/settings/keys` → Create key → set Linked account + Workspace |
| Multi-workspace Console key in headless CC | Same key + a workspace-id header | `ANTHROPIC_CUSTOM_HEADERS="anthropic-workspace-id: wrkspc_..."` (CC v2.1.227+) |
| Scripted runs paid from a Max/Ultra/Team plan's monthly API credits | Console key from the org linked to the plan | claude.ai Settings > Billing → API credits → Link organization; see [§ What a Scripted Run Bills](#what-a-scripted-run-bills) |

## See Also

- [CC-cloud-sessions-analysis.md](CC-cloud-sessions-analysis.md) — cloud VM execution, environment config, network policy, session handoff
- [CC-remote-control-analysis.md](CC-remote-control-analysis.md) — local execution with remote monitoring
- [CC-remote-access-landscape.md](CC-remote-access-landscape.md) — third-party remote access tools comparison
- [CC-print-mode-gotchas.md](../sessions/CC-print-mode-gotchas.md) — `--bare`, `stream-json`, and `--verbose` pitfalls
- [CC-session-cost-analysis.md][session-cost] — the claude.ai weekly/five-hour subscription usage pool, and the local `cleanupPeriodDays` transcript-retention setting, both distinct from the Console org-level content in §3 above
- [CC-env-vars-reference.md][cc-env-vars] — full `ANTHROPIC_CUSTOM_HEADERS`, `ANTHROPIC_API_KEY`, and `ANTHROPIC_WORKSPACE_ID` env-var catalog

## References

- [CC on the Web docs][cc-web]
- [CC Authentication docs][cc-auth]
- [CC CLI Reference][cc-cli]
- [CC Setup docs][cc-setup]
- [CC Security docs][cc-sec]
- [CC Web Quickstart docs][cc-web-quickstart]
- [CC MCP docs][cc-mcp]
- [CC env vars reference][cc-env-vars]
- [Claude Console][console]
- [Console Authentication docs][console-auth]
- [Console Workspaces docs][console-workspaces]
- [Console Rate limits docs][console-ratelimits]
- [Console Usage and Cost API docs][console-usagecost]
- [Console API and Data Retention docs][console-retention]
- [Console API overview docs][console-api-overview]
- [CC Settings docs][cc-settings]
- [Console Batch Processing docs][console-batch]
- [Console Files API docs][console-files]
- [Console Agent Skills overview][console-skills]
- [Claude Help Center — Playground article][support-playground]
- [Claude Marketplace — Connectors and plugins][marketplace-connectors]
- [Anthropic Usage Policy][aup]
- [CC Legal and compliance][cc-legal], [Consumer Terms][consumer-terms], [Agent SDK overview][cc-sdk], [CC headless docs][cc-headless], [CC scheduled tasks docs][cc-routines], [Monthly API credits article][api-credits], [Models, usage, and limits in Claude Code][cc-usage-metering], [Claude Platform pricing][platform-pricing] (all accessed 2026-11-15)
- Other CLIs (accessed 2026-11-15): [Codex auth][codex-auth]; Gemini CLI [auth][gemini-auth], [headless][gemini-headless], [quotas][gemini-quota], [terms][gemini-tos]; Copilot CLI [auth][copilot-auth], [Actions][copilot-actions], [billing][copilot-billing]; Cursor [headless][cursor-headless], [auth][cursor-auth], [pricing][cursor-pricing]; opencode [CLI][opencode-cli], [providers][opencode-providers], [Go][opencode-go]; [Z.ai usage policy][zai-policy]; [MiniMax M Plan FAQ][minimax-faq]

[cc-web]: https://code.claude.com/docs/en/claude-code-on-the-web
[cc-auth]: https://code.claude.com/docs/en/authentication
[cc-cli]: https://code.claude.com/docs/en/cli-usage
[cc-setup]: https://code.claude.com/docs/en/setup
[cc-sec]: https://code.claude.com/docs/en/security
[cc-web-quickstart]: https://code.claude.com/docs/en/web-quickstart
[cc-mcp]: https://code.claude.com/docs/en/mcp
[cc-env-vars]: https://code.claude.com/docs/en/env-vars
[console]: https://platform.claude.com
[console-auth]: https://platform.claude.com/docs/en/manage-claude/authentication
[console-workspaces]: https://platform.claude.com/docs/en/manage-claude/workspaces
[console-ratelimits]: https://platform.claude.com/docs/en/api/rate-limits
[console-usagecost]: https://platform.claude.com/docs/en/manage-claude/usage-cost-api
[console-retention]: https://platform.claude.com/docs/en/manage-claude/api-and-data-retention
[console-api-overview]: https://platform.claude.com/docs/en/api/overview
[cc-settings]: https://code.claude.com/docs/en/settings
[console-batch]: https://platform.claude.com/docs/en/build-with-claude/batch-processing
[console-files]: https://platform.claude.com/docs/en/build-with-claude/files
[console-skills]: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
[support-playground]: https://support.claude.com/en/articles/8606378
[marketplace-connectors]: https://claude.com/marketplace/connectors-plugins
[aup]: https://www.anthropic.com/legal/aup
[session-cost]: ../sessions/CC-session-cost-analysis.md#shared-plan-usage-across-claude-products
[cc-legal]: https://code.claude.com/docs/en/legal-and-compliance
[consumer-terms]: https://www.anthropic.com/legal/consumer-terms
[cc-sdk]: https://code.claude.com/docs/en/agent-sdk/overview
[cc-headless]: https://code.claude.com/docs/en/headless
[cc-routines]: https://code.claude.com/docs/en/routines
[api-credits]: https://support.claude.com/en/articles/17154008-monthly-api-credits-for-max-ultra-and-team-plans
[cc-usage-metering]: https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code
[platform-pricing]: https://platform.claude.com/docs/en/about-claude/pricing
[codex-auth]: https://learn.chatgpt.com/docs/auth
[gemini-auth]: https://geminicli.com/docs/get-started/authentication/
[gemini-quota]: https://github.com/google-gemini/gemini-cli/blob/main/docs/resources/quota-and-pricing.md
[gemini-tos]: https://github.com/google-gemini/gemini-cli/blob/main/docs/resources/tos-privacy.md
[copilot-auth]: https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli
[copilot-actions]: https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/automate-with-actions
[copilot-billing]: https://docs.github.com/en/copilot/concepts/billing-and-usage/individuals/billing
[cursor-headless]: https://cursor.com/docs/cli/headless
[cursor-auth]: https://cursor.com/docs/cli/reference/authentication
[cursor-pricing]: https://cursor.com/docs/models-and-pricing
[opencode-providers]: https://opencode.ai/docs/providers/
[opencode-cli]: https://opencode.ai/docs/cli/
[gemini-headless]: https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/headless.md
[opencode-go]: https://opencode.ai/docs/console/go/
[zai-policy]: https://docs.z.ai/devpack/usage-policy
[minimax-faq]: https://platform.minimax.io/docs/m-plan/faq
