use std::ops::RangeInclusive;

use crate::domain::attack::{AttackError, AttackResult, break_cipher};
use crate::domain::scheme::{Alphabet, CipherError, Operation, Scheme, Vigenere};

/// Порт вывода результата: приложение не зависит от консоли.
pub trait Output {
    fn write(&mut self, text: &str) -> std::io::Result<()>;
}

pub(super) fn transform(
    alphabet: Alphabet,
    scheme: Scheme,
    key: &str,
    text: &str,
    operation: Operation,
) -> Result<String, CipherError> {
    Vigenere::new(alphabet, scheme, key)?.transform(text, operation)
}

pub(super) fn execute(
    alphabet: Alphabet,
    scheme: Scheme,
    key: &str,
    text: &str,
    operation: Operation,
    output: &mut impl Output,
) -> color_eyre::Result<()> {
    let result = transform(alphabet, scheme, key, text, operation)?;
    output.write(&result)?;
    Ok(())
}

pub(super) fn analyze(
    alphabet: Alphabet,
    scheme: Scheme,
    text: &str,
    range: RangeInclusive<usize>,
) -> Result<AttackResult, AttackError> {
    break_cipher(text, alphabet, scheme, range)
}
