import subprocess
import sys
from textwrap import dedent


def run_flake8(tmp_path, source):
    target = tmp_path / "sample.py"
    target.write_text(dedent(source))
    return subprocess.run(
        [sys.executable, "-m", "flake8", "--select=DTI", str(target)],
        capture_output=True,
        text=True,
    )


def test_plugin_registered():
    result = subprocess.run(
        [sys.executable, "-m", "flake8", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "flake8-datetime-import" in result.stdout


def test_clean_file_has_no_errors(tmp_path):
    source = """
        import datetime as dt
        import time as tm

        dt.datetime.now()
        tm.time()
    """
    result = run_flake8(tmp_path, source)
    assert result.returncode == 0
    assert result.stdout == ""


def test_DTI100_from_datetime_import(tmp_path):
    result = run_flake8(tmp_path, "from datetime import datetime\n")
    assert "DTI100" in result.stdout
    assert result.returncode == 1


def test_DTI101_bare_import_datetime(tmp_path):
    result = run_flake8(tmp_path, "import datetime\n")
    assert "DTI101" in result.stdout
    assert result.returncode == 1


def test_DTI200_from_time_import(tmp_path):
    result = run_flake8(tmp_path, "from time import sleep\n")
    assert "DTI200" in result.stdout
    assert result.returncode == 1


def test_DTI201_bare_import_time(tmp_path):
    result = run_flake8(tmp_path, "import time\n")
    assert "DTI201" in result.stdout
    assert result.returncode == 1


def test_multiple_violations_reported(tmp_path):
    source = """
        from datetime import datetime
        import time
    """
    result = run_flake8(tmp_path, source)
    assert "DTI100" in result.stdout
    assert "DTI201" in result.stdout
    assert result.returncode == 1
