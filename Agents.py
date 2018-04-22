import numpy as np
import random
import pickle


class RandomAgent(object):

	"""docstring for RandomAgent"""
	def __init__(self, num_states, num_actions):
		self.num_actions = num_actions

	def action(self, state, legal_actions):
		# return random.randrange(num_actions)
		return random.choice(legal_actions)

	def update(self, state, action, reward):
		pass

	def save(self, filename):
		pass

	def load(self, filename):
		pass

class Learner(object):

	TREE = 'tree'

	"""docstring for Learner"""
	def __init__(self, game, playouts = 100):
		# self.Q = [[random.random() for a in range(num_actions)] for s in range(num_states)]
		# self.get_action = get_action
		self.game = game
		self.playouts = playouts

	def action(self, state, legal_actions):
		return self.get_action()

	def update(self, state, action, reward):
		Learner.TREE = 'bush'

	def think(self):
		for p in range(self.playouts):
			followers = self.game.followers()


	def save(self, filename):
		d = {'Q' : self.Q, 'get_action' : self.get_action}

	def load(self, filename):
		pass

'''
def get_softmax(nums):
	maxx = np.max(nums)
	return np.exp(nums-maxx)/np.sum(np.exp(nums-maxx))

def softmax(values, percomp = None, epsilon = None):
	options = np.cumsum(softmax(values))
	choice = np.random.rand()
	return next(action for action,value in enumerate(options) if value >= choice)

def egreedy(values, percomp = None, epsilon = 0.05):
	if np.random.rand() < epsilon:
		return get_action_uniform(values)
	return get_action_optimal(values)

def optimal(values, percomp = None, epsilon = None):
	return np.argmax(values)

def uniform(values, percomp = None, epsilon = None):
	return np.random.choice(values.shape[0],)'''