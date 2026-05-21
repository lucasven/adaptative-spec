# Verification — Worked Examples

The same component verified at each rung. Tests target the `parseExpenseMessage` component from the Behavior examples.

## Rung 1 — Manual eyeball (would fail sufficiency check)

This component handles user input and persists derived data; it fails the rung-1 check (not throwaway, not bounded). Climb.

## Rung 2 — One happy-path test

```ts
import { test, expect } from "vitest"
import { parseExpenseMessage } from "./parser"

test("parses a basic Portuguese expense message", () => {
  const result = parseExpenseMessage("gastei 50 no mercado")
  expect(result).toEqual({
    amount: 50,
    currency: "BRL",
    category: "groceries",
    description: "mercado",
  })
})
```

This is the minimum: one positive case, full assertion of the output shape.

## Rung 3 — Acceptance suite

The acceptance suite is generated *from* the Behavior rung 3 examples table, not maintained separately. Same artifact, two pillars.

```ts
import { describe, test, expect } from "vitest"
import { parseExpenseMessage } from "./parser"

// IMPORTANT: this array is the canonical source. The Behavior artifact
// references this same data. Do not duplicate or fork.
const cases = [
  { id: 1, input: "gastei 50 no mercado", expected: { amount: 50, currency: "BRL", category: "groceries", description: "mercado" }, rule: "R1, R2, R4" },
  { id: 2, input: "spent $12 on coffee", expected: { amount: 12, currency: "USD", category: "food", description: "coffee" }, rule: "R1, R2 ($), R4" },
  { id: 3, input: "uber 35", expected: { amount: 35, currency: "BRL", category: "transport", description: "uber" }, rule: "R1, R2 (default), R4" },
  { id: 4, input: "paguei 1.250,50 de aluguel", expected: { amount: 1250.50, currency: "BRL", category: "housing", description: "aluguel" }, rule: "R1, R2, R3 (pt), R4" },
  { id: 5, input: "paid 1,250.50 rent", expected: { amount: 1250.50, currency: "USD", category: "housing", description: "rent" }, rule: "R1, R2 (en), R3 (en), R4" },
  { id: 10, input: "mercado 100 mercado", expected: { amount: 100, currency: "BRL", category: "groceries", description: "mercado mercado" }, rule: "R1 (first number), R4" },
]

const rejections = [
  { id: 6, input: "25", error: "no_context", rule: "R5" },
  { id: 7, input: "gastei muito hoje", error: "no_amount", rule: "R6" },
  { id: 8, input: "gastei 0 no mercado", error: "invalid_amount", rule: "R1 (boundary: zero)" },
  { id: 9, input: "spent -50 on coffee", error: "invalid_amount", rule: "R1 (boundary: negative)" },
]

describe("parseExpenseMessage — acceptance", () => {
  test.each(cases)("[#$id $rule] $input", ({ input, expected }) => {
    expect(parseExpenseMessage(input)).toEqual(expected)
  })

  describe("rejections", () => {
    test.each(rejections)("[#$id $rule] $input → $error", ({ input, error }) => {
      expect(() => parseExpenseMessage(input)).toThrow(error)
    })
  })
})
```

Note the test name format: `[#1 R1, R2, R4] gastei 50 no mercado` — the rule reference is in the test name, so a failing CI run says exactly which rule broke, not just which assertion failed.

## Rung 4 — Evals + properties

