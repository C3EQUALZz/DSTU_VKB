## Создать файл `/etc/pam.d/su` и написать в нем такую строку: `auth sufficient pam_permit.so` Сохранить. Снова выполнить команду `su` из под пользвателя `student`, что произошло? Скриншот. Это произошло потому, что модуль `pam_permit.so` всегда возвращает положительный результат, `sufficient` тут же прерывает выполнение цепочки и система `PAM` возвращает положительный результат. Отредактируйте файл к следующему виду: `auth required pam_permit.so`; `auth requisite pam_deny.so`; `auth sufficient pam_permit.so` Модуль `pam_deny.so` всегда возвращает ошибку. Какой будет результат? Проверьте. А если заменить `requisite` на `required`? Скриншоты. 

Создание файла `/etc/pam.d/su` с содержимым: `echo "auth sufficient pam_permit.so" | sudo tee /etc/pam.d/su` --всегда разрешает

Редактирование файла /etc/pam.d/su:

nano /etc/pam.d/su

--заменить полностью

auth required pam_permit.so 
auth requisite pam_deny.so 
auth sufficient pam_permit.so 

-- после этого всегда будет выводится ошибка