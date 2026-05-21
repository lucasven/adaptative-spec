# Behavior — Review Checklist

Walk this after producing the artifact. Mark each box `[x]`, `[ ]` (with one-line note), or `[~]` (with note). Write the annotated checklist as `quality-bar.md` in the output folder.

Information for the user, not a gate.

## Rung 1 — Obvious (sufficiency check)

- [ ] Transformation has at most one defensible interpretation given the interface
- [ ] No money, auth, persisted state, or external side effects
- [ ] A peer reviewer would not need to ask "what should it do when X?"
- [ ] Decision to skip an explicit artifact is recorded in `README.md`

## Rung 2 — Worked examples

- [ ] At least 3 input/output pairs in `examples.json`
- [ ] Pairs cover happy path *and* at least one boundary or rejection
- [ ] Inputs are concrete values, not types or descriptions
- [ ] Outputs are concrete values, not "the expected result"
- [ ] Pairs are formatted such that they can be lifted into tests with no rewriting

## Rung 3 — Examples table / decision table / scenarios

- [ ] Form chosen matches the work shape (transformation → examples; logic → decision; flow → scenarios)
- [ ] Every rule in `rules.md` (or condition in `decisions.md`, or scenario in `scenarios.feature`) has at least one example demonstrating it
- [ ] Every example references which rule it demonstrates
- [ ] Boundary cases present (limits, empty, zero, max, off-by-one)
- [ ] Rejection cases present (what gets refused and resulting error)
- [ ] The data file is the canonical source — no rules exist only in prose elsewhere
- [ ] Data file can be consumed by a test runner with mechanical transformation

## Rung 4 — State machine + invariants

- [ ] All states enumerated in `state-machine.md` (no implicit "other" state)
- [ ] All events enumerated
- [ ] Every (state, event) cell filled with target state or explicit "invalid"/"ignored"
- [ ] Initial state and terminal states marked
- [ ] At least one invariant stated in `invariants.md` as plain-language assertion
- [ ] Every invariant checkable from observable system state
- [ ] Invariants reference quantities or relationships, not vibes

## Cross-cutting

- [ ] Artifact data files can be loaded directly into the Verification artifact (dual-purpose)
- [ ] Behavior rung ≤ Verification rung (note if otherwise; intentional V<B is allowed)
