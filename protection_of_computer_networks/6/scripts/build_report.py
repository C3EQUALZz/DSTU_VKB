"""Отчёт по ЛР №6 «Централизованный защищённый файловый сервер учётных
записей пользователей на платформе Astra Linux»."""

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
        "Что такое учётная запись пользователя и какую роль она играет в безопасности системы?",
        "Учётная запись пользователя (account) — это объект в системе, "
        "содержащий идентификационные данные (UID, имя), credentials (хеш пароля, "
        "ssh-ключи), принадлежность к группам (основная + дополнительные GID), "
        "ссылку на домашний каталог и shell. В Linux учётные записи хранятся в "
        "/etc/passwd, /etc/shadow, /etc/group. Роль в безопасности: учётная запись "
        "— фундамент модели доступа, на её основе ядро принимает решения о "
        "разрешении/запрете операций над файлами и системными ресурсами (DAC). "
        "Каждый процесс наследует UID/GID запустившего его пользователя, что "
        "позволяет применять права на уровне файла, директории или процесса.",
    ),
    (
        "Что такое файловый сервер и зачем он нужен?",
        "Файловый сервер — это сервер, предоставляющий сетевой доступ к файлам "
        "и каталогам по протоколам SMB/CIFS (Samba), NFS, FTP/FTPS, SFTP, WebDAV. "
        "Назначение: централизованное хранение данных, совместная работа над "
        "файлами, единая политика доступа, упрощение резервного копирования. "
        "В корпоративной среде заменяет хранение файлов на рабочих станциях, "
        "обеспечивает контроль доступа через ACL и интеграцию с каталогами "
        "(LDAP, Active Directory, FreeIPA).",
    ),
    (
        "Что такое разрезывание?",
        "В контексте методички — это процесс разделения хранилища данных и "
        "учётных записей на независимые логические блоки (подкаталоги, ACL, "
        "квоты), что обеспечивает изоляцию пользователей, упрощает управление и "
        "повышает безопасность. В нашей лабораторной разрезывание реализовано "
        "так: общая директория /srv/ftp принадлежит группе ftp_users, но внутри "
        "она «нарезана» на персональные подкаталоги /srv/ftp/user1, "
        "/srv/ftp/user2, причём ACL явно запрещает каждому пользователю доступ "
        "к чужому каталогу.",
    ),
    (
        "Как можно изменить права доступа к файлам и директориям с помощью команд chmod и chown?",
        "chmod — изменение прав доступа: chmod 755 file — задаёт rwxr-xr-x; "
        "chmod u+x file — добавить владельцу право выполнения; chmod g-w file — "
        "снять у группы право записи; chmod 2770 dir — setgid bit + rwx для "
        "владельца/группы. chown — смена владельца и группы: chown user:group "
        "file; chown -R alice:dev /srv/data — рекурсивно. Альтернативно: chgrp "
        "только группу. Для расширенных прав за пределами rwx используется ACL "
        "(setfacl/getfacl).",
    ),
    (
        "Как можно просмотреть информацию обо всех пользователях, зарегистрированных в системе?",
        "Основные способы: cat /etc/passwd — текстовый файл со всеми "
        "пользователями (формат login:x:UID:GID:GECOS:home:shell); getent passwd — "
        "вытаскивает запись через NSS (учитывает LDAP, sssd и др.); compgen -u — "
        "только имена. Для группы: cat /etc/group или getent group. Информация о "
        "конкретном пользователе: id user1 (UID, GID, supplementary groups), "
        "finger user1 (если установлен). Сессии: who, w, last.",
    ),
    (
        "Что делает команда usermod и какие ключевые параметры у неё существуют?",
        "usermod изменяет существующую учётную запись пользователя. Ключевые "
        "параметры: -l NEW_NAME — переименование (без смены UID); -u UID — "
        "сменить UID; -d DIR — новый домашний каталог (с -m — перенести "
        "содержимое); -s SHELL — сменить shell; -g GROUP — основная группа; "
        "-G GROUPS — список дополнительных групп (заменяет полностью); -aG GROUP "
        "— добавить в группу без потери остальных; -L / -U — заблокировать / "
        "разблокировать пароль; -e DATE — дата истечения учётной записи.",
    ),
    (
        "Как связаны группы пользователей с правами доступа в системе?",
        "В классической модели DAC каждый файл имеет владельца (UID), группу "
        "(GID) и три набора прав: для владельца, для группы, для остальных. "
        "Когда пользователь обращается к файлу, ядро проверяет: если он "
        "владелец — применяются user-права; если он в группе файла — "
        "group-права; иначе — other. Группы позволяют разграничить доступ без "
        "необходимости индивидуально настраивать ACL для каждого пользователя. "
        "В нашей лабе группа ftp_users — общая для всех владельцев каталогов в "
        "/srv/ftp, ACL дополняет базовые права тонкими исключениями.",
    ),
    (
        "Какие права доступа записываются в формате rwx и что они означают?",
        "Для файлов: r (read) — чтение содержимого, w (write) — изменение "
        "содержимого, x (execute) — выполнение как программы. Для директорий: "
        "r — листинг имён в директории, w — создание/удаление файлов в "
        "директории, x — вход в директорию (обращение к файлам по имени). "
        "Дополнительные биты: setuid (4 в octal) — процесс запускается с UID "
        "владельца файла; setgid (2) — для исполняемых: с GID владельца; для "
        "директорий: новые файлы наследуют группу директории. Sticky (1) — "
        "удалять файл может только его владелец (как в /tmp). В octal-нотации "
        "права записываются как chmod 2770 — setgid + rwxrwx---.",
    ),
    (
        "Как можно добавить пользователя в несколько групп и какие могут возникнуть ситуации при неправильной настройке групповых прав?",
        "Добавить в группу можно тремя способами: usermod -aG ftp_users,dev "
        "user1 (флаг -a критичен, без него -G заменяет ВСЕ supplementary "
        "группы), gpasswd -a user1 ftp_users (одна группа за вызов), либо "
        "прямой правкой /etc/group. Типичные ошибки: (1) использование -G "
        "вместо -aG приводит к потере членства в других группах — пользователь "
        "может перестать иметь доступ к нужным ресурсам. (2) Слишком широкая "
        "группа (например, добавление в sudo) даёт права root. (3) "
        "Конфликтующие ACL и групповые права — если ACL не учитывает базовые "
        "rwx маски, эффективные права могут оказаться меньше, чем ожидается. "
        "(4) Изменения в группах применяются только при следующем login — "
        "уже открытые сессии работают со старым списком групп.",
    ),
]


