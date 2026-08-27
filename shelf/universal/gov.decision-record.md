# `gov.decision-record` — Where do rulings live, and how is one reversed?

```yaml
slot: gov.decision-record
title: One append-only decision log; reversal is a new dated entry, never an edit
statement: >
  Every decision that closes an argument is recorded in one file, with a stable identifier,
  the date, the question, the answer, and the reason. The record is binding: a decision in
  it is not re-argued without new information. Reversal is a new dated entry that references
  the identifier it supersedes — the original is never edited or deleted, so the history of
  what was believed when stays readable.
rationale: >
  Without a record, the same question is re-litigated whenever context is lost — which for
  agent sessions is constantly. The reason matters as much as the answer: a ruling whose
  rationale is unrecorded cannot be correctly overturned later, because nobody can tell
  whether the conditions that produced it still hold. Editing in place destroys exactly the
  evidence a future reversal needs.
tier: U
evidence: documented
corroboration: 3
check: "ls docs 2>/dev/null | grep -qiE 'decision|adr' || test -d doc/adr || test -d docs/adr"
```

**Adapted for one person.** More valuable solo, not less: with a team, several people
remember why. With one person and a rotating cast of agent contexts, the file *is* the
memory. Numbered identifiers should be cited from code comments and other documents so a
reader meeting the constraint finds the reasoning.

**Sources** — the architecture decision record literature (adr.github.io) and its widespread
adoption; DORA on streamlining change approval; GitLab's public handbook, which treats the
written record as the primary artifact rather than a byproduct.
