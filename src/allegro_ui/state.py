import os
import pyautogui as ag

from .base import BAR

# Perceptor
class state():
	n = 0
	def __init__(self, window, path='.', name='screen'):
		print(window)
		self.path = path + BAR + 'img'
		self.win = window
		self.name = name
		if not os.path.exists(self.path):
			os.makedirs(self.path)
		
	def print(self):
		if self.win.isActive:
			self.n = self.n+1
			print_name = self.path+BAR+self.name+str(self.n)+'.png'

			return ag.screenshot(print_name, region=(self.win.left, self.win.top, self.win.width, self.win.height))
		else:
			return None