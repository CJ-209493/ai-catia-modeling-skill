"""Validate local AI-CATIA environment."""

from __future__ import annotations

import argparse
import importlib.util
import platform
import sys


def check_import(name):
    return importlib.util.find_spec(name) is not None


def validate(live=False):
    results = {
        "platform": platform.system(),
        "python": sys.version.split()[0],
        "pycatia_importable": check_import("pycatia"),
        "yaml_importable": check_import("yaml"),
        "catia_live": None,
    }
    if live:
        try:
            from pycatia import catia

            app = catia()
            results["catia_live"] = True
            results["catia_documents_count"] = app.documents.count
        except Exception as exc:
            results["catia_live"] = False
            results["catia_error"] = f"{exc.__class__.__name__}: {exc}"
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="Attempt to connect to CATIA V5 through COM.")
    args = parser.parse_args()
    results = validate(args.live)
    for key, value in results.items():
        print(f"{key}: {value}")
    if results["platform"] != "Windows" or not results["pycatia_importable"] or not results["yaml_importable"]:
        raise SystemExit(1)
    if args.live and not results["catia_live"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
