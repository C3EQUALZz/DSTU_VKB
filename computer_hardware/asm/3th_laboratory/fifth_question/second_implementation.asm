data segment
    count dw ?
    mas dw 10, 24, 76, 479, -347, 281, -24, 0, 124, 97
data ends

code segment
    assume cs: code, ds: data
    start:
        mov ax, data
        mov ds, ax ; Загрузить сегментный адрес данных
        mov si, 0 ; счетчик элемента массива
        mov cx, 10 ; счетчик повторений цикла
        beg:
            mov ax, mas [si] ; помещаем в регистр ax элемента массива
            inc si ; смещение на следующий элемент массива
            inc si
            cmp ax, 0 ; сравнение элемента с 0
            jle no ; если элемент больше нуля, то
            inc bx ; прибавляем единицу
        no: ; иначе ничего
            loop beg ; переходим на следующий круг
            mov count, bx
    quit:
        mov ax, 4C00h ; Код завершения 0
        int 21h ; Выход в DOS
    code ends
end start
