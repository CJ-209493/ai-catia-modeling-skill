import pytest

from cli import run_feature_plan


def test_imported_call_pattern_cannot_be_executed_as_user_recipe():
    plan_path = "tests/fixtures/imported_call_pattern_plan.yaml"
    with pytest.raises(SystemExit) as excinfo:
        run_feature_plan.run_plan(plan_path)

    assert "has no executable runner" in str(excinfo.value)
