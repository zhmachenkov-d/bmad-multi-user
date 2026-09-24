---
name: adversarial-architecture-review
target: ARCHITECTURE-SPINE.md
created: '2026-09-24'
method: dual-builder (feature/epic teams obey ADs literally; seek merge-time incompatibility)
---

# Adversarial Review — Architecture Spine (BMAD Multi-User)

## Executive verdict

**Conditional pass with material ambiguity debt.** The spine’s AD set is directionally coherent (preflight-gate, single home, single evaluator intent, native statuses). Under parallel implementation by feature/epic owners who treat AD text as the only contract, **at least nine credible incompatible pairs** emerge. Most holes sit where ADs defer “exact YAML micro-schemas” (explicitly in Deferred) or where two legitimate storage/entry surfaces are allowed without a **canonical key, file, or call graph**. Closing them does not require paradigm change—mostly **normative AD tightenings** plus one or two new ADs for identity, impact-review SoT, and evaluator packaging.

---

## Method

For each finding:

1. **Builder A / Builder B** — two epics one level down (F1–F6 / FR-aligned) that a staff engineer could scope independently.
2. **AD obedience** — each builder cites specific ADs and Consistency rows they believe they satisfy.
3. **Incompatibility** — what breaks at integration (data shape, dual ownership, divergent mutation paths) even if both land “by the book.”
4. **Spine patch** — new AD or tightened rule (not implementation detail beyond what’s needed to remove ambiguity).

---

## Findings (incompatible pairs)

### P-1 — Impact-review signal: Markdown vs YAML dual SoT

| | Builder A — Epic **F5 / FR-9** (Correct-Course coherence) | Builder B — Epic **F6 / FR-11** (Install + structural seed) |
| --- | --- | --- |
| **Delivers** | Skill creates `_bmad-output/multi-user/impact-review.md` with YAML frontmatter `status: open \| cleared` and checklist body | Installer template seeds `_bmad-output/multi-user/impact-review.yaml` with `state: open` and `items: []` |
| **Cites** | AD-3 (Module home; Markdown allowed for impact-review prose), AD-9 (open blocks coherent-merge / Build-ready), NFR-6 (plain text in git) | AD-3 (YAML structured state), Structural Seed `impact-review.*`, AD-11 (template Module home), AD-9 |
| **Incompatibility** | Evaluator A clears Build when frontmatter `status: cleared`; Evaluator B only reads YAML `state`. One artifact shows **open**, other **cleared** — Hard Block flips by entrypoint. Two mutation paths (skill edits MD vs script edits YAML). |
| **Close with** | **AD-9a (proposed):** Exactly one impact-review artifact path per project: fixed basename + format (`impact-review.yaml` *or* `impact-review.md`, not both); evaluator treats any other path as absent. Status field names enumerated. |

---

### P-2 — Story identity for deps filenames vs claims keys

| | Builder A — Epic **F3 / FR-5–FR-6** (Dependency Gates) | Builder B — Epic **F1 / FR-1–FR-2** (Ownership + conventions) |
| --- | --- | --- |
| **Delivers** | `deps/` files keyed by **exact** `sprint-status.yaml` story keys (e.g. `3-2-api-auth.yaml`) | Conventions doc + claim skill use **slug ids** (`api-auth`) in `claims.yaml` `story_slice` and soft-check maps deps via slug |
| **Cites** | AD-6 (`deps/<story-id>.yaml`), Consistency (“Story ids in deps filenames match sprint-status keys”) | AD-8 (central claims registry), AD-3, FR-2 (Story-related slices) |
| **Incompatibility** | Gate enrolls `3-2-api-auth`; claims/deps cross-reference fails; soft-check warns on wrong paths; cycle/layer scans miss files. **Same story, two ids** — not a violation of either AD read literally (AD-8 doesn’t bind claim keys to sprint-status). |
| **Close with** | **AD-12 (proposed):** Canonical `story_id` = sprint-status key everywhere (deps filename stem, claims, layer exceptions, impact-review items). Skills MUST reject slug-only aliases without mapping file in Module home. |

