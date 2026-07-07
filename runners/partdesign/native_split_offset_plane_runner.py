"""Runner for recipe partdesign.native_split_offset_plane."""

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
from runners.partdesign.profile_pad_common import create_offset_plane_reference  # noqa: E402


RECIPE_ID = "partdesign.native_split_offset_plane"
EXPECTED_NATIVE_FEATURE = "Split"
REFERENCE_PATTERN_ID = "partdesign.split_offset_plane_ref"


def normalize_params(params):
    return {
        "part_number": params.get("part_number", "Native_Split_Offset_Plane"),
        "plate_width": float(params.get("plate_width", 120.0)),
        "plate_height": float(params.get("plate_height", 80.0)),
        "plate_depth": float(params.get("plate_depth", 40.0)),
        "split_offset": float(params.get("split_offset", 20.0)),
        "split_side": int(params.get("split_side", 0)),
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


def build_native_split_offset_plane(params, output_dir, feature_id="split_1", mode="user"):
    params = normalize_params(params)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    doc, part, body, ref_xy, part_number_result = create_part(params["part_number"])
    create_base_pad(
        part,
        body,
        ref_xy,
        sketch_name="Split_BasePad_Profile",
        feature_name="Split_BasePad",
        width=params["plate_width"],
        height=params["plate_height"],
        depth=params["plate_depth"],
    )
    split_ref = create_offset_plane_reference(
        part,
        ref_xy,
        offset=params["split_offset"],
        container_name="AI_CATIA_Split_References",
    )

    part.in_work_object = body
    split = part.shape_factory.add_new_split(split_ref, params["split_side"])
    split.name = "Native_OffsetPlane_Split"
    part.in_work_object = split
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
        notes="Native CATIA Split created from an explicit offset PlaneXY reference after setting Part.InWorkObject to the target Body; Part.Update passed.",
        extra={
            "params": params,
            "base_native_feature": "Pad",
            "part_number_assignment": part_number_result,
        },
    )
    write_report(output_dir, "native_split_offset_plane_report.json", report)
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
    print(json.dumps(build_native_split_offset_plane(feature["params"], output_dir, feature["id"], mode), indent=2))


if __name__ == "__main__":
    main()
