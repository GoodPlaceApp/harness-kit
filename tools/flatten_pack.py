#!/usr/bin/env python3
"""Flatten a pack into ONE self-contained file you can send, paste or attach.

    python3 tools/flatten_pack.py <pack> [--brief] [-o out.md]

The directory is the working form — it is what `apply`, `merge` and `audit` read, and what
git diffs usefully. This is the *transport* form: a single file that still stands alone, for
handing to an agent in a project that has none of this installed.

  --full  (default)  everything an operation needs: statements, rationale, provenance,
                     bindings, checks, gaps, exclusions, rulings.
  --brief            statements and obligations only. Drops rationale, provenance, notes and
                     discrepancies. Roughly a third the size, and enough to APPLY — but not
                     enough to merge, audit or argue with, because the reasoning is gone.
"""
import sys, pathlib, argparse
import yaml

TIER = {"U": "universal", "S": "stack-conditional", "P": "project-bound"}


def flatten(pack: pathlib.Path, brief: bool) -> str:
    man = yaml.safe_load((pack / "manifest.yaml").read_text())
    L = [(pack / "PACK.md").read_text().rstrip(), "",
         "---", "", f"# Elements — {len(man['elements'])}", "",
         "*Flattened from the pack directory. "
         + ("Brief form: statements and obligations only — the reasoning, provenance and "
            "discrepancies are in the full pack. Enough to apply; not enough to merge or "
            "argue with.*" if brief else
            "Full form: this file alone is the pack.*"), ""]

    by_layer = {}
    for e in man["elements"]:
        by_layer.setdefault(e["layer"], []).append(e)

    for layer in sorted(by_layer):
        L += [f"## {layer}", ""]
        for e in by_layer[layer]:
            L += [f"### `{e['slot']}` — {e['title']}", ""]
            L += [e["statement"].strip(), ""]
            bits = [TIER[e["tier"]], f"applies: {e.get('applies_when', 'always')}"]
            if not brief:
                bits.append(f"evidence: {e['evidence']}")
            if e.get("bindings"):
                bits.append("binds " + ", ".join(f"`{b}`" for b in e["bindings"]))
            if e.get("check"):
                bits.append(f"check: `{e['check']}`")
            L += ["*" + " · ".join(bits) + "*", ""]
            if not brief:
                L += [f"**Why.** {e['rationale'].strip()}", ""]
                if e.get("notes"):
                    L += [f"> {e['notes'].strip()}", ""]

    for key, heading, render in (
        ("gaps", "Gaps — applicable and unanswered",
         lambda g: f"- **`{g['slot']}`** — {str(g.get('why','')).strip()}"),
        ("not_applicable", "Not applicable — excluded by profile",
         lambda n: f"- **`{n['slot']}`** — {n.get('why','')}"),
        ("not_covered_by_source", "Outside the source's subject",
         lambda c: f"- `{c['slot']}`"),
    ):
        if man.get(key):
            L += [f"## {heading}", ""] + [render(x) for x in man[key]] + [""]

    if not brief:
        for key, heading in (("rulings", "Rulings"), ("discrepancies", "Discrepancies"),
                             ("unhoused", "Unhoused — candidate new questions")):
            if man.get(key):
                L += [f"## {heading}", ""]
                for x in man[key]:
                    label = x.get("id") or x.get("candidate_question") or x.get("slot")
                    body = (x.get("finding") or x.get("answer") or x.get("practice")
                            or x.get("note") or "")
                    L += [f"**{label}** — {str(body).strip()}", ""]

        b = yaml.safe_load((pack / "bindings.yaml").read_text())["bindings"]
        L += ["## Bindings", "",
              "| binding | meaning | discover | default |", "|---|---|---|---|"]
        for x in b:
            L.append(f"| `{x['id']}` | {x.get('meaning','')} | "
                     f"{x.get('discover','—')} | `{x.get('default')}` |")
        L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pack")
    ap.add_argument("--brief", action="store_true")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    pack = pathlib.Path(a.pack).resolve()
    text = flatten(pack, a.brief)
    out = pathlib.Path(a.out) if a.out else pack.parent / (
        f"{pack.name}{'-brief' if a.brief else ''}.md")
    out.write_text(text)
    print(f"{out}  ·  {len(text) // 1024} KB  ·  ~{len(text) // 4:,} tokens")


if __name__ == "__main__":
    main()
