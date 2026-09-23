"""Запускает два реальных процесса и сохраняет их вывод для отчётов."""

from __future__ import annotations

import os
import shlex
import socket
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BIN = ROOT / "target" / "release" / "diffie_hellman"
ARTIFACTS = ROOT / "artifacts" / "diffie_hellman"


def main() -> None:
    if not BIN.exists():
        raise SystemExit("Сначала выполните: cargo build --release -p diffie_hellman")

    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]

    address = f"127.0.0.1:{port}"
    server_cmd = [str(BIN), "serve", "--bind", address, "--bits", "128", "--rounds", "32", "--once"]
    client_cmd = [
        str(BIN), "connect", "--addr", address, "--rounds", "32",
        "--message", "Привет, Боб!", "--message", "Канал работает",
    ]
    env = os.environ.copy()
    env["RUST_LOG"] = (
        "diffie_hellman::application=info,"
        "diffie_hellman::presentation=info,"
        "diffie_hellman::domain=warn"
    )

    server = subprocess.Popen(
        server_cmd, cwd=ROOT, env=env, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True,
    )
    try:
        time.sleep(0.3)
        client = subprocess.run(
            client_cmd, cwd=ROOT, env=env, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, timeout=120, check=False,
        )
        server_output, _ = server.communicate(timeout=120)
    except BaseException:
        server.kill()
        server.communicate()
        raise

    if client.returncode != 0 or server.returncode != 0:
        raise RuntimeError(
            f"Клиент ({client.returncode}):\n{client.stdout}\n"
            f"Сервер ({server.returncode}):\n{server_output}"
        )

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    for name, command, output in [
        ("07_server.txt", server_cmd, server_output),
        ("08_client.txt", client_cmd, client.stdout),
    ]:
        display = shlex.join(["target/release/diffie_hellman", *command[1:]])
        (ARTIFACTS / name).write_text(f"$ {display}\n{output}", encoding="utf-8")
        print(ARTIFACTS / name)

    examples = [
        ("01_gen_prime_128.txt", ["--seed", "42", "gen-prime", "--bits", "128", "--rounds", "32"]),
        ("02_gen_prime_256.txt", ["--seed", "42", "gen-prime", "--bits", "256", "--rounds", "32"]),
        ("03_range_primes.txt", ["range-primes", "--from", "1000", "--to", "1100"]),
        ("04_roots_1009.txt", ["roots", "--n", "1009", "--count", "100"]),
        ("05_dh_methodichka.txt", ["--seed", "42", "dh", "--n", "97", "--g", "5", "--xa", "36", "--xb", "58"]),
        ("06_dh_generated_128.txt", ["--seed", "7", "dh", "--bits", "128", "--rounds", "32"]),
    ]
    for name, args in examples:
        command = [str(BIN), *args]
        result = subprocess.run(
            command, cwd=ROOT, env={**env, "RUST_LOG": "warn"},
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, timeout=120, check=True,
        )
        (ARTIFACTS / name).write_text(result.stdout, encoding="utf-8")
        print(ARTIFACTS / name)


if __name__ == "__main__":
    main()
