# Live Promoted Transform and Shell Runner Report - 2026-07-07

Scope: verify promoted User Mode runners for native PartDesign transform and shell features.

Environment: local Windows CATIA V5 automation through pycatia.

## Results

| Recipe | Run ID | Classification | Native Feature | Part.Update | Reference Pattern |
| --- | --- | --- | --- | --- | --- |
| `partdesign.native_mirror_plane` | `20260707_001656_798437` | `NATIVE_SUCCESS` | `Mirror` | true | `partdesign.mirror_plane_ref` |
| `partdesign.native_shell_selected_face` | `20260707_001702_227483` | `NATIVE_SUCCESS` | `Shell` | true | `partdesign.shell_selected_face_ref` |

## Notes

- Mirror is verified for a generated seed Pad mirrored across explicit `OriginElements.PlaneYZ`.
- Shell is verified for a CATIA selection-derived face reference using `Selection.Search("Topology.Face,sel")` and `Selection.Item2(index).Reference`.
- Shell face semantics remain constrained to the selected face index; arbitrary top/front/side face intent still needs future selector and verifier work.
- Local CATPart outputs were generated for verification only and are intentionally not committed.
