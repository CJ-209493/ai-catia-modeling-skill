# Live Promoted Edge Fillet Runner Evidence

- date: 2026-07-07
- CATIA live COM run: true
- package version: 1.0.10-draft
- feature plan: `examples/feature_plans/native_edge_fillet_selected_edge.yaml`

| recipe_id | run_id | classification | expected_native_feature | Part.Update | reference_pattern |
| --- | --- | --- | --- | --- | --- |
| `partdesign.native_edge_fillet_selected_edge` | `20260707_003721_668816` | `NATIVE_SUCCESS` | `ConstRadEdgeFillet` | true | `partdesign.edge_fillet_selected_edge_ref` |

Notes:

- The runner created a rectangular base `Pad`, searched the pad selection with `Selection.Search("Topology.Edge,sel")`, used `Selection.Item2(index).Reference`, and created a native `ConstRadEdgeFillet`.
- This promotion is intentionally constrained to index-based selected-edge references.
- Exact four-vertical-edge filtering, arbitrary edge intent, and ordered fillet/chamfer workflows remain future Developer Mode promotion work.
- Local CATPart output is intentionally excluded from GitHub.
