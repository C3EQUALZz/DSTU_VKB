#!/usr/bin/env bash
# Прогон лабораторной работы №1 «Kerberos».
# Покрывает 10 практических заданий методички: установка KDC (через Dockerfile),
# настройка клиента, kinit, klist, SSH по Kerberos, kvno, kdestroy, анализ логов.
# Вывод каждого шага → artifacts/NN_*.txt, листинги отчёта читают эти файлы.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE_DIR="$ROOT/docker"
ART_DIR="$ROOT/artifacts"

rm -rf "$ART_DIR"
mkdir -p "$ART_DIR"

compose() {
    docker compose -f "$COMPOSE_DIR/docker-compose.yml" "$@"
}

kdc()    { compose exec -T kdc    bash -lc "$*"; }
tgt()    { compose exec -T target bash -lc "$*"; }
cli()    { compose exec -T client bash -lc "$*"; }
cli_u()  { compose exec -T -u labuser client bash -lc "$*"; }

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
        kdc)         kdc "$cmd"   >> "$file" 2>&1 || true ;;
        target)      tgt "$cmd"   >> "$file" 2>&1 || true ;;
        client)      cli "$cmd"   >> "$file" 2>&1 || true ;;
        client/lab)  cli_u "$cmd" >> "$file" 2>&1 || true ;;
    esac
    echo "→ $name"
}

echo "==> Поднимаем стенд (docker compose up --build)"
compose up -d --build

echo "==> Ждём, пока target подберёт keytab и поднимет sshd"
for i in $(seq 1 30); do
    if compose exec -T target test -s /etc/krb5.keytab 2>/dev/null; then
        echo "    target готов (попытка ${i})"
        break
    fi
    sleep 1
done
sleep 2

# ---------- Задание 1: установка и настройка KDC ----------
log_step kdc 01_kdc_config    "cat /etc/krb5.conf"
log_step kdc 02_kdc_conf      "cat /etc/krb5kdc/kdc.conf"
log_step kdc 03_kdc_acl       "cat /etc/krb5kdc/kadm5.acl"
log_step kdc 04_kdc_principals "kadmin.local -q 'listprincs'"
log_step kdc 05_kdc_services  "ss -tulpn | grep -E ':(88|464|749)' || netstat -tulpn 2>/dev/null | grep -E ':(88|464|749)' || true"

# ---------- Задание 2-3: kinit/klist на клиенте ----------
log_step client 06_client_krb5conf "cat /etc/krb5.conf"
log_step client 07_kinit_admin     "echo 'admin1234' | kinit admin/admin@LAB.LOCAL && klist"
log_step client 08_klist_flags     "klist -f"
log_step client 09_klist_enctypes  "klist -e"

# ---------- Задание 5: новый principal и проверка доступа ----------
# admin/admin создаёт нового пользователя через kadmin (не kadmin.local!) — это
# и есть демонстрация делегирования административных прав через ACL.
log_step client 10_kadmin_addprinc \
    "printf 'admin1234\n' | kadmin -p admin/admin -q 'addprinc -pw testpass testuser@LAB.LOCAL'"
log_step client 11_kadmin_listprincs \
    "printf 'admin1234\n' | kadmin -p admin/admin -q 'listprincs'"
log_step client 12_kinit_testuser \
    "kdestroy -A && echo 'testpass' | kinit testuser@LAB.LOCAL && klist"

# ---------- Задание 4: SSH с Kerberos ----------
# Возвращаемся к labuser (под ним есть UNIX-аккаунт на target).
log_step client 13_kinit_labuser \
    "kdestroy -A && echo 'labpass' | kinit labuser@LAB.LOCAL && klist"
log_step client 14_ssh_kerberos \
    "ssh -K labuser@target.lab.local 'hostname && whoami && klist 2>/dev/null | head -10 || true'"
log_step client 15_klist_after_ssh "klist"

# ---------- Задание 7: анализ логов KDC ----------
log_step kdc 16_kdc_log_tgs   "grep -E 'TGS_REQ|AS_REQ' /var/log/krb5kdc.log | tail -n 20"
log_step kdc 17_kdc_log_full  "tail -n 30 /var/log/krb5kdc.log"

# ---------- Задание 6: kvno (проверка ключа сервиса) ----------
log_step client 18_kvno_host  "kvno host/target.lab.local@LAB.LOCAL"

# ---------- Задание 9: forwardable tickets и обновление ----------
log_step client 19_kinit_forwardable \
    "kdestroy -A && echo 'labpass' | kinit -f -l 1h -r 12h labuser@LAB.LOCAL && klist -f"
log_step client 20_kinit_renew "kinit -R && klist"

# ---------- Задание 10: проверочный bash-скрипт ----------
log_step client 21_check_script "cat <<'EOS' > /tmp/krb_check.sh && bash /tmp/krb_check.sh
#!/usr/bin/env bash
# Скрипт мониторинга Kerberos-аутентификации.
set -e

echo '--- 1. Проверка билета ---'
if klist -s; then
    echo 'OK: действующий билет есть'
    klist | head -5
else
    echo 'FAIL: билета нет'
    exit 1
fi

echo
echo '--- 2. Проверка доступности KDC по порту 88 ---'
if (echo > /dev/tcp/kdc.lab.local/88) 2>/dev/null; then
    echo 'OK: KDC отвечает на 88/tcp'
else
    echo 'FAIL: KDC недоступен'
    exit 2
fi

echo
echo '--- 3. Проверка ключа сервиса (kvno) ---'
if kvno host/target.lab.local@LAB.LOCAL; then
    echo 'OK: ключ сервиса host/target.lab.local получен'
else
    echo 'FAIL: kvno не работает'
    exit 3
fi
EOS"

# ---------- Задание 2: SSH с Kerberos без пароля (повторно для отчёта) ----------
log_step client 22_ssh_demo_passwordless \
    "ssh -o BatchMode=yes -K labuser@target.lab.local 'echo Kerberos-only auth: OK, hostname=$(hostname)'"

# ---------- kdestroy ----------
log_step client 23_kdestroy "kdestroy -A && klist 2>&1 || true"

# ---------- Финальный snapshot ----------
log_step kdc 24_final_principals "kadmin.local -q 'listprincs'"

echo "==> Готово. Артефакты в $ART_DIR"
ls -la "$ART_DIR"

echo
echo "Останавливаем стенд (docker compose down -v)…"
compose down -v
