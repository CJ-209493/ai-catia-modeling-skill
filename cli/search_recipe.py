"""Search verified recipes and reference selection patterns."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_manifest():
    return yaml.safe_load((ROOT / "manifests" / "recipe_manifest.yaml").read_text(encoding="utf-8"))


def load_reference_manifest():
    path = ROOT / "manifests" / "reference_manifest.yaml"
    if not path.exists():
        return {"reference_patterns": []}
    return load_yaml(path)


def search(query):
    query = query.lower()
    matches = []
    for recipe in load_manifest()["recipes"]:
        haystack = " ".join([recipe["id"], recipe.get("title", ""), recipe.get("native_feature", ""), " ".join(recipe.get("tags", []))]).lower()
        if query in haystack:
            item = dict(recipe)
            item["kind"] = "recipe"
            matches.append(item)
    for pattern in load_reference_manifest()["reference_patterns"]:
        haystack = " ".join([pattern["id"], pattern.get("title", ""), " ".join(pattern.get("applies_to", []))]).lower()
        if query in haystack:
            item = dict(pattern)
            item["kind"] = "reference_pattern"
            item["runner"] = None
            matches.append(item)
    return matches


def format_result(item):
    if item["kind"] == "recipe":
        if item.get("runner_kind") == "imported_call_pattern":
            return f"{item['id']} [{item['status']}/imported call pattern] -> recipe card: {item['recipe_card']}"
        return f"{item['id']} [{item['status']}] -> runner: {item['runner']}"
    return f"{item['id']} [{item['status']}] -> reference only: {item['reference_doc']}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    args = parser.parse_args()
    for item in search(args.query):
        print(format_result(item))


if __name__ == "__main__":
    main()
