import numpy as np
import random


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

	"""docstring for LiarsDice"""
	def __init__(self, num_agents, num_opponents, num_dice):
		self.num_opponents = num_opponents
		self.num_dice = num_dice
		self.num_agents = num_agents
		self.num_players = num_agents + num_opponents
		self.player_dice_num = [num_dice for _, in self.num_players]
		self.dice = [np.random.randInt(1,num_dice) for _ in self.num_players]
		self.turn = np.random.randInt(num_players)

		self.state = [self.turn, ]


	def step(self, action):
		nxt_state 
		
class TicTacToe(object):

	"""docstring for TicTacToe"""
	def __init__(self, agent, opponent, size = 3):
		self.size = 3
		self.board = [['*' for c in range(size)] for r in range(size)]
		self.players = random.shuffle([agent,opponent])

	def done(self):
		# ROW
		if any(all(sq == 'x' for sq in row) or all(sq == 'o' for sq in row) for row in self.board): # row
			return True
		# COLUMN
		if any(all(row[c] == 'x' for row in self.board) or all(row[c] == 'o' for row in self.board) for c in range(self.size)): # column
			return True
		# DIAGONAL DOWN RIGHT
		if all(self.board[n][n] == 'x' for n in range(self.size)) or all(self.board[n][n] == 'o' for n in range(self.size)):
			return True
		# DIAGONAL UP RIGHT
		z = zip(list(range(self.size)),list(range(self.size-1,-1,-1)))
		if all(self.board[r][c] == 'x' for r,c in z) or all(self.board[r][c] == 'o' for r,c in z):
			return True
		return False

	def legal_actions(self):
		return [n for n,s in enumerate(flatten(self.board)) if s == '*']

	def play(self):
		while True:
			for player in self.players:
				action = player.action(self.state, self.legal_actions)

	def display(self):
		print(self.__str__())

	def __str__(self):
		return '\n'.join([' '.join(self.board[r]) for r in range(self.size)])

class RandomAgent(object):

	"""docstring for RandomAgent"""
	def __init__(self, num_states, num_actions):
		self.num_actions = num_actions

	def action(self, state, legal_actions):
		# return random.randrange(num_actions)
		return random.choice(legal_actions)

	def update(self, state, action, reward):
		pass

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