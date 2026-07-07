---
name: ai-catia-modeling-skill
description: Use when Codex needs to model CATIA V5 parts or products from natural language through pycatia, especially when verified CATIA feature recipes, reference selection patterns, native feature verification, or honest unsupported/failure reporting are required.
---

# AI-CATIA Modeling Skill

This skill is for Codex + pycatia CATIA V5 modeling. Use it to convert a user's modeling request into a Feature Plan, select verified recipes, apply required reference selection patterns, execute recipe runners, verify the CATIA feature tree, and report results honestly.

## Core Rule

Prefer verified recipes and executable runners. Do not generate fresh pycatia code unless no verified recipe exists and Developer Mode is explicitly enabled.

For CATIA features that are callable through pycatia but sensitive to reference construction, treat reference selection as part of the recipe. API availability is not capability.

## Modes

- **User Mode**: execute only recipes with status `stable`, `verified_repeatable`, or `live_verified_once` that also have an executable `runner` and `user_mode_allowed: true`.
- **Developer Mode**: required to create new recipes, promote recipes, run boundary tests, or write new pycatia calls.
- If mode is not specified, default to User Mode.

Imported regression recipes with `runner_kind: imported_call_pattern` are verified call memory, not User Mode runners. Use their recipe cards for reference selection and future promotion work; do not execute them through `cli/run_feature_plan.py` until a runner and verifier contract have been added.

`partdesign.native_shaft_centerline`, `partdesign.native_v_pulley_shaft`, and `partdesign.native_groove_centerline` are promoted User Mode runners for the verified same-sketch `CenterLine` reference pattern. Use them for the constrained segment-profile Shaft, V pulley half-profile Shaft, and rectangular Groove cases before considering Developer Mode exploration.

`partdesign.native_hole_from_sketch`, `partdesign.native_hole_unit_conversion`, `partdesign.native_counterbore_holes`, `partdesign.capsule_with_native_holes`, and `partdesign.native_slot_pocket` are promoted User Mode runners for constrained base-pad cut cases. Do not extrapolate them to countersink/threaded Hole variants, generic unit parsing, or native Slot features without Developer Mode promotion.

`partdesign.offset_plane_pad`, `partdesign.rounded_rectangle_pad`, and `partdesign.closed_spline_pad` are promoted User Mode runners for constrained Pad profile and support cases. They do not claim arbitrary support-plane inference, separate native Fillet features, sketch constraint completeness, or arbitrary spline repair.

`partdesign.native_rectangular_pattern` and `partdesign.native_circular_pattern` are promoted User Mode runners for constrained seed-feature pattern cases. They require explicit construction direction, center, or axis references; copied geometry is only geometry-equivalent unless the native pattern feature verifies.

`partdesign.native_mirror_plane` and `partdesign.native_shell_selected_face` are promoted User Mode runners for constrained transform and shell cases. Mirror requires the seed feature as `Part.InWorkObject` plus an explicit PlaneYZ reference. Shell requires a CATIA selection-derived face reference and is currently index-based, not arbitrary semantic face selection.

`partdesign.native_edge_fillet_selected_edge` is a promoted User Mode runner for constrained native `ConstRadEdgeFillet` creation from a selection-derived edge reference. It is index-based and does not solve exact four-vertical-edge filtering, arbitrary edge intent, or ordered fillet/chamfer workflows.

`partdesign.native_chamfer_selected_edge` is a promoted User Mode runner for constrained native `Chamfer` creation from a selection-derived edge reference. It is index-based and uses explicit Chamfer enum values; it does not solve ordered fillet/chamfer edge grouping.

## Workflow

1. Parse the user request into a Feature Plan matching `schemas/feature_plan_schema.yaml`.
2. Read `manifests/capability_manifest.yaml` and `manifests/reference_manifest.yaml` for required reference selection patterns.
3. Search `manifests/recipe_manifest.yaml` for verified recipes.
4. If the selected recipe has an executable runner and is allowed in the current mode, execute the matching runner from `runners/`.
5. Run verifiers from `verifiers/`.
6. Classify each feature as `NATIVE_SUCCESS`, `GEOMETRY_EQUIVALENT`, `PARTIAL_SUCCESS`, `HONEST_FAILURE`, or `UNSUPPORTED`.
7. Write a run report matching `schemas/report_schema.yaml`.

## Mandatory Verification Rules

