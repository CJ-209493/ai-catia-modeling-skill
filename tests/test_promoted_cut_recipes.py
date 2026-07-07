from pathlib import Path
import importlib.util

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
REPORT_SCHEMA = yaml.safe_load((ROOT / "schemas" / "report_schema.yaml").read_text(encoding="utf-8"))


def load_yaml(path):
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


def load_module(path):
    module_path = ROOT / path
    spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def recipe_by_id(recipe_id):
    manifest = load_yaml("manifests/recipe_manifest.yaml")
    return next(item for item in manifest["recipes"] if item["id"] == recipe_id)


def test_hole_and_pocket_are_promoted_to_user_mode_runners():
    expected = {
        "partdesign.native_hole_from_sketch": ("Hole", "runners/partdesign/native_hole_from_sketch_runner.py"),
        "partdesign.native_slot_pocket": ("Pocket", "runners/partdesign/native_slot_pocket_runner.py"),
    }

    for recipe_id, (native_feature, runner) in expected.items():
        recipe = recipe_by_id(recipe_id)
        assert recipe["status"] == "live_verified_once"
        assert recipe["native_feature"] == native_feature
        assert recipe["runner"] == runner
        assert recipe["user_mode_allowed"] is True
        assert recipe["promoted_from"]
        assert (ROOT / recipe["recipe_card"]).exists()
        assert (ROOT / runner).exists()


def test_promoted_cut_recipe_cards_record_native_feature_contracts():
    expected = {
        "recipes/partdesign/native_hole_from_sketch.yaml": "Hole",
        "recipes/partdesign/native_slot_pocket.yaml": "Pocket",
    }

    for recipe_path, native_feature in expected.items():
        card = load_yaml(recipe_path)
        assert card["status"] == "live_verified_once"
        assert card["verification"]["required_native_feature"] == native_feature
        assert card["verification"]["part_update_required"] is True
        assert any("Part.Update" in step for step in card["verified_pattern"])


def test_promoted_cut_runners_emit_schema_reports():
    cases = [
        (
            "runners/partdesign/native_hole_from_sketch_runner.py",
            "partdesign.native_hole_from_sketch",
            "hole_1",
            "Hole",
        ),
        (
            "runners/partdesign/native_slot_pocket_runner.py",
            "partdesign.native_slot_pocket",
            "slot_pocket_1",
            "Pocket",
        ),
    ]

    for runner_path, recipe_id, feature_id, native_feature in cases:
        module = load_module(runner_path)
        report = module.make_report(
            run_id="test-run",
            mode="user",
            feature_id=feature_id,
            recipe_id=recipe_id,
            catia_document="outputs/test.CATPart",
            classification="NATIVE_SUCCESS",
            part_update_success=True,
            verifier_passed=True,
            notes="schema contract test",
        )

        jsonschema.validate(report, REPORT_SCHEMA)
        assert report["feature_results"][0]["recipe_id"] == recipe_id
        assert report["expected_native_feature"] == native_feature
        assert report["feature_tree_contains"] == [native_feature]


def test_capability_manifest_marks_hole_and_pocket_as_executable():
    capability = load_yaml("manifests/capability_manifest.yaml")
    partdesign = capability["capabilities"]["partdesign"]

    assert "partdesign.native_hole_from_sketch" in partdesign["hole"]["executable_recipe_ids"]
    assert partdesign["hole"]["user_mode"] == "executable_runner_available"
    assert "partdesign.native_slot_pocket" in partdesign["pocket"]["executable_recipe_ids"]
    assert partdesign["pocket"]["user_mode"] == "executable_runner_available"
