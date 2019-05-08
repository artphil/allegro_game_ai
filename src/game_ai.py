import pyautogui as ag
import pygetwindow as gw
import os
import subprocess

class ctrl:
	def __init__(self,path,fexe,title):
		# Se desloca para a pasta do programa
		os.chdir(path)
		# Inicia o programa em um novo proocesso
		self.process = subprocess.Popen(fexe, shell=True)
		

		# Espera a janela abrir e a ativa 
		window = False
		while True:	
			try: 
				window = gw.getWindowsWithTitle(title)[0]
			except:
				pass 

			if window:
				self.window = window
				window.activate()
				break

class finder:
	def __init__(self, file_name):
		# Abre o arquivo *.c
		try:
			self.file = open(file_name, 'r').read()
		except:
			print("File {} not found.".format(file_name))
			return

		# Guarda todas as palavras do arquivo 
		self.words = self.to_list(self.file)
		# Recupera todas as teclas pressionaveis
		self.keys = self.get_keys('ALLEGRO_KEY_')
		
	# Transforma um arquivo.c em uma lista de palavras
	def to_list(self, txt):
		# Aprende todos osimbolos utilizados
		simbols = []
		valids = [' ','_']
		for a in txt:
			if not a.isalnum() and a not in valids:
				if a not in simbols:
					simbols.append(a)
		
		new_txt = txt
		
		# Retira os simbolos do texto para facilitar a separacao
		for s in simbols:
			new_txt = new_txt.replace(s, ' ')

		# Separa todas as palavras e cria uma lista das validas
		return [w for w in new_txt.split(' ') if len(w) > 0 ]

	# Retorna todas as palavras que contem um termo
	def search(self, name):
		word_list = []

		for word in self.words:
			if len(word) < len(name):
				continue

			for i in range(len(word)):
				if len(word)-i < len(name):
					break

				if name[0] == word[i]:
					found = False

					for j in range(len(name)):
						if name[j] == word[i+j]:
							found = True
						else:
							found = False
							break

					if found and word not in word_list:
						word_list.append(word)
						break

		return word_list

	# Retorna todas as teclas validas
	def get_keys(self, prefix):
		# Lista as palavras com comandos de tecla
		w_list = self.search(prefix)
		k_list = []
		
		# Retira o prefixo de comando
		for w in w_list:
			k_list.append(w.replace(prefix, ''))
		
		# Lista as teclas 
		return [k.lower() for k in k_list if len(k) > 0 ]
