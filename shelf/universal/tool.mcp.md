# `tool.mcp` — Which MCP servers are installed, at what scope, with what credentials?

```yaml
slot: tool.mcp
title: MCP servers earn their place; a CLI is the default
statement: >
  An MCP server is added only when the protocol buys something a command-line tool or a
  script cannot: a live connection, a structured resource the agent must query repeatedly,
  or an authenticated surface. Project-scoped servers are declared in a checked-in
  manifest with credentials referenced by environment variable, never inlined. Each server
  is recorded with what it is for and who it talks to.
rationale: >
  Protocol overhead is frequently unjustified against simply running a command. Every
  server is also a process with local access and, when it fetches external content, a
  prompt-injection surface — so the roster should be short and each entry should have a
  reason someone can read.
tier: U
evidence: documented
corroboration: 2
check: "test -f .mcp.json"
```

**Candidates by category, when the protocol does earn it.** Version-accurate library docs
(Context7) · code host (GitHub MCP) · browser and end-to-end (Playwright MCP, which returns
accessibility-tree snapshots rather than pixels) · error tracking (Sentry) · database
(DBHub) · sandboxed execution (E2B) · design handoff (Figma) · trackers (Linear, Notion).

**Cautions worth carrying with the default.** A project-scoped manifest prompts for approval
interactively but loads unprompted in non-interactive and cloud runs — so what is committed
is what runs unattended. Stdio servers execute as local processes with full system access.
The reference server repository now keeps only a small core set; its database and cloud
servers are archived and explicitly educational, not production.

**Sources** — ThoughtWorks Technology Radar Vol 34 places "MCP by default" in **Caution**;
Claude Code MCP documentation on scopes, approval behaviour and credential expansion;
the Model Context Protocol reference server repository.
