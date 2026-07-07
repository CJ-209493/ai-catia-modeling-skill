# Live CATIA Visual Verification - 2026-07-07

This report records the live CATIA V5 visual verification pass for promoted executable recipes in the draft AI-CATIA Modeling Skill.

## Scope

- Environment: Windows, CATIA V5 through pycatia COM automation.
- Evidence run: `../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2`.
- Runner count: 23 executable example Feature Plans.
- CATIA evidence: each runner connected to live CATIA, created a CATPart or CATProduct, ran `Part.Update` or `Product.Update`, wrote a runner report, and captured CATIA Viewer screenshots with `Viewer3D.CaptureToFile`.
- Screenshot contact sheets:
  - `../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/contact_sheets/final_contact_sheet_1.png`
  - `../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/contact_sheets/final_contact_sheet_2.png`
  - `../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/contact_sheets/final_contact_sheet_3.png`
  - `../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/contact_sheets/final_contact_sheet_4.png`
- Machine summary: `../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/final_visual_run_summary.json`.

Generated screenshots, CATPart, and CATProduct files are intentionally not committed. They were moved out of the installable skill package into the local evidence archive above.

Image links below are local evidence links. They render on the workstation where `ai-catia-modeling-skill-runtime-evidence` exists; the image binaries are not part of the GitHub skill package.

## Contact Sheets

![Contact sheet 1](../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/contact_sheets/final_contact_sheet_1.png)

![Contact sheet 2](../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/contact_sheets/final_contact_sheet_2.png)

![Contact sheet 3](../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/contact_sheets/final_contact_sheet_3.png)

![Contact sheet 4](../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/contact_sheets/final_contact_sheet_4.png)

## Verdict Terms

- `VISUAL_PASS`: screenshot visibly matches the intended geometric feature and runner verification passed.
- `TREE_PASS_VISUAL_LIMITED`: native feature tree and update verification passed, but the final screenshot is not visually distinctive enough to prove the native operation by appearance alone.
- `NON_GEOMETRIC_TREE_PASS`: the recipe is Knowledgeware or Assembly-tree oriented; screenshots are not geometric proof, so verification relies on parameter/product-tree report fields.

## Summary

- 23/23 executable runners exited successfully against live CATIA.
- 19 geometric recipes have `VISUAL_PASS` screenshots.
- 2 geometric recipes have `TREE_PASS_VISUAL_LIMITED` status: native `Intersect` and native `Split`.
- 2 non-geometric/tree recipes passed their report verification: `knowledgeware.real_param_formula` and `assembly.product_fix_constraint`.
- No screenshot-mismatched geometric recipe was promoted by this pass.

## Reviewed Results

| # | Recipe | Native feature | Verdict | Visual / verifier note |
|---|---|---|---|---|
| 1 | `partdesign.capsule_with_native_holes` | Hole | `VISUAL_PASS` | Capsule plate with two visible end holes; native Hole tree and update passed. |
| 2 | `partdesign.closed_spline_pad` | Pad | `VISUAL_PASS` | Closed spline Pad appears as the intended lens-like solid. |
| 3 | `partdesign.native_chamfer_selected_edge` | Chamfer | `VISUAL_PASS` | Block shows a chamfered selected edge; native Chamfer tree passed. |
| 4 | `partdesign.native_circular_pattern` | CircPattern | `VISUAL_PASS` | Disk shows a center hole and six circular patterned pockets; native CircPattern tree passed. |
| 5 | `partdesign.native_counterbore_holes` | Hole | `VISUAL_PASS` | Top face shows four counterbore holes after switching point sketches to a top offset plane. |
| 6 | `partdesign.native_edge_fillet_selected_edge` | ConstRadEdgeFillet | `VISUAL_PASS` | Block shows a rounded selected edge; native ConstRadEdgeFillet tree passed. |
| 7 | `partdesign.native_groove_centerline` | Groove | `VISUAL_PASS` | Cylinder shows a central groove; same-sketch CenterLine reference pattern passed. |
| 8 | `partdesign.native_hole_from_sketch` | Hole | `VISUAL_PASS` | Plate shows a native hole from a sketch point. |
| 9 | `partdesign.native_hole_unit_conversion` | Hole | `VISUAL_PASS` | Plate shows a converted inch-to-mm hole; conversion values are recorded in the runner report. |
| 10 | `partdesign.native_intersect_two_bodies` | Intersect | `TREE_PASS_VISUAL_LIMITED` | Final shape is visually a cuboid; native Intersect tree, target Body `InWorkObject`, and update verification passed. Screenshot alone is not distinctive. |
| 11 | `partdesign.native_mirror_plane` | Mirror | `VISUAL_PASS` | Plate shows two mirrored bosses across PlaneYZ; native Mirror tree passed. |
| 12 | `partdesign.native_rectangular_pattern` | RectPattern | `VISUAL_PASS` | Plate shows a 3 by 4 boss array after moving the seed boss to the top support plane. |
| 13 | `partdesign.native_shaft_centerline` | Shaft | `VISUAL_PASS` | Stepped revolved shaft is visible; same-sketch CenterLine pattern passed. |
| 14 | `partdesign.native_shell_selected_face` | Shell | `VISUAL_PASS` | Open shell box is visible; native Shell tree passed with selection-derived face reference. |
| 15 | `partdesign.native_slot_pocket` | Pocket | `VISUAL_PASS` | Through racetrack slot is visible after setting pocket direction orientation. |
| 16 | `partdesign.native_split_offset_plane` | Split | `TREE_PASS_VISUAL_LIMITED` | Result appears as a shortened block; native Split tree, offset PlaneXY reference, target Body `InWorkObject`, and update verification passed. Screenshot alone is not distinctive. |
| 17 | `partdesign.native_v_pulley_shaft` | Shaft | `VISUAL_PASS` | V pulley shaft geometry is visible; bore and groove are encoded in one native Shaft profile. |
| 18 | `partdesign.offset_plane_pad` | Pad | `VISUAL_PASS` | Secondary vertical Pad on explicit offset plane is visible. |
| 19 | `partdesign.parametric_plate_formula_holes` | Formula, Pad, Hole | `VISUAL_PASS` | Rectangular plate with four visible native holes after formula-driven length update; parameter offsets and constraints verified. |
| 20 | `assembly.product_fix_constraint` | Constraints | `NON_GEOMETRIC_TREE_PASS` | Product tree shows components and Constraints collection; report confirms `Fix.1` and Product.Update. Screenshot is not geometric proof. |
| 21 | `knowledgeware.real_param_formula` | Formula | `NON_GEOMETRIC_TREE_PASS` | Report confirms Formula relation and output value; screenshot has no meaningful geometry. |
| 22 | `partdesign.rectangular_pad` | Pad | `VISUAL_PASS` | Rectangular block is visible; native Pad tree and update passed. |
| 23 | `partdesign.rounded_rectangle_pad` | Pad | `VISUAL_PASS` | Rounded-rectangle Pad from tangent-arc sketch is visible. |

