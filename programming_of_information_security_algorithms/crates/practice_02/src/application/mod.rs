//! Сценарии калькулятора и формирование результатов для представления.

use crate::domain::{Curve, Error, Point};

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum PointInput {
    Infinity,
    Affine(i128, i128),
}

impl PointInput {
    fn resolve(self, curve: Curve) -> Point {
        match self {
            Self::Infinity => Point::Infinity,
            Self::Affine(x, y) => curve.point(x, y),
        }
    }
}

/// Типизированный запрос; входные точки нормализуются по модулю поля.
#[derive(Clone, Copy, Debug)]
pub enum Operation {
    Info,
    Check(PointInput),
    Neg(PointInput),
    Add(PointInput, PointInput),
    Sub(PointInput, PointInput),
    Double(PointInput),
    Mul(i128, PointInput),
    Linear(i128, PointInput, i128, PointInput),
    Points,
    Count,
    Order(PointInput),
    Subgroup(PointInput),
    Table,
    Dlog(PointInput, PointInput),
    Ecdh(PointInput, u64, u64),
    Inverse(i128),
}

impl Operation {
    fn name(self) -> &'static str {
        match self {
            Self::Info => "info",
            Self::Check(_) => "check",
            Self::Neg(_) => "neg",
            Self::Add(..) => "add",
            Self::Sub(..) => "sub",
            Self::Double(_) => "double",
            Self::Mul(..) => "mul",
            Self::Linear(..) => "linear",
            Self::Points => "points",
            Self::Count => "count",
            Self::Order(_) => "order",
            Self::Subgroup(_) => "subgroup",
            Self::Table => "table",
            Self::Dlog(..) => "dlog",
            Self::Ecdh(..) => "ecdh",
            Self::Inverse(_) => "inverse",
        }
    }
}

pub struct Calculator {
    curve: Curve,
}

impl Calculator {
    pub fn new(modulus: u64, a: i128, b: i128) -> Result<Self, Error> {
        let curve = Curve::new(modulus, a, b)?;
        tracing::debug!(modulus, "параметры кривой проверены");
        Ok(Self { curve })
    }

    pub fn description(&self) -> String {
        let (a, b) = self.curve.coefficients();
        format!(
            "E: y² = x³ + {a}x + {b} (mod {})",
            self.curve.field().modulus()
        )
    }

    pub fn execute(&self, operation: Operation) -> Result<Vec<String>, Error> {
        let name = operation.name();
        tracing::info!(operation = name, "начало вычисления");
        let result = self.calculate(operation);
        match &result {
            Ok(lines) => tracing::info!(
                operation = name,
                lines = lines.len(),
                "вычисление завершено"
            ),
            Err(error) => tracing::warn!(operation = name, %error, "вычисление отклонено"),
        }
        result
    }

