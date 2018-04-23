from __future__ import division
import numpy as np
import random
from random import choice
import datetime
import pickle
from math import log, sqrt



class RandomAgent(object):

	"""
	Docstring for RandomAgent
	"""
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

	""" 
	Docstring for Learner
	"""
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

class MonteCarlos(object):
	"""
	Docstring for MonteCarlos
	"""
	def __init__(self, env, **args):
		self.env = env
		self.states = []
		self.wins = {}
		self.plays = {}

		# Seconds to run simulations
		# Defaukt: 10
		sec = args.get('time', 10) 
		self.calc_time = datetime.timedelta(seconds=sec)

		# Max steps to play in simulation
		# Default: 100
		self.max_steps = args.get('max_steps', 100)

		# UCB1 const
		self.C = args.get('C', 1.4)




	def update(self, cur_state):
		self.states.append(cur_state)

	def run_episode(self):
		self.max_depth = 0
		state = self.states[-1]
		player = self.env.current_player(state)

		legal_actions = self.env.legal_actions(state)

		# Break out early if no possible actions of only a single action can be taken
		if not legal_actions:
			return
		if len(legal_actions) == 1:
			return legal_actions[0]

		games = 0
		begin = datetime.datetime.utcnow()
		while datetime.datetime.utcnow() - begin < self.calc_time:
			self.run_simulation()
			games += 1

		moves_states = [(p, self.board.next_state(state, p)) for p in legal]

		# Display the number of calls of `run_simulation` and the total time elapsed
		print(games, datetime.datetime.utcnow() - begin)

		# 
		percent_win, move = max((self.wins.get((player, S), 0) / 
								self.plays.get((player, S), 1), 
								p) for p, S in moves_states)

		# Display the stats for each possible play.
		for x in sorted(
			((100 * self.wins.get((player, S), 0) /
				self.plays.get((player, S), 1),
				self.wins.get((player, S), 0),
			self.plays.get((player, S), 0), p)
			for p, S in moves_states),
			reverse=True
		):
			print("{3}: {0:.2f}% ({1} / {2})".format(*x))

		print("Maximum depth searched:", self.max_depth)

		return move


	
	def run_simulation(self):
		# A bit of an optimization here, so we have a local
		# variable lookup instead of an attribute access each loop.
		plays, wins = self.plays, self.wins

		visited_states = set()
		states_cpy = self.states[:]
		state = states_cpy[-1]
		player = self.env.current_player(state)

		expand = True
		for t in xrange(self.max_steps):
			legal_actions = self.env.legal_actions(state)
			moves_states = [(p, self.board.next_state(state, p)) for p in legal_actions]

			if all((plays.get(player,S)) for p,S in moves_states):

				log_total = log(sum(plays[(player,S)] for p, S in moves_states))
				value, move, state = max(((wins[(player,S)] / plays[(player, S)]), p, S)
					for p, S in moves_states
				)
			else:
				move, state = choice(moves_states)


			nxt_state, reward, done = self.env.step(state, action)
			states_cpy.append(nxt_state)

			if expand and (player, state) not in self.plays:
				expand = False
				self.wins[(player,state)] = 0
				self.plays[(player,state)] = 0
				if t > self.max_depth:
					self.max_depth = t

			visited_states.add((player, state))

			player = self.env.current_player(state) 
			state = nxt_state
			winner = self.env.winner(states_cpy)
			if done:
				break

		for player, state in visited_states:
			if (player, state) not in self.play:
				continue
			self.plays[(player, state)] += 1
			if player == winner:
				self.wins[(player, state)] += 1



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