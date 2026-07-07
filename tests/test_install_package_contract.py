from pathlib import Path
import importlib.util
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def load_install_validator():
    path = ROOT / "cli" / "validate_install_package.py"
    spec = importlib.util.spec_from_file_location("validate_install_package", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_install_package_validator_accepts_current_project():
    validator = load_install_validator()
    result = validator.validate_skill_package(ROOT)
    assert result["errors"] == []
    assert result["warnings"] == []


def test_install_package_validator_accepts_relative_project_path(monkeypatch):
    validator = load_install_validator()
    monkeypatch.chdir(ROOT)
    result = validator.validate_skill_package(Path("."))
    assert result["errors"] == []
    assert result["warnings"] == []


def test_install_package_validator_rejects_missing_skill_md():
    validator = load_install_validator()
    with tempfile.TemporaryDirectory(prefix="install-validator-", dir=ROOT) as tmp_dir:
        result = validator.validate_skill_package(Path(tmp_dir))
        assert any("SKILL.md" in error for error in result["errors"])
