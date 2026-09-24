# Pilot Ops — Measurement Diary

Lightweight weekly protocol for validating Success Metrics during the Pilot. Not a gate invariant.

## Cadence

Once per week (~2–3 minutes), plus a one-line note after each Correct-Course run.

## SM-2 — Conflicts and rewrite

| Signal                               | How to record                                                                                        |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| Conflicted merges                    | Count of merge conflicts touching `_bmad-output` in the week                                         |
| Early-start / Correct-Course rewrite | Count of times the team rewrote code because a Story started too early or after Correct-Course drift |

## SM-3 — Project Truth after Correct-Course

After each Correct-Course: **Y/N** — docs, sprint status, and code describe the same system.

## SM-C1 — Preflight cost (watch-only)

| Signal         | How to record                                                                                 |
| -------------- | --------------------------------------------------------------------------------------------- |
| Feel           | **Y/N** — gate/status preflight felt like a normal fast local check (not a separate ceremony) |
| Optional proxy | Wall-clock seconds for Build/status preflight when convenient — not a v1 SLA                  |

## Notes

- SM-1 time-share (~50–60% → 15–25%) remains team-reported / diary; baseline is an estimate until measured.
- Keep entries in a Pilot-chosen plain-text location (e.g. under Module home or team notes); format is ops, not Module schema.
