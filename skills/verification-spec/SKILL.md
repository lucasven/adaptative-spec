---
name: verification-spec
description: Produce a Verification artifact at a chosen rung (1-4) — a single happy-path test, an executable acceptance suite derived from behavior data, or evals/properties/characterization tests. Use this whenever the user needs to pin down how to mechanically check that an implementation is correct. Trigger on phrases like "how do I test this", "spec the tests", "write the eval", "set up acceptance tests", "what should we assert", or when the parent skill spec-handoff dispatches Verification artifact production. The skill writes its output as actual runnable test files in a `verification/` subfolder, plus eval data as JSONL — formats the project's test runner can execute directly without translation.
---

# Verification Spec

## Inputs

- **Rung** (1–4)
- **Output path** (the `verification/` subfolder under the spec root)
- **Behavior path** (where the behavior pillar wrote its data; verification consumes it)
- **Interface path** (verification often runs through the interface boundary)
- **Stack** (for choosing test framework and extensions)

## Files this skill produces

| Rung | Files |
|---|---|
| 1 | `README.md` recording the manual decision and owner |
| 2 | `README.md` + `acceptance.test.<ext>` (one happy-path test) |
| 3 | `README.md` + `acceptance.test.<ext>` (parameterized suite consuming `behavior/examples.json`) |
| 4 | `README.md` + `acceptance.test.<ext>` + at least one of: `evals.jsonl`, `properties.test.<ext>`, `characterization.<ext>` |

Always write `quality-bar.md`.

## Method per rung

### Rung 1 — Manual eyeball

`README.md`:

```markdown
# Verification (manual)

Owner: <name>
Cost bound if missed: <how bad can it get>

Justification: <what makes this throwaway and bounded>
```

If the justification runs more than 2-3 sentences, this is probably the wrong rung — note that and let the user climb.

### Rung 2 — One happy-path test

Write a real test file using the project's test framework. TypeScript example (`acceptance.test.ts`):

```ts
import { describe, test, expect } from "vitest"
import { createExpense } from "../../../src/expenses/create"

test("creates an expense with valid input", async () => {
  const result = await createExpense({
    amount: 50,
    currency: "BRL",
    category: "groceries",
    description: "mercado",
  })

  expect(result.id).toMatch(/^[0-9a-f-]{36}$/)
  expect(result.status).toBe("pending")
  expect(result.created_at).toBeDefined()
})
```

`README.md`:

```markdown
# Verification (rung 2 — one happy-path test)

Run with: `<project test command, e.g., npm test>`

The test in `acceptance.test.<ext>` covers the main success path. Edge cases and rejections are not covered at this rung.
```

Constraints:
- Executes through the same boundary the user uses
- Asserts a specific observable outcome
- Runs in CI on every change
- Failure produces enough output to diagnose without re-running

### Rung 3 — Acceptance suite

The test consumes `behavior/examples.json` directly — no duplicate test data. TypeScript example (`acceptance.test.ts`):

```ts
import { describe, test, expect } from "vitest"
import { readFileSync } from "fs"
import { join } from "path"
import { parseExpenseMessage } from "../../../src/parser"

const cases = JSON.parse(
  readFileSync(join(__dirname, "..", "behavior", "examples.json"), "utf8")
)

const happy = cases.filter((c: any) => c.expected !== undefined)
const rejections = cases.filter((c: any) => c.expected_error !== undefined)

describe("parseExpenseMessage — acceptance", () => {
  test.each(happy)("[#$id $rules] $input", ({ input, expected }) => {
    expect(parseExpenseMessage(input)).toEqual(expected)
  })

  describe("rejections", () => {
    test.each(rejections)("[#$id $rules] $input → $expected_error", ({ input, expected_error }) => {
      expect(() => parseExpenseMessage(input)).toThrow(expected_error)
    })
  })
})
```

`README.md`:

