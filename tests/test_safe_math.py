import math
import pytest

import safe_math


def test_safe_divide_success():
    assert safe_math.safe_divide(10, 2) == 5
    assert safe_math.safe_divide(7.5, 2.5) == 3


def test_safe_divide_rejects_zero_division():
    with pytest.raises(ValueError):
        safe_math.safe_divide(1, 0)


def test_mean_accepts_numeric_strings():
    assert math.isclose(safe_math.mean(["1", "2", "3.5"]), 2.1666666667, rel_tol=1e-9)


def test_mean_rejects_empty_sequence():
    with pytest.raises(ValueError):
        safe_math.mean([])


def test_clamp_no_bounds_returns_value():
    assert safe_math.clamp(5) == 5


def test_clamp_applies_lower_and_upper_bounds():
    assert safe_math.clamp(1, lower=2) == 2
    assert safe_math.clamp(5, upper=3) == 3
    assert safe_math.clamp(4, lower=2, upper=6) == 4


def test_clamp_rejects_invalid_bounds():
    with pytest.raises(ValueError):
        safe_math.clamp(1, lower=5, upper=3)


def test_clamp_rejects_boolean_inputs():
    with pytest.raises(ValueError):
        safe_math.clamp(True, lower=0, upper=1)
