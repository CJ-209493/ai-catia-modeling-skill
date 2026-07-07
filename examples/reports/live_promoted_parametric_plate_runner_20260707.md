# Live Promoted Parametric Plate Runner Evidence

- date: 2026-07-07
- CATIA live COM run: true
- package version: 1.0.14-draft
- feature plan: `examples/feature_plans/parametric_plate_formula_holes.yaml`

| recipe_id | run_id | classification | expected_native_feature | Part.Update | reference_pattern |
| --- | --- | --- | --- | --- | --- |
| `partdesign.parametric_plate_formula_holes` | `20260707_010730_417231` | `NATIVE_SUCCESS` | `Formula` | true | `knowledgeware.formula_driven_sketch_dimensions` |

Measured update evidence:

| value | initial | after Length update |
| --- | ---: | ---: |
| base Length dimension | 120 mm | 150 mm |
| hole X offset dimension | 48 mm | 63 mm |
| hole Y offset dimension | 18 mm | 18 mm |

Notes:

- The runner created visible `Length`, `Width`, `Thickness`, `HoleDia`, and `EdgeOffset` LENGTH parameters.
- The base sketch length/width constraints were added while the sketch was open, then bound to parameters with Knowledgeware formulas.
- Four native `Hole` features were created from point sketches whose point-to-axis distance constraints were formula driven.
- The live report recorded 19 relations, 4 native Holes, and zero broken or unupdated sketch constraints after changing `Length` to 150 mm.
- This promotion is intentionally constrained to the T19-style rectangular plate pattern.
- Arbitrary sketch constraint inference, arbitrary formula parsing, and semantic edge-based offset constraints remain future Developer Mode promotion work.
- Local CATPart output is intentionally excluded from GitHub.
