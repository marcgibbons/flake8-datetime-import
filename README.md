# flake8-datetime-import

<!-- markdownlint-disable MD013 -->
[![codecov](https://codecov.io/gh/marcgibbons/flake8-datetime-import/branch/main/graph/badge.svg?token=Q7FLD0X8IU)](https://codecov.io/gh/marcgibbons/flake8-datetime-import)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/marcgibbons/flake8-datetime-import/main.svg)](https://results.pre-commit.ci/latest/github/marcgibbons/flake8-datetime-import/main)
<!-- markdownlint-enable -->

`flake8-datetime-import` is an opinionated plugin which aims to reduce
confusing or inconsistent usage of Python's `datetime` module. It checks that
`datetime` and `time` are imported as modules and aliased like:

```python
import datetime as dt
import time as tm
```

## Installation

```bash
pip install flake8-datetime-import
```

## flake8 codes

<!-- markdownlint-disable MD013 -->
| Code      | Description |
|-----------|-------------|
| DTI100    | `from datetime import ...` is not allowed. `datetime` must be imported as a module. |
| DTI101    | `datetime` imported without aliasing as `dt`. Expected `import datetime as dt`. |
| DTI200    | `from time import ...` is not allowed. `time` must be imported as a module. |
| DTI201    | `time` imported without aliasing as `tm`. Expected `import time as tm`. |
<!-- markdownlint-enable -->

## Rationale

`datetime` and `time` are confusing when encountered in code. Are they modules?
Are they classes or functions?

```python
# Bad
import datetime
from datetime import datetime, time, timezone

import time
from time import time, timezone
```

Consistently importing and aliasing the `datetime` and `time` modules helps
prevent this ambiguity.

```python
# Good
import datetime as dt
import time as tm

dt.datetime.now()
tm.time()
```

Importing and namespacing `datetime` prevents other naming collisions,
such as Django's `django.utils.timezone`:

```python
import datetime as dt

from django.utils import timezone

dt.timezone.utc
timezone.now()
```

This plugin was inspired by:

- A talk by @brandon-rhodes at PyCon Canada in which he mentioned
  this importing strategy
- Code review fatigue

Other notable mentions of this importing strategy:

<!-- markdownlint-disable MD013 -->
- <https://adamj.eu/tech/2019/09/12/how-i-import-pythons-datetime-module/>
- <https://www.atmos.albany.edu/facstaff/ktyle/pythia/foundations/_build/html/core/datetime/datetime.html>
<!-- markdownlint-enable -->

## pre-commit

To use with pre-commit, add `flake8-datetime-import` as an additional
dependency to `flake8`.

```yaml
# .pre-commit-config.yml

-   repo: https://github.com/pycqa/flake8
    rev: 5.0.4
    hooks:
    -   id: flake8
        additional_dependencies: [
          flake8-datetime-import==0.1.0,
        ]
```