---

### P-3 — Where “Story Layer tag” lives (layer-order vs deps vs sprint-status)

| | Builder A — Epic **F4 / FR-7–FR-8** (Layer Order) | Builder B — Epic **F3 / FR-5** (Declare story dependencies) |
| --- | --- | --- |
| **Delivers** | `layer-order.yaml` includes `story_layers: { "<story_id>": "<layer_token>" }` only | Each `deps/<story-id>.yaml` carries `layer: backend` plus dependency lists; no story→layer map elsewhere |
| **Cites** | AD-7 (Layer Order file, exceptions name `story`), AD-3 | AD-6 (per-Story deps enrollment), FR-5 (dependencies on Layers), AD-4 (Module doesn’t write arbitrary Core fields) |
| **Incompatibility** | Layer gate pass A reads `story_layers`; pass B reads `deps/*.yaml`. Story moved between layers in one file only → **frontend Build passes for A, Hard Block for B**. Loosen exceptions in AD-7 reference `story` without requiring same layer source. |
| **Close with** | **AD-7a (proposed):** Single SoT for story→layer binding (pick one: `layer-order.yaml` map *or* required field in deps file). Evaluator MUST NOT merge conflicting sources; mismatch = Hard Block + reason. |

---

### P-4 — Readiness map override vs hardcoded Layer `done` rule

| | Builder A — Epic **F2 / FR-3–FR-4** (Native status visibility) | Builder B — Epic **F2 / FR-10** (Status recalc + config) |
| --- | --- | --- |
| **Delivers** | `config.yaml` `readiness_map` extends **Story** artifact kind so Layer predecessor check treats `in-progress` as satisfying “earlier layer ready” for reporting | Evaluator core hardcodes FR-8: earlier-layer Stories MUST be **`done`** only; readiness map applies only to Planning Artifacts |
| **Cites** | AD-10 (default map + overrides in Module home), AD-5 (single evaluator), FR-4 | AD-10 (must not invent parallel enums—uses native values), AD-7, PRD FR-8 explicit `done` |
| **Incompatibility** | Status report **pass** (B’s map) vs Build hook **fail** (A’s layer pass)—same Story, same sprint-status, **divergent pass/fail** across FR-4 vs FR-6 despite AD-5. Both claim “native statuses only.” |
| **Close with** | **AD-10a (proposed):** Readiness map overrides apply only to **Planning Artifact kinds** listed in map; Story Layer Order (FR-8) uses fixed predicate `status == done` and is not overridable via readiness map. Single evaluator function for both.report and gate. |

---

### P-5 — “Single evaluator” as two CLI entrypoints + forked library

| | Builder A — Epic **F3 / FR-6** (Build hook integration) | Builder B — Epic **F2 / FR-4** (Status report skill) |
| --- | --- | --- |
| **Delivers** | `scripts/gate_eval.py` invoked from `bmad-build` hook; embeds layer + deps checks inline “for speed” | `scripts/status_report.py` with duplicated gate fragments “imported from copy-paste until shared lib lands” |
| **Cites** | AD-5 (shared script/library; hooks call it), AD-2 (hook wiring), AD-11 (scripts in package) | AD-5 (must not reimplement in prose—uses Python), NFR-5 (machine-readable reasons) |
| **Incompatibility** | Build Hard Block lists failing dep X; status report omits X after partial refactor. **Letter of AD-5** satisfied if each entrypoint “calls Python” but **spirit violated**—no enforced single module import path. |
| **Close with** | **AD-5a (proposed):** One importable package (e.g. `multi_user_gate/`) is the only place gate rules live; all CLIs are thin wrappers. CI test: report and gate JSON schema for same inputs MUST match. |

---

### P-6 — Claims registry: monolith vs path-prefix set without merge semantics

