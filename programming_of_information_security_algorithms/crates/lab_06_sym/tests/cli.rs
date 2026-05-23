//! e2e CLI-тест лаб 6.

use std::fs;
use std::path::PathBuf;
use std::process::Command;

fn unique_tmp(name: &str) -> PathBuf {
    let pid = std::process::id();
    let nanos = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.subsec_nanos())
        .unwrap_or(0);
    std::env::temp_dir().join(format!("psia_lab06_cli_{name}_{pid}_{nanos}"))
}

fn cli() -> Command {
    let mut cmd = Command::new(env!("CARGO_BIN_EXE_lab_06_sym"));
    cmd.env("RUST_LOG", "off");
    cmd.env("NO_COLOR", "1");
    cmd
}

#[test]
fn gen_encrypt_decrypt_round_trip() {
    let key = unique_tmp("k");
    let plain = unique_tmp("p.txt");
    let ct = unique_tmp("c.bin");
    let plain_out = unique_tmp("p.dec");

    let payload = "Симметричное шифрование, ¡hola! 1234567890";
    fs::write(&plain, payload).unwrap();

    let out = cli()
        .args(["gen-key", "--out", key.to_str().unwrap()])
        .output()
        .unwrap();
    assert!(
        out.status.success(),
        "gen-key stderr = {}",
        String::from_utf8_lossy(&out.stderr)
    );
    assert!(key.exists());
    assert_eq!(fs::metadata(&key).unwrap().len(), 16 + 32 + 32);

    let out = cli()
        .args([
            "encrypt",
            "--key",
            key.to_str().unwrap(),
            "--in",
            plain.to_str().unwrap(),
            "--out",
            ct.to_str().unwrap(),
        ])
        .output()
        .unwrap();
    assert!(out.status.success());

    let out = cli()
        .args([
            "decrypt",
            "--key",
            key.to_str().unwrap(),
            "--in",
            ct.to_str().unwrap(),
            "--out",
            plain_out.to_str().unwrap(),
        ])
        .output()
        .unwrap();
    assert!(out.status.success());
    assert_eq!(fs::read_to_string(&plain_out).unwrap(), payload);

    for p in [key, plain, ct, plain_out] {
        let _ = fs::remove_file(p);
    }
}

#[test]
fn corrupted_ciphertext_returns_nonzero() {
    let key = unique_tmp("k2");
    let plain = unique_tmp("p2.txt");
    let ct = unique_tmp("c2.bin");
    let plain_out = unique_tmp("p2.dec");

    fs::write(&plain, b"data").unwrap();
    cli()
        .args(["gen-key", "--out", key.to_str().unwrap()])
        .output()
        .unwrap();
    cli()
        .args([
            "encrypt",
            "--key",
            key.to_str().unwrap(),
            "--in",
            plain.to_str().unwrap(),
            "--out",
            ct.to_str().unwrap(),
        ])
        .output()
        .unwrap();

    let mut bytes = fs::read(&ct).unwrap();
    let last = bytes.len() - 1;
    bytes[last] ^= 0xFF;
    fs::write(&ct, &bytes).unwrap();

    let out = cli()
        .args([
            "decrypt",
            "--key",
            key.to_str().unwrap(),
            "--in",
            ct.to_str().unwrap(),
            "--out",
            plain_out.to_str().unwrap(),
        ])
        .output()
        .unwrap();
    assert!(
        !out.status.success(),
        "decrypt должен упасть на MAC mismatch"
    );

    for p in [key, plain, ct, plain_out] {
        let _ = fs::remove_file(p);
    }
}

#[test]
fn help_lists_three_subcommands() {
    let out = cli().arg("--help").output().expect("--help");
    assert!(out.status.success());
    let s = String::from_utf8_lossy(&out.stdout);
    assert!(s.contains("gen-key"));
    assert!(s.contains("encrypt"));
    assert!(s.contains("decrypt"));
}
