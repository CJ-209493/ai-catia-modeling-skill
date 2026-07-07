"""Feature-tree verifier primitives.

These functions accept plain lists so they can be tested without CATIA. Live
CATIA traversal can be added later without changing the semantic contract.
"""


def contains_native_feature(feature_names, expected_native_feature):
    return expected_native_feature in set(feature_names or [])


def verify_native_feature(report, expected_native_feature):
    feature_tree = report.get("feature_tree_contains", [])
    update_ok = bool(report.get("part_update_success"))
    return {
        "passed": update_ok and contains_native_feature(feature_tree, expected_native_feature),
        "expected_native_feature": expected_native_feature,
        "feature_tree_contains": feature_tree,
        "part_update_success": update_ok,
    }


def verify_revolution_centerline_feature(report, expected_native_feature):
    """Verify native Shaft/Groove reports include the required centerline pattern."""
    native = verify_native_feature(report, expected_native_feature)
    required_reference_pattern = "partdesign.sketch_revolution_axis"
    reference_patterns = set(report.get("reference_pattern_ids", []))
    reference_ok = required_reference_pattern in reference_patterns
    native["required_reference_pattern"] = required_reference_pattern
    native["reference_pattern_ids"] = sorted(reference_patterns)
    native["passed"] = native["passed"] and reference_ok
    return native
