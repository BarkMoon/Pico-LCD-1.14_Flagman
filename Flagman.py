# Flagman.py ver. 1.0.0

import Lcd1_14driver
from KeyInput import ExPin, KeyInput
from ImageBuf import ImageBuf
from ImageData import iyami_body_32_80, iyami_hand_up_15_25, iyami_hand_down_15_25, iyami_hand_left_27_12, iyami_hand_right_26_8
from machine import Pin,PWM
import time
import random
LCD = Lcd1_14driver.Lcd1_14()

#------pin declaration----- 
    
joyUp = ExPin(2 ,Pin.IN,Pin.PULL_UP) 
joyDown= ExPin(18 ,Pin.IN,Pin.PULL_UP)
joyLeft = ExPin(16 ,Pin.IN,Pin.PULL_UP)
joyRight = ExPin(20 ,Pin.IN,Pin.PULL_UP)
joySel = ExPin(3 ,Pin.IN,Pin.PULL_UP)
keyA = ExPin(15,Pin.IN,Pin.PULL_UP)
keyB = ExPin(17,Pin.IN,Pin.PULL_UP)

keyinput = KeyInput(joyUp, joyDown, joyLeft, joyRight, joySel, keyA, keyB)

BL = 13   # lcd back light pin declaration

#------image buffer declaration----- 

iyami_body = ImageBuf(32, 80, iyami_body_32_80)
iyami_hand_up = ImageBuf(15, 25, iyami_hand_up_15_25)
iyami_hand_down = ImageBuf(15, 25, iyami_hand_down_15_25)
iyami_hand_left = ImageBuf(27, 12, iyami_hand_left_27_12)
iyami_hand_right = ImageBuf(26, 8, iyami_hand_right_26_8)

iyami_hand = (iyami_hand_up, iyami_hand_down, iyami_hand_left, iyami_hand_right)
iyami_hand_offset = ((22, 12), (22, 31), (1, 29), (22, 29))

#------other declaration----- 

exit_game = False
keyname = ("UP", "DOWN", "LEFT", "RIGHT")

# color parameters are set for RGB565
# B (higher 5bit) R (middle 6bit) G (lower 5bit)

