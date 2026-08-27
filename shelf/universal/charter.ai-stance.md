# `charter.ai-stance` — What may agents decide unsupervised, and what must reach a human?

```yaml
slot: charter.ai-stance
title: A written line between what agents decide and what they escalate
statement: >
  The project states, in writing and in one place, what an agent may decide on its own and
  what must reach a human first. The line is drawn by reversibility and reach, not by
  difficulty: work that is cheap to undo and confined to the repository is decided by the
  agent; anything that spends money beyond a stated threshold, changes a public surface,
  touches production data, or contradicts a standing decision is escalated. Where the line
  is unclear the agent proceeds and flags, rather than blocking — with the flag being a
  confirm-or-overrule item rather than a notification.
rationale: >
  An unstated line is re-negotiated in every session, which is slow and produces different
  answers each time. Drawing it by reversibility rather than by importance is what keeps it
  workable: an agent cannot reliably judge what matters, but it can reliably judge whether
  something can be undone.
tier: U
evidence: documented
corroboration: 2
check: null
```

**Sources** — DORA's capability model names a "clear and communicated AI stance" as a
distinguishing practice of teams that get value from AI assistance; ThoughtWorks Technology
Radar Vol 34 places curated shared instructions in **Adopt** for the same reason.
