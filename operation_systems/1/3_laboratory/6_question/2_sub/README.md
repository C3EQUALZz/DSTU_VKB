## С помощью PowerShell создать новые задания планировщика Windows, экспортировать задания в xml-файл. Задача - создать задание планировщика которое бы запускалось в определенное время, задание должно выполнять некий PowerShell скрипт или команду.

> [!NOTE]
> Примечание. PowerShell предоставляет возможность экспортировать текущие настройки любого задания планировщика в текстовый XML файл.
> Таким образом можно выгрузить параметры любого задания и распространить задание любой сложности на другие компьютеры сети.
> Экспорт задания может быть выполнен как из графического интерфейса Task Scheduller, так и из командой строки PowerShell.

Запускайте от имени администратора, обязательно в файле `execute.ps1` поменять время на 1 минуту вперед от того, что у вас сейчас. 