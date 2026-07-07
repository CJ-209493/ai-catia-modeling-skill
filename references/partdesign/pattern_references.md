# Pattern Reference Construction

Use these reference patterns before attempting native CATIA rectangular or circular pattern features with pycatia.

## Rectangular Pattern Direction References

`ShapeFactory.add_new_rect_pattern(...)` requires valid direction references. Do not substitute explicit copied features and call that a native pattern.

Verified pattern:

- Create construction HybridShape lines for the first and second pattern directions.
- Convert those lines to CATIA references with `part.create_reference_from_object(line)`.
- Pass the references as `direction_1_ref` and `direction_2_ref` to `add_new_rect_pattern`.
- Confirm `Part.Update()` passes and the feature tree contains `RectPattern`.

## Circular Pattern Center and Axis References

`ShapeFactory.add_new_circ_pattern(...)` requires a center reference and an axis reference. Explicitly placing repeated holes is geometry equivalent, not native success.

Verified pattern:

- Create a construction point at the intended pattern center.
- Create a construction HybridShape line in the intended axis direction.
- Pass the center point reference and axis line reference to `add_new_circ_pattern`.
- Confirm `Part.Update()` passes and the feature tree contains `CircPattern`.
