---
name: ai-catia-modeling-skill
description: Use when Codex needs to model CATIA V5 parts or products from natural language through pycatia, especially when verified CATIA feature recipes, feature plans, native feature verification, or honest unsupported/failure reporting are required.
---

# AI-CATIA Modeling Skill

This skill is for Codex + pycatia CATIA V5 modeling. Use it to convert a user's modeling request into a Feature Plan, select verified recipes, execute recipe runners, verify the CATIA feature tree, and report results honestly.

## Core Rule

Prefer verified recipes and executable runners. Do not generate fresh pycatia code unless no verified recipe exists and Developer Mode is explicitly enabled.

## Modes

- **User Mode**: use only recipes with status `stable`, `verified_repeatable`, or `live_verified_once`.
- **Developer Mode**: required to create new recipes, promote recipes, run boundary tests, or write new pycatia calls.
- If mode is not specified, default to User Mode.

## Workflow

1. Parse the user request into a Feature Plan matching `schemas/feature_plan_schema.yaml`.
2. Search `manifests/recipe_manifest.yaml` for verified recipes.
3. Execute the matching runner from `runners/`.
4. Run verifiers from `verifiers/`.
5. Classify each feature as `NATIVE_SUCCESS`, `GEOMETRY_EQUIVALENT`, `PARTIAL_SUCCESS`, `HONEST_FAILURE`, or `UNSUPPORTED`.
6. Write a run report matching `schemas/report_schema.yaml`.

## Mandatory Verification Rules

- API call success is not enough. `Part.Update` and verification must pass.
- Native Shell / Mirror / Circular Pattern / Sheet Metal / Assembly Constraint cannot be claimed unless the verifier confirms a native CATIA feature tree entry.
- `Product.Position` is not an Assembly Constraint.
- Cosmetic thread is not solid thread.
- Geometry-equivalent output must be reported as geometry equivalent.
- Do not claim unsupported features as success.

## Recipe Selection

Read `manifests/capability_manifest.yaml` first to understand current v1.0 coverage. Then read only the recipe cards needed for the requested feature.

Use this order:

1. Exact verified recipe match.
2. Compatible verified recipe with explicit caveat.
3. `UNSUPPORTED` or `HONEST_FAILURE` report.
4. Developer Mode exploration only if explicitly enabled.

## v1.0 Scope

v1.0 primarily prevents common pycatia call mistakes by routing through known-good recipes. It does not fully solve all CATIA reference selection problems, complex BRep selection, solid loft/sweep edge cases, or full assembly BRep constraints.

## Key Files

- `manifests/recipe_manifest.yaml`: searchable recipe index.
- `recipes/`: recipe cards with status and constraints.
- `runners/`: executable pycatia patterns.
- `verifiers/`: semantic and feature-tree classifiers.
- `policies/`: native feature, execution, unsupported, and verification rules.
