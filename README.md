# AI-CATIA Modeling Skill

AI-CATIA Modeling Skill is a draft Codex skill project for CATIA V5 natural-language modeling with pycatia. It is recipe-driven: Codex should select verified CATIA feature recipes and executable runners instead of inventing pycatia automation code from scratch.

## Why This Exists

Direct Codex + pycatia modeling often fails because CATIA automation is sensitive to active body state, sketch support references, feature direction, COM wrapper properties, and `Part.Update` timing. A pycatia call can exist and still fail if the CATIA references are wrong.

This project captures working patterns as:

- recipe cards
- reference selection patterns
- executable runners
- verifier logic
- failure memory
- policy documents

The goal is not to benchmark CATIA ability. Benchmarking, boundary tests, and memory regression belong to Developer Mode. A normal user should call verified recipes directly.

## Project Status

This is v1.0.12 draft. It initially addresses wrong pycatia call patterns and repeated code-generation mistakes. It leaves room for future upgrades around robust reference selection, complex edge/face filtering, solid loft/sweep, sheet metal, and BRep-to-BRep assembly constraints.

The important modeling knowledge is not merely that pycatia exposes a method. Many CATIA APIs are callable while still failing because the selected reference is wrong. For example, native `Shaft` and `Groove` require an explicit revolution axis in the sketch; without that axis, Codex must not claim native success.

Current package state:

- 21 executable User Mode runner recipes: rectangular Pad, native Hole from sketch point, native Hole with inch-to-mm conversion, native counterbore Holes, native slot Pocket, offset Plane Pad, rounded rectangle Pad, capsule Pad with native Holes, closed spline Pad, native RectPattern, native CircPattern, native Mirror across PlaneYZ, native Shell from selected face reference, selected-edge native ConstRadEdgeFillet, selected-edge native Chamfer, native Split from explicit offset PlaneXY, same-sketch CenterLine Shaft, V pulley Shaft, same-sketch CenterLine Groove, real parameter formula, and Product Fix constraint.
- 16 imported `NATIVE_SUCCESS` CATIA call patterns from the 30-case regression run; all are now represented by promoted executable runners or a stricter promoted runner family.
- 2 `PARTIAL_SUCCESS`, 11 `UNSUPPORTED`, and 1 `HONEST_FAILURE` regression memory entries.
- Shaft and Groove now have promoted executable User Mode runners for the verified same-sketch `CenterLine` reference pattern. The imported regression cards remain as developer evidence and future extension material.
- Hole and Pocket now have promoted executable User Mode runners for constrained base-pad cut cases, native counterbore Hole cases, and capsule end-hole cases. Countersink/threaded hole variants and native Slot features remain separate promotion work.
- Pad profile variants now include promoted executable User Mode runners for offset-plane support, tangent-arc rounded rectangles, and closed spline profiles.
- RectPattern and CircPattern now have promoted executable User Mode runners with explicit construction direction/axis reference patterns.
- V pulley Shaft now has a promoted executable runner using one same-sketch CenterLine half-profile with bore and V groove geometry encoded in the Shaft profile.
- Unit-conversion Hole now has a promoted executable runner that records explicit inch-to-mm conversion before CATIA length assignment.
- Mirror and Shell now have promoted executable User Mode runners for constrained reference patterns. Mirror uses an explicit PlaneYZ reference; Shell uses a CATIA selection-derived face reference by index.
- Edge Fillet now has a promoted executable User Mode runner for constrained selected-edge index references. Exact four-vertical-edge filtering, arbitrary edge intent, and ordered fillet/chamfer workflows remain future work.
- Chamfer now has a promoted executable User Mode runner for constrained selected-edge index references and explicit Chamfer enum values. Ordered fillet/chamfer edge grouping remains future work.
- Split now has a promoted executable User Mode runner for generated offset PlaneXY references. Arbitrary angled cut plane synthesis remains future work.
- Latest live CATIA regression evidence: `catia_recipe_regression_20260706_232109`, recorded in `manifests/regression_manifest.yaml` and summarized in `examples/reports/live_regression_20260706_232109.md`.
- Latest promoted runner evidence: `examples/reports/live_promoted_revolution_runners_20260706.md`.
- Latest promoted cut runner evidence: `examples/reports/live_promoted_cut_runners_20260707.md`.
- Latest promoted pattern runner evidence: `examples/reports/live_promoted_pattern_runners_20260707.md`.
- Latest promoted transform/shell runner evidence: `examples/reports/live_promoted_transform_shell_runners_20260707.md`.
- Latest promoted profile/hole variant evidence: `examples/reports/live_promoted_profile_hole_runners_20260707.md`.
- Latest remaining native-success runner evidence: `examples/reports/live_promoted_remaining_native_runners_20260707.md`.
- Latest edge-fillet runner evidence: `examples/reports/live_promoted_edge_fillet_runner_20260707.md`.
- Latest chamfer runner evidence: `examples/reports/live_promoted_chamfer_runner_20260707.md`.
- Latest split runner evidence: `examples/reports/live_promoted_split_runner_20260707.md`.

## Requirements

