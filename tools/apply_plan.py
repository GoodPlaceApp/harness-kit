#!/usr/bin/env python3
"""Produce the plan diff `apply` shows before it writes anything.

    python3 tools/apply_plan.py <pack> <target-profile.yaml>

Decides, per element and mechanically: does it apply to this target at all, does its
tier survive the move, and does any recipe match this stack. Writing nothing is the
point — apply must be inspectable before it touches a repo.
"""
import sys, re, pathlib, collections
import yaml

KIT = pathlib.Path(__file__).resolve().parent.parent


def applies(pred, profile):
    """`always`, or an OR over the target's applicability facts."""
    if not pred or pred == "always":
        return True
    return any(profile["applies"].get(p.strip()) for p in str(pred).split(","))


def bindings_needed(pack, elements, stack):
    """The COMPLETE interview list: bindings named by applying elements, plus every
    placeholder inside the mechanism templates those elements will instantiate. The dummy
    apply run proved the second half matters — 18 declared bindings surfaced only at write
    time, as broken markers in written files, because the plan never asked about them."""
    import re
    need = set()
    for e in elements:
        need |= set(e.get("bindings") or [])
        for m in (e.get("mechanisms") or []):
            f = pack / m
            if not f.exists() or not f.name.endswith(".tmpl"):
                continue
            if not recipe_matches(recipe_of(pack, m), stack):
                continue
            need |= set(re.findall(r"\{([a-z_]+)\}", f.read_text(errors="ignore")))
    return sorted(need)


def recipe_of(pack, mech_path):
    p = pack / mech_path
    if not p.exists():
        return None
    m = re.search(r"recipe:\s*([a-z0-9/_-]+)", p.read_text()[:900])
    return m.group(1) if m else None


def recipe_matches(recipe, stack):
    """A recipe transfers only if this target actually runs that thing."""
    if recipe is None:
        return True                      # no recipe declared: portable as written
    langs = {str(x).lower() for x in (stack.get("languages") or [])}
    langs |= {str(stack.get(k) or "").lower()
              for k in ("build", "test_runner", "ci", "package_managers")}
    head = recipe.split("/")[0].lower()
    if head in ("javascript", "js") and ({"javascript", "typescript"} & langs):
        return True
    if head == "posix-shell":            # any unix target that actually deploys
        return bool(stack.get("deploy_target") not in (None, "none", "app-store"))
    return head in langs or recipe.lower() in langs


def main():
    pack = pathlib.Path(sys.argv[1]).resolve()
    profile = yaml.safe_load(pathlib.Path(sys.argv[2]).read_text())
    man = yaml.safe_load((pack / "manifest.yaml").read_text())
    stack = profile["stack"]

    rows, counts = [], collections.Counter()
    for e in man["elements"]:
        if not applies(e.get("applies_when"), profile):
            rows.append(("SKIP", e, "not applicable to this target")); counts["SKIP"] += 1
            continue
        if e["tier"] == "P":
            rows.append(("STUB", e, "project-bound — target must author its own"))
            counts["STUB"] += 1
            continue
        mechs = e.get("mechanisms") or []
        unmatched = [m for m in mechs if not recipe_matches(recipe_of(pack, m), stack)]
        if e["tier"] == "S" and mechs and len(unmatched) == len(mechs):
            why = f"no recipe for this stack ({', '.join(recipe_of(pack, m) or '—' for m in mechs)})"
            rows.append(("DEFER", e, why)); counts["DEFER"] += 1
        elif unmatched:
            rows.append(("PARTIAL", e, f"contract applies; {len(unmatched)} mechanism(s) deferred"))
            counts["PARTIAL"] += 1
        else:
            rows.append(("APPLY", e, "")); counts["APPLY"] += 1

    name = profile.get("name", pack.name)
    print(f"\nPLAN · {man['pack']} v{man['version']} → {name}")
    print(f"  stack   {', '.join(stack.get('languages') or ['?'])} · "
          f"{stack.get('build')} · tests {stack.get('test_runner')} · "
          f"ci {stack.get('ci')} · ui {stack.get('ui_surface')}")
    on = [k for k, v in profile["applies"].items() if v]
    print(f"  applies {', '.join(on) or 'nothing'}\n")
    for status in ("APPLY", "PARTIAL", "DEFER", "STUB", "SKIP"):
        sel = [r for r in rows if r[0] == status]
        if not sel:
            continue
        print(f"  {status}  ({len(sel)})")
        for _, e, why in sel[:60]:
            print(f"    {e['slot']:<34} {e['tier']}  {why}")
        print()
    total = sum(counts.values())
    owed = counts["DEFER"] + counts["STUB"] + counts["PARTIAL"]
    print(f"  {counts['APPLY']} applied · {owed} owed by the target · "
          f"{counts['SKIP']} not applicable · {total} elements considered")
    applying = [e for st, e, _ in rows if st in ("APPLY", "PARTIAL")]
    need = bindings_needed(pack, applying, stack)
    print(f"  interview: {len(need)} bindings to resolve before writing "
          f"(elements and their templates)")
    if counts["SKIP"]:
        print("  (skipped elements are excluded by profile, not failures)")


if __name__ == "__main__":
    main()
