---
name: harness-promote
description: Fold a practice found in one project back into the kit itself — either as a new question the slot vocabulary was not asking, or as a new best-practice default on the shelf. Use after an extraction turns up something good enough that every future project should be asked about it, or offered it. This is how the kit learns.
---

# Promote a finding into the kit

Extraction reads a project against a fixed vocabulary. Sooner or later a project answers
something well that the vocabulary never asked, or answers an existing question better than
the shelf does. Without a way back, the kit stops learning at whatever it knew on day one
and every later extraction quietly discards its best material.

This is that way back. It edits `format/` and `shelf/` — the kit itself — so **every future
extraction, apply and merge inherits it.**

**Arguments:** a pack path, optionally a specific element id or unhoused-finding id.

---

## Two promotions, and they are not the same

### A · A new slot — a question nobody was asking

Source: the `unhoused` section of a pack, where extract and ingest park content that is
clearly a practice but fits no existing slot.

Admission test, all four required (`format/SLOTS.md` § Adding a slot):

1. **No existing slot asks it.** Read the whole layer first. Most candidates are really an
   existing slot phrased differently — file them there instead, and say so.
2. **More than one defensible answer exists.** A question with one right answer is a rule,
   not a slot; it belongs in the shelf as a default.
3. **It names no language, tool or vendor.** If it cannot be phrased without one, it is a
   mechanism, not a question.
4. **It has a layer.** If it fits none of the twelve, that is a finding worth raising on its
   own — a missing layer is a much larger change than a missing slot.

To promote: add the row to the right layer table in `SLOTS.md` with an applicability
predicate, bump the format **minor** version in `PACK_SPEC.md`, and note the addition there.

**Existing packs stay valid.** A new slot simply becomes an unanswered gap in every pack
extracted before it — which is honest, and is exactly the signal that tells you which
projects to re-scout.

### B · A new shelf default — a better answer to a question already asked

Source: a strong element in a pack, where `shelf/universal/<slot>.md` has nothing.

Admission test:

1. **`production` evidence.** It was observed running, not merely written down.
2. **Tier `U`, or `S` with at least two recipes.** A single-stack answer is not a default.
3. **It carries a rationale someone can disagree with.** A default whose reason is missing
   cannot be correctly declined later.
4. **It generalises.** Ask plainly: would this be good advice for a project that shares none
   of this one's constraints? If the honest answer is "only because of how they deploy" —
   it is not a default, it is their practice.

To promote: write `shelf/universal/<slot>.md` in the shelf format — element block, a short
why, and the sources. **Strip harder than the pack did.** A pack element may keep a trace of
its origin; a shelf entry is offered to strangers and must survive with none.

---

## The self-corroboration trap

This is the rule that makes the whole loop safe, and it is easy to get wrong.

A shelf entry lifted out of project X, later merged back into a pack extracted from project
X, would look like **two independent sources agreeing** — when it is one project counted
twice. Left unchecked, every promotion silently inflates the evidence for whatever the kit
already believes.

So every promoted shelf entry records where it came from:

```yaml
provenance:
  source: shelf
  derived_from: meridian          # the pack this was lifted out of
```

and `merge` must not count such an entry as independent corroboration against any pack from
that same source. `format/MERGE_RULES.md` § Corroboration states this normatively.

Related and equally important: **a practice from one project is `documented` at best, never
`production`, once it is on the shelf.** That one project runs it is not evidence it
generalises. Promotion is a demotion in evidence, and that is correct.

---

## What promoting does not do

- It does not edit the source pack. The pack records what that project does; promotion
  records what the kit now believes. Those are different claims and both stay readable.
- It does not retro-apply. Packs extracted before a promotion keep their coverage; the new
  slot appears as a gap, and re-extraction is a deliberate act.
- It does not merge. If two packs disagree about the same slot, that is `/harness-merge`.

## Report

What was promoted and as which kind · the admission test result for each candidate,
including the ones **rejected and why** — a rejected candidate that stays visible is what
stops it being re-proposed · the format version before and after · which existing packs now
have a new gap.
