# Recipe: T06 Pad

## Status
verified_once

## Feature
- feature_type: offset_plane_secondary_pad
- native_feature: Pad
- backend: pycatia

## API Methods
- `part.hybrid_shape_factory.add_new_plane_offset(base_plane_ref, offset, False)`
- `part.create_reference_from_object(offset_plane)`
- `sketches.add(offset_plane_ref)`
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
plane = part.hybrid_shape_factory.add_new_plane_offset(ref_xy, z_offset, False)
construction_body.append_hybrid_shape(plane)
part.update()
sketch = body.sketches.add(part.create_reference_from_object(plane))
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
- test_id: T06
- timestamp: 2026-07-06T01:06:12