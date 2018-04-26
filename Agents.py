from __future__ import division
import numpy as np
import random
from random import choice
import datetime
import pickle
from math import log, sqrt
import string


class RandomAgent(object):

	"""
	Docstring for RandomAgent
	"""
	def __init__(self, game, name = 'Dom Randy'):
		self.name = name
		self.game = game

	def action(self, state):
		return random.choice(self.game.legal_actions(state))

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
			visited.append((s,turn))
			# update tree
			last = visited[-2][1]
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
		Learner.TREE['plays'] = Learner.PLAYS
		pickle.dump(Learner.TREE,open(filename,'wb'))

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
				move, state = random.choice(moves_states)


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
		self.game.display(state)
		alpha = string.ascii_lowercase
		legals = {alpha[i] : a for i,a in enumerate(self.game.legal_actions(state))}
		action = None
		while action not in legals.keys():
			print('Legal Actions:')
			print('\n'.join([str(i) + ': ' + str(a) for i,a in legals.items()]))
			action = input('What is your move?\n')
			if action == 'help':
				print(self.game.__doc__)
		return legals.get(action)

	def save(self, filename):
		pass

	def load(self, filename):
		pass


class Minimax(object):

    # Required
    def __init__(self, game, name = 'Max Minnie'):
    	self.name = name
		self.game = game
        # self.board = [b[:] for b in board]
        # self.rows = len(self.board)
        # self.cols = len(self.board[0])

    # def get_board(self):
    #     return self.board

    # def reset(self):
    #     self.board = [b[:] for b in [[False]*self.cols]*self.rows]

    # def is_legal_move(self, row, col, vertical):
    #     if vertical:
    #         if row + 1 < self.rows and col < self.cols:
    #             if row >= 0 and col >= 0:
    #                 return (not self.board[row][col]) & (not self.board[row+1][col])
    #         return False
    #     else:
    #         if row < self.rows and col + 1 < self.cols:
    #             if row >= 0 and col >= 0:
    #                 return (not self.board[row][col]) & (not self.board[row][col+1])
    #         return False

    # def legal_moves(self, vertical):
    #     return ((r,c) for r in xrange(self.rows) for c in xrange(self.cols) if self.is_legal_move(r,c,vertical))  ############## XRANGE

    # def perform_move(self, row, col, vertical):
    #     if self.is_legal_move(row,col,vertical):
    #         self.board[row][col] = True
    #         if vertical:
    #             self.board[row+1][col] = True
    #         else:
    #             self.board[row][col+1] = True
    #         return self

    # def game_over(self, vertical):
    #     return len(list(self.legal_moves(vertical))) == 0

    # def copy(self):
    #     return DominoesGame([b[:] for b in self.board])

    # def successors(self, vertical):
    #     return (((r,c),self.copy().perform_move(r,c,vertical)) for (r,c) in self.legal_moves(vertical))

    # def get_random_move(self, vertical):
    #     return random.choice(list(self.legal_moves(vertical)))

    # Required
    def get_best_move(state, limit = float('inf')):
        alpha = -float('inf')
        beta = float('inf')
        return self.max_value(state,limit,alpha,beta)

    def max_value(self,state,limit,alpha,beta):
        # if limit == 0 or self.game_over(vertical):
        #     return ((),self.utility(vertical),1)
        v = -float('inf')
        count = 0
        followers = [(self.game.step(s, a),a) for a in self.game.legal_actions(s)]
        for s,a in followers:
            (_,new_v,new_count) = s.min_value(not vertical,limit-1,alpha,beta)
            count += new_count
            if new_v > v:
                v = new_v
                if v >= beta:
                    return ((),v,count)
                alpha = max(alpha,v)
                action = a
        return (action,v,count)

    def min_value(self,vertical,limit,alpha,beta):
        # print('MIN')
        # print('Limit?',limit,limit == 0)
        # print('Game Over?',self.game_over(vertical))
        # print('Limit or Game Over?',limit == 0 | self.game_over(vertical))
        if limit == 0 or self.game_over(vertical):
            return ((),self.utility(not vertical),1)
        v = float('inf')
        count = 0
        # print('# Successors:',len(list(self.successors(vertical))))
        for a,s in self.successors(vertical):
            (_,new_v,new_count) = s.max_value(not vertical,limit-1,alpha,beta)
            count += new_count
            if new_v < v:
                v = new_v
                if v <= alpha:
                    return ((),v,count)
                beta = min(beta,v)
                action = a
        return (action,v,count)
        # v = min(v,max_value(not vertical,limit-1,alpha,beta))

    def utility(self,vertical):
        return len(list(self.legal_moves(vertical))) - len(list(self.legal_moves(not vertical)))