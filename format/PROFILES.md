# Profiles — how one pack fits many kinds of project

Two profiles decide what a pack does when it meets a specific repo. Both live in the pack
(`profile.yaml`, describing the *source*) and are re-derived for the *target* at apply time.

---

## Stack profile — what this project is built from

```yaml
stack:
  languages: [python, javascript]      # in rough order of mass
  package_managers: [pip, npm]
  build: vite                          # or gradle, cargo, xcodebuild, none
  test_runner: pytest                  # the primary one
  test_runners_secondary: [vitest]
  ci: github-actions                   # or gitlab-ci, none
  deploy_target: vps-systemd           # or app-store, serverless, container, library, none
  ui_surface: web                      # web | mobile | desktop | cli | tui | none
  vcs_host: github
```

Detected, not asked, wherever possible. Detection order is *manifest files first*
(`pyproject.toml`, `package.json`, `build.gradle.kts`, `go.mod`, `Cargo.toml`,
`Package.swift`, `pubspec.yaml`), then lockfiles, then config files, then file-extension
census as a last resort. Anything still unknown becomes one card in the single question round.

The stack profile drives **recipe selection** for `S`-tier mechanisms — see below.

---

## Applicability profile — what is true about this project's situation

```yaml
applies:
  has-agents: true          # AI agents do work in this repo
  has-production: true      # something is deployed that someone depends on
  has-users: false          # humans other than the author use it
  handles-user-data: false  # stores or processes data about people
  has-ui: true              # there is a human-facing interface
  is-public: false          # source or product is publicly visible
  has-deps: true            # uses third-party dependencies
  has-schema: true          # persistent store with a schema
  is-multi-env: false       # more than one deployment environment
  costs-money: true         # recurring spend — infrastructure or model calls
```

Each slot in `SLOTS.md` carries an `applies` predicate. A slot whose predicate is false is
**excluded** from that project's coverage — not counted as a gap, not offered a default, not
reported by audit. A single-user CLI tool is not failing because it has no error budget.

Detection is heuristic and always confirmable: a deploy workflow implies `has-production`,
a privacy policy or a users table implies `handles-user-data`, a public remote implies
`is-public`. Anything ambiguous becomes a card. Getting one of these wrong is cheap to fix
and expensive to leave — a false `has-users` fills the pack with support-triage obligations
nobody needs.

### Current state on extract, intended state on apply

The same predicate is read two different ways depending on the operation, and conflating
them breaks apply badly.

**`extract` reads the source as it is.** A project with no deployment has
`has-production: false`, and the Run layer is honestly excluded from its pack.

**`apply` reads the target as it is *meant to become*.** This matters most for
`has-agents`: a repository being given a harness for the first time has no agent
configuration *yet* — that is the whole reason it is being applied. Deriving
`has-agents: false` from its current state would skip the entire Agents layer plus the
agent-facing brief, the dispatch queue, harness configuration and the language-server and
server declarations, and install a harness containing nothing about agents. The predicate
answers "will this be true once this pack is applied", not "is this true now".

So apply asks rather than detects wherever the two readings diverge. The rule of thumb:
predicates about **circumstance** — `has-production`, `has-users`, `handles-user-data`,
`has-schema`, `is-multi-env`, `costs-money`, `is-public` — are detected, because intent
does not change them. Predicates about **practice** — `has-agents` above all — are
intentions, and are confirmed with the human in the single question round.

*(Found by applying a production-extracted pack to a Kotlin mobile app and a Node server,
neither of which had any agent configuration.)*

---

## Portability tiers — how a mechanism survives the move

Every mechanism in a pack carries a tier. This is the mechanism that makes packs
stack-agnostic in practice rather than in aspiration.

### `U` — universal

Transfers verbatim. States something true regardless of language, framework or platform.

> *The index of documents is updated in the same commit as the document it indexes.*

Apply writes it as-is, substituting bindings only.

### `S` — stack-conditional

A **contract** plus a set of **recipes**. The contract is the portable part and states the
property to be achieved; a recipe is one stack's way of achieving it.

> **Contract** — *A change-to-test selector maps edited files to the smallest test
> selection that still covers them. Files above a named hub threshold force the full suite.
> Every partial selection includes the core block. The selector never narrows silently:
> what it dropped is printed.*
>
> **Recipes** — `python/pytest` · `js/vitest` · `js/jest` · `kotlin/gradle` ·
> `swift/xctest` · `go/gotest` · `rust/cargo`

Apply picks the recipe matching the target's `stack` block. When no recipe matches, the
contract is written out with a stub and the slot is marked `deferred` in `pack.lock` —
never silently dropped, and never filled with a recipe for the wrong stack.

### `P` — project-bound

Cannot be carried across at all: it encodes something specific to one system's domain,
infrastructure or history. Exports as the contract plus a stub, so the target knows the
obligation exists and has to author its own answer.

> *The named list of hub files whose modification forces a full-suite run.*

---

## Bindings — the values lifted out of every mechanism

De-specialisation works by replacing every project-specific literal with a named binding.

```yaml
bindings:
  - id: main_branch
    meaning: The branch that represents shippable state
    discover: "git symbolic-ref refs/remotes/origin/HEAD, else default branch via host API"
    default: main
    required: true
  - id: integration_branch
    meaning: Where work lands before it ships; may equal main_branch
    discover: "most common merge target in git log over the last 100 merges"
    default: "{main_branch}"
    required: true
  - id: reviewer_model
    meaning: The model used for adversarial pre-merge review
    discover: "existing agent definitions under .claude/agents/"
    default: the strongest available model
    required: false
```

`discover` is a *procedure*, not a value — apply runs it against the target before asking
anything. A binding that resolves by discovery never becomes a question. Bindings that
remain unresolved and are `required: true` become cards in the single question round;
unresolved optional bindings fall back to `default` and are noted in `pack.lock`.

Bindings may reference each other with `{other_id}`. Cycles are a format error.
