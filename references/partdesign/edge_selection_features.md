# Edge Selection Feature References

Use these reference patterns before attempting native CATIA edge features with pycatia.

## Selected Edge Fillet Reference

`ShapeFactory.add_new_solid_edge_fillet_with_constant_radius(...)` can create a native `ConstRadEdgeFillet`, but only when the input is a valid CATIA edge reference.

Verified pattern:

- Create the solid target feature, such as a rectangular base `Pad`.
- Clear the active selection, add the target feature, then run `Selection.Search("Topology.Edge,sel")`.
- Use `Selection.Item2(index).Reference` as the edge reference.
- Pass that reference to `add_new_solid_edge_fillet_with_constant_radius(edge_reference, propagation, radius)`.
- Confirm `Part.Update()` passes and the feature tree contains `ConstRadEdgeFillet`.

This pattern is index-based. It is useful for repeatable generated geometry where the target edge index is known for the recipe, but it is not a general semantic edge selector. If the user asks for all vertical edges, all outer edges, ordered fillet plus chamfer, or an edge selected from arbitrary imported geometry, keep the task in Developer Mode until that edge filter and verifier are promoted.

Do not create rounded sketch geometry and call the result native edge fillet success. Rounded profiles can be valid native `Pad` recipes, but they are not native `ConstRadEdgeFillet` features.

## Selected Edge Chamfer Reference

`ShapeFactory.add_new_chamfer(...)` can create a native `Chamfer`, but only when the input is a valid CATIA edge or face reference. The promoted runner uses the same constrained selected-edge pattern as the native edge fillet runner.

Verified pattern:

- Create the solid target feature, such as a rectangular base `Pad`.
- Clear the active selection, add the target feature, then run `Selection.Search("Topology.Edge,sel")`.
- Use `Selection.Item2(index).Reference` as the edge reference.
- Use explicit enum values: `catMinimalChamfer = 1`, `catTwoLengthChamfer = 0`, and `catNoReverseChamfer = 0`.
- Pass the reference and dimensions to `add_new_chamfer(edge_reference, propagation, mode, orientation, length_1, length_2_or_angle)`.
- Confirm `Part.Update()` passes and the feature tree contains `Chamfer`.

This pattern is not an ordered fillet/chamfer selector. If the user needs a sequence such as "fillet these four edges, then chamfer those other edges", keep the task in Developer Mode until edge grouping, operation ordering, and verifier checks are promoted.
