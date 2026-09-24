# bmad-multi-user

Installable complementary BMAD Module package for multi-user coordination beside Core BMAD.

## Layout

- `skills/` — Module skills (status, claim, deps, Correct-Course assist); populated in later stories
- `scripts/` — shared gate evaluator CLI and helpers (`uv run`); evaluator arrives in Story 1.2

Module-owned state lives under `_bmad-output/multi-user/` (not in this package).

## Deferred (Stories 1.2–1.4)

- Gate evaluator CLI entrypoint (1.2)
- Custom `_bmad/custom` hooks for Build / Correct-Course (1.3)
- Install path docs and Core-untouched smoke check (1.4)

Do not edit installer-owned Core BMAD paths to use this package.
