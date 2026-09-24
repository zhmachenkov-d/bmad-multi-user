# Epic 1 Context: Installable Module Foundation

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Deliver the installable complementary BMAD Module substrate so a Pilot Team can adopt multi-user coordination beside Core BMAD without patching or forking Core. This epic establishes Module home, a single shared gate evaluator CLI, custom hook templates for Build and Correct-Course, and an install path with a Core-untouched smoke check — the foundation later epics use for Claims, Dependency Gates, Layer Order, and impact review.

## Stories

- Story 1.1: Scaffold complementary Module package & Module home
- Story 1.2: Single gate evaluator CLI entrypoint
- Story 1.3: Custom hook templates for Build & Correct-Course
- Story 1.4: Install path docs & Core-untouched smoke check

## Requirements & Constraints

- Install into a project that already has Core BMAD; Module skills/scripts land only in Module-owned or project-custom locations — never require edits to installer-owned Core vendor paths.
- Core BMAD skills stay invokable; the Module adds gates/checks around them via composition, not by replacing Core source.
- F1–F5 substrate must work offline with no mandatory SaaS or always-on network.
- Gate/status checks on the hot path must feel like a normal fast local preflight (no separate multi-step ceremony); no hard wall-clock SLA in v1.
- Evaluator results must be both machine-readable and human-readable (pass/fail with reasons).
- Module-owned state must be plain text in git (YAML preferred; JSON allowed) suitable for PR review.
- No secrets beyond what Core BMAD / git already need.
- Module versioning: semver for Module-home schema and gate behavior; incompatible changes bump major and ship a migration note; declare supported Core BMAD major(s); breaking Core upgrades are documented, not silently patched.
- Success failure signal for the product: if teams must patch or fork Core BMAD for the Module to work, the Module has failed.

## Technical Decisions

- **Paradigm:** Preflight-gate over shared truth — evaluate and Hard-Block only; do not become a second methodology runtime or replace git / Core process ownership.
- **Stack:** Python ≥3.11; `uv` ~0.12.x; host = local git repo + Core BMAD (no SaaS runtime).
- **Module home:** Single tree under `_bmad-output/` (seed name `multi-user/`) holding all Module-owned state. Seed placeholders: `config.yaml`, `layer-order.yaml`, `claims.yaml`, `deps/`, `impact-review.yaml`.
- **Write ownership (substrate):** Module home = Module writes; Planning Artifacts and sprint-status = humans + Core (Module reads for later gates); never touch installer-owned Core paths.
- **Single evaluator:** One shared Python package / one CLI implements Hard Block rules. Status report, Build hooks, and coherent-merge checks must invoke that same entrypoint — no forked gate scripts. On this epic the CLI may be pass-substrate (“no gate rules loaded”) but must not duplicate logic into separate scripts.
- **Composition:** Hard Block attaches through `_bmad/custom/*.toml` hooks (e.g. `activation_steps_prepend`) on every Module-supported Story execution entrypoint — at minimum `bmad-build`, `bmad-build-auto`, and `bmad-correct-course`. Wrappers must not be the sole gate. Git commit/push stay unrestricted (no mandatory git hooks for Hard Block).
- **Package shape:** Installable complementary module = skills + scripts + template `_bmad/custom` hooks; run scripts via `uv run`.
- **Consistency:** Story ids elsewhere will equal `sprint-status` keys; dates in registries use ISO-8601; config overrides live in Module home only.

## Cross-Story Dependencies

- 1.2 requires the package scaffold from 1.1.
- 1.3 requires 1.1–1.2 (hooks call the same evaluator CLI).
- 1.4 documents and smoke-checks the full substrate from 1.1–1.3.
- Epics 2–4 assume this installable foundation (Module home, evaluator CLI, custom hooks) is present; they add Claims, gates/Layer Order, and Correct-Course impact review on top of it.
