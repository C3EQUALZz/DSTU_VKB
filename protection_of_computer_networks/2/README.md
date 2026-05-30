# ЛР №2 «Настройка межсетевого экрана»

Дисциплина «Защита компьютерных сетей», преподаватель — Болдырихин Н.В.

Условие — `ЛР 1.docx` рядом с этим README (имя файла оставлено преподавателем,
но по факту это вторая лабораторная работа курса).

## Чем заменена Astra Linux

Методичка требует Astra Linux SE Smolensk. Стенд имитирован в Docker на базе
Debian bookworm: Astra SE построена на Debian, команды `ufw` и `iptables`
совпадают, а скрипт `astra-ufw-control` — это обёртка над `ufw`. Графическая
часть (`gufw`, рисунки 5–11 методички) опущена, делаем только консоль.

В отчёте об этом сказано явно — раздел «Замечание об инфраструктуре стенда».

## Что в репозитории

```
2/
├── docker/
│   ├── Dockerfile.server        # ufw + openssh-server + nginx
│   ├── Dockerfile.client        # ssh-client + curl
│   ├── docker-compose.yml       # bridge-сеть 172.28.0.0/24, два сервиса
│   ├── default-site.conf        # конфиг nginx (HTTP+HTTPS на одном vhost)
│   ├── index.html               # тестовая страница веб-сервера
│   └── entrypoint.sh            # запуск sshd + nginx внутри server
├── scripts/
│   ├── run_lab.sh               # прогон всех 19 шагов лабы
│   ├── report_builder.py        # обёртка над python-docx (титул, листинги, QA)
│   └── build_report.py          # генератор отчёта из артефактов
├── artifacts/                   # txt-логи команд (создаются run_lab.sh)
└── docs/
    ├── assets/dstu_logo.png
    └── reports/Ковалев Д.П. ВКБ43 2 лаба.docx
```

## Prerequisites

- Docker Desktop ≥ 27 (нужен `docker compose` v2);
- Python 3.10+ с `python-docx` (только для пересборки docx-отчёта):
  ```sh
  pip install python-docx
  ```

---

## Режим 1. Автоматический прогон

Всё одной командой — стенд поднимается, выполняются 19 шагов, артефакты
складываются в `artifacts/`, стенд гасится, docx собирается.

```sh
bash scripts/run_lab.sh && python3 scripts/build_report.py
```

Готовый отчёт — `docs/reports/Ковалев Д.П. ВКБ43 2 лаба.docx`.

---

## Режим 2. Ручное выполнение (для защиты)

Этот режим воспроизводит лабу руками — преподаватель может попросить
продемонстрировать каждый шаг вживую. Команды совпадают с методичкой 1-в-1.

### Шаг 0. Поднять стенд

Из директории `protection_of_computer_networks/2/`:

```sh
docker compose -f docker/docker-compose.yml up -d --build
```

Ожидаемый вывод (кусок):

```
[+] Running 4/4
 ✔ Network lab_net                   Created
 ✔ Volume "lab_firewall_rules"       Created
 ✔ Container lab_firewall_server     Started
 ✔ Container lab_firewall_client     Started
```

Проверить, что оба контейнера запущены:

```sh
docker compose -f docker/docker-compose.yml ps
```

### Шаг 1. Войти в контейнер server

Все команды настройки firewall выполняются на `lab-server`:

```sh
docker compose -f docker/docker-compose.yml exec server bash
```

После входа приглашение становится `root@lab-server:/#`. Все следующие шаги
(до раздела «Проверка с клиента») — внутри этого shell.

### Шаг 2. Информация о системе

```sh
uname -a
cat /etc/os-release | head -5
ip -4 addr show eth0 | grep inet
```

Ожидаемо: ядро `linuxkit`, ОС Debian GNU/Linux 12 (bookworm), адрес
`172.28.0.10/24` на интерфейсе `eth0`.

### Шаг 3. Сбросить ufw в исходное состояние

```sh
ufw --force reset
ufw status verbose
```

Ожидаемый вывод второй команды:

```
Status: inactive
```

### Шаг 4. Задать политики по умолчанию

```sh
ufw default deny incoming
ufw default allow outgoing
```

Вывод:

```
Default incoming policy changed to 'deny'
(be sure to update your rules accordingly)
Default outgoing policy changed to 'allow'
(be sure to update your rules accordingly)
```

Это пункт 3 методички — входящие по умолчанию запрещены, исходящие разрешены.

### Шаг 5. Разрешить SSH (порт 22)

```sh
ufw allow 22/tcp comment 'SSH access'
```

