# Formula-Driven Sketch Dimension Pattern

Use this pattern when a CATIA sketch dimension must be driven by a visible Knowledgeware parameter through pycatia.

## Open-Sketch Constraint Rule

For 2D sketch geometry, add the native constraint while the sketch is still open. Then close the sketch and bind the created `Constraint.Dimension` with `Relations.CreateFormula`.

Verified pattern:

- Create visible length parameters with `Parameters.CreateDimension(name, "LENGTH", value)` and `ValuateFromString`.
- Open the sketch with `sketch.open_edition()`.
- Create the 2D geometry.
- Add sketch constraints before `sketch.close_edition()`.
- For the promoted rectangular plate, constrain base profile edges with horizontal/vertical constraints.
- Center the base profile by adding distance constraints from the right/left edges to `sketch.absolute_axis.vertical_reference` and top/bottom edges to `sketch.absolute_axis.horizontal_reference`, then bind those dimensions to `Length / 2` and `Width / 2`.
- For point offsets, use `Constraints.AddBiEltCst(catCstTypeDistance, point_reference, sketch.absolute_axis.vertical_reference)` for X distance and the horizontal reference for Y distance.
- Set each point distance constraint `side` according to the intended quadrant so CATIA preserves left/right and front/back locations during formula updates.
- Close the sketch.
- Use `Parameters.GetNameToUseInRelation(parameter)` in formula expressions.
- Bind formulas to `constraint.dimension`, `pad.first_limit.dimension`, `hole.diameter`, or `hole.bottom_limit.dimension`.
- For native Holes created from bottom XY point sketches, call `hole.reverse()` so the hole cuts into the Pad.
- Change the driving parameter and call `Part.Update()`; verify broken and unupdated constraint counts remain zero.

Failure memory:

- Adding a `Length` constraint to a 2D line after `sketch.close_edition()` can fail with `CATIAConstraints: The method AddMonoEltCst failed`.
- Driving only a bottom-edge length and left-edge width can leave the base sketch under-constrained; CATIA may update without exception while the visible plate collapses or shifts.
- COM/feature-tree success is not enough for formula-driven sketches; capture top and isometric CATIA screenshots and confirm the updated plate and holes are visibly correct.
- This pattern promotes a constrained parametric plate workflow only. Arbitrary sketch constraint inference and semantic edge-based offset constraints need separate Developer Mode promotion.
