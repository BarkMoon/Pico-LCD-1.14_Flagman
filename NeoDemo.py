import Lcd1_14driver
from KeyInput import ExPin, KeyInput
from machine import Pin,PWM
import time
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

BL = 13   # lcd back light pin declaration

# color parameters are set for RGB565
# B (higher 5bit) R (middle 6bit) G (lower 5bit)

if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(100)
    pwm.duty_u16(32768)    #max value is 65535
    LCD.fill(LCD.white)
 
    #LCD.lcd_show()
    
    LCD.text("FLAGMAN",90,65,LCD.red)
    
    #LCD.hline(10,10,220,LCD.blue)
    #LCD.hline(10,125,220,LCD.blue)
    #LCD.vline(10,10,115,LCD.blue)
    #LCD.vline(230,10,115,LCD.blue)
    
    LCD.rect(10, 10, 220, 115, LCD.blue)
    
    LCD.lcd_show()
    
    while(1):
        
        if(keyinput.OnButtonDown(keyinput.up)):
            print("joyUp press")
            LCD.fill(0xfff0)      # 0x00ff for pink color 
            LCD.lcd_show()
                  
        elif(keyinput.OnButtonDown(keyinput.down)):
            print("joyDown press")
            LCD.fill(0x0f00)     # 0x00ff for blue color 
            LCD.lcd_show()
        
        elif(keyinput.OnButtonDown(keyinput.left)):
            print("joyLeft press")
            LCD.fill(0x00ff)      # 0x00ff for yellow color 
            LCD.lcd_show()
            
        elif(keyinput.OnButtonDown(keyinput.right)):
            print("joyRight press")
            LCD.fill(0x00f0)     # 0x00ff for red color 
            LCD.lcd_show()

        elif(keyinput.OnButtonDown(keyinput.select)):
            print("joySel press")
            LCD.fill(0x000f)      # 0x00ff for green color 
            LCD.lcd_show()
        
        elif(keyinput.OnButtonDown(keyinput.A)):
            print("A press")
            LCD.fill(LCD.red + LCD.blue)      # purple color 
            LCD.lcd_show()
            
        elif(keyinput.OnButtonDown(keyinput.B)):
            print("B press")
            LCD.fill(LCD.black)      # black color 
            LCD.lcd_show()
            
        keyinput.ReadAll()
        
            
            
    LCD.lcd_show()
    time.sleep(1)
    #LCD.fill(0xFFFF)
