"""The vocabulary is the backbone — if it is malformed, every pack silently is too."""
import re, pathlib, collections
import pytest, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
FMT = ROOT / "format"
PREDICATES = {
    "always", "has-agents", "has-production", "has-users", "handles-user-data",
    "has-ui", "is-public", "has-deps", "has-schema", "is-multi-env", "costs-money",
    "profile",
}
SLOT_ROW = re.compile(r"^\| `([a-z0-9._-]+)` \| (.+?) \| (.+?) \|\s*$", re.M)


@pytest.fixture(scope="session")
def vocab():
    return SLOT_ROW.findall((FMT / "SLOTS.md").read_text())


def test_every_slot_id_is_unique(vocab):
    ids = [s for s, _, _ in vocab]
    dupes = [s for s, n in collections.Counter(ids).items() if n > 1]
    assert not dupes, f"slot ids must be unique — merge and audit key on them: {dupes}"


def test_every_slot_asks_a_question(vocab):
    """A slot states a question. A slot that states an answer has prejudged the target."""
    bad = [s for s, q, _ in vocab if not q.strip().endswith("?")]
    assert not bad, f"slots must be phrased as questions: {bad}"


def test_every_applicability_predicate_is_known(vocab):
    used = set()
    for _, _, applies in vocab:
        used |= {p.strip() for p in applies.split(",")}
    assert used <= PREDICATES, f"unknown predicate(s): {sorted(used - PREDICATES)}"


def test_slot_id_prefix_matches_its_layer():
    """`gov.wip` must live under Governance. A misfiled slot breaks layer rendering."""
    txt = (FMT / "SLOTS.md").read_text()
    cur, wrong = None, []
    for line in txt.splitlines():
        m = re.match(r"^## \d\d · ([^—]+?)\s+—", line)
        if m:
            cur = m.group(1).strip().lower()
        m = re.match(r"^\| `([a-z0-9._-]+)\.", line)
        if m and cur:
            prefix = m.group(1)
            # the prefix is an abbreviation of the layer name, not necessarily equal
            if not (cur.startswith(prefix[:3]) or prefix[:3] in cur.replace(" ", "")):
                wrong.append((prefix, cur))
    assert not wrong, f"slot prefix does not match its layer: {set(wrong)}"


def test_no_slot_question_names_a_tool(vocab):
    """The whole format rests on questions being stack-neutral."""
    banned = re.compile(
        r"\b(pytest|vitest|jest|gradle|maven|cargo|npm|pip|poetry|python|javascript|"
        r"typescript|kotlin|swift|rust|golang|django|react|vite|sqlite|postgres|"
        r"systemd|github|gitlab|docker|kubernetes|eslint|ruff|prettier)\b", re.I)
    leaks = [(s, banned.findall(q)) for s, q, _ in vocab if banned.search(q)]
    assert not leaks, f"slot questions must name no tool or language: {leaks}"


def test_the_format_docs_all_exist():
    for f in ("SLOTS.md", "PACK_SPEC.md", "PROFILES.md", "MERGE_RULES.md"):
        assert (FMT / f).exists(), f"format/{f} is missing"


def _shelf_files():
    return sorted((ROOT / "shelf" / "universal").glob("*.md"))


def test_every_shelf_entry_names_a_real_slot(vocab):
    ids = {s for s, _, _ in vocab}
    bad = [f.name for f in _shelf_files() if f.stem not in ids]
    assert not bad, f"shelf entries whose filename is not a slot id: {bad}"


def test_no_shelf_entry_claims_production_evidence():
    """The shelf offers advice. Advice has not been observed running HERE."""
    bad = [f.name for f in _shelf_files() if "evidence: production" in f.read_text()]
    assert not bad, (
        f"shelf entries claiming production evidence — a practice on the shelf is "
        f"`documented` at best, because one project running it is not evidence it "
        f"generalises: {bad}")


def test_every_shelf_entry_cites_its_sources():
    """An entry without a source is not a default, it is an opinion."""
    bad = [f.name for f in _shelf_files()
           if "**Sources**" not in f.read_text() and "derived_from" not in f.read_text()]
    assert not bad, f"shelf entries with no sources section: {bad}"


def test_the_five_operations_and_promote_all_exist():
    for op in ("extract", "ingest", "apply", "merge", "audit", "promote"):
        assert (ROOT / "skills" / f"harness-{op}" / "SKILL.md").exists(), \
            f"skills/harness-{op}/SKILL.md is missing"
