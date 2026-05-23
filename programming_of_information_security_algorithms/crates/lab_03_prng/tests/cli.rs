//! Интеграционные тесты CLI лаб 3.

use std::fs;
use std::path::PathBuf;
use std::process::Command;

fn unique_tmp(name: &str) -> PathBuf {
    let pid = std::process::id();
    let nanos = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.subsec_nanos())
        .unwrap_or(0);
    std::env::temp_dir().join(format!("psia_lab03_cli_{name}_{pid}_{nanos}"))
}

fn cli() -> Command {
    let mut cmd = Command::new(env!("CARGO_BIN_EXE_lab_03_prng"));
    cmd.env("RUST_LOG", "off");
    cmd.env("NO_COLOR", "1");
    cmd
}

#[test]
fn gen_produces_binary_and_ascii_with_expected_sizes() {
    let bin = unique_tmp("a.bin");
    let asc = unique_tmp("a.bits");
    let out = cli()
        .args([
            "gen",
            "--count",
            "200",
            "--seed",
            "0xDEADBEEFCAFEBABE",
            "--out-bin",
            bin.to_str().unwrap(),
            "--out-ascii",
            asc.to_str().unwrap(),
        ])
        .output()
        .expect("gen");
    assert!(
        out.status.success(),
        "stderr = {}",
        String::from_utf8_lossy(&out.stderr)
    );
    assert_eq!(fs::metadata(&bin).unwrap().len(), 200 * 8);
    assert_eq!(fs::metadata(&asc).unwrap().len(), 200 * 64 + 1);
    let ascii = fs::read_to_string(&asc).unwrap();
    let line = ascii.trim_end_matches('\n');
    assert_eq!(line.len(), 200 * 64);
    assert!(line.chars().all(|c| c == '0' || c == '1'));
    let _ = fs::remove_file(bin);
    let _ = fs::remove_file(asc);
}

#[test]
fn same_seed_yields_byte_identical_files() {
    let a = unique_tmp("seq_a.bin");
    let b = unique_tmp("seq_b.bin");
    for path in [&a, &b] {
        let out = cli()
            .args([
                "gen",
                "--count",
                "200",
                "--seed",
                "0x1234567890ABCDEF",
                "--out-bin",
                path.to_str().unwrap(),
            ])
            .output()
            .unwrap();
        assert!(out.status.success());
    }
    assert_eq!(fs::read(&a).unwrap(), fs::read(&b).unwrap());
    let _ = fs::remove_file(a);
    let _ = fs::remove_file(b);
}

#[test]
fn count_below_200_fails_with_panic_message() {
    let out = cli()
        .args(["gen", "--count", "100", "--seed", "1"])
        .output()
        .expect("gen too small");
    // assert! в use case паникует — процесс падает с ненулевым кодом.
    assert!(!out.status.success());
    let combined =
        String::from_utf8_lossy(&out.stderr).into_owned() + &String::from_utf8_lossy(&out.stdout);
    assert!(
        combined.contains("по условию") || combined.to_lowercase().contains("panic"),
        "stderr+stdout = {combined}"
    );
}

#[test]
fn invalid_seed_returns_nonzero() {
    let out = cli()
        .args(["gen", "--count", "200", "--seed", "0xZZZZ"])
        .output()
        .expect("gen bad seed");
    assert!(!out.status.success());
}

#[test]
fn dec_seed_is_accepted() {
    let bin = unique_tmp("dec.bin");
    let out = cli()
        .args([
            "gen",
            "--count",
            "200",
            "--seed",
            "1234567890",
            "--out-bin",
            bin.to_str().unwrap(),
        ])
        .output()
        .unwrap();
    assert!(out.status.success());
    assert_eq!(fs::metadata(&bin).unwrap().len(), 200 * 8);
    let _ = fs::remove_file(bin);
}

#[test]
fn help_shows_gen_subcommand() {
    let out = cli().arg("--help").output().expect("--help");
    assert!(out.status.success());
    let stdout = String::from_utf8_lossy(&out.stdout);
    assert!(stdout.contains("gen"));
}
