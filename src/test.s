Start:  LD V0, 0x05     ; spr_height = 5
0x0202: LD V2, 0x00     ; Y = 0 
0x0204: LD V1, 0x00     ; X = 0
0x0206: LD V3, 0xA0     ; page_length = 160
0x0208: LD V4, 0x00     ; char_count = 0
0x020A: LD V5, 0xFF     ; delay_length = 255
0x020C: LD I,0x240      ; *sprite = 240

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

Waitloop: LD V6,DT        ; delay = DT
0x0224: SE V6, 0x00     ; if delay != 0
0x0226: JP 0x0222       ;   goto Wait_Loop
0x0228: LD V2, 0x00     ; Y = 0
0x022A: CLS             ; clear()
0x022C: ADD V4, 0x20    ; char_count += 32 
0x022E: SE V4, 0x60     ; if char_count != 64
0x0230: JP 0x020E       ;   goto Draw
0x0232: JP 0x0200       ; goto Start