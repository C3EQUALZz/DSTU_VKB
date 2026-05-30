#!/usr/bin/env bash
# Прогон лабораторной работы №1 «Настройка межсетевого экрана».
# Команды максимально соответствуют методичке (ufw + iptables Astra Linux SE).
# Каждый шаг логируется в artifacts/<NN>_<имя>.txt — листинги для отчёта.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE_DIR="$ROOT/docker"
ART_DIR="$ROOT/artifacts"

# Очищаем старые артефакты — лаба должна быть воспроизводима с чистого листа.
rm -rf "$ART_DIR"
mkdir -p "$ART_DIR"

compose() {
    docker compose -f "$COMPOSE_DIR/docker-compose.yml" "$@"
}

# Все команды на server выполняем под root (нужны привилегии для iptables/ufw).
srv() {
    compose exec -T server bash -lc "$*"
}

# Клиентские проверки.
cli() {
    compose exec -T client bash -lc "$*"
}

# log_step "01_name" "команда" — выполняет на server и записывает stdout+stderr в файл.
log_step() {
    local name="$1"; shift
    local cmd="$*"
    local file="$ART_DIR/${name}.txt"
    {
        echo "# host: lab-server"
        echo "# command: $cmd"
        echo "# ---"
    } > "$file"
    srv "$cmd" >> "$file" 2>&1 || true
    echo "→ $name"
}

log_step_cli() {
    local name="$1"; shift
    local cmd="$*"
    local file="$ART_DIR/${name}.txt"
    {
        echo "# host: lab-client"
        echo "# command: $cmd"
        echo "# ---"
    } > "$file"
    cli "$cmd" >> "$file" 2>&1 || true
    echo "→ $name (from client)"
}

echo "==> Поднимаем стенд (docker compose up --build)"
compose up -d --build

# Даём nginx/sshd время старутнуть.
sleep 3

echo "==> Шаг 0. Информация о системе server"
log_step "00_system_info" "uname -a && cat /etc/os-release | head -n 5 && ip -4 addr show eth0 | grep inet"

echo "==> Шаг 1. Сброс ufw до состояния «по умолчанию»"
log_step "01_ufw_reset" "ufw --force reset"

echo "==> Шаг 2. Проверяем статус ufw (должен быть inactive после reset)"
log_step "02_ufw_status_before" "ufw status verbose"

echo "==> Шаг 3. Политики по умолчанию: входящие — deny, исходящие — allow"
log_step "03_ufw_defaults" "ufw default deny incoming && ufw default allow outgoing"

echo "==> Шаг 4. Разрешаем SSH (порт 22)"
log_step "04_ufw_allow_ssh" "ufw allow 22/tcp comment 'SSH access'"

echo "==> Шаг 5. Разрешаем HTTP (80) и HTTPS (443)"
log_step "05_ufw_allow_http_https" "ufw allow 80/tcp comment 'HTTP' && ufw allow 443/tcp comment 'HTTPS'"

echo "==> Шаг 6. Активируем межсетевой экран"
log_step "06_ufw_enable" "ufw --force enable"

echo "==> Шаг 7. Состояние ufw после включения"
log_step "07_ufw_status_after" "ufw status numbered verbose"

echo "==> Шаг 8. Правило для уже установленных соединений (ESTABLISHED, RELATED)"
# ufw такие правила добавляет автоматически в before.rules, но методичка требует
# явно показать iptables-команду — добавляем дублирующую для наглядности.
log_step "08_iptables_established" \
    "iptables -I INPUT 1 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT && iptables -L INPUT -n -v --line-numbers | head -n 15"

echo "==> Шаг 9. Полный листинг iptables (INPUT/OUTPUT/FORWARD)"
log_step "09_iptables_list" "iptables -L -n -v"

echo "==> Шаг 10. Сохраняем правила в /etc/iptables/rules.v4 для загрузки при старте"
log_step "10_iptables_save" \
    "mkdir -p /etc/iptables && iptables-save > /etc/iptables/rules.v4 && echo '--- /etc/iptables/rules.v4 ---' && cat /etc/iptables/rules.v4"

echo "==> Шаг 11. Проверка с клиента: ping (ICMP не открыт — должен fail)"
log_step_cli "11_client_ping" "ping -c 2 -W 1 172.28.0.10 || true"

echo "==> Шаг 12. Проверка SSH с клиента — должен подключиться"
log_step_cli "12_client_ssh" \
    "sshpass -p lab ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null labuser@172.28.0.10 'hostname && whoami && uname -r'"

echo "==> Шаг 13. Проверка HTTP с клиента — должен ответить 200"
log_step_cli "13_client_http" "curl -sS -o - -w '\\n--- HTTP %{http_code}, %{size_download} bytes ---\\n' http://172.28.0.10/"

echo "==> Шаг 14. Проверка HTTPS с клиента (self-signed → -k)"
log_step_cli "14_client_https" "curl -skS -o - -w '\\n--- HTTPS %{http_code}, %{size_download} bytes ---\\n' https://172.28.0.10/"

echo "==> Шаг 15. Демонстрация запрета: добавляем DROP на 8080, проверяем"
log_step "15_iptables_drop_demo" \
    "iptables -A INPUT -p tcp --dport 8080 -j DROP && iptables -L INPUT -n -v --line-numbers | grep 8080"

echo "==> Шаг 16. Запрещаем SSH (удаляем allow 22, добавляем deny 22) — демонстрация astra-ufw-control deny"
# Эквивалент команды `astra-ufw-control deny SSH` из методички: ufw не позволяет
# держать одновременно allow и deny по одному и тому же порту, поэтому сначала
# снимаем разрешение, потом ставим запрет первым правилом.
log_step "16_ufw_deny_ssh_demo" \
    "ufw --force delete allow 22/tcp && ufw insert 1 deny 22/tcp comment 'deny SSH demo' && ufw status numbered"

echo "==> Шаг 17. Проверяем что SSH теперь блокируется"
log_step_cli "17_client_ssh_after_deny" \
    "sshpass -p lab ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=3 labuser@172.28.0.10 'echo OK' || true"

echo "==> Шаг 18. Откатываем запрет, возвращаем разрешение SSH"
log_step "18_ufw_delete_deny" \
    "ufw --force delete deny 22/tcp && ufw allow 22/tcp comment 'SSH access (restored)' && ufw status numbered"

echo "==> Шаг 19. Финальный статус — правила в норме"
log_step "19_final_status" "ufw status verbose && echo '--- iptables ---' && iptables -L INPUT -n -v --line-numbers"

echo "==> Готово. Артефакты в $ART_DIR"
ls -la "$ART_DIR"

echo
echo "Останавливаем стенд (docker compose down -v)…"
compose down -v
