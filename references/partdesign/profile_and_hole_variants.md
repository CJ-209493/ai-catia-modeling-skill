# Profile and Hole Variant Reference Construction

Use these reference patterns before attempting promoted Pad profile variants and native Hole variants with pycatia.

## Counterbore Hole Point Sketch

Native counterbore holes are still CATIA `Hole` features. Do not model counterbores as stacked Pockets and report native Hole success.

Verified pattern:

- Create a base Pad first.
- Create one point sketch per hole on the support sketch plane.
- Call `ShapeFactory.AddNewHoleFromSketch(point_sketch, depth)`.
- Set `hole.type = 2`, `hole.diameter.value`, `hole.head_diameter.value`, and `hole.head_depth.value`.
- Confirm `Part.Update()` passes and the feature tree contains `Hole`.

## Offset Plane Pad Support

Pads can be created from sketches on explicit offset planes.

Verified pattern:

- Create a base plane reference from `OriginElements.PlaneXY`.
- Create `HybridShapeFactory.AddNewPlaneOffset(base_plane_ref, offset, False)`.
- Append the offset plane to a hybrid body, update the Part, and create a reference from the plane.
- Add the sketch on that offset-plane reference, create the Pad, and confirm `Part.Update()`.

## Tangent Arc Closed Profile

Rounded rectangles and capsules use line and arc segments in one closed sketch. A native Pad or Hole result depends on the downstream feature, not on claiming a special native rounded-profile feature.

Verified pattern:

- Draw tangent straight segments and circular arcs in a single sketch.
- Keep the profile closed before calling `AddNewPad`.
- Confirm `Part.Update()` passes and the feature tree contains `Pad`.

## Capsule Profile with Native Holes

The promoted capsule recipe creates a tangent-arc capsule Pad, then native `Hole` features at the capsule ends.

Verified pattern:

- Create the capsule Pad from tangent lines and arcs.
- Create one point sketch per end-hole center.
- Call `AddNewHoleFromSketch` for each hole and set `hole.diameter.value`.
- Confirm `Part.Update()` passes and the feature tree contains `Hole`.

## Closed Spline Profile

Closed spline Pads require the first point to be repeated as the final spline pole in the promoted pattern.

Verified pattern:

- Create CATIA 2D points in one sketch.
- Call `Factory2D.CreateSpline(tuple(point_objects))`.
- Repeat the first point as the final point so the profile is closed.
- Call `AddNewPad` and confirm `Part.Update()` passes.
