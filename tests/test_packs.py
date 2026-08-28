"""Every pack in packs/ must satisfy the format, or it is not portable."""
import re, sys, pathlib, collections
import pytest, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from packs_dir import packs as _discover_packs  # noqa: E402

PACKS = _discover_packs()
TIERS = {"U", "S", "P"}
EVIDENCE = {"production", "documented", "claimed", "derived"}
SOURCES = {"project", "document", "web", "research", "shelf"}

# A universal statement claims to hold for a Kotlin mobile app and a Go service at once.
# Naming any of these means it does not, and the tier is a lie.
STACK_WORDS = re.compile(
    # `cargo` is deliberately absent: it collides with the English noun ("manual cargo").
    # `rust` still catches a Rust reference, so the class is covered without the false alarm.
    r"\b(pytest|vitest|jest|gradle|maven|npm|pip|poetry|python|javascript|"
    r"typescript|kotlin|swift|rust|golang|django|flask|fastapi|react|vue|vite|webpack|"
    r"sqlite|postgres|mysql|redis|systemd|nginx|github|gitlab|jenkins|docker|"
    r"kubernetes|eslint|ruff|black|prettier|mypy|pyright|terraform)\b", re.I)


def _vocab():
    txt = (ROOT / "format" / "SLOTS.md").read_text()
    return set(re.findall(r"^\| `([a-z0-9._-]+)` \|", txt, re.M))


pytestmark = pytest.mark.skipif(
    not PACKS,
    reason="no pack library found — set HARNESS_PACKS or clone harness-packs "
           "as a sibling of this repo. The kit is usable and testable without one.")


@pytest.fixture(scope="session", params=PACKS or [None], ids=lambda p: p.name if p else "none")
def pack(request):
    p = request.param
    return p, yaml.safe_load((p / "manifest.yaml").read_text())


def test_every_slot_exists_in_the_vocabulary(pack):
    path, man = pack
    vocab = _vocab()
    bad = {e["slot"] for e in man["elements"]} - vocab
    bad |= {g["slot"] for g in man.get("gaps", [])} - vocab
    bad |= {n["slot"] for n in man.get("not_applicable", [])} - vocab
    assert not bad, f"{path.name}: slots not in the vocabulary: {sorted(bad)}"


def test_one_element_per_slot(pack):
    """Two elements in one slot means a discrepancy was silently kept as both."""
    path, man = pack
    dupes = [s for s, n in collections.Counter(
        e["slot"] for e in man["elements"]).items() if n > 1]
    assert not dupes, f"{path.name}: more than one element answers: {dupes}"


def test_every_vocabulary_slot_is_accounted_for(pack):
    """Answered, a named gap, or excluded by profile. Silence is not an option."""
    path, man = pack
    seen = ({e["slot"] for e in man["elements"]}
            | {g["slot"] for g in man.get("gaps", [])}
            | {c["slot"] for c in man.get("not_covered_by_source", [])}
            | {n["slot"] for n in man.get("not_applicable", [])})
    missing = _vocab() - seen
    assert not missing, (
        f"{path.name}: {len(missing)} slots neither answered, nor named as a gap, nor "
        f"marked outside the source, nor excluded: {sorted(missing)[:8]}")


def test_element_required_fields(pack):
    path, man = pack
    for e in man["elements"]:
        for f in ("id", "slot", "layer", "title", "statement", "rationale",
                  "tier", "evidence", "provenance"):
            assert e.get(f), f"{path.name}/{e.get('id')}: missing {f}"
        assert e["tier"] in TIERS, f"{e['id']}: bad tier {e['tier']}"
        assert e["evidence"] in EVIDENCE, f"{e['id']}: bad evidence {e['evidence']}"
        for entry in _prov(e):
            assert entry.get("source") in SOURCES, \
                f"{e['id']}: bad provenance source {entry.get('source')!r}"


def test_universal_statements_name_no_tool_or_language(pack):
    """The stack-neutrality guarantee, enforced rather than asserted."""
    path, man = pack
    leaks = [(e["id"], sorted(set(STACK_WORDS.findall(e["statement"]))))
             for e in man["elements"]
             if e["tier"] == "U" and STACK_WORDS.search(e["statement"])]
    assert not leaks, (
        f"{path.name}: universal-tier statements naming a tool or language — "
        f"demote to S and move the name into a recipe: {leaks}")


