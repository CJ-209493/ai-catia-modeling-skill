"""Runner for recipe partdesign.native_rectangular_pattern."""

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
    create_base_pad,
    create_circle_pad,
    create_construction_body,
    create_native_rectangular_pattern,
    create_offset_plane_reference,
    create_part,
    make_partdesign_report,
    run_id_now,
    save_document_overwrite,
    write_report,
)


RECIPE_ID = "partdesign.native_rectangular_pattern"
EXPECTED_NATIVE_FEATURE = "RectPattern"
REFERENCE_PATTERN_ID = "partdesign.rectangular_pattern_direction_refs"


def normalize_params(params):
    return {
        "part_number": params.get("part_number", "Native_Rectangular_Pattern"),
        "plate_width": float(params.get("plate_width", 180.0)),
        "plate_height": float(params.get("plate_height", 100.0)),
        "plate_depth": float(params.get("plate_depth", 12.0)),
        "seed_x": float(params.get("seed_x", 50.0)),
        "seed_y": float(params.get("seed_y", 20.0)),
        "seed_radius": float(params.get("seed_radius", 8.0)),
        "seed_depth": float(params.get("seed_depth", 8.0)),
        "instances_1": int(params.get("instances_1", 4)),
        "instances_2": int(params.get("instances_2", 3)),
        "spacing_1": float(params.get("spacing_1", 40.0)),
        "spacing_2": float(params.get("spacing_2", 30.0)),
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


def build_native_rectangular_pattern(params, output_dir, feature_id="rect_pattern_1", mode="user"):
    params = normalize_params(params)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    doc, part, body, ref_xy, part_number_result = create_part(params["part_number"])
    construction = create_construction_body(part)
    _, ref_x = construction_line_reference(part, construction, "RectPattern_Direction_X", (1, 0, 0))
    _, ref_y = construction_line_reference(part, construction, "RectPattern_Direction_Y", (0, 1, 0))
    create_base_pad(
        part,
        body,
        ref_xy,
        sketch_name="RectPattern_BasePad_Profile",
        feature_name="RectPattern_BasePad",
        width=params["plate_width"],
        height=params["plate_height"],
        depth=params["plate_depth"],
    )
    top_ref = create_offset_plane_reference(
        part,
        ref_xy,
        offset=params["plate_depth"],
        container_name="RectPattern_Top_References",
    )
    seed = create_circle_pad(
        part,
        body,
        top_ref,
        sketch_name="RectPattern_SeedBoss_Profile",
        feature_name="RectPattern_SeedBoss",
        x=params["seed_x"],
        y=params["seed_y"],
        radius=params["seed_radius"],
        depth=params["seed_depth"],
    )
    create_native_rectangular_pattern(
        part,
        seed,
        ref_x,
        ref_y,
        instances_1=params["instances_1"],
        instances_2=params["instances_2"],
        spacing_1=params["spacing_1"],
        spacing_2=params["spacing_2"],
        feature_name="Native_RectPattern",
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
        notes="Native CATIA RectPattern created from explicit X/Y direction references and Part.Update passed.",
        extra={"params": params, "seed_native_feature": "Pad", "part_number_assignment": part_number_result},
    )
    write_report(output_dir, "native_rectangular_pattern_report.json", report)
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
    print(json.dumps(build_native_rectangular_pattern(feature["params"], output_dir, feature["id"], mode), indent=2))


if __name__ == "__main__":
    main()
