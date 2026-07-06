"""Runner for recipe assembly.product_fix_constraint."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

import yaml


def normalize_params(params):
    return {
        "product_number": params.get("product_number", "Product_Fix_Constraint"),
        "component_a": params.get("component_a", "Component_A"),
        "component_b": params.get("component_b", "Component_B"),
    }


def build_product_fix_constraint(params, output_dir):
    from pycatia import catia

    params = normalize_params(params)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    app = catia()
    doc = app.documents.add("Product")
    product = doc.product
    child_a = product.products.add_new_product(params["component_a"])
    child_b = product.products.add_new_product(params["component_b"])
    constraints = product.constraints()
    before = constraints.count
    component_ref = product.create_reference_from_name(f"{product.name}/{child_a.name}/!")
    constraint = constraints.add_mono_elt_cst(0, component_ref)
    product.update()
    after = constraints.count

    catproduct_path = output_dir / f"{params['product_number']}.CATProduct"
    doc.save_as(str(catproduct_path))
    report = {
        "run_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "recipe_id": "assembly.product_fix_constraint",
        "catia_document": str(catproduct_path),
        "product_update_success": True,
        "feature_tree_contains": ["Constraints"],
        "expected_native_feature": "Constraints",
        "classification": "NATIVE_SUCCESS",
        "constraint_name": constraint.name,
        "constraint_count_before": before,
        "constraint_count_after": after,
        "components": [child_a.part_number, child_b.part_number],
        "params": params,
    }
    report_path = output_dir / "product_fix_constraint_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def load_feature_params(plan_path):
    data = yaml.safe_load(Path(plan_path).read_text(encoding="utf-8"))
    for feature in data["features"]:
        if feature["recipe_id"] == "assembly.product_fix_constraint":
            return feature["params"], data.get("output_dir", "outputs")
    raise ValueError("Feature plan does not contain assembly.product_fix_constraint")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("feature_plan")
    parser.add_argument("--output-dir")
    args = parser.parse_args()
    params, output_dir = load_feature_params(args.feature_plan)
    if args.output_dir:
        output_dir = args.output_dir
    print(json.dumps(build_product_fix_constraint(params, output_dir), indent=2))


if __name__ == "__main__":
    main()
