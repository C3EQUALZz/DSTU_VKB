//! Автоматический взлом шифра простой замены.
//!
//! Алгоритм: частотная затравка (самый частый код → пробел и т.д.) и затем
//! имитация отжига (simulated annealing) по биграммной лог-модели русского языка
//! ([`super::bigram_model`]). Пробел закрепляется за самым частым кодом и не
//! участвует в перестановках — это сохраняет границы слов.

use std::collections::HashMap;

use rand::RngCore;
use rand::SeedableRng;
use rand::rngs::StdRng;
use rand::seq::SliceRandom;

use super::bigram_model::{BIGRAM_LOGP, N};

/// Порядок букв русского алфавита по убыванию частоты (для затравки).
const FREQ_ORDER: [usize; N] = [
    32, 14, 5, 0, 8, 18, 13, 17, 16, 2, 11, 10, 12, 4, 15, 19, 31, 27, 7, 28, 1, 3, 23, 9, 21, 6,
    30, 24, 22, 25, 29, 20, 26,
];

/// Результат взлома.
#[derive(Debug, Clone)]
pub struct Solution {
    /// Карта код → индекс буквы алфавита.
    pub map: HashMap<u32, usize>,
    /// Закодированный пробелом код.
    pub space_code: u32,
    /// Достигнутое значение приспособленности (сумма лог-вероятностей биграмм).
    pub fitness: f64,
}

fn frequency_order(codes: &[u32]) -> Vec<u32> {
    let mut counts: HashMap<u32, usize> = HashMap::new();
    for &c in codes {
        *counts.entry(c).or_default() += 1;
    }
    let mut order: Vec<(u32, usize)> = counts.into_iter().collect();
    order.sort_by(|a, b| b.1.cmp(&a.1).then(a.0.cmp(&b.0)));
    order.into_iter().map(|(c, _)| c).collect()
}

/// Уникальные коды по возрастанию.
fn unique_sorted(codes: &[u32]) -> Vec<u32> {
    let mut v: Vec<u32> = codes.to_vec();
    v.sort_unstable();
    v.dedup();
    v
}

type Bigrams = Vec<(usize, usize, f64)>;

/// Биграммы кодов: (i, j, частота) для соседних позиций шифртекста (по индексам в `uniq`).
fn code_bigrams(codes: &[u32], pos: &HashMap<u32, usize>) -> Bigrams {
    let mut cnt: HashMap<(usize, usize), f64> = HashMap::new();
    for w in codes.windows(2) {
        let a = pos[&w[0]];
        let b = pos[&w[1]];
        *cnt.entry((a, b)).or_default() += 1.0;
    }
    cnt.into_iter().map(|((a, b), c)| (a, b, c)).collect()
}

fn full_fitness(bigrams: &Bigrams, letters: &[usize]) -> f64 {
    bigrams
        .iter()
        .map(|&(a, b, cnt)| cnt * BIGRAM_LOGP[letters[a]][letters[b]])
        .sum()
}

