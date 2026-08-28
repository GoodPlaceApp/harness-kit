---
name: harness-extract
description: Read a project and emit a portable, project-agnostic harness pack — how that project is worked on, stripped of what makes it that project. Use when asked to extract, capture, export or lift a project's way of working, agent setup, process or engineering practices so they can be reused elsewhere. Works on any repo, including a clone of someone else's.
---

# Extract a harness from a project

Turn a working project into a pack another project can adopt. Read
`${CLAUDE_PLUGIN_ROOT}/format/SLOTS.md`, `PACK_SPEC.md` and `PROFILES.md` first — the slot
vocabulary and the element schema are binding, not suggestions.

**Argument:** a path. Defaults to the current repo. May be any checkout, including a clone
of a project you did not write — extracting how a well-run open-source project handles
releases is a legitimate use.

---

## 1 · Establish both profiles

Before reading anything else, derive the **stack profile** and the **applicability
profile** per `PROFILES.md`. Detect, do not ask:

- Stack: manifests first (`pyproject.toml`, `package.json`, `build.gradle*`, `go.mod`,
  `Cargo.toml`, `Package.swift`, `pubspec.yaml`), then lockfiles, then config, then a
  file-extension census as a last resort.
- Applicability: a deploy workflow or service definition implies `has-production`; a
  privacy policy, a users table or auth code implies `handles-user-data`; a public remote
  implies `is-public`; `.claude/`, `.cursor/` or agent definitions imply `has-agents`;
  model-call code or an infrastructure bill referenced in docs implies `costs-money`.

Anything ambiguous is held for the question round. Do not guess `has-users` — the
difference between a personal tool and a product changes twenty slots.

## 2 · Fan out one scout per layer

Dispatch `harness-scout` twelve times in parallel — one per layer. Each dispatch carries:
the layer id, that layer's slot table **verbatim** from `SLOTS.md`, the target path, the
source kind (`project`), and both profiles.

Do not read the whole project yourself first. The scouts are the readers; your job is
orchestration and reconciliation. Reading everything twice wastes the context that the
merge step needs.

Layers 09 (Economics), 11 (Product loop) and 12 (Reflexivity) are frequently thin. Dispatch
them anyway — a confirmed absence is a finding, and those are exactly the layers a project
does not know it is missing.

## 3 · Reconcile the returns

Scouts work blind to each other. When their returns land:

- **Cross-layer duplicates.** The same practice often surfaces in two layers — a review
  gate as both `method.review-standard` and `agents.review-of-agents`. Keep both only if
  they answer genuinely different questions; otherwise assign it to the more specific slot
  and cross-reference from the other.
- **Contradictions between scouts** go into the pack's discrepancy list and, if they matter
  to a statement, into the question round.
- **Confidence.** Anything `low` either gets verified by you directly or becomes a card.
  Do not launder a low-confidence guess into a pack element.

## 4 · De-specialise

Walk every statement and mechanism for leaked specifics. Four kinds leak most often:

1. **Names** — branches, paths, services, hosts, models, commands, file names.
2. **Domain vocabulary** — anything naming what the product is *about*. Rewrite in terms of
   the role the thing plays: not "the signals table", but "the primary derived-state store".
3. **Counts and thresholds** that are tuned to one system's size.
4. **Stack assumptions inside a `U` statement** — if it mentions a tool, it is not `U`.
   Demote it to `S`, move the tool into a recipe, and write the contract as the statement.

Each removal proposes a binding with a `discover` procedure. A stripped literal with no
binding behind it is a hole, not a generalisation.

Then re-read each statement and ask: *could this be true of a Kotlin mobile app and a Go
service at the same time?* If not, the tier is wrong.

## 5 · Coverage

Compute per layer: applicable slots, filled, gaps, not-applicable. Gaps are slots that
apply to this source and have no element. Report them plainly — an extraction that hides
holes is worth less than one that names them, because the holes are precisely what a later
merge is for.

## 6 · One question round

Collect into a single numbered card set:

- **Unknowns** from the scouts — where only the human can say whether something is a rule
  or an accident.
- **Unresolved required bindings** that discovery could not settle.
- **Ambiguous applicability facts.**
- **A shelf offer per gap**, where `${CLAUDE_PLUGIN_ROOT}/shelf/` has a defensible default.
  Each is accept-or-decline individually. Accepted defaults enter the pack with
  `provenance.source: shelf` and `evidence: claimed`, never disguised as project practice.

Card format: question · 2–4 options · marked recommendation. Answered by number; a bare
number accepts the recommendation. **One round, not one at a time.** If the round would
exceed roughly fifteen cards, cut the least consequential and note them in the pack as open
questions instead.

## 7 · Write the pack

Copy `${CLAUDE_PLUGIN_ROOT}/templates/pack-skeleton/` to the output path, then fill:

- `manifest.yaml` — every element in schema.
- `layers/01..12.md` — generated from the manifest, one readable section per slot. This is
  what a human reads to decide whether to adopt anything; write prose, not YAML dumps.
- `bindings.yaml`, `profile.yaml`, `COVERAGE.md`.
- `mechanisms/` — one file per carried mechanism, tier in the header, bindings as
  `{placeholders}`.
- `PACK.md` — identity, summary, coverage at a glance, the standalone apply protocol from
  the skeleton, and the binding table inline.

Default output: the pack library, resolved by `tools/packs_dir.py` — `$HARNESS_PACKS`,
else a sibling `harness-packs/` clone, else a legacy in-repo `packs/`. Name it
`<project>-v<n>/`, `n` incrementing on re-extraction; a diff between two versions is a
legitimate way to see how a way of working has changed. If no pack library resolves, say
so and write to an explicit path rather than inventing one — a pack written somewhere
nobody will look is a pack that was not written.

## 8 · Verify before reporting

- Every element's `slot` exists in `SLOTS.md`.
- Every `U` statement is free of tool and domain names.
- Every binding referenced by a mechanism is declared in `bindings.yaml`.
- Every non-`project` provenance carries a quote.
- `PACK.md` stands alone: read it as if you had never seen this repo, and confirm you could
  apply the pack from it.

Report: coverage numbers, the layers that came out thin, the discrepancies found, and what
went in from the shelf. Do not report a pack as complete when its gap list is long — say
what is missing.
