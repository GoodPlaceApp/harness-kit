# Pack format

**Format version: 1.0**

A *pack* is a portable description of how a project is worked on. It is produced by
`extract` (from a repo) or `ingest` (from documents, URLs, or a research topic), consumed by
`apply` (into a repo), combined by `merge`, and re-checked by `audit`.

A pack is a directory. It is also a self-contained instruction set: `PACK.md` alone is
enough for an agent with none of this tooling installed to apply the pack by hand.

---

## Layout

```
<pack>/
├── PACK.md              self-executing entry point — identity, summary, and the
│                        full apply protocol in prose
├── manifest.yaml        every element, keyed by slot
├── COVERAGE.md          applicable / filled / from-shelf / gaps, per layer
├── bindings.yaml        placeholders, discovery procedures, defaults
├── profile.yaml         stack + applicability profile of the source
├── layers/
│   ├── 01-charter.md    readable prose per layer — what a human reads
│   ├── 02-method.md
│   └── … 12-reflexivity.md
└── mechanisms/          templated files, each tagged U / S / P
    ├── agents/          agent role definitions
    ├── skills/          skill bodies
    ├── settings/        settings and permission fragments
    ├── mcp/             MCP server declarations
    ├── lsp/             language server declarations
    ├── ci/              pipeline definitions
    ├── docs/            document templates and the rules that govern them
    └── scripts/         support scripts, one subdirectory per stack recipe
```

`layers/` and `manifest.yaml` describe the same content twice on purpose: the manifest is
what tools read, the layer files are what a person reads before deciding to adopt anything.
They must not disagree — `layers/` is generated from the manifest, never hand-edited.

---

## Element schema

One element answers one slot. Elements are the unit of merge, of apply, and of audit.

```yaml
- id: agents.review-gate                 # unique within the pack
  slot: agents.review-of-agents          # from SLOTS.md — never invented
  layer: 04-agents
  title: Adversarial pre-merge review by a stronger model
  statement: >
    Anything an agent authored is reviewed on its branch, before merge, by a
    read-only reviewer running a stronger model than the author. The reviewer
    returns ranked findings and exactly one of three verdicts.
  rationale: >
    An implementer verifies its own claims and cannot see what it failed to
    consider. A fresh adversarial reader on a stronger model can.
  tier: U                                # U | S | P
  applies_when: has-agents               # inherited from the slot unless narrowed
  provenance:
    source: project                      # project | document | web | research | shelf
    ref: acme-api@64381d2
    path: .claude/agents/opus-reviewer.md
    quote: null                          # required when source is not `project`
  evidence: production                   # production | documented | claimed | derived
  corroboration: 1                       # independent sources asserting this
  bindings: [reviewer_model, integration_branch]
  mechanisms:
    - path: mechanisms/agents/reviewer.md.tmpl
      tier: U
  check: "ls .claude/agents/ 2>/dev/null | grep -qi review"
  conflicts_with: []                     # element ids known to be incompatible
  notes: null
```

### Field rules

- **`slot`** must exist in `SLOTS.md`. An element whose slot is not in the vocabulary is a
  format error — extend the vocabulary deliberately or file the content under the slot it
  actually answers.
- **`statement`** is the portable content: one binding rule, phrased so it could be true of
  a project in any language. If a statement cannot be written without naming a tool, the
  element is `S` or `P` tier and the tool name belongs in a recipe or a binding.
- **`rationale`** is not decoration. Merge uses it to tell a real contradiction from two
  phrasings of one idea, and a rule whose reason is unrecorded is a rule nobody can
  correctly overrule later.
- **`evidence`** — see below. **`provenance.quote`** is mandatory for every non-project
  source: an element that cannot quote its origin is downgraded to `derived`.
- **`provenance` may be a list** — and must be, for an element fused by `merge` from two
  sources. Each entry keeps its own `ref`, `evidence` and `corroboration`. The element's
  top-level `corroboration` then equals the number of independent origins listed, and a
  count exceeding the origins named is a format error rather than a judgement call.
- **`check`** is a shell predicate, exit 0 = present. It must be cheap, read-only, and
  false-negative-averse: it is better for audit to miss a subtle drift than to cry wolf.
  `null` is allowed and means "not mechanically checkable" — a large share of Charter and
  Method elements are legitimately in this class.

### Evidence ladder

| level | means | typical source |
|---|---|---|
| `production` | Observed in a repo where it demonstrably runs | `extract` from a live project |
| `documented` | A first-party account of a practice that runs somewhere real | company handbook, postmortem, specific engineering write-up |
| `claimed` | Asserted as good practice, no named practitioner | opinion piece, conference talk, advocacy |
| `derived` | Inferred by the tool; no source states it | synthesis during ingest |

`corroboration` counts *independent* sources. Two pages of one handbook is one source.
Evidence and corroboration together are the merge rubric — see `MERGE_RULES.md`.

---

## `PACK.md` — the standalone contract

`PACK.md` must let a bare agent apply the pack with no tooling. It carries:

1. **Identity** — pack name, version, format version, when and from what it was built.
2. **Summary** — what kind of way-of-working this is, in a paragraph a human can judge.
3. **Coverage at a glance** — which layers are well covered, which are thin.
4. **The apply protocol in prose** — read the target, derive both profiles, resolve
   bindings by discovery, ask only what discovery could not answer, write a plan diff,
   get approval, then write. Including: never delete, displaced files move aside;
   non-applicable slots are skipped, not forced; unmatched `S` recipes become stubs.
5. **The binding table**, inline.
6. **A pointer to `manifest.yaml`** for the full element list.

If `PACK.md` cannot stand alone, the pack is not portable — it is a tool output.

---

## `pack.lock` — what the target records

Written into the target repo at `.harness/pack.lock` by `apply`.

```yaml
format: 1.0
applied:
  - pack: acme-api-v1
    version: 1
    at: 2026-08-28
    mode: graft                # graft | replace
bindings:
  main_branch: main
  integration_branch: dev
  reviewer_model: opus
profile:
  stack: {…}
  applies: {…}
elements:
  agents.review-gate: applied
  tool.test-selection: deferred        # S-tier, no recipe for this stack
  run.slo: skipped                     # applies_when false for this target
  charter.obligations: declined        # human said no
```

Four dispositions, and the difference matters: `deferred` is an obligation the target still
owes, `skipped` was never owed, `declined` was owed and refused on purpose. Audit reports on
`applied` only; the other three are inventory, not drift.

---

## Versioning

Packs are versioned by integer. Re-extracting a project produces version *n+1*, and a
diff between versions is a legitimate way to see how a way of working has changed.

Format version changes when the element schema or the slot vocabulary changes. Adding a
slot is a minor bump; renaming or removing one is a major bump and requires a migration
note in this file. Slot ids are never recycled.
