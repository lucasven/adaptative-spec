---
name: verification-spec
description: Use when the user needs to define how to mechanically check that an implementation is correct — phrases like "how do I test this", "spec the tests", "write the eval", "set up acceptance tests", "what should we assert", or when spec-handoff dispatches Verification artifact production.
---

# Verification Spec

## When to Use

- User asks how to test, verify, or check correctness
- spec-handoff dispatched Verification production at a settled rung
- Need runnable checks before or alongside implementation

**Not this skill:** If the rung isn't settled yet, use `spec-handoff` — it handles discovery and calibration first.

## Inputs

- **Rung** (1–4)
- **Output path** (`verification/` subfolder under spec root)
- **Behavior path** (where behavior artifacts live; verification consumes them)
- **Interface path** (verification runs through the interface boundary)
- **Stack** (for test framework and extensions)

## Quick Reference

| Rung | Files | Method |
|---|---|---|
| 1 | `README.md` | Manual eyeball — owner + cost bound + justification |
| 2 | `README.md` + `acceptance.test.<ext>` | One happy-path test through the real boundary |
| 3 | `README.md` + `acceptance.test.<ext>` | Parameterized suite consuming `behavior/examples.json` |
| 4 | `README.md` + `acceptance.test.<ext>` + ≥1 of: `evals.jsonl`, `properties.test.<ext>`, `characterization.<ext>` | Expanded coverage by dominant risk |

Always write `quality-bar.md`.

## Rung 4: Pick by Dominant Risk

| Risk | File | Notes |
|---|---|---|
| Silent edge-case bugs | `properties.test.<ext>` | Predicates from `behavior/invariants.md` |
| AI/NLU quality regression | `evals.jsonl` | Growing eval set; new bugs become new lines |
| Behavior-preserving refactor | `characterization.<ext>` + `golden-master.json` | Capture-and-freeze |
| Test suite quality unclear | mutation testing config | Stryker / mutmut / PIT |
| Cross-service contract drift | `contracts/` | Pact or schema-driven |

## Constraints per Rung

**Rung 2:** Executes through the user-facing boundary. Asserts a specific observable outcome. Runs in CI. Failure output is diagnostic.

**Rung 3:** Every example in `behavior/examples.json` runs as a test. Test data and spec data are the *same file*. Both happy and rejection cases execute. Test names include the rule reference.

**Rung 4:** Property tests use invariants from `behavior/invariants.md` as predicates. Eval entries versioned with the codebase. All artifacts run in CI with a numeric quality signal.

See `references/templates.md` for exact file formats. See `references/examples.md` for a complete worked example.

## Loop Closure

At rung 2+, verification runs as part of the agent's iteration loop. If any check fails, the agent reads the output, modifies code, reruns — autonomous until green.

## Cross-Pillar Check: V ≥ B

Walk `behavior/` artifacts and confirm each rule/example/state-transition is referenced by ≥1 verification check. Annotate gaps in `quality-bar.md`.

## Quality Bar

After producing artifacts, walk `references/quality-bar.md` and write `quality-bar.md`. Information, not a gate.
