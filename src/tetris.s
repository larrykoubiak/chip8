;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;                               TETRIS                               ;
;;                         by unknown author                          ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; V0 = X-coord
; V1 = Y-coord
; V2 = key_down
; V3 = tetromino_dir (N,W,S,E)
; V4 = tetromino_offset (T,L,J,2,S,O,I)
; V5 = timer_value
; V6 = tmp
; V7 = key_left
; V8 = key_right
; V9 = key_rotate
; VA = score
; VB = pixel_count
; VC = top_y
; VD = temp_x
; VE = temp_y

; 0x0700[3] = backup_reg
; 0x0804[3] = score_BCD

start:
        LD I,pixel              ; I = single_pixel
        CALL reset_x_score      ; reset_x_score()
        CALL setup_variables    ; setup_variables()

draw_top_line:
        ADD V0,0x01             ; x += 1
        DRW V0,V1,1             ; draw(x,y,1)
        SE V0,0x25              ; if x!= 37
        JP draw_top_line        ; goto draw_top_line

draw_lr_border:
        ADD V1,0xFF             ; y -= 1
        DRW V0,V1,1             ; draw(x,y,1)
        LD V0,0x1A              ; x = 26
        DRW V0,V1,1             ; draw(x,y,1)
        LD V0,0x25              ; x = 37
        SE V1,0x00              ; if y != 0
        JP draw_lr_border       ; goto draw_lr_border

get_new_tetromino:
        RND V4,0x70             ; tetromino_offset = rnd & 0x70
        SNE V4,0x70             ; if tetromino_offset = 0x70
        JP get_new_tetromino    ;   goto get_new_tetromino
        RND V3,0x03             ; tetromino_dir = rnd & 0x03
        LD V0,0x1E              ; x = 30
        LD V1,0x03              ; y = 3
        CALL get_tetromino_tile ; get_tetromino_tile()

draw_tetromino:
        LD DT,V5                ; delay = 16 (1 second)
        DRW V0,V1,4             ; draw (x,y,4)
        SE VF,0x01              ; if !collision
        JP process_input        ; goto process_input
        DRW V0,V1,4             ; else draw(x,y,4) (erase)
        ADD V1,0xFF             ; y -= 1
        DRW V0,V1,4             ; draw (x,y,4)
        CALL scan_playfield     ; scan_playfield()
        JP get_new_tetromino    ; goto get_new_tetromino

process_input:
        SKNP V7                 ; if key_left_pressed
        CALL move_left          ;   goto move_left
        SKNP V8                 ; if key_right_pressed
        CALL move_right         ;   goto move_right
        SKNP V9                 ; if key_rotate_pressed
        CALL rotate             ;   goto rotate
        SKP V2                  ; if !key_down_pressed
        JP draw_erase           ;   goto draw_erase
        LD V6,0x00              ; tmp = 0
        LD DT,V6                ; DT = tmp

draw_erase:
        LD V6,DT                ; tmp = DT
        SE V6,0x00              ; if tmp != 0
        JP process_input        ;   goto process_input
        DRW V0,V1,4             ; draw(x,y,4) (erase)
        ADD V1,0x01             ; y += 1
        JP draw_tetromino       ; goto draw_tetromino

get_tetromino_tile:
        LD I,tetrominoes        ; I = tetromino_tiles
        ADD I,V4                ; I += tetromino_offset
        LD V6,0x00              ; tmp = 0
        SNE V3,0x01             ; if tetromino_dir = 1
        LD V6,0x04              ; tmp = 4
        SNE V3,0x02             ; elif tetromino_dir = 2
        LD V6,0x08              ; tmp = 8
        SNE V3,0x03             ; elif tetromino_dir = 3
        LD V6,0x0C              ; tmp = 12
        ADD I,V6                ; I += tmp
        RET                     ; return

move_left:
        DRW V0,V1,4             ; draw (x,y,4) (erase)
        ADD V0,0xFF             ; x -= 1
        CALL draw_and_wait      ; draw_and_wait()
        SE VF,0x01              ; if !collision
        RET                     ;   return
        DRW V0,V1,4             ; else draw (x,y,4) (erase)
        ADD V0,0x01             ;   x += 1
        CALL draw_and_wait      ;   draw_and_wait()
        RET                     ;   return

move_right:
        DRW V0,V1,4             ; draw (x,y,4) (erase)
        ADD V0,0x01             ; x += 1
        CALL draw_and_wait      ; draw_and_wait()
        SE VF,0x01              ; if !collision
        RET                     ;   return
        DRW V0,V1,4             ; else draw(x,y,4) (erase)
        ADD V0,0xFF             ;   x -= 1
        CALL draw_and_wait      ;   draw_and_wait()
        RET                     ;   return

rotate:
        DRW V0,V1,4             ; draw(x,y,4) (erase)
        ADD V3,0x01             ; tetromino_dir += 1
        SNE V3,0x04             ; if tetromino_dir == 4
        LD V3,0x00              ;   tetromino_dir = 0
        CALL get_tetromino_tile ; get_tetromino_tile()
        CALL draw_and_wait      ; draw_and_wait()
        SE VF,0x01              ; if !collision
        RET                     ;   return
        DRW V0,V1,4             ; draw(x,y,4) (erase)
        ADD V3,0xFF             ; tetromino_dir -= 1
        SNE V3,0xFF             ; if tetromino_dir = -1
        LD V3,0x03              ;   tetromino_dir = 3
        CALL get_tetromino_tile ; get_tetromino_tile()
        CALL draw_and_wait      ; draw_and_wait()
        RET                     ; return

