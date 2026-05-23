# Лаб 1 — RSA

**Crate:** `crates/lab_01_rsa`
**Статус:** ✅ готова — **42 теста** (34 unit/property + 4 интеграционных CLI + 4 file-IO round-trip), clippy clean, fmt clean

## Структура крейта (Clean Architecture)

```
crates/lab_01_rsa/src/
├── domain/
│   ├── bigint.rs       BigUint + операции (add, sub, mul, divrem, mod_pow, gcd, mod_inverse)
│   ├── primes.rs       Miller-Rabin + generate_prime(bits, rng)
│   ├── rng.rs          OsRng (/dev/urandom) + DeterministicRng (xorshift, для тестов)
│   └── rsa.rs          KeyPair, PublicKey, PrivateKey, encrypt, decrypt
├── infrastructure/
│   └── storage.rs      Чтение/запись ключей и шифртекста, простой текстовый формат
├── application/
│   └── usecases.rs     GenerateKeysUseCase, EncryptUseCase, DecryptUseCase
├── presentation/
│   └── cli.rs          clap: gen | encrypt | decrypt
└── tests/cli.rs        e2e gen → encrypt → decrypt через бинарь
```

## Алгоритм

1. **`gen --bits N`**:
   - `p, q = generate_prime(N/2)` — случайное N/2-битное число с установленным старшим битом, нечётное, прошедшее **20 раундов Миллера-Рабина** (после быстрого отсева делением на простые ≤ 317).
   - `n = p*q`, `φ = (p-1)(q-1)`.
   - `e = 65537` (фиксированный). Если `gcd(e, φ) ≠ 1` — повтор.
   - `d = mod_inverse(e, φ)` через расширенный Евклид с собственным `SignedBig`.
2. **`encrypt`**: блок plaintext'а длины `(n_bytes - 1)` → `BigUint` → `c = m^e mod n` → ровно `n_bytes` байт шифртекста. В шапке шифртекста — `u64`-длина исходного сообщения для корректного хвоста.
3. **`decrypt`**: блок шифртекста → `BigUint` → `m = c^d mod n` → возвращаем хвостовые `block_len` байт (для последнего блока `block_len = plain_len % (n_bytes - 1)`).

> **Учебная схема, без PKCS#1 padding.** Поэтому изменение шифртекста даёт мусор, но не паникует; шифровать с одним и тем же ключом одно и то же сообщение даст один и тот же шифртекст. Это нормально для целей лаб 1 и согласовано с условием.

## Условие

> Реализовать генерацию открытого и закрытого ключа RSA и записать полученные ключи в файлы.
> Реализовать с помощью сгенерированных ключей шифрование произвольного текстового сообщения. Полученный результат вывести на экран и записать в файл.
> Прочитать из файлов зашифрованное сообщение, ключи, расшифровать данные и вывести расшифрованное сообщение на экран.

Источник: `docs/conditions/Laboratornye_po_kursu_Programmirovanie_algoritmov_zaschity_informatsii.docx`.

## Реализация (план)

Без сторонних крипто-крейтов (`rsa`, `num-bigint`, `num-prime`).

- `domain::bigint` — переиспользуется идея из практики 1: беззнаковый `BigUint` поверх 32-битных limb'ов, операции `+`, `-`, `*`, `/`, `mod`, `mod_pow`, `gcd`, `ext_gcd`.
- `domain::primes::miller_rabin` — детерминированный тест Миллера-Рабина с заданным набором свидетелей для требуемого диапазона.
- `domain::primes::random_prime(bits)` — генерация случайного простого нужной разрядности (по умолчанию 512 бит, т.е. модуль 1024 бит — учебный размер).
- `domain::keys::{PublicKey, PrivateKey, KeyPair, generate(bits)}`.
- `domain::cipher::{encrypt, decrypt}` — учебный RSA (без padding, на «1 блок = одно число < n»). В CLI блочим UTF-8 текст по `(bits/8 - 1)` байт.
- `infrastructure::storage` — формат файлов: текстовый, поля `n`, `e`, `d`, `bits` в hex (свой простой формат, **не** PEM, чтобы не подключать `base64` без нужды).
- `application::usecases` — `GenerateKeyPair`, `EncryptMessage`, `DecryptMessage`.
- `presentation::cli` — `clap` с подкомандами `gen`, `encrypt`, `decrypt`.

## Файловый формат ключей

```
# RSA public key (учебный, лаб 1)
bits = 1024
n = 0x...
e = 0x010001
```

```
# RSA private key (учебный, лаб 1)
bits = 1024
n = 0x...
e = 0x010001
d = 0x...
p = 0x...
q = 0x...
```

## Как запустить

```bash
just lab-01 gen --bits 1024 \
    --public  artifacts/lab_01/public.key \
    --private artifacts/lab_01/private.key

just lab-01 encrypt \
    --public  artifacts/lab_01/public.key \
    --input   docs/explanations/lab_01_rsa/sample.txt \
    --output  artifacts/lab_01/ciphertext.rsa

just lab-01 decrypt \
    --private artifacts/lab_01/private.key \
    --input   artifacts/lab_01/ciphertext.rsa
```

Подкоманда `decrypt` печатает дешифрованное сообщение на stdout (как требует условие) и записывает копию в `artifacts/lab_01/plaintext.txt`.

## Логирование

`RUST_LOG=debug` — увидишь:
- размер генерируемых $p$, $q$;
- количество итераций Miller-Rabin до успеха;
- bit-length $n$;
- размер каждого блока шифртекста.

Приватные значения (`d`, `p`, `q`) логируются только под `trace`.

## Как протестировать

```bash
cargo test -p lab_01_rsa
```

- Round-trip: `decrypt(encrypt(m, pub), priv) == m` для случайных сообщений.
- Тестовые векторы маленьких параметров (как в учебных задачах: $p=61$, $q=53$ → $n=3233$, $e=17$, $d=2753$, шифровка/дешифровка числа 65 → 2790).
- Поведение `mod_pow` против контрольных значений.