- API call success is not enough. `Part.Update` and verification must pass.
- Native Shell / Mirror / Circular Pattern / Edge Fillet / Sheet Metal / Assembly Constraint cannot be claimed unless the verifier confirms a native CATIA feature tree entry.
- Native `Shaft` and `Groove` require the `partdesign.sketch_revolution_axis` reference pattern unless a recipe documents a stronger verified alternative.
- `Product.Position` is not an Assembly Constraint.
- Cosmetic thread is not solid thread.
- Geometry-equivalent output must be reported as geometry equivalent.
- Do not claim unsupported features as success.

## Reference Selection Patterns

Reference selection patterns live in `manifests/reference_manifest.yaml` and `references/`. Use them before writing or running any feature that depends on selected axes, faces, edges, profiles, or product references.

For `Shaft` and `Groove`, read `references/partdesign/sketch_revolution_axis.md`. The core rule is: create the closed profile and an explicitly named construction Line2D revolution axis in the same sketch before calling `add_new_shaft(sketch)` or `add_new_groove(sketch)`.

For `RectPattern` and `CircPattern`, read `references/partdesign/pattern_references.md`. For `Mirror` and `Shell`, read `references/partdesign/transform_shell_references.md`. For selected-edge `ConstRadEdgeFillet` and `Chamfer`, read `references/partdesign/edge_selection_features.md`. Explicit copied geometry is not native pattern or mirror success, manually built thin walls are not native Shell success, and rounded or beveled sketch geometry is not native edge Fillet/Chamfer success.

For native counterbore Holes, offset-plane Pads, tangent-arc rounded/capsule profiles, and closed spline Pads, read `references/partdesign/profile_and_hole_variants.md`. Pocket-modeled counterbores and holes are not native Hole success.

For V pulley Shaft and inch-to-mm native Hole conversion, read `references/partdesign/v_pulley_and_units.md`. V pulley bore/groove geometry is encoded in one native Shaft profile, and unit conversion must occur before assigning CATIA millimeter length values.

## Recipe Selection

Read `manifests/capability_manifest.yaml` first to understand current v1.0 coverage. Then read only the recipe cards needed for the requested feature.

Use this order:

1. Exact verified recipe match.
2. Compatible verified recipe with explicit caveat.
3. Imported call pattern card, if no executable runner exists.
4. `PARTIAL_SUCCESS`, `UNSUPPORTED`, or `HONEST_FAILURE` report.
5. Developer Mode exploration only if explicitly enabled.

## Regression Memory

`manifests/regression_manifest.yaml` records the imported 30-case CATIA call regression run. In v1.0.11-draft it indexes the live CATIA run `catia_recipe_regression_20260706_232109`: 16 `NATIVE_SUCCESS` call patterns, 2 `PARTIAL_SUCCESS` cases, 11 `UNSUPPORTED` cases, and 1 `HONEST_FAILURE`. These records are developer-stage memory and capability boundary evidence, not a benchmark and not a normal user workflow. Promoted runner evidence is summarized in `examples/reports/live_promoted_revolution_runners_20260706.md`, `examples/reports/live_promoted_cut_runners_20260707.md`, `examples/reports/live_promoted_pattern_runners_20260707.md`, `examples/reports/live_promoted_transform_shell_runners_20260707.md`, `examples/reports/live_promoted_profile_hole_runners_20260707.md`, `examples/reports/live_promoted_remaining_native_runners_20260707.md`, `examples/reports/live_promoted_edge_fillet_runner_20260707.md`, and `examples/reports/live_promoted_chamfer_runner_20260707.md`.

## v1.0 Scope

v1.0 primarily prevents common pycatia call mistakes by routing through known-good recipes, reference selection patterns, and imported call memory. It does not fully solve all CATIA reference selection problems, arbitrary revolved profiles, complex BRep selection, solid loft/sweep edge cases, or full assembly BRep constraints.

## Key Files

- `manifests/recipe_manifest.yaml`: searchable recipe index.
- `manifests/regression_manifest.yaml`: 30-case imported regression memory and failure boundary index.
- `manifests/reference_manifest.yaml`: reference selection patterns that recipes depend on.
- `recipes/`: recipe cards with status and constraints.
- `references/`: reusable reference construction notes for fragile CATIA selections.
- `runners/`: executable pycatia patterns.
- `verifiers/`: semantic and feature-tree classifiers.
- `policies/`: native feature, execution, unsupported, and verification rules.
