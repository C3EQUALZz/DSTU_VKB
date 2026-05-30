#!/usr/bin/env bash
# Прогон ЛР6 «Централизованный защищённый файловый сервер учётных записей
# пользователей на платформе Astra Linux». Покрывает 18 пунктов задания:
# пользователи и группы, права/ACL на /srv/ftp, проверка с клиента через SSH,
# настройка auditd.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE_DIR="$ROOT/docker"
ART_DIR="$ROOT/artifacts"

rm -rf "$ART_DIR"
mkdir -p "$ART_DIR"

compose() {
    docker compose -f "$COMPOSE_DIR/docker-compose.yml" "$@"
}

srv()      { compose exec -T server bash -lc "$*"; }
srv_user() { local u="$1"; shift; compose exec -T -u "$u" server bash -lc "$*"; }
cli()      { compose exec -T client bash -lc "$*"; }

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
        server)        srv "$cmd"        >> "$file" 2>&1 || true ;;
        server/user1)  srv_user user1 "$cmd" >> "$file" 2>&1 || true ;;
        server/user2)  srv_user user2 "$cmd" >> "$file" 2>&1 || true ;;
        client)        cli "$cmd"        >> "$file" 2>&1 || true ;;
    esac
    echo "→ $name"
}

echo "==> Поднимаем стенд (docker compose up --build)"
compose up -d --build
sleep 3

# ---------- Этап 1: подготовка (пункты 1-2) ----------
log_step server 01_system_info "uname -a && cat /etc/os-release | head -5"
log_step server 02_apt_update  "apt-get -qq update && echo 'apt-get update: OK'"

# ---------- Этап 2: пользователи и группы (пункты 4-5) ----------
log_step server 03_group_info     "getent group ftp_users"
log_step server 04_user1_info     "id user1"
log_step server 05_user2_info     "id user2"
log_step server 06_passwd_entries "getent passwd user1 user2"

# ---------- Этап 3: директории и базовые права (пункты 6, 8, 9) ----------
log_step server 07_dirs           "ls -la /srv/ftp"
log_step server 08_dir_perms      "stat -c '%n %A (octal: %a) owner=%U group=%G' /srv/ftp /srv/ftp/user1 /srv/ftp/user2"

# setgid bit (2 в начале octal) демонстрирует «новые файлы наследуют группу».
log_step server 09_setgid_demo \
    "rm -f /tmp/setgid_demo && touch /srv/ftp/_setgid_test.txt && stat -c '%n group=%G' /srv/ftp/_setgid_test.txt && rm -f /srv/ftp/_setgid_test.txt"

# ---------- Этап 4: ACL (пункты 10) ----------
log_step server 10_acl_installed "dpkg -l | grep -E '^ii\\s+acl' || apt-cache show acl | head -3"
log_step server 11_getfacl_root  "getfacl /srv/ftp"
log_step server 12_getfacl_user1 "getfacl /srv/ftp/user1"
log_step server 13_getfacl_user2 "getfacl /srv/ftp/user2"

# ---------- Этап 5: проверка изоляции (пункты 13-15) ----------
log_step server/user1 14_user1_create_file \
    "cd /srv/ftp/user1 && echo 'hello from user1' > my_file.txt && ls -la my_file.txt && stat -c '%n owner=%U group=%G perms=%a' my_file.txt"

log_step server/user2 15_user2_cannot_read_user1 \
    "ls -la /srv/ftp/user1/ 2>&1; cat /srv/ftp/user1/my_file.txt 2>&1; echo '--- exit: '\$?"

log_step server/user2 16_user2_create_file \
    "cd /srv/ftp/user2 && echo 'hello from user2' > note.txt && ls -la"

log_step server/user1 17_user1_cannot_read_user2 \
    "ls -la /srv/ftp/user2/ 2>&1; cat /srv/ftp/user2/note.txt 2>&1; echo '--- exit: '\$?"

# ---------- Этап 6: SSH с клиента (пункт 13) ----------
log_step client 18_ssh_user1 \
    "sshpass -p pass1 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null user1@172.31.0.10 'whoami && id && ls -la /srv/ftp/user1/'"

log_step client 19_ssh_user2 \
    "sshpass -p pass2 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null user2@172.31.0.10 'whoami && id && ls -la /srv/ftp/user2/ && echo --- user1: && ls -la /srv/ftp/user1/ 2>&1'"

# ---------- Этап 7: auditd (пункты 16-18) ----------
log_step server 20_audit_installed "dpkg -l | grep -E '^ii\\s+auditd' | awk '{print \$2, \$3}'"
log_step server 21_audit_rules     "cat /etc/audit/rules.d/ftp.rules"
log_step server 22_auditctl_status "auditctl -s 2>&1 || true"
log_step server 23_auditctl_list   "auditctl -l 2>&1 || true"
log_step server 24_audit_log       "tail -30 /var/log/audit/audit.log 2>&1 || cat /var/log/auditd-startup.log 2>&1 || echo '(audit недоступен — ядро Docker без CONFIG_AUDIT)'"

# В Docker под macOS audit-subsystem ядра обычно отсутствует, поэтому
# параллельно показываем функционально близкий способ через journalctl-эквивалент
# и ручную проверку доступов (stat, getfacl).
log_step server 25_alternative_audit \
    "echo '--- ls с timestamps ---' && find /srv/ftp -type f -printf '%T+ %M %u:%g %p\\n'"

# ---------- Итог ----------
log_step server 26_summary \
    "echo '=== /srv/ftp structure ===' && ls -laR /srv/ftp && echo && echo '=== ACL ===' && getfacl /srv/ftp /srv/ftp/user1 /srv/ftp/user2 2>/dev/null"

echo "==> Готово. Артефакты в $ART_DIR"
ls -la "$ART_DIR"

echo
echo "Останавливаем стенд (docker compose down)…"
compose down
