---
name: interface-spec
description: Produce an Interface specification artifact at a chosen rung (1-4) — a type signature, a runtime-validated schema, or a full protocol specification. Use this whenever the user needs to pin down the I/O shape of a function, module, API, or system component before implementation. Trigger on phrases like "what's the interface", "define the schema", "spec the API", "what's the type", "design the protocol", or when the parent skill spec-handoff dispatches Interface artifact production. The skill writes its output as real source files in an `interface/` subfolder so they can be type-checked, imported, and version-controlled directly. It does not gate or block.
---

# Interface Spec

## Inputs

- **Rung** (1–4)
- **Output path** (the `interface/` subfolder under the spec root)
- **Stack** (TypeScript, Python, Go, etc. — for choosing extensions and idioms)
- **Inherited references** (existing types, schemas, IDLs the artifact should align with)

If `inherited_contract` was set during calibration, the rung is 4 by default — the artifact already exists. Point to it in the README and skip authorship.

## Files this skill produces

The exact files depend on rung and stack. Always write `README.md` and `quality-bar.md`. Write code files appropriate to the rung:

| Rung | Files (TypeScript shown; substitute extensions per stack) |
|---|---|
| 1 | `README.md` recording the inferred decision and sibling references |
| 2 | `README.md` + `types.ts` (or `.py` / `.go`) |
| 3 | `README.md` + `schema.ts` (with constraints + error envelope) |
| 4 | `README.md` + `schema.ts` + `protocol.md` |

If the rung is INHERITED, write only `README.md` pointing to the existing artifact.

## Method per rung

### Rung 1 — Inferred (no schema artifact)

A deliberate choice to leave the interface implicit when:

- Shape is determined by ≥ 2 sibling implementations the AI can read
- Sibling implementations agree on the shape
- Sibling code is in scope

`README.md` content:

```markdown
# Interface (inferred)

Shape determined by sibling implementations:
- <path/to/sibling1>
- <path/to/sibling2>

Verified consistent on <date>.

No explicit schema written; the consuming agent should follow the sibling pattern.
```

### Rung 2 — Type signature

Write a real source file (`types.ts`, `types.py`, etc.) with the signatures.

TypeScript example (`types.ts`):

```ts
export type Capability = "spawn" | "message" | "terminate"

export type AgentPermission = {
  agent_id: string
  capabilities: ReadonlyArray<Capability>
  max_depth: number
  token_budget: number
}

export type CreatePermissionResult = {
  id: string
  created_at: string
}

export type CreatePermission = (input: AgentPermission) => Promise<CreatePermissionResult>
```

Python example (`types.py`):

```python
from typing import Literal, Sequence
from dataclasses import dataclass

Capability = Literal["spawn", "message", "terminate"]

@dataclass(frozen=True)
class AgentPermission:
    agent_id: str
    capabilities: Sequence[Capability]
    max_depth: int
    token_budget: int

@dataclass(frozen=True)
class CreatePermissionResult:
    id: str
    created_at: str
```

`README.md` content (~10 lines):

```markdown
# Interface (rung 2 — type signatures)

See `types.<ext>` for the type definitions.

Stack: <typescript / python / go / ...>
```

Constraints:
- Every parameter and return value has a named type (no `any`, no untyped dicts)
- Optional vs required is explicit
- Compound types are named, not inlined
- File compiles or type-checks in the target system

### Rung 3 — Schema with constraints

Write a real source file using the project's schema library. Match `CONVENTIONS.md` if it exists; otherwise pick the project's existing choice (Zod for TS, Pydantic for Python, JSON Schema for cross-language, etc.).

Zod example (`schema.ts`):

