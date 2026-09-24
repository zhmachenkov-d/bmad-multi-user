---
title: "1.1 Scaffold complementary Module package & Module home"
type: "feature"
created: "2026-09-24"
status: "done"
route: "dispatch"
review_loop_iteration: 0
baseline_commit: "1c15e2473ad67e5cebf26df7c8c0acf92fcf9924"
context:
  - "{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md"
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The Pilot repo has Core BMAD and WIP `skills/team-*` drafts, but no installable complementary Module package and no Module home under `_bmad-output/multi-user/`, so later gate/claim/layer work has nowhere durable to live without patching Core.

**Approach:** Scaffold an installable complementary Module package (`skills/` + `scripts/`) in a Module-owned location and seed `_bmad-output/multi-user/` with placeholder Module-home files — without touching installer-owned Core paths. Evaluator CLI, custom hooks, and install docs are out of scope (Stories 1.2–1.4).

**Decisions:**

- PACKAGE_ROOT: New top-level package at `packages/bmad-multi-user/` with `skills/` and `scripts/`; keep repo-root WIP `skills/` separate until a later migrate.
- WIP_TEAM_SKILLS: Leave `skills/team-*` and `planning-artifacts/team/` untouched in this story; Module home + new package scaffold only.

## Boundaries & Constraints

**Always:**

- Module home seed path is `_bmad-output/multi-user/` with placeholders: `config.yaml`, `layer-order.yaml`, `claims.yaml`, `impact-review.yaml`, and `deps/` (YAML plain text, PR-reviewable).
- Package root is `packages/bmad-multi-user/` with `skills/` and `scripts/` (Structural Seed shape).
- Skills/scripts land only in Module-owned or project-custom locations.
- Python ≥3.11 / `uv run` conventions for any script stubs; no SaaS/network requirement.

**Never:**

- Edit installer-owned Core: `_bmad/config.toml`, `_bmad/<module>/`, `_bmad/scripts/`, `_bmad/_config/`, `.agents/skills/bmad-*/**`.
- Implement gate evaluator CLI, `_bmad/custom` Build/Correct-Course hooks, or install/smoke docs (1.2–1.4).
- Invent a second Module home or keep Module state under `planning-artifacts/team/` as the SoT for this story.
- Modify, relocate, absorb, or delete existing `skills/team-*` / `planning-artifacts/team/` in this story.
- Replace or hard-lock git; no mandatory git hooks.

## I/O & Edge-Case Matrix

| Scenario             | Input / State                     | Expected Output / Behavior                                                                          | Error Handling                                  |
| -------------------- | --------------------------------- | --------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| Fresh scaffold       | Core BMAD present; no Module home | `_bmad-output/multi-user/` tree + package `skills/` + `scripts/` exist; Core vendor files unchanged | N/A                                             |
| Re-run / idempotent  | Placeholders already present      | No destructive overwrite of non-empty Module-home content; package dirs remain valid                | Leave existing content; do not wipe claims/deps |
| Core-untouched proof | Diff against vendor paths         | No required changes under installer-owned Core paths for scaffold to exist                          | Fail story if scaffold needs Core edits         |

</frozen-after-approval>

## Code Map

- `_bmad-output/planning-artifacts/architecture/.../ARCHITECTURE-SPINE.md` — Structural Seed + AD-3/AD-11 package & Module-home rules (reuse paths; do not invent alternate homes)
- `_bmad-output/implementation-artifacts/epic-1-context.md` — Epic constraints for installable substrate
- `_bmad-output/planning-artifacts/epics.md` — Story 1.1 AC source
- `_bmad-output/multi-user/` — **missing**; create Module home here
- `packages/bmad-multi-user/` — **missing**; create package root with `README.md`, `skills/.gitkeep`, `scripts/.gitkeep`
- `_bmad/custom/config.toml` — project-owned custom surface exists; **do not** add Build hooks here in 1.1
- `_bmad/{core,bmm,bmb,cis,bmad-loop}/`, `_bmad/scripts/`, `_bmad/_config/`, `.agents/skills/bmad-*/**` — **do not change**
- `skills/team-{claim,gates,ready,status}/` — WIP complementary skills; leave untouched this story
- `skills/reports/module-plan-multi-user.md` — older plan (`module_code: team`, state under `planning_artifacts/team/`); superseded by spine `multi-user/` for Module home — do not follow as SoT
- `.agents/skills/bmad-module-builder/assets/` — templates for setup/standalone modules; optional reference only
- No root `pyproject.toml` — prefer PEP 723 / `uv run` script style like `_bmad/scripts/*.py` when adding stubs later

