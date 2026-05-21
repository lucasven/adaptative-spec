#!/usr/bin/env python3
"""
Mechanical scoring: turn elicited answers into per-pillar suggested rungs.

Usage:
    python score.py answers.json
    cat answers.json | python score.py -

Input JSON shape (from references/questions.md):
{
  "novelty": "yes" | "partially" | "no",
  "blast": "feature" | "multiple" | "system",
  "reversibility": "flag" | "fix" | "migration",
  "inherited_contract": null | "string reference",
  "edge_density": "low" | "mixed" | "high",
  "blast_followup": null | "yes" | "no",
  "reversibility_followup": null | "string",
  "novelty_followup": null | "string"
}

Output: prints suggested per-pillar rungs with reasoning, plus any soft notes.
The user adjusts as needed; nothing is enforced.
"""

import json
import sys
from typing import Any


def cap(rung: int) -> int:
    return max(1, min(4, rung))


def score_intent(a: dict[str, Any]) -> tuple[int, list[str]]:
    rung = 1
    reasons = ["default 1"]
    if a.get("novelty") in {"partially", "no"}:
        rung += 1
        reasons.append(f"+1 novelty={a['novelty']}")
    if a.get("novelty") == "no" and not a.get("novelty_followup"):
        rung += 1
        reasons.append("+1 greenfield (no reference pattern)")
    if a.get("blast") == "system":
        rung += 1
        reasons.append("+1 blast=system")
    return cap(rung), reasons


def score_interface(a: dict[str, Any]) -> tuple[int, list[str]]:
    if a.get("inherited_contract"):
        return 4, [f"INHERITED from {a['inherited_contract']}"]
    rung = 2
    reasons = ["default 2"]
    if a.get("blast") in {"multiple", "system"}:
        rung += 1
        reasons.append(f"+1 blast={a['blast']}")
    if a.get("reversibility") == "migration":
        rung += 1
        reasons.append("+1 reversibility=migration (interfaces calcify)")
    return cap(rung), reasons


def score_behavior(a: dict[str, Any]) -> tuple[int, list[str]]:
    rung = 2
    reasons = ["default 2"]
    if a.get("edge_density") in {"mixed", "high"}:
        rung += 1
        reasons.append(f"+1 edge_density={a['edge_density']}")
    if a.get("edge_density") == "high" and a.get("blast") in {"multiple", "system"}:
        rung += 1
        reasons.append("+1 high edges & wide blast")
    if a.get("blast") == "system" and a.get("blast_followup") == "yes":
        rung += 1
        reasons.append("+1 money/auth/data/contracts")
    return cap(rung), reasons


def score_verification(a: dict[str, Any], behavior_rung: int) -> tuple[int, list[str]]:
    rung = behavior_rung
    reasons = [f"V ≥ B floor = {behavior_rung}"]
    if a.get("blast") == "system" and rung < 3:
        rung = 3
        reasons.append("raised to 3: blast=system")
    if a.get("blast") == "system" and a.get("blast_followup") == "yes":
        rung = 4
        reasons.append("raised to 4: money/auth/data/contracts")
    if a.get("reversibility") == "migration" and rung < 3:
        rung = 3
        reasons.append("raised to 3: reversibility=migration")
    return cap(rung), reasons


def evaluate(answers: dict[str, Any]) -> dict[str, Any]:
    intent, intent_why = score_intent(answers)
    interface, interface_why = score_interface(answers)
    behavior, behavior_why = score_behavior(answers)
    verification, verification_why = score_verification(answers, behavior)

    notes = []
    if intent == 4 and interface == 4 and behavior == 4 and verification == 4:
        notes.append(
            "all-pillars-high: this scored high across all pillars. It might be one task "
            "with a lot of design surface, or several tasks bundled together. Splitting first "
            "usually produces better specs in the multi-piece case. The skill can produce "
            "all-4 artifacts if you want them either way — the user decides."
        )
    if (
        intent == 1
        and interface <= 2
        and behavior == 2
        and verification == 2
        and (
            answers.get("blast") in {"multiple", "system"}
            or answers.get("reversibility") != "flag"
        )
    ):
        notes.append(
            "all-low-with-stakes: this scored as trivial but blast or reversibility is "
            "non-trivial. Worth a sanity check on whether the stakes are under-counted; "
            "familiarity is when these get under-weighted."
        )

    return {
        "rungs": {
            "intent": intent,
            "interface": interface,
            "behavior": behavior,
            "verification": verification,
        },
        "reasoning": {
            "intent": intent_why,
            "interface": interface_why,
            "behavior": behavior_why,
            "verification": verification_why,
        },
        "notes": notes,
        "answers": answers,
    }


def render(result: dict[str, Any]) -> str:
    r = result["rungs"]
    why = result["reasoning"]
    lines = [
        "Suggested calibration:",
        f"  Intent:       rung {r['intent']}  ({'; '.join(why['intent'])})",
        f"  Interface:    rung {r['interface']}  ({'; '.join(why['interface'])})",
        f"  Behavior:     rung {r['behavior']}  ({'; '.join(why['behavior'])})",
        f"  Verification: rung {r['verification']}  ({'; '.join(why['verification'])})",
    ]
    if result["notes"]:
        lines.append("")
        lines.append("Notes (suggestions, not gates):")
        for n in result["notes"]:
            lines.append(f"  - {n}")
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    src = sys.argv[1]
    if src == "-":
        answers = json.load(sys.stdin)
    else:
        with open(src) as f:
            answers = json.load(f)
    result = evaluate(answers)
    print(render(result))
    print()
    print("--- machine-readable ---")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
