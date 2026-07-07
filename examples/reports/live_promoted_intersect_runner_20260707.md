# Live Promoted Intersect Runner Evidence

- date: 2026-07-07
- CATIA live COM run: true
- package version: 1.0.13-draft
- feature plan: `examples/feature_plans/native_intersect_two_bodies.yaml`

| recipe_id | run_id | classification | expected_native_feature | Part.Update | reference_pattern |
| --- | --- | --- | --- | --- | --- |
| `partdesign.native_intersect_two_bodies` | `20260707_010109_382180` | `NATIVE_SUCCESS` | `Intersect` | true | `partdesign.intersect_target_body_ref` |

Notes:

- The runner created a generated target Body and a generated tool Body, each with a native rectangular `Pad`.
- The generated solids overlapped so the intersection was non-empty.
- The runner set `Part.InWorkObject` to the target Body immediately before `ShapeFactory.AddNewIntersect(tool_body)`.
- This promotion is intentionally constrained to generated target/tool Body intersections.
- Arbitrary BooleanIntersection construction, imported Body workflows, and semantic Body discovery remain future Developer Mode promotion work.
- Local CATPart output is intentionally excluded from GitHub.
