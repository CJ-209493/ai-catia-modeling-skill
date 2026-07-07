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


def test_profile_and_hole_variants_are_user_mode_runners():
    expected = {
        "partdesign.native_counterbore_holes": (
            "Hole",
            "runners/partdesign/native_counterbore_holes_runner.py",
            "partdesign.counterbore_hole_point_sketch",
        ),
        "partdesign.offset_plane_pad": (
            "Pad",
            "runners/partdesign/offset_plane_pad_runner.py",
            "partdesign.offset_plane_support_ref",
        ),
        "partdesign.rounded_rectangle_pad": (
            "Pad",
            "runners/partdesign/rounded_rectangle_pad_runner.py",
            "partdesign.tangent_arc_closed_profile",
        ),
        "partdesign.capsule_with_native_holes": (
            "Hole",
            "runners/partdesign/capsule_native_holes_runner.py",
            "partdesign.capsule_profile_native_holes",
        ),
        "partdesign.closed_spline_pad": (
            "Pad",
            "runners/partdesign/closed_spline_pad_runner.py",
            "partdesign.closed_spline_profile",
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


def test_profile_and_hole_reference_manifest_documents_required_patterns():
    manifest = load_yaml("manifests/reference_manifest.yaml")
    patterns = {item["id"]: item for item in manifest["reference_patterns"]}

    expected = {
        "partdesign.counterbore_hole_point_sketch": ["counterbore_hole"],
        "partdesign.offset_plane_support_ref": ["offset_plane_pad"],
        "partdesign.tangent_arc_closed_profile": ["rounded_rectangle_pad"],
        "partdesign.capsule_profile_native_holes": ["capsule_with_native_holes"],
        "partdesign.closed_spline_profile": ["closed_spline_pad"],
    }

    for pattern_id, applies_to in expected.items():
        pattern = patterns[pattern_id]
        assert pattern["applies_to"] == applies_to
        assert (ROOT / pattern["reference_doc"]).exists()
        assert pattern["promoted_recipe_ids"]


def test_profile_and_hole_cards_record_native_feature_contracts():
    expected = {
        "recipes/partdesign/native_counterbore_holes.yaml": ("Hole", "partdesign.counterbore_hole_point_sketch"),
        "recipes/partdesign/offset_plane_pad.yaml": ("Pad", "partdesign.offset_plane_support_ref"),
        "recipes/partdesign/rounded_rectangle_pad.yaml": ("Pad", "partdesign.tangent_arc_closed_profile"),
        "recipes/partdesign/capsule_with_native_holes.yaml": ("Hole", "partdesign.capsule_profile_native_holes"),
        "recipes/partdesign/closed_spline_pad.yaml": ("Pad", "partdesign.closed_spline_profile"),
    }

    for recipe_path, (native_feature, reference_pattern_id) in expected.items():
        card = load_yaml(recipe_path)
        assert card["status"] == "live_verified_once"
        assert card["reference_pattern_ids"] == [reference_pattern_id]
        assert card["verification"]["required_native_feature"] == native_feature
        assert card["verification"]["part_update_required"] is True
        assert any("Part.Update" in step for step in card["verified_pattern"])


def test_profile_and_hole_runners_emit_schema_reports():
    cases = [
        (
            "runners/partdesign/native_counterbore_holes_runner.py",
            "partdesign.native_counterbore_holes",
            "counterbore_holes_1",
            "Hole",
            "partdesign.counterbore_hole_point_sketch",
        ),
        (
            "runners/partdesign/offset_plane_pad_runner.py",
            "partdesign.offset_plane_pad",
            "offset_plane_pad_1",
            "Pad",
            "partdesign.offset_plane_support_ref",
        ),
        (
            "runners/partdesign/rounded_rectangle_pad_runner.py",
            "partdesign.rounded_rectangle_pad",
            "rounded_rectangle_pad_1",
            "Pad",
            "partdesign.tangent_arc_closed_profile",
        ),
        (
            "runners/partdesign/capsule_native_holes_runner.py",
            "partdesign.capsule_with_native_holes",
            "capsule_holes_1",
            "Hole",
            "partdesign.capsule_profile_native_holes",
        ),
        (
            "runners/partdesign/closed_spline_pad_runner.py",
            "partdesign.closed_spline_pad",
            "closed_spline_pad_1",
            "Pad",
            "partdesign.closed_spline_profile",
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


def test_capability_manifest_marks_profile_and_hole_variants_as_executable():
    capability = load_yaml("manifests/capability_manifest.yaml")
    partdesign = capability["capabilities"]["partdesign"]

    assert "partdesign.native_counterbore_holes" in partdesign["counterbore_hole"]["executable_recipe_ids"]
    assert partdesign["counterbore_hole"]["user_mode"] == "executable_runner_available"
    assert "partdesign.offset_plane_pad" in partdesign["offset_plane_pad"]["executable_recipe_ids"]
    assert partdesign["offset_plane_pad"]["user_mode"] == "executable_runner_available"
    assert "partdesign.rounded_rectangle_pad" in partdesign["rounded_rectangle_pad"]["executable_recipe_ids"]
    assert partdesign["rounded_rectangle_pad"]["user_mode"] == "executable_runner_available"
    assert "partdesign.capsule_with_native_holes" in partdesign["capsule_with_native_holes"]["executable_recipe_ids"]
    assert partdesign["capsule_with_native_holes"]["user_mode"] == "executable_runner_available"
    assert "partdesign.closed_spline_pad" in partdesign["closed_spline_pad"]["executable_recipe_ids"]
    assert partdesign["closed_spline_pad"]["user_mode"] == "executable_runner_available"
