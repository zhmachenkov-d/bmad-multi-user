# Technology Freshness Review — Architecture Spine (BMAD Multi-User)

**Reviewed:** 2026-09-24  
**Spine:** `ARCHITECTURE-SPINE.md` (updated 2026-09-24)  
**Memlog claim:** `.memlog.md` line 24 — `uv ~0.12.x (verified web 2026-09)`  
**Methods:** Web search (uv, PEP 723, BMAD customize/docs, BMad Builder module distribution), live workspace checks (`uv --version`, `python3 --version`), inspection of `_bmad/scripts/` and installed skills in this repo.

---

## Verdict

**Mostly verified — acceptable for draft spine with minor freshness notes.**

Every **versioned** stack row (Python, uv) is directionally correct and aligns with Core BMAD script conventions in this project. Composition surfaces (`_bmad/custom/*.toml`, `bmad-build`, `bmad-correct-course`, complementary module packaging) are **confirmed** against upstream BMAD documentation and the installed tree. No invented frameworks or deprecated products were found in the Stack table.

Remaining gaps are **operational pinning** (uv patch drift, devcontainer “latest” vs `~0.12.x`), **one Core script metadata outlier** (`memlog.py` PEP 723 floor), and **deferred / unspecified** items the spine correctly leaves to implementation (exact readiness-map rows, Core BMAD major pin, `sprint-status` file path). There is **no web-application greenfield starter** in the spine; the relevant “starter” substrate is **Core BMAD + BMad Builder module install**, which was checked against current docs.

---

## Committed technology inventory

| Source | Technology / decision | Version or shape |
| --- | --- | --- |
| Stack | Python | `>=3.11` |
| Stack | uv | `~0.12.x` (spine: “verified 2026-09”) |
| Stack | Module state | YAML; Markdown for impact-review |
| Stack | Host | Local git + Core BMAD (offline) |
| Stack | Composition | `_bmad/custom/*.toml` hooks |
| AD-2 | Hook targets | `bmad-build`, `bmad-correct-course`; `activation_steps_prepend` |
| AD-5 | Gate runtime | Single shared **Python** script/library; `uv run` |
| AD-10 | Status vocabulary | Native BMAD statuses only (e.g. story `done`) |
| AD-11 | Packaging | Installable complementary BMAD module (skills + scripts + hook templates) |
| Structural seed | Hook files | `_bmad/custom/bmad-build.toml`, `bmad-correct-course.toml` |
| Structural seed | Module home | `_bmad-output/multi-user/` (seed name) |
| Memlog | Anti-patterns excluded | No Node/Go gate runtime; no mandatory network service |

---

## Verification matrix

### Python `>=3.11`

| Check | Result | Evidence |
| --- | --- | --- |
| Core BMAD scripts in this repo | **Confirmed** | `_bmad/scripts/resolve_config.py`, `resolve_customization.py`, `render_skill.py` declare PEP 723 `# requires-python = ">=3.11"` and document `tomllib` requirement. |
| Memlog alignment | **Partial mismatch in Core** | `_bmad/scripts/memlog.py` declares `# requires-python = ">=3.8"` while other central scripts require 3.11+. Spine’s `>=3.11` matches the **gate-relevant** scripts, not every script file. |
| Pilot dev environment | **Compatible, not cited in spine** | `.devcontainer/Dockerfile` uses `python:1-3.12-bookworm`; live shell: `Python 3.12.11`. Satisfies `>=3.11` but spine does not document 3.12 as the pilot default. |
| Web (Python release policy) | **Not re-checked** | Constraint is a minimum, not a pinned release; no spine claim that “3.11 is latest.” Acceptable without a dated web pass. |

**Flag (low):** Implementers should treat **3.11+** as the module contract; note `memlog.py` metadata is looser than sibling scripts (installer-owned path — do not edit vendor; module scripts should still declare `>=3.11` consistently).

---

### uv `~0.12.x`

