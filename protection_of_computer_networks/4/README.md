# ЛР №4 «Установка и настройка DNS-сервера на платформе Astra Linux»

Дисциплина «Защита компьютерных сетей», преподаватель — Болдырихин Н.В.

Условие — `ЛР 4.docx` рядом с этим README.

## Чем заменена Astra Linux

Методичка требует Astra Linux SE Smolensk. Стенд имитирован в Docker на базе
Debian bookworm: пакеты `bind9`, `bind9utils`, `bind9-doc`, `dnsutils` и
расположение конфигов идентичны Astra/Debian-сборкам — команды совпадают 1-в-1.

## Что построено

Два контейнера в bridge-сети `172.30.0.0/24`:

| Хост                   | IP            | Роль                                       |
|------------------------|---------------|--------------------------------------------|
| `ns.example.local`     | 172.30.0.10   | DNS-сервер BIND9 (авторитетный + рекурсия) |
| `client.example.local` | 172.30.0.20   | клиент с `dig`/`nslookup`/`host`           |

Клиент использует наш BIND как единственный резолвер — это задаётся через
`dns: 172.30.0.10` в `docker-compose.yml`.

## Структура

```
4/
├── docker/
│   ├── Dockerfile.dns       # bind9 + утилиты
│   ├── Dockerfile.client    # dnsutils
│   ├── docker-compose.yml
│   ├── named.conf.options   # ACL trusted, forwarders 8.8.8.8/8.8.4.4
│   ├── named.conf.local     # объявление двух зон
│   ├── db.example.local     # SOA, NS, A, CNAME, MX, TXT
│   ├── db.192.168.local     # обратная зона PTR
│   └── entrypoint-dns.sh    # named-checkconf + checkzone + named -g
├── scripts/
│   ├── run_lab.sh           # 28 шагов (9 пунктов задания + расширенные dig)
│   ├── report_builder.py
│   └── build_report.py
├── artifacts/               # txt-логи команд
└── docs/
    ├── assets/dstu_logo.png
    └── reports/Ковалев Д.П. ВКБ43 4 лаба.docx
```

## Prerequisites

- Docker Desktop ≥ 27 (нужен `docker compose` v2)
- Python 3.10+ с `python-docx`: `pip install python-docx`

---

## Режим 1. Автоматический прогон

```sh
bash scripts/run_lab.sh && python3 scripts/build_report.py
```

Готовый отчёт — `docs/reports/Ковалев Д.П. ВКБ43 4 лаба.docx`.

---

## Режим 2. Ручное выполнение (для защиты)

### Шаг 0. Поднять стенд

Из директории `protection_of_computer_networks/4/`:

```sh
docker compose -f docker/docker-compose.yml up -d --build
docker compose -f docker/docker-compose.yml ps
```

Оба контейнера должны быть в состоянии `Up`.

### Шаг 1. Войти на DNS-сервер и проверить установку

```sh
docker compose -f docker/docker-compose.yml exec dns bash
```

Внутри:

```sh
uname -a
named -v
dpkg -l | grep -E '^ii\s+bind9'
```

Должны увидеть BIND ≥ 9.18 и пакеты `bind9`, `bind9utils`, `bind9-doc`, `dnsutils`.

### Шаг 2. Посмотреть конфигурацию

```sh
cat /etc/bind/named.conf.options
cat /etc/bind/named.conf.local
cat /etc/bind/db.example.local
cat /etc/bind/db.192.168.local
```

Ключевые места:
- `acl "trusted"` — кому разрешены запросы (172.30.0.0/24 + localhost);
- `allow-transfer { none; };` — запрет AXFR;
- `forwarders { 8.8.8.8; 8.8.4.4; };` — рекурсия наружу;
- В db-файле SOA / NS / A / CNAME / MX / TXT.

### Шаг 3. Проверить синтаксис конфигурации

```sh
named-checkconf /etc/bind/named.conf
named-checkzone example.local /etc/bind/db.example.local
named-checkzone 0.30.172.in-addr.arpa /etc/bind/db.192.168.local
```

Ожидаемо: `OK`, `zone example.local/IN: loaded serial 2 OK`.

### Шаг 4. Проверить что демон слушает порт 53

```sh
ss -tulpn | grep ':53'
ps -ef | grep '[n]amed'
```

### Шаг 5. Перезагрузить BIND после изменений

В контейнере без systemd — SIGHUP процессу named:

```sh
kill -HUP $(pidof named)
```

На реальной Astra: `systemctl reload bind9` или `rndc reload`.

Выйти из server'а: `exit`.

### Шаг 6. Зайти на клиент и проверить resolv.conf

```sh
docker compose -f docker/docker-compose.yml exec client bash
cat /etc/resolv.conf
```

Должно быть `nameserver 172.30.0.10`.

### Шаг 7. Запросы dig — основные типы записей

