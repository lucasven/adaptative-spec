# Verification — Review Checklist

Walk this after producing the artifact. Mark each box `[x]`, `[ ]` (with one-line note), or `[~]` (with note). Write the annotated checklist as `quality-bar.md` in the output folder.

Information for the user, not a gate.

## Rung 1 — Manual eyeball (sufficiency check)

- [ ] Work is genuinely throwaway, not load-bearing
- [ ] Failure mode is bounded and reversible in minutes
- [ ] A specific human owns "I will look at this" — recorded in `README.md`
- [ ] Decision to skip automation is recorded with the cost-bound that justifies it

## Rung 2 — One happy-path test

- [ ] `acceptance.test.<ext>` executes end-to-end through the same boundary the user will use
- [ ] Test asserts a specific observable outcome (not just "no error thrown")
- [ ] Test runs in CI on every change
- [ ] Test failure produces enough output to diagnose without re-running locally
- [ ] Test is independent — no shared state with other tests

## Rung 3 — Acceptance suite

- [ ] Every example or rule from `behavior/examples.json` (or equivalent) has a corresponding executable test
- [ ] Test data and spec data are the *same file* — no parallel maintenance
- [ ] Both happy and rejection cases execute
- [ ] Suite runs in CI and gates merge
- [ ] Failing test names which rule failed, not just which assertion failed
- [ ] Adding a new rule requires no test-framework boilerplate — only a new entry in the data file

## Rung 4 — Evals + properties + characterization

- [ ] At least one of: `properties.test.<ext>`, `evals.jsonl`, `characterization.<ext>`, mutation testing config, contract tests
- [ ] For property tests: invariants from `behavior/invariants.md` appear as predicates; generators cover the schema's full input space
- [ ] For eval sets: entries are versioned with the codebase; new bugs add new entries
- [ ] For characterization: captured behavior is dated and traceable to a known-good version
- [ ] For mutation testing: minimum mutation score threshold is set and gating
- [ ] Verification artifact runs in CI and produces a numeric quality signal
- [ ] Artifact is machine-extendable — new cases added without restructuring

## Cross-pillar V ≥ B

- [ ] Verification rung ≥ Behavior rung (note if otherwise; intentional V<B is allowed)
- [ ] Every rule/example/state-transition in `behavior/` is referenced by at least one verification check
- [ ] Verification artifacts are executable, not prose descriptions
