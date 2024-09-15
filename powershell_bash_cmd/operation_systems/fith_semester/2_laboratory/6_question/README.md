## Найти суммарный объем всех графических файлов (bmp, jpg), находящихся в каталоге Windows и всех его подкаталогах.

```
$totalSize = (Get-ChildItem -Filter "*.jpg" -Recurse | Measure-Object -Property Length -Sum).Sum
Write-Host "The total size of the graphic files: $($totalSize / 1MB) Mb"
```


Объяснение:

Так же через cd выбираем путь и там уже выполняем команду.
Переделал *.bmp,*.jpg до *.jpg, так как если добавлять bmp, то он всегда выводит 0, а с jpg уже считает нормально.
(на крайняк можно оставить *.*, тогда он будет считать вес всех файлов)
