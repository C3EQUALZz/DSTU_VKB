use lab_01_autokey_vigenere::domain::{Alphabet, AutokeyVigenere, CipherError, Operation};
use proptest::prelude::*;

#[test]
fn assignment_example() {
    let cipher = AutokeyVigenere::new(Alphabet::Latin, "MODE").unwrap();
    assert_eq!(
        cipher
            .transform("CRYPTOGRAPHY", Operation::Encrypt)
            .unwrap(),
        "OFBTVFEGTDNP"
    );
    assert_eq!(
        cipher
            .transform("OFBTVFEGTDNP", Operation::Decrypt)
            .unwrap(),
        "CRYPTOGRAPHY"
    );
}

#[test]
fn russian_example() {
    let cipher = AutokeyVigenere::new(Alphabet::Russian, "КЛЮЧ").unwrap();
    assert_eq!(
        cipher
            .transform("КРИПТОГРАФИЯ", Operation::Encrypt)
            .unwrap(),
        "ХЬЖЖЭЯЛАТГЛП"
    );
}

#[test]
fn case_punctuation_and_wrap() {
    let cipher = AutokeyVigenere::new(Alphabet::Latin, "z").unwrap();
    assert_eq!(
        cipher.transform("a-A a!", Operation::Encrypt).unwrap(),
        "z-A a!"
    );
    assert_eq!(
        cipher
            .transform(&"A".repeat(28), Operation::Encrypt)
            .unwrap(),
        "ZAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    );
    assert_eq!(cipher.transform("", Operation::Decrypt).unwrap(), "");
    assert_eq!(
        cipher.transform("z-A a!", Operation::Decrypt).unwrap(),
        "a-A a!"
    );
    let short = AutokeyVigenere::new(Alphabet::Russian, "ЯЁКЛЮЧ").unwrap();
    assert_eq!(short.transform("Бё", Operation::Encrypt).unwrap(), "Ал");
    assert_eq!(short.transform("Ал", Operation::Decrypt).unwrap(), "Бё");
    let ru = AutokeyVigenere::new(Alphabet::Russian, "Я").unwrap();
    assert_eq!(ru.transform("ААА", Operation::Encrypt).unwrap(), "ЯАА");
}

#[test]
fn invalid_inputs() {
    assert!(matches!(
        AutokeyVigenere::new(Alphabet::Latin, ""),
        Err(CipherError::EmptyKey)
    ));
    for key in ["A!", "КЛЮЧ", "ß", "ſ"] {
        assert!(AutokeyVigenere::new(Alphabet::Latin, key).is_err());
    }
    let cipher = AutokeyVigenere::new(Alphabet::Russian, "Ё").unwrap();
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
        let cipher = AutokeyVigenere::new(alphabet, &key).unwrap();
        let encrypted = cipher.transform(&text, Operation::Encrypt).unwrap();
        prop_assert_eq!(encrypted.chars().count(), text.chars().count());
        prop_assert_eq!(cipher.transform(&encrypted, Operation::Decrypt).unwrap(), text);
    }
}
