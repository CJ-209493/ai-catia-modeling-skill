"""Parameter verifier helpers."""


def require_params(params, required):
    missing = [name for name in required if name not in params]
    return {"passed": not missing, "missing": missing}


def positive_numbers(params, names):
    invalid = [name for name in names if float(params.get(name, 0)) <= 0]
    return {"passed": not invalid, "invalid": invalid}
