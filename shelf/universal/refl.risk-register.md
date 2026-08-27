# `refl.risk-register` — Which known risks are accepted, and when does each acceptance expire?

```yaml
slot: refl.risk-register
title: Accepted risks are written down with an expiry or a revisit trigger
statement: >
  A known risk that is deliberately not addressed is recorded with three things: what the
  risk is, why it is acceptable now, and what would make it unacceptable — a date, a
  threshold, or an event. Recording the trigger is what distinguishes an accepted risk from
  a forgotten one. Recommendations that were considered and declined are recorded the same
  way, next to the thing they were declined about.
rationale: >
  Every project accumulates deliberate exposure, and almost none of it is written down —
  so when conditions change nobody notices that the reason for accepting it has evaporated.
  An acceptance without an expiry is indistinguishable, six months later, from an oversight.
tier: U
evidence: documented
corroboration: 2
check: null
```

**A pattern worth carrying.** The record is strongest when it sits *in the artifact it
concerns* rather than in a central register — a declined hardening recommendation noted in
the header of the pipeline file it was declined for, with the condition that would reverse
it ("the moment anyone else gets push access"). Whoever next edits that file reads the
decision without having to know a register exists.

**Sources** — OWASP SAMM Governance → Policy and Compliance, which treats documented risk
acceptance with review triggers as a distinct maturity level; standard risk-register practice.
