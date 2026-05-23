# Лаб 7 — Асимметричное шифрование через встроенный криптопровайдер ОС

**Crate:** `crates/lab_07_asym`
**Статус:** ⏳ в разработке

## Условие

> Используя встроенный в операционную систему функционал CRYPTOAPI разработать приложение, реализующее следующий функционал:
> - Генерация пары ключей для асимметричного шифрования;
> - Сохранение сформированных ключей в файлы;
> - Загрузка ключей из файлов;
> - Шифрование произвольного файла открытым ключом;
> - Расшифрование зашифрованного файла закрытым ключом.

## Платформа

Аналог CRYPTOAPI на macOS — Security framework. Используем `SecKey` и алгоритм `RsaEncryptionOaepSha256` (RSA-OAEP с MGF1-SHA-256), 2048 бит.

В отличие от лаб 1, здесь RSA — это **системная** реализация, как и просит условие («встроенный функционал ОС»). Поверх него — наш CLI и адаптеры файлов.

## Реализация (план)

- `infrastructure::sec_key::{generate_rsa_keypair, export_public, export_private, import_public, import_private}` — через `SecKey`.
- `infrastructure::cipher::SecKeyCipher` — `encrypt_with_public`, `decrypt_with_private`.
- `application::usecases::{GenerateKeys, EncryptFile, DecryptFile}`.
- `presentation::cli` — `gen-keys`, `encrypt`, `decrypt`.

Файлы ключей — в PKCS#1 DER (то, что отдаёт `SecKey::external_representation`).

## Размер сообщения

RSA-OAEP-2048-SHA-256 шифрует за раз ≤ 190 байт. CLI принимает произвольный файл и:
- либо отказывается с понятной ошибкой, если файл больше (учебный режим),
- либо использует «гибридную схему»: AES ключ из лаб 6 + RSA-OAEP над AES-ключом (это уже расширенная реализация — обсудим, нужна ли).

Базовый вариант — отказ + сообщение «файл больше N байт, для произвольных файлов используйте гибридную схему».

## Как запустить

```bash
just lab-07 gen-keys \
    --public  artifacts/lab_07/pub.der \
    --private artifacts/lab_07/priv.der

just lab-07 encrypt \
    --public artifacts/lab_07/pub.der \
    --in     docs/explanations/lab_07_asym/sample.txt \
    --out    artifacts/lab_07/sample.enc

just lab-07 decrypt \
    --private artifacts/lab_07/priv.der \
    --in      artifacts/lab_07/sample.enc \
    --out     artifacts/lab_07/sample.dec
```

## Как протестировать

```bash
cargo test -p lab_07_asym
```

- Round-trip с системным RSA.
- Импорт сохранённого ключа → результат побайтово совпадает.
- Encrypt/decrypt с разными парами ключей дают разный шифртекст (рандомизированный OAEP).
- Попытка decrypt чужим ключом → ошибка.
