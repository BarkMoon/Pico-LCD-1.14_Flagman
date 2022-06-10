import Lcd1_14driver
from KeyInput import ExPin, KeyInput
from ImageBuf import ImageBuf
from ImageData import poyo_walk0_24_24, poyo_cro4_24_24
from machine import Pin,PWM
import time
import random
LCD = Lcd1_14driver.Lcd1_14()

#------joystck pin declaration----- 
    
joyUp = ExPin(2 ,Pin.IN,Pin.PULL_UP) 
joyDown= ExPin(18 ,Pin.IN,Pin.PULL_UP)
joyLeft = ExPin(16 ,Pin.IN,Pin.PULL_UP)
joyRight = ExPin(20 ,Pin.IN,Pin.PULL_UP)
joySel = ExPin(3 ,Pin.IN,Pin.PULL_UP)
keyA = ExPin(15,Pin.IN,Pin.PULL_UP)
keyB = ExPin(17,Pin.IN,Pin.PULL_UP)

keyinput = KeyInput(joyUp, joyDown, joyLeft, joyRight, joySel, keyA, keyB)

poyo_walk0 = ImageBuf(24, 24, poyo_walk0_24_24)
poyo_cro4 = ImageBuf(24, 24, poyo_cro4_24_24)

BL = 13   # lcd back light pin declaration

# color parameters are set for RGB565
# B (higher 5bit) R (middle 6bit) G (lower 5bit)

if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(100)
    pwm.duty_u16(32768)    #max value is 65535
    
    keyname = ["UP", "DOWN", "LEFT", "RIGHT"]
    
    while(1):
        
        LCD.fill(LCD.white)
        LCD.text("FLAGMAN", 90, 65, LCD.red)
        LCD.blit(poyo_walk0, 55, 55, 0xffff)
        LCD.blit(poyo_cro4, 155, 56, 0xffff)
    
        LCD.rect(10, 10, 220, 115, LCD.blue)
    
        LCD.lcd_show()
        
        number_list = []
    
        while(1):
            keyinput.ReadAll()
            time.sleep_us(16666)
            if keyinput.OnButtonDown(keyinput.A):
                keyinput.ReadAll()
                break
    
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
                LCD.text(keyname[x], 100, 65, LCD.white)
                LCD.lcd_show()
                time.sleep(1)
                LCD.fill(LCD.blue)
                LCD.lcd_show()
        
            answer_list = []
            i=0
            while i < len(number_list):
                answer = 0
                while(1):
                    if keyinput.OnButtonDown(keyinput.up):
                        answer = 0
                    elif keyinput.OnButtonDown(keyinput.down):
                        answer = 1
                    elif keyinput.OnButtonDown(keyinput.left):
                        answer = 2
                    elif keyinput.OnButtonDown(keyinput.right):
                        answer = 3
                    elif keyinput.OnButtonDown(keyinput.B):
                        if i > 0:
                            answer_list.pop(i-1)
                            i -= 1
                            break
                    elif keyinput.OnButtonDown(keyinput.A):
                        answer_list.append(answer)
                        i += 1
                        break
                    keyinput.ReadAll()
                    LCD.fill(LCD.white)
                    LCD.text("Answer the Directions!", 30, 20, LCD.red)
                    LCD.text(keyname[answer], 100, 65, LCD.black)
                    for j in range(len(answer_list)):
                        LCD.text(keyname[answer_list[j]], 48*(j%5), 95+(j//5)*12, LCD.black)
                    LCD.lcd_show()
                keyinput.ReadAll()
        
            LCD.fill(LCD.white)
            LCD.lcd_show()
            time.sleep(1)
            for i in range(len(number_list)):
                LCD.text(keyname[number_list[i]], 48*(i%5), 20+(i//5)*12, LCD.black)
                LCD.text(keyname[answer_list[i]], 48*(i%5), 80+(i//5)*12, LCD.black)
                LCD.lcd_show()
                if number_list[i] != answer_list[i]:
                    all_correct = False
                time.sleep(1)
        
            if all_correct:
                LCD.fill(LCD.green)
                for i in range(len(number_list)):
                    LCD.text(keyname[number_list[i]], 48*(i%5), 20+(i//5)*12, LCD.black)
                    LCD.text(keyname[answer_list[i]], 48*(i%5), 80+(i//5)*12, LCD.black)
                LCD.lcd_show()
            else:
                LCD.fill(LCD.red)
                for i in range(len(number_list)):
                    LCD.text(keyname[number_list[i]], 48*(i%5), 20+(i//5)*12, LCD.black)
                    LCD.text(keyname[answer_list[i]], 48*(i%5), 80+(i//5)*12, LCD.black)
                LCD.lcd_show()
            
            time.sleep_us(1250000)
        
        LCD.fill(LCD.white)
        LCD.text("Record: "+str(len(number_list)-1),70,65,LCD.red)
        LCD.rect(10, 10, 220, 115, LCD.blue)
        LCD.lcd_show()
        
        while(1):
            keyinput.ReadAll()
            time.sleep_us(16666)
            if keyinput.OnButtonDown(keyinput.A):
                keyinput.ReadAll()
                break
        #LCD.fill(0xFFFF)
