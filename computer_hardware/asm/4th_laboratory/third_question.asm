data segment
    NB db 0h, 0h, 0h, 1h, 0h, 1h,  1h, 1h
    ;     x0, x1, x2 ,x3, x4  x5,  x6  x7
data ends

code segment

    assume cs: code. ds:data

    START:
        mov ax, data
        mov ds, ax
        lea bx, NB

        mov cx, 1 ; store result inside ()
        mov dx, 0 ; store f result

    CON:
        ; f=(x7 & x6 & x1 ) V
        ; (x6 & x4 & x2 & x1 & x0) V
        ; (x7 & x6 & x3 & x1)


        ; (x7 & x6 & x1 )
        add bx, 7
        mov ax, [bx]
        sub bx, 7

        and cx, ax

        add bx, 6
        mov ax, [bx]
        sub bx, 6

        and cx, ax

        add bx, 1
        mov ax, [bx]
        sub bx, 1

        and cx, ax


        or dx, cx

        ; (x6 & x4 & x2 & x1 & x0)

        add bx, 6
        mov ax, [bx]
        sub bx, 6

        and cx, ax

        add bx, 4
        mov ax, [bx]
        sub bx, 4

        and cx, ax

        add bx, 2
        mov ax, [bx]
        sub bx, 2

        and cx, ax

        add bx, 1
        mov ax, [bx]
        sub bx, 1

        and cx, ax

        add bx, 0
        mov ax, [bx]
        sub bx, 0

        and cx, ax


        or dx, cx


        ; (x7 & x6 & x3 & x1)
        add bx, 7
        mov ax, [bx]
        sub bx, 7

        and cx, ax

        add bx, 6
        mov ax, [bx]
        sub bx, 6

        and cx, ax

        add bx, 3
        mov ax, [bx]
        sub bx, 3

        and cx, ax

        add bx, 1
        mov ax, [bx]
        sub bx, 1

        and cx, ax


        or dx, cx
        ; RESULT IN dx

    QUIT:
        mov ax, 4c00h ; exit code
 		Int 21h

code ends
end START