"""The portability claim, pinned.

A pack extracted from a Python/systemd project must not install Python or systemd
assumptions into a Gradle mobile repo. That property is the reason the tiers exist, and
this is where it is enforced rather than asserted.
"""
import sys, pathlib
import pytest, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from packs_dir import packs as _discover_packs      # noqa: E402
import apply_plan                                    # noqa: E402

PACKS = _discover_packs()
FIXTURE = ROOT / "tests" / "fixtures" / "profile-gradle-mobile.yaml"

pytestmark = pytest.mark.skipif(
    not PACKS, reason="no pack library found — see tools/packs_dir.py")


@pytest.fixture(scope="module")
def plan():
    pack = PACKS[0]
    profile = yaml.safe_load(FIXTURE.read_text())
    man = yaml.safe_load((pack / "manifest.yaml").read_text())
    out = []
    for e in man["elements"]:
        if not apply_plan.applies(e.get("applies_when"), profile):
            out.append(("SKIP", e, None)); continue
        if e["tier"] == "P":
            out.append(("STUB", e, None)); continue
        mechs = e.get("mechanisms") or []
        unmatched = [m for m in mechs
                     if not apply_plan.recipe_matches(
                         apply_plan.recipe_of(pack, m), profile["stack"])]
        if e["tier"] == "S" and mechs and len(unmatched) == len(mechs):
            out.append(("DEFER", e, unmatched))
        elif unmatched:
            out.append(("PARTIAL", e, unmatched))
        else:
            out.append(("APPLY", e, None))
    return pack, out


def test_no_foreign_stack_recipe_is_ever_planned_for_this_target(plan):
    """THE acid test. A pytest selector in a Gradle repo is worse than nothing,
    because it looks done."""
    pack, rows = plan
    stack = yaml.safe_load(FIXTURE.read_text())["stack"]
    leaked = []
    for status, e, _ in rows:
        if status not in ("APPLY", "PARTIAL"):
            continue
        for m in (e.get("mechanisms") or []):
            r = apply_plan.recipe_of(pack, m)
            if r and not apply_plan.recipe_matches(r, stack):
                if status == "APPLY":
                    leaked.append((e["slot"], r))
    assert not leaked, f"foreign-stack recipes planned for install: {leaked}"


def test_inapplicable_layers_are_skipped_not_installed(plan):
    """No production means no error budget, no runbooks, no deploy gesture."""
    _, rows = plan
    status = {e["slot"]: s for s, e, _ in rows}
    for slot in ("run.alerting", "run.backup-restore", "run.degradation",
                 "tool.ship", "econ.budget", "method.rollback"):
        assert status.get(slot) == "SKIP", (
            f"{slot} should be skipped for a target with no production/spend, "
            f"got {status.get(slot)}")


def test_the_portable_core_still_lands(plan):
    """Skipping must not be so aggressive that nothing useful transfers."""
    _, rows = plan
    status = {e["slot"]: s for s, e, _ in rows}
    for slot in ("work.doc-tree", "work.one-home", "work.index",
                 "gov.decision-record", "agents.review-of-agents", "method.done"):
        assert status.get(slot) == "APPLY", (
            f"{slot} is universal and must transfer, got {status.get(slot)}")
    applied = sum(1 for s, _, _ in rows if s == "APPLY")
    assert applied >= 60, f"only {applied} elements would transfer — tiers are too strict"


def test_project_bound_elements_become_stubs_not_installs(plan):
    _, rows = plan
    for status, e, _ in rows:
        if e["tier"] == "P" and status not in ("STUB", "SKIP"):
            pytest.fail(f"{e['slot']} is project-bound and must stub, got {status}")
