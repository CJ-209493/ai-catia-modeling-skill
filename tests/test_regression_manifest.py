from pathlib import Path
import re

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_regression_manifest_indexes_all_30_boundary_cases():
    manifest = yaml.safe_load((ROOT / "manifests" / "regression_manifest.yaml").read_text(encoding="utf-8"))

    assert manifest["source_run"] == "catia_recipe_regression_20260706_232109"
    assert manifest["live_verified_at"] == "2026-07-06T23:21:09"
    assert manifest["total_tests"] == 30
    assert len(manifest["entries"]) == 30
    assert manifest["classification_counts"] == {
        "NATIVE_SUCCESS": 16,
        "PARTIAL_SUCCESS": 2,
        "UNSUPPORTED": 11,
        "HONEST_FAILURE": 1,
    }


def test_regression_manifest_points_to_existing_recipe_or_failure_cards():
    manifest = yaml.safe_load((ROOT / "manifests" / "regression_manifest.yaml").read_text(encoding="utf-8"))

    for entry in manifest["entries"]:
        card = entry.get("recipe_card") or entry.get("failure_card")
        assert card, f"{entry['test_id']} must point to a recipe or failure card"
        assert (ROOT / card).exists(), f"{entry['test_id']} points to missing card: {card}"


def test_native_success_entries_are_imported_as_non_executable_call_patterns():
    recipe_manifest = yaml.safe_load((ROOT / "manifests" / "recipe_manifest.yaml").read_text(encoding="utf-8"))
    recipes = {recipe["test_id"]: recipe for recipe in recipe_manifest["recipes"] if recipe.get("test_id")}
    regression = yaml.safe_load((ROOT / "manifests" / "regression_manifest.yaml").read_text(encoding="utf-8"))

    success_ids = {entry["test_id"] for entry in regression["entries"] if entry["classification"] == "NATIVE_SUCCESS"}

    assert set(recipes) == success_ids
    for recipe in recipes.values():
        assert recipe["runner_kind"] == "imported_call_pattern"
        assert recipe["runner"] is None
        assert recipe["user_mode_allowed"] is False


def section_body(text, heading):
    pattern = rf"## {re.escape(heading)}\n(?P<body>.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, flags=re.S)
    assert match, f"Missing section: {heading}"
    return match.group("body").strip()


def test_imported_recipe_cards_record_api_methods_and_minimal_patterns():
    recipe_manifest = yaml.safe_load((ROOT / "manifests" / "recipe_manifest.yaml").read_text(encoding="utf-8"))
    imported = [recipe for recipe in recipe_manifest["recipes"] if recipe.get("runner_kind") == "imported_call_pattern"]

    for recipe in imported:
        text = (ROOT / recipe["recipe_card"]).read_text(encoding="utf-8")
        assert section_body(text, "API Methods"), f"{recipe['id']} must list API methods"
        minimal_pattern = section_body(text, "Minimal Successful Code Pattern")
        assert "```python" in minimal_pattern, f"{recipe['id']} must include a Python pattern"


def test_capability_manifest_references_existing_recipes_and_failure_cards():
    capability = yaml.safe_load((ROOT / "manifests" / "capability_manifest.yaml").read_text(encoding="utf-8"))
    recipe_manifest = yaml.safe_load((ROOT / "manifests" / "recipe_manifest.yaml").read_text(encoding="utf-8"))
    recipe_ids = {recipe["id"] for recipe in recipe_manifest["recipes"]}

    for domain in capability["capabilities"].values():
        for feature in domain.values():
            for key in ["executable_recipe_ids", "imported_recipe_ids"]:
                for recipe_id in feature.get(key, []):
                    assert recipe_id in recipe_ids
            for failure_card in feature.get("failure_card_ids", []):
                assert (ROOT / failure_card).exists()


def test_live_regression_report_is_sanitized_for_github():
    report = ROOT / "examples" / "reports" / "live_regression_20260706_232109.md"
    text = report.read_text(encoding="utf-8")

    assert "catia_recipe_regression_20260706_232109" in text
    assert "C:\\Users" not in text
    assert ".CATPart" not in text
