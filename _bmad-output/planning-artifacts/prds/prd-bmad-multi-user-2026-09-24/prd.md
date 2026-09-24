---
title: "PRD: BMAD Multi-User"
status: final
created: 2026-09-24
updated: 2026-09-24
---

# PRD: BMAD Multi-User

## 0. Document Purpose

This PRD defines requirements for an installable complementary BMAD Module that lets multi-role human teams collaborate on shared `_bmad-output` without patching Core BMAD. Audience: product owner, Pilot Team, and downstream Architecture / Epics / Build. It builds on the product brief at `_bmad-output/planning-artifacts/briefs/brief-bmad-multi-user-2026-09-24/brief.md` and Discovery research at `research-digest.md` in this folder. Vocabulary is anchored in Glossary; open assumptions are tagged inline.

## 1. Vision

BMAD Multi-User is an **installable BMAD Module** (skills, scripts, and conventions in git — no separate UI or SaaS) for multi-role teams that share one repository and `_bmad-output`. It makes parallel BMAD work the default: visible readiness for Planning Artifacts, Layer-aware Story start, and Correct-Course changes that keep Project Truth intact across docs, status, and code.

In 2–3 years it is part of the **BMAD ecosystem as an official complementary Module** — aligned with BMAD’s vision for custom/complementary modules, installable beside BMM, and never requiring a patch or fork of Core BMAD. It speaks BMAD’s artifact language (PRD, UX, Architecture, epics/Stories, sprint status, Correct-Course), not generic collab-markdown or multi-agent party-mode.

It complements Core BMAD; it does not replace git. Real-time cursors, SaaS collaboration, and enterprise ACL are refused as the collaboration model (see Non-Goals).

## 1.1 Comparables and positioning

The Module is **BMAD-fluent multi-human coordination** on shared `_bmad-output`. It is not a generic SDD toolkit and not a second methodology engine.

| Comparable                                                      | What it is                                                             | Gap vs this Module                                                                                                                                                                                              |
| --------------------------------------------------------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Core BMAD (process only)**                                    | Single-writer-per-document norms; Party Mode is multi-agent            | No mechanical Dependency Gates, Claim soft-checks, or Correct-Course Project Truth enforcement for multi-human parallel work                                                                                    |
| **GitHub Spec Kit**                                             | Spec→plan→tasks→implement for coding agents                            | Agent/SDD lifecycle; not BMAD Planning Artifact / Story / Correct-Course vocabulary                                                                                                                             |
| **OpenSpec**                                                    | Per-change isolation folders; optional planning Stores                 | Reduces merge collisions via isolation; light on BMAD readiness gates and Layer Order                                                                                                                           |
| **AWS AI-DLC Workflows**                                        | Full gated AI lifecycle with multi-team Unit claim → pin → gate → land | Peer methodology / heavy engine; Construction fan-out after Inception — not a complementary BMAD Module. Pattern borrow (Claims, DAG readiness, serialized integration) is fine; wholesale copy is out of scope |
| **Notion / Confluence / Linear-as-SoT**                         | Concurrent edit or board status                                        | Not git-native `_bmad-output` truth; dual-write drift risk                                                                                                                                                      |
| **Core-fork community patches** (e.g. Story locking via Issues) | Multi-human features by forking Core BMAD                              | Violates SM-4 / Non-Goals — Module must not require Core BMAD fork                                                                                                                                              |

**Intentional brief overrides retained in this PRD:** native BMAD Artifact Lifecycle Status instead of inventing `draft|review|ready`; Claim soft-check (not hard locks) in v1; Hard Block on Build start.

## 2. Target User

Who feels the pain most: **developers** — blocked on readiness, forced into bad starts, and rewriting after cross-Layer or Correct-Course drift. Other roles (PM, UX) participate; the Module’s primary JTBD payoff is coherent starts and less cleanup for implementers.

### 2.1 Jobs To Be Done

