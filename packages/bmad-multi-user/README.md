# bmad-multi-user

Installable complementary BMAD Module package for multi-user coordination beside Core BMAD.

## Layout

- `skills/` — Module skills (status, claim, deps, Correct-Course assist); populated in later stories
- `scripts/gate_eval.py` — single shared gate evaluator CLI (`uv run`); pass-substrate in Story 1.2
- `templates/_bmad/custom/` — team hook templates for `bmad-build`, `bmad-build-auto`, and `bmad-correct-course` (Story 1.3)

Module-owned state lives under `_bmad-output/multi-user/` (not in this package).

## Evaluator (Story 1.2)

From the repository root:

```bash
uv run packages/bmad-multi-user/scripts/gate_eval.py --project-root .
# equivalent: -p .
# optional: --story <sprint-status-key> (echoed in JSON; unused for gating yet)
```

- **Stdout:** JSON `{ok, mode, message, reasons, story, version, warnings, error}` (also on usage/runtime errors)
- **Stderr:** `warning:` lines + human one-liner (success), or `error:` text (failure)
- **Exit codes:** `0` pass (may include warnings), `1` fail/block, `2` usage/runtime error

Self-check:

```bash
uv run packages/bmad-multi-user/scripts/tests/test_gate_eval.py
```

## Custom hooks (Story 1.3)

Canonical templates (install by copying into the project’s `_bmad/custom/`):

- `templates/_bmad/custom/bmad-build.toml`
- `templates/_bmad/custom/bmad-build-auto.toml`
- `templates/_bmad/custom/bmad-correct-course.toml`

Each prepends one activation step that runs the shared `gate_eval.py` CLI and HALTs on non-zero exit, unparseable/missing `ok`, or `ok: false`. Pass-substrate (exit 0 with warnings) continues after surfacing warnings. Do not edit installer-owned `.agents/skills/bmad-*/**` — compose via `_bmad/custom` only.

Templates under `templates/_bmad/custom/` are the SoT; Pilot `_bmad/custom/*.toml` are create-if-missing copies — re-copy from templates after template fixes. In this Pilot repo the three files are already installed under `_bmad/custom/`. Full install path + Core-untouched smoke check: Story 1.4.

Real Hard Block rules land in later epics.

## Deferred (Story 1.4)

- Install path docs and Core-untouched smoke check (1.4)

Do not edit installer-owned Core BMAD paths to use this package.
