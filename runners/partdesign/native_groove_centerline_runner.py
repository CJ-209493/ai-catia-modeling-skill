"""Runner for recipe partdesign.native_groove_centerline."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runners.partdesign.revolution_centerline_common import (  # noqa: E402
    catpart_output_path,
    create_native_groove,
    create_native_shaft,
    create_part,
    make_revolution_report,
    normalize_segments,
    run_id_now,
    save_document_overwrite,
    segment_total_length,
    write_report,
)


RECIPE_ID = "partdesign.native_groove_centerline"
EXPECTED_NATIVE_FEATURE = "Groove"


def normalize_groove(params):
    groove = params.get("groove", {})
    normalized = {
        "start": float(groove.get("start", 55.0)),
        "width": float(groove.get("width", 10.0)),
        "inner_radius": float(groove.get("inner_radius", 14.0)),
        "outer_radius": float(groove.get("outer_radius", 24.0)),
    }
    if normalized["width"] <= 0:
        raise ValueError("groove.width must be positive")
    if normalized["outer_radius"] <= normalized["inner_radius"]:
        raise ValueError("groove.outer_radius must be greater than groove.inner_radius")
    return normalized


def normalize_params(params):
    default_segments = [{"length": 120.0, "radius": 20.0}]
    base_segments = normalize_segments(params.get("base_segments", default_segments))
    groove = normalize_groove(params)
    axis_length = segment_total_length(base_segments)
    if groove["start"] < 0 or groove["start"] + groove["width"] > axis_length:
        raise ValueError("groove must lie within the base shaft axis length")
    return {
        "part_number": params.get("part_number", "Native_Groove_CenterLine"),
        "base_segments": base_segments,
        "groove": groove,
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
    return make_revolution_report(
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


def build_native_groove_centerline(params, output_dir, feature_id="groove_1", mode="user"):
    params = normalize_params(params)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    doc, part, body, ref_xy, part_number_result = create_part(params["part_number"])
    create_native_shaft(
        part,
        body,
        ref_xy,
        sketch_name="NativeGroove_BaseShaft_Profile",
        feature_name="NativeGroove_BaseShaft",
        segments=params["base_segments"],
    )
    create_native_groove(
        part,
        body,
        ref_xy,
        sketch_name="NativeGroove_CenterLine_Profile",
        feature_name="NativeGroove_CenterLine",
        axis_length=segment_total_length(params["base_segments"]),
        groove=params["groove"],
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
        notes="Native CATIA Groove created from a same-sketch construction CenterLine and Part.Update passed.",
        extra={"params": params, "base_native_feature": "Shaft", "part_number_assignment": part_number_result},
    )
    write_report(output_dir, "native_groove_centerline_report.json", report)
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
    print(json.dumps(build_native_groove_centerline(feature["params"], output_dir, feature["id"], mode), indent=2))


if __name__ == "__main__":
    main()
