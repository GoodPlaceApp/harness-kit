# `run.backup-restore` — What is backed up, and when was a restore last actually tested?

```yaml
slot: run.backup-restore
title: A backup is not a backup until a restore has been performed
statement: >
  Backups run on a stated schedule to a location that survives loss of the host. A restore
  is performed end-to-end on a schedule — not inspected, actually performed into a scratch
  environment and verified against a known record. The date of the last successful restore
  is recorded where operations state is kept, and a restore older than the stated interval
  is treated as an open defect rather than a chore.
rationale: >
  Untested backups fail at exactly the moment they are needed, and the common failure is not
  a missing file — it is an unreadable format, a missing credential, or a procedure nobody
  has ever run. The date of the last successful restore is the only honest measure of
  whether a backup exists.
tier: U
evidence: documented
corroboration: 2
check: null
```

**Sources** — Google SRE Workbook, data-processing and disaster-recovery chapters; OWASP
SAMM Operations → Environment Management, which scores restore verification separately from
backup existence.
