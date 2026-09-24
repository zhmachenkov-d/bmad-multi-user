# PRD Quality Review — BMAD Multi-User

## Overall verdict
This is a launch-ready PRD for an OSS complementary BMAD module: the thesis, form-factor refusals, brief overrides, and FR set cohere, and Non-Goals / MVP boundaries are honest. What holds up is decision clarity (soft Claims, Hard Block on Build, native BMAD statuses, no Core fork) and shape fit for skills/scripts/conventions without UI theater. What is at risk is implementer done-ness on Layer Order and Correct-Course gate semantics (“project rules,” “significant” change) plus pilot-measurement softness on SM-2/SM-3 — Architecture can absorb schema, but those gaps should not stay invisible behind an empty Open Questions section.

## Decision-readiness — strong
Product bets are stated as decisions, not buried considerations. §1.1 names intentional brief overrides (native Artifact Lifecycle Status vs invented `draft|review|ready`; Claim soft-check; Hard Block on Build) and what comparables give up. §5 / §6.2 refuse SaaS, ACL-as-collab, Core forks, and smart-merge in v1 with enough bluntness that a skeptic’s objection is already on the page. SM-4 as an explicit failure signal (§7) is decision-grade. Remaining ambiguity is mostly schema/trigger detail for Architecture, not unresolved product strategy — though §8’s “none phase-blocking” claim slightly oversells residual gate semantics (see Scope honesty).

### Findings
_None that change the verdict._

## Substance over theater — strong
Vision (§1) is BMAD-module-specific and would not swap into a generic collab PRD. Comparables (§1.1) do real positioning work against Spec Kit, OpenSpec, AI-DLC, and Core-fork patches rather than novelty furniture. Four light UJs (§2.3) each map to FRs; none are decorative personas. JTBD-3 is correctly demoted to an outcome of gates/ordering (§2.1), not a fake quality-tool surface. NFRs (§4A) are mostly Module-shaped (no SaaS, no Core patch, git-native state, semver) rather than scalable/secure boilerplate — NFR-3’s qualitative preflight language is thin but intentional and acknowledged.

### Findings
_None._

## Strategic coherence — strong
Thesis is clear: BMAD-fluent multi-human coordination on shared `_bmad-output` without forking Core. Feature arc F1→F6 (§4) follows that thesis (structure → native status → Hard Block gates → Layer Order → Correct-Course Project Truth → installable coexistence), not an ease-first backlog. Success Metrics validate the bet (pain cut, coherence, Core-patch failure); SM-C1 is a real counter-metric; ecosystem adoption is deferred (§7). MVP kind matches a problem-solving complementary module for a Pilot Team, not a revenue or polish play.

### Findings
_None._

## Done-ness clarity — adequate
Most FRs carry testable consequences: enrollment Hard Block until deps declared or marked none (FR-5), non-zero blocked result with no undocumented override (FR-6), soft Claim warns without blocking git (FR-2), install without vendor edits (FR-11). That is enough for story slicing on F1–F3 and F6. Weak spots are Layer Order and Correct-Course, where “project rules” and change-significance absorb the hard semantics an engineer needs for “done,” and SM-2/SM-3 stay directional rather than operational for Pilot Team validation.

### Findings
- **high** Layer Order gate semantics underspecified (§4.4 FR-8) — “required prior-layer Stories” and “allowed ready state per project rules” have no testable definition of *which* Stories count as priors or *which* standard BMAD statuses pass. *Fix:* State the default rule (e.g. all Stories tagged with earlier Layers in `sprint-status` must be in `{ready-for-dev, in-progress, done}` / or only Stories listed as deps / or layer-complete marker) and name the status set; leave only project overrides as configuration.
- **medium** Correct-Course trigger and coherent-merge signal fuzzy (§4.5 FR-9) — “significant mid-flight change” and refuse “‘coherent merge’ / Build-ready signal” while impact items unchecked leave the start/stop conditions to interpretation. *Fix:* Define the trigger (e.g. any Correct-Course skill run, or status/dependency graph change affecting ≥1 in-progress Story) and the concrete Module signal that means “impact review complete.”
- **medium** SM-2 / SM-3 not operationally measurable (§7) — “Fewer large shared-artifact merges…” and “align more often than they diverge” validate important FRs but give the Pilot Team no count, diary rubric, or pass threshold. *Fix:* Add a minimal pilot protocol (e.g. weekly count of conflicted `_bmad-output` merges; binary weekly “docs/status/code agree after Correct-Course: Y/N”) without pretending precision.
- **low** NFR-3 / SM-C1 lack a proxy (§4A NFR-3, §7 SM-C1) — “feel like a normal fast preflight” / “not significantly slower” is honest for v1 but gives Architecture nothing to regress against. *Fix:* Optional pilot proxy (e.g. gate check wall-clock p95, or “preflight steps added ≤ N”) marked as watch-only.

