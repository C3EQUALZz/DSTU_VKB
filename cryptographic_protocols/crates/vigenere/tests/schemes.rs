use proptest::prelude::*;
use vigenere::domain::scheme::{Alphabet, CipherError, Operation, Scheme, Vigenere};

#[test]
fn assignment_examples() {
    for (scheme, expected) in [
        (Scheme::Standard, "ХЬЖЖЭЪБЗКАЖЦ"),
        (Scheme::Progressive, "ХЬЖЖЮЫВИМВИШ"),
        (Scheme::Autokey, "ХЬЖЖЭЯЛАТГЛП"),
    ] {
        let cipher = Vigenere::new(Alphabet::RussianWithYo, scheme, "КЛЮЧ").unwrap();
        assert_eq!(
            cipher
                .transform("КРИПТОГРАФИЯ", Operation::Encrypt)
                .unwrap(),
            expected
        );
        assert_eq!(
            cipher.transform(expected, Operation::Decrypt).unwrap(),
            "КРИПТОГРАФИЯ"
        );
    }
    let progressive = Vigenere::new(Alphabet::Latin, Scheme::Progressive, "MODE").unwrap();
    assert_eq!(
        progressive
            .transform("CRYPTOGRAPHY", Operation::Encrypt)
            .unwrap(),
        "OFBTGDKWOFME"
    );
}

#[test]
fn alphabet_and_punctuation_rules() {
    let with_yo = Vigenere::new(Alphabet::RussianWithYo, Scheme::Standard, "А").unwrap();
    assert_eq!(with_yo.transform("ЕЁ!", Operation::Encrypt).unwrap(), "ЕЁ!");
    let without_yo = Vigenere::new(Alphabet::RussianNoYo, Scheme::Standard, "А").unwrap();
    assert_eq!(
        without_yo.transform("ЕЁ_!", Operation::Encrypt).unwrap(),
        "ЕЕ_!"
    );
    let progressive = Vigenere::new(Alphabet::Latin, Scheme::Progressive, "Z").unwrap();
    assert_eq!(
        progressive.transform("a-A a!", Operation::Encrypt).unwrap(),
        "z-A b!"
    );
    assert_eq!(
        progressive.transform("А", Operation::Encrypt),
        Err(CipherError::InvalidText(1))
    );
    assert!(matches!(
        Vigenere::new(Alphabet::Latin, Scheme::Autokey, ""),
        Err(CipherError::EmptyKey)
    ));
    for key in ["A!", "КЛЮЧ", "ß", "ſ"] {
        assert!(Vigenere::new(Alphabet::Latin, Scheme::Autokey, key).is_err());
    }
    let autokey = Vigenere::new(Alphabet::RussianWithYo, Scheme::Autokey, "ЯЁКЛЮЧ").unwrap();
    assert_eq!(autokey.transform("Бё", Operation::Encrypt).unwrap(), "Ал");
}

proptest! {
    #[test]
    fn roundtrip_all_schemes_and_alphabets(
        indices in prop::collection::vec(0usize..70, 0..250),
        key_indices in prop::collection::vec(0usize..33, 1..15),
        alphabet_choice in 0usize..3,
        scheme_choice in 0usize..3,
    ) {
        let alphabet = match alphabet_choice {
            0 => Alphabet::Latin,
            1 => Alphabet::RussianWithYo,
            _ => Alphabet::RussianNoYo,
        };
        let scheme = match scheme_choice {
            0 => Scheme::Standard,
            1 => Scheme::Progressive,
            _ => Scheme::Autokey,
        };
        let letters = alphabet.letters();
        let key: String = key_indices.iter().map(|i| letters[i % letters.len()]).collect();
        let text: String = indices.iter().map(|i| {
            if *i == 69 { ' ' } else if *i % 2 == 0 { letters[i % letters.len()] } else { letters[i % letters.len()].to_lowercase().next().unwrap() }
        }).collect();
        let cipher = Vigenere::new(alphabet, scheme, &key).unwrap();
        let encrypted = cipher.transform(&text, Operation::Encrypt).unwrap();
        prop_assert_eq!(encrypted.chars().count(), text.chars().count());
        let expected = if alphabet == Alphabet::RussianNoYo { text.to_uppercase() } else { text };
        prop_assert_eq!(cipher.transform(&encrypted, Operation::Decrypt).unwrap(), expected);
    }
}
