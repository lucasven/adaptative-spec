---
name: interface-spec
description: Use when the user needs to define the I/O shape of a function, module, API, or system component before implementation — phrases like "what's the interface", "define the schema", "spec the API", "what's the type", "design the protocol", or when spec-handoff dispatches Interface artifact production.
---

# Interface Spec

## When to Use

- User asks to define types, schemas, API contracts, or protocols
- spec-handoff dispatched Interface production at a settled rung
- Need to pin down the I/O shape before implementation

**Not this skill:** If the rung isn't settled yet, use `spec-handoff` — it handles discovery and calibration first.

## Inputs

- **Rung** (1–4)
- **Output path** (`interface/` subfolder under spec root)
- **Stack** (TypeScript, Python, Go — for extensions and idioms)
- **Inherited references** (existing types, schemas, IDLs to align with)

If `inherited_contract` was set during calibration, rung defaults to 4 — the artifact exists. Point to it in README and skip authorship.

## Quick Reference

| Rung | Files | Method |
|---|---|---|
| 1 | `README.md` | Inferred from ≥2 sibling implementations that agree on shape |
| 2 | `README.md` + `types.<ext>` | Type signatures — every param/return typed, no `any` |
| 3 | `README.md` + `schema.<ext>` | Runtime-validated schema + constraints + error envelope |
| 4 | `README.md` + `schema.<ext>` + `protocol.md` | Schema + protocol (versioning, idempotency, auth, errors) |

If INHERITED: `README.md` only, pointing to existing artifact.

Always write `quality-bar.md`.

## Constraints per Rung

**Rung 2:** Every parameter and return has a named type. Optional vs required explicit. Compound types named, not inlined. File compiles/type-checks.

**Rung 3:** Every field has type + stated optionality. Constraints expressed (ranges, enums, regex, length). Error format defined as a real shape. Schema parses at the boundary; invalid inputs produce structured rejections.

**Rung 4:** All rung-3 constraints plus: operations listed with inputs/outputs/errors. Idempotency, auth, versioning, and transport semantics documented. Error envelope shared across operations.

See `references/templates.md` for exact file formats. See `references/examples.md` for a complete worked example.

## Before Authoring

**Inheritance check:** Is there an existing artifact covering the same area? If yes, point to it and skip authorship. This is the highest-leverage move at the Interface pillar.

**Convention check:** Read `CONVENTIONS.md`, `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`. Match schema library, error envelope shape, naming conventions, versioning strategy. If no convention, pick defaults and note assumptions.

## Quality Bar

After producing artifacts, walk `references/quality-bar.md` and write `quality-bar.md`. Information, not a gate.
