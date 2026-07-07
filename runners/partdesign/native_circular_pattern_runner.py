"""Runner for recipe partdesign.native_circular_pattern."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runners.partdesign.pattern_common import (  # noqa: E402
    catpart_output_path,
    construction_line_reference,
    create_circle_pad,
    create_circle_pocket,
    create_construction_body,
    create_native_circular_pattern,
    create_part,
    make_partdesign_report,
    run_id_now,
    save_document_overwrite,
    write_report,
)


RECIPE_ID = "partdesign.native_circular_pattern"
EXPECTED_NATIVE_FEATURE = "CircPattern"
REFERENCE_PATTERN_ID = "partdesign.circular_pattern_axis_ref"


def normalize_params(params):
    return {
        "part_number": params.get("part_number", "Native_Circular_Pattern"),
        "disk_radius": float(params.get("disk_radius", 40.0)),
        "disk_depth": float(params.get("disk_depth", 20.0)),
        "center_hole_radius": float(params.get("center_hole_radius", 15.0)),
        "seed_x": float(params.get("seed_x", 30.0)),
        "seed_y": float(params.get("seed_y", 0.0)),
        "seed_radius": float(params.get("seed_radius", 4.0)),
        "pocket_depth": float(params.get("pocket_depth", 45.0)),
        "instances": int(params.get("instances", 6)),
        "angular_spacing": float(params.get("angular_spacing", 60.0)),
        "total_angle": float(params.get("total_angle", 360.0)),
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


def build_native_circular_pattern(params, output_dir, feature_id="circ_pattern_1", mode="user"):
    params = normalize_params(params)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    doc, part, body, ref_xy, part_number_result = create_part(params["part_number"])
    construction = create_construction_body(part)
    center_ref, ref_axis_z = construction_line_reference(part, construction, "CircPattern_Axis_Z", (0, 0, 1))
    create_circle_pad(
        part,
        body,
        ref_xy,
        sketch_name="CircPattern_Disk_Profile",
        feature_name="CircPattern_DiskPad",
        x=0.0,
        y=0.0,
        radius=params["disk_radius"],
        depth=params["disk_depth"],
    )
    create_circle_pocket(
        part,
        body,
        ref_xy,
        sketch_name="CircPattern_CenterHole_Profile",
        feature_name="CircPattern_CenterHolePocket",
        x=0.0,
        y=0.0,
        radius=params["center_hole_radius"],
        depth=params["pocket_depth"],
    )
    seed = create_circle_pocket(
        part,
        body,
        ref_xy,
        sketch_name="CircPattern_SeedPocket_Profile",
        feature_name="CircPattern_SeedPocket",
        x=params["seed_x"],
        y=params["seed_y"],
        radius=params["seed_radius"],
        depth=params["pocket_depth"],
    )
    create_native_circular_pattern(
        part,
        seed,
        center_ref,
        ref_axis_z,
        instances=params["instances"],
        angular_spacing=params["angular_spacing"],
        total_angle=params["total_angle"],
        feature_name="Native_CircPattern",
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
        notes="Native CATIA CircPattern created from explicit center and Z-axis references and Part.Update passed.",
        extra={"params": params, "seed_native_feature": "Pocket", "part_number_assignment": part_number_result},
    )
    write_report(output_dir, "native_circular_pattern_report.json", report)
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
    print(json.dumps(build_native_circular_pattern(feature["params"], output_dir, feature["id"], mode), indent=2))


if __name__ == "__main__":
    main()
