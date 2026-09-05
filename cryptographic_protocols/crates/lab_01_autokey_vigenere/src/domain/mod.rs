//! Ключ продолжается буквами открытого текста; при расшифровании — восстановленными.

#[derive(Clone, Copy)]
pub enum Alphabet {
    Latin,
    Russian,
}

impl Alphabet {
    pub fn letters(self) -> &'static str {
        match self {
            Self::Latin => "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            Self::Russian => "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
        }
    }
}

#[derive(Clone, Copy, Debug)]
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

pub struct AutokeyVigenere {
    letters: Vec<char>,
    key: Vec<usize>,
}

fn index(letters: &[char], ch: char) -> Option<usize> {
    letters
        .iter()
        .position(|&letter| letter == ch || letter.to_lowercase().eq(std::iter::once(ch)))
}

impl AutokeyVigenere {
    pub fn new(alphabet: Alphabet, key: &str) -> Result<Self, CipherError> {
        if key.is_empty() {
            return Err(CipherError::EmptyKey);
        }
        let letters: Vec<_> = alphabet.letters().chars().collect();
        let key = key
            .chars()
            .enumerate()
            .map(|(i, ch)| index(&letters, ch).ok_or(CipherError::InvalidKey(i + 1)))
            .collect::<Result<Vec<_>, _>>()?;
        Ok(Self { letters, key })
    }

    /// Регистр сохраняется. Не-буквы копируются и не расходуют ключ.
    /// Буквы чужого алфавита отклоняются, чтобы избежать частичного шифрования.
    pub fn transform(&self, text: &str, operation: Operation) -> Result<String, CipherError> {
        let n = self.letters.len();
        let mut position = 0;
        // Кольцевой буфер хранит последние L букв открытого текста.
        let mut stream = self.key.clone();
        let mut output = String::with_capacity(text.len());
        tracing::info!(?operation, "начало преобразования");
        for (source_position, ch) in text.chars().enumerate() {
            let Some(value) = index(&self.letters, ch) else {
                if ch.is_alphabetic() {
                    return Err(CipherError::InvalidText(source_position + 1));
                }
                output.push(ch);
                continue;
            };
            let slot = position % stream.len();
            let shift = stream[slot];
            let result = match operation {
                Operation::Encrypt => (value + shift) % n,
                Operation::Decrypt => (value + n - shift) % n,
            };
            stream[slot] = match operation {
                Operation::Encrypt => value,
                Operation::Decrypt => result,
            };
            tracing::info!(position, "обработка буквы");
            let letter = self.letters[result];
            if ch.is_lowercase() {
                output.extend(letter.to_lowercase());
            } else {
                output.push(letter);
            }
            position += 1;
        }
        Ok(output)
    }
}
