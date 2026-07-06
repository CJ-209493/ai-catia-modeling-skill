"""Search recipe_manifest.yaml."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_manifest():
    return yaml.safe_load((ROOT / "manifests" / "recipe_manifest.yaml").read_text(encoding="utf-8"))


def search(query):
    query = query.lower()
    matches = []
    for recipe in load_manifest()["recipes"]:
        haystack = " ".join([recipe["id"], recipe.get("title", ""), recipe.get("native_feature", ""), " ".join(recipe.get("tags", []))]).lower()
        if query in haystack:
            matches.append(recipe)
    return matches


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    args = parser.parse_args()
    for recipe in search(args.query):
        print(f"{recipe['id']} [{recipe['status']}] -> {recipe['runner']}")


if __name__ == "__main__":
    main()
