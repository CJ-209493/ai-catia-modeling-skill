# Groove Without Sketch Axis Is Not Native Success

Native CATIA `Groove` depends on a valid revolved cut profile and an explicit revolution axis reference. A visually equivalent annular pocket or boolean cut is not a native Groove.

## Failure Pattern

- Codex creates a cut profile but omits the same-sketch construction axis line.
- Codex calls `add_new_groove(sketch)` or replaces it with pockets/cuts.
- `Part.Update()` fails, the feature tree lacks `Groove`, or the output is only geometry-equivalent.

## Required Memory

Use `partdesign.sketch_revolution_axis` before attempting native Groove. Do not report `NATIVE_SUCCESS` unless the feature tree verifier confirms native `Groove` after `Part.Update()`.
