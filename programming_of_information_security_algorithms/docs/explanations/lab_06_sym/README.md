# Лаб 6 — Симметричное шифрование через встроенный криптопровайдер ОС

**Crate:** `crates/lab_06_sym`
**Статус:** ✅ macOS — **18 тестов** (15 unit/property + 3 интеграционных CLI), включая NIST CAVS AES-256-CBC и RFC 4231 HMAC-SHA-256. Linux — провайдер написан, требует сборки на Linux. Windows — каркас (FFI к BCrypt оставлен как next step).

## Условие

> Используя встроенный в операционную систему функционал CRYPTOAPI разработать приложение, реализующее следующий функционал:
> - Генерация ключа для симметричного шифрования;
> - Сохранение сформированного ключа в файл;
> - Загрузку ключа из файла;
> - Шифрование произвольного файла;
> - Расшифрование зашифрованного файла.

## Архитектура: Strategy + cfg

Условие говорит «встроенный в ОС». Это значит — **не наша** криптореализация, а вызов системного криптопровайдера. На разных ОС это разные API:

| ОС | Встроенный криптопровайдер | Backend в крейте |
|----|----------------------------|-------------------|
| macOS | CommonCrypto + Security framework (`libSystem.dylib`, `Security.framework`) | прямой FFI |
| Linux | OpenSSL / `libcrypto.so` (часть дистрибутива) | крейт `openssl` (биндинг к системному libcrypto) |
| Windows | CNG (`bcrypt.dll`) | `windows-sys::Win32::Security::Cryptography` (FFI скелет) |

Все три скрыты за единым trait'ом `SymmetricCryptoProvider` (паттерн Strategy):

```rust
pub trait SymmetricCryptoProvider {
    fn name(&self) -> &'static str;
    fn fill_random(&self, buf: &mut [u8]) -> Result<(), CryptoError>;
    fn aes_cbc_encrypt(&self, key: &[u8; 32], iv: &[u8; 16], plaintext: &[u8]) -> Result<Vec<u8>, CryptoError>;
    fn aes_cbc_decrypt(&self, key: &[u8; 32], iv: &[u8; 16], ciphertext: &[u8]) -> Result<Vec<u8>, CryptoError>;
    fn hmac_sha256(&self, key: &[u8; 32], data: &[u8]) -> Result<[u8; 32], CryptoError>;
}
```

Выбор провайдера — статический через `cfg(target_os = …)`:

```rust
#[cfg(target_os = "macos")] pub type ActiveProvider = macos::CommonCryptoProvider;
#[cfg(target_os = "linux")] pub type ActiveProvider = linux::OpenSslProvider;
#[cfg(target_os = "windows")] pub type ActiveProvider = windows::CngProvider;
```

Логика use case'ов (`GenerateKey`, `EncryptFile`, `DecryptFile`) написана **один раз** и работает поверх trait'а — никаких `if cfg!` внутри.

## Алгоритм: AES-256-CBC + HMAC-SHA-256 (encrypt-then-MAC)

Стандартная криптоконструкция (как в TLS 1.0–1.2 с CBC-suite): сначала шифруем CBC'ом, потом MACаем `IV || ciphertext` ключом HMAC. На дешифровке сначала проверяем MAC, только потом расшифровываем.

| Поле | Размер | Содержание |
|------|--------|-----------|
| key.aes | 32 байта | AES-256 ключ |
| key.hmac | 32 байта | HMAC-SHA-256 ключ |
| IV | 16 байт | случайный, из системного RNG |
| Padding | PKCS#7 | стандартный для CBC |
| MAC | 32 байта | HMAC-SHA-256 от `IV || ciphertext` |

### Формат файлов

- **Ключ**: 16 байт magic `PSIA-LAB6-AES\0\0\0` + 32 байта AES + 32 байта HMAC = **80 байт**.
- **Шифртекст**: 16 байт magic `PSIA-LAB6-CTXT\0\0` + 16 байт IV + ciphertext + 32 байта HMAC.

`Debug` для `SymmetricKey` **не печатает** байты ключа (`<redacted>`) — чтобы случайный лог не утёк в файл или в SonarQube.

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

diff artifacts/lab_06/sample.dec docs/explanations/lab_06_sym/sample.txt
# должно быть пусто — файл восстановлен побайтово
```

## Тесты

```bash
cargo test -p lab_06_sym
```

Что покрыто:

| Слой | Тесты | Что |
|------|-------|-----|
| Domain | `SymmetricKey` round-trip через bytes, неверная длина и неверный magic → ошибка; `Debug` не утекает ключ; constant-time MAC compare | 5 |
| macOS provider | AES-CBC round-trip; **NIST CAVS** один блок нулей с нулевым ключом → `dc95c078a240898…`; **RFC 4231 §4.2** HMAC-SHA-256 от `0x0b…` и «Hi There» → `b0344c61d8db3853…`; `fill_random` даёт ненулевые байты | 4 |
| Storage | сериализация ключа и шифртекста через диск, неверный magic шифртекста → ошибка | 3 |
| Application | e2e gen→encrypt→decrypt; ломаем последний байт → ошибка `MAC mismatch` | 2 |
| CLI integration | gen-key/encrypt/decrypt через бинарь, повреждённый шифртекст → exit ≠ 0, `--help` | 3 |
| Misc | `constant_time_eq` базовые случаи | 1 |

## Безопасность

- **Encrypt-then-MAC** — устойчив к padding-oracle атакам, в отличие от MAC-then-encrypt.
- **constant-time** сравнение MAC: `constant_time_eq` в `domain/cipher.rs` не выходит по короткому пути при первом расхождении.
- **PKCS#7** padding — стандартный, но без `BCRYPT_BLOCK_PADDING` на Windows тонкость в том, что нужен `BCRYPT_BLOCK_PADDING` именно при шифровании и расшифровке.
- **IV** генерируется заново для каждого шифрования — нельзя переиспользовать с тем же ключом.
- **Разные ключи** для шифрования и MAC (RFC 7518 §5.2) — никогда один ключ для обоих.

## Известные ограничения

| Что | Статус | План |
|-----|--------|------|
| macOS — CommonCrypto + Security framework | ✅ работает, NIST/RFC векторы проходят | — |
| Linux — `openssl` крейт (системный libcrypto) | ⚠️ компилируется только на Linux-target, локально на macOS нет линковщика | Прогнать `cargo test -p lab_06_sym` на Linux-машине |
| Windows — CNG (BCrypt) | 🚧 каркас, FFI оставлен TODO | Реализовать на Windows-машине; в `windows.rs` подробный план с указанием функций и тонкостей `PCWSTR` |
