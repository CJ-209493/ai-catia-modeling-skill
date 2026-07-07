# Live Promoted Remaining Native Runner Report - 2026-07-07

Scope: verify promoted User Mode runners for the remaining imported `NATIVE_SUCCESS` PartDesign regression cases.

Environment: local Windows CATIA V5 automation through pycatia.

## Results

| Recipe | Run ID | Classification | Native Feature | Part.Update | Reference Pattern |
| --- | --- | --- | --- | --- | --- |
| `partdesign.native_v_pulley_shaft` | `20260707_003035_866572` | `NATIVE_SUCCESS` | `Shaft` | true | `partdesign.sketch_revolution_axis`, `partdesign.v_pulley_shaft_profile` |
| `partdesign.native_hole_unit_conversion` | `20260707_003043_293116` | `NATIVE_SUCCESS` | `Hole` | true | `partdesign.inch_to_mm_parameters` |

## Notes

- V pulley is verified as one native CATIA `Shaft` with same-sketch `CenterLine`; the bore boundary and V groove are encoded in the half-profile.
- Unit conversion is verified for explicit inch inputs converted with `25.4` before CATIA millimeter length assignment.
- This batch completes promotion coverage for all 16 imported `NATIVE_SUCCESS` PartDesign regression call patterns, while preserving separate partial/unsupported/failure memory.
- Local CATPart outputs were generated for verification only and are intentionally not committed.
