import os
import pyautogui as ag

from .base import BAR

# Perceptor
class state():
	n = 0
	nt = 0
	ct = 0.0
	def __init__(self, window):
		print(window)
		self.win = window
		if not os.path.exists('img'):
			os.makedirs('img')
		
	def print(self, name, serial=True):
		if self.win.isActive:
			self.n = self.n+1
			if serial:
				file_name = 'img'+BAR+name+str(self.n)+'.jpg'
			else: 
				file_name = 'img'+BAR+name+'.jpg'

			return ag.screenshot(file_name, region=(self.win.left, self.win.top, self.win.width, self.win.height))
