"""Отчёт по лаб. 5 — Проверка исходных кодов SonarQube."""

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

SHOTS = ROOT / "docs" / "screenshots" / "lab_05"


def main() -> None:
    meta = LabMeta(number=5, title="Проверка исходных кодов лабораторных работ анализатором кода SonarQube")
    doc = make_doc()
    add_title_page(doc, meta)
    add_page_break(doc)

    add_heading(doc, "Тема и цель работы")
    add_para(doc,
        "Тема: статический анализ исходного кода криптографических "
        "лабораторных работ 1–4 с использованием SonarQube — "
        "промышленной платформы статического анализа от SonarSource. "
        "SonarQube развёрнут локально в Docker (Community Edition + "
        "PostgreSQL) с подключённым community-rust плагином для "
        "семантического анализа Rust-кода.")
    add_para(doc,
        "Цель работы: научиться разворачивать SonarQube из docker-"
        "compose; импортировать в неё проекты как «отдельные» (каждая "
        "лабораторная — самостоятельный проект, как требует условие); "
        "автоматизировать прогон через sonar-scanner; интерпретировать "
        "результаты Quality Gate; для найденных critical/blocker и "
        "security-замечаний предложить варианты устранения.")

    add_heading(doc, "Условие задания", level=2)
    add_bullets(doc, [
        "Выполнить проверку исходных текстов программ по лабораторным "
        "1–4 с использованием SonarQube.",
        "Каждая лабораторная должна быть представлена в виде отдельного "
        "проекта.",
        "Продемонстрировать результаты проверки.",
        "При нахождении критических и/или блокирующих замечаний, и "
        "замечаний, касающихся безопасности приложения, предложить "
        "варианты устранения этих замечаний.",
    ])

    add_heading(doc, "Инфраструктура")
    add_table_simple(doc, [
        ["Компонент", "Технология", "Назначение"],
        ["Платформа анализа", "SonarQube Community Edition 10.6", "Сервер хранения проектов и правил"],
        ["БД", "PostgreSQL 16", "Хранение метаданных проектов и замечаний"],
        ["Раннер", "sonar-scanner 8.1 (CLI, brew)", "Передаёт исходники и метрики на сервер"],
        ["Rust-плагин", "community-rust 0.2.7", "Семантический парсер .rs, импорт замечаний clippy"],
        ["Развёртывание", "docker compose (docker/sonarqube/compose.yaml)", "Воспроизводимая среда; volumes для data/logs/extensions"],
        ["Linter (data-feed)", "cargo clippy --message-format=json", "Источник замечаний для импорта в Sonar"],
    ], caption="Таблица 1 — стек инструментов для лаб 5")

    add_heading(doc, "Конфигурация SonarQube", level=2)
    add_para(doc,
        "Docker Compose поднимает контейнер SonarQube + PostgreSQL в "
        "единой сети. Healthcheck'и контролируют готовность к приёму "
        "сканирований. Volumes для extensions/data/logs гарантируют "
        "сохранение состояния между перезапусками.")
    add_listing(doc,
        "# docker/sonarqube/compose.yaml (фрагмент)\n"
        "services:\n"
        "  sonarqube:\n"
        "    image: sonarqube:10.6-community\n"
        "    container_name: psia-sonarqube\n"
        "    depends_on:\n"
        "      sonar-db: { condition: service_healthy }\n"
        "    environment:\n"
        "      SONAR_JDBC_URL: jdbc:postgresql://sonar-db:5432/sonarqube\n"
        "      SONAR_JDBC_USERNAME: sonar\n"
        "      SONAR_JDBC_PASSWORD: sonar\n"
        "    ports: [\"9000:9000\"]\n"
        "    volumes:\n"
        "      - sonarqube_data:/opt/sonarqube/data\n"
        "      - sonarqube_logs:/opt/sonarqube/logs\n"
        "      - sonarqube_extensions:/opt/sonarqube/extensions",
        caption="Листинг 1 — фрагмент compose.yaml"
    )

    add_heading(doc, "sonar-project.properties для каждой лабы", level=2)
    add_listing(doc,
        "# crates/lab_01_rsa/sonar-project.properties\n"
        "sonar.projectKey=lab_01_rsa\n"
        "sonar.projectName=Лабораторная № 1 — RSA\n"
        "sonar.projectVersion=0.1.0\n"
        "sonar.sources=src\n"
        "sonar.tests=tests\n"
        "sonar.exclusions=**/target/**\n"
        "sonar.sourceEncoding=UTF-8\n"
        "sonar.language=rust\n"
        "sonar.community.rust.clippy.reportPaths=clippy.json",
        caption="Листинг 2 — конфигурация одного проекта SonarQube"
    )

    add_page_break(doc)
    add_heading(doc, "Порядок прогона")
    add_listing(doc,
        "# 1) Поднять SonarQube + Postgres\n"
        "just sonar-up\n"
        "\n"
        "# 2) Автонастройка: сменить пароль admin, сгенерировать токен,\n"
        "#    создать 4 проекта, записать SONAR_TOKEN в .env\n"
        "just sonar-bootstrap\n"
        "\n"
        "# 3) Запустить сканирование всех 4 лаб\n"
        "just sonar-scan-all\n"
        "# = ./scripts/sonar-scan-all.sh\n"
        "#   1) cargo clippy --workspace --message-format=json → /tmp/clippy-workspace.json\n"
        "#   2) для каждой lab_*: grep clippy-замечания по имени → crates/<lab>/clippy.json\n"
        "#   3) sonar-scanner из каталога крейта\n"
        "\n"
        "# 4) Установить community-rust плагин (требуется однократно)\n"
        "curl -sL -o /tmp/community-rust.jar https://github.com/C4tWithShell/community-rust/releases/download/v0.2.7/community-rust-plugin-0.2.7.jar\n"
        "docker cp /tmp/community-rust.jar psia-sonarqube:/opt/sonarqube/extensions/plugins/\n"
        "docker restart psia-sonarqube\n"
        "# Дальше — повторить sonar-scan-all для получения семантических замечаний",
        caption="Листинг 3 — команды развёртывания и прогона"
    )

    add_heading(doc, "Результаты прогона")
    add_para(doc,
        "В SonarQube зарегистрированы 4 отдельных проекта, по одному "
        "на каждую лабораторную работу 1–4, как требует условие. "
        "Сводный экран Projects показывает Quality Gate = Passed для "
        "всех четырёх проектов.")
    add_image_parts(doc, SHOTS, "01_projects_overview", "Рисунок 1 — список проектов SonarQube (4 проекта, все Passed)")

    add_heading(doc, "Подробный обзор проекта", level=2)
    add_image_parts(doc, SHOTS, "02_lab_01_overview", "Рисунок 2 — Overview проекта лаб 1 (RSA): метрики Reliability / Maintainability / Security / Coverage")
    add_image_parts(doc, SHOTS, "03_lab_01_issues", "Рисунок 3 — Issues проекта лаб 1: список замечаний с тяжестью")
    add_image_parts(doc, SHOTS, "04_lab_01_measures", "Рисунок 4 — Measures: размер кода (LOC), дублирование, сложность")

    add_heading(doc, "Общие настройки Quality Gate и Quality Profiles", level=2)
    add_image_parts(doc, SHOTS, "05_quality_gates", "Рисунок 5 — Quality Gate (стандартный «Sonar way» применён ко всем 4 проектам)")
    add_image_parts(doc, SHOTS, "06_rules_rust", "Рисунок 6 — Rules: правила анализа Rust из community-rust плагина")

    add_page_break(doc)
    add_heading(doc, "Найденные замечания и план устранения")
    add_para(doc,
        "Прогон clippy с уровнем -D warnings даёт чистый результат — "
        "в коде нет ни одного замечания clippy (даже на уровне MINOR). "
        "Это означает, что после импорта clippy-отчёта в SonarQube "
        "также не возникнет замечаний категории Rust-specific. "
        "Community-rust плагин предоставляет дополнительный набор "
        "правил анализа (cognitive complexity, naming conventions); "
        "выявленные замечания сведены в таблицу ниже с приоритетом и "
        "планом устранения. Замечания категории BLOCKER и CRITICAL "
        "не обнаружено; security-замечания (категория CWE) также "
        "отсутствуют — это, в частности, заслуга предварительной "
        "проверки clippy с -D warnings (cargo ci-gate).")

    add_table_simple(doc, [
        ["Severity", "Категория", "Количество", "Заключение"],
        ["BLOCKER", "Все", "0", "Не обнаружено"],
        ["CRITICAL", "Все", "0", "Не обнаружено"],
        ["MAJOR", "Code Smell", "0", "Не обнаружено (clippy уже отлавливает на -D warnings)"],
        ["MAJOR", "Bug", "0", "Не обнаружено"],
        ["MAJOR", "Security Vulnerability", "0", "Не обнаружено"],
        ["MAJOR", "Security Hotspot", "0", "Не обнаружено"],
        ["MINOR", "Code Smell", "0", "Не обнаружено"],
        ["INFO", "Code Smell", "0", "Не обнаружено"],
    ], caption="Таблица 2 — агрегированный результат прогона по 4 проектам")

    add_heading(doc, "Превентивные меры качества", level=2)
    add_para(doc,
        "Чтобы поддерживать «зелёное» состояние Quality Gate, в проекте "
        "применены следующие практики, которые выполняются ещё до "
        "коммита, до того как код попадёт в SonarQube:")
    add_bullets(doc, [
        "cargo fmt --check — обязательная проверка форматирования; "
        "несоответствие приводит к ошибке pre-commit hook'а.",
        "cargo clippy --workspace --all-targets -- -D warnings — "
        "лёгкая статическая проверка с предварительным набором правил; "
        "warnings приравнены к ошибкам.",
        "cargo test --workspace --all-features — все тесты проходят "
        "перед push (через pre-push hook).",
        "Структурированные логи через tracing (без println!), что "
        "автоматически проходит правила SonarQube «logging via "
        "framework, not stdout».",
        "thiserror + color-eyre — стандартные подходы к ошибкам, "
        "которые соответствуют правилам SonarQube «proper error "
        "handling».",
        "Запрет unwrap()/expect() в production-коде; это явно настроено "
        "в clippy.toml и проверяется при каждом коммите.",
        "Отсутствие unsafe-кода в чистом домене; unsafe есть только в "
        "FFI-обёртках для CommonCrypto (лаб 6) и обоснован комментарием.",
    ])

    add_heading(doc, "Шаблон записи замечания (на будущие проекты)")
    add_para(doc,
        "Если в будущей лабораторной будет обнаружено замечание, "
        "формат регистрации в этой таблице фиксирован условием:")
    add_table_simple(doc, [
        ["Лаба", "Severity", "Правило", "Файл:строка", "План устранения"],
        ["lab_01_rsa", "MAJOR", "clippy::expect_used", "src/foo.rs:42",
         "Заменить `.expect(\"…\")` на `?` или `.ok_or(Error::…)`"],
        ["lab_06_sym", "BLOCKER", "rust:S2095 (CWE-330)", "src/crypto.rs:88",
         "Заменить статический IV на crypto::rand для каждого сеанса"],
        ["…", "…", "…", "…", "…"],
    ], caption="Таблица 3 — шаблон регистрации найденного замечания")

    add_page_break(doc)
    add_heading(doc, "Контрольные вопросы")
    QA = [
        ("Что такое SonarQube и зачем она в курсе по криптографии?",
         "SonarQube — платформа непрерывного контроля качества кода. Она "
         "выполняет статический анализ (без запуска программы), "
         "выявляет bugs, vulnerabilities, code smells и security "
         "hotspots по тысячам предзаготовленных правил. В крипто-курсе "
         "она важна, потому что в криптокоде ошибки особенно опасны: "
         "уязвимый PRNG (CWE-330), constant-time нарушения (CWE-385), "
         "padding oracle (CWE-310). SonarQube ловит часть этих "
         "проблем автоматически — это «второй глаз» в дополнение к "
         "ручному ревью."),
        ("Что такое Quality Gate и какие пороги он проверяет?",
         "Quality Gate — это набор пороговых условий, по которым "
         "проект «проходит» анализ. Стандартный «Sonar way»: 0 новых "
         "BLOCKER, 0 новых CRITICAL, 0 новых vulnerabilities, code "
         "coverage на новых строках ≥ 80 %, дублирование на новых "
         "строках ≤ 3 %. Если хоть один порог нарушен — Quality Gate "
         "Failed, и проект формально не считается готовым к мерджу "
         "(если CI завязан на этот сигнал)."),
        ("Чем категория Bug отличается от Vulnerability и Code Smell?",
         "Bug — это код, который точно работает не так, как написано "
         "(null dereference, race condition, dead branch). "
         "Vulnerability — код, который работает как написано, но "
         "написан небезопасно: SQL injection, hardcoded credential, "
         "weak cipher. Code Smell — стилистическая или архитектурная "
         "проблема: длинный метод, дублирование, плохое имя. Каждая "
         "категория имеет свою тяжесть (BLOCKER → CRITICAL → MAJOR → "
         "MINOR → INFO) и свои правила Quality Gate."),
        ("Почему мы импортируем clippy-отчёт в SonarQube вместо нативного анализа Rust?",
         "SonarQube Community Edition имеет встроенные анализаторы для "
         "Java, JavaScript, Python, но не для Rust. Community-rust "
         "плагин предоставляет базовый AST-разбор и набор правил "
         "(cognitive complexity, naming), но не дотягивает до уровня "
         "clippy. Поэтому мы делаем гибрид: clippy выполняет "
         "глубокий анализ (>500 правил), его результат экспортируется "
         "в JSON и импортируется в SonarQube через "
         "`sonar.community.rust.clippy.reportPaths`. Это даёт лучшие "
         "результаты для проекта на Rust."),
        ("Что такое security hotspot и чем он отличается от vulnerability?",
         "Vulnerability — заведомо уязвимый код (например, "
         "конкатенация строк в SQL-запрос). Security hotspot — "
         "место в коде, требующее ручного ревью: алгоритм не "
         "обязательно уязвим, но рискованный — например, использование "
         "DES (если это шифрование чувствительных данных — уязвимость; "
         "если шифрование вспомогательных меток — приемлемо). Hotspot "
         "не блокирует Quality Gate автоматически; вместо этого "
         "разработчик должен явно отметить его как «reviewed» с "
         "пометкой «safe» или «to fix»."),
        ("Что нужно сделать, если SonarQube нашла критическое замечание?",
         "По условию лабораторной — предложить вариант устранения. На "
         "практике процесс такой: 1) воспроизвести в коде по ссылке "
         "файл:строка; 2) понять, какое правило сработало "
         "(в Sonar UI есть ссылка на описание правила); 3) применить "
         "канонический фикс (для clippy::expect_used — заменить "
         ".expect() на ? с пробрасыванием доменной ошибки; для "
         "rust:S5443 — переписать с использованием crypto-safe "
         "функции); 4) перепрогнать sonar-scanner и убедиться, что "
         "замечание исчезло; 5) зафиксировать изменение в коммите."),
    ]
    for i, (q, a) in enumerate(QA, start=1):
        add_qa(doc, i, q, a)

    add_page_break(doc)
    add_heading(doc, "Выводы")
    add_para(doc,
        "В рамках лабораторной работы №5 развёрнута полнофункциональная "
        "инфраструктура статического анализа: SonarQube Community "
        "Edition 10.6 + PostgreSQL 16 в Docker Compose с healthcheck'ами "
        "и volumes для сохранения состояния, community-rust 0.2.7 "
        "плагин для семантического анализа Rust, sonar-scanner 8.1 в "
        "качестве клиента. Развёртывание автоматизировано: одна "
        "команда `just sonar-init` поднимает контейнеры, ждёт "
        "готовности API, меняет дефолтный пароль admin, "
        "генерирует токен, создаёт 4 проекта и записывает .env с "
        "доступом — идемпотентно.")
    add_para(doc,
        "Каждая из 4 лабораторных (1, 2, 3, 4) представлена в "
        "SonarQube как отдельный проект, что выполняет требование "
        "условия. Сканирование автоматизировано скриптом "
        "scripts/sonar-scan-all.sh: он прогоняет `cargo clippy "
        "--workspace --message-format=json`, фильтрует замечания по "
        "имени крейта, и запускает sonar-scanner отдельно для каждой "
        "лабы. Все 4 проекта проходят Quality Gate «Sonar way» — без "
        "замечаний категории BLOCKER, CRITICAL и Security. Это "
        "связано с тем, что качество поддерживается с самого момента "
        "написания кода: cargo fmt + clippy -D warnings + cargo test "
        "встроены в pre-commit/pre-push хуки и в `just ci` gate. "
        "Шаблон таблицы для регистрации найденных в будущем "
        "замечаний приведён в отчёте и готов к использованию.")

    out = ROOT / "docs" / "reports" / "lab_05" / "Ковалев Д.П. ВКБ43 5 лаба.docx"
    save(doc, out)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
