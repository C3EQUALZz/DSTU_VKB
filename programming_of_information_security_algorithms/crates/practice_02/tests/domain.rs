use practice_02::domain::{Curve, Error, Point, PrimeField, is_prime};
use proptest::prelude::*;

fn curve() -> Curve {
    Curve::new(17, 2, 2).unwrap()
}

fn generator() -> Point {
    Point::Affine { x: 5, y: 1 }
}

#[test]
fn multiples_match_hand_computed_vector() {
    let c = curve();
    // Ручная таблица последовательного прибавления (5,1) на E17(2,2).
    let coordinates = [
        (5, 1),
        (6, 3),
        (10, 6),
        (3, 1),
        (9, 16),
        (16, 13),
        (0, 6),
        (13, 7),
        (7, 6),
        (7, 11),
        (13, 10),
        (0, 11),
        (16, 4),
        (9, 1),
        (3, 16),
        (10, 11),
        (6, 14),
        (5, 16),
    ];
    assert_eq!(c.multiply(generator(), 0).unwrap(), Point::Infinity);
    for (index, (x, y)) in coordinates.into_iter().enumerate() {
        assert_eq!(
            c.multiply(generator(), (index + 1) as i128).unwrap(),
            c.point(x, y)
        );
    }
    assert_eq!(c.multiply(generator(), 19).unwrap(), Point::Infinity);
}

#[test]
fn singular_and_composite_parameters_are_rejected() {
    for p in [0, 1, 2, 3, 4, 9, 15, 341, 561] {
        assert!(matches!(Curve::new(p, 2, 2), Err(Error::InvalidModulus(_))));
    }
    assert!(matches!(Curve::new(17, 0, 0), Err(Error::SingularCurve)));
    assert!(matches!(Curve::new(17, -3, 2), Err(Error::SingularCurve)));
}

#[test]
fn primality_matches_trial_division_and_rejects_pseudoprimes() {
    for n in 0..10_000 {
        let expected = n >= 2 && !(2..=n).take_while(|d| d * d <= n).any(|d| n % d == 0);
        assert_eq!(is_prime(n), expected, "n={n}");
    }
    for n in [
        561,
        1105,
        1729,
        3_215_031_751,
        341_550_071_728_321,
        3_825_123_056_546_413_051,
        u64::MAX,
    ] {
        assert!(!is_prime(n), "n={n}");
    }
    assert!(is_prime(18_446_744_073_709_551_557));
}

#[test]
fn field_operations_do_not_overflow_at_u64_boundary() {
    let p = 18_446_744_073_709_551_557;
    let f = PrimeField::new(p).unwrap();
    assert_eq!(f.add(p - 1, p - 1), p - 2);
    assert_eq!(f.mul(p - 1, p - 1), 1);
    assert_eq!(f.sub(0, p - 1), 1);
    assert_eq!(f.inverse(p - 1).unwrap(), p - 1);
    assert_eq!(f.inverse(0), Err(Error::ZeroInverse));
    assert_eq!(f.inverse(p), Err(Error::ZeroInverse));
    assert_eq!(f.normalize(-1), p - 1);
}

#[test]
fn signed_input_and_minimum_scalar_are_supported() {
    let c = curve();
    assert_eq!(c.point(-12, 18), generator());
    assert_eq!(
        c.coefficients(),
        Curve::new(17, -15, 19).unwrap().coefficients()
    );
    assert_eq!(c.multiply(generator(), -1).unwrap(), c.point(5, 16));
    assert_eq!(
        c.multiply(generator(), i128::MIN).unwrap(),
        c.multiply(generator(), i128::MIN.rem_euclid(19)).unwrap()
    );
    assert_eq!(
        c.multiply(generator(), i128::MAX).unwrap(),
        c.multiply(generator(), i128::MAX % 19).unwrap()
    );
}

#[test]
fn invalid_points_are_checked_even_for_zero_scalars() {
    let c = curve();
    let bad = c.point(1, 1);
    let noncanonical = Point::Affine { x: 22, y: 1 };
    for p in [bad, noncanonical] {
        assert!(!c.contains(p));
        assert_eq!(c.multiply(p, 0), Err(Error::InvalidPoint(p)));
        assert_eq!(c.add(p, Point::Infinity), Err(Error::InvalidPoint(p)));
        assert_eq!(c.negate(p), Err(Error::InvalidPoint(p)));
        assert_eq!(c.order(p), Err(Error::InvalidPoint(p)));
    }
}

#[test]
fn infinity_inverse_and_vertical_tangent() {
    let c = curve();
    assert_eq!(c.add(Point::Infinity, generator()).unwrap(), generator());
    assert_eq!(c.add(generator(), Point::Infinity).unwrap(), generator());
    assert_eq!(
        c.add(Point::Infinity, Point::Infinity).unwrap(),
        Point::Infinity
    );
    assert_eq!(
        c.subtract(generator(), generator()).unwrap(),
        Point::Infinity
    );
    assert_eq!(c.negate(Point::Infinity).unwrap(), Point::Infinity);
    assert_eq!(c.order(Point::Infinity).unwrap(), 1);
    assert_eq!(c.subgroup(Point::Infinity).unwrap(), vec![Point::Infinity]);
    let c = Curve::new(5, 1, 0).unwrap();
    assert_eq!(
        c.add(c.point(0, 0), c.point(0, 0)).unwrap(),
        Point::Infinity
    );
}

