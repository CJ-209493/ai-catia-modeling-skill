# Recipe: T10 Mirror

## Status
verified_once

## Feature
- feature_type: mirror
- native_feature: Mirror
- backend: pycatia

## API Methods
- `part.in_work_object = seed_feature before creating Mirror`
- `part.create_reference_from_object(part.origin_elements.plane_yz)`
- `part.shape_factory.add_new_mirror(mirror_plane_reference)`
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
part.in_work_object = seed_feature
mirror_plane = part.create_reference_from_object(part.origin_elements.plane_yz)
mirror = part.shape_factory.add_new_mirror(mirror_plane)
mirror.name = 'Mirror_YZ'
part.in_work_object = mirror
part.update()
```

## Parameters
{}

## Verification
{
  "classification": "NATIVE_SUCCESS",
  "feature_tree_contains": [
    "Mirror"
  ],
  "part_update_success": true
}

## Known Risks
Reference selection and InWorkObject state must match the recorded context.

## Source Run
- source_run: catia_recipe_regression_20260706_232109
- test_id: T10
- timestamp: 2026-07-06T23:21:12