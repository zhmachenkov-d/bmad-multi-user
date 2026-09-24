---
name: team-ready
description: "Set artifact ready lifecycle. Use when the user says 'set ready', 'mark PRD ready', 'propose artifact status', or wants draft/review/ready on PRD UX or Architecture."
---

# team-ready

## Overview

Act as the team's readiness steward for BMAD planning docs. You keep lifecycle honest and explicit in git; you do not invent readiness or patch core BMAD.

**Outcome:** the target artifact's YAML frontmatter `status` is `draft`, `review`, or `ready` (set), or a clear recommendation to do so (propose). **Consumer:** teammates and `team-gates` / `team-status` — they must trust the value without this chat. **Bar:** only those three statuses; no hard locks; changes via the status script; actor recorded when known.

## Resolution rules

- Bare paths and `{skill-root}` resolve from this skill's installed directory.
- `{project-root}` → the project working directory.
- `team-ready` → the skill directory's basename.

## On Activation

1. Resolve customization: `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --project-root {project-root} --key workflow`. On failure, merge `{skill-root}/customize.toml`, `{project-root}/_bmad/custom/team-ready.toml`, `{project-root}/_bmad/custom/team-ready.user.toml` (base → team → user). Read `{workflow.<name>}` so override scalars apply.
2. Execute each `{workflow.activation_steps_prepend}` entry in order. Hold `{workflow.persistent_facts}` for the run (`file:` / `skill:` / literal).
3. Load `{project-root}/_bmad/config.yaml` (and `.user.yaml` if present). Resolve `{planning_artifacts}`, `{communication_language}`, `{user_name}`. Stay in `{communication_language}`. Ensure `{planning_artifacts}/team/` exists (mkdir if needed) — headless audit memlog lives there.
4. If intent and/or target are underspecified, one open-floor invite (artifact, set vs propose, desired status), then ask only residuals. Skip when path + intent are already explicit. Interactive + still ambiguous → ask. Headless + still ambiguous → infer, then `uv run {project-root}/_bmad/scripts/memlog.py append --workspace {planning_artifacts}/team --type assumption --text "<inference>"`.
5. Identify the artifact (v1: PRD / UX / Architecture under `{planning_artifacts}`, or an explicit path). **Zero candidates:** ask (interactive) or headless blocked — guessing invents the wrong file. **Multiple candidates:** list paths and ask (interactive); headless blocked unless a path was pre-supplied.
6. Execute each `{workflow.activation_steps_append}` entry in order.

## Set

1. Resolve path. Run `uv run {skill-root}/scripts/artifact_status.py get --path <path>`.
2. **Missing path or status:** interactive → ask/confirm. Headless → do not write (untrusted lifecycle write); emit blocked JSON below. If both are already explicit, apply without confirm.
3. If get/set returns `ok: false` or the file is missing after a supplied path: interactive → stop with the script error; headless → blocked JSON (do not treat as missing-status confirm).
4. Apply: `uv run {skill-root}/scripts/artifact_status.py set --path <path> --status <draft|review|ready> --actor "{user_name}"`.
5. Report previous → new. If the artifact is a **PRD** and new status is `ready`, soft-offer **`team-drift`** (auto-start would skip human judgment).
6. Run `{workflow.on_complete}` if non-empty.
7. Headless success:

   ```json
   {
     "status": "complete",
     "intent": "set",
     "path": "<artifact>",
     "artifact_status": "<draft|review|ready>",
     "memlog": "{planning_artifacts}/team/.memlog.md",
     "soft_offer": "team-drift"
   }
   ```

   Include `soft_offer` only when a PRD newly became `ready`; omit otherwise.

   Headless blocked:

   ```json
   {
     "status": "blocked",
     "intent": "set",
     "reason": "<one line>",
     "memlog": "{planning_artifacts}/team/.memlog.md"
   }
   ```

## Propose

Recommend `draft` | `review` | `ready` from the artifact + script `get`, with a one-line rationale against these cues:

- Thin / missing sections or empty frontmatter → `draft`
- Substantive but not reviewed → `review`
- Reviewed and gate-consumable for downstream work → `ready`
- Legacy `final` / `complete` → propose an explicit remap (silent remap hides lifecycle drift)

Interactive: on accept run **Set**; on decline stop. **Headless:** recommendation-only JSON so automators cannot skip the set step; apply only via a separate **set**:

```json
{
  "status": "complete",
  "intent": "propose",
  "path": "<artifact>",
  "recommended_status": "<draft|review|ready>",
  "rationale": "<one line>",
  "memlog": "{planning_artifacts}/team/.memlog.md"
}
```

Log: `uv run {project-root}/_bmad/scripts/memlog.py append --workspace {planning_artifacts}/team --type decision --text "propose <path> → <status>: <rationale>"`.
