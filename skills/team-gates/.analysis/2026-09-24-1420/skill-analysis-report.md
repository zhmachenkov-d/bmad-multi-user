# Analysis Report: /workspaces/bmad-multi-user/skills/team-gates

Generated: 2026-09-24 · Schema: 2

**Grade: Fair**

> Solid soft-gate foundation (scripts own plumbing); two highs — incomplete check soft-offers/headless envelopes, and scanner flag on builder .memlog.md at root.

team-gates is a lean multi-intent workflow with the right determinism split: gates.py owns check/define/order plumbing, the prompt owns confirmation and explaining blockers. Customization is correctly wired. The main ship-gap is incomplete soft-offer and blocked JSON contracts on check/define/order versus the headless bar set by team-ready; Define's numbered CLI list is a false sequence.

| Severity | Count |
| --- | --- |
| Critical | 0 |
| High | 2 |
| Medium | 3 |
| Low | 0 |

## Themes

### 1. Uneven soft-offer / headless envelope

- Root cause: Check soft-offers team-ready for artifact blockers but not define when undefined; headless success/blocked shapes are incomplete for define/order and omit soft_offer — automators and team-status lack a next step.
- Fix: Mirror team-ready: soft-offer define on undefined check; emit soft_offer on headless check when applicable; add blocked JSON templates for define and order failures.
- Findings:
  - `enhancement-1` Add soft-offer define on undefined check — `SKILL.md:Check`
  - `enhancement-2` Add soft_offer on check headless JSON — `SKILL.md:Check (headless success)`
  - `enhancement-3` Add blocked JSON for define and order failures — `SKILL.md:Define / view; SKILL.md:Order`

### 2. Define false sequence

- Root cause: Independent gates.py writes are numbered 1–3, so the model may march through the full pipeline instead of writing only confirmed fields.
- Fix: Replace the numbered Define list with one goal sentence plus bullet CLI shapes.
- Findings:
  - `leanness-1` Define CLI steps numbered as false sequence — `SKILL.md:Define / view`

### 3. Builder memlog vs path scanner

- Root cause: Workflow-builder keeps process .memlog.md at skill root for resume; path-standards flags it as prompt-at-root — same known conflict as team-ready.
- Fix: Leave .memlog.md at root (builder process memory). Do not move into the shipped skill package narrative; long-term exclude .memlog.md from the path scanner.
- Findings:
  - `architecture-1` Prompt markdown at skill root — `skills/team-gates/.memlog.md`

## Strengths

- Overview states stance, outcome, consumer, and bar including undefined ≠ pass and soft-only.
- Determinism split is correct: gates.py owns get/list/set/check/order and frontmatter status; prompt keeps judgment.
- customize.toml universal defaults only; SKILL.md resolves and reads {workflow.*} including on_complete.
- Interactive + headless paths exist for all three intents; soft-offer team-ready on artifact blockers.

## Recommendations

1. On undefined check soft-offer define (interactive + soft_offer in headless); when artifact status blocks, add soft_offer: team-ready to headless check JSON; add blocked envelopes for define and order. (resolves: enhancement-1, enhancement-2, enhancement-3)
2. Un-number Define CLI steps into one goal + bullets. (resolves: leanness-1)
3. Keep .memlog.md at skill root (builder resume); treat architecture-1 as known scanner conflict, same as team-ready. (resolves: architecture-1)

## Experience

- **Developer checks a story before build** — Activates check with story id → script JSON → pass or reasons; may be offered team-ready or define.
- **PM defines gates for an epic** — Define artifact map + story requires/layer/depends_on → gates.json updated → view confirms.
- **Headless team-status consumer** — Calls check headless → expects pass/undefined/reasons plus soft_offer and blocked shapes.
- Headless: Partially ready: check has success+blocked; define/order need blocked templates and soft_offer parity with team-ready.

## Findings

### High (2)

#### architecture-1 — Prompt markdown at skill root

- Lens: architecture
- Location: `skills/team-gates/.memlog.md`
- Evidence: Skill root contains `.memlog.md` (builder process memory). Path conventions forbid workflow/prompt `.md` at skill root; only SKILL.md belongs there. Runtime memlog is correctly targeted at `{planning_artifacts}/team/.memlog.md`.
- Recommendation: Leave at root for builder resume (same as team-ready). Long-term: exclude `.memlog.md` from path-standards scanner.

#### enhancement-1 — Add soft-offer define on undefined check

- Lens: enhancement
- Location: `SKILL.md:Check`
- Evidence: Soft-offer is applied only for artifact-status blockers (`team-ready`). When `undefined: true`, the skill stops at not-ready with no invite to define — common after 'check gates' on an undeclared story.
- Recommendation: Interactive: soft-offer define when `undefined: true`. Headless: include `soft_offer: "define"` on the check envelope when applicable.

### Medium (3)

#### leanness-1 — Define CLI steps numbered as false sequence

- Lens: leanness
- Location: `SKILL.md:Define / view`
- Evidence: Test 3 / canon 'number only true sequences': after 'write only what the user confirmed', three independent gates.py writes (set-artifacts, optional set-layers, set) are numbered 1–3. Script actions are separate; order is not a failure guard. Numbering reads as a mandatory march through the full pipeline.
- Recommendation: Replace the numbered list with one goal: write only confirmed gate fields via gates.py. List the three CLI shapes as bullets (or a compact reference), not an ordered recipe.

#### enhancement-2 — Add soft_offer on check headless JSON

- Lens: enhancement
- Location: `SKILL.md:Check (headless success)`
- Evidence: Interactive check soft-offers `team-ready`, but headless success schema is only status/intent/result/memlog. Sibling team-ready already surfaces soft_offer in headless JSON.
- Recommendation: When check would soft-offer team-ready or define, emit soft_offer on the headless envelope; omit when none applies.

#### enhancement-3 — Add blocked JSON for define and order failures

- Lens: enhancement
- Location: `SKILL.md:Define / view; SKILL.md:Order`
- Evidence: Check documents a full blocked envelope. Define only says 'blocked JSON' in prose; Order has success only — underspecified headless runs lack a usable return shape.
- Recommendation: Add the same blocked envelope templates for define and order script/path failures.
