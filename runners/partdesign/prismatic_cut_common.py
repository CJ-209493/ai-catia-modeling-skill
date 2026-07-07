"""Shared helpers for native Hole and Pocket PartDesign runners."""

from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path


def safe_set_part_number(product, part_number):
    result = {"requested": part_number, "applied": False, "error": ""}
    try:
        product.part_number = part_number
    except Exception as exc:  # CATIA can reject PartNumber in reused live sessions.
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


def rectangle(factory_2d, cx, cy, width, height):
    x1, x2 = cx - width / 2, cx + width / 2
    y1, y2 = cy - height / 2, cy + height / 2
    factory_2d.create_line(x1, y1, x2, y1)
    factory_2d.create_line(x2, y1, x2, y2)
    factory_2d.create_line(x2, y2, x1, y2)
    factory_2d.create_line(x1, y2, x1, y1)


def capsule(factory_2d, cx, cy, half_center_distance, radius):
    left = cx - half_center_distance
    right = cx + half_center_distance
    factory_2d.create_line(left, cy - radius, right, cy - radius)
    factory_2d.create_circle(right, cy, radius, 1.5 * math.pi, 2.5 * math.pi)
    factory_2d.create_line(right, cy + radius, left, cy + radius)
    factory_2d.create_circle(left, cy, radius, 0.5 * math.pi, 1.5 * math.pi)


def create_base_pad(part, body, ref_xy, *, sketch_name, feature_name, width, height, depth):
    part.in_work_object = body
    sketch = body.sketches.add(ref_xy)
    sketch.name = sketch_name
    factory_2d = sketch.open_edition()
    rectangle(factory_2d, 0.0, 0.0, width, height)
    sketch.close_edition()
    part.update()
    pad = part.shape_factory.add_new_pad(sketch, depth)
    pad.name = feature_name
    part.in_work_object = pad
    part.update()
    return pad


def create_native_hole_from_sketch(part, body, ref_xy, *, sketch_name, feature_name, x, y, depth, diameter):
    part.in_work_object = body
    sketch = body.sketches.add(ref_xy)
    sketch.name = sketch_name
    factory_2d = sketch.open_edition()
    factory_2d.create_point(x, y)
    sketch.close_edition()
    part.update()
    hole = part.shape_factory.add_new_hole_from_sketch(sketch, depth)
    hole.name = feature_name
    hole.diameter.value = diameter
    part.in_work_object = hole
    part.update()
    return hole


def create_native_slot_pocket(part, body, ref_xy, *, sketch_name, feature_name, half_center_distance, radius, depth):
    part.in_work_object = body
    sketch = body.sketches.add(ref_xy)
    sketch.name = sketch_name
    factory_2d = sketch.open_edition()
    capsule(factory_2d, 0.0, 0.0, half_center_distance, radius)
    sketch.close_edition()
    part.update()
    pocket = part.shape_factory.add_new_pocket(sketch, depth)
    pocket.name = feature_name
    part.in_work_object = pocket
    part.update()
    return pocket


def make_partdesign_report(
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
