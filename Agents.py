import numpy as np
import random


class RandomAgent(object):

	"""docstring for RandomAgent"""
	def __init__(self, num_states, num_actions):
		self.num_actions = num_actions

	def action(self, state, legal_actions):
		# return random.randrange(num_actions)
		return random.choice(legal_actions)

	def update(self, state, action, reward):
		pass