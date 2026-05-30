#!/usr/bin/env bash
# Ждёт пока KDC выгрузит host-keytab в общий volume и копирует его в /etc/krb5.keytab,
# затем поднимает sshd с GSSAPI.

set -euo pipefail

SHARED_KEYTAB="/etc/krb5_shared/target.keytab"

echo "==> [target] Ожидаем keytab от KDC: ${SHARED_KEYTAB}"
for i in $(seq 1 60); do
    if [[ -s "${SHARED_KEYTAB}" ]]; then
        echo "==> [target] Keytab получен (попытка ${i})"
        break
    fi
    sleep 1
done

if [[ ! -s "${SHARED_KEYTAB}" ]]; then
    echo "[target] Keytab так и не появился за 60 секунд" >&2
    exit 1
fi

cp "${SHARED_KEYTAB}" /etc/krb5.keytab
chown root:root /etc/krb5.keytab
chmod 600 /etc/krb5.keytab

echo "==> [target] Содержимое keytab:"
klist -k /etc/krb5.keytab || true

echo "==> [target] Запуск sshd"
exec /usr/sbin/sshd -D -e
