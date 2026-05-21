# Intent — Review Checklist

Walk this after producing the artifact. Mark each box `[x]` (met), `[ ]` (not met, with one-line note), or `[~]` (met with caveats, with note). Write the annotated checklist as `quality-bar.md` in the output folder.

This is information for the user, not a gate. Failing criteria don't block production; they identify what's not yet pinned.

## Rung 1 — One sentence

- [ ] Names the actor (who or what triggers it)
- [ ] Names the action (what is done)
- [ ] Names the observable outcome (what changes that someone could see)
- [ ] Fits in one sentence without compound conjunctions
- [ ] Free of implementation language (no file names, function names, libraries)

## Rung 2 — Story + acceptance criteria

- [ ] Has a single primary actor and a single primary value statement
- [ ] At least one acceptance criterion in Given/When/Then (or input/expected) form
- [ ] Every AC has a measurable outcome (state change, output, error — not "works correctly")
- [ ] At least one explicit non-goal listed
- [ ] A reader can describe a scenario the story does *not* cover, given the non-goals

## Rung 3 — Working-backwards README

- [ ] Includes at least one complete usage example (input → output, or trigger → outcome)
- [ ] Documents at least one error case from the user's perspective
- [ ] States what the feature is *not* doing in this version
- [ ] Reads as if the feature already exists (no future tense)
- [ ] A reader unfamiliar with the implementation could predict whether a given output is correct

## Rung 4 — README + example map

- [ ] Every rule has at least two examples (one positive, one negative or boundary)
- [ ] Every example maps to exactly one rule (no orphans)
- [ ] Questions pile is explicitly present and either answered, deferred with a deadline, or marked out of scope
- [ ] Edge cases the user would care about are enumerated, not implied
- [ ] A second reader can identify ambiguities by reading only the artifact
