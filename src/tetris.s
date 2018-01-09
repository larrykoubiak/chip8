;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;                               TETRIS                               ;
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
; VC = 
; VD = temp_x
; VE = temp_y

; 0x0700[3] = backup_reg
; 0x0804[3] = score_BCD

; 0x02B4 = single_pixel
; 0x02C4[0x70] = tetrominoes tiles

0x0200: LD I,0x2B4      ; I = single_pixel
0x0202: CALL 0x03E6     ; reset_x_score()
0x0204: CALL 0x02B6     ; setup_variables()

draw_top_line:
0x0206: ADD V0,0x01     ; x += 1
0x0208: DRW V0,V1,1     ; draw(x,y,1)
0x020A: SE V0,0x25      ; if x!= 37
0x020C: JP 0x0206       ; goto start1

draw_left_right_border:
0x020E: ADD V1,0xFF     ; y -= 1
0x0210: DRW V0,V1,1     ; draw(x,y,1)
0x0212: LD V0,0x1A      ; x = 26
0x0214: DRW V0,V1,1     ; draw(x,y,1)
0x0216: LD V0,0x25      ; x = 37
0x0218: SE V1,0x00      ; if y != 0
0x021A: JP 0x020E       ; goto draw_left_right_border

get_new_tetromino:
0x021C: RND V4,0x70     ; tetromino_offset = rnd & 0x70
0x021E: SNE V4,0x70     ; if tetromino_offset = 0x70
0x0220: JP 0x021C       ; goto start_rand
0x0222: RND V3,0x03     ; tetromino_dir = rnd & 0x03
0x0224: LD V0,0x1E      ; x = 30
0x0226: LD V1,0x03      ; y = 3
0x0228: CALL 0x025C     ; get_tetromino_tile()

draw_tetromino:
0x022A: LD DT,V5        ; delay = 16 (1 second)
0x022C: DRW V0,V1,4     ; draw (x,y,4)
0x022E: SE VF,0x01      ; if !collision
0x0230: JP 0x023C       ; goto process_input
0x0232: DRW V0,V1,4     ; else draw(x,y,4) (erase)
0x0234: ADD V1,0xFF     ; y -= 1
0x0236: DRW V0,V1,4     ; draw (x,y,4)
0x0238: CALL 0x0340     ; scan_playfield()
0x023A: JP 0x021C       ; goto get_new_tetromino

process_input:
0x023C: SKNP V7         ; if key_left_pressed
0x023E: JP 0x0272       ;   goto move_left
0x0240: SKNP V8         ; if key_right_pressed
0x0242: JP 0x0284       ;   goto move_right
0x0244: SKNP V9         ; if key_rotate_pressed
0x0246: JP 0x0296       ;   goto rotate
0x0248: SKP V2          ; if !key_down_pressed
0x024A: JP 0x0250       ;   goto draw_erase
0x024C: LD V6,00        ; tmp = 0
0x024E: LD DT,V6        ; DT = tmp

draw_erase:
0x0250: LD V6,DT        ; tmp = DT
0x0252: SE V6,0x00      ; if tmp != 0
0x0254: JP 0x023C       ;   goto process_input
0x0256: DRW V0,V1,4     ; draw(x,y,4) (erase)
0x0258: ADD V1,0x01     ; y += 1
0x025A: JP 0x022A       ; goto draw_tetromino

get_tetromino_tile:
0x025C: LD I,0x2C4      ; I = tetromino_tiles
0x025E: ADD I,V4        ; I += tetromino_offset
0x0260: LD V6,0x00      ; tmp = 0
0x0262: SNE V3,0x01     ; if tetromino_dir = 1
0x0264: LD V6,0x04      ; tmp = 4
0x0266: SNE V3,0x02     ; elif tetromino_dir = 2
0x0268: LD V6,0x08      ; tmp = 8
0x026A: SNE V3,0x03     ; elif tetromino_dir = 3
0x026C: LD V6,0x0C      ; tmp = 12
0x026E: ADD I,V6        ; I += tmp
0x0270: RET             ; return