| | Builder A — Epic **F1 / FR-2** (Soft claim check) | Builder B — Epic **F1 / FR-1** (Conventions + scalable layout) |
| --- | --- | --- |
| **Delivers** | All claims in `claims.yaml`; soft-check reads one file | `claims/` directory with `backend-prefix.yaml`, `frontend-prefix.yaml` per AD-8 “small path-prefix set” |
| **Cites** | AD-8 (central registry `claims.yaml`), AD-3 | AD-8 (explicit alternative), AD-3 single tree, FR-1 documented conventions |
| **Incompatibility** | Overlapping path prefixes registered in both files by different teams → **dual owner** of same path; warn-once vs warn-twice; stale claim in unread file. No AD rule for scan order or prohibition of overlap. |
| **Close with** | **AD-8a (proposed):** If using prefix set, manifest file `claims/index.yaml` lists shard files; evaluator loads union; **overlapping path or prefix intersection = validation error on write**. v1 default remains single `claims.yaml` unless index present. |

---

### P-7 — Who may create / normalize `deps/` (explicit skill vs evaluator auto-enrollment)

| | Builder A — Epic **F3 / FR-5** (Declare dependencies UX) | Builder B — Epic **F3 / FR-6** (Gate evaluator + onboarding) |
| --- | --- | --- |
| **Delivers** | Missing deps file = Hard Block until human runs declare-deps; schema `dependencies: { stories: [], artifacts: [], explicit_none: true }` | First gate run auto-writes `deps/<story-id>.yaml` with `none: true` to unblock Pilot |
| **Cites** | AD-6 (missing = incomplete = Hard Block), AD-4 (Module skills write deps) | AD-6 (explicit `none`), AD-4 (scripts write Module home), FR-5 enrollment |
| **Incompatibility** | `explicit_none` vs `none: true` — both “explicit none” per AD-6 literal reading; cycle scanner treats unknown keys differently; **two mutation paths** for enrollment (skill vs evaluator write). |
| **Close with** | **AD-6a (proposed):** Only declare-deps skill (or Correct-Course recalc) may create or change deps files; evaluator **read-only** on deps. Canonical `none` representation single keyed form in schema AD. |

---

### P-8 — Coherent-merge / impact gating entrypoint split

| | Builder A — Epic **F5 / FR-9** (Impact review skill) | Builder B — Epic **F6 / FR-12** (Coexist with Core workflows) |
| --- | --- | --- |
| **Delivers** | Hard Block for open impact only inside impact-review skill “mark coherent” step | Hard Block only on `bmad-build` and `bmad-correct-course` hooks; no separate coherent-merge caller |
| **Cites** | AD-9 (Build-ready Hard-Block while impact open), AD-5 | AD-2 (hooks on build + correct-course only), Enforcement surface table (coherent-merge listed) |
| **Incompatibility** | User completes checklist in skill (thinks merge-coherent) but Build still blocked—or Build passes via Core unwrapped path while impact open. **“Coherent-merge”** named in Consistency but not bound to same hook set as AD-2. |
| **Close with** | **AD-9b (proposed):** Enumerate gated entrypoints: `build`, `correct_course`, and any skill whose description includes “coherent merge” MUST call evaluator with `--check impact_review`. No gate solely in prose skill without script call. |

---

### P-9 — Correct-Course status write path vs read-only Module on sprint-status

| | Builder A — Epic **F5 / FR-10** (Status recalculation) | Builder B — Epic **F2 / FR-3** (Read native statuses) |
| --- | --- | --- |
| **Delivers** | Recalc skill patches `sprint-status.yaml` Story rows to `backlog` when deps invalidate; cites AD-4 explicit Correct-Course write | Status reader treats any Module-touchable sprint-status as suspicious; caches immutable snapshot at preflight start; never re-reads after recalc in same session |
| **Cites** | AD-4 (write Story status via Correct-Course / recalc, native values only) | AD-4 (humans + Core write sprint-status; Module reads), AD-5 single evaluator read path |
| **Incompatibility** | Post-recalc statuses visible on disk but gate uses **stale cache** → Build Hard Block with wrong reasons; two views of **same entity** (sprint-status). |
| **Close with** | **AD-4a (proposed):** Evaluator MUST read sprint-status from disk (or git index) at each gate invocation—no cross-invocation cache of Core truth. Recalc skill MUST emit event file `multi-user/.last-recalc` timestamp; evaluator fails closed if recalc newer than last read in same composed workflow (or simply no caching). |

