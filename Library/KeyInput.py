from machine import Pin

class ExPin(Pin):
    def __init__(self, id, mode=-1, pull=-1):
        super().__init__(id, mode, pull)
        self.ON_VALUE = 0 if pull == Pin.PULL_UP else 1
        self.OFF_VALUE = 1 if pull == Pin.PULL_UP else 0
        self.last_value = self.OFF_VALUE

class KeyInput():
    def __init__(self, JoyUp, JoyDown, JoyLeft, JoyRight, JoySelect, ButtonA, ButtonB):
        self.up = JoyUp
        self.down = JoyDown
        self.left = JoyLeft
        self.right = JoyRight
        self.select = JoySelect
        self.A = ButtonA
        self.B = ButtonB
        
    def ReadAll(self):
        self.up.last_value = self.up.value()
        self.down.last_value = self.down.value()
        self.left.last_value = self.left.value()
        self.right.last_value = self.right.value()
        self.select.last_value = self.select.value()
        self.A.last_value = self.A.value()
        self.B.last_value = self.B.value()
        
    # previous name is OnButtonDown
    # True when the key is pressed
    def GetKeyDown(self, Key):
        if Key.last_value == Key.OFF_VALUE and Key.value() == Key.ON_VALUE:
            Key.last_value = Key.ON_VALUE
            return True
        else:
            return False
        
    # True when the key is released
    def GetKeyUp(self, Key):
        if Key.last_value == Key.ON_VALUE and Key.value() == Key.OFF_VALUE:
            Key.last_value = Key.OFF_VALUE
            return True
        else:
            return False
        
    # True when the key is being pressed
    def GetKey(self, Key):
        if Key.value() == Key.ON_VALUE:
            return True
        else:
            return False