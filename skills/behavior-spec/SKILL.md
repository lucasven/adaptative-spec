---
name: behavior-spec
description: Produce a Behavior specification artifact at a chosen rung (1-4) — worked examples, an exhaustive rules/examples table, or a state machine with invariants. Use this whenever the user needs to pin down the rules under conditions: what outputs follow from what inputs, what state transitions are valid, what must always hold true. Trigger on phrases like "what are the rules", "spec the logic", "list the cases", "design the state machine", "what are the invariants", or when the parent skill spec-handoff dispatches Behavior artifact production. The skill writes its output as files in a `behavior/` subfolder — examples and rules as data files, state machines as markdown — formatted so they double as test fixtures.
---

# Behavior Spec

## Inputs

- **Rung** (1–4)
- **Output path** (the `behavior/` subfolder under the spec root)
- **Interface artifact** (the behavior is described in terms of the interface — types, schemas, operations)
- **Stack** (for choosing data file format and idioms)
- **Work shape** (transformation, branching logic, user flow, workflow, stateful — picks the right form at rung 3+)

## Files this skill produces

| Rung | Files |
|---|---|
| 1 | `README.md` recording the "obvious" decision and justification |
| 2 | `README.md` + `examples.json` (worked input/output pairs) |
| 3 | `README.md` + `rules.md` (rule statements) + `examples.json` (test-fixture-shaped data) — OR `decisions.md` (decision table) — OR `scenarios.feature` (Gherkin) |
| 4 | `README.md` + `state-machine.md` + `invariants.md` + `examples.json` |

Always write `quality-bar.md`.

## Method per rung

### Picking the right shape at rung 3+

Match the form to the work:

| Work shape | Form |
|---|---|
| Pure transformation (input → output) | `examples.json` + `rules.md` |
| Branching / conditional logic | `decisions.md` (decision table) |
| User-facing flow with sequences | `scenarios.feature` (Gherkin) |
| Multi-step workflow with branches | `events.md` (event-storming timeline) |
| Stateful entity with transitions | `state-machine.md` (used at rung 4) |

Ask "what's the dominant question I need answered for any input?" If "what does it produce?" → examples. If "which branch fires?" → decisions. If "what happens next?" → scenarios or state machine.

### Rung 1 — Obvious

`README.md`:

```markdown
# Behavior (obvious)

The transformation is straightforward given the interface; no edge cases warrant explicit enumeration.

Justification: <one sentence>.
```

### Rung 2 — Worked examples

Write `examples.json` as real data, not embedded in markdown:

```json
[
  { "id": 1, "input": "gastei 50 no mercado", "expected": { "amount": 50, "currency": "BRL", "category": "groceries", "description": "mercado" }, "tag": "happy-path-pt" },
  { "id": 2, "input": "spent $12 on coffee", "expected": { "amount": 12, "currency": "USD", "category": "food", "description": "coffee" }, "tag": "happy-path-en" },
  { "id": 3, "input": "25", "expected_error": "no_context", "tag": "rejection-bare-number" },
  { "id": 4, "input": "gastei muito hoje", "expected_error": "no_amount", "tag": "rejection-no-amount" }
]
```

`README.md`:

```markdown
# Behavior (rung 2 — worked examples)

See `examples.json` for input/output pairs covering the happy path and at least one rejection.

The data file is structured to be loaded directly by `verification/acceptance.test.<ext>` — same source for spec and tests.
```

Constraints:
- Concrete values, not placeholders
- At least 3 cases including one boundary or rejection
- Lift-able into tests with no rewriting

### Rung 3 — Examples + rules (transformation shape)

`rules.md`:

```markdown
# Rules

- R1: <rule statement>
- R2: <rule statement>
- R3: <rule statement>
- ...
```

`examples.json` (richer than rung 2 — every rule has at least one example, including boundaries and rejections):

```json
[
  { "id": 1, "input": "gastei 50 no mercado", "expected": { "amount": 50, "currency": "BRL", "category": "groceries", "description": "mercado" }, "rules": ["R1", "R2", "R4"] },
  { "id": 2, "input": "uber 35", "expected": { "amount": 35, "currency": "BRL", "category": "transport", "description": "uber" }, "rules": ["R1", "R2-default", "R4"] },
  { "id": 8, "input": "gastei 0 no mercado", "expected_error": "invalid_amount", "rules": ["R1-boundary-zero"] },
  { "id": 9, "input": "spent -50 on coffee", "expected_error": "invalid_amount", "rules": ["R1-boundary-negative"] }
]
```

`README.md`:

```markdown
# Behavior (rung 3 — examples table)

Work shape: transformation.

- `rules.md` — rule statements
- `examples.json` — test-fixture-shaped data; every rule referenced by at least one example, including boundaries and rejections

The data file is the canonical source for both this spec and `verification/acceptance.test.<ext>`. Do not duplicate.
```

### Rung 3 — Decision table (branching logic)

`decisions.md`:

```markdown
# Decision table

| Condition A | Condition B | Condition C | Action |
|---|---|---|---|
| true | true | * | <action 1> |
| true | false | true | <action 2> |
| true | false | false | <action 3> |
| false | * | * | <action 4> |
```

(Any test runner can iterate over the table rows directly.)

### Rung 3 — Scenarios (user flow)

`scenarios.feature` (Gherkin):

```gherkin
Feature: <feature name>

  Scenario: <happy path name>
    Given <state>
    When <action>
    Then <observable outcome>

  Scenario: <rejection case>
    Given <state>
    When <action>
    Then <observable rejection>
```

### Rung 4 — State machine + invariants

`state-machine.md`:

```markdown
# State machine

## States

- `<state_1>` — <description>
- `<state_2>` — <description>
- ...

Initial state: `<state>`
Terminal states: `<state>`, `<state>`

## Events

- `<event_1>`
- `<event_2>`
- ...

## Transitions

|              | event_1   | event_2 | event_3 |
|--------------|-----------|---------|---------|
| **state_1**  | state_2   | invalid | state_1 |
| **state_2**  | invalid   | state_3 | state_2 |
| **state_3**  | invalid   | invalid | (terminal) |
```

`invariants.md`:

```markdown
# Invariants

Things that must always be true, regardless of code path. Each is checkable from observable system state.

1. <plain-language assertion>
2. <plain-language assertion>
3. <plain-language assertion>
```

`examples.json` (covers state-event combinations):

```json
[
  { "id": 1, "from_state": "idle", "event": "assign_task", "expected_to_state": "running" },
  { "id": 2, "from_state": "running", "event": "complete", "expected_to_state": "done" },
  { "id": 3, "from_state": "done", "event": "assign_task", "expected_error": "invalid_transition" }
]
```

Constraints:
- All states and events enumerated
- Every (state, event) cell filled with target state or explicit "invalid" / "ignored"
- Initial and terminal states marked
- At least one invariant in plain language
- Invariants reference quantities or relationships, not vibes
- Invariants checkable from observable state, not internal implementation

## Dual-purpose: behavior is also test fixtures

The `examples.json` (and decision tables, and state-machine examples) are designed to be loaded directly by the verification artifact. Same source, two consumers:

- The spec consumer: a human or AI reading what the rules are
- The test consumer: a `test.each(cases)` loop or a Cucumber runner

This is the V≥B promise made concrete: when behavior data is shaped right, verification reuses it without translation, eliminating drift.

## Quality bar annotation

After producing artifact(s), walk `references/quality-bar.md` and write `quality-bar.md` with each criterion marked. Information, not a gate.

## Reference files

- `references/quality-bar.md` — Per-rung review checklist
- `references/examples.md` — Worked examples per rung
