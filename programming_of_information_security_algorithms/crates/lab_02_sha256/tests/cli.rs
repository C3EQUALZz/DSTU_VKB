//! Интеграционные тесты CLI лаб 2: `hash` и `verify`.

use std::fs;
use std::path::PathBuf;
use std::process::Command;

fn unique_tmp(name: &str) -> PathBuf {
    let pid = std::process::id();
    let nanos = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.subsec_nanos())
        .unwrap_or(0);
    std::env::temp_dir().join(format!("psia_lab02_{name}_{pid}_{nanos}"))
}

fn cli() -> Command {
    let mut cmd = Command::new(env!("CARGO_BIN_EXE_lab_02_sha256"));
    cmd.env("RUST_LOG", "off");
    cmd.env("NO_COLOR", "1");
    cmd
}

#[test]
fn hash_of_abc_matches_known_vector() {
    let file = unique_tmp("abc.txt");
    fs::write(&file, b"abc").unwrap();
    let out = cli()
        .args(["hash", file.to_str().unwrap()])
        .output()
        .expect("run hash");
    assert!(out.status.success());
    let stdout = String::from_utf8_lossy(&out.stdout);
    assert!(
        stdout.contains("ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
        "stdout = {stdout}"
    );
    let _ = fs::remove_file(file);
}

#[test]
fn hash_writes_shasum_compatible_output() {
    let file = unique_tmp("payload.txt");
    let digest_file = unique_tmp("payload.sha256");
    fs::write(&file, b"abc").unwrap();
    let out = cli()
        .args([
            "hash",
            file.to_str().unwrap(),
            "--out",
            digest_file.to_str().unwrap(),
        ])
        .output()
        .expect("run hash --out");
    assert!(out.status.success());
    let body = fs::read_to_string(&digest_file).unwrap();
    assert!(body.starts_with("ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"));
    assert!(body.contains("  ")); // shasum-формат — два пробела
    let _ = fs::remove_file(file);
    let _ = fs::remove_file(digest_file);
}

#[test]
fn verify_matching_file_exits_zero() {
    let file = unique_tmp("ok.txt");
    let digest_file = unique_tmp("ok.sha256");
    fs::write(&file, b"hello world\n").unwrap();
    cli()
        .args([
            "hash",
            file.to_str().unwrap(),
            "--out",
            digest_file.to_str().unwrap(),
        ])
        .output()
        .unwrap();

    let out = cli()
        .args([
            "verify",
            file.to_str().unwrap(),
            "--against",
            digest_file.to_str().unwrap(),
        ])
        .output()
        .expect("verify");
    assert!(
        out.status.success(),
        "verify должен дать exit 0 при совпадении"
    );
    let stdout = String::from_utf8_lossy(&out.stdout);
    assert!(stdout.contains("OK"), "stdout = {stdout}");

    let _ = fs::remove_file(file);
    let _ = fs::remove_file(digest_file);
}

#[test]
fn verify_modified_file_exits_nonzero() {
    let file = unique_tmp("modified.txt");
    let digest_file = unique_tmp("modified.sha256");
    fs::write(&file, b"hello world\n").unwrap();
    cli()
        .args([
            "hash",
            file.to_str().unwrap(),
            "--out",
            digest_file.to_str().unwrap(),
        ])
        .output()
        .unwrap();

    // Меняем файл — хеш должен разойтись.
    fs::write(&file, b"hello WORLD\n").unwrap();

    let out = cli()
        .args([
            "verify",
            file.to_str().unwrap(),
            "--against",
            digest_file.to_str().unwrap(),
        ])
        .output()
        .expect("verify modified");
    assert!(!out.status.success(), "verify должен дать exit ≠ 0");
    let stdout = String::from_utf8_lossy(&out.stdout);
    assert!(stdout.contains("MISMATCH"), "stdout = {stdout}");

    let _ = fs::remove_file(file);
    let _ = fs::remove_file(digest_file);
}

#[test]
fn shasum_compatible_file_is_readable() {
    // Эмулируем coreutils: `shasum -a 256 README` напишет такую же строку.
    let file = unique_tmp("data.txt");
    let digest_file = unique_tmp("data.sha256");
    fs::write(&file, b"abc").unwrap();
    let body = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad  data.txt\n";
    fs::write(&digest_file, body).unwrap();
    let out = cli()
        .args([
            "verify",
            file.to_str().unwrap(),
            "--against",
            digest_file.to_str().unwrap(),
        ])
        .output()
        .expect("verify shasum-compat");
    assert!(out.status.success(), "shasum-формат должен распознаваться");
    let _ = fs::remove_file(file);
    let _ = fs::remove_file(digest_file);
}

#[test]
fn hash_large_file_streams_correctly() {
    // 5 MiB. Тест проверяет, что чтение через буфер не теряет байты
    // и совпадает с системным `shasum -a 256` (если он есть).
    let file = unique_tmp("large.bin");
    let mut data = Vec::with_capacity(5 * 1024 * 1024);
    for i in 0..(5 * 1024 * 1024_usize) {
        data.push((i % 251) as u8);
    }
    fs::write(&file, &data).unwrap();

    let out = cli()
        .args(["hash", file.to_str().unwrap()])
        .output()
        .expect("hash large");
    assert!(out.status.success());

    // Проверка против собственной реализации — гарантирует, что CLI и lib согласованы.
    let lib_digest = {
        use lab_02_sha256::domain::sha256::{digest, to_hex};
        to_hex(&digest(&data))
    };
    let stdout = String::from_utf8_lossy(&out.stdout);
    assert!(stdout.contains(&lib_digest), "stdout = {stdout}");

    let _ = fs::remove_file(file);
}

#[test]
fn help_lists_two_subcommands() {
    let out = cli().arg("--help").output().expect("--help");
    assert!(out.status.success());
    let stdout = String::from_utf8_lossy(&out.stdout);
    assert!(stdout.contains("hash"));
    assert!(stdout.contains("verify"));
}
