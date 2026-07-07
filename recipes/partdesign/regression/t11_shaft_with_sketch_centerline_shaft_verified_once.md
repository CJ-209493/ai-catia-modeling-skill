# Recipe: T11 Shaft

## Status
verified_once

## Feature
- feature_type: shaft_with_sketch_centerline
- native_feature: Shaft
- backend: pycatia

## API Methods
- `factory_2d.create_line(...) for the same-sketch construction axis`
- `axis.construction = True`
- `sketch.com_object.CenterLine = axis.com_object`
- `part.shape_factory.add_new_shaft(sketch)`
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
axis = f2d.create_line(0, 0, 120, 0)
axis.construction = True
# Draw closed half-profile in the same sketch.
sketch.com_object.CenterLine = axis.com_object
sketch.close_edition()
part.update()
shaft = part.shape_factory.add_new_shaft(sketch)
part.in_work_object = shaft
part.update()
```

## Parameters
{}

## Verification
{
  "classification": "NATIVE_SUCCESS",
  "feature_tree_contains": [
    "Shaft"
  ],
  "part_update_success": true
}

## Known Risks
Reference selection and InWorkObject state must match the recorded context.

## Source Run
- source_run: catia_recipe_regression_20260706_232109
- test_id: T11
- timestamp: 2026-07-06T23:21:12