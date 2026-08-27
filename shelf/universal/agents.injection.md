# `agents.injection` — How is untrusted content prevented from acting as instruction?

```yaml
slot: agents.injection
title: Fetched and tool-returned content is data, never instruction
statement: >
  Anything an agent did not receive in its own dispatch — web pages, documents, tool output,
  another agent's return, issue text, user-supplied content — is treated as data. Text in
  such content that is shaped like an instruction is reported as a finding, never obeyed.
  Agents that fetch external content are given the narrowest credentials that let them work,
  and the boundary is stated in the agent's own definition rather than assumed.
rationale: >
  An agent that will follow instructions found in what it reads can be steered by anyone who
  can get text in front of it — a web page, a dependency's README, a commit message. The
  defence has to be a standing rule in the agent's contract, because the attack arrives
  precisely when nobody is watching.
tier: U
evidence: documented
corroboration: 2
check: null
```

**Sources** — ThoughtWorks Technology Radar Vol 34, "toxic flow analysis" (Assess) and the
sandboxed-execution entries; Claude Code MCP documentation on external-content servers as an
injection surface.