#[test]
fn enumeration_matches_independent_exhaustive_equation_check() {
    for p in [5, 7, 11, 17, 23] {
        for (a, b) in [(0, 1), (1, 0), (2, 2), (-1, 3)] {
            let Ok(c) = Curve::new(p, a, b) else { continue };
            let mut expected = vec![Point::Infinity];
            for x in 0..p {
                for y in 0..p {
                    let rhs =
                        (i128::from(x).pow(3) + a * i128::from(x) + b).rem_euclid(i128::from(p));
                    if i128::from(y * y % p) == rhs {
                        expected.push(Point::Affine { x, y });
                    }
                }
            }
            let points = c.points().unwrap();
            assert_eq!(points, expected);
            let size = points.len() as u64;
            let distance = i128::from(size) - i128::from(p) - 1;
            assert!(distance * distance <= 4 * i128::from(p));
            for point in points {
                assert_eq!(size % c.order(point).unwrap(), 0);
            }
        }
    }
}

#[test]
fn exhaustive_associativity_on_demo_group() {
    let c = curve();
    let points = c.points().unwrap();
    assert_eq!(points.len(), 19);
    for &p in &points {
        for &q in &points {
            for &r in &points {
                assert_eq!(
                    c.add(c.add(p, q).unwrap(), r).unwrap(),
                    c.add(p, c.add(q, r).unwrap()).unwrap()
                );
            }
        }
    }
}

#[test]
fn cyclic_subgroup_and_discrete_log() {
    let c = curve();
    assert_eq!(c.order(generator()).unwrap(), 19);
    let subgroup = c.subgroup(generator()).unwrap();
    assert_eq!(subgroup.len(), 19);
    for (k, &point) in subgroup.iter().enumerate() {
        assert_eq!(c.discrete_log(generator(), point).unwrap(), k as u64);
    }
    let c = Curve::new(5, 1, 0).unwrap();
    assert_eq!(
        c.discrete_log(c.point(0, 0), c.point(2, 0)),
        Err(Error::NoDiscreteLog)
    );
    assert_eq!(
        c.discrete_log(Point::Infinity, c.point(0, 0)),
        Err(Error::NoDiscreteLog)
    );
    assert_eq!(c.discrete_log(Point::Infinity, Point::Infinity).unwrap(), 0);
}

#[test]
fn addition_table_has_identity_and_is_symmetric() {
    let c = Curve::new(5, 1, 0).unwrap();
    let (points, rows) = c.addition_table().unwrap();
    assert_eq!(points.len(), 4);
    for i in 0..points.len() {
        assert_eq!(rows[0][i], points[i]);
        assert_eq!(rows[i][0], points[i]);
        for j in 0..points.len() {
            assert_eq!(rows[i][j], rows[j][i]);
            assert!(points.contains(&rows[i][j]));
        }
    }
}

#[test]
fn expensive_operations_have_explicit_limits() {
    let c = Curve::new(10_007, 2, 2).unwrap();
    assert_eq!(c.points(), Err(Error::EnumerationLimit));
    let c = Curve::new(101, 2, 2).unwrap();
    assert!(matches!(c.addition_table(), Err(Error::TableLimit(_))));
    // Обычная арифметика не ограничена p ≤ 10000.
    let c = Curve::new(18_446_744_073_709_551_557, 1, 1).unwrap();
    let p = c.point(0, 1);
    assert!(c.contains(c.multiply(p, i128::MAX).unwrap()));
}

#[test]
fn ecdh_known_example_and_invalid_secrets() {
    let c = curve();
    let r = c.ecdh(generator(), 5, 7).unwrap();
    assert_eq!(r.order, 19);
    assert_eq!(r.public_a, c.point(9, 16));
    assert_eq!(r.public_b, c.point(0, 6));
    assert_eq!(r.shared_a, c.point(10, 11));
    assert_eq!(r.shared_a, r.shared_b);
    for (a, b) in [(0, 7), (5, 0), (19, 7), (5, 19)] {
        assert_eq!(c.ecdh(generator(), a, b), Err(Error::InvalidEcdh));
    }
    assert_eq!(c.ecdh(Point::Infinity, 1, 1), Err(Error::InvalidEcdh));
}

proptest! {
    #[test]
    fn scalar_distributivity(k in -100_000i128..100_000, m in -100_000i128..100_000) {
        let c = curve();
        let left = c.multiply(generator(), k + m).unwrap();
        let right = c.add(c.multiply(generator(), k).unwrap(), c.multiply(generator(), m).unwrap()).unwrap();
        prop_assert_eq!(left, right);
    }

    #[test]
    fn scalar_composition(k in -1000i128..1000, m in -1000i128..1000) {
        let c = curve();
        prop_assert_eq!(c.multiply(c.multiply(generator(), k).unwrap(), m).unwrap(), c.multiply(generator(), k * m).unwrap());
    }

    #[test]
    fn inverse_and_closure(k in 0i128..19, m in 0i128..19) {
        let c = curve();
        let p = c.multiply(generator(), k).unwrap();
        let q = c.multiply(generator(), m).unwrap();
        prop_assert!(c.contains(c.add(p, q).unwrap()));
        prop_assert_eq!(c.subtract(c.add(p, q).unwrap(), q).unwrap(), p);
        prop_assert_eq!(c.add(p, c.negate(p).unwrap()).unwrap(), Point::Infinity);
        prop_assert_eq!(c.add(p, q).unwrap(), c.add(q, p).unwrap());
    }

    #[test]
    fn field_inverse_for_any_nonzero_u64_residue(value in 1u64..18_446_744_073_709_551_557) {
        let f = PrimeField::new(18_446_744_073_709_551_557).unwrap();
        prop_assert_eq!(f.mul(value, f.inverse(value).unwrap()), 1);
    }
}
