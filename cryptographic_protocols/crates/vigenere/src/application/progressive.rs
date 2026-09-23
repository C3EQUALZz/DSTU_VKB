//! Сценарии прогрессивного сдвига блоков ключа.

use std::ops::RangeInclusive;

use crate::domain::attack::{AttackError, AttackResult};
use crate::domain::scheme::{Alphabet, Operation, Scheme};

use super::{Output, common};

pub fn execute(
    alphabet: Alphabet,
    key: &str,
    text: &str,
    operation: Operation,
    output: &mut impl Output,
) -> color_eyre::Result<()> {
    common::execute(alphabet, Scheme::Progressive, key, text, operation, output)
}

pub fn analyze(
    alphabet: Alphabet,
    text: &str,
    range: RangeInclusive<usize>,
) -> Result<AttackResult, AttackError> {
    common::analyze(alphabet, Scheme::Progressive, text, range)
}
