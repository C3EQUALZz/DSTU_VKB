use std::collections::BTreeMap;
use std::fmt;

use super::{Error, PrimeField};

/// Ограничения затратных учебных операций, не арифметики точек.
pub const MAX_ENUM_MODULUS: u64 = 10_000;
pub const MAX_WALK_STEPS: u64 = 100_000;
pub const MAX_TABLE_POINTS: usize = 32;

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum Point {
    Infinity,
    Affine { x: u64, y: u64 },
}

impl fmt::Display for Point {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Infinity => f.write_str("O"),
            Self::Affine { x, y } => write!(f, "({x}, {y})"),
        }
    }
}

#[derive(Clone, Copy, Debug)]
pub struct Curve {
    field: PrimeField,
    a: u64,
    b: u64,
}

#[derive(Debug, PartialEq, Eq)]
pub struct EcdhResult {
    pub order: u64,
    pub public_a: Point,
    pub public_b: Point,
    pub shared_a: Point,
    pub shared_b: Point,
}

impl Curve {
    pub fn new(modulus: u64, a: i128, b: i128) -> Result<Self, Error> {
        let field = PrimeField::new(modulus)?;
        let a = field.normalize(a);
        let b = field.normalize(b);
        if field.add(
            field.mul(4, field.pow(a, 3)),
            field.mul(27, field.pow(b, 2)),
        ) == 0
        {
            return Err(Error::SingularCurve);
        }
        Ok(Self { field, a, b })
    }

    pub fn field(self) -> PrimeField {
        self.field
    }

    pub fn coefficients(self) -> (u64, u64) {
        (self.a, self.b)
    }

    /// Нормализует координаты; принадлежность проверяют вычисляющие операции.
    pub fn point(self, x: i128, y: i128) -> Point {
        Point::Affine {
            x: self.field.normalize(x),
            y: self.field.normalize(y),
        }
    }

    fn rhs(self, x: u64) -> u64 {
        self.field.add(
            self.field
                .add(self.field.pow(x, 3), self.field.mul(self.a, x)),
            self.b,
        )
    }

    pub fn contains(self, point: Point) -> bool {
        match point {
            Point::Infinity => true,
            Point::Affine { x, y } => {
                x < self.field.modulus()
                    && y < self.field.modulus()
                    && self.field.mul(y, y) == self.rhs(x)
            }
        }
    }

    pub fn validate(self, point: Point) -> Result<(), Error> {
        if self.contains(point) {
            Ok(())
        } else {
            Err(Error::InvalidPoint(point))
        }
    }

    pub fn negate(self, point: Point) -> Result<Point, Error> {
        self.validate(point)?;
        Ok(self.negate_valid(point))
    }

    fn negate_valid(self, point: Point) -> Point {
        match point {
            Point::Infinity => point,
            Point::Affine { x, y } => Point::Affine {
                x,
                y: self.field.sub(0, y),
            },
        }
    }

    pub fn add(self, left: Point, right: Point) -> Result<Point, Error> {
        self.validate(left)?;
        self.validate(right)?;
        self.add_valid(left, right)
    }

    fn add_valid(self, left: Point, right: Point) -> Result<Point, Error> {
        let (Point::Affine { x: x1, y: y1 }, Point::Affine { x: x2, y: y2 }) = (left, right) else {
            return Ok(if left == Point::Infinity { right } else { left });
        };
        let f = self.field;
        if x1 == x2 && f.add(y1, y2) == 0 {
            return Ok(Point::Infinity);
        }
        let (numerator, denominator) = if left == right {
            (f.add(f.mul(3, f.mul(x1, x1)), self.a), f.mul(2, y1))
        } else {
            (f.sub(y2, y1), f.sub(x2, x1))
        };
        let slope = f.mul(numerator, f.inverse(denominator)?);
        let x3 = f.sub(f.sub(f.mul(slope, slope), x1), x2);
        let y3 = f.sub(f.mul(slope, f.sub(x1, x3)), y1);
        Ok(Point::Affine { x: x3, y: y3 })
    }