| Check | Result | Evidence |
| --- | --- | --- |
| Memlog “verified web 2026-09” | **Substantiated** | PyPI / Astral changelog: **0.12.17** (2026-09-18); **0.12.18** (2026-09-22, security fix on Windows wheel install). Both remain **0.12.x**. |
| Live workspace | **Within range, not latest patch** | `uv 0.12.17` in devcontainer at review time. |
| Devcontainer pin | **Drift from spine wording** | `.devcontainer/features/uv` option default is `"latest"`, not `~0.12.x`. Post-create uses `uv sync` only when `pyproject.toml` / lock exists (this repo has **no** root `pyproject.toml` at review time). |
| Usage pattern | **Confirmed** | Skills invoke `uv run {project-root}/_bmad/scripts/...` and module-builder templates use `uv run` for merge scripts; `bmad-workflow-builder/references/script-standards.md` mandates Python + `uv run`. |
| PEP 723 | **Confirmed current** | PEP 723 (inline script metadata) Final; [uv scripts guide](https://docs.astral.sh/uv/guides/scripts/) documents `# /// script` blocks matching Core scripts. |

**Flag (low):** Spine verification date predates **0.12.18** by two days; tilde range still valid. For reproducible Pilot CI, pin `uv` to a specific 0.12 patch (e.g. `0.12.18`) in devcontainer or docs — spine does not require this yet.

---

### YAML and Markdown (state formats)

| Check | Result | Evidence |
| --- | --- | --- |
| Fit for git-native module home | **Confirmed** | Standard practice; sprint tooling already uses YAML (`sprint-status.yaml` in bmad-sprint-planning references). |
| Parser dependency | **Unspecified in spine (OK)** | Spine does not commit to PyYAML vs ruamel; implementation choice. Gate evaluator will need a YAML library via PEP 723 `dependencies` when built — not a spine freshness defect. |

---

### Host platform — local git + Core BMAD (no SaaS)

| Check | Result | Evidence |
| --- | --- | --- |
| Project layout | **Confirmed** | `_bmad/config.toml` sets `output_folder`, `planning_artifacts`, `implementation_artifacts` under `_bmad-output/`. |
| Module home under `_bmad-output` | **Confirmed** | Aligns with `[core] output_folder` and BMM paths; seed `multi-user/` is convention only (memlog assumption). |
| Devcontainer boilerplate | **Not in spine stack** | Devcontainer enables Node LTS and exposes ports 3000/8000/5173 — typical template noise for a BMAD-only module. **Not a spine contradiction** (spine excludes SaaS runtime) but **not reality-checked against spine** because spine never claims a web stack. |

---

### `_bmad/custom/*.toml` and `activation_steps_prepend`

| Check | Result | Evidence |
| --- | --- | --- |
| Mechanism exists | **Confirmed (web + repo)** | [Customize BMad](https://docs.bmad-method.org/customize/customize-bmad/) documents `[workflow] activation_steps_prepend` / `_append`. |
| Override file naming | **Confirmed (repo)** | `resolve_customization.py` looks for `_bmad/custom/{skill_name}.toml`. `bmad-build/customize.toml` documents `_bmad/custom/bmad-build.toml`. |
| Hook file names in structural seed | **Confirmed** | `bmad-build.toml` and `bmad-correct-course.toml` match skill directory names present under `.agents/skills/`. |

---

### Target skills: `bmad-build`, `bmad-correct-course`

| Check | Result | Evidence |
| --- | --- | --- |
| Installed in workspace | **Confirmed** | `.agents/skills/bmad-build/`, `.agents/skills/bmad-correct-course/` with `SKILL.md` and `[workflow]` customize surfaces. |
| Hook integration point | **Confirmed** | Both skills’ workflows reference `{workflow.activation_steps_prepend}` (e.g. `bmad-build/workflow.md`). |
| Correct-Course scope vs spine | **Process fit** | Help CSV describes Correct Course as mid-sprint change assessment; spine extends with mandatory impact review — product decision, not a stale tech reference. |

---

### Native BMAD statuses (AD-10)

| Check | Result | Evidence |
| --- | --- | --- |
| Story statuses | **Confirmed (repo)** | `bmad-sprint-planning/scripts/sprint_plan.py`: `backlog`, `ready-for-dev`, `in-progress`, `review`, `done`. Spine Layer rule references `done`. |
| Planning artifact statuses | **Confirmed (repo)** | `bmad-architecture/assets/spine-template.md`: `status: draft · final`. Memlog examples (“PRD final”, “brief complete”) are illustrative; **exact readiness-map rows explicitly deferred** in spine § Deferred. |
| Invented `draft\|review\|ready` for artifacts | **Correctly rejected in spine** | AD-10 prevents parallel enums. |

**Note:** Spine does not pin **`sprint-status` path**; in this project it resolves to `{implementation_artifacts}/sprint-status.yaml` via BMM config — implementation detail, not verified as a spine version claim.

---

### Installable complementary BMAD module (AD-11)

| Check | Result | Evidence |
| --- | --- | --- |
| Packaging path still supported | **Confirmed (web)** | [BMad Builder — Distribute Your Module](https://bmad-builder-docs.bmad-method.org/how-to/distribute-your-module/): `npx bmad-method install --custom-source …`, setup skill or standalone self-registration, `module.yaml` + `module-help.csv`. |
| Repo has builder skill | **Confirmed** | `.agents/skills/bmad-module-builder/` and setup-skill template with `merge-config.py`, `merge-help-csv.py`, `uv run`. |
| Structural seed vs Builder output | **Conceptual match** | Spine shows generic `<module-package>/skills` + `scripts/`; Builder may add `{code}-setup` skill and marketplace manifest — **additive**, not conflicting. Spine does not name `npx bmad-method` or marketplace.json (distribution detail). |

**Flag (informational):** When implementing FR-11/12, follow **current** Module Builder (CM) output rather than treating the spine ASCII tree as the only layout; run **Validate Module (VM)** before Pilot.

---

### Explicit exclusions (no Node/Go gate runtime)

| Check | Result | Evidence |
| --- | --- | --- |
| Core gate pattern | **Confirmed** | Central scripts are Python; workflow builder script standards discourage bash for portability. |
| Node in devcontainer | **Present but out of scope** | Node LTS feature exists for generic devcontainer template; spine excludes Node for **gate runtime**, not from entire monorepo future. |

---

## Greenfield / starter defaults

The spine is **not** anchored to a web framework starter (Next, Vite app template, etc.). Its substrate is:

1. **Core BMAD install** — already present in this workspace (`_bmad/`, `.agents/skills/`).
2. **Complementary module** — to be produced via BMad Builder patterns above.
3. **Script execution** — PEP 723 + `uv run`, matching live Core skills.

**Checked:** BMAD customize hook merge order and install flow against 2026 docs; **not** checked against a separate “application starter” because the spine does not reference one.

**Project-only defaults not reflected in spine:** Python **3.12** base image, uv **latest** feature flag, optional Node/npm post-create — acceptable omission for a module architecture spine; call out if Pilot docs promise environment parity with the Stack table.

---

## Items correctly deferred (not freshness failures)

- Exact YAML micro-schemas for claims/deps/impact-review  
- Default readiness-map rows per artifact kind  
- Core BMAD **major** compatibility matrix (NFR-2 declared, no numeric major in spine)  
- Module home rename from `multi-user/`  

These are **intentionally unverified** at spine altitude.

---

## Summary of flags

| Severity | Item | Recommendation |
| --- | --- | --- |
| Low | uv patch drift (0.12.17 env vs 0.12.18 current in 0.12 line) | Refresh memlog/stack footnote or pin CI/devcontainer to a specific 0.12 patch. |
| Low | Devcontainer uv = `latest` vs spine `~0.12.x` | Align feature option or document that tilde is advisory. |
| Low | `memlog.py` PEP 723 `>=3.8` vs spine `>=3.11` | Module-owned scripts use `>=3.11`; do not rely on memlog metadata alone for floor. |
| Informational | Devcontainer Node/ports vs offline module spine | Ignore for gate design; strip from Pilot image if distracting. |
| Informational | Module package layout vs BMad Builder CM output | Implement using Builder VM-validated layout. |
| None | Web app starter defaults | N/A — spine does not claim a web starter. |

---

## Conclusion

The spine’s **committed technology choices are grounded**: Python/uv match Core BMAD script practice in this repo; hook and skill names match installed artifacts and official customize documentation; native status vocabulary matches `sprint_plan.py` and architecture spine templates; complementary module delivery matches current BMad Builder distribution docs. The memlog’s September 2026 uv verification is **credible** with only **patch-level** drift since.

No critical “training-data-only” technology assertions were found in the Stack or AD sections. Address the low-severity **pinning and metadata consistency** notes before treating the stack row as a reproducible Pilot contract.
