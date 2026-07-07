# Transform and Shell Reference Construction

Use these reference patterns before attempting native CATIA Mirror or Shell features with pycatia.

## Mirror Plane Reference

`ShapeFactory.add_new_mirror(...)` can create a native `Mirror`, but only after CATIA has a valid seed feature context and mirror-plane reference.

Verified pattern:

- Create the base Pad first.
- Create an explicit PlaneXY offset reference at the top face height.
- Create the seed Pad sketch on that top offset plane so the mirrored seed is visible on the body.
- Create the seed feature that should be mirrored.
- Set `part.in_work_object` to the seed feature.
- Create a reference from an explicit support plane, such as `part.origin_elements.plane_yz`.
- Pass that reference to `add_new_mirror`.
- Confirm `Part.Update()` passes, the feature tree contains `Mirror`, and the CATIA screenshot shows the mirrored feature.

Do not create copied pads or pockets and call the result native Mirror. That is geometry-equivalent only.

## Shell Selected Face Reference

`ShapeFactory.add_new_shell(...)` requires a CATIA face reference. The promoted draft runner uses a constrained selection-index pattern rather than arbitrary semantic face recognition.

Verified pattern:

- Create the base solid Pad.
- Clear the active selection, add the base Pad, then run `Selection.Search("Topology.Face,sel")`.
- Use `Selection.Item2(index).Reference` as the removed face reference.
- Pass that reference to `add_new_shell(face_reference, inside_thickness, outside_thickness)`.
- Confirm `Part.Update()` passes and the feature tree contains `Shell`.

Face ordering is not a general semantic selector. If the user needs a named top/front/side face or complex BRep filtering, use Developer Mode until that selector and verifier are promoted.
