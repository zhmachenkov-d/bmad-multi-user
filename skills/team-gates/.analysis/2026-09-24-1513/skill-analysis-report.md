# Analysis Report: /workspaces/bmad-multi-user/skills/team-gates

Generated: 2026-09-24 · Schema: 2

**Grade: Good**

> Upgraded from fair: prior remediations cleared; remaining are known .memlog.md scanner conflict plus two medium soft-offer/headless polish opportunities.

team-gates now has a coherent soft-gate contract: define/check/order share blocked envelopes, check soft-offers define and team-ready with headless soft_offer, and Define is un-numbered. Determinism, customization, and leanness pass clean. Left: path-standards flag on builder .memlog.md (leave), and optional extension of soft-offers / multi-story headless check docs.

| Severity | Count |
| --- | --- |
| Critical | 0 |
| High | 1 |
| Medium | 2 |
| Low | 0 |

## Themes

### 1. Optional soft-offer / multi-story polish

- Root cause: Core soft-offers cover undefined and status blockers; map-missing and depends_on reasons, plus all-stories check without --story, lack the same handoff/docs depth.
- Fix: Optionally map remaining reason classes to soft_offers and document the no-story headless check shape (or require --story headless).
- Findings:
  - `enhancement-1` opportunity: extend check soft-offers past undefined/status — `SKILL.md:Check`
  - `enhancement-2` opportunity: headless check contract for all-stories run — `SKILL.md:Check`

### 2. Builder memlog vs path scanner

- Root cause: Workflow-builder keeps process .memlog.md at skill root; path-standards flags it. Not a runtime defect.
- Fix: Leave .memlog.md at root; long-term exclude from path-standards scanner.
- Findings:
  - `architecture-1` Prompt markdown at skill root — `skills/team-gates/.memlog.md`

## Strengths

- Prior fair findings resolved: soft-offer define/team-ready, soft_offer in headless check, blocked JSON for define/order, Define bullets.
- Determinism split clean; customize.toml wired; leanness under budget (~1426 tokens).
- Overview bar still holds: undefined ≠ pass, soft only, gates.json via script.

## Recommendations

1. Optional polish: extend check soft-offers for map-missing and depends_on; document multi-story headless check or require --story. (resolves: enhancement-1, enhancement-2)
2. Keep .memlog.md at skill root (builder resume); treat architecture-1 as known scanner conflict. (resolves: architecture-1)

## Experience

- **Check undefined story** — check → undefined → soft-offer define → define writes gate → re-check.
- **Headless gate consumer** — check with story id → complete/blocked JSON with optional soft_offer.
- Headless: Ready for single-story check/define/order; multi-story check without --story is the remaining doc gap.

## Findings

### High (1)

#### architecture-1 — Prompt markdown at skill root

- Lens: architecture
- Location: `skills/team-gates/.memlog.md`
- Evidence: Path-standards: Prompt file at skill root `.memlog.md`. Builder process memory for resume; runtime audit memlog is `{planning_artifacts}/team/.memlog.md`.
- Recommendation: Leave at root (same as team-ready). Long-term: exclude `.memlog.md` from path-standards.

### Medium (2)

#### enhancement-1 — opportunity: extend check soft-offers past undefined/status

- Lens: enhancement
- Location: `SKILL.md:Check`
- Evidence: Soft-offer covers undefined → define and status blockers → team-ready. Script reasons also include missing artifact path/map and depends_on undefined/not-pass without a soft_offer.
- Recommendation: Map remaining reason classes to soft_offers (define for map/depends undefined; check for depends not-pass; team-ready for status).

#### enhancement-2 — opportunity: headless check contract for all-stories run

- Lens: enhancement
- Location: `SKILL.md:Check`
- Evidence: Omitting --story returns results/all_pass; headless envelope only documents a single result object.
- Recommendation: Document no-story headless shape or require --story in headless and blocked when absent.
