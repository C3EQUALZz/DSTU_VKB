; Часть 2. Разработать программу, которая вводит с клавиатуры строку и выводит каждое слово с новой строки.

.model small
.data
    input_str  db 80, ?, 80 dup('$')    ; тут заполняем всю строку знаком конца строки заранее
    word_str   db 80, ?, 80 dup('$')

    enter_msg  db 0dh,0ah, "Enter string:", 0dh,0ah, "$"
    output_msg db 0dh,0ah,0dh,0ah, "Words:", 0dh,0ah, "$"

    ln_msg db 0dh,0ah, "$"

    next_msg db 0dh,0ah, "----Next----", 0dh,0ah, "$"
    stop_msg db 0dh,0ah, "----Stop----", 0dh,0ah, "$"
    notw_msg db 0dh,0ah, "----not work to do----", 0dh,0ah, "$"

    space db ' '    ; знак пробела
    s_end db '$'    ; знак конца строки

.code
start:
    mov ax, @data
    mov ds, ax

main_loop:
    ; выводим сообщение для ввода строки
    mov ah, 09h
    lea dx, enter_msg
    int 21h

    ; считываем строку из консоли
    mov ah, 0Ah
    lea dx, input_str
    int 21h

    ; проверяем, не была ли введена пустая строка
    cmp byte ptr [input_str+1], 0
    je exit_program     ; если пустая - выходим

    ; проверям, есть ли в строке что-то, кроме пробелов
    call check_is_blank
    cmp ax, 0h
    jne only_blank

    ; вызываем подпрограмму логики
    call logic

next:
    ; Выводим сообщение-разделитель итераций работы прграммы
    mov ah, 09h
    lea dx, next_msg
    int 21h

    jmp main_loop   ; идём на следующий проход

only_blank:
    ; выводим сообщение о том, что в строке только пробелы
    mov ah, 09h
    lea dx, notw_msg
    int 21h

    jmp next ; идём на след проход main_loop

; подпрограмма проверки на то, есть ли в строке что-то кроме пробелов
; ставит в регистр ax 1-только пробелы, 0-есть и другие символы
check_is_blank proc

    ; подготавливаем регистр для индексации исходной строки
    xor di, di
    mov di, 2h

    ; ax будем использовать как промежуточный буфер
    xor ax, ax

    ; устанавливаем кол-во итераций цикла
    xor cx, cx
    mov cl, [input_str+1]

    check_lbody:
        ; проверяем пробел ли это
        mov al, [input_str+di]
        cmp al, space
        jne it_not_space    ; если не пробел

    check_loop:
        ; инкреминтируем для след итерации
        inc di
        loop check_lbody

        ; если мы тут, то по всей строке уже прошлись, а встретились лишь пробелы
        xor ax, ax
        mov ax, 1h
        ret

    it_not_space:
        ; если не пробел - ставим ax в 0 и выходим
        xor ax, ax
        mov ax, 0h
        ret

check_is_blank endp

logic proc
    ; регистром di будем индексировать input_str
    xor di, di
    mov di, 2h

    ; ax в качестве промежуточного буфера
    xor ax, ax

    ; 0. Выводим сообщение о том, что дальше идёт результат
    mov ah, 09h
    lea dx, output_msg
    int 21h

    ; 1. Отсеиваем первые пробелы
    lo_body:
        mov al, [input_str+di]
        cmp al, space
        jne calc ; если символ не пробел

        ; на след итерацию если символ оказался пробелом
        inc di
        jmp lo_body

    ; 2. Обработка слов
    calc:
        call word_copy

        ; выводим знак переноса строки
        mov ah, 09h
        lea dx, ln_msg
        int 21h

        ; выводим слово
        mov ah, 09h
        lea dx, word_str
        int 21h

        ; будем использовать регистр bx для уточнения, закончили ли мы проходиться по всей строке
        xor bx, bx
        mov bx, di

        sub bx, 2

        cmp [input_str+1], bl
        ja lo_body       ; если нет -> идём на след итерацию

    ret ; завершение подпрограммы. возврат в вызывающую программу (main_loop)

logic endp

word_copy proc

    ; регистром si будем индексировать word_str
    xor si, si

    ; ax в качестве промежуточного буфера
    xor ax, ax

    ; копирование слова
    copy_loop:
        ; если символ пробел - копирование слова завершено
        mov al, [input_str+di]
        cmp al, space
        je end_copy

        ; проверка на то, дошли ли мы до конца исходной строки
        xor bx, bx
        mov bx, di
        sub bx, 2
        cmp [input_str+1], bl
        jbe end_copy

        ; иначе - это всё ещё слово, копируем его
        mov al, [input_str+di]
        mov byte ptr [word_str+si], al

        ; след итерация копирования
        inc di
        inc si
        jmp copy_loop

    ; когда завершили копирование слова
    end_copy:
        mov al, s_end
        mov byte ptr [word_str+si], al
        ret  ; завершение подпрограммы. возврат в вызывающую программу (logic)

word_copy endp


exit_program:
    ; выводим сообщение о том, что программа завершается
    mov ah, 09h
    lea dx, stop_msg
    int 21h

    mov ah, 4Ch     ; выходим из программы
    int 21h         ; и передаём управление потоком обратно MS DOS

end start