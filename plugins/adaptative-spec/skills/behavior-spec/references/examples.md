# Behavior — Worked Examples

The same component rendered at each rung. Different work shapes use different forms at rung 3 — examples here cover all three forms.

## Source component

> `parseExpenseMessage(text)` — extract amount, currency, category, description from a free-form message in Portuguese or English.

## Rung 1 — Obvious (sufficiency check failed; this work needs at least rung 2)

This component fails the rung-1 check: parsing free-form text is the textbook case of "many defensible interpretations exist." Climb.

## Rung 2 — Worked examples

```markdown
## Behavior

| # | Input | Output | Notes |
|---|---|---|---|
| 1 | `gastei 50 no mercado` | `{ amount: 50, currency: "BRL", category: "groceries", description: "mercado" }` | happy path, pt |
| 2 | `spent $12 on coffee` | `{ amount: 12, currency: "USD", category: "food", description: "coffee" }` | happy path, en |
| 3 | `25` | rejection: `{ error: "no_context" }` | bare number |
| 4 | `gastei muito hoje` | rejection: `{ error: "no_amount" }` | no parseable amount |
```

## Rung 3 — Examples table (transformation shape)

```markdown
## Behavior

### Rules
- R1: amount is the first numeric value found
- R2: currency is BRL by default; USD if `$` prefix or `dollar(s)` word
- R3: number format follows locale: `1.250,50` is pt (BRL), `1,250.50` is en (USD)
- R4: category is mapped from description keywords (mercado → groceries, coffee → food, uber → transport, aluguel → housing)
- R5: bare numbers without context are rejected
- R6: messages without a parseable amount are rejected

### Examples

| # | Input | Output | Rule |
|---|---|---|---|
| 1 | `gastei 50 no mercado` | `{ amount: 50, currency: "BRL", category: "groceries", description: "mercado" }` | R1, R2, R4 |
| 2 | `spent $12 on coffee` | `{ amount: 12, currency: "USD", category: "food", description: "coffee" }` | R1, R2 ($), R4 |
| 3 | `uber 35` | `{ amount: 35, currency: "BRL", category: "transport", description: "uber" }` | R1, R2 (default), R4 |
| 4 | `paguei 1.250,50 de aluguel` | `{ amount: 1250.50, currency: "BRL", category: "housing", description: "aluguel" }` | R1, R2, R3 (pt), R4 |
| 5 | `paid 1,250.50 rent` | `{ amount: 1250.50, currency: "USD", category: "housing", description: "rent" }` | R1, R2 (en), R3 (en), R4 |
| 6 | `25` | `rejection: no_context` | R5 |
| 7 | `gastei muito hoje` | `rejection: no_amount` | R6 |
| 8 | `gastei 0 no mercado` | `rejection: invalid_amount` | R1 (boundary: zero) |
| 9 | `spent -50 on coffee` | `rejection: invalid_amount` | R1 (boundary: negative) |
| 10 | `mercado 100 mercado` | `{ amount: 100, currency: "BRL", category: "groceries", description: "mercado mercado" }` | R1 (first number), R4 |
```

## Rung 3 — Decision table (alternate form, for branching logic)

If the same component were *purely* a category classifier, the decision table form would be:

```markdown
| Has "mercado" | Has "coffee/food" | Has "uber/transport" | Has "aluguel/rent" | Category |
|---|---|---|---|---|
| true | * | * | * | groceries |
| false | true | * | * | food |
| false | false | true | * | transport |
| false | false | false | true | housing |
| false | false | false | false | uncategorized |
```

(Decision tables collapse multi-condition branching into a flat enumerable form.)

## Rung 4 — State machine + invariants

The parser doesn't have meaningful state, so this section uses a different example: an **agent lifecycle**.

```markdown
## States

- `idle` — agent created, no task assigned
- `running` — agent has a task and is processing
- `done` — task completed successfully
- `failed` — task completed with error
- `terminated` — agent killed (by parent, by timeout, or by error)

Initial state: `idle`
Terminal states: `done`, `failed`, `terminated`

## Events

- `assign_task` — task delivered to agent
- `complete` — task finished successfully
- `error` — task raised an unhandled error
- `parent_died` — parent agent terminated
- `timeout` — wall-clock deadline exceeded
- `kill` — explicit termination request

## Transitions

|              | assign_task | complete | error      | parent_died  | timeout      | kill         |
|--------------|-------------|----------|------------|--------------|--------------|--------------|
| **idle**     | running     | invalid  | invalid    | terminated   | terminated   | terminated   |
| **running**  | invalid     | done     | failed     | terminated   | terminated   | terminated   |
| **done**     | invalid     | invalid  | invalid    | (no-op)      | (no-op)      | (no-op)      |
| **failed**   | invalid     | invalid  | invalid    | (no-op)      | (no-op)      | (no-op)      |
| **terminated** | invalid   | invalid  | invalid    | (no-op)      | (no-op)      | (no-op)      |

## Invariants

1. An agent's total spawn count over its lifetime is bounded by `MAX_FANOUT` (configured per agent).
2. An agent's tree depth is bounded by `MAX_DEPTH`.
3. When a parent transitions to a terminal state, every descendant transitions to `terminated` within `T_propagation` seconds.
4. An agent in a terminal state never transitions out (terminal states are absorbing).
5. Every `assign_task` event has at most one corresponding `complete` or `error` event.
6. The number of agents in `running` state at any time is ≤ `MAX_CONCURRENT`.
```

## What changes across rungs

- **Rung 1 → 2**: rules become demonstrable but not enumerated. The AI sees the pattern but not the boundary.
- **Rung 2 → 3**: rules become enumerated and named. Rejections become first-class. The artifact becomes machine-checkable.
- **Rung 3 → 4**: state and lifecycle become explicit. Invariants make properties checkable across all paths, not just the enumerated ones. This is where property-based testing earns its keep.

## Same artifact, two pillars

Notice that the rung-3 examples table is *also* the test data. The rung-4 transition table is *also* the test matrix. The invariants list is *also* the property-test predicates. When the Behavior artifact is produced in this form, the Verification artifact reuses it directly — no translation, no drift.
