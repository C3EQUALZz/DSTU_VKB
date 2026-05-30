#!/usr/bin/env bash
# Поднимает KDC, создаёт базу, заводит admin/admin, labuser и host/target.lab.local,
# выгружает host-keytab в общий volume — оттуда target подберёт его при старте.

set -euo pipefail

REALM="LAB.LOCAL"
MASTER_PASS="1234"
ADMIN_PASS="admin1234"
USER_PASS="labpass"
SHARED_KEYTAB_DIR="/etc/krb5_shared"
TARGET_KEYTAB="${SHARED_KEYTAB_DIR}/target.keytab"

mkdir -p "${SHARED_KEYTAB_DIR}"

if [[ ! -f /var/lib/krb5kdc/principal ]]; then
    echo "==> [kdc] Создаём базу realm ${REALM}"
    printf '%s\n%s\n' "${MASTER_PASS}" "${MASTER_PASS}" \
        | kdb5_util create -r "${REALM}" -s

    echo "==> [kdc] Заводим admin/admin@${REALM}"
    kadmin.local -q "addprinc -pw ${ADMIN_PASS} admin/admin@${REALM}"

    echo "==> [kdc] Заводим labuser@${REALM}"
    kadmin.local -q "addprinc -pw ${USER_PASS} labuser@${REALM}"

    echo "==> [kdc] Заводим host/target.lab.local@${REALM}"
    kadmin.local -q "addprinc -randkey host/target.lab.local@${REALM}"

    echo "==> [kdc] Выгружаем keytab для target в ${TARGET_KEYTAB}"
    kadmin.local -q "ktadd -k ${TARGET_KEYTAB} host/target.lab.local@${REALM}"
    chmod 644 "${TARGET_KEYTAB}"
else
    echo "==> [kdc] База уже инициализирована, пропускаем bootstrap"
fi

echo "==> [kdc] Запуск krb5kdc и kadmind"
/usr/sbin/krb5kdc
/usr/sbin/kadmind

# Логи KDC: дублируем хвост в stdout контейнера.
touch /var/log/krb5kdc.log /var/log/kadmind.log
exec tail -F /var/log/krb5kdc.log /var/log/kadmind.log
