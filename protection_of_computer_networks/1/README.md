# ЛР №1 «Установка и настройка Kerberos»

Дисциплина «Защита компьютерных сетей», преподаватель — Болдырихин Н.В.

Условие — `Методичка Болдырихин.docx` рядом с этим README.

## Что построено

Стенд имитирует три машины из методички в Docker:

| Хост               | IP            | Роль                                       |
|--------------------|---------------|--------------------------------------------|
| `kdc.lab.local`    | 172.29.0.10   | KDC: krb5-kdc + krb5-admin-server          |
| `target.lab.local` | 172.29.0.30   | целевая машина: openssh-server + GSSAPI    |
| `client.lab.local` | 172.29.0.20   | клиент: krb5-user + openssh-client         |

Realm `LAB.LOCAL`, передача host-keytab от KDC к target — через общий
Docker-volume (замена `scp` из методички).

Учётные данные (захардкожены в `docker/entrypoint-kdc.sh`):

| Principal                | Пароль       | Назначение                             |
|--------------------------|--------------|----------------------------------------|
| master key DB            | `1234`       | мастер-ключ базы KDC                   |
| `admin/admin@LAB.LOCAL`  | `admin1234`  | админ для `kadmin` через сеть          |
| `labuser@LAB.LOCAL`      | `labpass`    | пользователь для SSH-теста             |
| `host/target.lab.local`  | randkey      | keytab сервиса sshd                    |

## Структура

```
1/
├── docker/
│   ├── Dockerfile.kdc / .target / .client
│   ├── docker-compose.yml
│   ├── krb5.conf, kdc.conf, kadm5.acl, sshd_config
│   ├── entrypoint-kdc.sh, entrypoint-target.sh
├── scripts/
│   ├── run_lab.sh               # прогон 24 шагов
│   ├── report_builder.py        # обёртка над python-docx
│   └── build_report.py          # генератор отчёта
├── artifacts/                   # txt-логи команд (создаются run_lab.sh)
└── docs/
    ├── assets/dstu_logo.png
    └── reports/Ковалев Д.П. ВКБ43 1 лаба.docx
```

## Prerequisites

- Docker Desktop ≥ 27 (нужен `docker compose` v2)
- Python 3.10+ с `python-docx`: `pip install python-docx`

---

## Режим 1. Автоматический прогон

Одной командой: стенд → 24 шага → docx-отчёт.

```sh
bash scripts/run_lab.sh && python3 scripts/build_report.py
```

Готовый отчёт — `docs/reports/Ковалев Д.П. ВКБ43 1 лаба.docx`.

---

## Режим 2. Ручное выполнение (для защиты)

### Шаг 0. Поднять стенд

Из директории `protection_of_computer_networks/1/`:

```sh
docker compose -f docker/docker-compose.yml up -d --build
```

Дождаться, пока entrypoint KDC создаст базу и выгрузит keytab. Проверка:

```sh
docker compose -f docker/docker-compose.yml exec target ls -l /etc/krb5.keytab
```

Должно показать файл с правами `-rw------- root root`.

### Шаг 1. Зайти на KDC и посмотреть конфигурацию

```sh
docker compose -f docker/docker-compose.yml exec kdc bash
```

Внутри (приглашение `root@kdc:/#`):

```sh
cat /etc/krb5.conf
cat /etc/krb5kdc/kdc.conf
cat /etc/krb5kdc/kadm5.acl
```

### Шаг 2. Список principal'ов в базе KDC

```sh
kadmin.local -q 'listprincs'
```

Ожидаемый вывод:

```
K/M@LAB.LOCAL
admin/admin@LAB.LOCAL
host/target.lab.local@LAB.LOCAL
kadmin/admin@LAB.LOCAL
kadmin/changepw@LAB.LOCAL
krbtgt/LAB.LOCAL@LAB.LOCAL
labuser@LAB.LOCAL
```

Выйти: `exit`.

### Шаг 3. Зайти на client и получить TGT

