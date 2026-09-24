# Input Reconciliation: Product Brief → PRD

**Input:** Product Brief — BMAD Multi-User (`brief-bmad-multi-user-2026-09-24/brief.md`)  
**Compared to:** `prd.md` (no `addendum.md` in workspace)  
**Reconciliation date:** 2026-09-24  
**Purpose:** Finalize gate — trace brief intent into PRD requirements; flag drops, shifts, and intentional overrides.

---

## 1. Brief extract (obligations)

### Executive summary

| Brief claim | PRD anchor |
|-------------|------------|
| Open-source BMAD module for multi-role teams sharing one repo + `_bmad-output` | §1 Vision (installable module); NFR-8 semver OSS releases — **“open-source” lead phrase softened** to ecosystem/complementary framing |
| Wedge = BMAD fluency (PRD, UX, Architecture, epics/stories, sprint status, correct-course), not generic collab markdown | §1 Vision, §5 Non-Goals (generic Spec Kit / AI-DLC clone) |
| Single-driver core BMAD breaks on parallel human roles: collisions, hidden readiness, early cross-layer starts, post–correct-course split truth | §2 JTBD, UJ-1–4, F3–F5 |
| Pilot pain ~50–60% time on merges/drift cleanup | SM-1 (target 15–25%); **problem-section vividness not repeated** in PRD §2 |
| Capabilities: ownership/structure, lifecycle + gates, layer order, correct-course recalc + impact review | F1–F5 |
| Complementary install **without patching core** | FR-11/12, NFR-1, SM-4 |
| Not git replacement or SaaS | §1, §5 Non-Goals |
| v1 success: cut merge/drift toward 15–25% | SM-1 |
| Longer bet: **community standard** for multi-human BMAD collaboration | §1 “**official complementary module**” in BMAD ecosystem — **aligned intent, different positioning word** |

### Problem

| Brief claim | PRD anchor |
|-------------|------------|
| Collisions on specs, `sprint-status.yaml`, `epics.md`, etc. | UJ-3, FR-1, SM-1 |
| No shared signal when PRD / UX / Architecture “done enough” for story start | F2, F3, UJ-4 — **mechanism differs** (see overrides) |
| Cross-layer early implementation → drift/rework | UJ-1, F4, JTBD-1 |
| Correct-course mid-story → docs/status/code diverge after merge | UJ-2, F5, JTBD-2, SM-3 |
| **Who feels it most: developers** (blocked, bad starts, rewrite) | **Not named explicitly**; implied via UJ-1 (Alex), SM-2 |
| Cost ~50–60% merges/drift; manual coordination doesn’t scale | SM-1 baseline only |

### Solution

| Brief claim | PRD anchor |
|-------------|------------|
| Git-native module; parallel work + correct course on shared `_bmad-output` | §1, F1–F6 |
| Outcome: developers build on coherent plan | JTBD-3, UJ-4 |
| Wedge vs **party-mode**, **process-only discipline**, **generic collab-markdown** | Party-mode + generic collab in §1/§5; **process-only discipline alternative dropped** |
| Complements core; does not fork | §1, FR-12, SM-4 |

### Who this serves

| Brief claim | PRD anchor |
|-------------|------------|
| Primary: BMAD multi-role teams, non-trivial project, shared repo/`_bmad-output` | §1, §2 JTBD |
| Not for: solo, no git, enterprise SaaS+ACL | §2.2 Non-Users |
| Secondary: BMAD OSS community wanting multi-human without forking core | **No dedicated secondary-audience section**; folded into ecosystem vision |

### Success criteria

| Brief claim | PRD anchor |
|-------------|------------|
| Time: ~50–60% → ~15–25% | SM-1 |
| Fewer large merges + less rewrite from early starts / inconsistency | SM-2 |
| Docs, status, code align more often than diverge | SM-3 |
| Near-term = pilot team pain drop, not community adoption metrics | SM-5 |
| Failure: must patch/fork core BMAD | SM-4 |

### Scope

| Brief v1 in | PRD |
|-------------|-----|
| Ownership/structure conventions under `_bmad-output` | F1 (FR-1, FR-2) — **soft claim/warn only** |
| Lifecycle `draft` / `review` / `ready` for PRD, UX, Architecture | **Intentional override → F2 native BMAD statuses** (see §3) |
| Per-story dependency gates (artifacts + layers) | F3 (FR-5, FR-6) — **hard block** |
| Layer implementation ordering | F4 |
| Correct-course: status recalculation + impact review before merge | F5 |
| Installable module, real install path, no core patch | F6 |

| Brief out / hard out | PRD |
|----------------------|-----|
| Smart merge assist (later; direction kept) | §5, §6.2 |
| Polished community docs beyond minimal install | §5, §6.2, SM-5 deferred adoption |
| Hard outs: cursors, SaaS, enterprise ACL, replace git | §5 Non-Goals |

---

## 2. PRD additions (brief silent — not gaps)

These strengthen or operationalize the brief without contradicting it:

