# Analysis Report: /workspaces/bmad-multi-user/skills/team-ready

Generated: 2026-09-24T13:30:55Z · Schema: 2

**Grade: Fair**

> Solid lean mutator with clean script placement; high findings cluster on Overview heading and incomplete headless propose/memlog contracts.

team-ready is a tight set/propose skill with correct intelligence placement (frontmatter via script) and a right-sized customize.toml. Highest leverage fixes: add ## Overview, define headless propose as recommendation-only JSON with memlog audit trail, and surface soft_offer in headless set returns. The .memlog.md path-scan hit conflicts with builder process-memory conventions — do not move it into references/.

| Severity | Count |
| --- | --- |
| Critical | 0 |
| High | 5 |
| Medium | 2 |
| Low | 4 |

## Themes

### 1. Incomplete headless contracts

- Root cause: Set documents headless JSON; Propose and assumption logging do not, so automators dead-end or lose audit trail.
- Fix: Specify headless propose as recommendation-only JSON; wire memlog.py for assumptions; add soft_offer on PRD→ready set returns.
- Findings:
  - `architecture-3` Headless Propose has no executable path — `SKILL.md:Propose`
  - `architecture-4` Headless assumption trail not wired — `SKILL.md:On Activation / Set`
  - `enhancement-1` Add headless memlog for assumptions — `SKILL.md:On Activation; Set`
  - `enhancement-2` Define headless propose contract — `SKILL.md:Propose`
  - `enhancement-3` Surface team-drift soft-offer in headless JSON — `SKILL.md:Set`

### 2. Section contract vs destination prose

- Root cause: Destination content exists but is not under ## Overview, so integrity scanners and agents looking for the standard heading miss it.
- Fix: Rename/promote the opening destination block to ## Overview.
- Findings:
  - `architecture-1` Missing ## Overview section — `SKILL.md`

### 3. Builder memlog vs path topology

- Root cause: Path-standards forbids non-SKILL.md markdown at root; workflow-builder keeps .memlog.md at skill root as process memory.
- Fix: Leave .memlog.md at root for this build; prefer scanner exclude for .memlog.md rather than relocating process memory.
- Findings:
  - `architecture-2` Markdown file at skill root — `.memlog.md`

### 4. Light prose density

- Root cause: Small restatements between Outcome/Constraints/Propose numbering.
- Fix: Trim Constraints duplication, keep soft-offer only in Set, collapse Propose to a goal sentence, optional skip-confirm when explicit.
- Findings:
  - `leanness-1` Constraints restates Outcome bar — `SKILL.md:Constraints`
  - `leanness-2` Soft-offer team-drift lives in Bar and Set — `SKILL.md:Outcome; SKILL.md:Set`
  - `leanness-3` Propose numbering is decoration — `SKILL.md:Propose`
  - `enhancement-4` Skip Set confirm when utterance fully explicit — `SKILL.md:Set step 2`

## Strengths

- Deterministic frontmatter get/set isolated in artifact_status.py with tests
- customize.toml universal-only is correct for an in-place mutator; SKILL.md reads {workflow.*}
- Clear set vs propose intents; soft-offer team-drift without auto-start
- SKILL.md well under token budget (~876)

## Recommendations

1. Add ## Overview and harden headless propose + memlog + soft_offer JSON in one pass (resolves: architecture-1, architecture-3, architecture-4, enhancement-1, enhancement-2, enhancement-3)
2. Trim leanness restatements (Constraints/Bar/Propose numbering) (resolves: leanness-1, leanness-2, leanness-3)
3. Leave .memlog.md; note path-scan false conflict for builder memlog (resolves: architecture-2)
4. Optional: skip interactive confirm when path+status already explicit (resolves: enhancement-4)

## Experience

- **Interactive set** — Activate → pick artifact → confirm status → script set → report → soft-offer team-drift if PRD ready
- **Interactive propose** — Activate → judge → recommend → wait accept → Set
- **Headless set** — Infer intent → script set → JSON complete (needs memlog/soft_offer fields)
- Headless: Set path is sketched; Propose and assumption audit trail are incomplete for automators.

## Findings

### High (5)

#### architecture-1 — Missing ## Overview section

- Lens: architecture
- Location: `SKILL.md`
- Evidence: Destination prose under # team-ready; integrity pre-pass flags Missing ## Overview.
- Recommendation: Promote opening block into ## Overview.

#### architecture-2 — Markdown file at skill root

- Lens: architecture
- Location: `.memlog.md`
- Evidence: Path-standards fails on .memlog.md at root.
- Recommendation: Builder process memory belongs at skill root per workflow-builder; treat scanner hit as known conflict — do not move to references/. Prefer excluding .memlog.md from path scan long-term.

#### architecture-3 — Headless Propose has no executable path

- Lens: architecture
- Location: `SKILL.md:Propose`
- Evidence: Propose waits for accept; no headless JSON path.
- Recommendation: Headless propose: recommendation-only JSON, no write; or mark propose interactive-only and blocked.

#### enhancement-1 — Add headless memlog for assumptions

- Lens: enhancement
- Location: `SKILL.md:On Activation; Set`
- Evidence: No memlog init/append for headless assumptions; JSON omits memlog path.
- Recommendation: Wire memlog.py for headless assumptions; return memlog path.

#### enhancement-2 — Define headless propose contract

- Lens: enhancement
- Location: `SKILL.md:Propose`
- Evidence: Propose accept-gated; headless JSON only under Set.
- Recommendation: Headless propose recommendation-only JSON; apply via separate set.

### Medium (2)

#### architecture-4 — Headless assumption trail not wired

- Lens: architecture
- Location: `SKILL.md:On Activation / Set`
- Evidence: Says log assumption but no memlog.py path in JSON.
- Recommendation: Append via memlog.py; include memlog path in headless JSON.

#### enhancement-3 — Surface team-drift soft-offer in headless JSON

- Lens: enhancement
- Location: `SKILL.md:Set`
- Evidence: Interactive soft-offer not in headless schema.
- Recommendation: Add soft_offer: team-drift when PRD newly ready; do not auto-start.

### Low (4)

#### leanness-1 — Constraints restates Outcome bar

- Lens: leanness
- Location: `SKILL.md:Constraints`
- Evidence: Constraints repeats allowed statuses and --actor already in Outcome/Bar.
- Recommendation: Keep only non-bar rules in Constraints (legacy mapping, no sidecar, no locks/vendor edits).

#### leanness-2 — Soft-offer team-drift lives in Bar and Set

- Lens: leanness
- Location: `SKILL.md:Outcome; SKILL.md:Set`
- Evidence: Soft-offer appears in Bar and Set step 4.
- Recommendation: Remove soft-offer from Outcome Bar; keep in Set with do-not-auto-start.

#### leanness-3 — Propose numbering is decoration

- Lens: leanness
- Location: `SKILL.md:Propose`
- Evidence: 1-2-3 list for one obligation.
- Recommendation: Collapse Propose to one goal sentence.

#### enhancement-4 — Skip Set confirm when utterance fully explicit

- Lens: enhancement
- Location: `SKILL.md:Set step 2`
- Evidence: Always confirms interactively even when path+status explicit.
- Recommendation: Skip confirm when both named; keep when ambiguous.