def test_non_project_provenance_carries_a_quote(pack):
    """An element that cannot quote its origin is not `documented`, it is `derived`."""
    path, man = pack
    bad = [e["id"] for e in man["elements"]
           if e["evidence"] != "derived"
           and any(x.get("source") not in ("project", None) and not x.get("quote")
                   and not x.get("path") for x in _prov(e))]
    assert not bad, f"{path.name}: non-project origins with neither quote nor path: {bad}"


def test_ingested_elements_never_claim_production(pack):
    """Reading about a practice is not observing it run."""
    path, man = pack
    bad = [e["id"] for e in man["elements"]
           if e["evidence"] == "production"
           and all(x.get("source") != "project" for x in _prov(e))]
    assert not bad, (
        f"{path.name}: elements claiming production with no project origin: {bad}")


def test_every_binding_used_is_declared_and_every_declared_binding_used(pack):
    path, man = pack
    declared = {b["id"] for b in
                yaml.safe_load((path / "bindings.yaml").read_text())["bindings"]}
    used = set()
    for e in man["elements"]:
        used |= set(e.get("bindings") or [])
        for f in ("check", "statement", "notes"):
            used |= set(re.findall(r"\{([a-z_]+)\}", str(e.get(f) or "")))
    used.discard("FEATURE")
    assert not (used - declared), f"{path.name}: undeclared bindings: {sorted(used - declared)}"
    assert not (declared - used), f"{path.name}: unused bindings: {sorted(declared - used)}"


def test_every_binding_can_be_resolved_without_asking_or_is_marked_required(pack):
    """A binding with neither a discovery procedure nor a default is a silent failure."""
    path, _ = pack
    for b in yaml.safe_load((path / "bindings.yaml").read_text())["bindings"]:
        assert b.get("discover") or b.get("default") is not None or b.get("required"), (
            f"{path.name}/{b['id']}: no discover, no default, not marked required")


def test_referenced_mechanism_files_exist(pack):
    path, man = pack
    missing = [(e["id"], m) for e in man["elements"]
               for m in (e.get("mechanisms") or []) if not (path / m).exists()]
    assert not missing, f"{path.name}: mechanisms referenced but absent: {missing}"


def test_pack_md_stands_alone(pack):
    """PACK.md must let a bare agent apply the pack with no tooling installed."""
    path, _ = pack
    txt = (path / "PACK.md").read_text().lower()
    for phrase in ("without any tooling", "applies_when", "bindings.yaml",
                   "never delete", "deferred"):
        assert phrase in txt, f"{path.name}/PACK.md omits the apply protocol's '{phrase}'"


def test_layers_and_coverage_are_in_sync_with_the_manifest(pack, tmp_path):
    """`layers/` and COVERAGE.md are generated. A hand-edit is a defect, not a change."""
    import shutil, subprocess, filecmp
    path, _ = pack
    staged = tmp_path / path.name
    shutil.copytree(path, staged)
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "render_pack.py"), str(staged)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    drifted = [f.name for f in (path / "layers").glob("*.md")
               if not filecmp.cmp(f, staged / "layers" / f.name, shallow=False)]
    if not filecmp.cmp(path / "COVERAGE.md", staged / "COVERAGE.md", shallow=False):
        drifted.append("COVERAGE.md")
    assert not drifted, (
        f"{path.name}: hand-edited or stale generated files — re-run "
        f"tools/render_pack.py: {drifted}")


def _prov(e):
    """Provenance entries, whether the element carries one mapping or a fused list."""
    p = e.get("provenance")
    return p if isinstance(p, list) else [p or {}]


def _origins(e):
    """Named independent origins, whether provenance is a single mapping or a list."""
    p = e.get("provenance")
    if isinstance(p, list):
        return len(p)
    ref = str((p or {}).get("ref") or "")
    parts = [x.strip() for x in re.split(r"[;]| \+ ", ref) if x.strip()]
    return len({re.split(r"[,—]", x)[0].strip().lower()[:22] for x in parts}) or 1


def test_corroboration_never_exceeds_the_origins_named(pack):
    """Tracking independence is pointless if a count can exceed the sources behind it.
    A fused element must list its origins so the NEXT merge can check them mechanically —
    prose in notes is unreadable to a tool."""
    path, man = pack
    over = [(e["slot"], e.get("corroboration"), _origins(e))
            for e in man["elements"] if e.get("corroboration", 1) > _origins(e)]
    assert not over, (
        f"{path.name}: elements claiming more independent sources than they name "
        f"(slot, claimed, named): {over}")
