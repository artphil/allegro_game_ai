import os
import io
import subprocess
import pygetwindow as gw
import pyautogui as ag

from .base import _OS

# Atuador
class Control:
	def __init__(self,fexe,title):
		# Se desloca para a pasta do programa
		# os.chdir(path)
		# Inicia o programa em um novo proocesso
		self.process = subprocess.Popen(fexe, 
						shell=True,
                        stdout=subprocess.PIPE,
						)
		
		if _OS == 'WIN':
			self.window = self.getWindowWindows(title)
		else:
			print('Sistema Operacional não suportado')
			quit()

	def getWindowWindows(self,title):
		# Espera a janela abrir e a ativa 
		count = 0
		while True:
			if count > 1000:
				return None
			try: 
				window = gw.getWindowsWithTitle(title)[0]
				window.activate()
				break
			except:
				pass 
			count += 1	

		return window

	def getWindowMac(self,title,locate_on_screen,box_height,box_width=None,adjust_top=0,adjust_left=0): # !!!! Workaround - NOT RECOMENDED !!!!
		return None # window_for_mac(title,locate_on_screen,box_height,box_width,adjust_top,adjust_left)


	def getWindowLinux(self,title,locate_on_screen,box_height,box_width=None,adjust_top=0,adjust_left=0): # !!!! Workaround - NOT RECOMENDED !!!!
		return None

	# Retorna o estado da janela
	def isActive(self):
		return self.window.isActive

	# Recupera as posições dos limites da janela 
	def edges(self):
		return self.window.left, self.window.left+self.window.width, self.window.top, self.window.top+self.window.height

	def stop(self):
		self.process.terminate()
		while self.window.isActive:
			pass

	# Preciona uma tecla
	def press(self, key):
		return ag.press(key)

	# Clica com o mouse
	def click(self, coord_x, coord_y):
		return ag.click(x=coord_x, y=coord_y)

	def getReward(self):
		try:
			output = self.process.stdout.read1().decode()
			reward = int(output.split()[0])
		except:
			self.stop()
			reward = 0
		return reward
	

# Classe de janela para Mac !!!! Workaround - NOT RECOMENDED !!!!
class window_for_mac:
	def __init__(self,title,locate_on_screen,box_height,box_width=None,adjust_top=0,adjust_left=0):
		self.title = title
		self.isActive = False
		self.box_region = None
		while not self.isActive:
			try:
				self.box_region=ag.locateOnScreen(locate_on_screen)
				self.isActive = self.box_region is not None
			except:
				pass

		self.top = self.box_region.top + self.box_region.height + adjust_top
		self.left = self.box_region.left + adjust_left
		self.width = box_width if box_width is not None else self.box_region.width
		self.height = box_height