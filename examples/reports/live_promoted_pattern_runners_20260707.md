# Live Promoted Pattern Runner Report

Date: 2026-07-07

Scope: verify promoted User Mode runners for native PartDesign pattern features.

## Results

| Recipe | Run ID | Classification | Native Feature | Part.Update | Reference Pattern |
|---|---|---|---|---|---|
| `partdesign.native_rectangular_pattern` | `20260707_000721_805509` | `NATIVE_SUCCESS` | `RectPattern` | true | `partdesign.rectangular_pattern_direction_refs` |
| `partdesign.native_circular_pattern` | `20260707_000735_606168` | `NATIVE_SUCCESS` | `CircPattern` | true | `partdesign.circular_pattern_axis_ref` |

## Notes

- Both runs were executed through `cli/run_feature_plan.py` against live CATIA V5 COM automation.
- Local `.CATPart` outputs were generated under the gitignored `outputs/` directory and are intentionally not committed.
- Rectangular Pattern uses explicit construction X/Y direction references.
- Circular Pattern uses explicit construction center point and Z-axis references.
- Explicitly duplicated/copy-placed features must remain `GEOMETRY_EQUIVALENT` unless the native pattern feature exists and verification passes.