    pub fn subtract(self, left: Point, right: Point) -> Result<Point, Error> {
        self.add(left, self.negate(right)?)
    }

    /// Двоичный double-and-add; unsigned_abs корректен даже для i128::MIN.
    pub fn multiply(self, point: Point, scalar: i128) -> Result<Point, Error> {
        self.validate(point)?;
        let mut base = if scalar < 0 {
            self.negate_valid(point)
        } else {
            point
        };
        let mut bits = scalar.unsigned_abs();
        let mut result = Point::Infinity;
        while bits != 0 {
            if bits & 1 != 0 {
                result = self.add_valid(result, base)?;
            }
            bits >>= 1;
            if bits != 0 {
                base = self.add_valid(base, base)?;
            }
        }
        Ok(result)
    }

    /// Все точки в порядке O, затем лексикографически (x,y).
    /// Таблица квадратов позволяет избежать вложенного перебора x и y.
    pub fn points(self) -> Result<Vec<Point>, Error> {
        let modulus = self.field.modulus();
        if modulus > MAX_ENUM_MODULUS {
            return Err(Error::EnumerationLimit);
        }
        let mut roots: BTreeMap<u64, Vec<u64>> = BTreeMap::new();
        for y in 0..modulus {
            roots.entry(self.field.mul(y, y)).or_default().push(y);
        }
        let mut points = vec![Point::Infinity];
        for x in 0..modulus {
            if let Some(ys) = roots.get(&self.rhs(x)) {
                points.extend(ys.iter().map(|&y| Point::Affine { x, y }));
            }
        }
        Ok(points)
    }

    pub fn order(self, point: Point) -> Result<u64, Error> {
        self.validate(point)?;
        let mut current = Point::Infinity;
        for order in 1..=MAX_WALK_STEPS {
            current = self.add_valid(current, point)?;
            if current == Point::Infinity {
                return Ok(order);
            }
        }
        Err(Error::WalkLimit)
    }

    pub fn subgroup(self, point: Point) -> Result<Vec<Point>, Error> {
        let order = self.order(point)?;
        let mut current = Point::Infinity;
        let mut points = Vec::new();
        for _ in 0..order {
            points.push(current);
            current = self.add_valid(current, point)?;
        }
        Ok(points)
    }

    pub fn addition_table(self) -> Result<(Vec<Point>, Vec<Vec<Point>>), Error> {
        let points = self.points()?;
        if points.len() > MAX_TABLE_POINTS {
            return Err(Error::TableLimit(points.len()));
        }
        let rows = points
            .iter()
            .map(|&p| points.iter().map(|&q| self.add_valid(p, q)).collect())
            .collect::<Result<Vec<_>, Error>>()?;
        Ok((points, rows))
    }

    pub fn discrete_log(self, base: Point, target: Point) -> Result<u64, Error> {
        self.validate(base)?;
        self.validate(target)?;
        let mut current = Point::Infinity;
        for scalar in 0..MAX_WALK_STEPS {
            if current == target {
                return Ok(scalar);
            }
            current = self.add_valid(current, base)?;
            if current == Point::Infinity {
                return Err(Error::NoDiscreteLog);
            }
        }
        Err(Error::WalkLimit)
    }

    pub fn ecdh(self, generator: Point, secret_a: u64, secret_b: u64) -> Result<EcdhResult, Error> {
        let order = self.order(generator)?;
        if generator == Point::Infinity
            || secret_a == 0
            || secret_b == 0
            || secret_a >= order
            || secret_b >= order
        {
            return Err(Error::InvalidEcdh);
        }
        let public_a = self.multiply(generator, i128::from(secret_a))?;
        let public_b = self.multiply(generator, i128::from(secret_b))?;
        let shared_a = self.multiply(public_b, i128::from(secret_a))?;
        let shared_b = self.multiply(public_a, i128::from(secret_b))?;
        if shared_a == Point::Infinity {
            return Err(Error::InvalidEcdh);
        }
        Ok(EcdhResult {
            order,
            public_a,
            public_b,
            shared_a,
            shared_b,
        })
    }
}
