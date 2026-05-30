#!/usr/bin/env bash
# Прогон ЛР №4 «Установка и настройка DNS-сервера на платформе Astra Linux».
# Покрывает 9 пунктов рабочего задания + дополнительные проверки.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE_DIR="$ROOT/docker"
ART_DIR="$ROOT/artifacts"

rm -rf "$ART_DIR"
mkdir -p "$ART_DIR"

compose() {
    docker compose -f "$COMPOSE_DIR/docker-compose.yml" "$@"
}

dns()    { compose exec -T dns    bash -lc "$*"; }
cli()    { compose exec -T client bash -lc "$*"; }

log_step() {
    local host="$1" name="$2"; shift 2
    local cmd="$*"
    local file="$ART_DIR/${name}.txt"
    {
        echo "# host: ${host}"
        echo "# command: ${cmd}"
        echo "# ---"
    } > "$file"
    case "$host" in
        dns)    dns "$cmd" >> "$file" 2>&1 || true ;;
        client) cli "$cmd" >> "$file" 2>&1 || true ;;
    esac
    echo "→ $name"
}

echo "==> Поднимаем стенд (docker compose up --build)"
compose up -d --build

echo "==> Ждём, пока BIND поднимется"
for i in $(seq 1 20); do
    if compose exec -T dns ss -tulpn 2>/dev/null | grep -q ':53'; then
        echo "    BIND слушает 53 (попытка ${i})"
        break
    fi
    sleep 1
done
sleep 1

# ---------- Пункт 1-3: установка и информация ----------
log_step dns 01_system_info "uname -a && cat /etc/os-release | head -5 && ip -4 addr show eth0 | grep inet"
log_step dns 02_bind_version "named -v && dpkg -l | grep -E '^ii\\s+bind9' | awk '{print \$2, \$3}'"

# ---------- Пункт 4: конфигурационные файлы ----------
log_step dns 03_named_conf_options "cat /etc/bind/named.conf.options"
log_step dns 04_named_conf_local   "cat /etc/bind/named.conf.local"
log_step dns 05_db_example_local   "cat /etc/bind/db.example.local"
log_step dns 06_db_reverse         "cat /etc/bind/db.192.168.local"

# ---------- Пункт 5: проверка синтаксиса ----------
log_step dns 07_named_checkconf "named-checkconf /etc/bind/named.conf && echo 'named.conf syntax: OK'"
log_step dns 08_checkzone_forward "named-checkzone example.local /etc/bind/db.example.local"
log_step dns 09_checkzone_reverse "named-checkzone 0.30.172.in-addr.arpa /etc/bind/db.192.168.local"

# ---------- Пункт 6-7: зона уже настроена через конфиги, проверяем что master ----------
log_step dns 10_named_status "ss -tulpn | grep ':53' && echo '--- named process ---' && ps -ef | grep '[n]amed'"

# ---------- Пункт 8: «перезапуск» — отправляем reload через rndc / SIGHUP ----------
log_step dns 11_named_reload "named-checkconf && kill -HUP \$(pidof named) && sleep 1 && echo 'BIND reloaded (SIGHUP)'"

# ---------- Пункт 9: проверка через dig с клиента ----------
log_step client 12_client_resolv "cat /etc/resolv.conf"

log_step client 13_dig_ns       "dig @172.30.0.10 example.local NS +short"
log_step client 14_dig_a_www    "dig @172.30.0.10 www.example.local A +short"
log_step client 15_dig_a_mail   "dig @172.30.0.10 mail.example.local A +short"
log_step client 16_dig_cname    "dig @172.30.0.10 web.example.local"
log_step client 17_dig_mx       "dig @172.30.0.10 example.local MX +short"
log_step client 18_dig_txt      "dig @172.30.0.10 example.local TXT +short"
log_step client 19_dig_ptr      "dig @172.30.0.10 -x 172.30.0.10 +short"
log_step client 20_dig_soa      "dig @172.30.0.10 example.local SOA"
log_step client 21_dig_any      "dig @172.30.0.10 example.local ANY"

# Без явного @ — клиент должен использовать наш DNS из /etc/resolv.conf.
log_step client 22_dig_implicit "dig www.example.local +short"
log_step client 23_nslookup     "nslookup www.example.local 172.30.0.10"
log_step client 24_host         "host -v db.example.local 172.30.0.10"

# ---------- Рекурсивный запрос наружу через forwarders ----------
log_step client 25_recursive    "dig @172.30.0.10 example.com A +short"

# ---------- Логи BIND ----------
log_step dns 26_named_logs "tail -30 /var/log/syslog 2>/dev/null || tail -30 /var/log/messages 2>/dev/null || echo '(BIND пишет логи в stdout контейнера — см. docker logs lab_dns_server)'"
log_step dns 27_rndc_status "rndc status || true"
log_step dns 28_rndc_stats  "rndc stats && cat /var/cache/bind/named.stats 2>/dev/null | head -40 || true"

echo "==> Готово. Артефакты в $ART_DIR"
ls -la "$ART_DIR"

echo
echo "Останавливаем стенд (docker compose down)…"
compose down
