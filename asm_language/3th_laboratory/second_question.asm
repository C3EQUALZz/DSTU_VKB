; Найти сумму всех положительных и отрицательных чисел. Массив слов.

data segment
    array dw 10,0,12,479,-347,40,50,70,124,97
    positive dw ?
    negative dw ?
data ends

code segment
    assume cs: code, ds: data

start:
    mov ax, data
    mov ds, ax

    lea bx, array   ; адрес начала массива
    mov cx, 10      ; количество элементов массива
    xor ax, ax      ; обнуляем регистр суммы положительных чисел
    mov dx, ax      ; обнуляем регистр суммы отрицательных чисел

beg:
    mov ax, [bx]    ; загружаем очередное слово в регистр AX
    test ax, 8000h  ; проверяем знак числа
    jns posit       ; если число положительное, переходим на метку posit

    neg ax          ; инвертируем знак числа
    add dx, ax      ; добавляем значение к сумме отрицательных чисел
    jmp next

posit:
    add ax, positive ; добавляем значение к сумме положительных чисел

next:
    add bx, 2       ; переходим к следующему элементу массива
    loop beg        ; продолжаем цикл до тех пор, пока не обойдем все элементы

    mov positive, ax ; сохраняем сумму положительных чисел в переменную positive
    mov negative, dx ; сохраняем сумму отрицательных чисел в переменную negative

    ; здесь можно вывести результаты

quit:
    mov ax, 4c00h
    int 21h
code ends
end start