# Calibration Rubric (Internal — NOT a Script)

This is the rubric the AI applies to its own understanding of the feature *after* discovery. **These are not questions to ask the user.** They are questions the AI answers itself based on what it learned in Phase 1.

If the user is asked these questions verbatim, the skill is being used wrong. The whole point is that the AI does discovery first, then applies the rubric to its own understanding.

## How to use this file

After Phase 1 (Discovery), walk through each of the five rubric items and answer it internally. For each one:

1. Form an answer from what you learned about the feature
2. Note your reasoning briefly (this becomes the "reasoning" entry in calibration.json)
3. If you genuinely can't answer, identify the *feature-level* question you need to ask the user — not a framework-level question

Pass the answered rubric to `references/scoring.md` (or `scripts/score.py`) to derive rung suggestions.

## The five rubric items

### R1 — Novelty

> Has this *shape* of work been done in this codebase before?

Answers:
- **yes** — multiple instances of this shape exist; the work is a new instance of a known pattern
- **partially** — some related work exists, but this has aspects that aren't represented yet
- **no** — this is a new pattern with no clear precedent in the codebase

How to answer from discovery: did you find sibling implementations during codebase exploration? Are there comparable features? "Shape" means the work pattern (adding a column, adding a screen, adding a service), not the domain content. The tenth admin screen is "yes" even if the underlying domain is new.

If unclear from discovery: explore more of the codebase before asking the user. The user often doesn't know what shapes exist; the code does.

### R2 — Blast radius

> If this is wrong in production, what's affected?

Answers:
- **feature** — just this feature, internal users only
- **multiple** — multiple features, or external users
- **system** — system-wide, persisted data, money, or external contracts

How to answer from discovery: what does the feature touch? Does it write to shared tables? Does it expose new external endpoints? Does it touch authentication or financial state? You can usually answer this from reading the code, not asking.

If `system` is the answer, also determine: does it specifically involve money, auth, persisted data, or external contracts? (This is the blast follow-up below.)

### R2b — Blast follow-up (only if R2 = system)

> Does this involve money, auth, persisted data, or external contracts?

Answers: yes / no.

If yes, Verification rung is recommended at 4. The reasoning: failures in these categories are silent, expensive, or unrecoverable, and rung-3 verification is not strong enough to catch them.

### R3 — Reversibility

> If the work ships and turns out wrong, how is it undone?

Answers:
- **flag** — revert the PR or flip a feature flag
- **fix** — a follow-up fix, no data loss, minor user impact
- **migration** — data migration, breaking change, or public commitment

How to answer from discovery: does the feature write data that would be hard to roll back? Does it change a public API others depend on? Does it gate a deploy or release? Reversibility is mostly determined by where the feature persists state and who depends on it externally — both visible from the codebase.

### R3b — Reversibility follow-up (only if R3 = migration)

> What's the rollback strategy if something goes wrong post-ship?

This isn't a yes/no — it's a check that the user has thought about rollback. If you can answer it from discovery (you saw a migration pattern, a snapshot system, etc.), note it. If not, surface it to the user gently: "I noticed this involves a data migration. If something goes wrong post-ship, how would you roll back?"

A missing answer here is a soft signal — flag it in the calibration but don't block.

### R4 — Existing contract / inheritance

> Is there an existing interface, schema, or contract this must satisfy?

Answers:
- The path/name of the inherited artifact, OR
- null (no inheritance — this is greenfield at the interface layer)

How to answer from discovery: did you find a relevant Zod schema, TypeScript type, OpenAPI spec, or protocol definition? Did the user mention extending or conforming to something existing? Inheritance is usually the most discoverable signal — it should rarely require asking the user.

### R5 — Edge case density

> Is the work mostly happy-path, or do edge cases dominate?

Answers:
- **low** — <20% of work is edge handling
- **mixed** — 20–50%
- **high** — >50%, edges dominate

How to answer from discovery: this is where conversation with the user matters most. As they describe the feature, count the explicit edge cases they bring up unprompted, plus the ones you ask about during discovery (boundary thresholds, error states, rejection cases, concurrent updates). Parsers, money handling, auth, and state machines almost always answer "high" honestly even when they feel simple.

If the user only described the happy path and didn't surface any edges, that's *itself* a signal — either the work is truly simple (low) or the user hasn't thought about edges yet (which is exactly what the spec is for). Ask one or two probing feature questions: "What happens if the threshold is exactly equal? What about zero? Negative?" — then judge based on the answers.

## Output format after rubric application

Produce a JSON object that scoring can consume:

```json
{
  "novelty": "yes|partially|no",
  "blast": "feature|multiple|system",
  "reversibility": "flag|fix|migration",
  "inherited_contract": null | "string reference",
  "edge_density": "low|mixed|high",
  "blast_followup": null | "yes|no" (if blast=system),
  "reversibility_followup": null | "string rollback plan" (if reversibility=migration),
  "novelty_followup": null | "string reference pattern" (if novelty=no)
}
```

Pass this to `scripts/score.py` or apply `references/scoring.md` directly to compute rungs.

Persist this object in `calibration.json` in the spec folder, alongside the AI's reasoning for each answer (drawn from discovery), so the calibration is auditable later.

## What conversation discovery looks like vs. rubric application

Discovery (Phase 1) and rubric application (Phase 2) sound similar but are distinct. Discovery is open and feature-centric; rubric is closed and framework-centric. Discovery happens *with* the user; rubric happens *internally to the AI*.

Examples of how the same signal surfaces differently:

| Rubric item | Bad (asked to user) | Good (discovered then self-answered) |
|---|---|---|
| Novelty | "Has this shape been done before?" | AI greps for similar features, sees three siblings → novelty=yes |
| Blast | "What's the blast radius?" | AI sees the feature writes to a shared table used by 4 services → blast=multiple |
| Reversibility | "How reversible is this?" | User mentions feature flag in discovery → reversibility=flag |
| Inheritance | "Is there an existing contract?" | AI finds `src/permissions/AgentPermission.ts` during discovery → inherited |
| Edges | "What's the edge case density?" | User brings up 3 edge cases unprompted, AI asks about 2 more → density=high |

The framework should be invisible to the user during discovery. They should feel like they're discussing their feature with someone who's understanding it, not filling out a calibration form.
