# Merge rules

Merging two packs produces a third that keeps the stronger half of each. The whole
procedure is decidable because both packs are keyed on the same slot vocabulary: alignment
is a join on `slot`, not a judgement call.

Merge is **not** symmetric in one respect only: when the rubric ties exactly, `A` wins.
Pass the pack you trust more as `A`.

---

## The four dispositions

For each slot in the union of both packs:

| case | disposition | action |
|---|---|---|
| Only one pack has an element | **adopt** | Copy it across unchanged. Silent. |
| Both have elements, and they are compatible | **reconcile** | Produce one element carrying the stronger statement and the union of the mechanisms. Logged, not asked. |
| Both have elements, and they are incompatible | **conflict** | Stop. Emit a card. Do not guess. |
| Neither has an element | **gap** | Record in coverage. Offer a shelf default if one exists. |

Slots that appear in neither pack's applicability profile are not merged at all — they are
carried as `not-applicable` and re-evaluated at apply time against the *target's* profile,
which may differ from both sources'.

### Compatible or incompatible?

Two elements in the same slot are **incompatible** when doing both is impossible or
self-defeating. They are **compatible** when one is a special case, a refinement, or a
differently-worded version of the other.

| A | B | verdict |
|---|---|---|
| "Every change is reviewed before merge" | "Agent-authored changes are reviewed before merge" | compatible — B is a narrowing of A; reconcile to A, note B's carve-out |
| "Work lands on an integration branch, then ships" | "Work commits directly to the main line behind flags" | **incompatible** — two answers to one question; card |
| "Tests run in parallel, always" | "Tests are selected by changed files" | compatible — different axes of one slot; reconcile to both |
| "A bugfix ships with a regression test" | "Tests are written before the code" | compatible — B implies A; reconcile to B, keep A's specific obligation |
| "Decisions are recorded and never re-litigated" | "Decisions are revisited each planning cycle" | **incompatible** — card |

`rationale` is what separates the two: elements with the same reason and different wording
reconcile; elements with different reasons pulling opposite ways conflict. When the
rationale of either side is missing, treat it as a conflict and ask — a rule whose reason is
unknown cannot be safely absorbed into another.

`conflicts_with` on either element forces a conflict regardless of the above.

---

## The ranking rubric

Applied when reconciling, and stated as the recommendation on every conflict card.
Criteria in strict order — a later criterion only breaks a tie in the earlier one.

1. **Evidence.** `production` › `documented` › `claimed` › `derived`.
2. **Corroboration.** More independent sources wins. Three `documented` sources outweigh
   one `production` observation *only* when that observation is itself a single project's
   local habit — which the extractor marks by leaving `rationale` thin. Otherwise
   criterion 1 holds.

   **Independence is checked, not assumed.** A shelf entry carrying
   `provenance.derived_from: X` was lifted out of project X by `/harness-promote`. It does
   **not** count as corroboration against a pack extracted from X — that is one project
   counted twice, and left unchecked it would inflate the evidence for whatever the kit
   already believes every time the kit learns something. Two chapters of one book, two
   articles restating one talk, and a shelf entry meeting its own origin are all one source.
3. **Specificity.** A statement that says what to do beats one that says to care.
   "Reviewed by a stronger model before merge" beats "code quality matters".
4. **Portability.** `U` › `S` › `P`. A rule that survives the next move is worth more than
   one that must be re-authored.
5. **Checkability.** An element with a `check` beats one without. What cannot be observed
   cannot be maintained.
6. **Cost.** The cheaper practice wins — in money, in wall-clock, and in human attention.
7. **Pack order.** `A` wins.

The rubric is stated in every report, with the criterion that decided each call named.
A reconciliation nobody can audit is indistinguishable from a coin flip.

---

## What actually gets merged

**Statements** — reconcile to the stronger, with the weaker preserved in `notes` when it
carries a carve-out or an exception the stronger one omits.

**Mechanisms** — union by tier. Two `U` mechanisms for one slot: keep the ranked winner,
list the other in `notes`. An `S` mechanism from each: keep both recipes; they cover
different stacks and both may be needed at apply time. A `P` from either: keep as a stub.

