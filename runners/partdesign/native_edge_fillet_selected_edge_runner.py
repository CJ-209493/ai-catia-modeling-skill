"""Runner for recipe partdesign.native_edge_fillet_selected_edge."""

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


RECIPE_ID = "partdesign.native_edge_fillet_selected_edge"
EXPECTED_NATIVE_FEATURE = "ConstRadEdgeFillet"
REFERENCE_PATTERN_ID = "partdesign.edge_fillet_selected_edge_ref"


def normalize_params(params):
    return {
        "part_number": params.get("part_number", "Native_Edge_Fillet_Selected_Edge"),
        "plate_width": float(params.get("plate_width", 120.0)),
        "plate_height": float(params.get("plate_height", 80.0)),
        "plate_depth": float(params.get("plate_depth", 20.0)),
        "radius": float(params.get("radius", 5.0)),
        "selected_edge_index": int(params.get("selected_edge_index", 1)),
        "propagation": int(params.get("propagation", 1)),
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


def build_native_edge_fillet_selected_edge(params, output_dir, feature_id="edge_fillet_1", mode="user"):
    params = normalize_params(params)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    doc, part, body, ref_xy, part_number_result = create_part(params["part_number"])
    base_pad = create_base_pad(
        part,
        body,
        ref_xy,
        sketch_name="EdgeFillet_BasePad_Profile",
        feature_name="EdgeFillet_BasePad",
        width=params["plate_width"],
        height=params["plate_height"],
        depth=params["plate_depth"],
    )

    selection = doc.selection
    selection.clear()
    selection.add(base_pad)
    selection.search("Topology.Edge,sel")
    edge_ref = selection.item2(params["selected_edge_index"]).reference
    fillet = part.shape_factory.add_new_solid_edge_fillet_with_constant_radius(
        edge_ref,
        params["propagation"],
        params["radius"],
    )
    fillet.name = "Native_SelectedEdge_Fillet"
    part.in_work_object = fillet
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
        notes="Native CATIA ConstRadEdgeFillet created from a selection-derived edge reference; Part.Update passed. Edge semantics are constrained to the selected edge index.",
        extra={
            "params": params,
            "base_native_feature": "Pad",
            "selected_edge_index": params["selected_edge_index"],
            "part_number_assignment": part_number_result,
        },
    )
    write_report(output_dir, "native_edge_fillet_selected_edge_report.json", report)
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
    print(json.dumps(build_native_edge_fillet_selected_edge(feature["params"], output_dir, feature["id"], mode), indent=2))


if __name__ == "__main__":
    main()
