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


def test_chamfer_is_user_mode_runner():
    recipe = recipe_by_id("partdesign.native_chamfer_selected_edge")

    assert recipe["status"] == "live_verified_once"
    assert recipe["native_feature"] == "Chamfer"
    assert recipe["runner"] == "runners/partdesign/native_chamfer_selected_edge_runner.py"
    assert recipe["user_mode_allowed"] is True
    assert recipe["reference_pattern_ids"] == ["partdesign.chamfer_selected_edge_ref"]
    assert recipe["promoted_from"] == ["partdesign.regression.t16_fillet_chamfer_order"]
    assert (ROOT / recipe["recipe_card"]).exists()
    assert (ROOT / recipe["runner"]).exists()


def test_chamfer_reference_manifest_documents_selected_edge_pattern():
    manifest = load_yaml("manifests/reference_manifest.yaml")
    patterns = {item["id"]: item for item in manifest["reference_patterns"]}

    pattern = patterns["partdesign.chamfer_selected_edge_ref"]
    assert pattern["applies_to"] == ["chamfer"]
    assert pattern["reference_doc"] == "references/partdesign/edge_selection_features.md"
    assert (ROOT / pattern["reference_doc"]).exists()
    assert pattern["promoted_recipe_ids"] == ["partdesign.native_chamfer_selected_edge"]
    assert any("AddNewChamfer" in expectation for expectation in pattern["verifier_expectations"])


def test_chamfer_card_records_native_feature_contract():
    card = load_yaml("recipes/partdesign/native_chamfer_selected_edge.yaml")

    assert card["status"] == "live_verified_once"
    assert card["reference_pattern_ids"] == ["partdesign.chamfer_selected_edge_ref"]
    assert card["verification"]["required_native_feature"] == "Chamfer"
    assert card["verification"]["part_update_required"] is True
    assert card["verification"]["required_reference_pattern"] == "partdesign.chamfer_selected_edge_ref"
    assert any("ShapeFactory.AddNewChamfer" in step for step in card["verified_pattern"])
    assert any("ordered fillet/chamfer" in caveat for caveat in card["caveats"])


def test_chamfer_runner_emits_schema_report():
    module = load_module("runners/partdesign/native_chamfer_selected_edge_runner.py")

    report = module.make_report(
        run_id="test-run",
        mode="user",
        feature_id="chamfer_1",
        recipe_id="partdesign.native_chamfer_selected_edge",
        catia_document="outputs/test.CATPart",
        classification="NATIVE_SUCCESS",
        part_update_success=True,
        verifier_passed=True,
        notes="schema contract test",
    )

    jsonschema.validate(report, REPORT_SCHEMA)
    assert report["feature_results"][0]["recipe_id"] == "partdesign.native_chamfer_selected_edge"
    assert report["expected_native_feature"] == "Chamfer"
    assert report["feature_tree_contains"] == ["Chamfer"]
    assert report["reference_pattern_ids"] == ["partdesign.chamfer_selected_edge_ref"]


def test_capability_manifest_marks_constrained_chamfer_as_executable():
    capability = load_yaml("manifests/capability_manifest.yaml")
    chamfer = capability["capabilities"]["partdesign"]["chamfer"]

    assert chamfer["status"] == "live_verified_once"
    assert chamfer["classification"] == "NATIVE_SUCCESS"
    assert "partdesign.native_chamfer_selected_edge" in chamfer["executable_recipe_ids"]
    assert "partdesign.chamfer_selected_edge_ref" in chamfer["reference_pattern_ids"]
    assert chamfer["user_mode"] == "executable_runner_available"
    assert "ordered fillet/chamfer" in chamfer["caveat"]
