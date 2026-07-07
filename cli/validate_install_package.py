"""Validate that the repository root is installable as a Codex skill package."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml


NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
BLOCKED_SUFFIXES = {
    ".CATPart",
    ".CATProduct",
    ".CATDrawing",
    ".cgr",
    ".sqlite",
    ".sqlite3",
    ".db",
    ".env",
}
REQUIRED_DIRS = [
    "manifests",
    "schemas",
    "recipes",
    "runners",
    "verifiers",
    "references",
    "policies",
    "failures",
    "cli",
    "templates",
]


def read_frontmatter(skill_md):
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, "SKILL.md must start with YAML frontmatter"
    end = text.find("\n---", 4)
    if end == -1:
        return None, "SKILL.md frontmatter must be closed with ---"
    try:
        return yaml.safe_load(text[4:end]) or {}, None
    except yaml.YAMLError as exc:
        return None, f"SKILL.md frontmatter is invalid YAML: {exc}"


def validate_skill_package(root):
    root = Path(root).resolve()
    errors = []
    warnings = []

    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        errors.append("Missing SKILL.md at package root")
    else:
        frontmatter, frontmatter_error = read_frontmatter(skill_md)
        if frontmatter_error:
            errors.append(frontmatter_error)
        else:
            name = frontmatter.get("name")
            description = frontmatter.get("description")
            if not name:
                errors.append("SKILL.md frontmatter missing name")
            elif not NAME_RE.match(name):
                errors.append("SKILL.md name must use lowercase letters, digits, and hyphens only")
            if not description:
                errors.append("SKILL.md frontmatter missing description")
            elif len(description) > 500:
                warnings.append("SKILL.md description is long; keep trigger metadata concise")
            if name and root.name != name:
                warnings.append(f"Package folder name '{root.name}' differs from SKILL.md name '{name}'")

    agents_metadata = root / "agents" / "openai.yaml"
    if agents_metadata.exists():
        try:
            data = yaml.safe_load(agents_metadata.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            errors.append(f"agents/openai.yaml is invalid YAML: {exc}")
        else:
            interface = data.get("interface", {})
            for key in ["display_name", "short_description", "default_prompt"]:
                if not interface.get(key):
                    warnings.append(f"agents/openai.yaml missing interface.{key}")

    for directory in REQUIRED_DIRS:
        if not (root / directory).exists():
            warnings.append(f"Expected project directory missing: {directory}")

    recipe_manifest = root / "manifests" / "recipe_manifest.yaml"
    if recipe_manifest.exists():
        try:
            manifest = yaml.safe_load(recipe_manifest.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            errors.append(f"recipe_manifest.yaml is invalid YAML: {exc}")
        else:
            for recipe in manifest.get("recipes", []):
                for key in ["recipe_card", "runner"]:
                    value = recipe.get(key)
                    if value and not (root / value).exists():
                        errors.append(f"Recipe {recipe.get('id', '<unknown>')} points to missing {key}: {value}")
    else:
        warnings.append("Missing manifests/recipe_manifest.yaml")

    reference_manifest = root / "manifests" / "reference_manifest.yaml"
    if reference_manifest.exists():
        try:
            manifest = yaml.safe_load(reference_manifest.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            errors.append(f"reference_manifest.yaml is invalid YAML: {exc}")
        else:
            for pattern in manifest.get("reference_patterns", []):
                reference_doc = pattern.get("reference_doc")
                if reference_doc and not (root / reference_doc).exists():
                    errors.append(f"Reference pattern {pattern.get('id', '<unknown>')} points to missing reference_doc: {reference_doc}")
                for failure_path in pattern.get("failure_memory", []):
                    if not (root / failure_path).exists():
                        errors.append(f"Reference pattern {pattern.get('id', '<unknown>')} points to missing failure memory: {failure_path}")

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.name == ".env" or path.suffix in BLOCKED_SUFFIXES:
            errors.append(f"Blocked runtime or sensitive artifact present: {path.relative_to(root)}")

    return {"errors": errors, "warnings": warnings}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    result = validate_skill_package(Path(args.root))
    for warning in result["warnings"]:
        print(f"warning: {warning}")
    for error in result["errors"]:
        print(f"error: {error}")
    if result["errors"]:
        raise SystemExit(1)
    print("install package preflight: ok")


if __name__ == "__main__":
    main()
