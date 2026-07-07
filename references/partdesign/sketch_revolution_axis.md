# Same-Sketch Revolution Axis

Use this reference pattern before attempting native CATIA `Shaft` or `Groove` features with pycatia.

## Problem

`ShapeFactory.add_new_shaft(sketch)` and `ShapeFactory.add_new_groove(sketch)` may be callable, but the call is not enough. CATIA needs the sketch profile to include a valid revolution axis. If Codex only draws the closed profile and forgets the axis, `Part.Update` may fail or the feature may not become a native `Shaft` / `Groove`.

## Required Pattern

- Create the closed profile and the revolution axis in the same sketch.
- Name the axis line explicitly, for example `REV_AXIS`.
- Mark the axis line as construction geometry.
- Keep the revolved profile on the intended side of the axis.
- Call the native operation only after the profile and axis are both present.
- Verify `Part.Update()` and confirm the feature tree contains native `Shaft` or `Groove`.

## pycatia Shape

```python
ref_plane = part.create_reference_from_object(part.origin_elements.plane_zx)
sketch = body.sketches.add(ref_plane)
sketch.name = "Shaft_Profile_With_Axis"
factory_2d = sketch.open_edition()

# Draw the closed revolved profile first.
# Example omitted: use create_line calls to create a closed profile.

axis_line = factory_2d.create_line(0.0, -50.0, 0.0, 50.0)
axis_line.name = "REV_AXIS"
axis_line.construction = True

sketch.close_edition()
part.update()

shaft = part.shape_factory.add_new_shaft(sketch)
shaft.name = "Native_Shaft"
part.update()
```

For a native groove, use the same same-sketch axis pattern, then call:

```python
groove = part.shape_factory.add_new_groove(sketch)
groove.name = "Native_Groove"
part.update()
```

## Do Not Claim Native Success When

- The axis is only implied by global origin, product position, or visual symmetry.
- The axis line is created in a different sketch unless the recipe explicitly verifies `add_new_*_from_ref`.
- The result is built from pads, pockets, boolean cuts, or surface approximations.
- The API call returns an object but `Part.Update()` fails.

Report those outcomes as `HONEST_FAILURE`, `PARTIAL_SUCCESS`, or `GEOMETRY_EQUIVALENT`, not `NATIVE_SUCCESS`.
