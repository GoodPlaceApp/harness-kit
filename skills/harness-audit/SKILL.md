---
name: harness-audit
description: Check a project against the harness pack it applied and report where it has drifted — elements gone missing, practices that stopped being followed, obligations still owed. Advisory only; never fixes and never blocks. Use when asked whether a project still follows its own process, to check harness drift, or to review what a project owes its pack.
---

# Audit a project against its pack

Advisory. Reports, never repairs, never blocks. The point is a true picture, so a false
alarm costs more here than a miss.

**Argument:** none — reads `.harness/pack.lock` from the current repo. Optional
`--pack <path>` to audit against a pack the project never formally applied.

---

## 1 · Read the lock

`.harness/pack.lock` names the pack, the bindings chosen and every element's disposition.
No lock file means the project never applied a pack: say so and stop. Do not guess which
pack it might have meant.

## 2 · Re-derive the profile

Projects change shape. A repo that gained a deploy pipeline since apply is now
`has-production: true`, and a batch of previously-skipped slots have become live
obligations. Compare the current profile against the one recorded in the lock and report
any change **first** — it reframes everything below it.

## 3 · Check the applied elements

Run each `applied` element's `check`. Three outcomes:

- **Pass** — silent.
- **Fail** — the element was installed and no longer holds. This is drift.
- **No check** — a large share of Charter and Method elements are legitimately unobservable.
  List them under "not mechanically checkable" and do not imply they passed.

For elements with no `check` but an observable proxy, look — cheaply. `method.regression`
has no shell predicate, but whether recent bugfix commits carried test changes is one `git
log` away. Report such findings as **observations**, clearly separated from `check`
failures, and never assert more than the evidence supports.

## 4 · Report the other dispositions

Kept separate, because they mean different things:

- **`deferred`** — obligations the project still owes. Anything deferred because no recipe
  matched should be re-checked: the stack may have changed, or a recipe may now exist.
- **`skipped`** — was never owed. Only interesting when the profile change in step 2 means
  it is owed now.
- **`declined`** — was owed and refused deliberately. Never re-raise a declined element as
  drift; it is a decision, not a defect.

## 5 · Report

```
PACK  meridian-v1 v1 · applied 2026-08-28 · graft

PROFILE   unchanged

DRIFT (2)
  agents.review-of-agents   .claude/agents/ has no reviewer definition
  work.index                docs/README.md lists 14 docs, 17 exist

OBSERVATIONS (1)
  method.regression         4 of the last 9 bugfix commits touched no test file

DEFERRED (1)  still owed
  tool.test-selection       no recipe matched at apply time (stack: gradle)

NOT CHECKABLE (23)   ·   SKIPPED (10)   ·   DECLINED (2)

No action taken.
```

Order by consequence, not by layer. Say plainly when there is no drift — a clean audit is
the normal outcome and should read as one, not as an anticlimax.
