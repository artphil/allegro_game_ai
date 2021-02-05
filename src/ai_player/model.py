import tensorflow as tf
from tensorflow import keras

class DQModel(keras.Model):
	def __init__(self, hidden_size: int, num_actions: int, dueling: bool):
		super(DQModel, self).__init__()
		self.dueling = dueling
		self.conv1 = keras.layers.Conv2D(16, (8, 8), (4, 4), activation='relu')
		self.conv2 = keras.layers.Conv2D(32, (4, 4), (2, 2), activation='relu')
		self.flatten = keras.layers.Flatten()
		self.adv_dense = keras.layers.Dense(hidden_size, activation='relu',
										 kernel_initializer=keras.initializers.he_normal())
		self.adv_out = keras.layers.Dense(num_actions,
										  kernel_initializer=keras.initializers.he_normal())
		if dueling:
			self.v_dense = keras.layers.Dense(hidden_size, activation='relu',
										 kernel_initializer=keras.initializers.he_normal())
			self.v_out = keras.layers.Dense(1, kernel_initializer=keras.initializers.he_normal())
			self.lambda_layer = keras.layers.Lambda(lambda x: x - tf.reduce_mean(x))
			self.combine = keras.layers.Add()

	def call(self, input):
		x = self.conv1(input)
		x = self.conv2(x)
		x = self.flatten(x)
		adv = self.adv_dense(x)
		adv = self.adv_out(adv)
		if self.dueling:
			v = self.v_dense(x)
			v = self.v_out(v)
			norm_adv = self.lambda_layer(adv)
			combined = self.combine([v, norm_adv])
			return combined
		return adv