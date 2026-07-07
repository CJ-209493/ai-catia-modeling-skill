# Recipe: T14 Shell

## Status
verified_once

## Feature
- feature_type: shell_from_face_reference
- native_feature: Shell
- backend: pycatia

## API Methods
- `selection.clear(); selection.add(base_pad)`
- `selection.search('Topology.Face,sel')`
- `selection.item2(index).reference for the removed face reference`
- `part.shape_factory.add_new_shell(face_reference, inside_thickness, outside_thickness)`
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
selection.clear()
selection.add(base_pad)
selection.search('Topology.Face,sel')
shell = part.shape_factory.add_new_shell(selection.item2(1).reference, 3, 0)
shell.name = 'Shell_3mm'
part.in_work_object = shell
part.update()
```

## Parameters
{}

## Verification
{
  "classification": "NATIVE_SUCCESS",
  "feature_tree_contains": [
    "Shell"
  ],
  "part_update_success": true
}

## Known Risks
Reference selection and InWorkObject state must match the recorded context.

## Source Run
- test_id: T14
- timestamp: 2026-07-06T01:06:15