# The slot vocabulary

A **slot** is one question a working setup must answer. Slots are phrased as questions,
never as answers — *"how is a change verified before merge?"*, never *"run pytest"*.
That is what lets one vocabulary describe a Compose app, a FastAPI service and a CLI tool.

The vocabulary is the backbone of every operation:

- **extract** and **ingest** fill slots, so a practice read out of a running repo and one
  read out of a book land in the same shape and become comparable.
- **apply** walks slots, so coverage is measurable and gaps are nameable.
- **merge** aligns on slot id: *same slot + incompatible answers = conflict (ask) ·
  different slots = union (silent) · only one side has it = adopt · both compatible =
  reconcile to the stronger form.*
- **audit** re-runs each filled slot's `check`.

## Reading a row

| column | meaning |
|---|---|
| **slot** | Stable id, `layer.name`. **Never renamed** — merge and audit key on it. |
| **question** | What the slot asks. An element answering it is the slot's content. |
| **applies** | Predicate over the target's profile (see `PROFILES.md`). A slot whose predicate is false is *excluded* from coverage, not counted as a gap. |

Predicates in use: `always` · `has-agents` · `has-production` · `has-users` ·
`handles-user-data` · `has-ui` · `is-public` · `has-deps` · `has-schema` ·
`is-multi-env` · `costs-money`. Multiple predicates are OR'd.

## Adding a slot

A new slot must be a question no existing slot asks, must be answerable by more than one
defensible answer, and must be phrased without naming any language, tool or vendor. Adding
one is a format version bump; renaming or deleting one breaks every existing pack and needs
a migration note in `PACK_SPEC.md`.

---

## 01 · Charter — why this exists and what is never traded

*Where to look:* README, the project brief (`CLAUDE.md` / `AGENTS.md`), licence files,
the top of any roadmap, any "principles" or "invariants" section, security policy.

| slot | question | applies |
|---|---|---|
| `charter.purpose` | What is this for, and what is explicitly out of scope? | always |
| `charter.invariants` | Which properties must no change ever break? | always |
| `charter.ai-stance` | What may agents decide unsupervised, and what must always reach a human? | has-agents |
| `charter.quality-speed` | When is shipping something known-imperfect acceptable? | always |
| `charter.blast-radius` | How much production risk is tolerable, and what is never risked? | has-production |
| `charter.licence` | What licence does this carry, and which dependency licences are admissible? | has-deps |
| `charter.obligations` | Which legal, contractual or ethical constraints bind the work? | handles-user-data, is-public |
| `charter.solo-adaptation` | Which team rituals are kept, which collapse into agents, which are dropped? | always |

---

## 02 · Method — how one change is made and verified

*Where to look:* contributing guide, test configuration and directory layout, CI workflow,
branch names in `git log`, the shape of recent merge commits, any testing section in the brief.

| slot | question | applies |
|---|---|---|
| `method.change-unit` | What is one unit of work, and how large may it get? | always |
| `method.branching` | How do changes reach the main line? | always |
| `method.ready` | When may work start — what must a task carry before it is dispatched? | always |
| `method.done` | When is a change done? | always |
| `method.spec-first` | Does a written spec precede code, and above what size? | always |
| `method.test-strategy` | Which test layers exist, what is never mocked, what is the floor? | always |
| `method.test-ladder` | Which checks run when, cheapest first? | always |
| `method.test-selection` | How is the right subset of tests chosen for a given change? | always |
| `method.ai-test-quality` | How is the quality of machine-written tests itself checked? | has-agents |
| `method.review-standard` | What bar must a change clear to be approved? | always |
| `method.verification` | What counts as "seen working" beyond a green suite? | always |
| `method.regression` | What must accompany a bugfix? | always |
| `method.refactor` | What cleanup needs no permission, and how is it kept apart from behaviour change? | always |
| `method.debt` | How is known-bad code recorded, and what triggers repaying it? | always |
| `method.rollback` | How is a bad change undone, and within what time budget? | has-production |
| `method.schema-change` | How do persistent-data changes ship, and how do they roll back? | has-schema |
| `method.risky-change` | How are risky changes gated — flags, canary, staged rollout? | has-production |

---

## 03 · Governance — how work is chosen, decided and recorded

*Where to look:* roadmap or backlog file, decisions/ADR log, issue tracker conventions,
bug list and its ranking, any ideas or someday file, meeting or session notes.

| slot | question | applies |
|---|---|---|
| `gov.worklist` | Where does open work live, and what does one item carry? | always |
| `gov.prioritisation` | What rule orders the work? | always |
| `gov.escalation` | What reaches the human for a decision, and in what form? | always |
| `gov.decision-record` | Where do rulings live, and how is one reversed? | always |
| `gov.provisional` | May work proceed before a pending decision, or does it block? | always |
| `gov.defects` | How are defects tracked, and what ranks one above another? | always |
| `gov.ideas` | How do unfunded ideas enter, get promoted, or die? | always |
| `gov.wip` | How much may be in flight at once? | always |
| `gov.cadence` | What is the planning / review / ship rhythm? | always |
| `gov.replan` | What triggers a re-plan rather than another task? | always |

