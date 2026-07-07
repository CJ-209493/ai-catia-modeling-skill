"""Shared helpers for same-sketch CenterLine Shaft/Groove runners."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


REFERENCE_PATTERN_ID = "partdesign.sketch_revolution_axis"


def normalize_segments(segments):
    normalized = []
    for index, segment in enumerate(segments or [], start=1):
        length = float(segment["length"])
        radius = float(segment["radius"])
        if length <= 0:
            raise ValueError(f"segment {index} length must be positive")
        if radius <= 0:
            raise ValueError(f"segment {index} radius must be positive")
        normalized.append({"length": length, "radius": radius})
    if not normalized:
        raise ValueError("at least one positive shaft segment is required")
    return normalized


def segment_total_length(segments):
    return sum(segment["length"] for segment in segments)


def draw_stepped_revolved_profile(factory_2d, segments):
    x = 0.0
    first_radius = segments[0]["radius"]
    factory_2d.create_line(x, 0.0, x, first_radius)
    current_radius = first_radius
    for index, segment in enumerate(segments):
        next_x = x + segment["length"]
        radius = segment["radius"]
        if radius != current_radius:
            factory_2d.create_line(x, current_radius, x, radius)
        factory_2d.create_line(x, radius, next_x, radius)
        x = next_x
        current_radius = radius
        if index + 1 < len(segments):
            next_radius = segments[index + 1]["radius"]
            if next_radius != current_radius:
                factory_2d.create_line(x, current_radius, x, next_radius)
                current_radius = next_radius
    factory_2d.create_line(x, current_radius, x, 0.0)
    factory_2d.create_line(x, 0.0, 0.0, 0.0)


def draw_rectangular_groove_profile(factory_2d, start, width, inner_radius, outer_radius):
    x1 = float(start)
    x2 = x1 + float(width)
    y1 = float(inner_radius)
    y2 = float(outer_radius)
    if x2 <= x1:
        raise ValueError("groove width must be positive")
    if y2 <= y1:
        raise ValueError("groove outer_radius must be greater than inner_radius")
    factory_2d.create_line(x1, y1, x2, y1)
    factory_2d.create_line(x2, y1, x2, y2)
    factory_2d.create_line(x2, y2, x1, y2)
    factory_2d.create_line(x1, y2, x1, y1)


def safe_set_part_number(product, part_number):
    result = {"requested": part_number, "applied": False, "error": ""}
    try:
        product.part_number = part_number
    except Exception as exc:  # CATIA can reject PartNumber in a reused live session.
        result["error"] = str(exc)
    else:
        result["applied"] = True
    return result


def create_part(part_number):
    from pycatia import catia

    app = catia()
    doc = app.documents.add("Part")
    part = doc.part
    part_number_result = safe_set_part_number(doc.product, part_number)
    body = part.bodies.item(1)
    body.name = "PartBody"
    part.in_work_object = body
    ref_xy = part.create_reference_from_object(part.origin_elements.plane_xy)
    return doc, part, body, ref_xy, part_number_result


def create_centerline_sketch(part, body, ref_xy, sketch_name, axis_length):
    part.in_work_object = body
    sketch = body.sketches.add(ref_xy)
    sketch.name = sketch_name
    factory_2d = sketch.open_edition()
    axis = factory_2d.create_line(0.0, 0.0, float(axis_length), 0.0)
    axis.name = f"{sketch_name}_RevolutionAxis"
    axis.construction = True
    return sketch, factory_2d, axis


def create_native_shaft(part, body, ref_xy, *, sketch_name, feature_name, segments):
    axis_length = segment_total_length(segments)
    sketch, factory_2d, axis = create_centerline_sketch(part, body, ref_xy, sketch_name, axis_length)
    draw_stepped_revolved_profile(factory_2d, segments)
    sketch.com_object.CenterLine = axis.com_object
    sketch.close_edition()
    part.update()
    shaft = part.shape_factory.add_new_shaft(sketch)
    shaft.name = feature_name
    part.in_work_object = shaft
    part.update()
    return shaft


def create_native_groove(part, body, ref_xy, *, sketch_name, feature_name, axis_length, groove):
    sketch, factory_2d, axis = create_centerline_sketch(part, body, ref_xy, sketch_name, axis_length)
    draw_rectangular_groove_profile(
        factory_2d,
        groove["start"],
        groove["width"],
        groove["inner_radius"],
        groove["outer_radius"],
    )
    sketch.com_object.CenterLine = axis.com_object
    sketch.close_edition()
    part.update()
    groove_feature = part.shape_factory.add_new_groove(sketch)
    groove_feature.name = feature_name
    part.in_work_object = groove_feature
    part.update()
    return groove_feature


def make_revolution_report(
    *,
    run_id,
    mode,
    feature_id,
    recipe_id,
    catia_document,
    classification,
    part_update_success,
    verifier_passed,
    expected_native_feature,
    notes="",
    extra=None,
):
    report = {
        "run_id": run_id,
        "mode": mode,
        "catia_document": str(catia_document),
        "classifications": {classification: 1},
        "feature_results": [
            {
                "feature_id": feature_id,
                "recipe_id": recipe_id,
                "classification": classification,
                "part_update_success": part_update_success,
                "verifier_passed": verifier_passed,
                "notes": notes,
            }
        ],
        "recipe_id": recipe_id,
        "part_update_success": part_update_success,
        "feature_tree_contains": [expected_native_feature] if part_update_success else [],
        "expected_native_feature": expected_native_feature,
        "classification": classification,
        "reference_pattern_ids": [REFERENCE_PATTERN_ID],
    }
    if extra:
        report.update(extra)
    return report


def write_report(output_dir, filename, report):
    report_path = Path(output_dir) / filename
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report_path


def save_document_overwrite(doc, catpart_path):
    resolved = Path(catpart_path).resolve()
    doc.save_as(resolved, overwrite=True)
    return resolved


def catpart_output_path(output_dir, part_number, run_id):
    return (Path(output_dir) / f"{part_number}_{run_id}.CATPart").resolve()


def run_id_now():
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")
