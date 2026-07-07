# Recipe: T20 Hole

## Status
verified_once

## Feature
- feature_type: unit_conversion_native_hole
- native_feature: Hole
- backend: pycatia

## API Methods
- `part.shape_factory.add_new_hole_from_ref_point(point_ref, support_ref, diameter_mm)`
- `Convert inch input to millimeters before assigning CATIA length values`
- `hole.bottom_limit.dimension.value = depth_mm`
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
mm = inch * 25.4
length = 4 * mm
width = 2 * mm
thickness = 0.25 * mm
hole_diameter = 0.5 * mm
# Create pad using converted dimensions, then native Hole from sketch point.
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
- test_id: T20
- timestamp: 2026-07-06T23:21:13