"""Рендерит ключевые фрагменты исходников Rust во freeze-PNG.

Запуск: `python3 scripts/render_snippets.py [lab_XX | all]`.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from snippet_tools import render_code_chunked  # noqa: E402

SNIPS_BASE = ROOT / "docs" / "snippets"


def ensure_clean(p: Path) -> None:
    if p.exists():
        shutil.rmtree(p)
    p.mkdir(parents=True, exist_ok=True)


def read_slice(rel_path: str, start: int, end: int) -> str:
    p = ROOT / rel_path
    text = p.read_text(encoding="utf-8")
    lines = text.splitlines()
    chunk = lines[start - 1 : end]
    return "\n".join(chunk) + "\n"


# Описание фрагментов: (имя_файла, rel_path, start, end, max_lines_chunk)
SNIPPETS: dict[str, list[tuple[str, str, int, int, int]]] = {
    "practice_01": [
        ("01_bigint_type", "crates/practice_01/src/domain/bigint.rs", 13, 49, 38),
        ("02_add_signed", "crates/practice_01/src/domain/bigint.rs", 213, 252, 40),
        ("03_add_abs_carry", "crates/practice_01/src/domain/bigint.rs", 360, 400, 40),
        ("04_verify_usecase", "crates/practice_01/src/application/verify.rs", 1, 50, 40),
    ],
    "lab_01": [
        ("01_keys_struct", "crates/lab_01_rsa/src/domain/rsa.rs", 1, 80, 40),
        ("02_miller_rabin", "crates/lab_01_rsa/src/domain/primes.rs", 1, 70, 40),
        ("03_generate_prime", "crates/lab_01_rsa/src/domain/primes.rs", 85, 135, 40),
        ("04_encrypt_decrypt", "crates/lab_01_rsa/src/domain/rsa.rs", 155, 220, 40),
        ("05_cli", "crates/lab_01_rsa/src/presentation/cli.rs", 1, 70, 40),
    ],
    "lab_02": [
        ("01_constants", "crates/lab_02_sha256/src/domain/sha256.rs", 1, 60, 40),
        ("02_helpers", "crates/lab_02_sha256/src/domain/sha256.rs", 95, 145, 40),
        ("03_compress", "crates/lab_02_sha256/src/domain/sha256.rs", 150, 230, 40),
        ("04_digest_top", "crates/lab_02_sha256/src/domain/sha256.rs", 275, 320, 40),
        ("05_hash_io", "crates/lab_02_sha256/src/infrastructure/hash_io.rs", 1, 60, 40),
    ],
    "lab_03": [
        ("01_xorshift", "crates/lab_03_prng/src/domain/prng.rs", 1, 65, 40),
        ("02_sequence", "crates/lab_03_prng/src/domain/prng.rs", 65, 130, 40),
        ("03_generate", "crates/lab_03_prng/src/domain/prng.rs", 105, 160, 40),
        ("04_file_sink", "crates/lab_03_prng/src/infrastructure/file_sink.rs", 1, 50, 40),
        ("05_cli", "crates/lab_03_prng/src/presentation/cli.rs", 1, 60, 40),
    ],
    "lab_04": [
        ("01_monobit", "crates/lab_04_nist/src/domain/stat_tests.rs", 60, 125, 40),
        ("02_runs", "crates/lab_04_nist/src/domain/stat_tests.rs", 120, 180, 40),
        ("03_erfc", "crates/lab_04_nist/src/domain/erfc.rs", 1, 70, 40),
        ("04_loader", "crates/lab_04_nist/src/infrastructure/loader.rs", 1, 55, 40),
        ("05_report", "crates/lab_04_nist/src/infrastructure/report.rs", 1, 55, 40),
    ],
    "lab_06": [
        ("01_provider_trait", "crates/lab_06_sym/src/infrastructure/providers/mod.rs", 1, 65, 40),
        ("02_key", "crates/lab_06_sym/src/domain/key.rs", 1, 75, 40),
        ("03_cipher", "crates/lab_06_sym/src/domain/cipher.rs", 80, 145, 40),
        ("04_macos_backend", "crates/lab_06_sym/src/infrastructure/providers/macos.rs", 60, 140, 40),
        ("05_usecases", "crates/lab_06_sym/src/application/usecases.rs", 1, 65, 40),
    ],
    "lab_07": [
        ("01_provider_trait", "crates/lab_07_asym/src/infrastructure/providers/mod.rs", 1, 55, 40),
        ("02_keys", "crates/lab_07_asym/src/domain/keys.rs", 1, 65, 40),
        ("03_cipher_types", "crates/lab_07_asym/src/domain/cipher.rs", 1, 60, 40),
        ("04_openssl_backend", "crates/lab_07_asym/src/infrastructure/providers/openssl_provider.rs", 16, 90, 40),
        ("05_usecases", "crates/lab_07_asym/src/application/usecases.rs", 1, 65, 40),
    ],
}


def render_for(work: str) -> None:
    if work not in SNIPPETS:
        print(f"unknown: {work}")
        return
    out_dir = SNIPS_BASE / work
    ensure_clean(out_dir)
    for name, rel, start, end, max_lines in SNIPPETS[work]:
        path = ROOT / rel
        if not path.exists():
            print(f"  ! {rel} doesn't exist, skipping {name}")
            continue
        try:
            src = read_slice(rel, start, end)
        except Exception as e:
            print(f"  ! {rel}:{start}-{end}: {e}")
            continue
        n = len(src.splitlines())
        print(f"  > {name}: {rel}:{start}-{end} ({n} lines)")
        render_code_chunked(src, out_dir, name, language="rust", max_lines=max_lines)


def main() -> None:
    args = sys.argv[1:] if len(sys.argv) > 1 else ["all"]
    works: list[str] = []
    for a in args:
        if a == "all":
            works = list(SNIPPETS.keys())
            break
        works.append(a)
    for w in works:
        print(f"=== {w} ===")
        render_for(w)


if __name__ == "__main__":
    main()
