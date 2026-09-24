---
name: team-status
description: "Show ready stories and gate blockers. Use when the user says 'team status', 'what's ready to build', 'why is this story blocked', or wants unfinished stories before bmad-build."
---

# team-status

## Overview

Act as the team's readiness board for BMAD stories. You surface what is safe to start; you do not invent green lights or lock the repo.

**Outcome:** a trustworthy ready list (and optional unfinished list), or a plain-language explain of why a story is red. **Consumer:** humans and `bmad-help` before `bmad-build` — they must trust "ready" without this chat. **Bar:** never mark ready if artifact/layer gates are red; empty fleet and undefined gates are not ready; this skill does not mutate gates, artifact status, or sprint files (mkdir for `team/` memlog only).

## Resolution rules

- Bare paths and `{skill-root}` resolve from this skill's installed directory.
- `{project-root}` → the project working directory.
- `team-status` → the skill directory's basename.

## On Activation

1. Resolve customization: `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --project-root {project-root} --key workflow`. On failure, merge `{skill-root}/customize.toml`, `{project-root}/_bmad/custom/team-status.toml`, `{project-root}/_bmad/custom/team-status.user.toml` (base → team → user). Read `{workflow.<name>}` so override scalars apply.
2. Execute each `{workflow.activation_steps_prepend}` entry in order. Hold `{workflow.persistent_facts}` for the run (`file:` / `skill:` / literal).
3. Load `{project-root}/_bmad/config.yaml` (and `.user.yaml` if present) plus BMM config when needed. Resolve `{planning_artifacts}`, `{implementation_artifacts}`, `{communication_language}`, `{user_name}`. Stay in `{communication_language}`. Ensure `{planning_artifacts}/team/` exists (mkdir if needed).
4. Resolve optional sprint file: prefer explicit path; else `{implementation_artifacts}/sprint-status.yaml` when it exists. Unfinished is a **runtime flag** (`--include-unfinished` / user ask) — never a setup config.
5. If intent is underspecified, one open-floor invite (ready list vs explain a story; include unfinished? only when a sprint-status path exists), then ask only residuals. Skip when already explicit. Interactive + still ambiguous → ask. Headless + still ambiguous → infer ready list, then `uv run {project-root}/_bmad/scripts/memlog.py append --workspace {planning_artifacts}/team --type assumption --text "<inference>"`.
6. Execute each `{workflow.activation_steps_append}` entry in order.

## Ready (default)

Run:

`uv run {skill-root}/scripts/status.py ready --team-dir {planning_artifacts}/team --planning-artifacts {planning_artifacts} [--sprint-status <path>] [--include-unfinished] [--layers ...]`

Interpret script JSON as source of truth:

- `empty_fleet: true` → not ready; soft-offer **team-gates** define (vacuous green would lie)
- `blocked` → do not flatten into ready
- `sprint_warning` → note it; still show gate-based ready
- Trust script cohorts (`ready` / `blocked` / optional `unfinished`) and any `soft_offer*` fields as written

Interactive: present the script's ready/blocked/(optional unfinished) and its soft_offers without inventing greens. Always surface script `soft_offer` / `soft_offer_story` when present (including all-blocked). Soft-gate after the board only when not `empty_fleet`: offer unfinished only if a sprint path exists and unfinished was not already decided (open-floor or `--include-unfinished`); offer explain only when `blocked` is non-empty; otherwise proceed via script soft_offer. Then stop. Run `{workflow.on_complete}` if non-empty.

Headless success:

```json
{
  "status": "complete",
  "intent": "ready",
  "ready": [],
  "blocked": [],
  "unfinished": [],
  "empty_fleet": false,
  "memlog": "{planning_artifacts}/team/.memlog.md",
  "soft_offer": "bmad-build",
  "soft_offer_story": "<id>"
}
```

Include `soft_offer` / `soft_offer_story` from the script when present; omit when none. Include `unfinished` only when the flag was set.

Script/path failure → interactive stop; headless blocked:

```json
{
  "status": "blocked",
  "intent": "ready",
  "reason": "<one line>",
  "memlog": "{planning_artifacts}/team/.memlog.md"
}
```

## Explain

Run:

`uv run {skill-root}/scripts/status.py explain --team-dir {planning_artifacts}/team --planning-artifacts {planning_artifacts} --story <id>`

- `ready: true` → soft-offer **bmad-build**
- `ready: false` → list `result.reasons`; apply script `soft_offer` fields

Interactive: plain-language blockers; do not rewrite gates here — hand off. Headless success:

```json
{
  "status": "complete",
  "intent": "explain",
  "story": "<id>",
  "ready": false,
  "result": {},
  "memlog": "{planning_artifacts}/team/.memlog.md",
  "soft_offer": "team-ready"
}
```

Include soft-offer fields only when the script provides them.

Script/path failure → interactive stop; headless blocked with `intent: explain`.
