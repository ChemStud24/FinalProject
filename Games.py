import numpy as np
import random
import pickle
import matplotlib.pyplot as plt


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

	"""
	Instructions: TicTacToe

	Try to get all of your pieces in a row, column, or diagonal to win.
	On your turn, make a move by indicating which space you want to put
	your piece in.  The squares are numbered starting with the top-left
	square as 0.  'x' moves first.

	Type 'help' to repeat these instructions.
	"""
	
	"""docstring for TicTacToe

	State: board (as deep tuple)

	Actions: int
	[[0, 1, 2],
	[3, 4, 5],
	[6, 7, 8]]
	"""

	PLAYERS = 2 # number of players

	def __init__(self, players, size = 3):
		self.size = size
		# self.board = [['*' for c in range(self.size)] for r in range(self.size)]
		# self.players = [0,1]
		# self.turn = random.choice(self.players)
		self.players = players

		# results for this game
		for player in self.players:
			player.wins_first = 0
			player.wins_second = 0
			player.losses_first = 0
			player.losses_second = 0
			player.draws_first = 0
			player.draws_second = 0

		# random.shuffle(self.players)
		self.reset()
		
	def initialize(self):
		self.board = [['*' for c in range(self.size)] for r in range(self.size)]
		# random.shuffle(self.players)
		self.turn = random.choice(self.players)
		return self.board, self.turn 

	def reward(board):
		# if board == None:
		# 	board = self.copy_board(self.board)\
		board = TicTacToe.copy_board(board)
		size = len(board)

		# ROW
		if any(all(sq == 'x' for sq in row) or all(sq == 'o' for sq in row) for row in board): # row
			# print(1)
			return 1
		# COLUMN
		if any(all(row[c] == 'x' for row in board) or all(row[c] == 'o' for row in board) for c in range(size)): # column
			# print(2)
			return 1
		# DIAGONAL DOWN RIGHT
		if all(board[n][n] == 'x' for n in range(size)) or all(board[n][n] == 'o' for n in range(size)):
			# print(3)
			return 1
		# DIAGONAL UP RIGHT
		z = list(zip(list(range(size)),list(range(size-1,-1,-1))))
		if all(board[r][c] == 'x' for r,c in z) or all(board[r][c] == 'o' for r,c in z):
			# print(4)
			return 1
				# DRAW
		if len(TicTacToe.legal_actions(board)) == 0:
			return 0
		# NOT DONE
		return None

	def legal_actions(board):
		# if board == None:
		# 	board = self.copy_board(self.board)
		board = TicTacToe.copy_board(board)
		return [n for n,s in enumerate(flatten(board)) if s == '*']

	def step(board, action):
		board = TicTacToe.copy_board(board)
		size = len(board)
		if flatten(board).count('x') > flatten(board).count('o'):
			piece = 'o'
		else:
			piece = 'x'
		board[int(action / size)][action % size] = piece
		return TicTacToe.state(board)

	def play(self, games = 1):
		for g in range(games):
			# play through
			self.reset()
			reward = None
			while reward is None:
				for player in self.players:
					action = player.action(TicTacToe.state(self.board))
					self.board = TicTacToe.step(self.board, action)
					reward = TicTacToe.reward(self.board)
					if reward is not None:
						break

			if reward > 0:
				if player is self.players[0]:
					player.wins_first += 1
					for p in self.players:
						if p is not player:
							p.losses_second += 1
				else:
					player.wins_second += 1
					for p in self.players:
						if p is not player:
							p.losses_first += 1
			else:
				self.players[0].draws_first += 1
				for p in self.players[1:]:
					p.draws_second += 1


	def copy_board(board):
		# if board == None:
			# board = self.board
		return [[sq for sq in row] for row in board]

	def state(board):
		# if board == None:
		# 	board = TicTacToe.copy_board(board)
		return tuple([tuple(row) for row in TicTacToe.copy_board(board)])

	def reset(self):
		self.board = [['*' for c in range(self.size)] for r in range(self.size)]
		random.shuffle(self.players)

	def display(board):
		# if board == None:
		# 	board = self.copy_board(self.board)
		# print(self.__str__(), board)
		board = TicTacToe.copy_board(board)
		if flatten(board).count('x') > flatten(board).count('o'):
			piece = 'o'
		else:
			piece = 'x'
		# print string
		print('\n'.join([' '.join(board[r]) for r in range(len(board))]) + '\n\'' + piece + '\' to move.\n\n')


	def __str__(self):
		# if board == None:
		# 	board = TicTacToe.copy_board(self.board)
		# piece to move
		board = TicTacToe.copy_board(self.board)
		if flatten(board).count('x') > flatten(board).count('o'):
			# piece = 'o'
			player = self.players[1].name
		else:
			# piece = 'x'
			player = self.players[0].name
		# return string
		return '\n'.join([' '.join(board[r]) for r in range(len(board))]) + '\n\'' + player + '\' to move.\n\n'

# class Game(object):
# 	"""docstring for Game"""
# 	def __init__(self, arg):
# 		pass

# 	def play(self):
# 		pass
		
