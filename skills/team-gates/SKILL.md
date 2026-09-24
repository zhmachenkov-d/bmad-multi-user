---
name: team-gates
description: "Per-story soft gates and layer order. Use when the user says 'check gates', 'define story gates', 'layer order', or wants artifact/layer readiness before starting a story."
---

# team-gates

## Overview

Act as the team's soft gatekeeper for BMAD stories. You make dependency truth visible in git; you do not invent green lights or lock the repo.

**Outcome:** a story's gate definition is visible (define/view), a pass/fail result with reasons exists (check), or stories are sequenced by layer (order). **Consumer:** humans and `team-status` — they must trust `pass` without this chat. **Bar:** soft only (warn / not-ready); undefined gate ≠ pass; changes via the gates script into `{planning_artifacts}/team/gates.json`.

## Resolution rules

- Bare paths and `{skill-root}` resolve from this skill's installed directory.
- `{project-root}` → the project working directory.
- `team-gates` → the skill directory's basename.

## On Activation

1. Resolve customization: `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --project-root {project-root} --key workflow`. On failure, merge `{skill-root}/customize.toml`, `{project-root}/_bmad/custom/team-gates.toml`, `{project-root}/_bmad/custom/team-gates.user.toml` (base → team → user). Read `{workflow.<name>}` so override scalars apply.
2. Execute each `{workflow.activation_steps_prepend}` entry in order. Hold `{workflow.persistent_facts}` for the run (`file:` / `skill:` / literal).
3. Load `{project-root}/_bmad/config.yaml` (and `.user.yaml` if present). Resolve `{planning_artifacts}`, `{communication_language}`, `{user_name}`. Stay in `{communication_language}`. Ensure `{planning_artifacts}/team/` exists (mkdir if needed).
4. If intent and/or story are underspecified, one open-floor invite (define/view vs check vs order; story id), then ask only residuals. Skip when already explicit. Interactive + still ambiguous → ask. Headless + still ambiguous → infer, then `uv run {project-root}/_bmad/scripts/memlog.py append --workspace {planning_artifacts}/team --type assumption --text "<inference>"`.
5. Resolve layers when needed: prefer explicit `--layers` / user list; else `gates.json` `layers`; else `{planning_artifacts}/team/layers.yaml`. Empty layers is fine for check; order still groups by declared story `layer`.
6. Execute each `{workflow.activation_steps_append}` entry in order.

## Define / view

**View:** `uv run {skill-root}/scripts/gates.py get --team-dir {planning_artifacts}/team --story <id>` or `list --team-dir ...`.

**Define:** write only confirmed gate fields via `gates.py` (do not invent deps). CLI shapes (independent — run only what was confirmed):

- Artifact map (paths relative to `{planning_artifacts}`): `uv run {skill-root}/scripts/gates.py set-artifacts --team-dir {planning_artifacts}/team --map prd=<rel>,ux=<rel>,architecture=<rel>`
- Optional layers: `uv run {skill-root}/scripts/gates.py set-layers --team-dir {planning_artifacts}/team --layers backend,frontend,...`
- Story gate: `uv run {skill-root}/scripts/gates.py set --team-dir {planning_artifacts}/team --story <id> --requires prd,architecture --layer <layer> --depends-on <ids>`

Interactive: confirm before write when the user did not supply the full gate. Headless: missing story or required fields → blocked JSON below. Report the saved gate. Soft-offer **check** on the defined story (verify loop; auto-start would skip judgment). Run `{workflow.on_complete}` if non-empty.

Headless success (define):

```json
{
  "status": "complete",
  "intent": "define",
  "story": "<id>",
  "gate": {},
  "memlog": "{planning_artifacts}/team/.memlog.md",
  "soft_offer": "check",
  "soft_offer_story": "<id>"
}
```

Include `soft_offer` / `soft_offer_story` only after a successful story gate write; omit after artifacts/layers-only updates with no story.

Headless blocked (define — missing fields or script/path failure):

```json
{
  "status": "blocked",
  "intent": "define",
  "reason": "<one line>",
  "memlog": "{planning_artifacts}/team/.memlog.md"
}
```

## Check

Run `uv run {skill-root}/scripts/gates.py check --team-dir {planning_artifacts}/team --planning-artifacts {planning_artifacts} [--story <id>] [--layers ...]`.

Interpret script JSON as source of truth:

- `undefined: true` → not ready (silent green would lie to `team-status`)
- `pass: false` → list `reasons`
- `pass: true` → soft green only — still no repo lock
- Empty fleet (`results: []` / no stories defined) → not ready; soft-offer **define** (vacuous `all_pass` must not read as green)

Soft-offer by reason (interactive + headless `soft_offer` + `soft_offer_story` when a target story is known; one primary handoff — first matching rule; omit when none):

| Reason class                                                           | soft_offer                      | soft_offer_story                |
| ---------------------------------------------------------------------- | ------------------------------- | ------------------------------- |
| empty fleet (no stories in gates)                                      | `define`                        | omit                            |
| undefined gate / artifact key missing from map / artifact file missing | `define`                        | checked story, or first failing |
| artifact status ≠ `ready`                                              | `team-ready`                    | omit                            |
| `depends_on` undefined                                                 | `define`                        | the depends_on story            |
| `depends_on` not pass                                                  | `check`                         | the depends_on story            |
| cycle                                                                  | none (fix the gate graph first) | omit                            |

Interactive: explain blockers in plain language; apply the table. Run `{workflow.on_complete}` if non-empty.

**With `--story`:** headless success mirrors one script result:

```json
{
  "status": "complete",
  "intent": "check",
  "result": {},
  "memlog": "{planning_artifacts}/team/.memlog.md",
  "soft_offer": "define",
  "soft_offer_story": "<id>"
}
```

Include `soft_offer` / `soft_offer_story` only when a handoff applies; omit otherwise.

**Without `--story`:** script returns `results` + `all_pass`. Headless envelope uses that shape; pick one primary soft-offer from the first failing story via the table (or `define` when `results` is empty — do not treat vacuous `all_pass` as ready):

```json
{
  "status": "complete",
  "intent": "check",
  "result": { "results": [], "all_pass": false },
  "memlog": "{planning_artifacts}/team/.memlog.md",
  "soft_offer": "define"
}
```

When `results` is empty, set `"all_pass": false` in the envelope (even if the script said true) so automators do not greenlight an empty fleet.

Script/path failure → interactive stop; headless blocked:

```json
{
  "status": "blocked",
  "intent": "check",
  "reason": "<one line>",
  "memlog": "{planning_artifacts}/team/.memlog.md"
}
```

## Order

Run `uv run {skill-root}/scripts/gates.py order --team-dir {planning_artifacts}/team [--layers ...]`. Present the ordered list (layer index, then story id). Does not mutate gates. Empty `ordered` → soft-offer **define** (empty list is not a plan). Run `{workflow.on_complete}` if non-empty.

Headless success:

```json
{
  "status": "complete",
  "intent": "order",
  "ordered": [],
  "memlog": "{planning_artifacts}/team/.memlog.md",
  "soft_offer": "define"
}
```

Include `soft_offer` only when `ordered` is empty; omit when the list is non-empty.

Script/path failure → interactive stop; headless blocked:

```json
{
  "status": "blocked",
  "intent": "order",
  "reason": "<one line>",
  "memlog": "{planning_artifacts}/team/.memlog.md"
}
```
