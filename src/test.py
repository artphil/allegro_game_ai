from game_ai import *
import pyautogui as ag
from random import randint
import sys
import platform

if platform.system() == "Windows":
    bar = '\\'
else:
    bar = '/'

if len(sys.argv) > 1:
    f_name = sys.argv[1]
else:
    f_name = 'teste'

folder, game = "frogger", "frogger"
# folder, game = "guitarhero", "ghero"
# folder, game = "osmos", "osmos"

print("game"+bar+folder+bar+game+".c")
data = finder("game"+bar+folder+bar+game+".c")
print(data.keys)

control = ctrl("game"+bar+folder, game+".exe", game+".exe")
capture = state(control.window)

# capture.print_clock(f_name, 300)

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


