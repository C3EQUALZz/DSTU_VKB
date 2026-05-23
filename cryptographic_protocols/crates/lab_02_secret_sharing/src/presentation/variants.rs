//! Таблицы заданий по 28 вариантам (упражнения 2 и 3 из методички).

use crate::domain::blakley::SecretPoint;
use crate::domain::shamir::Share;

/// Данные одного варианта упражнения 2 Шамира.
#[derive(Debug, Clone)]
pub struct ShamirCase {
    pub p: i64,
    /// Доли (m штук), по которым нужно восстановить секрет.
    pub shares: Vec<Share>,
}

/// Полный вариант упражнения 2: левая колонка (m=4, p=23) и правая (m=3, p=31).
#[derive(Debug, Clone)]
pub struct ShamirVariant {
    pub left: ShamirCase,
    pub right: ShamirCase,
}

/// Полный вариант упражнения 3 Блэкли: левая колонка (p=17) и правая (p=31).
#[derive(Debug, Clone)]
pub struct BlakleyVariant {
    pub left_p: i64,
    pub left_q: SecretPoint,
    /// 4 пары (a, b): A, B, D, C — порядок как в таблице методички.
    pub left_pairs: [(i64, i64); 4],
    pub right_p: i64,
    pub right_q: SecretPoint,
    pub right_pairs: [(i64, i64); 4],
}

#[allow(clippy::too_many_lines)]
pub fn shamir_variants() -> Vec<ShamirVariant> {
    fn s(pairs: &[(i64, i64)]) -> Vec<Share> {
        pairs.iter().map(|&(x, y)| Share { x, y }).collect()
    }
    vec![
        // 1
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(2, 17), (7, 13), (19, 14), (21, 20)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(9, 14), (19, 23), (21, 7)]),
            },
        },
        // 2
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(18, 14), (19, 4), (12, 22), (13, 8)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(1, 29), (17, 29), (22, 16)]),
            },
        },
        // 3
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(22, 11), (15, 16), (5, 13), (6, 9)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(22, 27), (12, 16), (2, 22)]),
            },
        },
        // 4
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(14, 3), (15, 19), (3, 22), (4, 7)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(12, 24), (9, 26), (3, 18)]),
            },
        },
        // 5
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(10, 14), (18, 20), (19, 14), (8, 3)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(15, 0), (13, 23), (4, 12)]),
            },
        },
        // 6
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(10, 6), (13, 8), (14, 3), (1, 6)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(20, 6), (10, 12), (13, 19)]),
            },
        },
        // 7
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(12, 4), (16, 22), (13, 8), (1, 20)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(11, 7), (3, 18), (1, 24)]),
            },
        },
        // 8
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(17, 1), (16, 22), (11, 10), (2, 18)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(18, 8), (11, 1), (4, 17)]),
            },
        },
        // 9
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(18, 20), (19, 14), (12, 4), (9, 3)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(20, 16), (7, 13), (14, 28)]),
            },
        },
        // 10
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(19, 4), (18, 14), (17, 1), (1, 6)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(15, 18), (7, 1), (16, 22)]),
            },
        },
        // 11
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(9, 3), (1, 20), (2, 17), (10, 14)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(6, 25), (16, 1), (18, 28)]),
            },
        },
        // 12
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(9, 21), (19, 4), (13, 8), (10, 6)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(14, 17), (21, 25), (2, 22)]),
            },
        },
        // 13
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(2, 17), (3, 18), (12, 4), (15, 16)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(8, 30), (17, 0), (10, 27)]),
            },
        },
        // 14
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(3, 22), (6, 14), (17, 1), (22, 2)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(8, 12), (13, 19), (18, 8)]),
            },
        },
        // 15
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(19, 14), (6, 9), (20, 6), (13, 8)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(7, 13), (15, 0), (20, 16)]),
            },
        },
        // 16
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(1, 6), (7, 14), (19, 4), (8, 20)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(12, 24), (10, 12), (2, 22)]),
            },
        },
        // 17
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(4, 1), (14, 4), (5, 13), (17, 0)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(21, 7), (5, 4), (17, 0)]),
            },
        },
        // 18
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(18, 14), (19, 4), (13, 8), (10, 6)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(18, 8), (14, 17), (5, 19)]),
            },
        },
        // 19
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(5, 13), (22, 11), (16, 22), (13, 8)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(13, 23), (1, 24), (8, 30)]),
            },
        },
        // 20
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(20, 6), (9, 21), (7, 14), (21, 9)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(3, 18), (16, 22), (8, 12)]),
            },
        },
        // 21
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(2, 17), (3, 18), (12, 4), (15, 16)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(6, 25), (10, 27), (16, 1)]),
            },
        },
        // 22
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(14, 3), (9, 21), (15, 19), (4, 7)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(6, 24), (19, 21), (21, 25)]),
            },
        },
        // 23
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(7, 13), (6, 9), (8, 3), (2, 17)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(18, 28), (12, 16), (2, 22)]),
            },
        },
        // 24
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(10, 6), (4, 7), (5, 8), (14, 3)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(22, 16), (15, 18), (7, 1)]),
            },
        },
        // 25
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(11, 14), (21, 20), (22, 11), (9, 3)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(22, 27), (9, 14), (3, 18)]),
            },
        },
        // 26
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(9, 21), (10, 6), (20, 6), (2, 18)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(1, 29), (9, 26), (13, 19)]),
            },
        },
        // 27
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(20, 6), (15, 16), (8, 3), (4, 1)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(11, 7), (4, 12), (19, 23)]),
            },
        },
        // 28
        ShamirVariant {
            left: ShamirCase {
                p: 23,
                shares: s(&[(14, 3), (15, 19), (7, 14), (8, 20)]),
            },
            right: ShamirCase {
                p: 31,
                shares: s(&[(17, 29), (11, 1), (4, 17)]),
            },
        },
    ]
}