```sh
docker compose -f docker/docker-compose.yml exec client bash
```

Внутри:

```sh
kinit admin/admin@LAB.LOCAL
# (вводим admin1234)
klist
```

Ожидаемый вывод `klist`:

```
Ticket cache: FILE:/tmp/krb5cc_0
Default principal: admin/admin@LAB.LOCAL

Valid starting   Expires            Service principal
05/30 15:09:49   05/31 15:09:49     krbtgt/LAB.LOCAL@LAB.LOCAL
        renew until 06/06 15:09:49
```

Дополнительно — флаги и алгоритмы шифрования:

```sh
klist -f    # флаги F (forwardable), R (renewable), I (initial)
klist -e    # AES256-CTS-HMAC-SHA1-96
```

### Шаг 4. Создать нового principal через сетевой kadmin

Это демонстрация ACL — `admin/admin` через сеть управляет базой:

```sh
kadmin -p admin/admin -q 'addprinc -pw testpass testuser@LAB.LOCAL'
kadmin -p admin/admin -q 'listprincs'
```

Получить TGT под новым пользователем:

```sh
kdestroy -A
kinit testuser@LAB.LOCAL
klist
```

### Шаг 5. SSH через Kerberos (главный шаг)

Получаем TGT под labuser (под ним есть UNIX-аккаунт на target):

```sh
kdestroy -A
kinit labuser@LAB.LOCAL
# (вводим labpass)
ssh -K labuser@target.lab.local
```

Флаг `-K` включает GSSAPI с делегированием. Пароль НЕ запрашивается.
В сессии:

```sh
hostname    # target.lab.local
whoami      # labuser
klist       # внутри сессии виден делегированный TGT
exit
```

После выхода — у клиента в кеше появился Service Ticket:

```sh
klist
```

```
Default principal: labuser@LAB.LOCAL

Valid starting   Expires            Service principal
...              ...                krbtgt/LAB.LOCAL@LAB.LOCAL
...              ...                host/target.lab.local@LAB.LOCAL
```

### Шаг 6. Проверка ключа сервиса (kvno)

```sh
kvno host/target.lab.local@LAB.LOCAL
```

Вывод:

```
host/target.lab.local@LAB.LOCAL: kvno = 2
```

### Шаг 7. Forwardable-билеты и обновление

```sh
kdestroy -A
kinit -f -l 1h -r 12h labuser@LAB.LOCAL
klist -f       # видим флаги FRI (forwardable, renewable, initial)
kinit -R       # обновление без ввода пароля
klist
```

### Шаг 8. Анализ логов KDC

В другом терминале:

```sh
docker compose -f docker/docker-compose.yml exec kdc bash
grep -E 'TGS_REQ|AS_REQ' /var/log/krb5kdc.log | tail -20
tail -30 /var/log/krb5kdc.log
```

Будут видны записи вида:

```
... AS_REQ ... labuser@LAB.LOCAL for krbtgt/LAB.LOCAL@LAB.LOCAL
... TGS_REQ ... labuser@LAB.LOCAL for host/target.lab.local@LAB.LOCAL
```

### Шаг 9. Скрипт автоматизированного мониторинга

В клиенте:

```sh
cat > /tmp/krb_check.sh <<'EOF'
#!/usr/bin/env bash
set -e
echo '--- 1. Проверка билета ---'
klist -s && echo OK || { echo FAIL; exit 1; }
echo '--- 2. Доступность KDC ---'
(echo > /dev/tcp/kdc.lab.local/88) 2>/dev/null && echo OK || { echo FAIL; exit 2; }
echo '--- 3. kvno ---'
kvno host/target.lab.local@LAB.LOCAL && echo OK || { echo FAIL; exit 3; }
EOF
bash /tmp/krb_check.sh
```

Все три проверки должны вернуть OK.

### Шаг 10. Очистка и остановка стенда

```sh
kdestroy -A
exit
docker compose -f docker/docker-compose.yml down -v
```