For an LLM-driven version of the same parser (where deterministic rules don't fully cover the input space), the verification stack expands:

### Eval set (growing JSONL)

```jsonl
{"id": "exp-001", "input": "gastei 50 no mercado", "expected": {"amount": 50, "currency": "BRL", "category": "groceries"}, "added": "2026-01-15", "source": "initial"}
{"id": "exp-002", "input": "spent $12 on coffee", "expected": {"amount": 12, "currency": "USD", "category": "food"}, "added": "2026-01-15", "source": "initial"}
{"id": "exp-042", "input": "almoço 80 reais com cliente", "expected": {"amount": 80, "currency": "BRL", "category": "food"}, "added": "2026-02-03", "source": "bug-report-#42"}
{"id": "exp-077", "input": "Uber black 95.50", "expected": {"amount": 95.50, "currency": "BRL", "category": "transport"}, "added": "2026-02-18", "source": "bug-report-#77"}
```

Run via:

```ts
// scripts/run-evals.ts
const cases = readJsonl("evals/expenses.jsonl")
const results = await Promise.all(cases.map(async (c) => {
  const actual = await parseExpenseMessage(c.input)
  return { id: c.id, passed: deepEqual(actual, c.expected), expected: c.expected, actual }
}))

const passRate = results.filter(r => r.passed).length / results.length
console.log(`Pass rate: ${passRate * 100}%`)
process.exit(passRate >= 0.95 ? 0 : 1)  // CI gate
```

### Property tests (for invariants)

```ts
import { fc, test } from "@fast-check/vitest"

// Invariant: any positive integer with a known category keyword should parse with that category
test.prop([
  fc.integer({ min: 1, max: 100000 }),
  fc.constantFrom("mercado", "uber", "coffee", "aluguel"),
])("any positive integer + known keyword → correct category", (amount, keyword) => {
  const result = parseExpenseMessage(`gastei ${amount} no ${keyword}`)
  const expectedCategory = { mercado: "groceries", uber: "transport", coffee: "food", aluguel: "housing" }[keyword]
  return result.amount === amount && result.category === expectedCategory
})

// Invariant: parsing is deterministic — same input always returns same output
test.prop([fc.string()])("parsing is deterministic", (input) => {
  try {
    const a = parseExpenseMessage(input)
    const b = parseExpenseMessage(input)
    return JSON.stringify(a) === JSON.stringify(b)
  } catch (e1) {
    try { parseExpenseMessage(input) } catch (e2) { return e1.message === e2.message }
    return false
  }
})

// Invariant: parsed amount is always positive (rejections happen otherwise)
test.prop([fc.string()])("parsed amount is positive when parse succeeds", (input) => {
  try {
    const result = parseExpenseMessage(input)
    return result.amount > 0
  } catch {
    return true  // rejection is acceptable
  }
})
```

### Characterization test (for migration scenarios)

When migrating the parser implementation (e.g., from regex-based to LLM-based), capture current behavior first:

```ts
// scripts/capture-golden.ts — run once against the trusted implementation
const inputs = readLines("evals/golden-inputs.txt")
const golden = inputs.map(input => {
  try { return { input, output: parseExpenseMessage(input) } }
  catch (e) { return { input, error: e.message } }
})
fs.writeFileSync("golden-master.json", JSON.stringify(golden, null, 2))
```

```ts
// tests/characterization.test.ts — runs against the new implementation forever
import golden from "../golden-master.json"

test.each(golden)("characterization: $input", ({ input, output, error }) => {
  if (output) expect(parseExpenseMessage(input)).toEqual(output)
  else expect(() => parseExpenseMessage(input)).toThrow(error)
})
```

## What changes across rungs

- **Rung 1 → 2**: a single executable assertion replaces vibes. Failure is now visible.
- **Rung 2 → 3**: the suite becomes exhaustive *of the enumerated cases*. The Behavior table feeds the tests directly.
- **Rung 3 → 4**: verification covers cases the spec didn't enumerate. Properties and evals catch what tables miss; characterization preserves what migrations might break.

## Loop closure

At rung 2 and above, the verification artifact must run as part of the agent's iteration loop:

```bash
# What the agent runs after each code generation:
npm test                              # rung 2/3 unit + acceptance
npm run test:property                 # rung 4 properties
npm run evals                         # rung 4 evals (gates merge)
```

If any check fails, the agent reads the failure output, modifies the code, and reruns. This is what "autonomous" means in practice — the loop runs without human intervention until green.
