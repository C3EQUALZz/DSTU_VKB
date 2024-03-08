data segment

    max dw ?
    mass dw 10,24,76,79,47,81,67,70,124,97

data ends

code segment
    assume cs: code, ds: data

    start:
        mov ax, data
        mov ds, ax

  		lea bx, mass

 		mov cx, 5

  	beg:
  	    mov ax, [bx] ; tmp1 = bx[1]
  	    inc bx
  	    inc bx       ; make bx[2]
  	    mov dx, [bx] ; tmp2 = bx[2]

  	    mov [bx], ax ; bx[2] = tmp1
  	    dec bx
  	    dec bx       ; make bx[1]
  	    mov [bx], dx ; bx[1] = tmp2


  	    ;;; for debug.

  	    mov ax, [bx]
  	    inc bx
  	    inc bx

  	    mov dx, [bx]
  	    dec bx
  	    dec bx

  	    ;;;


  	    inc bx
  	    inc bx
  	    inc bx
  	    inc bx       ; next -> bx[3]


 	no:
		loop beg


 	quit:
 	    mov ax,4C00h
        int 21h

code ends

end start