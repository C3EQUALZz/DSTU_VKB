"""Реальные сессии pdb/pytest; терминальные иллюстрации оформляет Freeze."""

import argparse
import difflib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from xml.etree import ElementTree as ET

import pexpect

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "report_assets"
LOGS = ASSETS / "logs"
SCREENS = ROOT.parent / "docs/screenshots/lab_06"
ENV = {**os.environ, "NO_COLOR": "1", "PYTHON_COLORS": "0", "COLUMNS": "88"}


def render(path, name, language="text", lines=None):
    svg_path = SCREENS / f"{name}.svg"
    options = ["--lines", lines] if lines else []
    subprocess.run([
        "freeze", str(path), "--output", str(svg_path), "--language", language,
        "--theme", "github-dark", "--window", "--font.family", "FiraCode Nerd Font",
        "--font.size", "16", "--line-height", "1.35", "--padding", "22", "--margin", "24",
        "--border.radius", "12", "--wrap", "92", *options,
    ], check=True, cwd=ROOT)
    ns = "{http://www.w3.org/2000/svg}"
    svg = ET.fromstring(svg_path.read_bytes())
    # Исправления SVG Freeze 0.2.2: отсутствующий clipPath и съехавший фон diff.
    if language == "diff":
        for group in svg.findall(ns + "g"):
            for rect in group.findall(ns + "rect"):
                group.remove(rect)
    clip = ET.SubElement(ET.SubElement(svg, ns + "defs"), ns + "clipPath", {"id": "terminalMask"})
    ET.SubElement(clip, ns + "rect", {"width": svg.attrib["width"], "height": svg.attrib["height"]})
    ET.register_namespace("", ns[1:-1])
    svg_path.write_bytes(ET.tostring(svg, encoding="utf-8", xml_declaration=True))
    config_path = ASSETS / "fonts.conf"
    config_path.write_text(
        '<?xml version="1.0"?><fontconfig><dir>/System/Library/Fonts</dir>'
        f'<dir>{Path.home() / "Library/Fonts"}</dir><cachedir>{ASSETS / "font-cache"}</cachedir></fontconfig>',
        encoding="utf-8")
    env = {**ENV, "DYLD_FALLBACK_LIBRARY_PATH": "/opt/homebrew/lib", "FONTCONFIG_FILE": str(config_path)}
    subprocess.run([sys.executable, "-c", "import cairosvg,sys; cairosvg.svg2png(url=sys.argv[1], write_to=sys.argv[2], scale=2, background_color='#e9edf4')", str(svg_path), str(SCREENS / f"{name}.png")], env=env, check=True)


def command(name, args, expected, cwd=ROOT):
    run = subprocess.run([sys.executable, *args], cwd=cwd, env=ENV, text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    text = "$ .venv/bin/python " + " ".join(args) + "\n\n" + run.stdout.rstrip() + f"\n\n[exit code: {run.returncode}]\n"
    output = LOGS / f"{name}.txt"
    output.write_text(text, encoding="utf-8")
    assert run.returncode == expected, text
    render(output, name)
    return {"name": name, "args": args, "exit_code": run.returncode}


def pdb_session(name, version, commands):
    output = LOGS / f"{name}.txt"
    with output.open("w", encoding="utf-8") as log:
        log.write(f"$ .venv/bin/python -m pdb demo.py --version {version}\n\n")
        child = pexpect.spawn(sys.executable, ["-m", "pdb", "demo.py", "--version", version],
                              cwd=str(ROOT), env=ENV, encoding="utf-8", timeout=15,
                              dimensions=(80, 100))
        child.logfile_read = log
        child.expect_exact("(Pdb) ")
        for cmd in commands:
            child.sendline(cmd)
            if cmd == "q":
                child.expect(pexpect.EOF)
            else:
                child.expect_exact("(Pdb) ")
        child.close()
        assert child.exitstatus == 0
    output.write_text(output.read_text(encoding="utf-8").replace("\r\n", "\n"), encoding="utf-8")
    excerpts = {"02_pdb_steps": "7,30", "03_pdb_cause": "7,19"}
    render(output, name, lines=excerpts.get(name))
    return {"name": name, "debugger": "pdb", "version": version, "commands": commands}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("before", "after"), required=True)
    args = parser.parse_args()
    LOGS.mkdir(parents=True, exist_ok=True)
    SCREENS.mkdir(parents=True, exist_ok=True)
    manifest = []
    if args.stage == "before":
        manifest.append(command("01_reproduce", ["demo.py", "--version", "legacy", "--check"], 1))
        manifest.append(pdb_session("02_pdb_steps", "legacy", [
            "b average_legacy.py:9", "c", "p values", "p list(range(len(values) - 1))",
            "display total", "n", "p index", "n", "p total", "q",
        ]))
        manifest.append(pdb_session("03_pdb_cause", "legacy", [
            "b average_legacy.py:11", "c", "p values", "p (index, total, len(values))",
            "p values[-1]", "p sum(values)", "p total / len(values)", "where", "q",
        ]))
        # Тот же тест на изолированном снимке до исправления.
        with tempfile.TemporaryDirectory(prefix="lab6-before-") as directory:
            snapshot = Path(directory)
            for source in ("average.py", "average_legacy.py", "demo.py", "pyproject.toml"):
                shutil.copy2(ROOT / source, snapshot / source)
            shutil.copytree(ROOT / "tests", snapshot / "tests", ignore=shutil.ignore_patterns("__pycache__"))
            path = snapshot / "average.py"
            text = path.read_text(encoding="utf-8").replace("range(len(values)):", "range(len(values) - 1):")
            path.write_text(text, encoding="utf-8")
            manifest.append(command("11_regression_before", ["-m", "pytest", "tests/test_average.py::test_regression_includes_last_element", "-q", "--tb=short"], 1, cwd=snapshot))
    else:
        manifest.append(pdb_session("07_pdb_fixed", "fixed", [
            "b average.py:11", "c", "p (index, total, len(values))",
            "p list(range(len(values)))", "p total / len(values)", "c", "q",
        ]))
        manifest.append(command("10_tests", ["-m", "pytest", "-vv", "--tb=short"], 0))
        manifest.append(command("12_regression_after", ["-m", "pytest", "tests/test_average.py::test_regression_includes_last_element", "-q", "--tb=short"], 0))
        manifest.append(command("13_fixed_cli", ["demo.py", "--version", "fixed", "--check"], 0))
        fixed = (ROOT / "average.py").read_text(encoding="utf-8")
        before = fixed.replace("range(len(values)):", "range(len(values) - 1):")
        diff = "".join(difflib.unified_diff(before.splitlines(True), fixed.splitlines(True), fromfile="average.py (before)", tofile="average.py (after)"))
        path = LOGS / "06_fix.diff"
        path.write_text(diff, encoding="utf-8")
        render(path, "06_fix", "diff")
    (ASSETS / f"manifest_{args.stage}.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Captured stage: {args.stage}")


if __name__ == "__main__":
    main()
