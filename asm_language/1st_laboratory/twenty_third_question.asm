; 23. X = A / 2 - 3 * (A + B) + C * 4

data segment
    a dw 10
    b dw 20
    c dw 5
    x dw ?
data ends

code segment
    assume cs: code, ds: data

    start:
        mov ax, data
        mov ds, ax 		; load addresses

        mov bx, a       ; bx = a
        sar bx, 1       ; bx = a / 2

        mov ax, a       ; ax = a
        add ax, b       ; ax = a + b
        mov cx, 3       ; cx = 3
        mul cx          ; ax = 3 * (a + b)

        sub bx, ax      ; bx = a / 2 - 3 * (a + b)

        mov ax, c       ; ax = c
        sal ax, 2       ; ax = c * 4

        add ax, bx      ; ax = a / 2 - 3 * (a + b) + c * 4

        mov x, ax       ; record result into x
    quit:
        mov ax, 4c00h 	; end code 0
        int 21h 			; exit into dos
    end start
code ends

