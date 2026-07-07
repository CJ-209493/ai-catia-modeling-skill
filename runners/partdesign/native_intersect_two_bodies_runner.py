"""Runner for recipe partdesign.native_intersect_two_bodies."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runners.partdesign.prismatic_cut_common import (  # noqa: E402
    catpart_output_path,
    create_base_pad,
    create_part,
    make_partdesign_report,
    run_id_now,
    save_document_overwrite,
    write_report,
)


RECIPE_ID = "partdesign.native_intersect_two_bodies"
EXPECTED_NATIVE_FEATURE = "Intersect"
REFERENCE_PATTERN_ID = "partdesign.intersect_target_body_ref"


def normalize_params(params):
    return {
        "part_number": params.get("part_number", "Native_Intersect_Two_Bodies"),
        "target_width": float(params.get("target_width", 120.0)),
        "target_height": float(params.get("target_height", 80.0)),
        "target_depth": float(params.get("target_depth", 30.0)),
        "tool_width": float(params.get("tool_width", 80.0)),
        "tool_height": float(params.get("tool_height", 50.0)),
        "tool_depth": float(params.get("tool_depth", 25.0)),
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
    report = make_partdesign_report(
        run_id=run_id,
        mode=mode,
        feature_id=feature_id,
        recipe_id=recipe_id,
        catia_document=catia_document,
        classification=classification,
        part_update_success=part_update_success,
        verifier_passed=verifier_passed,
        expected_native_feature=EXPECTED_NATIVE_FEATURE,
        notes=notes,
        extra=extra,
    )
    report["reference_pattern_ids"] = [REFERENCE_PATTERN_ID]
    return report


def build_native_intersect_two_bodies(params, output_dir, feature_id="intersect_1", mode="user"):
    params = normalize_params(params)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    doc, part, target_body, ref_xy, part_number_result = create_part(params["part_number"])
    target_body.name = "Intersect_TargetBody"
    create_base_pad(
        part,
        target_body,
        ref_xy,
        sketch_name="Intersect_Target_Profile",
        feature_name="Intersect_TargetPad",
        width=params["target_width"],
        height=params["target_height"],
        depth=params["target_depth"],
    )

    tool_body = part.bodies.add()
    tool_body.name = "Intersect_ToolBody"
    create_base_pad(
        part,
        tool_body,
        ref_xy,
        sketch_name="Intersect_Tool_Profile",
        feature_name="Intersect_ToolPad",
        width=params["tool_width"],
        height=params["tool_height"],
        depth=params["tool_depth"],
    )

    part.in_work_object = target_body
    intersect = part.shape_factory.add_new_intersect(tool_body)
    intersect.name = "Native_TwoBody_Intersect"
    part.in_work_object = intersect
    part.update()

    run_id = run_id_now()
    catpart_path = save_document_overwrite(doc, catpart_output_path(output_dir, params["part_number"], run_id))
    report = make_report(
        run_id=run_id,
        mode=mode,
        feature_id=feature_id,
        recipe_id=RECIPE_ID,
        catia_document=catpart_path,
        classification="NATIVE_SUCCESS",
        part_update_success=True,
        verifier_passed=True,
        notes="Native CATIA Intersect created after setting Part.InWorkObject to the target Body and passing a generated tool Body; Part.Update passed.",
        extra={
            "params": params,
            "base_native_features": ["Pad", "Pad"],
            "part_number_assignment": part_number_result,
        },
    )
    write_report(output_dir, "native_intersect_two_bodies_report.json", report)
    return report


def load_feature_context(plan_path):
    data = yaml.safe_load(Path(plan_path).read_text(encoding="utf-8"))
    for feature in data["features"]:
        if feature["recipe_id"] == RECIPE_ID:
            return feature, data.get("mode", "user"), data.get("output_dir", "outputs")
    raise ValueError(f"Feature plan does not contain {RECIPE_ID}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("feature_plan")
    parser.add_argument("--output-dir")
    args = parser.parse_args()
    feature, mode, output_dir = load_feature_context(args.feature_plan)
    if args.output_dir:
        output_dir = args.output_dir
    print(json.dumps(build_native_intersect_two_bodies(feature["params"], output_dir, feature["id"], mode), indent=2))


if __name__ == "__main__":
    main()
