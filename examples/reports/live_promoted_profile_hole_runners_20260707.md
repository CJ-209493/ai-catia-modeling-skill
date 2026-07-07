# Live Promoted Profile and Hole Variant Runner Report - 2026-07-07

Scope: verify promoted User Mode runners for native PartDesign profile and Hole variant features.

Environment: local Windows CATIA V5 automation through pycatia.

## Results

| Recipe | Run ID | Classification | Native Feature | Part.Update | Reference Pattern |
| --- | --- | --- | --- | --- | --- |
| `partdesign.native_counterbore_holes` | `20260707_002457_491882` | `NATIVE_SUCCESS` | `Hole` | true | `partdesign.counterbore_hole_point_sketch` |
| `partdesign.offset_plane_pad` | `20260707_002503_272362` | `NATIVE_SUCCESS` | `Pad` | true | `partdesign.offset_plane_support_ref` |
| `partdesign.rounded_rectangle_pad` | `20260707_002509_849108` | `NATIVE_SUCCESS` | `Pad` | true | `partdesign.tangent_arc_closed_profile` |
| `partdesign.capsule_with_native_holes` | `20260707_002518_804533` | `NATIVE_SUCCESS` | `Hole` | true | `partdesign.capsule_profile_native_holes` |
| `partdesign.closed_spline_pad` | `20260707_002534_617340` | `NATIVE_SUCCESS` | `Pad` | true | `partdesign.closed_spline_profile` |

## Notes

- Counterbore is verified as native CATIA `Hole` features with type/head diameter/head depth set through pycatia/COM properties.
- Offset Plane Pad is verified only for a generated PlaneXY offset support reference.
- Rounded rectangle and capsule profiles are tangent line/arc sketches; they do not claim native Fillet features or full sketch constraint completeness.
- Closed spline Pad is verified for a repeated first/last point profile pattern.
- Local CATPart outputs were generated for verification only and are intentionally not committed.
