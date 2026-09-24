# Analysis Report: /workspaces/bmad-multi-user/skills/team-status

Generated: 2026-09-24T17:35:00Z · Schema: 2

**Grade: Good**

> Prior critical soft_offer bug and Ready ceremony are cleared; remaining high is builder .memlog.md at skill root (sibling convention).

team-status is shippable as a lean readiness board: status.py owns cohorts and soft-offers (depends_on targeting fixed and tested), SKILL.md trusts script JSON, and customize.toml matches siblings. Path-standards still flags builder .memlog.md; one medium soft-gate polish remains around not re-offering unfinished.

| Severity | Count |
| --- | --- |
| Critical | 0 |
| High | 1 |
| Medium | 1 |
| Low | 0 |

## Themes

### 1. Builder memlog vs path-standards

- Root cause: Builder process memory lives at skill root as .memlog.md; scanner allows only SKILL.md there — same accepted pattern as team-ready/team-gates.
- Fix: Leave .memlog.md in place for resume; clear the fail only if ship lint requires excluding it from the root-*.md check or packaged contents.
- Findings:
  - `architecture-1` Prompt file at skill root: .memlog.md — `.memlog.md`

### 2. Soft-gate path awareness

- Root cause: Post-board soft-gate can re-offer unfinished after open-floor already settled it, or pitch unfinished/explain on empty_fleet.
- Fix: Offer unfinished only when sprint exists and not already decided; explain only when blocked; skip soft-gate on empty_fleet.
- Findings:
  - `enhancement-1` Opportunity: path-aware soft-gate (don't re-offer unfinished) — `SKILL.md:Ready interactive`

## Strengths

- Deterministic ready/explain via status.py + sibling gates import
- soft_offer_for_check depends_on-first matching with unit and integration coverage
- Headless JSON contracts; empty fleet ≠ ready
- SKILL trusts script cohorts/soft_offers; unfinished is runtime flag
- customize.toml sole mechanism, universal defaults only
- Tokens 1185 under budget; scripts/integrity clean

## Recommendations

1. Optional: path-aware soft-gate (skip re-offer unfinished; skip on empty_fleet) (resolves: enhancement-1)
2. Accept or exclude builder .memlog.md from path-standards like siblings (resolves: architecture-1)

## Experience

- **Headless ready** — explicit ready → status.py ready → JSON with ready/blocked/soft_offer
- **Headless explain depends_on undefined** — story id → status.py explain → soft_offer_story = dependency
- **Interactive all-blocked** — board shows blocked + script soft_offer; soft-gate may still re-ask unfinished
- Headless: Ready when paths explicit; soft_offer targets deps correctly after the fix.

## Findings

### High (1)

#### architecture-1 — Prompt file at skill root: .memlog.md

- Lens: architecture
- Location: `.memlog.md`
- Evidence: path-standards reports high: .memlog.md sits at skill root (only SKILL.md allowed). Pre-pass: 1 structure finding. Same builder process-memory convention as team-ready/team-gates; not workflow content, but the scanner still fails the skill.
- Recommendation: Keep as builder memlog beside SKILL.md (do not move to references/). Clear the path-standards fail by excluding .memlog.md from the root-*.md check or from packaged skill contents if ship lint must be green.

### Medium (1)

#### enhancement-1 — Opportunity: path-aware soft-gate (don't re-offer unfinished)

- Lens: enhancement
- Location: `SKILL.md:Ready interactive`
- Evidence: Soft-gate elicitation after the board always offers unfinished when sprint exists, but Open-floor opening already invites unfinished on the underspecified path when sprint exists; empty_fleet still gets unfinished/explain while soft_offer is team-gates define.
- Recommendation: One soft-gate: offer unfinished only if sprint exists and unfinished was not already decided (open-floor or --include-unfinished); offer explain only when blocked; else proceed via script soft_offer. Skip soft-gate on empty_fleet.