---

## 04 · Agents — the cast, their limits, and what they are told

*Where to look:* `.claude/agents/`, `.claude/skills/`, `.claude/settings*.json`, plugin
manifests, the workflow section of the project brief, dispatch-prompt files, `git log`
for agent-authored commits.

| slot | question | applies |
|---|---|---|
| `agents.roster` | Which agent roles exist, and what is each one's single responsibility? | has-agents |
| `agents.routing` | Which model and effort level for which role or task class? | has-agents |
| `agents.autonomy` | What may an agent do unattended, and where must it stop and ask? | has-agents |
| `agents.isolation` | How are concurrent agents kept from colliding — worktrees, branches, sandboxes? | has-agents |
| `agents.credentials` | What access does an agent get, and what is deliberately withheld? | has-agents |
| `agents.dispatch` | What must a task prompt contain to be runnable by a fresh agent with no history? | has-agents |
| `agents.partitioning` | How is concurrent work split so two agents never write the same file? | has-agents |
| `agents.report` | What shape must an agent's return take? | has-agents |
| `agents.review-of-agents` | Who reviews agent output, against what checklist, and what may skip review? | has-agents |
| `agents.context` | What goes into an agent's context, what is deliberately excluded, and how is bloat controlled? | has-agents |
| `agents.sensors` | What automated feedback does an agent get while working — tests, types, diagnostics? | has-agents |
| `agents.recovery` | What happens when an agent stalls, dies, or is killed mid-flight? | has-agents |
| `agents.attribution` | How is agent-authored work marked in history? | has-agents |
| `agents.injection` | How is untrusted content — web pages, documents, tool output — prevented from acting as instruction? | has-agents |
| `agents.budget` | What token or cost ceiling applies per task class? | has-agents, costs-money |

---

## 05 · Workstate — the knowledge base agents and humans read

*Where to look:* the docs tree and its index, archive folders, naming patterns across
filenames, the project brief, any handoff or session-state file — **and the project's
user-level state directory**, which holds durable memory outside the repository. See
`tools/user_state.py`; never read the session transcripts there.

| slot | question | applies |
|---|---|---|
| `work.doc-tree` | Where does each kind of knowledge live? | always |
| `work.naming` | What are the file naming rules, and what do they encode? | always |
| `work.one-home` | What prevents the same fact living in two places? | always |
| `work.index` | What keeps the index of documents true as documents change? | always |
| `work.lifecycle` | When does a document stop being current, and where does it go? | always |
| `work.context-file` | What does the agent-facing project brief contain, and what is kept out of it? | has-agents |
| `work.handoff` | What does the next session read first to resume work? | always |
| `work.onboarding` | In what order does a newcomer — human or fresh agent — read? | always |
| `work.danger-list` | Where is the register of things not to change without understanding? | always |
| `work.research-cache` | Where does external research land so it is not re-fetched? | always |
| `work.memory` | What knowledge outlives a session without living in the repository, and what belongs there rather than in the docs? | always |
| `work.queue` | Where do ready-to-run task prompts live, and when is one removed? | has-agents |

---

## 06 · Toolchain — what is installed and how it is wired

*Where to look:* manifests and lockfiles, `.mcp.json`, `.lsp.json`, linter and formatter
config, CI workflow files, container and environment definitions, setup scripts, hook config.

| slot | question | applies |
|---|---|---|
| `tool.stack` | What languages, package manager and build does this use? | always |
| `tool.runtime-pinning` | How are runtime and dependency versions pinned and reproduced? | always |
| `tool.bootstrap` | What single command takes a clean machine to a working checkout? | always |
| `tool.harness-config` | Where does agent configuration live — settings, hooks, permissions? | has-agents |
| `tool.mcp` | Which MCP servers are installed, at what scope, with what credentials? | has-agents |
| `tool.lsp` | Which language servers run, and how do diagnostics reach the agent? | has-agents |
| `tool.static` | What lints, formats and type-checks, and where does each run? | always |
| `tool.test-runner` | What runs the tests, and how is it parallelised? | always |
| `tool.visual` | How is a change to the interface actually looked at? | has-ui |
| `tool.ci` | What runs automatically on push, and what gates a merge? | always |
| `tool.ship` | What is the gesture that ships, and what must be true before it fires? | has-production |
| `tool.secrets` | Where does configuration and secret material live, and how does it reach the process? | always |
| `tool.environments` | Which environments exist, and how do they differ from each other? | is-multi-env |

---

## 07 · Run — what happens once it is live, and when it breaks

*Where to look:* monitoring and alert config, service definitions, cron and scheduler
entries, operations docs, runbooks, backup scripts, incident or postmortem notes.

