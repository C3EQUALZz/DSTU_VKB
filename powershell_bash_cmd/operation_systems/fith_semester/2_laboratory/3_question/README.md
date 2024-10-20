## Вывести в текстовый файл список свойств процесса, возвращаемый командлетом Get-process и на экран – их общее количество

Важно поменяйте путь на результирующий файл на ваше расположение, посмотрите на путь правее от tee. 

```
$properties = Get-Process | Get-Member -MemberType Property | Select-Object -ExpandProperty Name
$properties | tee "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\2_laboratory\3_question\result.txt"
$properties.Count
```

Объяснение:

Здесь я создал переменную properties, к ней привязываю команды, а потом загружаю его в txt файл.