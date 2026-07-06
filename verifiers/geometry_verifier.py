"""Geometry verifier placeholders for v1.0.

v1.0 runners can report expected dimensions from recipe parameters. Live SPA
measurement integration is intentionally left as an extension point.
"""


def expected_rectangular_pad_bbox(params):
    return [float(params["width"]), float(params["height"]), float(params["depth"])]


def compare_bbox(expected, measured, tolerance=0.1):
    if measured is None:
        return {"passed": False, "reason": "measured bounding box unavailable"}
    if len(expected) != len(measured):
        return {"passed": False, "reason": "bounding box length mismatch"}
    deltas = [abs(float(a) - float(b)) for a, b in zip(expected, measured)]
    return {"passed": all(delta <= tolerance for delta in deltas), "deltas": deltas, "tolerance": tolerance}
