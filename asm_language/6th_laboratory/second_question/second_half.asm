.model small
.data
  str1 db 80, ?, 80 dup ("$")
  msg1 db 5Bh, 0Ch, 7Ch, 0Bh, 5Dh, ' Input string: $'
  msg2 db 0Dh, 0Ah, 5Bh, 03h, 5Dh, ' Output: $'
  is_start_word db 1h

.code
  mov ax, @data
  mov ds, ax

  ; ask input (stdout)
  lea dx, msg1
  mov ah, 09h    ; view data into screan
  int 21h        ; inerapt

  ; ask stdin
  lea dx, str1
  mov ah, 0Ah
  int 21h


  xor ax, ax  ; clear

  lea di, str1 + 2 ; pointer
  xor cx, cx  ; counter

  ; load string length into CX
  mov cl, [str1 + 1] ; str + 1 -> len of str in 2 byte
  mov ch, 0

beg:
  ; if [di] == space then lo
  cmp [di], 20h
  je lo

  ; if is_start_word == 0 then lo
  cmp is_start_word, 0
  je cool_block


  cmp [di], 91
  jb cool_block

  cmp [di], 123
  jge cool_block

  cmp [di], 97
  jbe cool_block


  sub [di], 32

  jmp cool_block

cool_block:
  ; is_start_word = 0
  mov is_start_word, 0

  ; if [di + 1] != space then lo
  cmp [di + 1], 20h
  jne lo

  ; is_start_word = 1
  mov is_start_word, 1



lo:
  ; loop
  inc di
  loop beg

next:
  ; finally
  lea dx, msg2
  mov ah, 09h
  int 21h

  ; finally
  lea dx, str1 + 2
  mov ah, 09h
  int 21h



exit:
  mov ah, 4Ch
  int 21h
end
