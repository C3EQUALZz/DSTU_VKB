//! Три способа построения ключевой последовательности шифра Виженера.

use shared::alphabet::ALPHABET;

const LATIN: &str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
const RUSSIAN_WITH_YO: &str = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ";

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Alphabet {
    Latin,
    RussianWithYo,
    RussianNoYo,
}

impl Alphabet {
    pub fn letters(self) -> Vec<char> {
        match self {
            Self::Latin => LATIN.chars().collect(),
            Self::RussianWithYo => RUSSIAN_WITH_YO.chars().collect(),
            Self::RussianNoYo => ALPHABET.to_vec(),
        }
    }

    pub fn index(self, ch: char) -> Option<usize> {
        let normalized = match (self, ch) {
            (Self::RussianNoYo, 'Ё' | 'ё') => 'Е',
            (_, other) => other,
        };
        self.letters().iter().position(|&letter| {
            letter == normalized || letter.to_lowercase().eq(std::iter::once(normalized))
        })
    }

    pub fn symbol(self, index: usize) -> char {
        self.letters()[index % self.size()]
    }

    pub const fn size(self) -> usize {
        match self {
            Self::Latin => 26,
            Self::RussianWithYo | Self::RussianNoYo => 33,
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Scheme {
    Standard,
    Progressive,
    Autokey,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Operation {
    Encrypt,
    Decrypt,
}

#[derive(Debug, thiserror::Error, PartialEq, Eq)]
pub enum CipherError {
    #[error("ключ не должен быть пустым")]
    EmptyKey,
    #[error("символ ключа на позиции {0} не принадлежит выбранному алфавиту")]
    InvalidKey(usize),
    #[error("буква текста на позиции {0} не принадлежит выбранному алфавиту")]
    InvalidText(usize),
}

pub struct Vigenere {
    alphabet: Alphabet,
    scheme: Scheme,
    key: Vec<usize>,
}

impl Vigenere {
    pub fn new(alphabet: Alphabet, scheme: Scheme, key: &str) -> Result<Self, CipherError> {
        if key.is_empty() {
            return Err(CipherError::EmptyKey);
        }
        let key = key
            .chars()
            .enumerate()
            .map(|(i, ch)| alphabet.index(ch).ok_or(CipherError::InvalidKey(i + 1)))
            .collect::<Result<Vec<_>, _>>()?;
        Ok(Self {
            alphabet,
            scheme,
            key,
        })
    }

    /// Знаки вне алфавита копируются без расходования ключа; чужие буквы отклоняются.
    pub fn transform(&self, text: &str, operation: Operation) -> Result<String, CipherError> {
        let n = self.alphabet.size();
        let mut position = 0;
        let mut stream = self.key.clone();
        let mut output = String::with_capacity(text.len());
        tracing::info!(?operation, ?self.scheme, ?self.alphabet, "начало преобразования");
        for (source_position, ch) in text.chars().enumerate() {
            let Some(value) = self.alphabet.index(ch) else {
                if ch.is_alphabetic() {
                    return Err(CipherError::InvalidText(source_position + 1));
                }
                output.push(ch);
                continue;
            };
            let slot = position % self.key.len();
            let block = position / self.key.len();
            let shift = match self.scheme {
                Scheme::Standard => self.key[slot],
                Scheme::Progressive => (self.key[slot] + block % n) % n,
                Scheme::Autokey => stream[slot],
            };
            let result = match operation {
                Operation::Encrypt => (value + shift) % n,
                Operation::Decrypt => (value + n - shift) % n,
            };
            if self.scheme == Scheme::Autokey {
                stream[slot] = match operation {
                    Operation::Encrypt => value,
                    Operation::Decrypt => result,
                };
            }
            tracing::info!(position, block, shift, "обработка символа");
            let letter = self.alphabet.symbol(result);
            if ch.is_lowercase() && self.alphabet != Alphabet::RussianNoYo {
                output.extend(letter.to_lowercase());
            } else {
                output.push(letter);
            }
            position += 1;
        }
        Ok(output)
    }
}
