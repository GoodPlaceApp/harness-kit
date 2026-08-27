# `tool.lsp` — Which language servers run, and how do diagnostics reach the agent?

```yaml
slot: tool.lsp
title: A language server per primary language, with diagnostics fed back after every edit
statement: >
  Each primary language in the project has a language server declared in the agent
  configuration. After an edit, the server's diagnostics are returned to the agent
  automatically, giving it compiler-grade feedback rather than requiring a full build or a
  grep to notice a break.
rationale: >
  Without a language server an agent's only signals are the test suite and its own reading.
  Go-to-definition, find-references and push diagnostics turn a guess about a symbol into a
  lookup, and turn a broken edit into an immediate correction instead of a failed CI run.
tier: S
evidence: documented
corroboration: 2
check: "test -f .lsp.json || grep -q lspServers .claude-plugin/plugin.json 2>/dev/null"
```

**Recipes** — the server per language, installed separately from its declaration:
TypeScript/JavaScript `typescript-language-server` · Python `pyright-langserver` ·
Go `gopls` · Rust `rust-analyzer` · Kotlin `kotlin-lsp` · Swift `sourcekit-lsp` ·
Ruby `ruby-lsp` · C/C++ `clangd` · Java `jdtls` · C# `csharp-ls` · PHP `intelephense` ·
Lua `lua-language-server`. Also common: `terraform-ls`, `yaml-language-server`.

**Gotchas worth carrying with the default.** The first server registered for a file
extension claims it and the others never start — declare one server per extension. Servers
must log to stderr; anything on stdout is protocol traffic and stray output is read as a
crash.

**Sources** — Claude Code plugin reference (`.lsp.json` schema: required `command` and
`extensionToLanguage`, optional `args`, `transport`, `env`, `initializationOptions`,
`restartOnCrash`, `maxRestarts`); ThoughtWorks Technology Radar Vol 34, "feedback sensors
for coding agents" (Trial) and "code intelligence as agentic tooling" (Assess).