Вывод:

```
Rules updated
Rules updated (v6)
```

### Шаг 6. Разрешить HTTP (80) и HTTPS (443)

```sh
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'
```

После каждой команды — две строки `Rules updated` / `Rules updated (v6)`.

### Шаг 7. Активировать межсетевой экран

```sh
ufw --force enable
```

Вывод:

```
Firewall is active and enabled on system startup
```

### Шаг 8. Проверить состояние

```sh
ufw status numbered verbose
```

Ожидаемый вывод:

```
Status: active

     To                         Action      From
     --                         ------      ----
[ 1] 22/tcp                     ALLOW IN    Anywhere                   # SSH access
[ 2] 80/tcp                     ALLOW IN    Anywhere                   # HTTP
[ 3] 443/tcp                    ALLOW IN    Anywhere                   # HTTPS
[ 4] 22/tcp (v6)                ALLOW IN    Anywhere (v6)              # SSH access
[ 5] 80/tcp (v6)                ALLOW IN    Anywhere (v6)              # HTTP
[ 6] 443/tcp (v6)               ALLOW IN    Anywhere (v6)              # HTTPS
```

### Шаг 9. Разрешить уже установленные соединения (ESTABLISHED, RELATED)

Это пункт 3.3 методички. Правило вставляется первым в цепочку INPUT:

```sh
iptables -I INPUT 1 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -L INPUT -n -v --line-numbers | head -15
```

В первой строке INPUT должно появиться:

```
1        0     0 ACCEPT     0    --  *      *       0.0.0.0/0            0.0.0.0/0            ctstate RELATED,ESTABLISHED
```

### Шаг 10. Просмотреть все правила iptables

```sh
iptables -L -n -v
```

Покажет все три цепочки (INPUT, FORWARD, OUTPUT) и служебные ufw-chains
(`ufw-user-input`, `ufw-before-input`, `ufw-after-input` и т. д.).

### Шаг 11. Сохранить правила в файл

Пункт 4 методички — чтобы правила восстанавливались при перезагрузке:

```sh
mkdir -p /etc/iptables
iptables-save > /etc/iptables/rules.v4
cat /etc/iptables/rules.v4 | head -20
```

В файл попадут все цепочки и правила в формате `iptables-save`. Восстановление
после ребута — `iptables-restore < /etc/iptables/rules.v4`.

### Шаг 12. Выйти из контейнера server

```sh
exit
```

Возвращаемся в shell macOS.

### Шаг 13. Войти в контейнер client и проверить ICMP

```sh
docker compose -f docker/docker-compose.yml exec client bash
ping -c 2 -W 1 172.28.0.10
```

Ожидаемо **fail** — ICMP не разрешали:

```
PING 172.28.0.10 (172.28.0.10) 56(84) bytes of data.
--- 172.28.0.10 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 1010ms
```

### Шаг 14. Проверка SSH с клиента

Пользователь `labuser`, пароль `lab`:

```sh
sshpass -p lab ssh -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    labuser@172.28.0.10 'hostname && whoami && uname -r'
```

Вывод:

```
Warning: Permanently added '172.28.0.10' (ED25519) to the list of known hosts.
lab-server
labuser
6.12.76-linuxkit
```

Если хочется интерактивную SSH-сессию — без `sshpass` и без последнего
аргумента, просто `ssh labuser@172.28.0.10`, пароль вводится руками.

### Шаг 15. Проверка HTTP

```sh
curl -sS -w '\n--- HTTP %{http_code} ---\n' http://172.28.0.10/
```

Должна вернуться HTML-страница и в конце:

```
--- HTTP 200 ---
```

### Шаг 16. Проверка HTTPS

Сертификат self-signed, поэтому флаг `-k`:

```sh
curl -skS -w '\n--- HTTPS %{http_code} ---\n' https://172.28.0.10/
```

Аналогично: HTML и `--- HTTPS 200 ---` в конце.

### Шаг 17. Выйти из контейнера client

```sh
exit
```

### Шаг 18. Демонстрация запрета (опционально, для защиты)

Вернуться в server:

```sh
docker compose -f docker/docker-compose.yml exec server bash
```

Добавить DROP на порт 8080 — пример из методички:

```sh
iptables -A INPUT -p tcp --dport 8080 -j DROP
iptables -L INPUT -n -v --line-numbers | grep 8080
```

Запретить SSH через ufw (аналог `astra-ufw-control deny SSH`). Из-за того,
что ufw не держит одновременно allow и deny по одному порту, сначала снимаем
разрешение:

