; 7: Ввести с клавиатуры строку, состоящую из нескольких слов. Вывести каждое слово на экран в отдельной строке, т.е. выдать слова с столбик.

DATA_S segment
    buffer db 255 dup('$')
    new db 10, 13, '$'
DATA_S ends

CODE_S segment
    assume cs:CODE_S, ds:DATA_S

    start:
        mov ax, DATA_S
        mov ds, ax

        mov ah, 0ah
        lea dx, buffer
        int 21h

        lea si, buffer + 2

    print_new_line:
        mov ah, 09h
        lea dx, new
        int 21h

    iterate_buffer:
        mov al, [si]

        cmp al, '$'
        je quit

        inc si

        cmp al, ' '
        je print_new_line

        mov ah, 02h
        mov dl, al
        int 21h

        jmp iterate_buffer

    quit:
        mov ax, 4c00h
        int 21h

CODE_S ends
end start