| slot | question | applies |
|---|---|---|
| `run.slo` | What level of service is promised, and how is the error budget spent? | has-production |
| `run.alerting` | What wakes a human, and what merely queues for later? | has-production |
| `run.incident` | What happens, step by step, when production breaks? | has-production |
| `run.postmortem` | What does an incident leave behind so it cannot recur silently? | has-production |
| `run.runbooks` | Where are the procedures for known operations? | has-production |
| `run.observability` | What logs, metrics and traces exist, and how does an agent inspect production? | has-production |
| `run.backup-restore` | What is backed up, and when was a restore last actually tested? | has-production |
| `run.degradation` | What does the system do when a dependency fails? | has-production |
| `run.dr` | How is the whole thing rebuilt if the host is lost? | has-production |
| `run.toil` | What manual recurring work exists, and what is the plan to remove it? | has-production |

---

## 08 · Trust — security, supply chain and data

*Where to look:* security policy, dependency manifests and update automation, scanning
config in CI, secret-management setup, privacy or retention docs, third-party integration config.

| slot | question | applies |
|---|---|---|
| `trust.threat-model` | Who or what is this defended against, and what is out of scope? | always |
| `trust.secrets` | How is secret material stored, injected and rotated? | always |
| `trust.least-privilege` | What is the minimum access each actor gets, and who has more than that? | always |
| `trust.scanning` | What scans for vulnerabilities and leaked secrets, and when? | always |
| `trust.cve` | How fast must a known vulnerability be answered? | has-deps |
| `trust.deps` | How are dependencies chosen, updated and vetted before adoption? | has-deps |
| `trust.provenance` | What proves the running artifact came from this source? | has-production, is-public |
| `trust.third-party-agents` | How is a third-party MCP server, plugin or skill trusted before use? | has-agents |
| `trust.pii` | What personal data is held, and how is it classified? | handles-user-data |
| `trust.retention` | What is deleted, and when? | handles-user-data |
| `trust.source-terms` | What terms bind the data and content this ingests or republishes? | always |
| `trust.disclosure` | How does someone report a vulnerability, and what happens then? | is-public, has-users |

---

## 09 · Economics — what it costs to run and to build

*Where to look:* cost notes in code or docs, model routing tables, billing dashboards
referenced in docs, any budget or cost-review file, infrastructure sizing.

| slot | question | applies |
|---|---|---|
| `econ.budget` | What is the spend ceiling, and what happens when it is reached? | costs-money |
| `econ.unit-cost` | What does one run, one feature, or one model call cost? | costs-money |
| `econ.review` | How often is spend reviewed, and against what baseline? | costs-money |
| `econ.tradeoff` | When is money spent to save time, and when is the reverse correct? | costs-money |

---

## 10 · Conventions — the surface craft

*Where to look:* style and formatter config, recent commit messages, existing code for
naming and comment density, user-facing copy, error strings, any voice or tone document.

| slot | question | applies |
|---|---|---|
| `conv.code-style` | What style applies, how are things named, and what enforces it? | always |
| `conv.comments` | What gets a comment, and what deliberately does not? | always |
| `conv.commits` | What shape do commits, branches and pull requests take? | always |
| `conv.voice` | What rules bind anything a human reads? | always |
| `conv.asking` | How must a question be put to the human — format, options, defaults? | always |
| `conv.errors` | What shape do error messages and log lines take? | always |
| `conv.a11y` | What accessibility bar must the interface clear? | has-ui |
| `conv.api` | How are public interfaces versioned and deprecated? | has-users |
| `conv.handles` | What stable identifiers exist, and what may never be renumbered? | always |

---

## 11 · Product loop — the path between users and the work list

*Where to look:* changelog, release notes, issue templates, support or feedback channels
named in docs, analytics configuration.

| slot | question | applies |
|---|---|---|
| `prod.feedback` | How does user feedback reach the work list? | has-users |
| `prod.support` | How is a user report triaged? | has-users |
| `prod.changelog` | How do users learn what changed? | has-users |
| `prod.deprecation` | How is something taken away from users? | has-users |
| `prod.analytics` | What usage is measured, and what is deliberately not measured? | has-users |
| `prod.acceptance` | Who decides a feature is good enough for users, and how? | has-users |

---

## 12 · Reflexivity — the process examining itself

*Where to look:* retrospective notes, metrics dashboards, any file recording accepted
risks or deferred verifications, the rationale attached to standing rules.

| slot | question | applies |
|---|---|---|
| `refl.delivery-metrics` | What is measured about the work itself? | always |
| `refl.banned-targets` | Which measures may never become targets? | always |
| `refl.pack-retro` | When is this way of working itself reviewed? | always |
| `refl.falsification` | What evidence would show a rule here is wrong? | always |
| `refl.risk-register` | Which known risks are accepted, and when does each acceptance expire? | always |
| `refl.rule-origin` | Does every standing rule record why it exists? | always |
