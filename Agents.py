import numpy as np
import random
import pickle
from math import sqrt, log


class RandomAgent(object):

	"""
	Instantiate RandomAgent with Game object as an argument.
	This agent will make pseudo-random legal moves in the game it plays.
	"""

	def __init__(self, game, name = 'Dom Randy'):
		self.name = name
		self.num_actions = num_actions

	def action(self, state):
		return random.choice(self.game.legal_actions())

	def update(self, state, action, reward):
		pass

	def save(self, filename):
		pass

	def load(self, filename):
		pass

class Learner(object):

	TREE = {}
	PLAYS = 0

	"""docstring for Learner"""
	def __init__(self, game, playouts = 100, name = 'Carlos Monty'):
		self.name = name
		self.game = game
		self.playouts = playouts

	def action(self, state):
		self.think(state)
		followers = [(self.game.step(state, a),a) for a in self.game.legal_actions(state)]
		return max((self.minwin(s2),a) for s2,a in followers)[1]

	def think(self, state):
		players = game.PLAYERS
		for p in range(self.playouts):
			reward = None
			turn = 0
			s = state
			visited = []
			# play game
			while reward == None:
				followers = [(self.game.step(s, a)[0],a) for a in self.game.legal_actions(s)]
				if any(s2 not in TREE.keys() for s2,_ in followers):
					action = random.choice(a for s2,a in followers if s2 not in TREE.keys())
				else:
					action = max((self.minUCT(s2),a) for s2,a in followers)[1]
				visited.append((state,turn))
				s, reward = game.step(s, action)
				turn = (turn + 1) % players
			# update tree
			winner = visited[-1][1]
			for s,p in visited:
				TREE[s][1] += 1
				if p is winner:
					TREE[s][0] += 1
			PLAYS += 1

	def save(self, filename):
		TREE['plays'] = PLAYS
		pickle.dump(TREE,open(filename,'wb'))

	def load(self, filename):
		TREE = pickle.load(open(filename,'rb'))
		PLAYS = TREE.pop('plays')

	def UCT(self, state):
		score, plays = TREE.get(state)
		return score / float(plays) + sqrt( 2*log(PLAYS) / float(plays) )

	def minUCT(self, state):
		score, plays = TREE.get(state)
		return (plays - score) / float(plays) + sqrt( 2*log(PLAYS) / float(plays) )

	def win(self, state):
		score, plays = TREE.get(state)
		return score / float(plays)

	def minwin(self, state):
		score, plays = TREE.get(state)
		return (plays - score) / float(plays)

class Human(object):

	'''
	This class represents a human player in a Game class.
	Use it to allow humans to play.
	The class will diplay a representation of the Game and
	query a user input for the human's next move.
	'''

	def __init__(self, game, name = 'Hugh Mann'):
		self.name = name
		self.game = game

	def action(self, state):
		print(self.game)

	def save(self, filename):
		pass

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