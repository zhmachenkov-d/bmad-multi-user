---
stepsCompleted:
  - step-01-validate-prerequisites
  - step-02-design-epics
  - step-03-create-stories
  - step-04-final-validation
inputDocuments:
  - _bmad-output/planning-artifacts/prds/prd-bmad-multi-user-2026-09-24/prd.md
  - _bmad-output/planning-artifacts/architecture/architecture-bmad-multi-user-2026-09-24/ARCHITECTURE-SPINE.md
  - _bmad-output/planning-artifacts/briefs/brief-bmad-multi-user-2026-09-24/brief.md
---

# bmad-multi-user - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for bmad-multi-user, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: Pilot Team members can follow Module-published conventions for `_bmad-output` layout and Claim / Ownership of paths or Story-related slices (documented conventions covering Planning Artifact folders and high-churn status files; usable without modifying Core BMAD).
FR2: A team member can record or refresh a Claim on a path or Story slice; Module skills/scripts soft-check active Claims and warn on conflicting edits (clear warning naming the other Claim; soft check does not prevent git commit/push).
FR3: A team member (or Build preflight) can obtain the current standard BMAD Artifact Lifecycle Statuses for required Planning Artifacts and Stories (status values match Core BMAD vocabularies; Module does not write a parallel lifecycle enum for Planning Artifacts).
FR4: A team member can run a Module command/skill that lists readiness-relevant statuses for a Story’s Dependency Gate inputs (report names each required artifact/Story and its status; indicates pass/fail without requiring Core BMAD patches).
FR5: A team member can declare which Stories, Planning Artifacts, and Layers a Story depends on (stored in Module-owned git-native data; all Stories in sprint-status enrolled once Module is active; missing declaration = incomplete Hard Block until declared or explicitly marked none).
FR6: Build (or Module-wrapped Story start) refuses to proceed when any Dependency Gate fails (non-zero / blocked result listing failing conditions; no undocumented override flag in v1; actionable message of what must reach which status first).
FR7: A team member can declare an ordered list of Layers for the project (Layer Order stored git-natively; invalid/cyclic declarations rejected with an error).
FR8: Dependency Gates fail (Hard Block) when a Story’s Layer would start before all Stories of earlier Layers meet the default ready condition (every Story tagged with a strictly earlier Layer must have status `done`; enforcement uses native BMAD `done`; projects may tighten via FR5 deps but must not loosen without documented project override).
FR9: After a significant mid-flight change (every Correct-Course run), a team member must complete an impact review covering affected Planning Artifacts, Stories, and Layers before merge is considered coherent (impact review artifact listing affected items; Module refuses coherent-merge / Build-ready signal while required impact items remain unchecked; git push/commit unrestricted).
FR10: Correct-Course support recalculates Dependency Gate inputs and sprint-facing readiness after plan changes (status report reflects post-change reality; invalidated Stories marked blocked or returned to a non-executable standard BMAD status without inventing new status names — default `backlog`).
FR11: A team can install the Module into a project that already has Core BMAD and use F1–F5 capabilities without editing installer-owned Core BMAD paths (documented install path; Module skills/scripts in Module-owned or project-custom locations; smoke check proves Core vendor files were not required to be modified).
FR12: Standard Core BMAD skills continue to run; Module adds gates/checks around them rather than replacing Core BMAD (Core skills remain invokable after install; Hard Block via Module wrapper/hook/skill composition without Core source edits).

### NonFunctional Requirements

NFR1: Module MUST install and operate without modifying installer-owned Core BMAD paths.
NFR2: Module MUST remain compatible with the Pilot Team’s supported Core BMAD major version at release; breaking Core BMAD upgrades are documented, not silently patched.
NFR3: Gate and status checks on the hot path (Story start / Build preflight) MUST feel like a normal fast preflight — not a separate ceremony — and MUST NOT meaningfully inflate standard BMAD workflow time (no hard wall-clock SLA in v1).
NFR4: Module MUST NOT require mandatory SaaS or always-on network services for F1–F5.
NFR5: Hard Block and soft-Claim warnings MUST emit machine-readable and human-readable reasons (failing dependency, status, Layer).
NFR6: Module-owned state files MUST be plain text in git (JSON/YAML/Markdown) suitable for PR review.
NFR7: Module MUST NOT require storing secrets beyond what Core BMAD / git already need for the Pilot Team.
NFR8: Module releases follow semantic versioning; incompatible gate/data schema changes bump major and ship a migration note.