## Tasks & Acceptance

**Execution:**

Idempotency: create if missing; if a target file already exists and is non-empty, leave it unchanged; never wipe `claims.yaml`, `deps/`, or other Module-home content.

Placeholder YAML rule: each Module-home file is valid YAML (`{}` or `null`) plus ≤10 lines of `#` purpose comments — no full schemas.

- [x] `_bmad-output/multi-user/config.yaml` -- create-if-missing placeholder for readiness-map overrides / project settings -- Module home SoT starts empty-but-valid
- [x] `_bmad-output/multi-user/layer-order.yaml` -- create-if-missing placeholder for ordered layers + loosen-exceptions shape -- later FR7/FR8 substrate
- [x] `_bmad-output/multi-user/claims.yaml` -- create-if-missing placeholder claims registry -- later soft-claim SoT (not `planning-artifacts/team/`)
- [x] `_bmad-output/multi-user/impact-review.yaml` -- create-if-missing placeholder documenting `status` open|cleared in comments -- later coherent-merge signal
- [x] `_bmad-output/multi-user/deps/.gitkeep` -- create-if-missing so empty deps tree is tracked -- enrollment lives here later; no per-story files required in 1.1
- [x] `packages/bmad-multi-user/README.md` -- create-if-missing short README: package layout (`skills/`, `scripts/`) and note that evaluator/hooks/install docs land in Stories 1.2–1.4 -- AD-11 package shape without Core edits
- [x] `packages/bmad-multi-user/skills/.gitkeep` -- create-if-missing so empty skills dir is tracked in git -- AC survives clean clone
- [x] `packages/bmad-multi-user/scripts/.gitkeep` -- create-if-missing so empty scripts dir is tracked in git -- evaluator CLI arrives in 1.2
- [x] Leave `skills/team-*` and `planning-artifacts/team/` unchanged -- per WIP_TEAM_SKILLS decision -- avoid half-migrate and dual SoT
- [x] Verify Core-untouched -- `git status` / path audit shows no installer-owned Core vendor file required for scaffold -- FR11 / NFR1

**Acceptance Criteria:**

- Given a project with Core BMAD installed, when the Module package scaffold is present at `packages/bmad-multi-user/`, then `skills/` and `scripts/` directories exist under that package (tracked in git) without requiring edits to installer-owned Core paths.
- Given the scaffold is applied, when inspecting `_bmad-output/multi-user/`, then `config.yaml`, `layer-order.yaml`, `claims.yaml`, `impact-review.yaml`, and a `deps/` directory exist as plain-text YAML-oriented Module-home placeholders suitable for PR review.
- Given the scaffold is complete, when reviewing the diff, then no installer-owned Core BMAD vendor file was modified as a prerequisite for the scaffold to be present, and existing `skills/team-*` / `planning-artifacts/team/` remain untouched.

### Review Findings

- [x] [Review][Defer] Pin PACKAGE_ROOT in epic-1-context [`_bmad-output/implementation-artifacts/epic-1-context.md:36`] — deferred: pre-existing continuity gap; epic was compiled before PACKAGE_ROOT froze; already tracked in deferred-work for Stories 1.2–1.4

**Rejected**

- false — Spec frontmatter `done` vs sprint `review`: sprint correctly awaits this review; changing frontmatter would edit the spec under review.
- false — `{}` vs `null` placeholders: Design Notes allow both; comments document intended shapes.
- false — README says “Installable”: product/shape term; Deferred section already points install/smoke to Story 1.4.
- false — Empty Spec Change Log: template stays empty until a bad_spec loopback.
- false — Fail-closed when Core absent: no executable scaffold in this story; AC preconditions Core installed.
- low (rejected) — Code Map still labels paths **missing** / ellipsis spine path / thin Verification Commands: fix would edit this build’s spec; presence + Core-untouched commands match AC.
- low (rejected) — `deps/` lacks enrollment README / Module home lacks README: not in 1.1 AC; enrollment and Hard Block arrive later; package README + Design Notes cover SoT.

## Implementation Notes

