---
name: harness-merge
description: Combine two harness packs into one that keeps the stronger half of each — union where they do not overlap, reconcile where they agree, and ask only where they genuinely contradict. Use when asked to merge, combine, reconcile or unify two ways of working, or to fold a theory pack into a pack extracted from a real project.
---

# Merge two harness packs

`${CLAUDE_PLUGIN_ROOT}/format/MERGE_RULES.md` is the specification. Read it in full before
merging anything — the dispositions, the rubric, and the compatibility test are all defined
there and this skill does not restate them.

**Arguments:** two pack paths, optionally `-o <out>`. The first pack is `A` and wins exact
ties, so pass the one you trust more first.

---

## 1 · Validate both packs

Same format version, both manifests parse, every `slot` in each exists in `SLOTS.md`. A
pack from an older format version is migrated per the notes in `PACK_SPEC.md` before
merging, never merged as-is.

Report both coverage profiles side by side before doing any work. Where the two packs are
strong is usually complementary — a production pack is thick in Method and Agents and thin
in Run and Trust; a canon pack is the reverse. Saying so up front frames every decision
that follows.

## 2 · Align on slots

Join both manifests on `slot`. Every slot in the union falls into exactly one disposition:
**adopt**, **reconcile**, **conflict**, or **gap**. Do this mechanically first, before
judging anything — the join is arithmetic, and separating it from the judgement keeps the
judgement honest.

## 3 · Classify each overlap

Apply the compatibility test from `MERGE_RULES.md`: incompatible means doing both is
impossible or self-defeating; compatible means one is a narrowing, a refinement, or a
rewording of the other.

Two traps, both common:

- **A wording difference read as a contradiction.** Compare `rationale`, not phrasing. Same
  reason, different words → reconcile.
- **A real contradiction read as a wording difference.** If reconciling would require the
  target to do two mutually exclusive things, it is a conflict however similar the prose
  looks. When either side's `rationale` is missing, treat it as a conflict — a rule whose
  reason is unknown cannot be safely absorbed into another.

## 4 · Reconcile with the rubric, and show your work

For every reconciliation, record which criterion decided it — evidence, corroboration,
specificity, portability, checkability, cost, pack order. Preserve the loser's carve-outs
and exceptions in `notes`; that is usually where the loser's real value was.

Merge mechanisms by tier: keep the winner's `U`; keep **both** `S` recipes, since they
cover different stacks and the target may need either; keep `P` as a stub.

## 5 · Ask, in one round

Conflicts become numbered cards in the format `MERGE_RULES.md` specifies: both statements
with their evidence, a plain statement of *why they are incompatible*, a marked
recommendation naming the deciding criterion, and always a fourth option to leave the slot
open. One card per slot. One round.

A merged pack with an honest hole beats one with a coerced answer.

## 6 · Emit

The merged pack in normal layout, plus `MERGE_REPORT.md` with the four sections
`MERGE_RULES.md` requires: summary counts, adopted, reconciled with deciding criteria, and
conflicts with their rulings. Recompute coverage — never inherit it.

Report: counts by disposition, coverage before and after for each input, the conflicts and
how they were ruled, and which layers the merge actually strengthened. If the merge changed
nothing meaningful, say that — two packs that produce no new coverage and no conflicts were
probably the same pack twice.
