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
		# I changed ANY to ALL so that it only picks a random unexplored action if it has no prior experience in this state
		if all(s2 not in Learner.TREE.keys() for s2,_ in followers):
			return random.choice([a for s2,a in followers if s2 not in Learner.TREE.keys()])
		else:
			return max((self.minwin(s2),a) for s2,a in followers if s2 in Learner.TREE.keys())[1]

	def think(self, state):
		players = self.game.PLAYERS
		for p in range(self.playouts):
			reward = None
			turn = 0
			s = state
			visited = []
			# play game
			while reward == None:
				followers = [(self.game.step(s, a),a) for a in self.game.legal_actions(s)]

				if any(s2 not in Learner.TREE.keys() for s2,_ in followers):
					action = random.choice([a for s2,a in followers if s2 not in Learner.TREE.keys()])
				else:
					action = max((self.minUCT(s2),a) for s2,a in followers)[1]
				visited.append((s,turn))
				s = self.game.step(s, action)
				reward = self.game.reward(s)
				turn = (turn + 1) % players
			# update tree
			last = visited[-1][1]
			for s,p in visited:
				# add to tree if not present
				if Learner.TREE.get(s) is None:
					Learner.TREE[s] = [0,0]
				# increment visit count
				Learner.TREE[s][1] += 1
				# increment win count
				if p is last:
					Learner.TREE[s][0] += reward
				else:
					Learner.TREE[s][0] -= reward
			# increment total plays
			Learner.PLAYS += 1
		# update all Learners' trees
		Learner.TREE = Learner.TREE
		Learner.PLAYS = Learner.PLAYS

	def save(self, filename):
		Learner.TREE['plays'] = PLAYS
		pickle.dump(Learner.TREE.open(filename,'wb'))

	def load(self, filename):
		Learner.TREE = pickle.load(open(filename,'rb'))
		Learner.PLAYS = Learner.TREE.pop('plays')
	

	def UCT(self, state):
		score, plays = Learner.TREE.get(state)
		return score / float(plays) + sqrt( 2*log(Learner.PLAYS) / float(plays) )

	def minUCT(self, state):
		score, plays = Learner.TREE.get(state)
		return (plays - score) / float(plays) + sqrt( 2*log(Learner.PLAYS) / float(plays) )

	def win(self, state):
		score, plays = Learner.TREE.get(state)
		return score / float(plays)

	def minwin(self, state):
		score, plays = Learner.TREE.get(state)
		return (plays - score) / float(plays)

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
		print(self.game.__doc__)

	def action(self, state):
		print(self.game)
		legals = {i : a for i,a in enumerate(self.game.legal_actions())}
		action = None
		while action not in legals.keys():
			print('Legal Actions:')
			print('\n'.join([str(i) + ': ' + str(a) for i,a in legals.items()]))
			action = int(input('What is your move?\n'))
		return legals.get(action)

	def save(self, filename):
		pass

	def load(self, filename):
		pass