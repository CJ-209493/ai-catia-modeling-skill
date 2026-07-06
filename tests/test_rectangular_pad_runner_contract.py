from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners" / "partdesign"))

from rectangular_pad_runner import normalize_params


def test_normalize_params_sets_defaults_and_numbers():
    params = normalize_params({"width": "120", "height": 80, "depth": 20})
    assert params["part_number"] == "Rectangular_Pad"
    assert params["width"] == 120.0
    assert params["center"] == [0.0, 0.0]