if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(100)
    pwm.duty_u16(32768)    #max value is 65535
    
    while(not exit_game):
        
        title_n = 2
        while(1):
            if keyinput.GetKeyDown(keyinput.up):
                title_n = 0
            elif keyinput.GetKeyDown(keyinput.down):
                title_n = 1
            elif keyinput.GetKeyDown(keyinput.left):
                title_n = 2
            elif keyinput.GetKeyDown(keyinput.right):
                title_n = 3
            elif keyinput.GetKeyDown(keyinput.A):
                break
            if keyinput.GetKeyDown(keyinput.B):
                exit_game = True
                break
            keyinput.ReadAll()
            
            LCD.fill(LCD.white)
            LCD.text("FLAGMAN", 90, 65, LCD.red)
            LCD.blit(iyami_body, 35, 25, 0xffff)
            LCD.blit(iyami_hand[title_n], 35 + iyami_hand_offset[title_n][0], 25 + iyami_hand_offset[title_n][1], 0xffff)
            LCD.blit(iyami_body, 170, 25, 0xffff)
            LCD.blit(iyami_hand[title_n], 170 + iyami_hand_offset[title_n][0], 25 + iyami_hand_offset[title_n][1], 0xffff)
            LCD.rect(10, 10, 220, 115, LCD.blue)
            LCD.lcd_show()
        
        number_list = []
            
        if exit_game:
            LCD.fill(LCD.black)
            LCD.rect(10, 10, 220, 115, LCD.blue)
            LCD.text("SEE YOU NEXT GAME!", 50, 65, LCD.white)
            LCD.lcd_show()
            time.sleep_us(2000000)
            LCD.fill(LCD.black)
            LCD.lcd_show()
            continue
    
        all_correct = True
        while(all_correct):
        
            n = random.randrange(4)
            number_list.append(n)
            print(number_list)
        
            LCD.fill(LCD.blue)
            LCD.text("Remember the Directions!", 25, 20, LCD.red)
            LCD.lcd_show()
            time.sleep(2)
        
            for x in number_list:
                LCD.fill(LCD.black)
                LCD.fill_rect(42, 12, 160, 96, LCD.white)
                LCD.blit(iyami_body, 105, 20, 0xffff)
                LCD.blit(iyami_hand[x], 105 + iyami_hand_offset[x][0], 20 + iyami_hand_offset[x][1], 0xffff)
                LCD.lcd_show()
                time.sleep_us(500000)
                LCD.fill(LCD.blue)
                LCD.lcd_show()
        
            answer_list = []
            i=0
            while i < len(number_list):
                answer = 2
                while(1):
                    if keyinput.GetKeyDown(keyinput.up):
                        answer = 0
                    elif keyinput.GetKeyDown(keyinput.down):
                        answer = 1
                    elif keyinput.GetKeyDown(keyinput.left):
                        answer = 2
                    elif keyinput.GetKeyDown(keyinput.right):
                        answer = 3
                    elif keyinput.GetKeyDown(keyinput.B):
                        if i > 0:
                            answer_list.pop(i-1)
                            i -= 1
                            break
                    elif keyinput.GetKeyDown(keyinput.A):
                        answer_list.append(answer)
                        i += 1
                        break
                    keyinput.ReadAll()
                    LCD.fill(LCD.white)
                    LCD.text("Answer the Directions!", 30, 15, LCD.red)
                    LCD.blit(iyami_body, 105, 20, 0xffff)
                    LCD.blit(iyami_hand[answer], 105 + iyami_hand_offset[answer][0], 20 + iyami_hand_offset[answer][1], 0xffff)
                    for j in range(len(answer_list)):
                        LCD.text(keyname[answer_list[j]], 48*(j%5), 100+(j//5)*12, LCD.black)
                    LCD.lcd_show()
                keyinput.ReadAll()
        
            LCD.fill(LCD.white)
            LCD.lcd_show()
            time.sleep(1)
            
            for i in range(len(number_list)):
                LCD.fill(LCD.white)
                LCD.blit(iyami_body, 55, 25, 0xffff)
                LCD.blit(iyami_hand[number_list[i]], 55 + iyami_hand_offset[number_list[i]][0], 25 + iyami_hand_offset[number_list[i]][1], 0xffff)
                LCD.blit(iyami_body, 150, 25, 0xffff)
                LCD.blit(iyami_hand[answer_list[i]], 150 + iyami_hand_offset[answer_list[i]][0], 25 + iyami_hand_offset[answer_list[i]][1], 0xffff)
                LCD.lcd_show()
                if number_list[i] != answer_list[i]:
                    all_correct = False
                time.sleep_us(500000)
            
            if all_correct:
                LCD.fill(LCD.green)
                LCD.blit(iyami_body, 55, 25, 0xffff)
                LCD.blit(iyami_hand[number_list[i]], 55 + iyami_hand_offset[number_list[i]][0], 25 + iyami_hand_offset[number_list[i]][1], 0xffff)
                LCD.blit(iyami_body, 150, 25, 0xffff)
                LCD.blit(iyami_hand[answer_list[i]], 150 + iyami_hand_offset[answer_list[i]][0], 25 + iyami_hand_offset[answer_list[i]][1], 0xffff)
                LCD.lcd_show()
            else:
                LCD.fill(LCD.red)
                LCD.blit(iyami_body, 55, 25, 0xffff)
                LCD.blit(iyami_hand[number_list[i]], 55 + iyami_hand_offset[number_list[i]][0], 25 + iyami_hand_offset[number_list[i]][1], 0xffff)
                LCD.blit(iyami_body, 150, 25, 0xffff)
                LCD.blit(iyami_hand[answer_list[i]], 150 + iyami_hand_offset[answer_list[i]][0], 25 + iyami_hand_offset[answer_list[i]][1], 0xffff)
                LCD.lcd_show()
            
            time.sleep_us(1250000)
        
        record = len(number_list)-1
        
        LCD.fill(LCD.white)
        if record >= 25:
            LCD.text("You are Memory Master!", 30, 32, LCD.red)
        LCD.text("Record: " + str(record), 70, 65, LCD.black)
        LCD.rect(10, 10, 220, 115, LCD.blue)
        LCD.lcd_show()
        
        while(1):
            keyinput.ReadAll()
            time.sleep_us(16666)
            if keyinput.GetKeyDown(keyinput.A):
                break
