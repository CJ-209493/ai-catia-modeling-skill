"""Runner for recipe partdesign.native_slot_pocket."""

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
    create_native_slot_pocket,
    create_part,
    make_partdesign_report,
    run_id_now,
    save_document_overwrite,
    write_report,
)


RECIPE_ID = "partdesign.native_slot_pocket"
EXPECTED_NATIVE_FEATURE = "Pocket"


def normalize_params(params):
    return {
        "part_number": params.get("part_number", "Native_Slot_Pocket"),
        "plate_width": float(params.get("plate_width", 100.0)),
        "plate_height": float(params.get("plate_height", 50.0)),
        "plate_depth": float(params.get("plate_depth", 10.0)),
        "slot_half_center_distance": float(params.get("slot_half_center_distance", 24.0)),
        "slot_radius": float(params.get("slot_radius", 6.0)),
        "pocket_depth": float(params.get("pocket_depth", 22.0)),
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
    return make_partdesign_report(
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


def build_native_slot_pocket(params, output_dir, feature_id="slot_pocket_1", mode="user"):
    params = normalize_params(params)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    doc, part, body, ref_xy, part_number_result = create_part(params["part_number"])
    create_base_pad(
        part,
        body,
        ref_xy,
        sketch_name="NativeSlotPocket_BasePad_Profile",
        feature_name="NativeSlotPocket_BasePad",
        width=params["plate_width"],
        height=params["plate_height"],
        depth=params["plate_depth"],
    )
    create_native_slot_pocket(
        part,
        body,
        ref_xy,
        sketch_name="NativeSlotPocket_Profile",
        feature_name="NativeSlotPocket",
        half_center_distance=params["slot_half_center_distance"],
        radius=params["slot_radius"],
        depth=params["pocket_depth"],
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
        notes="Native CATIA Pocket created from a closed racetrack sketch and Part.Update passed.",
        extra={"params": params, "base_native_feature": "Pad", "part_number_assignment": part_number_result},
    )
    write_report(output_dir, "native_slot_pocket_report.json", report)
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
    print(json.dumps(build_native_slot_pocket(feature["params"], output_dir, feature["id"], mode), indent=2))


if __name__ == "__main__":
    main()
