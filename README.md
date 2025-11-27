# Safe math helpers

This repository contains a tiny collection of defensive math utilities. The
functions reject ambiguous inputs (such as booleans) and raise clear error
messages so misuse can be caught quickly.

## Usage

```python
import safe_math

result = safe_math.safe_divide(10, 2)  # returns 5.0
average = safe_math.mean([1, 2, 3])    # returns 2.0
bounded = safe_math.clamp(10, lower=0, upper=5)  # returns 5.0
```

## Tests

Install the test dependency and run the suite with `pytest`:

```bash
python -m pip install --upgrade pip
python -m pip install pytest
python -m pytest
```
