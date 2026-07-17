// batch-sources.workflow.js — Workflow-tool script for the `adding-research-source` skill.
// Parallel first-party research + adversarial verify across N new sources, so the main
// session can then write/place/ship each per SKILL.md steps 3-6.
//
// Invoke via the Workflow tool with args = array of URL strings (or {url, hint} objects).
// Requires explicit user opt-in (spawns many agents). Returns verified findings.

export const meta = {
  name: 'batch-sources',
  description: 'Parallel first-party research + adversarial verify for N new sources → structured, placement-tagged findings',
  phases: [{ title: 'Research', detail: 'one first-party research agent per source' },
           { title: 'Verify', detail: 'adversarially re-check the riskiest claims (license/counts/version)' }],
}

const urls = (Array.isArray(args) ? args : (args && args.urls) || [])
  .map(u => (typeof u === 'string' ? { url: u } : u))
  .filter(u => u && u.url)

if (!urls.length) { log('No URLs in args — pass args: ["https://…", …]'); return [] }
log(`Researching ${urls.length} source(s) first-party, then verifying.`)

const FINDING = {
  type: 'object',
  properties: {
    name: { type: 'string' }, what: { type: 'string' },
    license: { type: 'string' }, version: { type: 'string' },
    facts: { type: 'array', items: { type: 'string' } },
    placement: { type: 'string', description: 'cc-native|cc-community|non-cc|sdlc-lcm + subdir + new-vs-extend' },
    existing_coverage: { type: 'string' }, dup_risk: { type: 'boolean' },
    unverifiable: { type: 'array', items: { type: 'string' } },
  },
  required: ['name', 'what', 'placement'],
}
const VERDICT = {
  type: 'object',
  properties: { holds: { type: 'boolean' }, corrections: { type: 'string' } },
  required: ['holds'],
}

// pipeline: each source flows research → verify independently (no barrier).
const findings = await pipeline(
  urls,
  (u) => agent(
    `Read-only FIRST-PARTY research on ${u.url}${u.hint ? ` (hint: ${u.hint})` : ''} for the ai-agents-research corpus. `
    + `Return: canonical name; what it is (1-2 lines); LICENSE from the LICENSE file (not marketing); version/stars/date; `
    + `5-7 concrete first-party facts; a placement recommendation (cc-native / cc-community / non-cc / sdlc-lcm + subdir + new-vs-extend, `
    + `per the skill's decision tree); an existing-coverage note (git grep the repo's docs/); and list any claim you could NOT source first-party. `
    + `Verify counts/license/version against the upstream README/LICENSE/releases. Do not fabricate.`,
    { label: `research:${u.url}`, phase: 'Research', schema: FINDING }),
  (f, u) => f
    ? agent(
        `Adversarially verify the 2 riskiest claims in this finding (especially LICENSE, counts, and version) by re-fetching first-party. `
        + `Set holds=false with corrections if any is unsupported.\n\n${JSON.stringify(f)}`,
        { label: `verify:${f.name}`, phase: 'Verify', schema: VERDICT })
        .then(v => ({ ...f, url: u.url, verified: v }))
    : null,
)

const ok = findings.filter(Boolean)
log(`Done: ${ok.length}/${urls.length} researched; ${ok.filter(f => f.verified && !f.verified.holds).length} had claims corrected on verify.`)
return ok