- Windows
- CATIA V5 installed and licensed
- Python 3.10+
- `pycatia`
- CATIA must be allowed to run COM automation

Install Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Environment Check

```powershell
python cli\validate_environment.py
python cli\validate_environment.py --live
```

The first command checks Python dependencies. `--live` also attempts to connect to CATIA.

Check the skill package before sharing or installing:

```powershell
python cli\validate_install_package.py .
```

Installers should point at the directory that contains `SKILL.md`. Do not point an installer at the parent `CATIA_Harness` folder, a generated `outputs` folder, or a folder that contains `.CATPart`, `.CATProduct`, `.env`, SQLite databases, screenshots, or logs.

## User Mode vs Developer Mode

User Mode:

- uses only `stable`, `verified_repeatable`, or `live_verified_once` recipes
- requires an executable `runner` and `user_mode_allowed: true`
- does not create new recipes
- does not invent fresh pycatia code
- reports unsupported or partial features honestly

Developer Mode:

- may run boundary probes
- may create new recipes
- may promote recipes after verification
- must preserve failure memory and verifier evidence

## Natural Language to Feature Plan

Codex should first convert a prompt into a Feature Plan, for example:

```yaml
mode: user
units: mm
output_dir: outputs/demo_rectangular_pad
features:
  - id: base_pad
    recipe_id: partdesign.rectangular_pad
    params:
      part_number: Demo_Rectangular_Pad
      width: 120
      height: 80
      depth: 20
      center: [0, 0]
```

Use `templates/feature_plan_template.yaml` as the starting point.

## Reference Selection Patterns

Before executing a feature, Codex should check `manifests/reference_manifest.yaml` for required reference construction. The core draft reference patterns are:

- `partdesign.sketch_revolution_axis`: use for native `Shaft` and `Groove`; create the closed profile and a named construction Line2D revolution axis in the same sketch before calling `add_new_shaft(sketch)` or `add_new_groove(sketch)`.
- `partdesign.rectangular_pattern_direction_refs`: use explicit construction direction references for native `RectPattern`.
- `partdesign.circular_pattern_axis_ref`: use explicit center and axis references for native `CircPattern`.
- `partdesign.mirror_plane_ref`: set the seed feature as `Part.InWorkObject` and pass an explicit mirror plane reference for native `Mirror`.
- `partdesign.shell_selected_face_ref`: use CATIA selection to obtain a face reference before native `Shell`.
- `partdesign.edge_fillet_selected_edge_ref`: use CATIA selection to obtain an edge reference before native `ConstRadEdgeFillet`.
- `partdesign.chamfer_selected_edge_ref`: use CATIA selection to obtain an edge reference before native `Chamfer`.
- `partdesign.counterbore_hole_point_sketch`: create point sketches and set native Hole counterbore COM properties.
- `partdesign.offset_plane_support_ref`: create and reference an explicit offset PlaneXY support for secondary Pads.
- `partdesign.tangent_arc_closed_profile`: draw closed tangent line/arc profiles for rounded rectangle Pads.
- `partdesign.capsule_profile_native_holes`: combine a tangent-arc capsule Pad with native point-sketch Holes.
- `partdesign.closed_spline_profile`: repeat the first point as the final spline pole before creating a Pad.
- `partdesign.v_pulley_shaft_profile`: encode bore and V groove geometry in one native Shaft half-profile.
- `partdesign.inch_to_mm_parameters`: convert inch inputs with 25.4 before assigning CATIA millimeter values.
- `partdesign.split_offset_plane_ref`: create an explicit offset PlaneXY reference and set `Part.InWorkObject` to the target Body before native `Split`.

These patterns are documented in `references/partdesign/sketch_revolution_axis.md`, `references/partdesign/pattern_references.md`, `references/partdesign/transform_shell_references.md`, `references/partdesign/edge_selection_features.md`, `references/partdesign/profile_and_hole_variants.md`, `references/partdesign/v_pulley_and_units.md`, and `references/partdesign/split_references.md`. Arbitrary revolved profiles, arbitrary pattern reference inference, arbitrary mirror planes, semantic Shell face selection, arbitrary edge filtering and operation ordering, arbitrary angled cut plane synthesis, arbitrary spline repair, generic unit parsing, and full sketch constraint inference still require Developer Mode promotion work.

The 30-case imported regression memory is indexed in `manifests/regression_manifest.yaml`. Native-success entries are also indexed in `manifests/recipe_manifest.yaml` with `runner_kind: imported_call_pattern`, `runner: null`, and `user_mode_allowed: false`. They are useful for Developer Mode recipe promotion and for preventing Codex from rediscovering known pycatia mistakes. The current evidence run was executed live through CATIA COM and generated local CATPart artifacts that are intentionally not committed.

## Run a Verified Recipe

