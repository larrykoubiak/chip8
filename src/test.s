Start:  LD V0, 0x05     ; spr_height = 5
0x0202: LD V2, 0x00     ; Y = 0 
0x0204: LD V1, 0x00     ; X = 0
0x0206: LD V3, 0xA0     ; page_length = 160
0x0208: LD V4, 0x00     ; char_count = 0
0x020A: LD V5, 0x1F     ; delay_length = 255
0x020C: LD I,0x23E      ; *sprite = 240

Draw: DRW V1,V2,0x5     ; draw(sprite,X,Y,5)
0x0210: ADD I,V0        ; sprite += spr_height
0x0212: ADD V1, 0x08    ; X += 8
0x0214: SE V1, 0x40     ; if X!=64
0x0216: JP 0x020E       ;   goto Draw
0x0218: LD V1, 0x00     ; X = 0
0x021A: ADD V2, 0x08    ; Y += 8
0x021C: SE V2, 0x20     ; if Y != 32
0x021E: JP 0x020E       ;   goto Draw
0x0220: LD DT,V5        ; DT = delay_length

Wait_1: LD V6,DT        ; delay = DT
0x0224: SE V6, 0x00     ; if delay != 0
0x0226: JP 0x0222       ;   goto Wait_1
0x0228: LD V2, 0x00     ; Y = 0
0x022A: CLS             ; clear()
0x022C: ADD V4, 0x20    ; char_count += 32 
0x022E: SE V4, 0x60     ; if char_count != 64
0x0230: JP 0x020E       ;   goto Draw
0x0232: LD VC, 0x00     ; y param
0x0234: CALL 0x042C     ; call draw string
0x0236: JP 0x0200       ; goto Start
0x0238: dw 0x0000
0x023A: dw 0x0000
0x023C: dw 0x0000

0x023E: inc ../fonts/5x8font.bin

0x041E: db "Hello!!!"
0x0426: db 0x0
0x0427: db "Bye!"
0x042B: db 0x00

0x042C: LD I, 0x700     ; I = backup_reg
0x042E: LD [I], V8      ; backup_reg = [V0:V8]
0x0430: LD I, 0x041E    ; I = str1
drawst: LD V7, [I]      ; I = str(8)
0x0434: LD VA,0x20      ; va = 0x20 (offset ascii)
0x0436: LD VB,0x00      ; x = 0
0x0438: LD V8, V0       ; V8 = reg
0x043A: CALL 0x0484     ; get font char
0x043C: SNE V1, 0x0     ; if str1_len = 1
0x043E: JP 0x0474       ;   return
0x0440: LD V8, V1       ; V8 = reg
0x0442: CALL 0x0484     ; get font char
0x0444: SNE V2, 0x0     ; if str1_len = 1
0x0446: JP 0x0474       ;   return
0x0448: LD V8, V2       ; V8 = reg
0x044A: CALL 0x0484     ; get font char
0x044C: SNE V3, 0x0     ; if str1_len = 1
0x044E: JP 0x0474       ;   return
0x0450: LD V8, V3       ; V8 = reg
0x0452: CALL 0x0484     ; get font char
0x0454: SNE V4, 0x0     ; if str1_len = 1
0x0456: JP 0x0474       ;   return
0x0458: LD V8, V4       ; V8 = reg
0x045A: CALL 0x0484     ; get font char
0x045C: SNE V5, 0x0     ; if str1_len = 1
0x045E: JP 0x0474       ;   return
0x0460: LD V8, V5       ; V8 = reg
0x0462: CALL 0x0484     ; get font char
0x0464: SNE V6, 0x0     ; if str1_len = 1
0x0466: JP 0x0474       ;   return
0x0468: LD V8, V6       ; V8 = reg
0x046A: CALL 0x0484     ; get font char
0x046C: SNE V7, 0x0     ; if str1_len = 1
0x046E: JP 0x0474       ;   return
0x0470: LD V8, V7       ; V8 = reg
0x0472: CALL 0x0484     ; get font char
0x0474: LD I, 0x700     ; I = backup_reg
0x0476: LD V8, [I]      ; [V0:V8] = backup_reg
0x0478: LD DT,V5        ; DT = delay_length
Wait_2: LD V6,DT        ; delay = DT
0x047C: SE V6, 0x00     ; if delay != 0
0x047E: JP 0x047A       ;   goto Wait_2
0x0480: CLS             ; clear
0x0482: RET             ; return

drawch: LD I,0x23E      ; font_start
0x0486: LD VD,0x05      ; vd= step
0x0488: SUB V8,VA       ; v8 -= 32
Mult_5: ADD I, V8       ; i += reg
0x048C: ADD VD,0xFF     ; vd -=1
0x048E: SE VD,0x0       ; if vd != 0
0x0490: JP 0x048A       ; goto mult_5
0x0492: DRW VB,VC,0x5   ; draw char at x,y
0x0494: ADD VB,0x8      ; x+=8
0x0496: RET             ; return