class HexaPawn(object):

	"""docstring for Hexapawn

	Actions: 2-tuple (pawn, direction)
	0: top-most, left-most pawn ; take left
	1: middle pawn ; move forward
	2: bottom-most, right=most pawn ; take right
	"""
	PLAYERS = 2 # number of players
	def __init__(self, players, size = 3):
		self.size = size
		# self.board = [['*' for c in range(self.size)] for r in range(self.size)]
		# self.players = [0,1]
		# self.turn = random.choice(self.players)
		self.players = players

		# results for this game
		for player in self.players:
			player.wins_first = 0
			player.wins_second = 0
			player.losses_first = 0
			player.losses_second = 0
			player.draws_first = 0
			player.draws_second = 0

		self.reset()

		# self.players = random.shuffle([agent,opponent])

	def reward(self, board):
		###########################################################################################
		# this needs to be more nuanced because in some of these black wins while others white wins
		###########################################################################################
		board = TicTacToe.copy_board(board)
		size = len(board[0])
		if board == None:
			board = self.board
		if any(sq == 'W' for sq in board[0]): # white at the end
			return 1
		if any(sq == 'B' for sq in board[len(board)-1]): # black at the end
			return 1
		if len(self.legal_actions(board)) == 0: # no legal moves
			return 1
		if not any(sq == 'W' for sq in flatten(board)): # no white pawns
			return 1
		if not any(sq == 'B' for sq in flatten(board)): # no black pawns
			return 1
		return 0

	def legal_actions(board, piece):
		board = HexaPawn.copy_board(board)
		free_spaces = [n for n,s in enumerate(flatten(board)) if s == '*']
		black_pieces = [n for n,s in enumerate(flatten(board)) if s == 'B']
		white_pieces = [n for n,s in enumerate(flatten(board)) if s == 'W']
		size = len(board[0])
		if piece == 'B': 
			black_forward = [a for a in free_spaces if any(np.array(black_pieces) + size == a)] 
			black_forward_piece = np.concatenate([list(np.where(np.array(black_pieces) + size == a)[0]) for a in free_spaces]).astype(int)

			black_take_right = [a for a in white_pieces if any(np.array(black_pieces) + size + 1 == a) and a % size != 0] 
			black_right_piece = np.concatenate([list(np.where(np.array(black_pieces) + size + 1 == a )[0]) for a in white_pieces if a % size != 0]).astype(int)

			black_take_left = [a for a in white_pieces if any(np.array(black_pieces) + size - 1 == a) and a % size != size-1]
			black_left_piece = np.concatenate([list(np.where(np.array(black_pieces) + size - 1 == a )[0]) for a in white_pieces if a % size != size-1]).astype(int)

			forward = list(zip(black_forward_piece,black_forward))
			right = list(zip(black_right_piece,black_take_right))
			left = list(zip(black_left_piece,black_take_left))
			return np.concatenate((forward, right, left))


		else:
			white_forward = [a for a in free_spaces if any(np.array(white_pieces) - size == a)] 
			white_forward_piece = np.concatenate([list(np.where(np.array(white_pieces) + size == a)[0]) for a in free_spaces]).astype(int)

			white_take_right = [a for a in black_pieces if any(np.array(white_pieces) - size + 1 == a) and a % size != 0] 
			white_right_piece = np.concatenate([list(np.where(np.array(white_pieces) - size + 1 == a )[0]) for a in black_pieces if a % size != 0]).astype(int)

			white_take_left = [a for a in black_pieces if any(np.array(white_pieces) - size - 1 == a) and a % size != size-1] 
			white_left_piece = np.concatenate([list(np.where(np.array(white_pieces) - size - 1 == a )[0]) for a in black_pieces if a % size != size-1]).astype(int)

			forward = list(zip(white_forward_piece,white_forward))
			right = list(zip(white_right_piece,white_take_right))
			left = list(zip(white_left_piece,white_take_left))

			return np.concatenate((forward, right, left))
	
	def copy_board(board):
		return [[sq for sq in row] for row in board]

	def step(board, action, piece):
		board = HexaPawn.copy_board(board)
		size = len(board[0])
		board[int(action[0] / size)][action[0] % size] = '*'
		board[int(action[1] / size)][action[1] % size] = piece

		return HexaPawn.state(board)

	def play(self, games = 1):
		for g in range(games):
			self.reset()
			reward = None
			while reward is None:
				for player in self.players:
					action = player.action(HexaPawn.state(self.board))
					self.board = HexaPawn.step(self.board, action)
					reward = HexaPawn.reward(self.board)
					if reward is not None:
						break

			if reward > 0:
				if player is self.players[0]:
					player.wins_first += 1
					for p in self.players:
						if p is not player:
							p.losses_second += 1
				else:
					player.wins_second += 1
					for p in self.players:
						if p is not player:
							p.losses_first += 1
			else:
				self.players[0].draws_first += 1
				for p in self.players[1:]:
					p.draws_second += 1

	def state(board):
		# if board == None:
		# 	board = TicTacToe.copy_board(board)
		return tuple([tuple(row) for row in HexaPawn.copy_board(board)])

	def reset(self):
		self.board = [['B' for s in range(self.size)]]
		for s in range(self.size-2):
			self.board += [['*' for s in range(self.size)]]
		self.board += [['W' for s in range(self.size)]]
		random.shuffle(self.players)

		

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