from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from verifiers.semantic_classifier import classify_feature, is_user_mode_recipe_allowed


def test_geometry_equivalent_is_not_native_success():
    assert classify_feature("Shell", ["Pad"], True, True, geometry_equivalent=True) == "GEOMETRY_EQUIVALENT"


def test_part_update_failure_is_honest_failure():
    assert classify_feature("Pad", ["Pad"], False, True) == "HONEST_FAILURE"


def test_native_success_requires_expected_feature():
    assert classify_feature("Pad", ["Pad"], True, True) == "NATIVE_SUCCESS"
    assert classify_feature("Shell", ["Pad"], True, True) == "PARTIAL_SUCCESS"


def test_user_mode_status_filter():
    assert is_user_mode_recipe_allowed("stable")
    assert is_user_mode_recipe_allowed("verified_repeatable")
    assert is_user_mode_recipe_allowed("live_verified_once")
    assert not is_user_mode_recipe_allowed("experimental")
