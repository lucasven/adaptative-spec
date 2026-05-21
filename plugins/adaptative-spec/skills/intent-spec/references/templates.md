# Intent — File Templates

Format templates for each rung. For complete worked examples, see `examples.md`.

## Rung 1 — README.md

```markdown
# <Task name>

When <actor or trigger>, the <system component> <does action> so that <observable outcome>.
```

## Rung 2 — story.md

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

## Rung 2 — README.md

```markdown
# <Task name>

<one-sentence summary>

See `story.md` for the user story, acceptance criteria, and non-goals.
```

## Rung 3 — README.md (working-backwards)

The README is the artifact. Write as if the feature already shipped.

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

<Optional. Questions a real user would ask, answered.>
```

## Rung 4 — example-map.md

(In addition to the rung-3 README.md)

```markdown
# Example map

## Rules

1. <rule statement>
2. <rule statement>

## Examples

- [Rule 1] <input or scenario> → <expected outcome>
- [Rule 1] <input or scenario> → <expected outcome>  (boundary or negative)
- [Rule 2] <input or scenario> → <expected outcome>

## Open questions

- <question> — <status: deferred to <date>, out of scope, or answered: <answer>>
- <question> — <status>
```
