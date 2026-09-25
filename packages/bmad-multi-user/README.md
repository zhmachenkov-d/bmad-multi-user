# bmad-multi-user

Installable complementary BMAD Module package for multi-user coordination beside Core BMAD.

## Layout

- `skills/` — Module skills (status, claim, deps, Correct-Course assist); populated in later stories
- `scripts/gate_eval.py` — single shared gate evaluator CLI (`uv run`); pass-substrate in Story 1.2

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

Real Hard Block rules land in later epics; custom hooks in Story 1.3; install-layout docs in Story 1.4.

## Deferred (Stories 1.3–1.4)

- Custom `_bmad/custom` hooks for Build / Correct-Course (1.3)
- Install path docs and Core-untouched smoke check (1.4)

Do not edit installer-owned Core BMAD paths to use this package.