## Screenshot Gallery

| # | Recipe | Local screenshot evidence |
|---|---|---|
| 1 | `partdesign.capsule_with_native_holes` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/01_capsule_with_native_holes_iso.png" width="360"> |
| 2 | `partdesign.closed_spline_pad` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/02_closed_spline_pad_iso.png" width="360"> |
| 3 | `partdesign.native_chamfer_selected_edge` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/03_native_chamfer_selected_edge_iso.png" width="360"> |
| 4 | `partdesign.native_circular_pattern` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/04_native_circular_pattern_iso.png" width="300"> <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/04_native_circular_pattern_top.png" width="300"> |
| 5 | `partdesign.native_counterbore_holes` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/05_native_counterbore_holes_iso.png" width="300"> <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/05_native_counterbore_holes_top.png" width="300"> |
| 6 | `partdesign.native_edge_fillet_selected_edge` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/06_native_edge_fillet_selected_edge_iso.png" width="360"> |
| 7 | `partdesign.native_groove_centerline` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/07_native_groove_centerline_iso.png" width="360"> |
| 8 | `partdesign.native_hole_from_sketch` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/08_native_hole_from_sketch_iso.png" width="360"> |
| 9 | `partdesign.native_hole_unit_conversion` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/09_native_hole_unit_conversion_iso.png" width="360"> |
| 10 | `partdesign.native_intersect_two_bodies` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/10_native_intersect_two_bodies_iso.png" width="360"> |
| 11 | `partdesign.native_mirror_plane` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/11_native_mirror_plane_iso.png" width="300"> <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/11_native_mirror_plane_top.png" width="300"> |
| 12 | `partdesign.native_rectangular_pattern` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/12_native_rectangular_pattern_iso.png" width="300"> <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/12_native_rectangular_pattern_top.png" width="300"> |
| 13 | `partdesign.native_shaft_centerline` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/13_native_shaft_centerline_iso.png" width="360"> |
| 14 | `partdesign.native_shell_selected_face` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/14_native_shell_selected_face_iso.png" width="360"> |
| 15 | `partdesign.native_slot_pocket` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/15_native_slot_pocket_iso.png" width="300"> <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/15_native_slot_pocket_top.png" width="300"> |
| 16 | `partdesign.native_split_offset_plane` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/16_native_split_offset_plane_iso.png" width="360"> |
| 17 | `partdesign.native_v_pulley_shaft` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/17_native_v_pulley_shaft_iso.png" width="360"> |
| 18 | `partdesign.offset_plane_pad` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/18_offset_plane_pad_iso.png" width="360"> |
| 19 | `partdesign.parametric_plate_formula_holes` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/19_parametric_plate_formula_holes_iso.png" width="300"> <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/19_parametric_plate_formula_holes_top.png" width="300"> |
| 20 | `assembly.product_fix_constraint` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/20_product_fix_constraint_iso.png" width="360"> |
| 21 | `knowledgeware.real_param_formula` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/21_real_param_formula_iso.png" width="360"> |
| 22 | `partdesign.rectangular_pad` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/22_rectangular_pad_iso.png" width="360"> |
| 23 | `partdesign.rounded_rectangle_pad` | <img src="../../../ai-catia-modeling-skill-runtime-evidence/outputs_20260707_live_visual/visual_verification/final_run_v2/screenshots/23_rounded_rectangle_pad_iso.png" width="360"> |

## Fixes Confirmed By Visual Review

- Counterbore holes now use point sketches on an explicit top offset plane instead of bottom XY entry.
- Slot Pocket now sets the pocket direction orientation so the racetrack cut is visible through the plate.
- Rectangular Pattern, Circular Pattern, and Mirror runners build seed features or pockets from top support references before creating native pattern/mirror features.
- Formula-driven plate sketch dimensions are tied to sketch axes with side-preserving constraints; native holes are reversed when created from bottom XY sketches.
- Reports now preserve schema fields required by the skill contract: `mode`, `classifications`, and `feature_results`.

## Promotion Rule Applied

For geometric recipes, API success, `Part.Update`, and native feature-tree checks are not enough. A CATIA screenshot must be reviewed against the intended feature. If the screenshot is wrong-direction, hidden, off-body, or visibly absent, the recipe must not be promoted.

For Knowledgeware-only or Assembly-tree recipes, screenshots are retained as context but not used as geometric proof. Their success claim must come from parameter, relation, constraint, and product-tree verification.
