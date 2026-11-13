"""Запустить проверки проекта и сохранить фактический протокол ЛР2."""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    commands = [
        ("ruff", "format", "--check", "."),
        ("ruff", "check", "."),
        ("mypy",),
        ("bandit", "-c", "pyproject.toml", "-r", "src"),
        ("lint-imports",),
        ("pytest", "--cov", "--cov-report=term-missing"),
    ]
    output = [
        "Лабораторная работа № 2. Протокол локальных проверок.",
        datetime.now().astimezone().isoformat(timespec="seconds"),
        "Docker не собирался и не запускался.",
    ]
    failed = False
    for command in commands:
        completed = subprocess.run(
            [str(Path(sys.executable).parent / command[0]), *command[1:]],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        output.extend(
            [
                "\n$ " + " ".join(command),
                completed.stdout,
                completed.stderr,
                f"Exit code: {completed.returncode}",
            ]
        )
        print(f"{' '.join(command)}: {completed.returncode}")
        failed |= completed.returncode != 0
    path = ROOT / "docs" / "verification.txt"
    path.parent.mkdir(exist_ok=True)
    path.write_text("\n".join(output) + "\n", encoding="utf-8")
    print(path)
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