pixel:  dw 0x8000

setup_variables:
        LD V7,0x05              ; key_down = 5
        LD V8,0x06              ; key_right = 6
        LD V9,0x04              ; key_left = 4
        LD V1,0x1F              ; y = 31
        LD V5,0x10              ; timer = 16
        LD V2,0x07              ; key_drop = 7
        RET                     ; return

tetrominoes: incbin tetrominoes.bin

draw_and_wait:
        DRW V0,V1,4             ; draw x,y,4
        LD V6,0x35              ; tmp = 35
loop_start:
        ADD V6,0xFF             ; tmp -= 1
        SE V6,0x00              ; if tmp !=0
        JP loop_start           ;   goto loop_start
        RET                     ; else return

scan_playfield:
        LD I,pixel              ; I = single_pixel
        LD VC,V1                ; top_y = y
        SE VC,0x1E              ; if top_y != 30
        ADD VC,0x01             ; top_y += 1
        SE VC,0x1E              ; if top_y != 30
        ADD VC,0x01             ; top_y +=1
        SE VC,0x1E              ; if top_y != 30
        ADD VC,0x01             ; top_y += 1
scan_full_line:
        CALL scan_line          ; scan_line()
        SNE VB,0x0A             ; if pixel_count == 12
        CALL clean_line         ;   clean_line()
        SNE V1,VC               ; if y == top_y
        RET                     ;   return
        ADD V1,0x01             ; y += 1
        JP scan_full_line       ; goto scan_full_line

scan_line:
        LD V0,0x1B              ; x = 27
        LD VB,0x00              ; pixel_count = 0
scan_pixel:
        DRW V0,V1,1             ; draw(x,y,1)
        SE VF,0x00              ; if !collision
        ADD VB,0x01             ;   pixel_count += 1
        DRW V0,V1,1             ; draw(x,y,1)
        ADD V0,0x01             ; x += 1
        SE V0,0x25              ; if x != 37
        JP scan_pixel           ;   goto scan_pixel 
        RET                     ; else return

clean_line:
        LD V0,0x1B              ; x = 27
erase_pixel:
        DRW V0,V1,1             ; draw(x,y,1) (erase pixel)
        ADD V0,0x01             ; x += 1
        SE V0,0x25              ; if x != 37
        JP erase_pixel          ;   goto erase_pixel
        LD VE,V1                ; cur_y = y
        LD VD,VE                ; prev_y = cur_y
        ADD VE,0xFF             ; cur_y -= 1
init_scan:
        LD V0,0x1B              ; x = 27
        LD VB,0x00              ; pixel_count = 0
test_pixel:
        DRW V0,VE,1             ; draw(x,cur_y,1) (draw pixel)
        SE VF,0x00              ; if !collision
        JP no_pixel             ;   goto no_pixel
        DRW V0,VE,1             ; else draw(x,cur_y,1) (erase pixel)
        JP next_pixel           ;   goto next_pixel
no_pixel:
        DRW V0,VD,1             ; draw(x,prev_y,1)
        ADD VB,0x01             ; pixel_count +=1
next_pixel:
        ADD V0,0x01             ; x += 1
        SE V0,0x25              ; if x !=37
        JP test_pixel           ;   goto test_pixel
        SNE VB,0x00             ; if pixel_count = 0
        JP erase_score          ;   goto erase_score
        ADD VD,0xFF             ; prev_y -=1
        ADD VE,0xFF             ; cur_y -=1
        SE VD,0x01              ; if prevy = 1
        JP init_scan            ;   goto init_scan
erase_score:
        CALL draw_score         ; draw_score()
        SE VF,0x01              ; if !collision
        CALL draw_score         ; draw_score()
        ADD VA,0x01             ; score += 1
update_score:
        CALL draw_score         ; draw_score()
        LD V0,VA                ; temp_score = score
        LD VD,0x07              ; mask = 7
        AND V0,VD               ; temp_score &= mask
        SNE V0,0x04             ; if temp_score = 4
        ADD V5,0xFE             ; delay -= 2
        SNE V5,0x02             ; if delay = 2
        LD V5,0x04              ; delay = 4
        RET                     ; return

draw_score:
        LD I,0x700              ; I = backup_reg
        LD [I],V2               ; backup_reg = [V0:V2]
        LD I,0x804              ; I = BCD_score
        LD B,VA                 ; BCD_score = bcd(score)
        LD V2,[I]               ; [V0:V2] = BCD_score
        LD F,V0                 ; I = char(BCD_score[0])
        LD VD,0x32              ; temp_x = 50
        LD VE,0x00              ; temp_y = 0
        DRW VD,VE,5             ; draw(temp_x,temp_y,5)
        ADD VD,0x05             ; x_score += 5
        LD F,V1                 ; I = char(BCD_score[1])
        DRW VD,VE,5             ; draw(temp_x,temp_y,5)
        ADD VD,0x05             ; temp_x += 5
        LD F,V2                 ; I = char(BCD_score[2])
        DRW VD,VE,5             ; draw(temp_x,temp_y,5)
        LD I,0x700              ; I = backup_reg
        LD V2,[I]               ; [V0:V2] = backup_reg
        LD I,pixel              ; I = single_pixel
        RET                     ; return

reset_x_score:
        LD VA,0x00              ; score = 0
        LD V0,0x19              ; x = 25
        RET                     ; return

        db 0x37                 ; ??
        db 0x23                 ; ??