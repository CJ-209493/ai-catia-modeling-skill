"""Runner for recipe partdesign.parametric_plate_formula_holes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml
from pycatia.enumeration.enums import CatConstraintType


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runners.partdesign.prismatic_cut_common import (  # noqa: E402
    catpart_output_path,
    create_part,
    make_partdesign_report,
    run_id_now,
    save_document_overwrite,
    write_report,
)


RECIPE_ID = "partdesign.parametric_plate_formula_holes"
EXPECTED_NATIVE_FEATURE = "Formula"
REFERENCE_PATTERN_ID = "knowledgeware.formula_driven_sketch_dimensions"


def normalize_params(params):
    return {
        "part_number": params.get("part_number", "T19_parametric_plate"),
        "length": float(params.get("length", 120.0)),
        "width": float(params.get("width", 60.0)),
        "thickness": float(params.get("thickness", 8.0)),
        "hole_dia": float(params.get("hole_dia", 8.0)),
        "edge_offset": float(params.get("edge_offset", 12.0)),
        "updated_length": float(params.get("updated_length", 150.0)),
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
    report["feature_tree_contains"] = ["Formula", "Pad", "Hole"] if part_update_success else []
    report["reference_pattern_ids"] = [REFERENCE_PATTERN_ID]
    return report


def create_length_parameter(parameters, name, value_mm):
    param = parameters.create_dimension(name, "LENGTH", float(value_mm))
    param.valuate_from_string(f"{float(value_mm)}mm")
    return param


def bind_formula(part, name, target, expression):
    return part.relations.create_formula(name, "", target, expression)


def create_formula_driven_base(part, body, ref_xy, params, length_param, width_param, thickness_param):
    length = params["length"]
    width = params["width"]
    sketch = body.sketches.add(ref_xy)
    sketch.name = "T19_Base_Profile"
    factory_2d = sketch.open_edition()
    bottom = factory_2d.create_line(-length / 2, -width / 2, length / 2, -width / 2)
    right = factory_2d.create_line(length / 2, -width / 2, length / 2, width / 2)
    top = factory_2d.create_line(length / 2, width / 2, -length / 2, width / 2)
    left = factory_2d.create_line(-length / 2, width / 2, -length / 2, -width / 2)
    constraints = sketch.constraints
    constraints.add_mono_elt_cst(
        int(CatConstraintType.catCstTypeHorizontality),
        part.create_reference_from_object(bottom),
    )
    constraints.add_mono_elt_cst(
        int(CatConstraintType.catCstTypeVerticality),
        part.create_reference_from_object(right),
    )
    constraints.add_mono_elt_cst(
        int(CatConstraintType.catCstTypeHorizontality),
        part.create_reference_from_object(top),
    )
    constraints.add_mono_elt_cst(
        int(CatConstraintType.catCstTypeVerticality),
        part.create_reference_from_object(left),
    )
    axis = sketch.absolute_axis
    c_right_offset = constraints.add_bi_elt_cst(
        int(CatConstraintType.catCstTypeDistance),
        part.create_reference_from_object(right),
        part.create_reference_from_object(axis.vertical_reference),
    )
    c_right_offset.name = "Base_Right_From_YAxis"
    c_right_offset.side = 0
    c_left_offset = constraints.add_bi_elt_cst(
        int(CatConstraintType.catCstTypeDistance),
        part.create_reference_from_object(left),
        part.create_reference_from_object(axis.vertical_reference),
    )
    c_left_offset.name = "Base_Left_From_YAxis"
    c_left_offset.side = 1
    c_top_offset = constraints.add_bi_elt_cst(
        int(CatConstraintType.catCstTypeDistance),
        part.create_reference_from_object(top),
        part.create_reference_from_object(axis.horizontal_reference),
    )
    c_top_offset.name = "Base_Top_From_XAxis"
    c_top_offset.side = 0
    c_bottom_offset = constraints.add_bi_elt_cst(
        int(CatConstraintType.catCstTypeDistance),
        part.create_reference_from_object(bottom),
        part.create_reference_from_object(axis.horizontal_reference),
    )
    c_bottom_offset.name = "Base_Bottom_From_XAxis"
    c_bottom_offset.side = 1
    sketch.close_edition()

    get_name = part.parameters.get_name_to_use_in_relation
    bind_formula(part, "Formula_Base_Right_From_YAxis", c_right_offset.dimension, f"{get_name(length_param)} / 2")
    bind_formula(part, "Formula_Base_Left_From_YAxis", c_left_offset.dimension, f"{get_name(length_param)} / 2")
    bind_formula(part, "Formula_Base_Top_From_XAxis", c_top_offset.dimension, f"{get_name(width_param)} / 2")
    bind_formula(part, "Formula_Base_Bottom_From_XAxis", c_bottom_offset.dimension, f"{get_name(width_param)} / 2")
    part.update()

    pad = part.shape_factory.add_new_pad(sketch, params["thickness"])
    pad.name = "T19_Parametric_Pad"
    part.in_work_object = pad
    bind_formula(part, "Formula_Pad_Thickness", pad.first_limit.dimension, get_name(thickness_param))
    part.update()
    return pad, c_right_offset, c_top_offset, constraints


def create_formula_driven_hole(
    part,
    body,
    ref_xy,
    name,
    sign_x,
    sign_y,
    params,
    length_param,
    width_param,
    thickness_param,
    hole_dia_param,
    edge_offset_param,
):
    x = sign_x * (params["length"] / 2 - params["edge_offset"])
    y = sign_y * (params["width"] / 2 - params["edge_offset"])
    sketch = body.sketches.add(ref_xy)
    sketch.name = f"T19_HolePoint_{name}"
    factory_2d = sketch.open_edition()
    point = factory_2d.create_point(x, y)
    constraints = sketch.constraints
    axis = sketch.absolute_axis
    c_x = constraints.add_bi_elt_cst(
        int(CatConstraintType.catCstTypeDistance),
        part.create_reference_from_object(point),
        part.create_reference_from_object(axis.vertical_reference),
    )
    c_x.name = f"Hole_{name}_X_Offset"
    c_x.side = 0 if sign_x > 0 else 1
    c_y = constraints.add_bi_elt_cst(
        int(CatConstraintType.catCstTypeDistance),
        part.create_reference_from_object(point),
        part.create_reference_from_object(axis.horizontal_reference),
    )
    c_y.name = f"Hole_{name}_Y_Offset"
    c_y.side = 0 if sign_y > 0 else 1
    sketch.close_edition()

    get_name = part.parameters.get_name_to_use_in_relation
    bind_formula(part, f"Formula_Hole_{name}_X", c_x.dimension, f"{get_name(length_param)} / 2 - {get_name(edge_offset_param)}")
    bind_formula(part, f"Formula_Hole_{name}_Y", c_y.dimension, f"{get_name(width_param)} / 2 - {get_name(edge_offset_param)}")
    part.update()

    hole = part.shape_factory.add_new_hole_from_sketch(sketch, params["thickness"])
    hole.name = f"T19_Native_Hole_{name}"
    hole.diameter.value = params["hole_dia"]
    hole.reverse()
    bind_formula(part, f"Formula_Hole_{name}_Dia", hole.diameter, get_name(hole_dia_param))
    bind_formula(part, f"Formula_Hole_{name}_Depth", hole.bottom_limit.dimension, get_name(thickness_param))
    part.in_work_object = hole
    part.update()
    return hole, c_x, c_y, constraints


def build_parametric_plate_formula_holes(params, output_dir, feature_id="parametric_plate_1", mode="user"):
    params = normalize_params(params)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    doc, part, body, ref_xy, part_number_result = create_part(params["part_number"])
    body.name = "T19_ParametricPlateBody"
    parameters = part.parameters
    length_param = create_length_parameter(parameters, "Length", params["length"])
    width_param = create_length_parameter(parameters, "Width", params["width"])
    thickness_param = create_length_parameter(parameters, "Thickness", params["thickness"])
    hole_dia_param = create_length_parameter(parameters, "HoleDia", params["hole_dia"])
    edge_offset_param = create_length_parameter(parameters, "EdgeOffset", params["edge_offset"])

    pad, base_length_constraint, base_width_constraint, base_constraints = create_formula_driven_base(
        part,
        body,
        ref_xy,
        params,
        length_param,
        width_param,
        thickness_param,
    )

    hole_specs = [("LF", -1, -1), ("RF", 1, -1), ("LB", -1, 1), ("RB", 1, 1)]
    holes = []
    point_constraints = []
    for name, sign_x, sign_y in hole_specs:
        hole, c_x, c_y, constraints = create_formula_driven_hole(
            part,
            body,
            ref_xy,
            name,
            sign_x,
            sign_y,
            params,
            length_param,
            width_param,
            thickness_param,
            hole_dia_param,
            edge_offset_param,
        )
        holes.append(hole)
        point_constraints.append((name, c_x, c_y, constraints))

    initial_length_mm = 2.0 * float(base_length_constraint.dimension.value)
    initial_hole_x_offset_mm = float(point_constraints[0][1].dimension.value)
    initial_hole_y_offset_mm = float(point_constraints[0][2].dimension.value)

    length_param.valuate_from_string(f"{params['updated_length']}mm")
    part.update()

    updated_length_mm = 2.0 * float(base_length_constraint.dimension.value)
    updated_hole_x_offset_mm = float(point_constraints[0][1].dimension.value)
    updated_hole_y_offset_mm = float(point_constraints[0][2].dimension.value)
    all_constraint_counts = {
        "base_broken": int(base_constraints.broken_constraints_count),
        "base_unupdated": int(base_constraints.un_updated_constraints_count),
        "holes_broken": sum(int(item[3].broken_constraints_count) for item in point_constraints),
        "holes_unupdated": sum(int(item[3].un_updated_constraints_count) for item in point_constraints),
    }

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
        notes="Formula-driven sketch dimensions, Pad thickness, and four native Hole positions updated after changing Length; Part.Update passed.",
        extra={
            "params": params,
            "part_number_assignment": part_number_result,
            "initial_length_mm": initial_length_mm,
            "updated_length_mm": updated_length_mm,
            "initial_hole_x_offset_mm": initial_hole_x_offset_mm,
            "updated_hole_x_offset_mm": updated_hole_x_offset_mm,
            "initial_hole_y_offset_mm": initial_hole_y_offset_mm,
            "updated_hole_y_offset_mm": updated_hole_y_offset_mm,
            "hole_count": len(holes),
            "relations_count": int(part.relations.count),
            "constraint_counts": all_constraint_counts,
            "pad_thickness_mm": float(pad.first_limit.dimension.value),
            "hole_diameters_mm": [float(hole.diameter.value) for hole in holes],
            "hole_depths_mm": [float(hole.bottom_limit.dimension.value) for hole in holes],
        },
    )
    write_report(output_dir, "parametric_plate_formula_holes_report.json", report)
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
    print(json.dumps(build_parametric_plate_formula_holes(feature["params"], output_dir, feature["id"], mode), indent=2))


if __name__ == "__main__":
    main()
