from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_recipe_manifest_points_to_existing_files():
    manifest = yaml.safe_load((ROOT / "manifests" / "recipe_manifest.yaml").read_text(encoding="utf-8"))
    for recipe in manifest["recipes"]:
        assert (ROOT / recipe["recipe_card"]).exists()
        assert (ROOT / recipe["runner"]).exists()


def test_rectangular_pad_is_user_mode_stable():
    manifest = yaml.safe_load((ROOT / "manifests" / "recipe_manifest.yaml").read_text(encoding="utf-8"))
    recipe = next(item for item in manifest["recipes"] if item["id"] == "partdesign.rectangular_pad")
    assert recipe["status"] == "stable"
    assert recipe["user_mode_allowed"] is True
