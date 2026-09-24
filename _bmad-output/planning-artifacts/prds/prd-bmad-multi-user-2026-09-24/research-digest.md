---
title: Discovery research digest — BMAD Multi-User
created: 2026-09-24
status: draft
---

# Discovery research digest

Synthesized from three parallel web-research subagent passes (collab tooling, readiness/gates, AI workflow multi-human), plus a user-requested deep pass on [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows). Parent may use this for Concern scan and later input reconciliation; not a PRD section.

## Landscape (what exists)

- **Git-native Spec-Driven Development is the hot adjacent space** (GitHub Spec Kit, OpenSpec): markdown plans/tasks in-repo; collaboration = branches/PRs, not live cursors.
- **AWS AI-DLC Workflows (aidlc-workflows)** is a full gated AI lifecycle engine (5 phases / 33 stages / 14 agents) with explicit **multi-human Construction fan-out** — closest public mechanical analogue for claims + dependency DAG + serialized merge gates (see dedicated section below).
- **Docs-as-code vs wiki SaaS** is settled tradeoff: Git wins for diff/PR/AI context; Notion/Confluence for non-eng UX, ACLs, comments.
- **Status source of truth is contested**: Linear/Jira boards vs markdown checklists vs brittle dual-write sync.
- **Ownership primitives exist** (CODEOWNERS, ADR owner/status) but are review-routing, not artifact lifecycle or layer gates — except AI-DLC's Unit claim/ownership model during Construction.
- **Merge pain is structural**: hot shared files beat semantic merge drivers; fragment/isolation patterns (per-change folders, towncrier scraps) work best in practice; AI-DLC serializes main via pin→gate→land so teams never race-push main.
- **BMAD core (public docs)** assumes **one owner / one writer skill per document**; parallel epics, not parallel edits to the same file. Party Mode = multi-agent roundtable, **not** multi-human file coordination. No mechanical locks, readiness machine-state, or layer gating in core.
- **Community fork signal**: jschulte/BMAD-METHOD PR for story locking / PRD crowdsourcing via Issues — enterprise-ish and **forks core**.

## Closest comparables vs this wedge

| Name                               | Solves                                                                                    | Gap vs BMAD Multi-User wedge                                                                                                                                                                                                |
| ---------------------------------- | ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **AWS AI-DLC Workflows**           | Gated AI lifecycle + multi-team Unit claims, DAG, pin/gate/land, spaces, per-user cursors | Different methodology (not BMAD); multi-human focus is Construction units after Inception — not BMAD PRD/UX/Arch lifecycle, per-story planning gates, or BMAD correct-course; heavy engine, not a complementary BMAD module |
| Spec Kit                           | Spec→plan→tasks→implement for agents                                                      | Agent/SDD lifecycle; not multi-role BMAD layers, readiness, correct-course impact                                                                                                                                           |
| OpenSpec (+ Stores beta)           | Per-change folders; planning repo for cross-repo teams                                    | Isolation reduces collisions; light on PRD/UX/Arch ready → story gates                                                                                                                                                      |
| Linear/Jira (+ sync tools)         | Board status/assignees                                                                    | Weak on layered planning readiness & git-doc consistency after course corrections                                                                                                                                           |
| Notion/Confluence                  | Concurrent edit, comments, ACL                                                            | Not git-native; drifts from code                                                                                                                                                                                            |
| CODEOWNERS / ADRs                  | Path review; decision history                                                             | ≠ draft/review/ready lifecycle or implement-order gates                                                                                                                                                                     |
| Task Master / Aider / cloud agents | Task DAGs, worktrees, agent isolation                                                     | Soft multi-user; merge/status drift left to humans                                                                                                                                                                          |
| Semantic merge drivers             | Field/section merges                                                                      | Infra only; same-key conflicts remain                                                                                                                                                                                       |

## Deep dive: awslabs/aidlc-workflows (AI-DLC)

**What it is:** Open-source (MIT-0) AWS Labs implementation of the AI-Driven Development Life Cycle — harness-neutral `core/` rendered for Claude Code, Kiro, Codex, Cursor, opencode, GitHub Copilot. ~4.8k★. Structured, verifiable delivery with human approval after stages; deterministic engine + conductor; audit trail (105 event types).

**Lifecycle shape:** 5 phases (Initialization → Ideation → Inception → Construction → Operation), 33 stages, 14 agents (11 domain + 2 reviewers + adaptive composer), 11 scopes. Multi-agent topologies (inline / hub-and-spoke / pipeline / mob) are **agent collaboration inside a stage**, not multi-human file ownership — conductor always delegates; agents never spawn agents. Mob writing model: contributors write contribution files; lead alone edits `produces[]`.

**Multi-human mechanics (highly relevant):**

