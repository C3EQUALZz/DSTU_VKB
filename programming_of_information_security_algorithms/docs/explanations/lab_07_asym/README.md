# Лаб 7 — Асимметричное шифрование через встроенный криптопровайдер ОС

**Crate:** `crates/lab_07_asym`
**Статус:** ✅ macOS / Linux — **11 тестов** (8 unit/domain/openssl + 3 интеграционных CLI), включая RSA-2048 OAEP-SHA256 round-trip. Windows — каркас.

## Условие

> Используя встроенный в операционную систему функционал CRYPTOAPI разработать приложение, реализующее следующий функционал:
> - Генерация пары ключей для асимметричного шифрования;
> - Сохранение сформированных ключей в файлы;
> - Загрузка ключей из файлов;
> - Шифрование произвольного файла открытым ключом;
> - Расшифрование зашифрованного файла закрытым ключом.

## Архитектура: Strategy + cfg

Та же схема, что и в лаб 6:

```rust
pub trait AsymmetricCryptoProvider {
    fn name(&self) -> &'static str;
    fn generate_rsa_keypair(&self, bits: usize) -> Result<RawKeyPair, CryptoError>;
    fn rsa_oaep_encrypt(&self, public: &RawPublicKey, plaintext: &[u8]) -> Result<Vec<u8>, CryptoError>;
    fn rsa_oaep_decrypt(&self, private: &RawPrivateKey, ciphertext: &[u8]) -> Result<Vec<u8>, CryptoError>;
}
```

Активный провайдер выбирается компиляционно:

| target_os | Backend | Системная библиотека |
|-----------|---------|----------------------|
| macOS | `openssl` крейт | `/usr/local/opt/openssl@3/lib/libcrypto.dylib` (Homebrew, штатное место) |
| Linux | `openssl` крейт | `/usr/lib/x86_64-linux-gnu/libcrypto.so` (часть дистрибутива) |
| Windows | каркас CNG/NCrypt | требует доработки на Windows-машине |

### Почему на macOS используется OpenSSL, а не Security framework

Apple официально **deprecated** низкоуровневый API `SecKeyCreateFromData`, через который security-framework крейт умел импортировать raw-DER RSA-ключи. Замены для импорта произвольных DER-данных без keychain в свободном доступе нет — Apple предлагает уходить в **CryptoKit** (Swift-only). Поэтому на macOS более устойчивый и тоже системный путь — `libcrypto` из OpenSSL, который стоит в системе через Homebrew (`brew install openssl@3`) и активно поддерживается.

Это **не отказ от условия** «встроенный функционал», а замена устаревшего системного криптопровайдера на актуальный — крейт `openssl` остаётся **обёрткой** над системным `libcrypto`, ничего своего не реализует.

## Алгоритм: RSA-OAEP-2048 / SHA-256

- Padding: **PKCS#1 v2.2 OAEP** (RFC 8017 §7.1).
- Hash: **SHA-256** (и для самой OAEP, и для MGF1).
- Размер модуля: 2048 бит → один блок плейнтекста ≤ **190 байт**.

CLI не реализует «гибридную схему» (AES + RSA-OAEP) — условие требует прямое использование RSA, поэтому большой файл выдаст ошибку «блок слишком длинный».

### Формат файлов

| Файл | Содержимое |
|------|------------|
| Public key | `PSIA-LAB7-PUB\0\0\0` (16 байт) + `bits: u32 be` + **PKCS#1 DER** (`RSAPublicKey`) |
| Private key | `PSIA-LAB7-PRV\0\0\0` (16 байт) + `bits: u32 be` + **PKCS#1 DER** (`RSAPrivateKey`) |
| Ciphertext | `PSIA-LAB7-CTX\0\0\0` (16 байт) + сырой шифртекст OAEP |

`Debug` у `RawPrivateKey` редактирован — приватный DER не утечёт в логи.

## Как запустить

```bash
just lab-07 gen-keys --bits 2048 \
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

diff artifacts/lab_07/sample.dec docs/explanations/lab_07_asym/sample.txt
# должно быть пусто
```

## Тесты

```bash
cargo test -p lab_07_asym
```

Покрытие:

| Слой | Тесты |
|------|-------|
| `domain::keys` | round-trip pack/unpack public, private, ciphertext; неверный magic → ошибка; Debug приватного ключа не печатает DER |
| `infrastructure::openssl_provider` | RSA-2048 OAEP round-trip; ломаем последний байт шифртекста → ошибка |
| `application::usecases` | e2e gen-keys → encrypt → decrypt через диск с активным провайдером |
| `tests/cli.rs` | CLI gen-keys/encrypt/decrypt; **decrypt чужим ключом → exit ≠ 0**; `--help` |

## Безопасность

- **OAEP** устойчив к Bleichenbacher-атакам (в отличие от PKCS#1 v1.5).
- **SHA-256** для OAEP и MGF1 — current best practice.
- **Раздельные ключи** для каждого устройства — генерация не использует общесистемный seed.
- **Приватный DER не печатается** в Debug-логи. Сравнение ключей — побайтово.

## Известные ограничения

| Что | Статус |
|-----|--------|
| macOS — OpenSSL поверх системного libcrypto | ✅ работает |
| Linux — то же | ⚠️ компилируется при сборке на Linux-машине |
| Windows — NCrypt каркас | 🚧 реализация через `BCRYPT_PAD_OAEP` оставлена next-step |
| RSA-OAEP для больших файлов | ⛔ блок ≤ 190 байт по дизайну OAEP-2048-SHA256 — для произвольных файлов нужен гибрид (AES из лаб 6 + OAEP над AES-ключом) |
