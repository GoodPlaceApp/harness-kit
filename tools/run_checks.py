#!/usr/bin/env python3
"""Run a pack's conformance checks against a repository.

    python3 tools/run_checks.py <pack> <repo>

This is the mechanical half of `/harness-audit`. Audit proper reads `.harness/pack.lock` to
know what was applied and what was deliberately declined; this runs every check a pack
carries against a target that may never have applied it, which answers a different and still
useful question: how much of this way of working does that repository already satisfy?

A check is a shell predicate. Unresolvable bindings are not guessed — the check is reported
`skipped`, because a check run with a wrong path is worse than one not run.
"""
import subprocess, sys, pathlib, re, collections
import yaml

PLACEHOLDER = re.compile(r"\{([a-z_]+)\}")


def bindings_for(pack: pathlib.Path) -> dict:
    f = pack / "bindings.yaml"
    if not f.exists():
        return {}
    out = {}
    for b in yaml.safe_load(f.read_text())["bindings"]:
        d = b.get("default")
        if d not in (None, "null"):
            out[b["id"]] = str(d)
    # defaults may reference each other
    for _ in range(3):
        for k, v in list(out.items()):
            out[k] = PLACEHOLDER.sub(lambda m: out.get(m.group(1), m.group(0)), v)
    return out


def main():
    pack = pathlib.Path(sys.argv[1]).resolve()
    repo = pathlib.Path(sys.argv[2]).resolve()
    man = yaml.safe_load((pack / "manifest.yaml").read_text())
    binds = bindings_for(pack)

    res = collections.Counter()
    fails, skips = [], []
    for e in man["elements"]:
        chk = e.get("check")
        if not chk:
            res["no check"] += 1
            continue
        missing = [m for m in PLACEHOLDER.findall(chk) if m not in binds]
        if missing:
            res["skipped"] += 1
            skips.append((e["slot"], missing))
            continue
        cmd = PLACEHOLDER.sub(lambda m: binds[m.group(1)], chk)
        try:
            ok = subprocess.run(cmd, shell=True, cwd=repo, capture_output=True,
                                timeout=20).returncode == 0
        except subprocess.TimeoutExpired:
            ok = False
        res["satisfied" if ok else "not satisfied"] += 1
        if not ok:
            fails.append((e["layer"], e["slot"], e["title"]))

    total = sum(res.values())
    checked = res["satisfied"] + res["not satisfied"]
    print(f"\nCHECKS · {man['pack']} v{man['version']} → {repo.name}")
    print(f"  {total} elements · {checked} checked · {res['no check']} carry no check "
          f"· {res['skipped']} skipped for unresolved bindings")
    if checked:
        print(f"  satisfied {res['satisfied']}/{checked} "
              f"({round(100 * res['satisfied'] / checked)}%)\n")
    if fails:
        print("  NOT SATISFIED")
        for layer, slot, title in sorted(fails):
            print(f"    {layer[:2]} {slot:<28} {title[:56]}")
    if skips:
        print(f"\n  skipped — unresolved bindings ({len(skips)})")
        for slot, m in skips[:8]:
            print(f"    {slot:<28} needs {', '.join(m)}")
    print("\n  A check is a cheap observable, not a proof. Not-satisfied means the signature "
          "is absent,\n  which may equally mean the practice is held somewhere this check "
          "does not look.")


if __name__ == "__main__":
    main()
