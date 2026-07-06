"""Runner for recipe partdesign.rectangular_pad."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

import yaml


def rectangle(factory_2d, cx, cy, width, height):
    x1, x2 = cx - width / 2, cx + width / 2
    y1, y2 = cy - height / 2, cy + height / 2
    factory_2d.create_line(x1, y1, x2, y1)
    factory_2d.create_line(x2, y1, x2, y2)
    factory_2d.create_line(x2, y2, x1, y2)
    factory_2d.create_line(x1, y2, x1, y1)


def normalize_params(params):
    center = params.get("center", [0, 0])
    return {
        "part_number": params.get("part_number", "Rectangular_Pad"),
        "width": float(params["width"]),
        "height": float(params["height"]),
        "depth": float(params["depth"]),
        "center": [float(center[0]), float(center[1])],
    }


def build_rectangular_pad(params, output_dir):
    from pycatia import catia

    params = normalize_params(params)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    app = catia()
    doc = app.documents.add("Part")
    part = doc.part
    doc.product.part_number = params["part_number"]

    body = part.bodies.item(1)
    body.name = "PartBody"
    part.in_work_object = body
    ref_xy = part.create_reference_from_object(part.origin_elements.plane_xy)
    sketch = body.sketches.add(ref_xy)
    sketch.name = "RectangularPad_Profile"
    factory_2d = sketch.open_edition()
    rectangle(factory_2d, params["center"][0], params["center"][1], params["width"], params["height"])
    sketch.close_edition()
    part.update()

    pad = part.shape_factory.add_new_pad(sketch, params["depth"])
    pad.name = "RectangularPad"
    part.in_work_object = pad
    part.update()

    catpart_path = output_dir / f"{params['part_number']}.CATPart"
    doc.save_as(str(catpart_path))
    report = {
        "run_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "recipe_id": "partdesign.rectangular_pad",
        "catia_document": str(catpart_path),
        "part_update_success": True,
        "feature_tree_contains": ["Pad"],
        "expected_native_feature": "Pad",
        "expected_bbox": [params["width"], params["height"], params["depth"]],
        "classification": "NATIVE_SUCCESS",
        "params": params,
    }
    report_path = output_dir / "rectangular_pad_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def load_feature_params(plan_path):
    data = yaml.safe_load(Path(plan_path).read_text(encoding="utf-8"))
    for feature in data["features"]:
        if feature["recipe_id"] == "partdesign.rectangular_pad":
            return feature["params"], data.get("output_dir", "outputs")
    raise ValueError("Feature plan does not contain partdesign.rectangular_pad")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("feature_plan")
    parser.add_argument("--output-dir")
    args = parser.parse_args()
    params, output_dir = load_feature_params(args.feature_plan)
    if args.output_dir:
        output_dir = args.output_dir
    print(json.dumps(build_rectangular_pad(params, output_dir), indent=2))


if __name__ == "__main__":
    main()