- Named user journeys (Alex, Jordan, Sam, Riley) and JTBD block (§2.1).
- Glossary with **Claim/Ownership**, **Hard Block**, **Project Truth**, native **Artifact Lifecycle Status** definition.
- FR-5: all `sprint-status` stories enrolled in gating; undeclared dependencies = incomplete / hard block until resolved.
- FR-6: no undocumented override to skip hard block in v1.
- FR-9: impact review blocks Module “coherent merge / Build-ready signal,” not git push — enforcement via Module composition.
- **SM-C1** counter-metric: gates must not materially slow standard BMAD workflows.
- **§6.2:** multi-repo / sibling-repo orchestration explicitly out of v1.
- Cross-cutting NFRs (compat, perf qualitative, observability, security, semver).
- Explicit non-goal: parallel Planning Artifact enum `draft|review|ready`.
- Reference to `research-digest.md` (input not reconciled in this pass).

---

## 3. Intentional PRD overrides (brief → PRD)

| Topic | Brief | PRD decision | Rationale (from PRD text) |
|-------|-------|--------------|---------------------------|
| Planning artifact readiness vocabulary | Unified **`draft` / `review` / `ready`** for PRD, UX, Architecture | **F2:** use each artifact type’s **standard BMAD status** (e.g. PRD `draft`/`final`, story states in `sprint-status.yaml`); **non-goal** to invent parallel enum | Align with Core BMAD; avoid second lifecycle language |
| Ownership enforcement | “Ownership/structure” (neutral on strictness) | **F1 soft check:** warn on conflicting claim; **no hard lock** v1; git commit/push unrestricted | Reduce friction; defer hard locks unless pilot proves need (§6.2) |
| Gate strictness | Gates “enforced in practice”; brief doesn’t define override | **Hard Block** on Build / story start; **no silent skip** in v1 | Makes JTBD-1 and pilot success criteria testable |
| Long-term positioning | “Community-standard” module | “Official complementary module” in ecosystem | Same direction; PRD ties to upstream complementary-module norms |
| Correct-course “before merge” | Brief wording suggests merge gate | FR-9: Module workflow signal blocked until impact review complete; **git merge/push not blocked by hooks** | Git-native; enforcement wraps BMAD Build/Correct-Course |

---

## 4. Gaps and qualitative drops

### 4.1 Substantive (brief ideas weak or absent in PRD)

1. **Developer-as-primary sufferer** — Brief explicitly centers developers as who feels merge/readiness/drift pain most. PRD distributes pain across roles in journeys but does not preserve that prioritization for downstream UX/persona work.

2. **Alternative: process-only discipline** — Brief lists disciplined human process (without module) as a wedge contrast. PRD omits it; only party-mode and generic tooling called out.

3. **Unified “done enough” signal (`draft|review|ready`)** — Brief’s readable cross-artifact readiness ladder is **replaced** by heterogeneous native statuses (intentional). Downstream docs must not reintroduce `review` as a Module requirement without PRD change.

4. **Open-source as headline identity** — Brief leads with “open-source BMAD module”; PRD emphasizes installable complementary package and semver OSS releases without the same prominence (minor tone shift).

5. **Secondary audience (OSS community)** — Brief’s explicit secondary segment is not mirrored in §2; only ecosystem vision carries it.

### 4.2 Narrative / tone (FR structure tends to flatten)

- Brief’s **problem cost story** (~50–60%, firefighting, doesn’t scale) lives mainly in SM-1 baseline, not in a dedicated problem narrative — acceptable for PRD shape but **emotional/stakes framing is thinner**.
- Brief **“speaks BMAD’s artifact and workflow language”** as primary wedge is present in Vision but less punchy than brief’s executive contrast block.

### 4.3 Covered with refinement (not true gaps)

- **Ownership** — Present; brief didn’t specify soft vs hard; PRD chose soft (documented override).
- **Gates** — Present; PRD **harder** than brief’s prose minimum.
- **Hard outs / deferred scope** — Fully reflected in §5–§6.
- **Success / failure** — Mapped to §7; PRD adds SM-C1 (brief had no counter-metric).

---

## 5. Traceability summary

| Brief section | PRD sections | Status |
|---------------|--------------|--------|
| Executive Summary | §1, §6, §7, F1–F6 | **Mostly covered**; positioning + OSS tone shifted |
| Problem | §2 JTBD/UJ, §7 SM | **Covered functionally**; developer-centric + cost narrative reduced |
| Solution | §1, F1–F5 | **Covered**; one wedge alternative dropped |
| Who This Serves | §1, §2.2 | **Primary/non-users covered**; secondary audience implicit |
| Success Criteria | §7 | **Covered** + SM-C1 added |
| Scope in/out/hard out | §4–§6, §5 | **Covered**; lifecycle vocabulary **overridden** in F2 |

---

## 6. Reconciliation verdict

**Overall:** The PRD faithfully carries the brief’s v1 capability set (ownership conventions, gates, layer order, correct-course coherence, complementary install) and success/failure signals. The main deliberate divergence is **F2 native BMAD statuses instead of brief `draft|review|ready`**, with explicit non-goals preventing regression to a parallel enum.

**Action for Finalize (optional PM choices):**

- Accept F2 override and document in memlog if not already logged.
- Optionally restore one line in §2 or Vision naming **developers** as primary pain bearer and **process-only discipline** as a rejected alternative (qualitative only).
- Optionally restore **“open-source”** in Vision first sentence if OSS positioning matters for launch narrative.

**No phase-blocking gap identified** for UX / Architecture / Epics — unless stakeholders require the unified three-state lifecycle from the brief; that would be a **scope change**, not a reconciliation fix.
