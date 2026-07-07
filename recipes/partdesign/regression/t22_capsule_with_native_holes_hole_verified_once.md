# Recipe: T22 Hole

## Status
verified_once

## Feature
- feature_type: capsule_with_native_holes
- native_feature: Hole
- backend: pycatia

## API Methods
- `factory_2d.create_line(...) and factory_2d.create_circle(...) for capsule pad profile`
- `part.shape_factory.add_new_pad(sketch, depth)`
- `part.shape_factory.add_new_hole_from_ref_point(point_ref, support_ref, diameter)`
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
# Create closed capsule pad from tangent arc sketch.
# Add left and right native holes with AddNewHoleFromSketch point sketches.
for x, y in [(left_x, cy), (right_x, cy)]:
    hole = part.shape_factory.add_new_hole_from_sketch(point_sketch, depth)
    hole.diameter.value = diameter
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
- test_id: T22
- timestamp: 2026-07-06T01:06:16