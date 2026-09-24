---
title: Input reconciliation — research digest vs PRD
created: 2026-09-24
status: draft
purpose: BMAD PRD Finalize — gap scan for positioning, borrowed patterns, risks
inputs:
  - research-digest.md
  - prd.md
---

# Input reconciliation: research digest → PRD

## Summary

The PRD **aligns** with research on wedge (BMAD-fluent module, no core fork, git-native, refuse SaaS/cursors/ACL, dependency/layer gates, correct-course coherence) and **explicitly rejects** cloning Spec Kit / AI-DLC. Gaps are mostly **missing narrative and traceability**: competitive positioning is one non-goal line vs research’s comparables table and AI-DLC deep dive; **borrowable patterns** from AI-DLC are only partially reflected in FRs without a “what we took / what we deferred” map; **landscape risks and research confidence caveats** are not carried into PRD assumptions, open questions, or a risk register. One **intentional tension** (native BMAD status vs research “draft→review→ready” opportunity) is resolved in the PRD but not documented as a reconciliation decision.

---

## 1. Positioning vs AI-DLC / Spec Kit

### Research says

| Comparable | Role in landscape |
| ---------- | ----------------- |
| **GitHub Spec Kit** | Hot adjacent: spec→plan→tasks→implement for agents; collab = branches/PRs; not multi-role BMAD layers, readiness, correct-course |
| **OpenSpec (+ Stores)** | Per-change folder isolation; light on PRD/UX/Arch ready → story gates |
| **AWS AI-DLC Workflows** | Closest **mechanical** analogue: multi-human Construction (Unit DAG, claims, pin→gate→land); **peer full engine**, not BMAD add-on; overlap is **pattern-level**, not artifact vocabulary (PRD/UX/Arch/sprint-status/correct-course) |
| **BMAD core** | One owner / one writer; Party Mode ≠ multi-human file coordination |

Research **positioning implication**: AI-DLC proves demand for git-native multi-human coordination inside an AI methodology; blind wholesale copy of Construction fan-out would overbuild v1 and diverge from “complementary module without patching core.”

### PRD says

- Vision: installable complementary module; BMAD artifact language; refuses cursors/SaaS/ACL.
- **§5 Non-Goals:** “Becoming a generic Spec Kit / AI-DLC clone (different methodology); pattern borrowing is fine, product identity remains BMAD-fluent.”
- **§6.2 MVP Out of Scope:** “Multi-repo / sibling-repo orchestration (AI-DLC-style) — not required for v1 Pilot Team single-repo model.”

### Gaps

1. **No stakeholder-facing competitive frame** — Research comparables table and AI-DLC “peer methodology vs pattern borrow” story are absent from PRD (Vision/§0/appendix). Finalize may need a short **Landscape & differentiation** subsection so Architecture/Epics don’t re-litigate Spec Kit vs AI-DLC vs this module.
2. **Spec Kit / OpenSpec wedge under-specified** — PRD does not state that adjacent SDD tools solve **agent lifecycle + branch isolation**, not **BMAD layer readiness + correct-course impact + sprint-status truth**. Research’s one-line gaps per comparable are not mirrored.
3. **AI-DLC scope boundary** — Research distinguishes Inception/planning lifecycle vs Construction multi-team; PRD only excludes “multi-repo AI-DLC-style.” It does **not** document that v1 targets **planning artifact + story gates** (brief-aligned), not AI-DLC’s 33-stage / 14-agent engine — leaving room for scope creep toward “mini AI-DLC.”
4. **Community fork signal** — Research cites jschulte/BMAD-METHOD PR (story locking / PRD crowdsourcing via Issues) as enterprise-ish **core fork** pressure. PRD SM-4 covers “must not patch core” but does not mention this alternative path for buyers comparing options.

### Alignments (no gap)

- Refusal of SaaS, real-time cursors, enterprise ACL as collab model (Vision + Non-Goals).
- Single-repo pilot vs AI-DLC spaces/intents multi-repo (MVP out of scope).
- Product identity = BMAD-fluent, not generic SDD markdown.

---

## 2. Borrowed patterns (research → PRD traceability)

### Research borrowables (explicit “PRD concern scan”, not FRs yet)

| Pattern | Research intent |
| ------- | ---------------- |
| Per-user **gitignored cursors** (active-space / active-intent) | Avoid teammates fighting over shared cursor files; shared state commits |
| **Claim-bound work** | Exactly one concurrent claimant; CAS/handoff |
| **DAG-gated start** | Units/stories blocked until `depends_on` satisfied |
| **Integration-lead merge gate** | pin → merge gate → land; teams never race-push main |
| **Refuse silent same-file merge** | If merge result ≠ pinned/reviewed candidate, reject |

Research also notes useful **isolation** patterns (OpenSpec per-change folders, fragment paths) for hot shared files.

### PRD mapping

