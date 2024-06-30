; Часть 1. Разработать подпрограмму, которая разбивает заданную строку на две части: первое слов (до первого пробела)
; и остальная часть строки (пробелы в начале строки убираются)

.model small
.data
    input_str  db 80, ?, 80 dup('$')    ; тут заполняем всю строку знаком конца строки заранее
    first_word db 80, ?, 80 dup('$')
    other_str  db 80, ?, 80 dup('$')

    enter_msg db 0dh,0ah, "Enter string:", 0dh,0ah, "$"
    output_msg db 0dh,0ah, "Output string:", 0dh,0ah, "$"

    fword_msg db 0dh,0ah, "First word:", 0dh,0ah, "$"
    other_msg db 0dh,0ah, "Other string:", 0dh,0ah, "$"

    next_msg db 0dh,0ah, "----Next----", 0dh,0ah, "$"
    stop_msg db 0dh,0ah, "----Stop----", 0dh,0ah, "$"
    blnk_msg db 0dh,0ah, "----Only spaces.not work to do----", 0dh,0ah, "$"

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
    lea dx, blnk_msg
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

    ; регистром si будем индексировать first_word
    xor si, si

    ; ax в качестве промежуточного буфера
    xor ax, ax

    ; 1. Отсеиваем первые пробелы
    lo_body:
        mov al, [input_str+di]
        cmp al, space
        jne start_calc_fword ; если символ не пробел

        ; на след итерацию если символ оказался пробелом
        inc di
        jmp lo_body

    ; 2. Обработка первого слова
    start_calc_fword:
        call fword_copy

        ; выводим сообщение о том, что это первое слово
        mov ah, 09h
        lea dx, fword_msg
        int 21h

        ; выводим первое слово
        mov ah, 09h
        lea dx, first_word
        int 21h

    ; 3. Обработка остальной части строки
    start_calc_other:
        ; +1, так как в input_str+di сейчас пробел
        inc di
        call other_copy

        ; выводим сообщение о том, что это other_str
        mov ah, 09h
        lea dx, other_msg
        int 21h

        ; выводим other_str
        mov ah, 09h
        lea dx, other_str
        int 21h

    ret ; завершение подпрограммы. возврат в вызывающую программу (main_loop)

logic endp

fword_copy proc

    ; регистром si будем индексировать first_word
    xor si, si

    ; ax в качестве промежуточного буфера
    xor ax, ax

    ; копирование первого слова
    f_copy_loop:
        ; если символ пробел - копирование первого слова завершено
        mov al, [input_str+di]
        cmp al, space
        je f_end_copy

        ; иначе - это всё ещё первое слово, копируем его
        mov al, [input_str+di]
        mov byte ptr [first_word+si], al

        ; след итерация копирования
        inc di
        inc si
        jmp f_copy_loop

    ; когда завершили копирование первого слова
    f_end_copy:
        ret  ; завершение подпрограммы. возврат в вызывающую программу (logic)

fword_copy endp



other_copy proc
    ; регистром si будем индексировать other_str
    xor si, si

    ; ax в качестве промежуточного буфера
    xor ax, ax

    ; утсанавливаем кол-во итераций цикла, чтобы программа не ушла дальше конца строки
    xor cx, cx
    mov cl, [input_str+1]
    sub cx, di
    add cx, 2h

    ; копирование
    o_copy_loop:
        ; копируем
        mov al, [input_str+di]
        mov byte ptr [other_str+si], al

    lo_beg:
        ; след итерация копирования
        inc di
        inc si

        loop o_copy_loop

    ; когда завершили копирование
    o_end_copy:
        ; добавляем в конец знак конца строки, так как в исходной его может и не быть
        mov al, s_end
        mov byte ptr [other_str+si], al
        ret  ; завершение подпрограммы. возврат в вызывающую программу (logic)

other_copy endp

exit_program:
    ; выводим сообщение о том, что программа завершается
    mov ah, 09h
    lea dx, stop_msg
    int 21h

    mov ah, 4Ch     ; выходим из программы
    int 21h         ; и передаём управление потоком обратно MS DOS

end start

