# Canon recipes

Ingest recipes for well-known corpora. A recipe tells `/harness-ingest` where a canon lives,
which layers it actually covers, and what evidence level its claims carry — so a canon reads
into slots cleanly instead of being re-derived every time.

| canon | covers layers | evidence | note |
|---|---|---|---|
| **12-Factor App** | 02 Method, 06 Toolchain | `documented` | Config, dependencies, build/release/run separation, dev-prod parity, logs. Silent on process and governance. |
| **DORA capability model** | 02 Method, 03 Governance, 12 Reflexivity | `documented` | Delivery and stability capabilities, change approval, AI stance. Research-backed; strongest available non-project evidence. |
| **Google SRE Workbook** | 07 Run | `documented` | SLOs and error budgets, alerting, on-call, incident response, postmortems, toil. The reference for layer 07. |
| **Google Engineering Practices** | 02 Method, 10 Conventions | `documented` | Code review standard ("improves overall code health"), reviewer and author guides. |
| **OWASP SAMM** | 08 Trust, 07 Run | `documented` | Five business functions; scores practices by maturity, which maps well onto slot answers. |
| **SLSA / OpenSSF Scorecard** | 08 Trust | `documented` | Build provenance levels; ~20 discrete repository checks that read almost directly as slot answers. |
| **ThoughtWorks Technology Radar** | 04 Agents, 06 Toolchain, 12 Reflexivity | `claimed` to `documented` | Current practice blips including agent tooling. Adopt/Trial entries are `documented`; Assess is `claimed`. |
| **GitLab Handbook** | 01 Charter, 03 Governance, 11 Product loop | `documented` | A public, complete company handbook — the richest single source for the team-and-company-guidelines layers. |
| **AWS Well-Architected** | 07 Run, 09 Economics | `documented` | Operational excellence, reliability, cost optimization, sustainability pillars. |

**Reading a canon into slots.** Canons are organised by their own structure, never by this
vocabulary. Read the whole corpus, then map claims onto slots — do not try to read a canon
slot-by-slot, which produces `derived` elements and misses everything the canon says that
the vocabulary did not anticipate. Anything a canon covers that no slot asks about is a
finding: report it as a candidate new slot rather than discarding it.
