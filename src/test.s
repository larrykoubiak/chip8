;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;                         TEST font display                          ;
;;                         by Larry Koubiak                           ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; V0 = spr_height
;; V1 = x
;; V2 = y
;; V3 = page_length
;; V4 = char_count
;; V5 = delay_length
;; V6 = timer_value
;; V8 = current_char
;; V9 = msg_left
;; VA = offset_ascii
;; VB = char_x
;; VC = char_y
;; VD = font_height

start:
        LD V0, 0x05             ; spr_height = 5
        LD V2, 0x00             ; Y = 0 
        LD V1, 0x00             ; X = 0
        LD V3, 0xA0             ; page_length = 160
        LD V4, 0x00             ; char_count = 0
        LD V5, 0x1F             ; delay_length = 255
        CALL draw_string        ; call draw string
        LD I,font58             ; I = font58
draw_font_page:
        DRW V1,V2,0x5           ; draw(sprite,X,Y,5)
        ADD I,V0                ; sprite += spr_height
        ADD V1, 0x08            ; X += 8
        SE V1, 0x40             ; if X!=64
        JP draw_font_page       ;   goto Draw
        LD V1, 0x00             ; X = 0
        ADD V2, 0x08            ; Y += 8
        SE V2, 0x20             ; if Y != 32
        JP draw_font_page       ;   goto Draw
        LD DT,V5                ; DT = delay_length
Wait_1: LD V6,DT                ; delay = DT
        SE V6, 0x00             ; if delay != 0
        JP Wait_1               ;   goto Wait_1
        LD V2, 0x00             ; Y = 0
        CLS                     ; clear()
        ADD V4, 0x20            ; char_count += 32 
        SE V4, 0x60             ; if char_count != 64
        JP draw_font_page       ;   goto draw_font_page
        JP start                ; goto start

font58: incbin ../fonts/5x8font.bin

msg_01: db " HELLO"
        db 0x0
msg_02: db " WORLD!"
        db 0x00
msg_03: db " CHIP-8"
        db 0x00
msg_04: db " ROCKS!"
        db 0x00

draw_string:
        LD I, 0x700             ; I = backup_reg
        LD [I], V8              ; backup_reg = [V0:V8]
        LD I, msg_01            ; I = msg_01
        LD V9,0x4               ; msg_left = 4
        LD VC,0x0               ; y = 0
draw_line:
        LD V7, [I]              ; I = str(8)
        LD VA,0x20              ; va = 0x20 (offset ascii)
        LD VB,0x00              ; x = 0
        LD V8, V0               ; V8 = reg
        CALL draw_character     ; draw_character()
        SNE V1, 0x0             ; if str[1] == 0
        JP restore_regs         ;   goto restore_regs
        LD V8, V1               ; V8 = str[1]
        CALL draw_character     ; draw_character()
        SNE V2, 0x0             ; if str[2] == 0
        JP restore_regs         ;   goto restore_regs
        LD V8, V2               ; V8 = str[2]
        CALL draw_character     ; draw_character()
        SNE V3, 0x0             ; if str[3] == 0
        JP restore_regs         ;   goto restore_regs
        LD V8, V3               ; V8 = str[3]
        CALL draw_character     ; draw_character()
        SNE V4, 0x0             ; if str[4] == 0
        JP restore_regs         ;   goto restore_regs
        LD V8, V4               ; V8 = str[4]
        CALL draw_character     ; draw_character()
        SNE V5, 0x0             ; if str[5] == 0
        JP restore_regs         ;   goto restore_regs
        LD V8, V5               ; V8 = str[5]
        CALL draw_character     ; draw_character()
        SNE V6, 0x0             ; if str[6] == 0
        JP restore_regs         ;   goto str[6]
        LD V8, V6               ; V8 = reg
        CALL draw_character     ; draw_character()
        SNE V7, 0x0             ; if str[7] == 0
        JP restore_regs         ;   goto restore_regs
        LD V8, V7               ; V8 = str[7]
        CALL draw_character     ; draw_character()
restore_regs:
        LD I, 0x700             ; I = backup_reg
        LD V8, [I]              ; [V0:V8] = backup_reg
        LD DT,V5                ; DT = delay_length
Wait_2: LD V6,DT                ; delay = DT
        SE V6, 0x00             ; if delay != 0
        JP Wait_2               ;   goto Wait_2
        ADD V9,0xFF             ; msg_left -=1
        SNE V9, 0x0             ; if msg_left == 0
        JP draw_end             ;   goto draw_end
        SNE V9, 0x1             ; if msg_left == 1
        JP draw_line_4          ; goto draw_line_4
        SNE V9, 0x2             ; if msg_left == 2
        JP draw_line_3          ; goto draw_line_3
        SNE V9, 0x3             ; if msg_left == 3
        JP draw_line_2          ; goto draw_line_2
draw_line_2:
        LD I, msg_02            ; I = msg_02
        ADD VC,0x8              ; y +=8
        JP draw_line            ; goto draw_line
draw_line_3:
        LD I, msg_03            ; I = msg_03
        ADD VC,0x8              ; y +=8
        JP draw_line            ; goto draw_line
draw_line_4:
        LD I, msg_04            ; I = msg_04
        ADD VC,0x8              ; y +=8
        JP draw_line            ; goto draw_line
draw_end:
        CLS                     ; clear()
        RET                     ; return

draw_character:
        LD I,font58             ; font_start
        LD VD,0x05              ; vd= step
        SUB V8,VA               ; v8 -= 32
Mult_5: ADD I, V8               ; i += reg
        ADD VD,0xFF             ; vd -=1
        SE VD,0x0               ; if vd != 0
        JP Mult_5               ; goto mult_5
        DRW VB,VC,0x5           ; draw char at x,y
        ADD VB,0x8              ; x+=8
        RET                     ; return