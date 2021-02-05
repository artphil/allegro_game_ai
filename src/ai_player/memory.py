import numpy as np


class Memory:
	def __init__(self, max_memory, num_frames, bath_size, image_size):
		self._max_memory = max_memory
		self._actions = np.zeros(max_memory, dtype=np.int32)
		self._rewards = np.zeros(max_memory, dtype=np.float32)
		self._frames = np.zeros((image_size[0], image_size[1], max_memory), dtype=np.float32)
		self._terminal = np.zeros(max_memory, dtype=np.bool)
		self._i = 0
		self.image_size = image_size
		self.num_frames = num_frames
		self.bath_size = bath_size

	def add_sample(self, frame, action, reward, terminal):
		self._actions[self._i] = action
		self._rewards[self._i] = reward
		self._frames[:, :, self._i] = frame[:, :, 0]
		self._terminal[self._i] = terminal
		if self._i % (self._max_memory - 1) == 0 and self._i != 0:
			self._i = self.bath_size + self.num_frames + 1
		else:
			self._i += 1

	def sample(self):
		if self._i < self.bath_size +  self.num_frames + 1:
			raise ValueError("Not enough memory to extract a batch")
		else:
			rand_idxs = np.random.randint( self.num_frames + 1, self._i, size=self.bath_size)
			states = np.zeros((self.bath_size, self.image_size[0], self.image_size[1], self.num_frames),
							 dtype=np.float32)
			next_states = np.zeros((self.bath_size, self.image_size[0], self.image_size[1], self.num_frames),
							 dtype=np.float32)
			for i, idx in enumerate(rand_idxs):
				states[i] = self._frames[:, :, idx - 1 -  self.num_frames:idx - 1]
				next_states[i] = self._frames[:, :, idx -  self.num_frames:idx]
			return states, self._actions[rand_idxs], self._rewards[rand_idxs], next_states, self._terminal[rand_idxs]