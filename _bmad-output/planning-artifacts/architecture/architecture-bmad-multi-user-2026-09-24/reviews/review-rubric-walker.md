# Rubric Walker Review — ARCHITECTURE-SPINE.md

**Reviewed:** 2026-09-24  
**Spine:** `ARCHITECTURE-SPINE.md` (altitude: initiative, status: draft)  
**Authority:** `.memlog.md`  
**Driving spec:** `prd-bmad-multi-user-2026-09-24/prd.md`  
**Mechanical lint:** `lint_spine.py` — **0 findings** (`ok: true`)

---

## Verdict

**Conditional pass** — The spine is a strong build substrate for a complementary BMAD Module: paradigm, state home, write ownership, single evaluator, and PRD F1–F6 are largely pinned. It is safe to proceed to spec/epics **after** tightening a short list of divergence leaks (gated entrypoint coverage, deferred schema ownership, and one silent NFR dimension). None of the issues invalidate the AD set; they are fixable with small AD/convention/deferred clarifications without reopening coaching.

---

## Checklist (good-spine)

### 1. Fixes real divergence points for the level below; misses none

**Strengths**

| Divergence risk (feature/epic builders) | Spine fix |
| --- | --- |
| Orchestrator vs preflight gate | AD-1 |
| Vendor Core edits vs custom hooks | AD-2 |
| Module state scattered vs single home | AD-3 |
| Who may write Planning Artifacts / sprint status | AD-4 |
| Different pass/fail in hook vs status report vs recalc | AD-5 |
| Monolith deps vs per-story vs frontmatter | AD-6 |
| Silent layer bypass vs audited exceptions | AD-7 |
| Dual claim ledgers / hard locks in v1 | AD-8 |
| Skipped Correct-Course / chat “review done” | AD-9 |
| Parallel `draft\|review\|ready` vocab | AD-10 |
| Ad-hoc install vs complementary module + semver | AD-11 |

Memlog decisions are faithfully distilled into AD-1–AD-11; binds align with PRD FR/NFR IDs in frontmatter.

**Misses / thin coverage (level below could still diverge)**

1. **Build entrypoint surface (FR-6, FR-12)** — AD-2 names hooks on `bmad-build` and `bmad-correct-course` only. Core BMAD also exposes **`bmad-build-auto`** (and potentially other “Story start / Build” paths). Two epics could gate one path and leave another unhooked → Hard Block bypass without violating AD-2 literally. *Recommendation:* Extend AD-2 Rule to “all Core skills that start Story Build / unattended build loops” or explicitly list `bmad-build-auto` beside `bmad-build`.

2. **Claim soft-check trigger (FR-2, F1)** — AD-8 defines registry semantics; AD-2 does not require claim intersection checks on the same gated entrypoints (or a single script entry). One builder wires soft-check only in a UX skill; another only at Build preflight → inconsistent warnings, not gate divergence, but FR-2 “conflicting edit attempt” behavior diverges. *Recommendation:* AD-5 or Consistency Conventions: claim soft-check callable from Build/Correct-Course preflight via shared scripts (same library as evaluator or explicit second entrypoint documented in structural seed).

3. **FR-10 invalid Story disposition after recalc** — AD-4 allows native status writes via Correct-Course/recalc but does not decide **which** native Story status means “no longer executable” (`backlog`, `ready-for-dev`, etc.). Two implementers pick different mappings → sprint-status semantics diverge while both “comply” with AD-4. *Recommendation:* AD-4 bullet or AD-9: project rule lives in Module home `config.yaml` with Module default documented in seed (even if exact enum rows stay implementation-owned).

4. **FR-7 Layer Order validation** — PRD requires invalid/cyclic **Layer Order declarations** rejected. AD-7 describes runtime gate behavior and loosen exceptions; AD-6 says cycle checks scan the **deps** tree. Ambiguity: cycles in `layer-order.yaml` itself vs dependency cycles. *Recommendation:* AD-7 Rule: layer-order file validated on write (ordered list integrity); cycle detection scope = deps graph (already) + reject duplicate/unknown layer tokens in deps.

5. **F1 convention docs location (FR-1)** — Conventions are bound to AD-3/AD-8 but not **where** shipped (module package `docs/` vs Module home). Low severity; two teams could document in incompatible places. *Recommendation:* One line in Structural Seed or Consistency Conventions.

6. **“Coherent-merge” as enforcement surface** — Used in paradigm, AD-9, and Consistency Conventions but not defined as a Core skill vs Module skill vs alias for “Build-ready after Correct-Course.” Builders may implement a third gate path. *Recommendation:* Define coherent-merge = evaluator pass with impact-review `cleared` + Dependency Gates (same script as Build), not a separate ruleset.

