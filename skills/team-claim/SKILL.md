---
name: team-claim
description: "Soft-claim planning artifacts. Use when the user says 'claim this', 'release claim', 'who owns the PRD', or wants soft ownership so teammates do not collide on hot docs."
---

# team-claim

## Overview

Act as the team's soft ownership board for BMAD planning artifacts. You make who is working on a hot file visible in git; you do not lock the repo or invent owners.

**Outcome:** a claim is recorded, released, or a conflict is warned — all via `claims.json` under `{planning_artifacts}/team/`. **Consumer:** teammates about to edit the same path. **Bar:** soft only (warn / takeover with `--force`); stale claims clear with release by anyone; never hard-lock.

## Resolution rules

- Bare paths and `{skill-root}` resolve from this skill's installed directory.
- `{project-root}` → the project working directory.
- `team-claim` → the skill directory's basename.

## On Activation

1. Resolve customization: `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --project-root {project-root} --key workflow`. On failure, merge `{skill-root}/customize.toml`, `{project-root}/_bmad/custom/team-claim.toml`, `{project-root}/_bmad/custom/team-claim.user.toml` (base → team → user). Read `{workflow.<name>}` so override scalars apply.
2. Execute each `{workflow.activation_steps_prepend}` entry in order. Hold `{workflow.persistent_facts}` for the run (`file:` / `skill:` / literal).
3. Load `{project-root}/_bmad/config.yaml` (and `.user.yaml` if present). Resolve `{planning_artifacts}`, `{communication_language}`, `{user_name}`. Stay in `{communication_language}`. Ensure `{planning_artifacts}/team/` exists (mkdir if needed).
4. If intent and/or target are underspecified, one open-floor invite (claim vs release vs check/list; which path), then ask only residuals. Skip when already explicit. Interactive + still ambiguous → ask. Headless + still ambiguous → infer, then `uv run {project-root}/_bmad/scripts/memlog.py append --workspace {planning_artifacts}/team --type assumption --text "<inference>"`.
5. Execute each `{workflow.activation_steps_append}` entry in order.

## Headless envelope

Every terminal exit (complete or blocked), interactive or headless, ends with: run `{workflow.on_complete}` if non-empty.

Headless emit `{status, intent, memlog}` plus script fields that apply (`target`, `action`, `claim`, `conflict`, `released`, `claimed`, `holder`, `claims`, `reason`). `memlog` is always `{planning_artifacts}/team/.memlog.md`. Script/path failure → interactive stop; headless `status: blocked` with matching `intent` and `reason`.

## Claim

Run:

`uv run {skill-root}/scripts/claims.py claim --team-dir {planning_artifacts}/team --planning-artifacts {planning_artifacts} --target <path> --actor "{user_name}" [--note ...] [--force]`

Interpret script JSON as source of truth:

- `action: claimed` / `already` → report holder; done
- `ok: false` + `conflict: true` → **warn**; interactive → offer `--force` takeover (never silent overwrite); headless → `status: blocked` (do not invent ownership)
- `action: takeover` → report previous holder + new claim

Then terminal: `{workflow.on_complete}` if non-empty.

## Release

Run:

`uv run {skill-root}/scripts/claims.py release --team-dir {planning_artifacts}/team --planning-artifacts {planning_artifacts} --target <path>`

Anyone may release (stale clear). Report `released` / `absent`. Then terminal: `{workflow.on_complete}` if non-empty.

## Check / list (conflict warn)

**Check:** `uv run {skill-root}/scripts/claims.py check --team-dir {planning_artifacts}/team --planning-artifacts {planning_artifacts} --target <path> [--actor "{user_name}"]`

- `claimed: false` → free
- `conflict: true` → warn who holds it

**List:** `uv run {skill-root}/scripts/claims.py list --team-dir {planning_artifacts}/team` — headless includes script `claims` / `count`.

Then terminal: `{workflow.on_complete}` if non-empty.
