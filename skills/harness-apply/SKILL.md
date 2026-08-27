---
name: harness-apply
description: Install or graft a harness pack into a project — adapting it to that project's stack and situation, writing a plan before touching anything, and recording what was applied. Use when asked to apply, install, adopt, set up or graft a way of working, agent setup or engineering process into a repo, whether the repo is new or already has practices of its own.
---

# Apply a harness pack to a project

Read `${CLAUDE_PLUGIN_ROOT}/format/PROFILES.md` and `PACK_SPEC.md` first — tiers,
applicability and bindings are what make this work on a repo unlike the one the pack came
from.

**Arguments:** a pack path. Optional `--replace` (default is `--graft`), `--dry-run`.

- **graft** — the project's existing practice wins where the two collide; pack elements are
  added around it. The right default for a repo that already works.
- **replace** — the pack wins collisions. Still never deletes: a displaced file moves to
  `.harness/replaced/` first.

---

## 1 · Read the target before the pack

Derive the target's **stack profile** and **applicability profile** per `PROFILES.md`.
Detect from manifests, lockfiles, config and CI; ask only what detection cannot settle.

The target's profile is authoritative, not the pack's. A pack extracted from a deployed
backend applied into a library gets its whole Run layer skipped — correctly.

Then inventory what the target already does, at least across Method, Governance, Agents,
Workstate and Toolchain. Applying a pack blind over existing practice is how you end up with
two roadmaps and three review gates.

## 2 · Resolve bindings by discovery

Run each binding's `discover` procedure against the target. A binding that resolves this way
never becomes a question. Unresolved optional bindings take their `default` and are noted.

## 3 · Select elements

For each element in the pack, in order:

1. **Applicability.** Predicate false against the *target's* profile → `skipped`. Not a
   gap, not a failure, not mentioned again.
2. **Tier.**
   - `U` → write as-is with bindings substituted.
   - `S` → select the recipe matching the target's stack. **No matching recipe → write the
     contract plus a stub and mark `deferred`.** Never install a recipe for the wrong stack;
     a pytest selector in a Gradle project is worse than nothing, because it looks done.
   - `P` → contract plus stub, always.
3. **Collision.** Target already answers this slot → graft mode keeps the target's answer
   and records the pack's as an alternative in the plan; replace mode moves the target's
   aside and installs the pack's.

## 4 · Ask, in one round

Unresolved required bindings, ambiguous applicability facts, and every collision that
`--replace` would overwrite. Numbered cards, 2–4 options, marked recommendation, answered by
number. One round.

## 5 · Plan before writing

Show a plan diff and get approval before creating or modifying anything:

```
CREATE   .claude/agents/reviewer.md              U    agents.review-of-agents
CREATE   docs/DECISIONS.md                       U    gov.decision-record
MODIFY   CLAUDE.md                    +18 lines  U    work.context-file
LEAVE    .github/workflows/ci.yml                     target already answers tool.ci
STUB     scripts/testselect.md                   S    no recipe for gradle → deferred
SKIP     (10 elements)                                not applicable to this target
```

Under `--dry-run`, stop here. This is also the mode for pointing the tool at a repo you do
not want modified.

## 6 · Write

Create and modify per the approved plan. Rules that hold in every mode:

- **Never delete.** Displaced files move to `.harness/replaced/` with their original path
  preserved underneath.
- **Never silently reformat** a file you are only adding to.
- **A stub is honest.** It states the contract, says why no recipe applied, and names what
  the project owes. It never pretends to be an implementation.

Then write `.harness/pack.lock` per `PACK_SPEC.md`: pack identity, mode, bindings, both
profiles, and every element as `applied`, `deferred`, `skipped` or `declined`.

## 7 · Verify

Run every applied element's `check`. A `check` that fails immediately after apply means the
element did not install correctly — fix it or mark it `deferred` honestly. Do not report a
pack as applied while its own checks are red.

Report: counts by disposition, what was deferred and what the project therefore owes, what
was left alone because the target already answered it, and the `check` results. The
deferred list is the most useful part of the report — it is the work the pack could not do
for this project.