## Scope honesty — strong
Non-Goals (§5) and MVP Out of Scope (§6.2) do real work: smart merge deferred with direction kept; hard Claim locks deferred unless Pilot proves soft check insufficient; multi-repo orchestration refused for v1; parallel status vocabulary and Core fork refused. Brief overrides are explicit in §1.1. SM-1 baseline is tagged `[ASSUMPTION]` (§7) and indexed (§9). Open-item density is low for OSS-launch stakes — good — but §8’s empty Open Questions understates residual product ambiguities that still affect Architecture kickoff.

### Findings
- **medium** Empty Open Questions oversells closure (§8) — “None phase-blocking… Residual items deferred in MVP Out of Scope” while FR-8/FR-9 still need default gate/trigger rules that are not deferred Non-Goals. *Fix:* Add 2–3 Open Questions (or `[NOTE FOR PM]`) for Layer prior-Story default, Correct-Course trigger, and Pilot measurement of SM-2/SM-3; keep them non-blocking but visible.

## Downstream usability — adequate
Glossary (§3) anchors Module, Dependency Gate, Hard Block, Project Truth, Artifact Lifecycle Status; FR / UJ / SM / NFR IDs are contiguous and cross-refs (“Realizes UJ-…”, “Validates FR-…”) resolve. UJs name protagonists with context inline. Shape is chain-top (Document Purpose → Architecture / Epics / Build). Gaps: cited Discovery digest missing from the workspace folder; “project rules” used as a load-bearing phrase without Glossary entry; JTBD-1 cited in F3 without numbered JTBD IDs in §2.1.

### Findings
- **medium** Broken Discovery cross-ref (§0 Document Purpose) — cites `research-digest.md` in this folder; file is not present alongside `prd.md` / `.memlog.md`. *Fix:* Restore the digest into the PRD folder or retarget the path to wherever Discovery lives.
- **low** “Project rules” undefined (§4.4 FR-8, §4.5 FR-10) — used as the escape hatch for ready states and status transitions but absent from Glossary. *Fix:* Glossary entry or replace with named Module config keys.
- **low** JTBD ID mismatch (§2.1 vs §4.3) — F3 says “Realizes UJ-1, JTBD-1” but §2.1 lists jobs as bullets without JTBD-N IDs. *Fix:* Number the three JTBDs in §2.1.

## Shape fit — strong
Product is an installable complementary BMAD module (skills/scripts/conventions in git; no UI/SaaS). Capability-first Features with light UJs (§2.3 note: “Light format (module / CLI)”) match that shape — not consumer-product UJ density, not regulatory constraint matrices. Positioning against methodology peers and Core-fork patches (§1.1) fits an OSS ecosystem module. NFRs emphasize compatibility, workflow cost, and git-native state over SaaS SLAs. Neither over-formalized nor under-specified for launch stakes.

### Findings
_None._

## Mechanical notes
- **Assumptions Index roundtrip:** Inline `[ASSUMPTION]` on SM-1 (§7) appears in §9; §9 also lists cleared items and narrative notes (FR-5/FR-9 promotions, NFR-3, primary sufferers) that are no longer inline tags — fine as history, slightly noisy as an index.
- **ID continuity:** FR-1–12, UJ-1–4, SM-1–5, SM-C1, NFR-1–8 contiguous; no duplicates spotted. F1–F6 feature groups map cleanly to FR ranges.
- **Glossary drift:** Mostly consistent (“Claim / Ownership”, “Hard Block”, “Project Truth”). Watch synonyms “Build” / “Story start” / “Story execution” — used interchangeably in FR-6/FR-9; acceptable if Architecture treats them as one Module-wrapped entrypoint.
- **Missing artifact:** `research-digest.md` referenced in §0 but absent from the PRD folder (see Downstream finding).
- **Required sections for stakes:** Vision, Users/UJs, Glossary, Features+FRs, NFRs, Non-Goals, MVP, Success Metrics, Open Questions, Assumptions Index — present and appropriately weighted for OSS module launch.
