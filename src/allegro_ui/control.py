import os
import subprocess
import pygetwindow as gw
import pyautogui as ag

from .base import _OS

# Atuador
class control:
	def __init__(self,fexe,title):
		# Se desloca para a pasta do programa
		# os.chdir(path)
		# Inicia o programa em um novo proocesso
		self.process = subprocess.Popen(fexe, stdout=subprocess.PIPE, shell=True)
		
		if _OS == 'WIN':
			self.window = getWindowWindows(title)
		else:
			print('Sistema Operacional não suportado')
			quit()

	def getWindowWindows(self,title):
		# Espera a janela abrir e a ativa 
		while True:	
			try: 
				window = gw.getWindowsWithTitle(title)[0]
				window.activate()
				break
			except:
				pass 

		return window

	def getWindowMac(self,title,locate_on_screen,box_height,box_width=None,adjust_top=0,adjust_left=0): # !!!! Workaround - NOT RECOMENDED !!!!
		return window_for_mac(title,locate_on_screen,box_height,box_width,adjust_top,adjust_left)


	def getWindowLinux(self,title,locate_on_screen,box_height,box_width=None,adjust_top=0,adjust_left=0): # !!!! Workaround - NOT RECOMENDED !!!!
		return None

	# Retorna o estado da janela
	def isActive(self):
		return self.window.isActive

	# Recupera as posições dos limites da janela 
	def edges(self):
		return self.window.left, self.window.left+self.window.width, self.window.top, self.window.top+self.window.height

	# Preciona uma tecla
	def press(self, key):
		return ag.press(key)

	# Clica com o mouse
	def click(self, coord_x, coord_y):
		return ag.click(x=coord_x, y=coord_y)