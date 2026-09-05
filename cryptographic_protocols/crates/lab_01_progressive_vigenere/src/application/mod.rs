use crate::domain::{Alphabet, Operation, ProgressiveVigenere};

/// Порт вывода результата: CLI не определяет способ записи.
pub trait Output {
    fn write(&mut self, text: &str) -> std::io::Result<()>;
}

pub fn execute(
    alphabet: Alphabet,
    key: &str,
    text: &str,
    operation: Operation,
    output: &mut impl Output,
) -> color_eyre::Result<()> {
    let cipher = ProgressiveVigenere::new(alphabet, key)?;
    let result = cipher.transform(text, operation)?;
    output.write(&result)?;
    Ok(())
}
