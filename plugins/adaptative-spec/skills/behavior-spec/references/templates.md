# Behavior — File Templates

Format templates for each rung. For complete worked examples, see `examples.md`.

## Rung 1 — README.md

```markdown
# Behavior (obvious)

The transformation is straightforward given the interface; no edge cases warrant explicit enumeration.

Justification: <one sentence>.
```

## Rung 2 — examples.json

```json
[
  { "id": 1, "input": "<concrete input>", "expected": { "<field>": "<value>" }, "tag": "<descriptive-tag>" },
  { "id": 2, "input": "<concrete input>", "expected": { "<field>": "<value>" }, "tag": "<descriptive-tag>" },
  { "id": 3, "input": "<boundary input>", "expected_error": "<error_code>", "tag": "<descriptive-tag>" }
]
```

## Rung 2 — README.md

```markdown
# Behavior (rung 2 — worked examples)

See `examples.json` for input/output pairs covering the happy path and at least one rejection.

The data file is structured to be loaded directly by `verification/acceptance.test.<ext>` — same source for spec and tests.
```

## Rung 3 — rules.md (transformation shape)

```markdown
# Rules

- R1: <rule statement>
- R2: <rule statement>
- R3: <rule statement>
```

## Rung 3 — examples.json (transformation shape)

```json
[
  { "id": 1, "input": "<input>", "expected": { "<field>": "<value>" }, "rules": ["R1", "R2"] },
  { "id": 2, "input": "<boundary>", "expected_error": "<error>", "rules": ["R1-boundary-zero"] }
]
```

## Rung 3 — README.md (transformation shape)

```markdown
# Behavior (rung 3 — examples table)

Work shape: transformation.

- `rules.md` — rule statements
- `examples.json` — test-fixture-shaped data; every rule referenced by at least one example, including boundaries and rejections

The data file is the canonical source for both this spec and `verification/acceptance.test.<ext>`. Do not duplicate.
```

## Rung 3 — decisions.md (branching logic)

```markdown
# Decision table

| Condition A | Condition B | Condition C | Action |
|---|---|---|---|
| true | true | * | <action 1> |
| true | false | true | <action 2> |
| true | false | false | <action 3> |
| false | * | * | <action 4> |
```

## Rung 3 — scenarios.feature (user flow)

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

## Rung 4 — state-machine.md

```markdown
# State machine

## States

- `<state_1>` — <description>
- `<state_2>` — <description>

Initial state: `<state>`
Terminal states: `<state>`, `<state>`

## Events

- `<event_1>`
- `<event_2>`

## Transitions

|              | event_1   | event_2 | event_3 |
|--------------|-----------|---------|---------|
| **state_1**  | state_2   | invalid | state_1 |
| **state_2**  | invalid   | state_3 | state_2 |
| **state_3**  | invalid   | invalid | (terminal) |
```

## Rung 4 — invariants.md

```markdown
# Invariants

Things that must always be true, regardless of code path. Each is checkable from observable system state.

1. <plain-language assertion>
2. <plain-language assertion>
3. <plain-language assertion>
```

## Rung 4 — examples.json (state-event pairs)

```json
[
  { "id": 1, "from_state": "<state>", "event": "<event>", "expected_to_state": "<state>" },
  { "id": 2, "from_state": "<terminal>", "event": "<event>", "expected_error": "invalid_transition" }
]
```
