# Analysis Report: /workspaces/bmad-multi-user/skills/team-ready

Generated: 2026-09-24T13:42:45Z · Schema: 2

**Grade: Good**

> Stable good: zero highs; remaining mediums are polish (drop Constraints ceremony, open-floor, script-failure stop).

Third analyze: prior headless/Overview highs stay cleared. Architecture, determinism, and customization remain clean. Leftover work is density and graceful failure—not structural risk. Ship-ready with optional polish.

| Severity | Count |
| --- | --- |
| Critical | 0 |
| High | 0 |
| Medium | 3 |
| Low | 2 |

## Themes

### 1. Ceremony left in Constraints

- Root cause: Constraints duplicates Overview/Propose after remediations.
- Fix: Fold no-hard-locks into Overview; delete Constraints; light failure-framing.
- Findings:
  - `leanness-1` Constraints section is restatement ceremony — `SKILL.md:Constraints`
  - `leanness-2` Stacked Never without failure why — `SKILL.md`

### 2. Graceful entry and script failure

- Root cause: Happy-path headless is solid; vague entry and script errors need one more rule each.
- Fix: Open-floor when vague; blocked on script failure; fence blocked JSON.
- Findings:
  - `enhancement-1` Open-floor when underspecified — `SKILL.md:On Activation`
  - `enhancement-2` Script/path failure → stop or blocked — `SKILL.md:Set`
  - `enhancement-3` Document headless blocked JSON — `SKILL.md:Set`

## Strengths

- Zero high/critical after remediations
- Headless set/propose contracts + multi-candidate + propose cues in place
- Clean script/prompt boundary and customize.toml wiring
- Integrity Overview pass

## Recommendations

1. Delete Constraints; fold no-hard-locks into Overview; add script-failure blocked + fenced blocked JSON (resolves: leanness-1, enhancement-2, enhancement-3)
2. Optional open-floor when underspecified; reframe Never as failure-why (resolves: enhancement-1, leanness-2)

## Experience

- **Headless set explicit** — path+status → script set → JSON complete (+ soft_offer if PRD ready)
- **Headless propose** — cues → recommendation JSON → separate set to apply
- **Interactive vague** — could use one open-floor dump (optional polish)
- Headless: Ready when inputs explicit; script failure and blocked schema polish remain optional.

## Findings

### Medium (3)

#### leanness-1 — Constraints section is restatement ceremony

- Lens: leanness
- Location: `SKILL.md:Constraints`
- Evidence: Constraints largely repeats Overview/Propose; unique bit is no hard locks.
- Recommendation: Delete Constraints; fold no hard locks into Overview Bar.
- Proposed smallest: Overview Bar includes no hard locks; Propose keeps legacy remap; no Constraints.
- Predicted delta: No material change on set/propose if Overview/Propose carry the rules.

#### enhancement-1 — Open-floor when underspecified

- Lens: enhancement
- Location: `SKILL.md:On Activation`
- Evidence: Vague invoke serializes asks; no single dump invite.
- Recommendation: One adaptive open-floor when intent/target underspecified; skip when explicit.

#### enhancement-2 — Script/path failure → stop or blocked

- Lens: enhancement
- Location: `SKILL.md:Set`
- Evidence: Missing path/status covered; script ok:false / file-not-found after supplied path not.
- Recommendation: On get/set non-ok: interactive stop; headless blocked + reason + memlog.

### Low (2)

#### leanness-2 — Stacked Never without failure why

- Lens: leanness
- Location: `SKILL.md`
- Evidence: Never invent / never silent / do not write shout compliance.
- Recommendation: Reframe each as the failure it guards.

#### enhancement-3 — Document headless blocked JSON

- Lens: enhancement
- Location: `SKILL.md:Set`
- Evidence: complete schemas fenced; blocked is prose-only.
- Recommendation: Add minimal blocked JSON example beside complete schemas.
