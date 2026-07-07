# Recipe: T04 Hole

## Status
verified_once

## Feature
- feature_type: native_counterbore_holes
- native_feature: Hole
- backend: pycatia

## API Methods
- `part.shape_factory.add_new_hole_from_ref_point(point_ref, support_ref, diameter)`
- `hole.type = catHoleCounterbored-equivalent enum value from CATIA COM`
- `hole.head_diameter.value / hole.head_depth.value through COM properties`
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
hole = part.shape_factory.add_new_hole_from_sketch(point_sketch, depth)
hole.type = 2
hole.diameter.value = drill_diameter
hole.head_diameter.value = head_diameter
hole.head_depth.value = head_depth
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
- source_run: catia_recipe_regression_20260706_232109
- test_id: T04
- timestamp: 2026-07-06T23:21:11