from pathlib import Path
import importlib.util
import subprocess
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_shaft_and_groove_require_explicit_revolution_axis_pattern():
    capability = yaml.safe_load((ROOT / "manifests" / "capability_manifest.yaml").read_text(encoding="utf-8"))
    partdesign = capability["capabilities"]["partdesign"]

    for feature_name in ["shaft", "groove"]:
        feature = partdesign[feature_name]
        assert feature["status"] == "live_verified_once"
        assert feature["classification"] == "NATIVE_SUCCESS"
        assert "partdesign.sketch_revolution_axis" in feature["reference_pattern_ids"]
        assert feature["user_mode"] == "imported_call_pattern_only"
        assert feature["imported_recipe_ids"]


def test_reference_manifest_contains_sketch_revolution_axis_pattern():
    manifest = yaml.safe_load((ROOT / "manifests" / "reference_manifest.yaml").read_text(encoding="utf-8"))
    pattern = next(item for item in manifest["reference_patterns"] if item["id"] == "partdesign.sketch_revolution_axis")

    assert pattern["applies_to"] == ["shaft", "groove"]
    assert pattern["reference_doc"] == "references/partdesign/sketch_revolution_axis.md"
    assert (ROOT / pattern["reference_doc"]).exists()
    reference_doc = (ROOT / pattern["reference_doc"]).read_text(encoding="utf-8")
    assert "CenterLine" in reference_doc


def test_skill_mentions_reference_selection_before_fresh_code():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "reference selection" in skill.lower()
    assert "partdesign.sketch_revolution_axis" in skill
    assert "Shaft" in skill and "Groove" in skill


def test_search_finds_reference_pattern_without_runner():
    path = ROOT / "cli" / "search_recipe.py"
    spec = importlib.util.spec_from_file_location("search_recipe", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    results = module.search("shaft")

    assert any(item["kind"] == "reference_pattern" for item in results)
    pattern = next(item for item in results if item["id"] == "partdesign.sketch_revolution_axis")
    assert pattern["runner"] is None


def test_search_cli_labels_imported_call_patterns():
    result = subprocess.run(
        [sys.executable, "cli/search_recipe.py", "shaft"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "partdesign.regression.t11_shaft_with_sketch_centerline" in result.stdout
    assert "imported call pattern" in result.stdout
    assert "-> None" not in result.stdout
