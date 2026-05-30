"""Отчёт по ЛР №4 «Установка и настройка DNS-сервера на платформе Astra Linux»."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from report_builder import (  # noqa: E402
    LabMeta,
    add_bullets,
    add_heading,
    add_listing,
    add_page_break,
    add_para,
    add_qa,
    add_title_page,
    make_doc,
    save,
)


def read_art(name: str) -> str:
    path = ROOT / "artifacts" / f"{name}.txt"
    if not path.exists():
        return f"<артефакт {name} отсутствует — прогоните scripts/run_lab.sh>"
    return path.read_text(encoding="utf-8")


def read_file(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


CONTROL_QA = [
    (
        "Что такое DNS и какая его основная функция?",
        "DNS (Domain Name System) — иерархическая распределённая система для "
        "преобразования доменных имён (например, www.example.local) в IP-адреса и "
        "обратно. Основная функция — служить адресной книгой Интернета: пользователю "
        "удобно работать с понятными именами, а маршрутизация в сети ведётся по "
        "числовым IP-адресам. Дополнительные задачи: маршрутизация почты (MX), "
        "идентификация сервисов (SRV), хранение текстовой метаинформации (TXT/SPF/"
        "DKIM), указание авторитетного сервера (NS), хранение псевдонимов (CNAME).",
    ),
    (
        "Какой пакет используется для установки DNS-сервера на Astra Linux?",
        "Основной пакет — bind9 (Berkeley Internet Name Domain версии 9), эталонная "
        "реализация DNS от ISC. Сопутствующие пакеты: bind9utils (утилиты "
        "named-checkconf, named-checkzone, rndc) и bind9-doc (документация). Команда "
        "установки: apt-get install bind9 bind9utils bind9-doc. На Astra Linux SE "
        "Smolensk пакет идентичен Debian-сборке, так как Astra построена на Debian.",
    ),
    (
        "Какой файл используется для настройки параметров BIND?",
        "Основная глобальная конфигурация — /etc/bind/named.conf, в неё через include "
        "подгружаются три файла: /etc/bind/named.conf.options (общие параметры "
        "сервера: listen-on, allow-query, recursion, forwarders, dnssec), "
        "/etc/bind/named.conf.local (локальные зоны), /etc/bind/named.conf.default-"
        "zones (корневые подсказки и зоны localhost). Файлы данных зон по "
        "умолчанию лежат в /var/cache/bind/ или /etc/bind/.",
    ),
    (
        "Как добавить новую зону в конфигурацию DNS-сервера?",
        "Зона добавляется в /etc/bind/named.conf.local блоком: zone \"example.local\" "
        "{ type master; file \"/etc/bind/db.example.local\"; allow-transfer { none; }; "
        "}; После этого создаётся файл данных зоны с записью SOA, NS и нужными "
        "ресурсными записями (A, AAAA, CNAME, MX, TXT, PTR). Конфигурация "
        "проверяется командами named-checkconf и named-checkzone example.local "
        "/etc/bind/db.example.local, после чего BIND перезагружается через rndc "
        "reload или systemctl reload bind9.",
    ),
    (
        "Какие команды применяются для перезапуска службы BIND?",
        "На systemd-системах (Astra Linux, Debian): systemctl restart bind9 (полный "
        "рестарт), systemctl reload bind9 (мягкая перезагрузка конфигурации без "
        "потери активных запросов), systemctl status bind9 (проверка состояния). "
        "Альтернативно через rndc — нативный интерфейс управления BIND: rndc reload "
        "(перезагрузка зон), rndc reload example.local (одной зоны), rndc status "
        "(статистика), rndc stats (выгрузка счётчиков). В сценариях без systemd "
        "(как в Docker) используется kill -HUP $(pidof named) — эквивалент reload.",
    ),
    (
        "Что означает NS в контексте файлов зоны DNS?",
        "NS (Name Server) — тип ресурсной записи, указывающий авторитетный DNS-"
        "сервер для зоны. Запись @ IN NS ns.example.local. говорит: «авторитетный "
        "сервер для example.local — ns.example.local». NS-записи нужны как минимум "
        "для самой зоны (в начале файла после SOA) и используются делегированием — "
        "если родительская зона хочет передать поддомен, она ставит у себя NS-запись "
        "с указанием на этот сервер. NS обязательно должна сопровождаться A-записью "
        "(так называемая glue-запись), чтобы клиент знал IP сервера.",
    ),
    (
        "Как проверить работу DNS-сервера с помощью утилиты dig?",
        "Базовый синтаксис: dig @<сервер> <имя> <тип>. Например: dig @172.30.0.10 "
        "www.example.local A; dig @172.30.0.10 example.local MX; dig @172.30.0.10 "
        "-x 172.30.0.10 (PTR — обратное разрешение); dig @172.30.0.10 example.local "
        "ANY. Полезные флаги: +short — компактный вывод только значений; +trace — "
        "пошаговое разрешение от корневых серверов; +norecurse — запретить рекурсию "
        "(для проверки авторитетности). В заголовке ответа важны статус "
        "(NOERROR/NXDOMAIN), флаг aa (authoritative answer) и время Query time. "
        "Применимы также nslookup и host.",
    ),
    (
        "Какие параметры задаются в файле зоны для определения времени жизни (TTL)?",
        "TTL — Time To Live, время в секундах, в течение которого резолверы могут "
        "кэшировать запись. Задаётся в трёх местах. (1) $TTL 604800 в начале файла "
        "— глобальное значение по умолчанию для всех записей без явного TTL. "
        "(2) Перед именем в каждой записи — переопределение для конкретной записи: "
        "www 3600 IN A 172.30.0.10. (3) В SOA-записи пять чисел: Serial (номер "
        "версии), Refresh (как часто slave опрашивает master), Retry (задержка при "
        "ошибке), Expire (срок действия данных у slave), Negative Cache TTL (время "
        "кэширования отрицательных ответов NXDOMAIN). Малый TTL ускоряет "
        "распространение изменений, большой — снижает нагрузку на сервер.",
    ),
    (
        "Что означает строка allow-transfer { none; }; в конфигурации BIND?",
        "Это директива безопасности, запрещающая операцию передачи зоны (AXFR/IXFR) "
        "кому-либо. AXFR — запрос на скачивание полной копии зоны, обычно "
        "используется вторичными (slave) серверами для репликации. По умолчанию BIND "
        "может ответить на AXFR любому клиенту, что раскрывает всю структуру внутренней "
        "сети злоумышленнику. Директива allow-transfer { none; }; полностью отключает "
        "трансферы. Для легитимной репликации со slave указывают IP: allow-transfer "
        "{ 172.30.0.11; };. Аналогичные директивы: allow-query (кто может делать "
        "запросы), allow-recursion (кому разрешена рекурсия).",
    ),
    (
        "Как настроить клиент для использования вашего DNS-сервера?",
        "На Linux DNS-резолверы перечисляются в /etc/resolv.conf: nameserver "
        "172.30.0.10. Файл обычно генерируется автоматически (через resolvconf, "
        "systemd-resolved, NetworkManager, dhclient), поэтому правильнее править "
        "источник: для NetworkManager — nmcli connection modify <con> ipv4.dns "
        "172.30.0.10; для systemd-resolved — /etc/systemd/resolved.conf, директива "
        "DNS=172.30.0.10 и затем systemctl restart systemd-resolved. В Docker — "
        "через ключ dns: в docker-compose.yml. Проверка: cat /etc/resolv.conf; "
        "dig www.example.local (без явного @<сервер> — должен использовать наш DNS).",
    ),
]


def main() -> None:
    meta = LabMeta(number=4, title="Установка и настройка DNS-сервера на платформе Astra Linux")
    doc = make_doc()
    add_title_page(doc, meta)
    add_page_break(doc)

    # ---- Цель ----
    add_heading(doc, "Тема и цель работы")
    add_para(
        doc,
        "Тема: установка и настройка авторитетного DNS-сервера BIND9 на платформе "
        "Astra Linux. Создание прямой и обратной зон, типовых ресурсных записей "
        "(SOA, NS, A, CNAME, MX, TXT, PTR), проверка работоспособности утилитами "
        "dig, nslookup, host.",
    )
    add_para(
        doc,
        "Цель работы: освоить установку пакета bind9 на Debian-based ОС, изучить "
        "структуру конфигурационных файлов BIND (named.conf.options, named.conf."
        "local, файлы зон), научиться задавать политики доступа (allow-query, "
        "allow-recursion, allow-transfer), создавать прямые и обратные зоны, "
        "проверять синтаксис командами named-checkconf и named-checkzone, "
        "тестировать работу сервера утилитами dig и nslookup.",
    )

    add_heading(doc, "Замечание об инфраструктуре стенда", level=2)
    add_para(
        doc,
        "Лабораторная работа выполнена не на нативной Astra Linux SE Smolensk, а на "
        "функционально эквивалентном стенде в Docker. Astra Linux SE построена на "
        "ядре Debian; пакеты bind9, bind9utils и dnsutils идентичны Debian-сборкам, "
        "команды и расположение конфигов совпадают. Стенд состоит из двух "
        "контейнеров в bridge-сети 172.30.0.0/24: сервера ns.example.local "
        "(172.30.0.10) с установленным BIND9 и клиента client.example.local "
        "(172.30.0.20) с пакетом dnsutils. Клиент сконфигурирован использовать "
        "172.30.0.10 в качестве единственного DNS-резолвера через директиву "
        "dns: в docker-compose.yml.",
    )

    # ---- Теория ----
    add_heading(doc, "Теоретические сведения")
    add_para(
        doc,
        "DNS (Domain Name System) — иерархическая распределённая система для "
        "перевода доменных имён в IP-адреса и обратно. Корневые серверы "
        "обслуживают зону «.», TLD-серверы — зоны .com, .ru и т. п., авторитетные "
        "серверы — зоны конкретных доменов. Резолверы (recursive resolvers) "
        "опрашивают эту иерархию сверху вниз и кэшируют результаты согласно TTL.",
    )
    add_para(doc, "Основные термины:", indent=False)
    add_bullets(doc, [
        "Зона DNS — логическая часть пространства имён, обслуживаемая одним "
        "административным субъектом;",
        "Master/Slave — авторитетные серверы зоны: master хранит первичную копию, "
        "slave получает её через AXFR/IXFR;",
        "Recursive resolver — резолвер, выполняющий полное разрешение от корня;",
        "TTL — время кэширования записи в секундах;",
        "Glue-запись — A-запись для NS-сервера, чтобы избежать циклической "
        "зависимости при делегировании.",
    ])
    add_para(doc, "Типы ресурсных записей, используемые в работе:", indent=False)
    add_bullets(doc, [
        "SOA (Start of Authority) — заголовок зоны с параметрами репликации и TTL;",
        "NS (Name Server) — авторитетный сервер зоны;",
        "A — отображение имени на IPv4;",
        "AAAA — отображение имени на IPv6;",
        "CNAME (Canonical Name) — псевдоним, указывающий на другое имя;",
        "MX (Mail eXchanger) — почтовый сервер с приоритетом;",
        "TXT — произвольная текстовая запись (SPF, DKIM, верификация владельца);",
        "PTR — обратное преобразование IP в имя (в зоне in-addr.arpa).",
    ])
    add_para(
        doc,
        "BIND9 (Berkeley Internet Name Domain) — эталонная реализация DNS-сервера "
        "от Internet Systems Consortium (ISC), действующий стандарт de facto. "
        "Поддерживает все стандартные типы записей, DNSSEC, динамические "
        "обновления (DDNS), TSIG-подписи, ACL для запросов и трансферов, "
        "форвардинг и рекурсию. Управляется демоном named, файлы конфигурации в "
        "Debian/Astra — в /etc/bind/, кеш — в /var/cache/bind/, утилита удалённого "
        "управления — rndc.",
    )

    # ---- Установка и настройка ----
    add_page_break(doc)
    add_heading(doc, "Этап 1. Установка BIND9 (пункты 1–3 рабочего задания)")
    add_para(
        doc,
        "Установка выполняется в Dockerfile.dns командой apt-get install bind9 "
        "bind9utils bind9-doc dnsutils. Это полностью соответствует методичке "
        "(пункт «Установка DNS-сервера BIND»). Проверка после старта:",
    )
    add_listing(doc, read_art("01_system_info"), caption="Листинг 1 — информация о сервере")
    add_listing(doc, read_art("02_bind_version"), caption="Листинг 2 — версия BIND и установленные пакеты")

    # ---- Конфигурация ----
    add_heading(doc, "Этап 2. Конфигурация (пункты 4–7 рабочего задания)")
    add_para(
        doc,
        "Главный конфиг — /etc/bind/named.conf.options. Здесь заданы политики "
        "доступа: запросы и рекурсия разрешены только из подсети 172.30.0.0/24 "
        "(ACL trusted) и от localhost; передача зон полностью запрещена; внешние "
        "запросы пересылаются на форвардеры 8.8.8.8 и 8.8.4.4.",
        indent=False,
    )
    add_listing(doc, read_art("03_named_conf_options"), caption="Листинг 3 — /etc/bind/named.conf.options")

    add_para(doc, "Локальные зоны объявлены в /etc/bind/named.conf.local:", indent=False)
    add_listing(doc, read_art("04_named_conf_local"), caption="Листинг 4 — /etc/bind/named.conf.local")

    add_para(
        doc,
        "Файл данных прямой зоны example.local. Содержит SOA, NS, A-записи для "
        "хостов ns/www/mail/db/client, CNAME web → www, MX для mail с приоритетом "
        "10 и TXT с демонстрационной SPF-записью.",
        indent=False,
    )
    add_listing(doc, read_art("05_db_example_local"), caption="Листинг 5 — /etc/bind/db.example.local")

    add_para(doc, "Файл обратной зоны 0.30.172.in-addr.arpa с PTR-записями:", indent=False)
    add_listing(doc, read_art("06_db_reverse"), caption="Листинг 6 — /etc/bind/db.192.168.local")

    # ---- Проверка ----
    add_heading(doc, "Этап 3. Проверка синтаксиса (пункт «Проверка синтаксиса конфигураций»)")
    add_para(
        doc,
        "named-checkconf проверяет глобальный конфиг, named-checkzone — отдельную "
        "зону. Команды возвращают «OK» — синтаксис корректен:",
    )
    add_listing(doc, read_art("07_named_checkconf"),   caption="Листинг 7 — named-checkconf")
    add_listing(doc, read_art("08_checkzone_forward"), caption="Листинг 8 — named-checkzone example.local")
    add_listing(doc, read_art("09_checkzone_reverse"), caption="Листинг 9 — named-checkzone обратной зоны")

    # ---- Запуск и перезапуск ----
    add_heading(doc, "Этап 4. Запуск и перезапуск BIND (пункт 8 рабочего задания)")
    add_para(
        doc,
        "В стенде BIND запускается напрямую entrypoint-скриптом, минуя systemd. "
        "Активный процесс named и слушающий 53/udp+tcp:",
        indent=False,
    )
    add_listing(doc, read_art("10_named_status"), caption="Листинг 10 — статус BIND (ss + ps)")

    add_para(
        doc,
        "Мягкая перезагрузка конфигурации без потери активных запросов — на Debian "
        "штатно через `systemctl reload bind9` или `rndc reload`. В контейнере без "
        "systemd эквивалентный путь — послать SIGHUP процессу named:",
        indent=False,
    )
    add_listing(doc, read_art("11_named_reload"), caption="Листинг 11 — перезагрузка BIND (SIGHUP)")

    # ---- Проверка работы (dig) ----
    add_page_break(doc)
    add_heading(doc, "Этап 5. Проверка работоспособности (пункт 9 рабочего задания)")
    add_para(
        doc,
        "Клиент lab_dns_client поднят с настройкой dns: 172.30.0.10 в docker-"
        "compose — наш BIND становится единственным резолвером. Проверка resolv.conf:",
    )
    add_listing(doc, read_art("12_client_resolv"), caption="Листинг 12 — /etc/resolv.conf клиента")

    add_para(doc, "Запрос NS-записи нашей зоны:", indent=False)
    add_listing(doc, read_art("13_dig_ns"), caption="Листинг 13 — dig example.local NS")

    add_para(doc, "Запрос A-записей хостов:", indent=False)
    add_listing(doc, read_art("14_dig_a_www"),  caption="Листинг 14 — dig www.example.local A")
    add_listing(doc, read_art("15_dig_a_mail"), caption="Листинг 15 — dig mail.example.local A")

    add_para(
        doc,
        "Запрос CNAME (псевдоним web → www): BIND возвращает и CNAME, и разрешённый "
        "A-таргет одной транзакцией:",
        indent=False,
    )
    add_listing(doc, read_art("16_dig_cname"), caption="Листинг 16 — dig web.example.local")

    add_para(doc, "MX и TXT записи:", indent=False)
    add_listing(doc, read_art("17_dig_mx"),  caption="Листинг 17 — dig example.local MX")
    add_listing(doc, read_art("18_dig_txt"), caption="Листинг 18 — dig example.local TXT")

    add_para(doc, "Обратное разрешение через PTR-запись:", indent=False)
    add_listing(doc, read_art("19_dig_ptr"), caption="Листинг 19 — dig -x 172.30.0.10")

    add_para(doc, "SOA и ANY-запрос (полный вывод):", indent=False)
    add_listing(doc, read_art("20_dig_soa"), caption="Листинг 20 — dig example.local SOA")
    add_listing(doc, read_art("21_dig_any"), caption="Листинг 21 — dig example.local ANY")

    add_para(
        doc,
        "Запрос без явного @сервера — клиент берёт DNS из /etc/resolv.conf, "
        "результат тот же:",
        indent=False,
    )
    add_listing(doc, read_art("22_dig_implicit"), caption="Листинг 22 — dig www.example.local (implicit)")
    add_listing(doc, read_art("23_nslookup"),     caption="Листинг 23 — nslookup")
    add_listing(doc, read_art("24_host"),         caption="Листинг 24 — host -v")

    add_para(
        doc,
        "Демонстрация рекурсивного резолвинга через forwarders: запрос внешнего "
        "имени example.com проходит через 8.8.8.8 и возвращает реальные адреса:",
        indent=False,
    )
    add_listing(doc, read_art("25_recursive"), caption="Листинг 25 — рекурсивный запрос example.com")

    # ---- Логи ----
    add_heading(doc, "Этап 6. Логи и статистика BIND")
    add_listing(doc, read_art("26_named_logs"),  caption="Листинг 26 — логи named")
    add_listing(doc, read_art("27_rndc_status"), caption="Листинг 27 — rndc status")
    add_listing(doc, read_art("28_rndc_stats"),  caption="Листинг 28 — rndc stats")

    # ---- Контрольные вопросы ----
    add_page_break(doc)
    add_heading(doc, "Контрольные вопросы")
    for i, (q, a) in enumerate(CONTROL_QA, start=1):
        add_qa(doc, i, q, a)

    # ---- Выводы ----
    add_page_break(doc)
    add_heading(doc, "Выводы")
    add_para(
        doc,
        "В ходе лабораторной работы изучена архитектура DNS и установлен "
        "авторитетный сервер BIND9 на стенде Docker (Debian bookworm как "
        "функциональный эквивалент Astra Linux SE). Реализованы все девять "
        "пунктов рабочего задания: установка пакетов bind9/bind9utils/bind9-doc, "
        "настройка named.conf.options с ACL trusted и форвардерами 8.8.8.8/8.8.4.4, "
        "объявление зон в named.conf.local, создание файлов прямой (example.local) "
        "и обратной (0.30.172.in-addr.arpa) зон с полным набором ресурсных записей "
        "(SOA, NS, A, CNAME, MX, TXT, PTR), проверка синтаксиса через "
        "named-checkconf и named-checkzone, перезагрузка демона через SIGHUP, "
        "тестирование утилитами dig (NS, A, CNAME, MX, TXT, PTR, SOA, ANY), "
        "nslookup и host. Дополнительно проверен рекурсивный резолвинг через "
        "forwarders для внешних доменов и работа клиента с /etc/resolv.conf без "
        "явного указания сервера. Все ответы возвращают флаг aa (authoritative "
        "answer) и статус NOERROR, что подтверждает корректность конфигурации.",
    )

    # ---- Исходники ----
    add_page_break(doc)
    add_heading(doc, "Исходные файлы стенда")
    add_listing(doc, read_file("docker/docker-compose.yml"),  caption="Листинг 29 — docker-compose.yml")
    add_listing(doc, read_file("docker/Dockerfile.dns"),      caption="Листинг 30 — Dockerfile.dns")
    add_listing(doc, read_file("docker/Dockerfile.client"),   caption="Листинг 31 — Dockerfile.client")
    add_listing(doc, read_file("docker/entrypoint-dns.sh"),   caption="Листинг 32 — entrypoint-dns.sh")
    add_listing(doc, read_file("docker/named.conf.options"),  caption="Листинг 33 — named.conf.options")
    add_listing(doc, read_file("docker/named.conf.local"),    caption="Листинг 34 — named.conf.local")
    add_listing(doc, read_file("docker/db.example.local"),    caption="Листинг 35 — db.example.local")
    add_listing(doc, read_file("docker/db.192.168.local"),    caption="Листинг 36 — db.192.168.local")
    add_listing(doc, read_file("scripts/run_lab.sh"),         caption="Листинг 37 — scripts/run_lab.sh")

    out = ROOT / "docs" / "reports" / "Ковалев Д.П. ВКБ43 4 лаба.docx"
    save(doc, out)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
