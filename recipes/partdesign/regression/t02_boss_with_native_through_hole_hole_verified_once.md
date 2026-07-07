# Recipe: T02 Hole

## Status
verified_once

## Feature
- feature_type: boss_with_native_through_hole
- native_feature: Hole
- backend: pycatia

## API Methods
- `part.shape_factory.add_new_pad(sketch, depth)`
- `part.shape_factory.add_new_hole_from_ref_point(point_ref, support_ref, diameter)`
- `hole.bottom_limit.dimension.value = depth`
- `part.update()`

## Preconditions
Active document is CATPart; active body is set as Part.InWorkObject.

## Reference Construction
{
  "active_body": "part.in_work_object = body before creating each feature",
  "support_plane_reference": "Part.CreateReferenceFromObject(OriginElements.PlaneXY) or recorded offset/construction reference"
}

## Minimal Successful Code Pattern
```python
sketch = body.sketches.add(ref_xy)
f2d = sketch.open_edition()
f2d.create_point(x, y)
sketch.close_edition()
part.update()
hole = part.shape_factory.add_new_hole_from_sketch(sketch, depth)
hole.name = name
hole.diameter.value = diameter
part.in_work_object = hole
part.update()
```

## Parameters
{}

## Verification
{
  "classification": "NATIVE_SUCCESS",
  "feature_tree_contains": [
    "Hole"
  ],
  "part_update_success": true
}

## Known Risks
Reference selection and InWorkObject state must match the recorded context.

## Source Run
- test_id: T02
- timestamp: 2026-07-06T01:06:10