### Additional Requirements

- **Starter / package shape (AD-11):** Ship as installable complementary BMAD module (skills + scripts + template `_bmad/custom` hooks); offline for F1–F5; semver Module-home schema and gate behavior; declare supported Core BMAD major(s); install path includes smoke check that Core vendor files were not modified. Impacts Epic 1 Story 1.
- **Stack:** Python >=3.11; uv ~0.12.x; Module state YAML preferred (JSON allowed); Markdown allowed for impact-review prose appendix only; host = local git repo + Core BMAD (no SaaS runtime).
- **AD-1 Preflight-gate paradigm:** Module may only evaluate and gate; must not become a second methodology runtime or replace git / Core BMAD process ownership.
- **AD-2 Core composition via custom hooks:** Hard Block attaches through `_bmad/custom/*.toml` hooks on every Module-supported Story execution entrypoint — at minimum `bmad-build` and `bmad-build-auto` — plus `bmad-correct-course`. Wrappers must not be the sole gate. Git commit/push stay unrestricted.
- **AD-3 Single Module home:** All Module-owned state lives under `_bmad-output/` (seed path: `multi-user/`) — deps, Layer Order, Claims, impact-review signal, readiness-map overrides.
- **AD-4 Write ownership:** Module home = Module writes only; Planning Artifacts = humans + Core write (Module reads statuses); sprint-status = humans + Core, Module may write Story status only via Correct-Course/recalc using native BMAD values; invalidated Stories default to `backlog` (overridable to another native non-executable status only); never invent `blocked` as Module enum; never touch installer-owned Core paths.
- **AD-5 Single gate evaluator:** One shared Python package / one CLI implements Hard Block rules; status report, Build hooks, and coherent-merge checks must invoke that same entrypoint.
- **AD-6 Dependency enrollment:** Each Story in sprint-status must have `deps/<story-id>.yaml` under Module home; story-id must equal sprint-status key; file declares `depends_on_stories`, `depends_on_artifacts`, `layer`, or explicit `none`; missing file = Hard Block; cycle checks; Layer membership for gating declared only here.
- **AD-7 Layer Order + loosen exceptions:** `layer-order.yaml` holds ordered Layer names + named loosen exceptions (`story` id, relaxed constraints, `reason`, `approved_by`); invalid/cyclic Layer order rejected; loosen only via those exceptions.
- **AD-8 Claims soft-check registry:** Central `claims.yaml` (or small path-prefix set); Claim targets use sprint-status Story ids or repo-relative paths; soft-check warns on intersecting Module-mediated edits and Build/status preflight; no per-path `.claim` sidecar as primary SoT; conventions cover Planning Artifact folders and high-churn status files.
- **AD-9 Correct-Course always + impact-review signal:** Every `bmad-correct-course` run requires impact review + status recalc; canonical signal is `impact-review.yaml` with `status: open|cleared`; Hard Block while any required review is `open`; Markdown prose must not carry authoritative open|cleared.
- **AD-10 Native status readiness map:** Module ships default artifact-kind → acceptable native BMAD statuses map (at least PRD, UX Design/Experience, Architecture; brief/spec as shipped defaults); project may override in Module home; map applies to Planning Artifact readiness only — not FR8 Story Layer `done` checks.
- **AD-12 Fast preflight cost:** Gate/status checks stay a normal fast local preflight (no mandatory network, no separate multi-step ceremony).
- **Structural seed:** Module home layout (`config.yaml`, `layer-order.yaml`, `claims.yaml`, `deps/<story-id>.yaml`, `impact-review.yaml`); custom hook templates for build/build-auto/correct-course; package skills (status, claim, declare deps, Correct-Course assist) + scripts (evaluator CLI + helpers via `uv run`).
- **Consistency conventions:** Story ids everywhere = sprint-status keys; dates ISO-8601 in registries; gate results machine-readable + human-readable; config overrides in Module home only.
- **Brief context (non-conflicting):** Primary JTBD payoff is for developers (coherent starts, less rewrite); Pilot success targets merge/drift time toward 15–25%; failure if Core BMAD must be patched/forked. Brief’s invented `draft|review|ready` lifecycle is superseded by PRD/Architecture native BMAD status approach — do not implement parallel vocabulary.

