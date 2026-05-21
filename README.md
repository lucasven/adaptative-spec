# Motivations [This section was NOT AI generated]

Goal: __*Generate the most assertive code while reviewing the least ammount of code/text possible upfront*__

I decided to create *(yet another)* spec skill to overcome a pain I have been feeling lately when using AI coding tools to development purposes.

## Problem it tries to resolve

My main issue is that, oftentimes we do research and create plans, where we have to analyze a lot of code that will be written when our actual main goal is to have a feature developed. That feature (in our heads) is not code, it is also not specific data, it is a behavior we are trying to codify. And for that specific purpose, analysing code in a plan is overkill, since we're mostly trying to get work done, and it's not time to review specific code yet.

## Other Solutions and their problems

Specification techniques for coding exist for ages, and they are great. So, why not just use it? we already have many spec techniques and many AI skills to help us define and review them.

My pain point with all other skills I tested was: it either tried to be specify too much (a common AI problem) or too little, and it generated too much text to review (or gaps), and my main pain with that is that if I need to review all this written text I should probably just create a plan with code and analyze the plan and code instead of reading and reviewing all these descriptions.

## My solution

After some back and forth with AI, with a simple goal in mind 
__"Generate the most assertive code while reviewing the least ammount of code/text possible"__
I decided that the best spec approach in the AI era would actually be to adjust specification levels to the task we're trying to complete.

With that AI suggested to have 4 specification levels across 4 pillars. 

Too simple? light spec.
Too complex? heavy spec.
Need to do a second pass to confirm behavior intent works as expected? just point your AI to the verification-spec folder of the spec you created with a clean context and let it burn to verify it actually satisfies what you needed.

---
# Spec Handoff Skill Bundle (v3)

Five skills that help shape a task into a spec the user can hand to AI for autonomous, verifiable work. The skill *discusses the feature and explores the codebase first*, then proposes a calibration based on what it learned, then produces a folder of real files. The user never has to score their own task in framework vocabulary.

## What changed in v3

The major shift versus v2: **discovery before calibration.** The skill no longer opens with the five framework questions. Instead it asks the user to describe the feature, explores the codebase, and applies the rubric to its own understanding. Only then does it propose a calibration — as a summary the user can confirm or correct.

This matches how people actually want to use the skill: I tell you what I want to build, you understand it, you tell me how much spec it needs. Not: I describe it in your vocabulary, you score it.

The rubric (`spec-handoff/references/questions.md`) is now explicitly marked as internal. It's the framework the AI applies to itself after discovery, not a script to read at the user.

## Posture

The bundle is **assistive**, not gating. It never says "do not proceed." It says "here's what I understood, here's what I'd suggest, here's where I'd put the artifacts — confirm or adjust."

## What's here

| Skill | Role | When to invoke |
|---|---|---|
| `spec-handoff` | Orchestrator: discover, calibrate, dispatch | When you have a task and want help structuring its spec |
| `intent-spec` | Produces Intent artifacts (rungs 1–4) | When the rung is settled and you need just an intent artifact |
| `interface-spec` | Produces Interface artifacts (rungs 1–4) | When the rung is settled |
| `behavior-spec` | Produces Behavior artifacts (rungs 1–4) | When the rung is settled |
| `verification-spec` | Produces Verification artifacts (rungs 1–4) | When the rung is settled |

Typical use: invoke `spec-handoff` with a feature description. It handles discovery, calibration, and dispatch.

## Output: a folder of real files

```
specs/<task-name>/
├── README.md                    # ~50 lines: navigation, calibration summary
├── calibration.json             # rubric answers, computed rungs, reasoning, discovery notes
├── intent/
│   ├── README.md
│   ├── story.md                 # rung 2+
│   └── example-map.md           # rung 4
├── interface/
│   ├── README.md
│   ├── schema.<ext>             # actual code: .ts, .py, .go etc.
│   └── protocol.md              # rung 4
├── behavior/
│   ├── README.md
│   ├── rules.md
│   ├── examples.json            # data file, not embedded markdown
│   ├── state-machine.md         # rung 4
│   └── invariants.md            # rung 4
└── verification/
    ├── README.md
    ├── acceptance.test.<ext>    # actual runnable test file
    ├── evals.jsonl              # rung 4
    └── properties.test.<ext>    # rung 4
```

Code in code files. Data in data files. Prose in markdown. Root README is navigation only.

## Mental model

Every task ready for autonomous AI handoff typically pins:

1. **Intent** — what success looks like
2. **Interface** — the I/O shape
3. **Behavior** — the rules under conditions
4. **Verification** — how to check correctness

Each pillar has a 4-rung ladder from loose (rung 1) to tight (rung 4). Rungs are calibrated **independently per pillar** based on three signals:

- **Novelty** — has this shape of work been done before?
- **Blast radius** — what breaks if it's wrong?
- **Reversibility** — how hard is it to undo?

The cross-pillar default: **Verification rung ≥ Behavior rung**.

## Workflow

```
1. Discover     — discuss feature with user, explore codebase
2. Self-calibrate — apply rubric to discovered understanding
3. Propose      — summarize feature + show calibration with reasoning
4. (user adjusts if needed)
5. Inheritance + convention check (mostly already done in step 1)
6. Produce      — dispatch to pillar skills, write files to folder
7. Annotate     — walk quality bars, write annotated checklists
8. Present      — point to folder, summarize, stop
```

Discovery is the most important phase and the one that's most invisible — the user should feel like they're describing their feature to someone who understands it, not filling out a calibration form.

## Installation

This is a Claude Code skill plugin.

**Clone and use locally:**

```bash
git clone https://github.com/lucasven/adaptative-spec.git
claude --plugin-dir /path/to/adaptative-spec
```

**Via marketplace (for persistent installation):**

```bash
# Inside Claude Code, add this repo as a marketplace
/plugin marketplace add lucasven/adaptative-spec

# Then install the plugin
/plugin install adaptative-spec
```

Once installed, skills are invoked as `/adaptative-spec:spec-handoff`, `/adaptative-spec:behavior-spec`, etc. Run `/reload-plugins` after installation to apply changes.

## Customization

The defaults reflect general patterns. Adjustable per project:

- **Scoring formula** in `plugins/adaptative-spec/skills/spec-handoff/references/scoring.md`
- **Quality bars** in each pillar's `plugins/adaptative-spec/skills/<pillar>/references/quality-bar.md`
- **File extensions** in `plugins/adaptative-spec/skills/spec-handoff/references/handoff-folder.md`
- **Method choices** at rung 3 Behavior (examples vs decision table vs scenarios)

## Tested examples

The scoring script reproduces the four worked examples from the design conversation:

- LLM provider adapter → 1 / 4 / 3 / 3
- Admin UI screen → 1 / 2 / 3 / 3
- JSON → Postgres migration → 2 / 4 / 4 / 4
- Multi-agent infrastructure → 4 / 4 / 4 / 4 (with all-pillars-high note)

## Changelog

**v3** (this version):
- Discovery before calibration. The skill discusses the feature and explores the codebase before applying any framework. Pillar questions are now an internal rubric the AI runs against its own understanding, not a script to read at the user.
- Proposal step shows the user a feature summary + calibration with reasoning, in feature-specific language. User confirms or adjusts.

**v2**:
- Posture changed from gating to assistive. Quality bars annotate rather than block.
- Output is a folder of real files instead of a monolithic markdown.

**v1**:
- Initial release. Monolithic markdown handoff package; quality bars enforced; all-4s blocked production.
