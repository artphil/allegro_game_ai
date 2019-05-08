from game_ai import *
import pyautogui as ag
from random import randint

data = finder("games\\frogger\\frogger.c")
print(data.keys)
control = ctrl("games\\frogger", "frogger.exe", "frogger.exe")

l = len(data.keys)-1
while control.window.isActive():
# for i in range(10):
    a = data.keys[randint(0,l)]
    print("Pressed:", a) 
    ag.press(a)


