# Split Reference Construction

Use this reference pattern before attempting native CATIA `Split` features with pycatia.

## Offset Plane Split Reference

`ShapeFactory.add_new_split(...)` can create a native `Split`, but two conditions must be true:

- the splitting element must be a valid CATIA plane or face reference
- `part.in_work_object` must be set to the target `Body` before calling `add_new_split`

Verified pattern:

- Create the target solid feature, such as a rectangular base `Pad`.
- Create an explicit offset plane with `HybridShapeFactory.AddNewPlaneOffset(base_plane_reference, offset, False)`.
- Append the offset plane to a construction HybridBody and call `Part.Update()`.
- Create a reference from the generated offset plane.
- Set `part.in_work_object = body` before the split call.
- Call `ShapeFactory.AddNewSplit(split_plane_reference, split_side)`.
- Set `part.in_work_object` to the returned `Split` and confirm `Part.Update()` passes.

Failure memory:

- Calling `AddNewSplit` with the same offset plane reference fails when `Part.InWorkObject` is left on the previous feature state.
- This recipe promotes generated offset PlaneXY splits only. Arbitrary angled cut plane synthesis, design-intent side selection, and imported-face splitting need separate Developer Mode promotion.
