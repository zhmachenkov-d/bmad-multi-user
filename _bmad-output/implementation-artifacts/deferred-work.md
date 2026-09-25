# Deferred Work

- source_spec: `_bmad-output/implementation-artifacts/spec-1-1-scaffold-complementary-module-package-module-home.md`
  summary: Pin decided package root `packages/bmad-multi-user/` in `epic-1-context.md` Technical Decisions so Stories 1.2–1.4 inherit the SoT path.
  evidence: Epic context was compiled before PACKAGE_ROOT was frozen; it still describes only “skills + scripts + hooks” without the concrete package directory chosen in 1.1.
  status: resolved in Story 1.2 (`epic-1-context.md` Package shape now pins `packages/bmad-multi-user/` and `scripts/gate_eval.py`)

## Deferred from: code review of spec-1-1-scaffold-complementary-module-package-module-home.md (2026-09-24)

- Pin `packages/bmad-multi-user/` as PACKAGE_ROOT in `epic-1-context.md` Technical Decisions (Package shape) so Stories 1.2–1.4 inherit the concrete SoT path — continuity gap confirmed by Blind Hunter + Edge Case Hunter; not required by 1.1 AC. **Resolved in Story 1.2.**

## Deferred from: oneshot review of spec-1-2-single-gate-evaluator-cli-entrypoint.md (2026-09-25)

- source_spec: `_bmad-output/implementation-artifacts/spec-1-2-single-gate-evaluator-cli-entrypoint.md`
  summary: Document or stub the future Hard Block plug-in site on `evaluate()` so Stories 1.3 / Epic 3 know where rules attach.
  evidence: Pass-substrate only discards `project_root`/`story`; no named extension seam yet — intentional for 1.2 scope; hooks and real rules come later.
  status: open

## Deferred from: code review of spec-1-2-single-gate-evaluator-cli-entrypoint.md (2026-09-25)

- JSON field semantics (`message` vs `warnings` vs `reasons`) for Hard Block callers — undefined beyond pass-substrate; leave until Epic 3 rules define which field carries block reasons. Evidence would settle earlier only if a hook already consumes these fields differently.
