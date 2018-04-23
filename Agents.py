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
		self.game = game

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
		self.playouts = max(playouts,1)

	def action(self, state):
		self.think(state)
		followers = [(self.game.step(state, a),a) for a in self.game.legal_actions(state)]
		return max((self.minwin(s2),a) for s2,a in followers if s2 in self.TREE.keys())[1]

	def think(self, state):
		players = self.game.PLAYERS
		for p in range(self.playouts):
			reward = None
			turn = 0
			s = state
			visited = []
			# play game
			while reward == None:
				followers = [(self.game.step(s, a)[0],a) for a in self.game.legal_actions(s)]
				if any(s2 not in self.TREE.keys() for s2,_ in followers):
					action = random.choice([a for s2,a in followers if s2 not in self.TREE.keys()])
				else:
					action = max((self.minUCT(s2),a) for s2,a in followers)[1]
				visited.append((s,turn))
				s = self.game.step(s, action)
				reward = self.game.reward(s)
				turn = (turn + 1) % players
			# update tree
			winner = visited[-1][1]
			for s,p in visited:
				# add to tree if not present
				if self.TREE.get(s) is None:
					self.TREE[s] = [0,0]
				# increment visit count
				self.TREE[s][1] += 1
				# increment win count
				if p is winner:
					self.TREE[s][0] += 1
			# increment total plays
			self.PLAYS += 1
		# update all Learners' trees
		Learner.TREE = self.TREE
		Learner.PLAYS = self.PLAYS

	def save(self, filename):
		self.TREE['plays'] = PLAYS
		pickle.dump(self.TREE,open(filename,'wb'))

	def load(self, filename):
		self.TREE = pickle.load(open(filename,'rb'))
		self.PLAYS = self.TREE.pop('plays')
		Learner.TREE = self.TREE
		Learner.PLAYS = self.PLAYS

	def UCT(self, state):
		score, plays = self.TREE.get(state)
		return score / float(plays) + sqrt( 2*log(self.PLAYS) / float(plays) )

	def minUCT(self, state):
		score, plays = self.TREE.get(state)
		return (plays - score) / float(plays) + sqrt( 2*log(self.PLAYS) / float(plays) )

	def win(self, state):
		score, plays = self.TREE.get(state)
		return score / float(plays)

	def minwin(self, state):
		score, plays = self.TREE.get(state)
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