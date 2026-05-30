#!/usr/bin/env bash
# Стартует BIND9 в foreground'е, логи направляет в stdout контейнера —
# чтобы `docker logs` показывал работу демона.

set -euo pipefail

echo "==> [dns] Версия BIND:"
named -v

echo "==> [dns] Проверка named.conf:"
named-checkconf /etc/bind/named.conf
echo "    OK"

echo "==> [dns] Проверка зоны example.local:"
named-checkzone example.local /etc/bind/db.example.local

echo "==> [dns] Проверка обратной зоны 0.30.172.in-addr.arpa:"
named-checkzone 0.30.172.in-addr.arpa /etc/bind/db.192.168.local

echo "==> [dns] Запуск named (foreground, логи на stderr)"
exec /usr/sbin/named -u bind -g -c /etc/bind/named.conf
