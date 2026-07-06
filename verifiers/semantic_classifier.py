"""Semantic classification helpers for AI-CATIA reports."""

CLASSIFICATIONS = {
    "NATIVE_SUCCESS",
    "GEOMETRY_EQUIVALENT",
    "PARTIAL_SUCCESS",
    "HONEST_FAILURE",
    "UNSUPPORTED",
}


def classify_feature(native_feature_expected, feature_tree_contains, part_update_success, verifier_passed, geometry_equivalent=False):
    """Return a strict feature classification.

    Geometry-equivalent output is never native success.
    """
    if geometry_equivalent:
        return "GEOMETRY_EQUIVALENT"
    if not part_update_success:
        return "HONEST_FAILURE"
    if verifier_passed and native_feature_expected in set(feature_tree_contains or []):
        return "NATIVE_SUCCESS"
    if feature_tree_contains:
        return "PARTIAL_SUCCESS"
    return "UNSUPPORTED"


def reject_native_claim(reason):
    return {
        "classification": "GEOMETRY_EQUIVALENT",
        "native_success": False,
        "reason": reason,
    }


def is_user_mode_recipe_allowed(status):
    return status in {"stable", "verified_repeatable", "live_verified_once"}
