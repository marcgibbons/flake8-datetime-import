import ast

import pytest

from flake8_datetime_import import Plugin


def run_plugin(code):
    tree = ast.parse(code)
    plugin = Plugin(tree)
    return {f"{line}:{col} {msg}" for line, col, msg, _ in plugin.run()}


def test_empty():
    assert run_plugin("") == set()


@pytest.mark.parametrize(
    "code",
    [
        "from datetime import datetime",
        "from datetime import time",
        "from datetime import date",
        "from datetime import *",
        "from datetime import datetime, timedelta",
    ],
)
def test_DTI100_from_datetime_import(code):
    result = run_plugin(code)
    assert result == {
        "1:0 DTI100 `from datetime import ...` is not allowed. "
        "`datetime` must be imported as a module."
    }


@pytest.mark.parametrize(
    "code",
    [
        "import datetime",
        "import datetime as foo",
        "import datetime as datetime",
    ],
)
def test_DTI101_import_datetime_not_as_dt(code):
    result = run_plugin("import datetime")
    assert result == {
        "1:0 DTI101 `datetime` imported without aliasing as `dt`. "
        "Expected `import datetime as dt`."
    }


def test_import_datetime_as_dt():
    result = run_plugin("import datetime as dt")
    assert result == set()


@pytest.mark.parametrize(
    "code",
    [
        "from time import time",
        "from time import sleep",
        "from time import *",
        "from time import time, sleep",
    ],
)
def test_DTI200_from_ime_import(code):
    result = run_plugin(code)
    assert result == {
        "1:0 DTI200 `from time import ...` is not allowed. "
        "`time` must be imported as a module."
    }


@pytest.mark.parametrize(
    "code",
    [
        "import time",
        "import time as foo",
        "import time as time",
    ],
)
def test_DTI201_import_time_not_as_tm(code):
    result = run_plugin(code)
    assert result == {
        "1:0 DTI201 `time` imported without aliasing as `tm`. "
        "Expected `import time as tm`."
    }


def test_import_time_as_tm():
    result = run_plugin("import time as tm")
    assert result == set()