### UX Design Requirements

None — no UX design contract (DESIGN.md / EXPERIENCE.md or legacy UX docs) exists for this Module. Product is skills/scripts/conventions in git with no separate UI or SaaS surface.

### FR Coverage Map

FR1: Epic 2 - Document ownership and path conventions
FR2: Epic 2 - Soft claim check
FR3: Epic 3 - Read native BMAD statuses
FR4: Epic 3 - Status report for readiness
FR5: Epic 3 - Declare story dependencies
FR6: Epic 3 - Hard-block Build on failed gates
FR7: Epic 3 - Declare Layer Order
FR8: Epic 3 - Enforce Layer Order in gates
FR9: Epic 4 - Impact review before merge
FR10: Epic 4 - Status recalculation
FR11: Epic 1 - Install without Core patch
FR12: Epic 1 - Coexist with Core workflows

## Epic List

### Epic 1: Installable Module Foundation

Team can install the complementary Module beside Core BMAD with Module home, single gate evaluator CLI, custom hook templates, and a smoke check that proves Core vendor files were not modified.
**FRs covered:** FR11, FR12

### Epic 2: Ownership & Soft Claims

Parallel roles follow `_bmad-output` layout and Claim conventions; soft-check warns on conflicting Claims/edits without hard-locking git.
**FRs covered:** FR1, FR2

### Epic 3: Ready Starts — Status, Gates & Layer Order

Before Build, the team sees native readiness, declares Story deps and Layer Order, and Hard Block refuses starts until Dependency Gates and Layer Order pass.
**FRs covered:** FR3, FR4, FR5, FR6, FR7, FR8

### Epic 4: Correct-Course Project Truth

Every Correct-Course run produces impact review + status recalc; coherent-merge / Build-ready stays blocked while impact-review is open.
**FRs covered:** FR9, FR10

## Epic 1: Installable Module Foundation

Team can install the complementary Module beside Core BMAD with Module home, single gate evaluator CLI, custom hook templates, and a smoke check that proves Core vendor files were not modified.

### Story 1.1: Scaffold complementary Module package & Module home

As a Pilot Team member,
I want an installable complementary BMAD Module package with a single Module home under `_bmad-output`,
So that we can adopt multi-user coordination without patching Core BMAD.

**Acceptance Criteria:**

**Given** a project that already has Core BMAD installed
**When** the Module package is installed via the documented complementary-module path
**Then** Module-owned skills and scripts land in Module-owned or project-custom locations (not installer-owned Core paths)
**And** a Module home tree exists under `_bmad-output/` (seed name `multi-user/`) with placeholder files for `config.yaml`, `layer-order.yaml`, `claims.yaml`, `deps/`, and `impact-review.yaml` (plain text YAML/JSON suitable for PR review)
**And** no installer-owned Core BMAD vendor file is required to be modified for the scaffold to be present (FR11, AD-3, AD-11, NFR1, NFR6)

### Story 1.2: Single gate evaluator CLI entrypoint

As a Pilot Team member,
I want one shared gate evaluator CLI runnable via `uv`,
So that Build hooks, status reports, and coherent-merge checks use the same Hard Block rules later without forked scripts.

**Acceptance Criteria:**

**Given** the Module package from Story 1.1 is present
**When** I run the Module’s evaluator CLI via `uv run` (Python ≥3.11)
**Then** a single entrypoint exists in the Module scripts package and returns a structured pass/fail result with both machine-readable and human-readable output
**And** the CLI can be invoked independently of any Core BMAD source edit
**And** on this story the evaluator may report “no gate rules loaded” / pass-substrate behavior, but must not duplicate logic into separate scripts (AD-5, AD-12, NFR3, NFR5, FR12 substrate)

