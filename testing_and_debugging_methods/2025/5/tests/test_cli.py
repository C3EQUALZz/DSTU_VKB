"""CLI проверяет результат и сохраняет журнал стандартным FileHandler."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(("version", "status", "marker"), [
    ("legacy", 1, "CHECK: FAIL"), ("fixed", 0, "CHECK: PASS"),
])
def test_cli_check_and_log_file(tmp_path, version, status, marker):
    log_file = tmp_path / "run.log"
    result = subprocess.run(
        [sys.executable, "-m", "fifth_laboratory", "--version", version,
         "--log-level", "DEBUG", "--log-file", str(log_file), "--check"],
        cwd=ROOT, env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
        capture_output=True, text=True,
    )
    assert result.returncode == status
    assert marker in result.stdout
    assert "discount_percent=10 rate=" in log_file.read_text(encoding="utf-8")


def test_cli_invalid_input(tmp_path):
    result = subprocess.run(
        [sys.executable, "-m", "fifth_laboratory", "--input", str(tmp_path / "missing.json")],
        cwd=ROOT, env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
        capture_output=True, text=True,
    )
    assert result.returncode == 2
    assert "ERROR" in result.stderr
    assert "Traceback" in result.stderr
