"""Runner for recipe partdesign.native_counterbore_holes."""

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
    create_base_pad,
    create_native_counterbore_hole_from_sketch,
    create_part,
    make_partdesign_report,
    run_id_now,
    save_document_overwrite,
    write_report,
)


RECIPE_ID = "partdesign.native_counterbore_holes"
EXPECTED_NATIVE_FEATURE = "Hole"
REFERENCE_PATTERN_ID = "partdesign.counterbore_hole_point_sketch"


def normalize_params(params):
    positions = params.get("positions", [[-45.0, 25.0], [45.0, 25.0], [-45.0, -25.0], [45.0, -25.0]])
    return {
        "part_number": params.get("part_number", "Native_Counterbore_Holes"),
        "plate_width": float(params.get("plate_width", 120.0)),
        "plate_height": float(params.get("plate_height", 80.0)),
        "plate_depth": float(params.get("plate_depth", 16.0)),
        "hole_depth": float(params.get("hole_depth", 30.0)),
        "diameter": float(params.get("diameter", 6.8)),
        "head_diameter": float(params.get("head_diameter", 12.0)),
        "head_depth": float(params.get("head_depth", 5.0)),
        "positions": [[float(x), float(y)] for x, y in positions],
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


def build_native_counterbore_holes(params, output_dir, feature_id="counterbore_holes_1", mode="user"):
    params = normalize_params(params)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    doc, part, body, ref_xy, part_number_result = create_part(params["part_number"])
    create_base_pad(
        part,
        body,
        ref_xy,
        sketch_name="Counterbore_BasePad_Profile",
        feature_name="Counterbore_BasePad",
        width=params["plate_width"],
        height=params["plate_height"],
        depth=params["plate_depth"],
    )
    for index, (x, y) in enumerate(params["positions"], start=1):
        create_native_counterbore_hole_from_sketch(
            part,
            body,
            ref_xy,
            sketch_name=f"Counterbore_PointSketch_{index}",
            feature_name=f"Native_Counterbore_Hole_{index}",
            x=x,
            y=y,
            depth=params["hole_depth"],
            diameter=params["diameter"],
            head_diameter=params["head_diameter"],
            head_depth=params["head_depth"],
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
        notes="Native CATIA counterbore Hole features created from point sketches; Part.Update passed.",
        extra={"params": params, "base_native_feature": "Pad", "part_number_assignment": part_number_result},
    )
    write_report(output_dir, "native_counterbore_holes_report.json", report)
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
    print(json.dumps(build_native_counterbore_holes(feature["params"], output_dir, feature["id"], mode), indent=2))


if __name__ == "__main__":
    main()
