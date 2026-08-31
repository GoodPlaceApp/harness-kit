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
from __future__ import annotations   # PEP 604 unions below; stock macOS python3 is 3.9

import re, sys, pathlib

TRANSCRIPT_SUFFIXES = {".jsonl"}
DURABLE = ("memory",)          # widen only with a reason; default to excluding
MAX_REFERENCED = 40            # a note that names a hundred paths is not naming a plan
_PATH = re.compile(r"(?:\(|\s|^)((?:~|\.{0,2}/)[A-Za-z0-9._~/-]{6,120})")


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


def referenced(repo: pathlib.Path) -> list[pathlib.Path]:
    """Files a durable note names by path, and that exist.

    Plans, briefs and working documents live outside the note store — for this tool's own
    host, in a directory shared by EVERY project, which is exactly why the store is not
    simply widened to include it. Reading that directory wholesale would pull one project's
    planning into another project's pack. Following a reference is narrow: a note in THIS
    project's store named this file, so this file is about this project.

    Bounded deliberately: never a transcript, never outside the repository or the tool's own
    configuration directory, and capped.
    """
    roots = [pathlib.Path(repo).resolve(), (pathlib.Path.home() / ".claude").resolve()]
    out, seen = [], set()
    for note in readable(repo):
        for m in _PATH.finditer(note.read_text(errors="ignore")):
            raw = m.group(1)
            cand = pathlib.Path(raw.replace("~", str(pathlib.Path.home()), 1)) if raw.startswith("~") \
                else (pathlib.Path(repo) / raw.lstrip("./"))
            try:
                cand = cand.resolve()
            except OSError:
                continue
            if cand in seen or not cand.is_file():
                continue
            if cand.suffix in TRANSCRIPT_SUFFIXES:
                continue
            if not any(str(cand).startswith(str(r)) for r in roots):
                continue
            seen.add(cand)
            out.append(cand)
            if len(out) >= MAX_REFERENCED:
                return out
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
        ref = referenced(r)
        print(f"referenced: {len(ref)} file(s) named by a note and existing")
        for f in ref[:6]:
            print(f"            {f}")
        print(f"excluded  : {excluded_count(r)} session transcripts — never read")