```markdown
# Verification (rung 3 — acceptance suite)

Run with: `<project test command>`

The suite in `acceptance.test.<ext>` consumes `../behavior/examples.json` directly. To add a case, add it to the data file — the test picks it up on next run.

Test names include the rule reference (e.g., `[#1 R1, R2, R4] gastei 50 no mercado`), so a failing CI run identifies which rule broke, not just which assertion failed.
```

Constraints:
- Every example in `behavior/examples.json` runs as a test
- Test data and spec data are the *same file* (no parallel maintenance)
- Both happy and rejection cases execute
- Suite runs in CI and gates merge
- Failing test names include the rule reference

### Rung 4 — Evals + properties + characterization

Pick at least one of the following based on dominant risk:

| Risk | File | Notes |
|---|---|---|
| Silent edge-case bugs | `properties.test.<ext>` | Property-based tests; predicates from `behavior/invariants.md` |
| AI/NLU quality regression | `evals.jsonl` | Growing eval set; new bugs become new lines |
| Behavior-preserving refactor | `characterization.<ext>` + `golden-master.json` | Golden master capture-and-freeze |
| Test suite quality unclear | (mutation testing config) | Stryker / mutmut / PIT in CI |
| Cross-service contract drift | `contracts/` directory | Pact or schema-driven contract tests |

**Property tests** (`properties.test.ts`):

```ts
import { fc, test } from "@fast-check/vitest"
import { Agent } from "../../../src/agents/agent"

// Invariant 1 from behavior/invariants.md:
// "An agent's spawn count over its lifetime is bounded by MAX_FANOUT"
test.prop([fc.array(fc.constantFrom("spawn", "message", "terminate"), { maxLength: 100 })])(
  "spawn count never exceeds MAX_FANOUT",
  (events) => {
    const agent = new Agent({ maxFanout: 10 })
    for (const e of events) agent.handle(e)
    return agent.spawnCount <= 10
  }
)

// Invariant 4: "An agent in a terminal state never transitions out"
test.prop([
  fc.constantFrom("done", "failed", "terminated"),
  fc.array(fc.constantFrom("assign_task", "complete", "error", "kill"), { maxLength: 20 }),
])("terminal states are absorbing", (terminalState, events) => {
  const agent = Agent.inState(terminalState)
  for (const e of events) agent.handle(e)
  return agent.state === terminalState
})
```

**Eval set** (`evals.jsonl`):

```jsonl
{"id": "exp-001", "input": "gastei 50 no mercado", "expected": {"amount": 50, "currency": "BRL", "category": "groceries"}, "added": "2026-01-15", "source": "initial"}
{"id": "exp-042", "input": "almoço 80 reais com cliente", "expected": {"amount": 80, "currency": "BRL", "category": "food"}, "added": "2026-02-03", "source": "bug-report-#42"}
```

Plus a runner script (location per project conventions):

```ts
// scripts/run-evals.ts
import fs from "fs"
import path from "path"
import { parseExpenseMessage } from "../src/parser"

const cases = fs.readFileSync(path.join(__dirname, "..", "specs", "<task>", "verification", "evals.jsonl"), "utf8")
  .trim().split("\n").map(line => JSON.parse(line))

const results = await Promise.all(cases.map(async c => ({
  id: c.id,
  passed: JSON.stringify(await parseExpenseMessage(c.input)) === JSON.stringify(c.expected),
})))

const passRate = results.filter(r => r.passed).length / results.length
console.log(`Pass rate: ${(passRate * 100).toFixed(1)}%`)
process.exit(passRate >= 0.95 ? 0 : 1)
```

**Characterization** (`golden-master.json` + `characterization.test.ts`):

```ts
import { test, expect } from "vitest"
import golden from "./golden-master.json"
import { newImplementation } from "../../../src/parser-v2"

test.each(golden)("characterization: $input", ({ input, expected, error }) => {
  if (error) expect(() => newImplementation(input)).toThrow(error)
  else expect(newImplementation(input)).toEqual(expected)
})
```

`README.md`:

```markdown
# Verification (rung 4 — evals/properties/characterization)

Run with:

\`\`\`bash
<project test command>          # acceptance.test + properties.test
<eval runner command>           # evals.jsonl
\`\`\`

## What's here

- `acceptance.test.<ext>` — same as rung 3, consuming behavior/examples.json
- `properties.test.<ext>` — property-based tests; predicates from behavior/invariants.md
- `evals.jsonl` — eval set; every reported bug becomes a new line
- `characterization.<ext>` + `golden-master.json` — only present for migrations/refactors
```

Constraints:
- For property tests: invariants from `behavior/invariants.md` appear as predicates; generators cover the schema's full input space
- For eval sets: every reported bug becomes a new entry; entries versioned with the codebase
- For characterization: captured behavior is dated and traceable
- All artifacts run in CI and produce a numeric quality signal

## Loop closure

At rung 2 and above, the verification artifact runs as part of the agent's iteration loop:

```bash
npm test                              # acceptance + properties
npm run evals                         # eval set with pass-rate gate
```

If any check fails, the agent reads the output, modifies the code, reruns. This is "autonomous" in practice — the loop runs without human intervention until green.

## Quality bar annotation

After producing artifact(s), walk `references/quality-bar.md` and write `quality-bar.md` with each criterion marked.

The cross-pillar V ≥ B check happens here too: walk through `behavior/`'s artifacts and confirm each rule/example/state-transition is referenced by at least one verification check. If gaps exist, annotate them in `quality-bar.md` — the user can fill them in or accept the gap.

## Reference files

- `references/quality-bar.md` — Per-rung review checklist
- `references/examples.md` — Worked examples per rung
