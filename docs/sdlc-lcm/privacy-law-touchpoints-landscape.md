---
title: Privacy Law Touchpoints for Agent Systems (GDPR, UK GDPR, CCPA, PIPEDA, Quebec)
purpose: Map of what five privacy regimes require, and where those duties touch memory, logs, model-provider data use, transfers, automated decisions and scraping in this knowledge base.
created: 2026-11-27
updated: 2026-11-27
validated_links_on: 2026-11-27
status: assess
---

## What It Is

A requirements map for five privacy regimes, followed by a table that ties each duty to the KB topic it
touches. The regimes: the EU General Data Protection Regulation (GDPR), the UK GDPR with the Data Protection
Act 2018 (DPA 2018), the California Consumer Privacy Act as amended by the California Privacy Rights Act
(CCPA/CPRA), Canada's federal Personal Information Protection and Electronic Documents Act (PIPEDA), and
Quebec's private-sector law as changed by Law 25.

**Not legal advice.** This is a research note by a non-lawyer, built from statute and regulator text read on
2026-11-27. Whether a regime applies to a given system, and how, is a question for counsel. Cells that could not
be read at the first-party source say **unverified**. The EU AI Act and the AI-specific frameworks are out of
scope here; see [ai-security-governance-analysis.md](ai-security-governance-analysis.md).

Every regime below is a different statute with different definitions; the table lines up topics, not
equivalence. Article and section numbers are the load-bearing part; the wording is our paraphrase unless quoted.

## Requirements at a glance

