//! Сценарии лаб 5.

use tracing::info;

use crate::domain::xor::xor_stream;

/// Результат операции XOR: входной текст, ключ, выход и hex-представление.
#[derive(Debug, Clone)]
pub struct XorReport {
    pub input: Vec<u8>,
    pub key: Vec<u8>,
    pub output: Vec<u8>,
}

impl XorReport {
    pub fn output_hex(&self) -> String {
        self.output
            .iter()
            .map(|b| format!("{b:02X}"))
            .collect::<Vec<_>>()
            .join(" ")
    }

    pub fn output_decimal(&self) -> String {
        self.output
            .iter()
            .map(u8::to_string)
            .collect::<Vec<_>>()
            .join(" ")
    }
}

/// Применить XOR. Возвращает байтовый поток. Шифр и дешифр — одно и то же.
pub fn xor_apply(input: &[u8], key: &[u8]) -> XorReport {
    let output = xor_stream(input, key);
    info!(input_len = input.len(), key_len = key.len(), "XOR применён");
    XorReport {
        input: input.to_vec(),
        key: key.to_vec(),
        output,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn xor_roundtrip() {
        let plaintext = b"hello, world";
        let key = b"KEY";
        let enc = xor_apply(plaintext, key);
        let dec = xor_apply(&enc.output, key);
        assert_eq!(dec.output, plaintext);
    }
}
