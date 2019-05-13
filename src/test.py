from game_ai import *
import pyautogui as ag
from random import randint
import sys

if len(sys.argv) > 1:
    f_name = sys.argv[1]
else:
    f_name = 'teste'

data = finder("games\\frogger\\frogger.c")
print(data.keys)
control = ctrl("games\\frogger", "frogger.exe", "frogger.exe")
capture = state(control.window)

l = len(data.keys)-1
while control.window.isActive:
# for i in range(10):
    a = data.keys[randint(0,l)]
    if a != 'escape':
        print("Pressed:", a) 
        ag.press(a)
    else:
        print('pause') 
    capture.print(f_name)


