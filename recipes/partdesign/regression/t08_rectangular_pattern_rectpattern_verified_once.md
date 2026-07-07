# Recipe: T08 RectPattern

## Status
verified_once

## Feature
- feature_type: rectangular_pattern
- native_feature: RectPattern
- backend: pycatia

## API Methods
- `part.shape_factory.add_new_rect_pattern(seed_feature, instances1, instances2, spacing1, spacing2, ...) `
- `part.create_reference_from_object(direction_reference_object)`
- `part.in_work_object = rect_pattern`
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
seed = part.shape_factory.add_new_pad(seed_sketch, seed_depth)
rect_pattern = part.shape_factory.add_new_rect_pattern(
    seed, 4, 3, 40, 30, 1, 1, ref_x, ref_y, False, False, 0
)
rect_pattern.name = 'RectPattern_4x3'
part.in_work_object = rect_pattern
part.update()
```

## Parameters
{}

## Verification
{
  "classification": "NATIVE_SUCCESS",
  "feature_tree_contains": [
    "RectPattern"
  ],
  "part_update_success": true
}

## Known Risks
Reference selection and InWorkObject state must match the recorded context.

## Source Run
- source_run: catia_recipe_regression_20260706_232109
- test_id: T08
- timestamp: 2026-07-06T23:21:12