import numpy as np


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
		self.num_players = num_agents+num_opponents
		self.player_dice_num = [num_dice for _, in self.num_players]
		self.dice = [np.random.randInt(1,num_dice) for _ in self.num_players]
		self.turn = np.random.randInt(num_players)

		self.state = [self.turn, ]


	def step(self, action):
		nxt_state 
		