Флаг `-v` удаляет volume с базой KDC и keytab — чистый старт в следующий раз.

---

## Шпаргалка команд Kerberos

| Команда                             | Назначение                                       |
|-------------------------------------|--------------------------------------------------|
| `kinit user@REALM`                  | получить TGT                                     |
| `kinit -f -l 1h -r 12h user@REALM`  | forwardable, время жизни 1ч, продление до 12ч    |
| `kinit -R`                          | обновить существующий TGT                        |
| `klist`                             | список билетов в кеше                            |
| `klist -f`                          | + флаги (F/R/I/D/...)                            |
| `klist -e`                          | + алгоритмы шифрования                           |
| `klist -k /etc/krb5.keytab`         | посмотреть содержимое keytab                     |
| `kdestroy [-A]`                     | удалить билет(ы) из кеша                         |
| `kvno SERVICE/host@REALM`           | получить версию ключа сервиса                    |
| `kpasswd user@REALM`                | сменить пароль principal'а                       |
| `kadmin.local -q 'listprincs'`      | список principal'ов (локально на KDC)            |
| `kadmin -p admin/admin -q 'addprinc -pw P user'` | создать principal через сеть         |
| `ssh -K user@host`                  | SSH с GSSAPI-аутентификацией (passwordless)      |

## Соответствие пунктам методички

| Пункт методички | Где реализовано в стенде                        |
|-----------------|-------------------------------------------------|
| 2.1–2.7 KDC     | `Dockerfile.kdc` + `entrypoint-kdc.sh`          |
| 3.1–3.4 клиент  | `Dockerfile.client` + `krb5.conf`               |
| 4.1–4.6 target  | `Dockerfile.target` + `sshd_config` + entrypoint |
| 5. Тестирование | шаги 13–14 в `run_lab.sh`                       |
| 6.1–6.6         | шаги 7–18 в `run_lab.sh` (klist, kvno, logs)    |
| Задание 1       | этап 1 (KDC поднят, realm создан)               |
| Задание 2       | kinit admin/admin                               |
| Задание 3       | klist / klist -f / klist -e                     |
| Задание 4       | `ssh -K labuser@target.lab.local`               |
| Задание 5       | `kadmin -p admin/admin -q 'addprinc testuser'`  |
| Задание 6       | время хоста shared в Docker; NTP не требуется   |
| Задание 7       | grep AS_REQ/TGS_REQ в krb5kdc.log               |
| Задание 8       | Wireshark — не входит в стенд (вручную)         |
| Задание 9       | `kinit -f -l 1h -r 12h` + `kinit -R`            |
| Задание 10      | bash-скрипт /tmp/krb_check.sh                   |

## Особенности и известные проблемы

1. **`udp_preference_limit = 1`** в `krb5.conf` — заставляет клиент использовать
   TCP вместо UDP для запросов к KDC. Под Docker Desktop на macOS UDP
   иногда теряет пакеты на стыке хост/виртуалка, TCP стабильнее.
2. **`extra_hosts`** в `docker-compose.yml` — Kerberos требует и прямое, и
   обратное разрешение имён. Service-имена Docker (`kdc`, `target`) не работают,
   потому что Kerberos строит principal'ы из FQDN (`host/target.lab.local`).
   `extra_hosts` прописывает FQDN в `/etc/hosts` каждого контейнера.
3. **Время.** Все три контейнера разделяют часы хоста — расхождение нулевое.
   На физических машинах потребовался бы NTP (задание 6 методички), здесь нет.
4. **Wireshark (задание 8)** — в Docker-стенде не реализован: захват трафика
   между контейнерами требует `tcpdump` внутри одного из них и последующего
   импорта `.pcap` в Wireshark. Можно сделать отдельной командой:
   `docker compose exec kdc tcpdump -i eth0 -w /tmp/krb.pcap port 88`.
5. **GUI gufw/настройки Astra Linux** — не применяется, эта работа полностью
   консольная.
