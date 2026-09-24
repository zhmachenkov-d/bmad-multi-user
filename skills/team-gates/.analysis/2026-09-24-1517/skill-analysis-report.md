# Analysis Report: /workspaces/bmad-multi-user/skills/team-gates

Generated: 2026-09-24 · Schema: 2

**Grade: Good**

> Core soft-gate contract is shippable; remaining mediums are handoff polish (empty fleet, soft_offer_story, define→check).

Optional polish landed: reason-class soft-offer table and no-story headless envelopes. Leanness, architecture, determinism, and customization pass clean. Three medium enhancement opportunities remain around empty check/order, carrying a target story on soft_offer, and offering check after define. Path-standards still flags builder .memlog.md (leave).

| Severity | Count |
| --- | --- |
| Critical | 0 |
| High | 1 |
| Medium | 3 |
| Low | 0 |

## Themes

### 1. Handoff polish after core contract

- Root cause: Soft-offer matrix covers failing reasons well; empty fleets, missing soft_offer target id, and define→check verify loop are still implicit.
- Fix: Soft-offer define on empty check/order; add soft_offer_story when target known; soft-offer check after successful define.
- Findings:
  - `enhancement-1` opportunity: soft-offer define on empty check/order — `SKILL.md:Check, SKILL.md:Order`
  - `enhancement-2` opportunity: headless soft_offer needs target story — `SKILL.md:Check`
  - `enhancement-3` opportunity: soft-offer check after define success — `SKILL.md:Define / view`

### 2. Builder memlog vs path scanner

- Root cause: Process .memlog.md at skill root flagged by path-standards; not a runtime defect.
- Fix: Leave .memlog.md; long-term exclude from scanner.
- Findings:
  - `architecture-1` Prompt markdown at skill root — `skills/team-gates/.memlog.md`

## Strengths

- Soft-offer table by reason class; with/without --story headless shapes documented.
- Define/check/order blocked envelopes; customize.toml wired; gates.py owns plumbing.
- Leanness under builder budgets (~1588 tokens).

## Recommendations

1. Optional: empty check/order → soft_offer define; soft_offer_story on headless; define success → soft_offer check. (resolves: enhancement-1, enhancement-2, enhancement-3)
2. Keep .memlog.md at skill root (known scanner conflict). (resolves: architecture-1)

## Experience

- **Fresh project check** — check with no gates → should soft-offer define rather than vacuous all_pass.
- **Define then verify** — define story gate → soft-offer check → pass/fail with reasons.
- Headless: Single- and multi-story check contracts ready; soft_offer_story would complete automator handoffs.

## Findings

### High (1)

#### architecture-1 — Prompt markdown at skill root

- Lens: architecture
- Location: `skills/team-gates/.memlog.md`
- Evidence: Path-standards high: `.memlog.md` at skill root (builder process memory). Runtime audit memlog is `{planning_artifacts}/team/.memlog.md`.
- Recommendation: Leave at root (same as team-ready). Long-term exclude from path-standards.

### Medium (3)

#### enhancement-1 — opportunity: soft-offer define on empty check/order

- Lens: enhancement
- Location: `SKILL.md:Check, SKILL.md:Order`
- Evidence: No-story check with zero stories yields results=[] and all_pass true with soft_offer omitted; empty order has no handoff — vacuous green / empty list.
- Recommendation: When results or ordered is empty, soft_offer define; do not treat vacuous all_pass as ready.

#### enhancement-2 — opportunity: headless soft_offer needs target story

- Lens: enhancement
- Location: `SKILL.md:Check`
- Evidence: Table says define/check '(that story)' but headless only exposes soft_offer string — no story id for the handoff target.
- Recommendation: Add soft_offer_story when soft_offer is define/check and a target story is known.

#### enhancement-3 — opportunity: soft-offer check after define success

- Lens: enhancement
- Location: `SKILL.md:Define / view`
- Evidence: Define reports saved gate with no soft_offer; define→check verify loop is implicit.
- Recommendation: After successful define, soft_offer check (interactive + headless).