move_left:
0x0272: DRW V0,V1,4     ; draw (x,y,4) (erase)
0x0274: ADD V0,0xFF     ; x -= 1
0x0276: CALL 0x0334     ; draw_and_wait()
0x0278: SE VF,0x01      ; if !collision
0x027A: RET             ;   return
0x027C: DRW V0,V1,4     ; else draw (x,y,4) (erase)
0x027E: ADD V0,0x01     ;   x += 1
0x0280: CALL 0x0334     ;   draw_and_wait()
0x0282: RET             ;   return

move_right:
0x0284: DRW V0,V1,4     ; draw (x,y,4) (erase)
0x0286: ADD V0,0x01     ; x += 1
0x0288: CALL 0x0334     ; draw_and_wait()
0x028A: SE VF,0x01      ; if !collision
0x028C: RET             ;   return
0x028E: DRW V0,V1,4     ; else draw(x,y,4) (erase)
0x0290: ADD V0,0xFF     ;   x -= 1
0x0292: CALL 0x0334     ;   draw_and_wait()
0x0294: RET             ;   return

rotate:
0x0296: DRW V0,V1,4     ; draw(x,y,4) (erase)
0x0298: ADD V3,0x01     ; tetromino_dir += 1
0x029A: SNE V3,0x04     ; if tetromino_dir == 4
0x029C: LD V3,0x00      ;   tetromino_dir = 0
0x029E: CALL 0x025C     ; get_tetromino_tile()
0x02A0: CALL 0x0334     ; draw_and_wait()
0x02A2: SE VF,0x01      ; if !collision
0x02A4: RET             ;   return
0x02A6: DRW V0,V1,4     ; draw(x,y,4) (erase)
0x02A8: ADD V3,0xFF     ; tetromino_dir -= 1
0x02AA: SNE V3,0xFF     ; if tetromino_dir = -1
0x02AC: LD V3,0x03      ;   tetromino_dir = 3
0x02AE: CALL 0x025C     ; get_tetromino_tile()
0x02B0: CALL 0x0334     ; draw_and_wait()
0x02B2: RET             ; return

setup_variables:
0x02B6: LD V7,0x05      ; key_down = 5
0x02B8: LD V8,0x06      ; key_right = 6
0x02BA: LD V9,0x04      ; key_left = 4
0x02BC: LD V1,0x1F      ; y = 31
0x02BE: LD V5,0x10      ; timer = 16
0x02C0: LD V2,0x07      ; key_drop = 7
0x02C2: RET

draw_and_wait:
0x0334: DRW V0,V1,4     ; draw x,y,4
0x0336: LD V6,0x35      ; tmp = 35
loop_start:
0x0338: ADD V6,0xFF     ; tmp -= 1
0x033A: SE V6,0x00      ; if tmp !=0
0x033C: JP 0x0338       ;   goto loop_start
0x033E: RET             ; else return

scan_playfield:
0x0340: LD I,0x2B4      ; I = single_pixel
0x0342: LD VC,V1        ; VC = y
0x0344: SE VC,0x1E      ; if VC != 30
0x0346: ADD VC,0x01     ; VC += 1
0x0348: SE VC,0x1E      ; if VC != 30
0x034A: ADD VC,0x01     ; VC +=1
0x034C: SE VC,0x1E      ; if VC != 30
0x034E: ADD VC,0x01     ; VC += 1
scan_full_line:
0x0350: CALL 0x035E     ; scan_line()
0x0352: SNE VB,0x0A     ; if pixel_count == 12
0x0354: CALL 0x0372     ;   clean_line()
0x0356: SNE V1,V0       ; if y == x
0x0358: RET             ;   return
0x035A: ADD V1,0x01     ; y += 1
0x035C: JP 0x0350       ; goto scan_full_line

scan_line:
0x035E: LD V0,0x1B      ; x = 27
0x0360: LD VB,0x00      ; pixel_count = 0
scan_pixel:
0x0362: DRW V0,V1,1     ; draw(x,y,1)
0x0364: SE VF,0x00      ; if !collision
0x0366: ADD VB,0x01     ;   pixel_count += 1
0x0368: DRW V0,V1,1     ; draw(x,y,1)
0x036A: ADD V0,0x01     ; x += 1
0x036C: SE V0,0x25      ; if x != 37
0x036E: JP 0x0362       ;   goto scan_pixel 
0x0370: RET             ; else return

