"""Run a feature plan using verified recipes."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
USER_ALLOWED_STATUSES = {"stable", "verified_repeatable", "live_verified_once"}


def load_yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def recipe_index():
    manifest = load_yaml(ROOT / "manifests" / "recipe_manifest.yaml")
    return {recipe["id"]: recipe for recipe in manifest["recipes"]}


def run_plan(plan_path):
    plan = load_yaml(plan_path)
    recipes = recipe_index()
    mode = plan.get("mode", "user")
    for feature in plan["features"]:
        recipe = recipes.get(feature["recipe_id"])
        if recipe is None:
            raise SystemExit(f"Unsupported recipe: {feature['recipe_id']}")
        if mode == "user" and recipe["status"] not in USER_ALLOWED_STATUSES:
            raise SystemExit(f"Recipe {recipe['id']} is not allowed in User Mode")
        runner = ROOT / recipe["runner"]
        subprocess.check_call([sys.executable, str(runner), str(plan_path)], cwd=str(ROOT))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("feature_plan")
    args = parser.parse_args()
    run_plan(Path(args.feature_plan))


if __name__ == "__main__":
    main()
