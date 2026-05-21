---
name: intent-spec
description: Produce an Intent specification artifact at a chosen rung (1-4) — a one-line goal, a user story with acceptance criteria, a working-backwards README, or a full example map. Use this whenever the user needs to pin down what success looks like for a task. Trigger on phrases like "what does done mean", "spec out the intent", "write the user story", "draft the README", "what's the goal", or when the parent skill spec-handoff dispatches Intent artifact production. The skill writes its output as files in an `intent/` subfolder and annotates a quality bar checklist alongside — it does not gate or block.
---

# Intent Spec

## Inputs

- **Rung** (1–4)
- **Task description** (free text from the user)
- **Output path** (the `intent/` subfolder under the spec root; default `specs/<task-slug>/intent/`)
- **Inherited references** (optional — existing stories, READMEs, OKRs the artifact should align with)

## Files this skill produces

Per chosen rung, write the following files into the output path:

| Rung | Files |
|---|---|
| 1 | `README.md` (the one-sentence goal in a tiny doc) |
| 2 | `README.md` (orientation, ~10 lines), `story.md` (story + AC + non-goals) |
| 3 | `README.md` (the full working-backwards README, ~30-60 lines) |
| 4 | `README.md` (working-backwards) + `example-map.md` (rules + examples + questions) |

Always also write `quality-bar.md` with the annotated checklist.

## Method per rung

### Rung 1 — One sentence

Write a single declarative sentence using the grammar:

> "When *<actor or trigger>*, the *<system component>* *<does action>* so that *<observable outcome>*."

Constraints:
- One sentence, no compound conjunctions
- No implementation language (no file names, function names, library names)
- The outcome is something a user or external observer could confirm

`README.md` content:

```markdown
# <Task name>

<the single sentence>
```

### Rung 2 — Story + acceptance criteria

`story.md` content:

```markdown
# Story

As a <role>, I want <capability>, so that <value>.

## Acceptance criteria

1. Given <state>, when <action>, then <observable outcome>.
2. Given <state>, when <action>, then <observable outcome>.
3. ...

## Non-goals

- <thing this story is NOT doing>
- <thing this story is NOT doing>
```

Constraints:
- Each AC has a measurable outcome (state change, output, error — not "works correctly")
- At least one explicit non-goal
- Apply INVEST: Independent, Negotiable, Valuable, Estimable, Small, Testable

`README.md` content (~10 lines):

```markdown
# <Task name>

<one-sentence summary>

See `story.md` for the user story, acceptance criteria, and non-goals.
```

### Rung 3 — Working-backwards README

`README.md` is the artifact. Write the README/changelog/usage doc as if the feature already shipped (Amazon working-backwards memo, scaled down).

```markdown
# <Feature name>

<One-paragraph description of what the feature does, in present tense, observable terms.>

## Usage

<At least one complete worked example: input → output, or trigger → outcome.>

## Errors

<At least one error case from the user's perspective: what they did wrong, what they see.>

## Not in this version

<Explicit non-goals.>

## FAQ

<Optional but recommended. Questions a real user would ask, answered.>
```

Constraints:
- Present tense throughout (no "will be", no "we plan to")
- No architecture or implementation discussion — observable behavior only
- A reader unfamiliar with the implementation can predict whether an output is correct

### Rung 4 — README + example map

Write the rung-3 `README.md` as above, then add `example-map.md`:

```markdown
# Example map

## Rules

1. <rule statement>
2. <rule statement>
...

## Examples

- [Rule 1] <input or scenario> → <expected outcome>
- [Rule 1] <input or scenario> → <expected outcome>  (boundary or negative)
- [Rule 2] <input or scenario> → <expected outcome>
- ...

## Open questions

- <question> — <status: deferred to <date>, marked out of scope, or answered: <answer>>
- <question> — <status>
```

Constraints:
- Every rule has at least two examples (one positive, one negative or boundary)
- Every example maps to exactly one rule (no orphans)
- Questions pile is explicitly present — empty questions pile is a soft signal that the work is trivial (try rung 3) or the mapping wasn't honest (revisit)

## Quality bar annotation

After producing the artifact, walk the bar in `references/quality-bar.md` for the chosen rung. Write `quality-bar.md` in the output folder with each criterion marked:

- `[x]` if the criterion is met
- `[ ]` if not met (with a one-line note explaining what's missing)
- `[~]` if met with caveats (with a note)

The annotation is information, not a gate. The skill produces and writes the artifact regardless of whether all boxes check.

## Common gaps the bar surfaces

- **Describing how, not what.** Implementation language sneaks in. Annotate as `[ ]` and the user can revise.
- **AC as a feature list.** "Form should be validated" is not a check. Annotate.
- **Empty questions pile at rung 4.** If there were no ambiguities, rung 3 was probably enough.
- **README in future tense.** Working-backwards means *as if shipped*. Annotate so the user can shift the tense.
- **Missing non-goals.** Non-goals do as much work as goals — they tell the AI what NOT to add.

## Reference files

- `references/quality-bar.md` — Per-rung review checklist
- `references/examples.md` — Worked examples of each rung produced from the same task