def main() -> None:
    meta = LabMeta(
        number=6,
        title="Централизованный защищённый файловый сервер учётных записей пользователей",
    )
    doc = make_doc()
    add_title_page(doc, meta)
    add_page_break(doc)

    # ---- Цель ----
    add_heading(doc, "Тема и цель работы")
    add_para(
        doc,
        "Тема: организация централизованного файлового сервера с разделением "
        "учётных записей пользователей на платформе Astra Linux. Создание "
        "пользователей и групп, настройка прав через chmod/chown, ACL "
        "(setfacl/getfacl), демонстрация изоляции через SSH, аудит доступов "
        "через auditd.",
    )
    add_para(
        doc,
        "Цель работы: освоить управление учётными записями (useradd, usermod, "
        "groupadd), задание прав через chmod/chown и расширенных прав через "
        "ACL, организацию изолированных подкаталогов внутри shared-директории, "
        "настройку audit-правил для журналирования доступа к чувствительным "
        "каталогам.",
    )

    add_heading(doc, "Замечание об инфраструктуре стенда", level=2)
    add_para(
        doc,
        "Стенд имитирован в Docker: server (Debian bookworm + openssh-server + "
        "acl + auditd) и client (openssh-client) в bridge-сети 172.31.0.0/24. "
        "Astra Linux SE построена на Debian, команды управления пользователями "
        "и ACL идентичны. Контейнер server запущен с capabilities AUDIT_CONTROL, "
        "AUDIT_WRITE, AUDIT_READ. Однако ядро LinuxKit под Docker Desktop на "
        "macOS не предоставляет полную поддержку audit-подсистемы (отсутствует "
        "CONFIG_AUDIT_PRIORITIES), поэтому демон auditd не может загрузить "
        "правила. Это известное ограничение, отмечено в отчёте; на нативной "
        "Astra Linux audit-подсистема работает штатно.",
    )

    # ---- Теория ----
    add_heading(doc, "Теоретические сведения")
    add_para(
        doc,
        "Учётная запись пользователя — фундаментальный объект безопасности ОС. "
        "Каждая запись связывает имя пользователя с UID, GID, домашним "
        "каталогом, shell и членством в группах. Ядро использует UID/GID "
        "процессов для проверки прав на файлы. В Astra Linux SE Smolensk "
        "учётные записи дополнительно интегрированы с мандатным разграничением "
        "доступа (МРД), но базовая дискреционная модель (DAC) — основа всего.",
    )
    add_para(doc, "Уровни управления правами:", indent=False)
    add_bullets(doc, [
        "Классические rwx-права — владелец, группа, остальные (3 + 3 + 3 бита);",
        "Setuid/setgid/sticky — специальные биты (setgid на директории заставляет "
        "новые файлы наследовать группу — критично для shared-каталогов);",
        "POSIX ACL — расширенные права на уровне конкретных пользователей и "
        "групп (setfacl/getfacl, пакет acl);",
        "Default ACL — права, которые наследуют новые файлы/подкаталоги;",
        "Аудит — журналирование доступа через auditd с правилами в "
        "/etc/audit/rules.d/.",
    ])
    add_para(
        doc,
        "В лабораторной построена типовая конфигурация shared-сервера: общая "
        "группа ftp_users, общий корень /srv/ftp с setgid-битом (новые файлы "
        "автоматически попадают в ftp_users), персональные подкаталоги "
        "/srv/ftp/user1 и /srv/ftp/user2 с собственными владельцами и ACL, "
        "явно запрещающим чужому пользователю доступ.",
    )

    # ---- Этап 1: установка и пользователи ----
    add_page_break(doc)
    add_heading(doc, "Этап 1. Подготовка системы (пункты 1–3 задания)")
    add_listing(doc, read_art("01_system_info"), caption="Листинг 1 — информация о сервере")
    add_listing(doc, read_art("02_apt_update"),  caption="Листинг 2 — apt-get update")

    add_heading(doc, "Этап 2. Создание группы и пользователей (пункты 4–5)")
    add_para(doc, "Группа ftp_users создана; в неё добавлены user1 и user2:", indent=False)
    add_listing(doc, read_art("03_group_info"),     caption="Листинг 3 — getent group ftp_users")
    add_listing(doc, read_art("04_user1_info"),     caption="Листинг 4 — id user1")
    add_listing(doc, read_art("05_user2_info"),     caption="Листинг 5 — id user2")
    add_listing(doc, read_art("06_passwd_entries"), caption="Листинг 6 — записи в /etc/passwd")

    # ---- Этап 3: директории и базовые права ----
    add_heading(doc, "Этап 3. Директории и базовые права (пункты 6, 8, 9)")
    add_para(
        doc,
        "Корневая директория /srv/ftp принадлежит root:ftp_users с правами 2770 "
        "(setgid + rwxrwx---). Подкаталоги /srv/ftp/user1 и /srv/ftp/user2 — "
        "владельцу пользователю + группе ftp_users, тот же setgid.",
        indent=False,
    )
    add_listing(doc, read_art("07_dirs"),       caption="Листинг 7 — ls -la /srv/ftp")
    add_listing(doc, read_art("08_dir_perms"),  caption="Листинг 8 — stat по правам директорий")

    add_para(
        doc,
        "Демонстрация setgid: новый файл, созданный в /srv/ftp, автоматически "
        "получает группу ftp_users, а не основную группу процесса:",
        indent=False,
    )
    add_listing(doc, read_art("09_setgid_demo"), caption="Листинг 9 — setgid-наследование группы")

    # ---- Этап 4: ACL ----
    add_heading(doc, "Этап 4. Настройка ACL (пункт 10)")
    add_listing(doc, read_art("10_acl_installed"), caption="Листинг 10 — пакет acl установлен")

    add_para(
        doc,
        "ACL на /srv/ftp задаёт дефолтные права для новых файлов: default:group:"
        "ftp_users:rwx — все участники группы автоматически получают rwx:",
        indent=False,
    )
    add_listing(doc, read_art("11_getfacl_root"), caption="Листинг 11 — getfacl /srv/ftp")

    add_para(
        doc,
        "ACL на персональных подкаталогах содержат явный запрет для второго "
        "пользователя (user:user2:--- для /srv/ftp/user1 и наоборот) — это и "
        "есть «разрезывание» из методички:",
        indent=False,
    )
    add_listing(doc, read_art("12_getfacl_user1"), caption="Листинг 12 — getfacl /srv/ftp/user1")
    add_listing(doc, read_art("13_getfacl_user2"), caption="Листинг 13 — getfacl /srv/ftp/user2")

    # ---- Этап 5: проверка изоляции ----
    add_page_break(doc)
    add_heading(doc, "Этап 5. Проверка изоляции пользователей (пункты 13–15)")
    add_para(doc, "user1 успешно создаёт файл в собственном каталоге:", indent=False)
    add_listing(doc, read_art("14_user1_create_file"), caption="Листинг 14 — user1 создаёт файл")

    add_para(
        doc,
        "user2 не может ни прочитать содержимое каталога user1, ни прочитать "
        "созданный там файл — Permission denied, exit code 1:",
        indent=False,
    )
    add_listing(doc, read_art("15_user2_cannot_read_user1"), caption="Листинг 15 — user2 → user1: denied")

    add_para(doc, "Симметрично — user2 создаёт файл в своём каталоге:", indent=False)
    add_listing(doc, read_art("16_user2_create_file"), caption="Листинг 16 — user2 создаёт файл")

    add_para(doc, "user1 тоже не может зайти в чужой каталог:", indent=False)
    add_listing(doc, read_art("17_user1_cannot_read_user2"), caption="Листинг 17 — user1 → user2: denied")

    # ---- Этап 6: SSH ----
    add_heading(doc, "Этап 6. Проверка с клиентского контейнера через SSH")
    add_para(
        doc,
        "Клиент подключается по SSH под user1 (пароль pass1) и видит "
        "содержимое только своего каталога:",
        indent=False,
    )
    add_listing(doc, read_art("18_ssh_user1"), caption="Листинг 18 — ssh user1@server")

    add_para(
        doc,
        "Под user2 — аналогично; попытка зайти в /srv/ftp/user1 даёт "
        "Permission denied:",
        indent=False,
    )
    add_listing(doc, read_art("19_ssh_user2"), caption="Листинг 19 — ssh user2@server")

    # ---- Этап 7: auditd ----
    add_page_break(doc)
    add_heading(doc, "Этап 7. Настройка аудита auditd (пункты 16–18)")
    add_listing(doc, read_art("20_audit_installed"), caption="Листинг 20 — пакет auditd установлен")
    add_listing(doc, read_art("21_audit_rules"),     caption="Листинг 21 — правило в /etc/audit/rules.d/ftp.rules")

    add_para(
        doc,
        "Демон auditd попытался запуститься, но не смог — ядро LinuxKit под "
        "Docker Desktop на macOS не имеет полной поддержки audit-подсистемы. "
        "Команды auditctl возвращают «Operation not permitted», демон "
        "завершается на этапе изменения priority:",
        indent=False,
    )
    add_listing(doc, read_art("22_auditctl_status"), caption="Листинг 22 — auditctl -s")
    add_listing(doc, read_art("23_auditctl_list"),   caption="Листинг 23 — auditctl -l")
    add_listing(doc, read_art("24_audit_log"),       caption="Листинг 24 — диагностика запуска auditd")

    add_para(
        doc,
        "На реальной Astra Linux auditd работает штатно и записывает события "
        "в /var/log/audit/audit.log. Просмотр выполняется командами "
        "ausearch -k ftp-access и aureport -k. В Docker-стенде для "
        "демонстрации мониторинга используется альтернативный путь — find с "
        "timestamps файлов:",
        indent=False,
    )
    add_listing(doc, read_art("25_alternative_audit"), caption="Листинг 25 — альтернативный мониторинг файлов")

    # ---- Итог ----
    add_heading(doc, "Итоговая структура")
    add_listing(doc, read_art("26_summary"), caption="Листинг 26 — финальное состояние /srv/ftp и ACL")

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
        "В ходе лабораторной работы изучена организация централизованного "
        "файлового сервера с разграничением доступа на основе учётных записей "
        "и групп. Реализованы все пункты рабочего задания на стенде "
        "Debian/Docker как функциональном эквиваленте Astra Linux SE: создана "
        "группа ftp_users, добавлены пользователи user1 и user2, организована "
        "директория /srv/ftp с подкаталогами user1/ и user2/, базовые права "
        "(2770 setgid) дополнены ACL — дефолтные права наследуют группа "
        "ftp_users, а ACL-исключения user:user2:--- и user:user1:--- "
        "обеспечивают взаимную изоляцию пользователей. Проверка показала: "
        "user1 и user2 успешно создают файлы в своих каталогах, не имеют "
        "доступа в чужие каталоги (Permission denied), SSH-подключение с "
        "отдельного клиентского контейнера подтверждает работу изоляции на "
        "уровне сетевой сессии. Демон auditd установлен и правила настроены, "
        "однако на стенде Docker под macOS audit-подсистема ядра LinuxKit "
        "ограничена — на нативной Astra Linux SE этот компонент работает "
        "штатно, в отчёте отмечено явно.",
    )

    # ---- Исходники ----
    add_page_break(doc)
    add_heading(doc, "Исходные файлы стенда")
    add_listing(doc, read_file("docker/docker-compose.yml"),     caption="Листинг 27 — docker-compose.yml")
    add_listing(doc, read_file("docker/Dockerfile.server"),      caption="Листинг 28 — Dockerfile.server")
    add_listing(doc, read_file("docker/Dockerfile.client"),      caption="Листинг 29 — Dockerfile.client")
    add_listing(doc, read_file("docker/audit.rules"),            caption="Листинг 30 — audit.rules")
    add_listing(doc, read_file("docker/entrypoint-server.sh"),   caption="Листинг 31 — entrypoint-server.sh")
    add_listing(doc, read_file("scripts/run_lab.sh"),            caption="Листинг 32 — scripts/run_lab.sh")

    out = ROOT / "docs" / "reports" / "Ковалев Д.П. ВКБ43 6 лаба.docx"
    save(doc, out)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
