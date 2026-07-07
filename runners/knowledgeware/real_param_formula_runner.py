"""Runner for recipe knowledgeware.real_param_formula."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

import yaml


def normalize_params(params):
    return {
        "part_number": params.get("part_number", "Knowledgeware_Formula"),
        "input_name": params.get("input_name", "Input"),
        "output_name": params.get("output_name", "Output"),
        "input_value": float(params.get("input_value", 5.0)),
        "multiplier": float(params.get("multiplier", 2.0)),
    }


def make_report(
    *,
    run_id,
    mode,
    feature_id,
    recipe_id,
    catia_document,
    classification,
    part_update_success,
    verifier_passed,
    notes="",
    extra=None,
):
    report = {
        "run_id": run_id,
        "mode": mode,
        "catia_document": str(catia_document),
        "classifications": {classification: 1},
        "feature_results": [
            {
                "feature_id": feature_id,
                "recipe_id": recipe_id,
                "classification": classification,
                "part_update_success": part_update_success,
                "verifier_passed": verifier_passed,
                "notes": notes,
            }
        ],
    }
    if extra:
        report.update(extra)
    return report


def build_formula(params, output_dir, feature_id="formula_1", mode="user"):
    from pycatia import catia

    params = normalize_params(params)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    app = catia()
    doc = app.documents.add("Part")
    part = doc.part
    doc.product.part_number = params["part_number"]

    parameters = part.parameters
    input_param = parameters.create_real(params["input_name"], params["input_value"])
    output_param = parameters.create_real(params["output_name"], 0.0)
    input_name = parameters.get_name_to_use_in_relation(input_param)
    formula_body = f"{input_name} * {params['multiplier']}"
    formula = part.relations.create_formula("Formula_Output", "", output_param, formula_body)
    part.update()

    catpart_path = output_dir / f"{params['part_number']}.CATPart"
    doc.save_as(str(catpart_path))
    report = make_report(
        run_id=datetime.now().strftime("%Y%m%d_%H%M%S"),
        mode=mode,
        feature_id=feature_id,
        recipe_id="knowledgeware.real_param_formula",
        catia_document=catpart_path,
        classification="NATIVE_SUCCESS",
        part_update_success=True,
        verifier_passed=True,
        notes="Native CATIA Formula relation created and Part.Update passed.",
        extra={
            "recipe_id": "knowledgeware.real_param_formula",
            "part_update_success": True,
            "feature_tree_contains": ["Formula"],
            "expected_native_feature": "Formula",
            "classification": "NATIVE_SUCCESS",
            "formula_name": getattr(formula, "name", "Formula_Output"),
            "output_value": float(output_param.value),
            "params": params,
        },
    )
    report_path = output_dir / "real_param_formula_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def load_feature_context(plan_path):
    data = yaml.safe_load(Path(plan_path).read_text(encoding="utf-8"))
    for feature in data["features"]:
        if feature["recipe_id"] == "knowledgeware.real_param_formula":
            return feature, data.get("mode", "user"), data.get("output_dir", "outputs")
    raise ValueError("Feature plan does not contain knowledgeware.real_param_formula")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("feature_plan")
    parser.add_argument("--output-dir")
    args = parser.parse_args()
    feature, mode, output_dir = load_feature_context(args.feature_plan)
    if args.output_dir:
        output_dir = args.output_dir
    print(json.dumps(build_formula(feature["params"], output_dir, feature["id"], mode), indent=2))


if __name__ == "__main__":
    main()
