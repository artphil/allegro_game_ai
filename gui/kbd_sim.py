import pyautogui as pg
import time

# new terminal
pg.hotkey("ctrl","alt", "t")

time.sleep(3)
pg.click(100, 100)
# Go to dir
pg.typewrite("cd Git/allegro_game_ai/games/frogger")
pg.press("return")

pg.typewrite("./frogger.exe")
pg.press("return")

time.sleep(0.1)
pg.click(100, 100)
for i in range(5):
	pg.press("w")

time.sleep(3)
for i in range(2):
	pg.press("w")


time.sleep(3)
for i in range(3):
	pg.press("w")
