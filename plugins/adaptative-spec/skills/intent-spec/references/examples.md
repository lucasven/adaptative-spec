# Intent — Worked Examples

The same task description rendered at each rung. Use these to calibrate your output for any task — the *shape* of each rung is consistent regardless of domain.

## Source task

> "We want users to be able to flag agent permissions as needing review when they exceed certain thresholds, and reviewers should see flagged ones first."

## Rung 1 — One sentence

> When an agent permission exceeds configured thresholds, the system marks it as needing review so that reviewers see it ahead of unflagged permissions.

## Rung 2 — Story + AC

```markdown
## Story
As a permissions reviewer, I want flagged permissions to surface ahead of unflagged ones, so that I review high-risk configurations first.

## Acceptance criteria
1. Given a permission with `max_depth > 5`, when it's saved, then it's marked `needs_review = true`.
2. Given a permission with `token_budget > 100000`, when it's saved, then it's marked `needs_review = true`.
3. Given a list of permissions, when displayed in the review queue, then `needs_review = true` rows appear above `false` rows.
4. Given a flagged permission, when a reviewer changes thresholds and re-saves, then `needs_review` recomputes.

## Non-goals
- Notifying reviewers of new flags (no email/push)
- Auto-rejecting flagged permissions
- Configuring thresholds via UI (config is code-only this version)
```

## Rung 3 — Working-backwards README

```markdown
# Permission review flagging

Permissions exceeding configured thresholds are automatically marked as needing review. Reviewers see flagged permissions at the top of the review queue, sorted by flag time (oldest first).

## Usage

When an admin saves a permission with `max_depth = 7`, the system records the permission with `needs_review = true`. The next reviewer to open the queue sees this permission at the top, with a yellow "needs review" badge.

When the same admin reduces `max_depth` to 3 and re-saves, `needs_review` is recomputed against current thresholds and clears to `false`. The permission moves to the standard queue position.

## Errors

If thresholds aren't configured, the system marks no permissions as flagged. Reviewers see a banner: "No review thresholds configured — all permissions appear in standard order." Saving a permission still works; flagging is just inactive.

## Not in this version

- Email or push notifications when a permission is newly flagged
- Auto-rejection of flagged permissions
- UI for configuring thresholds (thresholds are code-only)
- Per-reviewer queue customization

## FAQ

**Q: What if a threshold is changed after a permission is flagged?**
A: Existing flags don't recompute automatically. They recompute the next time that permission is saved. A separate backfill is out of scope for this version.

**Q: Can multiple thresholds flag the same permission?**
A: Yes. The flag is binary; reasons are not surfaced in this version.
```

## Rung 4 — README + example map

(Rung 3 README, plus:)

```markdown
## Example map

### Rules
1. A permission is flagged when any threshold is exceeded.
2. Flag state is recomputed on save, not on read.
3. Flagged permissions sort above unflagged in the review queue.
4. Among flagged permissions, sort is by flag time, oldest first.

### Examples
- [Rule 1] `max_depth=7`, `token_budget=10000` → flagged (depth exceeds)
- [Rule 1] `max_depth=3`, `token_budget=10000` → not flagged (within all thresholds)
- [Rule 1] `max_depth=5`, `token_budget=10000` → not flagged (boundary: equal is not exceeded)
- [Rule 2] permission saved at T1 with thresholds A, thresholds change to B at T2, permission read at T3 → still reflects T1 flag, not T2-recomputed
- [Rule 2] permission re-saved at T3 → recomputes against thresholds B
- [Rule 3] queue with one flagged + two unflagged → flagged appears at index 0
- [Rule 3] queue with all flagged → all appear in flag-time order, no demotion
- [Rule 4] flagged at T1, flagged at T2, T1 < T2 → T1 appears first

### Open questions
- What happens if `flagged_at` is null (legacy data)? — DEFERRED to next sprint; for now treat null as oldest possible time.
- Should non-reviewer roles see the flag badge? — OUT OF SCOPE; only reviewers see queue.
- Should the system log threshold exceedances for audit? — DEFERRED to audit feature epic.
```

## What changes across rungs

- **Rung 1 → 2**: adds AC and non-goals. The shape of the work becomes testable.
- **Rung 2 → 3**: adds usage examples and error cases. The user-facing surface becomes concrete.
- **Rung 3 → 4**: adds rule decomposition and explicit questions. Ambiguities become visible artifacts rather than implicit assumptions.

Each climb costs more time but removes a class of ambiguity that lower rungs leave open. Climb only when calibration says you need to.
