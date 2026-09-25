---
title: "1.3 Custom hook templates for Build & Correct-Course"
type: "feature"
created: "2026-09-25"
status: "done"
route: "oneshot"
review_loop_iteration: 0
baseline_commit: "379b7615d485b1248cf9f9dc69a12c0b2d98c675"
context:
  - "{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md"
  - "{project-root}/_bmad-output/implementation-artifacts/spec-1-2-single-gate-evaluator-cli-entrypoint.md"
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Story 1.2 shipped `gate_eval.py`, but Hard Block never runs on Build / Correct-Course because no `_bmad/custom` hooks call that CLI (AD-2 / FR12).

**Approach:** Ship identical team-hook templates for `bmad-build`, `bmad-build-auto`, and `bmad-correct-course` that prepend a single `uv run` of the shared evaluator; install the same three files into this Pilot’s `_bmad/custom/` so composition is live without editing Core vendor skills.

**Decisions:**

- TEMPLATES: Canonical copies under `packages/bmad-multi-user/templates/_bmad/custom/` as `bmad-build.toml`, `bmad-build-auto.toml`, `bmad-correct-course.toml` (mirrors install destination; not under `skills/`).
- INSTALL_PILOT: Copy the same three files into `_bmad/custom/` in this repo (create-if-missing; if a non-empty team hook already exists, leave it unchanged and note in Implementation Notes — do not merge or overwrite).
- HOOK_BODY: Each file is sparse — only `[workflow]` + `activation_steps_prepend` with one instruction string that runs `uv run "{project-root}/packages/bmad-multi-user/scripts/gate_eval.py" --project-root "{project-root}"`, then HALTs the skill if exit code ≠ 0 or stdout JSON has `ok` false. No `--story` (unknown at prepend). Do not fork gate logic into the TOML.
- COMPOSITION: Hooks are LLM activation instructions (not auto-shell); they must compose around Core skills via the existing customize merge (list append). Never edit `.agents/skills/bmad-*/**` or other installer-owned Core paths.
- DOCS: Update package README to name the three templates, the Pilot install location, and that full install/smoke docs are Story 1.4. No install script in this story.
- CONTINUITY: Reuse Story 1.2 ENTRYPOINT path and pass-substrate behavior (exit 0 with warnings continues Build). Leave deferred Hard Block plug-in-site / JSON field semantics for Epic 3.

**Always:**

- Same evaluator CLI for all three hooks (AD-5); no second gate script.
- Core skills remain invokable; hooks compose, not replace.
- Offline; no mandatory git commit/push hooks for Hard Block (AD-2).

**Never:**

- Real Hard Block rules, evaluator API changes, or Story 1.4 install/smoke ceremony.
- Edit vendor Core customize.toml / SKILL.md; add personal `*.user.toml` hooks; mandatory git hooks; absorb `skills/team-*`.

</frozen-after-approval>

## Implementation Notes

- Added canonical templates under `packages/bmad-multi-user/templates/_bmad/custom/` for `bmad-build`, `bmad-build-auto`, `bmad-correct-course` — each sparse `[workflow].activation_steps_prepend` calling shared `gate_eval.py` with HALT on non-zero / unparseable / `ok` false; surface warnings on pass-substrate continue.
- Pilot install: `_bmad/custom/` had no existing team hooks; copied all three templates unchanged (create-if-missing). Templates remain SoT; Pilot copies re-synced after review patches.
- README documents templates path (all three skills), Pilot install location, SoT/re-copy note, and defers full install/smoke to Story 1.4.
- Verified: TOML parse OK for templates + install copies; `resolve_customization.py` merges prepend for `bmad-build`, `bmad-build-auto`, and `bmad-correct-course` (1 step each); `gate_eval` exit 0 pass-substrate.
- Core-untouched audit: `git status --short` on `.agents/skills/bmad-{build,build-auto,correct-course}`, `_bmad/scripts`, `_bmad/core`, `_bmad/bmm`, `_bmad/config.toml` — empty (exit 0).
- Review patches: fail-closed parse rules; PACKAGE_ROOT retarget comments; README Layout + SoT alignment; Implementation Notes evidence for all three resolvers.

## Review Triage Log

- medium (patch) — Blind: hardcoded Pilot PACKAGE_ROOT path undocumented in TOML — Added retarget comment pointing to Story 1.4.
- medium (patch) — Blind: Implementation Notes only verified `bmad-build` resolver — Ran resolver for `bmad-build-auto` and `bmad-correct-course`; notes updated.
- medium (patch) — Blind: no fail-closed on empty/non-JSON/missing `ok` — Strengthened activation instruction.
- low (patch) — Blind: README Layout omitted `bmad-build-auto` — Fixed Layout bullet.
- false — Blind: README lacks concrete `cp` commands — Intent defers full install docs to Story 1.4; file list + Pilot install note is in scope.
- low (patch) — Blind: no Pilot↔template alignment note — README states templates are SoT; re-copy after template fixes.
- medium (patch) — Blind: pass-substrate may swallow warnings — Hook now requires surfacing stderr `warning:` / JSON `warnings` before continue.
- false — Blind: Approach says “identical” but halt labels differ — Decisions require same CLI + HALT rules; only skill name in halt sentence may differ (parity comment added).
- low (rejected) — Blind: README omits “not git hooks” restatement — Intent Always + AD-2 already cover; Story 1.4 owns install ceremony surface.
- low (patch) — Blind: Core-untouched asserted without audit command — Recorded empty `git status` audit paths in Implementation Notes.
