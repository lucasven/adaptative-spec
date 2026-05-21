# Interface — Review Checklist

Walk this after producing the artifact. Mark each box `[x]`, `[ ]` (with one-line note), or `[~]` (with note). Write the annotated checklist as `quality-bar.md` in the output folder.

Information for the user, not a gate.

## Rung 1 — Inferred (sufficiency check)

- [ ] Shape determined by ≥ 2 sibling implementations the AI can read
- [ ] Sibling implementations agree on the shape (no drift)
- [ ] Sibling code is in scope for the AI's context
- [ ] Decision to skip an explicit artifact is recorded in `README.md`

## Rung 2 — Type signature

- [ ] Every parameter and return value has a named type (no `any`, no untyped dicts, no `interface{}`)
- [ ] Optional vs required is explicit
- [ ] Compound types are named, not inlined repeatedly
- [ ] The type compiles or type-checks in the target system
- [ ] Reading the signature alone tells you what the function consumes and produces

## Rung 3 — Schema with constraints

- [ ] Every field has a type
- [ ] Every field has stated optionality (required, optional, nullable — distinguished)
- [ ] Constraints beyond type are expressed (ranges, enums, regex, length bounds, conditional)
- [ ] An error format for validation failures is defined (shape, not just "throws")
- [ ] Schema parses inputs at the boundary (not just static types)
- [ ] Invalid inputs produce structured rejections, not crashes

## Rung 4 — Protocol specification

- [ ] Every operation has named inputs, named outputs, and named error cases
- [ ] A versioning strategy is stated (URI version, header, content negotiation, or "frozen forever")
- [ ] Idempotency semantics stated for every mutating operation
- [ ] Authentication and authorization expectations explicit per operation
- [ ] Transport semantics explicit (sync/async, streaming, ordering, delivery guarantees)
- [ ] A consumer could implement against the spec without reading the producer's source

## Cross-cutting

- [ ] Inheritance check performed (existing artifacts identified or absence confirmed in `README.md`)
- [ ] Convention check performed (project's existing format choices respected, or chosen defaults noted in `README.md`)
