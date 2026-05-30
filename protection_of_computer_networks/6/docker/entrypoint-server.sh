#!/usr/bin/env bash
# Поднимает sshd, создаёт группу ftp_users, пользователей user1/user2,
# директории /srv/ftp/{user1,user2}, расставляет права через chmod/chown/setfacl,
# запускает auditd. Соответствует пунктам 4–17 рабочего задания.

set -euo pipefail

echo "==> [server] Создание группы ftp_users"
getent group ftp_users >/dev/null || groupadd ftp_users

echo "==> [server] Создание пользователей user1, user2"
for u in user1 user2; do
    if ! id -u "$u" >/dev/null 2>&1; then
        useradd -m -s /bin/bash -G ftp_users "$u"
        echo "${u}:pass${u#user}" | chpasswd
    fi
done

echo "==> [server] Создание директории /srv/ftp и подкаталогов"
mkdir -p /srv/ftp/user1 /srv/ftp/user2
chown root:ftp_users /srv/ftp
chmod 2770 /srv/ftp                 # setgid: новые файлы наследуют группу ftp_users

chown user1:ftp_users /srv/ftp/user1
chown user2:ftp_users /srv/ftp/user2
chmod 2770 /srv/ftp/user1 /srv/ftp/user2

echo "==> [server] Настройка ACL"
# Дефолтный ACL: новые файлы получают rwx для владельца, rwx для группы, и
# rwX-маску — корректно для shared-каталога.
setfacl -d -m g:ftp_users:rwx /srv/ftp /srv/ftp/user1 /srv/ftp/user2 || true
# user1 не должен видеть содержимое user2 и наоборот — ставим явный deny через ACL.
setfacl -m u:user2:--- /srv/ftp/user1
setfacl -m u:user1:--- /srv/ftp/user2

echo "==> [server] Запуск sshd"
/usr/sbin/sshd

echo "==> [server] Попытка запустить auditd (нужны CAP_AUDIT_*)"
if auditd -f -s nochange 2>/var/log/auditd-startup.log &
then
    AUDITD_PID=$!
    sleep 1
    if kill -0 "$AUDITD_PID" 2>/dev/null; then
        echo "    auditd запущен (pid=$AUDITD_PID)"
        # Загружаем правила.
        auditctl -R /etc/audit/rules.d/ftp.rules || true
    else
        echo "    [WARN] auditd упал — ядро LinuxKit на macOS обычно не содержит CONFIG_AUDIT"
        cat /var/log/auditd-startup.log 2>/dev/null || true
    fi
else
    echo "    [WARN] не удалось запустить auditd"
fi

echo "==> [server] Готово, ждём команды через docker exec"
exec sleep infinity
