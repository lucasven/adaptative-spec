# Quality Bars (Review Checklists)

Each bar is a checklist for *review*, not a gate. The skill walks the bar after producing each artifact, marks each criterion pass/fail, and writes the annotated checklist as `<pillar>/quality-bar.md` alongside the artifact.

Failing criteria don't block anything. They tell the user what's not yet pinned, so the user can decide: fix it, climb a rung, or accept the gap as intentional.

## Format

When annotating, use:

- `[x]` for criteria that pass
- `[ ]` for criteria that don't pass (with a one-line note explaining what's missing)
- `[~]` for criteria that pass with caveats (with a note)

Example annotation:

```markdown
- [x] Names the actor (who or what triggers it)
- [x] Names the action
- [ ] Names the observable outcome — current spec says "system handles it"; concrete outcome not stated
- [x] Fits in one sentence
- [~] Free of implementation language — mentions "Postgres" but only in passing
```

The user reads this and decides what to act on.

## Intent

### Rung 1 — One sentence

- [ ] Names the actor (who or what triggers it)
- [ ] Names the action (what is done)
- [ ] Names the observable outcome (what changes that someone could see)
- [ ] Fits in one sentence without compound conjunctions
- [ ] Free of implementation language (no file names, function names, libraries)

### Rung 2 — Story + acceptance criteria

- [ ] Has a single primary actor and a single primary value statement
- [ ] At least one acceptance criterion in Given/When/Then (or input/expected) form
- [ ] Every AC has a measurable outcome (state change, output, error — not "works correctly")
- [ ] At least one explicit non-goal listed
- [ ] A reader can describe a scenario the story does *not* cover, given the non-goals

### Rung 3 — Working-backwards README

- [ ] Includes at least one complete usage example (input → output, or trigger → outcome)
- [ ] Documents at least one error case from the user's perspective
- [ ] States what the feature is *not* doing in this version
- [ ] Reads as if the feature already exists (no future tense)
- [ ] A reader unfamiliar with the implementation could predict whether a given output is correct

### Rung 4 — README + example map

- [ ] Every rule has at least two examples (one positive, one negative or boundary)
- [ ] Every example maps to exactly one rule (no orphans)
- [ ] Questions pile is explicitly present and either answered, deferred with a deadline, or marked out of scope
- [ ] Edge cases the user would care about are enumerated, not implied
- [ ] A second reader can identify ambiguities by reading only the artifact

## Interface

### Rung 1 — Inferred (sufficiency check)

- [ ] Shape determined by ≥ 2 sibling implementations the AI can read
- [ ] Sibling implementations agree on the shape (no drift)
- [ ] Sibling code is in scope for the AI's context
- [ ] Decision to skip an explicit artifact is recorded

### Rung 2 — Type signature

- [ ] Every parameter and return value has a named type (no `any`, no untyped dicts, no `interface{}`)
- [ ] Optional vs required is explicit
- [ ] Compound types are named, not inlined repeatedly
- [ ] The type compiles or type-checks in the target system
- [ ] Reading the signature alone tells you what the function consumes and produces

### Rung 3 — Schema with constraints

- [ ] Every field has a type
- [ ] Every field has stated optionality (required, optional, nullable — distinguished)
- [ ] Constraints beyond type are expressed (ranges, enums, regex, length bounds, conditional)
- [ ] An error format for validation failures is defined (shape, not just "throws")
- [ ] Schema can be parsed by a runtime validator (not just static types)
- [ ] Invalid inputs produce structured rejections, not crashes

### Rung 4 — Protocol specification

- [ ] Every operation has named inputs, named outputs, and named error cases
- [ ] A versioning strategy is stated
- [ ] Idempotency semantics stated for every mutating operation
- [ ] Authentication and authorization expectations explicit per operation
- [ ] Transport semantics explicit (sync/async, streaming, ordering, delivery guarantees)
- [ ] A consumer could implement against the spec without reading the producer's source

## Behavior

### Rung 1 — Obvious (sufficiency check)

- [ ] Transformation has at most one defensible interpretation given the interface
- [ ] No money, auth, persisted state, or external side effects
- [ ] A peer reviewer would not need to ask "what should it do when X?"
- [ ] Decision to skip an explicit artifact is recorded

### Rung 2 — Worked examples

- [ ] At least 3 input/output pairs
- [ ] Pairs cover happy path *and* at least one boundary or rejection
- [ ] Inputs are concrete values, not types or descriptions
- [ ] Outputs are concrete values, not "the expected result"
- [ ] Pairs are formatted such that they can be lifted into tests with no rewriting

### Rung 3 — Examples / rules table (or decision table, or scenarios)

- [ ] Form chosen matches the work shape (transformation → examples; logic → decision; flow → scenarios)
- [ ] Every rule has at least one example demonstrating it
- [ ] Every example references which rule it demonstrates
- [ ] Boundary cases present (limits, empty, zero, max, off-by-one)
- [ ] Rejection cases present (what gets refused and resulting error)
- [ ] Table is the canonical source — no rules exist only in prose elsewhere
- [ ] Table can be consumed by a test runner with mechanical transformation

### Rung 4 — State machine + invariants

- [ ] All states enumerated (no implicit "other" state)
- [ ] All events enumerated
- [ ] Every (state, event) cell filled with target state or explicit "invalid"/"ignored"
- [ ] Initial state and terminal states marked
- [ ] At least one invariant stated as plain-language assertion
- [ ] Every invariant checkable from observable system state
- [ ] Invariants reference quantities or relationships, not vibes

## Verification

### Rung 1 — Manual eyeball (sufficiency check)

- [ ] Work is genuinely throwaway, not load-bearing
- [ ] Failure mode is bounded and reversible in minutes
- [ ] A specific human owns "I will look at this"
- [ ] Decision to skip automation is recorded with the cost-bound that justifies it

### Rung 2 — One happy-path test

- [ ] Test executes end-to-end through the same boundary the user will use
- [ ] Test asserts a specific observable outcome (not just "no error thrown")
- [ ] Test runs in CI on every change, not on demand
- [ ] Test failure produces enough output to diagnose without re-running locally
- [ ] Test is independent — no shared state with other tests

### Rung 3 — Acceptance suite

- [ ] Every example or rule from Behavior rung 3 has a corresponding executable test
- [ ] Test data and spec data are the *same artifact* — not maintained in parallel
- [ ] Both happy and rejection cases execute
- [ ] Suite runs in CI and gates merge
- [ ] Failing test names which rule failed, not just which assertion failed
- [ ] Adding a new rule requires no test-framework boilerplate — only a new row

### Rung 4 — Evals + properties + characterization

- [ ] At least one of: property-based generator, eval set with growing entries, characterization snapshot, mutation-tested suite, contract tests
- [ ] For property tests: invariants from Behavior rung 4 appear as predicates; generator covers the schema's full input space
- [ ] For eval sets: every reported bug becomes a new entry; entries are versioned with the codebase
- [ ] For characterization tests: captured behavior is dated and traceable
- [ ] Verification artifact runs in CI and produces a numeric quality signal
- [ ] Artifact is machine-extendable — new cases added without restructuring

## Cross-pillar (review checklist)

- [ ] Every rule/example/state-transition in the Behavior artifact is referenced by at least one Verification check
- [ ] Behavior table row count ≤ Verification test count (for tabular formats)
- [ ] Verification rung ≥ Behavior rung (note if otherwise; intentional V<B is allowed)
- [ ] Format choices match project conventions where discoverable
