---
name: spec-handoff
description: Use when planning a feature, refactor, migration, or any coding task that needs structured specs before delegating to an agent or developer. Trigger on "spec out this task", "what spec do I need", "prepare this for AI", "is this ready to hand off", or when the user mentions calibration, granularity, ATDD, or pillar-based specs (intent, interface, behavior, verification).
---

# Spec Handoff

## When to Use

- User has a task and wants help structuring its spec before delegating
- User is at the boundary between planning and implementation
- User mentions calibration, granularity, ATDD, or pillar-based specs

**Not this skill:** If the rung is already settled for a specific pillar, use the pillar skill directly (`intent-spec`, `interface-spec`, `behavior-spec`, `verification-spec`).

## Purpose

Help the user produce a spec that's structured enough for AI handoff without forcing more ceremony than the task warrants. The skill *first understands the feature*, then calibrates rung-per-pillar from that understanding, then produces artifacts.

This is an **assistive** skill, not a gating one. It never says "do not proceed." It says "here's what's there, here's what's not, here's what would help if you want it."

## The four pillars

A spec ready for autonomous AI handoff typically pins:

- **Intent** — what success looks like
- **Interface** — the I/O shape
- **Behavior** — the rules under conditions
- **Verification** — how to check correctness

Each pillar has a 4-rung ladder from loose (rung 1) to tight (rung 4). Rungs are calibrated independently per pillar based on the task's actual risk profile — not uniformly. A migration has high blast radius (pushes Behavior + Verification up) but low novelty in intent (Intent stays low). Calibrate per pillar; don't apply uniform process.

## Critical workflow principle

**The AI must understand the feature before applying the framework, not the other way around.** Pillar-level questions (novelty, blast radius, reversibility, etc.) are an internal rubric the AI applies to its own understanding *after* discovery. They are not opening questions to ask the user.

The user should never be asked to score their own task in the framework's vocabulary. If they could do that, they wouldn't need the skill. The AI's job is to discover enough that it can do the scoring itself, then show the user the result and let them adjust.

## Workflow

### Phase 1: Discover

Start by understanding what the user actually wants to build. This phase is conversational, not interrogative. Do not jump to framework questions.

**Open by asking the user to describe the feature in their own words.** Something like: "Tell me about what you want to build — what is it, who uses it, what does success look like for you?" Then listen.

**Form a working understanding of the feature.** As the user talks, build up:

- What the feature does (user-observable outcomes)
- Who/what triggers it
- Where it fits in their system (new module? extends existing? replaces something?)
- What it touches (data, services, UI, external APIs)
- What "done" looks like to them

**Explore the codebase actively.** This is essential — most of the calibration signal comes from the code, not the conversation. While discussing the feature, look for:

- Similar features already in the codebase (signals novelty, finds inheritable artifacts)
- Existing interfaces this feature would extend or conform to (signals interface inheritance)
- Conventions files (`CONVENTIONS.md`, `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`)
- Test structure and frameworks already in use
- Where this feature's data persists (signals blast radius and reversibility)
- Whether the feature touches money, auth, persisted data, or external contracts

Use whatever tools are available to read the codebase. Don't ask the user to paste files when you can grep, glob, or view directly.

**Ask follow-up questions about the feature itself, not about the framework.** Good questions in this phase:

- "When a user does X, what should they see happen?"
- "What about when Y fails — what's the right error?"
- "Does this need to handle [edge case you noticed]?"
- "I see you have a `UserPermissions` schema — should this conform to it?"
- "Should this be reversible if it ships and turns out wrong?"

Bad questions in this phase (these belong to the rubric, not the conversation):

- "Has this shape of work been done in this codebase before?"
- "What's the blast radius?"
- "How reversible is this?"
- "What's the edge case density?"

The user should feel like they're describing their feature, not filling out a form.

**Know when discovery is enough.** You're ready to move on when:

- You could describe the feature back to the user in their own terms and they'd agree
- You know what existing code (if any) it touches or conforms to
- You know roughly where it fits in the system's risk profile
- The user hasn't surfaced new aspects in the last few exchanges

This usually takes 3–8 turns. Less for trivial work; more for genuinely novel features. Don't rush; don't stretch. If the user gives a one-line description and the task is obviously simple ("add a copy-to-clipboard button"), don't force a long discovery — proceed.

If discovery surfaces that the work is actually multiple features bundled together, say so and ask whether they want to spec one at a time or spec the whole thing as one (most often the right answer is "one at a time" — surface this gently).

### Phase 2: Self-calibrate

Now apply the rubric in `references/questions.md` to what you learned. Answer each question *internally* based on your understanding from Phase 1. Do not ask the user these questions — answer them yourself.

If you genuinely cannot answer a rubric question from discovery, that's a signal to ask one more discovery-style question. For example, if you're unsure about reversibility because you don't know the data model, ask "Where does this data end up — in Postgres? A flag? A config file?" — not "How reversible is this change on a scale of high/medium/low?"

Apply the scoring mapping in `references/scoring.md` to compute rungs from your answers.

### Phase 3: Propose calibration

Present the calibration to the user as a proposal, with two parts:

**First, summarize the feature in your own words.** This shows the user you understood, and gives them a chance to correct misunderstandings before they propagate into the spec. Something like:

> "Here's what I understand: you want to build X that does Y when Z happens, conforming to the existing W interface, with the main risk being [the thing you noticed]. Does that match?"

