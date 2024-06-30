; Часть 1. Разработать две подпрограммы, одна из которых преобразует любую заданную букву в заглавную
; (в том числе для русских букв), а другая преобразует букву в строчную.

.model small
.data
  letter db 2, ?, dup('$')
  option db 2, ?, dup('$')
  buffer db 80, ?, dup('$')

  menu_top db 0B0h, 0B0h, 0B1h, 0B1h, 0B1h, 0B2h, 0B2h, 0B2h, " Supa Menu ", 0B2h, 0B2h, 0B2h, 0B1h, 0B1h, 0B1h, 0B0h, 0B0h, "$"
  menu_option_hint db 0Ah, 0Ah, 0Dh, " Type 1 or 2 for select: $",
  menu_option_one db 0Ah, 0Dh, "   [1] - for make low case letter $",
  menu_option_two db 0Ah, 0Dh, "   [2] - for make HIGH case letter $",
  menu_select_option db 0Ah, 0Ah, 0Dh, 5Bh, 0Ch, 7Ch, 0Bh, 5Dh, ' Select: $'
  menu_input_letter db 0Ah, 0Dh, 5Bh, 0Ch, 7Ch, 0Bh, 5Dh, ' Input letter: $'
  menu_output db 0Ah, 0Dh, 5Bh, 03h, 5Dh, ' Output: $'
  menu_interept db 0Ah, 0Dh, ' Please press any key to continue: $'


.code
  mov ax, @data
  mov ds, ax

  jmp menu



menu:

  xor ax, ax  ; clear

  MOV AH, 0
  MOV AL, 3
  INT 10H


  xor ax, ax  ; clear

  ; output
  lea dx, menu_top
  mov ah, 09h    ; view data into screan
  int 21h        ; inerapt

  lea dx, menu_option_hint
  mov ah, 09h
  int 21h

  lea dx, menu_option_one
  mov ah, 09h
  int 21h

  lea dx, menu_option_two
  mov ah, 09h
  int 21h

  lea dx, menu_select_option
  mov ah, 09h
  int 21h

  ; ask stdin
  lea dx, option
  mov ah, 0Ah
  int 21h
  mov [option + 3], 24h

  lea dx, menu_input_letter
  mov ah, 09h
  int 21h

  ; ask stdin
  lea dx, letter
  mov ah, 0Ah
  int 21h
  mov [letter + 3], 24h

  cmp [option + 2], 31h
  je sub1

  cmp [option + 2], 32h
  je sub2

  cmp [option + 2], 24h
  je jmp exit

  cont:
      lea dx, menu_interept
      mov ah, 09h
      int 21h

      ; ask stdin

      lea dx, buffer
      mov ah, 0Ah
      int 21h

      jmp menu

sub2:

  sub [letter + 2], 32


  ; finally
  lea dx, menu_output
  mov ah, 09h
  int 21h

  lea dx, letter + 2
  mov ah, 09h
  int 21h

  jmp cont


sub1:
  add [letter + 2], 32


  ; finally
  lea dx, menu_output
  mov ah, 09h
  int 21h

  lea dx, letter + 2
  mov ah, 09h
  int 21h

  jmp cont


exit:
  mov ah, 4Ch
  int 21h
end

