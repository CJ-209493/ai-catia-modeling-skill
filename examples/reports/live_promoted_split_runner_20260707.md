# Live Promoted Split Runner Evidence

- date: 2026-07-07
- CATIA live COM run: true
- package version: 1.0.12-draft
- feature plan: `examples/feature_plans/native_split_offset_plane.yaml`

| recipe_id | run_id | classification | expected_native_feature | Part.Update | reference_pattern |
| --- | --- | --- | --- | --- | --- |
| `partdesign.native_split_offset_plane` | `20260707_005507_503010` | `NATIVE_SUCCESS` | `Split` | true | `partdesign.split_offset_plane_ref` |

Notes:

- The runner created a rectangular base `Pad`, generated an explicit offset PlaneXY reference, set `Part.InWorkObject` back to the target Body, and created a native `Split`.
- The verified split side was `catPositiveSide = 0`.
- This promotion is intentionally constrained to generated offset PlaneXY references.
- Arbitrary angled cut plane synthesis and design-intent split-side inference remain future Developer Mode promotion work.
- Local CATPart output is intentionally excluded from GitHub.
