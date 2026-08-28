#!/usr/bin/env python3
"""Generate a pack's readable surfaces from its manifest.

`layers/*.md` and `COVERAGE.md` are GENERATED. Never hand-edit them — edit
`manifest.yaml` and re-run this. See format/PACK_SPEC.md.

    python3 tools/render_pack.py packs/<pack>/
"""
import sys, re, pathlib, collections

try:
    import yaml
except ImportError:
    sys.exit("needs pyyaml: pip install pyyaml")

LAYER_TITLES = {
    "01-charter": "Charter — why this exists and what is never traded",
    "02-method": "Method — how one change is made and verified",
    "03-governance": "Governance — how work is chosen, decided and recorded",
    "04-agents": "Agents — the cast, their limits, and what they are told",
    "05-workstate": "Workstate — the knowledge base agents and humans read",
    "06-toolchain": "Toolchain — what is installed and how it is wired",
    "07-run": "Run — what happens once it is live, and when it breaks",
    "08-trust": "Trust — security, supply chain and data",
    "09-economics": "Economics — what it costs to run and to build",
    "10-conventions": "Conventions — the surface craft",
    "11-product-loop": "Product loop — the path between users and the work list",
    "12-reflexivity": "Reflexivity — the process examining itself",
}
TIER_WORD = {"U": "universal", "S": "stack-conditional", "P": "project-bound"}


def slot_questions(fmt_dir):
    """slot id -> the question it asks, read from the vocabulary."""
    txt = (fmt_dir / "SLOTS.md").read_text()
    return dict(re.findall(r"^\| `([a-z0-9._-]+)` \| (.+?) \|", txt, re.M))


def slot_layers(fmt_dir):
    """slot id -> layer key, by walking the vocabulary's headings."""
    txt = (fmt_dir / "SLOTS.md").read_text()
    out, cur = {}, None
    for line in txt.splitlines():
        m = re.match(r"^## (\d\d) · ([^—]+?)\s+—", line)
        if m:
            cur = f"{m.group(1)}-{m.group(2).strip().lower().replace(' ', '-')}"
        m = re.match(r"^\| `([a-z0-9._-]+)` \|", line)
        if m and cur:
            out[m.group(1)] = cur
    return out


def render_layers(pack, man, questions):
    by_layer = collections.defaultdict(list)
    for e in man["elements"]:
        by_layer[e["layer"]].append(e)
    gaps = {g["slot"]: g for g in man.get("gaps", [])}
    nas = {n["slot"]: n for n in man.get("not_applicable", [])}

    outdir = pack / "layers"
    outdir.mkdir(exist_ok=True)
    for key, title in LAYER_TITLES.items():
        els = by_layer.get(key, [])
        L = [f"# {title}", ""]
        L.append(f"*Generated from `manifest.yaml` — do not hand-edit.* "
                 f"{len(els)} element{'s' if len(els) != 1 else ''} in this layer.")
        L.append("")
        for e in els:
            L.append(f"## {e['title']}")
            L.append("")
            L.append(f"**Answers** `{e['slot']}` — {questions.get(e['slot'], '?')}")
            L.append("")
            L.append(e["statement"].strip())
            L.append("")
            L.append(f"**Why.** {e['rationale'].strip()}")
            L.append("")
            bits = [f"`{TIER_WORD[e['tier']]}`", f"evidence `{e['evidence']}`"]
            if e.get("bindings"):
                bits.append("binds " + ", ".join(f"`{b}`" for b in e["bindings"]))
            if e.get("mechanisms"):
                bits.append(f"{len(e['mechanisms'])} mechanism"
                            f"{'s' if len(e['mechanisms']) != 1 else ''}")
            L.append(" · ".join(bits))
            L.append("")
            if e.get("notes"):
                L.append(f"> **Also worth knowing.** {e['notes'].strip()}")
                L.append("")
            L.append(f"<sub>Seen at {e['provenance']['path']}</sub>")
            L.append("")
            L.append("---")
            L.append("")
        # gaps and exclusions for this layer, so a reader sees the holes in place
        lg = [s for s in gaps if slot_layer_of(s, man) == key]
        ln = [s for s in nas if slot_layer_of(s, man) == key]
        if lg:
            L += ["## Gaps in this layer", ""]
            for s in lg:
                L += [f"**`{s}`** — {questions.get(s, '?')}", "",
                      gaps[s]["why"].strip(), ""]
        if ln:
            L += ["## Not applicable to the source", ""]
            for s in ln:
                L.append(f"- **`{s}`** — {nas[s]['why']}"
                         + ("  **(disputed)**" if nas[s].get("disputed") else ""))
            L.append("")
        (outdir / f"{key}.md").write_text("\n".join(L).rstrip() + "\n")
    return len(LAYER_TITLES)


_SLOT_LAYER_CACHE = {}


