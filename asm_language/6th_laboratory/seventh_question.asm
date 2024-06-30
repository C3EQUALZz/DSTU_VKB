; Разработать подпрограмму, которая определяет, содержится ли одна
; заданная строка в другой заданной строке и, если да, то, начиная с какой
; позиции. Разработать программу, которая вводит с клавиатуры две строки
; и сообщает содержится ли одна в другой и сколько раз.

.model small
.stack 100h

.data
    input_string_msg db "Enter initial string: $"
    input_substring_msg db "Enter substring to find: $"

    string_buf db 255 dup('$')
    substring_buf db 255 dup('$')

    string_buf_s db ?
    substring_buf_s db ?

    no_substring_found db 'No occurrencies found here$'
    occurrence_count_msg db 'Occurrence count: $'
    occurrence_index_first db 'First occurrence index: $'

    newline db 10, 13, '$'

    kostil db 0

.code
    extrn putchar:near
    public main

main proc
    mov ax, @data
    mov ds, ax

    ; Выводим сообщение ввести строку
    lea dx, input_string_msg
    call p

    ; Вводим строку
    lea dx, string_buf
    call i

    ; Делаем перенос строки
    call line

    ; Выводим сообщение ввести подстроку
    lea dx, input_substring_msg
    call p

    ; Вводим подстроку
    lea dx, substring_buf
    call i

    ; Делаем перенос строки
    call line

    ; Вызываем процедуру поиска подстроки
    lea bx, string_buf + 2
    lea dx, substring_buf + 2
    call exists

    ; Если cl != 0, то нашли подстроку
    cmp cl, 0
    je not_found
    jmp found

    not_found:
        ; Выводим сообщение о том что не нашли
        lea dx, no_substring_found
        call p

        jmp quit

    found:
        ; Выводим сообщение о количестве вхождений
        lea dx, occurrence_count_msg
        call p

        ; Выводим кол-во вхождений
        mov dl, cl
        add dl, '0'
        call c

        ; Новая строка
        call line

        ; Выводим сообщение об индексе первого вхождения
        lea dx, occurrence_index_first
        call p

        ; Выводим первый индекс
        mov dl, ch
        add dl, '0'
        call c

        jmp quit



    quit:
        mov ah, 4ch
        int 21h

main endp

p proc
    mov ah, 09h
    int 21h
    ret
p endp

i proc
    mov ah, 0ah
    int 21h
    ret
i endp

c proc
    mov ah, 02h
    int 21h
    ret
c endp

line proc
    mov ah, 09h
    lea dx, newline
    int 21h
    ret
line endp

; bx - string
; dx - substring
; cl - occurrencies count
; ch - first occurrence index
; si - copy of dx for iterations
exists proc
    prep:
        mov kostil, 0 ; string index iterator
        mov cl, 0
        mov ch, 0
        mov si, dx
    iterate_string:
        mov al, [bx]
        mov ah, [si]

        cmp al, 0Dh
        je string_end

        cmp al, ah
        je chars_equal

        chars_not_equal:
            mov si, dx

        chars_equal:

        ; Тут символы равны
        cmp si, dx ; Если текущий первый символ равен первому символу подстроки
        jne ok

        cmp cl, 0
        jne ok

        mov ch, kostil

        ok:

        inc si

        mov ah, [si]

        cmp ah, 0Dh
        je found_occurrence

        jmp increment



        found_occurrence:
            add cl, 1
            mov si, dx

        increment:
            inc bx
            inc kostil
            jmp iterate_string

    string_end:
        ret
exists endp

end main