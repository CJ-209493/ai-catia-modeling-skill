# Boolean Reference Construction

Use this reference pattern before attempting native CATIA boolean `Intersect` features with pycatia.

## Target Body State for Intersect

`ShapeFactory.add_new_intersect(tool_body)` can create a native `Intersect`, but CATIA resolves the other side of the boolean from the current Part state. The target Body must be active before the call.

Verified pattern:

- Create the target solid in one Body.
- Create the tool solid in a second generated Body.
- Confirm the target and tool solids overlap so the result is non-empty.
- Set `part.in_work_object = target_body` immediately before the boolean call.
- Call `ShapeFactory.AddNewIntersect(tool_body)`.
- Set `part.in_work_object` to the returned `Intersect` and confirm `Part.Update()` passes.

Failure memory:

- Calling `AddNewIntersect(tool_body)` while `Part.InWorkObject` is left on the tool Body or previous feature state can throw a CATIA COM server exception.
- This recipe promotes generated target/tool Body intersection only. Arbitrary BooleanIntersection construction, semantic Body selection, and imported body workflows need separate Developer Mode promotion.
