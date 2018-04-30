import numpy as np
import random
import pickle
import matplotlib.pyplot as plt
from Agents import Learner


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

	'''
	Liar's Dice
	'''

	"""docstring for LiarsDice

	State: 3-tuple (my_roll, opponent_dice, prev_bids)
	where
	my_roll is a d-tuple of ints where d is the number of dice I have and each int is a die I have
	opponent_dice is an n-tuple of ints where n is the number of opponents and each int is each opponent's number of dice
	prev_bids is a b-tuple of bids (2-tuples) where b is the number of previous bids since I last acted

	Actions: 2-tuple bid (quantity, face value) or 'challenge'
	"""
	def __init__(self, players, dice = 5, bids = 1, virtual_number = 10):
		# self.num_opponents = num_opponents
		# self.num_dice = num_dice
		# self.num_agents = num_agents
		# self.num_players = num_agents + num_opponents
		# self.player_dice_num = [num_dice for _, in self.num_players]
		# self.dice = [np.random.randInt(1,num_dice) for _ in self.num_players]
		# self.turn = np.random.randInt(num_players)

		for p in players:
			if type(p) == Learner:
				LiarsDice.virtual_number = max(p.playouts / 100,virtual_number)
			else:
				LiarsDice.virtual_number = virtual_number


		self.dice = dice
		# self.players = [{'player' : p, 'dice' : self.dice, 'roll' : ()} for p in players]
		self.order = [p for p in players]
		LiarsDice.PLAYERS = len(self.order)
		LiarsDice.BIDS = min(bids,LiarsDice.PLAYERS-1)
		
		self.reset()

		# results for this game
		for player in self.players:
			# player[0].wins_first = 0
			# player[0].wins_second = 0
			# player[0].losses_first = 0
			# player[0].losses_second = 0
			# player[0].draws_first = 0
			# player[0].draws_second = 0
			player.get('player').wins = [0]*LiarsDice.PLAYERS
			player.get('player').losses = [0]*LiarsDice.PLAYERS
			player.get('player').draws = [0]*LiarsDice.PLAYERS

	def reward(state, game = None):
		my_roll, opp_dice, prev_bids = state
		if prev_bids[-1] is not 'challenge':
			return None

		bid = prev_bids[-2]

		# REWARD called externally
		if game == None:
			# evaluate using temporary players
			count = [die for player in LiarsDice.temp_players for die in player.get('roll')].count(bid[1])
			# every so often
			LiarsDice.temp_count += 1
			if LiarsDice.temp_count >= LiarsDice.virtual_number:
				# reset temporary players
				LiarsDice.temp_players = None
			# return reward
			if count >= bid[0]:
				return -1
			else:
				return 1
		else: # REWARD called internally
			count = [die for player in game.players for die in player.get('roll')].count(bid[1])
			# give reward for actual game
			if count >= bid[0]:
				# decrement dice
				game.players[-1]['dice'] -= 1
				# update losses
				if game.players[-1].get('dice') == 0:
					game.players[-1].get('player').losses[game.order.index(game.players[-1].get('player'))] += 1
				# go back 1 player
				game.players = [game.players[-1]] + game.players[0:-1]
			else:
				# decrement dice
				game.players[-2]['dice'] -= 1
				# update losses
				if game.players[-1].get('dice') == 0:
					game.players[-1].get('player').losses[game.order.index(game.players[-1].get('player'))] += 1
				# go back 2 players
				game.players = game.players[-2:] + game.players[0:-2]
			# eliminate players with no dice
			game.players = [p for p in game.players if p.get('dice') > 0]
			# check if someone won
			# if len(game.players) == 1:
			# 	game.players[-1].get('player').wins[game.order.index(game.players[-1].get('player'))] += 1
			# 	return 1
			# else:
			# 	game.next_round()
			game.next_round()
			return 1

	def legal_actions(state):
		my_roll, opponent_dice, prev_bids = state
		max_bid = [len(my_roll) + sum(opponent_dice), 6]

		if prev_bids == ():
			return [(quantity, value) for quantity, value in LiarsDice.all_legal_bids(max_bid)]
		else:
			return [(quantity, value) for quantity, value in LiarsDice.all_legal_bids(max_bid) if quantity > prev_bids[-1][0] or (quantity == prev_bids[-1][0] and value > prev_bids[-1][1])] + ['challenge']

	def step(state, action, game = None):
		my_roll, opp_dice, prev_bids = state
		# print('PREV BIDS',prev_bids)
		# STEP called externally
		if game == None:
			# if temporary players don't exist or my_roll isn't in the temporary players
			# print(str(LiarsDice.temp_players))
			if LiarsDice.temp_players == None or all(p.get('roll') is not my_roll for p in LiarsDice.temp_players):
				# create them
				# print('created new players')
				LiarsDice.temp_players = [{'roll' : my_roll, 'dice' : len(my_roll)}] + [{'roll' : LiarsDice.roll(dice), 'dice' : dice} for dice in opp_dice]
				LiarsDice.temp_count = 0
			# step the virtual game
			# find turn
			turn = next(i for i,p in enumerate(LiarsDice.temp_players) if p.get('roll') is my_roll)
			# change turn
			turn += 1
			turn %= LiarsDice.PLAYERS
			# print('turn:',turn)
			# LiarsDice.temp_players = LiarsDice.temp_players[1:] + [LiarsDice.temp_players[0]]
			# change order
			LiarsDice.temp_players = LiarsDice.temp_players[turn:] + LiarsDice.temp_players[0:turn]
			# next state
			my_roll = LiarsDice.temp_players[0].get('roll')
			opp_dice = tuple(player.get('dice') for player in LiarsDice.temp_players[1:])
			if action == 'challenge':
				return (my_roll, opp_dice, prev_bids + (action,))
			prev_bids += (action,)
			return (my_roll, opp_dice, prev_bids[-LiarsDice.BIDS:])
		else: # STEP called internally
			# step the actual game 
			# change turn
			game.players = game.players[1:] + [game.players[0]]
			my_roll = game.players[0].get('roll')
			opp_dice = tuple(player.get('dice') for player in game.players[1:])
			if action is 'challenge':
				return (my_roll, opp_dice, prev_bids + (action,))
			elif prev_bids == ():
				prev_bids = (action,)
			else:
				prev_bids += (action,)
			return (my_roll, opp_dice, prev_bids[-LiarsDice.BIDS:])

	def play(self, games = 1):
		for g in range(games):
			print('Game',g)
			self.reset()

			while len(self.players) > 1:

				# inital state
				my_roll = self.players[0].get('roll')
				opp_dice = tuple(player.get('dice') for player in self.players[1:])
				prev_bids = ()
				state = (my_roll, opp_dice, prev_bids)
				# print(state)

				reward = None
				while reward is None:
					action = self.players[0].get('player').action(state)
					state = LiarsDice.step(state,action,self)
					reward = LiarsDice.reward(state,self)

			self.players[-1].get('player').wins[self.order.index(self.players[-1].get('player'))] += 1
			print(self.players[-1].get('player').name + ' wins!')

	def reset(self):
		random.shuffle(self.order)
		self.players = [{'player' : p, 'dice' : self.dice, 'roll' : LiarsDice.roll(self.dice)} for p in self.order]
		LiarsDice.temp_players = None
		# for p in self.order:
		# 	p['dice'] = self.dice
		# 	p['roll'] = self.roll(self.dice)

	def next_round(self):
		LiarsDice.temp_players = None
		for p in self.players:
			p['roll'] = LiarsDice.roll(p.get('dice'))

	def display(state):
		my_roll, opp_dice, prev_bids = state
		print('\nYour dice: ' + ' '.join(str(r) for r in my_roll))
		print('\nOpponents:')
		for i in range(len(opp_dice)):
			if i >= len(opp_dice) - len(prev_bids):
				print('Dice:',opp_dice[i],'Bid:',prev_bids[i - (len(opp_dice) - len(prev_bids))])
			else:
				print('Dice:',opp_dice[i])

	def __str__(self):
		pass

	def roll(dice):
		return tuple(sorted(random.choice(range(1,6+1)) for d in range(dice)))

	def all_legal_bids(max_bid):
		for quantity in range(1,max_bid[0]+1):
			for value in range(1,6 + 1):
				bid = (quantity, value)
				if bid == max_bid:
					StopIteration
				yield (quantity, value)
		
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

	def reward(board):
		board = HexaPawn.copy_board(board)
		size = len(board[0])
		if any(sq == 'W' for sq in board[0]): # white at the end
			return 1
		if any(sq == 'B' for sq in board[len(board)-1]): # black at the end
			return 1
		if len(HexaPawn.legal_actions(board)) == 0: # no legal moves
			return 1
		if not any(sq == 'W' for sq in flatten(board)): # no white pawns
			return 1
		if not any(sq == 'B' for sq in flatten(board)): # no black pawns
			return 1
		return None

	def determine_turn(board):
		size = len(board)
		x = np.linspace(0, size-1, size)
		y = np.linspace(0, size-1, size)
		_, black_energy = np.meshgrid(x, y)

		x = np.linspace(size-1, 0, size)
		y = np.linspace(size-1, 0, size)
		_, white_energy = np.meshgrid(x, y)

		black_energy = flatten(black_energy)
		white_energy = flatten(white_energy)


		black_tot = sum([black_energy[n] for n,s in enumerate(flatten(board)) if s == 'B'])
		white_tot = sum([white_energy[n] for n,s in enumerate(flatten(board)) if s == 'W'])
		black_pieces = [n for n,s in enumerate(flatten(board)) if s == 'B']
		white_pieces = [n for n,s in enumerate(flatten(board)) if s == 'W']
		if len(white_pieces) == 0:
			return 'W'
		if len(black_pieces) == 0:
			return 'B'
		if white_tot/len(white_pieces) > black_tot/len(black_pieces):
			return 'B'
		else:
			return 'W'

	def legal_actions(board):
		board = HexaPawn.copy_board(board)
		cur_piece = HexaPawn.determine_turn(board)
		free_spaces = [n for n,s in enumerate(flatten(board)) if s == '*']
		black_pieces = [n for n,s in enumerate(flatten(board)) if s == 'B']
		white_pieces = [n for n,s in enumerate(flatten(board)) if s == 'W']
		size = len(board[0])
		if cur_piece == 'B': 
			play_forward = [a for a in free_spaces if any(np.array(black_pieces) + size == a)] 
			black_forward_piece = [list(np.array(black_pieces)[np.array(black_pieces) + size == a]) for a in free_spaces]

			forward_pieces = []
			for p in black_forward_piece:
				forward_pieces += p

			take_right = [a for a in white_pieces if any(np.array(black_pieces) + size + 1 == a) and a % size != 0] 
			black_right_piece = [list(np.array(black_pieces)[np.array(black_pieces) + size + 1 == a ]) for a in white_pieces if a % size != 0]
			
			right_pieces = []
			for p in black_right_piece:
				right_pieces += p

			take_left = [a for a in white_pieces if any(np.array(black_pieces) + size - 1 == a) and a % size != size-1]
			black_left_piece = [list(np.array(black_pieces)[np.array(black_pieces) + size - 1 == a ]) for a in white_pieces if a % size != size-1]
			
			left_pieces = []
			for p in black_left_piece:
				left_pieces += p

			


		else:

			play_forward = [a for a in free_spaces if any(np.array(white_pieces) - size == a)] 
			white_forward_piece = [list(np.array(white_pieces)[np.array(white_pieces) - size == a]) for a in free_spaces]

			forward_pieces = []
			for p in white_forward_piece:
				forward_pieces += p

			take_right = [a for a in black_pieces if any(np.array(white_pieces) - size + 1 == a) and a % size != 0] 
			white_right_piece = [list(np.array(white_pieces)[np.array(white_pieces) - size + 1 == a]) for a in black_pieces if a % size != 0]

			right_pieces = []
			for p in white_right_piece:
				right_pieces += p

			take_left = [a for a in black_pieces if any(np.array(white_pieces) - size - 1 == a) and a % size != size-1] 
			white_left_piece = [list(np.array(white_pieces)[np.array(white_pieces) - size - 1 == a ]) for a in black_pieces if a % size != size-1]

			left_pieces = []
			for p in white_left_piece:
				left_pieces += p

		forward = list(zip(forward_pieces,play_forward))
		right = list(zip(right_pieces,take_right))
		left = list(zip(left_pieces,take_left))

		return forward + right + left
	
	def copy_board(board):
		return [[sq for sq in row] for row in board]

	def step(board, action):
		board = HexaPawn.copy_board(board)
		size = len(board[0])
		piece = board[int(action[0] / size)][action[0] % size]
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