### Story 1.3: Custom hook templates for Build & Correct-Course

As a Pilot Team member,
I want `_bmad/custom` hook templates that invoke the Module evaluator on every supported Build and Correct-Course entrypoint,
So that Hard Block composition works without patching Core BMAD and without relying on optional wrappers alone.

**Acceptance Criteria:**

**Given** Stories 1.1–1.2 (Module package + evaluator CLI)
**When** the Module’s template custom hooks are installed for the team
**Then** `_bmad/custom` hooks exist for at least `bmad-build`, `bmad-build-auto`, and `bmad-correct-course`, each calling the same evaluator CLI entrypoint (e.g. via `activation_steps_prepend`)
**And** Core BMAD skills remain invokable; hooks compose around them rather than replacing Core source
**And** git commit/push are not required to enforce gates (no Hard Block via mandatory git hooks) (FR12, AD-2, NFR1)

### Story 1.4: Install path docs & Core-untouched smoke check

As a Pilot Team member,
I want a documented install path and an automated or manual smoke check,
So that we can prove the Module installs and runs without modifying installer-owned Core BMAD paths.

**Acceptance Criteria:**

**Given** Stories 1.1–1.3 are available in the Module package
**When** a team follows the minimal install documentation
**Then** the docs describe how to install the complementary Module, seed Module home, and apply custom hook templates
**And** a smoke check (script or documented checklist) verifies that installer-owned Core BMAD vendor files were not modified as a requirement of install
**And** Module F1–F5 substrate (package, evaluator, hooks) is usable offline with no mandatory SaaS/network (FR11, AD-11, NFR1, NFR2, NFR4)
**And** Module versioning intent is documented as semver for Module-home schema / gate behavior (NFR8)

## Epic 2: Ownership & Soft Claims

Parallel roles follow `_bmad-output` layout and Claim conventions; soft-check warns on conflicting Claims/edits without hard-locking git.

### Story 2.1: Document ownership & path conventions

As a Pilot Team member,
I want Module-published conventions for `_bmad-output` layout and Claim / Ownership of paths or Story-related slices,
So that parallel roles collide less on shared Planning Artifacts and high-churn status files.

**Acceptance Criteria:**

**Given** the Module is installed (Epic 1)
**When** a team member reads Module ownership conventions
**Then** docs cover at least Planning Artifact folder layout under `_bmad-output` and who may edit high-churn shared status files (e.g. sprint-status)
**And** conventions are usable without modifying Core BMAD files
**And** Claim targets are defined to use sprint-status Story ids for Story slices and repo-relative paths for path claims (FR1, AD-8)

### Story 2.2: Claims registry & record/refresh Claim

As a Pilot Team member,
I want to record or refresh a Claim on a path or Story slice in the Module home registry,
So that ownership of parallel work is visible in git-native Module state.

**Acceptance Criteria:**

**Given** Module home exists and ownership conventions from Story 2.1
**When** a team member records or refreshes a Claim via Module skill/script
**Then** the Claim is stored in the central Module-home registry (`claims.yaml` or equivalent path-prefix set) — not a per-path `.claim` sidecar as primary SoT
**And** Story-slice Claims use the same Story id as the `sprint-status` key; path Claims use repo-relative paths
**And** registry entries are plain text suitable for PR review and include enough identity to name the Claim holder in later warnings (FR2, AD-3, AD-8, NFR6)

### Story 2.3: Soft-check warn on conflicting Claims/edits

As a Pilot Team member,
I want Module soft-checks to warn when my edit or Claim conflicts with an active Claim,
So that I avoid trampling parallel work without being hard-locked out of git.

**Acceptance Criteria:**

