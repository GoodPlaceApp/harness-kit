# The shelf

Defensible defaults, one file per slot, offered when a source leaves that slot empty.

Shelf content is **never** disguised as source practice. An accepted shelf default enters a
pack with `provenance.source: shelf` and its own evidence level, and appears in
`COVERAGE.md` under a heading that says it did not come from the project. That separation is
the whole point: a pack must let you tell what you actually do from what a tool thinks you
should do.

Shelf entries are offered per gap, accept-or-decline individually. Declining is normal.
An empty slot with a name is more useful than a borrowed answer nobody follows.

`universal/` — defaults that hold regardless of stack.
`stacks/<stack>/` — recipes for `S`-tier mechanisms, one directory per stack.
`canon/` — ingest recipes for well-known corpora, so a canon reads into slots cleanly.

The shelf is itself just a curated theory pack, maintained the same way — built by
`/harness-ingest` over the canon, and subject to the same citation discipline. An entry
without a source is not a default, it is an opinion.