/// Взломать шифртекст. `rounds` — число рестартов, `iters` — итераций отжига на рестарт.
pub fn solve(codes: &[u32], rounds: usize, iters: usize) -> Solution {
    let uniq = unique_sorted(codes);
    let pos: HashMap<u32, usize> = uniq.iter().enumerate().map(|(i, &c)| (c, i)).collect();
    let bigrams = code_bigrams(codes, &pos);

    // Биграммы, сгруппированные по индексу — для быстрой дельты.
    let mut by_idx: Vec<Vec<(usize, usize, f64)>> = vec![Vec::new(); uniq.len()];
    for &(a, b, cnt) in &bigrams {
        by_idx[a].push((a, b, cnt));
        if b != a {
            by_idx[b].push((a, b, cnt));
        }
    }

    // Самый частый код → пробел (индекс 32). Его фиксируем.
    let freq = frequency_order(codes);
    let space_code = freq[0];
    let space_idx = pos[&space_code];

    // Стартовая раскладка: частотная затравка.
    let seed_letters = |order: &[u32]| -> Vec<usize> {
        let mut letters = vec![0usize; uniq.len()];
        let mut used = [false; N];
        for (rank, &code) in order.iter().enumerate() {
            let li = if rank < FREQ_ORDER.len() {
                FREQ_ORDER[rank]
            } else {
                (0..N).find(|x| !used[*x]).unwrap_or(0)
            };
            letters[pos[&code]] = li;
            used[li] = true;
        }
        letters[space_idx] = 32; // пробел
        letters
    };

    let swap_pool: Vec<usize> = (0..uniq.len()).filter(|&i| i != space_idx).collect();
    let mut best_global = seed_letters(&freq);
    let mut best_global_fit = full_fitness(&bigrams, &best_global);

    for r in 0..rounds {
        let mut rng = StdRng::seed_from_u64(1000 + r as u64);
        let mut letters = seed_letters(&freq);
        if r > 0 {
            // случайная перестановка букв для непробельных кодов
            let mut vals: Vec<usize> = swap_pool.iter().map(|&i| letters[i]).collect();
            vals.shuffle(&mut rng);
            for (k, &i) in swap_pool.iter().enumerate() {
                letters[i] = vals[k];
            }
            letters[space_idx] = 32;
        }
        let mut cur_fit = full_fitness(&bigrams, &letters);
        let mut best = letters.clone();
        let mut best_fit = cur_fit;

        for it in 0..iters {
            let t = (3.0 * (1.0 - it as f64 / iters as f64)).max(0.05);
            let a = *swap_pool.choose(&mut rng).unwrap();
            let mut b = *swap_pool.choose(&mut rng).unwrap();
            while b == a {
                b = *swap_pool.choose(&mut rng).unwrap();
            }
            // дельта только по затронутым биграммам
            let affected: Vec<(usize, usize, f64)> = by_idx[a]
                .iter()
                .copied()
                .chain(
                    by_idx[b]
                        .iter()
                        .copied()
                        .filter(|&(ci, cj, _)| ci != a && cj != a),
                )
                .collect();
            let before: f64 = affected
                .iter()
                .map(|&(ci, cj, cnt)| cnt * BIGRAM_LOGP[letters[ci]][letters[cj]])
                .sum();
            letters.swap(a, b);
            let after: f64 = affected
                .iter()
                .map(|&(ci, cj, cnt)| cnt * BIGRAM_LOGP[letters[ci]][letters[cj]])
                .sum();
            let d = after - before;
            let accept = d >= 0.0 || rng.next_u64() as f64 / (u64::MAX as f64) < (d / t).exp();
            if accept {
                cur_fit += d;
                if cur_fit > best_fit {
                    best_fit = cur_fit;
                    best.clone_from(&letters);
                }
            } else {
                letters.swap(a, b); // откат
            }
        }
        if best_fit > best_global_fit {
            best_global_fit = best_fit;
            best_global = best;
        }
    }

    let map: HashMap<u32, usize> = uniq.iter().map(|&c| (c, best_global[pos[&c]])).collect();
    Solution {
        map,
        space_code,
        fitness: best_global_fit,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::cipher::parse_codes;

    #[test]
    fn recovers_known_substitution_text() {
        // Зашифруем известный русский текст простой заменой и проверим взлом.
        let plain = "В_ДАННОЙ_СТАТЬЕ_ПРИВЕДЕНЫ_РЕЗУЛЬТАТЫ_АНАЛИЗА_ФАКТОРОВ_ВЛИЯЮЩИХ_\
                     НА_ВЫБОР_ОБОРУДОВАНИЯ_ДЛЯ_СТРОИТЕЛЬСТВА_ЗДАНИЙ_И_СООРУЖЕНИЙ_\
                     РАЗЛИЧНОГО_НАЗНАЧЕНИЯ_В_УСЛОВИЯХ_ПЛОТНОЙ_ГОРОДСКОЙ_ЗАСТРОЙКИ";
        use shared::alphabet::index_of;
        let idx: Vec<usize> = plain.chars().map(|c| index_of(c).unwrap()).collect();
        // случайная подстановка letter->code (code = letter*7+3 как простая инъекция)
        let codes: Vec<u32> = idx.iter().map(|&i| (i as u32) * 7 + 3).collect();
        let sol = solve(&codes, 6, 20_000);
        // Восстановленный текст должен совпасть хотя бы на 85% символов.
        let recovered: Vec<usize> = codes.iter().map(|c| sol.map[c]).collect();
        let matches = recovered.iter().zip(&idx).filter(|(a, b)| a == b).count();
        let ratio = matches as f64 / idx.len() as f64;
        assert!(ratio > 0.85, "совпадение {ratio:.2} < 0.85");
    }

    #[test]
    fn parse_then_solve_smoke() {
        let codes = parse_codes("50 50 50 45 45 42 50 45").unwrap();
        let sol = solve(&codes, 2, 1000);
        assert_eq!(sol.map.len(), 3);
    }
}
