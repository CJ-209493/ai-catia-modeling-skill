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


def test_parametric_plate_is_user_mode_runner():
    recipe = recipe_by_id("partdesign.parametric_plate_formula_holes")

    assert recipe["status"] == "live_verified_once"
    assert recipe["native_feature"] == "Formula"
    assert recipe["runner"] == "runners/partdesign/parametric_plate_formula_holes_runner.py"
    assert recipe["user_mode_allowed"] is True
    assert recipe["reference_pattern_ids"] == ["knowledgeware.formula_driven_sketch_dimensions"]
    assert recipe["promoted_from"] == ["partdesign.regression.t19_parameters_formulas"]
    assert (ROOT / recipe["recipe_card"]).exists()
    assert (ROOT / recipe["runner"]).exists()


def test_parametric_plate_reference_manifest_documents_open_sketch_constraint_pattern():
    manifest = load_yaml("manifests/reference_manifest.yaml")
    patterns = {item["id"]: item for item in manifest["reference_patterns"]}

    pattern = patterns["knowledgeware.formula_driven_sketch_dimensions"]
    assert pattern["applies_to"] == ["formula_driven_sketch"]
    assert pattern["reference_doc"] == "references/knowledgeware/formula_driven_sketch_dimensions.md"
    assert (ROOT / pattern["reference_doc"]).exists()
    assert pattern["promoted_recipe_ids"] == ["partdesign.parametric_plate_formula_holes"]
    assert any("sketch is still open" in expectation for expectation in pattern["verifier_expectations"])


def test_parametric_plate_card_records_update_contract():
    card = load_yaml("recipes/partdesign/parametric_plate_formula_holes.yaml")

    assert card["status"] == "live_verified_once"
    assert card["reference_pattern_ids"] == ["knowledgeware.formula_driven_sketch_dimensions"]
    assert card["verification"]["required_native_feature"] == "Formula"
    assert card["verification"]["part_update_required"] is True
    assert card["verification"]["required_reference_pattern"] == "knowledgeware.formula_driven_sketch_dimensions"
    assert card["verification"]["length_update_mm"] == 150
    assert any("sketch is open" in step for step in card["verified_pattern"])
    assert any("arbitrary sketch constraint inference" in caveat for caveat in card["caveats"])


def test_parametric_plate_runner_emits_schema_report():
    module = load_module("runners/partdesign/parametric_plate_formula_holes_runner.py")

    report = module.make_report(
        run_id="test-run",
        mode="user",
        feature_id="parametric_plate_1",
        recipe_id="partdesign.parametric_plate_formula_holes",
        catia_document="outputs/test.CATPart",
        classification="NATIVE_SUCCESS",
        part_update_success=True,
        verifier_passed=True,
        notes="schema contract test",
        extra={
            "initial_length_mm": 120.0,
            "updated_length_mm": 150.0,
            "updated_hole_x_offset_mm": 63.0,
            "relations_count": 19,
        },
    )

    jsonschema.validate(report, REPORT_SCHEMA)
    assert report["feature_results"][0]["recipe_id"] == "partdesign.parametric_plate_formula_holes"
    assert report["expected_native_feature"] == "Formula"
    assert report["feature_tree_contains"] == ["Formula", "Pad", "Hole"]
    assert report["reference_pattern_ids"] == ["knowledgeware.formula_driven_sketch_dimensions"]
    assert report["updated_length_mm"] == 150.0


def test_capability_manifest_marks_formula_driven_sketch_as_executable():
    capability = load_yaml("manifests/capability_manifest.yaml")
    formula_sketch = capability["capabilities"]["knowledgeware"]["formula_driven_sketch"]

    assert formula_sketch["status"] == "live_verified_once"
    assert formula_sketch["classification"] == "NATIVE_SUCCESS"
    assert "partdesign.parametric_plate_formula_holes" in formula_sketch["executable_recipe_ids"]
    assert "knowledgeware.formula_driven_sketch_dimensions" in formula_sketch["reference_pattern_ids"]
    assert formula_sketch["user_mode"] == "executable_runner_available"
    assert "arbitrary sketch constraint inference" in formula_sketch["caveat"]
