# Interface — Worked Examples

The same component rendered at each rung. Use these as shape references; the syntax shown is one instance of each method.

## Source component

> A function that creates an agent permission record.

## Rung 1 — Inferred

```markdown
INFERRED. Shape determined by sibling implementations:
- src/permissions/createUserPermission.ts
- src/permissions/createTeamPermission.ts

Both take a permission object and return `Promise<{ id: string }>`. New function follows the same shape.

Verified consistent on 2026-05-08.
```

## Rung 2 — Type signature

```ts
type Capability = "spawn" | "message" | "terminate"

type AgentPermission = {
  agent_id: string
  capabilities: ReadonlyArray<Capability>
  max_depth: number
  token_budget: number
}

type CreatePermissionResult = {
  id: string
  created_at: string
}

function createAgentPermission(
  input: AgentPermission
): Promise<CreatePermissionResult>
```

## Rung 3 — Schema with constraints

```ts
import { z } from "zod"

const Capability = z.enum(["spawn", "message", "terminate"])

const AgentPermissionInput = z.object({
  agent_id: z.string().uuid(),
  capabilities: z.array(Capability).min(1),
  max_depth: z.number().int().min(0).max(5),
  token_budget: z.number().int().positive().max(1_000_000),
})

const CreatePermissionResult = z.object({
  id: z.string().uuid(),
  created_at: z.string().datetime(),
})

const ValidationError = z.object({
  code: z.literal("validation_failed"),
  field: z.string(),
  message: z.string(),
  received: z.unknown().optional(),
})

type AgentPermissionInput = z.infer<typeof AgentPermissionInput>
type CreatePermissionResult = z.infer<typeof CreatePermissionResult>
type ValidationError = z.infer<typeof ValidationError>

// Behavior contract: createAgentPermission(input) either resolves
// with a CreatePermissionResult or throws an error matching ValidationError.
```

## Rung 4 — Protocol specification

```markdown
# Agent Permissions API

## Operations

### POST /v1/agent-permissions

Create an agent permission record.

**Inputs**: `AgentPermissionInput` (Zod schema in src/schemas/agentPermission.ts)
**Outputs (201)**: `CreatePermissionResult`
**Errors**:
- `400 validation_failed` — input failed schema validation; body is `ValidationError`
- `401 unauthorized` — caller lacks valid token
- `403 forbidden` — caller lacks `permissions:write` scope
- `409 conflict` — `agent_id` already has an active permission
- `429 rate_limited` — caller exceeded their write quota; `Retry-After` header present
- `500 internal_error` — unexpected; correlation ID in `X-Request-Id`

**Idempotency**: idempotent with key. Caller supplies `Idempotency-Key` header (UUID). Same key + same body within 24h returns the original 201; same key + different body returns 422.

**Auth**: Bearer token (JWT) with `permissions:write` scope.

## Versioning

URI versioning. `/v1/...` is the current major. Breaking changes will introduce `/v2/...` and run both for ≥ 12 months.

## Transport semantics

Synchronous HTTPS. Single response per request. No ordering guarantees across concurrent requests. At-most-once delivery (network failures may leave the client uncertain; idempotency key resolves).

## Error envelope

All non-2xx responses share this body shape:

\`\`\`json
{
  "code": "<error_code>",
  "message": "<human-readable>",
  "request_id": "<correlation id>",
  "details": <optional, code-specific>
}
\`\`\`

Specifically: `details` for `validation_failed` is the `ValidationError` from the schema.
```

## What changes across rungs

- **Rung 1 → 2**: shape becomes inspectable without reading code.
- **Rung 2 → 3**: invalid inputs now have a defined behavior (rejection with structured error), not just "the type system would have caught it at compile time."
- **Rung 3 → 4**: the interface becomes a contract for *clients you don't control*. Versioning, idempotency, auth, and error envelope all move from "implicit" to "explicit and documented."

The cost progression matters: rung 4 is meaningfully more work than rung 3, and is wasted unless someone outside the producer's codebase needs to consume the interface stably.
