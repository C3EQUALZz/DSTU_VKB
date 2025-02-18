## Измените файл, укажите две строки: `auth requisite pam_wheel.so`, `auth required pam_permit.so`. Ответить кто сможет успешно выполнить команду `su` и, что для этого нужно будет сделать? После выполнения задания верните на место оригинальный файл `su`.

Изменение файла /etc/pam.d/su:

nano /etc/pam.d/su

--добавить

auth requisite pam_wheel.so 
auth required pam_permit.so

--в файле должна быть только

вернуть исходный файл на место

rm /etc/pam.d/su
sudo mv /home/astrastud/su_backup /etc/pam.d/su