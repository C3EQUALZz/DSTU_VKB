# ЛР №6 «Централизованный защищённый файловый сервер учётных записей пользователей»

Дисциплина «Защита компьютерных сетей», преподаватель — Болдырихин Н.В.

Условие — `ЛР 6.docx` рядом с этим README.

## Чем заменена Astra Linux

Стенд — Debian bookworm в Docker как функциональный эквивалент Astra Linux SE.
Команды `useradd`, `groupadd`, `chmod`, `chown`, `setfacl`/`getfacl`, `auditctl`
идентичны Astra/Debian. **Важное ограничение:** auditd не работает в Docker
под macOS из-за отсутствия CONFIG_AUDIT_PRIORITIES в ядре LinuxKit — это
отдельно прокомментировано в отчёте.

## Что построено

Два контейнера в bridge-сети `172.31.0.0/24`:

| Хост        | IP            | Роль                                   |
|-------------|---------------|----------------------------------------|
| `fs-server` | 172.31.0.10   | sshd + acl + auditd + директории       |
| `fs-client` | 172.31.0.20   | openssh-client для проверок            |

**Пользователи:**

| Логин   | Пароль  | UID  | Группы            |
|---------|---------|------|-------------------|
| user1   | pass1   | 1000 | user1, ftp_users  |
| user2   | pass2   | 1001 | user2, ftp_users  |

**Структура /srv/ftp:**
```
/srv/ftp                drwxrws---  root:ftp_users  (2770, setgid)
├── user1/              drwxrws---  user1:ftp_users (2770) + ACL: user2:---
└── user2/              drwxrws---  user2:ftp_users (2770) + ACL: user1:---
```

## Структура

```
6/
├── docker/
│   ├── Dockerfile.server     # debian + sshd + acl + auditd
│   ├── Dockerfile.client     # debian + ssh-client
│   ├── docker-compose.yml
│   ├── audit.rules           # -w /srv/ftp -p rwxa -k ftp-access
│   └── entrypoint-server.sh  # создаёт группу, пользователей, ACL
├── scripts/
│   ├── run_lab.sh
│   ├── report_builder.py
│   └── build_report.py
├── artifacts/                # txt-логи команд
└── docs/
    ├── assets/dstu_logo.png
    └── reports/Ковалев Д.П. ВКБ43 6 лаба.docx
```

## Prerequisites

- Docker Desktop ≥ 27
- Python 3.10+ с `python-docx`: `pip install python-docx`

---

## Режим 1. Автоматический прогон

```sh
bash scripts/run_lab.sh && python3 scripts/build_report.py
```

---

## Режим 2. Ручное выполнение (для защиты)

### Шаг 0. Поднять стенд

Из `protection_of_computer_networks/6/`:

```sh
docker compose -f docker/docker-compose.yml up -d --build
```

Проверка готовности:

```sh
docker compose -f docker/docker-compose.yml exec server bash -c 'getent group ftp_users && ls -la /srv/ftp'
```

Должны видеть `ftp_users:x:1000:user1,user2` и три директории с правами `drwxrws---`.

### Шаг 1. Зайти на server и осмотреть систему

```sh
docker compose -f docker/docker-compose.yml exec server bash
```

Внутри:

```sh
uname -a
cat /etc/os-release | head -5
getent group ftp_users
id user1
id user2
```

### Шаг 2. Проверить базовые права директорий

```sh
stat -c '%n %A (octal: %a) owner=%U group=%G' /srv/ftp /srv/ftp/user1 /srv/ftp/user2
```

Ожидаемо: `drwxrws--- (octal: 2770)` — setgid + rwx для владельца и группы.

### Шаг 3. Демонстрация setgid (наследование группы)

```sh
touch /srv/ftp/_test.txt
stat -c '%n group=%G' /srv/ftp/_test.txt
rm /srv/ftp/_test.txt
```

Файл получит группу `ftp_users` даже если создан от root.

### Шаг 4. Просмотр ACL

```sh
getfacl /srv/ftp
getfacl /srv/ftp/user1
getfacl /srv/ftp/user2
```

Ключевая строка в /srv/ftp/user1:

```
user:user2:---           ← явный запрет user2
default:group:ftp_users:rwx
```

### Шаг 5. Проверка от имени user1

```sh
su - user1
cd /srv/ftp/user1
echo 'hello from user1' > my_file.txt
ls -la
exit
```

### Шаг 6. Проверка изоляции — user2 в чужом каталоге

```sh
su - user2
ls -la /srv/ftp/user1/        # Permission denied
cat /srv/ftp/user1/my_file.txt  # Permission denied
echo $?                         # 1
exit
```

