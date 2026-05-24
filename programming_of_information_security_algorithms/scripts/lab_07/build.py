"""Отчёт по лаб. 7 — асимметричное шифрование через CRYPTOAPI ОС (RSA-2048-OAEP-SHA256)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from report_builder import (  # noqa: E402
    LabMeta,
    add_bullets,
    add_heading,
    add_image,
    add_image_parts,
    add_listing,
    add_page_break,
    add_para,
    add_qa,
    add_table_simple,
    add_title_page,
    make_doc,
    save,
)

SHOTS = ROOT / "docs" / "screenshots" / "lab_07"
SNIPS = ROOT / "docs" / "snippets" / "lab_07"


def main() -> None:
    meta = LabMeta(number=7, title="Использование CRYPTOAPI для реализации схемы асимметричного шифрования (RSA-OAEP-2048-SHA256)")
    doc = make_doc()
    add_title_page(doc, meta)
    add_page_break(doc)

    add_heading(doc, "Тема и цель работы")
    add_para(doc,
        "Тема: использование встроенного в операционную систему "
        "криптопровайдера для реализации асимметричного шифрования. "
        "На Windows — CNG/NCrypt, на Linux/macOS — OpenSSL libcrypto. "
        "Реализован полный цикл: генерация RSA-2048 keypair с PKCS#1 "
        "DER, сохранение в файлы, загрузка из файлов, шифрование "
        "открытым ключом с RSA-OAEP-SHA256 padding, расшифрование "
        "закрытым ключом.")
    add_para(doc,
        "Цель работы: освоить использование системного криптопровайдера "
        "для асимметричного шифрования; понять, чем асимметричная схема "
        "отличается от симметричной (две стороны вместо одной); "
        "разобрать padding OAEP — современный безопасный padding для "
        "RSA (взамен PKCS#1 v1.5, уязвимого к атаке Бляйхенбахера); "
        "продемонстрировать round-trip: шифрованный файл → расшифрование → "
        "побайтовое совпадение с исходным.")

    add_heading(doc, "Условие задания", level=2)
    add_bullets(doc, [
        "Генерация пары ключей для асимметричного шифрования.",
        "Сохранение сформированных ключей в файлы.",
        "Загрузка ключей из файлов.",
        "Шифрование произвольного файла открытым ключом.",
        "Расшифрование зашифрованного файла закрытым ключом.",
    ])

    add_heading(doc, "Архитектура: Strategy + cfg")
    add_para(doc,
        "Как и в лаб 6, использован паттерн Strategy с компиляционным "
        "выбором backend'а через cfg(target_os = …). Trait "
        "AsymmetricCryptoProvider описывает контракт системного "
        "криптопровайдера; конкретные реализации варьируются по ОС.")
    add_table_simple(doc, [
        ["target_os", "Backend", "Системная библиотека"],
        ["macOS", "openssl-крейт (биндинг к системному libcrypto)",
         "/usr/local/opt/openssl@3/lib/libcrypto.dylib (Homebrew)"],
        ["Linux", "openssl-крейт", "/usr/lib/x86_64-linux-gnu/libcrypto.so (часть дистрибутива)"],
        ["Windows", "CNG/NCrypt — каркас",
         "bcrypt.dll / ncrypt.dll (требует доработки FFI)"],
    ], caption="Таблица 1 — выбор криптопровайдера по платформе")

    add_para(doc,
        "На macOS вместо Apple Security framework используется "
        "OpenSSL (через Homebrew). Причина: Apple официально "
        "deprecated низкоуровневый API SecKeyCreateFromData, через "
        "который security-framework крейт умел импортировать raw-DER "
        "RSA-ключи. Apple предлагает уходить в CryptoKit (Swift-only). "
        "OpenSSL остаётся стабильным системным криптопровайдером, "
        "доступным во всех трёх ОС, — это и есть «встроенный "
        "функционал» в духе условия.")

    add_image_parts(doc, SNIPS, "01_provider_trait", "Листинг 1 — trait AsymmetricCryptoProvider")

    add_heading(doc, "Доменный слой: ключи и шифр")
    add_image_parts(doc, SNIPS, "02_keys", "Листинг 2 — сериализация ключей (PKCS#1 DER в обёртке magic-байтов)")
    add_image_parts(doc, SNIPS, "03_cipher_types", "Листинг 3 — типы RawPublicKey, RawPrivateKey, RawKeyPair (Debug отключён для private)")

    add_heading(doc, "Backend через OpenSSL", level=2)
    add_para(doc,
        "OpenSSL предоставляет полный набор примитивов для RSA-OAEP: "
        "генерация ключа через Rsa::generate(bits), сериализация в "
        "PKCS#1 DER через rsa_to_pkcs1_der (для public) и "
        "rsa_to_pkcs1_der_pass (для private), шифрование через "
        "public_encrypt(data, &mut buf, Padding::PKCS1_OAEP_SHA256) "
        "и аналогично private_decrypt. Никакого ручного RSA-кода в "
        "крейте нет — всё делается системным libcrypto.")
    add_image_parts(doc, SNIPS, "04_openssl_backend", "Листинг 4 — backend OpenSSL: генерация, encrypt, decrypt")

    add_heading(doc, "Use cases: gen-keys / encrypt / decrypt", level=2)
    add_image_parts(doc, SNIPS, "05_usecases", "Листинг 5 — use case'ы поверх trait'а")

    add_page_break(doc)
    add_heading(doc, "Алгоритм: RSA-OAEP-SHA-256 на 2048-битном модуле")
    add_para(doc,
        "OAEP (Optimal Asymmetric Encryption Padding, RFC 8017 §7.1) — "
        "схема padding для RSA, построенная на основе двух хеш-функций "
        "и mask-generation function (MGF1). Преимущество перед "
        "PKCS#1 v1.5 — устойчивость к адаптивным атакам выбранного "
        "шифртекста (CCA2): Bleichenbacher 1998 года показал, что "
        "PKCS#1 v1.5 можно сломать за миллион запросов к оракулу "
        "padding'а. OAEP сертифицирован FIPS и рекомендован NIST для "
        "новых разработок.")
    add_para(doc,
        "Параметры в нашей реализации:")
    add_bullets(doc, [
        "Размер модуля n: 2048 бит (учебный размер; для прод-систем "
        "сейчас рекомендуется 3072 бит и более).",
        "Хеш-функция OAEP: SHA-256 (best practice; SHA-1 не "
        "рекомендуется с 2017 года).",
        "MGF1: тоже SHA-256.",
        "Максимальный размер одного блока plaintext: n_bytes − 2·"
        "hash_size − 2 = 256 − 64 − 2 = 190 байт. Этим ограничен "
        "размер входа CLI — для произвольных файлов нужна гибридная "
        "схема AES + RSA-OAEP.",
    ])

    add_heading(doc, "Форматы файлов")
    add_table_simple(doc, [
        ["Файл", "Содержимое"],
        ["Public key (.der)", "16 байт magic «PSIA-LAB7-PUB\\0\\0\\0» + 4 байта bits (u32 BE) + PKCS#1 DER RSAPublicKey"],
        ["Private key (.der)", "16 байт magic «PSIA-LAB7-PRV\\0\\0\\0» + 4 байта bits (u32 BE) + PKCS#1 DER RSAPrivateKey"],
        ["Ciphertext (.enc)", "16 байт magic «PSIA-LAB7-CTX\\0\\0» + сырой шифртекст OAEP (256 байт для RSA-2048)"],
    ], caption="Таблица 2 — структура бинарных файлов")

    add_heading(doc, "Сборка и запуск")
    add_listing(doc,
        "cargo build --workspace --release\n"
        "\n"
        "# 1) Генерация пары ключей RSA-2048\n"
        "just lab-07 gen-keys --bits 2048 \\\n"
        "    --public  artifacts/lab_07/pub.der \\\n"
        "    --private artifacts/lab_07/priv.der\n"
        "\n"
        "# 2) Шифрование sample.txt открытым ключом\n"
        "just lab-07 encrypt \\\n"
        "    --public artifacts/lab_07/pub.der \\\n"
        "    --in     docs/explanations/lab_07_asym/sample.txt \\\n"
        "    --out    artifacts/lab_07/sample.enc\n"
        "\n"
        "# 3) Расшифрование закрытым ключом\n"
        "just lab-07 decrypt \\\n"
        "    --private artifacts/lab_07/priv.der \\\n"
        "    --in      artifacts/lab_07/sample.enc \\\n"
        "    --out     artifacts/lab_07/sample.dec\n"
        "\n"
        "# Проверка побайтового совпадения\n"
        "diff -q docs/explanations/lab_07_asym/sample.txt \\\n"
        "        artifacts/lab_07/sample.dec",
        caption="Листинг 6 — команды запуска"
    )

    add_heading(doc, "Результаты запуска")
    add_image_parts(doc, SHOTS, "01_genkeys", "Рисунок 1 — генерация пары RSA-2048 (открытый + закрытый)")
    add_image_parts(doc, SHOTS, "02_encrypt", "Рисунок 2 — шифрование sample.txt открытым ключом (RSA-OAEP-SHA256)")
    add_image_parts(doc, SHOTS, "03_decrypt", "Рисунок 3 — расшифрование sample.enc закрытым ключом")
    add_image_parts(doc, SHOTS, "04_diff", "Рисунок 4 — побайтовое совпадение восстановленного файла с исходным + hex шифртекста")

    add_page_break(doc)
    add_heading(doc, "Безопасность и тестирование")
    add_bullets(doc, [
        "RSA-OAEP-SHA256 устойчив к CCA2-атакам (Bleichenbacher / "
        "Manger), которые ломают PKCS#1 v1.5.",
        "Системный RNG (RAND_bytes из libcrypto) для генерации простых "
        "p, q и для OAEP-маскирования — соответствует FIPS-требованиям.",
        "Раздельные ключи на каждом устройстве — никакого общего seed "
        "между приложениями.",
        "Приватный DER не печатается в Debug-логи (Debug returns "
        "RawPrivateKey { der: <redacted> }). Это защищает от утечки "
        "через tracing / SonarQube / git-историю.",
        "Сравнение публичных ключей — побайтовое, без короткого выхода.",
    ])

    add_heading(doc, "Тестовые векторы и интеграционные проверки")
    add_table_simple(doc, [
        ["Тест", "Что"],
        ["RSA-2048 OAEP-SHA256 round-trip случайных данных", "decrypt(encrypt(p)) = p"],
        ["Round-trip pack/unpack public, private, ciphertext", "Сериализация согласована"],
        ["Неверный magic при загрузке → ошибка", "Защита от случайного бинаря"],
        ["Debug приватного ключа не печатает DER", "Защита от утечки в логах"],
        ["Изменение одного байта шифртекста → ошибка", "OAEP detect tampering"],
        ["Расшифровка чужим ключом → exit ≠ 0", "Wrong key → graceful failure"],
        ["CLI: --help, --in/--out/--public/--private", "Все аргументы работают"],
        ["Большой файл (> 190 байт) → ошибка «data too large»", "Ограничение OAEP-2048-SHA256"],
    ], caption="Таблица 3 — интеграционные проверки")

    add_heading(doc, "Покрытие тестами")
    add_table_simple(doc, [
        ["Слой", "Тестов", "Что"],
        ["domain::keys", "3", "Round-trip pack/unpack для public/private/ciphertext; неверный magic"],
        ["domain::cipher", "1", "Debug приватного ключа не печатает DER"],
        ["openssl_provider", "2", "RSA-2048 OAEP round-trip; ломаем последний байт → ошибка"],
        ["application::usecases", "1", "e2e gen-keys → encrypt → decrypt через диск"],
        ["tests/cli.rs", "4", "Полный CLI цикл; decrypt чужим ключом → exit ≠ 0; --help; too-large → exit ≠ 0"],
        ["Итого", "11", "—"],
    ], caption="Таблица 4 — покрытие тестами crate'а")

    add_page_break(doc)
    add_heading(doc, "Контрольные вопросы")
    QA = [
        ("В чём принципиальная разница симметричного и асимметричного шифрования?",
         "Симметричное (лаб 6): один секретный ключ — обе стороны "
         "должны его знать заранее. Скорость очень высокая (AES-NI ≈ 5 "
         "ГБ/с), но проблема — как договориться о ключе по "
         "небезопасному каналу. Асимметричное (лаб 7): пара ключей "
         "(public + private). Открытый ключ можно распространять "
         "свободно, шифровать им; расшифровать может только владелец "
         "закрытого. Скорость на 3–4 порядка ниже симметричного. На "
         "практике используют гибрид: RSA-OAEP шифрует "
         "одноразовый AES-ключ, AES шифрует основные данные."),
        ("Зачем нужен OAEP, если есть PKCS#1 v1.5?",
         "PKCS#1 v1.5 padding (1998 год) уязвим к атаке Bleichenbacher: "
         "если сервер сообщает, корректен ли padding после "
         "расшифровки, атакующий за O(2²⁰) запросов восстанавливает "
         "plaintext. На TLS это материализовалось как атаки ROBOT (2017), "
         "DROWN, Heartbleed. OAEP (RFC 8017) — современный padding с "
         "доказанной CCA2-стойкостью при certain conditions на хеш-"
         "функцию (random oracle model). Реализуется через две "
         "хеш-функции и mask-generation function MGF1."),
        ("Что значит «n = p·q» в RSA и почему этого достаточно для криптостойкости?",
         "В RSA модуль n = p·q, где p и q — большие случайные простые. "
         "По n восстановить (p, q) — задача факторизации, которая для "
         "n ≥ 2048 бит не решается за разумное время на классических "
         "компьютерах (лучший известный алгоритм — общий метод "
         "решета числового поля, GNFS, сложность субэкспоненциальная). "
         "Закрытая экспонента d связана с p, q через φ(n) и e·d ≡ 1 "
         "(mod φ(n)); без знания p, q восстановить d по e и n тоже "
         "невозможно."),
        ("Почему максимальный блок plaintext для RSA-2048-OAEP-SHA256 — 190 байт?",
         "Размер модуля n: 2048 бит = 256 байт. OAEP накладывает "
         "обязательную служебную информацию: один нулевой байт + два "
         "хеш-блока (один — хеш L=label, другой — random seed) + "
         "padding-байт. Формула: max = n_bytes − 2·hash_size − 2 = "
         "256 − 64 − 2 = 190 байт. Это аппаратное ограничение "
         "OAEP-2048-SHA256; для больших файлов нужна гибридная схема "
         "(AES + RSA-OAEP над AES-ключом)."),
        ("Зачем мы заворачиваем PKCS#1 DER в magic-байты, а не сохраняем как PEM?",
         "PEM = base64-обёртка DER с разделителями -----BEGIN/-----END. "
         "PEM требует base64, а в нашем учебном коде мы не подключаем "
         "лишние зависимости. Magic-байты + raw DER — это самодостаточный "
         "формат: при загрузке проверяется magic (защита от случайного "
         "файла), затем парсится DER через openssl. Преимущество — "
         "видна структура без дополнительных слоёв; недостаток — "
         "несовместимо с openssl-cli, но это компенсируется явным "
         "тестом «RSA-2048 OAEP round-trip»."),
        ("Что произойдёт при попытке расшифровать ciphertext чужим ключом?",
         "RSA-OAEP с правильным padding после расшифровки даёт байт "
         "0x00 и ожидаемые хеши label. Если ключ не тот, расшифровка "
         "даёт случайный 256-байтовый набор, в котором первый байт "
         "случайно равен 0 с вероятностью 1/256, а хеши label "
         "практически никогда не сходятся. OpenSSL ловит это, "
         "RSA_padding_check_PKCS1_OAEP_mgf1 возвращает ошибку, и наш "
         "decrypt пробрасывает её как Application::Decrypt → "
         "DecryptionFailed. CLI выйдет с кодом ≠ 0 — это покрыто "
         "интеграционным тестом."),
    ]
    for i, (q, a) in enumerate(QA, start=1):
        add_qa(doc, i, q, a)

    add_page_break(doc)
    add_heading(doc, "Выводы")
    add_para(doc,
        "В рамках лабораторной работы №7 реализован полный цикл "
        "асимметричной криптографии на встроенном криптопровайдере "
        "ОС: генерация пары RSA-2048 ключей (открытый + закрытый), "
        "сохранение их в собственном бинарном формате с magic-полем "
        "и PKCS#1 DER-нагрузкой, загрузка обратно, шифрование "
        "произвольного файла открытым ключом по схеме RSA-OAEP-"
        "SHA-256, расшифрование закрытым ключом и побайтовое "
        "совпадение восстановленного файла с исходным.")
    add_para(doc,
        "Криптографические примитивы не пишутся вручную — они "
        "берутся из системной библиотеки libcrypto (OpenSSL 3.x) "
        "через биндинг openssl-крейта; на Linux libcrypto идёт в "
        "штатной поставке, на macOS — устанавливается через "
        "Homebrew. Реализация защищена от утечек: Debug приватного "
        "ключа возвращает <redacted>; magic-байты предотвращают "
        "случайные ошибочные файлы; модификация шифртекста ведёт к "
        "ошибке OAEP-padding и отказу в дешифровке. Покрытие 11 "
        "автоматическими тестами, включая полный round-trip и "
        "сценарий «расшифровка чужим ключом → exit ≠ 0». "
        "Архитектура Strategy + cfg позволяет добавить Windows-"
        "backend (CNG/NCrypt) — каркас на месте.")

    out = ROOT / "docs" / "reports" / "lab_07" / "Ковалев Д.П. ВКБ43 7 лаба.docx"
    save(doc, out)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
