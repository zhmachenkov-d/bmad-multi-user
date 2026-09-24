---
title: "Module Plan"
status: "complete"
module_name: "Multi-User Collaboration"
module_code: "team"
module_description: "Git-native multi-human collaboration for BMAD teams sharing one repo and _bmad-output — ownership, readiness gates, layer ordering, and coherent course correction without patching core."
architecture: "hybrid: workflows core + optional facilitation agent"
standalone: false
expands_module: "bmm"
skills_planned:
  - team-status
  - team-ready
  - team-gates
  - team-claim
  - team-impact
  - team-drift
  - team-agent-facilitator
config_variables:
  - team_layers
created: "2026-09-24T13:00:58Z"
updated: "2026-09-24T13:19:00Z"
source_brief: "{project-root}/_bmad-output/planning-artifacts/briefs/brief-bmad-multi-user-2026-09-24/brief.md"
---

# Module Plan

## Vision

**Multi-User Collaboration (`team`)** is a BMM expansion for multi-role teams on one repo and shared `_bmad-output`. It makes parallel human work the default: soft ownership, visible readiness, story/layer gates, bidirectional drift checks that propose correct-course, and impact review when course changes — without patching core BMAD. Developer delight: open `bmad-help` and see what is ready to build. Success feel: fewer merges and better code quality.

## Architecture

**Decision: Hybrid (C)** — deterministic **workflows** are the v1 core; a **facilitation agent** handles conversational drift/impact → correct-course proposals.

**Rationale:** Developer delight is “open `bmad-help`, see ready stories” and fast checks — short, headless-friendly workflows. Drift and correct-course proposals need dialogue. Avoids orchestrator complexity and persona overload. Aligns with anti-patterns: simple to use, soft warnings, no hard locks.

**Skill naming:** `team-*` workflows; `team-agent-facilitator` for the agent.

**Integration:** BMM expansion — must not patch vendor BMAD. Git-tracked state under `planning_artifacts/team/`; help CSV points implementers at `team-status`.

### Memory Architecture

**Locked:** `{planning_artifacts}/team/` (git-tracked). Prefer few files (anti YAML-hell). Soft claims only — no hard locks.

Agent personal memory (facilitator): prefs only — not project truth.

**Pattern:** project-shared git memory + optional personal agent memory.

### Memory Contract

| File / area                | Purpose                          | Readers                       | Writers                |
| -------------------------- | -------------------------------- | ----------------------------- | ---------------------- |
| `planning_artifacts/team/` | Module-owned collaboration state | All `team-*`; help via status | `team-*` / facilitator |
| BMM planning artifacts     | Source planning truth            | `team-*` (read)               | BMM skills primarily   |

### Cross-Agent Patterns

- User + `bmad-help` route day-to-day work.
- Workflows run checks; facilitator proposes `bmad-correct-course` on drift.
- BMM owns content; `team` owns multi-human consistency.

## Skills

### team-status

**Type:** workflow

**Core Outcome:** Developer sees trustworthy ready (and optional unfinished) stories in seconds.

**The Non-Negotiable:** Never mark a story ready if artifact or layer gates are red.

**Capabilities:**

| Capability      | Outcome                         | Inputs                          | Outputs             |
| --------------- | ------------------------------- | ------------------------------- | ------------------- |
| Ready list      | Stories green to start          | sprint/epics/team state, layers | Ready list          |
| Unfinished list | Optional in-progress visibility | same                            | Unfinished list     |
| Gate explain    | Why a story is red              | story id                        | Blocker explanation |

**Activation Modes:** interactive + headless

**Design Notes:** Primary delight surface for `bmad-help`. Runtime flag for unfinished — not setup config.

**Relationships:** before `bmad-build`; uses `team-gates` results.

---

### team-ready

**Type:** workflow

**Core Outcome:** Shared artifact lifecycle (`draft` / `review` / `ready`) for PRD / UX / Architecture.

**The Non-Negotiable:** Humans and agents may set or propose; changes explicit in git.

**Capabilities:**

| Capability     | Outcome               | Inputs                      | Outputs            |
| -------------- | --------------------- | --------------------------- | ------------------ |
| Set status     | Lifecycle updated     | artifact ref, status, actor | Confirm + metadata |
| Propose status | Agent suggests status | artifact ref, rationale     | Proposal for human |

**Activation Modes:** interactive + headless

**Relationships:** feeds `team-gates` / `team-status`; PRD-ready may trigger `team-drift`.

---

### team-gates

**Type:** workflow

**Core Outcome:** Per-story gates (artifacts + layers) and layer implementation ordering.

**The Non-Negotiable:** Soft enforcement (warn / not-ready) — never repo locks.

**Capabilities:**

| Capability        | Outcome                | Inputs                 | Outputs         |
| ----------------- | ---------------------- | ---------------------- | --------------- |
| Define/view gates | Story deps visible     | story / epic           | Gate definition |
| Check story       | Pass/fail + reasons    | story id               | Gate result     |
| Layer order       | Sequence across layers | `team_layers`, stories | Ordered plan    |

**Activation Modes:** interactive + headless

**Tool Dependencies:** none beyond git/filesystem

---

### team-claim

**Type:** workflow

**Core Outcome:** Soft ownership reduces accidental collisions on hot artifacts.

**The Non-Negotiable:** Never hard-lock; stale claims easy to clear.

**Capabilities:**

| Capability    | Outcome         | Inputs        | Outputs          |
| ------------- | --------------- | ------------- | ---------------- |
| Claim         | Soft-own target | target, actor | Claim in `team/` |
| Release       | Clear claim     | target        | Claim removed    |
| Conflict warn | Overlap warning | target        | Warning          |

**Activation Modes:** interactive + headless

---

### team-impact