```sh
ufw --force delete allow 22/tcp
ufw insert 1 deny 22/tcp comment 'deny SSH demo'
ufw status numbered
```

После этого первая строка вывода должна стать:

```
[ 1] 22/tcp                     DENY IN     Anywhere                   # deny SSH demo
```

Проверить из client'а (в другом терминале):

```sh
docker compose -f docker/docker-compose.yml exec client \
    sshpass -p lab ssh -o StrictHostKeyChecking=no \
        -o UserKnownHostsFile=/dev/null -o ConnectTimeout=3 \
        labuser@172.28.0.10 'echo OK'
```

Ожидаемо — таймаут:

```
ssh: connect to host 172.28.0.10 port 22: Connection timed out
```

Откатить запрет (в server'е):

```sh
ufw --force delete deny 22/tcp
ufw allow 22/tcp comment 'SSH access (restored)'
ufw status numbered
```

### Шаг 19. Остановить стенд

Выйти из контейнера (`exit`) и из директории `2/`:

```sh
docker compose -f docker/docker-compose.yml down -v
```

Флаг `-v` удаляет volume `lab_firewall_rules` — чистый старт в следующий
раз. Если хочется сохранить правила между запусками — без `-v`.

---

## Шпаргалка ufw / iptables (для контрольных вопросов)

| Задача                                  | ufw                                          | iptables                                                        |
|-----------------------------------------|----------------------------------------------|-----------------------------------------------------------------|
| Включить firewall                       | `ufw enable`                                 | —                                                               |
| Отключить                               | `ufw disable`                                | `iptables -F` (только очистка)                                 |
| Статус                                  | `ufw status verbose`                         | `iptables -L -n -v`                                            |
| Разрешить порт                          | `ufw allow 22/tcp`                           | `iptables -A INPUT -p tcp --dport 22 -j ACCEPT`                |
| Запретить порт                          | `ufw deny 8080/tcp`                          | `iptables -A INPUT -p tcp --dport 8080 -j DROP`                |
| Удалить правило                         | `ufw delete allow 22/tcp` или `delete N`     | `iptables -D INPUT N`                                          |
| Политика по умолчанию                   | `ufw default deny incoming`                  | `iptables -P INPUT DROP`                                       |
| Сохранить                               | (ufw сам персистит)                          | `iptables-save > /etc/iptables/rules.v4`                       |
| Восстановить                            | (после ребута сам)                           | `iptables-restore < /etc/iptables/rules.v4`                    |
| Сбросить всё                            | `ufw reset`                                  | `iptables -F && iptables -X`                                   |

Команды Astra `astra-ufw-control enable|disable|status|allow|deny|reset` —
1-в-1 обёртка над соответствующими `ufw` командами.

---

## Почему контейнеру server нужны cap_add

`iptables` и `ufw` модифицируют netfilter — для этого требуется capability
`NET_ADMIN`. `NET_RAW` нужен для работы с сырыми сокетами (используется
некоторыми проверками ufw). Они прописаны в `docker-compose.yml`:

```yaml
cap_add:
  - NET_ADMIN
  - NET_RAW
```

Без них `ufw enable` падает с `operation not permitted`.

## Известные особенности

1. **`iptables-legacy`.** Под macOS / Apple Silicon Docker запускает контейнеры
   на ядре LinuxKit, в котором `iptables-nft` работает неустойчиво с `ufw`.
   `entrypoint.sh` переключает alternatives на `iptables-legacy` — это и есть
   путь Astra SE Smolensk «из коробки».
2. **Отсутствие GUI.** Скриншоты `gufw` в отчёт не входят — стенд консольный.
   Если преподаватель потребует — это придётся одолжить у одногруппника на
   реальной Astra.
3. **Не нативная Astra.** Команды `astra-ufw-control` (специфичные для Astra)
   на Debian отсутствуют; используется их эквивалент `ufw`. В контрольных
   вопросах команды Astra перечислены корректно.
4. **`Skipping inserting existing rule`.** Если ufw отказывается добавлять
   `deny` для порта, по которому уже есть `allow` — сначала удалить `allow`
   (`ufw delete allow 22/tcp`), потом вставить `deny`. ufw не различает
   ACCEPT и DROP при дедупликации по портам.

## Откуда брать примеры вывода

Все ожидаемые выводы выше — это сокращённые версии файлов из `artifacts/`,
сгенерированных автоматическим прогоном (`bash scripts/run_lab.sh`). Если
во время ручной демонстрации что-то отличается, сравнить с эталонным
артефактом: например, `cat artifacts/07_ufw_status_after.txt`.
