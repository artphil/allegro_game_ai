# https://pyautogui.readthedocs.io/en/latest/cheatsheet.html

import pyautogui as pg
import pygetwindow as gw
import os
import time
import subprocess
import sys

''''''
# start the app in a separate process using the same interpreter as this script
# process = subprocess.Popen([sys.executable, 'games/frogger/frogger.exe'])
print(os.listdir())
os.chdir('games\\frogger')
print(os.listdir())
process = subprocess.Popen('frogger.exe', shell=True)
# wait for the window
for x in gw.getAllTitles():
	print(x) 
while True:	
	# window = pg.getWindow("frogger.exe")
	window = False
	try: 
		window = gw.getWindowsWithTitle("frogger.exe")[0]
	except:
		pass 

	if window:
		window.activate()
		break

for i in range(10):
	pg.press("w")
