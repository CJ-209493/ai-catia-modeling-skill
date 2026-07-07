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

This is v1.0.x draft. It initially addresses wrong pycatia call patterns and repeated code-generation mistakes. It leaves room for future upgrades around robust reference selection, complex edge/face filtering, solid loft/sweep, sheet metal, and BRep-to-BRep assembly constraints.

The important modeling knowledge is not merely that pycatia exposes a method. Many CATIA APIs are callable while still failing because the selected reference is wrong. For example, native `Shaft` and `Groove` require an explicit revolution axis in the sketch; without that axis, Codex must not claim native success.

Current package state:

- 3 executable User Mode runner recipes: rectangular Pad, real parameter formula, and Product Fix constraint.
- 16 imported `NATIVE_SUCCESS` CATIA call patterns from the 30-case regression run.
- 2 `PARTIAL_SUCCESS`, 11 `UNSUPPORTED`, and 1 `HONEST_FAILURE` regression memory entries.
- Shaft and Groove are included as imported native-success call patterns using the same-sketch `CenterLine` reference pattern, but they are not yet promoted to executable User Mode runners.
- Latest live CATIA regression evidence: `catia_recipe_regression_20260706_232109`, recorded in `manifests/regression_manifest.yaml` and summarized in `examples/reports/live_regression_20260706_232109.md`.

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

Before executing a feature, Codex should check `manifests/reference_manifest.yaml` for required reference construction. The core draft reference pattern is:

- `partdesign.sketch_revolution_axis`: use for native `Shaft` and `Groove`; create the closed profile and a named construction Line2D revolution axis in the same sketch before calling `add_new_shaft(sketch)` or `add_new_groove(sketch)`.

This pattern is documented in `references/partdesign/sketch_revolution_axis.md`. It is deliberately separate from executable recipe status: knowing the reference pattern does not by itself mean a stable User Mode runner exists.

The 30-case imported regression memory is indexed in `manifests/regression_manifest.yaml`. Native-success entries are also indexed in `manifests/recipe_manifest.yaml` with `runner_kind: imported_call_pattern`, `runner: null`, and `user_mode_allowed: false`. They are useful for Developer Mode recipe promotion and for preventing Codex from rediscovering known pycatia mistakes. The current evidence run was executed live through CATIA COM and generated local CATPart artifacts that are intentionally not committed.

## Run a Verified Recipe

```powershell
python cli\run_feature_plan.py examples\feature_plans\rectangular_pad.yaml
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
- Shaft and Groove have imported native-success call patterns, but still need promoted executable User Mode runners before they can be run directly from a user feature plan.
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
