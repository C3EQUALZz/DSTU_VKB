# Лаб 6 — Симметричное шифрование через встроенный криптопровайдер ОС

**Crate:** `crates/lab_06_sym`
**Статус:** ⏳ в разработке

## Условие

> Используя встроенный в операционную систему функционал CRYPTOAPI разработать приложение, реализующее следующий функционал:
> - Генерация ключа для симметричного шифрования;
> - Сохранение сформированного ключа в файл;
> - Загрузку ключа из файла;
> - Шифрование произвольного файла;
> - Расшифрование зашифрованного файла.

## Замечание про платформу

Условие написано под Windows (CRYPTOAPI). На macOS аналог — **Security framework** / **CommonCrypto**. Это **системный API ОС**, поставляемый Apple, идеологически точно такой же, как CRYPTOAPI: студенческое приложение не реализует криптографию, а использует встроенный криптопровайдер.

Через крейт `security-framework` (тонкая обёртка над системным API). Алгоритм:
- **AES-256 в режиме GCM** через `SecKey` + `SecKeyAlgorithm::AESGCM` — авторизованное шифрование, защищающее от подмены шифртекста.
- Если на нынешней версии security-framework GCM не выставлен — fallback на `CryptorRef` (CommonCrypto, AES-256-CBC + HMAC-SHA256 «encrypt-then-MAC»).

Окончательный выбор примитива зафиксирую при реализации.

## Реализация (план)

- `domain::keys::SymmetricKey` — 32 байта + опционально длинна IV/nonce.
- `infrastructure::keychain::FileKeyStore` — сохранение/загрузка ключа из файла (с предупреждением о небезопасности, как и в условии).
- `infrastructure::crypto::CommonCryptoCipher` — обёртка над системным API.
- `application::usecases::{GenerateKey, EncryptFile, DecryptFile}`.
- `presentation::cli` — `gen-key`, `encrypt`, `decrypt`.

## Файловые форматы

- Ключ: 16-байтовый magic `LAB06_AES256GCM\n` + 32 байта ключа + (для CBC) 32 байта MAC-ключа.
- Шифртекст: magic + 12 байт nonce + ciphertext || 16 байт GCM tag (или 32 байта HMAC для CBC-варианта).

## Как запустить

```bash
just lab-06 gen-key --out artifacts/lab_06/symm.key

just lab-06 encrypt \
    --key artifacts/lab_06/symm.key \
    --in  docs/explanations/lab_06_sym/sample.txt \
    --out artifacts/lab_06/sample.enc

just lab-06 decrypt \
    --key artifacts/lab_06/symm.key \
    --in  artifacts/lab_06/sample.enc \
    --out artifacts/lab_06/sample.dec
```

После расшифрования `sample.dec` должен побайтово совпадать с `sample.txt`.

## Как протестировать

```bash
cargo test -p lab_06_sym
```

- Round-trip: encrypt → decrypt → исходные байты.
- Изменение хоть одного байта шифртекста → ошибка тэга/MAC (фейл decrypt).
- Загруженный ключ из файла → совпадает с тем, что был сохранён (побайтово).