- **Block premature Story work:** do not allow a Story to be executed while Stories (and readiness conditions) it depends on are not ready.
- **Correct course without desync:** change direction mid-flight and keep docs, status, and code describing the same system (Project Truth).
- **Raise delivered code quality:** ship on a coherent plan so less rewrite and fewer integration surprises (outcome of readiness, Dependency Gates, and Layer Order — not a separate code-quality tooling surface).

### 2.2 Non-Users (v1)

- Solo operators with no parallel work on shared artifacts
- Teams not using git
- Enterprises that need SaaS + ACL as the collaboration model

### 2.3 Key User Journeys

- **UJ-1. Alex (frontend) cannot start a Story until deps are ready.** Alex opens the next frontend Story; the Module reports it blocked because the backend API Story (and/or required Planning Artifacts / Layer Order) is not ready. Alex picks other ready work or waits — no speculative implementation against a guessed contract.
- **UJ-2. Jordan (PM) runs Correct-Course without splitting Project Truth.** Mid-sprint a requirement changes; Jordan runs Correct-Course. The Module forces impact review, recalculates status, and surfaces what must update before merge — docs, sprint status, and in-flight Stories stay aligned instead of silently diverging.
- **UJ-3. Sam (backend) owns a slice without trampling shared files.** Sam Claims ownership for a backend epic/Story path under `_bmad-output` conventions; parallel work by UX/frontend proceeds on other paths. Merge collisions on hot shared status files drop because structure and Ownership steer edits.
- **UJ-4. Riley (any role) sees planning readiness before kicking Build.** Before starting implementation, Riley checks standard BMAD statuses on required Planning Artifacts and Stories and only proceeds when the Story’s Dependency Gates pass — fewer “we built the wrong thing” rewrites (realizes the code-quality JTBD via coherent starts).

## 3. Glossary

- **Module** — This installable complementary BMAD package (skills, scripts, conventions in git); not a SaaS product and not a Core BMAD patch.
- **Core BMAD** — Upstream BMAD Method install that the Module must not require patching or forking.
- **Planning Artifact** — A BMAD planning document under `_bmad-output` that participates in readiness (at least PRD, UX Design/Experience, Architecture).
- **Artifact Lifecycle Status** — The **standard BMAD status** already used by that artifact type (e.g. PRD `draft`/`final`, product brief `complete`, Story statuses in `sprint-status.yaml` such as `backlog`/`ready-for-dev`/`in-progress`/`done`, spec statuses such as `draft`/`ready-for-dev`/`done`). The Module must not invent a parallel status vocabulary.
- **Story** — An implementable unit tracked in epics/stories and sprint status.
- **Dependency Gate** — A check that a Story may start only when its required Stories, Planning Artifacts, and/or Layers are satisfied.
- **Layer** — An implementation concern slice (e.g. backend, frontend, mobile) used for ordering and gates.
- **Layer Order** — Declared sequence constraining when Stories for a Layer may start relative to other Layers.
- **Claim / Ownership** — Convention plus soft-check assignment of who may edit a path or Story-related artifact set under shared `_bmad-output`. v1 does not hard-lock edits; it warns on conflict with an active Claim.
- **Correct-Course** — The BMAD change workflow when plans shift mid-flight; in this Module it includes status recalculation and mandatory impact review before merge.
- **Project Truth** — Consistent alignment of Planning Artifacts, sprint status, and code after parallel work or Correct-Course.
- **Pilot Team** — The first multi-role team used to validate Success Metrics for v1.
- **Hard Block** — A Dependency Gate failure that prevents starting Build (or equivalent Story execution) until conditions are satisfied; no silent override path in v1.

## 4. Features

### 4.1 Ownership and artifact structure (F1)

**Description:** The Module defines conventions for how shared `_bmad-output` is structured and who Claims paths or Story-related slices, so parallel roles collide less often. v1 enforcement is **soft check** (warn), not hard lock.

**Functional Requirements:**

