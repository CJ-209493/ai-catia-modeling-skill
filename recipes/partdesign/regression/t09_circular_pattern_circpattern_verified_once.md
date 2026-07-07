# Recipe: T09 CircPattern

## Status
verified_once

## Feature
- feature_type: circular_pattern
- native_feature: CircPattern
- backend: pycatia

## API Methods
- `part.shape_factory.add_new_circ_pattern(seed_feature, instances, angular_spacing, ...) `
- `part.create_reference_from_object(axis_or_direction_reference_object)`
- `part.in_work_object = circ_pattern`
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
seed = part.shape_factory.add_new_pocket(seed_hole_sketch, depth)
circ = part.shape_factory.add_new_circ_pattern(
    seed, 1, 6, 0, 60, 1, 1, ref_center, ref_axis_z, False, 360, True
)
circ.name = 'CircPattern_6x'
part.in_work_object = circ
part.update()
```

## Parameters
{}

## Verification
{
  "classification": "NATIVE_SUCCESS",
  "feature_tree_contains": [
    "CircPattern"
  ],
  "part_update_success": true
}

## Known Risks
Reference selection and InWorkObject state must match the recorded context.

## Source Run
- test_id: T09
- timestamp: 2026-07-06T01:06:13