# Live Promoted Cut Runner Report

Date: 2026-07-07

Scope: verify promoted User Mode runners for native PartDesign cut features.

## Results

| Recipe | Run ID | Classification | Native Feature | Part.Update |
|---|---|---|---|---|
| `partdesign.native_hole_from_sketch` | `20260707_000240_989782` | `NATIVE_SUCCESS` | `Hole` | true |
| `partdesign.native_slot_pocket` | `20260707_000246_235760` | `NATIVE_SUCCESS` | `Pocket` | true |

## Notes

- Both runs were executed through `cli/run_feature_plan.py` against live CATIA V5 COM automation.
- Local `.CATPart` outputs were generated under the gitignored `outputs/` directory and are intentionally not committed.
- `partdesign.native_hole_from_sketch` verifies `ShapeFactory.AddNewHoleFromSketch(point_sketch, depth)` plus `hole.diameter.value`.
- `partdesign.native_slot_pocket` verifies `ShapeFactory.AddNewPocket(sketch, depth)` from a closed racetrack sketch.
- These recipes do not claim counterbore/countersink/threaded Hole variants or a native Slot feature type.
