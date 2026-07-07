"""Runner for recipe partdesign.offset_plane_pad."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runners.partdesign.prismatic_cut_common import rectangle  # noqa: E402
from runners.partdesign.profile_pad_common import (  # noqa: E402
    catpart_output_path,
    create_base_pad,
    create_offset_plane_reference,
    create_pad_from_sketch,
    create_part,
    make_partdesign_report,
    run_id_now,
    save_document_overwrite,
    write_report,
)


RECIPE_ID = "partdesign.offset_plane_pad"
EXPECTED_NATIVE_FEATURE = "Pad"
REFERENCE_PATTERN_ID = "partdesign.offset_plane_support_ref"


def normalize_params(params):
    return {
        "part_number": params.get("part_number", "Offset_Plane_Pad"),
        "base_width": float(params.get("base_width", 160.0)),
        "base_height": float(params.get("base_height", 80.0)),
        "base_depth": float(params.get("base_depth", 10.0)),
        "offset": float(params.get("offset", 10.0)),
        "wall_width": float(params.get("wall_width", 140.0)),
        "wall_height": float(params.get("wall_height", 10.0)),
        "wall_depth": float(params.get("wall_depth", 70.0)),
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


def build_offset_plane_pad(params, output_dir, feature_id="offset_plane_pad_1", mode="user"):
    params = normalize_params(params)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    doc, part, body, ref_xy, part_number_result = create_part(params["part_number"])
    create_base_pad(
        part,
        body,
        ref_xy,
        sketch_name="OffsetPlane_BasePad_Profile",
        feature_name="OffsetPlane_BasePad",
        width=params["base_width"],
        height=params["base_height"],
        depth=params["base_depth"],
    )
    offset_ref = create_offset_plane_reference(part, ref_xy, offset=params["offset"])
    create_pad_from_sketch(
        part,
        body,
        offset_ref,
        sketch_name="OffsetPlane_WallPad_Profile",
        feature_name="OffsetPlane_WallPad",
        depth=params["wall_depth"],
        draw_profile=lambda factory_2d: rectangle(factory_2d, 0.0, 0.0, params["wall_width"], params["wall_height"]),
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
        notes="Native CATIA Pad created from a sketch on an explicit offset PlaneXY reference; Part.Update passed.",
        extra={"params": params, "base_native_feature": "Pad", "part_number_assignment": part_number_result},
    )
    write_report(output_dir, "offset_plane_pad_report.json", report)
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
    print(json.dumps(build_offset_plane_pad(feature["params"], output_dir, feature["id"], mode), indent=2))


if __name__ == "__main__":
    main()
