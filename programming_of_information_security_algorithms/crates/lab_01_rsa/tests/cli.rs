//! Полный e2e цикл через CLI: gen → encrypt → decrypt.

use std::fs;
use std::path::PathBuf;
use std::process::Command;

fn unique_tmp(name: &str) -> PathBuf {
    let pid = std::process::id();
    let nanos = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.subsec_nanos())
        .unwrap_or(0);
    std::env::temp_dir().join(format!("psia_lab01_cli_{name}_{pid}_{nanos}"))
}

fn cli() -> Command {
    let mut cmd = Command::new(env!("CARGO_BIN_EXE_lab_01_rsa"));
    cmd.env("RUST_LOG", "off");
    cmd.env("NO_COLOR", "1");
    cmd
}

#[test]
fn gen_encrypt_decrypt_round_trip() {
    let pubk = unique_tmp("pub");
    let privk = unique_tmp("priv");
    let plain = unique_tmp("plain.txt");
    let ct = unique_tmp("ct.bin");
    let plain_out = unique_tmp("plain_out.txt");

    let message = "Привет из CLI-теста лаб 1!\nMulti-line message: 1234567890.";
    fs::write(&plain, message).unwrap();

    // gen
    let out = cli()
        .args([
            "gen",
            "--bits",
            "256", // быстро для CI
            "--public",
            pubk.to_str().unwrap(),
            "--private",
            privk.to_str().unwrap(),
        ])
        .output()
        .expect("gen subcommand");
    assert!(
        out.status.success(),
        "gen failed: stderr = {}",
        String::from_utf8_lossy(&out.stderr)
    );
    assert!(pubk.exists() && privk.exists(), "ключи должны быть созданы");

    // encrypt
    let out = cli()
        .args([
            "encrypt",
            "--public",
            pubk.to_str().unwrap(),
            "--in",
            plain.to_str().unwrap(),
            "--out",
            ct.to_str().unwrap(),
        ])
        .output()
        .expect("encrypt subcommand");
    assert!(out.status.success(), "encrypt failed");
    let ct_bytes = fs::read(&ct).unwrap();
    assert!(!ct_bytes.is_empty());
    assert_ne!(
        ct_bytes,
        message.as_bytes(),
        "шифртекст не должен совпадать с открытым текстом"
    );

    // decrypt — печатает в stdout и сохраняет копию
    let out = cli()
        .args([
            "decrypt",
            "--private",
            privk.to_str().unwrap(),
            "--in",
            ct.to_str().unwrap(),
            "--out",
            plain_out.to_str().unwrap(),
        ])
        .output()
        .expect("decrypt subcommand");
    assert!(
        out.status.success(),
        "decrypt failed: stderr = {}",
        String::from_utf8_lossy(&out.stderr)
    );

    let stdout = String::from_utf8_lossy(&out.stdout);
    assert!(
        stdout.contains(message),
        "stdout должен содержать исходное сообщение; stdout = {stdout:?}"
    );

    let recovered = fs::read_to_string(&plain_out).unwrap();
    assert_eq!(
        recovered, message,
        "файловая копия plaintext'а должна совпадать"
    );

    for p in [pubk, privk, plain, ct, plain_out] {
        let _ = fs::remove_file(p);
    }
}

#[test]
fn key_files_are_human_readable() {
    let pubk = unique_tmp("pub_readable");
    let privk = unique_tmp("priv_readable");
    let out = cli()
        .args([
            "gen",
            "--bits",
            "256",
            "--public",
            pubk.to_str().unwrap(),
            "--private",
            privk.to_str().unwrap(),
        ])
        .output()
        .expect("gen");
    assert!(out.status.success());

    let pub_text = fs::read_to_string(&pubk).unwrap();
    assert!(pub_text.contains("bits = 256"));
    assert!(pub_text.contains("n = 0x"));
    assert!(pub_text.contains("e = 0x"));
    assert!(
        !pub_text.contains(" d = "),
        "в открытом ключе не должно быть d"
    );

    let priv_text = fs::read_to_string(&privk).unwrap();
    assert!(priv_text.contains("d = 0x"));
    assert!(priv_text.contains("p = 0x"));
    assert!(priv_text.contains("q = 0x"));

    let _ = fs::remove_file(pubk);
    let _ = fs::remove_file(privk);
}

#[test]
fn decrypt_with_wrong_key_does_not_equal_plaintext() {
    let pub1 = unique_tmp("pub1");
    let priv1 = unique_tmp("priv1");
    let pub2 = unique_tmp("pub2");
    let priv2 = unique_tmp("priv2");
    let plain = unique_tmp("p.txt");
    let ct = unique_tmp("c.bin");

    fs::write(&plain, "secret message").unwrap();

    for (pubp, privp) in [(&pub1, &priv1), (&pub2, &priv2)] {
        cli()
            .args([
                "gen",
                "--bits",
                "256",
                "--public",
                pubp.to_str().unwrap(),
                "--private",
                privp.to_str().unwrap(),
            ])
            .output()
            .unwrap();
    }

    cli()
        .args([
            "encrypt",
            "--public",
            pub1.to_str().unwrap(),
            "--in",
            plain.to_str().unwrap(),
            "--out",
            ct.to_str().unwrap(),
        ])
        .output()
        .unwrap();

    // Расшифровка чужим приватным ключом.
    let out = cli()
        .args([
            "decrypt",
            "--private",
            priv2.to_str().unwrap(),
            "--in",
            ct.to_str().unwrap(),
        ])
        .output()
        .unwrap();
    // Учебный RSA без padding'а не паникует, но восстановит мусор.
    let stdout = out.stdout;
    assert_ne!(stdout, b"secret message\n");

    for p in [pub1, priv1, pub2, priv2, plain, ct] {
        let _ = fs::remove_file(p);
    }
}

#[test]
fn help_lists_three_subcommands() {
    let out = cli().arg("--help").output().expect("--help");
    assert!(out.status.success());
    let stdout = String::from_utf8_lossy(&out.stdout);
    assert!(stdout.contains("gen"));
    assert!(stdout.contains("encrypt"));
    assert!(stdout.contains("decrypt"));
}