```powershell
python cli\run_feature_plan.py examples\feature_plans\rectangular_pad.yaml
python cli\run_feature_plan.py examples\feature_plans\native_hole_from_sketch.yaml
python cli\run_feature_plan.py examples\feature_plans\native_hole_unit_conversion.yaml
python cli\run_feature_plan.py examples\feature_plans\native_counterbore_holes.yaml
python cli\run_feature_plan.py examples\feature_plans\native_slot_pocket.yaml
python cli\run_feature_plan.py examples\feature_plans\offset_plane_pad.yaml
python cli\run_feature_plan.py examples\feature_plans\rounded_rectangle_pad.yaml
python cli\run_feature_plan.py examples\feature_plans\capsule_with_native_holes.yaml
python cli\run_feature_plan.py examples\feature_plans\closed_spline_pad.yaml
python cli\run_feature_plan.py examples\feature_plans\native_rectangular_pattern.yaml
python cli\run_feature_plan.py examples\feature_plans\native_circular_pattern.yaml
python cli\run_feature_plan.py examples\feature_plans\native_mirror_plane.yaml
python cli\run_feature_plan.py examples\feature_plans\native_shell_selected_face.yaml
python cli\run_feature_plan.py examples\feature_plans\native_edge_fillet_selected_edge.yaml
python cli\run_feature_plan.py examples\feature_plans\native_chamfer_selected_edge.yaml
python cli\run_feature_plan.py examples\feature_plans\native_split_offset_plane.yaml
python cli\run_feature_plan.py examples\feature_plans\native_shaft_centerline.yaml
python cli\run_feature_plan.py examples\feature_plans\native_v_pulley_shaft.yaml
python cli\run_feature_plan.py examples\feature_plans\native_groove_centerline.yaml
```

Search recipes:

```powershell
python cli\search_recipe.py pad
python cli\search_recipe.py shaft
```

Search results label executable runners separately from imported call patterns and reference-only patterns.

Open the latest report:

```powershell
python cli\open_latest_report.py outputs
```

## Classification Rules

The skill must distinguish:

- `NATIVE_SUCCESS`
- `GEOMETRY_EQUIVALENT`
- `PARTIAL_SUCCESS`
- `HONEST_FAILURE`
- `UNSUPPORTED`

Geometry-equivalent output must not be reported as native CATIA feature success.

## Current Unsupported or Narrow Boundaries

- Solid rect-to-circle multi-section loft is not fully proven.
- Full 3D rounded-path pipe sweep is not fully proven.
- Solid helix sweep spring is not fully proven.
- Countersink/threaded Hole variants are not yet promoted to User Mode runners.
- A native Slot feature is not claimed; `partdesign.native_slot_pocket` creates a native Pocket from a slot-shaped sketch.
- Counterbore is promoted only through native Hole type/head properties; visual top/bottom direction is not independently measured by the current verifier.
- Rounded rectangle and capsule recipes use tangent-arc sketches; they do not claim separate native Fillet features or full sketch constraint completeness.
- Closed spline Pad is promoted only for a first-point-repeated closed profile; arbitrary spline repair remains future work.
- Unit conversion is promoted only for explicit inch-to-mm numeric conversion; generic text/unit parsing remains future work.
- V pulley Shaft encodes bore and V groove geometry in one native Shaft profile; it does not create separate native Hole or Groove features.
- Pattern recipes are promoted only for generated construction references; inferring directions or axes from arbitrary model edges/faces remains future work.
- Mirror is promoted only for a generated seed feature and explicit PlaneYZ reference; arbitrary mirror plane selection remains future work.
- Shell is promoted only for a selection-index face reference; semantic top/front/side face selection remains future work.
- Edge Fillet is promoted only for a selection-index edge reference that verifies `ConstRadEdgeFillet`; exact four-vertical-edge filtering and ordered fillet/chamfer workflows remain future work.
- Chamfer is promoted only for a selection-index edge reference that verifies `Chamfer`; ordered fillet/chamfer edge grouping remains future work.
- Split is promoted only for generated offset PlaneXY references and explicit target Body `InWorkObject` state; arbitrary angled cut plane synthesis remains future work.
- Arbitrary Shaft/Groove profiles beyond the promoted segment-profile Shaft and rectangular Groove runner are not yet generalized.
- Sheet Metal features are not supported in v1.0.
- Product `Position` is not an assembly constraint.
- BRep-to-BRep Product constraints are not fully proven.
- Cosmetic thread is not solid thread.
- Complex edge/face filtering needs future verifier work.

## Draft Skill Usage Without Installing

Do not copy this folder into Codex's auto-loaded skills directory yet. To test it without installing, start a Codex thread and say:

```text
Use the draft skill at <repo-path> for this request. Read SKILL.md first, then follow its manifests and policies.
```

You can also patch and test the project directly by running its CLI and tests from this repository. This keeps the draft out of global skill discovery while still letting Codex use it explicitly.

## Installation Troubleshooting

If another user gets an install error, ask for the exact error text and run:

```powershell
python cli\validate_install_package.py .
python C:\Users\User\.codex\skills\.system\skill-creator\scripts\quick_validate.py .
```

Common causes are installing the wrong directory, stale generated CATIA files in the package, invalid `SKILL.md` frontmatter, missing recipe runner paths, or private GitHub access not being available to the installer.

## GitHub Notes

Do not commit CATPart/CATProduct outputs, SQLite runtime databases, `.env`, API keys, company-internal paths, large screenshots, or large logs.
