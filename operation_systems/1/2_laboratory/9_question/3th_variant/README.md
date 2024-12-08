## Выполнить индивидуальные задания для студентов согласно (табл. 6).

- Нахождение чисел в файле

```
$fileContent = Get-Content -Path "C:\Users\1\Desktop\PowerShell\TestTXT.txt"

$numbers = $fileContent | Where-Object { $_ -match '^\d+$' }


Write-Host "number of words:"
$numbers
```

- Вывод строк с текстом, в которых слово начинает с заглавной буквы

```
$fileContent = Get-Content -Path "C:\Users\1\Desktop\PowerShell\TestTXT.txt"

$capitalizedWords = $fileContent | Where-Object { $_ -match '^([A-Z].*)' }

Write-Host "Uppercase words:"
$capitalizedWords
```

Объяснение: 

Убрал проверки на русские слова, так у меня при их вводе просто появляются пробелы, а смена кодировки не помогала, в ином случае, в конце просто нужно расширить регулярное выражение до [A-ZА-Я])
