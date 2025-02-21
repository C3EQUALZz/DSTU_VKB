## Вы должны находится под пользователем `root/` Перейдите в каталог `/etc/pam.d/`. Перенесите файл su в домашнюю директорию (чтобы можно было восстановить его). Выполните команду `su` из-под пользователя `student` в терминале, чтобы перейти в режим суперпользователя. После ввода пароля система выдаст ошибку аутентификации, так как отсутствует `123` конфигурационный файл для программы `su`, сделать скриншот.

> [!IMPORTANT]
> Для выполнения задания я пользовался терминалом, который открывается через приложение `Konsole`.

Перейдем в рута, используя команду, которая представлена ниже: 

```bash
sudo su
```

Теперь перейдем в директорию `/etc/pam.d/`, используя команду, которая представлена ниже:

```bash
cd /etc/pam.d
```

Теперь сделаем перенос файла `su`, используя команду ниже:

```bash
sudo mv /etc/pam.d/su ~/su_backup 
```

Теперь попробуем выполнить команду, которая представлена ниже:

```bash
sudo su
```

> [!IMPORTANT]
> - Будет выведен сбой при проверке подлинности.
> - Лучше верните `su` обратно. Для этого выполните команду: `sudo mv ~/su_backup /etc/pam.d/su`

![изображение](https://github.com/user-attachments/assets/c01b5aef-32d3-4da9-82d6-b687d0b398f5)

<details>
    <summary>Бэкап</summary>

```bash
#
# The PAM configuration file for the Shadow `su' service
#

# This allows root to su without passwords (normal operation)
auth       sufficient pam_rootok.so

# Uncomment this to force users to be a member of group wheel
# before they can use `su'. You can also add "group=foo"
# to the end of this line if you want to use a group other
# than the default "wheel" (but this may have side effect of
# denying "root" user, unless she's a member of "foo" or explicitly
# permitted earlier by e.g. "sufficient pam_rootok.so").
# (Replaces the `SU_WHEEL_ONLY' option from login.defs)
# auth       required   pam_wheel.so

# Uncomment this if you want wheel members to be able to
# su without a password.
# auth       sufficient pam_wheel.so trust

# Uncomment this if you want members of a specific group to not
# be allowed to use su at all.
# auth       required   pam_wheel.so deny group=nosu

# Uncomment and edit /etc/security/time.conf if you need to set
# time restrainst on su usage.
# (Replaces the `PORTTIME_CHECKS_ENAB' option from login.defs
# as well as /etc/porttime)
# account    requisite  pam_time.so

# This module parses environment configuration file(s)
# and also allows you to use an extended config
# file /etc/security/pam_env.conf.
# 
# parsing /etc/environment needs "readenv=1"
session       required   pam_env.so readenv=1
# locale variables are also kept into /etc/default/locale in etch
# reading this file *in addition to /etc/environment* does not hurt
session       required   pam_env.so readenv=1 envfile=/etc/default/locale

# Defines the MAIL environment variable
# However, userdel also needs MAIL_DIR and MAIL_FILE variables
# in /etc/login.defs to make sure that removing a user 
# also removes the user's mail spool file.
# See comments in /etc/login.defs
#
# "nopen" stands to avoid reporting new mail when su'ing to another user
session    optional   pam_mail.so nopen

# Sets up user limits according to /etc/security/limits.conf
# (Replaces the use of /etc/limits in old login)
session    required   pam_limits.so

# The standard Unix authentication modules, used with
# NIS (man nsswitch) as well as normal /etc/passwd and
# /etc/shadow entries.
@include common-auth
@include common-account
@include common-session
session required pam_parsec_cap.so
session required pam_parsec_aud.so


account required pam_su.so
```
</details>