clean_line:
0x0372: LD V0,0x1B      ; x = 27
erase_pixel:
0x0374: DRW V0,V1,1     ; draw(x,y,1) (erase pixel)
0x0376: ADD V0,0x01     ; x += 1
0x0378: SE V0,0x25      ; if x != 37
0x037A: JP 0x0374       ;   goto erase_pixel
0x037C: LD VE,V1        ; cur_y = y
0x037E: LD VD,VE        ; prev_y = cur_y
0x0380: ADD VE,0xFF     ; cur_y -= 1
init_scan:
0x0382: LD V0,0x1B      ; x = 27
0x0384: LD VB,0x00      ; pixel_count = 0
test_pixel:
0x0386: DRW V0,VE,1     ; draw(x,cur_y,1) (draw pixel)
0x0388: SE VF,0x00      ; if !collision
0x038A: JP 0x0390       ;   goto no_pixel
0x038C: DRW V0,VE,1     ; else draw(x,cur_y,1) (erase pixel)
0x038E: JP 0x0394       ;   goto 0x394
no_pixel:
0x0390: DRW V0,VD,1     ; draw(x,prev_y,1)
0x0392: ADD VB,0x01     ; pixel_count +=1
0x0394: ADD V0,0x01     ; x += 1
0x0396: SE V0,0x25      ; if x !=37
0x0398: JP 0x0386       ;   goto test_pixel
0x039A: SNE VB,0x00     ; if pixel_count = 0
0x039C: JP 0x03A6       ; goto_update_score
0x039E: ADD VD,0xFF     ; prev_y -=1
0x03A0: ADD VE,0xFF     ; cur_y -=1
0x03A2: SE VD,0x01      ; if prevy = 1
0x03A4: JP 0x0382       ; goto init_scan
0x03A6: CALL 0x03C0     ; draw_score()
0x03A8: SE VF,0x01      ; if !collision
0x03AC: ADD VA,0x01     ; score += 1
update_score:
0x03AE: CALL 0x03C0     ; draw_score()
0x03B0: LD V0,VA        ; temp_score = score
0x03B2: LD VD,0x07      ; mask = 7
0x03B4: AND V0,VD       ; temp_score &= mask
0x03B6: SNE V0,0x04     ; if temp_score = 4
0x03B8: ADD V5,0xFE     ; delay -= 2
0x03BA: SNE V5,0x02     ; if delay = 2
0x03BC: LD V5,0x04      ; delay = 4
0x03BE: RET             ; return

draw_score:
0x03C0: LD I,0x700      ; I = backup_reg
0x03C2: LD [I],V2       ; backup_reg = [V0:V2]
0x03C4: LD I,0x804      ; I = BCD_score
0x03C6: LD B,VA         ; BCD_score = bcd(score)
0x03C8: LD V2,[I]       ; [V0:V2] = BCD_score
0x03CA: LD F,V0         ; I = char(BCD_score[0])
0x03CC: LD VD,0x32      ; temp_x = 50
0x03CE: LD VE,0x00      ; temp_y = 0
0x03D0: DRW VD,VE,5     ; draw(temp_x,temp_y,5)
0x03D2: ADD VD,0x05     ; x_score += 5
0x03D4: LD F,V1         ; I = char(BCD_score[1])
0x03D6: DRW VD,VE,5     ; draw(temp_x,temp_y,5)
0x03D8: ADD VD,0x05     ; temp_x += 5
0x03DA: LD F,V2         ; I = char(BCD_score[2])
0x03DC: DRW VD,VE,5     ; draw(temp_x,temp_y,5)
0x03DE: LD I,0x700      ; I = backup_reg
0x03E0: LD V2,[I]       ; [V0:V2] = backup_reg
0x03E2: LD I,0x2B4      ; I = single_pixel
0x03E4: RET             ; return

reset_x_score:
0x03E6: LD VA,0x00      ; score = 0
0x03E8: LD V0,0x19      ; x = 25
0x03EA: RET             ; return