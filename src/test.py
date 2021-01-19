import allegro_ui as au

import sys
import os
from random import randint
from tkinter import filedialog

BAR = au.base.BAR

print('Iniciando programa')

print('Selecione o código fonte do jogo')
path_file_code = filedialog.askopenfilename(filetypes=[("Código C", ".c")])
print (path_file_code)
print()

print('Selecione o executável do jogo')
path_file_exe = filedialog.askopenfilename(filetypes=[("Execuável", ".exe")])
filename_exe = path_file_exe.split('/')[-1]
print (path_file_exe)
print ('Executável:', filename_exe)
print()

print('Selecione um diretório para os resultados')
path_results = filedialog.askdirectory()
print (path_results)
print()

# Obitendo dados do jogo
data = au.finder(path_file_code)
print(data)
# mouse =
print('Mouse ON' if data.mouse else 'Mouse OFF')
print('Teclas:',data.keys)
print()

control = au.control(path_file_exe, filename_exe)

capture = au.state(control.window, path_results)

l = len(data.keys)-1
while control.window.isActive:
    if data.keyboard:
        a = data.keys[randint(0,l)]
        if a != 'escape':
            print("Pressed:", a) 
            control.press(a)
        else:
            print('pause') 
        capture.print()
    if data.mouse:
        x1, x2, y1, y2 = control.edges()
        x = randint(x1,x2)
        y = randint(y1,y2)
        print("Clicked:", x, y)
        control.click(x,y)
        capture.print()
