.MODEL SMALL
.STACK 100h

.DATA
  current_row db 10
  current_col db 10
  char_input db ' '
  output_char db ' '

  stop_msg db 0dh,0ah, "----Stop----", 0dh,0ah, "$"

.CODE
start:
  mov ax, @data
  mov ds, ax

  ; начальные модификации позиции курсора
  mov current_col, 1
  mov current_row, 1

  ; установка обработчика прерывания клавиатуры (не раб)
  ;mov ah, 25h
  ;mov al, 1Ch
  ;lea dx, keyboard_handler
  ;int 21h

  loop:
      ; ставим курсор на правильное место
      mov ah, 2
      mov dl, current_col
      mov dh, current_row
      int 10h

      ; ввод символа
      mov ah, 00h
      int 16h
      mov char_input, al

      call keyboard_handler

      jmp loop


keyboard_handler proc

  ; обработчик прерывания клавиатуры
  cmp char_input, 38h ; клавиша "8"
  je up
  cmp char_input, 32h ; клавиша "2"
  je down
  cmp char_input, 34h ; клавиша "4"
  je left
  cmp char_input, 36h ; клавиша "6"
  je right
  cmp char_input, 30h ; клавиша "0"
  je exit_program

  mov al, char_input  ; если это символ
  mov output_char, al

  return:
      ; вывод символа в нужную позицию
      mov ah, 02h
      mov dl, output_char
      int 21h
  ret ; для 1Ch тут нужно писать iret


up:
  ; установка новой позиции вывода символа
  mov ah, 2
  sub current_row, 1
  mov dl, current_col
  mov dh, current_row
  int 10h

  ; цикл задержки
  xor cx, cx
  mov cl, 8h
  shl cx, 2 ; умножаю на 2 в 9 степени (сдвиг влево на 9)
  up_delay_loop:
      nop
      loop up_delay_loop

  jmp return

down:
  ; установка новой позиции вывода символа
  mov ah, 2
  add current_row, 1
  mov dl, current_col
  mov dh, current_row
  int 10h

  ; цикл задержки
  xor cx, cx
  mov cl, 2h
  shl cx, 2 ; умножаю на 2 в 9 степени (сдвиг влево на 9)
  down_delay_loop:
      nop
      loop down_delay_loop

  jmp return

left:
  ; установка новой позиции вывода символа
  mov ah, 2
  sub current_col, 1
  mov dl, current_col
  mov dh, current_row
  int 10h

  ; цикл задержки
  xor cx, cx
  mov cl, 4h
  shl cx, 2 ; умножаю на 2 в 9 степени (сдвиг влево на 9)
  left_delay_loop:
      nop
      loop left_delay_loop

  jmp return

right:
  ; установка новой позиции вывода символа
  mov ah, 2
  add current_col, 1
  mov dl, current_col
  mov dh, current_row
  int 10h

  ; цикл задержки
  xor cx, cx
  mov cl, 6h
  shl cx, 2 ; умножаю на 2 в 9 степени (сдвиг влево на 9)
  right_delay_loop:
      nop
      loop right_delay_loop

  jmp return

keyboard_handler endp


exit_program:
  ; выводим сообщение о том, что программа завершается
  mov ah, 09h
  lea dx, stop_msg
  int 21h

  mov ah, 4Ch     ; выходим из программы
  int 21h         ; и передаём управление потоком обратно MS DOS

end start