**Then propose the calibration with reasoning per pillar.** Tie each rung to what you learned in discovery, in plain English. Don't reference the rubric question names — translate them to feature-specific language:

> Suggested calibration:
> - **Intent**: rung 2 (story + acceptance criteria) — the feature is new in concept but follows a familiar pattern, so a brief story should be enough.
> - **Interface**: rung 4 (INHERITED) — this conforms to your existing `AgentPermission` Zod schema, no new interface authoring needed.
> - **Behavior**: rung 3 (examples table) — you mentioned several edge cases around threshold boundaries, worth enumerating them as test fixtures.
> - **Verification**: rung 3 (acceptance suite) — matches the behavior rung; reuses the examples table as test data.

**Then ask if it matches their read.** "Want to adjust any of these, or should I proceed?"

If they adjust, update only the relevant rung. They might say "actually this is more novel than you think because we've never done permissions-flagging before" — that bumps Intent or Behavior. They might say "this needs to be at rung 4 because it gates production deploys" — that's a blast-radius adjustment.

Loop until they confirm.

### Phase 4: Inheritance and convention check (mostly already done)

You did most of this during discovery. Confirm the references you'll point to and the conventions you'll match. If any are missing or unclear, ask now.

### Phase 5: Produce the spec folder

Create a folder at the path the user specifies (or `specs/<task-slug>/` by default) with this structure:

```
specs/<task-name>/
├── README.md                    # navigation + calibration summary, ~50 lines
├── calibration.json             # answers + computed rungs + reasoning + discovery notes
├── intent/
├── interface/
├── behavior/
└── verification/
```

For each pillar, dispatch to the corresponding pillar skill (`intent-spec`, `interface-spec`, `behavior-spec`, `verification-spec`) with:
- Chosen rung
- Output path (the pillar's subfolder)
- Inherited artifact references discovered in Phase 1
- Project conventions discovered in Phase 1
- Feature context (what you learned, so the pillar skill doesn't re-discover)

Each pillar skill writes its artifacts as real files with appropriate extensions. See `references/handoff-folder.md` for the template.

### Phase 6: Annotate against quality bars

After producing each artifact, walk its quality bar in `references/quality-bars.md` and write the annotated checklist as `<pillar>/quality-bar.md` alongside the artifact.

Annotation, not enforcement. Failing criteria are surfaced to the user, not blocking.

### Phase 7: Present the folder

Tell the user where the spec is. Briefly summarize what's in it (one line per pillar). Note any quality-bar gaps that came up. Stop. The user takes it from there.

## What discovery looks like in practice

A realistic Phase 1 transcript might go:

> **User**: I want to add a permissions flagging feature where exceeding thresholds marks a permission as needing review.
>
> **AI** (also exploring the codebase): That sounds useful. Let me look at your permissions code first... I see you have `src/permissions/AgentPermission.ts` with a Zod schema, and a `permissions` table with read/write/admin levels. A few questions to make sure I understand:
> - When you say "exceeding thresholds" — what's a threshold? Token budget? Depth? Both?
> - Where should the flag live? A new column on the permission row, or a separate flags table?
> - Who reviews flagged permissions, and where do they see them?
>
> **User**: Thresholds are configured per-tenant. Flag lives on the permission row. Reviewers see flagged ones at the top of the existing review queue.
>
> **AI**: Got it. I see you already have a review queue UI at `src/admin/reviews/`. Two more things:
> - If thresholds change after flagging, should existing flags recompute, or only on next save?
> - What about flagged permissions in production — should this go behind a feature flag for rollout?
>
> **User**: Recompute only on save. No feature flag — it's additive, low risk.
>
> **AI** (now ready to self-calibrate): Here's what I understand: you're adding automatic flagging of agent permissions when per-tenant thresholds are exceeded; the flag is a new column on the existing permission row, computed at save time only, surfaced via your existing review queue. Low blast — additive, easy to disable. Does that match?

Notice what the AI never did: ask "is this novel?" or "what's the blast radius?" or "is it reversible?". It asked feature questions. The framework questions got answered internally — novelty: partial (new column on familiar schema), blast: feature-scoped, reversibility: easy. Those internal answers feed the scoring.

## Cross-pillar defaults

- **V ≥ B by default.** If V<B emerges from scoring, raise V and note. If the user explicitly wants V<B, comply with one note.
- **Format consistency by default.** New artifacts match existing project format choices when discoverable.
- **Inheritance over authorship by default.** Existing artifacts preferred over new ones.

In each case the skill suggests; the user decides.

## Reference files

- `references/questions.md` — Internal rubric (NOT a script to read to the user)
- `references/scoring.md` — Answer-to-rung mapping
- `references/quality-bars.md` — Per-rung checklists for review
- `references/handoff-folder.md` — Folder layout, file extensions, root README template
- `scripts/score.py` — Optional automated scoring (consumes a JSON answers file)

## Per-pillar skills

This skill handles discovery, calibration, and orchestration. The four pillar skills produce artifacts:

- `intent-spec` — Intent artifacts (sentence → story → README → example map)
- `interface-spec` — Interface artifacts (inferred → type → schema → protocol)
- `behavior-spec` — Behavior artifacts (obvious → examples → table → state+invariants)
- `verification-spec` — Verification artifacts (eyeball → test → suite → evals+properties)

Use `spec-handoff` when starting from a feature idea. Use pillar skills directly when the rung is already settled and you just need the artifact produced.
