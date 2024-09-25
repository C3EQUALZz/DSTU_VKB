## 10) С помощью PowerShell создать Zip-архив и распаковать его.

### 1. Чтобы заархивировать `Compress-Archive [-Path] String[] [-DestinationPath] String  [-CompressionLevel String ] [-Update]`

- `Path` - задаётся путь к файлам или каталогам, которые нужно заархивировать
- `DestinationPath` – указывает местоположение создаваемого ZIP файла
- `CompressionLevel` – задает уровень сжатия (NoCompression, Optimal или Fastest)
- `Update` — позволяет добавить/обновить файлы в уже существующем ZIP архиве	
- `Force` — если архив с указанным именем уже существует, он будет перезаписан

Уточнение: 

```
Compress-Archive -Path [Сюда вводите путь без скобок что заархивировать] -DestinationPath [Сюда вводим путь, куда сохранять архив, и название файла с расширением .zip Также без скобок] -CompressionLevel Optimal
```

Пример, я архивирую каталог с лабами для powershell

```
Compress-Archive -Path D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\10_sub\LABA3 -DestinationPath D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\10_sub\archive.zip -CompressionLevel Optimal
```


### 2. Чтобы распаковать zip файл есть команда `Expand-Archive [-Path] String [-DestinationPath] String [-Force]  [-Confirm]`

Пример распаковки файла, полученного выше (учитываем, что будет распаковано именно содержимое, а не создаваться отдельный каталог с названием архива и его содержимым)

```
Expand-Archive -Path D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\10_sub\archive.zip -DestinationPath D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\10_sub
```

- `Path` - задаётся путь к архиву, который нужно распаковать
- `DestinationPath` – указывает местоположение распаковки содержимого архива	
- `Force` — если содержимое с указанным именем уже существует, оно будет перезаписано
- `Confirm` - отображение приглашение подверждения перед выполнением действия