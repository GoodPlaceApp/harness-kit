# `refl.banned-targets` — Which measures may never become targets?

```yaml
slot: refl.banned-targets
title: A named list of measures that are watched but never optimised
statement: >
  The project names, in writing, which measures are observational only and may never become
  goals: volume of code produced, number of commits, count of tasks closed, lines changed,
  and any per-agent productivity figure. They may be looked at to notice a change in
  conditions; they may not be raised deliberately, and no decision cites them as a reason.
rationale: >
  Any measure of throughput becomes dishonest the moment it becomes a goal, and an agent
  optimising for it will produce more of the wrong thing very efficiently. The measures
  worth targeting are outcome measures — is it correct, is it shipped, does it stay up.
tier: U
evidence: documented
corroboration: 2
check: null
```

**Sources** — ThoughtWorks Technology Radar Vol 34 places "coding throughput metrics" in
**Hold/Caution**, explicitly noting that AI-assisted output makes volume measures worse than
useless. DORA's research consistently pairs delivery measures with stability measures for
the same reason: either alone is gameable.
