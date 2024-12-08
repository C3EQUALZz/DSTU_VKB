## Создать текстовый файл, содержащий справочные сведения по командам DIR, COPY и XCOPY.

Здесь можно сделать по-разному, предложу пару вариантов

### Вариант 1
```
help DIR > help-dir.txt
help COPY > help-copy.tx
help XCOPY > help-xcopy.txt
COPY help-dir.txt + help-copy.txt + help-xcopy.txt result.txt
```

### Вариант 2
```
help dir > result.txt
help copy >> result.txt
help xcopy >> result.txt
```