**Brownfield note:** This repo already has prototype `team-gates` / `team-claim` under `skills/` using `{planning_artifacts}/team/gates.json`. The spine correctly targets the **new** Module home under `_bmad-output/multi-user/`; it does not ratify legacy team skills. Pilot install must migrate or replace prototypes — worth a Deferred or migration AD note if brownfield adoption is expected (optional, not in PRD MVP).

---

### 2. Every AD Rule is enforceable and prevents its stated divergence

| AD | Enforceability | Notes |
| --- | --- | --- |
| AD-1 | Partial — architectural / review | “Must not become orchestrator” enforced by package shape + hooks-only composition, not runtime guard. Acceptable at initiative altitude if AD-11 install smoke checks exist. |
| AD-2 | **Strong** — if hook templates ship and smoke test verifies `_bmad/custom` wiring | Gap: entrypoint list completeness (see §1). “Wrappers not sole gate” enforceable via install test invoking Core skill without custom hooks → must fail or warn per FR-12 test design. |
| AD-3 | **Strong** — path convention + evaluator reads single tree | Renames allowed if single-home invariant holds (Deferred aligns). |
| AD-4 | **Strong** — write paths + “vendor never” in CI/review | Story status mapping gap (§1) weakens FR-10 half of prevention. |
| AD-5 | **Strong** — single Python library + non-zero exit | Explicit ban on prose-only reimplementation is enforceable in code review + one integration test per entrypoint. |
| AD-6 | **Strong** — missing `deps/<id>.yaml` = Hard Block | `none` sentinel must be schema-defined in implementation (deferred detail). |
| AD-7 | **Strong** — evaluator reads layer-order + exceptions | Loosen records require `approved_by` — auditable plain text. |
| AD-8 | **Moderate** — soft-check only | Enforcement depends on calling convention (see §1). Prevents hard-lock creep: **yes**. |
| AD-9 | **Strong** — impact-review `open` blocks via same evaluator | PRD open Q1–Q2 resolved in memlog and AD-9 (every Correct-Course run). |
| AD-10 | **Strong** — config map in Module home | Default rows deferred but override mechanism decided. |
| AD-11 | **Strong** — semver + no SaaS + complementary module layout | “Declare supported Core BMAD major(s)” needs a concrete file in seed (e.g. `config.yaml` or module manifest) at implementation — not yet named in Structural Seed. |

**Summary:** Rules are implementable as scripts + git text + hook templates. AD-1 and AD-8 rely on discipline/review more than runtime. No AD Rule is purely aspirational.

---

### 3. Nothing under Deferred could let two units diverge unsafely

| Deferred item | Divergence risk | Assessment |
| --- | --- | --- |
| Smart merge assist | Low for v1 — git conflict handling stays human/git; no second SoT | **Safe** |
| Hard Claim locks | Explicitly post-v1 | **Safe** |
| Multi-repo orchestration | Out of scope single-repo Pilot | **Safe** |
| Correct-Course touch-heuristic skip | **Closed in v1** (always run) — defers only future optimization | **Safe** |
| Pilot diary / SM-C1 proxy | Measurement only, not gate logic | **Safe** |
| Module home folder rename | Single-home invariant preserved | **Safe** |
| **Exact YAML micro-schemas** (claims/deps/impact-review) | **High during parallel implementation** — two epics can ship incompatible field names/shapes; gates read different semantics until major semver | **Unsafe deferral for multi-builder cold start** unless treated as **seed owned by one epic** or minimum schema AD added |
| **Exact default readiness-map rows** | **Moderate** — AD-10 requires defaults exist; deferring rows lets evaluator vs config epic diverge on “PRD final means X” | **Mitigate:** first implementation epic owns canonical `config.yaml` defaults; or promote minimal rows to seed in spine |

**Finding:** Two Deferred bullets defer **contract shape** that AD-5/AD-6/AD-10 already treat as binding. That is appropriate for *post-v1* evolution via semver, but **unsafe** if multiple stories implement parsers/writers in parallel without a single schema owner. Fix: mark as “implementation seed — single owner epic; breaking change = major” in Deferred wording, or add a one-paragraph **minimum schema invariant** (required keys only) to Consistency Conventions.

---

### 4. Named tech verified-current

| Name | Spine claim | Verification (2026-09-24) |
| --- | --- | --- |
| Python | `>=3.11` | Env: 3.12.11; Core scripts mix 3.10–3.11 in skills — `>=3.11` matches memlog and party-mode script; consistent with “align Core BMAD scripts” intent |
| uv | `~0.12.x (verified 2026-09)` | Env: **0.12.17** — matches |
| YAML / Markdown | state formats | Appropriate |
| `_bmad/custom/*.toml` hooks | composition surface | Matches installed BMAD customization model (`activation_steps_prepend`) |
| Host | local git, no SaaS | Matches PRD NFR-4 |

**Note:** Memlog says “matching Core BMAD _bmad/scripts”; repo `_bmad/scripts/` has no PEP 723 pin — spine choice is forward-looking for the Module, not a ratification scan of every skill script. **Acceptable** for greenfield module.

