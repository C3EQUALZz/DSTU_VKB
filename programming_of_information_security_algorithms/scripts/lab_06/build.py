"""Отчёт по лаб. 6 — симметричное шифрование через CRYPTOAPI ОС (AES-256-CBC + HMAC)."""

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

SHOTS = ROOT / "docs" / "screenshots" / "lab_06"
SNIPS = ROOT / "docs" / "snippets" / "lab_06"


def main() -> None:
    meta = LabMeta(number=6, title="Использование CRYPTOAPI для реализации схемы симметричного шифрования (AES-256-CBC + HMAC-SHA-256)")
    doc = make_doc()
    add_title_page(doc, meta)
    add_page_break(doc)

    add_heading(doc, "Тема и цель работы")
    add_para(doc,
        "Тема: использование встроенного в операционную систему "
        "криптопровайдера (на Windows — CRYPTOAPI / CNG, на Linux — "
        "OpenSSL libcrypto, на macOS — CommonCrypto + Security "
        "framework) для реализации симметричного шифрования "
        "произвольного файла. Реализация — без ручной криптографии: "
        "AES-256 в режиме CBC + аутентификация HMAC-SHA-256 в схеме "
        "encrypt-then-MAC.")
    add_para(doc,
        "Цель работы: освоить работу с системным криптопровайдером, "
        "не реализуя криптоалгоритмы вручную; сгенерировать стойкий "
        "симметричный ключ (32 байта для AES + 32 байта для HMAC); "
        "сохранить ключ в файле и затем загрузить из файла; "
        "зашифровать произвольный файл и расшифровать его обратно; "
        "убедиться, что после round-trip восстановленный файл "
        "побайтово совпадает с исходным.")

    add_heading(doc, "Условие задания", level=2)
    add_bullets(doc, [
        "Генерация ключа для симметричного шифрования.",
        "Сохранение сформированного ключа в файл.",
        "Загрузка ключа из файла.",
        "Шифрование произвольного файла.",
        "Расшифрование зашифрованного файла.",
    ])
    add_para(doc,
        "Платформа разработки — macOS. Условие требует «встроенный "
        "функционал ОС» — на macOS это Apple CommonCrypto и Security "
        "framework, прямой эквивалент Windows CRYPTOAPI / CNG. "
        "Сам криптокод (AES, HMAC) поставляется системой; в нашем "
        "крейте только FFI-обёртки.")

    add_heading(doc, "Архитектура: Strategy + cfg")
    add_para(doc,
        "Чтобы код был портируемым между ОС, использован паттерн "
        "Strategy. Trait SymmetricCryptoProvider описывает абстрактный "
        "криптопровайдер; конкретные реализации (CommonCryptoProvider "
        "для macOS, OpenSslProvider для Linux, CngProvider для Windows) "
        "выбираются компиляционно через cfg(target_os = …). Слой "
        "use case'ов работает только через trait — никаких "
        "`if cfg!` внутри бизнес-логики.")
    add_table_simple(doc, [
        ["ОС", "Системный криптопровайдер", "Backend в крейте"],
        ["macOS", "CommonCrypto + Security framework", "Прямой FFI к C-функциям системы"],
        ["Linux", "OpenSSL / libcrypto.so (часть дистрибутива)", "Крейт openssl (биндинг к системному libcrypto)"],
        ["Windows", "CNG / bcrypt.dll", "windows-sys::Win32::Security::Cryptography (каркас)"],
    ], caption="Таблица 1 — выбор криптопровайдера по платформе")

    add_image_parts(doc, SNIPS, "01_provider_trait", "Листинг 1 — trait SymmetricCryptoProvider (общий контракт всех backend'ов)")

    add_heading(doc, "Доменный слой: ключ и шифр")
    add_heading(doc, "Тип SymmetricKey", level=2)
    add_para(doc,
        "Ключ — 64 байта: первые 32 для AES-256, вторые 32 для "
        "HMAC-SHA-256. Раздельные ключи для шифрования и MAC — "
        "требование RFC 7518 §5.2 (никогда один ключ для двух разных "
        "операций). Debug отключает печать содержимого, чтобы случайный "
        "лог не утёк в SonarQube или в файл.")
    add_image_parts(doc, SNIPS, "02_key", "Листинг 2 — структура SymmetricKey")

    add_heading(doc, "Шифрование: encrypt-then-MAC", level=2)
    add_para(doc,
        "Алгоритм encrypt-then-MAC: сначала шифруем plaintext в "
        "AES-256-CBC с случайным IV, затем MAC'ируем (IV || ciphertext) "
        "ключом HMAC. На дешифровке сначала проверяем MAC (constant-"
        "time сравнение!), и только если он совпал — расшифровываем. "
        "Эта схема устойчива к padding oracle атаке (в отличие от "
        "MAC-then-encrypt).")
    add_image_parts(doc, SNIPS, "03_cipher", "Листинг 3 — функции seal / open (encrypt-then-MAC)")

    add_heading(doc, "Backend macOS: CommonCrypto", level=2)
    add_para(doc,
        "На macOS используется системная C-библиотека CommonCrypto "
        "(часть libSystem.dylib). FFI-обёртки вызывают CCCrypt с "
        "флагами kCCAlgorithmAES, kCCOptionPKCS7Padding и "
        "kCCModeCBC. Случайные байты для ключа и IV берутся из "
        "CCRandomGenerateBytes (системный CSPRNG, безопасен для "
        "криптографических ключей).")
    add_image_parts(doc, SNIPS, "04_macos_backend", "Листинг 4 — backend macOS через FFI к CommonCrypto")

    add_heading(doc, "Use cases: gen-key / encrypt / decrypt", level=2)
    add_image_parts(doc, SNIPS, "05_usecases", "Листинг 5 — три use case'а через trait-абстракцию провайдера")

    add_page_break(doc)
    add_heading(doc, "Форматы файлов")
    add_table_simple(doc, [
        ["Файл", "Структура"],
        ["Ключ (.key)", "16 байт magic «PSIA-LAB6-AES\\0\\0\\0» + 32 байта AES + 32 байта HMAC = 80 байт"],
        ["Шифртекст (.enc)", "16 байт magic «PSIA-LAB6-CTXT\\0\\0» + 16 байт IV + ciphertext + 32 байта HMAC"],
    ], caption="Таблица 2 — структуры бинарных файлов")

    add_para(doc,
        "Magic-байты в начале каждого файла нужны, чтобы быстро "
        "отличить наш формат от случайного бинаря: при загрузке "
        "первые 16 байт сравниваются с эталоном, иначе сразу "
        "возвращается ошибка «invalid file format», и расшифровка "
        "не начинается. Это страховка от подмешивания мусора в "
        "файл — пусть и слабая (не криптографическая, но удобная для "
        "диагностики).")

    add_heading(doc, "Сборка и запуск")
    add_listing(doc,
        "cargo build --workspace --release\n"
        "\n"
        "# 1) Генерация симметричного ключа\n"
        "just lab-06 gen-key --out artifacts/lab_06/symm.key\n"
        "\n"
        "# 2) Шифрование произвольного файла\n"
        "just lab-06 encrypt \\\n"
        "    --key artifacts/lab_06/symm.key \\\n"
        "    --in  docs/explanations/lab_06_sym/sample.txt \\\n"
        "    --out artifacts/lab_06/sample.enc\n"
        "\n"
        "# 3) Расшифрование обратно\n"
        "just lab-06 decrypt \\\n"
        "    --key artifacts/lab_06/symm.key \\\n"
        "    --in  artifacts/lab_06/sample.enc \\\n"
        "    --out artifacts/lab_06/sample.dec\n"
        "\n"
        "# Проверка побайтового совпадения\n"
        "diff -q docs/explanations/lab_06_sym/sample.txt \\\n"
        "        artifacts/lab_06/sample.dec",
        caption="Листинг 6 — команды запуска"
    )

    add_heading(doc, "Результаты запуска")
    add_image_parts(doc, SHOTS, "01_genkey", "Рисунок 1 — генерация симметричного ключа (80 байт)")
    add_image_parts(doc, SHOTS, "02_encrypt", "Рисунок 2 — шифрование sample.txt → sample.enc")
    add_image_parts(doc, SHOTS, "03_decrypt", "Рисунок 3 — расшифрование sample.enc → sample.dec")
    add_image_parts(doc, SHOTS, "04_diff", "Рисунок 4 — побайтовое совпадение восстановленного файла с исходным + hex-дамп шифртекста")

    add_page_break(doc)
    add_heading(doc, "Безопасность и тестирование")
    add_para(doc,
        "В реализации применены следующие защитные практики:")
    add_bullets(doc, [
        "Encrypt-then-MAC: устойчиво к padding oracle (в отличие от "
        "MAC-then-encrypt, как в SSL 3.0 / TLS 1.0 с CBC).",
        "Constant-time сравнение MAC (constant_time_eq) — без раннего "
        "выхода по первому несовпадению байта; защита от time-based "
        "side-channel атак.",
        "IV генерируется заново для каждого шифрования через "
        "системный CSPRNG; ни в коем случае не переиспользуется с тем "
        "же ключом (повторное использование IV в CBC раскрывает "
        "повторяющиеся блоки plaintext'а).",
        "Раздельные ключи для AES и HMAC — никогда один ключ для двух "
        "криптопримитивов (RFC 7518 §5.2).",
        "Debug у SymmetricKey подавлен: вместо содержимого выводится "
        "«<redacted>», чтобы случайный лог не утёк в SonarQube и не "
        "попал в git-историю.",
        "PKCS#7 padding в CBC — стандартный и совместимый с системными "
        "криптопровайдерами всех трёх ОС.",
    ])

    add_heading(doc, "Тестовые векторы")
    add_table_simple(doc, [
        ["Вектор", "Источник", "Что проверяет"],
        ["AES-256-CBC: ключ нули, IV нули, plaintext нули, ciphertext = dc95c078a2408989…",
         "NIST CAVS", "Корректность AES-256 на одном блоке"],
        ["HMAC-SHA-256: ключ = 0x0b·20, data = 'Hi There', tag = b0344c61d8db38535ca8…",
         "RFC 4231 §4.2", "Корректность HMAC-SHA-256"],
        ["AES-CBC round-trip случайных данных",
         "—", "decrypt(encrypt(p)) = p"],
        ["Ломаем последний байт шифртекста → MAC mismatch",
         "—", "Аутентификация работает: подделка не пройдёт"],
    ], caption="Таблица 3 — тестовые векторы NIST/RFC и интеграционные проверки")

    add_heading(doc, "Покрытие тестами")
    add_table_simple(doc, [
        ["Слой", "Тестов", "Что"],
        ["Domain", "5", "SymmetricKey round-trip; неверная длина и magic → ошибка; Debug не утекает; constant_time_eq"],
        ["macOS provider", "4", "AES-CBC round-trip; NIST CAVS; RFC 4231; fill_random отдаёт ненулевые байты"],
        ["Storage", "3", "Round-trip через диск; неверный magic → ошибка"],
        ["Application", "2", "e2e gen→encrypt→decrypt; ломаем последний байт → MAC mismatch"],
        ["CLI integration", "3", "gen-key/encrypt/decrypt через бинарь; повреждённый ciphertext → exit ≠ 0; --help"],
        ["Misc", "1", "constant_time_eq базовые случаи"],
        ["Итого", "18", "—"],
    ], caption="Таблица 4 — покрытие автоматическими тестами")

    add_page_break(doc)
    add_heading(doc, "Контрольные вопросы")
    QA = [
        ("Что такое CRYPTOAPI на разных ОС и почему мы должны использовать именно её?",
         "CRYPTOAPI (на Windows — CNG / Bcrypt, на macOS — CommonCrypto + "
         "Security framework, на Linux — OpenSSL libcrypto) — это "
         "штатные системные криптопровайдеры. Их использование "
         "предпочтительнее самописной реализации по трём причинам: "
         "1) они проходят сертификацию (FIPS 140-2/3) и аудиты; "
         "2) ОС обновляет их при найденных уязвимостях независимо от "
         "приложения; 3) они часто используют аппаратное ускорение "
         "(AES-NI, ARM Crypto Extensions). Условие лаб 6 явно требует "
         "именно встроенный функционал ОС."),
        ("В чём разница CBC и других режимов AES?",
         "AES — блочный шифр, шифрует ровно 16 байт за раз. Режим "
         "определяет, как сцепить много блоков: ECB шифрует каждый "
         "независимо (плохо — одинаковые блоки plaintext дают "
         "одинаковые ciphertext); CBC использует XOR-сцепление с "
         "предыдущим блоком и случайный IV (безопасно при "
         "правильном IV); CTR/GCM превращают AES в потоковый шифр и "
         "позволяют параллельную работу. Мы выбрали CBC + отдельный "
         "HMAC, потому что эта схема прозрачно поддерживается всеми "
         "тремя системными API и хорошо изучена."),
        ("Зачем нужен IV (Initialization Vector) и почему его нельзя переиспользовать?",
         "IV — это случайный 16-байтовый блок, который XOR'ится с "
         "первым блоком plaintext перед шифрованием. Без IV "
         "одинаковые сообщения, зашифрованные одним и тем же ключом, "
         "дают одинаковые шифртексты, что раскрывает повторы в "
         "плейнтексте (атака frequency analysis). Повторное "
         "использование одного IV с разными сообщениями приводит к "
         "тому же эффекту: XOR двух шифртекстов даёт XOR двух "
         "плейнтекстов, и атакующий может восстановить оба, зная "
         "статистику языка. Поэтому IV генерируется заново для каждого "
         "шифрования и записывается в файл вместе с ciphertext "
         "(не секретен, но не должен повторяться)."),
        ("Что такое padding oracle и почему encrypt-then-MAC безопасен?",
         "Padding oracle — атака на CBC, использующая то, что "
         "получатель сообщает ошибку «invalid padding» отдельно от "
         "«invalid mac». Атакующий побайтово подбирает плейнтекст, "
         "проверяя у сервера каждый кандидат на корректный padding "
         "(byte-at-a-time). В схеме encrypt-then-MAC получатель "
         "сначала проверяет MAC всего пакета IV+ciphertext, и если "
         "он не совпал — отвергает запрос без проверки padding. "
         "Атакующий не имеет возможности отличить «плохой padding» "
         "от «плохой MAC», и атака невозможна."),
        ("Почему мы хешируем именно IV || ciphertext, а не IV + plaintext?",
         "Если бы MAC считался от plaintext (MAC-then-encrypt), "
         "получатель сначала должен был бы расшифровать (а padding "
         "может быть невалидным — оракул!) и только потом проверить "
         "MAC. Encrypt-then-MAC переворачивает порядок: MAC покрывает "
         "именно то, что передаётся по сети (IV + ciphertext), и "
         "проверяется первым делом. Это устраняет padding oracle и "
         "позволяет атакующему даже не доходить до AES-decrypt."),
        ("Что произойдёт, если изменить хотя бы один бит шифртекста?",
         "HMAC от испорченного пакета будет другим — не совпадёт с "
         "сохранённым тегом. Приложение сразу ответит «MAC mismatch» и "
         "не будет даже пытаться расшифровать. Это тестируется в нашем "
         "крейте отдельным тестом: ломаем последний байт ciphertext, "
         "ожидаем ошибку Application::Decrypt → MacMismatch. Без MAC "
         "(или с MAC-then-encrypt) такое изменение могло бы пройти и "
         "выдать «правильно расшифрованный» мусор."),
    ]
    for i, (q, a) in enumerate(QA, start=1):
        add_qa(doc, i, q, a)

    add_page_break(doc)
    add_heading(doc, "Выводы")
    add_para(doc,
        "В рамках лабораторной работы №6 реализован весь требуемый "
        "функционал симметричной криптосистемы на основе встроенного "
        "криптопровайдера ОС: генерация 64-байтового ключа (32 для "
        "AES-256 + 32 для HMAC-SHA-256), сохранение и загрузка ключа "
        "в собственном бинарном формате с magic-полем, шифрование "
        "произвольного файла в AES-256-CBC с случайным IV и "
        "аутентификацией encrypt-then-MAC, расшифрование обратно с "
        "проверкой MAC в constant-time. Криптокод не пишется руками — "
        "он берётся из системы (на macOS — CommonCrypto через FFI).")
    add_para(doc,
        "Корректность подтверждена прохождением тестовых векторов "
        "NIST CAVS (AES-256-CBC) и RFC 4231 §4.2 (HMAC-SHA-256), а "
        "также сценарием побайтового совпадения после round-trip. "
        "Реализация покрыта 18 автоматическими тестами (включая "
        "проверку «ломаем шифртекст → MAC не сходится»). Архитектура "
        "Strategy + cfg позволяет добавлять другие ОС без правки "
        "use case'ов — Linux-backend через OpenSSL уже написан, "
        "Windows-backend через BCrypt оставлен как next step "
        "(каркас на месте).")

    out = ROOT / "docs" / "reports" / "lab_06" / "Ковалев Д.П. ВКБ43 6 лаба.docx"
    save(doc, out)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
