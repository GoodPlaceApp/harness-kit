# harness-kit

Capture how a project is worked on, strip the project out of it, and install it somewhere else.

A **harness** here is not just agent configuration. It is the whole operating system of a
one-person shop that runs on agents: engineering method, governance, the agent cast and
model routing, the knowledge base, the toolchain including MCP and LSP, operations,
security, economics, conventions — the team guidelines and company guidelines a solo
developer still needs, minus the team and the company.

## The five operations

| command | does |
|---|---|
| `/harness-extract [path]` | Read a project — yours or a clone of someone else's — and emit a de-specialised pack |
| `/harness-ingest <sources \| topic>` | Build the same pack from documents, slides, PDFs, URLs, or a research topic answered by web search |
| `/harness-apply <pack> [--graft \| --replace] [--dry-run]` | Install or graft a pack into a target project |
| `/harness-merge <pack-a> <pack-b>` | Combine two packs, keeping the stronger half of each |
| `/harness-audit` | Report where a project has drifted from the pack it applied |

`extract` and `ingest` are peers. A practice observed running in production and a practice
read out of a handbook land in the same format and can be compared, ranked and merged.

## How it works

Everything rests on a **slot vocabulary** — 121 questions a working setup must answer,
phrased so that no answer names a language or a tool. *"How is the right subset of tests
chosen for a change?"*, never *"run pytest -n auto"*.

Because both packs key on the same slots, merging is a join rather than a judgement call:

> same slot, incompatible answers → **conflict**, ask
> different slots → **union**, silent
> only one side has it → **adopt**
> both compatible → **reconcile** to the stronger form

Three properties on every element make packs survive the move between projects:

- **Portability tier** — `U` universal (transfers verbatim), `S` stack-conditional (a
  contract plus per-stack recipes), `P` project-bound (contract and stub only).
- **Applicability** — a predicate against the target's situation. A CLI tool is not marked
  down for having no error budget.
- **Evidence** — `production` › `documented` › `claimed` › `derived`, with a corroboration
  count. This is why a conference talk cannot quietly overrule a practice that has been
  load-bearing for months.

## Format

| file | is |
|---|---|
| [`format/SLOTS.md`](format/SLOTS.md) | The vocabulary. 12 layers, 121 slots. |
| [`format/PACK_SPEC.md`](format/PACK_SPEC.md) | Pack layout, element schema, evidence ladder, `pack.lock`. |
| [`format/PROFILES.md`](format/PROFILES.md) | Stack and applicability profiles, portability tiers, bindings. |
| [`format/MERGE_RULES.md`](format/MERGE_RULES.md) | Dispositions, ranking rubric, conflict cards. |

## The twelve layers

| # | layer | asks about |
|---|---|---|
| 01 | Charter | purpose, invariants, what agents may decide, risk appetite, licensing |
| 02 | Method | how one change is made, tested, reviewed, verified, rolled back |
| 03 | Governance | how work is chosen, escalated, decided and recorded |
| 04 | Agents | the roster, model routing, autonomy, isolation, context, recovery |
| 05 | Workstate | the knowledge base: doc tree, naming, lifecycle, handoff, onboarding |
| 06 | Toolchain | runtimes, bootstrap, MCP, LSP, static analysis, CI, ship gesture, secrets |
| 07 | Run | SLOs, alerting, incidents, postmortems, observability, restore, DR |
| 08 | Trust | threat model, secrets, dependencies, scanning, provenance, data retention |
| 09 | Economics | budget ceiling, unit cost, cost review, spend-vs-time tradeoffs |
| 10 | Conventions | code style, commits, voice, how questions are put, stable handles |
| 11 | Product loop | feedback, support, changelog, deprecation, analytics |
| 12 | Reflexivity | delivery metrics, banned targets, retro on the harness itself |

Layers 07–09 and 11–12 exist because a first draft without them silently dropped operations,
security, cost and self-measurement from every export.

## Install

```bash
gh repo clone GoodPlaceApp/harness-kit ~/GitProjects/harness-kit
claude
> /plugin install ~/GitProjects/harness-kit
```

Installed once, available in every project on the machine — which is what makes it possible
to extract from one repo and apply into another.

## Packs

| pack | from | evidence |
|---|---|---|
| `packs/meridian-v1` | practice — a live agent-run project | `production` |
| `packs/theory-review-v1` | theory — external engineering canon | `documented` / `claimed` |

A pack is a directory, and also a self-contained instruction set: `PACK.md` alone is enough
for an agent with none of this installed to apply it by hand. If that is not true of a pack,
it is a tool output rather than a portable artifact.
