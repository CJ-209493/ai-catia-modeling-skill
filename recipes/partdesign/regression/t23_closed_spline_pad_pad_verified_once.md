# Recipe: T23 Pad

## Status
verified_once

## Feature
- feature_type: closed_spline_pad
- native_feature: Pad
- backend: pycatia

## API Methods
- `factory_2d.create_spline(points) or CATIA 2D spline COM creation for closed profile`
- `sketch.close_edition()`
- `part.shape_factory.add_new_pad(sketch, depth)`
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
point_objs = [f2d.create_point(x, y) for x, y in closed_points]
spline = f2d.create_spline(tuple(point_objs))
sketch.close_edition()
part.update()
pad = part.shape_factory.add_new_pad(sketch, depth)
part.in_work_object = pad
part.update()
```

## Parameters
{}

## Verification
{
  "classification": "NATIVE_SUCCESS",
  "feature_tree_contains": [
    "Pad"
  ],
  "part_update_success": true
}

## Known Risks
Reference selection and InWorkObject state must match the recorded context.

## Source Run
- source_run: catia_recipe_regression_20260706_232109
- test_id: T23
- timestamp: 2026-07-06T23:21:13