> Это простое приложение с выбором лабораторных, имеется поддержка под Windows, Linux, Mac

![img.png](photo_description/img.png)
![img_1.png](photo_description/img_1.png)

### Замечания и предупреждения по использованию

Важно, что приложение является модульным, не нужно вручную добавлять условия и ссылки на задания.
Главное, чтобы вы папку с заданиями называли с использованием порядковых числительных на английском.
Например, "first_laba_lang". Обязательно в конце "lang".

Стили приложения можете менять по своему, но тут надо быть аккуратным.

Учитывайте, что если функция изначально по вашей задумке не принимает аргументов,
то надо сделать затычку "s=None", так как из-под приложения идет передача аргумента с QLineEdit.
Если вы ничего не вписывали, то там будет пустая строка, то есть пустая строка будет передаваться функции.

Если в лабораторной работе не 4 задания, то нужно самому это исправлять в main_interface. 