Legal text read 2026-11-27: GDPR on [EUR-Lex][gdpr] (version in force as published there); UK GDPR as
revised on [legislation.gov.uk][ukgdpr]; CCPA from the [California statute text][ccpa-stat], with the
[Attorney General's page][oag] as the pointer; PIPEDA from [Justice Laws][pipeda]. The Quebec column is
**unverified** throughout: LégisQuébec and the Commission d'accès à l'information (CAI) blocked every
read attempt (see [Not verified](#not-verified)).

| Topic | EU GDPR | UK GDPR + DPA 2018 | CCPA / CPRA | PIPEDA | Quebec (Law 25) |
|---|---|---|---|---|---|
| Who it applies to | Controllers and processors established in the EU; also non-EU ones offering goods or services to, or monitoring the behaviour of, people in the EU (Art. 3(1)-(2)) | Same structure as the EU text with UK territorial wording: controllers and processors established in the United Kingdom, and non-UK ones whose "relevant processing" (defined in the inserted Art. 3(2A)) relates to offering goods or services to, or monitoring the behaviour of, people in the UK (Art. 3(1)-(2A), read on legislation.gov.uk) | A "business" doing business in California that meets a threshold: gross revenue over $25,000,000 (as adjusted), or buys, sells or shares data of 100,000+ consumers or households, or earns 50% of revenue from selling or sharing (§ 1798.140(d)(1)). "Consumer" = California resident (§ 1798.140(i)) | Every organization in respect of personal information collected, used or disclosed in the course of commercial activities (s. 4(1)(a)) | Unverified |
| Lawful basis or notice | One of six bases, e.g. consent, contract, legitimate interests (Art. 6(1)(a)-(f)) | Art. 6(1) plus a new basis (ea), "processing is necessary for the purposes of a recognised legitimate interest", limited to conditions in Annex 1 (Art. 6(1)(ea), (5)) | No lawful-basis test. Notice at or before collection of categories, purposes, and whether sold or shared (§ 1798.100(a)) | Knowledge and consent of the individual, with exceptions (Sch. 1 cl. 4.3; Principle 3) | Unverified |
| Access, correction, deletion, opt-out | Access (Art. 15), erasure (Art. 17(1)(a)-(f), with exceptions in 17(3)) | Same articles (Art. 15, 17 opened on legislation.gov.uk, no UK amendment note) | Delete (§ 1798.105(a)), know/access (§ 1798.110), correct (§ 1798.106), limit use of sensitive data (§ 1798.121), opt out of sale or sharing (§ 1798.120(a)(1)) | Individual access (Sch. 1 cl. 4.9, 4.9.1); destroy, erase or anonymize data no longer needed (cl. 4.5.3). No general erasure right read | Unverified |
| Automated decisions | A right not to be subject to a decision "based solely on automated processing" with legal or similarly significant effects, with contract, law and explicit-consent exceptions and a right to human intervention (Art. 22(1)-(3)) | Art. 22 replaced from 2026-02-05 by Arts. 22A-22D (22D not read): a "significant decision" without "meaningful human involvement" needs safeguards (information, representations, human intervention, contest) (Art. 22A(1), 22C(2)); barred if based on special-category data without a listed condition, or on recognised legitimate interests (Art. 22B(1), (4)) | No decision-level right in the statute. The CPPA is directed to issue rules on access and opt-out rights for "automated decisionmaking technology, including profiling" (§ 1798.185(a)(15)). Whether final rules exist: **unverified** | No provision found in the Act text read (searched "automated": none) | Unverified |
| Records, DPIAs, risk assessment | Records of processing (Art. 30); impact assessment before high-risk processing, required for systematic evaluation that drives significant decisions (Art. 35(1), (3)(a)) | Art. 30 and Art. 35 present in the revised text, no UK change noted in Art. 35(1) | Statute directs the CPPA to issue rules on annual cybersecurity audits and risk assessments for high-risk processing (§ 1798.185(a)(14)). Final rules: **unverified** | Records of every breach (s. 10.3); no impact-assessment duty found in the Act text read | Unverified |
| Breach notification | Controller to the authority within 72 hours where feasible, unless unlikely to cause risk (Art. 33(1)); processor to controller "without undue delay" (Art. 33(2)) | Art. 33 same, notifying "the Commission" (the revised text substitutes it; read) | No notification clock in the CCPA text read. Private action for data breaches from failed security, $100-$750 per consumer per incident or actual damages, whichever is greater, amounts as adjusted (§ 1798.150(a)(1)(A)). State breach-notice law not read: **unverified** | Report to the Commissioner and notify individuals where there is "a real risk of significant harm", "as soon as feasible" (s. 10.1(1)-(3)) | Unverified |
| Cross-border transfer | Allowed only on Chapter V conditions: adequacy (Art. 45), safeguards such as standard clauses (Art. 46), derogations (Art. 49) (Art. 44) | Art. 44 omitted 2026-02-05; Art. 44A allows transfer if approved by regulations under Art. 45A (which apply the "data protection test" in Art. 45B), made with appropriate safeguards (Art. 46) or under a derogation (Art. 49) | No transfer restriction identified in the sections read ("outside of California" occurs only in other contexts); not an exhaustive search | No transfer ban; the organization stays responsible for data it passes to a third party for processing and must use "contractual or other means" for comparable protection (Sch. 1 cl. 4.1.3) | Unverified |
| Processor or service-provider contracts | Binding contract with listed terms, e.g. process only on documented instructions, incl. on transfers (Art. 28(3)(a)) | Art. 28 present | Written contract prohibiting selling or sharing and use outside the business purpose (§ 1798.140(ag)(1)); agreement required when disclosing to a service provider (§ 1798.100(d)) | Contractual or other means (Sch. 1 cl. 4.1.3) | Unverified |
| Penalties | Up to EUR 20,000,000 or 4% of worldwide annual turnover for basic-principle, rights and transfer infringements; EUR 10,000,000 or 2% for controller and processor duties incl. Arts. 25-39 (Art. 83(4)-(5)) | Up to GBP 17,500,000 or 4%; GBP 8,700,000 or 2% (Art. 83(4)-(5), as revised) | Administrative fine up to $2,500 per violation, $7,500 per intentional violation or those involving known minors under 16, as adjusted (§ 1798.155(a)) | Offence, fine up to $100,000 on indictment (up to $10,000 on summary conviction), for knowingly contravening s. 8(8), 10.1, 10.3(1) or 27.1(1) or obstructing a complaint investigation or audit (s. 28) | Unverified |

Reading notes:

- The UK column is a separate legal text from the EU one. Art. 22 and Art. 44 differ, and the UK amendments
  come from the Data (Use and Access) Act 2025 (DUAA), whose [contents page][duaa] shows no outstanding
  effects (read 2026-11-27). The Arts. 22A-22C and 44A texts above come from the revised UK GDPR pages,
  each of which names DUAA and S.I. 2026/82 as the amending source and 2026-02-05 as the commencement date for the parts not already in force (Art. 22A-22C pages: "19.6.2025 for specified purposes, 5.2.2026 in so far as not already in force").
- Not every UK difference is from DUAA: Art. 3(2A) was inserted by the EU-exit regulations, S.I. 2019/419
  (per the revised Art. 3 page).
- Under the CCPA, "service provider" is defined by contract terms (§ 1798.140(ag)(1)), not by role. The
  statute's dollar figures are "as adjusted"; the adjusted figures live in a separate section not read.
- PIPEDA is principle-based (Schedule 1) and has no analogue of Art. 22 or Art. 35 in the text read.

## KB touchpoints

How each duty reaches a topic in this knowledge base. Obligations are those in the table above. The "How"
column is **our synthesis**, not a legal conclusion.

| KB topic | Obligations it touches | KB doc | How (our synthesis) |
|---|---|---|---|
| Agent memory and long-term stores | Erasure (GDPR Art. 17; CCPA § 1798.105), access (Art. 15; § 1798.110), retention (PIPEDA cl. 4.5.3), records (Art. 30) | [memory hub](../_topics/memory.md); [CC memory system analysis](../cc-native/context-memory/CC-memory-system-analysis.md); [temporal knowledge-graph memory](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#temporal-knowledge-graph-memory-evidence-and-caveats) | A store that holds a person's data needs a way to find and delete it. Designs that invalidate instead of delete, or never summarize, need a separate purge path. |
| Session logs, transcripts and telemetry | Erasure and access (above), breach reporting (GDPR Art. 33; PIPEDA s. 10.1), records of breaches (s. 10.3) | [CC-1x session schema](../cc-native/sessions/CC-1x-session-schema.md); [monitoring and telemetry](../cc-native/configuration/CC-monitoring-telemetry-analysis.md); [agent observability methods](../non-cc/protocols/agent-observability-methods-analysis.md) | Transcripts hold whatever users typed or tools returned, so a log store is a personal-data store once any of it names a person. Log retention and who can read exported telemetry become privacy questions. |
| Model-provider data use and training clauses | Processor terms (Art. 28(3)(a); § 1798.140(ag)(1); PIPEDA cl. 4.1.3), lawful basis (Art. 6) | [enterprise data APIs for agents](../non-cc/frameworks/agentic-enterprise-os-landscape.md#enterprise-data-apis-for-agents); [model provider configuration](../cc-native/configuration/CC-model-provider-configuration.md) | Sending personal data to a model API makes the provider a processor or service provider; "not used for training" and zero-retention claims in provider docs are the facts a processor contract would pin down. |
| Cross-border transfer and data residency | GDPR Arts. 44-46; UK Arts. 44A, 45B, 46; PIPEDA cl. 4.1.3 | [Google Cloud agent stack, Regions](../non-cc/agents/google-cloud-agent-stack-analysis.md#regions); [decision models landscape](../non-cc/reference/system-1-decision-models-landscape.md) | A region list covers data at rest only in at least one platform doc ("model processing follows the model endpoint's location"), so residency and transfer analysis must follow where inference runs, not only where sessions and memory sit. |
| Automated decisions by agents | GDPR Art. 22; UK Arts. 22A-22C; CCPA § 1798.185(a)(15) (rules directed) | [decision models landscape § Tool-call gating](../non-cc/reference/system-1-decision-models-landscape.md#3-tool-call-gating); [§ Confidence gate](../non-cc/reference/system-1-decision-models-landscape.md#6-confidence-gate-act--confirm--human-in-the-loop-escalation) | A confidence gate that escalates to a person is the shape of "meaningful human involvement" (UK Art. 22A(1)(a)) or "human intervention" (Art. 22(3)); a gate that only logs does not meet either wording. |
| Web scraping and crawling | Lawful basis and notice (Art. 6; § 1798.100(a); PIPEDA consent), territorial reach (Art. 3(2)(b)) | [web scraping and extraction landscape](../non-cc/infrastructure/web-scraping-extraction-landscape.md); [AI crawlers and discoverability](../non-cc/infrastructure/ai-crawlers-discoverability-landscape.md) | Scraped pages that name people carry the same duties as data collected directly; robots.txt and crawler tokens are access signals, not a lawful basis. |
| Agent identity | Access and records (Art. 15, 30), processor contracts | [agent identity and auth landscape](agent-identity-auth-landscape.md) | Agent-held credentials and delegated access create records of who an agent acted for, which are themselves personal data of the principal. |
| Evals and datasets with personal data | Lawful basis and purpose (Art. 6), DPIA (Art. 35), erasure | [evals and benchmarks hub](../_topics/evals-benchmarks.md) | A test or eval set built from real user content is personal data processing; the purpose is "evaluation", which should be named in notices. |

## Where they interfere or interact

All items are **our synthesis**; each points at the obligations cited above.

- **Erasure against append-only stores.** GDPR Art. 17(1) and CCPA § 1798.105(a) ask for deletion; event logs,
  git history, bi-temporal memory that keeps invalidated facts, and vector stores without per-record delete
  conflict with it unless data is kept out of immutable layers or can be removed from them. PIPEDA cl. 4.5.3
  allows "made anonymous" as an alternative to destroying data, which GDPR Art. 17 does not.
- **Autonomous decisions against Art. 22 and 22A-22C.** An agent that approves, denies or ranks people with no
  human step falls under the EU text when legal or similarly significant effects follow; the UK text adds a
  definition of "meaningful human involvement" and bars solely automated decisions based on recognised
  legitimate interests (Art. 22B(4)).
- **US-hosted model APIs against transfer rules.** Sending EU or UK personal data to a model endpoint outside
  those territories is a transfer under Art. 44 (EU) or Art. 44A (UK); the CCPA has no matching restriction
  in the text read, and PIPEDA relies on contract (cl. 4.1.3).
- **Processor terms differ by statute.** One provider contract can be asked to satisfy GDPR Art. 28(3),
  CCPA § 1798.140(ag)(1) and PIPEDA cl. 4.1.3 at once; the CCPA ties "service provider" status to listed
  contract prohibitions, so a missing clause changes the legal category, not only the risk.
- **Breach clocks do not align.** 72 hours (GDPR Art. 33) against "as soon as feasible" (PIPEDA s. 10.1(2));
  agent platforms that log tool outputs have to decide which clock starts when.
- **Impact assessments are statute-driven in the EU and UK, rule-driven in California.** GDPR Art. 35(3)(a)
  names automated evaluation of people as a trigger; the CCPA has only a rulemaking direction
  (§ 1798.185(a)(14)), whose final rules were not read.
- **UK divergence.** DUAA created UK-only text (Arts. 22A-22C, 44A, 45B, a recognised-legitimate-interest basis),
  so a design checked against the EU GDPR is not automatically checked against the UK one.

## Not verified

- **Quebec Law 25 (all cells).** The Act respecting the protection of personal information in the private
  sector (P-39.1) on LégisQuébec returned 502 on every attempt, the CAI site returned 429, and the Bill 64 PDF
  on Publications du Québec was not extractable by the helper. A search summary named provisions on privacy
  impact assessments, automated decisions and profiling notices; none are quoted here because none were read.
- **Canada Bill C-27.** LEGISinfo on parl.ca returned 403. The only source read is the Privacy Commissioner's
  [2024-2025 annual report][opc-ar], which states that "Bill C-27, which would have modernized PIPEDA, died on
  the order paper with the prorogation of Parliament in January 2025" (read 2026-11-27). Whether a successor bill
  exists in the 45th Parliament is unverified.
- **CPPA regulations** (risk assessments, cybersecurity audits, ADMT, access and opt-out rules): the
  cppa.ca.gov pages returned 403. The [Attorney General's page][oag] (read 2026-11-27) still describes the
  right-to-correct and right-to-limit rules as not final, so it lags the statute and is not used for rule status.
- **CCPA adjusted dollar amounts and the state breach-notification statute** (Civil Code § 1798.82): not read.
- **UK text read and not read.** Read: Arts. 3, 6, 22A-22C, 33, 35, 44, 44A, 45B and 83. Opened, with no UK
  amendment note: Arts. 15, 17 and 30. Art. 28 is marked "present" from the table of contents only. Not read:
  Art. 12 time limits, Art. 22D, Art. 49, and EDPB or ICO guidance (including how regulators treat model weights
  or logs).
- **No court or regulator decisions** are cited; none were read.

## Sources

| Source | Content |
|---|---|
| [GDPR, Regulation (EU) 2016/679, EUR-Lex][gdpr] | Arts. 3, 6, 15, 17, 22, 28, 30, 33, 35, 44, 46, 83 (read 2026-11-27) |
| [UK GDPR, legislation.gov.uk][ukgdpr] | Revised text: Arts. 3, 6, 22A-22C, 33, 35, 44, 44A, 45B, 83 (read 2026-11-27) |
| [Data (Use and Access) Act 2025][duaa] | Amending Act; no outstanding effects noted (read 2026-11-27) |
| [CCPA statute text, California Legislative Information][ccpa-stat] | Civil Code §§ 1798.100-1798.185 (read 2026-11-27) |
| [California Attorney General, CCPA][oag] | Pointer page, lags the statute on rulemaking (read 2026-11-27) |
| [PIPEDA, Justice Laws Website][pipeda] | ss. 4, 10.1, 10.3, 28; Schedule 1 clauses 4.1.3, 4.5.3, 4.9 (read 2026-11-27) |
| [OPC annual report 2024-2025][opc-ar] | C-27 status (read 2026-11-27) |
| LégisQuébec P-39.1, CAI, parl.ca LEGISinfo C-27, cppa.ca.gov | Unreadable on 2026-11-27 (502, 429, 403, 403); plain text, not linked |

[gdpr]: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679
[ukgdpr]: https://www.legislation.gov.uk/eur/2016/679/contents
[duaa]: https://www.legislation.gov.uk/ukpga/2025/18/contents
[ccpa-stat]: https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?lawCode=CIV&division=3.&title=1.81.5.&part=4.&chapter=&article=
[oag]: https://www.oag.ca.gov/privacy/ccpa
[pipeda]: https://laws-lois.justice.gc.ca/eng/acts/P-8.6/FullText.html
[opc-ar]: https://www.priv.gc.ca/en/opc-actions-and-decisions/ar_index/202425/ar_202425/
