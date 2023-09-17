<!DOCTYPE html>
<body>
<h3 align="center"> Проект: PyOfficeBlocker
    <a href="https://github.com/C3EQUALZz">
        <img src="https://skillicons.dev/icons?i=python,cs,linux" align="center"/>
    </a>
</h3>
<div style="font-family: FiraCode; font-size: 20px">
    <hr>
    <p> Данная программа позволяет пользователю в автоматическом порядке изменять состояние файла <b>.docx, .xlsx</b>. Есть такая возможность, как: </p>
    <li> Заблокировать файл с собственным паролем; </li>
    <li> Снять все ограничения с файла, если пользователь помнит пароль; </li>
    <li> Защитить лист, если у нас <b>.xlsx(.xls) </b>файл; </li>
    <li> Разблокировать лист, если у нас <b>.xlsx(.xls) </b>файл; </li>
    <li> Заблокировать диапазон, если у нас <b>.xlsx(.xls) </b>файл; </li>
    <li> Разблокировать диапазон, если у нас <b>.xlsx(.xls) </b>файл; </li>
</div>

<div style="font-family: FiraCode; font-size: 20px">
    <hr>
    <p>Данная программа протестирована на: </p>
    <li> <img height="15px" src="https://www.svgrepo.com/show/306371/manjaro.svg"/> Manjaro 23.0; </li>
    <li> <img height="15px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fedora/fedora-original.svg" /> Fedora 38; </li>
    <p>Здесь присутствуют unittests, но автор не гарантирует полное отсутствие ошибок. </p>
    <hr>
    <b>Важно для пользователей с Pycharm или других IDE, где есть venv!!!</b>
    <p>В пункте <b>Environmental variables</b> нужно добавить: </p>
</div>

```bash
DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1
```
<div style="font-family: FiraCode; font-size: 20px">
    <hr>
    <h5 align="center" style="font-size: 30px"> Установка зависимостей </h5>
</div>

- [Требования для библиотеки aspose](https://docs.aspose.com/finance/python-net/system-requirements/)
- [Установка библиотек С# и зависимостей (Fedora)](https://developer.fedoraproject.org/tech/languages/dotnet/dotnetcore.html)
- [Установка библиотек С# и зависимостей (Manjaro)](https://www.jeremymorgan.com/tutorials/linux/how-to-install-dotnet-manjaro/)

<div style="font-family: FiraCode; font-size: 20px">
    <hr>
    <h5 align="center" style="font-size: 30px"> Логика алгоритма </h5>
    <span>
    Главный файл программы - <b>main.py</b>, где происходит взаимодействие с пользователем. 
    Скрипт запрашивает у пользователя путь к его файлу. Если формат файла корректен, программа запросит пароль, который
    должен соответствовать следующим стандартам:
        <li> Длина пароля должна быть больше 5 символов; </li>
        <li> Пароль должен содержать хотя бы одну цифру; </li>
    Затем программа предоставит пользователю варианты действий с файлом, как описано ранее.
    Например, если пользователь хочет заблокировать файл, то будет вызван метод <b>block_file</b> у экземпляра класса,
    не зависящего от типа файла. Все последующие действия выполняются с использованием библиотеки <b>aspose</b>.
    Обратите внимание, что в процессе выполнения операций создается новый файл с тем же именем, но его оформление может 
    измениться из-за особенностей бесплатного API. Если программа вернула статус код 0, то она отработала. 
    </span>
</div>
</body>
