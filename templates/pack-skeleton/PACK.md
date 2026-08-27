# {{pack_name}}

**Pack version** {{version}} · **Format** 1.0 · **Built** {{built_date}}
**Source** {{source_description}}

## What this is

{{summary}}

## Coverage at a glance

{{coverage_table}}

## How to apply this pack without any tooling

You are reading a self-contained instruction set. If `harness-kit` is not installed, follow
this protocol by hand; it is the same one the `/harness-apply` skill runs.

1. **Read the target.** Establish its stack profile (languages, package manager, build,
   test runner, CI, deploy target, UI surface) and its applicability profile
   (`has-agents`, `has-production`, `has-users`, `handles-user-data`, `has-ui`, `is-public`,
   `has-deps`, `has-schema`, `is-multi-env`, `costs-money`). Detect from manifests and
   config first; ask only what detection cannot settle.

2. **Skip what does not apply.** Every element carries `applies_when`. An element whose
   predicate is false against the target is skipped — not forced, not counted against
   coverage. A CLI tool owes no error budget.

3. **Resolve bindings by discovery first.** Each binding in the table below carries a
   `discover` procedure. Run it. Only unresolved required bindings become questions.

4. **Ask once.** Collect everything unresolved into a single round of numbered questions,
   each with 2–4 options and a marked recommendation. Do not ask one at a time.

5. **Write a plan before writing anything.** List every file to be created, modified, or
   left alone, and show it for approval. Then execute.

6. **Never delete.** In `replace` mode, a file the pack displaces moves to
   `.harness/replaced/` first. In `graft` mode, existing project practice wins and pack
   elements are added around it.

7. **Handle tiers honestly.** `U` elements are written as-is with bindings substituted.
   `S` elements select the recipe matching the target's stack — and when no recipe matches,
   write the contract plus a stub and mark the slot `deferred`. Never install a recipe for
   the wrong stack. `P` elements always become contract-plus-stub.

8. **Record what happened** in `.harness/pack.lock`: bindings chosen, both profiles, and
   every element as `applied`, `deferred`, `skipped` or `declined`.

## Bindings

{{bindings_table}}

## Elements

Full element list with statements, rationale, provenance and mechanisms:
`manifest.yaml`. Human-readable prose, one file per layer: `layers/`.
