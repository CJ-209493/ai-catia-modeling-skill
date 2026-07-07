"""Shared helpers for native RectPattern and CircPattern runners."""

from __future__ import annotations

from runners.partdesign.prismatic_cut_common import (
    catpart_output_path,
    create_base_pad,
    create_part,
    make_partdesign_report,
    run_id_now,
    save_document_overwrite,
    write_report,
)


def create_circle_pad(part, body, ref_xy, *, sketch_name, feature_name, x, y, radius, depth):
    part.in_work_object = body
    sketch = body.sketches.add(ref_xy)
    sketch.name = sketch_name
    factory_2d = sketch.open_edition()
    factory_2d.create_closed_circle(x, y, radius)
    sketch.close_edition()
    part.update()
    pad = part.shape_factory.add_new_pad(sketch, depth)
    pad.name = feature_name
    part.in_work_object = pad
    part.update()
    return pad


def create_circle_pocket(part, body, ref_xy, *, sketch_name, feature_name, x, y, radius, depth):
    part.in_work_object = body
    sketch = body.sketches.add(ref_xy)
    sketch.name = sketch_name
    factory_2d = sketch.open_edition()
    factory_2d.create_closed_circle(x, y, radius)
    sketch.close_edition()
    part.update()
    pocket = part.shape_factory.add_new_pocket(sketch, depth)
    pocket.name = feature_name
    part.in_work_object = pocket
    part.update()
    return pocket


def create_offset_plane_reference(part, ref_xy, *, offset, container_name):
    construction = part.hybrid_bodies.add()
    construction.name = container_name
    plane = part.hybrid_shape_factory.add_new_plane_offset(ref_xy, offset, False)
    plane.name = f"PlaneXY_Offset_{offset:g}"
    construction.append_hybrid_shape(plane)
    part.update()
    return part.create_reference_from_object(plane)


def create_construction_body(part):
    construction = part.hybrid_bodies.add()
    construction.name = "AI_CATIA_Pattern_References"
    return construction


def construction_line_reference(part, construction, name, direction):
    hsf = part.hybrid_shape_factory
    point = hsf.add_new_point_coord(0, 0, 0)
    construction.append_hybrid_shape(point)
    part.update()
    point_ref = part.create_reference_from_object(point)
    direction_obj = hsf.add_new_direction_by_coord(*direction)
    line = hsf.add_new_line_pt_dir(point_ref, direction_obj, 0, 100, False)
    line.name = name
    construction.append_hybrid_shape(line)
    part.update()
    return point_ref, part.create_reference_from_object(line)


def create_native_rectangular_pattern(
    part,
    seed_feature,
    direction_1_ref,
    direction_2_ref,
    *,
    instances_1,
    instances_2,
    spacing_1,
    spacing_2,
    feature_name,
):
    pattern = part.shape_factory.add_new_rect_pattern(
        seed_feature,
        int(instances_1),
        int(instances_2),
        float(spacing_1),
        float(spacing_2),
        1,
        1,
        direction_1_ref,
        direction_2_ref,
        False,
        False,
        0,
    )
    pattern.name = feature_name
    part.in_work_object = pattern
    part.update()
    return pattern


def create_native_circular_pattern(
    part,
    seed_feature,
    center_ref,
    axis_ref,
    *,
    instances,
    angular_spacing,
    total_angle,
    feature_name,
):
    pattern = part.shape_factory.add_new_circ_pattern(
        seed_feature,
        1,
        int(instances),
        0,
        float(angular_spacing),
        1,
        1,
        center_ref,
        axis_ref,
        False,
        float(total_angle),
        True,
    )
    pattern.name = feature_name
    part.in_work_object = pattern
    part.update()
    return pattern