#### FR-1: Document ownership and path conventions

Pilot Team members can follow Module-published conventions for `_bmad-output` layout and Claim / Ownership of paths or Story-related slices. Realizes UJ-3.

**Consequences (testable):**

- Module ships documented conventions covering at least Planning Artifact folders and high-churn status files.
- Conventions are usable without modifying Core BMAD files.

#### FR-2: Soft claim check

A team member can record or refresh a Claim on a path or Story slice; Module skills/scripts soft-check active Claims and warn on conflicting edits. Realizes UJ-3.

**Consequences (testable):**

- Conflicting Claim or edit attempt produces a clear warning naming the other Claim.
- Soft check does not prevent git commit/push by itself (no hard lock in v1).

**Out of Scope:**

- Hard file locks, exclusive checkout enforcement, real-time cursors.

### 4.2 Native BMAD status visibility (F2)

**Description:** The Module surfaces and uses each artifact’s **standard BMAD Artifact Lifecycle Status** — it does not invent `draft|review|ready`.

**Functional Requirements:**

#### FR-3: Read native statuses

A team member (or Build preflight) can obtain the current standard BMAD statuses for required Planning Artifacts and Stories. Realizes UJ-4.

**Consequences (testable):**

- Status values match Core BMAD vocabularies for that artifact type (e.g. PRD `draft`/`final`, Story entries in `sprint-status.yaml`).
- Module does not write a parallel lifecycle enum for Planning Artifacts.

#### FR-4: Status report for readiness

A team member can run a Module command/skill that lists readiness-relevant statuses for a Story’s Dependency Gate inputs. Realizes UJ-4.

**Consequences (testable):**

- Report names each required artifact/Story and its status.
- Report indicates pass/fail against the Story’s Dependency Gate without requiring Core BMAD patches.

### 4.3 Dependency Gates (F3)

**Description:** A Story cannot start Build until Dependency Gates pass. Failure is a **Hard Block**.

**Functional Requirements:**

#### FR-5: Declare story dependencies

A team member can declare which Stories, Planning Artifacts, and Layers a Story depends on. Realizes UJ-1.

**Consequences (testable):**

- Dependencies are stored in Module-owned, git-native data under the project (not only in chat memory).
- Once the Module is active, all Stories in `sprint-status` are enrolled in gating; missing declaration is incomplete (Hard Block until dependencies are declared or explicitly marked none).

#### FR-6: Hard-block Build on failed gates

Build (or Module-wrapped Story start) refuses to proceed when any Dependency Gate fails. Realizes UJ-1.

**Consequences (testable):**

- Failed gate returns a non-zero / blocked result and lists failing conditions.
- No undocumented override flag in v1 that skips the Hard Block.
- Message is actionable (what must reach which status first).

### 4.4 Layer Order (F4)

**Description:** The Pilot Team declares Layer Order; Stories tagged with a Layer respect that order via Dependency Gates.

**Functional Requirements:**

#### FR-7: Declare Layer Order

A team member can declare an ordered list of Layers for the project. Realizes UJ-1.

**Consequences (testable):**

- Layer Order is stored git-natively with the Module data.
- Invalid/cyclic declarations are rejected with an error.

#### FR-8: Enforce Layer Order in gates

Dependency Gates fail (Hard Block) when a Story’s Layer would start before all Stories of earlier Layers meet the default ready condition. Realizes UJ-1.

**Default rule (v1):** For a Story tagged with Layer _L_, every Story in `sprint-status` tagged with a Layer strictly earlier than _L_ in the declared Layer Order MUST have status `done`. Until then, starting Build for the Story is a Hard Block.

**Consequences (testable):**

- Example: a frontend Story is Hard-Blocked while any backend-Layer Story (earlier in Layer Order) is not `done`.
- Enforcement uses the standard BMAD Story status `done` (not a Module-invented status).
- Projects MAY tighten further via explicit Dependency Gate declarations (FR-5); they MUST NOT loosen the default without a documented project override mechanism defined at Architecture time.

