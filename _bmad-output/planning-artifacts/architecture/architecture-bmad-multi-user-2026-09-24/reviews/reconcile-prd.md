# PRD ↔ Architecture Spine Reconciliation

**Date:** 2026-09-24  
**PRD:** `_bmad-output/planning-artifacts/prds/prd-bmad-multi-user-2026-09-24/prd.md` (status: final)  
**Spine:** `_bmad-output/planning-artifacts/architecture/architecture-bmad-multi-user-2026-09-24/ARCHITECTURE-SPINE.md` (status: draft)

## Method

- Mapped PRD §4 FR-1–FR-12, §5 NFR-1–NFR-8, glossary constraints, and testable consequences against spine frontmatter `binds`, AD-1–AD-11, capability map, deferred list, and stack/structural seed.
- Treated vision/journeys/success metrics as binding only where they imply hard constraints on build substrate.
- Open Questions (PRD §9) noted when spine preemptively decided them.

## Coverage summary

| PRD area | Spine coverage |
| --- | --- |
| F1–F6 / FR-1–FR-12 | Explicit `binds`; capability map; AD-1–AD-11 |
| NFR-1–NFR-8 | Explicit `binds`; AD-2, AD-4, AD-5, AD-11, conventions table |
| Non-Goals / MVP out-of-scope | Largely mirrored in spine **Deferred** |
| Glossary (Hard Block, native status, Claim soft-check, etc.) | Reflected in AD-5, AD-7, AD-8, AD-10 |

Spine adds implementation choices not specified in PRD (Python ≥3.11, uv, `_bmad-output/multi-user/` seed path, single Python evaluator, hook filenames)—acceptable architecture elaboration, not PRD conflicts.

---

## 1. Quiet requirements / constraints (PRD) not landed in spine

These are PRD-stated requirements or testable consequences with no clear, checkable home in the spine (missing, only implied, or explicitly deferred without restating the PRD obligation).

### Conventions & F1 (FR-1)

- **High-churn status files:** FR-1 consequences require Module-published conventions covering at least Planning Artifact folders **and high-churn status files**. Spine mentions “conventions docs” for F1 but does not call out status-file layout / ownership steering for hot shared files (e.g. sprint-status paths).

### Install & validation (FR-11)

- **Smoke check for Core integrity:** FR-11 consequences require an automated or manual smoke check proving installer-owned Core BMAD paths were not required to be modified. Spine covers “never edit vendor” (AD-2, AD-4, AD-11) but does not require or describe an install/smoke validation step.

### Layer Order validation (FR-7)

- **Reject invalid/cyclic Layer Order declarations:** FR-7 consequences require invalid/cyclic Layer Order declarations to be rejected with an error. Spine AD-7 defines default enforcement and audited loosen exceptions; AD-6 mentions cycle checks on the **deps** tree. Spine does not state validation/rejection rules for the **Layer Order file itself** (duplicates, unknown layers, malformed order, etc.).

### Dependency Gate inputs (FR-5)

- **Planning Artifact and Layer as gate inputs:** FR-5 allows declaring dependencies on Stories, **Planning Artifacts**, and **Layers**. Spine AD-6 centers on `deps/<story-id>.yaml` enrollment; exact dep schema (PA references, layer constraints beyond AD-7 default) is deferred to implementation seed. PRD testable consequence (“stored git-natively”, gate uses them) is only partially anchored until schema exists.

### Native readiness coverage (FR-3, FR-4, glossary)

- **Artifact kinds and native status examples:** PRD glossary/fixtures cite PRD `draft`/`final`, product brief `complete`, Story sprint statuses, spec statuses. Spine AD-10 commits to a default readiness map + overrides but **defers exact default rows**; spine does not restate PRD minimum Planning Artifact set (PRD, UX Design/Experience, Architecture) as default map content.

### Correct-Course & recalc (FR-9, FR-10)

- **FR-9 “significant mid-flight change” qualifier:** PRD feature description scopes impact review to **significant** mid-flight change; spine does not preserve that qualifier (see contradictions).
- **FR-10 “blocked” vs native-only writes:** FR-10 allows Stories that became invalid to be marked **blocked** or returned to a non-executable **standard** BMAD status without inventing names. Spine AD-4 only mentions writing **native** BMAD status values on recalc; it does not say whether `blocked` (not listed in PRD glossary Story enum) is in or out of scope.

### Claims behavior (FR-2)

- **Warn on conflicting edit attempts:** FR-2 requires soft-check on conflicting **edits**, not only Build preflight. AD-8 mentions “intersecting edits/preflight” but does not specify **when** edit-time warning runs (hook vs manual skill vs optional editor integration)—enforcement surface under-specified vs PRD consequence.

### NFRs & workflow

- **NFR-3 (qualitative fast preflight):** PRD requires gate/status checks on Story start / Build preflight to feel like a normal fast preflight and not meaningfully inflate BMAD workflow time (SM-C1). Spine chooses a single evaluator (helps) but does not record NFR-3 / SM-C1 as a design constraint (only defers optional SM-C1 proxy to pilot ops).

- **NFR-6 JSON:** PRD allows Module-owned state as **JSON/YAML/Markdown**. Spine structural seed and AD-3 emphasize **YAML** (+ Markdown for impact review); JSON is not listed as an allowed Module-home format.

### Process / audience (non-build but PRD constraints)