**Type:** workflow

**Core Outcome:** After course correction, status is recalculated and impact is reviewed before merge.

**The Non-Negotiable:** Explicit impact review before merge of course-correction changes.

**Capabilities:**

| Capability    | Outcome                 | Inputs           | Outputs                        |
| ------------- | ----------------------- | ---------------- | ------------------------------ |
| Recalc status | Gates/ready refreshed   | team + BMM state | Derived status                 |
| Impact review | Affected layers/stories | change summary   | Impact report (HTML candidate) |

**Activation Modes:** interactive + headless

**Relationships:** after `bmad-correct-course`; may hand to facilitator for dialogue.

---

### team-drift

**Type:** workflow (deep dialogue may use facilitator)

**Core Outcome:** Bidirectional PRD ↔ story divergence caught; **propose correct-course**.

**The Non-Negotiable:** Propose CC — do not silently rewrite specs/code.

**Capabilities:**

| Capability          | Outcome                   | Inputs       | Outputs              |
| ------------------- | ------------------------- | ------------ | -------------------- |
| Check on story-done | Drift vs PRD if PRD ready | story, PRD   | Report + CC proposal |
| Check on PRD-ready  | Drift vs done stories     | PRD, stories | Report + CC proposal |

**Activation Modes:** interactive + headless

**Relationships:** → propose `bmad-correct-course`; pairs with `team-agent-facilitator`.

---

### team-agent-facilitator

**Type:** agent

**Persona:** Calm multi-human facilitator — low-ceremony, clear, allergic to process theater.

**Core Outcome:** Drift/impact talks end in propose-correct-course or explicit no-action.

**The Non-Negotiable:** Never patch core BMAD; never hard-lock; never invent YAML sprawl.

**Capabilities:**

| Capability        | Outcome                             | Inputs                   | Outputs                      |
| ----------------- | ----------------------------------- | ------------------------ | ---------------------------- |
| Facilitate drift  | Team understands divergence         | drift report / artifacts | CC proposal or no-action     |
| Facilitate impact | Team agrees what course change hits | impact draft             | Reviewed impact + next steps |
| Coach readiness   | Team uses ready/claims lightly      | context                  | Guidance                     |

**Memory:** reads `planning_artifacts/team/` + relevant BMM docs; personal memory for facilitation prefs only.

**Init Responsibility:** ensure `team/` exists; optional welcome on first run.

**Activation Modes:** interactive

**Relationships:** uses `team-drift`, `team-impact`; hands off to `bmad-correct-course`.

## Configuration

**Simplified — one custom variable:**

| Variable      | Prompt                                                                                               | Default             | Result Template | User Setting |
| ------------- | ---------------------------------------------------------------------------------------------------- | ------------------- | --------------- | ------------ |
| `team_layers` | Which implementation layers does this project use? (comma-separated, e.g. backend, frontend, mobile) | `backend, frontend` | Layers: {value} | false        |

No other module config. Unfinished-in-help is a runtime option on `team-status`, not setup.

## External Dependencies

None beyond git and installed BMAD/BMM. No MCP/SaaS.

## UI and Visualization

No web app in v1. Surfaces: `bmad-help` + skill outputs. Optional HTML for impact/drift reports later. Hard outs: real-time cursors, SaaS.

## Setup Extensions

- Scaffold `{planning_artifacts}/team/`
- Persist `team_layers`
- Post-install: point people at `bmad-help` / `team-status`

## Integration

Expansion of **BMM**. Limited value without BMM artifacts; with BMM, enables multi-human shared `_bmad-output` without vendor patches. Register help entries for `team-status` et al.

## Creative Use Cases

- Onboarding a second teammate: setup + layers early
- Post-merge cleanup week: drift + impact rituals
- Parked: smart merge assist (post-v1)

## Ideas Captured

### Spark (from product brief + pilot team)

- Multi-role parallel work; merge hell; invisible readiness; cross-layer drift; correct-course inconsistency
- Pilot: ~50–60% time on merges/drift; developers hit hardest
- v1: ownership/structure, readiness, gates, layer order, impact review, installable without core patch
- Later: smart merge assist; polished community docs
- Hard outs: cursors, SaaS, ACL-as-collab, replace git

### Identity locked (Phase 1)

- Name: Multi-User Collaboration · Code: `team` · Expansion of BMM

### Phase 2 exploration + decisions

- Dev first gesture: `bmad-help` → ready (+ optional unfinished) stories
- Bidirectional PRD ↔ story drift → **propose correct-course**
- Ready set by **humans and agents**
- Anti: YAML hell, hard locks, confusing UX
- Delight: fewer merges + better code quality

### Architecture locked (Phase 3–4)

- Hybrid C; memory at `planning_artifacts/team/`; config = `team_layers` only

## Build Roadmap

Recommended order (dependency / delight first):

1. **team-ready** + **team-gates** — readiness and gates are the foundation of “ready”
2. **team-status** — developer delight / help surface
3. **team-claim** — soft ownership (lightweight)
4. **team-impact** — correct-course consistency
5. **team-drift** — bidirectional divergence → CC proposal
6. **team-agent-facilitator** — conversational layer on drift/impact
7. **Create Module (CM)** — setup skill, help CSV, `team_layers`, scaffold `team/`

**Rationale:** Status without gates lies; drift/facilitator need the status model first; CM packages what exists.

**Capability review:** User confirmed skill set as-is (2026-09-24) — no merges/drops.

**Next steps:**

1. Build each skill using **Build a Workflow (BW)** or **Build an Agent (BA)** — share this plan as context
2. When all skills are built, return to **Create Module (CM)** to scaffold the module infrastructure

**Suggested first build:** `team-ready` and `team-gates` (foundation), then `team-status` (developer delight).
