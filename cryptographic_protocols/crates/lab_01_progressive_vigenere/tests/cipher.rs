use lab_01_progressive_vigenere::domain::{Alphabet, CipherError, Operation, ProgressiveVigenere};
use proptest::prelude::*;

#[test]
fn assignment_example() {
    let cipher = ProgressiveVigenere::new(Alphabet::Latin, "MODE").unwrap();
    assert_eq!(
        cipher
            .transform("CRYPTOGRAPHY", Operation::Encrypt)
            .unwrap(),
        "OFBTGDKWOFME"
    );
    assert_eq!(
        cipher
            .transform("OFBTGDKWOFME", Operation::Decrypt)
            .unwrap(),
        "CRYPTOGRAPHY"
    );
}

#[test]
fn russian_example() {
    let cipher = ProgressiveVigenere::new(Alphabet::Russian, "КЛЮЧ").unwrap();
    assert_eq!(
        cipher
            .transform("КРИПТОГРАФИЯ", Operation::Encrypt)
            .unwrap(),
        "ХЬЖЖЮЫВИМВИШ"
    );
}

#[test]
fn case_punctuation_and_wrap() {
    let cipher = ProgressiveVigenere::new(Alphabet::Latin, "z").unwrap();
    assert_eq!(
        cipher.transform("a-A a!", Operation::Encrypt).unwrap(),
        "z-A b!"
    );
    assert_eq!(
        cipher
            .transform(&"A".repeat(28), Operation::Encrypt)
            .unwrap(),
        "ZABCDEFGHIJKLMNOPQRSTUVWXYZA"
    );
    assert_eq!(cipher.transform("", Operation::Decrypt).unwrap(), "");
    let ru = ProgressiveVigenere::new(Alphabet::Russian, "Я").unwrap();
    assert_eq!(ru.transform("ААА", Operation::Encrypt).unwrap(), "ЯАБ");
}

#[test]
fn invalid_inputs() {
    assert!(matches!(
        ProgressiveVigenere::new(Alphabet::Latin, ""),
        Err(CipherError::EmptyKey)
    ));
    for key in ["A!", "КЛЮЧ", "ß", "ſ"] {
        assert!(ProgressiveVigenere::new(Alphabet::Latin, key).is_err());
    }
    let cipher = ProgressiveVigenere::new(Alphabet::Russian, "Ё").unwrap();
    assert_eq!(
        cipher.transform("АZ", Operation::Encrypt),
        Err(CipherError::InvalidText(2))
    );
}

proptest! {
    #[test]
    fn roundtrip(indices in prop::collection::vec(0usize..70, 0..400), key_indices in prop::collection::vec(0usize..33, 1..30), russian in any::<bool>()) {
        let alphabet = if russian { Alphabet::Russian } else { Alphabet::Latin };
        let letters: Vec<_> = alphabet.letters().chars().collect();
        let key: String = key_indices.iter().map(|i| letters[i % letters.len()]).collect();
        let text: String = indices.iter().map(|i| {
            if *i == 69 { ' ' } else if *i % 2 == 0 { letters[i % letters.len()] } else { letters[i % letters.len()].to_lowercase().next().unwrap() }
        }).collect();
        let cipher = ProgressiveVigenere::new(alphabet, &key).unwrap();
        let encrypted = cipher.transform(&text, Operation::Encrypt).unwrap();
        prop_assert_eq!(encrypted.chars().count(), text.chars().count());
        prop_assert_eq!(cipher.transform(&encrypted, Operation::Decrypt).unwrap(), text);
    }
}
