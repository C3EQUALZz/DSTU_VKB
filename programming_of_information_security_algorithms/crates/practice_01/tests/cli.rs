//! Интеграционные тесты CLI — запускают собранный бинарь `practice_01`
//! и проверяют его поведение «снаружи».
//!
//! Cargo экспортирует путь к собранному бинарю в env-переменной
//! `CARGO_BIN_EXE_<bin-name>`, поэтому никаких новых dev-dependencies
//! (`assert_cmd`/`escargot`) не нужно.

use std::process::Command;

/// Создаёт `Command` для нашего бинаря и глушит логгер,
/// чтобы stderr не засорял ассерты.
fn cli() -> Command {
    let mut cmd = Command::new(env!("CARGO_BIN_EXE_practice_01"));
    cmd.env("RUST_LOG", "off");
    cmd.env("NO_COLOR", "1"); // стабилизация вывода для contains-ассертов
    cmd
}

fn run(args: &[&str]) -> (bool, String, String) {
    let out = cli().args(args).output().expect("запуск practice_01");
    (
        out.status.success(),
        String::from_utf8_lossy(&out.stdout).into_owned(),
        String::from_utf8_lossy(&out.stderr).into_owned(),
    )
}

#[test]
fn add_small_prints_result_and_checks_against_i128() {
    let (ok, stdout, _stderr) = run(&["add", "12345", "67890"]);
    assert!(ok, "exit code must be 0");
    assert!(stdout.contains("BigInt:    80235"), "stdout = {stdout}");
    assert!(stdout.contains("i128:      80235"));
    assert!(stdout.contains("OK"));
}

#[test]
fn sub_small_prints_negative_when_b_gt_a() {
    let (ok, stdout, _) = run(&["sub", "100", "200"]);
    assert!(ok);
    assert!(stdout.contains("BigInt:    -100"));
    assert!(stdout.contains("i128:      -100"));
}

#[test]
fn add_long_numbers_succeeds_and_reports_unchecked() {
    // 80-разрядное число.
    let a = "1".to_string() + &"0".repeat(79);
    let b = "9".repeat(80);
    let (ok, stdout, _) = run(&["add", &a, &b]);
    assert!(ok);
    // Сумма: единица + 80 девяток = 10999...999 (80 девяток после старшей цифры).
    assert!(
        stdout.contains(
            "10999999999999999999999999999999999999999999999999999999999999999999999999999999"
        ),
        "stdout = {stdout}"
    );
    // Должно явно сообщить, что i128 не справилась.
    assert!(stdout.contains("вне диапазона"));
}

#[test]
fn sub_long_numbers_negative_result() {
    let (ok, stdout, _) = run(&[
        "sub",
        "10",
        "10000000000000000000000000000000000000000000000",
    ]);
    assert!(ok);
    assert!(stdout.contains("-9999999999999999999999999999999999999999999990"));
}

#[test]
fn hex_input_is_accepted() {
    let (ok, stdout, _) = run(&["add", "0xFF", "1"]);
    assert!(ok);
    assert!(stdout.contains("BigInt:    256"));
}

#[test]
fn invalid_operand_returns_nonzero_exit_code() {
    let (ok, stdout, stderr) = run(&["add", "12abc", "1"]);
    assert!(
        !ok,
        "exit code must be non-zero. stdout = {stdout} stderr = {stderr}"
    );
    let msg = stderr + &stdout;
    assert!(msg.to_lowercase().contains("симв") || msg.to_lowercase().contains("char"));
}

#[test]
fn missing_arguments_returns_nonzero_exit_code() {
    let (ok, _stdout, stderr) = run(&["add", "12"]);
    assert!(!ok);
    assert!(
        stderr.to_lowercase().contains("required")
            || stderr.to_lowercase().contains("argument")
            || stderr.contains("Usage"),
        "stderr = {stderr}"
    );
}

#[test]
fn demo_runs_to_completion_without_error() {
    let (ok, stdout, _) = run(&["demo"]);
    assert!(ok);
    // Демо обязательно показывает и совпадение, и невозможность проверки.
    assert!(stdout.contains("OK"));
    assert!(stdout.contains("вне диапазона"));
}

#[test]
fn help_subcommand_lists_operations() {
    let (ok, stdout, _) = run(&["--help"]);
    assert!(ok);
    assert!(stdout.contains("add"));
    assert!(stdout.contains("sub"));
    assert!(stdout.contains("demo"));
}
