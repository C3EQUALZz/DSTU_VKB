//! Векторные тесты на числах ≥ 64 разрядов — то, что прямо требует условие
//! практики. Эталонные значения посчитаны заранее и зашиты в тесты.

use practice_01::application::{Operation, VerifyService};
use practice_01::domain::{BigInt, add, sub};

/// Главный тест условия: оба операнда ≥ 64 десятичных разрядов, перенос идёт
/// далеко за пределы `u128`. Эталон — вручную сложенные строки.
#[test]
fn add_two_70_digit_numbers() {
    // 70 цифр: 1 затем 69 нулей.
    let a: BigInt = "1000000000000000000000000000000000000000000000000000000000000000000000"
        .parse()
        .unwrap();
    // 70 цифр: 70 девяток.
    let b: BigInt = "9999999999999999999999999999999999999999999999999999999999999999999999"
        .parse()
        .unwrap();
    // Сумма = 10999...999 (всего 71 цифра).
    let expected = "10999999999999999999999999999999999999999999999999999999999999999999999";

    let sum = add(&a, &b);
    assert_eq!(sum.to_string(), expected);
    assert_eq!(sum.decimal_digits(), 71);
}

#[test]
fn sub_brings_70_digit_number_below_70_digits() {
    let a: BigInt = "1000000000000000000000000000000000000000000000000000000000000000000000"
        .parse()
        .unwrap();
    let one = BigInt::from_i128(1);
    let diff = sub(&a, &one);
    // 10^69 - 1 = 69 девяток.
    assert_eq!(
        diff.to_string(),
        "999999999999999999999999999999999999999999999999999999999999999999999"
    );
    assert_eq!(diff.decimal_digits(), 69);
}

#[test]
fn sub_yields_negative_when_subtrahend_is_larger() {
    let a: BigInt = "10".parse().unwrap();
    let b: BigInt = "10000000000000000000000000000000000000000000000"
        .parse()
        .unwrap();
    let diff = sub(&a, &b);
    assert_eq!(
        diff.to_string(),
        "-9999999999999999999999999999999999999999999990"
    );
}

#[test]
fn add_of_mixed_signs_cancels_high_limbs() {
    // a и b отличаются только на 1, но оба огромные → результат маленький.
    let a: BigInt = "100000000000000000000000000000000000000000000000000000000000000000"
        .parse()
        .unwrap();
    let b: BigInt = "-99999999999999999999999999999999999999999999999999999999999999999"
        .parse()
        .unwrap();
    let s = add(&a, &b);
    assert_eq!(s.to_string(), "1");
}

#[test]
fn add_is_commutative_on_big_numbers() {
    let a: BigInt =
        "12345678901234567890123456789012345678901234567890123456789012345678901234567890"
            .parse()
            .unwrap();
    let b: BigInt = "98765432109876543210987654321098765432109876543210987654321098765432109876543"
        .parse()
        .unwrap();
    assert_eq!(add(&a, &b), add(&b, &a));
}

#[test]
fn add_is_associative_on_big_numbers() {
    let a: BigInt = "11111111111111111111111111111111111111111111111111111111111111111111"
        .parse()
        .unwrap();
    let b: BigInt = "22222222222222222222222222222222222222222222222222222222222222222222"
        .parse()
        .unwrap();
    let c: BigInt = "-33333333333333333333333333333333333333333333333333333333333333333334"
        .parse()
        .unwrap();
    let lhs = add(&add(&a, &b), &c);
    let rhs = add(&a, &add(&b, &c));
    assert_eq!(lhs, rhs);
    // По построению a + b + c = -1.
    assert_eq!(lhs.to_string(), "-1");
}

#[test]
fn sub_is_inverse_of_add_on_big_numbers() {
    let a: BigInt =
        "12345678901234567890123456789012345678901234567890123456789012345678901234567890"
            .parse()
            .unwrap();
    let b: BigInt =
        "987654321098765432109876543210987654321098765432109876543210987654321098765432"
            .parse()
            .unwrap();
    let round_trip = sub(&add(&a, &b), &b);
    assert_eq!(round_trip, a);
}

#[test]
fn carry_propagates_through_many_limbs() {
    // a — 100 девяток, b = 1. Перенос пройдёт через все 100 десятичных разрядов,
    // то есть через ~11 u32-limb'ов (ceil(log2(10^100)/32) ≈ 11).
    let a: BigInt = "9".repeat(100).parse().unwrap();
    let s = add(&a, &BigInt::from_i128(1));
    let expected = "1".to_string() + &"0".repeat(100);
    assert_eq!(s.to_string(), expected);
    assert_eq!(s.decimal_digits(), 101);
}

#[test]
fn borrow_propagates_through_many_limbs() {
    // a = 10^100, a - 1 = 100 девяток.
    let a: BigInt = ("1".to_string() + &"0".repeat(100)).parse().unwrap();
    let d = sub(&a, &BigInt::from_i128(1));
    assert_eq!(d.to_string(), "9".repeat(100));
    assert_eq!(d.decimal_digits(), 100);
}

#[test]
fn verify_service_marks_big_numbers_as_unchecked() {
    let svc = VerifyService::new();
    let a = "1".to_string() + &"0".repeat(80);
    let report = svc.run(Operation::Add, &a, &a).unwrap();
    assert!(
        report.builtin_result.is_none(),
        "i128 не должна охватить число с 80 нулями"
    );
    assert!(!report.builtin_matches);
    assert_eq!(report.result.decimal_digits(), 81);
}

#[test]
fn verify_service_matches_i128_within_range() {
    let svc = VerifyService::new();
    // i128::MAX / 2 + i128::MAX / 2 ≈ i128::MAX. Полностью внутри диапазона.
    let half = (i128::MAX / 2).to_string();
    let report = svc.run(Operation::Add, &half, &half).unwrap();
    assert_eq!(report.builtin_result, Some(i128::MAX - 1));
    assert!(report.builtin_matches);
}

#[test]
fn parse_hex_with_64_hex_digits_round_trips_to_decimal() {
    // 64 hex-цифры = 256 бит = ~77 десятичных цифр (≥ 64 разрядов).
    let hex = "0x".to_string() + &"F".repeat(64);
    let n: BigInt = hex.parse().unwrap();
    assert_eq!(n.bit_length(), 256);
    let expected_dec =
        "115792089237316195423570985008687907853269984665640564039457584007913129639935";
    assert_eq!(n.to_string(), expected_dec);
    assert_eq!(n.decimal_digits(), 78);
}
