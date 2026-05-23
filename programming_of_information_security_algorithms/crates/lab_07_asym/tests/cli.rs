//! e2e CLI лаб 7.

use std::fs;
use std::path::PathBuf;
use std::process::Command;

fn unique_tmp(name: &str) -> PathBuf {
    let pid = std::process::id();
    let nanos = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.subsec_nanos())
        .unwrap_or(0);
    std::env::temp_dir().join(format!("psia_lab07_cli_{name}_{pid}_{nanos}"))
}

fn cli() -> Command {
    let mut cmd = Command::new(env!("CARGO_BIN_EXE_lab_07_asym"));
    cmd.env("RUST_LOG", "off");
    cmd.env("NO_COLOR", "1");
    cmd
}

#[test]
fn gen_keys_encrypt_decrypt_round_trip() {
    let pubk = unique_tmp("pub");
    let privk = unique_tmp("priv");
    let plain = unique_tmp("p.txt");
    let ct = unique_tmp("c.bin");
    let recovered = unique_tmp("p.dec");

    let payload = "RSA-OAEP-SHA256: Привет, асимметрия!";
    fs::write(&plain, payload).unwrap();

    let out = cli()
        .args([
            "gen-keys",
            "--bits",
            "2048",
            "--public",
            pubk.to_str().unwrap(),
            "--private",
            privk.to_str().unwrap(),
        ])
        .output()
        .unwrap();
    assert!(
        out.status.success(),
        "gen-keys stderr = {}",
        String::from_utf8_lossy(&out.stderr)
    );
    assert!(pubk.exists() && privk.exists());

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
        .unwrap();
    assert!(out.status.success());

    let out = cli()
        .args([
            "decrypt",
            "--private",
            privk.to_str().unwrap(),
            "--in",
            ct.to_str().unwrap(),
            "--out",
            recovered.to_str().unwrap(),
        ])
        .output()
        .unwrap();
    assert!(out.status.success());
    assert_eq!(fs::read_to_string(&recovered).unwrap(), payload);

    for f in [pubk, privk, plain, ct, recovered] {
        let _ = fs::remove_file(f);
    }
}

#[test]
fn cross_key_decrypt_returns_nonzero() {
    let pubk1 = unique_tmp("pub1");
    let privk1 = unique_tmp("priv1");
    let pubk2 = unique_tmp("pub2");
    let privk2 = unique_tmp("priv2");
    let plain = unique_tmp("p.txt");
    let ct = unique_tmp("c.bin");
    let recovered = unique_tmp("p.dec");

    fs::write(&plain, b"secret").unwrap();
    for (pubk, privk) in [(&pubk1, &privk1), (&pubk2, &privk2)] {
        let out = cli()
            .args([
                "gen-keys",
                "--bits",
                "2048",
                "--public",
                pubk.to_str().unwrap(),
                "--private",
                privk.to_str().unwrap(),
            ])
            .output()
            .unwrap();
        assert!(out.status.success());
    }

    cli()
        .args([
            "encrypt",
            "--public",
            pubk1.to_str().unwrap(),
            "--in",
            plain.to_str().unwrap(),
            "--out",
            ct.to_str().unwrap(),
        ])
        .output()
        .unwrap();

    let out = cli()
        .args([
            "decrypt",
            "--private",
            privk2.to_str().unwrap(),
            "--in",
            ct.to_str().unwrap(),
            "--out",
            recovered.to_str().unwrap(),
        ])
        .output()
        .unwrap();
    assert!(!out.status.success(), "decrypt чужим ключом должен упасть");

    for f in [pubk1, privk1, pubk2, privk2, plain, ct, recovered] {
        let _ = fs::remove_file(f);
    }
}

#[test]
fn help_lists_three_subcommands() {
    let out = cli().arg("--help").output().expect("--help");
    assert!(out.status.success());
    let s = String::from_utf8_lossy(&out.stdout);
    assert!(s.contains("gen-keys"));
    assert!(s.contains("encrypt"));
    assert!(s.contains("decrypt"));
}
