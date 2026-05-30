"""Отчёт по ЛР №1 «Установка и настройка Kerberos».

Стенд имитирован в Docker: три контейнера (kdc, target, client) в bridge-сети
172.29.0.0/24. KDC поднимает realm LAB.LOCAL, выгружает host-keytab для target
в общий volume, target подбирает keytab при старте и поднимает sshd с GSSAPI.
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
        "В чём заключается основная цель и назначение протокола Kerberos?",
        "Kerberos предназначен для безопасной взаимной аутентификации сторон в "
        "недоверенной сети без передачи пароля. Вместо пароля стороны обмениваются "
        "криптографически защищёнными билетами с ограниченным временем жизни, что "
        "исключает перехват учётных данных и replay-атаки. Протокол реализует модель "
        "Zero Trust: клиент доказывает свою подлинность KDC и получает временный "
        "TGT, затем через TGS получает сервисный билет — конкретно для целевого "
        "сервиса. Сервер также аутентифицирует себя перед клиентом (mutual auth).",
    ),
    (
        "Какие этапы прошёл протокол Kerberos в своём развитии и какие версии существуют?",
        "Kerberos разработан в MIT в рамках проекта Athena в 1980-х. Версия 4 (1989) "
        "использовала только DES, работала только с IP-сетями, не поддерживала "
        "делегирование. Версия 5 (1993, RFC 4120 в 2005) — действующий стандарт: "
        "поддержка AES/Camellia/RC4, любых сетевых протоколов, делегирования прав, "
        "защиты от replay через timestamps и nonce. Используется в Active Directory "
        "(MS-KILE), MIT Kerberos и Heimdal (UNIX), macOS. Существуют расширения для "
        "PKI (PKINIT), федерации, FAST-канала для усиленного предаут.",
    ),
    (
        "Какие компоненты входят в архитектуру Kerberos и каковы их функции?",
        "Архитектура состоит из четырёх компонентов. (1) Клиент — пользователь или "
        "сервис, желающий получить доступ. (2) AS (Authentication Server) — выдаёт "
        "TGT после проверки идентичности клиента. (3) TGS (Ticket Granting Server) — "
        "выдаёт сервисные билеты по предъявленному TGT. AS и TGS вместе образуют KDC "
        "(Key Distribution Center). (4) AP (Application Server) — целевой сервис, "
        "проверяющий сервисный билет и предоставляющий доступ. KDC хранит базу "
        "principal'ов и их долгосрочные ключи.",
    ),
    (
        "Как осуществляется процесс аутентификации в Kerberos от начала до получения доступа к сервису?",
        "Аутентификация состоит из шести шагов. (1) AS-REQ: клиент → AS, запрос TGT "
        "с предаут-блоком (timestamp, зашифрованный паролем). (2) AS-REP: AS → клиент, "
        "TGT, зашифрованный ключом TGS, и сессионный ключ клиент-TGS, зашифрованный "
        "паролем клиента. (3) TGS-REQ: клиент → TGS, TGT + аутентикатор (timestamp, "
        "зашифрованный сессионным ключом) + имя сервиса. (4) TGS-REP: TGS → клиент, "
        "сервисный билет, зашифрованный ключом сервиса, и сессионный ключ клиент-"
        "сервис. (5) AP-REQ: клиент → сервис, сервисный билет + аутентикатор. "
        "(6) AP-REP (опционально): сервис → клиент, подтверждение с timestamp+1 — "
        "взаимная аутентификация.",
    ),
    (
        "Что такое TGT и Service Ticket, какова их роль и как они защищены?",
        "TGT (Ticket Granting Ticket) — «пропуск» в систему Kerberos: содержит ID "
        "клиента, срок действия (обычно 8–24 ч), сессионный ключ клиент-TGS, флаги. "
        "Зашифрован долгосрочным ключом TGS — клиент не может его прочитать, только "
        "предъявлять. Service Ticket — разовый билет на конкретный сервис: ID клиента, "
        "короткий срок (10–60 минут), сессионный ключ клиент-сервис. Зашифрован "
        "долгосрочным ключом этого сервиса. Защита: симметричное шифрование "
        "(AES256-CTS-HMAC-SHA1-96), целостность через HMAC, привязка к идентификатору "
        "клиента и временной метке.",
    ),
    (
        "Какие криптографические алгоритмы используются в Kerberos и зачем нужны сессионные ключи?",
        "Современный набор: AES128/256-CTS-HMAC-SHA1-96 (рекомендуется), Camellia. "
        "Устаревшие: DES, 3DES, RC4-HMAC (только для обратной совместимости с Windows). "
        "Все алгоритмы — симметричные, кроме PKINIT (асимметричный обмен ключами на "
        "стартовом этапе). Сессионные ключи — одноразовые ключи, генерируемые KDC "
        "для каждой пары клиент-партнёр: клиент-TGS (внутри TGT), клиент-сервис "
        "(внутри Service Ticket). Они нужны, чтобы долгосрочные ключи никогда не "
        "передавались по сети, для шифрования аутентикаторов и для защиты данных "
        "после успешной аутентификации.",
    ),
    (
        "Какие основные механизмы безопасности реализованы в Kerberos?",
        "(1) Взаимная аутентификация — обе стороны доказывают свою подлинность. "
        "(2) Защита от replay-атак — каждый аутентикатор содержит timestamp (допуск "
        "по умолчанию 5 минут) и nonce; KDC хранит replay cache. (3) Ограниченное "
        "время жизни билетов — TGT до 24 ч, Service Ticket до 1 ч. (4) "
        "Шифрование всего трафика чувствительными данными. (5) Контроль целостности "
        "через HMAC. (6) Поддержка предаут-блоков (preauth), без которых KDC отвечает "
        "только проверенным запросам — защита от offline-brute-force. (7) Отсутствие "
        "передачи паролей: пароль никогда не уходит в сеть, только производные ключи.",
    ),
    (
        "Какие угрозы и уязвимости существуют в протоколе Kerberos и как с ними борются?",
        "(1) Golden Ticket — компрометация ключа krbtgt позволяет генерировать "
        "произвольные TGT; защита — регулярная смена пароля krbtgt каждые 30–40 дней. "
        "(2) Silver Ticket — компрометация ключа конкретного сервиса; защита — "
        "ротация ключей сервисов через ktadd. (3) Pass-the-Ticket — кража билетов "
        "из памяти LSASS на Windows; защита — Credential Guard, ограничение "
        "делегирования. (4) Расхождение времени > 5 мин ломает всё; защита — "
        "обязательный NTP. (5) Устаревшие алгоритмы (DES, RC4) — отключаются на "
        "уровне kdc.conf через supported_enctypes. (6) Атаки на делегирование — "
        "использовать constrained delegation вместо unconstrained.",
    ),
    (
        "Где и как применяется Kerberos в современных IT-системах?",
        "(1) Windows Active Directory — основа аутентификации с Windows 2000, "
        "интегрирован с PAC. (2) Linux/UNIX — MIT Kerberos и Heimdal, FreeIPA как "
        "комплексное решение (LDAP + Kerberos + PKI + DNS). (3) Облака — Azure AD "
        "Kerberos Hybrid Auth, AWS Managed Microsoft AD. (4) Big Data — Hadoop, "
        "Kafka используют SASL/GSSAPI с Kerberos для аутентификации узлов кластера. "
        "(5) Сетевые сервисы — NFSv4, Apache (mod_auth_kerb), SSH (GSSAPI), почтовые "
        "серверы. (6) HPC-кластеры — Slurm/PBS с короткоживущими билетами. "
        "(7) Финансовые системы — SWIFT, банковские шлюзы.",
    ),
    (
        "Каковы перспективы развития протокола Kerberos в условиях новых технологий?",
        "(1) Квантово-устойчивая криптография — внедрение CRYSTALS-Kyber для "
        "ключевого обмена, Falcon/SPHINCS+ для подписей. RFC-черновики на гибридные "
        "схемы уже обсуждаются в IETF. (2) Облачная интеграция — KDC-as-a-Service, "
        "микросервисная архитектура KDC, контейнеризация. (3) IoT и встроенные "
        "системы — Lightweight Kerberos с ECC и сокращёнными заголовками. "
        "(4) Многофакторная аутентификация на уровне протокола (FAST armoring, "
        "OTP-PA-DATA). (5) Интеграция с современными протоколами федерации (OIDC, "
        "SAML) через шлюзы. (6) Усовершенствованное обнаружение аномалий и "
        "автоматизированный ответ на угрозы в KDC.",
    ),
]


def main() -> None:
    meta = LabMeta(number=1, title="Установка и настройка Kerberos")
    doc = make_doc()
    add_title_page(doc, meta)
    add_page_break(doc)

    # ---- Цель ----
    add_heading(doc, "Тема и цель работы")
    add_para(
        doc,
        "Тема: изучение протокола Kerberos — установка и настройка KDC, клиента и "
        "целевой машины с SSH-аутентификацией по GSSAPI; работа с билетами TGT и "
        "Service Ticket, анализ безопасности и диагностика инфраструктуры.",
    )
    add_para(
        doc,
        "Цель работы: освоить архитектуру Kerberos v5 (AS, TGS, AP, TGT, Service "
        "Ticket, сессионные ключи); развернуть собственный realm LAB.LOCAL; "
        "выполнить десять практических заданий методички — от создания базы KDC "
        "до автоматизированного мониторинга через bash-скрипт.",
    )

    add_heading(doc, "Замечание об инфраструктуре стенда", level=2)
    add_para(
        doc,
        "Стенд имитируется в Docker: три контейнера в bridge-сети 172.29.0.0/24 — "
        "kdc.lab.local (172.29.0.10) с krb5-kdc и krb5-admin-server, target.lab.local "
        "(172.29.0.30) с openssh-server и GSSAPI, client.lab.local (172.29.0.20) с "
        "krb5-user и openssh-client. Имена хостов прописаны в extra_hosts каждого "
        "контейнера — Kerberos требует обратное и прямое разрешение имён. Передача "
        "host-keytab от KDC к target выполнена через общий volume (вместо `scp` из "
        "методички — функционально эквивалентно). Realm: LAB.LOCAL, master password "
        "базы — 1234, admin/admin — admin1234, пользователь labuser — labpass.",
    )

    # ---- Теория ----
    add_heading(doc, "Теоретические сведения")
    add_para(
        doc,
        "Kerberos — сетевой протокол взаимной аутентификации, разработанный в MIT в "
        "рамках проекта Athena (1980-е), названный в честь Цербера — трёхглавого пса "
        "из греческой мифологии (символика «трёх голов»: KDC, клиент, сервис). "
        "Действующая версия — Kerberos v5 (RFC 4120, 2005). Решает фундаментальную "
        "проблему: как доказать серверу свою подлинность в небезопасной сети, не "
        "передавая пароль в открытом виде.",
    )
    add_para(doc, "Архитектура протокола включает четыре компонента:", indent=False)
    add_bullets(doc, [
        "Клиент (Client) — пользователь или сервис, желающий получить доступ;",
        "AS (Authentication Server) — выдаёт TGT после проверки идентичности;",
        "TGS (Ticket Granting Server) — выдаёт сервисные билеты по TGT;",
        "AP (Application Server) — конечный сервис, проверяющий Service Ticket.",
    ])
    add_para(
        doc,
        "AS и TGS вместе образуют KDC (Key Distribution Center) — центральный "
        "сервер, хранящий базу principal'ов и их долгосрочные ключи. Аутентификация "
        "состоит из шести обменов: AS-REQ/AS-REP (получение TGT), TGS-REQ/TGS-REP "
        "(получение Service Ticket), AP-REQ/AP-REP (доступ к сервису, опционально "
        "взаимная аутентификация).",
    )
    add_para(doc, "Типы билетов:", indent=False)
    add_bullets(doc, [
        "TGT (Ticket Granting Ticket) — «пропуск» в KDC, срок 8–24 ч, "
        "зашифрован ключом TGS;",
        "Service Ticket — разовый билет на конкретный сервис, срок 10–60 мин, "
        "зашифрован ключом сервиса;",
        "Сессионные ключи — одноразовые симметричные ключи для каждой пары "
        "клиент-партнёр.",
    ])
    add_para(
        doc,
        "Механизмы безопасности: симметричное шифрование (AES256-CTS-HMAC-SHA1-96), "
        "защита от replay-атак (timestamp + nonce, replay cache), ограниченное время "
        "жизни билетов, preauthentication для защиты от offline-brute-force, "
        "взаимная аутентификация, контроль целостности через HMAC. Критическое "
        "требование: расхождение часов между участниками ≤ 5 минут (контролируется "
        "NTP).",
    )

    # ---- Установка KDC ----
    add_page_break(doc)
    add_heading(doc, "Этап 1. Установка и настройка KDC")
    add_para(
        doc,
        "KDC поднимается в контейнере kdc.lab.local. При первом старте entrypoint "
        "выполняет команды, аналогичные пунктам 2.1–2.7 методички: устанавливает "
        "пакеты krb5-kdc, krb5-admin-server, krb5-config (через apt-get на этапе "
        "сборки образа), создаёт базу командой `kdb5_util create -r LAB.LOCAL -s` "
        "с мастер-паролем 1234, заводит administrative principal admin/admin, "
        "пользователя labuser и host/target.lab.local для SSH, выгружает host-keytab "
        "в общий volume.",
    )

    add_para(doc, "Главный конфиг — /etc/krb5.conf:", indent=False)
    add_listing(doc, read_art("01_kdc_config"), caption="Листинг 1 — /etc/krb5.conf на KDC")

    add_para(doc, "Конфигурация KDC — /etc/krb5kdc/kdc.conf:", indent=False)
    add_listing(doc, read_art("02_kdc_conf"), caption="Листинг 2 — /etc/krb5kdc/kdc.conf")

    add_para(
        doc,
        "ACL администрирования — /etc/krb5kdc/kadm5.acl, разрешает любому principal'у "
        "с компонентом /admin полный доступ к kadmin:",
        indent=False,
    )
    add_listing(doc, read_art("03_kdc_acl"), caption="Листинг 3 — kadm5.acl")

    add_para(
        doc,
        "После инициализации в базе зарегистрированы principal'ы: admin/admin, "
        "labuser, host/target.lab.local и служебные krbtgt, kadmin/admin, "
        "kadmin/changepw, K/M:",
        indent=False,
    )
    add_listing(doc, read_art("04_kdc_principals"), caption="Листинг 4 — listprincs")

    add_para(
        doc,
        "Сетевые сервисы KDC: krb5kdc слушает 88/udp и 88/tcp, kadmind — 749/tcp:",
        indent=False,
    )
    add_listing(doc, read_art("05_kdc_services"), caption="Листинг 5 — порты KDC")

    # ---- Клиент ----
    add_page_break(doc)
    add_heading(doc, "Этап 2. Настройка клиента и получение TGT")
    add_para(
        doc,
        "На client.lab.local установлен пакет krb5-user (kinit/klist/kdestroy/kvno/"
        "kadmin) и openssh-client с настройкой GSSAPIAuthentication=yes в "
        "/etc/ssh/ssh_config. Конфигурация /etc/krb5.conf клиента совпадает с "
        "серверной:",
    )
    add_listing(doc, read_art("06_client_krb5conf"), caption="Листинг 6 — /etc/krb5.conf на клиенте")

    add_para(
        doc,
        "Задание 2–3 методички: получаем TGT под admin/admin и смотрим выданный "
        "билет (`klist`):",
        indent=False,
    )
    add_listing(doc, read_art("07_kinit_admin"), caption="Листинг 7 — kinit admin/admin@LAB.LOCAL")

    add_para(doc, "Просмотр флагов билета (`klist -f`) — флаги F (forwardable), R (renewable), I (initial):", indent=False)
    add_listing(doc, read_art("08_klist_flags"), caption="Листинг 8 — klist -f")

    add_para(doc, "Алгоритмы шифрования (`klist -e`):", indent=False)
    add_listing(doc, read_art("09_klist_enctypes"), caption="Листинг 9 — klist -e")

    # ---- Создание principal ----
    add_heading(doc, "Этап 3. Создание нового principal через admin/admin")
    add_para(
        doc,
        "Задание 5 методички: имея TGT admin/admin, через сетевой `kadmin` (не "
        "`kadmin.local`!) создаём нового principal testuser. Это демонстрирует "
        "работу ACL — `*/admin@LAB.LOCAL *` разрешает админу выполнять любые "
        "операции:",
    )
    add_listing(doc, read_art("10_kadmin_addprinc"), caption="Листинг 10 — kadmin addprinc testuser")
    add_listing(doc, read_art("11_kadmin_listprincs"), caption="Листинг 11 — listprincs (виден testuser)")
    add_para(doc, "Получаем TGT под новым пользователем:", indent=False)
    add_listing(doc, read_art("12_kinit_testuser"), caption="Листинг 12 — kinit testuser@LAB.LOCAL")

    # ---- SSH ----
    add_page_break(doc)
    add_heading(doc, "Этап 4. SSH-аутентификация по Kerberos (GSSAPI)")
    add_para(
        doc,
        "Задание 4 методички — самое показательное: SSH-подключение без пароля, "
        "только по Kerberos-билету. На target.lab.local в /etc/ssh/sshd_config "
        "включены `GSSAPIAuthentication yes`, `GSSAPICleanupCredentials yes`, "
        "`KerberosAuthentication yes`. На клиенте — `GSSAPIDelegateCredentials yes` "
        "(проброс билета внутрь сессии).",
    )
    add_para(doc, "Получаем TGT под labuser (под этим именем есть UNIX-аккаунт на target):", indent=False)
    add_listing(doc, read_art("13_kinit_labuser"), caption="Листинг 13 — kinit labuser@LAB.LOCAL")

    add_para(
        doc,
        "Команда `ssh -K labuser@target.lab.local` — флаг `-K` явно включает "
        "GSSAPI-аутентификацию с делегированием. SSH запрашивает у TGS Service "
        "Ticket для host/target.lab.local, предъявляет его sshd, который проверяет "
        "билет своим keytab — пароль не запрашивается. После входа в сессии "
        "доступен делегированный TGT:",
        indent=False,
    )
    add_listing(doc, read_art("14_ssh_kerberos"), caption="Листинг 14 — ssh -K labuser@target.lab.local")

    add_para(
        doc,
        "После `ssh -K` в кеше клиента появляется Service Ticket для "
        "host/target.lab.local:",
        indent=False,
    )
    add_listing(doc, read_art("15_klist_after_ssh"), caption="Листинг 15 — klist после SSH")

    add_para(doc, "Демонстрация passwordless-режима (`BatchMode=yes` отключает любой запрос пароля):", indent=False)
    add_listing(doc, read_art("22_ssh_demo_passwordless"), caption="Листинг 16 — passwordless SSH через Kerberos")

    # ---- Диагностика ----
    add_page_break(doc)
    add_heading(doc, "Этап 5. Диагностика и анализ логов")
    add_para(doc, "Задание 7 — анализ /var/log/krb5kdc.log, фильтр по AS_REQ и TGS_REQ:", indent=False)
    add_listing(doc, read_art("16_kdc_log_tgs"), caption="Листинг 17 — записи AS_REQ и TGS_REQ")
    add_listing(doc, read_art("17_kdc_log_full"), caption="Листинг 18 — последние 30 строк krb5kdc.log")

    add_para(
        doc,
        "Задание 6 — проверка ключа сервиса (`kvno`). Команда запрашивает Service "
        "Ticket для host/target.lab.local, попутно выводя версию ключа сервиса "
        "(KVNO = Key Version Number):",
        indent=False,
    )
    add_listing(doc, read_art("18_kvno_host"), caption="Листинг 19 — kvno host/target.lab.local")

    # ---- Делегирование ----
    add_heading(doc, "Этап 6. Forwardable-билеты и обновление")
    add_para(
        doc,
        "Задание 9 — `kinit -f` запрашивает forwardable TGT (флаг F), который можно "
        "делегировать другим сервисам. Параметр `-l 1h` задаёт время жизни 1 час, "
        "`-r 12h` — срок продления до 12 часов:",
    )
    add_listing(doc, read_art("19_kinit_forwardable"), caption="Листинг 20 — kinit -f -l 1h -r 12h")

    add_para(doc, "Обновление билета (`kinit -R`) продлевает срок без повторного ввода пароля:", indent=False)
    add_listing(doc, read_art("20_kinit_renew"), caption="Листинг 21 — kinit -R")

    # ---- Скрипт мониторинга ----
    add_page_break(doc)
    add_heading(doc, "Этап 7. Автоматизированный мониторинг (задание 10)")
    add_para(
        doc,
        "Скрипт на bash проверяет три условия: наличие действующего билета "
        "(`klist -s`), доступность KDC по 88/tcp и возможность получить Service "
        "Ticket для host/target.lab.local через `kvno`. Все три проверки прошли "
        "успешно:",
    )
    add_listing(doc, read_art("21_check_script"), caption="Листинг 22 — bash-скрипт мониторинга и его вывод")

    # ---- Завершение ----
    add_heading(doc, "Этап 8. Очистка кеша и финальное состояние")
    add_para(doc, "Удаление всех билетов из кеша:", indent=False)
    add_listing(doc, read_art("23_kdestroy"), caption="Листинг 23 — kdestroy -A")
    add_para(doc, "Финальный список principal'ов в базе KDC:", indent=False)
    add_listing(doc, read_art("24_final_principals"), caption="Листинг 24 — listprincs после прогона")

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
        "В ходе лабораторной работы изучена архитектура и принципы работы протокола "
        "Kerberos v5. Развёрнут собственный realm LAB.LOCAL на стенде из трёх "
        "контейнеров Docker (KDC, target, client), выполнены все десять практических "
        "заданий методички. Получены TGT под разными principal'ами (admin/admin, "
        "labuser, testuser), продемонстрирована passwordless SSH-аутентификация "
        "через GSSAPI: SSH-клиент запрашивает Service Ticket для host/target.lab.local, "
        "sshd проверяет его собственным keytab — пароль не запрашивается. Проверены "
        "флаги билетов (forwardable, renewable, initial), алгоритмы шифрования "
        "(AES256-CTS-HMAC-SHA1-96), команды диагностики (kvno, klist -ef, kdestroy). "
        "Выполнен анализ логов krb5kdc.log с фильтрацией по AS_REQ/TGS_REQ. "
        "Реализован bash-скрипт автоматизированного мониторинга — все три проверки "
        "(наличие билета, доступность KDC, kvno) прошли успешно. Стенд подтвердил, "
        "что Kerberos обеспечивает безопасную взаимную аутентификацию в сети без "
        "передачи пароля и устойчив к replay-атакам за счёт коротких билетов и "
        "временных меток.",
    )

    # ---- Листинги конфигов ----
    add_page_break(doc)
    add_heading(doc, "Исходные файлы стенда")
    add_listing(doc, read_file("docker/docker-compose.yml"), caption="Листинг 25 — docker-compose.yml")
    add_listing(doc, read_file("docker/Dockerfile.kdc"),      caption="Листинг 26 — Dockerfile.kdc")
    add_listing(doc, read_file("docker/Dockerfile.target"),   caption="Листинг 27 — Dockerfile.target")
    add_listing(doc, read_file("docker/Dockerfile.client"),   caption="Листинг 28 — Dockerfile.client")
    add_listing(doc, read_file("docker/krb5.conf"),           caption="Листинг 29 — krb5.conf (общий)")
    add_listing(doc, read_file("docker/kdc.conf"),            caption="Листинг 30 — kdc.conf")
    add_listing(doc, read_file("docker/kadm5.acl"),           caption="Листинг 31 — kadm5.acl")
    add_listing(doc, read_file("docker/sshd_config"),         caption="Листинг 32 — sshd_config (с GSSAPI)")
    add_listing(doc, read_file("docker/entrypoint-kdc.sh"),   caption="Листинг 33 — entrypoint-kdc.sh")
    add_listing(doc, read_file("docker/entrypoint-target.sh"), caption="Листинг 34 — entrypoint-target.sh")
    add_listing(doc, read_file("scripts/run_lab.sh"),         caption="Листинг 35 — scripts/run_lab.sh")

    out = ROOT / "docs" / "reports" / "Ковалев Д.П. ВКБ43 1 лаба.docx"
    save(doc, out)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
