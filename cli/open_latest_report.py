"""Print the latest report path under an output directory."""

from __future__ import annotations

import argparse
from pathlib import Path


def latest_report(root):
    reports = list(Path(root).rglob("*report*.*"))
    if not reports:
        return None
    return max(reports, key=lambda path: path.stat().st_mtime)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default="outputs")
    args = parser.parse_args()
    report = latest_report(args.root)
    if report is None:
        raise SystemExit("No reports found")
    print(report)


if __name__ == "__main__":
    main()
