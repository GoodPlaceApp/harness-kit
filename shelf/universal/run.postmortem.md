# `run.postmortem` — What does an incident leave behind so it cannot recur silently?

```yaml
slot: run.postmortem
title: Every incident leaves a regression test and, where applicable, a rule
statement: >
  An incident is not closed when service returns. It is closed when it has left behind: a
  test that would have failed before the fix, a written note of what happened and what was
  actually wrong, and — where a process would have prevented it — an amendment to the
  standing rules. The note records the sequence and the cause, not a person.
rationale: >
  Restoring service removes the symptom and leaves the cause. The artifact matters more than
  the ceremony: a solo operator has no audience for a blameless review, but still needs the
  thing that stops the same failure arriving twice. A rule change with an incident behind it
  is the only kind that reliably sticks.
tier: U
evidence: documented
corroboration: 3
check: null
```

**Adapted for one person.** Blamelessness is trivial when there is one person. What survives
the collapse from a team practice is the artifact set: the test, the note, the rule. The
incident-commander role collapses into the runbook — the runbook is the missing colleague.

**Sources** — Google SRE Workbook, "Postmortem Culture"; OWASP SAMM Operations → Incident
Management; the widely-documented practice of pairing every production defect with a
regression test.