### 4.5 Correct-Course coherence (F5)

**Description:** When Correct-Course runs, the Module requires impact review and status recalculation so Project Truth does not split.

**Functional Requirements:**

#### FR-9: Impact review before merge

After a significant mid-flight change, a team member must complete an impact review covering affected Planning Artifacts, Stories, and Layers before merge is considered coherent. Realizes UJ-2.

**Consequences (testable):**

- Module produces or updates an impact review artifact listing affected items.
- Module skill/script refuses a “coherent merge” / Build-ready signal while required impact items remain unchecked. Git push/commit remain unrestricted; enforcement is via Module composition around Build / Correct-Course, not git hooks that rewrite Core BMAD.

#### FR-10: Status recalculation

Correct-Course support recalculates Dependency Gate inputs and sprint-facing readiness after plan changes. Realizes UJ-2.

**Consequences (testable):**

- After recalculation, status report (FR-4) reflects post-change reality.
- Stories that became invalid are marked blocked or returned to a non-executable standard BMAD status per project rules — without inventing new status names.

### 4.6 Installable complementary Module (F6)

**Description:** The Module installs and runs as a complementary BMAD package without patching Core BMAD. Validates SM-4.

**Functional Requirements:**

#### FR-11: Install without Core patch

A team can install the Module into a project that already has Core BMAD and use F1–F5 capabilities without editing installer-owned Core BMAD paths. Realizes Vision / SM-4.

**Consequences (testable):**

- Documented install path exists (minimal docs acceptable in v1).
- Module skills/scripts live in Module-owned or project-custom locations consistent with BMAD complementary-module norms.
- Automated or manual smoke check proves Core BMAD vendor files were not required to be modified.

#### FR-12: Coexist with Core workflows

Standard Core BMAD skills continue to run; Module adds gates/checks around them rather than replacing Core BMAD. Supports SM-C1.

**Consequences (testable):**

- Core BMAD skills remain invokable after Module install.
- Module Hard Block on Build is implemented via Module wrapper/hook/skill composition that does not require Core BMAD source edits.

## 5. Cross-Cutting NFRs and Constraints

### Compatibility

- **NFR-1:** Module MUST install and operate without modifying installer-owned Core BMAD paths.
- **NFR-2:** Module MUST remain compatible with the Pilot Team’s supported Core BMAD major version at release; breaking Core BMAD upgrades are documented, not silently patched.

### Performance / workflow cost (SM-C1)

- **NFR-3:** Gate and status checks on the hot path (Story start / Build preflight) MUST feel like a normal fast preflight — not a separate ceremony — and MUST NOT meaningfully inflate standard BMAD workflow time (supports SM-C1). No hard wall-clock SLA in v1.
- **NFR-4:** Module MUST NOT require mandatory SaaS or always-on network services for F1–F5.

### Reliability / observability

- **NFR-5:** Hard Block and soft-Claim warnings MUST emit machine-readable and human-readable reasons (failing dependency, status, Layer).
- **NFR-6:** Module-owned state files MUST be plain text in git (JSON/YAML/Markdown) suitable for PR review.

### Security / trust

- **NFR-7:** Module MUST NOT require storing secrets beyond what Core BMAD / git already need for the Pilot Team.

### Versioning (OSS module)

- **NFR-8:** Module releases follow semantic versioning; incompatible gate/data schema changes bump major and ship a migration note.

## 6. Non-Goals (Explicit)

- Smart merge assist for conflicting markdown/YAML (deferred post-v1; direction kept).
- Polished community documentation / wide-adoption packaging beyond a minimal install path.
- Real-time collaborative cursors.
- SaaS collaboration product.
- Enterprise ACL as the collaboration model.
- Replacing git.
- Inventing a parallel Planning Artifact status vocabulary (`draft|review|ready`).
- Hard file locks / exclusive edit enforcement for Claims in v1.
- Patching or forking Core BMAD.
- Becoming a generic Spec Kit / AI-DLC clone (different methodology); pattern borrowing is fine, product identity remains BMAD-fluent.

