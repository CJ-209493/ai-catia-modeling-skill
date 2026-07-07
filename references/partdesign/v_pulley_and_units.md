# V Pulley Shaft and Unit Conversion References

Use these reference patterns for the promoted V-pulley Shaft and inch-to-millimeter native Hole recipes.

## V Pulley Shaft Profile

The V pulley recipe is a native CATIA `Shaft`, not a boolean assembly of pads and grooves. The central bore boundary and V groove valley are encoded directly in one closed half-profile sketch.

Verified pattern:

- Create a construction Line2D revolution axis in the same sketch.
- Assign `sketch.com_object.CenterLine = axis.com_object`.
- Draw one closed half-profile with an inner bore radius, outer radius, and V groove valley.
- Call `ShapeFactory.AddNewShaft(sketch)`.
- Confirm `Part.Update()` passes and the feature tree contains `Shaft`.

Do not report separate geometry-equivalent pads/pockets as this native V pulley Shaft recipe.

## Inch-to-Millimeter Parameters

CATIA length values are assigned in millimeters in these runners. Inch input must be converted before assigning dimensions to sketches, Pads, or Holes.

Verified pattern:

- Use `25.4` as the inch-to-millimeter conversion factor.
- Convert plate length, width, thickness, and hole diameter before creating geometry.
- Create the base Pad with converted millimeter values.
- Create the native Hole from a point sketch and set `hole.diameter.value` to the converted millimeter diameter.
- Include the converted values in the run report for auditability.
