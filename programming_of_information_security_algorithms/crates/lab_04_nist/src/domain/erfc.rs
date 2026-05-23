//! Реализация комплементарной функции ошибок без `libm`.
//!
//! Используется аппроксимация Abramowitz-Stegun 7.1.26 — полином пятой степени.
//! Максимальная погрешность для всех `x ≥ 0` — не больше `1.5·10⁻⁷`,
//! чего более чем достаточно для NIST-тестов (там сравнение с α = 0.01).
//!
//! Условие лаб 4 говорит «реализовать самостоятельно» — здесь это про сам
//! статистический тест, но опираться на `libm`/`statrs` тоже не хочется,
//! поэтому всю математику считаем своими силами.

/// Аппроксимация `erfc(x)` для произвольного вещественного `x`.
///
/// Для `x < 0` используется симметрия `erfc(-x) = 2 - erfc(x)`.
#[must_use]
pub fn erfc(x: f64) -> f64 {
    if x < 0.0 {
        2.0 - erfc(-x)
    } else {
        erfc_nonneg(x)
    }
}

fn erfc_nonneg(x: f64) -> f64 {
    // Abramowitz-Stegun 7.1.26. Только для x ≥ 0.
    const A: [f64; 5] = [
        0.254_829_592,
        -0.284_496_736,
        1.421_413_741,
        -1.453_152_027,
        1.061_405_429,
    ];
    const P: f64 = 0.327_591_1;

    let t = 1.0 / (1.0 + P * x);
    let y = (((A[4] * t + A[3]) * t + A[2]) * t + A[1]) * t + A[0];
    y * t * exp_neg(x * x)
}

/// Аппроксимация `exp(-z)` для `z ≥ 0`.
///
/// Используется тождество `exp(-z) = (exp(-z/2^k))^(2^k)`. `k` подбирается
/// динамически так, чтобы `z/2^k ≤ 0.5` — тогда ряд Тейлора сходится
/// очень быстро (≤ 18 членов до уровня `1e-18`). Это критично: NIST-тесты
/// дают `z = x²` вплоть до ~500 (статистика 22+), при фиксированном маленьком
/// `k` ряд бы расходился.
fn exp_neg(z: f64) -> f64 {
    if z == 0.0 {
        return 1.0;
    }
    // Сводим к |scaled| ≤ 0.5.
    let mut shift: u32 = 0;
    let mut scaled = z;
    while scaled > 0.5 {
        scaled *= 0.5;
        shift += 1;
    }
    let mut acc = taylor_exp_neg(scaled);
    for _ in 0..shift {
        acc *= acc;
    }
    acc
}

fn taylor_exp_neg(z: f64) -> f64 {
    // exp(-z) = sum_{k=0..∞} (-z)^k / k!
    let mut term = 1.0;
    let mut sum = 1.0;
    for k in 1..18 {
        term *= -z / f64::from(k);
        sum += term;
        if term.abs() < 1e-18 {
            break;
        }
    }
    sum
}

#[cfg(test)]
mod tests {
    use super::*;

    fn close(a: f64, b: f64, tol: f64) -> bool {
        (a - b).abs() < tol
    }

    #[test]
    fn erfc_at_zero_is_one() {
        assert!(close(erfc(0.0), 1.0, 1e-7));
    }

    #[test]
    fn erfc_is_antisymmetric_around_one() {
        // erfc(-x) + erfc(x) = 2.
        for &x in &[0.1, 0.5, 1.0, 2.0, 3.0] {
            let s = erfc(-x) + erfc(x);
            assert!(close(s, 2.0, 1e-6), "erfc(-{x}) + erfc({x}) = {s}");
        }
    }

    /// Известные значения erfc, сверенные с математическим справочником.
    #[test]
    fn erfc_known_values() {
        let cases = [
            (0.5, 0.479_500),
            (1.0, 0.157_299),
            (1.5, 0.033_895),
            (2.0, 0.004_678),
            (2.5, 0.000_407),
            (3.0, 0.000_022),
        ];
        for (x, expected) in cases {
            let v = erfc(x);
            assert!(
                close(v, expected, 5e-5),
                "erfc({x}) = {v}, ожидалось ≈ {expected}",
            );
        }
    }
}
