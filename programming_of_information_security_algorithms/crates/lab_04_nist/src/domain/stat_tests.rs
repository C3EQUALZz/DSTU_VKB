//! Собственные реализации статистических тестов из
//! [NIST SP 800-22 Rev. 1a](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-22r1a.pdf).
//!
//! Основной — **Monobit Frequency Test** (§2.1).
//! Бонусом — **Runs Test** (§2.3) с предварительной проверкой пропорции единиц.

use tracing::{debug, info};

use crate::domain::erfc::erfc;

/// Граница принятия теста: NIST SP 800-22 рекомендует α = 0.01.
pub const ALPHA: f64 = 0.01;

/// Решение по конкретному тесту.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Verdict {
    /// `P-value ≥ α` — последовательность считается случайной.
    Random,
    /// `P-value < α` — последовательность не прошла тест.
    NonRandom,
}

impl Verdict {
    pub const fn label(self) -> &'static str {
        match self {
            Self::Random => "RANDOM",
            Self::NonRandom => "NON-RANDOM",
        }
    }
}

/// Результат одного NIST-теста.
#[derive(Debug, Clone)]
pub struct NistTestResult {
    pub name: &'static str,
    pub n: usize,
    pub ones: usize,
    pub zeros: usize,
    /// Числитель статистики (`S_n` для monobit, `V_n` для runs).
    pub statistic_raw: f64,
    /// Нормированная статистика (то, что идёт в `erfc`).
    pub statistic_norm: f64,
    pub p_value: f64,
    pub verdict: Verdict,
    /// Подробности теста для отчёта.
    pub details: Vec<(&'static str, String)>,
}

impl NistTestResult {
    #[must_use]
    pub fn passed(&self) -> bool {
        matches!(self.verdict, Verdict::Random)
    }
}

/// Считает кол-во единиц и нулей.
fn count(bits: &[bool]) -> (usize, usize) {
    let ones = bits.iter().filter(|&&b| b).count();
    let zeros = bits.len() - ones;
    (ones, zeros)
}

/// NIST SP 800-22 §2.1 — **Frequency (Monobit) Test**.
///
/// Преобразует `bᵢ ∈ {0,1}` в `Xᵢ = 2bᵢ − 1`, считает `Sₙ = ΣXᵢ`,
/// статистику `s_obs = |Sₙ| / √n` и P-value = `erfc(s_obs / √2)`.
///
/// # Panics
/// Если последовательность пуста.
#[must_use]
pub fn monobit(bits: &[bool]) -> NistTestResult {
    assert!(!bits.is_empty(), "monobit: пустая последовательность");
    let n = bits.len();
    let (ones, zeros) = count(bits);
    // S_n = (число единиц) − (число нулей).
    let s_n = ones as i64 - zeros as i64;
    let s_obs = (s_n as f64).abs() / (n as f64).sqrt();
    let p_value = erfc(s_obs / std::f64::consts::SQRT_2);
    let verdict = if p_value >= ALPHA {
        Verdict::Random
    } else {
        Verdict::NonRandom
    };
    debug!(
        n,
        ones,
        zeros,
        s_n,
        s_obs,
        p_value,
        verdict = ?verdict,
        "monobit result"
    );
    info!(
        test = "Monobit Frequency",
        n,
        p_value,
        verdict = verdict.label()
    );
    NistTestResult {
        name: "NIST SP 800-22 §2.1 Frequency (Monobit) Test",
        n,
        ones,
        zeros,
        statistic_raw: s_n as f64,
        statistic_norm: s_obs,
        p_value,
        verdict,
        details: vec![
            ("S_n (ones - zeros)", format!("{s_n}")),
            ("s_obs", format!("{s_obs:.6}")),
            ("alpha", format!("{ALPHA}")),
        ],
    }
}

/// NIST SP 800-22 §2.3 — **Runs Test**.
///
/// Сначала проверяется пропорция единиц `π = ones/n`: если `|π − 0.5| ≥ 2/√n`,
/// тест считается провалившимся ещё до подсчёта runs (NIST §2.3.4 шаг 1).
/// Иначе `V_n = 1 + Σ I[bᵢ ≠ b_{i+1}]`, статистика
/// `(V_n − 2nπ(1−π)) / (2√n · π(1−π))`, P-value через `erfc(|·| / √2)`.
///
/// # Panics
/// Если последовательность пуста.
#[must_use]
pub fn runs(bits: &[bool]) -> NistTestResult {
    assert!(!bits.is_empty(), "runs: пустая последовательность");
    let n = bits.len();
    let (ones, zeros) = count(bits);
    let pi = ones as f64 / n as f64;

    let pre_threshold = 2.0 / (n as f64).sqrt();
    if (pi - 0.5).abs() >= pre_threshold {
        // Не прошли предварительную проверку — P-value считаем нулём по NIST §2.3.4.
        info!(
            test = "Runs",
            n,
            pi,
            pre_threshold,
            verdict = "NON-RANDOM",
            "пропорция единиц вне диапазона предварительного теста"
        );
        return NistTestResult {
            name: "NIST SP 800-22 §2.3 Runs Test",
            n,
            ones,
            zeros,
            statistic_raw: 0.0,
            statistic_norm: 0.0,
            p_value: 0.0,
            verdict: Verdict::NonRandom,
            details: vec![
                ("pi", format!("{pi:.6}")),
                ("|pi - 0.5|", format!("{:.6}", (pi - 0.5).abs())),
                ("pre-threshold (2/√n)", format!("{pre_threshold:.6}")),
                ("reason", "failed pre-test".to_string()),
            ],
        };
    }

    let mut v_n: u64 = 1;
    for i in 0..n - 1 {
        if bits[i] != bits[i + 1] {
            v_n += 1;
        }
    }
    let mean = 2.0 * n as f64 * pi * (1.0 - pi);
    let denom = 2.0 * (n as f64).sqrt() * pi * (1.0 - pi);
    let statistic = (v_n as f64 - mean) / denom;
    let p_value = erfc(statistic.abs() / std::f64::consts::SQRT_2);
    let verdict = if p_value >= ALPHA {
        Verdict::Random
    } else {
        Verdict::NonRandom
    };
    info!(test = "Runs", n, p_value, verdict = verdict.label());
    NistTestResult {
        name: "NIST SP 800-22 §2.3 Runs Test",
        n,
        ones,
        zeros,
        statistic_raw: v_n as f64,
        statistic_norm: statistic,
        p_value,
        verdict,
        details: vec![
            ("V_n (число переходов + 1)", format!("{v_n}")),
            ("pi", format!("{pi:.6}")),
            ("mean", format!("{mean:.6}")),
            ("statistic", format!("{statistic:.6}")),
            ("alpha", format!("{ALPHA}")),
        ],
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn to_bits(s: &str) -> Vec<bool> {
        s.chars().map(|c| c == '1').collect()
    }

    /// NIST SP 800-22 §2.1.8 (Example): ε = «11001001000011111101101010100010
    /// 0010000101101000110000100011010011000100110001100110001010001011100000
    /// 11011100000010100110100100110000 (100 bit prefix of π)» — P-value ≈ 0.109599.
    #[test]
    fn monobit_matches_nist_example_pi_prefix() {
        let s = "1100100100001111110110101010001000100001011010001100\
                 001000110100110001001100011001100010100010111000";
        let bits = to_bits(s);
        assert_eq!(bits.len(), 100);
        let r = monobit(&bits);
        assert!(
            (r.p_value - 0.109_599).abs() < 5e-4,
            "P-value = {p}",
            p = r.p_value
        );
        assert_eq!(r.verdict, Verdict::Random);
    }

    #[test]
    fn monobit_rejects_all_zeros() {
        let bits = vec![false; 100];
        let r = monobit(&bits);
        assert_eq!(r.verdict, Verdict::NonRandom);
        assert!(
            r.p_value < 1e-15,
            "ожидалось ≈ 0, получено {p}",
            p = r.p_value
        );
    }

    #[test]
    fn monobit_rejects_all_ones() {
        let bits = vec![true; 100];
        let r = monobit(&bits);
        assert_eq!(r.verdict, Verdict::NonRandom);
    }

    /// 50/50 на чередующейся последовательности → S_n = 0 → P-value = 1.
    #[test]
    fn monobit_accepts_alternating() {
        let bits: Vec<bool> = (0..100).map(|i| i % 2 == 0).collect();
        let r = monobit(&bits);
        assert!((r.p_value - 1.0).abs() < 1e-7);
        assert_eq!(r.verdict, Verdict::Random);
    }

    /// NIST §2.3.8 (Example): тот же 100-битный префикс π — P-value ≈ 0.500798.
    #[test]
    fn runs_matches_nist_example_pi_prefix() {
        let s = "1100100100001111110110101010001000100001011010001100\
                 001000110100110001001100011001100010100010111000";
        let bits = to_bits(s);
        assert_eq!(bits.len(), 100);
        let r = runs(&bits);
        assert!(
            (r.p_value - 0.500_798).abs() < 2e-3,
            "P-value = {p}",
            p = r.p_value
        );
        assert_eq!(r.verdict, Verdict::Random);
    }

    /// Чередующаяся 010101... — много переходов → Runs Test покажет
    /// статистику далеко от ожидаемой → отвергнет.
    #[test]
    fn runs_rejects_alternating() {
        let bits: Vec<bool> = (0..1000).map(|i| i % 2 == 0).collect();
        let r = runs(&bits);
        assert_eq!(r.verdict, Verdict::NonRandom);
    }

    /// Однородная последовательность (все нули) не проходит даже
    /// предварительный тест Runs.
    #[test]
    fn runs_rejects_all_zeros_via_pre_test() {
        let bits = vec![false; 1000];
        let r = runs(&bits);
        assert_eq!(r.verdict, Verdict::NonRandom);
        assert!(r.p_value < 1e-15);
    }
}
