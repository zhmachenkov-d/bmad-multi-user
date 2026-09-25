---
title: "1.2 Single gate evaluator CLI entrypoint"
type: "feature"
created: "2026-09-25"
status: "done"
route: "oneshot"
review_loop_iteration: 0
baseline_commit: "d17c53a9c8139026ea3356f78c8083dd33088d03"
context:
  - "{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md"
  - "{project-root}/_bmad-output/implementation-artifacts/spec-1-1-scaffold-complementary-module-package-module-home.md"
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Story 1.1 left `packages/bmad-multi-user/scripts/` empty, so Build hooks, status reports, and coherent-merge checks have no shared Hard Block entrypoint to call later (AD-5).

**Approach:** Add one stdlib PEP 723 evaluator CLI under `packages/bmad-multi-user/scripts/`, runnable via `uv run`, that returns structured pass/fail with machine-readable JSON on stdout and a human-readable summary — pass-substrate (“no gate rules loaded”) only; no real gate rules, hooks, or forked CLIs.

**Decisions:**

- ENTRYPOINT: `packages/bmad-multi-user/scripts/gate_eval.py` (snake_case; single CLI; helpers may be sibling modules, never a second public gate CLI).
- PACKAGING: PEP 723 inline metadata, `requires-python = ">=3.11"`, stdlib only — no `pyproject.toml` in this story.
- OUTPUT: JSON on stdout for success and usage/runtime errors (`ok`, `mode`, `message`, `reasons`, `story`, `version`, `warnings`, `error`); human lines on stderr (`warning:` / message, or `error:`). Exit codes: `0` pass (may warn), `1` fail/block, `2` usage/runtime error (script-standards).
- CLI SURFACE: `--project-root` / `-p` required; optional `--story` echoed in JSON as `story` and not used for gating until Hard Block rules. `--help` via argparse. No network, no interactive prompts. `version` is CLI constant `0.1.0`.
- PASS_SUBSTRATE: `ok: true`, `mode: "pass_substrate"`, exit `0`, plus non-empty `warnings[]` and stderr `warning:` so callers see rules are inactive (not silent green). Real Hard Block rules are out of scope.
- CONTINUITY: Pin `packages/bmad-multi-user/` as PACKAGE_ROOT in `epic-1-context.md` Technical Decisions (deferred from 1.1). Update package README to name the entrypoint. Leave `skills/team-*` and Core vendor paths untouched.

**Always:**

- Single shared evaluator entrypoint; status/Build/coherent-merge must call this same CLI later (AD-5).
- Invokable without editing installer-owned Core BMAD paths.
- Python ≥3.11 / `uv run`; offline; fast local preflight feel.

**Never:**

- Implement real Dependency Gate / Layer / Claims / impact-review Hard Block rules.
- Add `_bmad/custom` Build/Correct-Course hooks (Story 1.3) or install/smoke docs (Story 1.4).
- Fork gate logic into a second CLI; invent parallel lifecycle status enums; edit Core vendor paths; migrate/absorb `skills/team-*`.

</frozen-after-approval>

## Implementation Notes

- Added `packages/bmad-multi-user/scripts/gate_eval.py` (PEP 723, stdlib, argparse) with `evaluate()` returning pass-substrate payload; removed empty `scripts/.gitkeep`.
- Self-check at `packages/bmad-multi-user/scripts/tests/test_gate_eval.py` (happy path with `-p`/`--story`, full JSON fields, missing root → 2 + empty stdout, missing `--project-root` → 2).
- README documents invocation, exit codes, `--story`, and self-check command.
- Pinned PACKAGE_ROOT + gate_eval path in `epic-1-context.md`; marked matching deferred-work entries resolved.
- Review patches: `--help` epilog documents pass-substrate + JSON schema; self-check and README contracts tightened.
- Verified: CLI exit 0 + JSON; self-test `ok`; Core vendor path audit empty.
- Human renegotiation during walkthrough: added `story`/`version`/`warnings`/`error` to JSON; pass-substrate warning mode; JSON on exit-2 paths; clarified `--story` as echo-only until gating.
- Review patches (post CR): empty `-p` rejected; OSError → exit-2 JSON; usage errors preserve `--story`; self-check covers no-`--story`, `version == 0.1.0`, stderr `error:`; deferred-work seam entry marked `status: open`.

## Review Triage Log

- medium (patch) — Blind: deferred-work still listed open PACKAGE_ROOT pin — Annotated resolved in deferred-work.md after epic-1-context pin.
- false — Blind: oneshot spec lacks Tasks/AC/Code Map like 1.1 — Oneshot route intentionally omits those sections; Intent + Implementation Notes are the contract.
- medium (patch) — Blind: self-check thin on exit 2 / JSON fields / `-p` / `--story` — Strengthened test_gate_eval.py assertions.
- medium (patch) — Blind: README omitted exit codes / `--story` / self-check — Expanded README Evaluator section.
- low (rejected) — Blind: README lacks PACKAGE_ROOT-relative / install-layout examples — Story 1.4 owns install docs; monorepo path is correct for this pilot repo.
- medium (patch) — Blind: `--help` omitted pass-substrate / JSON schema — Added argparse epilog.
- low (rejected) — Blind: usage/runtime errors emit no JSON on stdout — Frozen contract: JSON for evaluation results; exit 2 + stderr for usage/runtime; callers check returncode first.
- false — Blind: status still in-progress while notes claim verified — Mid-oneshot before Finalize; now set `done` / sprint `review`.
- maybe-false → defer — Blind: `evaluate()` lacks named Hard Block plug-in seam — Deferred; 1.2 pass-substrate only; rules attach in later epics.

### Review Findings

- [x] [Review][Patch] Self-check misses documented CLI contract (no-`--story` path, stderr `error:` prefix, `version == "0.1.0"`) [`packages/bmad-multi-user/scripts/tests/test_gate_eval.py`]
- [x] [Review][Patch] Empty `--project-root` resolves to cwd and exits 0 [`packages/bmad-multi-user/scripts/gate_eval.py:120`]
- [x] [Review][Patch] `resolve()` / `is_dir()` OSError escapes exit-2 JSON path [`packages/bmad-multi-user/scripts/gate_eval.py:120`]
- [x] [Review][Patch] Usage-error JSON drops provided `--story` [`packages/bmad-multi-user/scripts/gate_eval.py:81`]
- [x] [Review][Patch] Deferred-work Hard Block seam entry lacks `status:` [`_bmad-output/implementation-artifacts/deferred-work.md`]
- [x] [Review][Defer] JSON field semantics (`message` vs `warnings` vs `reasons`) undefined for Hard Block callers [`packages/bmad-multi-user/scripts/gate_eval.py`] — deferred: intentional until real gate rules land (Epic 3); pass-substrate leaves `reasons` empty by design

#### Rejected

- false — Exit code `1` documented but unreachable: `main` already returns `1` when `ok` is false (`gate_eval.py:140`); pass-substrate correctly never sets that.
- false — Spec `status: done` vs sprint `review`: expected BMAD state while code review runs.
- false (spec edit) — Implementation Notes / Review Triage Log contradict exit-2 JSON contract: fix would edit the spec under review; frozen OUTPUT + code/README/tests already agree on JSON on exit 2.
- low — Self-check uses `sys.executable` not `uv run`: stdlib script behaves the same; forcing `uv` adds ceremony without catching a real regression.
- low — README Layout omits `scripts/tests/`: Evaluator section already documents the self-check path.
- low — stdout UTF-8 reconfigure without matching stderr: rare encoding divergence; not worth dual-stream complexity now.
