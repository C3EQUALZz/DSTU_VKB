## Создать файл `/etc/pam.d/su` и написать в нем такую строку: `auth sufficient pam_permit.so` Сохранить. Снова выполнить команду `su` из под пользвателя `student`, что произошло? Скриншот. Это произошло потому, что модуль `pam_permit.so` всегда возвращает положительный результат, `sufficient` тут же прерывает выполнение цепочки и система `PAM` возвращает положительный результат. Отредактируйте файл к следующему виду: `auth required pam_permit.so`; `auth requisite pam_deny.so`; `auth sufficient pam_permit.so` Модуль `pam_deny.so` всегда возвращает ошибку. Какой будет результат? Проверьте. А если заменить `requisite` на `required`? Скриншоты. 

> [!IMPORTANT]
> Для выполнения задания я пользовался терминалом, который открывается через комбинацию (`CTRL + ALT + F<number>`), где `number` - это число от 1 до 6.

В начале войдите под главного пользователя, котого создали в системе. В моем случае - это `c3equalz`. 

Теперь перейдем к созданию файла `/etc/pam.d/su`, для этого используйте команду, которая представлена ниже:

```bash
echo "auth sufficient pam_permit.so" | sudo tee /etc/pam.d/su
```

> [!NOTE]
> Всегда разрешает создавать.

Для редактирование файла `/etc/pam.d/su` используйте команду, которая представлена ниже:

```bash
nano /etc/pam.d/su
```

Теперь в файле замените все строки полностью, чтобы 

```bash
auth required pam_permit.so 
auth requisite pam_deny.so 
auth sufficient pam_permit.so 
```

> [!NOTE]
> После этого всегда будет выводится ошибка.

![изображение](https://github.com/user-attachments/assets/c2ecfb47-4876-4c22-b5b0-965d4ac52b0e)
