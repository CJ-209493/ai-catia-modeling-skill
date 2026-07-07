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


def test_rectangular_and_circular_patterns_are_user_mode_runners():
    expected = {
        "partdesign.native_rectangular_pattern": (
            "RectPattern",
            "runners/partdesign/native_rectangular_pattern_runner.py",
            "partdesign.rectangular_pattern_direction_refs",
        ),
        "partdesign.native_circular_pattern": (
            "CircPattern",
            "runners/partdesign/native_circular_pattern_runner.py",
            "partdesign.circular_pattern_axis_ref",
        ),
    }

    for recipe_id, (native_feature, runner, reference_pattern_id) in expected.items():
        recipe = recipe_by_id(recipe_id)
        assert recipe["status"] == "live_verified_once"
        assert recipe["native_feature"] == native_feature
        assert recipe["runner"] == runner
        assert recipe["user_mode_allowed"] is True
        assert recipe["reference_pattern_ids"] == [reference_pattern_id]
        assert recipe["promoted_from"]
        assert (ROOT / recipe["recipe_card"]).exists()
        assert (ROOT / runner).exists()


def test_pattern_reference_manifest_documents_required_references():
    manifest = load_yaml("manifests/reference_manifest.yaml")
    patterns = {item["id"]: item for item in manifest["reference_patterns"]}

    expected = {
        "partdesign.rectangular_pattern_direction_refs": ["rect_pattern"],
        "partdesign.circular_pattern_axis_ref": ["circ_pattern"],
    }

    for pattern_id, applies_to in expected.items():
        pattern = patterns[pattern_id]
        assert pattern["applies_to"] == applies_to
        assert (ROOT / pattern["reference_doc"]).exists()
        assert pattern["promoted_recipe_ids"]


def test_promoted_pattern_cards_record_native_feature_contracts():
    expected = {
        "recipes/partdesign/native_rectangular_pattern.yaml": ("RectPattern", "partdesign.rectangular_pattern_direction_refs"),
        "recipes/partdesign/native_circular_pattern.yaml": ("CircPattern", "partdesign.circular_pattern_axis_ref"),
    }

    for recipe_path, (native_feature, reference_pattern_id) in expected.items():
        card = load_yaml(recipe_path)
        assert card["status"] == "live_verified_once"
        assert card["reference_pattern_ids"] == [reference_pattern_id]
        assert card["verification"]["required_native_feature"] == native_feature
        assert card["verification"]["part_update_required"] is True
        assert any(native_feature in step or native_feature.replace("Pattern", "_pattern") in step for step in card["verified_pattern"])


def test_promoted_pattern_runners_emit_schema_reports():
    cases = [
        (
            "runners/partdesign/native_rectangular_pattern_runner.py",
            "partdesign.native_rectangular_pattern",
            "rect_pattern_1",
            "RectPattern",
            "partdesign.rectangular_pattern_direction_refs",
        ),
        (
            "runners/partdesign/native_circular_pattern_runner.py",
            "partdesign.native_circular_pattern",
            "circ_pattern_1",
            "CircPattern",
            "partdesign.circular_pattern_axis_ref",
        ),
    ]

    for runner_path, recipe_id, feature_id, native_feature, reference_pattern_id in cases:
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
        assert report["reference_pattern_ids"] == [reference_pattern_id]


def test_capability_manifest_marks_patterns_as_executable():
    capability = load_yaml("manifests/capability_manifest.yaml")
    partdesign = capability["capabilities"]["partdesign"]

    assert "partdesign.native_rectangular_pattern" in partdesign["rect_pattern"]["executable_recipe_ids"]
    assert partdesign["rect_pattern"]["user_mode"] == "executable_runner_available"
    assert "partdesign.native_circular_pattern" in partdesign["circ_pattern"]["executable_recipe_ids"]
    assert partdesign["circ_pattern"]["user_mode"] == "executable_runner_available"
