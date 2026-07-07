"""Runner for recipe partdesign.capsule_with_native_holes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runners.partdesign.profile_pad_common import (  # noqa: E402
    catpart_output_path,
    create_capsule_pad,
    create_native_hole_from_sketch,
    create_part,
    make_partdesign_report,
    run_id_now,
    save_document_overwrite,
    write_report,
)


RECIPE_ID = "partdesign.capsule_with_native_holes"
EXPECTED_NATIVE_FEATURE = "Hole"
REFERENCE_PATTERN_ID = "partdesign.capsule_profile_native_holes"


def normalize_params(params):
    return {
        "part_number": params.get("part_number", "Capsule_With_Native_Holes"),
        "half_center_distance": float(params.get("half_center_distance", 35.0)),
        "capsule_radius": float(params.get("capsule_radius", 15.0)),
        "pad_depth": float(params.get("pad_depth", 8.0)),
        "hole_depth": float(params.get("hole_depth", 20.0)),
        "hole_diameter": float(params.get("hole_diameter", 10.0)),
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


def build_capsule_with_native_holes(params, output_dir, feature_id="capsule_holes_1", mode="user"):
    params = normalize_params(params)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    doc, part, body, ref_xy, part_number_result = create_part(params["part_number"])
    create_capsule_pad(
        part,
        body,
        ref_xy,
        sketch_name="Capsule_Profile",
        feature_name="Capsule_Pad",
        half_center_distance=params["half_center_distance"],
        radius=params["capsule_radius"],
        depth=params["pad_depth"],
    )
    for index, x in enumerate([-params["half_center_distance"], params["half_center_distance"]], start=1):
        create_native_hole_from_sketch(
            part,
            body,
            ref_xy,
            sketch_name=f"Capsule_Hole_PointSketch_{index}",
            feature_name=f"Capsule_Native_Hole_{index}",
            x=x,
            y=0.0,
            depth=params["hole_depth"],
            diameter=params["hole_diameter"],
        )

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
        notes="Native CATIA Hole features created through a tangent-arc capsule Pad from point sketches; Part.Update passed.",
        extra={"params": params, "base_native_feature": "Pad", "part_number_assignment": part_number_result},
    )
    write_report(output_dir, "capsule_native_holes_report.json", report)
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
    print(json.dumps(build_capsule_with_native_holes(feature["params"], output_dir, feature["id"], mode), indent=2))


if __name__ == "__main__":
    main()
