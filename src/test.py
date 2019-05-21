from game_ai import *
import pyautogui as ag
from random import randint
import sys
import os
import platform

if platform.system() == "Windows":
    bar = '\\'
else:
    bar = '/'

if len(sys.argv) > 1:
    folder = game = sys.argv[1]
else:
    print('\nE necessario o nome do jogo.\n')
    quit()

if len(sys.argv) > 2:
    f_name = sys.argv[2]
else:
    f_name = 'teste'

if not os.path.isfile("games"+bar+folder+bar+game+".c"):
    print("Arquivo 'games"+bar+folder+bar+game+".c' nao existe")
    quit()

print("games"+bar+folder+bar+game+".c")
data = finder("games"+bar+folder+bar+game+".c")
print(data)
print(data.keys)

control = ctrl("games"+bar+folder, game+".exe", game+".exe")
capture = state(control.window)

# capture.print_clock(f_name, 300)

l = len(data.keys)-1
while control.window.isActive:
    if data.keyboard:
        a = data.keys[randint(0,l)]
        if a != 'escape':
            print("Pressed:", a) 
            ag.press(a)
        else:
            print('pause') 
        capture.print(f_name)
    if data.mouse:
        x1, x2, y1, y2 = control.edges()
        x = randint(x1,x2)
        y = randint(y1,y2)
        print("Clicked:", x, y)
        ag.click(x=x,y=y)
        capture.print(f_name)