    fn calculate(&self, operation: Operation) -> Result<Vec<String>, Error> {
        let c = self.curve;
        let point = |input: PointInput| input.resolve(c);
        let line = match operation {
            Operation::Info => return Ok(self.info()),
            Operation::Check(input) => {
                let p = point(input);
                format!("P = {p}; принадлежит кривой: {}", c.contains(p))
            }
            Operation::Neg(input) => {
                let p = point(input);
                format!("−{p} = {}", c.negate(p)?)
            }
            Operation::Add(left, right) => {
                let (p, q) = (point(left), point(right));
                format!("{p} + {q} = {}", c.add(p, q)?)
            }
            Operation::Sub(left, right) => {
                let (p, q) = (point(left), point(right));
                format!("{p} − {q} = {}", c.subtract(p, q)?)
            }
            Operation::Double(input) => {
                let p = point(input);
                format!("2 × {p} = {}", c.add(p, p)?)
            }
            Operation::Mul(k, input) => {
                let p = point(input);
                format!("{k} × {p} = {}", c.multiply(p, k)?)
            }
            Operation::Linear(k, left, m, right) => {
                let (p, q) = (point(left), point(right));
                let sum = c.add(c.multiply(p, k)?, c.multiply(q, m)?)?;
                format!("{k} × {p} + {m} × {q} = {sum}")
            }
            Operation::Points => {
                let points = c.points()?;
                let mut lines = vec![format!("#E(Fp) = {} (включая O)", points.len())];
                lines.extend(
                    points
                        .iter()
                        .enumerate()
                        .map(|(i, p)| format!("{i:>5}: {p}")),
                );
                return Ok(lines);
            }
            Operation::Count => format!("#E(Fp) = {} (включая O)", c.points()?.len()),
            Operation::Order(input) => {
                let p = point(input);
                format!("ord({p}) = {}", c.order(p)?)
            }
            Operation::Subgroup(input) => {
                let p = point(input);
                let points = c.subgroup(p)?;
                let mut lines = vec![format!("⟨{p}⟩: порядок {}", points.len())];
                lines.extend(
                    points
                        .iter()
                        .enumerate()
                        .map(|(k, q)| format!("{k:>5}P = {q}")),
                );
                return Ok(lines);
            }
            Operation::Table => return self.table(),
            Operation::Dlog(base, target) => {
                let (p, q) = (point(base), point(target));
                format!(
                    "{q} = k × {p}; k = {} (минимальное k ≥ 0)",
                    c.discrete_log(p, q)?
                )
            }
            Operation::Ecdh(base, a, b) => return self.ecdh(point(base), a, b),
            Operation::Inverse(value) => {
                let f = c.field();
                let v = f.normalize(value);
                format!("{v}⁻¹ mod {} = {}", f.modulus(), f.inverse(v)?)
            }
        };
        Ok(vec![line])
    }

    fn info(&self) -> Vec<String> {
        let (a, b) = self.curve.coefficients();
        let f = self.curve.field();
        let discriminant = f.sub(
            0,
            f.mul(16, f.add(f.mul(4, f.pow(a, 3)), f.mul(27, f.pow(b, 2)))),
        );
        vec![
            format!("p = {} — простое; a = {a}; b = {b}", f.modulus()),
            format!("Δ = −16(4a³ + 27b²) mod p = {discriminant} ≠ 0"),
            "Точка O — нейтральный элемент. Координаты нормализуются mod p.".into(),
            "Перебор: p ≤ 10000; порядок/dlog: ≤ 100000 сложений; таблица: ≤ 32 точки.".into(),
        ]
    }

    fn table(&self) -> Result<Vec<String>, Error> {
        let (points, rows) = self.curve.addition_table()?;
        let mut lines = vec!["Обозначения элементов группы:".to_owned()];
        lines.extend(
            points
                .iter()
                .enumerate()
                .map(|(i, p)| format!("P{i} = {p}")),
        );
        lines.push(format!(
            "   + | {}",
            (0..points.len())
                .map(|i| format!("{i:>3}"))
                .collect::<Vec<_>>()
                .join(" ")
        ));
        for (i, row) in rows.iter().enumerate() {
            let cells = row
                .iter()
                .map(|p| {
                    // Публичный список получен из той же группы; отсутствие — нарушение инварианта.
                    points
                        .iter()
                        .position(|q| q == p)
                        .map_or_else(|| "  ?".into(), |j| format!("{j:>3}"))
                })
                .collect::<Vec<_>>()
                .join(" ");
            lines.push(format!("{i:>4} | {cells}"));
        }
        lines.push("Число j в ячейке означает Pj; строка i + столбец k = Pj.".into());
        Ok(lines)
    }

    fn ecdh(&self, base: Point, secret_a: u64, secret_b: u64) -> Result<Vec<String>, Error> {
        let r = self.curve.ecdh(base, secret_a, secret_b)?;
        Ok(vec![
            "Учебная демонстрация ECDH (заданные скаляры, без генерации ключей).".into(),
            format!("G = {base}; ord(G) = {}", r.order),
            format!("A = aG = {}; B = bG = {}", r.public_a, r.public_b),
            format!("Sₐ = aB = {}; Sᵦ = bA = {}", r.shared_a, r.shared_b),
            format!("Совпадение общих точек: {}", r.shared_a == r.shared_b),
            "Результат — общая точка; получение сеансового ключа через KDF здесь не выполняется."
                .into(),
        ])
    }
}
