"""Прогоняет CLI каждой работы и сохраняет freeze-PNG логов в docs/screenshots/.

Запуск: `python3 scripts/capture_screens.py [lab_XX | all]`.
По умолчанию запускает все лабы.

Команды запускаются из корня репозитория с относительными путями — чтобы абсолютные
пути не съедали полезную ширину в логах.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from snippet_tools import (  # noqa: E402
    capture_command,
    render_term_chunked,
)

SHOTS_BASE = ROOT / "docs" / "screenshots"
ARTIFACTS = ROOT / "artifacts"
TARGET = ROOT / "target" / "release"


def bin_rel(name: str) -> str:
    return f"./target/release/{name}"


def ensure_clean(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def run_and_save(
    label: str,
    cmd: list[str],
    out: Path,
    *,
    env_extra: dict[str, str] | None = None,
    max_lines: int = 26,
    wrap: int | None = 100,
) -> list[Path]:
    print(f"  > {label}: {' '.join(cmd)}")
    text, rc = capture_command(
        cmd,
        cwd=ROOT,
        env_extra=env_extra or {"RUST_LOG": "info"},
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.with_suffix(".log").write_text(text, encoding="utf-8")
    print(f"    rc={rc}, lines={len(text.splitlines())}")
    return render_term_chunked(text, out.parent, out.stem, max_lines=max_lines, wrap=wrap)


def capture_practice_01() -> None:
    out_dir = SHOTS_BASE / "practice_01"
    ensure_clean(out_dir)
    run_and_save(
        "small add",
        [bin_rel("practice_01"), "add", "12345", "67890"],
        out_dir / "01_add_small.png",
    )
    run_and_save(
        "small sub negative",
        [bin_rel("practice_01"), "sub", "100", "12345"],
        out_dir / "02_sub_negative.png",
    )
    run_and_save(
        "big add 64 digits",
        [
            bin_rel("practice_01"),
            "add",
            "1234567890123456789012345678901234567890123456789012345678901234",
            "9876543210987654321098765432109876543210987654321098765432109876",
        ],
        out_dir / "03_add_big.png",
        max_lines=30,
        wrap=90,
    )
    run_and_save(
        "big sub borrow",
        [
            bin_rel("practice_01"),
            "sub",
            "10000000000000000000000000000000000000000000000000000000000000000",
            "99999999999999999999999999999999999999999999999999999999999",
        ],
        out_dir / "04_sub_big.png",
        max_lines=30,
        wrap=90,
    )
    run_and_save(
        "demo (random table)",
        [bin_rel("practice_01"), "demo"],
        out_dir / "05_demo.png",
        max_lines=30,
        wrap=90,
    )


def capture_lab_01() -> None:
    out_dir = SHOTS_BASE / "lab_01"
    ensure_clean(out_dir)
    art = "artifacts/lab_01"
    (ARTIFACTS / "lab_01").mkdir(parents=True, exist_ok=True)
    run_and_save(
        "gen 1024-bit keys",
        [
            bin_rel("lab_01_rsa"),
            "gen",
            "--bits", "1024",
            "--public", f"{art}/pub.key",
            "--private", f"{art}/priv.key",
        ],
        out_dir / "01_gen_keys.png",
        max_lines=24,
    )
    sample = "docs/explanations/lab_01_rsa/sample.txt"
    run_and_save(
        "encrypt",
        [
            bin_rel("lab_01_rsa"),
            "encrypt",
            "--public", f"{art}/pub.key",
            "--in", sample,
            "--out", f"{art}/sample.enc",
        ],
        out_dir / "02_encrypt.png",
    )
    run_and_save(
        "decrypt",
        [
            bin_rel("lab_01_rsa"),
            "decrypt",
            "--private", f"{art}/priv.key",
            "--in", f"{art}/sample.enc",
            "--out", f"{art}/sample.dec",
        ],
        out_dir / "03_decrypt.png",
    )
    run_and_save(
        "inspect key file",
        ["bash", "-lc", f"head -20 {art}/pub.key"],
        out_dir / "04_pub_key.png",
        env_extra={},
    )


def capture_lab_02() -> None:
    out_dir = SHOTS_BASE / "lab_02"
    ensure_clean(out_dir)
    art = "artifacts/lab_02"
    (ARTIFACTS / "lab_02").mkdir(parents=True, exist_ok=True)
    run_and_save(
        "hash README",
        [bin_rel("lab_02_sha256"), "hash", "README.md", "--out", f"{art}/readme.sha256"],
        out_dir / "01_hash.png",
    )
    run_and_save(
        "verify (match)",
        [bin_rel("lab_02_sha256"), "verify", "README.md", "--against", f"{art}/readme.sha256"],
        out_dir / "02_verify_ok.png",
    )
    run_and_save(
        "system shasum compare",
        ["bash", "-lc", f"shasum -a 256 README.md && echo '--- our .sha256 file:' && cat {art}/readme.sha256"],
        out_dir / "03_shasum_compare.png",
        env_extra={},
    )


def capture_lab_03() -> None:
    out_dir = SHOTS_BASE / "lab_03"
    ensure_clean(out_dir)
    art = "artifacts/lab_03"
    (ARTIFACTS / "lab_03").mkdir(parents=True, exist_ok=True)
    run_and_save(
        "gen 200 values",
        [
            bin_rel("lab_03_prng"),
            "gen",
            "--count", "200",
            "--seed", "0xDEADBEEFCAFEBABE",
            "--out-bin", f"{art}/sequence.bin",
            "--out-ascii", f"{art}/sequence.bits",
        ],
        out_dir / "01_gen.png",
        max_lines=22,
    )
    run_and_save(
        "file inspect",
        [
            "bash", "-lc",
            f"ls -la {art}/sequence.* && echo '--- first 64 ASCII bits:' && head -c 64 {art}/sequence.bits && echo && echo '--- first 16 bytes bin (hex):' && xxd -l 16 {art}/sequence.bin",
        ],
        out_dir / "02_inspect.png",
        env_extra={},
    )


def capture_lab_04() -> None:
    out_dir = SHOTS_BASE / "lab_04"
    ensure_clean(out_dir)
    art = "artifacts/lab_04"
    (ARTIFACTS / "lab_04").mkdir(parents=True, exist_ok=True)
    run_and_save(
        "monobit check",
        [
            bin_rel("lab_04_nist"),
            "check",
            "--input", "artifacts/lab_03/sequence.bits",
            "--out", f"{art}/report.txt",
        ],
        out_dir / "01_check.png",
        max_lines=26,
    )
    run_and_save(
        "report content",
        ["bash", "-lc", f"cat {art}/report.txt"],
        out_dir / "02_report.png",
        env_extra={},
    )


def capture_lab_06() -> None:
    out_dir = SHOTS_BASE / "lab_06"
    ensure_clean(out_dir)
    art = "artifacts/lab_06"
    (ARTIFACTS / "lab_06").mkdir(parents=True, exist_ok=True)
    sample = "docs/explanations/lab_06_sym/sample.txt"
    run_and_save(
        "gen-key",
        [bin_rel("lab_06_sym"), "gen-key", "--out", f"{art}/symm.key"],
        out_dir / "01_genkey.png",
    )
    run_and_save(
        "encrypt",
        [
            bin_rel("lab_06_sym"),
            "encrypt",
            "--key", f"{art}/symm.key",
            "--in", sample,
            "--out", f"{art}/sample.enc",
        ],
        out_dir / "02_encrypt.png",
    )
    run_and_save(
        "decrypt",
        [
            bin_rel("lab_06_sym"),
            "decrypt",
            "--key", f"{art}/symm.key",
            "--in", f"{art}/sample.enc",
            "--out", f"{art}/sample.dec",
        ],
        out_dir / "03_decrypt.png",
    )
    run_and_save(
        "diff + hexdump",
        [
            "bash", "-lc",
            f"diff -q {sample} {art}/sample.dec && echo '✓ identical' ; echo '--- enc hex (first 8 lines):' ; xxd {art}/sample.enc | head -8",
        ],
        out_dir / "04_diff.png",
        env_extra={},
    )


def capture_lab_07() -> None:
    out_dir = SHOTS_BASE / "lab_07"
    ensure_clean(out_dir)
    art = "artifacts/lab_07"
    (ARTIFACTS / "lab_07").mkdir(parents=True, exist_ok=True)
    sample = "docs/explanations/lab_07_asym/sample.txt"
    run_and_save(
        "gen-keys 2048",
        [
            bin_rel("lab_07_asym"),
            "gen-keys",
            "--bits", "2048",
            "--public", f"{art}/pub.der",
            "--private", f"{art}/priv.der",
        ],
        out_dir / "01_genkeys.png",
    )
    run_and_save(
        "encrypt",
        [
            bin_rel("lab_07_asym"),
            "encrypt",
            "--public", f"{art}/pub.der",
            "--in", sample,
            "--out", f"{art}/sample.enc",
        ],
        out_dir / "02_encrypt.png",
    )
    run_and_save(
        "decrypt",
        [
            bin_rel("lab_07_asym"),
            "decrypt",
            "--private", f"{art}/priv.der",
            "--in", f"{art}/sample.enc",
            "--out", f"{art}/sample.dec",
        ],
        out_dir / "03_decrypt.png",
    )
    run_and_save(
        "diff + hexdump",
        [
            "bash", "-lc",
            f"diff -q {sample} {art}/sample.dec && echo '✓ identical' ; echo '--- enc hex (first 8 lines):' ; xxd {art}/sample.enc | head -8",
        ],
        out_dir / "04_diff.png",
        env_extra={},
    )


CAPTURES = {
    "practice_01": capture_practice_01,
    "lab_01": capture_lab_01,
    "lab_02": capture_lab_02,
    "lab_03": capture_lab_03,
    "lab_04": capture_lab_04,
    "lab_06": capture_lab_06,
    "lab_07": capture_lab_07,
}


def main() -> None:
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    targets = list(CAPTURES.keys()) if target == "all" else [target]
    for t in targets:
        if t not in CAPTURES:
            print(f"unknown: {t}")
            continue
        print(f"=== {t} ===")
        CAPTURES[t]()


if __name__ == "__main__":
    main()
