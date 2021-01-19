import os
import subprocess
import pygetwindow as gw
import pyautogui as ag

# Atuador
class control:
	def __init__(self,fexe,title):
		# Se desloca para a pasta do programa
		# os.chdir(path)
		# Inicia o programa em um novo proocesso
		self.process = subprocess.Popen(fexe, shell=True)
		
		# Espera a janela abrir e a ativa 
		while True:	
			try: 
				self.window = gw.getWindowsWithTitle(title)[0]
				self.window.activate()
				break
			except:
				pass 

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