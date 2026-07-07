"""Runner for recipe partdesign.native_v_pulley_shaft."""

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
    create_native_shaft_from_profile,
    create_part,
    make_revolution_report,
    run_id_now,
    save_document_overwrite,
    write_report,
)


RECIPE_ID = "partdesign.native_v_pulley_shaft"
EXPECTED_NATIVE_FEATURE = "Shaft"
REFERENCE_PATTERN_IDS = ["partdesign.sketch_revolution_axis", "partdesign.v_pulley_shaft_profile"]


def normalize_params(params):
    return {
        "part_number": params.get("part_number", "Native_V_Pulley_Shaft"),
        "width": float(params.get("width", 24.0)),
        "bore_radius": float(params.get("bore_radius", 10.0)),
        "outer_radius": float(params.get("outer_radius", 50.0)),
        "groove_start": float(params.get("groove_start", 8.0)),
        "groove_mid": float(params.get("groove_mid", 12.0)),
        "groove_end": float(params.get("groove_end", 16.0)),
        "groove_valley_radius": float(params.get("groove_valley_radius", 42.0)),
    }


def draw_v_pulley_profile(factory_2d, params):
    width = params["width"]
    bore_radius = params["bore_radius"]
    outer_radius = params["outer_radius"]
    groove_start = params["groove_start"]
    groove_mid = params["groove_mid"]
    groove_end = params["groove_end"]
    groove_valley_radius = params["groove_valley_radius"]

    factory_2d.create_line(0.0, bore_radius, 0.0, outer_radius)
    factory_2d.create_line(0.0, outer_radius, groove_start, outer_radius)
    factory_2d.create_line(groove_start, outer_radius, groove_mid, groove_valley_radius)
    factory_2d.create_line(groove_mid, groove_valley_radius, groove_end, outer_radius)
    factory_2d.create_line(groove_end, outer_radius, width, outer_radius)
    factory_2d.create_line(width, outer_radius, width, bore_radius)
    factory_2d.create_line(width, bore_radius, 0.0, bore_radius)


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
    report = make_revolution_report(
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
    report["reference_pattern_ids"] = REFERENCE_PATTERN_IDS
    return report


def build_native_v_pulley_shaft(params, output_dir, feature_id="v_pulley_shaft_1", mode="user"):
    params = normalize_params(params)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    doc, part, body, ref_xy, part_number_result = create_part(params["part_number"])
    create_native_shaft_from_profile(
        part,
        body,
        ref_xy,
        sketch_name="NativeVPulley_Shaft_Profile",
        feature_name="NativeVPulley_Shaft",
        axis_length=params["width"],
        draw_profile=lambda factory_2d: draw_v_pulley_profile(factory_2d, params),
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
        notes="Native CATIA Shaft created from one V-pulley half-profile with same-sketch CenterLine; Part.Update passed.",
        extra={"params": params, "part_number_assignment": part_number_result},
    )
    write_report(output_dir, "native_v_pulley_shaft_report.json", report)
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
    print(json.dumps(build_native_v_pulley_shaft(feature["params"], output_dir, feature["id"], mode), indent=2))


if __name__ == "__main__":
    main()
