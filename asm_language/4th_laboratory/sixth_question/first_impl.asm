                                               ;
.8086
.MODEL TINY
;
.CODE
      ORG   100h
START:
      LEA   SI, dbArr
      XOR   DL, DL      ; Counter of 1
      MOV   CX, 8       ; Byte number
BYTE_LOOP:
      PUSH  CX
      MOV   CX, 8       ; Bit number in byte
      LODSB
BIT_LOOP:
      ROR   AL, 1
      ADC   DL, 0
      LOOP  BIT_LOOP
      POP   CX
      LOOP  BYTE_LOOP
; Display Result
      MOV   AL, DL
      AAM
      MOV   CX, AX
      TEST  CH, CH
      JZ    LOW_DIGIT
      MOV   DL, CH
      CALL  DISP_DIGIT
LOW_DIGIT:
      MOV   DL, CL
DISP_DIGIT:
      ADD   DL, "0"
      MOV   AH, 2
      INT   21h
EXIT:
      RET
;
.DATA
dbArr DB    01101010b, 10011010b, 01011001b, 00111100b
      DB    01110111b, 10100101b, 11100010b, 00100110b
;
      END   START
;