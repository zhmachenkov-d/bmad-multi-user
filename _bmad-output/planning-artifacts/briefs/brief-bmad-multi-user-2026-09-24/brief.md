---
title: "Product Brief: BMAD Multi-User"
status: complete
created: 2026-09-24
updated: 2026-09-24
---

# Product Brief: BMAD Multi-User

## Executive Summary

BMAD Multi-User is an open-source BMAD module for multi-role teams that share one repo and `_bmad-output`. Its wedge is BMAD fluency — PRD, UX, Architecture, epics/stories, sprint status, correct-course — not generic collaborative markdown. Core BMAD fits a single driver; on multi-role teams, parallel work collides on shared artifacts, hides planning readiness, lets stories start before dependent layers exist, and lets course corrections leave inconsistent project truth after merge. The pilot team estimates ~50–60% of time goes to merges and drift cleanup.

The module adds ownership/structure, artifact lifecycle and per-story gates, layer implementation ordering, and correct-course impact review with status recalculation — as a complementary install **without patching core**. It is not a git replacement or a SaaS (see Scope hard outs). Success for v1: the pilot team cuts merge/drift time toward **15–25%** while keeping project truth coherent. Longer bet: community standard for multi-human BMAD collaboration.

## The Problem

On multi-role teams (PM, UX, backend, frontend, mobile) sharing one repo and `_bmad-output`, people constantly collide on shared files (specs, `sprint-status.yaml`, `epics.md`, and related artifacts), with frequent merge mistakes. There is no shared signal for when PRD, UX, or Architecture are “done enough” to start a story. Stories that depend on other layers (e.g. frontend on a backend API) get implemented too early → drift and rework. Course corrections on one layer while another is mid-story leave docs, status, and code describing different systems after merge.

**Who feels it most:** developers — blocked on readiness, forced into bad starts, and rewriting after cross-layer or correct-course drift.

**Cost (team estimate):** ~50–60% of working time on merges and drift cleanup. Manual coordination and post-merge firefighting do not scale.

## The Solution

A git-native BMAD module so multi-role teams can work and correct course in parallel on shared `_bmad-output` without burning most of the week on collisions and drift. Capabilities (detail in Scope): ownership/structure for safer parallel edits; artifact lifecycle + per-story gates; layer implementation ordering; correct-course status recalculation + impact review before merge. Outcome: developers build on a coherent plan instead of cleaning up.

**Primary wedge vs alternatives:** speaks BMAD’s artifact and workflow language — unlike party-mode (multi-agent, not multi-human), process-only discipline, or generic collab-markdown tools. Complements core BMAD; does not fork it.

## Who This Serves

**Primary:** any BMAD multi-role team on a non-trivial project sharing one repo and `_bmad-output`, and losing time to merge collisions, unclear readiness, and cross-layer drift.

**Not for:** solo users with no parallel work; teams without git; enterprises that need SaaS + ACL as the collaboration model.

**Secondary:** BMAD OSS community members who want multi-human collaboration without forking core.

## Success Criteria

- **Time cost:** merge/drift cleanup from ~50–60% to roughly **15–25%** of working time.
- **Developer outcome:** fewer large artifact merges and less code rewrite from early starts or post-merge inconsistency (readiness/gates and impact review enforced in practice).
- **Consistency:** after parallel work and course correction, docs, status, and code align more often than they diverge.
- **Near-term proof:** pilot team reports a sustained drop in merge/drift pain — not community adoption metrics yet.

**Failure signal:** teams must patch or fork **core BMAD** for the module to work.

## Scope

### In for v1 (pilot team)

- Artifact structure and ownership conventions under shared `_bmad-output` to reduce merge collisions
- Artifact lifecycle status for PRD / UX / Architecture (`draft` / `review` / `ready`)
- Per-story dependency gates (artifacts + layers)
- Layer implementation ordering (sequence planning across backend / frontend / mobile / etc.)
- Correct-course support: status recalculation + explicit impact review before merge
- Ship as an installable BMAD module that works **without patching core BMAD** (docs may be minimal but install path must be real)

### Out of v1 (later)

- Smart merge assist (direction kept; not required for v1)
- Polished community documentation / wide adoption packaging beyond the minimal install path

### Hard out (refuse)

- Real-time collaborative cursors
- SaaS collaboration product
- Enterprise ACL as the collaboration model
- Replacing git

## Vision

In 2–3 years this is the **community-standard** BMAD module for multi-human collaboration: parallel work on one repo and shared `_bmad-output` is the default, with visible readiness and layer order, and course corrections that do not split project truth — still git-native and complementary to core. Refusals stay in Scope hard outs.
