import os
import numpy as np
from random import randint
from tkinter import filedialog

import allegro_ui as au
from ai_player import Image, Player

MAX_EPSILON = 1
MIN_EPSILON = 0.05
EPSILON_MIN_ITER = 50000

NUM_FRAMES = 4
POST_PROCESS_IMAGE_SIZE = (84, 84, 1)
MAX_MEMORY_SIZE = 50000
GIF_RECORDING_FREQ = 200

NUM_EPISODES = 100001
DELAY_TRAINING = 5000


print('Iniciando programa')

print('Selecione o código fonte do jogo')
path_file_code = filedialog.askopenfilename(filetypes=[("Código C", ".c")])
print (path_file_code)
print()

print('Selecione o executável do jogo')
path_file_exe = filedialog.askopenfilename(filetypes=[("Execuável", ".exe")])
filename_exe = path_file_exe.split('/')[-1]
path_folder = path_file_exe.replace('/'+filename_exe, '')
print (path_file_exe)
print ('Pasta', path_folder)
print ('Executável:', filename_exe)
print()

os.chdir(path_folder)

print('Selecione um diretório para os resultados')
path_results = filedialog.askdirectory()
print (path_results)
print()

if not path_file_code or not path_file_exe or not path_results:
	print('Arquivos necessário não encontrados')
	quit()

# Obitendo dados do jogo
data = au.Finder(path_file_code)
print(data)
# mouse =
print('Mouse ON' if data.mouse else 'Mouse OFF')
print('Teclas:',data.keys)
print()

image = Image(path_results)
player = Player(len(data.keys), MAX_MEMORY_SIZE, path_results)

# Carregando pesos antigos
op = input('Deseja usar pesos salvos?(S/N)')
if op.lower() == 's':
	player.load_networks()

# Treinamento
eps = MAX_EPSILON
double_q = True
steps = 0
max_tot_reward = 0
tot_reward_hist = []

for i in range(NUM_EPISODES):
	# Iniciando o jogo
	last_reward = 0
	position = 0
	cnt = 1
	avg_loss = 0
	frame_list = []
	done = False

	control = au.Control(path_file_exe, filename_exe)
	if not control:
		continue
	capture = au.State(control.window, path_results)
	width = control.window.width
	height = control.window.height
	
	try:
		screen = np.array(capture.print())[:,:,:3]
	except:
		print(f'Erro ao iniciar jogo. Episodio {i}')
		control.stop()
		continue

	state = image.preprocess(screen)
	state_stack = image.stack(state, NUM_FRAMES)
	frame_list.append(image.cast(screen, width, height))

	while True:
		choice = player.choose_action(state_stack, eps, steps)
		action = data.keys[choice]
		
		# Takes action and get observation
		if action != 'escape':
			control.press(action)

		tot_reward = control.getReward()
		reward = tot_reward - last_reward
		last_reward = tot_reward
		try:
			screen = np.array(capture.print())[:,:,:3]
		except:
			# print(f'Erro ao atualizar jogo. Episodio {i}')
			control.stop()
			done = True

		if done:
			if steps > DELAY_TRAINING:
				if i%100 == 0:
					player.save_networks()
				avg_loss /= cnt
				print(f"Episode: {i}, Reward: {tot_reward:.2f}, avg loss: {avg_loss:.5f}, eps: {eps:.3f}, total steps: {steps}")
				player.save_training(tot_reward, avg_loss, i)
			else:
				print(f"Pre-training...Episode: {i}, Reward: {tot_reward:.2f}, total steps: {steps}")
			if i % GIF_RECORDING_FREQ == 0:
				image.save_gif(frame_list, i)
			if tot_reward > max_tot_reward:
				max_tot_reward = tot_reward
				image.save_gif(frame_list,i,best=True)
			tot_reward_hist.append(tot_reward)
			break

		next_state = image.preprocess(screen)
		state_stack = image.process_stack(state_stack, next_state)
		frame_list.append(image.cast(screen, width, height))

		# store in memory
		player.memory.add_sample(next_state, choice, reward, done)

		if steps > DELAY_TRAINING:
			loss = player.training(target=True if double_q else False)
			player.update_network(steps)
		else:
			loss = -1
		avg_loss += loss

		# linearly decay the eps value
		if steps > DELAY_TRAINING:
			eps = MAX_EPSILON - ((steps - DELAY_TRAINING) / EPSILON_MIN_ITER) * \
				  (MAX_EPSILON - MIN_EPSILON) if steps < EPSILON_MIN_ITER+DELAY_TRAINING else \
				MIN_EPSILON
	
		steps += 1
		cnt += 1

np.array(tot_reward_hist).tofile(os.path.join(path_results, 'tot_reward_hist.csv'),sep='\n',format='%.2f')