---

### 5. Covers driving spec capabilities

**PRD coverage map**

| PRD | Spine |
| --- | --- |
| F1 FR-1–2 | AD-3, AD-8; map row F1 |
| F2 FR-3–4 | AD-4, AD-5, AD-10 |
| F3 FR-5–6 | AD-5, AD-6; Hard Block |
| F4 FR-7–8 | AD-7; default earlier layers `done` |
| F5 FR-9–10 | AD-9, AD-4, AD-5 |
| F6 FR-11–12 | AD-2, AD-11 |
| NFR-1–2,4–8 | AD-2, AD-11, stack, conventions |
| NFR-3 | **Not explicitly bound** — see §6 |
| NFR-6 JSON/YAML/MD | Spine emphasizes YAML; JSON allowed by NFR — minor doc alignment only |
| Non-Goals | Reflected in Deferred + AD-1/AD-11 |
| Open Q1–Q2 (FR-9) | **Resolved** in AD-9 (memlog lines 26–27) |
| Open Q3–Q4 | Correctly Deferred (pilot ops) |

User journeys UJ-1–4 trace to F1–F5 rows. **Capability map is complete** for MVP architecture purposes.

---

### 6. Every dimension at initiative altitude — decided, deferred, or open

| Dimension | Status in spine |
| --- | --- |
| Paradigm / boundaries | **Decided** (AD-1–AD-4, AD-11) |
| State & mutation | **Decided** |
| Gate logic & enrollment | **Decided** (AD-5–AD-7) |
| Correct-Course / Project Truth signal | **Decided** (AD-9) |
| Stack & composition | **Decided** |
| Structural seed / tree | **Decided** (seed paths) |
| Operational / environmental envelope | **Decided** — “no cloud deploy; offline in git tree; environments = Core BMAD major compatibility (NFR-2)” |
| Performance / ceremony cost (NFR-3, SM-C1) | **Silent** — not listed under Deferred or Open Questions in spine |
| Observability beyond gate reasons (NFR-5) | **Decided** in conventions |
| Security/secrets (NFR-7) | **Decided** in conventions |
| Versioning / migration (NFR-8) | **Decided** (AD-11) |
| Pilot measurement | **Deferred** |

**Finding:** **NFR-3 / SM-C1** (“fast preflight, no meaningful workflow inflation”) is a cross-cutting constraint with no AD, Deferred entry, or Open Question in the spine. Memlog defers only optional SM-C1 **proxy metric**, not the NFR itself. At initiative altitude this should be **Decided (qualitative)** in Consistency Conventions or **Open** with revisit at pilot — silence fails the rubric’s “whole dimension” test.

Deployment topology is appropriately decided (none). **Compatibility matrix** (which Core BMAD majors) is decided in principle (AD-11) but **not** where declared in repo — minor seed gap.

---

## AD ↔ memlog fidelity

Spot-check: All memlog `(decision)` entries from paradigm through Deferred confirm appear in AD-1–AD-11 or Deferred section. No memlog decision contradicts spine. Coaching path and “spine only” deliverable match frontmatter `purpose: build-substrate`.

---

## Recommended fixes (priority)

1. **P0 — Gated entrypoints:** Extend AD-2 to include every Build-start Core skill (at minimum `bmad-build-auto`) and equate “coherent-merge” checks with evaluator + impact-review state (no third rule engine).

2. **P0 — Deferred schema work:** Clarify Deferred “micro-schemas” — either minimum required keys in Consistency Conventions, or “single epic owns schema v1 before parallel dep/claim stories.”

3. **P1 — NFR-3:** Add one convention row or Deferred/Open line: qualitative preflight budget; optional SM-C1 proxy remains pilot Deferred.

4. **P1 — FR-10 status mapping:** Module home default for “invalidated Story → native status X” in AD-4 or AD-9.

5. **P2 — FR-7 layer-order validation:** Clarify validation vs deps-cycle in AD-7.

6. **P2 — Core major declaration:** Name file in Structural Seed (e.g. `supported_core_bmad_majors` in module manifest or `config.yaml`).

---

## Summary table

| Rubric item | Result |
| --- | --- |
| Divergence points for level below | **Mostly fixed**; gaps: Build entrypoints, coherent-merge definition, FR-10 status pick, layer-order validation wording |
| AD Rules enforceable | **Yes**, with AD-1/AD-8 partial; entrypoint list must widen |
| Deferred safety | **Two items risky** for parallel build (micro-schemas, readiness-map rows) |
| Tech verified-current | **Pass** |
| Spec capabilities | **Pass**; NFR-3 implicit only |
| Altitude dimensions | **Pass** except NFR-3/SM-C1 performance dimension silent |

---

*Reviewer: rubric walker (good-spine checklist). Mechanical lint passed; judgment per `references/reviewer-gate.md`.*
