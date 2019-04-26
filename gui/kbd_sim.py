# https://pyautogui.readthedocs.io/en/latest/cheatsheet.html

import pyautogui as pg
import os
import time
import subprocess
import sys

''''''
# start the app in a separate process using the same interpreter as this script
process = subprocess.Popen([sys.executable, 'frogger.exe'])
# wait for the window
while True:	
	window = pg.getWindow("frogger.exe")
	if window:
		window.set_foreground()
		break
'''

# new terminal
pg.hotkey("ctrl","alt", "t")

time.sleep(3)
pg.click(100, 100)

# Go to dir
pg.typewrite("cd Git/allegro_game_ai/games/frogger")
pg.press("return")

pg.typewrite("./frogger.exe")
pg.press("return")

# time.sleep(0.1)
pg.click(100, 100)

'''
for i in range(5):
	pg.press("w")

time.sleep(3)
for i in range(2):
	pg.press("w")


time.sleep(3)
for i in range(3):
	pg.press("w")
