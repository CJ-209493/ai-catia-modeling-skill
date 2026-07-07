# Live Promoted Chamfer Runner Evidence

- date: 2026-07-07
- CATIA live COM run: true
- package version: 1.0.11-draft
- feature plan: `examples/feature_plans/native_chamfer_selected_edge.yaml`

| recipe_id | run_id | classification | expected_native_feature | Part.Update | reference_pattern |
| --- | --- | --- | --- | --- | --- |
| `partdesign.native_chamfer_selected_edge` | `20260707_004956_282399` | `NATIVE_SUCCESS` | `Chamfer` | true | `partdesign.chamfer_selected_edge_ref` |

Notes:

- The runner created a rectangular base `Pad`, searched the pad selection with `Selection.Search("Topology.Edge,sel")`, used `Selection.Item2(index).Reference`, and created a native `Chamfer`.
- The verified enum values were `catMinimalChamfer = 1`, `catTwoLengthChamfer = 0`, and `catNoReverseChamfer = 0`.
- This promotion is intentionally constrained to index-based selected-edge references.
- Ordered fillet/chamfer edge grouping remains future Developer Mode promotion work.
- Local CATPart output is intentionally excluded from GitHub.
