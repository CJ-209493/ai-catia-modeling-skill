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