- Created `_bmad-output/multi-user/` placeholders (`{}` / `null` + short comments) and `packages/bmad-multi-user/` with README + `skills/.gitkeep` + `scripts/.gitkeep`.
- Left `skills/team-*`, `planning-artifacts/team/`, and installer-owned Core paths untouched.
- Verification: presence checks exit 0; Core `git status` empty; YAML parse OK; create-if-missing re-check left hashes unchanged (idempotent).

## Spec Change Log

## Review Triage Log

- false — Blind: Spec Change Log empty mid-scaffold — Template requires empty until first bad_spec loopback; not a defect.
- false — Blind: Review Triage Log empty at review start — Expected until this pass fills it; now populated.
- false — Blind: Spec `in-review` vs sprint vocabulary `review` — Different files use different vocabularies by design; map via sprint sync, not rename.
- false — Blind: `impact-review.yaml` uses `null` while siblings use `{}` — Design Notes allow both; file comments document `status: open|cleared`.
- false — Blind: No install identity (semver/pyproject/manifest) — Intent defers install docs/smoke to Story 1.4; layout-only scaffold is in scope.
- maybe-false → carried as defer — Blind: epic-1-context omits `packages/bmad-multi-user/` — Real continuity gap for 1.2+; not required by 1.1 AC; deferred.
- low (rejected) — Blind: Verification Commands omit YAML-parse/idempotency — Fix would edit this build's Verification section; notes already record the checks ran.
- low (rejected) — Blind: Code Map ellipsis path to ARCHITECTURE-SPINE — Fix would edit this build's spec Code Map.
- low (rejected) — Blind: Code Map still labels Module home/package **missing** (also verification-gap other) — Fix would edit this build's spec Code Map.
- low (rejected) — Blind: deps/ lacks enrollment README — Convention lives in architecture; everyday 1.1 users won't hit Hard Block yet.
- low (rejected) — Blind: Module home lacks README — Package README + Design Notes cover single-home SoT for this story.
- low (rejected) — Blind: Missing blank line before Spec Change Log — Cosmetic scanability only.
- low (rejected) — Blind: AC/Verification omit ≤10-comment YAML rule assertion — Fix would edit this build's spec.
- medium (patch) — Blind: sprint-status still `in-progress` while implementation is complete and spec is `in-review` — Updated story key to `review`.
- (edge-case-hunter) — No findings.
- (verification-gap) — No verification gaps; other Code Map finding rejected as above.

## Design Notes

Module home name `multi-user/` is the architecture seed (rename later OK if single-home invariant holds). Do not continue `planning-artifacts/team/` as Module SoT.

Epic 1.1 wording about a “documented complementary-module path” is deferred to Story 1.4; this story’s acceptance is package layout + Module-home placeholders only.

Minimal placeholders: valid YAML `{}` or `null` plus ≤10 lines of `#` purpose comments — not full schemas. Real enrollment files and evaluator come in later stories.

Golden tree after 1.1:

```text
_bmad-output/multi-user/
  config.yaml
  layer-order.yaml
  claims.yaml
  impact-review.yaml
  deps/.gitkeep
packages/bmad-multi-user/
  README.md
  skills/.gitkeep
  scripts/.gitkeep
```

## Verification

**Commands:**

- `test -f _bmad-output/multi-user/deps/.gitkeep && test -f _bmad-output/multi-user/config.yaml && test -f _bmad-output/multi-user/layer-order.yaml && test -f _bmad-output/multi-user/claims.yaml && test -f _bmad-output/multi-user/impact-review.yaml` -- expected: exit 0
- `test -f packages/bmad-multi-user/README.md && test -f packages/bmad-multi-user/skills/.gitkeep && test -f packages/bmad-multi-user/scripts/.gitkeep` -- expected: exit 0
- `git status --short -- _bmad/config.toml _bmad/config.user.toml _bmad/core _bmad/bmm _bmad/bmb _bmad/cis _bmad/bmad-loop _bmad/scripts _bmad/_config .agents/skills` -- expected: empty (no vendor changes)

**Manual checks (if no CLI):**

- Open Module-home YAMLs: plain text, `{}`/`null` + short `#` comments only, no secrets.
- README states layout and defers evaluator/hooks/install docs to 1.2–1.4.
- Confirm Build/Correct-Course hook tomls were not added under `_bmad/custom/` in this story.
