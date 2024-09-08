## Скопировать все имеющиеся в каталоге Windows растровые графические файлы в каталог WinGrafika на диске С:. Если диск С: недоступен, использовать любой другой доступный диск. 

Если нужно создать папку заранее, то делаем команду
```
MD  D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\1_laboratory\7_question\WinEx
```

Команда для создания 
```
COPY %WINDIR%\*.png D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\1_laboratory\7_question\WinEx /S & %WINDIR%\*.jpg D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\1_laboratory\7_question\WinEx /S
```



---

## Скопировать все имеющиеся в каталоге Windows исполняемые файлы в каталог WinEx на диске С:. Если диск С: недоступен, использовать любой другой доступный диск.

Если нужно создать папку заранее, то делаем команду

```
MD  D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\1_laboratory\7_question\WinEx
```

```
COPY %WINDIR%\*.exe D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\1_laboratory\7_question\WinEx
```