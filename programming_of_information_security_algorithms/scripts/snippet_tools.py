"""Утилиты для генерации freeze-сниппетов (PNG) кода и терминальных логов.

Назначение:
- render_code(source, out_png, language="rust") — PNG с подсветкой кода.
- render_term(ansi_text, out_png) — PNG с эмуляцией терминала (сохраняет ANSI).
- split_text(text, max_lines) — нарезка длинного текста на части одинакового размера.

Все вызовы — синхронные, ошибки прокидываются как CalledProcessError.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

FREEZE = shutil.which("freeze") or "freeze"

# Параметры рендера. Размер 1100 пикселей по ширине + ~28 строк помещается на
# страницу Word при width_cm=15.5 (см. report_builder.add_image).
CODE_THEME = "github"
TERM_THEME = "dracula"
FONT_FAMILY = ""  # пусто — freeze возьмёт встроенный JetBrains Mono (надёжно)
FONT_SIZE = 14
WIDTH = 110  # символов в строке (для языкового рендера)


def _run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"freeze failed (exit {proc.returncode}):\n"
            f"  cmd: {' '.join(cmd)}\n"
            f"  stdout: {proc.stdout}\n"
            f"  stderr: {proc.stderr}"
        )


def render_code(
    source: str,
    out_png: Path,
    *,
    language: str = "rust",
    theme: str = CODE_THEME,
    width: int | None = None,
    font_size: int = FONT_SIZE,
    show_line_numbers: bool = True,
) -> Path:
    """Рендер кода → PNG через freeze с подсветкой."""
    out_png = Path(out_png)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=f".{language}", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(source)
        tmp_path = Path(tmp.name)
    try:
        cmd: list[str] = [
            FREEZE,
            str(tmp_path),
            "--language", language,
            "--theme", theme,
            "--output", str(out_png),
            "--font.size", str(font_size),
            "--padding", "20,30",
            "--margin", "20",
            "--border.radius", "8",
            "--shadow.blur", "16",
            "--shadow.x", "0",
            "--shadow.y", "8",
            "--background", "#ffffff",
        ]
        if FONT_FAMILY:
            cmd.extend(["--font.family", FONT_FAMILY])
        if show_line_numbers:
            cmd.append("--show-line-numbers")
        if width:
            cmd.extend(["--width", str(width)])
        _run(cmd)
        return out_png
    finally:
        tmp_path.unlink(missing_ok=True)


def render_term(
    ansi_text: str,
    out_png: Path,
    *,
    theme: str = TERM_THEME,
    width: int | None = None,
    font_size: int = FONT_SIZE,
    wrap: int | None = 100,
) -> Path:
    """Рендер ANSI-вывода → PNG через freeze c терминальным фреймом."""
    out_png = Path(out_png)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(ansi_text)
        tmp_path = Path(tmp.name)
    try:
        cmd: list[str] = [
            FREEZE,
            str(tmp_path),
            "--theme", theme,
            "--output", str(out_png),
            "--font.size", str(font_size),
            "--padding", "20,30",
            "--margin", "20",
            "--border.radius", "8",
            "--shadow.blur", "16",
            "--shadow.x", "0",
            "--shadow.y", "8",
            "--window",
        ]
        if FONT_FAMILY:
            cmd.extend(["--font.family", FONT_FAMILY])
        if width:
            cmd.extend(["--width", str(width)])
        if wrap:
            cmd.extend(["--wrap", str(wrap)])
        _run(cmd)
        return out_png
    finally:
        tmp_path.unlink(missing_ok=True)


def split_text(text: str, max_lines: int) -> list[str]:
    """Разбиение длинного текста на части ≤ max_lines строк."""
    lines = text.splitlines()
    if not lines:
        return [""]
    return [
        "\n".join(lines[i : i + max_lines])
        for i in range(0, len(lines), max_lines)
    ]


def render_code_chunked(
    source: str,
    out_dir: Path,
    base_name: str,
    *,
    language: str = "rust",
    max_lines: int = 30,
    theme: str = CODE_THEME,
    font_size: int = FONT_SIZE,
) -> list[Path]:
    """Рендерит длинный исходник по частям. Возвращает список PNG."""
    parts = split_text(source, max_lines)
    out: list[Path] = []
    for idx, part in enumerate(parts, start=1):
        suffix = f"_{idx}" if len(parts) > 1 else ""
        png = Path(out_dir) / f"{base_name}{suffix}.png"
        render_code(
            part,
            png,
            language=language,
            theme=theme,
            font_size=font_size,
        )
        out.append(png)
    return out


def render_term_chunked(
    ansi_text: str,
    out_dir: Path,
    base_name: str,
    *,
    max_lines: int = 28,
    theme: str = TERM_THEME,
    font_size: int = FONT_SIZE,
    wrap: int | None = 100,
) -> list[Path]:
    """Терминальный вывод по частям."""
    parts = split_text(ansi_text, max_lines)
    out: list[Path] = []
    for idx, part in enumerate(parts, start=1):
        suffix = f"_{idx}" if len(parts) > 1 else ""
        png = Path(out_dir) / f"{base_name}{suffix}.png"
        render_term(part, png, theme=theme, font_size=font_size, wrap=wrap)
        out.append(png)
    return out


_BAD_CONTROL = {
    "\x00",  # NUL
    "\x07",  # BEL
    "\x08",  # backspace — ломает SVG в freeze
    "\x0b",  # VT
    "\x0c",  # FF
    "\x0e",  # SO
    "\x0f",  # SI
}


def _clean_ansi(text: str) -> str:
    """Очистка ANSI-потока для безопасной передачи в freeze.

    Убирает: CR, плохие управляющие коды, остаточный ^D от script(1) на macOS.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    for ch in _BAD_CONTROL:
        text = text.replace(ch, "")
    # script(1) на macOS иногда оставляет последовательность "^D\b" в конце.
    text = text.replace("^D", "")
    # Иногда script печатает первую строку «Script started…» — её мы не запрашивали.
    # На macOS с `-q /dev/null` такой строки нет; на всякий случай отрезаем её, если появилась.
    lines = text.split("\n")
    while lines and lines[0].startswith("Script started"):
        lines.pop(0)
    while lines and lines[-1].startswith("Script done"):
        lines.pop()
    return "\n".join(lines).rstrip("\n") + "\n"


def capture_command(
    cmd: list[str],
    cwd: Path | None = None,
    env_extra: dict[str, str] | None = None,
    *,
    timeout: int = 300,
    use_pty: bool = True,
) -> tuple[str, int]:
    """Запуск команды с принудительным цветом (CLICOLOR_FORCE=1) через эмуляцию TTY.

    На macOS используется `script -q /dev/null`, на Linux — `script -qfc cmd /dev/null`.
    Возвращает (очищенный ANSI-вывод, exit_code).
    """
    import os
    import sys

    env = os.environ.copy()
    env["CLICOLOR_FORCE"] = "1"
    env["FORCE_COLOR"] = "1"
    env["TERM"] = "xterm-256color"
    if env_extra:
        env.update(env_extra)

    wrapped = cmd
    if use_pty and shutil.which("script"):
        if sys.platform == "darwin":
            wrapped = ["script", "-q", "/dev/null", *cmd]
        else:
            joined = " ".join(__import__("shlex").quote(a) for a in cmd)
            wrapped = ["script", "-qfc", joined, "/dev/null"]
    proc = subprocess.run(
        wrapped, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout
    )
    output = proc.stdout
    if proc.stderr:
        output += proc.stderr
    return _clean_ansi(output), proc.returncode
