# Recipe: T05 Pocket

## Status
verified_once

## Feature
- feature_type: slot_through_pocket
- native_feature: Pocket
- backend: pycatia

## API Methods
- `sketches.add(support_reference)`
- `factory_2d.create_line(...) and factory_2d.create_circle(...) for closed slot profile`
- `part.shape_factory.add_new_pocket(sketch, depth)`
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
# Draw a closed racetrack/capsule profile from tangent lines and arcs.
pocket = part.shape_factory.add_new_pocket(sketch, through_depth)
pocket.name = 'RacetrackSlotPocket'
part.in_work_object = pocket
part.update()
```

## Parameters
{}

## Verification
{
  "classification": "NATIVE_SUCCESS",
  "feature_tree_contains": [
    "Pocket"
  ],
  "part_update_success": true
}

## Known Risks
Reference selection and InWorkObject state must match the recorded context.

## Source Run
- source_run: catia_recipe_regression_20260706_232109
- test_id: T05
- timestamp: 2026-07-06T23:21:11