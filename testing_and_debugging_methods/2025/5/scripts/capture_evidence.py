"""Реальные запуски CLI/pytest и оформление их вывода через Freeze.

Ошибочная версия для красного регрессионного теста создаётся в /tmp;
рабочие исходники и тесты при этом не меняются.
"""

import difflib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "report_assets"
LOGS = ASSETS / "logs"
SCREENS = ROOT.parent / "docs/screenshots/lab_05"
BEFORE = 'rate = Decimal(int(order.discount_percent / Decimal("100")))'
AFTER = 'rate = order.discount_percent / Decimal("100")'


def main():
    LOGS.mkdir(parents=True, exist_ok=True)
    SCREENS.mkdir(parents=True, exist_ok=True)
    manifest = []

    def capture(name, args, expected_code, *, cwd=ROOT, source=ROOT / "src"):
        command = [sys.executable, *args]
        env = {**os.environ, "PYTHONPATH": str(source), "NO_COLOR": "1", "COLUMNS": "96"}
        result = subprocess.run(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True)
        # Относительный путь делает команду в иллюстрации переносимой.
        display = "PYTHONPATH=src .venv/bin/python " + " ".join(args)
        content = f"$ {display}\n\n{result.stdout.rstrip()}\n\n[exit code: {result.returncode}]\n"
        (LOGS / f"{name}.txt").write_text(content, encoding="utf-8")
        manifest.append({"name": name, "command": display, "exit_code": result.returncode,
                         "expected_exit_code": expected_code, "snapshot": source != ROOT / "src"})
        if result.returncode != expected_code:
            raise RuntimeError(f"{name}: unexpected exit code {result.returncode}\n{result.stdout}")
        render(LOGS / f"{name}.txt", name, language="text")
        print(f"{name}: exit {result.returncode} (expected {expected_code})", flush=True)

    capture("01_reproduce", ["-m", "fifth_laboratory", "--version", "legacy", "--check"], 1)
    capture("02_trace_legacy", ["-m", "fifth_laboratory", "--version", "legacy", "--log-level", "DEBUG",
                                "--log-file", "report_assets/logs/legacy.log", "--check"], 1)
    # Изолированный снимок до исправления: тот же тест, одна изменённая строка.
    with tempfile.TemporaryDirectory(prefix="lab5-before-") as directory:
        snapshot = Path(directory)
        for folder in ("src", "tests", "data"):
            shutil.copytree(ROOT / folder, snapshot / folder, ignore=shutil.ignore_patterns("__pycache__"))
        original = snapshot / "src/fifth_laboratory/order.py"
        text = original.read_text(encoding="utf-8")
        assert text.count(AFTER) == 1, "Expected exactly one corrected line"
        original.write_text(text.replace(AFTER, BEFORE), encoding="utf-8")
        capture("03_regression_before", ["-m", "pytest", "tests/test_order.py::test_discount_regression", "-q",
                                          "--tb=short", "-o", "console_output_style=classic"], 1,
                cwd=snapshot, source=snapshot / "src")

    capture("04_trace_fixed", ["-m", "fifth_laboratory", "--version", "fixed", "--log-level", "DEBUG",
                               "--log-file", "report_assets/logs/fixed.log", "--check"], 0)
    capture("05_regression_after", ["-m", "pytest", "tests/test_order.py::test_discount_regression", "-q",
                                    "--tb=short", "-o", "console_output_style=classic"], 0)
    capture("06_tests", ["-m", "pytest", "-vv", "--tb=short", "-o", "console_output_style=classic"], 0)
    capture("07_info", ["-m", "fifth_laboratory", "--check"], 0)
    source = (ROOT / "src/fifth_laboratory/order.py").read_text(encoding="utf-8")
    fixed = source.splitlines(keepends=True)
    buggy = source.replace(AFTER, BEFORE).splitlines(keepends=True)
    diff = "".join(difflib.unified_diff(buggy, fixed, fromfile="order.py (before)", tofile="order.py (after)"))
    (LOGS / "08_fix.diff").write_text(diff, encoding="utf-8")
    render(LOGS / "08_fix.diff", "08_fix", language="diff")
    cli_source = (ROOT / "src/fifth_laboratory/__main__.py").read_text(encoding="utf-8")
    config = cli_source[cli_source.index("def configure_logging"):cli_source.index("\n\ndef main")]
    (LOGS / "09_logging.py").write_text("import logging\nfrom pathlib import Path\n\n" + config.rstrip() + "\n", encoding="utf-8")
    render(LOGS / "09_logging.py", "09_logging", language="python")
    (ASSETS / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render(path, name, *, language):
    svg_path = SCREENS / f"{name}.svg"
    subprocess.run([
        "freeze", str(path), "--output", str(svg_path),
        "--language", language, "--theme", "github-dark", "--window",
        "--font.family", "FiraCode Nerd Font", "--font.size", "16", "--line-height", "1.35",
        "--padding", "22", "--margin", "24", "--border.radius", "12",
        "--background", "#e9edf4", "--shadow.blur", "12", "--shadow.y", "5", "--wrap", "100",
    ], check=True, cwd=ROOT)
    # Freeze 0.2.2 ссылается на отсутствующий terminalMask: это скрывает текст
    # в PNG. Восстанавливаем только SVG-область отсечения; вывод не изменяется.
    svg = ET.fromstring(svg_path.read_text(encoding="utf-8"))
    ns = "{http://www.w3.org/2000/svg}"
    if language == "diff":
        # Freeze размещает фон diff в ch/em без отступов окна. CairoSVG
        # рисует эти плашки поверх заголовка. Оставляем цвет текста +/-;
        # убираем только декоративный фон внутри текстовой группы.
        for group in svg.findall(ns + "g"):
            for background in list(group.findall(ns + "rect")):
                group.remove(background)
    definitions = ET.SubElement(svg, ns + "defs")
    clip = ET.SubElement(definitions, ns + "clipPath", {"id": "terminalMask"})
    ET.SubElement(clip, ns + "rect", {"width": svg.attrib["width"], "height": svg.attrib["height"]})
    ET.register_namespace("", ns[1:-1])
    svg_path.write_bytes(ET.tostring(svg, encoding="utf-8", xml_declaration=True))
    config_path = ASSETS / "fonts.conf"
    config_path.write_text(
        '<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig>'
        '<dir>/System/Library/Fonts</dir><dir>/System/Library/Fonts/Supplemental</dir>'
        f'<dir>{Path.home() / "Library/Fonts"}</dir>'
        f'<cachedir>{ASSETS / "font-cache"}</cachedir></fontconfig>', encoding="utf-8")
    env = {**os.environ, "DYLD_FALLBACK_LIBRARY_PATH": "/opt/homebrew/lib", "FONTCONFIG_FILE": str(config_path)}
    subprocess.run([sys.executable, "-c", "import cairosvg,sys; cairosvg.svg2png(url=sys.argv[1], write_to=sys.argv[2], scale=2, background_color='#e9edf4')",
                    str(svg_path), str(SCREENS / f"{name}.png")], env=env, check=True)


if __name__ == "__main__":
    main()
