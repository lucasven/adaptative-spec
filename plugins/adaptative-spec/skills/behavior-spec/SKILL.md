---
name: behavior-spec
description: Use when the user needs to pin down rules under conditions — what outputs follow from what inputs, what state transitions are valid, what must always hold true. Trigger on "what are the rules", "spec the logic", "list the cases", "design the state machine", "what are the invariants", or when spec-handoff dispatches Behavior artifact production.
---

# Behavior Spec

## When to Use

- User asks to enumerate rules, cases, edge cases, or state transitions
- spec-handoff dispatched Behavior production at a settled rung
- Need to define what the system does under each condition

**Not this skill:** If the rung isn't settled yet, use `spec-handoff` — it handles discovery and calibration first.

## Inputs

- **Rung** (1–4)
- **Output path** (`behavior/` subfolder under spec root)
- **Interface artifact** (behavior described in terms of the interface)
- **Stack** (for data file format and idioms)
- **Work shape** (transformation, branching, user flow, workflow, stateful)

## Quick Reference

| Rung | Files | Method |
|---|---|---|
| 1 | `README.md` | Record "obvious" decision + justification |
| 2 | `README.md` + `examples.json` | Worked input/output pairs (≥3 including one rejection) |
| 3 | `README.md` + `rules.md` + `examples.json` — OR `decisions.md` — OR `scenarios.feature` | Rules + test-fixture data; form matches work shape |
| 4 | `README.md` + `state-machine.md` + `invariants.md` + `examples.json` | States/events enumerated, invariants as checkable assertions |

Always write `quality-bar.md`.

## Picking the Form at Rung 3+

| Work shape | Form |
|---|---|
| Pure transformation (input → output) | `examples.json` + `rules.md` |
| Branching / conditional logic | `decisions.md` (decision table) |
| User-facing flow with sequences | `scenarios.feature` (Gherkin) |
| Multi-step workflow | `events.md` (event-storming timeline) |
| Stateful entity with transitions | `state-machine.md` (rung 4) |

Ask: "What's the dominant question for any input?" If "what does it produce?" → examples. If "which branch fires?" → decisions. If "what happens next?" → scenarios or state machine.

## Constraints per Rung

**Rung 2:** Concrete values, not placeholders. ≥3 cases including one boundary/rejection. Lift-able into tests directly.

**Rung 3:** Every rule has ≥1 example including boundaries and rejections. Each example references which rule(s) it exercises.

**Rung 4:** All states and events enumerated. Every (state, event) cell filled. Initial/terminal states marked. ≥1 invariant: plain language, checkable from observable state.

See `references/templates.md` for exact file formats. See `references/examples.md` for a complete worked example.

## Dual-Purpose: Behavior is Test Fixtures

`examples.json`, decision tables, and state-machine examples load directly into the verification artifact. Same source, two consumers. This is the V≥B promise made concrete.

## Quality Bar

After producing artifacts, walk `references/quality-bar.md` and write `quality-bar.md`. Information, not a gate.
