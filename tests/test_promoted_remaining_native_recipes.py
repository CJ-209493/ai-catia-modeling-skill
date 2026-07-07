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


def test_remaining_native_successes_are_user_mode_runners():
    expected = {
        "partdesign.native_v_pulley_shaft": (
            "Shaft",
            "runners/partdesign/native_v_pulley_shaft_runner.py",
            ["partdesign.sketch_revolution_axis", "partdesign.v_pulley_shaft_profile"],
        ),
        "partdesign.native_hole_unit_conversion": (
            "Hole",
            "runners/partdesign/native_hole_unit_conversion_runner.py",
            ["partdesign.inch_to_mm_parameters"],
        ),
    }

    for recipe_id, (native_feature, runner, reference_pattern_ids) in expected.items():
        recipe = recipe_by_id(recipe_id)
        assert recipe["status"] == "live_verified_once"
        assert recipe["native_feature"] == native_feature
        assert recipe["runner"] == runner
        assert recipe["user_mode_allowed"] is True
        assert recipe["reference_pattern_ids"] == reference_pattern_ids
        assert recipe["promoted_from"]
        assert (ROOT / recipe["recipe_card"]).exists()
        assert (ROOT / runner).exists()


def test_remaining_reference_manifest_documents_required_patterns():
    manifest = load_yaml("manifests/reference_manifest.yaml")
    patterns = {item["id"]: item for item in manifest["reference_patterns"]}

    expected = {
        "partdesign.v_pulley_shaft_profile": ["v_pulley_shaft"],
        "partdesign.inch_to_mm_parameters": ["unit_conversion_native_hole"],
    }

    for pattern_id, applies_to in expected.items():
        pattern = patterns[pattern_id]
        assert pattern["applies_to"] == applies_to
        assert (ROOT / pattern["reference_doc"]).exists()
        assert pattern["promoted_recipe_ids"]


def test_remaining_recipe_cards_record_native_feature_contracts():
    expected = {
        "recipes/partdesign/native_v_pulley_shaft.yaml": (
            "Shaft",
            ["partdesign.sketch_revolution_axis", "partdesign.v_pulley_shaft_profile"],
        ),
        "recipes/partdesign/native_hole_unit_conversion.yaml": (
            "Hole",
            ["partdesign.inch_to_mm_parameters"],
        ),
    }

    for recipe_path, (native_feature, reference_pattern_ids) in expected.items():
        card = load_yaml(recipe_path)
        assert card["status"] == "live_verified_once"
        assert card["reference_pattern_ids"] == reference_pattern_ids
        assert card["verification"]["required_native_feature"] == native_feature
        assert card["verification"]["part_update_required"] is True
        assert any("Part.Update" in step for step in card["verified_pattern"])


def test_remaining_runners_emit_schema_reports():
    cases = [
        (
            "runners/partdesign/native_v_pulley_shaft_runner.py",
            "partdesign.native_v_pulley_shaft",
            "v_pulley_shaft_1",
            "Shaft",
            ["partdesign.sketch_revolution_axis", "partdesign.v_pulley_shaft_profile"],
        ),
        (
            "runners/partdesign/native_hole_unit_conversion_runner.py",
            "partdesign.native_hole_unit_conversion",
            "unit_conversion_hole_1",
            "Hole",
            ["partdesign.inch_to_mm_parameters"],
        ),
    ]

    for runner_path, recipe_id, feature_id, native_feature, reference_pattern_ids in cases:
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
        assert report["reference_pattern_ids"] == reference_pattern_ids


def test_capability_manifest_marks_remaining_native_successes_as_executable():
    capability = load_yaml("manifests/capability_manifest.yaml")
    partdesign = capability["capabilities"]["partdesign"]

    assert "partdesign.native_v_pulley_shaft" in partdesign["shaft"]["executable_recipe_ids"]
    assert "partdesign.native_v_pulley_shaft" in partdesign["v_pulley_shaft"]["executable_recipe_ids"]
    assert partdesign["v_pulley_shaft"]["user_mode"] == "executable_runner_available"
    assert "partdesign.native_hole_unit_conversion" in partdesign["hole"]["executable_recipe_ids"]
    assert "partdesign.native_hole_unit_conversion" in partdesign["unit_conversion_native_hole"]["executable_recipe_ids"]
    assert partdesign["unit_conversion_native_hole"]["user_mode"] == "executable_runner_available"