- **Primary sufferer / JTBD audience (§2):** Developers as primary JTBD payoff—not reflected in spine (acceptable for substrate doc unless team wants persona-driven ops).
- **Success metrics & pilot measurement (§8, §9 Q3–Q4):** SM-1 baseline, diary protocol, SM-C1 watch metric—spine correctly defers to pilot ops; PRD constraints on **measuring** success are not architecture invariants (intentionally omitted).

### Vision / positioning (§1, §1.1)

- Ecosystem positioning, comparables table, refusal of AI-DLC wholesale copy—inform AD-1 paradigm but are not captured as traceable constraints (low risk).

---

## 2. Contradictions

Direct or material tension between PRD text and spine rules (not mere elaboration).

### C-1 — Correct-Course impact review trigger (FR-9 vs AD-9)

| Source | Text |
| --- | --- |
| PRD FR-9 (description) | Impact review after a **significant** mid-flight change |
| PRD §9 OQ1 | Still open: every `bmad-correct-course` run vs touch-heuristic |
| Spine AD-9 | **Every** `bmad-correct-course` run requires impact review + recalc in v1 |
| Spine Deferred | Touch-heuristic skip deferred; v1 always runs impact review |

**Nature:** Spine **closes** OQ1 with the strictest interpretation. That is consistent with FR-9 consequences (no merge-ready while impact open) but **tighter** than the “significant change” wording and **ahead of** PRD §9 which still lists the question as open. Treat as **process drift** + **scope tension**: trivial Correct-Course runs must run full impact review in v1 per spine.

**Severity:** Medium—implementers follow spine; PM may expect PRD “significant” to limit ceremony.

### C-2 — Module state formats (NFR-6 vs AD-3 / Stack)

| Source | Text |
| --- | --- |
| PRD NFR-6 | Plain text in git: **JSON/YAML/Markdown** |
| Spine AD-3 / Stack | Module home: **YAML**; Markdown for impact-review prose; no JSON |

**Nature:** Spine narrows allowed formats. If any Module state were JSON (e.g. tool-generated), spine would forbid it as primary home format.

**Severity:** Low–medium—easy to align by amending spine to “YAML preferred; JSON allowed for structured state” or PRD to YAML-primary.

### C-3 — Open Questions vs spine decisions (FR-9, §9 OQ2)

| Source | Text |
| --- | --- |
| PRD §9 OQ2 | What concrete artifact/flag means “impact review complete”? |
| Spine AD-9 + seed | `impact-review.*` with `open` \| cleared when all items checked |

**Nature:** Not a logical conflict—spine **answers** OQ2. PRD still lists OQ2 as open → **documentation inconsistency**, not opposing rules.

**Severity:** Low (reconcile PRD §9 or add spine note “closes OQ2”).

---

No contradiction found for: Hard Block without undocumented skip (AD-7 audited loosen only), soft Claim vs hard lock, no Core vendor edits, no git hooks for Hard Block, native status map (no parallel enum), Layer Order default (`done` on earlier layers), FR-5 enrollment / missing deps = Hard Block (AD-6), offline F1–F5 (AD-11).

---

## 3. Preemptive spine decisions (PRD still open—track for PRD edit)

| PRD §9 item | Spine decision |
| --- | --- |
| OQ1 Correct-Course trigger | Always on hook (AD-9) |
| OQ2 Coherent-merge signal | `impact-review.*` open/cleared (AD-9, structural seed) |
| OQ4 SM-C1 proxy | Deferred to pilot ops (spine Deferred) |
| FR-8 loosen mechanism | `layer-order.yaml` named exceptions (AD-7)—matches PRD “Architecture-time override” intent |

---

## 4. Verdict rationale

**Bind completeness:** All FR-1–FR-12 and NFR-1–NFR-8 appear in spine `binds` with governing ADs.

**Gaps:** Several **testable PRD consequences** (conventions scope, Layer Order file validation, install smoke check, NFR-3/SM-C1 design note, dep schema for PA/Layer refs, JSON in NFR-6) are thin or deferred without echoing the PRD obligation—implementation could miss them without epics/stories.

**Contradictions:** One **material scope tension** (FR-9 “significant” vs AD-9 “every run”); one **format narrowing** (JSON); open-question documentation drift.

---

## 5. Verdict

**FAIL**

Fail on reconciliation bar: spine does not fully **land** several quiet PRD testable consequences, and AD-9 materially **tightens** FR-9 trigger language while PRD §9 still treats that trigger as open—without spine explicitly marking that as an approved PRD override.

**Recommended spine follow-ups (minimal):**

1. AD-9: Cross-reference FR-9; state v1 policy overrides “significant” → all Correct-Course hook invocations; or align AD-9 to touch-heuristic once PRD OQ1 is resolved.
2. AD-3 / Stack: Align with NFR-6 (allow JSON) or note “YAML canonical; JSON only if NFR-6 amended.”
3. Add explicit bullets: FR-1 high-churn status conventions; FR-7 Layer Order validation; FR-11 install smoke check; NFR-3 design note on evaluator hot-path cost.
4. Defer section: link dep YAML schema to FR-5 PA/Layer inputs and AD-10 default map rows to PRD Planning Artifact minimum set.

**Recommended PRD follow-ups:**

- Close or update §9 OQ1/OQ2 to match AD-9 and impact-review artifact.
- Clarify FR-9 “significant” vs always-on Correct-Course if spine policy stands.