## 7. MVP Scope

### 7.1 In Scope

- F1–F6 as specified in §4 (FR-1–FR-12)
- Pilot Team validation against §8 Success Metrics
- Minimal install path and enough docs to install and run gates, Claims, and Correct-Course checks

### 7.2 Out of Scope for MVP

Deferred items already listed in Non-Goals (§6), plus:

- Ecosystem adoption packaging and upstream “default install” promotion — post-v1
- Multi-repo / sibling-repo orchestration (AI-DLC-style) — not required for the v1 Pilot Team single-repo model
- Hard Claim locks — deferred unless the Pilot Team proves soft check insufficient

## 8. Success Metrics

**Primary**

- **SM-1**: Pilot Team time spent on merge conflicts and drift cleanup falls from ~50–60% of working time to roughly **15–25%**, sustained (team-reported / diary), not a one-week spike. Validates FR-1, FR-2. `[ASSUMPTION: the ~50–60% baseline is a Pilot Team estimate, not independently measured public data; measure during pilot.]`
- **SM-2**: Fewer large shared-artifact merges and less code rewrite caused by early Story starts or post–Correct-Course inconsistency. Validates FR-5, FR-6, FR-8, FR-9, FR-10.
- **SM-3**: After parallel work and course correction, docs, status, and code **align more often than they diverge** on the Pilot Team. Validates FR-9, FR-10.
- **SM-4 (failure signal)**: Module is a failure if teams must **patch or fork Core BMAD** for it to work. Validates FR-11, FR-12.

**Secondary**

- **SM-5**: Near-term proof is **Pilot Team** sustained pain reduction — not community adoption metrics in v1.

**Counter-metrics (do not optimize away)**

- **SM-C1**: Standard BMAD workflows (brief → PRD → UX → architecture → epics → sprint → Build / Correct-Course) must **not** become significantly slower due to Module gates and process. Counterbalances SM-1–SM-3. Watched against FR-6 Hard Block UX and FR-12.

**Deferred post-v1 (not v1 success criteria)**

- Ecosystem adoption signals (upstream docs links, N external teams, “default complementary install”) — revisit after v1.

## 9. Open Questions

All former open questions resolved (Architecture + Spec). Layer Order default (FR-8) remains: all earlier-Layer Stories must be `done`.

1. **Correct-Course trigger (FR-9):** _(resolved)_ Every `bmad-correct-course` run requires impact review + status recalculation (architecture AD-9).
2. **Coherent-merge signal (FR-9):** _(resolved)_ Authoritative signal is Module-home `impact-review.yaml` with `status: open|cleared` (AD-9).
3. **Pilot measurement for SM-2 / SM-3:** _(resolved)_ Weekly Pilot diary protocol in `_bmad-output/specs/spec-bmad-multi-user/pilot-ops.md`.
4. **Optional SM-C1 proxy:** _(resolved)_ Watch-only Y/N “felt like normal fast preflight” + optional wall-clock seconds; not a v1 SLA (`pilot-ops.md`).

**Also resolved (Spec):** Correct-Course recalc default for invalidated Stories is native status `backlog` (overridable in Module home to another native non-executable status only).

## 10. Assumptions Index

- _(cleared)_ FR-5 enrollment default and FR-9 Module-not-git enforcement were confirmed and promoted into FR text.
- NFR-3 uses qualitative fast-preflight language (no numeric SLA), confirmed.
- SM-1 ~50–60% baseline is Pilot Team estimate pending measurement.
- Developers are the primary sufferers (from brief); restored in §2.
- _(cleared)_ §9 OQ1–OQ4 resolved via Architecture AD-9 and Spec `pilot-ops.md` / recalc default `backlog`.
