from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_recipe_manifest_points_to_existing_files():
    manifest = yaml.safe_load((ROOT / "manifests" / "recipe_manifest.yaml").read_text(encoding="utf-8"))
    for recipe in manifest["recipes"]:
        assert (ROOT / recipe["recipe_card"]).exists()
        if recipe.get("runner"):
            assert (ROOT / recipe["runner"]).exists()


def test_rectangular_pad_is_user_mode_stable():
    manifest = yaml.safe_load((ROOT / "manifests" / "recipe_manifest.yaml").read_text(encoding="utf-8"))
    recipe = next(item for item in manifest["recipes"] if item["id"] == "partdesign.rectangular_pad")
    assert recipe["status"] == "stable"
    assert recipe["user_mode_allowed"] is True


def test_regression_verified_call_patterns_are_indexed_but_not_user_runners():
    manifest = yaml.safe_load((ROOT / "manifests" / "recipe_manifest.yaml").read_text(encoding="utf-8"))
    imported = [item for item in manifest["recipes"] if item.get("runner_kind") == "imported_call_pattern"]
    ids = {item["id"] for item in imported}

    assert len(imported) >= 16
    assert "partdesign.regression.t11_shaft_with_sketch_centerline" in ids
    assert "partdesign.regression.t12_groove_with_sketch_centerline" in ids
    assert "partdesign.regression.t14_shell_from_face_reference" in ids

    for recipe in imported:
        assert recipe["status"] == "live_verified_once"
        assert recipe["classification"] == "NATIVE_SUCCESS"
        assert recipe["runner"] is None
        assert recipe["user_mode_allowed"] is False