| Pattern | PRD coverage | Gap |
| ------- | ------------ | --- |
| Claim-bound work | FR-2 soft claim + warn; v1 no hard lock | **Weaker than AI-DLC CAS**; no handoff/adopt/tombstone semantics |
| DAG-gated start | FR-5, FR-6 story dependencies + Hard Block | **Aligned** for story-level DAG |
| Layer ordering | FR-7, FR-8 | **Aligned** (BMAD-specific extension) |
| DAG for planning artifacts | FR-5 includes Planning Artifacts in deps | **Partial** — no Unit/workshop-scale Construction fan-out |
| Per-user gitignored cursors | — | **Not in PRD** — no convention for local “active story/intent” files |
| pin → gate → land / integration lead | — | **Not in PRD** — merge discipline left to git + structure (FR-1) |
| Refuse silent merge ≠ candidate | §5 deferred “Smart merge assist”; §6.2 out of scope | **Explicit deferral** — research flags as anti-pattern; PRD acknowledges direction but no v1 mitigation beyond ownership/structure |
| Per-change folder isolation | FR-1 conventions mention layout + high-churn files | **Not explicit** OpenSpec-style per-change dirs; worth naming in conventions doc, not FR gap if F1 is sufficient |

### Gaps

1. **No borrowables decision log** — Finalize should record **adopt / adapt / defer** for each research-listed pattern so Build doesn’t implement AI-DLC semantics by accident.
2. **Merge trust model missing** — Research’s serialized main integration is the main answer to “hot shared YAML/markdown”; PRD relies on F1 structure + deferred smart merge — **risk accepted but not cross-referenced** to research (see §3).
3. **Soft claim vs research “exactly one claimant”** — Intentional v1 downgrade; reconciliation should flag **pilot exit criterion** (already partially in §6.2 hard locks deferred) tied to claim collision rate.

---

## 3. Risks and anti-patterns

### Research risks / anti-patterns

- Forking/patching core BMAD
- SaaS / real-time cursors / enterprise ACL as collab model
- **Over-process gates** heavier than pilot ROI (DoR theater)
- **Conflating multi-agent isolation with multi-human project truth**
- **Blind ours/theirs merges** on AI markdown / YAML status
- Confidence: **50–60% merge/drift anecdote** until measured; little public data on multi-role `_bmad-output` co-authoring; no AI-DLC vs BMAD field comparisons

### PRD coverage

| Risk | In PRD? |
| ---- | ------- |
| Core fork/patch | SM-4, NFR-1, Non-Goals, FR-11 |
| SaaS/cursors/ACL | Vision, Non-Goals, NFR-4 |
| Over-process / ceremony | SM-C1, NFR-3 (qualitative fast preflight) |
| Multi-agent vs multi-human | **Missing** |
| Blind merges on shared artifacts | Non-Goal defer smart merge; F1 reduce collisions |
| Anecdote baseline for SM-1 | **SM-1 uses 50–60%** without Assumptions Index tag or measurement plan |
| Research blind spots | **§8 Open Questions cleared** — residual research uncertainty not captured |

### Gaps

1. **No PRD risk register** — Research anti-patterns #4–#5 should appear as **explicit out-of-scope behaviors** or **pilot watch items** (e.g. “Module must not market Party Mode as multi-user coordination”).
2. **SM-1 baseline provenance** — Treat ~50–60% as **assumption from research (medium confidence)**; add assumption or open question on how Pilot Team will measure “merge conflicts and drift cleanup” time.
3. **Gate theater** — Research warns informal DoR failure modes; PRD Hard Blocks (FR-6) increase theater risk if dependencies are boilerplate. SM-C1 helps but no FR on **minimal dependency declaration** or pilot review of gate signal-to-noise.
4. **Status source of truth** — Research: contested Linear/Jira vs markdown vs dual-write. PRD is git-native BMAD status-only; **gap** if Pilot Team uses external boards — no NFR on “module remains authoritative for gates despite Jira display.”

---

## 4. Resolved tensions (research opportunity vs PRD choice)

| Research opportunity | PRD resolution | Reconciliation note |
| -------------------- | -------------- | ------------------- |
| Multi-role **draft→review→ready** visibility on planning artifacts | Use **native BMAD Artifact Lifecycle Status** only; Non-Goal forbids parallel `draft\|review\|ready` enum | **Correct product choice** — document in Finalize so research §Opportunity #1 is not re-opened as missing FR |
| Enforcement vs convention-only SDD | Hard Block on Build (FR-6), soft claims (FR-2) | **Aligned** with research opportunity #5 |
| Correct-course impact + status recompute | FR-9, FR-10 | **Aligned** with research readiness & course-correction patterns |

---

## 5. Recommended PRD Finalize actions (concise)

1. Add **Landscape & differentiation** (½–1 page): Spec Kit / OpenSpec / AI-DLC / core BMAD — what we solve vs pattern we borrow; cite non-goals.
2. Add **Pattern adoption table** (borrowables §2 above) with adopt/adapt/defer + owner (F1 doc vs post-v1).
3. Extend **Assumptions or Open Questions**: SM-1 measurement; optional external board vs git-native gate truth; research confidence on baseline%.
4. Add **Risk / watch list** (3–5 bullets): multi-agent conflation, merge theater, hot-file merges until smart-merge, over-build toward AI-DLC engine.
5. Optional: mention **community core-fork alternatives** (Issues/crowdsourcing) as competitive context for SM-4 narrative.

---

## 6. Input checklist for Finalize gate

| Input | Reconciled? | Notes |
| ----- | ----------- | ----- |
| research-digest.md | Partial | Substance reflected in features; narrative, traceability, and residual risks gaps |
| prd.md | Current draft | Ready for Finalize patches per §5 |