**Given** at least one active Claim in the Module-home registry
**When** a conflicting Claim is recorded or a Module-mediated edit / Build-or-status preflight intersects an active Claim
**Then** the Module emits a clear warning that names the other Claim (holder and target) in both human-readable and machine-readable form
**And** the soft check does not prevent git commit or push by itself (no hard lock in v1)
**And** soft-check uses the same Claims registry as Story 2.2 (FR2, AD-8, NFR5)

## Epic 3: Ready Starts — Status, Gates & Layer Order

Before Build, the team sees native readiness, declares Story deps and Layer Order, and Hard Block refuses starts until Dependency Gates and Layer Order pass.

### Story 3.1: Native status readiness map & status read

As a Pilot Team member (or Build preflight),
I want to read standard BMAD Artifact Lifecycle Statuses using a Module readiness map of acceptable native statuses,
So that readiness checks use Core vocabularies instead of a parallel Module lifecycle enum.

**Acceptance Criteria:**

**Given** Planning Artifacts and Stories with their native BMAD statuses exist in the project
**When** the Module reads statuses for required Planning Artifacts and Stories
**Then** returned status values match Core BMAD vocabularies for that artifact type (e.g. PRD `draft`/`final`, Story entries in `sprint-status.yaml`)
**And** the Module ships a default artifact-kind → acceptable native statuses map covering at least PRD, UX Design/Experience, and Architecture (brief/spec included as shipped defaults), overridable in Module home `config.yaml`
**And** the Module does not invent or write a parallel Planning Artifact lifecycle enum; the map applies to Planning Artifact readiness only, not Story Layer `done` checks (FR3, AD-4, AD-10)

### Story 3.2: Story readiness status report

As a Pilot Team member,
I want a Module command/skill that lists readiness-relevant statuses for a Story’s Dependency Gate inputs,
So that I can see pass/fail before kicking Build.

**Acceptance Criteria:**

**Given** Story 3.1 status reading and readiness map are available
**When** a team member runs the Module status/readiness report for a Story
**Then** the report names each required artifact/Story input and its current native status
**And** the report indicates pass/fail against that Story’s Dependency Gate inputs without requiring Core BMAD patches
**And** the report is produced via the same single evaluator CLI entrypoint (AD-5), with machine-readable and human-readable output (FR4, NFR5)

### Story 3.3: Declare Layer Order

As a Pilot Team member,
I want to declare an ordered list of Layers for the project in Module home,
So that Stories tagged with a Layer can later be gated by that sequence.

**Acceptance Criteria:**

**Given** Module home exists
**When** a team member declares Layer Order via Module skill/script or by editing Module-home state
**Then** `layer-order.yaml` stores the ordered Layer name list git-natively under Module home
**And** invalid or cyclic Layer **order** declarations are rejected with an error
**And** the file may include named loosen exceptions (`story` id matching sprint-status, relaxed earlier-layer constraints, `reason`, `approved_by`) but must not introduce a second story→layer map (FR7, AD-7, NFR6)

### Story 3.4: Per-story dependency enrollment

As a Pilot Team member,
I want to declare which Stories, Planning Artifacts, and Layers a Story depends on (or explicitly mark none),
So that every Story in sprint-status is enrolled in gating with git-native Module data.

**Acceptance Criteria:**

**Given** Stories exist as keys in `sprint-status` and Module home is present
**When** a team member declares dependencies for a Story via Module skill/script
**Then** Module home has `deps/<story-id>.yaml` where `<story-id>` equals the `sprint-status` key
**And** the file declares `depends_on_stories`, `depends_on_artifacts`, `layer`, or explicit `none`
**And** Layer membership for gating is declared only in this deps file (not a second story→layer map)
**And** dependency cycles across the deps tree are detectable/rejected with an error (FR5, AD-6, NFR6)

### Story 3.5: Hard-block Build on failed Dependency Gates

As a developer starting a Story,
I want Build (via Module-composed hooks) to Hard Block when Dependency Gates fail — including missing enrollment,
So that I cannot start implementation against unready Stories or Planning Artifacts.

**Acceptance Criteria:**

