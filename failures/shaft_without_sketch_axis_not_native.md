# Shaft Without Sketch Axis Is Not Native Success

Native CATIA `Shaft` requires a valid revolution axis reference. In pycatia, the presence of `ShapeFactory.add_new_shaft(sketch)` is not enough.

## Failure Pattern

- Codex creates a closed shaft profile.
- Codex calls `add_new_shaft(sketch)`.
- The sketch does not contain an explicit same-sketch construction axis line.
- The call or `Part.Update()` fails, or the result is replaced by a pad/boolean approximation.

## Required Memory

Use `partdesign.sketch_revolution_axis` before attempting native Shaft. Do not report `NATIVE_SUCCESS` unless the feature tree verifier confirms native `Shaft` after `Part.Update()`.
