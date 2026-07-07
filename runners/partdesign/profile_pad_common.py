"""Shared helpers for promoted profile Pad and native Hole variant runners."""

from __future__ import annotations

import math

from runners.partdesign.prismatic_cut_common import (
    capsule,
    catpart_output_path,
    create_base_pad,
    create_native_hole_from_sketch,
    create_part,
    make_partdesign_report,
    run_id_now,
    save_document_overwrite,
    write_report,
)


def rounded_rectangle(factory_2d, cx, cy, width, height, radius):
    factory_2d.create_line(cx - width / 2 + radius, cy - height / 2, cx + width / 2 - radius, cy - height / 2)
    factory_2d.create_circle(cx + width / 2 - radius, cy - height / 2 + radius, radius, 1.5 * math.pi, 2 * math.pi)
    factory_2d.create_line(cx + width / 2, cy - height / 2 + radius, cx + width / 2, cy + height / 2 - radius)
    factory_2d.create_circle(cx + width / 2 - radius, cy + height / 2 - radius, radius, 0, 0.5 * math.pi)
    factory_2d.create_line(cx + width / 2 - radius, cy + height / 2, cx - width / 2 + radius, cy + height / 2)
    factory_2d.create_circle(cx - width / 2 + radius, cy + height / 2 - radius, radius, 0.5 * math.pi, math.pi)
    factory_2d.create_line(cx - width / 2, cy + height / 2 - radius, cx - width / 2, cy - height / 2 + radius)
    factory_2d.create_circle(cx - width / 2 + radius, cy - height / 2 + radius, radius, math.pi, 1.5 * math.pi)


def create_pad_from_sketch(part, body, support_ref, *, sketch_name, feature_name, depth, draw_profile):
    part.in_work_object = body
    sketch = body.sketches.add(support_ref)
    sketch.name = sketch_name
    factory_2d = sketch.open_edition()
    draw_profile(factory_2d)
    sketch.close_edition()
    part.update()
    pad = part.shape_factory.add_new_pad(sketch, depth)
    pad.name = feature_name
    part.in_work_object = pad
    part.update()
    return pad


def create_offset_plane_reference(part, ref_xy, *, offset, container_name="AI_CATIA_Offset_References"):
    construction = part.hybrid_bodies.add()
    construction.name = container_name
    plane = part.hybrid_shape_factory.add_new_plane_offset(ref_xy, offset, False)
    plane.name = f"PlaneXY_Offset_{offset:g}"
    construction.append_hybrid_shape(plane)
    part.update()
    return part.create_reference_from_object(plane)


def create_native_counterbore_hole_from_sketch(
    part,
    body,
    support_ref,
    *,
    sketch_name,
    feature_name,
    x,
    y,
    depth,
    diameter,
    head_diameter,
    head_depth,
):
    part.in_work_object = body
    sketch = body.sketches.add(support_ref)
    sketch.name = sketch_name
    factory_2d = sketch.open_edition()
    factory_2d.create_point(x, y)
    sketch.close_edition()
    part.update()
    hole = part.shape_factory.add_new_hole_from_sketch(sketch, depth)
    hole.name = feature_name
    hole.diameter.value = diameter
    hole.type = 2
    hole.head_diameter.value = head_diameter
    hole.head_depth.value = head_depth
    part.in_work_object = hole
    part.update()
    return hole


def create_rounded_rectangle_pad(part, body, ref_xy, *, sketch_name, feature_name, width, height, radius, depth):
    return create_pad_from_sketch(
        part,
        body,
        ref_xy,
        sketch_name=sketch_name,
        feature_name=feature_name,
        depth=depth,
        draw_profile=lambda factory_2d: rounded_rectangle(factory_2d, 0.0, 0.0, width, height, radius),
    )


def create_capsule_pad(part, body, ref_xy, *, sketch_name, feature_name, half_center_distance, radius, depth):
    return create_pad_from_sketch(
        part,
        body,
        ref_xy,
        sketch_name=sketch_name,
        feature_name=feature_name,
        depth=depth,
        draw_profile=lambda factory_2d: capsule(factory_2d, 0.0, 0.0, half_center_distance, radius),
    )


def create_closed_spline_pad(part, body, ref_xy, *, sketch_name, feature_name, points, depth):
    def draw(factory_2d):
        point_objs = [factory_2d.create_point(float(x), float(y)) for x, y in points]
        spline = factory_2d.create_spline(tuple(point_objs))
        spline.name = f"{feature_name}_Spline"

    return create_pad_from_sketch(
        part,
        body,
        ref_xy,
        sketch_name=sketch_name,
        feature_name=feature_name,
        depth=depth,
        draw_profile=draw,
    )
