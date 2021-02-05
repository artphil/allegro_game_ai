import tensorflow as tf
from tensorflow import keras
import numpy as np
import datetime as dt
import random

from .model import DQModel
from .memory import Memory

DELAY_TRAINING = 5000
POST_PROCESS_IMAGE_SIZE = (84, 84, 1)
NUM_FRAMES = 4
HARD_UPDATE_FREQ = 10000
TAU = 0.08
GAMMA = 0.99
BATCH_SIZE = 32


class Player:
	def __init__(self, num_actions, max_memory_size, path):
		self.num_actions = num_actions
		self.primary_network = DQModel(256, num_actions, True)
		self.target_network = DQModel(256, num_actions, True)
		self.primary_network.compile(optimizer=keras.optimizers.Adam(), loss='mse')
		self.path = path
		self.train_writer = tf.summary.create_file_writer(path + f"/DuelingQSI_{dt.datetime.now().strftime('%d%m%Y%H%M')}")

		# make target_network = primary_network
		for t, e in zip(self.target_network.trainable_variables, self.primary_network.trainable_variables):
			t.assign(e)

		self.primary_network.compile(optimizer=keras.optimizers.Adam(), loss=tf.keras.losses.Huber())

		self.memory = Memory(max_memory_size, NUM_FRAMES, BATCH_SIZE, POST_PROCESS_IMAGE_SIZE)

	def choose_action(self, state, eps, step):
		if step < DELAY_TRAINING:
			return random.randint(0, self.num_actions - 1)
		else:
			if random.random() < eps:
				return random.randint(0, self.num_actions - 1)
			else:
				return np.argmax(self.primary_network(tf.reshape(state, (1, POST_PROCESS_IMAGE_SIZE[0],
															POST_PROCESS_IMAGE_SIZE[1], NUM_FRAMES)).numpy()))

	def update_network(self, steps=None, hard_copy=True):
		# update target network parameters slowly from primary network
		for t, e in zip(self.target_network.trainable_variables, self.primary_network.trainable_variables):
			if not hard_copy:
				# Soft Update
				t.assign(t * (1 - TAU) + e * TAU)
			elif steps%HARD_UPDATE_FREQ == 0:
					# Hard Update - Cannot be as frequent
					t.assign(e) 

	def training(self, target=False):
		states, actions, rewards, next_states, terminal = self.memory.sample()
		# predict Q(s,a) given the batch of states
		prim_qt = self.primary_network(states)
		# predict Q(s',a') from the evaluation network
		prim_qtp1 = self.primary_network(next_states)
		# copy the prim_qt tensor into the target_q tensor - we then will update one index corresponding to the max action
		target_q = prim_qt.numpy()
		updates = rewards
		valid_idxs = terminal != True
		batch_idxs = np.arange(BATCH_SIZE)
		if target:
			prim_action_tp1 = np.argmax(prim_qtp1.numpy(), axis=1)
			q_from_target = self.target_network(next_states)
			updates[valid_idxs] += GAMMA * q_from_target.numpy()[batch_idxs[valid_idxs], prim_action_tp1[valid_idxs]]
		else:
			updates[valid_idxs] += GAMMA * np.amax(prim_qtp1.numpy()[valid_idxs, :], axis=1)

		target_q[batch_idxs, actions] = updates
		loss = self.primary_network.train_on_batch(states, target_q)
		return loss
	
	def save_training(self, tot_reward, avg_loss, i):
		with self.train_writer.as_default():
			tf.summary.scalar('reward', tot_reward, step=i)
			tf.summary.scalar('avg loss', avg_loss, step=i)
	

	def save_networks(self):
		self.primary_network.save_weights(self.path+"/pretrained_primary_weights.h5")
		self.target_network.save_weights(self.path+"/pretrained_target_weights.h5")

	def load_networks(self):
		try:
			self.primary_network.load_weights(self.path+"/pretrained_primary_weights.h5")
			self.target_network.load_weights(self.path+"/pretrained_target_weights.h5")
		except:
			print('Arquivos de treino não encontrados')


