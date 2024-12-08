## 4) Добавить в контекстное меню проводника File Explorer для файлов с расширением *.ps1, пункт, позволявший запустить скрипт PowerShell с правами администратора.


### Реализация зависит от версии ОС

Вариант 1 (Windows 10 до 22H2): 

- Запустите редактор реестра (regedit.exe)

- Перейдите в ветку HKEY_CLASSES_ROOT\Microsoft.PowerShellScript.1\shell

- Создайте подраздел с именем runas и перейдите в него

- Внутри раздела runas создайте пустой строковый параметр (String Value) с именем HasLUAShield (этот параметр добавит иконку UAC в контекстное меню проводника)

- В разделе runas создайте вложенный подраздел command

- В качестве значения параметра Default раздела command укажите значение: 
```
powershell.exe –NoExit "-Command" "if((Get-ExecutionPolicy ) -ne 'AllSigned') { Set-ExecutionPolicy -Scope Process Bypass }; & '%1'"
```

- Теперь, если щелкнуть ПКМ по любому *.PS1 файлу, в контекстном меню можно выбрать пункт Run as administrat

[Это сайт с картинками](https://winitpro.ru/index.php/2016/09/30/zapusk-powershell-skripta-iz-provodnika-s-pravami-administratora/)


Вариант 2 (Windows 11 22H2):

- Запустите редактор реестра (regedit.exe)

- Перейдите в ветку HKEY_CLASSES_ROOT\SystemFileAssociations\.ps1\Shell\

- Создайте подраздел с именем runas и перейдите в него

- Внутри раздела runas создайте пустой строковый параметр (String Value) с именем HasLUAShield (этот параметр добавит иконку UAC в контекстное меню проводника)

- В разделе runas создайте вложенный подраздел command

- В качестве значения параметра Default раздела command укажите значение: 
```
@=»powershell.exe \»-Command\» \»if((Get-ExecutionPolicy ) -ne ‘AllSigned’) { Set-ExecutionPolicy -Scope Process Bypass }; & ‘%1’\»»
```

- Теперь, если щелкнуть ПКМ по любому *.PS1 файлу, в контекстном меню можно выбрать пункт Run as administrat
