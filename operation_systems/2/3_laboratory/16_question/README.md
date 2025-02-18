## С помощью команды kill -9 PID отправьте этому процессу сигнал принудительного завершения. С другой консоли проконтролируйте выполнение команды. Остановился ли процесс? Остался ли он в списке процессов? Какая программа на самом деле перехватывает и исполняет команду kill -9 PID?

Перейдем во 2 консоль. Для этого используйте комбинацию клавиш, которая представлена ниже: 

```bash
CTRL + ALT + F2
```

Как только перешли во вторую консоль, набираем команду в терминале для запуска процесса. 
Это будет тот же наш скрипт, который до этого писали: 

```bash
./abcd
```

Теперь перейдем в 1 консоль. Для этого используйте комбинацию клавиш, которая представлена ниже: 

```bash
CTRL + ALT + F1
```

Теперь остается Вам только убить процесс, узнав заранее его идентификатор. 

```bash
kill -9 PID
```

> [!NOTE]
> `PID` - номер процесса, его можно узнать через `top`
> `kill -9 PID` - принудительное завершение без перехвата.


