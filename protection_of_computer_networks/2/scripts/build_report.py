"""Отчёт по ЛР №2 «Настройка межсетевого экрана».

Стенд имитируется в Docker: server (debian + ufw + sshd + nginx) и client
(debian + ssh-client + curl) в bridge-сети 172.28.0.0/24. Все команды лабы
прогоняются скриптом scripts/run_lab.sh, а вывод каждой команды кладётся
в artifacts/NN_*.txt — отсюда и собираются листинги отчёта.
"""

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
        "Что такое ОС Astra Linux SE?",
        "Astra Linux Special Edition — операционная система специального назначения, "
        "разработанная АО «НПО РусБИТех» совместно с Академией ФСБ России и ИСП РАН. "
        "Сертифицирована ФСТЭК и Минобороны РФ, имеет встроенные средства защиты "
        "информации, в том числе мандатный контроль целостности (МКЦ) и мандатное "
        "разграничение доступа (МРД), и предназначена для построения автоматизированных "
        "систем, обрабатывающих сведения, содержащие государственную тайну, в том числе "
        "с грифом «особой важности».",
    ),
    (
        "Какие существуют версии Astra Linux SE?",
        "Три версии по уровню защищённости: «Орёл» (базовый, без МКЦ и МРД), "
        "«Воронеж» (усиленный, есть МКЦ, нет МРД) и «Смоленск» (максимальный, есть "
        "и МКЦ, и МРД). В работе рассматривалась версия Astra Linux SE «Смоленск».",
    ),
    (
        "Что такое брандмауэр?",
        "Брандмауэр (межсетевой экран, firewall) — программно-аппаратный комплекс, "
        "контролирующий и фильтрующий проходящий через него сетевой трафик согласно "
        "заданным правилам. Решает задачи защиты сегмента сети от несанкционированных "
        "подключений, ограничения доступа к сервисам и ведения журнала сетевых событий.",
    ),
    (
        "Как можно настроить межсетевой экран (виды настройки)?",
        "В Astra Linux SE Smolensk доступны три способа: (1) графическая утилита gufw "
        "(«Пуск → Панель управления → Прочее → Настройка межсетевого экрана») с "
        "профилями «дом / офис / общественное место»; (2) консольная обёртка "
        "astra-ufw-control (enable/status/allow/deny/reset/disable); (3) низкоуровневое "
        "управление netfilter через iptables — команды -A/-D/-I/-L/-P, iptables-save/restore.",
    ),
    (
        "Как создать правило в iptables на запрет подключения к порту SSH?",
        "iptables -A INPUT -p tcp --dport 22 -j DROP — добавляет в конец цепочки INPUT "
        "правило, отбрасывающее все TCP-пакеты на порт 22. Если требуется блокировать "
        "конкретный источник: iptables -A INPUT -s 192.168.1.5 -p tcp --dport 22 -j DROP. "
        "Для приоритета над уже разрешающими правилами используют -I INPUT 1 — вставка "
        "в начало цепочки.",
    ),
    (
        "С помощью каких команд создаются запреты и разрешения в утилите iptables?",
        "Разрешение: iptables -A <цепочка> ... -j ACCEPT. Запрет: -j DROP (тихо "
        "отбрасывает) или -j REJECT (отвечает ICMP unreachable). Удаление правила: "
        "-D <цепочка> ... (с теми же параметрами, что и при добавлении). Установка "
        "политики по умолчанию: -P <цепочка> ACCEPT|DROP. Вставка в произвольную "
        "позицию: -I <цепочка> <N> ... -j ACCEPT|DROP.",
    ),
    (
        "Перечислите основные команды для работы с МЭ в ОС Astra Linux SE Smolensk.",
        "astra-ufw-control enable | status | disable | reset, astra-ufw-control "
        "app list, astra-ufw-control allow|deny <приложение или порт>; для низкоуровневой "
        "работы — iptables -L (просмотр), -F (очистка), -A/-D/-I (добавление/удаление/"
        "вставка), -P (политика по умолчанию), -N/-X (создание/удаление цепочки), "
        "iptables-save и iptables-restore (сохранение/восстановление правил).",
    ),
    (
        "В чём отличие между gufw и ufw?",
        "ufw (uncomplicated firewall) — консольная утилита-обёртка над netfilter/iptables, "
        "позволяющая задавать правила декларативно: ufw allow ssh, ufw deny 8080/tcp. "
        "gufw — графическая надстройка (GTK) над ufw: тот же функционал, но через окно "
        "с переключателями профилей, списком правил и журналом событий. По сути gufw "
        "вызывает те же команды ufw, что и пользователь в терминале.",
    ),
    (
        "Для каких профилей в gufw можно настроить МЭ?",
        "В gufw доступны три предустановленных профиля: «Дом» (home), «Офис» (office) и "
        "«Общественное место» (public). Каждый профиль хранит независимый набор политик "
        "по умолчанию (incoming/outgoing) и список разрешённых приложений, что позволяет "
        "быстро переключаться между сценариями использования компьютера.",
    ),
    (
        "В чём отличие Astra Linux SE Smolensk от других версий?",
        "«Смоленск» — версия с максимальным уровнем защищённости. В отличие от «Орла» "
        "(базовый уровень) и «Воронежа» (усиленный, только МКЦ), в «Смоленске» "
        "реализованы и мандатный контроль целостности, и мандатное разграничение "
        "доступа. Это позволяет обрабатывать сведения с грифом «особой важности» и "
        "строить полноценные многоуровневые защищённые системы.",
    ),
]


