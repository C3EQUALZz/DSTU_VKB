use vigenere::domain::attack::break_cipher;
use vigenere::domain::scheme::{Alphabet, Operation, Scheme, Vigenere};

#[test]
fn recovers_lab_four_key_from_original_ciphertext() {
    let cipher = include_str!("../../../artifacts/lab_04_vigenere/cipher_texts/var_11.txt");
    let result = break_cipher(
        cipher.trim(),
        Alphabet::RussianNoYo,
        Scheme::Standard,
        2..=8,
    )
    .unwrap();
    assert_eq!(result.key, "ДВОР");
    assert!(result.plain.starts_with("ВАСИЛИСА_ЕГОРОВНА"));
}

#[test]
fn recovers_progressive_and_autokey_on_long_russian_text() {
    let plain: String = include_str!("../../../artifacts/lab_04_vigenere/var_11/plaintext.txt")
        .chars()
        .take(800)
        .collect();
    for scheme in [Scheme::Progressive, Scheme::Autokey] {
        let cipher = Vigenere::new(Alphabet::RussianNoYo, scheme, "КЛЮЧ")
            .unwrap()
            .transform(&plain, Operation::Encrypt)
            .unwrap();
        let result = break_cipher(&cipher, Alphabet::RussianNoYo, scheme, 2..=8).unwrap();
        assert_eq!(result.key, "КЛЮЧ");
        assert_eq!(result.plain, plain);
    }
}

#[test]
fn recovers_all_schemes_for_english_and_russian_with_yo() {
    // Проверочные тексты не входят в языковую модель: Dickens, Project Gutenberg #98,
    // и отдельный русский текст из docs/explanations/LOGGING.md.
    for (alphabet, key, plain) in [
        (
            Alphabet::Latin,
            "LEMON",
            include_str!("fixtures/english_dickens.txt").trim(),
        ),
        (
            Alphabet::RussianWithYo,
            "КЛЮЧ",
            include_str!("fixtures/russian_logging.txt").trim(),
        ),
    ] {
        for scheme in [Scheme::Standard, Scheme::Progressive, Scheme::Autokey] {
            let cipher = Vigenere::new(alphabet, scheme, key)
                .unwrap()
                .transform(plain, Operation::Encrypt)
                .unwrap();
            let result = break_cipher(&cipher, alphabet, scheme, 2..=8).unwrap();
            assert_eq!(result.key, key, "{scheme:?} {alphabet:?}");
            assert_eq!(result.plain, plain, "{scheme:?} {alphabet:?}");
        }
    }
}
