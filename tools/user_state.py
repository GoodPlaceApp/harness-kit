#!/usr/bin/env python3
"""Where a project's DURABLE state lives outside its repository.

A harness has a user-level half. Agent memory, per-project preferences and accumulated
working rules are kept beside the tool rather than inside the project, so an extraction that
reads only the repository misses them — and misses, in particular, the rules a human gave by
correcting the agent rather than by writing a document.

    python3 tools/user_state.py <repo-path>

READ ONLY the durable state. The same directory holds session transcripts: one file per
conversation, enormous, containing every keystroke of every session including anything
pasted into them. They are not harness content, they are a privacy surface, and reading them
would flood any context they entered. `readable()` returns the safe subset and nothing else.
"""
import sys, pathlib

TRANSCRIPT_SUFFIXES = {".jsonl"}
DURABLE = ("memory",)          # widen only with a reason; default to excluding


def state_dir(repo: pathlib.Path) -> pathlib.Path | None:
    """The user-level state directory for a repo, or None if it has none yet."""
    slug = str(pathlib.Path(repo).resolve()).replace("/", "-")
    d = pathlib.Path.home() / ".claude" / "projects" / slug
    return d if d.is_dir() else None


def readable(repo: pathlib.Path) -> list[pathlib.Path]:
    """Durable files only. Never a transcript, never a session directory."""
    d = state_dir(repo)
    if d is None:
        return []
    out = []
    for name in DURABLE:
        sub = d / name
        if sub.is_dir():
            out += [f for f in sorted(sub.rglob("*"))
                    if f.is_file() and f.suffix not in TRANSCRIPT_SUFFIXES]
    return out


def excluded_count(repo: pathlib.Path) -> int:
    """How much was deliberately not read — worth stating in the extraction report."""
    d = state_dir(repo)
    return 0 if d is None else len([f for f in d.iterdir()
                                    if f.suffix in TRANSCRIPT_SUFFIXES])


if __name__ == "__main__":
    r = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    d = state_dir(r)
    print(f"state dir : {d or 'none — this project has no user-level state'}")
    if d:
        files = readable(r)
        print(f"readable  : {len(files)} durable file(s)")
        for f in files[:6]:
            print(f"            {f.relative_to(d)}")
        if len(files) > 6:
            print(f"            … and {len(files) - 6} more")
        print(f"excluded  : {excluded_count(r)} session transcripts — never read")