def slot_layer_of(slot, man):
    if not _SLOT_LAYER_CACHE:
        _SLOT_LAYER_CACHE.update(man["_slot_layers"])
    return _SLOT_LAYER_CACHE.get(slot)


def render_coverage(pack, man, questions):
    by_layer = collections.Counter(e["layer"] for e in man["elements"])
    gaps, nas = man.get("gaps", []), man.get("not_applicable", [])
    ncs = man.get("not_covered_by_source", [])
    gl = collections.Counter(slot_layer_of(g["slot"], man) for g in gaps)
    nl = collections.Counter(slot_layer_of(n["slot"], man) for n in nas)
    cl = collections.Counter(slot_layer_of(c["slot"], man) for c in ncs)

    total_app = len(man["elements"]) + len(gaps) + len(ncs)
    pct = round(100 * len(man["elements"]) / total_app)
    bar = "█" * round(pct / 5) + "░" * (20 - round(pct / 5))

    L = [f"# Coverage — {man['pack']} v{man['version']}", "",
         "*Generated from `manifest.yaml` — do not hand-edit.*", "",
         f"`{bar}`  **{len(man['elements'])} of {total_app} applicable slots "
         f"answered ({pct}%)**", "",
         f"{len(nas)} further slots do not apply to this source and are excluded "
         f"rather than counted against it. All {total_app + len(nas)} vocabulary "
         "slots are accounted for.", "",
         "| layer | answered | gaps | outside the source | not applicable |",
         "|---|---|---|---|---|"]
    for key, title in LAYER_TITLES.items():
        L.append(f"| {title.split(' — ')[0]} | {by_layer.get(key, 0)} "
                 f"| {gl.get(key, 0) or '—'} | {cl.get(key, 0) or '—'} "
                 f"| {nl.get(key, 0) or '—'} |")
    L += ["", "## Gaps", "",
          "Slots that apply to this source and have no answer. Each was checked, "
          "not assumed — an extraction that hides its holes is worth less than one "
          "that names them, because the holes are exactly what a later merge is for.", ""]
    for g in gaps:
        shelf = " · *a shelf default is available*" if g.get("shelf_available") else ""
        L += [f"### `{g['slot']}`{shelf}", "",
              f"*{questions.get(g['slot'], '?')}*", "", g["why"].strip(), ""]
    if ncs:
        L += ["## Outside the source's subject", "",
              f"{len(ncs)} slots this source simply does not address. **Not gaps in the "
              "source, and not excluded by profile** — questions this material does not "
              "answer. Merging with a pack that does answer them is precisely what this "
              "pack is for.", "",
              ", ".join(f"`{c['slot']}`" for c in ncs), ""]
    L += ["## Not applicable", "",
          "Excluded by this source's profile. These are **not** gaps, and they are "
          "re-evaluated against the *target's* profile at apply time — a target that "
          "does have users owes every slot marked here.", ""]
    for n in nas:
        d = "  **(disputed — see open question Q1)**" if n.get("disputed") else ""
        L.append(f"- **`{n['slot']}`** — {n['why']}{d}")
    shelf = [e for e in man["elements"]
             if (e.get("provenance") or {}).get("source") == "shelf"]
    L += ["", "## From the shelf", ""]
    if shelf:
        L += [f"{len(shelf)} element{'s' if len(shelf) != 1 else ''} did **not** come from "
              "the source. Each was offered against a confirmed gap and accepted "
              "individually, and each carries `provenance.source: shelf` so it can never be "
              "mistaken for observed practice.", ""]
        for e in shelf:
            L.append(f"- **`{e['slot']}`** — {e['title']} "
                     f"(`{e['evidence']}`, {e.get('corroboration', 0)} independent sources)")
        L.append("")
    else:
        L += ["None. Every element in this pack came from the source; no best-practice "
              "defaults were accepted.", ""]
    if man.get("discrepancies"):
        L += ["## Discrepancies found", "",
              "Places the source contradicts itself. Reported, never silently resolved — "
              "several are the reason an element's evidence level is what it is.", ""]
        for d in man["discrepancies"]:
            L += [f"**{d['id']}** ({d['severity']}) — {d['finding'].strip()}", ""]
    (pack / "COVERAGE.md").write_text("\n".join(L).rstrip() + "\n")


def main():
    pack = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    # The kit is found from this script's own location, so a pack may live anywhere —
    # in a sibling packs repo, in a target project, or on a scratch path.
    fmt = pathlib.Path(__file__).resolve().parent.parent / "format"
    man = yaml.safe_load((pack / "manifest.yaml").read_text())
    questions = slot_questions(fmt)
    man["_slot_layers"] = slot_layers(fmt)
    n = render_layers(pack, man, questions)
    render_coverage(pack, man, questions)
    print(f"rendered {n} layer files and COVERAGE.md into {pack.name}/")


if __name__ == "__main__":
    main()