| Mechanism               | Behavior                                                                                                                                                                                                                                         |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Spaces & intents        | Space = team world (method/knowledge/intents); intent = one lifecycle run. Per-user `active-space` / `active-intent` cursors are **gitignored** so teammates don't fight over a shared cursor file; shared state/audit/artifacts commit with git |
| Multi-Team Construction | After Inception: Unit dependency DAG; `Unit Ownership: team`; claim → scoped stages 3.1–3.5 → publish candidate → integration lead **pin → merge gate → land** on main                                                                           |
| Claims                  | Exactly one concurrent claimant; CAS on claim refs; adopt for handoff across machines; release = tombstone                                                                                                                                       |
| Dependency ordering     | Units blocked until `depends_on` rows are merged; walking skeleton optional on main before claims open                                                                                                                                           |
| Merge trust model       | Teams never race-push main; pin re-verifies artifacts/fingerprints; clean auto-merge of shared file refused if result ≠ pinned candidate; state fold under per-intent lock                                                                       |
| Status board            | `/aidlc --status` / dispatcher board: Unit progress, claims, pinned candidates, claimable vs blocked                                                                                                                                             |

**Implication for BMAD Multi-User positioning:**

- AI-DLC proves demand for **git-native multi-human coordination** (claims, DAG readiness, serialized integration, ignore local cursors) inside an AI methodology — not just Spec Kit isolation.
- It is a **peer methodology / full engine**, not a BMAD add-on. Overlap is pattern-level (claim/gate/land, dependency-ready work units), not artifact vocabulary (PRD/UX/Arch/`sprint-status.yaml`/correct-course).
- Blind copy risk: importing AI-DLC's heavy Construction fan-out wholesale would overbuild v1 and diverge from "complementary BMAD module without patching core."
- Useful borrowables for PRD concern scan (not FRs yet): per-user gitignored cursors; claim-bound work; DAG-gated start; integration-lead merge gate with evidence; refuse silent same-file merge that ≠ reviewed candidate.

**Sources:** [repo](https://github.com/awslabs/aidlc-workflows) · [intro](https://awslabs.github.io/aidlc-workflows/guide/00-introduction/) · [spaces/intents](https://awslabs.github.io/aidlc-workflows/guide/03-spaces-and-intents/) · [multi-team / workshop](https://awslabs.github.io/aidlc-workflows/guide/workshop-mode/) · [architecture](https://awslabs.github.io/aidlc-workflows/reference/01-architecture/)

## Readiness & course-correction patterns

- Industry DoR = shared checklist (AC, deps, artifacts) + often contract/CI gates for layer order (OpenAPI-first, ADR-linked PRs).
- Course correction today: formal change proposal, impact across artifacts, recompute status, superseding ADR/decision log.
- Informal readiness failure modes: thrash on vague AC, FE against guessed APIs, mid-sprint scope change → stale stories / conflicting truth, over-rigid DoR as theater.
- Flags ≠ readiness (exposure vs may-start).

## Opportunity (underserved — aligns with brief)

1. Multi-role **readiness visibility** (PRD/UX/Arch draft→review→ready) as agent-readable in-repo state
2. **Per-story dependency gates** + **layer implementation ordering** before start
3. **Correct-course impact review** that keeps docs ↔ status ↔ code consistent
4. **BMAD-fluent ownership/structure** without SaaS ACL/cursors or forking core
5. Convention-only SDD leaves **enforcement and cross-artifact drift** to humans

## Risks / anti-patterns (from landscape)

- Forking/patching core BMAD
- SaaS / real-time cursors / enterprise ACL as the collab model
- Over-process gates heavier than pilot ROI
- Conflating multi-agent isolation with multi-human project truth
- Blind ours/theirs merges on AI markdown / YAML status

## Key sources

- https://github.com/awslabs/aidlc-workflows
- https://awslabs.github.io/aidlc-workflows/guide/00-introduction/
- https://awslabs.github.io/aidlc-workflows/guide/03-spaces-and-intents/
- https://awslabs.github.io/aidlc-workflows/guide/workshop-mode/
- https://docs.bmad-method.org/plan/plan-inside-an-organization/
- https://github.com/github/spec-kit/
- https://openspec.dev/docs/team-workflow
- https://openspec.dev/docs/stores
- https://resources.scrumalliance.org/Article/definition-vs-ready
- https://microsoft.github.io/code-with-engineering-playbook/agile-development/team-agreements/definition-of-ready/
- https://github.com/jschulte/BMAD-METHOD/pull/2
- https://docs.task-master.dev/
- https://code.claude.com/docs/en/agent-teams

## Confidence

Medium-high on positioning, BMAD org model, and AI-DLC public multi-team Construction contract (docs are detailed and current). Medium on adoption depth of sync/merge-driver tools and how often AI-DLC multi-team mode is used outside workshops. Blind spot: little public longitudinal data on multi-PM/UX/eng teams co-authoring `_bmad-output`-like trees; pilot ~50–60% merge/drift figure remains anecdote until measured; AI-DLC vs BMAD head-to-head field comparisons absent.
