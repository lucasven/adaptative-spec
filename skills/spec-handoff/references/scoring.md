# Scoring: Answers → Suggested Rungs

Mechanical mapping from question answers to per-pillar rungs. These are *suggestions* the skill computes; the user adjusts as needed.

## Convention

Throughout: rungs are 1 (loosest) through 4 (tightest). Each pillar starts at a *default* rung and accumulates *adjustments* based on specific answers.

## Intent rung

```
default = 1
if novelty in {partially, no}: +1
if novelty == no AND novelty_followup is null: +1   (genuine greenfield, no reference pattern)
if blast == system: +1                               (high blast warrants explicit success criteria)
cap at 4
```

Why: novel work needs explicit success criteria because there's no familiar shape carrying the intent. Greenfield with no reference is even higher novelty than novel-with-reference. High blast independently demands explicit success because failures are visible.

## Interface rung

```
if inherited_contract is not null:
    rung = 4    # inherited, point to the existing artifact
else:
    default = 2
    if blast in {multiple, system}: +1   (it's a contract others depend on)
    if reversibility == migration: +1     (interfaces calcify)
    cap at 4
```

Why: interfaces are most expensive to change once others depend on them. When inherited, jump straight to 4 and reference the existing artifact rather than authoring a duplicate.

## Behavior rung

```
default = 2
if edge_density in {mixed, high}: +1
if edge_density == high AND blast in {multiple, system}: +1
if blast == system AND blast_followup == "yes": +1   (money/auth/data/contracts)
cap at 4
```

Why: edge density is the primary signal because behavior rigor is mostly about enumerating non-happy-path cases. The compounding bumps reflect the categories where edge cases are also the highest-stakes.

## Verification rung

```
verification_default = behavior_rung    # V ≥ B by default
if blast == system: at least 3
if blast == system AND blast_followup == "yes": 4    (recommended)
if reversibility == migration: at least 3
cap at 4
```

Verification is computed as the maximum of: the Behavior rung (V ≥ B floor), and the rung implied by blast and reversibility independently.

If the user explicitly wants V < B, the skill complies and notes once: "rules without checks — intentional?" It does not auto-correct.

## Pattern detection (suggestions, not gates)

After computing the four rungs, evaluate these patterns and surface them as notes:

```
if all rungs == 4:
    note: "this scored high across all pillars. It might be one task with a lot
    of design surface, or it might be several. Splitting first usually produces
    better specs in the multi-piece case. The skill can produce all-4 artifacts
    if you want them either way."
elif all rungs == 1 AND (blast in {multiple, system} OR reversibility != flag):
    note: "this scored as trivial. Worth a sanity check on whether you've
    under-counted blast radius or reversibility — familiarity is when these
    get under-weighted."
```

Both are suggestions the user can ignore. The skill produces artifacts at the suggested rungs unless the user adjusts.

## Worked examples (validation)

These reproduce the four examples from the design conversation against this formula.

### Example A — LLM provider adapter

Inputs: novelty=yes, blast=multiple, reversibility=flag, inherited_contract="LLMProvider interface", edge_density=mixed.

Computed:
- Intent: 1 (default, no adjustments)
- Interface: 4 (inherited)
- Behavior: 3 (default 2 + edge_density mixed)
- Verification: 3 (V ≥ B floor; blast=multiple doesn't push past behavior)

### Example B — Admin UI screen

Inputs: novelty=yes, blast=feature, reversibility=flag, inherited_contract=null, edge_density=mixed.

Computed:
- Intent: 1
- Interface: 2 (default)
- Behavior: 3 (default 2 + edges mixed)
- Verification: 3 (V ≥ B)

Note: the v1 of this skill discussed an optional rule "+1 Interface if the artifact crosses a serialization boundary (HTTP, persistence, DB)" which would push UI screens to Interface=3. Default leaves it off; the user can add it per-project by editing this file.

### Example C — JSON to Postgres migration

Inputs: novelty=partially, blast=system, reversibility=migration, inherited_contract=null, edge_density=high, blast_followup=yes.

Computed:
- Intent: 2 (default 1 + novelty partially)
- Interface: 4 (default 2 + blast system + reversibility migration)
- Behavior: 4 (default 2 + edges high + edges high & blast system)
- Verification: 4 (raised by blast_followup=yes)

### Example D — Multi-agent infrastructure

Inputs: novelty=no, blast=system, reversibility=migration, inherited_contract=null, edge_density=high, novelty_followup=null, blast_followup=yes.

Computed:
- Intent: 4 (default 1 + novelty no + greenfield + blast system)
- Interface: 4
- Behavior: 4
- Verification: 4

All-4s → note suggesting decomposition. Not a block.

## Implementation

The companion `scripts/score.py` implements this formula. Prefer running the script over manual calculation when answers are already in JSON form — it eliminates arithmetic errors and produces consistent reasoning strings.
