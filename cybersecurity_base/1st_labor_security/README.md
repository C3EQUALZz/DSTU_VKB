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
    <p>Здесь присутствуют проверки методов с помощью <code>unittests</code>, но автор не гарантирует полное отсутствие ошибок. </p>
    <hr>
    <b>Важно для пользователей с Pycharm или других IDE, где есть venv!!!</b>
    <p>В пункте <code>Environmental variables</code> нужно добавить: </p>
</div>

```bash
DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1
```
<div style="font-family: FiraCode; font-size: 20px">
    <hr>
    <h5 align="center" style="font-size: 30px"> Установка зависимостей </h5>
    <span> Указанные библиотеки размещены на <a href="https://pypi.org/project/aspose-words/">PyPI</a> и могут быть установлены с помощью следующих команд: <br> </span>
</div>

```bash
pip install aspose-words
pip install aspose-cells
```

- [Требования для библиотеки aspose](https://docs.aspose.com/finance/python-net/system-requirements/)
- [Установка библиотек С# и зависимостей (Fedora)](https://developer.fedoraproject.org/tech/languages/dotnet/dotnetcore.html)
- [Установка библиотек С# и зависимостей (Manjaro)](https://www.jeremymorgan.com/tutorials/linux/how-to-install-dotnet-manjaro/)

<div style="font-family: FiraCode; font-size: 20px">
    <hr>
    <h5 align="center" style="font-size: 30px"> Логика алгоритма </h5>
    <span>
    Главный файл программы - <code>main.py</code>, где происходит взаимодействие с пользователем. 
    Скрипт запрашивает у пользователя путь к его файлу. Если формат файла корректен, программа запросит пароль, который
    должен соответствовать следующим стандартам:
        <li> Длина пароля должна быть больше 5 символов; </li>
        <li> Пароль должен содержать хотя бы одну цифру; </li>
    Затем программа предоставит пользователю варианты действий с файлом, как описано ранее.
    В некоторых случаях потребуется указать номер листа или диапазон. 
    Например, если пользователь хочет заблокировать файл, то будет вызван метод <code>block_file</code> у экземпляра класса,
    не зависящего от типа файла. Все последующие действия выполняются с использованием библиотеки <code>aspose</code>.
    Обратите внимание, что в процессе выполнения операций создается новый файл с тем же именем, но его оформление может 
    измениться из-за особенностей бесплатного API. Если программа вернула статус код 0, то она отработала. 
    </span>
    <hr>
    <h5 align="center" style="font-size: 30px"> Возможности класса WordBlock </h5>
    <span>
    <li> <code>block_file</code> - метод для блокировки файла с использованием заданного пароля с определенными 
параметрами. Из требуемых аргументов - пароль. Более подробно можете ознакомиться <a href="https://blog.aspose.com/ru/words/protect-word-documents-using-python">здесь</a>;</li>
    <li> <code>unblock_file</code> - это метод, который позволяет полностью разблокировать файл, сняв все поставленные
    до этого ограничения. Из требуемых аргументов - пароль. Более подробно можете ознакомиться <a href="https://blog.aspose.com/ru/words/unprotect-word-documents-in-python/">здесь</a>;</li>
    </span>
    <hr>
    <h5 align="center" style="font-size: 30px"> Возможности класса ExcelBlock </h5>
    <span>
    <li> <code>block_file</code> - метод для блокировки файла с использованием заданного пароля с определенными параметрами. 
    Более подробно с параметрами блокировки можете ознакомиться <a href="https://blog.aspose.com/ru/protect-unprotect-excel-files-in-python/">здесь</a>;</li>
    <li> <code>unblock_file</code> - метод, который позволяет снять все ограничения с <b>xlsx</b> файла, в аргументах ожидается пароль. Более подробно как это предлагают разработчики
    можете ознакомится <a href="https://blog.aspose.com/ru/protect-unprotect-excel-files-in-python/">здесь</a>;</li>
    <li><code>block_list</code> - метод, который блокирует отдельный лист. Ожидается номер страницы, который мы хотим заблокировать (нумерация начинается с 1),
    пароль, который мы хотим установить;</li>
    <li><code>unblock_list</code> - метод, который снимает все ограничения с листа. Ожидается номер страницы, который мы хотим разблокировать (нумерация начинается с 1),
    пароль;</li>
    <li><code>block_range</code> - это метод, который позволяет заблокировать диапазон у определенного листа. Изначально метод принимает нумерацию с 0, но для удобства пользователей в <code>main.py</code> нумерация с 1.
    Ожидается номер страницы, у которой мы хотим заблокировать диапазон, и диапазон в виде <code>A1:C3</code>;</li>
    <li><code>unblock_range</code> - это метод, который позволяет снять ограничения с диапазона у определенного листа. 
    Ожидается номер страницы и диапазон; </li>
    </span>
</div>
</body>
