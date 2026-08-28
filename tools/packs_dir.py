"""Where packs live, resolved the same way everywhere.

Packs are DATA and live in their own repository; the kit is the TOOL. Resolution order,
first hit wins:

  1. $HARNESS_PACKS                     — explicit, wins everything
  2. <kit>/../harness-packs             — the sibling-clone convention
  3. <kit>/packs                        — legacy in-repo layout, still honoured

Returns None when no pack library is present, which is a normal state: the kit is fully
usable and fully testable without one.
"""
import os, pathlib

KIT = pathlib.Path(__file__).resolve().parent.parent


def packs_dir():
    env = os.environ.get("HARNESS_PACKS")
    if env:
        p = pathlib.Path(env).expanduser().resolve()
        return p if p.is_dir() else None
    for cand in (KIT.parent / "harness-packs", KIT / "packs"):
        if cand.is_dir():
            return cand
    return None


def packs():
    d = packs_dir()
    if d is None:
        return []
    return sorted(p for p in d.iterdir() if (p / "manifest.yaml").exists())
