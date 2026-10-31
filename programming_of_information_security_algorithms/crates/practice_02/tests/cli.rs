use std::process::{Command, Output};

fn run(args: &[&str]) -> Output {
    Command::new(env!("CARGO_BIN_EXE_practice_02"))
        .args(args)
        .env("RUST_LOG", "off")
        .env("NO_COLOR", "1")
        .output()
        .unwrap()
}

fn success(args: &[&str], expected: &str) {
    let output = run(args);
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(
        output.status.success(),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );
    assert!(stdout.contains(expected), "{args:?}: {stdout}");
}

#[test]
fn arithmetic_commands() {
    for (args, expected) in [
        (vec!["add", "5,1", "6,3"], "(10, 6)"),
        (vec!["sub", "5,1", "6,3"], "(5, 16)"),
        (vec!["double", "5,1"], "(6, 3)"),
        (vec!["neg", "5,1"], "(5, 16)"),
        (vec!["mul", "7", "5,1"], "(0, 6)"),
        (vec!["mul", "--", "-3", "5,1"], "(10, 11)"),
        (vec!["linear", "2", "5,1", "3", "6,3"], "(13, 7)"),
        (vec!["add", "5,1", "O"], "= (5, 1)"),
        (vec!["inverse", "2"], "= 9"),
    ] {
        success(&args, expected);
    }
}

#[test]
fn group_commands() {
    for (args, expected) in [
        (vec!["info"], "Δ ="),
        (vec!["check", "5,1"], "true"),
        (vec!["check", "1,1"], "false"),
        (vec!["points"], "#E(Fp) = 19"),
        (vec!["count"], "#E(Fp) = 19"),
        (vec!["order", "5,1"], "= 19"),
        (vec!["subgroup", "5,1"], "18P = (5, 16)"),
        (vec!["dlog", "5,1", "0,6"], "k = 7"),
        (
            vec!["ecdh", "5,1", "5", "7"],
            "Совпадение общих точек: true",
        ),
    ] {
        success(&args, expected);
    }
}

#[test]
fn alternate_curve_and_table() {
    success(
        &["--p", "5", "--a", "1", "--b", "0", "table"],
        "P3 = (3, 0)",
    );
    success(
        &["--p", "5", "--a", "1", "--b", "0", "double", "0,0"],
        "= O",
    );
}

#[test]
fn normalization_and_negative_coefficients() {
    success(&["--a", "-15", "--b", "19", "check", "-12,18"], "true");
}

#[test]
fn errors_have_nonzero_exit_status() {
    for args in [
        vec!["--p", "15", "info"],
        vec!["--a", "0", "--b", "0", "info"],
        vec!["add", "1,1", "O"],
        vec!["mul", "0", "1,1"],
        vec!["inverse", "0"],
        vec!["check", "5"],
        vec!["check", "1,2,3"],
        vec!["ecdh", "5,1", "0", "7"],
        vec!["--p", "10007", "points"],
        vec!["--p", "101", "table"],
        vec!["--p", "5", "--a", "1", "--b", "0", "dlog", "0,0", "2,0"],
    ] {
        let output = run(&args);
        assert!(!output.status.success(), "{args:?}");
        assert!(!output.stderr.is_empty());
    }
}

#[test]
fn demo_and_help() {
    success(&["demo"], "Sₐ = aB = (10, 11)");
    success(&["--help"], "калькулятор");
}
