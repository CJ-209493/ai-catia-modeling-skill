# Live Promoted Revolution Runner Report

Date: 2026-07-06

Scope: verify promoted User Mode runners for the same-sketch `CenterLine` revolution reference pattern.

## Results

| Recipe | Run ID | Classification | Native Feature | Part.Update | Reference Pattern |
|---|---|---|---|---|---|
| `partdesign.native_shaft_centerline` | `20260706_235722_795927` | `NATIVE_SUCCESS` | `Shaft` | true | `partdesign.sketch_revolution_axis` |
| `partdesign.native_groove_centerline` | `20260706_235727_504205` | `NATIVE_SUCCESS` | `Groove` | true | `partdesign.sketch_revolution_axis` |

## Notes

- Both runs were executed through `cli/run_feature_plan.py` against live CATIA V5 COM automation.
- Local `.CATPart` outputs were generated under the gitignored `outputs/` directory and are intentionally not committed.
- `Product.PartNumber` assignment may be rejected in a reused CATIA session; the runner treats this as non-fatal because native feature creation, `Part.Update`, feature classification, and report verification are independent of that cosmetic document naming field.
- CATPart filenames include `run_id` to avoid collisions with files that may still be open in CATIA.