#[allow(clippy::too_many_lines)]
pub fn blakley_variants() -> Vec<BlakleyVariant> {
    // Q фиксированы: левая колонка p=17, Q=(15,5,4); правая p=31, Q=(11,10,25).
    let lq = SecretPoint {
        x0: 15,
        y0: 5,
        z0: 4,
    };
    let rq = SecretPoint {
        x0: 11,
        y0: 10,
        z0: 25,
    };

    // (a_A, b_A, a_B, b_B, a_D, b_D, a_C, b_C) для левой и правой колонок.
    // Данные из таблицы упражнения 3 методички.
    type Row = (i64, i64, i64, i64, i64, i64, i64, i64);
    let table: [(Row, Row); 28] = [
        // 1
        ((16, 5, 0, 1, 11, 14, 1, 5), (1, 0, 30, 0, 15, 11, 10, 0)),
        // 2
        ((12, 0, 11, 1, 2, 16, 10, 2), (15, 2, 27, 5, 12, 15, 11, 1)),
        // 3
        ((10, 1, 1, 0, 14, 3, 1, 5), (12, 0, 4, 3, 22, 12, 5, 2)),
        // 4
        ((16, 4, 1, 2, 4, 5, 3, 12), (7, 15, 15, 5, 5, 4, 5, 5)),
        // 5
        ((0, 2, 10, 12, 8, 1, 15, 0), (6, 4, 12, 7, 6, 3, 9, 8)),
        // 6
        ((2, 8, 0, 10, 3, 9, 10, 12), (1, 1, 15, 4, 22, 7, 6, 4)),
        // 7
        ((2, 6, 8, 10, 11, 8, 8, 0), (4, 2, 17, 8, 25, 11, 8, 3)),
        // 8
        ((10, 9, 10, 2, 10, 0, 11, 10), (4, 1, 15, 5, 23, 13, 7, 6)),
        // 9
        ((2, 0, 16, 14, 1, 5, 10, 1), (0, 10, 0, 6, 5, 14, 5, 9)),
        // 10
        ((11, 14, 6, 13, 0, 3, 2, 4), (10, 25, 11, 3, 14, 1, 6, 4)),
        // 11
        ((10, 7, 6, 0, 3, 8, 10, 12), (0, 15, 17, 12, 27, 5, 3, 7)),
        // 12
        ((10, 2, 1, 1, 3, 0, 14, 3), (10, 11, 15, 1, 26, 12, 2, 8)),
        // 13
        ((2, 2, 10, 0, 3, 1, 0, 10), (1, 3, 1, 6, 25, 17, 1, 5)),
        // 14
        ((11, 10, 15, 14, 11, 1, 1, 10), (6, 10, 0, 4, 2, 18, 4, 3)),
        // 15
        ((1, 1, 5, 7, 15, 4, 1, 0), (23, 17, 10, 5, 14, 19, 7, 6)),
        // 16
        ((1, 4, 7, 11, 10, 13, 16, 10), (7, 0, 9, 2, 5, 0, 8, 1)),
        // 17
        ((2, 5, 15, 0, 6, 8, 14, 9), (2, 0, 15, 8, 4, 20, 9, 0)),
        // 18
        ((10, 4, 3, 8, 9, 12, 0, 1), (9, 30, 9, 1, 8, 21, 6, 0)),
        // 19
        ((7, 4, 5, 2, 2, 11, 0, 6), (29, 11, 1, 2, 0, 4, 5, 2)),
        // 20
        ((6, 2, 12, 8, 14, 1, 12, 5), (10, 28, 2, 11, 1, 5, 0, 5)),
        // 21
        ((3, 4, 7, 10, 13, 16, 0, 10), (6, 2, 27, 0, 5, 4, 5, 8)),
        // 22
        ((7, 1, 3, 6, 0, 11, 9, 15), (10, 4, 0, 26, 5, 0, 7, 9)),
        // 23
        ((3, 2, 4, 5, 1, 9, 4, 0), (6, 4, 10, 0, 25, 6, 10, 16)),
        // 24
        ((8, 10, 12, 2, 0, 16, 1, 13), (0, 4, 4, 10, 5, 11, 17, 20)),
        // 25
        ((0, 14, 3, 11, 14, 6, 7, 15), (8, 2, 0, 4, 12, 14, 21, 10)),
        // 26
        ((2, 4, 5, 10, 7, 6, 1, 1), (17, 15, 3, 13, 18, 23, 22, 0)),
        // 27
        ((12, 8, 1, 13, 2, 16, 0, 11), (25, 2, 4, 19, 4, 24, 0, 10)),
        // 28
        ((1, 3, 6, 9, 0, 1, 15, 1), (1, 14, 15, 2, 5, 5, 10, 0)),
    ];

    table
        .iter()
        .map(|(left_row, right_row)| {
            let (la_a, la_b, lb_a, lb_b, ld_a, ld_b, lc_a, lc_b) = *left_row;
            let (ra_a, ra_b, rb_a, rb_b, rd_a, rd_b, rc_a, rc_b) = *right_row;
            BlakleyVariant {
                left_p: 17,
                left_q: lq,
                left_pairs: [(la_a, la_b), (lb_a, lb_b), (ld_a, ld_b), (lc_a, lc_b)],
                right_p: 31,
                right_q: rq,
                right_pairs: [(ra_a, ra_b), (rb_a, rb_b), (rd_a, rd_b), (rc_a, rc_b)],
            }
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn shamir_variants_have_28_entries() {
        assert_eq!(shamir_variants().len(), 28);
    }

    #[test]
    fn blakley_variants_have_28_entries() {
        assert_eq!(blakley_variants().len(), 28);
    }
}