---

### P-10 — Dependency “Layer” reference vs Layer Order tokens

| | Builder A — Epic **F4 / FR-7** (Declare Layer Order) | Builder B — Epic **F3 / FR-5** (Declare story dependencies) |
| --- | --- | --- |
| **Delivers** | Layer tokens: `backend`, `frontend`, `mobile` in ordered list | FR-5 deps reference Layers by **display names** `Backend API`, `Frontend UI` in artifact dependency section |
| **Cites** | AD-7 (project-declared tokens in Layer Order file), Consistency naming | FR-5 (depend on Layers), AD-6 deps file stores declarations |
| **Incompatibility** | Layer gate compares token sets that never match → permanent Hard Block or spurious pass if one side normalizes fuzzily. **Shared-data shape** for layer reference undefined. |
| **Close with** | **AD-7b (proposed):** Layer Order file defines canonical token list; deps and story_layers MUST reference tokens only; declare-deps validates against list. |

---

## Cross-cutting observations

1. **Deferred micro-schemas are the largest attack surface.** The spine correctly lists exact YAML schemas as deferred (line 180), but AD-6, AD-8, and AD-9 already **require** those files to exist and drive Hard Block. Parallel builders will ** invent schemas** unless ADs point to a single normative schema doc or AD-13 “Module home schema version field.”

2. **Consistency table vs ADs.** The table says deps keys match sprint-status; AD-8 doesn’t bind claims to the same id. Treat Consistency rows as **binding** or duplicate them inside ADs (P-2).

3. **PRD open questions (§9) are adversarially exploitable.** FR-9 trigger and coherent-merge flag (items 1–2) let Builder A assume “every correct-course” and Builder B “only if graph touched”—both compatible with AD-9 today. Tighten AD-9 to match v1 spine choice: **every** `bmad-correct-course` run (already in AD-9) and single cleared signal definition (P-1).

4. **No hole found** for: vendor path writes (AD-4/11 clear), git hooks as sole gate (AD-2), SaaS coupling (AD-11), parallel lifecycle enum invention if AD-10a applied for Stories vs artifacts.

---

## Recommended AD delta summary

| ID | Action | Closes |
| --- | --- | --- |
| AD-9a | Impact-review single path + status fields | P-1 |
| AD-12 | Canonical story_id = sprint-status key | P-2 |
| AD-7a | Single story→layer SoT | P-3, P-10 |
| AD-10a | Readiness map scope; FR-8 not overridable | P-4 |
| AD-5a | One Python package; CLI wrappers only | P-5 |
| AD-8a | Claims shard index + overlap validation | P-6 |
| AD-6a | Deps write ownership + canonical `none` | P-7 |
| AD-9b | Enumerate gated entrypoints incl. coherent-merge | P-8 |
| AD-4a | No stale sprint-status cache in evaluator | P-9 |
| AD-13 (new) | `config.yaml` `schema_version` + semver linkage to AD-11 | Cross-cutting schema drift |

---

## Test harness suggestion (for Architecture phase)

For each proposed AD tightening, add an **integration fixture**: two minimal Module-home trees labeled Builder A/B from the table above; **single evaluator run** must yield identical pass/fail and reason codes after merge—or fail CI with “ambiguous spine.”

---

## Sign-off

| Role | Result |
| --- | --- |
| Adversarial review | **Verdict: conditional pass** — adopt AD deltas before epic split |
| Blockers for epic parallelization | P-1, P-2, P-3, P-5, P-7 (highest merge conflict risk) |
| Non-blockers but watch | P-4, P-6, P-8, P-9, P-10 |
