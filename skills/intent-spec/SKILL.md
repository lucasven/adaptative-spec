---
name: intent-spec
description: Use when the user needs to pin down what success looks like for a task — phrases like "what does done mean", "spec out the intent", "write the user story", "draft the README", "what's the goal", or when spec-handoff dispatches Intent artifact production at a settled rung.
---

# Intent Spec

## When to Use

- User asks what "done" means or needs goals defined
- spec-handoff dispatched Intent production at a settled rung
- Need to pin down success criteria before implementation

**Not this skill:** If the rung isn't settled yet, use `spec-handoff` — it handles discovery and calibration first.

## Inputs

- **Rung** (1–4)
- **Task description** (free text from the user)
- **Output path** (`intent/` subfolder; default `specs/<task-slug>/intent/`)
- **Inherited references** (optional — existing stories, READMEs, OKRs to align with)

## Quick Reference

| Rung | Files | Method |
|---|---|---|
| 1 | `README.md` | One declarative sentence: "When *trigger*, the *component* *does action* so that *outcome*." |
| 2 | `README.md` + `story.md` | User story + acceptance criteria + non-goals (INVEST) |
| 3 | `README.md` | Working-backwards README as if the feature shipped (~30-60 lines) |
| 4 | `README.md` + `example-map.md` | Working-backwards README + rules/examples/open questions |

Always write `quality-bar.md`.

## Constraints per Rung

**Rung 1:** One sentence, no compound conjunctions. No implementation language. Outcome confirmable by an observer.

**Rung 2:** Each AC has a measurable outcome (state change, output, error — not "works correctly"). ≥1 explicit non-goal. Apply INVEST.

**Rung 3:** Present tense throughout. No architecture or implementation. A reader unfamiliar with the code can predict correctness.

**Rung 4:** Every rule has ≥2 examples (one positive, one negative/boundary). Every example maps to exactly one rule. Questions pile explicitly present — empty pile suggests rung 3 sufficed.

See `references/templates.md` for exact file formats. See `references/examples.md` for a complete worked example.

## Common Gaps

- **Describing how, not what** — implementation language sneaks in
- **AC as feature list** — "form should be validated" is not a check
- **Empty questions pile at rung 4** — if no ambiguities, rung 3 was enough
- **README in future tense** — working-backwards means *as if shipped*
- **Missing non-goals** — non-goals do as much work as goals

## Quality Bar

After producing artifacts, walk `references/quality-bar.md` and write `quality-bar.md`. Information, not a gate.
