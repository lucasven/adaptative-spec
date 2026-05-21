# Handoff Folder

The skill produces a folder of real files, not a monolithic markdown document. Code lives in code files; data lives in data files; prose lives in markdown.

## Folder layout

```
specs/<task-slug>/
├── README.md                # navigation + calibration summary, ~50 lines
├── calibration.json         # answers, computed rungs, reasoning, flags
├── intent/
│   ├── README.md            # the intent prose (rung 3+) or a one-line goal (rung 1-2)
│   ├── story.md             # rung 2+ — story + AC + non-goals
│   └── example-map.md       # rung 4 only
├── interface/
│   ├── README.md            # 5-10 lines orienting; points to the schema/protocol files
│   ├── schema.<ext>         # the actual schema (rung 3) — .ts, .py, .json depending on stack
│   ├── types.<ext>          # rung 2 type signatures — only if rung exactly 2
│   └── protocol.md          # rung 4 — protocol-level concerns; references schema files
├── behavior/
│   ├── README.md            # rule statements + cross-references to data files
│   ├── examples.json        # rung 2-3 worked cases as data, not markdown
│   ├── rules.md             # rung 3 rule descriptions
│   └── state-machine.md     # rung 4 only
└── verification/
    ├── README.md            # what's here, how to run it
    ├── acceptance.test.<ext># rung 2-3 — actual runnable test file
    ├── evals.jsonl          # rung 4 — actual eval data
    ├── properties.test.<ext># rung 4 — property-based tests
    ├── characterization.<ext># rung 4 — only for migrations/refactors
    └── quality-bar.md       # the annotated checklist for this pillar
```

Not every file is present at every rung. Each pillar skill writes only the files appropriate for the chosen rung.

## File extension rules

Pick extensions per the project's stack. Default mapping:

| Artifact type | TypeScript/Node | Python | Go |
|---|---|---|---|
| Schema | `.ts` | `.py` | `.go` |
| Test file | `.test.ts` | `_test.py` or `test_*.py` | `_test.go` |
| Eval data | `.jsonl` | `.jsonl` | `.jsonl` |
| Worked examples | `.json` or `.ts` | `.json` or `.py` | `.json` |
| Prose, rules, state machines, READMEs | `.md` | `.md` | `.md` |

If `CONVENTIONS.md` (or equivalent) declares specific extensions, follow it. If unclear, ask the user once.

## Root README template

The root `README.md` is the navigation document. Keep it short — around 50 lines. The user reads it once to orient, then jumps to specific files.

```markdown
# <Task name>

<one-paragraph description, present tense, observable terms>

## Calibration

| Pillar | Rung | Method |
|---|---|---|
| Intent | <N> | <method name> |
| Interface | <N> | <method name or "INHERITED from <ref>"> |
| Behavior | <N> | <method name> |
| Verification | <N> | <method name> |

See `calibration.json` for the answers and reasoning that produced these rungs.

## What's here

- `intent/` — what success looks like
- `interface/` — the I/O shape
- `behavior/` — rules and cases
- `verification/` — runnable checks

## Quality bar status

| Pillar | Status |
|---|---|
| Intent | <N>/<M> criteria checked |
| Interface | <N>/<M> criteria checked |
| Behavior | <N>/<M> criteria checked |
| Verification | <N>/<M> criteria checked |

See `<pillar>/quality-bar.md` for the per-pillar checklists.

## How to run verification

\`\`\`bash
<command per project — e.g., npm test, pytest, go test ./...>
\`\`\`

## Open questions

<from intent/example-map.md if rung 4, else: "none recorded">

## Inheritance and conventions

- <list any inherited artifacts referenced from this spec>
- <project conventions followed: schema library, test framework, etc.>
```

## calibration.json shape

```json
{
  "task_slug": "agent-permissions-flagging",
  "task_description": "<the user's original ask, paraphrased>",
  "answers": {
    "novelty": "partially",
    "blast": "multiple",
    "reversibility": "flag",
    "inherited_contract": "src/permissions/AgentPermission.ts",
    "edge_density": "mixed",
    "blast_followup": null,
    "reversibility_followup": null,
    "novelty_followup": null
  },
  "rungs": {
    "intent": 2,
    "interface": 4,
    "behavior": 3,
    "verification": 3
  },
  "reasoning": {
    "intent": ["default 1", "+1 novelty=partially"],
    "interface": ["INHERITED from src/permissions/AgentPermission.ts"],
    "behavior": ["default 2", "+1 edge_density=mixed"],
    "verification": ["V ≥ B floor = 3"]
  },
  "notes": [],
  "produced_at": "2026-05-08T14:30:00Z"
}
```

The `notes` array carries any soft warnings (all-1s sanity check, V<B override, all-4s decomposition suggestion). Each is a string the skill emitted to the user; persisting them keeps the calibration self-explanatory later.

## Why a folder, not a document

Three concrete reasons:

**Code is reviewable as code.** A `schema.ts` gets type checking, syntax highlighting, IDE navigation, and AST diffing. A code block embedded in markdown gets none of those. The reviewer has to extract before evaluating.

**Atomicity matches the consumer.** CI runs test files. Type checkers parse `.ts` files. Eval harnesses read JSONL. Schemas are imported. The output should match what consumers actually need, not be a bundle they have to unpack.

**Partial regeneration is cheap.** Climbing a rung in one pillar regenerates one subfolder, not the whole document. Editing the schema doesn't risk touching the eval cases. Smaller atomic units = smaller blast radius for spec changes.

## Notes on the README

Keep the root README around 50 lines. It is *navigation*, not content. The user reads it once to orient — every detail belongs in a specific file, not in the root. If the README starts growing past ~80 lines, sections are leaking that should live in the pillar subfolders.