**Bindings** — union by id. Same id with different `meaning` is a conflict (the two packs
mean different things by one name). Same id, same meaning, different `default`: take the
winner's, note the other.

**Provenance and evidence** — never merged away. A reconciled element carries both origins
and the *lower* of the two evidence levels unless the winner's statement is adopted whole,
in which case it keeps the winner's level. Corroboration sums across independent sources.

**Coverage** — recomputed, never inherited.

---

## Conflict cards

Conflicts surface as a numbered card set. Cards are answered by number; a bare number
accepts the recommendation.

```
C1 · gov.decision-record — how a ruling is kept

   A  meridian-v1        Rulings are recorded the same day in a standing
      evidence: production   decisions file, are binding, and are reversed
      corroboration: 1       only by a new dated entry — never a silent edit.

   B  theory-review-v1   Decisions are captured as numbered ADRs in the repo,
      evidence: documented   superseded by a new ADR that references the old.
      corroboration: 3

   Incompatible: both answer "where does a ruling live", with different
   formats and different reversal mechanics. Doing both means two registers
   and no single source of truth.

   → Recommend A (criterion 1: production evidence over documented).
     B's numbering discipline is worth grafting on; taking A does not lose it.

   1) A   2) B   3) A with B's numbering   4) neither, leave the slot open
```

Rules for cards:

- **One card per slot**, never per element pair. If three packs are merged pairwise, the
  same slot must not be asked twice.
- **Always name why they are incompatible.** A card that only shows two options and no
  analysis pushes the work back onto the human.
- **Always mark a recommendation and name the criterion** that produced it.
- **Always offer a fourth way out**: leave the slot open. A merged pack with an honest hole
  is better than one with a coerced answer.
- Cards are asked in one round, not one at a time.

---

## Output

```
<out>/                     the merged pack, normal pack layout
MERGE_REPORT.md            what happened, in four sections
```

**The merged pack must be self-describing.** The report is for a human reading it once; the
manifest is what every later operation reads. A merged `manifest.yaml` therefore carries the
same sections any other pack does — `gaps`, `not_applicable`, `not_covered_by_source` where
it applies, `discrepancies` and `unhoused` unioned from both inputs, and `rulings` recording
every conflict card and its answer. Writing the accounting only into the report leaves
`audit` unable to say what the target owes, and leaves the next merge unable to see a gap.
Recompute all of it against the merged applicability profile rather than inheriting either
input's.

**Fused elements record both origins structurally.** A reconciled element's `provenance`
becomes a list, one entry per contributing source, each keeping its own `ref`, `evidence` and
`corroboration`. Prose in `notes` is not sufficient: the whole point of tracking independence
is that the *next* merge can check it mechanically, and it cannot read prose. An element that
sums corroboration across origins it does not name has over-claimed by construction.

```yaml
  provenance:
    - {source: project, ref: "meridian@3912b82", path: "docs/…", evidence: production, corroboration: 1}
    - {source: web, ref: "Google SRE Book Ch. 15 — https://…", quote: "…", evidence: documented, corroboration: 1}
  corroboration: 2          # equals the number of INDEPENDENT origins listed above
```

`MERGE_REPORT.md` contains:

1. **Summary counts** — adopted, reconciled, conflicted, gaps; coverage before and after.
2. **Adopted** — one line each: slot, which pack, evidence.
3. **Reconciled** — one block each: slot, both statements, the winner, the deciding
   criterion, what was preserved in notes.
4. **Conflicts and their rulings** — the card, the answer given, and the resulting element.

The report is the audit trail for every automatic decision. Any reconciliation a human
disagrees with should be reversible by reading this file alone.

---

## Merging more than two

`merge` takes two packs. For more, fold left: `((A ⊕ B) ⊕ C)`. Order matters — the rubric's
last tiebreaker is pack order, and earlier merges fix decisions the later ones inherit. Put
the most trusted pack first and note the fold order in the report.
