; 17. X = (3*A + 2*B) - C / 4 + 217

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

        mov ax, a       ; ax = a
        mov bx, 3       ; bx = 3
        mul bx          ; ax *= bx <=> ax = 3 * a

        mov bx, b       ; bx = b
        sal bx, 1       ; bx = 2 * b

        add ax, bx      ; ax = (3 * a + 2 * b)

        mov bx, c       ; bx = c
        neg bx          ; bx = -c
        sar bx, 2       ; bx = -c / 4

        add ax, bx      ; ax = (3 * a + 2*b) - c / 4

        add ax, 217     ; ax += 217

        mov x, ax       ; record result into x
    quit:
        mov ax, 4c00h 	; end code 0
        int 21h 			; exit into dos
    end start
code ends

