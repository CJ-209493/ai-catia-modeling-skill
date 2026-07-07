from pathlib import Path
import importlib.util

import jsonschema
import yaml

from verifiers.feature_tree_verifier import verify_revolution_centerline_feature
from runners.partdesign.revolution_centerline_common import (
    catpart_output_path,
    safe_set_part_number,
    save_document_overwrite,
)


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


def test_shaft_and_groove_are_promoted_to_user_mode_runners():
    expected = {
        "partdesign.native_shaft_centerline": ("Shaft", "runners/partdesign/native_shaft_centerline_runner.py"),
        "partdesign.native_groove_centerline": ("Groove", "runners/partdesign/native_groove_centerline_runner.py"),
    }

    for recipe_id, (native_feature, runner) in expected.items():
        recipe = recipe_by_id(recipe_id)
        assert recipe["status"] == "live_verified_once"
        assert recipe["native_feature"] == native_feature
        assert recipe["runner"] == runner
        assert recipe["user_mode_allowed"] is True
        assert recipe["reference_pattern_ids"] == ["partdesign.sketch_revolution_axis"]
        assert (ROOT / recipe["recipe_card"]).exists()
        assert (ROOT / runner).exists()


def test_promoted_revolution_recipe_cards_record_centerline_reference_pattern():
    for recipe_path in [
        "recipes/partdesign/native_shaft_centerline.yaml",
        "recipes/partdesign/native_groove_centerline.yaml",
    ]:
        card = load_yaml(recipe_path)
        assert card["status"] == "live_verified_once"
        assert card["reference_pattern_ids"] == ["partdesign.sketch_revolution_axis"]
        assert any("CenterLine" in step for step in card["verified_pattern"])
        assert card["verification"]["part_update_required"] is True
        assert card["verification"]["required_native_feature"] in {"Shaft", "Groove"}


def test_promoted_revolution_runners_emit_schema_reports():
    cases = [
        (
            "runners/partdesign/native_shaft_centerline_runner.py",
            "partdesign.native_shaft_centerline",
            "shaft_1",
            "Shaft",
        ),
        (
            "runners/partdesign/native_groove_centerline_runner.py",
            "partdesign.native_groove_centerline",
            "groove_1",
            "Groove",
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
        assert report["reference_pattern_ids"] == ["partdesign.sketch_revolution_axis"]


def test_revolution_centerline_verifier_requires_reference_pattern():
    report = {
        "part_update_success": True,
        "feature_tree_contains": ["Shaft"],
        "reference_pattern_ids": ["partdesign.sketch_revolution_axis"],
    }

    assert verify_revolution_centerline_feature(report, "Shaft")["passed"] is True

    report["reference_pattern_ids"] = []
    failed = verify_revolution_centerline_feature(report, "Shaft")
    assert failed["passed"] is False
    assert "partdesign.sketch_revolution_axis" in failed["required_reference_pattern"]


def test_part_number_assignment_is_best_effort_for_live_catia_sessions():
    class BrokenProduct:
        @property
        def part_number(self):
            return "OriginalPartNumber"

        @part_number.setter
        def part_number(self, value):
            raise RuntimeError("CATIA rejected PartNumber")

    result = safe_set_part_number(BrokenProduct(), "DemoPart")

    assert result["requested"] == "DemoPart"
    assert result["applied"] is False
    assert "CATIA rejected PartNumber" in result["error"]


def test_save_document_overwrite_uses_absolute_path_and_overwrite_flag():
    class FakeDocument:
        def __init__(self):
            self.calls = []

        def save_as(self, path, overwrite=False):
            self.calls.append((Path(path), overwrite))

    target = ROOT / "outputs" / "contract_only" / "demo.CATPart"
    doc = FakeDocument()

    saved_path = save_document_overwrite(doc, target)

    assert saved_path == target.resolve()
    assert doc.calls == [(target.resolve(), True)]


def test_catpart_output_path_includes_run_id_to_avoid_open_file_collisions():
    path = catpart_output_path(ROOT / "outputs" / "demo", "DemoPart", "20260706_235959_123456")

    assert path == (ROOT / "outputs" / "demo" / "DemoPart_20260706_235959_123456.CATPart").resolve()
