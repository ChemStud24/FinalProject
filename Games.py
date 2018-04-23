import numpy as np
import random
import pickle

# ========= State Space =========
# Your dice : M
# Opponents dice : M
# Opponents ante : N*M | N = 6

# ========= Action Space =========
# Call BS
# Ante: n*m
# n e [1, N], m e [1, M]

# Dynamic action space
# Changed depending on the number of dice you have



# Give each play a number of known dice
# previous bets
	# Learn how an opponent bets
	# Proof of concept would be to beat some hard coded strategies 

class LiarsDice(object):

	"""docstring for LiarsDice

	State: 3-tuple (my_roll, opponent # of dice, opponent previous bid)
	Actions: 2-tuple bid
	"""
	def __init__(self, num_agents, num_opponents, num_dice):
		self.num_opponents = num_opponents
		self.num_dice = num_dice
		self.num_agents = num_agents
		self.num_players = num_agents + num_opponents
		self.player_dice_num = [num_dice for _, in self.num_players]
		self.dice = [np.random.randInt(1,num_dice) for _ in self.num_players]
		self.turn = np.random.randInt(num_players)

		self.state = [self.turn, ]

	def done(self):
		#########################
		# should rename to reward
		#########################
		pass

	def legal_actions(self):
		pass

	def step(self, action):
		nxt_state 

	def play(self):
		pass

	def display(self):
		pass

	def __str__(self):
		pass
		
class TicTacToe(object):

	"""docstring for TicTacToe

	State: board (as deep tuple)

	Actions: int
	[[0, 1, 2],
	[3, 4, 5],
	[6, 7, 8]]
	"""

	PLAYERS = 2 # number of players

	def __init__(self, agent, opponent, size = 3):
		self.size = size
		self.board = [['*' for c in range(self.size)] for r in range(self.size)]
		self.players = [agent(self),opponent(self)]
		random.shuffle(self.players)

	def reward(self, board = None):
		if board == None:
			board = self.copy_board(self.board)
		# DRAW
		if len(self.legal_actions(board)) == 0:
			return 0
		# ROW
		if any(all(sq == 'x' for sq in row) or all(sq == 'o' for sq in row) for row in self.board): # row
			return 1
		# COLUMN
		if any(all(row[c] == 'x' for row in self.board) or all(row[c] == 'o' for row in self.board) for c in range(self.size)): # column
			return 1
		# DIAGONAL DOWN RIGHT
		if all(self.board[n][n] == 'x' for n in range(self.size)) or all(self.board[n][n] == 'o' for n in range(self.size)):
			return 1
		# DIAGONAL UP RIGHT
		z = zip(list(range(self.size)),list(range(self.size-1,-1,-1)))
		if all(self.board[r][c] == 'x' for r,c in z) or all(self.board[r][c] == 'o' for r,c in z):
			return 1
		# NOT DONE
		return None

	def legal_actions(self, board = None):
		if board == None:
			board = self.copy_board(self.board)
		return [n for n,s in enumerate(flatten(board)) if s == '*']

	def step(self, board, action):
		board = self.copy_board(board)
		if flatten(board).count('x') > flatten(board).count('o'):
			piece = 'o'
		else:
			piece = 'x'
		board[int(action / self.size)][action % self.size] = piece
		return self.state(board)

	def play(self):
		# play through
		self.reset()
		reward = None
		while reward is None:
			for player in self.players:
				action = player.action(self.state())
				self.board = self.step(self.board, action)
				reward = self.reward()
				if reward is not None:
					print(reward)
					break
				print(self)
		# print result
		if reward > 0:
			print(player.name + ' wins!')
			print(self)
		else:
			print('Draw!')
			print(self)

	def get_players(self):
		return self.players

	def copy_board(self, board = None):
		if board == None:
			board = self.board
		return [[sq for sq in row] for row in board]

	def state(self, board = None):
		if board == None:
			board = self.copy_board(self.board)
		return tuple([tuple(row) for row in board])

	def reset(self):
		self.board = self.board = [['*' for c in range(self.size)] for r in range(self.size)]
		random.shuffle(self.players)

	def display(self, board = None):
		if board == None:
			board = self.copy_board(self.board)
		print(self.__str__(), board)

	def __str__(self, board = None):
		if board == None:
			board = self.copy_board(self.board)
		# piece to move
		if flatten(board).count('x') > flatten(board).count('o'):
			piece = 'o'
		else:
			piece = 'x'
		# print string
		return '\n'.join([' '.join(board[r]) for r in range(len(board))]) + '\n\'' + piece + '\' to move.\n\n'

class Hexapawn(object):

	"""docstring for Hexapawn

	Actions: 2-tuple (pawn, direction)
	0: top-most, left-most pawn ; take left
	1: middle pawn ; move forward
	2: bottom-most, right=most pawn ; take right
	"""
	def __init__(self, agent, opponent, size = 3):
		self.size = size
		self.board = [['B' for s in range(self.size)]]
		for s in range(self.size-2):
			self.board += [['*' for s in range(self.size)]]
		self.board += [['W' for s in range(self.size)]]
		self.players = random.shuffle([agent,opponent])
		self.pieces = ['W','B']
		self.turn = 0

	def done(self, board = None):
		###########################################################################################
		# this needs to be more nuanced because in some of these black wins while others white wins
		###########################################################################################
		if board == None:
			board = self.board
		if any(sq == 'W' for sq in board[0]): # white at the end
			return True
		if any(sq == 'B' for sq in board[len(board)-1]): # black at the end
			return True
		if len(self.legal_actions(board)) == 0: # no legal moves
			return True
		if not any(sq == 'W' for sq in flatten(board)): # no white pawns
			return True
		if not any(sq == 'B' for sq in flatten(board)): # no black pawns
			return True
		return False

	def legal_actions(self):
		pass

	def step(self):
		pass

	def play(self):
		while True:
			self.step
			if self.done():
				breakS

	def display(self, board = None):
		if board == None:
			board = self.board
		print(self.__str__(), board)

	def __str__(self, board = None):
		###############################
		# add whose move it is to print
		###############################
		if board == None:
			board = self.board
		return '\n'.join([' '.join(board[r]) for r in range(len(board))])

def flatten(seqs):
	return [el for seq in seqs for el in seq]


if __name__ == '__main__':

	# test cases: False, 0-8, True, 3-8, True, 124578, True, 123567, True, 013578
	ttt = TicTacToe(0,0)
	print(ttt.done())
	print(ttt.legal_actions())

	ttt.board = [['x','x','x'],['*','*','*'],['*','*','*']]
	print(ttt.done())
	print(ttt.legal_actions())

	ttt.board = [['x','*','*'],['x','*','*'],['x','*','*']]
	print(ttt.done())
	print(ttt.legal_actions())

	ttt.board = [['x','*','*'],['*','x','*'],['*','*','x']]
	print(ttt.done())
	print(ttt.legal_actions())

	ttt.board = [['*','*','x'],['*','x','*'],['x','*','*']]
	print(ttt.done())
	print(ttt.legal_actions())