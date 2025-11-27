"""Simple, defensive math helpers.

The functions here focus on keeping inputs predictable and error messages
clear, avoiding the surprises that come from silently coercing unexpected
values.
"""
from __future__ import annotations

from typing import Iterable, Union

NumberLike = Union[int, float]


def _coerce_number(value: object) -> float:
    """Convert *value* to ``float`` while rejecting invalid types.

    ``bool`` is treated as invalid to avoid accidental truthiness sneaking into
    calculations. A :class:`ValueError` is raised for any input that cannot be
    converted.
    """

    if isinstance(value, bool):
        raise ValueError("Boolean values are not valid numeric inputs.")

    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError) as exc:  # pragma: no cover - defensive
        raise ValueError(f"{value!r} is not a valid number") from exc


def safe_divide(numerator: NumberLike, denominator: NumberLike) -> float:
    """Divide two numbers while guarding against divide-by-zero.

    :raises ValueError: if the denominator is zero or either argument cannot be
        treated as a number.
    """

    num = _coerce_number(numerator)
    den = _coerce_number(denominator)
    if den == 0:
        raise ValueError("Cannot divide by zero.")
    return num / den


def mean(values: Iterable[NumberLike]) -> float:
    """Return the arithmetic mean of *values*.

    Empty iterables or non-numeric inputs raise :class:`ValueError` to surface
    mistakes early.
    """

    coerced = [_coerce_number(value) for value in values]
    if not coerced:
        raise ValueError("Cannot calculate the mean of an empty sequence.")
    return sum(coerced) / len(coerced)


def clamp(value: NumberLike, *, lower: NumberLike | None = None, upper: NumberLike | None = None) -> float:
    """Return *value* constrained between *lower* and *upper* bounds.

    Bounds are optional; when provided they must be valid numbers, and the
    lower bound cannot exceed the upper bound.
    """

    if lower is not None and upper is not None:
        lower_val = _coerce_number(lower)
        upper_val = _coerce_number(upper)
        if lower_val > upper_val:
            raise ValueError("Lower bound cannot exceed upper bound.")
    else:
        lower_val = _coerce_number(lower) if lower is not None else None
        upper_val = _coerce_number(upper) if upper is not None else None

    number = _coerce_number(value)

    if lower_val is not None and number < lower_val:
        number = lower_val
    if upper_val is not None and number > upper_val:
        number = upper_val

    return number
