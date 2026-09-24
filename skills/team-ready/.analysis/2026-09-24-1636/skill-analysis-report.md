# Analysis Report: /workspaces/bmad-multi-user/skills/team-ready

Generated: 2026-09-24T13:38:54Z · Schema: 2

**Grade: Good**

> Upgraded from fair: Overview and headless propose/memlog/soft_offer land; remaining high is incomplete headless set inputs; else low polish.

Re-analyze after rank-1 fixes: architecture, determinism, and customization are clean; integrity Overview passes. One high finding remains—block headless set when path or status is missing. Medium opportunities: propose judgment cues and multi-artifact disambiguation. Path-scan still flags builder .memlog.md (accepted conflict).

| Severity | Count |
| --- | --- |
| Critical | 0 |
| High | 1 |
| Medium | 2 |
| Low | 3 |

## Themes

### 1. Headless incomplete inputs

- Root cause: Interactive Set guards missing path/status; headless does not yet refuse the write.
- Fix: Add blocked JSON when headless set lacks path or status.
- Findings:
  - `enhancement-1` Headless incomplete set → blocked — `SKILL.md:Set`

### 2. Judgment defaults for propose/pick

- Root cause: Propose and artifact identity lack short default rules under ambiguity.
- Fix: Add readiness cues and zero/many candidate rules.
- Findings:
  - `enhancement-2` Propose readiness cues — `SKILL.md:Propose`
  - `enhancement-3` Multi-candidate artifact disambiguation — `SKILL.md:On Activation`

### 3. Residual prose density

- Root cause: Non-write and Constraints still carry light restatement.
- Fix: One-pass trim of Propose/Constraints.
- Findings:
  - `leanness-1` Propose restates non-write three times — `SKILL.md:Propose`
  - `leanness-2` Constraints points at --help — `SKILL.md:Constraints`
  - `leanness-3` Sidecar ban is negative space — `SKILL.md:Constraints`

## Strengths

- ## Overview present; workflow-integrity pass
- Headless propose recommendation-only with memlog; soft_offer on PRD→ready
- Script/prompt intelligence boundary clean; customize.toml right-sized
- Prior fair-grade highs on Overview/headless contracts cleared

## Recommendations

1. Block headless set when path or status missing (resolves: enhancement-1)
2. Add propose cues + multi-candidate pick rules (resolves: enhancement-2, enhancement-3)
3. Trim Propose/Constraints restatements (resolves: leanness-1, leanness-2, leanness-3)

## Experience

- **Interactive set** — Activate → artifact → set via script → soft-offer team-drift if PRD ready
- **Headless propose** — Recommend status JSON only; apply via separate set
- **Headless set** — Needs explicit path+status or should blocked (gap: enhancement-1)
- Headless: Propose and audit trail in place; incomplete set inputs still need an explicit blocked path.

## Findings

### High (1)

#### enhancement-1 — Headless incomplete set → blocked

- Lens: enhancement
- Location: `SKILL.md:Set`
- Evidence: Headless missing path/status can invent a write; no blocked parallel to interactive confirm.
- Recommendation: If headless and path or status missing/ambiguous: do not write; emit blocked + reason + memlog.

### Medium (2)

#### enhancement-2 — Propose readiness cues

- Lens: enhancement
- Location: `SKILL.md:Propose`
- Evidence: No testable judgment rubric for draft/review/ready.
- Recommendation: Add 3–5 one-line cues for consistent proposals.

#### enhancement-3 — Multi-candidate artifact disambiguation

- Lens: enhancement
- Location: `SKILL.md:On Activation`
- Evidence: No rule when zero/many PRD/UX/ARCH candidates.
- Recommendation: Zero/many: ask interactive or blocked headless; never invent active.

### Low (3)

#### leanness-1 — Propose restates non-write three times

- Lens: leanness
- Location: `SKILL.md:Propose`
- Evidence: without writing / never write / apply via separate set.
- Recommendation: Keep one non-write rule; drop redundant phrasing.

#### leanness-2 — Constraints points at --help

- Lens: leanness
- Location: `SKILL.md:Constraints`
- Evidence: --help bullet re-teaches tool fluency.
- Recommendation: Delete the --help bullet.

#### leanness-3 — Sidecar ban is negative space

- Lens: leanness
- Location: `SKILL.md:Constraints`
- Evidence: Sidecar clause restates Overview frontmatter bar.
- Recommendation: Drop sidecar clause.