```sh
dig @172.30.0.10 example.local NS +short
dig @172.30.0.10 www.example.local A +short
dig @172.30.0.10 mail.example.local A +short
dig @172.30.0.10 web.example.local              # CNAME → A
dig @172.30.0.10 example.local MX +short
dig @172.30.0.10 example.local TXT +short
dig @172.30.0.10 -x 172.30.0.10 +short          # PTR
dig @172.30.0.10 example.local SOA
dig @172.30.0.10 example.local ANY
```

Ожидаемые значения:

| Запрос          | Ответ                                    |
|-----------------|------------------------------------------|
| NS              | `ns.example.local.`                      |
| www A           | `172.30.0.10`                            |
| web (CNAME)     | `CNAME → www.example.local.` → `172.30.0.10` |
| MX              | `10 mail.example.local.`                 |
| TXT             | `"v=spf1 mx ~all"`                       |
| PTR (172.30.0.10) | `ns.`, `www.`, `mail.example.local.`   |

### Шаг 8. Запрос без явного @ — клиент использует наш DNS

```sh
dig www.example.local +short
nslookup www.example.local 172.30.0.10
host -v db.example.local 172.30.0.10
```

Все должны вернуть IP/имена нашей зоны.

### Шаг 9. Рекурсивный запрос наружу через forwarders

```sh
dig @172.30.0.10 example.com A +short
```

Должны вернуться реальные IP сайта `example.com` — это значит forwarders
работают и наш BIND корректно проксирует внешние запросы.

### Шаг 10. Логи и статистика

Выйти из клиента, вернуться на DNS:

```sh
docker compose -f docker/docker-compose.yml exec dns bash
rndc status
rndc stats
cat /var/cache/bind/named.stats | head -40
```

`docker compose logs lab_dns_server` покажет полный stderr BIND (загрузка зон,
обработка запросов).

### Шаг 11. Остановить стенд

```sh
exit
docker compose -f docker/docker-compose.yml down
```

---

## Шпаргалка типов DNS-записей

| Тип    | Назначение                              | Пример                                       |
|--------|------------------------------------------|----------------------------------------------|
| SOA    | заголовок зоны (Serial, Refresh, TTL)    | `@ IN SOA ns.example.local. admin (...)`     |
| NS     | авторитетный сервер зоны                 | `@ IN NS ns.example.local.`                  |
| A      | IPv4 для имени                           | `www IN A 172.30.0.10`                       |
| AAAA   | IPv6 для имени                           | `www IN AAAA 2001:db8::1`                    |
| CNAME  | псевдоним (имя → имя)                    | `web IN CNAME www.example.local.`            |
| MX     | почтовый сервер с приоритетом            | `@ IN MX 10 mail.example.local.`             |
| TXT    | произвольный текст (SPF, DKIM, верификация) | `@ IN TXT "v=spf1 mx ~all"`              |
| PTR    | обратное разрешение IP → имя             | `10 IN PTR ns.example.local.`                |
| SRV    | сервис (host:port, weight, priority)     | `_kerberos._tcp IN SRV 0 5 88 kdc.lab.local.`|

## Соответствие пунктам методички

| Пункт                                | Шаги в `run_lab.sh`           |
|--------------------------------------|-------------------------------|
| 1. Войти под админом                 | `docker exec ... bash` = root |
| 2. Обновить систему                  | (в Dockerfile, apt-get update)|
| 3. Установить пакеты bind            | 02                            |
| 4. Открыть named.conf.options        | 03                            |
| 5. Настройка                         | 03 (allow-query, forwarders)  |
| 6. Настройка зоны                    | 04                            |
| 7. Создать файл зоны                 | 05, 06                        |
| 8. Перезапуск BIND                   | 11                            |
| 9. Проверка работы DNS-сервера       | 13–25                         |

## Известные особенности

1. **`.local` и mDNS.** TLD `.local` зарезервирован RFC 6762 за Multicast DNS
   (Bonjour/Avahi). `dig` выдаёт предупреждение «mDNS query is leaked to DNS»,
   но запрос всё равно резолвится через наш unicast BIND. На реальном
   деплое лучше выбрать другой TLD (например, `.lab.internal` или `.test`).
2. **`docker run` и `dns:`.** Параметр `dns:` в `docker-compose.yml` записывает
   адрес в `/etc/resolv.conf` контейнера. На реальной Astra то же самое
   достигается через NetworkManager / `nmcli ipv4.dns`.
3. **DNSSEC отключён.** `dnssec-validation no` в `named.conf.options` — нет
   цепочки доверия для `example.local`. В продакшне обязательно включать.
4. **Логи BIND в Docker.** Демон запущен с флагом `-g` (foreground + stderr),
   поэтому логи доступны через `docker logs lab_dns_server`, а не через
   `/var/log/syslog` (на безсистемдном контейнере его нет).
