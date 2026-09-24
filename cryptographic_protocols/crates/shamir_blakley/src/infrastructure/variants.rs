//! Загрузка исходных долей из таблицы 5.1 или пользовательского JSON.

use std::fs;
use std::path::Path;

use serde::Deserialize;
use thiserror::Error;

use crate::application::usecases::VariantInput;
use crate::domain::blakley::PlaneShare;
use crate::domain::shamir::Share;

const BUILTIN_DATA: &str = include_str!("../../data/variants.json");

#[derive(Debug, Error)]
pub enum InputError {
    #[error("не удалось прочитать файл входных данных: {0}")]
    Io(#[from] std::io::Error),
    #[error("ошибка формата JSON: {0}")]
    Json(#[from] serde_json::Error),
    #[error("вариант должен быть в диапазоне 1..=20, получено {0}")]
    UnknownVariant(usize),
    #[error("наборы долей Шамира и Блэкли должны содержать одинаковое ненулевое число символов")]
    InvalidSymbolCount,
}

#[derive(Deserialize)]
struct Catalog {
    variants: Vec<VariantRecord>,
}

#[derive(Deserialize)]
struct VariantRecord {
    number: Option<usize>,
    shamir: ShamirData,
    blakley: BlakleyData,
}

#[derive(Deserialize)]
struct ShamirData {
    x: [i64; 5],
    values: Vec<[i64; 5]>,
}

#[derive(Deserialize)]
struct BlakleyData {
    coefficients: [[i64; 3]; 5],
    values: Vec<[i64; 5]>,
}

pub fn load_builtin(number: usize) -> Result<VariantInput, InputError> {
    let catalog: Catalog = serde_json::from_str(BUILTIN_DATA)?;
    let record = catalog
        .variants
        .into_iter()
        .find(|record| record.number == Some(number))
        .ok_or(InputError::UnknownVariant(number))?;
    convert(record)
}

pub fn load_file(path: &Path) -> Result<VariantInput, InputError> {
    let text = fs::read_to_string(path)?;
    let record: VariantRecord = serde_json::from_str(&text)?;
    convert(record)
}

fn convert(record: VariantRecord) -> Result<VariantInput, InputError> {
    if record.shamir.values.is_empty() || record.shamir.values.len() != record.blakley.values.len()
    {
        return Err(InputError::InvalidSymbolCount);
    }
    let shamir = record
        .shamir
        .values
        .into_iter()
        .map(|values| {
            std::array::from_fn(|index| Share {
                x: record.shamir.x[index],
                y: values[index],
            })
        })
        .collect();
    let blakley = record
        .blakley
        .values
        .into_iter()
        .map(|values| {
            std::array::from_fn(|index| PlaneShare {
                coefficients: record.blakley.coefficients[index],
                value: values[index],
            })
        })
        .collect();
    Ok(VariantInput {
        number: record.number,
        shamir,
        blakley,
    })
}

#[cfg(test)]
mod tests {
    use super::load_builtin;

    #[test]
    fn all_twenty_variants_load() {
        for number in 1..=20 {
            let input = load_builtin(number).unwrap();
            assert_eq!(input.number, Some(number));
            assert_eq!(input.shamir.len(), 6);
            assert_eq!(input.blakley.len(), 6);
        }
        assert!(load_builtin(0).is_err());
        assert!(load_builtin(21).is_err());
    }
}
