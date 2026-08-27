# `agents.budget` — What token or cost ceiling applies per task class?

```yaml
slot: agents.budget
title: Every task class carries a stated ceiling and a stated fallback
statement: >
  Each class of agent work has a written ceiling — in spend, in tokens, or in wall-clock —
  and a stated behaviour on reaching it: stop and report, or fall back to a cheaper model.
  The ceiling is chosen from the value of the task rather than from the price of the model,
  and a task that exceeds it is a finding to report, not a limit to raise silently. Actual
  spend is attributed to task classes often enough that the ceilings can be checked against
  reality.
rationale: >
  Unbounded agent work fails in one direction only: expensively, and without producing a
  signal until the bill arrives. A ceiling per class also forces the useful question of what
  each class of work is actually worth, which is otherwise never asked.
tier: U
evidence: documented
corroboration: 1
check: null
```

**A pattern worth carrying.** Attribution is the hard half. A cheap and durable version:
every feature that makes a model call carries a cost note in its own source, and a test
pins that note against the current price table — so the note cannot silently go stale, and
the sum of the notes is a standing estimate of the run rate.

**Sources** — AWS Well-Architected, Cost Optimization pillar (expenditure awareness and
attribution as distinct practices).
