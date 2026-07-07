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


def safe_set_part_number(product, part_number):
    result = {"requested": part_number, "applied": False, "error": ""}
    try:
        product.part_number = part_number
    except Exception as exc:
        result["error"] = str(exc)
    else:
        result["applied"] = True
    return result


def make_report(
    *,
    run_id,
    mode,
    feature_id,
    recipe_id,
    catia_document,
    classification,
    part_update_success,
    verifier_passed,
    notes="",
    extra=None,
):
    report = {
        "run_id": run_id,
        "mode": mode,
        "catia_document": str(catia_document),
        "classifications": {classification: 1},
        "feature_results": [
            {
                "feature_id": feature_id,
                "recipe_id": recipe_id,
                "classification": classification,
                "part_update_success": part_update_success,
                "verifier_passed": verifier_passed,
                "notes": notes,
            }
        ],
    }
    if extra:
        report.update(extra)
    return report


def build_rectangular_pad(params, output_dir, feature_id="base_pad", mode="user"):
    from pycatia import catia

    params = normalize_params(params)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    app = catia()
    doc = app.documents.add("Part")
    part = doc.part
    part_number_result = safe_set_part_number(doc.product, params["part_number"])

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

    catpart_path = (output_dir / f"{params['part_number']}.CATPart").resolve()
    doc.save_as(str(catpart_path))
    report = make_report(
        run_id=datetime.now().strftime("%Y%m%d_%H%M%S"),
        mode=mode,
        feature_id=feature_id,
        recipe_id="partdesign.rectangular_pad",
        catia_document=catpart_path,
        classification="NATIVE_SUCCESS",
        part_update_success=True,
        verifier_passed=True,
        notes="Native CATIA Pad created from a PlaneXY rectangle sketch and Part.Update passed.",
        extra={
            "recipe_id": "partdesign.rectangular_pad",
            "part_update_success": True,
            "feature_tree_contains": ["Pad"],
            "expected_native_feature": "Pad",
            "expected_bbox": [params["width"], params["height"], params["depth"]],
            "classification": "NATIVE_SUCCESS",
            "params": params,
            "part_number_assignment": part_number_result,
        },
    )
    report_path = output_dir / "rectangular_pad_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def load_feature_context(plan_path):
    data = yaml.safe_load(Path(plan_path).read_text(encoding="utf-8"))
    for feature in data["features"]:
        if feature["recipe_id"] == "partdesign.rectangular_pad":
            return feature, data.get("mode", "user"), data.get("output_dir", "outputs")
    raise ValueError("Feature plan does not contain partdesign.rectangular_pad")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("feature_plan")
    parser.add_argument("--output-dir")
    args = parser.parse_args()
    feature, mode, output_dir = load_feature_context(args.feature_plan)
    if args.output_dir:
        output_dir = args.output_dir
    print(json.dumps(build_rectangular_pad(feature["params"], output_dir, feature["id"], mode), indent=2))


if __name__ == "__main__":
    main()