```ts
import { z } from "zod"

export const Capability = z.enum(["spawn", "message", "terminate"])

export const AgentPermissionInput = z.object({
  agent_id: z.string().uuid(),
  capabilities: z.array(Capability).min(1),
  max_depth: z.number().int().min(0).max(5),
  token_budget: z.number().int().positive().max(1_000_000),
})

export const CreatePermissionResult = z.object({
  id: z.string().uuid(),
  created_at: z.string().datetime(),
})

export const ValidationError = z.object({
  code: z.literal("validation_failed"),
  field: z.string(),
  message: z.string(),
  received: z.unknown().optional(),
})

export type AgentPermissionInput = z.infer<typeof AgentPermissionInput>
export type CreatePermissionResult = z.infer<typeof CreatePermissionResult>
export type ValidationError = z.infer<typeof ValidationError>
```

`README.md` content:

```markdown
# Interface (rung 3 — schema with constraints)

See `schema.<ext>` for the runtime-validated schema, types, and error envelope.

Stack: <stack>
Schema library: <library>

## Error envelope

Validation failures throw or return `ValidationError` objects with shape `{ code: "validation_failed", field, message, received? }`.

## Inheritance

<list any imports from existing project schemas>
```

Constraints:
- Every field has a type
- Every field has stated optionality (required, optional, nullable — distinguished)
- Constraints expressed: ranges, enums, regex, length bounds, conditional
- Error format defined as a real shape, not just "throws"
- Schema parses inputs at the boundary (not just static types)
- Invalid inputs produce structured rejections

### Rung 4 — Protocol specification

Combine `schema.ts` (the data shapes) with `protocol.md` (the protocol-level concerns):

`protocol.md` content:

```markdown
# <Protocol name>

## Operations

### POST /v1/agent-permissions

Create an agent permission record.

- **Inputs**: `AgentPermissionInput` (see `schema.<ext>`)
- **Outputs (201)**: `CreatePermissionResult`
- **Errors**:
  - `400 validation_failed` — body matches `ValidationError`
  - `401 unauthorized`
  - `403 forbidden` — caller lacks `permissions:write` scope
  - `409 conflict` — `agent_id` already has an active permission
  - `429 rate_limited` — `Retry-After` header present
  - `500 internal_error` — correlation ID in `X-Request-Id`

- **Idempotency**: idempotent with key. Caller supplies `Idempotency-Key` header (UUID). Same key + same body within 24h returns the original 201; same key + different body returns 422.

- **Auth**: Bearer token (JWT) with `permissions:write` scope.

## Versioning

URI versioning. `/v1/...` is the current major. Breaking changes will introduce `/v2/...` and run both for ≥ 12 months.

## Transport

Synchronous HTTPS. Single response per request. No ordering guarantees across concurrent requests. At-most-once delivery (network failures may leave the client uncertain; idempotency key resolves).

## Error envelope

All non-2xx responses share this body:

\`\`\`json
{
  "code": "<error_code>",
  "message": "<human-readable>",
  "request_id": "<correlation id>",
  "details": <optional>
}
\`\`\`

`details` for `validation_failed` is `ValidationError` from the schema.
```

## Inheritance check

Before authoring at any rung, look around the codebase:

1. Is there an existing artifact at this rung covering the same area?
2. If yes, does it cover this case?
3. If both, write a `README.md` pointing to it and skip authorship of new files.

This is the highest-leverage move at the Interface pillar — most systems have inherited interfaces that should be reused. The skill suggests reuse; the user can override and ask for new authorship anyway.

## Convention check

Before authoring, read project conventions (`CONVENTIONS.md`, `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`). Match:

- Schema library
- Error envelope shape
- Naming conventions (camelCase, snake_case, kebab-case)
- Versioning strategy

If no convention exists, pick reasonable defaults and note them in the `README.md` so the user knows what was assumed.

## Quality bar annotation

After producing the artifact(s), walk the bar in `references/quality-bar.md`. Write `quality-bar.md` in the output folder with each criterion marked. Information, not a gate.

## Reference files

- `references/quality-bar.md` — Per-rung review checklist
- `references/examples.md` — Worked examples per rung
