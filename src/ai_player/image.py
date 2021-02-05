
import os
import tensorflow as tf
import imageio
import numpy as np


PRE_PROCESS_IMAGE_SIZE = (84, 84)

class Image:
	def __init__(self, path):
		self.path = path + '/recorded_episodes'
		if not os.path.exists(self.path):
			os.makedirs(self.path)

	def preprocess(self, image, new_size=PRE_PROCESS_IMAGE_SIZE):
		# convert to greyscale, resize and normalize the image
		img = tf.image.rgb_to_grayscale(image)
		img = tf.image.resize(img, new_size)
		return img #/ 255

	def stack(self, image, num_frames):
		img = tf.Variable(np.repeat(image.numpy(), num_frames).reshape((PRE_PROCESS_IMAGE_SIZE[0], PRE_PROCESS_IMAGE_SIZE[1], num_frames)))
		return img

	def process_stack(self, state_stack, state):
		for i in range(1, state_stack.shape[-1]):
			state_stack[:, :, i - 1].assign(state_stack[:, :, i])
		state_stack[:, :, -1].assign(state[:, :, 0])
		return state_stack

	def cast(self, image, width, height):
		return tf.cast(tf.image.resize(image, (width, height)), tf.uint8).numpy()
		
	def save_gif(self, frame_list, episode, fps=5, best=False):
		if best:
			imageio.mimsave(self.path + f'/BEST_EPISODE-{episode}.gif', frame_list, fps=fps)
		else:
			imageio.mimsave(self.path + f'/EPISODE-{episode}.gif', frame_list, fps=fps)


