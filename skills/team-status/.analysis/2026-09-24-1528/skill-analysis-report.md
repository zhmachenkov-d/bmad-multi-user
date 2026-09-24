# Analysis Report: /workspaces/bmad-multi-user/skills/team-status

Generated: 2026-09-24T15:30:00Z · Schema: 2

**Grade: Poor**

> Critical soft_offer reason-string bug mis-targets depends_on-undefined; otherwise lean simple-workflow board with medium ceremony in Ready.

team-status correctly pushes ready/explain plumbing into status.py and wires customize.toml like its siblings. The ship blocker is soft_offer_for_check classifying English gate reasons—depends_on 'X' has no gate definition routes soft_offer_story to the checked story instead of X. Secondary: Ready restates script filters, read-only vs mkdir tension, and under-surfaced soft_offers on all-blocked.

| Severity | Count |
| --- | --- |
| Critical | 1 |
| High | 1 |
| Medium | 5 |
| Low | 2 |

## Themes

### 1. Soft-offer intelligence leak

- Root cause: status.py maps handoffs by English substrings from gates.py reasons; order shadows depends_on-undefined onto the wrong story.
- Fix: Emit stable reason codes from team-gates (or shared mapper) and map codes→soft_offer; add a unit test for depends_on undefined.
- Findings:
  - `determinism-1` soft_offer classifies English reason substrings — `scripts/status.py:soft_offer_for_check`

### 2. Ready ceremony vs script truth

- Root cause: SKILL.md re-teaches filters and presentation the script already owns, while under-using script soft_offers on all-blocked.
- Fix: Trust script cohorts/soft_offers; trim Ready bullets and interactive script; always surface soft_offer when present.
- Findings:
  - `leanness-1` Ready bullets re-teach script filters — `SKILL.md:Ready (interpret list)`
  - `leanness-2` Interactive Ready is presentation script — `SKILL.md:Ready (Interactive paragraph)`
  - `leanness-3` Explain restates script soft_offer table — `SKILL.md:Explain (ready true/false bullets)`
  - `enhancement-1` Add: surface script soft_offer on all-blocked Ready — `SKILL.md:Ready interactive`

### 3. Principle / entry polish

- Root cause: Read-only bar conflicts with mkdir; unfinished invite fires before sprint exists; builder memlog sits at skill root.
- Fix: Narrow read-only to no gate/sprint mutations; invite unfinished only when sprint exists; leave/gitignore builder .memlog.md like siblings.
- Findings:
  - `architecture-1` Builder memlog at skill root — `skills/team-status/.memlog.md`
  - `architecture-2` Read-only bar vs mkdir on activation — `SKILL.md:Overview vs On Activation step 3`
  - `enhancement-2` Opportunity: condition unfinished invite on sprint-status — `SKILL.md:On Activation step 4–5`
  - `enhancement-3` Opportunity: add soft-gate after Ready board — `SKILL.md:Ready interactive close`

## Strengths

- Deterministic ready/explain via status.py + sibling gates import
- Headless JSON contracts for ready and explain
- customize.toml sole mechanism, correctly wired
- Empty fleet ≠ ready; unfinished is runtime flag not setup config
- Tokens 1182 well under budget

## Recommendations

1. Fix soft_offer_for_check: reason codes or ordered depends_on checks before generic 'no gate definition'; unit-test depends_on undefined → soft_offer_story=dep (resolves: determinism-1)
2. Trim Ready interpret/interactive ceremony; always present script soft_offer including all-blocked (resolves: leanness-1, leanness-2, leanness-3, enhancement-1)
3. Clarify read-only vs mkdir; condition unfinished invite on sprint-status; optional soft-gate after board (resolves: architecture-2, enhancement-2, enhancement-3)

## Experience

- **Headless ready** — explicit ready → status.py ready → JSON with ready/blocked/soft_offer
- **Headless explain** — story id → status.py explain → reasons + soft_offer (bug on depends_on undefined)
- **Interactive all-blocked** — board shows blocked; soft_offer under-surfaced today
- Headless: Ready when paths explicit; soft_offer bug can mis-route automators on depends_on-undefined.

## Findings

### Critical (1)

#### determinism-1 — soft_offer classifies English reason substrings

- Lens: determinism
- Location: `scripts/status.py:soft_offer_for_check`
- Evidence: Substring rules infer handoff from gates.py phrasing. Order makes depends_on '{dep}' has no gate definition match 'no gate definition' first and set soft_offer_story to the checked story; the depends_on-define branch is unreachable for that shape.
- Recommendation: Emit stable reason codes from team-gates (or shared mapping) and map codes→soft_offer; unit-test depends_on undefined.

### High (1)

#### architecture-1 — Builder memlog at skill root

- Lens: architecture
- Location: `skills/team-status/.memlog.md`
- Evidence: Path-standards flags .memlog.md at skill root. Same as team-ready/team-gates builder process memory pattern.
- Recommendation: Keep builder memlog out of shipped tree (gitignore) or accept sibling convention; runtime memlog stays at planning_artifacts/team/.

### Medium (5)

#### leanness-1 — Ready bullets re-teach script filters

- Lens: leanness
- Location: `SKILL.md:Ready (interpret list)`
- Evidence: Bullets redefine ready/blocked/unfinished semantics status.py already applied after 'trust script JSON'.
- Recommendation: Keep empty_fleet why, do-not-flatten blocked, sprint_warning; drop semantic redefinitions.

#### leanness-2 — Interactive Ready is presentation script

- Lens: leanness
- Location: `SKILL.md:Ready (Interactive paragraph)`
- Evidence: Prescribes cohort order and soft-offer already in script JSON.
- Recommendation: One goal: present script cohorts/soft_offers without inventing greens; offer explain on blocked.
- Proposed smallest: Interactive: present the script's ready/blocked/(optional unfinished) and its soft_offers without inventing greens; offer explain for blocked. Run {workflow.on_complete} if non-empty.
- Predicted delta: Loss of forced ordering and one-line-reason formatting only. Route to variant eval to confirm.

#### architecture-2 — Read-only bar vs mkdir on activation

- Lens: architecture
- Location: `SKILL.md:Overview vs On Activation step 3`
- Evidence: Overview says read-only; activation mkdir team/ if needed.
- Recommendation: Narrow bar to no gate/sprint mutations, or drop mkdir and treat missing team as empty fleet.

#### enhancement-1 — Add: surface script soft_offer on all-blocked Ready

- Lens: enhancement
- Location: `SKILL.md:Ready interactive`
- Evidence: Interactive Ready under-uses script soft_offer when ready=[] and blocked nonempty.
- Recommendation: Always surface soft_offer fields from script JSON when present.

#### enhancement-2 — Opportunity: condition unfinished invite on sprint-status

- Lens: enhancement
- Location: `SKILL.md:On Activation step 4–5`
- Evidence: Open-floor may ask unfinished before sprint resolves; empty unfinished underwhelms.
- Recommendation: Invite unfinished only after sprint-status exists.

### Low (2)

#### leanness-3 — Explain restates script soft_offer table

- Lens: leanness
- Location: `SKILL.md:Explain (ready true/false bullets)`
- Evidence: Enumerates soft_offer targets already in script JSON.
- Recommendation: Keep list reasons + apply script soft_offer; drop enumeration.

#### enhancement-3 — Opportunity: add soft-gate after Ready board

- Lens: enhancement
- Location: `SKILL.md:Ready interactive close`
- Evidence: No soft pivot to unfinished/explain after explicit team-status.
- Recommendation: One soft-gate after board, then stop.