**Given** custom hooks from Epic 1 invoke the single evaluator CLI and Stories 3.1–3.4 provide statuses, report, Layer Order, and deps enrollment
**When** Build / Story start is attempted for a Story whose gates fail (unsatisfied story/artifact deps, missing `deps/<story-id>.yaml`, or incomplete enrollment)
**Then** the evaluator returns non-zero / blocked and lists failing conditions with actionable messages (what must reach which status first)
**And** there is no undocumented override flag in v1 that skips the Hard Block
**And** status report and Build preflight use the same evaluator entrypoint (FR5, FR6, AD-5, AD-6, NFR5)

### Story 3.6: Enforce Layer Order in gates

As a developer starting a Layer-tagged Story,
I want Dependency Gates to Hard Block when earlier-Layer Stories are not yet `done` (unless a named loosen exception applies),
So that frontend (or later) work cannot start before required earlier Layers finish.

**Acceptance Criteria:**

**Given** Layer Order from Story 3.3, per-story `layer` in deps from Story 3.4, and Hard Block substrate from Story 3.5
**When** Build / Story start is attempted for a Story tagged with Layer _L_
**Then** the evaluator Hard Blocks unless every `sprint-status` Story whose deps file names a strictly earlier Layer has native status `done`
**And** enforcement uses standard BMAD Story status `done` (not a Module-invented status); readiness maps must not redefine Story `done` for this rule
**And** named loosen exceptions in `layer-order.yaml` are the only way to relax earlier-layer constraints; projects may tighten further via FR5 deps
**And** failing Layer Order checks emit actionable machine- and human-readable reasons (FR8, AD-7, NFR5)

## Epic 4: Correct-Course Project Truth

Every Correct-Course run produces impact review + status recalc; coherent-merge / Build-ready stays blocked while impact-review is open.

### Story 4.1: Impact review on every Correct-Course run

As a PM (or any role) running Correct-Course,
I want every `bmad-correct-course` run to produce/update an impact review listing affected Planning Artifacts, Stories, and Layers,
So that mid-flight changes cannot silently skip Project Truth alignment.

**Acceptance Criteria:**

**Given** the `bmad-correct-course` custom hook from Epic 1 is installed
**When** Correct-Course runs
**Then** Module home `impact-review.yaml` is created or updated with affected items and authoritative `status: open|cleared`
**And** optional Markdown prose appendix (if any) must not carry the authoritative open|cleared signal
**And** v1 requires impact review on every Correct-Course run (no “small change” skip) (FR9, AD-9, NFR6)

### Story 4.2: Hard-block coherent-merge while impact-review open

As a Pilot Team member,
I want coherent-merge / Build-ready to Hard Block while any required impact review remains `open`,
So that merges are not treated as coherent until impact items are checked.

**Acceptance Criteria:**

**Given** `impact-review.yaml` from Story 4.1 with at least one required review at `status: open`
**When** coherent-merge check or Build-ready / Story start preflight runs via the evaluator CLI
**Then** the evaluator Hard Blocks and reports the open impact-review as a failing condition
**And** git commit/push remain unrestricted; enforcement is via Module composition around Build / Correct-Course / coherent-merge, not git hooks
**And** the same single evaluator entrypoint is used as for Dependency Gates (FR9, AD-5, AD-9, NFR5)

### Story 4.3: Status recalculation after Correct-Course

As a Pilot Team member after Correct-Course,
I want Dependency Gate inputs and sprint-facing readiness recalculated, with invalidated Stories moved to a non-executable native status,
So that status reports and gates reflect post-change reality without inventing new status names.

**Acceptance Criteria:**

**Given** a Correct-Course run has updated plans and impact review (Stories 4.1–4.2)
**When** Module Correct-Course support recalculates readiness
**Then** subsequent status reports (FR4 / Story 3.2) reflect post-change Dependency Gate inputs
**And** Stories that became invalid are moved to a non-executable **native** BMAD status — default `backlog`, overridable in Module home config to another native non-executable status only (never invent `blocked` as a Module enum)
**And** Module writes Story status only via this explicit Correct-Course / recalc path; Planning Artifact statuses remain human/Core-owned reads (FR10, AD-4, AD-9)
