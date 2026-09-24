---
id: SPEC-bmad-multi-user
companions:
  - ../../planning-artifacts/architecture/architecture-bmad-multi-user-2026-09-24/ARCHITECTURE-SPINE.md
  - pilot-ops.md
sources:
  - ../../planning-artifacts/prds/prd-bmad-multi-user-2026-09-24/prd.md
  - ../../planning-artifacts/briefs/brief-bmad-multi-user-2026-09-24/brief.md
---

> **Canonical contract.** This SPEC and the files in `companions:` are the complete, preservation-validated contract for what to build, test, and validate. Source documents listed in frontmatter are for traceability — consult them only if you need narrative rationale or prose color this contract intentionally omits.

# BMAD Multi-User

## Why

**Pain to solve** for multi-role teams (PM, UX, backend, frontend, mobile) sharing one git repo and `_bmad-output`: parallel BMAD work collides on shared artifacts, hides Planning Artifact readiness, lets Stories start before dependent Layers exist, and lets Correct-Course leave docs/status/code describing different systems. Developers feel it most — bad starts and rewrite. Pilot estimate: ~50–60% of time on merges and drift cleanup. The Module makes coherent parallel BMAD work the default as an installable complementary package — never a Core BMAD fork.

## Capabilities

- **CAP-1** Ownership and artifact structure
  - **intent:** Team members can follow Module conventions for `_bmad-output` layout and soft-Claim paths or Story-related slices so parallel roles collide less.
  - **success:** Conventions cover Planning Artifact folders and high-churn status files without Core edits; conflicting Claim/edit produces a clear warning naming the other Claim; soft-check does not hard-lock git commit/push.

- **CAP-2** Native BMAD status visibility
  - **intent:** Team members or Build preflight can obtain and report standard BMAD Artifact Lifecycle Statuses for required Planning Artifacts and Stories that feed a Story’s Dependency Gate.
  - **success:** Status values match Core vocabularies for each artifact type; report names each required artifact/Story and pass/fail against the gate; Module does not invent a parallel Planning Artifact lifecycle enum.

- **CAP-3** Dependency Gates
  - **intent:** Team members can declare which Stories, Planning Artifacts, and Layers a Story depends on; Build (or equivalent Story start) Hard-Blocks until gates pass.
  - **success:** Dependencies live in Module-owned git-native data; every Story in `sprint-status` is enrolled (missing declaration = incomplete Hard Block, or explicit none); failed gate returns non-zero/blocked with actionable failing conditions; no undocumented override that skips Hard Block in v1.

- **CAP-4** Layer Order
  - **intent:** Team can declare an ordered list of Layers; Stories tagged with a Layer start only when earlier Layers satisfy the default ready rule (and any tighter FR-5 deps).
  - **success:** Layer Order stored git-natively; invalid/cyclic Layer order rejected; default Hard Block until every earlier-Layer Story in `sprint-status` is native status `done`; loosen only via documented audited project exceptions (see companion AD-7).

- **CAP-5** Correct-Course coherence
  - **intent:** After mid-flight plan change via Correct-Course, the team must complete impact review and status recalculation so Project Truth (docs, status, code) does not split before coherent merge / Build-ready.
  - **success:** Every `bmad-correct-course` run requires impact review + recalc; authoritative signal is Module `impact-review.yaml` (`open`|`cleared`); coherent-merge/Build-ready Hard-Blocks while required review is `open`; invalidated Stories move to non-executable native status defaulting to `backlog` (overridable in Module home; never invent `blocked`); git commit/push stay unrestricted.

- **CAP-6** Installable complementary Module
  - **intent:** Team can install the Module into a project that already has Core BMAD and use CAP-1–CAP-5 without editing installer-owned Core paths; Core workflows remain invokable with Module gates composed around them.
  - **success:** Documented install path exists; smoke check proves Core vendor files were not required to be modified; Hard Block attaches via `_bmad/custom` hooks (at minimum `bmad-build`, `bmad-build-auto`, `bmad-correct-course`), not Core source edits.

## Constraints

- Must not patch or fork Core BMAD; Hard Block via `_bmad/custom` skill hooks on every Module-supported Story execution entrypoint (min. `bmad-build`, `bmad-build-auto`) plus `bmad-correct-course` — never required git hooks for gates.
- Preflight-gate over shared truth only: evaluate and Hard-Block; must not become a second methodology runtime or derived readiness index SoT away from Core `_bmad-output` artifacts.
- All Module-owned state in one tree under `_bmad-output/` (seed `multi-user/`); plain text (YAML preferred, JSON allowed; Markdown prose appendix for impact review only); one shared gate evaluator CLI for status report, Build hooks, and coherent-merge checks.
- Write ownership: Module home = Module skills/scripts only; Planning Artifacts = humans + Core (Module reads statuses); Story status writes only on Correct-Course/recalc using native BMAD values.
- Correct-Course recalc default for invalidated Stories is native status `backlog`; project may override in Module home config to another native non-executable status only.
- Story ids in deps filenames, Claims Story slices, impact-review items, and Layer exceptions MUST equal `sprint-status` keys; Layer membership declared only in per-Story deps files.
- Readiness map maps artifact kinds → acceptable **native** BMAD statuses for Planning Artifact readiness only — must not redefine Story Layer `done`.
- Offline for CAP-1–CAP-5; no mandatory SaaS/network; no secrets beyond Core/git; gate preflight must stay a normal fast local check (no numeric SLA in v1).
- Semver for Module-home schema and gate behavior; incompatible changes bump major and ship migration note; declare supported Core BMAD major(s); breaking Core upgrades documented, not patched around.
- Architecture decisions AD-1–AD-12 in the companion spine are binding invariants for implementation shape (stack, structural seed, enforcement surface).

## Non-goals

- Smart merge assist for conflicting markdown/YAML (post-v1).
- Polished community documentation / wide-adoption packaging beyond minimal install path.
- Real-time collaborative cursors; SaaS collaboration product; enterprise ACL as collaboration model.
- Replacing git.
- Inventing parallel Planning Artifact status vocabulary (`draft|review|ready`).
- Hard file locks / exclusive Claim enforcement in v1.
- Patching or forking Core BMAD.
- Becoming a generic Spec Kit / AI-DLC product (pattern borrow OK; identity stays BMAD-fluent).
- Multi-repo / sibling-repo orchestration (v1 = single-repo Pilot).
- Ecosystem adoption metrics as v1 success criteria.

## Success signal

Pilot Team sustained merge/drift cleanup toward **15–25%** of working time (from ~50–60% estimate); fewer large shared-artifact merges and rewrites from early Story starts or post–Correct-Course inconsistency; after parallel work and course correction, docs/status/code align more often than they diverge — **without** requiring a Core BMAD patch or fork. Standard BMAD workflow time must not become significantly slower due to Module gates (SM-C1). Measure via the weekly Pilot diary in `pilot-ops.md`.

## Assumptions

- SM-1 ~50–60% baseline is Pilot Team estimate pending measurement.
- Developers are the primary sufferers; PM/UX participate.
- PRD open questions on Correct-Course trigger and coherent-merge signal are resolved by architecture: every `bmad-correct-course` run + authoritative `impact-review.yaml`.
