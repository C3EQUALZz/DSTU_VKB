//! XOR-шифрование байтового потока с циклическим ключом.
//!
//! Шифрование и дешифрование — одна и та же операция (симметричный шифр,
//! инволюция): `encrypt(encrypt(p)) == p`.

/// Поток-в-поток XOR с ключом `key` (повторяется циклически).
///
/// Если `key.is_empty()` — поведение бесполезное, поэтому в CLI всегда
/// гарантируется хотя бы один байт ключа.
pub fn xor_stream(data: &[u8], key: &[u8]) -> Vec<u8> {
    if key.is_empty() {
        tracing::info!(
            step = "xor.empty_key",
            "пустой ключ: данные возвращены без изменений"
        );
        return data.to_vec();
    }
    data.iter()
        .zip(key.iter().cycle())
        .enumerate()
        .map(|(i, (d, k))| {
            let output = d ^ k;
            tracing::info!(
                step = "xor.byte",
                position = i + 1,
                key_position = i % key.len() + 1,
                output = output,
                "вычислено output = input XOR key; байт ключа скрыт"
            );
            output
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn xor_is_involution() {
        let plaintext = "Ночь, улица, фонарь, аптека".as_bytes();
        let key = &[70u8];
        let cipher = xor_stream(plaintext, key);
        let decrypted = xor_stream(&cipher, key);
        assert_eq!(decrypted, plaintext);
    }

    #[test]
    fn xor_with_multi_byte_key() {
        let plaintext = b"ABCDEFG";
        let key = b"XY";
        let cipher = xor_stream(plaintext, key);
        assert_eq!(xor_stream(&cipher, key), plaintext);
    }

    #[test]
    fn xor_empty_key_is_identity() {
        assert_eq!(xor_stream(b"abc", b""), b"abc");
    }

    #[test]
    fn methodichka_example_first_byte() {
        // По примеру методички (стих Блока, ключ K=70=0x46).
        // 'Н' в Win-1251 = 0xCD = 205. 205 ^ 70 = 139.
        let p = [205u8];
        assert_eq!(xor_stream(&p, &[70u8]), vec![139u8]);
    }
}
