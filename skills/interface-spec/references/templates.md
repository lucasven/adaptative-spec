# Interface — File Templates

Format templates for each rung. For complete worked examples, see `examples.md`.

## Rung 1 — README.md (inferred)

```markdown
# Interface (inferred)

Shape determined by sibling implementations:
- <path/to/sibling1>
- <path/to/sibling2>

Verified consistent on <date>.

No explicit schema written; the consuming agent should follow the sibling pattern.
```

## Rung 2 — types file

Write real source files using the project's language. Every parameter and return value gets a named type.

TypeScript (`types.ts`):

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

Python (`types.py`):

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

## Rung 2 — README.md

```markdown
# Interface (rung 2 — type signatures)

See `types.<ext>` for the type definitions.

Stack: <typescript / python / go / ...>
```

## Rung 3 — schema file

Use the project's schema library (Zod for TS, Pydantic for Python, JSON Schema for cross-language). Match `CONVENTIONS.md` if it exists.

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

## Rung 3 — README.md

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

## Rung 4 — protocol.md

(In addition to the rung-3 schema file)

```markdown
# <Protocol name>

## Operations

### POST /v1/<resource>

<Description.>

- **Inputs**: `<InputSchema>` (see `schema.<ext>`)
- **Outputs (201)**: `<ResultSchema>`
- **Errors**:
  - `400 validation_failed` — body matches `ValidationError`
  - `401 unauthorized`
  - `403 forbidden` — caller lacks required scope
  - `409 conflict` — resource already exists
  - `429 rate_limited` — `Retry-After` header present
  - `500 internal_error` — correlation ID in `X-Request-Id`

- **Idempotency**: <strategy>
- **Auth**: <mechanism and required scopes>

## Versioning

<strategy — URI versioning, header versioning, etc.>

## Transport

<synchronous/async, delivery semantics, ordering guarantees>

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
```
