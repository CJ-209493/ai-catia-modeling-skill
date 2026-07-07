# Recipe: T21 Pad

## Status
verified_once

## Feature
- feature_type: rounded_rectangle_pad
- native_feature: Pad
- backend: pycatia

## API Methods
- `factory_2d.create_line(...) and factory_2d.create_circle(...) for tangent rounded-corner profile`
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
# Draw rounded rectangle as tangent lines plus corner arcs in a closed sketch.
pad = part.shape_factory.add_new_pad(rounded_rect_sketch, depth)
pad.name = 'RoundedRectanglePad'
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
- test_id: T21
- timestamp: 2026-07-06T01:06:16