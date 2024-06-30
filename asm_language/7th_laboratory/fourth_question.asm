; Тут работа с часами

data segment
    attribute db 11111000b ; white bg, black text
    right_pos dw 1000
    left_pos dw 0
    timer db "00:00:00$"
    timer_len db 8
    digit db ?
    digit_l db ?
    digit_r db ?
data ends
code segment
    print_time proc
        pusha
        mov cx, 0
        xor ax, ax
        mov si, left_pos
        mov ah, attribute
        lea bx, timer
        print_loop:
            mov al, [bx]
            inc bx
            mov es:[si], ax
            inc si
            inc si
            inc cx
            cmp cl, timer_len
            jne print_loop
        popa
        ret
    print_time endp
    ; 0-99 byte to ascii converter
    itoa proc
        mov al, digit
        mov ah, 0
        pusha
        mov bx, 10
        div bl
        add al, '0'
        add ah, '0'
        mov digit_l, al
        mov digit_r, ah
        popa
        ret
    itoa endp
    get_time proc
        pusha
        mov ah, 2ch
        int 21h
        ; hours
        mov digit, ch
        call itoa
        mov bh, digit_l
        mov bl, digit_r
        mov [timer], bh
        mov [timer+1], bl
        ; minutes
        mov digit, cl
        call itoa
        mov bh, digit_l
        mov bl, digit_r
        mov [timer+3], bh
        mov [timer+4], bl
        ; seconds
        mov digit, dh
        call itoa
        mov bh, digit_l
        mov bl, digit_r
        mov [timer+6], bh
        mov [timer+7], bl
        popa
        ret
    get_time endp
    delay1s proc
        pusha
        mov cx, 7h
        mov dx, 0a120h
        mov ah, 86h
        int 15h
        popa
        ret
    delay1s endp
    main:
        mov ax, data
        mov ds, ax
        mov ax, 0b800h
        mov es, ax
        infinite_loop:
            call get_time
            call print_time
            call delay1s
            jmp infinite_loop
    quit:
        mov ax, 4c00h
        int 21h
code ends
end main