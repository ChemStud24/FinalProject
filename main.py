from Games import *
from Agents import *
import matplotlib.pyplot as plt



# env = HexPawn2(None, None)
# print(env.board)
# env.pawn_locations = [[(1,0),(0,1),(0,2)],[(2,0),(2,1),(2,2)]]
# print(env.legal_actions(None))

num_games = 50

game = TicTacToe(size = 3)
players = [Learner( game), RandomAgent( game)]
games_won = [0,0]
ties = 0
for _ in range(num_games):
	state,turn = game.initialize()
	print('Player: ', turn, ' is starting')

	while True:
		if len(game.legal_actions()) > 0:
			action = players[turn].action(game.state())
			game.board  = game.step(game.board, action)
			print(game)
			reward = game.reward(None)
			print('Reward: ', reward,'Turn: ', turn)
			if reward > 0:
				games_won[turn] += 1
				turn = (turn + 1) % 2
				break
			turn = (turn + 1) % 2

		else:
			ties += 1
			break

	print(games_won, ties)




