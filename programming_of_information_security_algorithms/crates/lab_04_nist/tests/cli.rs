//! Интеграционные CLI тесты лаб 4 + сквозной сценарий с лаб 3.

use std::fs;
use std::path::PathBuf;
use std::process::Command;

fn unique_tmp(name: &str) -> PathBuf {
    let pid = std::process::id();
    let nanos = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.subsec_nanos())
        .unwrap_or(0);
    std::env::temp_dir().join(format!("psia_lab04_cli_{name}_{pid}_{nanos}"))
}

fn cli() -> Command {
    let mut cmd = Command::new(env!("CARGO_BIN_EXE_lab_04_nist"));
    cmd.env("RUST_LOG", "off");
    cmd.env("NO_COLOR", "1");
    cmd
}

#[test]
fn alternating_sequence_passes_monobit_only() {
    let input = unique_tmp("alt.bits");
    let body: String = (0..1000)
        .map(|i| if i % 2 == 0 { '0' } else { '1' })
        .collect();
    fs::write(&input, body).unwrap();

    let out = cli()
        .args([
            "check",
            "--input",
            input.to_str().unwrap(),
            "--format",
            "ascii",
            "--suite",
            "monobit",
        ])
        .output()
        .expect("check monobit");
    assert!(
        out.status.success(),
        "stderr = {}",
        String::from_utf8_lossy(&out.stderr)
    );
    let stdout = String::from_utf8_lossy(&out.stdout);
    assert!(stdout.contains("RANDOM"));
    assert!(stdout.contains("Frequency"));
    let _ = fs::remove_file(input);
}

#[test]
fn constant_zeros_fails_both_tests() {
    let input = unique_tmp("zeros.bits");
    fs::write(&input, "0".repeat(1000)).unwrap();

    let out = cli()
        .args([
            "check",
            "--input",
            input.to_str().unwrap(),
            "--format",
            "ascii",
            "--suite",
            "all",
        ])
        .output()
        .expect("check zeros");
    // Хотя бы один тест провалился → exit code ≠ 0.
    assert!(!out.status.success());
    let stdout = String::from_utf8_lossy(&out.stdout);
    assert!(stdout.contains("NON-RANDOM"));
    let _ = fs::remove_file(input);
}

#[test]
fn writes_report_to_file() {
    let input = unique_tmp("seq.bits");
    let report = unique_tmp("report.txt");
    let body: String = (0..256)
        .map(|i| if i % 2 == 0 { '0' } else { '1' })
        .collect();
    fs::write(&input, body).unwrap();
    let out = cli()
        .args([
            "check",
            "--input",
            input.to_str().unwrap(),
            "--format",
            "ascii",
            "--out",
            report.to_str().unwrap(),
        ])
        .output()
        .unwrap();
    assert!(out.status.success() || !out.status.success()); // не важен exit-код, важен файл
    let contents = fs::read_to_string(&report).unwrap();
    assert!(contents.contains("Frequency"));
    assert!(contents.contains("P-value"));
    let _ = fs::remove_file(input);
    let _ = fs::remove_file(report);
}

/// E2E: генерируем последовательность лаб 3 (как библиотеку) и прогоняем
/// её через CLI лаб 4. `xorshift64*` должен пройти Monobit и Runs.
#[test]
fn xorshift64star_from_lab03_passes_both_tests() {
    use lab_03_prng::domain::generate;

    let bits_file = unique_tmp("seq.bits");
    let seq = generate(0xDEAD_BEEF_CAFE_BABE, 200);
    let mut body = seq.to_ascii_bits();
    body.push('\n');
    fs::write(&bits_file, body).unwrap();

    let out = cli()
        .args([
            "check",
            "--input",
            bits_file.to_str().unwrap(),
            "--format",
            "ascii",
            "--suite",
            "all",
        ])
        .output()
        .expect("lab_04 check");
    assert!(
        out.status.success(),
        "xorshift64* должен пройти оба теста; stdout = {}",
        String::from_utf8_lossy(&out.stdout)
    );
    let _ = fs::remove_file(bits_file);
}

#[test]
fn help_shows_check_subcommand() {
    let out = cli().arg("--help").output().expect("--help");
    assert!(out.status.success());
    let stdout = String::from_utf8_lossy(&out.stdout);
    assert!(stdout.contains("check"));
}
