.model small
.data
  letter db 2, ?, dup('$')
  char1  db "20h$"
  char2  db "10h$"
  delay  db 10h

.code
  mov ax, @data
  mov ds, ax

  mov ax, 3
  int 10h


mainland:

  lea dx, char1
  mov ah, 09h
  int 21h

  call sleep

  mov ax, 3
  int 10h

  lea dx, char2
  mov ah, 09h
  int 21h

  call sleep

  mov ax, 3
  int 10h

  jmp mainland


sleep proc

  mov ah, 01h
  int 16h
  jz next

  mov ah, 00h
  int 16h

  sub al, 30
  mov byte ptr [delay], al

  next:

  xor ax, ax
  mov cl, [delay]

  shl cx, 2

  lo:
      loop lo

  ret



sleep endp


exit:
  mov ah, 4Ch
  int 21h
end

