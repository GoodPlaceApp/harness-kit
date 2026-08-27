# `run.alerting` — What wakes a human, and what merely queues?

```yaml
slot: run.alerting
title: Two severities only — page now, or queue for the next working session
statement: >
  Every alert is classified into exactly one of two levels. **Page** means a human is
  interrupted immediately, and is reserved for conditions where waiting causes damage that
  cannot be undone: the service is down, data is being lost, or spend is running away. Everything
  else **queues** and is read at the next working session. A new alert must be assigned a
  level when it is created, and an alert that has paged without requiring immediate action
  is either re-levelled or deleted.
rationale: >
  A rotation is impossible with one person, so the only lever left is a brutally short list
  of things allowed to interrupt. An alert that fires without demanding action trains the
  operator to ignore the channel, which costs more than the alert ever saved.
tier: U
evidence: documented
corroboration: 2
check: null
```

**Adapted for one person.** The rotation drops entirely — sustainable on-call needs six to
eight people, which is not available. What replaces it is an explicit, written accepted-downtime
window: the hours during which the service may be down without anyone being woken. Stating it
converts an unbounded obligation into a bounded one.

**Sources** — Google SRE Workbook, "On-Call" (minimum sustainable rotation size) and
"Alerting on SLOs" (symptom-based alerting, actionability as the admission test).
