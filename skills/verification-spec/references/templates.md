# Verification — File Templates

Format templates for each rung. For complete worked examples, see `examples.md`.

## Rung 1 — README.md

```markdown
# Verification (manual)

Owner: <name>
Cost bound if missed: <how bad can it get>

Justification: <what makes this throwaway and bounded>
```

If the justification runs more than 2-3 sentences, this is probably the wrong rung.

## Rung 2 — acceptance.test file

One happy-path test using the project's test framework.

TypeScript example (`acceptance.test.ts`):

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

## Rung 2 — README.md

```markdown
# Verification (rung 2 — one happy-path test)

Run with: `<project test command>`

The test in `acceptance.test.<ext>` covers the main success path. Edge cases and rejections are not covered at this rung.
```

## Rung 3 — acceptance.test file (parameterized)

Consumes `behavior/examples.json` directly — no duplicate test data.

TypeScript example (`acceptance.test.ts`):

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

## Rung 3 — README.md

```markdown
# Verification (rung 3 — acceptance suite)

Run with: `<project test command>`

The suite in `acceptance.test.<ext>` consumes `../behavior/examples.json` directly. To add a case, add it to the data file — the test picks it up on next run.

Test names include the rule reference (e.g., `[#1 R1, R2, R4] gastei 50 no mercado`), so a failing CI run identifies which rule broke.
```

## Rung 4 — property tests

Predicates from `behavior/invariants.md`. TypeScript example (`properties.test.ts`):

```ts
import { fc, test } from "@fast-check/vitest"
import { Agent } from "../../../src/agents/agent"

test.prop([fc.array(fc.constantFrom("spawn", "message", "terminate"), { maxLength: 100 })])(
  "spawn count never exceeds MAX_FANOUT",
  (events) => {
    const agent = new Agent({ maxFanout: 10 })
    for (const e of events) agent.handle(e)
    return agent.spawnCount <= 10
  }
)
```

## Rung 4 — eval set (evals.jsonl)

```jsonl
{"id": "exp-001", "input": "<input>", "expected": {"<field>": "<value>"}, "added": "<date>", "source": "initial"}
{"id": "exp-042", "input": "<input>", "expected": {"<field>": "<value>"}, "added": "<date>", "source": "bug-report-#42"}
```

## Rung 4 — characterization test

Capture current behavior, then freeze as golden master:

```ts
import { test, expect } from "vitest"
import golden from "./golden-master.json"
import { newImplementation } from "../../../src/parser-v2"

test.each(golden)("characterization: $input", ({ input, expected, error }) => {
  if (error) expect(() => newImplementation(input)).toThrow(error)
  else expect(newImplementation(input)).toEqual(expected)
})
```

## Rung 4 — README.md

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
