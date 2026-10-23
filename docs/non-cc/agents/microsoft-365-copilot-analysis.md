---
title: Microsoft 365 Copilot Analysis — SharePoint Skills, Copilot Studio, Work IQ, Agent 365
purpose: First-party fact-check and practitioner how-to for the Microsoft 365 Copilot ecosystem (Copilot in SharePoint, Copilot Studio, Work IQ, Agent 365) against first-party documentation, as of 2026-10-21.
created: 2026-10-21
updated: 2026-10-23
validated_links: 2026-10-23
status: assess
---

**Details:** Covers four separately versioned products — Copilot in SharePoint, Microsoft Copilot
Studio, Work IQ, and Microsoft Agent 365 — each at its own GA/preview stage; no single version
string applies to "Microsoft 365 Copilot" as a whole. See [Timeline](#timeline) below.

> **Disambiguation.** "Microsoft 365 Copilot" (this doc) is a third, unrelated "Copilot" brand —
> not GitHub Copilot CLI and not the GitHub Copilot coding agent, which are disambiguated from
> each other in [github-copilot-cli-analysis.md](github-copilot-cli-analysis.md) and in the
> Backlog status section of [../README.md](../README.md). Inside the Microsoft 365 Copilot family
> itself, this doc also treats **Copilot in SharePoint**, **Microsoft Copilot Studio**, **Work
> IQ**, and **Microsoft Agent 365** as four separate products on four separate timelines — not one
> undifferentiated "Copilot."

## TL;DR

- Most claims tested held up under a first-party challenge pass: of 85 Microsoft
  365 Copilot-ecosystem claims tested against vendor documentation, 47 were fully supported and
  24 were partly right (true core, wrong or unconfirmed detail). Only 3 were flatly wrong, and 11
  could not be settled either way — absent from the pages checked, or sourced only to non-vendor
  coverage. See [Results](#results).
- "Skills" names at least two different shipped things — Copilot-in-SharePoint Skills and custom
  skills in declarative agents — plus a third, unrelated document-generation feature often cited
  alongside them. Conflating any two of the three produces wrong claims. See
  [Two things called "skill"](#two-things-called-skill-and-one-feature-often-paired-with-them).
- Microsoft Agent 365 is the emerging single governance control plane for agents, but SharePoint's
  own Skills documentation never mentions it — no registry entry, no lifecycle action, governed
  only by ordinary file permissions. See
  [Governance](#governance-agent-365-covers-agents-not-sharepoint-skills).
- Anthropic's models are excluded from the EU Data Boundary outright, and disabled by default for
  customers within the EU Data Boundary and in the UK; Claude's own hosting on Microsoft Foundry
  has no EU-region deployment type either — a gap on both sides of this integration, stated here
  without favoring either vendor. See
  [Residency](#residency-anthropic-excluded-from-the-eu-data-boundary-claude-on-foundry-has-no-eu-data-zone-either).
- Claude's contractual relationship to this family is not one thing: three different postures
  apply depending on path (Microsoft Foundry, standard Microsoft 365 Copilot subprocessor models,
  or opt-in "Data Retention" models), and two Microsoft encryption options point in opposite
  directions for Copilot access. See
  [Claude's contractual posture](#claudes-contractual-posture-across-this-family) and
  [Encryption](#encryption-customer-key-vs-double-key-encryption).
- Publishing an agent out of Microsoft Foundry into Microsoft 365 Copilot's chat surface moves
  that agent's data under the receiving surface's own compliance terms, not Foundry's. See
  [Outside-in control](#outside-in-control-publishing-moves-the-compliance-boundary).

## Scope

As of **2026-10-21**. Covers: Copilot in SharePoint (Skills, structured document generation),
Microsoft Copilot Studio (model selection, knowledge sources, tools, MCP, agent flows), Work IQ,
Microsoft Agent 365 (registry, governance, licensing, APIs), the EU Data Boundary/Flex
Routing/Multi-Geo residency story, Microsoft Foundry facts that intersect with this family
(structured outputs, workflow retirement, publishing an agent into Copilot), and adjacent
SharePoint/Power Automate automation mechanics (Rules, Quick Steps, triggers, approvals,
connectors). Also covers Claude's contractual posture and an encryption trade-off (Customer Key
vs. Double Key Encryption) where they intersect with this family, eight recurring
operational/automation scenarios assessed against the same vendor documentation, and a
numbers-free pointer to each surface's current pricing page.

**Explicitly out of scope here:** the open Agent Skills specification itself and coding-agent
comparisons (Claude Code, Codex CLI) — see [CC-skills-adoption-analysis.md][cc-skills-doc].

## Method

Claims entering this pass came from unverified secondary input — a product description and a
practitioner how-to guide covering hands-on setup and governance steps. Neither is treated as a
source: each statement in them is an unverified **claim**, not evidence. Each claim was run through a
challenge pass: fetch the vendor's own current documentation directly, quote the load-bearing
sentence verbatim with the page's own displayed date, and assign two independent labels.

**Bucket** — how the check went:

- `checked` — a vendor page was fetched and the claim judged against it
- `checked-absent` — the exact wording was actively searched for on a vendor page and not found
  there; this is **absence, not refutation**
- `secondary-only` — no first-party vendor confirmation exists at all; any corroboration is
  non-vendor (community, consultancy, or administrative-mirror) coverage
- `not-checked` — no attempt was made, usually because the claim was low-novelty or an
  in-session-only observation
- `blocked` — a cited resource was inaccessible to the research session (unused in this subset)

**Verdict** — whether the claim held up: `refuted`, `partly`, `unverifiable`, or `supported`.

A small adversarial second read corrected three rows. The underlying vendor quotes were never in
dispute — only which direction of the claim they had been tested against — so all three are
presented below in their confirmed, positive framing: Copilot Studio's bring-your-own-model
feature explicitly excludes the GPT-5 family (see [Timeline](#timeline)); publishing a
Foundry-hosted agent into Microsoft 365 Copilot moves its data under Microsoft 365's own
compliance terms (see [Outside-in control](#outside-in-control-publishing-moves-the-compliance-boundary));
and Microsoft Foundry documents a dedicated non-generative decision model (covered in
[system-1-decision-models-landscape.md § Microsoft-Decision-1](../reference/system-1-decision-models-landscape.md#microsoft-decision-1-microsoft-foundry),
not repeated here). A second, later adversarial pass on this same evidence base tightened a
further set of rows toward the vendor's exact wording — most visibly the Agent 365/SharePoint
Skills non-coverage framing, the Flex Routing default-on cutover, and the Package Management
API's licence-and-preview split, all reflected in the sections below — without changing any
verdict or bucket.

## Results

This fact-check pass covered **85 claims specific to the Microsoft 365 Copilot ecosystem**. Claims
about the open Agent Skills specification and coding-agent parity from the same input are covered
in [CC-skills-adoption-analysis.md][cc-skills-doc] instead.

**The 85 Microsoft 365 Copilot-ecosystem claims below, by verdict and bucket:**

| Verdict | checked | not-checked | checked-absent | secondary-only | **Total** |
|---|---|---|---|---|---|
| refuted | 3 | — | — | — | **3** |
| partly | 24 | — | — | — | **24** |
| supported | 47 | — | — | — | **47** |
| unverifiable | — | 2 | 6 | 3 | **11** |
| **Total** | **74** | **2** | **6** | **3** | **85** |

The three in-scope claims that were flatly wrong: a claim that Microsoft's Agent Framework SDK and
Foundry portal don't support structured, schema-constrained outputs is wrong — the SDK supports it
via a `ResponseFormat` property [agent-framework-structured-outputs], and the Foundry workflow designer
lets an agent step return output in a **JSON Schema** text format [foundry-workflow]; a claim that two distinct Microsoft 365 billing
products (Copilot Credits and a separate pay-as-you-go product) share the same spending-cap
behavior is also wrong — they are two different features on two different documentation pages
[credits-overview]; and a tenant-configuration-monitoring capability for Entra (sometimes called
UTCM/TCM) does have first-party documentation (see [Governance](#governance-agent-365-covers-agents-not-sharepoint-skills)
for why that one is also a case study in "not found" versus "refuted").

## Key Findings

### Skills boundary: what Copilot-in-SharePoint Skills can and cannot do

- Skills "can't connect to external systems or execute custom code. A skill can only perform
  actions the user already has permission to do and doesn't expand access or introduce new
  capabilities beyond what Copilot in SharePoint provides" [sp-skills] — confirmed for both
  personal and site skills.
- A skill is either auto-selected by a matching request, or invoked explicitly by name
  [sp-skills].
- Personal skills are available to their owner across SharePoint sites; site skills are scoped to
  their one associated site; neither type is automatically tenant-wide [sp-skills].
- The vendor's September 2026 product blog confirms reuse — "Create a personal skill once and use
  it across all your SharePoint sites." — and an evaluation step: "You can see whether a change
  actually improves quality before you share the skill more broadly." [sp-whats-new-2026-09]. How a
  personal skill is shared is not documented.
- A community catalog of ready-made skill folders exists ([pnp/sharepoint-skills][pnp-skills],
  MIT, PnP community; the repository calls itself "not official Microsoft documentation"). The GA
  announcement lists a "SharePoint skills library" among its resources, but its link target could
  not be read, so whether the two are the same is **unconfirmed** [sp-ga-2026-09-25].
- Skills run on a model Microsoft chooses: "Copilot in SharePoint currently runs on a
  Microsoft-managed reasoning model from OpenAI. Microsoft selects and manages the model, and the
  specific model might change over time" — and "You don't need to configure a model to use Copilot
  in SharePoint" [sp-get-started]. Unlike Copilot Studio, there is no model choice here, so none of
  the Claude/residency detail below applies to SharePoint Skills themselves.
- The documented skills panel has three categories — personal, site, and built-in. The word
  "enterprise" does not appear anywhere on the canonical documentation page, re-checked on two
  separate fetches: a fourth "enterprise" category sometimes claimed is not documented.
- Built-in lifecycle skills help with "creating, checking, and improving skills," and the vendor
  names exactly one of them explicitly ("Create skill"); no fixed public roster confirms literal
  identifiers like `init` beyond that [sp-skills].
- Governance is standard SharePoint file governance only: permissions, retention, sensitivity
  labels, and auditing apply to skill files the same way they apply to any other library content.
  Site owners get a settings panel, but there is no skill-specific admin on/off switch
  [sp-skills] [sp-get-started].
- The vendor's documented display name and conceptual path both use a space — the "Agent Assets"
  library, at `/Agent Assets/Skills/<skill-name>/SKILL.md`. The literal browser/REST URL segment
  for that library is **not documented anywhere** on the vendor's page. Confirm the real
  addressable segment against a live tenant before hard-coding either the spaced or unspaced
  form — this is undocumented, not confirmed either way.
- A skill file in this mechanism is a single markdown file, with no documented subfolder or
  package concept. That is a real contrast with the open Agent Skills specification's optional
  `scripts/`/`references/`/`assets/` package directories (covered separately in
  [CC-skills-adoption-analysis.md][cc-skills-doc]) — Microsoft's own skill documentation is simply
  silent on any such structure for this specific feature, not inconsistent with it.

### Two things called "skill" (and one feature often paired with them)

Microsoft ships at least two separate things called a "skill" inside this family, plus a third
feature that regularly gets cited alongside them but is not a skill at all:

1. **Copilot in SharePoint Skills** — personal and site skills, written as a markdown file under
   a site's Agent Assets library. The Copilot in SharePoint product's own general availability
   rollout begins 2026-09-30 [sp-get-started]; a separate per-item roadmap feed for this same
   Skills capability specifically states GA May CY2026 [rm-sp-custom-skills] — two separately
   documented milestones, neither presented here as derived from or superseding the other. The GA
   announcement (2026-09-25) adds the licence position: "Included with your Microsoft 365 Copilot
   license: The everyday work capabilities customers have been using throughout preview remain
   included", naming "building reusable skills your teams can share" among them
   [sp-ga-2026-09-25]. This is the mechanism covered above.
2. **Custom skills in declarative agents** — a separately named feature for agents built with
   Agent Builder, Agents Toolkit, or Copilot Studio-style declarative agents. As of this pass, the
   only material describing a general-availability rollout by a specific date is a non-vendor
   mirror of an internal messaging post. No vendor documentation page and no vendor roadmap-feed
   entry names this specific feature-and-date combination, and — well past the claimed completion
   window — there is still no first-party confirmation it actually finished rolling out. Treat any
   "custom skills in declarative agents is GA" claim as **unconfirmed** until a vendor page says so
   directly.
3. **Structured document generation** — not a "skill," but a Word-template-to-form-to-document
   renderer that gets cited alongside Skills in capability claims about the product. A claim that
   "Copilot in SharePoint has no saved workflow mechanism and no document-template renderer" is
   wrong on both counts: Skills turns a repeatable workflow into a reusable saved asset, and
   Structured document generation renders completed documents from `.docx` templates and submitted
   form values. Only its three automation-connector actions (form submitted, get form metadata,
   generate document from form) are preview-labelled — the feature itself is not
   [sp-doc-gen].

### Governance: Agent 365 covers agents, not SharePoint skills

- Microsoft Agent 365 reached general availability for the commercial segment on a per-user basis
  on 2026-05-01 ([agent365-overview]; roadmap feed [RM558448][rm-agent365]) and now provides one
  registry and one set of lifecycle actions (approve, block, delete, pin, reassign owner) across
  Copilot Studio agents, Foundry agents, Agent Builder agents, SharePoint-type declarative agents,
  Agents Toolkit agents, and synced third-party agents.
- **SharePoint's own Skills documentation never mentions Agent 365, Entra Agent ID, or any
  centralized registry.** It states plainly: "There are no separate admin controls to turn skills
  on or off" [sp-skills] — no Agent 365 registry entry, no Entra identity, no block/approve
  action; governance is limited to ordinary SharePoint file permissions. **This is the Skills
  page's own documented silence on Agent 365, not a stated exclusion by either page** — the
  governs-agents-not-skills framing above describes what is and isn't covered, not a claim that
  either vendor page says skills are excluded.
- The bring-your-own remote-tool-server registry — the mechanism that *does* unify Copilot
  Studio's MCP story — is itself preview, gated behind the Agent 365 licence, and **explicitly**
  excludes Azure AI Foundry and Microsoft 365 Declarative Agents as supported client surfaces
  during preview (this one is a stated exclusion, unlike the SharePoint Skills non-coverage
  above). Copilot Studio, Visual Studio Code, Claude Code, and GitHub Copilot CLI are the
  supported clients [byo-mcp].
- A narrower, related surface — the Package Management API for listing, updating, blocking,
  unblocking, and reassigning installed apps/agents — has unlabelled (GA-shaped) read operations
  (list/get) and explicitly preview-labelled write operations (update, block, unblock, reassign),
  and requires the Agent 365 licence for **every** operation, including the reads [package-api]
  (roadmap feed [RM502875][rm-package-api]).
- The legacy beta Microsoft Graph agent-registry API documented no licence requirement of its
  own; starting May 2026 it is being replaced by the Agent-365-branded registry API, which does
  require the licence — a real narrowing of who can reach programmatic agent inventory without it
  [agent-registry-beta].
- A separate Entra tenant-configuration-monitoring capability (sometimes called UTCM/TCM) does
  have first-party documentation and public-preview service-principal (app-only) authentication —
  contrary to an earlier internal pass of this same research effort concluding no such page
  existed. A direct example of "not found" meaning "we didn't look hard enough yet," not "doesn't
  exist" [utcm-setup].
- Administrators must explicitly choose, at usage-based billing policy setup, between "don't
  limit monthly spending" and "limit monthly spending" — no default *numeric* spending limit
  exists on the activation page itself, only a preconfigured default billing *method*
  [credits-setup]. Separately, newly released consumptive services are auto-enrolled into that
  default policy unless an administrator changes it [credits-overview] — a silent-by-default
  exposure worth tracking alongside the registry gaps above.
- No first-party Microsoft Agent 365 page states the product's own EU Data Boundary or
  data-residency status, unlike at least two adjacent products in the same family that do carry
  their own documented regional-boundary statements. This is an absence, not a confirmed
  exclusion.

### Lockdown limits: what an admin cannot switch off

- **Copilot Studio authoring is not blockable by group alone.** The "Copilot Studio authors"
  setting "is designed to grant access to users in the specified security group in a
  pay-as-you-go licensing scenario. It doesn't automatically revoke access from other users." A
  block needs all three conditions, the third being "The user doesn't have a Microsoft 365 Copilot
  license." [studio-authors-access] — so Microsoft 365 Copilot licensees keep authoring access.
- **Default environment:** "All licensed users have the environment maker role", with security
  described as "Limited control" [pp-environments].
- **Agent Builder:** the admin center's agent settings page lists seven settings; none of them
  restricts *creating* agents, and "Sharing control only applies to agents built with Microsoft
  Copilot Agent Builder" [agent-settings]. No creation switch was found — not found, not refuted.
- **Agent Assets library:** "created and managed by the product and can't be deleted" [sp-skills];
  restricting who edits it is ordinary SharePoint permission work.

### Tracking changes: which channels have a feed

| Channel | RSS | iCal | Documented alternatives | Source |
|---|---|---|---|---|
| Message center | not documented | not documented | e-mail digest ("a weekly digest of services you select"), one-way Planner sync, Graph `serviceAnnouncement` (JSON) | [message-center], [mc-planner-sync], [service-comms-api] |
| Service health | not documented | not documented | per-tenant e-mail notifications, Graph service communications API (JSON) | [service-health], [service-comms-api] |
| Microsoft 365 Roadmap | **yes** — full-roadmap RSS 2.0 feed, plus per-item feeds (`RoadmapFeatureRSS/<id>`) | not documented | — | [roadmap-rss] |

"Not documented" means no mention in the vendor's pages for that channel, checked 2026-10-22; it
does not prove absence. The vendor's product blog (Tech Community) blocks automated page fetches
but serves the same posts through its board RSS feed.

### Residency: Anthropic excluded from the EU Data Boundary; Claude-on-Foundry has no EU Data Zone either

- Anthropic models deployed in Microsoft 365 Copilot, Researcher, Copilot Studio, Power Platform,
  and Copilot in Microsoft 365 apps "are currently excluded from the EU Data Boundary," and
  "customers within the EU Data Boundary and customers in the UK have Anthropic models disabled by
  default" [eudb-subprocessor] — two separate facts, not one: the exclusion itself is outright, not
  a default that can be toggled from inside the boundary; the disablement is the separate,
  opt-in-able default for in-scope customers.
- Flex Routing — the feature that can send a request outside a tenant's home region — is on by
  default for eligible tenants created after 2026-03-25; for eligible tenants that existed on or
  before that date, Microsoft's own page encourages administrators to check the setting directly
  rather than assume a default one way or the other [flex-routing]. Multi-Geo tenants are outside
  the EU Data Boundary's scope entirely, even when their primary region is listed as being in the
  EU or EFTA [flex-routing].
- Copilot Studio's own per-agent model dropdown lets a maker add external models from Anthropic,
  xAI, or Mistral; in the product's regional-availability table, Anthropic's rows are tagged "GA
  (cross-geo)" in the Europe column while some other vendors' rows read plain "GA" in the same
  column [copilot-model-select].
- Turning external models on takes two switches, not one: admins must "Turn on external models in
  Power Platform admin center for the environment or the environment group" **and** "Allow access
  to each external model provider in the Microsoft 365 admin center" [copilot-model-select].
- Government clouds: "As of July 22, 2026, a new setting is available in the Microsoft 365 admin
  center that allows non-federal customers in Government Community Cloud (GCC) to use Anthropic
  models"; Anthropic models "aren't available for federal customers in GCC or for any customers in
  GCC High and Department of Defense (DoD) environments" [eudb-subprocessor].
- Separately, Microsoft introduced a Microsoft 365 admin center setting on 2026-04-03 letting
  EU/EFTA/UK tenant administrators enable Anthropic as the default model for Copilot in Microsoft
  365 apps — an opt-in setting, off by default, with no preview label on the page documenting it
  [eudb-subprocessor].
- **Stated here as plainly as the Microsoft-side gaps above:** Claude's own hosting on Microsoft
  Foundry has the same shape of limitation. Claude is available only in a **Global Standard** or a
  **US Data Zone Standard** deployment type on Foundry — no EU-region deployment type is listed
  for either hosting option [claude-foundry]. That is a real gap, not a Microsoft-only story. It
  does not by itself mean Claude cannot be deployed at all from an EU-based resource using a
  globally routed deployment option, but there is no EU-region-pinned deployment type to point to
  today.

### Claude's contractual posture across this family

Depending on which path a workload actually uses, Anthropic's contractual role toward Microsoft
documents three different shapes within this family. The summary below states only what each
vendor's own page documents or commits to — it is not legal advice, and a DPIA or vendor-risk
assessment should confirm the path actually in use per workload before relying on any of it:

1. **Claude via Microsoft Foundry** (either the Hosted-on-Azure or the Hosted-on-Anthropic-
   Infrastructure deployment option) — Microsoft documents that "for both hosting options,
   Anthropic is the seller and operator of Claude models in Microsoft Foundry and acts as an
   independent data processor for prompts and outputs associated with Claude models," with
   Microsoft's own Data Protection Addendum governing only billing/marketplace data, not prompts
   or outputs [claude-foundry-privacy]. The two hosting options also diverge on processing
   location: Hosted-on-Azure keeps processing on Azure infrastructure in the selected Azure
   geography; for Hosted-on-Anthropic-Infrastructure, "data might be processed outside of Azure
   including outside of your selected Azure region" [claude-foundry-privacy].
2. **Claude via Microsoft 365 Copilot, standard subprocessor models** — the same family's
   M365-side page documents that "to enable this change, Anthropic has onboarded as a Microsoft
   subprocessor," with the Microsoft Product Terms and Data Protection Addendum applying "unless
   models are labeled 'Anthropic models with Data Retention'" [eudb-subprocessor].
3. **Claude via Microsoft 365 Copilot, opt-in "Data Retention" models** — the same page's "unless
   models are labeled 'Anthropic models with Data Retention'" clause excludes this separately
   opted-in variant from the Microsoft Product Terms and Data Protection Addendum that otherwise
   apply to posture 2, and separately documents that Anthropic, not Microsoft, "stores most inputs
   and outputs for up to 30 days before deleting them" (longer if flagged by Anthropic's own
   trust-and-safety classifiers) [eudb-subprocessor]. The page does not itself name which of
   Anthropic's own terms then governs this variant.

A direct Anthropic API relationship — outside this Microsoft-integrated family entirely — is a
fourth, separate path with its own terms and is not covered by any of the three above.

**Which posture applies is per model, not per vendor.** The same page says "for certain
organizations, Fable 5.1 is available with Anthropic acting as a subprocessor", with no retention of
customer content, while "Anthropic models with Data Retention (such as Fable 5.0)" are "off by
default for all scenarios" [eudb-subprocessor]. Check the posture of the exact model in use, not
"Claude" in general.

### Encryption: Customer Key vs. Double Key Encryption

Microsoft documents two encryption mechanisms with opposite effects on Copilot access, worth
flagging explicitly before relying on either as a blanket policy:

- **Customer Key** (a customer-controlled root key, bring-your-own-key) can be configured, via a
  multi-workload Data Encryption Policy, to cover "Microsoft 365 Copilot interactions" among the
  workloads it lists [customer-key] — Copilot keeps working for content protected this way.
- **Double Key Encryption (DKE)** has the opposite effect: Microsoft states that DKE-encrypted
  data "isn't accessible at rest to Microsoft 365 services including Copilot," and that "you
  can't use Copilot in apps while you're using DKE encrypted data" [dke] — Copilot is unavailable
  for content protected this way, both at rest and (in current Office versions) in use.

Treat this as a deliberate, documented trade-off to plan around when DKE is in use alongside
Copilot — not an oversight to flag during a security review.

### Outside-in control: publishing moves the compliance boundary

Publishing an agent out of Microsoft Foundry and into Microsoft 365 Copilot's Copilot and Teams
chat surface does not keep that agent's data inside the originating platform's own terms.
Microsoft's own publish-to-Copilot documentation states that once published, "those services
process and store certain data associated with publishing and using the agent," and that data "is
subject to the terms, compliance commitments, data residency commitments, and data handling
practices applicable to Microsoft 365 and Teams" [foundry-publish-copilot] — the destination
surface's terms, not the originating hosting platform's own residency commitments. Anyone planning
to publish a Foundry-hosted (or similarly hosted) agent into Microsoft 365 Copilot or Teams should
treat that step as a residency-boundary decision in its own right, not a routine deployment
action.

### Timeline

Dated items worth watching, with the vendor's own per-item roadmap feed where one exists (pattern:
`microsoft.com/microsoft-365/RoadmapFeatureRSS/<id>`) in preference to a general roadmap search
page or a third-party mirror. First-party sources only — no secondary-source items are included in
this table (see [What We Did Not Check](#what-we-did-not-check) for the unverified "custom skills
in declarative agents GA" claim, which stays out of this table for exactly that reason):

| When | Item | Status | Source |
|---|---|---|---|
| 2026-05-01 (passed) | Microsoft Agent 365 reaches GA | GA | [RM558448][rm-agent365] |
| 2026-06-16 (passed) | Work IQ API reaches general availability; billed exclusively through Copilot Credits, with no separate Work IQ API subscription, SKU, or per-user licence | GA | [work-iq-ga] |
| 2026-09-02 (passed) | Product blog: personal skills reusable across all SharePoint sites; evaluate a change before sharing a skill | blog announcement | [sp-whats-new-2026-09] |
| 2026-09-25 (passed) | GA announcement: skills included with the Microsoft 365 Copilot licence; Copilot Search in SharePoint and OneDrive "Rolling out to Frontier Public." | announcement | [sp-ga-2026-09-25] |
| 2026-09-30 (passed) | Copilot in SharePoint GA rollout begins | GA, rolling out | [sp-get-started] |
| 2026-09-30 (passed) | "Copilot in OneDrive becomes generally available September 30." | GA | [sp-ga-2026-09-25] |
| 2026-10-01 (passed) | Product blog: quick access to skills; example of "a custom skill that defines company-specific terms such as 'PII.'" | blog announcement | [sp-whats-new-2026-10] |
| March → April CY2026 (passed, per roadmap feed) | Package Management API preview → GA | mixed — list/get read GA-shaped, 4 mutation operations (update/block/unblock/reassign) still preview | [RM502875][rm-package-api] |
| April → May CY2026 (per roadmap feed) | Roadmap feed for Copilot in SharePoint's custom-skills capability — the same Skills mechanism as the 2026-09-30 GA row above — states preview beginning April CY2026 and GA May CY2026, tagged "Launched"/"General Availability"; the same feed entry still also carries a "Preview" category tag. This is the feed's own tracked milestone for the Skills capability specifically — a separate data point from the product-wide 2026-09-30 rollout above, sourced from a different page; neither date supersedes the other here | GA per roadmap feed (feed also tags Preview) | [RM559800][rm-sp-custom-skills] |
| 2026-04-03 (passed) | Microsoft 365 admin center setting introduced, letting EU/EFTA/UK tenant administrators enable Anthropic as the default model for Copilot in Microsoft 365 apps | GA setting (opt-in, off by default, no preview label) | [eudb-subprocessor] |
| May CY2026 (passed) | Legacy Graph beta agent-registry API begins being replaced by the Agent 365-branded registry API | superseded | [agent-registry-beta] |
| October CY2026, per roadmap feed (in progress — this is the current month) | Structured document generation reaches GA | roadmap-stated GA; 3 automation-connector actions still preview | [RM545896][rm-docgen] |
| 2026-07-22 (passed) | Microsoft 365 admin center setting lets non-federal GCC customers use Anthropic models (not GCC federal, GCC High or DoD) | GA setting | [eudb-subprocessor] |
| 2026-10-15 (passed) | Copilot Studio retires GPT-5.3 Chat and GPT-5.4 Reasoning (replacement "GPT Chat Latest"; extension available) | retired | [copilot-model-select] |
| 2026-10-31 (upcoming) | Copilot Studio retires GPT-5.5 Chat — no extension available | retiring | [copilot-model-select] |
| 2026-11-12 (upcoming) | Copilot Studio retires GPT-4.1, GPT-4.1 Mini, GPT-5 Chat, GPT-5 Auto and GPT-5 Reasoning (extension available); FedRAMP tenants and regions where cross-geo movement is restricted keep GPT-4.1 and GPT-5 | retiring | [copilot-model-select] |
| 2026-11-01 (upcoming) | Preview-era PowerShell opt-in parameters for Copilot in SharePoint stop being honored | retiring | [sp-get-started] |
| 2026-12-01 (upcoming) | Microsoft Foundry's visual workflow designer and in-portal execution retire; YAML-defined workflows keep running as hosted agents under Microsoft Agent Framework | preview feature, partial retirement | [foundry-workflow] |
| ongoing, per roadmap feed | A unified "Workflows" app for Teams + SharePoint automation menus | GA per roadmap feed | [RM491632][rm-workflows-app] |
| — | Copilot Studio's bring-your-own-model feature for prompt-tool nodes explicitly excludes the GPT-5 family and later models | current, no preview label found | [byom-prompts] |

## Guardrails for SharePoint and Microsoft 365 agent skills

Our recommendations, not Microsoft's, for anyone writing a SharePoint skill or a Copilot Studio
agent that answers questions about Microsoft 365 features (licensing, availability, limits). They
come from the failure modes this pass kept running into, and can be written into the skill's own
instructions:

- **Silence is not a "no."** If the docs the agent searched don't mention a feature or limit, it
  should say "not documented in the pages checked", never "not supported". Only a page that states
  the opposite justifies a "no".
- **Say how sure, and why.** Pair every answer with how it was checked — found on a Microsoft page,
  searched and not found, only in community or partner content, or not checked — so a reader can
  tell "nobody looked" from "looked and found nothing".
- **Don't stretch a quote.** A sentence about one product, plan or region doesn't prove the same
  for the whole family. State the narrower scope the source supports.
- **A product description is a claim.** Text from another assistant, a how-to or marketing copy is
  input to check against Microsoft's documentation, not evidence by itself.
- **Dates come from the roadmap item itself.** For preview, GA or retirement dates, use the
  per-item Microsoft 365 Roadmap feed (`microsoft.com/microsoft-365/RoadmapFeatureRSS/<id>`) or the
  product's own Learn page, not a mirror site or search snippet — they can disagree, and the
  vendor's item is what it commits to.

## Operational Scenarios

Separate from the 93-claim challenge pass above, an additional first-party research pass (same
2026-10-21 fetch date) assessed eight recurring operational and automation scenarios against
current vendor documentation: scheduled/event-driven execution, triggering an agent from a
workflow or quick-action shortcut, steering from outside via CLI/API/REST, a daily tenant-wide
sweep, recursive/multi-agent patterns, memory shared across agents or sessions, tracing/tracking,
and a summary feasibility table. **These scenario ratings are not part of the 93-claim verdict ×
bucket counts above** — they use a separate three-value documented / partly documented / not
documented scale, distinct from the verdict × bucket labels the Results section counts, because
they answer a different, scenario-shaped set of questions rather than checking a specific claim
against a specific vendor sentence.

| Scenario | Feasibility | Documented path | Caveat |
|---|---|---|---|
| 1. Daily tenant sweep (unattended, app-only) | Partly documented | Microsoft Graph Change Notifications + Delta Query, app-only confirmed for SharePoint/OneDrive [change-notifications] [delta-query]; agent inventory via the Package Management API (Agent 365 licence required; update/block/unblock/reassign remain preview, see [Governance](#governance-agent-365-covers-agents-not-sharepoint-skills)) [package-api] | SharePoint Advanced Management's data-access-governance reports are admin-center UI only, with no documented REST/PowerShell retrieval for unattended use; Copilot Studio agent interactions are explicitly excluded from the Interaction Export API below |
| 2. A thin CLI-based workflow steering M365 via MCP/API | Partly documented | Claude Code documents OAuth 2.0 support for remote MCP servers over HTTP [code-mcp]; a tenant's own BYO MCP server registration is the documented path to a tenant-registered MCP server [byo-mcp] | No first-party page names Claude Code (or any other specific client) as a consumer of the Microsoft-hosted Work IQ MCP endpoint; that endpoint's own actions are user-bound, not app-only [mcp-work-iq] |
| 3. Recursive / multi-agent patterns | Partly documented | Copilot Studio documents Child Agents (embedded, no separate authentication) and Connected Agents (independently published, referenced by a main agent), plus A2A connections including to Work IQ [add-other-agents] [agent-to-agent] [work-iq-overview] | A reuse rule is documented (an agent already acting as a main agent with its own Connected Agents cannot also serve as a Connected Agent elsewhere); no numeric depth or hop limit is documented, only a qualitative latency warning |
| 4. Shared memory across agents/sessions | Not documented as a finished feature; partly documented as a building block | Work IQ Workspaces (SharePoint-Embedded-backed storage within the tenant boundary) is the closest documented building block for shared state across a long-running workflow [work-iq-overview] | Personal Copilot memory and Copilot Studio's own agent memory are both preview and explicitly siloed per user (and per agent, for Studio) — neither is a shared or global memory; Copilot Studio memory auto-deletes after 28 days of inactivity [copilot-memory] [studio-memory] |
| 5. Tracing and tracking across the tenant | Documented, as a mix of GA and preview pieces | Microsoft Purview Audit logs every Copilot/agent interaction automatically under dedicated record types (GA for Microsoft's own apps) [audit-copilot]; the Office 365 Management Activity API can export that audit data, including Copilot interaction records, to an external HTTPS endpoint (GA) [mgmt-activity-api] | Copilot Studio's own OpenTelemetry-format agent telemetry to Application Insights is preview, excludes declarative agents, and has no documented export beyond Azure [agent-telemetry]; Defender XDR's AI-agent detection on Agent 365 telemetry is a separate, public-preview capability [defender-agent-detection] |
| 6. CLI/API steering instead of each user's own Copilot session | Partly documented | Copilot Studio's "Execute Agent" / "Execute Agent and wait" connector actions are callable from any Power Automate flow (GA) [copilot-studio-connector] | The Chat API is delegated (a signed-in user is required), preview, and cannot take actions (no file creation, no email, no calendar entries) [chat-api]; the Interaction Export API is app-only but is a read-only compliance export, and explicitly excludes Copilot Studio agent interactions [interaction-export-api] |
| 7. A quick-action shortcut or rule triggers an agent | Partly documented, only indirectly | The only documented path is two-step: a quick-action shortcut starts a Power Automate flow, and that flow calls "Execute Agent" / "Execute Agent and wait" as its own action [copilot-studio-connector]; alternatively, a Copilot Studio event trigger placed directly on the agent itself | Whether a SharePoint rule (beyond its notification function) can also start a flow or agent was not checked in this pass; a direct, one-step call from a shortcut straight into an agent is not documented |
| 8. Scheduled Copilot runs | Documented, via two separate mechanisms | Scheduled prompts for Copilot Chat/Teams/Outlook — no preview marker on the support page, capped at 10 scheduled prompts [scheduled-prompts]; a Copilot Studio Recurrence trigger for agents with generative orchestration switched on, authenticated currently using only the agent author's own credentials, not each end user's [studio-triggers] | A third, more capable "Workflows" agent exists for natural-language automation with its own recurrence/event triggers, but it is Frontier early access, not generally available [workflows-agent-start] |

## Pricing

This doc deliberately does not quote Microsoft 365 Copilot, Copilot Studio, Microsoft Agent 365,
Work IQ, Power Automate, Azure OpenAI/Foundry, or Claude list prices. Prices change faster than a
research doc's own review cycle, and a stale number quoted here would be worse than a pointer to
the vendor's own current page. As of **2026-10-21**, consult the vendor's own pricing page
directly for each surface:

- [Microsoft 365 Copilot pricing (Enterprise)][m365-copilot-pricing]
- [Microsoft 365 Copilot pricing (Copilot Studio)][copilot-studio-pricing]
- [Microsoft Agent 365][agent365-pricing]
- [Work IQ general availability and licensing][work-iq-ga] — billed exclusively through Copilot
  Credits, with no separate Work IQ API subscription, SKU, or per-user licence; Microsoft's own
  worked examples on this page are explicitly labelled "illustrative," and the page states that
  prices "will vary based on the complexity of the scenario" — treat any specific number quoted
  anywhere else as a snapshot, not a rate card.
- [Power Automate pricing][power-automate-pricing]
- [Claude pricing][claude-pricing] — Claude via Microsoft Foundry is billed in consumption units;
  check both Anthropic's and Microsoft's current pages for how each surface's pricing is
  presented before relying on either — this doc did not independently verify which page(s) show
  the Foundry consumption-unit rate.

Re-check all of the above directly before using any number for a budget or a contract — none of
them are reproduced here.

## What We Did Not Check

Separate from `checked` results, two further buckets record what this pass could not settle:

**`checked-absent`** (actively searched for on a vendor page; specific wording not found —
absence, not refutation):

- A document-library automation trigger specifically for an approval-status change (only a
  general item/metadata-modified trigger exists; approval status is an action, not a trigger).
- A predefined-action shortcut's internal action name for starting a cloud flow, and whether a
  flow can in turn trigger that same shortcut.
- A system-managed subfolder holding a document library's default-view definition (every source
  describing this names the product's classic, pre-modern experience, not the current one).
- Whether a standard list/library automation rule is scoped to the whole library or can target a
  subfolder — the vendor's own page for this capability never states its scope either way.
- An automation action purpose-built for logging a result or an error at the end of a workflow.
- Whether a named workflow-automation agent feature saves and versions its own definitions and
  which document-template formats it supports (the vendor confirms the feature exists, in a
  limited early-access program, but states nothing about either question).

**`secondary-only`** (no first-party vendor confirmation at all; any corroboration is non-vendor
coverage):

- A persisted planning artifact saved at a specific document-library path, and a specifically
  named feature for scheduling such plans.
- Custom skills in declarative agents reaching GA by a specific date (see
  [Two things called "skill"](#two-things-called-skill-and-one-feature-often-paired-with-them)).
  This is a different feature from the Copilot-in-SharePoint custom-skills roadmap entry in the
  [Timeline](#timeline) above — that entry is about the same mechanism already covered as GA in
  this doc, not about this declarative-agent feature.
- A custom, user-authored context file automatically loaded as agent context by a built-in
  initialization skill — described only in non-vendor blogs.

**`not-checked`** (no attempt made, usually low-novelty or in-session-only):

- Whether deploying a skill automatically creates an associated automation flow, connector, or
  application (directionally consistent with the confirmed "skills can't connect to external
  systems" boundary above, but not independently targeted against a vendor page).

## Adoption Decision

| Dimension | Assessment |
|---|---|
| Use case | Deciding whether and how to build on or alongside Microsoft 365 Copilot's skills, Copilot Studio agents, Work IQ, and Agent 365 governance — not a single tool pick |
| Skills extensibility | Copilot-in-SharePoint Skills: GA, but no admin on/off switch and no governance-registry entry; cannot call external systems or run custom code |
| Agent governance | Agent 365: GA control plane for agents and BYO tool servers; SharePoint Skills are not represented in it at all (documented silence, not a stated exclusion), and the BYO MCP registry explicitly excludes Foundry/declarative-agent tool consumption during preview |
| Model choice, residency & contract | Copilot Studio supports external models from Anthropic, xAI, and Mistral; Anthropic models are excluded from the EU Data Boundary outright and off by default for in-scope customers; Claude's own Foundry hosting has no EU Data Zone deployment type; Claude's contractual posture differs by path (Foundry vs. standard M365 subprocessor vs. opt-in Data Retention models) |
| Licensing model | Mixed by design across surfaces — a seat-based Copilot licence, usage-based credits, and a free gated tier each apply to different parts of the family, not one rule; see [Pricing](#pricing) for current numbers (not reproduced here) |
| Maturity | Mixed: core Skills, Agent 365, and Work IQ are GA; several adjacent automation hooks (document-generation connectors, Package Management API mutations, the BYO MCP registry) remain preview |

**Strengths:** The core SharePoint Skills and Agent 365 mechanics documented here are confirmed,
quote-backed, and dated — most of what the inputs got right, they got right.
Agent 365 is a real, working attempt at a single cross-product governance surface for agents.

**Risks:** Skills and the declarative-agent "custom skills" feature share a name but not a
mechanism — any plan, diagram, or automation that treats them as one thing will misfire. SharePoint
Skills themselves have no governance registry entry, so an organization relying on Agent 365 as its
single control plane will not see them there. The EU residency story has gaps on both the Microsoft
side (Anthropic excluded from the EU Data Boundary outright, and off by default for in-scope
customers) and the Anthropic side (no EU Data Zone on Foundry) — plan around both, not just one. Customer Key and Double Key Encryption have opposite effects on Copilot
access — confirm which one actually protects a given workload before assuming either. Several
cited pages carry near-term dates (2026-11-01, 2026-12-01) that will be in the past within weeks of
this doc's `validated_links` date.

## Action Items

- Re-run this challenge pass on a cadence — a drift job is tracked in #705 — since several
  cited pages carry near-term dates that will go stale quickly.
- Before building against SharePoint Skills, confirm the live tenant's Agent Assets library URL
  segment directly; Microsoft's documented display name and conceptual path both use a space, but
  the real addressable segment is undocumented — don't assume either spelling.
- Treat "custom skills in declarative agents" and "Copilot in SharePoint Skills" as two different
  features in any comparison, diagram, or automation; they share a name, not a mechanism.
- Before assuming any externally hosted model has an EU Data Zone on Microsoft Foundry, confirm
  current region support directly — Claude did not have one as of this pass, and that can change
  independently of anything Microsoft documents.
- Treat any plan to publish a Foundry-hosted agent into Microsoft 365 Copilot or Teams as a
  residency-boundary decision, not a routine deployment step.
- Before relying on Customer Key or Double Key Encryption as a blanket encryption policy for
  content Copilot needs to read, confirm which one actually protects each workload — they have
  opposite, documented effects on Copilot's ability to access that content.

## Cross-References

- [github-copilot-cli-analysis.md](github-copilot-cli-analysis.md) — the disambiguation pattern
  this doc follows for its own "Copilot" name collision
- [agentic-enterprise-os-landscape.md](../frameworks/agentic-enterprise-os-landscape.md) — the
  Tier-1 Copilot Studio landscape row this doc extends with model-choice, BYO-MCP, residency, and
  governance detail
- [CC-skills-adoption-analysis.md][cc-skills-doc] — the open Agent Skills specification that
  SharePoint's SKILL.md-style skills resemble
- [system-1-decision-models-landscape.md § Microsoft-Decision-1](../reference/system-1-decision-models-landscape.md#microsoft-decision-1-microsoft-foundry)
  — Foundry's decision model, covered there
- [agent-identity-auth-landscape.md](../../sdlc-lcm/agent-identity-auth-landscape.md) — Entra Agent
  ID, the identity layer under Agent 365 and Copilot Studio agents
- [CC-memory-system-analysis.md](../../cc-native/context-memory/CC-memory-system-analysis.md) —
  compares Copilot Studio memory (28-day auto-delete) with Claude Code's memory model

## Sources

| Source | Content |
|---|---|
| [Copilot in SharePoint — Skills][sp-skills] | Mechanics, categories, built-in skills, governance, Agent Assets path |
| [Copilot in SharePoint — Get started][sp-get-started] | GA date, PowerShell retirement date, settings panel, "Workflow" terminology |
| [Copilot in SharePoint — Structured document generation][sp-doc-gen] | Template format, preview-labelled automation actions |
| [Microsoft Agent 365 — Overview][agent365-overview] | GA date, registry scope, per-user licensing model |
| [Microsoft 365 admin — Manage BYO MCP servers][byo-mcp] | Preview status, supported/excluded client surfaces |
| [Microsoft 365 Copilot — Package Management API overview][package-api] | GA-shaped reads vs. preview writes, licence requirement |
| [Microsoft Graph — agentRegistry (beta) resource][agent-registry-beta] | Legacy API replacement notice |
| [Microsoft Graph — UTCM/TCM authentication setup][utcm-setup] | Public preview, service-principal (app-only) authentication |
| [Microsoft 365 Copilot — Connect to AI subprocessor][eudb-subprocessor] | Anthropic EU Data Boundary exclusion, subprocessor/Data-Retention postures, EU/EFTA/UK admin setting |
| [Microsoft 365 Copilot — Flex routing][flex-routing] | Default-on cutover date, older-tenant guidance, Multi-Geo scope |
| [Claude in Microsoft Foundry][claude-foundry] | Deployment types, absence of an EU-region type |
| [Claude in Microsoft Foundry — Data, privacy, and security][claude-foundry-privacy] | Processor role, hosting-option processing-location split |
| [Microsoft Foundry — Publish an agent to Copilot][foundry-publish-copilot] | Residency-boundary shift on publish |
| [Microsoft Foundry — Workflows (preview)][foundry-workflow] | December 2026 retirement, YAML continuity, JSON Schema output format per agent step |
| [Microsoft Agent Framework — Structured outputs][agent-framework-structured-outputs] | Refutes a "no structured output support" claim |
| [Microsoft 365 Copilot — Usage-based billing credits setup][credits-setup] | No default numeric spending limit |
| [Microsoft 365 Copilot — Usage-based billing overview][credits-overview] | Auto-enrollment of new services; distinct pay-as-you-go product |
| [Microsoft Copilot Studio — Bring your own model for prompts][byom-prompts] | GPT-5 family excluded |
| [Microsoft Copilot Studio — Select agent model][copilot-model-select] | Anthropic/xAI/Mistral support, cross-geo tagging |
| [Microsoft 365 Copilot — Copilot APIs overview][copilot-apis-overview] | Licensing distinct from the general-purpose Graph API |
| [Microsoft Purview — Customer Key overview][customer-key] | Customer Key coverage including Copilot interactions |
| [Microsoft Purview — Double Key Encryption][dke] | DKE blocks Copilot access, at rest and in use |
| [Work IQ overview][work-iq-overview] | REST/MCP/A2A surfaces, licensing model, Workspaces |
| [Microsoft Graph — Change notifications overview][change-notifications] | App-only tenant-sweep mechanism (push) |
| [Microsoft Graph — Delta query overview][delta-query] | App-only tenant-sweep mechanism (pull) |
| [Work IQ API — MCP overview][mcp-work-iq] | User-bound MCP access, no named client product |
| [Claude Code — Model Context Protocol (MCP)][code-mcp] | OAuth 2.0 remote-MCP client support, managed configuration |
| [Copilot Studio — Authoring: add other agents][add-other-agents] | Child/Connected agent reuse rule, no depth limit |
| [Copilot Studio — Add an Agent2Agent agent][agent-to-agent] | A2A protocol connections |
| [Copilot personalization and memory][copilot-memory] | Preview, per-user, siloed, no audit log |
| [Copilot Studio — Memory overview][studio-memory] | Preview, per-user-per-agent, 28-day auto-delete |
| [Microsoft Purview — Audit for Copilot][audit-copilot] | GA audit logging of Copilot/agent interactions |
| [Office 365 Management Activity API reference][mgmt-activity-api] | SIEM export path for audit data |
| [Copilot Studio — Advanced environment-level agent telemetry][agent-telemetry] | Preview OpenTelemetry export, excludes declarative agents |
| [Defender XDR — AI agent detection and protection][defender-agent-detection] | Public-preview Agent 365 telemetry detection |
| [Microsoft Copilot Studio connector (Power Platform)][copilot-studio-connector] | "Execute Agent" / "Execute Agent and wait" actions |
| [Copilot APIs — Chat API][chat-api] | Delegated-only, preview, no actions |
| [Microsoft Graph — aiInteractionHistory: getAllEnterpriseInteractions][interaction-export-api] | App-only, read-only compliance export |
| [Schedule your most used Copilot prompts][scheduled-prompts] | Scheduled prompts, capped at 10, no preview marker |
| [Copilot Studio — Authoring triggers][studio-triggers] | Recurrence/event triggers, author-credential auth |
| [Get started with Workflows in Microsoft 365 Copilot][workflows-agent-start] | Frontier early access, not GA |
| [Roadmap feed 491632][rm-workflows-app] | Unified Workflows app (Teams + SharePoint) |
| [Roadmap feed 502875][rm-package-api] | Package Management API preview/GA timing |
| [Roadmap feed 545896][rm-docgen] | Structured document generation GA timing |
| [Roadmap feed 558448][rm-agent365] | Agent 365 GA timing |
| [Roadmap feed 559800][rm-sp-custom-skills] | Copilot in SharePoint custom-skills preview/GA timing |
| [Microsoft 365 Copilot pricing — Enterprise][m365-copilot-pricing] | Pricing pointer only, no figures reproduced |
| [Microsoft 365 Copilot pricing — Copilot Studio][copilot-studio-pricing] | Pricing pointer only, no figures reproduced |
| [Microsoft Agent 365][agent365-pricing] | Pricing pointer only, no figures reproduced |
| [Work IQ general availability][work-iq-ga] | GA date, licensing model, "illustrative"-labelled pricing examples |
| [Power Automate pricing][power-automate-pricing] | Pricing pointer only, no figures reproduced |
| [Claude pricing][claude-pricing] | Pricing pointer only, no figures reproduced |
| [SharePoint blog — "SharePoint AI innovations hit GA…" (2026-09-25)][sp-ga-2026-09-25] | Skills licence inclusion, OneDrive GA date, Frontier rollout; text read via the blog's RSS feed |
| [SharePoint blog — What's new, September 2026][sp-whats-new-2026-09] | Personal-skill reuse across sites, evaluate before sharing |
| [SharePoint blog — What's new, October 2026][sp-whats-new-2026-10] | Quick access to skills, company-terms skill example |
| [Copilot Studio — Authors access (troubleshoot)][studio-authors-access] | Authors setting does not revoke access; three conditions for a block |
| [Microsoft 365 admin — Agent settings][agent-settings] | Seven agent settings, sharing control scope |
| [Power Platform — Environments overview][pp-environments] | Default environment: every licensed user is a maker |
| [Microsoft 365 admin — Message center][message-center] | E-mail digest options |
| [Microsoft Graph — Service communications API][service-comms-api] | Programmatic (JSON) access to Message center and Service health |
| [Track message center tasks in Planner][mc-planner-sync] | Message center → Planner one-way sync |
| [View service health][service-health] | Service health notification channels |
| [Microsoft 365 Roadmap RSS feed][roadmap-rss] | Full-roadmap RSS 2.0 feed |
| [pnp/sharepoint-skills][pnp-skills] (secondary — prior art, not evidence) | "Skills for Copilot in SharePoint": MIT community catalog in the [PnP][pnp-home] org (Microsoft 365 & Power Platform community); says it is "not official Microsoft documentation". SKILL.md samples and Agent Assets path conventions |
| [ShareGate — "Skills in SharePoint: What IT pros need to know"][sharegate-skills] (secondary — prior art, not evidence) | By Jasper Oosterveld, 2026-10-13. [ShareGate][sharegate-about] is "developed by Workleap Technologies" and sells Microsoft 365 migration and governance tools (ShareGate Migrate, ShareGate Protect) — a vendor with a stake in governance advice. Governance checklist for SharePoint Skills |
| ["Governing SharePoint Skills and Agents: What Admins Need to Know" webinar][governing-sp-skills-webinar] (secondary — prior art, not evidence) | Free webinar, 2026-11-12 (upcoming), presented by [Vlad Catrinescu][catrinescu-about] ("Microsoft MVP and MCT · Pluralsight Author") and [Drew Madelung][madelung-profile] ("Director, Microsoft Solutions at Protiviti"); [registration][governing-sp-skills-reg]. Maps each governance control to the area it governs |

[sp-skills]: https://learn.microsoft.com/en-us/sharepoint/copilot-in-sharepoint-skills
[sp-get-started]: https://learn.microsoft.com/en-us/sharepoint/copilot-in-sharepoint-get-started
[sp-doc-gen]: https://learn.microsoft.com/en-us/sharepoint/copilot-in-sharepoint-structured-document-generation
[agent365-overview]: https://learn.microsoft.com/en-us/microsoft-agent-365/overview
[byo-mcp]: https://learn.microsoft.com/en-us/microsoft-365/admin/manage/manage-byo-mcp-server
[package-api]: https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/api/admin-settings/package/overview
[agent-registry-beta]: https://learn.microsoft.com/en-us/graph/api/resources/agentregistry
[utcm-setup]: https://learn.microsoft.com/en-us/graph/utcm-authentication-setup
[eudb-subprocessor]: https://learn.microsoft.com/en-us/microsoft-365/copilot/connect-to-ai-subprocessor
[flex-routing]: https://learn.microsoft.com/en-us/microsoft-365/copilot/copilot-flex-routing
[claude-foundry]: https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry
[code-mcp]: https://code.claude.com/docs/en/mcp
[claude-foundry-privacy]: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/claude-models/data-privacy
[foundry-publish-copilot]: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/publish-copilot
[foundry-workflow]: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/workflow
[agent-framework-structured-outputs]: https://learn.microsoft.com/en-us/agent-framework/agents/structured-outputs
[credits-setup]: https://learn.microsoft.com/en-us/microsoft-365/copilot/usage-based-billing-copilot-credits-setup
[credits-overview]: https://learn.microsoft.com/en-us/microsoft-365/copilot/usage-based-billing-overview-copilot-credits
[byom-prompts]: https://learn.microsoft.com/en-us/microsoft-copilot-studio/bring-your-own-model-prompts
[copilot-model-select]: https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-select-agent-model
[copilot-apis-overview]: https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/copilot-apis-overview
[customer-key]: https://learn.microsoft.com/en-us/purview/customer-key-overview
[dke]: https://learn.microsoft.com/en-us/purview/double-key-encryption
[work-iq-overview]: https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/
[change-notifications]: https://learn.microsoft.com/en-us/graph/change-notifications-overview
[delta-query]: https://learn.microsoft.com/en-us/graph/delta-query-overview
[mcp-work-iq]: https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/work-iq/mcp/overview
[add-other-agents]: https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-add-other-agents
[agent-to-agent]: https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-agent-to-agent
[copilot-memory]: https://learn.microsoft.com/en-us/microsoft-365/copilot/copilot-personalization-memory
[studio-memory]: https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/memory-overview
[audit-copilot]: https://learn.microsoft.com/en-us/purview/audit-copilot
[mgmt-activity-api]: https://learn.microsoft.com/en-us/office/office-365-management-api/office-365-management-activity-api-reference
[agent-telemetry]: https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-environment-level-agent-telemetry
[defender-agent-detection]: https://learn.microsoft.com/en-us/defender-xdr/security-for-ai/ai-agent-detection-protection
[copilot-studio-connector]: https://learn.microsoft.com/en-gb/connectors/microsoftcopilotstudio
[chat-api]: https://learn.microsoft.com/microsoft-365/copilot/extensibility/api/ai-services/chat/copilotroot-post-conversations
[interaction-export-api]: https://learn.microsoft.com/en-us/graph/api/aiinteractionhistory-getallenterpriseinteractions
[scheduled-prompts]: https://support.microsoft.com/en-us/topic/schedule-your-most-used-copilot-prompts-29dfd5fb-211a-4515-88a6-730b8074e489
[studio-triggers]: https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-triggers-about
[workflows-agent-start]: https://support.microsoft.com/topic/get-started-with-workflows-in-microsoft-365-copilot-8c6aba25-db31-443d-8319-bc79747b280a
[rm-workflows-app]: https://www.microsoft.com/microsoft-365/RoadmapFeatureRSS/491632
[rm-docgen]: https://www.microsoft.com/microsoft-365/RoadmapFeatureRSS/545896
[rm-agent365]: https://www.microsoft.com/microsoft-365/RoadmapFeatureRSS/558448
[rm-package-api]: https://www.microsoft.com/microsoft-365/RoadmapFeatureRSS/502875
[rm-sp-custom-skills]: https://www.microsoft.com/microsoft-365/RoadmapFeatureRSS/559800
[m365-copilot-pricing]: https://www.microsoft.com/en-us/microsoft-365-copilot/pricing/enterprise
[copilot-studio-pricing]: https://www.microsoft.com/en-us/microsoft-365-copilot/pricing/copilot-studio
[agent365-pricing]: https://www.microsoft.com/en-us/microsoft-agent-365
[work-iq-ga]: https://www.microsoft.com/en-us/licensing/news/work-iq-general-availability
[power-automate-pricing]: https://www.microsoft.com/en-us/power-platform/products/power-automate/pricing
[claude-pricing]: https://platform.claude.com/docs/en/about-claude/pricing
[pnp-skills]: https://github.com/pnp/sharepoint-skills
[sp-ga-2026-09-25]: https://techcommunity.microsoft.com/blog/spblog/sharepoint-ai-innovations-hit-ga-powering-new-copilot-app-and-agents/4555724
[sp-whats-new-2026-09]: https://techcommunity.microsoft.com/t5/microsoft-sharepoint-blog/what-s-new-in-copilot-in-sharepoint-september-2026/ba-p/4535422
[sp-whats-new-2026-10]: https://techcommunity.microsoft.com/t5/microsoft-sharepoint-blog/what-s-new-in-copilot-in-sharepoint-october-2026/ba-p/4535423
[studio-authors-access]: https://learn.microsoft.com/en-us/troubleshoot/power-platform/copilot-studio/licensing/authors-access
[agent-settings]: https://learn.microsoft.com/en-us/microsoft-365/admin/manage/agent-settings
[mc-planner-sync]: https://learn.microsoft.com/en-us/office365/planner/track-message-center-tasks-planner
[message-center]: https://learn.microsoft.com/en-us/microsoft-365/admin/manage/message-center
[service-comms-api]: https://learn.microsoft.com/en-us/graph/api/resources/service-communications-api-overview
[pp-environments]: https://learn.microsoft.com/en-us/power-platform/admin/environments-overview
[service-health]: https://learn.microsoft.com/en-us/microsoft-365/enterprise/view-service-health
[roadmap-rss]: https://www.microsoft.com/releasecommunications/api/v2/m365/rss
[sharegate-skills]: https://sharegate.com/blog/skills-in-sharepoint-what-it-pros-need-to-know
[governing-sp-skills-webinar]: https://vladtalkstech.com/microsoft-events-and-discount-codes/governing-sharepoint-skills-agents-webinar/
[governing-sp-skills-reg]: https://vladtalks.com/Governing-SharePoint-Skills-Agents
[catrinescu-about]: https://vladtalkstech.com/about/
[madelung-profile]: https://drewmadelung.com
[sharegate-about]: https://sharegate.com/about
[pnp-home]: https://pnp.github.io/
[cc-skills-doc]: ../../cc-native/agents-skills/CC-skills-adoption-analysis.md
