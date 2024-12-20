## Организовать запуск PowerShell скрипта при загрузке компьютера с помощью групповой политики. 

Вариант для домашней версии: 

В домашней версии можно реализовать запуск через планировщик задач.

- Для этого создаём простую задачу
- Задаём имя задаче для задания 6-1 выбираем запуск при входе в Windows
- Запуск программы
- В программу или сценарий вводим путь до PowerShell.exe (C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe)
- В аргумент добавляем -File [путь до вашего скрипта]
- Сохраняем и запускаем для проверки через планировщик

Вариант для нормальной системы:

- Создание скрипта
- Создайте PowerShell скрипт, который вы хотите запускать при загрузке компьютера. Например, сохраните его как StartupScript.ps1. 
- Создание задачи в планировщике задач

- Создайте задачу в планировщике задач, которая будет запускать ваш PowerShell скрипт при загрузке компьютера.

    - Откройте "Планировщик задач" (Task Scheduler).
    - В правой панели выберите "Создать задачу" (Create Task).
    - На вкладке "Общие" (General) введите имя задачи, например, "Run PowerShell Script at Startup".
    - На вкладке "Триггеры" (Triggers) нажмите "Создать" (New) и выберите "При загрузке" (At startup). Нажмите "ОК".
    - На вкладке "Действия" (Actions) нажмите "Создать" (New) и выберите "Запустить программу" (Start a program).
        - В поле "Программа или скрипт" (Program/script) введите powershell.exe.
        - В поле "Добавить аргументы (необязательно)" (Add arguments (optional)) введите -File "D:\PycharmProjects\DSTU_VKB\operation_systems\1\3_laboratory\6_question\1_sub\hello.ps1".
        - Нажмите "ОК".
    - На вкладке "Параметры" (Settings) выберите "Разрешить запуск при запросе" (Allow task to be run on demand) и "Запускать задачу при доступности" (Run task as soon as possible after a scheduled start is missed).
    - Нажмите "ОК" для сохранения задачи.

- Настройка групповой политики для запуска задачи

    - Откройте редактор групповой политики (Group Policy Editor). Для этого нажмите Win + R, введите gpedit.msc и нажмите Enter.
    - Перейдите в раздел "Конфигурация компьютера" (Computer Configuration) -> "Административные шаблоны" (Administrative Templates) -> "Система" (System) -> "Планировщик задач" (Task Scheduler).
    - Найдите и откройте параметр "Планировщик задач: Разрешить запуск задач при загрузке" (Task Scheduler: Allow Task To Run On Demand).
    - Установите параметр на "Включено" (Enabled).
    - Нажмите "ОК" для сохранения изменений.

- Экспорт и импорт задачи через групповую политику

    - Экспортируйте созданную задачу из планировщика задач:
        - Откройте "Планировщик задач" (Task Scheduler).
        - Найдите вашу задачу в библиотеке планировщика задач.
        - Щелкните правой кнопкой мыши на задаче и выберите "Экспорт" (Export).
        - Сохраните задачу в файл с расширением .xml.

    - Импортируйте задачу через групповую политику:
        - Откройте редактор групповой политики (Group Policy Editor).
        - Перейдите в раздел "Конфигурация компьютера" (Computer Configuration) -> "Настройки" (Preferences) -> "Параметры Windows" (Windows Settings) -> "Планировщик задач" (Scheduled Tasks).
        - Щелкните правой кнопкой мыши на "Планировщик задач" (Scheduled Tasks) и выберите "Создать" (Create) -> "Импорт задачи" (Import Task).
        - Укажите путь к экспортированному файлу задачи (.xml).
        - Нажмите "ОК" для импорта задачи.
