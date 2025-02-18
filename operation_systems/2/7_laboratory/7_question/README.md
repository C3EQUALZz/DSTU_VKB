## Конфигурационные файлы в каталоге `/etc/pam.d/` можно создавать только для файлов которые используют систему `PAM`. Создайте файл `/etc/pam.d/ls` со строкой `auth requisite pam_deny.so` `# touch /etc/pam.d/ls` `# vi /etc/pam.d/ls` `auth required pam_permit.so` Проверьте, будет ли выполнятся команда `ls`? Какой результат? Скриншоты.

Создание файла `/etc/pam.d/ls` с содержимым:

```bash
echo "auth requisite pam_deny.so" | sudo tee /etc/pam.d/ls 
```

