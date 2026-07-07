from pathlib import Path
import importlib.util

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
REPORT_SCHEMA = yaml.safe_load((ROOT / "schemas" / "report_schema.yaml").read_text(encoding="utf-8"))


def load_module(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_runner_reports_match_report_schema():
    runner_cases = [
        (
            ROOT / "runners" / "partdesign" / "rectangular_pad_runner.py",
            "partdesign.rectangular_pad",
            "base_pad",
        ),
        (
            ROOT / "runners" / "knowledgeware" / "real_param_formula_runner.py",
            "knowledgeware.real_param_formula",
            "formula_1",
        ),
        (
            ROOT / "runners" / "assembly" / "product_fix_constraint_runner.py",
            "assembly.product_fix_constraint",
            "fix_1",
        ),
    ]

    for runner_path, recipe_id, feature_id in runner_cases:
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
        assert report["classifications"] == {"NATIVE_SUCCESS": 1}
        assert report["feature_results"][0]["feature_id"] == feature_id
        assert report["feature_results"][0]["recipe_id"] == recipe_id


def test_legacy_runners_resolve_catpart_paths_before_catia_save_as():
    runner_paths = [
        ROOT / "runners" / "partdesign" / "rectangular_pad_runner.py",
        ROOT / "runners" / "knowledgeware" / "real_param_formula_runner.py",
        ROOT / "runners" / "assembly" / "product_fix_constraint_runner.py",
    ]

    for runner_path in runner_paths:
        text = runner_path.read_text(encoding="utf-8")
        assert ".resolve()" in text, f"{runner_path.name} must pass an absolute path to CATIA SaveAs"


def test_legacy_runners_do_not_fail_when_part_number_assignment_is_rejected():
    runner_paths = [
        ROOT / "runners" / "partdesign" / "rectangular_pad_runner.py",
        ROOT / "runners" / "knowledgeware" / "real_param_formula_runner.py",
        ROOT / "runners" / "assembly" / "product_fix_constraint_runner.py",
    ]

    for runner_path in runner_paths:
        text = runner_path.read_text(encoding="utf-8")
        assert "safe_set_part_number" in text, f"{runner_path.name} must tolerate CATIA PartNumber assignment failures"


def test_xy_sketch_native_holes_reverse_into_the_base_pad():
    helper = ROOT / "runners" / "partdesign" / "prismatic_cut_common.py"
    text = helper.read_text(encoding="utf-8")

    start = text.index("def create_native_hole_from_sketch")
    end = text.index("def create_native_slot_pocket", start)
    function_body = text[start:end]

    assert "hole.reverse()" in function_body


def test_xy_sketch_native_slot_pockets_cut_into_the_base_pad():
    helper = ROOT / "runners" / "partdesign" / "prismatic_cut_common.py"
    text = helper.read_text(encoding="utf-8")

    start = text.index("def create_native_slot_pocket")
    end = text.index("def make_partdesign_report", start)
    function_body = text[start:end]

    assert "pocket.direction_orientation = 0" in function_body


def test_counterbore_uses_top_entry_offset_plane_not_bottom_xy_plane():
    runner = ROOT / "runners" / "partdesign" / "native_counterbore_holes_runner.py"
    text = runner.read_text(encoding="utf-8")

    assert "create_offset_plane_reference" in text
    assert 'offset=params["plate_depth"]' in text
    assert "top_ref" in text


def test_parametric_plate_holes_reverse_into_the_base_pad():
    runner = ROOT / "runners" / "partdesign" / "parametric_plate_formula_holes_runner.py"
    text = runner.read_text(encoding="utf-8")

    start = text.index("def create_formula_driven_hole")
    end = text.index("def build_parametric_plate_formula_holes", start)
    function_body = text[start:end]

    assert "hole.reverse()" in function_body


def test_parametric_plate_base_sketch_is_centered_and_orientation_constrained():
    runner = ROOT / "runners" / "partdesign" / "parametric_plate_formula_holes_runner.py"
    text = runner.read_text(encoding="utf-8")

    start = text.index("def create_formula_driven_base")
    end = text.index("def create_formula_driven_hole", start)
    function_body = text[start:end]

    assert "catCstTypeHorizontality" in function_body
    assert "catCstTypeVerticality" in function_body
    assert "Formula_Base_Right_From_YAxis" in function_body
    assert "Formula_Base_Left_From_YAxis" in function_body
    assert "Formula_Base_Top_From_XAxis" in function_body
    assert "Formula_Base_Bottom_From_XAxis" in function_body


def test_pattern_and_mirror_seed_features_use_top_entry_planes():
    runner_paths = [
        ROOT / "runners" / "partdesign" / "native_rectangular_pattern_runner.py",
        ROOT / "runners" / "partdesign" / "native_circular_pattern_runner.py",
        ROOT / "runners" / "partdesign" / "native_mirror_plane_runner.py",
    ]

    for runner_path in runner_paths:
        text = runner_path.read_text(encoding="utf-8")
        assert "create_offset_plane_reference" in text
        assert "top_ref" in text
