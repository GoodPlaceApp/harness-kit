"""Where packs live, resolved the same way everywhere.

Packs are DATA and live outside the kit; the kit is the TOOL. Resolution order,
first hit wins:

  1. $HARNESS_PACKS                     — explicit, wins everything
  2. ~/.harness/packs                   — the default, and outside every repository
  3. <kit>/../harness-packs             — the sibling-clone convention
  4. <kit>/packs                        — legacy, WARNED AGAINST: see below

Returns None when no pack library is present, which is a normal state: the kit is fully
usable and fully testable without one.

Why the in-kit location is discouraged. This kit is a public repository. A pack records how
a real project is actually worked on — host and service names, spend ceilings, and the
discrepancies and open findings an extraction turned up — so a pack sitting inside a
checkout of a public repo is one absent-minded push, or one fork, away from being published.
The default lives at ~/.harness/packs precisely because it is inside no repository at all;
run `git init` there if you want history and a private remote.
"""
import os, pathlib

KIT = pathlib.Path(__file__).resolve().parent.parent


def packs_dir():
    env = os.environ.get("HARNESS_PACKS")
    if env:
        p = pathlib.Path(env).expanduser().resolve()
        return p if p.is_dir() else None
    cands = [pathlib.Path.home() / ".harness" / "packs",
             KIT.parent / "harness-packs",
             KIT / "packs"]
    # Prefer a location that actually holds packs. A freshly created, still-empty default
    # must not shadow a library that exists elsewhere — otherwise installing the kit
    # silently hides the packs the user already had.
    for cand in cands:
        if cand.is_dir() and any((c / "manifest.yaml").exists() for c in cand.iterdir()):
            return cand
    for cand in cands:
        if cand.is_dir():
            return cand
    return None


def warn_if_inside_the_kit(d):
    """A pack library inside this repository is a leak waiting to happen."""
    try:
        d.relative_to(KIT)
    except (ValueError, AttributeError):
        return None
    return (f"WARNING: pack library at {d} sits inside the kit, which is a public "
            f"repository. Move it to ~/.harness/packs — outside every repo — before you "
            f"extract anything you would not publish.")


def packs():
    d = packs_dir()
    if d is None:
        return []
    return sorted(p for p in d.iterdir() if (p / "manifest.yaml").exists())