def main() -> None:
    meta = LabMeta(number=2, title="Настройка межсетевого экрана")
    doc = make_doc()
    add_title_page(doc, meta)
    add_page_break(doc)

    # ---- Цель и условия выполнения ----
    add_heading(doc, "Тема и цель работы")
    add_para(
        doc,
        "Тема: настройка межсетевого экрана в защищённой ОС Astra Linux SE Smolensk "
        "с использованием графической утилиты gufw, консольной обёртки astra-ufw-control "
        "и низкоуровневой подсистемы фильтрации пакетов iptables.",
    )
    add_para(
        doc,
        "Цель работы: ознакомиться с параметрами настройки межсетевого экрана Astra "
        "Linux (ufw и gufw) и модулями iptables, научиться проводить их настройку, "
        "формировать разрешающие и запрещающие правила для типичных сервисов "
        "(SSH, HTTP, HTTPS) и проверять корректность работы межсетевого экрана.",
    )

    add_heading(doc, "Замечание об инфраструктуре стенда", level=2)
    add_para(
        doc,
        "Лабораторная работа выполнена не на нативной Astra Linux SE Smolensk, а на "
        "функционально эквивалентном стенде в Docker. Astra Linux SE построена на ядре "
        "Debian; команды ufw и iptables, рассматриваемые в методичке, идентичны таковым "
        "в Debian/Ubuntu. Команда astra-ufw-control является обёрткой над ufw и вызывает "
        "те же системные действия. Стенд состоит из двух контейнеров в одной bridge-сети "
        "172.28.0.0/24: сервер lab-server (172.28.0.10) с установленными ufw, openssh-server, "
        "nginx с TLS-сертификатом и клиентом lab-client (172.28.0.20). Контейнеру сервера "
        "выданы capabilities NET_ADMIN и NET_RAW, без которых iptables не способен "
        "модифицировать таблицы netfilter.",
    )

    # ---- Теоретическая часть ----
    add_heading(doc, "Теоретические сведения")
    add_para(
        doc,
        "Astra Linux Special Edition — операционная система специального назначения, "
        "сертифицированная ФСТЭК и Минобороны РФ. Имеет три уровня защищённости — "
        "«Орёл» (базовый), «Воронеж» (усиленный, мандатный контроль целостности — МКЦ) "
        "и «Смоленск» (максимальный, дополнительно мандатное разграничение доступа — МРД). "
        "Лабораторная работа выполняется в редакции «Смоленск», поскольку именно она "
        "содержит полноценные средства настройки межсетевого экрана уровня ядра.",
    )
    add_para(
        doc,
        "Межсетевой экран в Astra Linux SE Smolensk реализован на базе netfilter, "
        "управление трафиком ведётся утилитой iptables; для удобной декларативной "
        "настройки используется надстройка ufw (uncomplicated firewall), а для "
        "графического управления — gufw (Gtk-обёртка над ufw). В дистрибутиве также "
        "имеется специфичный скрипт astra-ufw-control, дублирующий команды ufw "
        "(enable/disable/status/allow/deny/reset/app list) для совместимости с "
        "административными политиками Astra.",
    )
    add_para(doc, "Основные команды iptables:", indent=False)
    add_bullets(doc, [
        "iptables -L — просмотр правил во всех цепочках (INPUT, OUTPUT, FORWARD);",
        "iptables -F — полная очистка цепочек;",
        "iptables -A <цепочка> … -j <ACCEPT|DROP|REJECT> — добавление правила в конец;",
        "iptables -I <цепочка> N … — вставка правила в позицию N (приоритет);",
        "iptables -D <цепочка> … — удаление правила;",
        "iptables -P <цепочка> <ACCEPT|DROP> — политика по умолчанию;",
        "iptables -N MYCHAIN / -X MYCHAIN — создание/удаление пользовательской цепочки;",
        "iptables-save > /etc/iptables/rules.v4 — выгрузка текущих правил;",
        "iptables-restore < /etc/iptables/rules.v4 — восстановление правил из файла.",
    ])
    add_para(doc, "Команды astra-ufw-control (обёртка над ufw):", indent=False)
    add_bullets(doc, [
        "astra-ufw-control enable — активировать межсетевой экран;",
        "astra-ufw-control disable — отключить;",
        "astra-ufw-control status — текущее состояние и правила;",
        "astra-ufw-control app list — список профилей приложений;",
        "astra-ufw-control allow <имя|порт> — добавить разрешающее правило;",
        "astra-ufw-control deny <имя|порт> — добавить запрещающее правило;",
        "astra-ufw-control reset — вернуть состояние «по умолчанию».",
    ])

    # ---- Программная часть ----
    add_page_break(doc)
    add_heading(doc, "Выполнение рабочего задания")

    add_para(doc, "Информация о стенде:", indent=False)
    add_listing(
        doc,
        read_art("00_system_info"),
        caption="Листинг 1 — информация о сервере и сетевом интерфейсе",
    )

    add_para(doc, "Шаг 1. Сбрасываем ufw в исходное состояние и проверяем статус.", indent=False)
    add_listing(doc, read_art("01_ufw_reset"), caption="Листинг 2 — сброс ufw")
    add_listing(doc, read_art("02_ufw_status_before"), caption="Листинг 3 — статус ufw после сброса")

    add_para(
        doc,
        "Шаг 2. Задаём политику по умолчанию: входящие соединения запрещены, "
        "исходящие — разрешены. Это рекомендованная для серверных стендов конфигурация.",
        indent=False,
    )
    add_listing(doc, read_art("03_ufw_defaults"), caption="Листинг 4 — политика по умолчанию")

    add_para(
        doc,
        "Шаг 3. Добавляем разрешающие правила для SSH (22), HTTP (80) и HTTPS (443) "
        "согласно пунктам 3.1 и 3.2 рабочего задания. К каждому правилу добавляется "
        "комментарий, чтобы в дальнейшем правила были самодокументируемы.",
        indent=False,
    )
    add_listing(doc, read_art("04_ufw_allow_ssh"), caption="Листинг 5 — разрешение SSH")
    add_listing(doc, read_art("05_ufw_allow_http_https"), caption="Листинг 6 — разрешение HTTP и HTTPS")

    add_para(doc, "Шаг 4. Активируем межсетевой экран и проверяем итоговую конфигурацию.", indent=False)
    add_listing(doc, read_art("06_ufw_enable"), caption="Листинг 7 — активация ufw")
    add_listing(
        doc,
        read_art("07_ufw_status_after"),
        caption="Листинг 8 — статус ufw с нумерованными правилами",
    )

    add_para(
        doc,
        "Шаг 5. Добавляем явное правило iptables для разрешения уже установленных "
        "соединений (состояния ESTABLISHED и RELATED, пункт 3.3 рабочего задания). "
        "ufw создаёт такое правило автоматически в before.rules, однако методичка "
        "требует продемонстрировать команду iptables напрямую.",
        indent=False,
    )
    add_listing(
        doc,
        read_art("08_iptables_established"),
        caption="Листинг 9 — правило для ESTABLISHED/RELATED",
    )

    add_para(doc, "Полный листинг iptables после применения всех правил:", indent=False)
    add_listing(doc, read_art("09_iptables_list"), caption="Листинг 10 — таблицы iptables")

    add_para(
        doc,
        "Шаг 6. Сохраняем правила в файл /etc/iptables/rules.v4, чтобы они "
        "восстанавливались при перезагрузке системы (пункт 4 рабочего задания).",
        indent=False,
    )
    add_listing(
        doc,
        read_art("10_iptables_save"),
        caption="Листинг 11 — выгрузка iptables-save в /etc/iptables/rules.v4",
    )

    # ---- Проверка с клиента ----
    add_page_break(doc)
    add_heading(doc, "Проверка доступности сервисов из внешней сети")
    add_para(
        doc,
        "Все проверки выполнялись с отдельного контейнера lab-client (172.28.0.20), "
        "находящегося в той же bridge-сети, что и сервер. Это эквивалент пунктов 5 и 6 "
        "рабочего задания «проверьте доступность сервера из внешней сети».",
    )

    add_para(doc, "Шаг 7. Проверка ICMP (ping) — должна провалиться, так как ICMP мы не разрешали.", indent=False)
    add_listing(doc, read_art("11_client_ping"), caption="Листинг 12 — ping с клиента (ожидается тайм-аут)")

    add_para(doc, "Шаг 8. Подключение по SSH под пользователем labuser/lab.", indent=False)
    add_listing(doc, read_art("12_client_ssh"), caption="Листинг 13 — SSH-подключение к серверу")

    add_para(doc, "Шаг 9. Проверка HTTP через curl.", indent=False)
    add_listing(doc, read_art("13_client_http"), caption="Листинг 14 — curl http://172.28.0.10/")

    add_para(
        doc,
        "Шаг 10. Проверка HTTPS через curl (используется self-signed сертификат, "
        "поэтому передаётся флаг -k).",
        indent=False,
    )
    add_listing(doc, read_art("14_client_https"), caption="Листинг 15 — curl https://172.28.0.10/")

    add_para(
        doc,
        "Шаг 11. Демонстрация запрета: добавляем правило DROP на порт 8080 и проверяем, "
        "что оно появилось в таблице.",
        indent=False,
    )
    add_listing(
        doc,
        read_art("15_iptables_drop_demo"),
        caption="Листинг 16 — добавление DROP на 8080",
    )

    add_para(
        doc,
        "Шаг 12. Демонстрация запрета SSH через ufw (аналогично команде "
        "astra-ufw-control deny SSH из методички) и проверка, что подключение блокируется.",
        indent=False,
    )
    add_listing(doc, read_art("16_ufw_deny_ssh_demo"), caption="Листинг 17 — запрет SSH в ufw")
    add_listing(
        doc,
        read_art("17_client_ssh_after_deny"),
        caption="Листинг 18 — попытка SSH после запрета (ожидается тайм-аут)",
    )

    add_para(doc, "Шаг 13. Откатываем запрещающее правило и фиксируем финальное состояние.", indent=False)
    add_listing(doc, read_art("18_ufw_delete_deny"), caption="Листинг 19 — удаление запрещающего правила")
    add_listing(doc, read_art("19_final_status"), caption="Листинг 20 — итоговая конфигурация ufw и iptables")

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
        "В ходе лабораторной работы изучены принципы настройки межсетевого экрана "
        "в защищённой ОС Astra Linux SE Smolensk и реализованы все пункты рабочего "
        "задания на функционально эквивалентном стенде Debian/Docker. Освоены три "
        "уровня управления firewall: графическая утилита gufw (рассмотрена теоретически), "
        "консольная обёртка ufw/astra-ufw-control и низкоуровневая утилита iptables. "
        "Сформированы разрешающие правила для SSH (22), HTTP (80), HTTPS (443) и для "
        "уже установленных соединений (ESTABLISHED, RELATED), правила сохранены в "
        "/etc/iptables/rules.v4. Проверена доступность сервисов с клиента: SSH-подключение "
        "под labuser выполняется успешно, HTTP/HTTPS-запросы возвращают корректный "
        "HTML-ответ. На примере запрета порта 8080 и временного запрета SSH "
        "продемонстрировано, что межсетевой экран действительно блокирует трафик, не "
        "соответствующий заданным правилам.",
    )

    # ---- Листинги конфигов и скрипта ----
    add_page_break(doc)
    add_heading(doc, "Исходные файлы стенда")
    add_para(
        doc,
        "Ниже приведены конфигурационные файлы Docker-стенда и скрипт автоматического "
        "прогона лабораторной работы.",
    )
    add_listing(
        doc,
        read_file("docker/docker-compose.yml"),
        caption="Листинг 21 — docker-compose.yml",
    )
    add_listing(
        doc,
        read_file("docker/Dockerfile.server"),
        caption="Листинг 22 — Dockerfile.server",
    )
    add_listing(
        doc,
        read_file("docker/Dockerfile.client"),
        caption="Листинг 23 — Dockerfile.client",
    )
    add_listing(
        doc,
        read_file("docker/entrypoint.sh"),
        caption="Листинг 24 — entrypoint.sh сервера",
    )
    add_listing(
        doc,
        read_file("scripts/run_lab.sh"),
        caption="Листинг 25 — scripts/run_lab.sh",
    )

    out = ROOT / "docs" / "reports" / "Ковалев Д.П. ВКБ43 2 лаба.docx"
    save(doc, out)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
