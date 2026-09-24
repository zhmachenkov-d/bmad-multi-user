# Analysis Report: /workspaces/bmad-multi-user/skills/team-claim

Generated: 2026-09-24T17:48:00Z · Schema: 2

**Grade: Fair**

> Lean soft-ownership board with solid claims.py; two highs — builder .memlog.md at root and on_complete underwired beyond interactive Claim.

team-claim matches sibling soft-skill shape: claims.py owns claim/release/check/list, SKILL.md judges intent and soft UX, customize.toml is universal-only. Ship polish: wire on_complete on every terminal, trim headless JSON ceremony and vague soft-offer check, and accept (or exclude) builder .memlog.md like siblings.

| Severity | Count |
| --- | --- |
| Critical | 0 |
| High | 2 |
| Medium | 3 |
| Low | 1 |

## Themes

### 1. Terminal-hook and headless contract gaps

- Root cause: on_complete and headless envelopes are documented for Claim interactive/success paths but not uniformly for Release, Check/list, blocked exits, and list intent — automators and overrides get silent no-ops.
- Fix: One terminal rule: after every Claim/Release/Check/list exit (interactive+headless, complete+blocked), run on_complete if set; replace JSON fences with a compact key contract plus list/blocked envelopes.
- Findings:
  - `customization-1` on_complete only on interactive Claim — `SKILL.md:Claim; Release; Check / list`
  - `enhancement-2` add missing headless envelopes for list and non-claim failures — `SKILL.md:Release; SKILL.md:Check / list`
  - `leanness-1` Headless JSON examples are format ceremony — `SKILL.md:Claim/Release/Check headless blocks`

### 2. Builder memlog vs path-standards

- Root cause: Builder process memory lives at skill root as .memlog.md; scanner allows only SKILL.md there — same accepted pattern as team-ready/team-gates/team-status.
- Fix: Leave .memlog.md in place for resume; clear the fail only if ship lint requires excluding it from the root-*.md check or packaged contents.
- Findings:
  - `architecture-1` Prompt file at skill root: .memlog.md — `.memlog.md`

### 3. Vague soft-offer and soft restatement

- Root cause: Soft-offer check after claim is gated by 'when useful'; soft/don't-block is restated after Overview already set the bar.
- Fix: Remove soft-offer check (or pin to claimed|takeover only with headless soft_offer); drop soft restatements.
- Findings:
  - `enhancement-1` remove or pin vague soft-offer check after claim — `SKILL.md:Claim`
  - `leanness-2` Soft/don't-block editing restated after Overview bar — `SKILL.md:Claim interactive; Check bullets`

## Strengths

- Deterministic claim/release/check/list via claims.py with conflict/--force/takeover
- Soft-only bar in Overview; headless conflict → blocked without inventing ownership
- customize.toml sole mechanism, universal defaults only
- Tokens 1143 under budget; integrity + scripts clean; simple-workflow topology
- Smoke-tested against real planning brief path

## Recommendations

1. Wire {workflow.on_complete} after every terminal Claim/Release/Check/list (interactive+headless); add list + blocked envelopes; compact headless key contract (resolves: customization-1, enhancement-2, leanness-1)
2. Remove vague soft-offer check (or pin claimed|takeover + soft_offer) and soft restatements (resolves: enhancement-1, leanness-2)
3. Accept or exclude builder .memlog.md from path-standards like siblings (resolves: architecture-1)

## Experience

- **Headless claim free** — target+actor → claims.py claim → complete JSON with action claimed
- **Headless claim conflict** — other actor holds target → blocked JSON conflict true; --force → takeover
- **Interactive release stale** — anyone release → claim removed; no actor match required
- Headless: Claim/release/check work when paths explicit; list and some blocked envelopes underspecified; on_complete may no-op outside interactive Claim.

## Findings

### High (2)

#### architecture-1 — Prompt file at skill root: .memlog.md

- Lens: architecture
- Location: `.memlog.md`
- Evidence: path-standards reports high: .memlog.md at skill root (only SKILL.md allowed). Same builder process-memory convention as team-ready/team-gates/team-status; not workflow content, but scanner still fails.
- Recommendation: Keep as builder memlog beside SKILL.md (do not move to references/). Clear path-standards fail by excluding .memlog.md from root-*.md check or packaged contents if ship lint must be green.

#### customization-1 — on_complete only on interactive Claim

- Lens: customization
- Location: `SKILL.md:Claim; Release; Check / list`
- Evidence: customize.toml exposes on_complete. SKILL.md runs {workflow.on_complete} only in Claim Interactive; Release, Check/list, and headless Claim never reference it — override silently no-ops.
- Recommendation: After every successful and blocked-as-terminal Claim/Release/Check/list exit—interactive and headless—run {workflow.on_complete} if non-empty.

### Medium (3)

#### leanness-1 — Headless JSON examples are format ceremony

- Lens: leanness
- Location: `SKILL.md:Claim/Release/Check headless blocks`
- Evidence: Three near-identical full JSON envelopes with empty claim: {} placeholders. Script JSON already carries action/claim/conflict; skill only adds status/intent/memlog wrapping.
- Recommendation: Replace JSON fences with one headless envelope contract naming required keys and blocked-vs-complete rules; keep script output as field source.
- Proposed smallest: Headless: emit {status: complete|blocked, intent, target, memlog} plus script fields (action/claim/conflict/released/claimed/reason as applicable). Conflict without --force → blocked; do not invent ownership.
- Predicted delta: Likely nothing material if consumers read keys not formatting; route to variant eval to confirm.

#### enhancement-1 — remove or pin vague soft-offer check after claim

- Lens: enhancement
- Location: `SKILL.md:Claim`
- Evidence: Soft-offer check after successful claim gated only by 'only when useful'; headless success has no soft_offer. Successful claim JSON already confirms the write.
- Recommendation: Remove soft-offer check, or pin to action claimed|takeover only with headless soft_offer: check; omit on already and conflict-blocked.

#### enhancement-2 — add missing headless envelopes for list and non-claim failures

- Lens: enhancement
- Location: `SKILL.md:Release; SKILL.md:Check / list`
- Evidence: list is a first-class intent but only check headless success is documented; Release/check omit blocked envelopes that siblings provide per intent.
- Recommendation: Add headless complete for list; add blocked JSON for release and check/list script-or-path failures with matching intent.

### Low (1)

#### leanness-2 — Soft/don't-block editing restated after Overview bar

- Lens: leanness
- Location: `SKILL.md:Claim interactive; Check bullets`
- Evidence: Overview already sets soft-only bar; Claim/Check repeat do-not-hard-block and soft-offer-check-when-useful.
- Recommendation: Drop soft restatements and vague soft-offer-check line; keep conflict/--force/no-silent-overwrite and on_complete where they add non-obvious failure modes.