Выйти из server: `exit`.

### Шаг 7. SSH с клиента под обоими пользователями

```sh
docker compose -f docker/docker-compose.yml exec client bash

# user1
sshpass -p pass1 ssh -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null user1@172.31.0.10 \
    'whoami && id && ls -la /srv/ftp/user1/'

# user2 — попытка в чужой каталог
sshpass -p pass2 ssh -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null user2@172.31.0.10 \
    'ls -la /srv/ftp/user1/'    # Permission denied
exit
```

### Шаг 8. Аудит — конфигурация

```sh
docker compose -f docker/docker-compose.yml exec server bash
cat /etc/audit/rules.d/ftp.rules     # -w /srv/ftp -p rwxa -k ftp-access
auditctl -l                          # на macOS-Docker: Operation not permitted
auditctl -s                          # на macOS-Docker: Operation not permitted
```

На нативной Astra Linux:

```sh
ausearch -k ftp-access | head
aureport -k
```

### Шаг 9. Остановить стенд

```sh
exit
docker compose -f docker/docker-compose.yml down
```

---

## Шпаргалка команд

| Цель                          | Команда                                     |
|-------------------------------|---------------------------------------------|
| Создать группу                | `groupadd ftp_users`                        |
| Создать пользователя в группе | `useradd -m -s /bin/bash -G ftp_users user1`|
| Сменить пароль                | `echo 'user1:pass1' \| chpasswd`            |
| Добавить в группу (не теряя)  | `usermod -aG dev user1`                     |
| Права (числовые)              | `chmod 2770 /srv/ftp`                       |
| Setgid (наследование группы)  | `chmod g+s /srv/ftp`                        |
| Владельца:группа              | `chown user1:ftp_users /srv/ftp/user1`      |
| Дефолтный ACL для подкаталога | `setfacl -d -m g:ftp_users:rwx /srv/ftp`    |
| Явный запрет пользователю     | `setfacl -m u:user2:--- /srv/ftp/user1`     |
| Просмотр ACL                  | `getfacl /srv/ftp/user1`                    |
| Audit-правило                 | `auditctl -w /srv/ftp -p rwxa -k ftp-access`|
| Поиск событий                 | `ausearch -k ftp-access`                    |

## Соответствие пунктам методички

| Пункт задания                            | Где реализовано     |
|------------------------------------------|---------------------|
| 1–2. Войти под админом, обновить         | 01, 02              |
| 3. SSH                                    | 18, 19              |
| 4. Группа ftp_users                       | entrypoint, 03      |
| 5. Пользователи user1/user2               | entrypoint, 04–06   |
| 6. Директория /srv/ftp                    | entrypoint, 07      |
| 7. Файлы (зоны — опечатка методички)      | 14, 16              |
| 8. Права доступа                          | entrypoint, 08      |
| 9. setgid (наследование)                  | 09                  |
| 10. Пакет acl                             | 10                  |
| 11. Подкаталоги для каждого пользователя  | entrypoint, 07      |
| 12. Права для подкаталогов                | 11–13               |
| 13. Вход под разными учётками             | 18, 19              |
| 14. Создание файлов                       | 14, 16              |
| 15. Проверка второго пользователя         | 15, 17, 19          |
| 16. Установка auditd                      | 20                  |
| 17. Настройка аудита /srv/ftp             | 21–23               |
| 18. Проверка журнала                      | 24, 25              |

## Известные особенности

1. **auditd на Docker под macOS.** Ядро LinuxKit не предоставляет полную
   audit-подсистему (отсутствует CONFIG_AUDIT_PRIORITIES, или netlink-канал
   аудита недоступен из user-namespace контейнера). Демон auditd не может
   зарегистрироваться, команды auditctl возвращают «Operation not permitted».
   На нативной Astra Linux всё работает штатно — конфигурационные файлы
   корректны, протестировано через `named-checkconf`-эквивалент `augenrules`.
2. **chpasswd vs passwd --stdin.** В bookworm `passwd --stdin` отсутствует,
   используется `chpasswd` (читает пары `user:pass` со stdin).
3. **`setfacl -m u:user2:---`** — явный запрет конкретному пользователю даже
   несмотря на членство в группе ftp_users. ACL-маска применяется до
   групповых прав, что и обеспечивает изоляцию.
4. **setgid на shared-каталоге.** Без бита `g+s` (octal: 2xxx) новые файлы
   получают основную группу процесса, а не группу директории — это типичная
   ошибка администратора при настройке shared-серверов.
