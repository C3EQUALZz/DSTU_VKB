; 5. X = 5*(A - B) - 2*C + 5

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
        sub ax, b       ; ax -= b

        mov bx, 5       ; bx = 5
        mul bx          ; ax *= bx

        mov bx, c       ; bx = c
        sal bx, 1       ; bx *= 2
        neg bx          ; bx *= -1

        add ax, bx      ; ax += bx

        add ax, 5       ; ax += 5


        mov x, ax       ; record result into x

    quit:
        mov ax, 4c00h 	; end code 0
        int 21h 			; exit into dos
    end start
code ends

